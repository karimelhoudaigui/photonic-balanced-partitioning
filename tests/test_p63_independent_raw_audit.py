"""Small deterministic audit fixtures; CODE ONLY until separate authorization.

No production helper, DEV graph, primary data or optical sampler is imported.
"""
from fractions import Fraction
import importlib.util
from pathlib import Path
import sys

import pytest


@pytest.fixture(scope="module")
def checker():
    path = Path(__file__).resolve().parents[1]/"research/P63_independent_raw_audit.py"
    spec = importlib.util.spec_from_file_location("p63_independent_checker_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_scalar_cut_uses_each_undirected_edge_once(checker):
    adjacency = [[0, 2, 0, 1], [2, 0, 3, 0], [0, 3, 0, 4], [1, 0, 4, 0]]
    assert checker.scalar_cut(adjacency, [0, 3]) == 6
    assert checker.scalar_cut(adjacency, [1, 2]) == 6
    assert checker.scalar_cut(adjacency, [0, 1]) == 4


def test_little_endian_mask_and_padding(checker):
    assert checker.unpack_mask([255, 1, 0]) == list(range(9))
    assert checker.unpack_mask([0, 0, 3]) == [16, 17]
    for bad in ([0, 0, 4], [0, 0], [256, 0, 0], [False, 0, 0]):
        with pytest.raises(checker.InvalidEvidence):
            checker.unpack_mask(bad)


def test_count_rank_precedes_carried_mapping(checker):
    counts = [18]+[0]*17
    order = list(reversed(range(18)))
    mapping = list(reversed(range(18)))
    physical, vertices = checker.decode(counts, order, mapping)
    assert physical == [0]+list(range(10, 18))
    assert vertices == list(range(8))+[17]


def test_fraction_spsa_has_shared_direction_and_all_four_losses(checker):
    delta = (1, -1)*5
    theta, gradient, plus, minus = checker.spsa((Fraction(0),)*10, delta, [0, 10, 10, 10], [4]*4, 10)
    assert plus == Fraction(3, 4) and minus == Fraction(2, 5)
    assert gradient == tuple(Fraction(7, 10)*d for d in delta)
    assert theta == tuple(-Fraction(7, 20)*d for d in delta)


def test_tensor_matrix_fixed_zero_phase_rows_and_cycle(checker):
    np = checker.np
    u = checker.rebuild_matrix((Fraction(0),)*10)
    expected0 = np.repeat(np.asarray([1., 37., 37.])/450, 6)
    expected6 = np.repeat(np.asarray([49., 13., 13.])/450, 6)
    assert abs(u[0])**2 == pytest.approx(expected0, abs=3e-14, rel=0)
    assert abs(u[6])**2 == pytest.approx(expected6, abs=3e-14, rel=0)
    assert u.conj().T@u == pytest.approx(np.eye(18), abs=3e-14, rel=0)
    shift = [6*b+(j+1) % 6 for b in range(3) for j in range(6)]
    diagonal = np.exp(2j*np.pi*np.tile(np.arange(6), 3)/6)
    assert u[:, shift] == pytest.approx(diagonal[:, None]*u, abs=3e-14, rel=0)


def gate_fixture(checker):
    B = {cid: {"best": 10} for cid, _, _ in checker.CASES}
    fast = {(cid, mode): {"prefix": True, "acceptance": True, "best": 11}
            for cid, _, _ in checker.CASES for mode in checker.MODES}
    return B, fast


def test_same_fixed_mode_required_and_timely_prefix_can_veto(checker):
    B, fast = gate_fixture(checker)
    left, right = (case[0] for case in checker.CASES)
    fast[left, "random"]["best"] = 9
    fast[right, "spectral"]["best"] = 9
    assert checker.gate(B, fast) == ("STAGE1_OPTIONAL_CONTROLS_REQUIRED", [], True)
    fast[right, "random"] = {"prefix": True, "acceptance": False, "best": 10}
    assert checker.gate(B, fast) == ("DEV_REJECTED_FIXED_FAST", ["random"], False)


def test_missing_or_ineligible_call_cannot_complete_favorable_gate(checker):
    B, fast = gate_fixture(checker)
    key = next(iter(fast))
    fast[key]["acceptance"] = False
    assert checker.gate(B, fast) == ("INCONCLUSIVE_FAST_ELIGIBILITY", [], False)
    del fast[key]
    assert checker.gate(B, fast) == ("INCONCLUSIVE_FAST_ELIGIBILITY", [], False)


def test_nonfinite_or_float_exact_fields_are_rejected(checker):
    assert not checker.finite(float("nan"))
    assert not checker.finite(True)
    with pytest.raises(checker.InvalidEvidence):
        checker.fraction(.5)
    assert checker.fraction("2/4") == Fraction(1, 2)
