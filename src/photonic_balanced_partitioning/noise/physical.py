"""Bounded pure-internal-state interference and independent detection losses.

Inputs contain at most one photon per occupied spatial mode. Detectors do not
resolve the normalized pure internal states, whose Gram matrix is S[a,b] =
<phi_a|phi_b>. U has output rows and input columns. All Fock outcomes, collisions
and loss sectors are retained. See docs/NOISE_MODEL.md for the derivation.

Returned numbers are float64 estimates, not interval-certified probabilities.
No probability renormalization, postselection, fitted device parameter or QPU
access is performed. Runtime guards deliberately exclude large experiments.
"""
from __future__ import annotations

from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations_with_replacement, permutations, product
import math
from numbers import Integral
from types import MappingProxyType

import numpy as np

Occupation = tuple[int, ...]
MAX_EXACT_PHOTONS = 5
MAX_EXACT_MODES = 32
DEFAULT_MAX_TERMS = 2_000_000
_VALIDATION_ATOL = 1e-10
_PROBABILITY_ATOL = 1e-10


@dataclass(frozen=True)
class FockDistribution(Mapping[Occupation, float]):
    """Full outcome mapping with explicit floating-point diagnostics.

    Only negative roundoff within 1e-10 is clipped to zero, with its total mass
    recorded. Positive entries are never rescaled or discarded. raw_total is
    measured before clipping at the current stage; clipped mass includes any
    upstream FockDistribution corrections. These are diagnostics, not rigorous
    error bars. Use sum(result.values()) to inspect the returned total.
    """

    probabilities: Mapping[Occupation, float]
    raw_total_probability: float
    minimum_raw_probability: float
    roundoff_clipped_mass: float = 0.0
    maximum_imaginary_residual: float = 0.0
    numerical_semantics: str = "FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED"

    def __getitem__(self, state: Occupation) -> float:
        return self.probabilities[state]

    def __iter__(self) -> Iterator[Occupation]:
        return iter(self.probabilities)

    def __len__(self) -> int:
        return len(self.probabilities)

    def sector_probabilities(self) -> dict[int, float]:
        """Unconditioned probability mass by detected photon number."""
        sectors: dict[int, float] = {}
        for state, probability in self.items():
            sectors[sum(state)] = sectors.get(sum(state), 0.0) + probability
        return dict(sorted(sectors.items()))


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _work_budget(value: int) -> int:
    value = _positive_integer(value, "max_terms")
    if value > DEFAULT_MAX_TERMS:
        raise ValueError(f"max_terms may not exceed the hard limit {DEFAULT_MAX_TERMS}")
    return value


def _distribution(
    probabilities: Mapping[Occupation, float], *, upstream_clipped: float = 0.0,
    imaginary_residual: float = 0.0,
) -> FockDistribution:
    raw_total = math.fsum(probabilities.values())
    minimum = min(probabilities.values())
    if (not all(math.isfinite(p) for p in probabilities.values())
            or minimum < -_PROBABILITY_ATOL
            or abs(raw_total - 1.0) > _PROBABILITY_ATOL
            or imaginary_residual > _PROBABILITY_ATOL):
        raise ArithmeticError("Full distribution failed positivity, reality or normalization")
    clipped = -math.fsum(p for p in probabilities.values() if p < 0.0)
    return FockDistribution(
        MappingProxyType({state: max(0.0, p) for state, p in probabilities.items()}),
        raw_total, minimum, upstream_clipped + clipped, imaginary_residual,
    )


