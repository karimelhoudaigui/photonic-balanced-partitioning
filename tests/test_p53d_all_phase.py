"""Finite exact component fixtures, no real fixed B/full35/all70 run or LP."""
from fractions import Fraction as Q
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"research"))
SPEC = importlib.util.spec_from_file_location("p53d", ROOT/"research/P53d_fixed_w_all_phase.py")
p = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(p)


def direct_creation(group, n):
    """Independent distinct assignments to input labels, polynomial coefficients."""
    rows = tuple(i for i, value in enumerate(n) for _ in range(value))
    result = [0]*(3*sum(a >= 4 for a in group)+1)
    for assignment in set(itertools.permutations(rows)):
        coefficient, power = 1, 0
        for row, source in zip(assignment, group):
            j, a = row % 4, source % 4
            coefficient *= (-1)**((j//2)*(a % 2)+(j % 2)*(a//2)+(row >= 4 and source >= 4))
            power += j if source >= 4 else 0
        result[power] += coefficient
    return tuple(result)


def python_contraction(first, second, matrix):
    degree_a, degree_b = (len(first[0])-1)//2, (len(second[0])-1)//2
    result = [0]*25
    for u, row_a in enumerate(first):
        for v, row_b in enumerate(second):
            for i, a in enumerate(row_a):
                for j, b in enumerate(row_b):
                    result[i+j-degree_a-degree_b+12] += int(matrix[u, v])*a*b
    return result


def cosine_for_shifted_square(a, epsilon):
    # (cos(phi)-a)^2+epsilon, an independent explicit positive polynomial.
    result = [Q(0)]*13
    result[0], result[1], result[2] = Q(1, 2)+a*a+epsilon, -2*a, Q(1, 2)
    return tuple(result)


@pytest.fixture(scope="module")
def one_spectrum():
    counts = tuple(p.exact.compositions(8, 4))
    return counts, p.group_spectrum((0, 1, 4, 6), counts)


def test_column_bound_is_per_column_not_sum_over_all_laurent_columns():
    bank = [[4096]*13]
    assert p.guard_bank(bank) == (4096,)*13
    assert sum(p.guard_bank(bank)) > 4096


def test_python_column_guard_runs_before_any_dtype_conversion(monkeypatch):
    matrix = np.array([[1]], dtype=np.int64)
    def forbidden(*args, **kwargs): raise AssertionError("conversion preceded proof guard")
    monkeypatch.setattr(p.np, "asarray", forbidden)
    with pytest.raises(ValueError): p.contract_scalar([[4097]], [[1]], matrix)
    with pytest.raises(TypeError): p.contract_scalar([[.5]], [[1]], matrix)


def test_integer_contraction_matches_independent_python_sum_and_swapped_banks():
    first = [[1, 2, 1], [0, 3, 0]]
    second = [[0, 1, 2, 1, 0], [1, 0, 3, 0, 1]]
    matrix = np.array([[2, -1], [-1, 3]], dtype=np.int64)
    expected = python_contraction(first, second, matrix)
    forward, backward = p.contract_scalar(first, second, matrix), p.contract_scalar(second, first, matrix)
    assert forward["laurent_numerators"] == backward["laurent_numerators"] == expected
    assert forward["banks_swapped_to_multiply_shorter_first"] is True
    assert backward["banks_swapped_to_multiply_shorter_first"] is False
    assert forward["cosine_numerators"] == (expected[12],)+tuple(2*expected[12+k] for k in range(1, 13))


def test_worst_allowed_integer_products_and_thirteen_pair_accumulation_do_not_overflow():
    bank = [[4096]*13]; matrix = np.array([[420]], dtype=np.int64)
    result = p.contract_scalar(bank, bank, matrix)
    assert result["laurent_numerators"][12] == 13*420*4096**2 == 91603599360
    assert result["cosine_numerators"][1] == 2*12*420*4096**2
    assert result["laurent_numerators"] == python_contraction(bank, bank, matrix)


def test_float_asymmetric_or_out_of_bound_matrix_cannot_enter_integer_product():
    banks = [[1], [1]]
    for matrix in (np.eye(2), np.array([[0, 1], [0, 0]], dtype=np.int64),
                   np.array([[421, 0], [0, 0]], dtype=np.int64)):
        with pytest.raises(TypeError): p.contract_scalar(banks, banks, matrix)


def test_exact_tie_scalar_and_symmetric_small_matrix_have_known_values():
    a, b = (4, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 4, 0, 0, 0)
    counts8, values, matrix = p.make_tie_matrix((a, b)); lookup = dict(zip(counts8, values))
    assert lookup[(4, 0, 0, 0, 4, 0, 0, 0)] == -224
    assert lookup[(0, 4, 0, 0, 0, 4, 0, 0)] == 224
    assert lookup[(8, 0, 0, 0, 0, 0, 0, 0)] == lookup[(1,)*8] == 0
    assert matrix.dtype == np.dtype(np.int64) and np.array_equal(matrix, matrix.T)
    assert int(matrix[0, 1]) == -224


def test_selected_creation_polynomials_match_independent_input_assignment_reference(one_spectrum):
    counts, record = one_spectrum; lookup = {n: i for i, n in enumerate(counts)}
    examples = [tuple(4 if i == row else 0 for i in range(8)) for row in range(8)]
    examples += [(2, 2, 0, 0, 0, 0, 0, 0), (1, 1, 1, 1, 0, 0, 0, 0),
                 (0, 1, 0, 1, 0, 1, 0, 1), (1, 0, 2, 0, 0, 1, 0, 0)]
    for n in examples:
        expected = direct_creation((0, 1, 4, 6), n)
        assert record["creation_coefficients"][lookup[n]] == expected
        for h in range(-6, 7):
            reference = math.prod(math.factorial(x) for x in n)*sum(
                a*b for i, a in enumerate(expected) for j, b in enumerate(expected) if j-i == h)
            assert record["probability_laurent_numerators"][lookup[n]][h+6] == reference


def test_group_parseval_masses_all_harmonics_and_fock_bunch_factor_are_exact(one_spectrum):
    counts, record = one_spectrum; lookup = {n: i for i, n in enumerate(counts)}
    assert record["normalization_harmonic_sums"] == (0,)*6+(4096,)+(0,)*6
    assert all(x <= 4096 for x in record["per_column_L1"])
    for row in range(8):
        n = tuple(4 if i == row else 0 for i in range(8))
        assert record["probability_laurent_numerators"][lookup[n]] == (0,)*6+(24,)+(0,)*6


def test_invalid_groups_are_rejected_without_reinterpreting_photons():
    counts = tuple(p.exact.compositions(8, 4))
    for group in ((0, 0, 1, 2), (0, 1, 2), (0, 1, 2, 8), (0., 1, 2, 3)):
        with pytest.raises(ValueError): p.group_spectrum(group, counts)


def test_exact_rational_cosine_anchors_and_corruption_rejection():
    cosine = [Q(0)]*13
    cosine[0], cosine[1], cosine[2], cosine[6] = Q(1, 7), Q(1, 2), Q(-1, 3), Q(1, 10)
    expected = {"0": Q(1, 7)+Q(1, 2)-Q(1, 3)+Q(1, 10),
                "pi/2": Q(1, 7)+Q(1, 3)-Q(1, 10), "pi/3": Q(1, 7)+Q(1, 4)+Q(1, 6)+Q(1, 10)}
    assert all(record["equal"] for record in p.exact_anchors(cosine, expected).values())
    expected["pi/3"] += Q(1, 10000)
    with pytest.raises(ArithmeticError): p.exact_anchors(cosine, expected)


def test_affine_power_matches_direct_values_and_exact_inverse():
    power = (Q(1, 7), Q(-3), Q(2), Q(1, 9)); left, right = Q(3, 8), Q(4, 8)
    transformed = p.affine_power(power, left, right)
    for u in (Q(0), Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
        assert p.evaluate_power(transformed, u) == p.evaluate_power(power, left+(right-left)*u)
    assert p.affine_power(transformed, -left/(right-left), (1-left)/(right-left)) == power


def test_bernstein_full_power_reconstruction_detects_tiny_corruption_and_accepts_int_endpoints():
    power = (Q(1, 7), Q(2), Q(-3), Q(1, 9))
    for degree, left, right in ((12, 0, 1), (24, Q(3, 8), Q(4, 8))):
        record = p.bernstein_record(power, degree, left, right)
        assert p.verify_bernstein(power, degree, left, right, record["controls"])
        broken = list(record["controls"]); broken[3] += Q(1, 10**20)
        assert not p.verify_bernstein(power, degree, left, right, broken)


def test_triangle_strict_bound_requires_no_bernstein_stage():
    result = p.certify_scalar((Q(1),)+(Q(0),)*12, Q(0))
    assert result["status"] == "STRICT_UNIFORM_GAP" and result["lower_bound"] == 1
    assert result["certificate_stage"] == "triangle" and result["Bernstein_stages"] == []


def test_weak_bound_and_registered_zero_are_never_declared_strict():
    cosine = [Q(0)]*13; cosine[0] = cosine[2] = Q(1, 2)  # cos(phi)^2.
    result = p.certify_scalar(cosine, Q(0))
    assert result["status"] == "NONNEGATIVE_WITHOUT_STRICT_BOUND" and result["lower_bound"] == 0
    assert 4 in result["zero_node_indices"] and result["nonnegative_proven"]


def test_global_bernstein_can_certify_when_triangle_bound_is_negative():
    result = p.certify_scalar(cosine_for_shifted_square(Q(1, 4), Q(1, 10)), Q(0))
    assert result["triangle_lower_bound"] < 0 and result["status"] == "STRICT_UNIFORM_GAP"
    assert result["certificate_stage"] == "Bernstein12_global" and result["lower_bound"] > 0


def test_fixed_eight_intervals_degree24_can_certify_without_adaptive_subdivision():
    result = p.certify_scalar(cosine_for_shifted_square(Q(1, 8), Q(1, 1000)), Q(0))
    assert result["status"] == "STRICT_UNIFORM_GAP" and result["certificate_stage"] == "Bernstein24_fixed8"
    assert len(result["Bernstein_stages"]) == 9 and result["Bernstein_stages"][0]["minimum_control"] < 0
    assert [record["x_interval"] for record in result["Bernstein_stages"][1:]] == [(Q(j, 8), Q(j+1, 8)) for j in range(8)]


def test_registered_negative_value_is_a_real_falsifier_without_phase_optimization():
    cosine = [Q(0)]*13; cosine[0], cosine[1] = Q(-1, 2), Q(1)
    result = p.certify_scalar(cosine, Q(0))
    assert result["status"] == "EXACT_NEGATIVE_REGISTERED_ENDPOINT" and not result["nonnegative_proven"]
    assert result["registered_node_values"][0] == Q(-3, 2) and result["Bernstein_stages"] == []


def test_negative_bernstein_controls_of_a_positive_polynomial_remain_inconclusive():
    # Strictly positive everywhere, but its minimum lies between the fixed nodes.
    result = p.certify_scalar(cosine_for_shifted_square(Q(1, 8), Q(1, 10**12)), Q(0))
    assert min(result["registered_node_values"]) > 0 and result["status"] == "INCONCLUSIVE"
    assert not result["nonnegative_proven"] and result["lower_bound"] is None
    assert min(row["minimum_control"] for row in result["Bernstein_stages"]) < 0


def test_aggregate_keeps_strict_weak_falsifier_and_unresolved_scopes_distinct():
    strict = {"status": "STRICT_UNIFORM_GAP", "nonnegative_proven": True, "lower_bound": Q(1, 100), "zero_node_indices": []}
    rows = [dict(strict) for _ in range(35)]
    result = p.aggregate(rows, Q(1, 50), Q(14))
    assert result["status"] == "STRICT_UNIFORM_FIXED_W_B4_PHASE_GAP" and result["same_old_normalized_graph_lower_bound"] == Q(1, 1400)
    rows[0] = {**strict, "status": "NONNEGATIVE_WITHOUT_STRICT_BOUND", "lower_bound": Q(0), "zero_node_indices": [4]}
    assert p.aggregate(rows, Q(1, 50), Q(14))["status"] == "NONNEGATIVE_FIXED_W_B4_PHASE_GAP_WITHOUT_STRICT_BOUND"
    rows[0] = {"status": "INCONCLUSIVE", "nonnegative_proven": False, "lower_bound": None, "zero_node_indices": []}
    assert p.aggregate(rows, Q(1, 50), Q(14))["status"] == "INCONCLUSIVE_FIXED_W_B4_PHASE"
    rows[0]["status"] = "EXACT_NEGATIVE_REGISTERED_ENDPOINT"
    assert p.aggregate(rows, Q(1, 50), Q(14))["status"] == "FIXED_W_FALSIFIED_BY_REGISTERED_B4_PHASE"


def test_aggregate_registered_zero_does_not_prove_nonnegativity_at_unresolved_phases():
    row = {"status": "EXACT_ZERO_REGISTERED_ENDPOINT", "nonnegative_proven": False, "lower_bound": None, "zero_node_indices": [4]}
    result = p.aggregate([row]*35, Q(1), Q(14))
    assert result["status"] == "STRICTNESS_FALSIFIED_BY_REGISTERED_ZERO_OTHER_PHASES_UNRESOLVED"
    assert result["uniform_lower_bound"] is None


def test_frozen_spec_rejects_another_B_w_ladder_or_any_LP_call():
    p.validate_spec(p.frozen_spec())
    for key, value in (("B_theta", "pi/4"), ("w", "other"), ("interval_count", 16),
                       ("interval_Bernstein_degree", 48), ("maximum_LP_calls", 1)):
        spec = p.frozen_spec(); spec[key] = value
        with pytest.raises(ValueError): p.validate_spec(spec)


def test_float_coefficients_or_affine_nodes_cannot_enter_rational_proof():
    with pytest.raises(TypeError): p.certify_scalar((.5,)+(Q(0),)*12, Q(0))
    with pytest.raises(TypeError): p.evaluate_power((Q(1), Q(2)), .1)
    with pytest.raises(TypeError): p.affine_power((Q(1), Q(2)), .1, Q(1))
