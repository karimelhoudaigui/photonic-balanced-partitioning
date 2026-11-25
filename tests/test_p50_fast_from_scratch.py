"""P50 raw-input qualification: no DEV graph, optimizer optimum or timing test."""
import importlib.util
import inspect
import itertools
import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p50_fast", ROOT / "research/P50_fast_from_scratch.py")
fast = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fast)


def fixture(n):
    # Explicit small test family, no generated DEV population or graph seed.
    return np.array([[0 if i == j else 1 + ((i + 1) * (j + 1) + abs(i - j)) % 7
                      for j in range(n)] for i in range(n)], dtype=np.int64)


def direct_cut(a, subset):
    selected = set(map(int, subset))
    return sum(int(a[i, j]) for i in range(len(a)) for j in range(i + 1, len(a))
               if (i in selected) != (j in selected))


def direct_ell(a, subset):
    selected = set(map(int, subset))
    return np.array([sum(int(a[i, j]) * (-1 if j in selected else 1)
                         for j in range(len(a))) for i in range(len(a))], dtype=np.int64)


def decode(mask, n):
    return np.flatnonzero(np.unpackbits(mask, count=n, bitorder="little"))


class TickClock:
    """Elapsed CPU/wall ticks are synthetic; pytest/runner real clocks untouched."""
    def __init__(self, step=1.):
        self.now = -step
        self.step = step
    def __call__(self):
        self.now += self.step
        return self.now, self.now


def inactive_clock(monkeypatch):
    monkeypatch.setattr(fast, "_clock", lambda: (0., 0.))


