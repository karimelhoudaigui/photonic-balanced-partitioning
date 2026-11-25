"""Independent-engine symbolic guards; no full mean table or primary result."""
from fractions import Fraction as F
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p59_independent", ROOT/"research/P59_independent_quadratic_check.py")
p = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(p)


def reference(pair):
    a, b = pair
    return F(a)+F(b, 2), F(b, 2)  # 1,i*sqrt3 basis.


def test_integer_field_matches_independent_quadratic_basis():
    fixtures = ((0, 0), (1, 0), (0, 1), (7, -4), (3, 4), (-1402, 40))
    for a in fixtures:
        x, y = reference(a)
        assert reference(p.conjugate(a)) == (x, -y)
        assert p.norm(a) == x*x+3*y*y
        for b in fixtures:
            r, s = reference(b)
            assert reference(p.mul(a, b)) == (x*r-3*y*s, x*s+y*r)


def test_three_twelve_term_factors_have_only_registered_even_exponents():
    factors = [p.quadratic_factor(i) for i in range(3)]
    assert [len(factor) for factor in factors] == [12, 12, 12]
    assert all(sum(n) == 2 for factor in factors for n, _, _ in factor)
    assert {h for _, h, _ in factors[0]+factors[2]} == {0}
    assert {h for _, h, _ in factors[1]} == {0, 2}
    assert p.EVEN[0] == ((-1, 0), (7, 0), (5, 0))


def test_selected_preexecution_coefficient_and_pnr_slope_fixture():
    n = (4, 2, 0, 0, 0, 0)
    coefficients = p.coefficient_table(only=[n])[n]
    assert coefficients == ((-35050, 1000), (0, 0), (175, -1000))
    spectrum = p.probability_spectrum(coefficients, math.factorial(4)*math.factorial(2))
    assert spectrum["derivative_over_sqrt3"] == F(-124, 421875)
    assert spectrum["sin2_over_sqrt3"] == F(-62, 421875)


def test_own_multiset_occupation_population_and_parity_counts():
    states = p.occupations()
    assert len(states) == len(set(states)) == 462
    assert all(len(n) == 6 and sum(n) == 6 and min(n) >= 0 for n in states)
    assert sum(sum(n[1::2]) % 2 == 0 for n in states) == 236


def test_explicit_matrix_gram_and_fixed_q_match_manual_intensities():
    _, q = p.matrix_and_q()
    assert q[0] == tuple(F(x, 150) for x in (1, 1, 37, 37, 37, 37))
    assert q[2] == tuple(F(x, 150) for x in (49, 49, 13, 13, 13, 13))
    assert q[4] == (F(1, 6),)*6
    assert all(sum(row) == 1 for row in q)


def test_hypergeometric_decoder_matches_small_four_mode_toy_without_primary_twenty_subsets():
    for counts in ((4, 0, 0, 0), (2, 2, 1, 1), (1, 1, 1, 1)):
        ranked = sorted(counts, reverse=True); threshold = ranked[1]
        eligible = [subset for subset in itertools.combinations(range(4), 2)
                    if all(i in subset for i, n in enumerate(counts) if n > threshold)
                    and all(counts[i] >= threshold for i in subset)]
        expected = tuple(F(sum((i in subset) != (j in subset) for subset in eligible), len(eligible))
                         for i, j in itertools.combinations(range(4), 2))
        assert p.edge_kernel(counts, k=2) == expected


def test_top3_known_hypergeometric_cases_and_all_sixty_denominators():
    assert p.edge_kernel((6, 0, 0, 0, 0, 0)) == (F(3, 5),)*15
    kernel = p.edge_kernel((5, 1, 0, 0, 0, 0))
    assert kernel[0] == 0 and kernel[1] == F(3, 4) and kernel[-1] == F(1, 2)
    lcm = 1
    for n in p.occupations():
        for weight in p.edge_kernel(n): lcm = math.lcm(lcm, weight.denominator)
    assert lcm == 60


def test_ten_class_gram_is_nine_five_and_inverts_uniform_bunch_decoder():
    vectors = [tuple(int((a in subset) != (b in subset)) for a, b in p.EDGES) for subset in p.CLASSES]
    assert len(vectors) == 10
    for i, first in enumerate(vectors):
        for j, second in enumerate(vectors):
            assert sum(a*b for a, b in zip(first, second)) == (9 if i == j else 5)
    assert p.class_kernel((F(3, 5),)*15) == (F(1, 10),)*10


def test_q_only_moments_match_independent_single_mode_elementary_formula():
    _, q = p.matrix_and_q(); row = q[0]
    for order in (1, 2, 3):
        elementary = sum((math.prod(row[i] for i in subset) for subset in itertools.combinations(range(6), order)), F(0))
        powers = (order, 0, 0, 0, 0, 0)
        assert p.q_moment(powers, q) == math.factorial(order)**2*elementary
    assert len(p.moment_powers()) == len(set(p.moment_powers())) == 83
    hom = ((F(1, 2), F(1, 2)),)*2
    assert p.q_moment((1, 1), hom) == 0
    assert p.q_moment((2, 1), hom) == 0
    assert p.q_pmf(hom[0])[:3] == (F(1, 2), F(0), F(1, 2))


def test_canonical_proof_comparison_rejects_float_nonreduced_or_bool_values():
    encoded = p.encoded({"u": F(1, 3), "F2": (F(1, 5), F(-1, 7))})
    assert p.math_equal(encoded, {"u": F(1, 3), "F2": (F(1, 5), F(-1, 7))})
    for value in (.5, {"numerator": 2, "denominator": 4}, {"numerator": True, "denominator": 2}):
        with pytest.raises(TypeError): p.rational(value)
    assert not p.math_equal(True, 1)


def test_primary_winner_validation_uses_count_plus_eligibility_not_subset_enumeration():
    n = (5, 1, 0, 0, 0, 0)
    winners = [[0, 1, i] for i in range(2, 6)]
    assert p.valid_winners(n, winners)
    assert not p.valid_winners(n, winners[:-1])
    assert not p.valid_winners(n, winners[:-1]+[winners[0]])
    assert not p.valid_winners(n, [[0, 2, i] for i in range(2, 6)])


def test_positive_harmonic_spectrum_derivative_curvature_and_corruption():
    result = p.response((F(1, 2), F(1, 10), F(-1, 20)))
    assert result["cos2"] == F(3, 20)
    assert result["derivative_over_sqrt3"] == F(1, 10)
    assert result["curvature_upper"] == 1
    encoded = p.encoded(result); encoded["F2"][1]["numerator"] *= -1
    assert not p.math_equal(encoded, result)
