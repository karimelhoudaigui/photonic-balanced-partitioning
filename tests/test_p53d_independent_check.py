"""Independent-checker guards only: no archived proof decoding or full replay."""
import ast
from fractions import Fraction as Q
import gzip
import importlib.util
import itertools
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p53d_checker", ROOT/"research/P53d_independent_check.py")
p = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(p)


def test_checker_has_no_production_import_or_matmul_kernel():
    tree = ast.parse(Path(p.__file__).read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): assert all(not (a.name.startswith("P") and a.name[1:2].isdigit()) for a in node.names)
        if isinstance(node, ast.ImportFrom): assert not ((node.module or "").startswith("P") and (node.module or "")[1:2].isdigit())
        assert not isinstance(node, ast.MatMult)


def test_slot_multisets_are_complete_without_production_compositions():
    four = list(p.occupations(4)); eight = list(p.occupations(8))
    assert len(four) == len(set(four)) == 330 and len(eight) == len(set(eight)) == 6435
    assert all(sum(row) == 4 for row in four) and all(sum(row) == 8 for row in eight)


@pytest.mark.parametrize("n,group,expected,mass", [
    ((4, 0, 0, 0, 0, 0, 0, 0), (0, 1, 4, 6), (1, 0, 0, 0, 0, 0, 0), 24),
    ((0, 4, 0, 0, 0, 0, 0, 0), (0, 1, 4, 6), (0, 0, -1, 0, 0, 0, 0), 24),
    ((2, 2, 0, 0, 0, 0, 0, 0), (0, 1, 2, 3), (-2,), 16),
    ((1, 1, 1, 1, 0, 0, 0, 0), (0, 1, 2, 3), (8,), 64)])
def test_24_permanent_monomials_divide_output_factorials_exactly(n, group, expected, mass):
    c = p.permanent_polynomial(n, group)
    assert c == expected
    row = p.laurent_probability(c, n)
    assert row == tuple(mass if j == len(row)//2 else 0 for j in range(len(row)))


def test_invalid_photon_input_or_group_cannot_be_reinterpreted():
    n = (4, 0, 0, 0, 0, 0, 0, 0)
    for counts, group in ((tuple(float(x) for x in n), (0, 1, 2, 3)), (n, (0, 0, 1, 2)),
                          (n, (0, 1, 2, 8)), (n, (True, 1, 2, 3))):
        with pytest.raises(ArithmeticError): p.permanent_polynomial(counts, group)


def test_direct_70_subset_ties_have_independent_known_values():
    assert p.direct_tie_scalar((4, 0, 0, 0, 4, 0, 0, 0)) == -224
    assert p.direct_tie_scalar((0, 4, 0, 0, 0, 4, 0, 0)) == 224
    assert p.direct_tie_scalar((1,)*8) == p.direct_tie_scalar((8, 0, 0, 0, 0, 0, 0, 0)) == 0


def test_column_bounds_are_enforced_BEFORE_any_numpy_conversion(monkeypatch):
    matrix = np.array([[1]], dtype=np.int64)
    monkeypatch.setattr(p.np, "asarray", lambda *args, **kwargs: pytest.fail("Conversion before Python guard"))
    with pytest.raises(ArithmeticError): p.two_einsum_spectrum([[4097]], [[1]], matrix)
    with pytest.raises(ArithmeticError): p.two_einsum_spectrum([[.5]], [[1]], matrix)
    assert p.column_bounds([[4096]*13]) == (4096,)*13


def test_two_einsums_and_antidiagonals_match_an_independent_python_sum():
    first, second = [[1, 2, 1], [0, 3, 0]], [[0, 1, 2, 1, 0], [1, 0, 3, 0, 1]]
    matrix = np.array([[2, -1], [-1, 3]], dtype=np.int64)
    expected = [0]*25
    for u, v in itertools.product(range(2), repeat=2):
        for i, j in itertools.product(range(3), range(5)):
            expected[i+j-3+12] += int(matrix[u, v])*first[u][i]*second[v][j]
    laurent, cosine = p.two_einsum_spectrum(first, second, matrix)
    assert laurent == tuple(expected)
    assert p.two_einsum_spectrum(second, first, matrix) == (laurent, cosine)
    assert cosine == (expected[12],)+tuple(2*expected[12+k] for k in range(1, 13))


def test_worst_13_pair_accumulation_and_float_matrix_rejection():
    bank = [[4096]*13]; matrix = np.array([[420]], dtype=np.int64)
    laurent, cosine = p.two_einsum_spectrum(bank, bank, matrix)
    assert laurent[12] == 13*420*4096**2 and max(map(abs, cosine)) < 2**38
    with pytest.raises(ArithmeticError): p.two_einsum_spectrum([[1]], [[1]], np.array([[1.]]))


def test_anchors_and_triangle_are_exact_without_Bernstein_or_phase_search():
    cosine = (Q(1), Q(0), Q(1, 2)) + (Q(0),)*10
    assert p.anchor_value(cosine, Q(0)) == Q(1, 2)
    assert p.anchor_value(cosine, Q(1, 2)) == Q(3, 4)
    assert p.triangle_margin(cosine, Q(1, 4)) == Q(1, 4)
    with pytest.raises(ArithmeticError): p.triangle_margin((.5,)+(Q(0),)*12, Q(0))


def test_current_proof_floats_rejected_historical_decimals_opaque_and_inflation_bounded(tmp_path):
    path = tmp_path/"fixture.json.gz"
    with gzip.open(path, "wb") as stream: stream.write(b'{"unused":0.5}')
    with pytest.raises(TypeError): p.read_json(path)
    opaque = p.read_json(path, historical=True)["unused"]
    assert isinstance(opaque, str)
    with pytest.raises(ArithmeticError): p.q(opaque)
    with pytest.raises(ArithmeticError): p.read_json(path, maximum=4)
    for value in (True, .5, {"numerator": 2, "denominator": 4}):
        with pytest.raises(ArithmeticError): p.q(value)
