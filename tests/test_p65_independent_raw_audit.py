"""Unexecuted deterministic fixtures for the independent P65 checker only."""
from fractions import Fraction
import importlib.util
import math
from pathlib import Path
import sys

import pytest


@pytest.fixture(scope="module")
def checker():
    path = Path(__file__).resolve().parents[1]/"research/P65_independent_raw_audit.py"
    spec = importlib.util.spec_from_file_location("p65_independent_checker_fixtures", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def adjacency():
    return [[0, 3, 0, 0], [3, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]


def test_scalar_cut_and_K10_little_endian_padding(checker):
    assert checker.cut(adjacency(), [0, 1]) == 1
    assert checker.cut(adjacency(), [0, 2]) == 4
    assert checker.unpack([255, 3, 0]) == list(range(10))
    assert checker.unpack([0, 0, 15]) == [16, 17, 18, 19]
    with pytest.raises(checker.InvalidEvidence): checker.unpack([0, 0, 16])
    with pytest.raises(checker.InvalidEvidence): checker.unpack([False, 0, 0])


def test_collision_self_loop_never_consumes_coin(checker):
    row = checker.transition(adjacency(), [0, 1], 1, [2, 0, 0, 0], 1., None)
    assert row["collision"] and row["current"] == [0, 1] and row["current_cut"] == row["chain_best_cut"] == 1
    assert row["proposal"] is row["proposal_cut"] is row["acceptance_probability"] is None
    assert not row["accepted"] and not row["coin_seed_used"]
    with pytest.raises(checker.InvalidEvidence): checker.transition(adjacency(), [0, 1], 1, [2, 0, 0, 0], 1., .2)


def test_CF_probability_one_still_requires_coin(checker):
    row = checker.transition(adjacency(), [0, 1], 1, [1, 1, 0, 0], 2., .9)
    assert row["acceptance_probability"] == 1 and row["accepted"] and row["coin_seed_used"]
    with pytest.raises(checker.InvalidEvidence): checker.transition(adjacency(), [0, 1], 1, [1, 1, 0, 0], 2., None)


def test_rejected_CF_keeps_current_and_own_chain_best(checker):
    row = checker.transition(adjacency(), [0, 1], 1, [1, 0, 1, 0], math.log(2)/3, .75)
    assert row["proposal_cut"] == 4 and row["acceptance_probability"] == pytest.approx(.5, abs=1e-15, rel=0)
    assert not row["accepted"] and row["current"] == [0, 1] and row["chain_best_cut"] == 1
    with pytest.raises(checker.InvalidEvidence): checker.transition(adjacency(), [0, 1], 1, [1, 0, 0, 0], 1., None)


def test_next_attempt_uses_changed_current_and_collision_keeps_it(checker):
    first = checker.transition(adjacency(), [0, 2], 4, [1, 1, 0, 0], 1., .8)
    assert first["accepted"] and first["current"] == [0, 1] and first["chain_best_cut"] == 1
    second = checker.transition(adjacency(), first["current"], first["chain_best_cut"], [2, 0, 0, 0], 1., None)
    assert second["current_before_cut"] == 1 and second["current"] == [0, 1] and second["chain_best_cut"] == 1


def test_exact_fitness_ties_choose_first(checker):
    values = [Fraction(1, 2)]*8
    values[2] = values[5] = Fraction(1, 3)
    assert checker.choose_fitness(values) == 2
    assert checker.choose_fitness([Fraction(1, 2)]*8) == 0
    with pytest.raises(checker.InvalidEvidence): checker.choose_fitness([.5]*8)


def test_spectral_Cayley_weighted_small_reference(checker):
    np = checker.np
    u, _, scale, degrees = checker.reference_cayley([[0, 7], [7, 0]], Fraction(1, 2), Fraction(0))
    assert degrees == [7, 7] and scale == 7
    assert u == pytest.approx(np.asarray([[3/5, 4j/5], [4j/5, 3/5]]), abs=3e-14, rel=0)
    weighted = [[0, 7, 0, 0], [7, 0, 2, 0], [0, 2, 0, 3], [0, 0, 3, 0]]
    _, h, scale, degrees = checker.reference_cayley(weighted, Fraction(1, 2), Fraction(1, 4))
    assert degrees == [7, 9, 5, 3] and scale == Fraction(39, 4)
    assert h[0, 1] == pytest.approx(29/39, abs=1e-15, rel=0)


def test_fixed_mode_both_cases_and_failure_priority(checker):
    B = {cid: {"best": 10} for cid, _, _ in checker.CASES}
    fast = {(cid, mode): {"prefix": True, "acceptance": True, "best": 11} for cid, _, _ in checker.CASES for mode in checker.MODES}
    left, right = (c[0] for c in checker.CASES)
    fast[left, "random"]["best"], fast[right, "spectral"]["best"] = 9, 9
    assert checker.gate(B, fast) == ("STAGE1_OPTIONAL_CONTROLS_REQUIRED", [], True)
    fast[right, "random"] = {"prefix": True, "acceptance": False, "best": 10}
    assert checker.gate(B, fast) == ("DEV_REJECTED_FIXED_FAST", ["random"], False)
    assert checker.gate(B, fast, failed=True) == ("INCONCLUSIVE_FIRST_FAILURE", [], False)


def test_all820_metadata_roles_unique_native_nonzero(checker):
    table = checker.namespace_table()
    assert len(table) == len(set(table.values())) == 820
    assert all(v != 0 for k, v in table.items() if k[-1] == "count")