def validate_internal_gram(gram: np.ndarray, photons: int) -> np.ndarray:
    """Validate pure-state internal overlaps, without projecting or rescaling.

    Any Hermitian PSD matrix with diagonal one is a Gram matrix of normalized
    pure vectors. This is not a model for arbitrary mixed/correlated photons.
    """
    if (isinstance(photons, bool) or not isinstance(photons, Integral)
            or photons < 0):
        raise ValueError("photons must be a nonnegative integer")
    s = np.asarray(gram, dtype=complex)
    if s.shape != (photons, photons) or not np.isfinite(s).all():
        raise ValueError("Internal Gram matrix must be finite with shape (photons, photons)")
    if not np.allclose(s, s.conj().T, atol=_VALIDATION_ATOL, rtol=0):
        raise ValueError("Internal Gram matrix must be Hermitian")
    if not np.allclose(np.diag(s), 1.0, atol=_VALIDATION_ATOL, rtol=0):
        raise ValueError("Internal Gram matrix must have diagonal one")
    if photons and np.linalg.eigvalsh(s).min() < -_VALIDATION_ATOL:
        raise ValueError("Internal Gram matrix must be positive semidefinite")
    return s.copy()


def gram_from_internal_states(states: np.ndarray) -> np.ndarray:
    """Rows are normalized pure internal vectors; no normalization is applied."""
    states = np.asarray(states, dtype=complex)
    if states.ndim != 2 or not np.isfinite(states).all() or states.shape[1] < 1:
        raise ValueError("Internal states must be a finite (photons, dimension) matrix")
    s = states.conj() @ states.T
    return validate_internal_gram(s, len(states))


def partial_distinguishability_distribution(
    unitary: np.ndarray,
    input_modes: Sequence[int],
    internal_gram: np.ndarray | None = None,
    *,
    max_terms: int = DEFAULT_MAX_TERMS,
) -> FockDistribution:
    """Full number-resolved probabilities for distinct singly occupied inputs.

    None means all internal states coincide (S is the all-ones matrix); identity
    means fully distinguishable. The double permutation sum costs
    C(m+k-1,k)*(k!)^2 terms. k<=5 and max_terms are checked before enumeration.
    Vacuum is supported with input_modes=() and a 0-by-0 Gram matrix.
    """
    budget = _work_budget(max_terms)
    u = np.asarray(unitary, dtype=complex)
    if (u.ndim != 2 or u.shape[0] != u.shape[1] or u.shape[0] < 1
            or not np.isfinite(u).all()):
        raise ValueError("unitary must be a finite nonempty square matrix")
    m = len(u)
    if m > MAX_EXACT_MODES:
        raise ValueError(f"Exact noise calculation supports at most {MAX_EXACT_MODES} modes")
    if not np.allclose(u.conj().T @ u, np.eye(m), atol=_VALIDATION_ATOL, rtol=0):
        raise ValueError("unitary must be unitary; apply losses as a separate channel")
    modes = tuple(input_modes)
    if (any(isinstance(a, bool) or not isinstance(a, Integral) or not 0 <= a < m
            for a in modes) or len(set(modes)) != len(modes)):
        raise ValueError("input_modes must be distinct integer mode indices; bunched inputs unsupported")
    k = len(modes)
    if k > MAX_EXACT_PHOTONS:
        raise ValueError(f"Exact noise calculation supports at most {MAX_EXACT_PHOTONS} photons")
    terms = math.comb(m + k - 1, k) * math.factorial(k) ** 2
    if terms > budget:
        raise ValueError(f"Exact distribution needs {terms} permutation pairs, exceeding max_terms={budget}")
    s = validate_internal_gram(np.ones((k, k)) if internal_gram is None else internal_gram, k)
    if k == 0:
        return _distribution({(0,) * m: 1.0})
    orders = np.array(list(permutations(range(k))), dtype=int)
    # First axis sigma, second tau: <phi_tau(j)|phi_sigma(j)> = S[tau,sigma].
    weights = np.prod(s[orders[None, :, :], orders[:, None, :]], axis=2)
    columns = np.asarray(modes)[orders]
    probabilities: dict[Occupation, float] = {}
    max_imaginary = 0.0
    for rows in combinations_with_replacement(range(m), k):
        occupation = tuple(int(c) for c in np.bincount(rows, minlength=m))
        amplitudes = np.prod(u[np.asarray(rows)[None, :], columns], axis=1)
        probability = np.einsum("s,st,t->", amplitudes, weights, amplitudes.conj())
        probability /= math.prod(math.factorial(c) for c in occupation)
        max_imaginary = max(max_imaginary, abs(float(probability.imag)))
        probabilities[occupation] = float(probability.real)
    return _distribution(probabilities, imaginary_residual=max_imaginary)


