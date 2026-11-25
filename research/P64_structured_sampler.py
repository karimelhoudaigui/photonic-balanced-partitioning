"""Prospective P64 complete, fixed-phase sampler; rounded conditional state.

No graph, optimizer, backend, QPU or automatic experiment is imported here.
Source and local transition coefficients are exact in Z[xi], xi**2=xi-1.
Conditioning and trigonometry are floating and explicitly *not* certified TV.
All construction/cache/RNG/phase work belongs inside a caller's paid boundary.
"""
from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable, Protocol

Pair = tuple[int, int]
Occupation = tuple[int, ...]
State = dict[tuple[tuple[int, int, int], ...], complex]
MASS_TOLERANCE = 2e-10
REFERENCE_ABSOLUTE_TOLERANCE = 2e-11
SMALL_LAW_TV_TOLERANCE = 2e-9
MAX_SOURCE_SUPPORT = {2: 2, 6: 80}
MAX_TRANSITION_ENTRIES = 2 * 7**3 * 190
XI_POWERS: tuple[Pair, ...] = (
    (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)
)


class NumericalFailure(ArithmeticError):
    """Retain the first failure; never prune, retry, clip or relax tolerances."""


class RandomInterface(Protocol):
    def randrange(self, stop: int) -> int: ...
    def random(self) -> float: ...


def add(a: Pair, b: Pair) -> Pair:
    return a[0] + b[0], a[1] + b[1]


def multiply(a: Pair, b: Pair) -> Pair:
    return a[0] * b[0] - a[1] * b[1], (
        a[0] * b[1] + a[1] * b[0] + a[1] * b[1]
    )


def scale(a: Pair, n: int) -> Pair:
    return a[0] * n, a[1] * n


def norm(a: Pair) -> int:
    return a[0]**2 + a[0] * a[1] + a[1]**2


def as_complex(a: Pair) -> complex:
    return complex(a[0] + a[1] / 2, a[1] * math.sqrt(3) / 2)


def occupations(total: int, modes: int) -> Iterable[Occupation]:
    if total < 0 or modes < 1:
        raise ValueError("nonnegative total and positive modes required")
    if modes == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in occupations(total - first, modes - 1):
                yield (first,) + tail


def factorial_product(n: Occupation) -> int:
    return math.prod(math.factorial(x) for x in n)


def polynomial_step(poly: dict[Occupation, Pair], column: tuple[Pair, ...]):
    """Multiply by one unnormalized linear creation polynomial, exactly."""
    result: dict[Occupation, Pair] = {}
    for n, coefficient in poly.items():
        for mode, entry in enumerate(column):
            next_n = n[:mode] + (n[mode] + 1,) + n[mode + 1:]
            result[next_n] = add(result.get(next_n, (0, 0)),
                                 multiply(coefficient, entry))
    return result


def require_mass(value: float, target: float = 1.0) -> None:
    if not math.isfinite(value) or abs(value - target) > MASS_TOLERANCE:
        raise NumericalFailure(f"mass drift: observed={value!r}, target={target!r}")


def squared(z: complex) -> float:
    answer = z.real * z.real + z.imag * z.imag
    if not math.isfinite(answer) or answer < 0:
        raise NumericalFailure("negative or nonfinite Born mass")
    return answer


def draw_probabilities(weights: list[float], rng: RandomInterface) -> int:
    """Explicit monitored normalization; no discarded outcome or CDF fallback.

    This uses a finite-bit uniform float and rounded arithmetic. It is not an
    exact-real categorical operation or a certified total-variation bound.
    """
    if not weights or any(not math.isfinite(w) or w < 0 for w in weights):
        raise NumericalFailure("invalid categorical weights")
    mass = math.fsum(weights)
    require_mass(mass)
    quantile = rng.random()
    if not math.isfinite(quantile) or not 0 <= quantile < 1:
        raise NumericalFailure("invalid RNG quantile")
    cdf = [math.fsum(weights[:index + 1]) / mass
           for index in range(len(weights))]
    if cdf[-1] != 1.0 or any(a > b for a, b in zip(cdf, cdf[1:])):
        raise NumericalFailure("unusable categorical CDF")
    selected = bisect_right(cdf, quantile)
    if selected >= len(weights) or weights[selected] <= 0:
        raise NumericalFailure("CDF selected an inaccessible outcome")
    return selected


