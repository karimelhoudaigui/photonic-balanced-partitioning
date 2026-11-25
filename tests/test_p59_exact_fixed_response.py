"""Small exact synthetic guards only: never call calibrate or full462 source."""
from fractions import Fraction as F
import itertools
import json
import math

import pytest

from research import P59_exact_fixed_response as p


def test_eisenstein_ring_and_conjugation():
    xi = (0, 1)
    assert p.mul(xi, xi) == (-1, 1)
    for a in ((0, 0), (1, 0), (0, 1), (-7, 11), (3, -4)):
        assert p.conj(p.conj(a)) == a
        assert p.mul(a, p.conj(a)) == (p.norm(a), 0)
    assert p.mul((-1, 1), (0, -1)) == (1, 0)


def test_exact_integer_rejection():
    for value in (True, False, 1.0, F(1), "1"):
        with pytest.raises(ArithmeticError):
            p.integer(value)
    assert p.integer(-7) == -7


def test_frozen_gram_and_q():
    matrix = p.frozen_matrix()
    q = p.validate_matrix(matrix)
    assert q[0] == tuple(F(x, 150) for x in (1, 1, 37, 37, 37, 37))
    assert q[2] == tuple(F(x, 150) for x in (49, 49, 13, 13, 13, 13))
    assert 2*(1-sum(x*x for x in q[0])) == F(2837, 1875)
    assert 2*(1-sum(x*x for x in q[4])) == F(5, 3)


def test_phase_column_convention_and_gram_failure():
    matrix = p.frozen_matrix()
    assert {(i, a) for i in range(6) for a in range(6) if matrix[i][a][2]} == set(itertools.product((1, 3, 5), (2, 3)))
    broken = [list(row) for row in matrix]
    broken[0][0] = (broken[0][0][0]+1, broken[0][0][1], 0)
    with pytest.raises(ArithmeticError, match="Gram"):
        p.validate_matrix(broken)


def test_two_photon_hom_from_actual_columns():
    h2 = (((1, 0, 0), (1, 0, 0)), ((1, 0, 0), (-1, 0, 0)))
    coefficients = p.creation_coefficients(h2)
    assert len(coefficients) == 3
    assert coefficients[(1, 1)] == (p.ZERO,)*3
    for n in ((2, 0), (0, 2)):
        assert p.probability_spectrum(coefficients[n], n, 4) == (F(1, 2), F(0), F(0))
    assert p.sum_spectra((1, p.probability_spectrum(c, n, 4)) for n, c in coefficients.items()) == (F(1), F(0), F(0))


def test_independent_single_pnr_permanent_fixture():
    n, c = p.hand_fixture(p.frozen_matrix())
    assert n == (4, 2, 0, 0, 0, 0)
    assert c == ((-35050, 1000), p.ZERO, (175, -1000))
    assert p.response(p.probability_spectrum(c, n))["derivative_over_sqrt3"] == -F(124, 421875)


def test_probability_fourier_orientation_and_forbidden_harmonic():
    spectrum = p.probability_spectrum(((1, 0), p.ZERO, (0, 1)), (1,), 1)
    assert spectrum == (F(2), F(0), F(1))
    response = p.response(spectrum)
    assert response["cos2"] == 1 and response["sin2_over_sqrt3"] == -1
    assert response["derivative_over_sqrt3"] == -2
    with pytest.raises(ArithmeticError, match="harmonic"):
        p.probability_spectrum(((1, 0), (1, 0), p.ZERO), (1,), 1)


def test_all_ones_decoder_uniform_ties():
    winners, edges, classes = p.decoder((1,)*6)
    assert winners == p.SUBSETS and len(winners) == 20
    assert edges == (F(3, 5),)*15 and classes == (F(1, 10),)*10


def test_all_bunch_decoder_keeps_all_class_mass():
    winners, edges, classes = p.decoder((6, 0, 0, 0, 0, 0))
    assert len(winners) == 10 and all(0 in s for s in winners)
    assert edges == (F(3, 5),)*15 and classes == (F(1, 10),)*10


def test_independent_tie_count_support_and_lcm():
    examples = ((2, 2, 2, 0, 0, 0), (2, 2, 1, 1, 0, 0), (3, 1, 1, 1, 0, 0),
                (3, 3, 0, 0, 0, 0), (2, 1, 1, 1, 1, 0), (6, 0, 0, 0, 0, 0), (1,)*6)
    ways = [len(p.decoder(n)[0]) for n in examples]
    assert ways == [1, 2, 3, 4, 6, 10, 20] and math.lcm(*ways) == 60
    assert math.lcm(*range(1, 21)) == 232792560


def test_all_ten_cut_classes_gram_inverse():
    crossing = tuple(tuple(int((i in s) != (j in s)) for i, j in p.EDGES) for s in p.CLASSES)
    assert len(crossing) == 10
    for c, first in enumerate(crossing):
        for d, second in enumerate(crossing):
            assert sum(x*y for x, y in zip(first, second)) == (9 if c == d else 5)
    law = tuple(F(i, 55) for i in range(1, 11))
    means = tuple(sum(law[c]*crossing[c][e] for c in range(10)) for e in range(15))
    assert tuple((sum(pattern[e]*means[e] for e in range(15))-5)/4 for pattern in crossing) == law


def test_low_moment_targets_identity_source():
    q = tuple(tuple(F(i == j) for j in range(6)) for i in range(6))
    count = 0
    for degree in (1, 2, 3):
        for powers in p.occupations(6, degree):
            assert p.moment_target(q, powers) == int(max(powers) <= 1)
            count += 1
    assert count == 83
    q_hom = ((F(1, 2),)*2,)*2
    for degree in (1, 2, 3):
        for powers in p.occupations(2, degree):
            explicit = sum(F(1, 2)*p.factorial_weight(n, powers) for n in ((2, 0), (0, 2)))
            assert p.moment_target(q_hom, powers) == explicit


def test_exact_diagonal_pgf_known_marginals():
    assert p.diagonal_pmf((F(1), F(0))) == (F(0), F(1), F(0))
    assert p.diagonal_pmf((F(1, 2), F(1, 2))) == (F(1, 2), F(0), F(1, 2))


def test_decoder_rejects_inexact_or_outside_domain():
    for n in ((1.0, 1, 1, 1, 1, 1), (True, 1, 1, 1, 1, 1), (1,)*5, (0,)*6, (-1, 7, 0, 0, 0, 0)):
        with pytest.raises(ArithmeticError):
            p.decoder(n)


def test_small_occupation_coverage_and_factorial_weights():
    assert set(p.occupations(2, 2)) == {(0, 2), (1, 1), (2, 0)}
    assert p.factorial_weight((2, 1), (2, 1)) == 2
    assert p.factorial_weight((1, 2), (2, 0)) == 0
    with pytest.raises(ArithmeticError):
        tuple(p.occupations(2, 2.0))


def test_exact_rational_serialization_and_curvature():
    row = p.response((F(1, 3), F(-2, 7), F(3, 11)))
    assert row["curvature_upper"] == 4*(abs(row["cos2"])+abs(row["derivative_over_sqrt3"]))
    assert row["center_mean"] == row["u"]+row["cos2"]
    encoded = json.loads(json.dumps(p.exact_json({"x": F(-2, 7), "field": (F(1, 3), F(0))})))
    assert encoded["x"] == {"numerator": -2, "denominator": 7}
    assert encoded["field"][1] == {"numerator": 0, "denominator": 1}
    with pytest.raises(ArithmeticError, match="inexact"):
        p.exact_json({"proof_number": 0.5})
