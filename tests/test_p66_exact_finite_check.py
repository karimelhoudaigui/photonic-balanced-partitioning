"""Tiny authored fixtures only; never construct a P66 main-family graph."""
from fractions import Fraction as F
import importlib.util
from itertools import permutations
import json
import math
from pathlib import Path

import pytest


PATH = Path(__file__).resolve().parents[1] / "research" / "P66_exact_finite_check.py"
SPEC = importlib.util.spec_from_file_location("p66_independent_finite", PATH)
p66 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p66)


def test_exact_complex_field():
    i = p66.C(0, 1)
    assert i * i == -1
    assert (1 + i) / (1 - i) == i
    assert p66.C(F(1, 3), F(2, 5)).norm2() == F(61, 225)
    with pytest.raises(ZeroDivisionError):
        i / 0


def test_gaussian_inverse_requires_pivot_swap():
    i = p66.C(0, 1)
    matrix = [[p66.C(), i], [i, p66.C(1)]]
    expected = [[p66.C(1), -i], [-i, p66.C()]]
    assert p66.inverse(matrix) == expected
    assert p66.multiply(matrix, expected) == p66.identity(2)
    assert p66.multiply(expected, matrix) == p66.identity(2)
    with pytest.raises(ArithmeticError):
        p66.inverse([[1, 1], [1, 1]])
    with pytest.raises(ValueError):
        p66.inverse([])


def test_matrix_order_and_adjoint():
    a = [[p66.C(1), p66.C(0, 1)], [p66.C(), p66.C(1)]]
    b = [[p66.C(1), p66.C()], [p66.C(2), p66.C(1)]]
    assert p66.multiply(a, b) != p66.multiply(b, a)
    assert p66.adjoint(a) == [[p66.C(1), p66.C()], [p66.C(0, -1), p66.C(1)]]


def test_ryser_against_independent_four_mode_permutation_sum():
    matrix = [[p66.C(1), p66.C(0, 1), p66.C(2), p66.C()],
              [p66.C(3), p66.C(-1), p66.C(), p66.C(1, 1)],
              [p66.C(), p66.C(2), p66.C(1), p66.C(0, -1)],
              [p66.C(1), p66.C(), p66.C(1, 2), p66.C(2)]]
    reference = p66.C()
    for order in permutations(range(4)):
        term = p66.C(1)
        for row, col in enumerate(order):
            term = term * matrix[row][col]
        reference = reference + term
    assert p66.permanent(matrix) == reference
    assert p66.permanent([[1, 2], [3, 4]]) == 10
    assert p66.permanent([]) == 1


def test_collided_fock_normalization_both_factorials():
    # Rational orthogonal splitter; all three two-photon outputs are explicit.
    u = [[p66.C(F(3, 5)), p66.C(F(4, 5))],
         [p66.C(F(-4, 5)), p66.C(F(3, 5))]]
    targets = [[2, 0], [1, 1], [0, 2]]
    from_distinct = [p66.fock_probability(u, [1, 1], target) for target in targets]
    from_bunched = [p66.fock_probability(u, [2, 0], target) for target in targets]
    assert from_distinct == [F(288, 625), F(49, 625), F(288, 625)]
    assert from_bunched == [F(81, 625), F(288, 625), F(256, 625)]
    assert sum(from_distinct) == sum(from_bunched) == 1
    with pytest.raises(ValueError):
        p66.fock_probability(u, [1, 1], [1, 0])


def test_single_bright_pgf_two_modes():
    assert p66.bright_pgf(2, 2) == [F(1, 2), F(0), F(1, 2)]
    assert p66.bright_pgf(2, 1) == [F(1, 2), F(1, 2)]
    with pytest.raises(ValueError):
        p66.bright_pgf(2, 3)


def test_scalar_cut_and_dark_projector_four_modes():
    a = [[F(0), F(2), F(0), F(1)],
         [F(2), F(0), F(3), F(0)],
         [F(0), F(3), F(0), F(4)],
         [F(1), F(0), F(4), F(0)]]
    assert p66.cut(a, [0, 1]) == 4
    assert p66.cut(a, [0, 2]) == 10
    projector = p66.dark_projector(4, [0, 1])
    assert projector == [[p66.C(F(1, 2)), p66.C(F(-1, 2)), p66.C(), p66.C()],
                         [p66.C(F(-1, 2)), p66.C(F(1, 2)), p66.C(), p66.C()],
                         [p66.C(), p66.C(), p66.C(), p66.C()],
                         [p66.C(), p66.C(), p66.C(), p66.C()]]
    assert p66.multiply(projector, projector) == projector


def test_exact_serialization_and_exclusive_output(tmp_path):
    encoded = json.loads(p66.json_bytes({"fraction": F(1, 3), "complex": p66.C(F(2, 7), -1)}))
    assert encoded == {"fraction": "1/3", "complex": ["2/7", "-1"]}
    path = tmp_path / "only_tiny_fixture"
    ledger = p66.Ledger(path)
    try:
        ledger.emit("fixture", probability=F(1, 2))
        with pytest.raises(p66.FirstFailure):
            ledger.require(False, "intentional fixture failure")
        assert ledger.checks == 1
    finally:
        ledger.stream.close()
    with pytest.raises(FileExistsError):
        p66.Ledger(path)


def test_native_five_fixed_hom_probabilities(record_property):
    # Two modes/two photons only; no draw, random seed, main-family or calibration.
    api, metadata = p66.native_api()
    half = math.sqrt(0.5)
    u = [[p66.C(half), p66.C(half)], [p66.C(half), p66.C(-half)]]
    cases = [([1, 1], [1, 1], 0.0), ([1, 1], [2, 0], 0.5),
             ([1, 1], [0, 2], 0.5), ([2, 0], [2, 0], 0.25),
             ([2, 0], [1, 1], 0.5)]
    observations = []
    try:
        backend = p66.native_backend(u, api)
        for source, target, expected in cases:
            amplitude, observed = p66.native_point(backend, source, target, api)
            observations.append({"source": source, "target": target, "expected": expected,
                                 "observed": observed, "amplitude": [amplitude.real, amplitude.imag]})
    finally:
        record_property("native_fixture_points", json.dumps(observations))
        record_property("native_runtime_provenance", json.dumps(metadata))
    for row in observations:
        assert abs(row["observed"] - row["expected"]) <= (
            p66.ABS_TOL + p66.REL_TOL * max(row["expected"], row["observed"]))
    assert p66.native_readback(api[1]) == 1
    for item in metadata["loaded_module_files"].values():
        assert p66.digest(item["path"]) == item["sha256"]