@dataclass(frozen=True)
class SourceRow:
    occupation: Occupation
    coefficient: Pair
    weight: int
    amplitude: complex


class FourierSource:
    """All F_d |1**d> outcomes, including exact zeros, for d=2 or6 only."""

    def __init__(self, d: int):
        if d not in MAX_SOURCE_SUPPORT:
            raise ValueError("qualification restricted to d=2 or d=6")
        self.d = d
        poly = {(0,) * d: (1, 0)}
        for column in range(d):
            entries = tuple(XI_POWERS[(6 // d * row * column) % 6]
                            for row in range(d))
            poly = polynomial_step(poly, entries)
        self.denominator = d**d
        self.rows = tuple(
            SourceRow(n, poly.get(n, (0, 0)),
                      factorial_product(n) * norm(poly.get(n, (0, 0))),
                      as_complex(poly.get(n, (0, 0))) *
                      math.sqrt(factorial_product(n) / self.denominator))
            for n in occupations(d, d)
        )
        if sum(row.weight for row in self.rows) != self.denominator:
            raise NumericalFailure("exact Fourier source normalization failed")
        self.support = tuple(row for row in self.rows if row.weight != 0)
        if not 0 < len(self.support) <= MAX_SOURCE_SUPPORT[d]:
            raise NumericalFailure("exact source support bound violated")
        if any(sum(i * n for i, n in enumerate(row.occupation)) % d
               for row in self.support):
            raise NumericalFailure("exact source suppression rule violated")
        self.lookup = {row.occupation: row for row in self.support}
        running = 0
        cdf = []
        for row in self.support:
            running += row.weight
            cdf.append(running)
        self.integer_cdf = tuple(cdf)

    def draw(self, rng: RandomInterface) -> Occupation:
        rank = rng.randrange(self.denominator)
        if type(rank) is not int or not 0 <= rank < self.denominator:
            raise NumericalFailure("invalid integer RNG rank")
        return self.support[bisect_right(self.integer_cdf, rank)].occupation

    def sample_totals(self, rng: RandomInterface) -> Occupation:
        # Latent rows are immediately discarded; they are not an initial state.
        return tuple(map(sum, zip(*(self.draw(rng) for _ in range(3)))))


def raw_tritter(mixed: bool) -> tuple[tuple[Pair, ...], ...]:
    fourier = tuple(tuple(XI_POWERS[(2 * a * b) % 6] for b in range(3))
                    for a in range(3))
    if not mixed:
        return fourier
    return (
        tuple(add(scale(fourier[0][b], 3), scale(fourier[1][b], -4))
              for b in range(3)),
        tuple(add(scale(fourier[0][b], 4), scale(fourier[1][b], 3))
              for b in range(3)),
        tuple(scale(fourier[2][b], 5) for b in range(3)),
    )


@dataclass(frozen=True)
class TransitionColumn:
    outputs: tuple[Occupation, ...]
    coefficients: tuple[Pair, ...]
    amplitudes: tuple[complex, ...]
    norm_denominator: int


class TritterCache:
    """Lazy columns only: exact DP, full bunched-input Fock normalization."""

    def __init__(self, source_d: int):
        if source_d not in (2, 6):
            raise ValueError("unsupported source size")
        self.source_d = source_d
        self.columns: dict[tuple[bool, Occupation], TransitionColumn] = {}
        self.entries = 0

    def column(self, x: Occupation, mixed: bool) -> TransitionColumn:
        if len(x) != 3 or any(type(v) is not int or not 0 <= v <= self.source_d
                              for v in x):
            raise ValueError("input triplet outside source cube")
        key = mixed, x
        if key in self.columns:
            return self.columns[key]
        entries = raw_tritter(mixed)
        poly = {(0, 0, 0): (1, 0)}
        for b, multiplicity in enumerate(x):
            for _ in range(multiplicity):
                poly = polynomial_step(poly, tuple(entries[a][b] for a in range(3)))
        output = tuple(occupations(sum(x), 3))
        if self.entries + len(output) > MAX_TRANSITION_ENTRIES:
            raise NumericalFailure("transition logical entry guard exceeded")
        coefficients = tuple(poly.get(o, (0, 0)) for o in output)
        denominator = (75 if mixed else 3)**sum(x) * factorial_product(x)
        mass_numerator = sum(factorial_product(o) * norm(c)
                             for o, c in zip(output, coefficients))
        if mass_numerator != denominator:
            raise NumericalFailure("exact tritter Fock-column normalization failed")
        amplitudes = tuple(as_complex(c) * math.sqrt(factorial_product(o) / denominator)
                           for o, c in zip(output, coefficients))
        require_mass(math.fsum(map(squared, amplitudes)))
        result = TransitionColumn(output, coefficients, amplitudes, denominator)
        self.columns[key] = result
        self.entries += len(output)
        return result


class StructuredSampler:
    """Full fixed-Theta distribution, monitored rounded conditional arithmetic.

    Construction, conditional reconstruction, phases and cache misses are
    deliberately visible; callers must time/pay them, rather than just a draw.
    """

    def __init__(self, d: int = 6):
        self.source = FourierSource(d)
        self.cache = TritterCache(d)
        self.d = d
        self.max_width = MAX_SOURCE_SUPPORT[d]**2

    def conditional_state(self, totals: Occupation,
                          theta: tuple[tuple[float, ...], ...]) -> tuple[State, Fraction]:
        if (len(totals) != self.d or sum(totals) != 3 * self.d or
                any(type(v) is not int or v < 0 for v in totals)):
            raise ValueError("invalid color totals")
        if (len(theta) != 3 or any(len(row) != self.d for row in theta) or
                any(not math.isfinite(v) for row in theta for v in row)):
            raise ValueError("finite 3xd phase array required")
        state: State = {}
        integer_mass = 0
        for first in self.source.support:
            for second in self.source.support:
                third_n = tuple(m - a - b for m, a, b in
                                zip(totals, first.occupation, second.occupation))
                third = self.source.lookup.get(third_n)
                if third is None:
                    continue
                rows = first, second, third
                key = tuple(tuple(row.occupation[i] for row in rows)
                            for i in range(self.d))
                phase = math.fsum(theta[b][i] * rows[b].occupation[i]
                                  for b in range(3) for i in range(self.d))
                if not math.isfinite(phase):
                    raise NumericalFailure("phase accumulation overflow")
                state[key] = math.prod(row.amplitude for row in rows) * complex(
                    math.cos(phase), math.sin(phase))
                integer_mass += math.prod(row.weight for row in rows)
        if not state or integer_mass <= 0:
            raise NumericalFailure("zero-probability color total requested")
        if len(state) > self.max_width:
            raise NumericalFailure("conditional width guard exceeded")
        probability = Fraction(integer_mass, self.source.denominator**3)
        floating_mass = math.fsum(map(squared, state.values()))
        # Test a relative error before explicitly normalizing the rounded state.
        require_mass(floating_mass / float(probability))
        divisor = math.sqrt(floating_mass)
        return {key: amplitude / divisor for key, amplitude in state.items()}, probability

    def local_distribution(self, state: State, color: int):
        """Stream one suffix output vector; trace distinct suffixes incoherently."""
        if not state or not 0 <= color < self.d:
            raise ValueError("nonempty state and valid color required")
        require_mass(math.fsum(map(squared, state.values())))
        ordered = sorted(state.items(), key=lambda pair: pair[0][1:])
        total = sum(ordered[0][0][0])
        outputs = tuple(occupations(total, 3))
        probabilities = [0.0] * len(outputs)
        groups: list[list[tuple[Occupation, complex]]] = []
        suffixes = []
        for key, amplitude in ordered:
            if len(key) != self.d - color or sum(key[0]) != total:
                raise NumericalFailure("inconsistent current-sector state")
            suffix = key[1:]
            if not suffixes or suffix != suffixes[-1]:
                suffixes.append(suffix)
                groups.append([])
            groups[-1].append((key[0], amplitude))
        # Groups hold exactly one copy of each live amplitude, not R*D values.
        for group in groups:
            accumulated = [0j] * len(outputs)
            for x, amplitude in group:
                column = self.cache.column(x, mixed=(color == 0))
                if column.outputs != outputs:
                    raise NumericalFailure("tritter output ordering changed")
                for index, transition in enumerate(column.amplitudes):
                    accumulated[index] += amplitude * transition
            for index, amplitude in enumerate(accumulated):
                probabilities[index] += squared(amplitude)
        require_mass(math.fsum(probabilities))
        return outputs, probabilities, suffixes, groups

    def project(self, outputs, probabilities, suffixes, groups,
                chosen: int, color: int) -> State:
        if not 0 <= chosen < len(outputs) or probabilities[chosen] <= 0:
            raise NumericalFailure("projecting inaccessible local output")
        result = {}
        for suffix, group in zip(suffixes, groups):
            amplitude = sum((weight * self.cache.column(x, mixed=(color == 0)).amplitudes[chosen]
                             for x, weight in group), 0j)
            # Keep rounded/exact cancellation zeros; no threshold pruning.
            result[suffix] = amplitude / math.sqrt(probabilities[chosen])
        require_mass(math.fsum(map(squared, result.values())))
        return result

    def sample(self, theta: tuple[tuple[float, ...], ...],
               rng: RandomInterface) -> Occupation:
        totals = self.source.sample_totals(rng)
        state, _ = self.conditional_state(totals, theta)
        selected = []
        for color in range(self.d):
            outputs, probabilities, suffixes, groups = self.local_distribution(state, color)
            index = draw_probabilities(probabilities, rng)
            selected.append(outputs[index])
            state = self.project(outputs, probabilities, suffixes, groups, index, color)
        require_mass(math.fsum(map(squared, state.values())))
        counts = tuple(selected[i][a] for a in range(3) for i in range(self.d))
        if sum(counts) != 3 * self.d:
            raise NumericalFailure("output photon number changed")
        return counts

    def complete_small_law(self, theta: tuple[tuple[float, ...], ...]) -> dict[Occupation, float]:
        """Qualification ONLY: complete six-mode law; refused for d6/N18."""
        if self.d != 2:
            raise ValueError("complete enumeration allowed only for d2/N6")
        # No S^3 configuration table: enumerate the possible small total M.
        law = {n: 0.0 for n in occupations(6, 6)}
        for totals in occupations(6, 2):
            try:
                state, mass = self.conditional_state(totals, theta)
            except NumericalFailure as error:
                if str(error) == "zero-probability color total requested":
                    continue
                raise
            def descend(color, current, prefix, probability):
                if color == 2:
                    counts = tuple(prefix[i][a] for a in range(3) for i in range(2))
                    law[counts] += float(mass) * probability
                    return
                output, probs, suffixes, groups = self.local_distribution(current, color)
                for index, p in enumerate(probs):
                    if p == 0:
                        continue  # An exactly zero rounded branch, no threshold.
                    next_state = self.project(output, probs, suffixes, groups, index, color)
                    descend(color + 1, next_state, prefix + [output[index]], probability * p)
            descend(0, state, [], 1.0)
        require_mass(math.fsum(law.values()))
        return law
