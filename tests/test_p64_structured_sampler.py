"""Frozen P64 synthetic qualification; no graph or 18-photon random draw."""
import cmath
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import random
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p64_structured_candidate",
                                          ROOT / "research/P64_structured_sampler.py")
subject = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = subject
SPEC.loader.exec_module(subject)


@pytest.fixture(scope="session")
def evidence_directory(tmp_path_factory):
    requested = os.environ.get("P64_QUALIFICATION_ARTIFACT")
    directory = (Path(requested) if requested else
                 tmp_path_factory.getbasetemp() / "p64-evidence")
    directory.mkdir(parents=True, exist_ok=False)
    return directory


def _write_exclusive(path, artifact):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(artifact, stream, indent=2, allow_nan=False)
        stream.write("\n")


def _matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def _independent_six_mode_matrix(phi):
    # Direct dense factorization, independent of source/transition integer DP.
    source = [[0j] * 6 for _ in range(6)]
    middle = [[0j] * 6 for _ in range(6)]
    final = [[complex(i == j) for j in range(6)] for i in range(6)]
    for b, i, j in itertools.product(range(3), range(2), range(2)):
        source[2 * b + i][2 * b + j] = (-1)**(i * j) / math.sqrt(2)
    for a, b, i in itertools.product(range(3), range(3), range(2)):
        phase = phi if (b, i) == (1, 1) else 0
        middle[2 * a + i][2 * b + i] = cmath.exp(
            2j * math.pi * a * b / 3 + 1j * phase) / math.sqrt(3)
    final[0][0], final[0][2] = 3 / 5, -4 / 5
    final[2][0], final[2][2] = 4 / 5, 3 / 5
    return _matmul(final, _matmul(middle, source))


def _ryser_reference(matrix, n):
    # Full six-input Ryser formula, with output row repetition only.
    rows = [matrix[i] for i, count in enumerate(n) for _ in range(count)]
    permanent = 0j
    for mask in range(1, 1 << 6):
        columns = [j for j in range(6) if mask & (1 << j)]
        permanent += (-1)**(6 - len(columns)) * math.prod(
            sum(row[j] for j in columns) for row in rows)
    return abs(permanent)**2 / math.prod(math.factorial(count) for count in n)


def _theta(d, phi=0.0):
    result = [[0.0] * d for _ in range(3)]
    result[1][1] = phi
    return tuple(map(tuple, result))


def test_exact_field_and_fourier_hom_source():
    assert subject.multiply((0, 1), (0, 1)) == (-1, 1)
    assert subject.norm((3, -4)) == 13
    source = subject.FourierSource(2)
    by_n = {row.occupation: row for row in source.rows}
    assert len(source.rows) == 3
    assert by_n[(1, 1)].coefficient == (0, 0)
    assert by_n[(0, 2)].weight == by_n[(2, 0)].weight == 2
    assert source.denominator == 4


def test_complete_source_zeros_mass_and_residue():
    source = subject.FourierSource(6)
    assert len(source.rows) == 462
    assert sum(row.weight for row in source.rows) == 6**6
    assert 0 < len(source.support) <= 80  # Actual support is not presupposed.
    for row in source.rows:
        assert (row.coefficient == (0, 0)) == (row.weight == 0)
        if sum(i * count for i, count in enumerate(row.occupation)) % 6:
            assert row.weight == 0
    assert len(source.lookup) == len(source.support)


@pytest.mark.parametrize("mixed", [False, True])
def test_exact_bunched_tritter_columns_and_vacuum(mixed):
    cache = subject.TritterCache(6)
    vacuum = cache.column((0, 0, 0), mixed)
    assert vacuum.outputs == ((0, 0, 0),)
    assert vacuum.amplitudes == (1 + 0j,)
    for x in [(1, 1, 0), (2, 0, 0), (6, 6, 6)]:
        column = cache.column(x, mixed)
        assert len(column.outputs) == math.comb(sum(x) + 2, 2)
        assert sum(subject.factorial_product(o) * subject.norm(c)
                   for o, c in zip(column.outputs, column.coefficients)) == column.norm_denominator
        assert math.fsum(abs(a)**2 for a in column.amplitudes) == pytest.approx(1, abs=2e-12)
    assert len(cache.column((6, 6, 6), mixed).outputs) == 190