def apply_independent_loss(
    distribution: Mapping[Occupation, float],
    eta: float | Sequence[float],
    *,
    max_terms: int = DEFAULT_MAX_TERMS,
) -> FockDistribution:
    """Independent per-photon detection loss after the interferometer.

    eta is a common survival probability, or a vector of output-mode survival
    probabilities. The latter is a post-interferometer channel and must not be
    commuted through U. The input mapping must already be normalized and include
    all its physical sectors, not a subnormalized CF-only selection.
    """
    budget = _work_budget(max_terms)
    if not isinstance(distribution, Mapping) or not distribution or len(distribution) > budget:
        raise ValueError("Expected a nonempty bounded full outcome mapping")
    first = next(iter(distribution))
    if not isinstance(first, tuple) or not first:
        raise ValueError("Occupations must be nonempty tuples")
    m = len(first)
    if m > MAX_EXACT_MODES:
        raise ValueError(f"Loss calculation supports at most {MAX_EXACT_MODES} modes")
    for state, probability in distribution.items():
        if (not isinstance(state, tuple) or len(state) != m
                or any(isinstance(n, bool) or not isinstance(n, Integral) or n < 0 for n in state)):
            raise ValueError("Occupations must have a common length and nonnegative integer entries")
        if sum(state) > MAX_EXACT_PHOTONS:
            raise ValueError(f"Loss calculation supports at most {MAX_EXACT_PHOTONS} photons")
        if (not np.isscalar(probability) or np.iscomplexobj(probability)
                or not math.isfinite(float(probability)) or probability < 0):
            raise ValueError("Input probabilities must be finite nonnegative real numbers")
    if abs(math.fsum(distribution.values()) - 1.0) > _PROBABILITY_ATOL:
        raise ValueError("Input distribution must be normalized; postselection is not implicit")
    survival = np.asarray(eta)
    if np.iscomplexobj(survival):
        raise ValueError("eta must be real")
    survival = np.asarray(survival, dtype=float)
    if survival.ndim == 0:
        survival = np.full(m, float(survival))
    if (survival.shape != (m,) or not np.isfinite(survival).all()
            or np.any(survival < 0) or np.any(survival > 1)):
        raise ValueError("eta must be in [0,1], either scalar or one value per output mode")
    needed = sum(math.prod(n + 1 for n in state) for state in distribution)
    if needed > budget:
        raise ValueError(f"Loss channel needs {needed} thinning terms, exceeding max_terms={budget}")
    output: dict[Occupation, float] = {}
    for state, probability in distribution.items():
        factors = [
            [math.comb(n, r) * float(e) ** r * (1 - float(e)) ** (n - r) for r in range(n + 1)]
            for n, e in zip(state, survival)
        ]
        for detected in product(*(range(n + 1) for n in state)):
            weight = math.prod(factors[i][r] for i, r in enumerate(detected))
            output[detected] = output.get(detected, 0.0) + float(probability) * weight
    return _distribution(
        output, upstream_clipped=getattr(distribution, "roundoff_clipped_mass", 0.0),
        imaginary_residual=getattr(distribution, "maximum_imaginary_residual", 0.0),
    )


def noisy_distribution(
    unitary: np.ndarray,
    input_modes: Sequence[int],
    internal_gram: np.ndarray | None = None,
    *,
    eta: float | Sequence[float] = 1.0,
    max_terms: int = DEFAULT_MAX_TERMS,
) -> FockDistribution:
    """Compose the pure-internal-state distribution with independent loss."""
    ideal = partial_distinguishability_distribution(
        unitary, input_modes, internal_gram, max_terms=max_terms,
    )
    return apply_independent_loss(ideal, eta, max_terms=max_terms)
