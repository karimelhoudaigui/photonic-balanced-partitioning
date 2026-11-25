"""Independent integer cuts, deltas and prefix checks; no DEV graph/optimum."""
import importlib.util
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p49_fast_classical", ROOT / "research/P49_fast_classical.py")
fast = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fast)


def graph(n):
    rng = np.random.default_rng(490000 + n)
    upper = np.triu(rng.integers(0, 10, size=(n, n), dtype=np.int64), 1)
    return upper + upper.T


def direct_cut(a, subset):
    """Scalar undirected edge sum, independent of cache/vectorized formulas."""
    selected = set(map(int, subset))
    return sum(int(a[i, j]) for i in range(len(a)) for j in range(i + 1, len(a))
               if (i in selected) != (j in selected))


def direct_ell(a, subset):
    selected = set(map(int, subset))
    return np.array([sum(int(a[i, j]) * (-1 if j in selected else 1)
                         for j in range(len(a))) for i in range(len(a))], dtype=np.int64)


def decoded_masks(result):
    return [np.flatnonzero(np.unpackbits(row, count=result["n"], bitorder="little"))
            for row in result["trace"]["best_subset_packbits_little"]]


@pytest.mark.parametrize("n", [6, 10])
def test_every_balanced_state_delta_by_independent_edge_sum(n):
    a = graph(n)
    for subset in itertools.combinations(range(n), n // 2):
        state = fast.BalancedSwapState(a, subset)
        assert state.cost == direct_cut(a, subset)
        assert np.array_equal(state.ell, direct_ell(a, subset))
        deltas = state.all_deltas()
        for i, inside in enumerate(state.inside):
            for j, outside in enumerate(state.outside):
                changed = set(subset) - {int(inside)} | {int(outside)}
                difference = direct_cut(a, changed) - direct_cut(a, subset)
                assert state.delta(i, j) == int(deltas[i, j]) == difference


@pytest.mark.parametrize("n", [6, 10])
def test_incremental_swap_sequence_never_recomputes_or_drifts(n):
    a = graph(n)
    state = fast.BalancedSwapState(a, np.arange(n // 2))
    rng = np.random.default_rng(491000 + n)
    for _ in range(100):
        i, j = int(rng.integers(n // 2)), int(rng.integers(n // 2))
        before, change = state.cost, state.delta(i, j)
        state.swap(i, j)
        assert state.cost == before + change == direct_cut(a, state.inside)
        assert np.array_equal(state.ell, direct_ell(a, state.inside))
        assert np.array_equal(np.flatnonzero(state.membership), np.sort(state.inside))
        assert len(set(map(int, state.inside)) & set(map(int, state.outside))) == 0


@pytest.mark.parametrize("n", [6, 10])
def test_fixed_count_reproducibility_and_all_trace_cuts(n):
    a = graph(n)
    kwargs = dict(seed=492000 + n, max_proposals=3000)
    first = fast.solve_balanced(a, np.arange(n // 2), **kwargs)
    second = fast.solve_balanced(a, np.arange(n // 2), **kwargs)
    for name in ("best_cut", "overall_completed_best_cut", "counters", "proposal_count", "stop_reason"):
        assert first[name] == second[name]
    for name in ("best_cut", "proposal_count", "best_subset_packbits_little"):
        assert np.array_equal(first["trace"][name], second["trace"][name])
    assert first["trace"]["stage"] == second["trace"]["stage"]
    assert first["counters"]["vectorized_scans"] > 0
    assert first["counters"]["perturbations"] > 0
    assert first["counters"]["uniform_restarts"] > 0
    assert first["proposal_count"] == 3000
    assert first["proposal_count"] == first["counters"]["delta_evaluations"] + first["counters"]["full_restart_costs"]
    assert np.all(np.diff(first["trace"]["best_cut"]) <= 0)
    assert np.all(np.diff(first["trace"]["proposal_count"]) >= 0)
    for subset, cut in zip(decoded_masks(first), first["trace"]["best_cut"]):
        assert len(subset) == n // 2
        assert direct_cut(a, subset) == int(cut)
    assert direct_cut(a, first["best_subset"]) == first["best_cut"]
    assert first["best_cut"] <= direct_cut(a, np.arange(n // 2))
    # Serialization is a separate callable, outside the measured search.
    restored = json.loads(json.dumps(fast.json_safe_result(first), allow_nan=False))
    assert restored["best_cut"] == first["best_cut"]
    assert restored["trace"]["best_subset_packbits_little"] == first["trace"]["best_subset_packbits_little"].tolist()


def test_carried_priority_makes_fixed_count_trajectory_relabel_covariant():
    a, n = graph(10), 10
    rng = np.random.default_rng(493000)
    old_at_new = rng.permutation(n)
    new_at_old = np.argsort(old_at_new)
    priority = rng.permutation(n)
    source = np.arange(n // 2)
    first = fast.solve_balanced(a, source, seed=493001, max_proposals=1800, vertex_priority=priority)
    relabeled = fast.solve_balanced(a[np.ix_(old_at_new, old_at_new)], new_at_old[source],
                                   seed=493001, max_proposals=1800, vertex_priority=priority[old_at_new])
    assert np.array_equal(first["trace"]["best_cut"], relabeled["trace"]["best_cut"])
    assert first["counters"] == relabeled["counters"]
    for old_subset, new_subset in zip(decoded_masks(first), decoded_masks(relabeled)):
        assert np.array_equal(np.sort(new_at_old[old_subset]), new_subset)


@pytest.mark.parametrize("cap", [0, 1, 15])
def test_zero_and_small_safety_caps(cap):
    result = fast.solve_balanced(graph(6), np.arange(3), seed=494000, max_proposals=cap)
    assert result["proposal_count"] == cap
    assert result["stop_reason"] == "max_proposals" and result["cap_hit"]
    assert not result["proposal_cap_is_cost_equivalent"]


def test_prefix_selector_rejects_a_late_batch_under_either_clock():
    cpu, wall = np.array([0., 1., 2., 3.]), np.array([0., 2., 4., 6.])
    assert fast._eligible_prefix(cpu, wall, 1.5, None) == 1
    assert fast._eligible_prefix(cpu, wall, None, 3.5) == 1
    assert fast._eligible_prefix(cpu, wall, 3., 3.5) == 1
    assert fast._eligible_prefix(cpu, wall, 2., 6.) == 2


def install_virtual_clocks(monkeypatch):
    """Deterministic clock values, not an elapsed-runtime performance test."""
    class Tick:
        def __init__(self):
            self.value = 0.
        def __call__(self):
            self.value += 1.
            return self.value
    monkeypatch.setattr(fast.time, "process_time", Tick())
    monkeypatch.setattr(fast.time, "perf_counter", Tick())


def test_late_search_chunk_cannot_improve_returned_deadline_prefix(monkeypatch):
    install_virtual_clocks(monkeypatch)
    result = fast.solve_balanced(graph(6), np.arange(3), seed=495000,
                                 max_proposals=1000, cpu_budget_seconds=1.5)
    assert result["stop_reason"] == "cpu_deadline"
    assert result["eligible_checkpoint_index"] == 1
    assert result["trace"]["cpu_seconds"][-1] > 1.5
    assert result["best_cut"] == result["initial_cut"]
    assert result["cpu_overrun_seconds"] > 0
    assert direct_cut(graph(6), result["best_subset"]) == result["best_cut"]


def test_early_cap_or_wall_guard_is_inconclusive_for_positive(monkeypatch):
    install_virtual_clocks(monkeypatch)
    capped = fast.solve_balanced(graph(6), np.arange(3), seed=495001,
                                 max_proposals=1, cpu_budget_seconds=100.)
    assert capped["early_cap_inconclusive"]
    install_virtual_clocks(monkeypatch)
    wall = fast.solve_balanced(graph(6), np.arange(3), seed=495001, max_proposals=1000,
                               cpu_budget_seconds=100., wall_budget_seconds=1.5)
    assert wall["stop_reason"] == "wall_deadline" and wall["early_wall_inconclusive"]


def test_shared_cost_and_int64_validation():
    a = graph(6)
    source = np.arange(3)
    cost = direct_cut(a, source)
    result = fast.solve_balanced(a, source, seed=496000, max_proposals=0, incumbent_cost=cost)
    assert result["best_cut"] == cost
    invalid = [a.astype(float), a + np.eye(6, dtype=np.int64), a[:5, :5]]
    asymmetric = a.copy(); asymmetric[0, 1] += 1; invalid.append(asymmetric)
    negative = a.copy(); negative[0, 1] = negative[1, 0] = -1; invalid.append(negative)
    huge = a.copy(); huge[0, 1] = huge[1, 0] = np.iinfo(np.int64).max; invalid.append(huge)
    for adjacency in invalid:
        with pytest.raises(ValueError):
            fast.solve_balanced(adjacency, source, seed=496000, max_proposals=0)
    for subset in ([0, 0, 1], [0, 1], [0, 1, 6], [0., 1., 2.]):
        with pytest.raises(ValueError):
            fast.solve_balanced(a, subset, seed=496000, max_proposals=0)
    for kwargs in ({"incumbent_cost": cost + 1}, {"incumbent_cost": float(cost)},
                   {"cpu_budget_seconds": -1}, {"wall_budget_seconds": float("inf")},
                   {"vertex_priority": [0] * 6}):
        with pytest.raises(ValueError):
            fast.solve_balanced(a, source, seed=496000, max_proposals=0, **kwargs)


def test_zero_weight_graph_and_smallest_balanced_instance():
    for n in (2, 6):
        result = fast.solve_balanced(np.zeros((n, n), dtype=np.int64), np.arange(n // 2),
                                     seed=497000, max_proposals=200)
        assert result["best_cut"] == result["initial_cut"] == 0
        assert direct_cut(np.zeros((n, n), dtype=np.int64), result["best_subset"]) == 0