def test_single_particle_columns_orthogonal_and_bunched_input_factorial():
    cache = subject.TritterCache(6)
    for mixed in [False, True]:
        columns = [cache.column(tuple(int(i == j) for i in range(3)), mixed)
                   for j in range(3)]
        for i, j in itertools.product(range(3), repeat=2):
            overlap = sum(a.conjugate() * b for a, b in
                          zip(columns[i].amplitudes, columns[j].amplitudes))
            assert overlap == pytest.approx(int(i == j), abs=2e-12)
    # F3 sends two photons in one input into multinomial output weights.
    column = cache.column((2, 0, 0), False)
    for output, amplitude in zip(column.outputs, column.amplitudes):
        expected = math.factorial(2) / subject.factorial_product(output) / 9
        assert abs(amplitude)**2 == pytest.approx(expected, abs=2e-12)


def test_coherent_inputs_and_orthogonal_suffixes_are_distinct():
    sampler = subject.StructuredSampler(2)
    coherent = {((1, 0, 0),): 1 / math.sqrt(2),
                ((0, 1, 0),): 1 / math.sqrt(2)}
    output, probabilities, *_ = sampler.local_distribution(coherent, 1)
    index = output.index((1, 0, 0))
    assert probabilities[index] == pytest.approx(2 / 3, abs=2e-12)
    opposite = {((1, 0, 0),): 1 / math.sqrt(2),
                ((0, 1, 0),): -1 / math.sqrt(2)}
    assert sampler.local_distribution(opposite, 1)[1][index] == pytest.approx(0, abs=2e-12)
    distinct_suffixes = {((1, 0, 0), (1, 0, 0)): 1 / math.sqrt(2),
                         ((0, 1, 0), (0, 1, 0)): 1 / math.sqrt(2)}
    output, probabilities, *_ = sampler.local_distribution(distinct_suffixes, 0)
    first = sampler.cache.column((1, 0, 0), True)
    second = sampler.cache.column((0, 1, 0), True)
    for p, a, b in zip(probabilities, first.amplitudes, second.amplitudes):
        assert p == pytest.approx((abs(a)**2 + abs(b)**2) / 2, abs=2e-12)


def test_reconstruction_discards_latent_rows_and_retains_coherences():
    sampler = subject.StructuredSampler(2)
    state, probability = sampler.conditional_state((2, 4), _theta(2, math.pi / 3))
    assert len(state) == 3
    assert probability == subject.Fraction(3, 8)
    assert math.fsum(abs(amplitude)**2 for amplitude in state.values()) == pytest.approx(1)
    # All three placements of the two photons remain, with their complex phase.
    assert len(set(state.values())) > 1


def test_extreme_n18_sector_is_width_one_and_keeps_full_outputs():
    sampler = subject.StructuredSampler(6)
    state, mass = sampler.conditional_state((18, 0, 0, 0, 0, 0), _theta(6))
    assert len(state) == 1 and mass > 0
    output, probabilities, suffixes, groups = sampler.local_distribution(state, 0)
    assert len(output) == 190 and (18, 0, 0) in output
    assert math.fsum(probabilities) == pytest.approx(1, abs=2e-12)
    selected = max(range(len(probabilities)), key=probabilities.__getitem__)
    suffix = sampler.project(output, probabilities, suffixes, groups, selected, 0)
    assert len(suffix) == 1 and len(next(iter(suffix))) == 5
    # No residual row-sum constraint is imposed after measuring output.
    assert all(sum(x) == 0 for x in next(iter(suffix)))


@pytest.mark.parametrize("phase_index,phi", enumerate([0.0, math.pi / 6, math.pi / 3, -0.4]))
def test_all_462_small_probabilities_against_independent_ryser(phase_index, phi,
                                                            evidence_directory):
    sampler = subject.StructuredSampler(2)
    actual = sampler.complete_small_law(_theta(2, phi))
    matrix = _independent_six_mode_matrix(phi)
    reference = {n: _ryser_reference(matrix, n) for n in actual}
    assert len(actual) == len(reference) == 462
    errors = [abs(actual[n] - reference[n]) for n in actual]
    artifact = {
        "status": "NORMALIZED_CATEGORICAL_KERNEL_NOT_FINITE_BIT_LAW_OR_GLOBAL_TV_CERTIFICATE",
        "probability_convention": "Rounded conditional masses divided by their explicit fsum at every node; real-probability categorical kernel, distinct from finite-bit MT19937 quantile law",
        "phase_index": phase_index,
        "phase_label": ("0", "pi/6", "pi/3", "-0.4")[phase_index],
        "binary64_phase": phi, "binary64_phase_hex": phi.hex(),
        "modes": 6, "photons": 6, "occupation_count": len(actual),
        "max_absolute_error": max(errors),
        "half_L1_error": math.fsum(errors) / 2,
        "actual_norm": math.fsum(actual.values()),
        "reference_norm": math.fsum(reference.values()),
        "reference_absolute_tolerance": subject.REFERENCE_ABSOLUTE_TOLERANCE,
        "small_law_TV_tolerance": subject.SMALL_LAW_TV_TOLERANCE,
        "rows": [{"occupation": n, "actual_probability": actual[n],
                  "reference_probability": reference[n],
                  "absolute_error": abs(actual[n] - reference[n])} for n in actual],
    }
    # Seal complete laws/diagnostics before applying the comparison assertions.
    _write_exclusive(evidence_directory / f"phase_{phase_index}.json", artifact)
    assert max(errors) <= subject.REFERENCE_ABSOLUTE_TOLERANCE
    assert math.fsum(errors) / 2 <= subject.SMALL_LAW_TV_TOLERANCE
    assert math.fsum(reference.values()) == pytest.approx(1, abs=2e-11)