@pytest.mark.parametrize("n", [6, 10])
def test_all_balanced_cross_swaps_match_independent_scalar_edge_sums(n):
    a = fixture(n); order = np.arange(n - 1, -1, -1)
    for subset in itertools.combinations(range(n), n // 2):
        state = fast._SwapState(a, subset, order, a.sum(axis=1))
        before = direct_cut(a, subset)
        assert state.cost == before
        assert np.array_equal(state.ell, direct_ell(a, subset))
        deltas = state.all_deltas()
        for i, old in enumerate(state.inside):
            for j, new in enumerate(state.outside):
                changed = set(subset) - {int(old)} | {int(new)}
                assert state.delta(i, j) == int(deltas[i, j]) == direct_cut(a, changed) - before


@pytest.mark.parametrize("n", [6, 10])
def test_swap_sequence_and_carried_internal_priority_are_exact(n):
    a = fixture(n); order = np.arange(n - 1, -1, -1)
    subset = np.arange(n // 2)
    state = fast._SwapState(a, subset, order, a.sum(axis=1))
    permutation = np.roll(np.arange(n), 2)
    carried = np.zeros_like(a); carried[np.ix_(permutation, permutation)] = a
    other = fast._SwapState(carried, permutation[subset], permutation[order], carried.sum(axis=1))
    rng = np.random.default_rng(1730)
    for _ in range(100):
        i, j = int(rng.integers(n // 2)), int(rng.integers(n // 2))
        state.swap(i, j); other.swap(i, j)
        assert state.cost == other.cost == direct_cut(a, state.inside)
        assert np.array_equal(state.ell, direct_ell(a, state.inside))
        assert np.array_equal(state.all_deltas(), other.all_deltas())
        assert np.array_equal(np.sort(permutation[state.inside]), np.sort(other.inside))


@pytest.mark.parametrize("initialization", ["random", "spectral"])
@pytest.mark.parametrize("n", [6, 10])
def test_fixed_work_reproducibility_all_cuts_and_first_scan(monkeypatch, initialization, n):
    inactive_clock(monkeypatch)
    a = fixture(n); before = a.copy()
    kwargs = dict(seed=1731, initialization=initialization,
                  cpu_budget_seconds=100., max_proposals=3000)
    first = fast.solve_from_raw(a, **kwargs)
    second = fast.solve_from_raw(a, **kwargs)
    assert np.array_equal(a, before)
    for key in ("best_cut", "initial_cut", "proposal_count", "counters", "stop_reason"):
        assert first[key] == second[key]
    for key in ("best_cut", "proposal_count", "best_subset_packbits_little"):
        assert np.array_equal(first["trace"][key], second["trace"][key])
    assert first["trace"]["stage"] == second["trace"]["stage"]
    assert first["trace"]["stage"][:2] == ["initialization", "initial_scan"]
    assert first["counters"]["anneal_proposals"] > 0
    assert first["counters"]["vectorized_scans"] > 0
    assert first["first_scan_completed_before_deadline"]
    assert first["proposal_count"] <= 3000
    assert first["proposal_count"] == (first["counters"]["initial_cut_scores"]
        + first["counters"]["delta_evaluations"] + first["counters"]["full_restart_cut_scores"])
    assert np.all(np.diff(first["trace"]["best_cut"]) <= 0)
    for mask, cut in zip(first["trace"]["best_subset_packbits_little"], first["trace"]["best_cut"]):
        selected = decode(mask, n)
        assert len(selected) == n // 2 and direct_cut(a, selected) == int(cut)
    assert direct_cut(a, first["best_subset"]) == first["best_cut"]
    assert not first["free_incumbent_used"] and not first["external_features_used"]
    json.loads(json.dumps(fast.json_safe_result(first), allow_nan=False))


@pytest.mark.parametrize("initialization", ["random", "spectral"])
def test_late_initialization_is_retained_only_for_audit(monkeypatch, initialization):
    monkeypatch.setattr(fast, "_clock", TickClock())
    result = fast.solve_from_raw(fixture(6), seed=1729, initialization=initialization,
                                 cpu_budget_seconds=1.5, max_proposals=1000)
    assert result["initial_cut"] is not None and result["overall_completed_best_cut"] is not None
    assert result["trace"]["cpu_seconds"].tolist() == [2.]
    assert result["best_cut"] is None and result["best_subset"] is None
    assert result["eligible_checkpoint_index"] is None and not result["has_eligible_result"]
    assert not result["comparison_acceptance_eligible"]
    assert not result["initialization_completed_before_deadline"]
    assert result["counters"]["vectorized_scans"] == result["counters"]["anneal_proposals"] == 0


def test_validation_deadline_has_no_fabricated_time_zero_candidate(monkeypatch):
    monkeypatch.setattr(fast, "_clock", TickClock())
    result = fast.solve_from_raw(fixture(6).astype(float), seed=1729,
                                 cpu_budget_seconds=.5, max_proposals=1000)
    assert result["stop_reason"] == "cpu_deadline_during_validation"
    assert result["initial_cut"] is result["best_cut"] is result["best_subset"] is None
    assert len(result["trace"]["best_cut"]) == 0
    assert result["trace"]["best_subset_packbits_little"].shape == (0, 1)


def test_late_first_scan_cannot_improve_eligible_initialization(monkeypatch):
    monkeypatch.setattr(fast, "_clock", TickClock())
    result = fast.solve_from_raw(fixture(6), seed=1729,
                                 cpu_budget_seconds=2.5, max_proposals=1000)
    assert result["eligible_checkpoint_index"] == 0
    assert result["best_cut"] == result["initial_cut"]
    assert result["trace"]["stage"] == ["initialization", "initial_scan"]
    assert not result["first_scan_completed_before_deadline"]
    assert result["counters"]["anneal_proposals"] == 0


def test_no_improvement_scan_still_records_timely_checkpoint(monkeypatch):
    monkeypatch.setattr(fast, "_clock", TickClock())
    result = fast.solve_from_raw(np.zeros((6, 6), dtype=np.int64), seed=1729,
                                 cpu_budget_seconds=3.5, max_proposals=1000)
    assert result["trace"]["stage"][:2] == ["initialization", "initial_scan"]
    assert result["trace"]["best_cut"][:2].tolist() == [0, 0]
    assert result["eligible_checkpoint_index"] == 1
    assert result["first_scan_completed_before_deadline"]
    assert result["initial_descent_completed_before_deadline"]
    assert result["counters"]["anneal_proposals"] == 0


def test_spectral_eigensolve_is_owned_and_charged_before_init(monkeypatch):
    class Clock:
        now = 0.
        def __call__(self):
            return self.now, self.now
    clock = Clock(); monkeypatch.setattr(fast, "_clock", clock)
    actual = np.linalg.eigh; observed = []
    def paid_eigensolve(matrix):
        observed.append(matrix.copy()); clock.now += 5.
        return actual(matrix)
    monkeypatch.setattr(fast.np.linalg, "eigh", paid_eigensolve)
    a = fixture(6)
    result = fast.solve_from_raw(a, seed=1729, initialization="spectral",
                                 cpu_budget_seconds=1., max_proposals=1000)
    assert len(observed) == 1 and result["best_cut"] is None
    own = result["initialization_details"]
    degree = a.sum(axis=1); expected = (np.diag(degree) - a) / int(degree.max())
    expected += .001 * np.diag(own["own_marks"])
    assert observed[0] == pytest.approx(expected, abs=1e-15)
    vector = own["spectral_rounding_vector"]
    assert observed[0] @ vector == pytest.approx(own["spectral_eigenvalue"] * vector, abs=1e-12)
    assert result["compute_cpu_seconds"] == 5.
    assert direct_cut(a, result["initial_subset"]) == result["initial_cut"]


@pytest.mark.parametrize("cap", [1, 2, 26])
def test_small_guards_stop_before_unfunded_scan_or_anneal(monkeypatch, cap):
    inactive_clock(monkeypatch)
    result = fast.solve_from_raw(fixture(10), seed=1729,
                                 cpu_budget_seconds=100., max_proposals=cap)
    assert result["early_cap_inconclusive"] and not result["comparison_acceptance_eligible"]
    assert result["proposal_count"] <= cap
    assert result["counters"]["anneal_proposals"] == 0
    assert result["cap_hit"] or result["guard_blocked_full_scan"]
    assert not result["proposal_cap_is_cost_equivalent"]


@pytest.mark.parametrize("initialization", ["random", "spectral"])
def test_zero_graph_and_smallest_size_still_restart_without_free_best(monkeypatch, initialization):
    inactive_clock(monkeypatch)
    for n in (2, 6):
        result = fast.solve_from_raw(np.zeros((n, n)), seed=1729, initialization=initialization,
                                     cpu_budget_seconds=100., max_proposals=1500)
        assert result["best_cut"] == result["initial_cut"] == 0
        assert result["counters"]["uniform_restarts"] > 0
        assert result["trace"]["stage"][:2] == ["initialization", "initial_scan"]


def test_raw_conversion_bounds_invalid_inputs_and_no_free_feature_parameters(monkeypatch):
    inactive_clock(monkeypatch)
    a = fixture(6)
    for raw in (a.astype(float), a.tolist(), a.astype(np.uint64)):
        result = fast.solve_from_raw(raw, seed=1729, cpu_budget_seconds=100., max_proposals=1)
        assert direct_cut(a, result["initial_subset"]) == result["initial_cut"]
        assert result["counters"]["input_conversions_and_validations"] == 1
    invalid = [a[:5, :5], a + np.eye(6, dtype=np.int64)]
    for value in (-1., .5, float("nan"), float("inf")):
        changed = a.astype(float); changed[0, 1] = changed[1, 0] = value; invalid.append(changed)
    huge = a.astype(np.uint64); huge[0, 1] = huge[1, 0] = np.uint64(2**63); invalid.append(huge)
    asymmetric = a.copy(); asymmetric[0, 1] += 1; invalid.append(asymmetric)
    for raw in invalid:
        with pytest.raises(ValueError):
            fast.solve_from_raw(raw, seed=1729, cpu_budget_seconds=100.)
    for kwargs in ({"initialization": "free_spectral"}, {"max_proposals": 0},
                   {"max_proposals": True}, {"cpu_budget_seconds": -1},
                   {"cpu_budget_seconds": float("inf")}):
        params = dict(seed=1729, cpu_budget_seconds=100.); params.update(kwargs)
        with pytest.raises(ValueError):
            fast.solve_from_raw(a, **params)
    names = set(inspect.signature(fast.solve_from_raw).parameters)
    assert names == {"adjacency", "seed", "initialization", "cpu_budget_seconds", "max_proposals"}