def test_phase_response_is_not_dephased_by_the_sampler():
    sampler = subject.StructuredSampler(2)
    first = sampler.complete_small_law(_theta(2, 0))
    second = sampler.complete_small_law(_theta(2, math.pi / 3))
    assert max(abs(first[n] - second[n]) for n in first) > 1e-5


def test_seeded_synthetic_draw_path_reproducible_without_graph():
    one, two = subject.StructuredSampler(2), subject.StructuredSampler(2)
    rng_one, rng_two = random.Random(6400001), random.Random(6400001)
    samples_one = [one.sample(_theta(2, math.pi / 6), rng_one) for _ in range(12)]
    samples_two = [two.sample(_theta(2, math.pi / 6), rng_two) for _ in range(12)]
    assert samples_one == samples_two
    assert all(len(n) == 6 and sum(n) == 6 for n in samples_one)


@pytest.mark.parametrize("bad", [[-1.0, 2.0], [float("nan"), 1.0],
                                 [0.2, 0.2], [], [float("inf")]])
def test_invalid_mass_is_failure_without_repair(bad):
    with pytest.raises(subject.NumericalFailure):
        subject.draw_probabilities(bad, random.Random(6400002))


def test_zero_cdf_bins_and_inaccessible_rng_are_explicit():
    class FixedQuantile:
        def __init__(self, value): self.value = value
        def random(self): return self.value
    assert subject.draw_probabilities([0.0, 0.5, 0.0, 0.5], FixedQuantile(0)) == 1
    assert subject.draw_probabilities([0.0, 0.5, 0.0, 0.5], FixedQuantile(0.5)) == 3
    with pytest.raises(subject.NumericalFailure):
        subject.draw_probabilities([1.0], FixedQuantile(1.0))


def test_bad_inputs_and_allocation_guards(monkeypatch):
    sampler = subject.StructuredSampler(2)
    with pytest.raises(subject.NumericalFailure, match="zero-probability"):
        sampler.conditional_state((1, 5), _theta(2))
    with pytest.raises(ValueError):
        sampler.conditional_state((2, 4), ((float("nan"), 0), (0, 0), (0, 0)))
    with pytest.raises(ValueError):
        subject.StructuredSampler(6).complete_small_law(_theta(6))
    monkeypatch.setattr(subject, "MAX_TRANSITION_ENTRIES", 0)
    with pytest.raises(subject.NumericalFailure, match="guard"):
        subject.TritterCache(6).column((1, 0, 0), False)


def test_emit_complete_exact_source_evidence(evidence_directory):
    source = subject.FourierSource(6)
    artifact = {
        "status": "EXACT_SOURCE_TABLE_ONLY_NOT_OPTIMIZER_OR_TV_CERTIFICATE",
        "d": 6, "denominator": source.denominator,
        "all_occupations": len(source.rows), "observed_nonzero_support": len(source.support),
        "rows": [{"occupation": row.occupation, "coefficient": row.coefficient,
                  "weight": row.weight} for row in source.rows],
        "rounding_policy": "exact source/tritter coefficients; monitored rounded conditional state",
        "mass_tolerance": subject.MASS_TOLERANCE,
        "reference_absolute_tolerance": subject.REFERENCE_ABSOLUTE_TOLERANCE,
        "small_law_TV_tolerance": subject.SMALL_LAW_TV_TOLERANCE,
        "randomness": "Python Random MT19937, synthetic N6 only, seeds6400001/6400002",
        "graphs": 0, "N18_random_draws": 0,
    }
    _write_exclusive(evidence_directory / "source_table.json", artifact)
