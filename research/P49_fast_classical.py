"""P49 integer feasible search, with completed-prefix CPU/wall accounting.

No optimum/target is an input. No disk I/O occurs inside solve_balanced. The
proposal cap is a guardrail, not a matched resource unit. NumPy is the only
non-stdlib dependency; callers are responsible for setting BLAS threads to one.
"""
from __future__ import annotations

import math
import numbers
import time

import numpy as np


def _validated_graph(adjacency):
    a = np.asarray(adjacency)
    if a.dtype != np.dtype("int64"):
        raise ValueError("adjacency must already be int64; charge any conversion")
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] < 2 or a.shape[0] % 2:
        raise ValueError("adjacency must be square with positive even N>=2")
    n = a.shape[0]
    if np.any(a < 0) or np.any(np.diag(a) != 0) or not np.array_equal(a, a.T):
        raise ValueError("adjacency must be symmetric, nonnegative and loop-free")
    # Protect degree, cut, signed ell updates and vectorized delta arithmetic.
    if int(a.max()) > np.iinfo(np.int64).max // (4 * n * n):
        raise ValueError("edge weights exceed conservative int64 arithmetic bound")
    return np.ascontiguousarray(a)


def _validated_subset(subset, n):
    values = np.asarray(subset)
    if values.ndim != 1 or len(values) != n // 2 or values.dtype.kind not in "iu":
        raise ValueError("incumbent must be a one-dimensional balanced integer subset")
    if np.any(values < 0) or np.any(values >= n) or len(np.unique(values)) != len(values):
        raise ValueError("incumbent vertices must be distinct and in range")
    return values.astype(np.int64, copy=True)


def _validated_priority(priority, n):
    p = np.arange(n, dtype=np.int64) if priority is None else np.asarray(priority)
    if p.shape != (n,) or p.dtype.kind not in "iuf" or not np.all(np.isfinite(p)):
        raise ValueError("vertex_priority must contain N finite real numbers")
    if len(np.unique(p)) != n:
        raise ValueError("vertex_priority must be distinct (carry it under relabeling)")
    return np.argsort(p, kind="stable"), np.argsort(np.argsort(p, kind="stable"))


class BalancedSwapState:
    """Exact cached state; public primitives also support independent tests."""

    def __init__(self, adjacency, subset, *, vertex_priority=None):
        self.adjacency = _validated_graph(adjacency)
        self.n = self.adjacency.shape[0]
        self.k = self.n // 2
        self.canonical_order, self.rank = _validated_priority(vertex_priority, self.n)
        self.degree = self.adjacency.sum(axis=1, dtype=np.int64)
        self.load(_validated_subset(subset, self.n))

    def load(self, subset):
        """Internal balanced reset; caller supplies an already validated subset."""
        self.inside = np.asarray(subset, dtype=np.int64).copy()
        self.inside = self.inside[np.argsort(self.rank[self.inside], kind="stable")]
        self.membership = np.zeros(self.n, dtype=bool)
        self.membership[self.inside] = True
        self.outside = self.canonical_order[~self.membership[self.canonical_order]].copy()
        self.cost = int(self.adjacency[np.ix_(self.inside, self.outside)].sum(dtype=np.int64))
        self.ell = self.degree - 2 * self.adjacency[:, self.inside].sum(axis=1, dtype=np.int64)

    def delta(self, inside_position, outside_position):
        a, b = int(self.inside[inside_position]), int(self.outside[outside_position])
        return int(self.ell[b] - self.ell[a] + 2 * self.adjacency[a, b])

    def all_deltas(self):
        return (self.ell[self.outside][None, :] - self.ell[self.inside][:, None]
                + 2 * self.adjacency[np.ix_(self.inside, self.outside)])

    def swap(self, inside_position, outside_position, delta=None):
        a, b = int(self.inside[inside_position]), int(self.outside[outside_position])
        change = self.delta(inside_position, outside_position) if delta is None else int(delta)
        self.cost += change
        self.ell += 2 * self.adjacency[:, a] - 2 * self.adjacency[:, b]
        self.membership[a], self.membership[b] = False, True
        self.inside[inside_position], self.outside[outside_position] = b, a
        return change


def _packed_subset(subset, n):
    membership = np.zeros(n, dtype=np.uint8)
    membership[subset] = 1
    return np.packbits(membership, bitorder="little")


def _unpacked_subset(packed, n):
    return np.flatnonzero(np.unpackbits(packed, count=n, bitorder="little")).astype(np.int64)


def _eligible_prefix(trace_cpu, trace_wall, cpu_budget_seconds, wall_budget_seconds):
    eligible = np.ones(len(trace_cpu), dtype=bool)
    if cpu_budget_seconds is not None:
        eligible &= trace_cpu <= cpu_budget_seconds
    if wall_budget_seconds is not None:
        eligible &= trace_wall <= wall_budget_seconds
    indices = np.flatnonzero(eligible)
    # Index0 is the given-free common incumbent at time0, not a new discovery.
    return int(indices[-1]) if len(indices) else 0


def solve_balanced(adjacency, incumbent, *, seed, max_proposals,
                   cpu_budget_seconds=None, wall_budget_seconds=None,
                   incumbent_cost=None, vertex_priority=None):
    """Anneal, descend, perturb and restart with an auditable feasible prefix.

    A completed batch is timestamped at its END. A late batch is retained for
    audit but cannot improve the returned deadline-eligible best. Giving a CPU
    allowance equal to optical classical-postprocessing WALL time is allowed,
    but that conservative convention belongs in the caller's scientific ledger.
    Fixed-count runs (both deadlines None) have clock-independent trajectories.
    """
    cpu_start, wall_start = time.process_time(), time.perf_counter()
    if isinstance(max_proposals, bool) or not isinstance(max_proposals, numbers.Integral) or max_proposals < 0:
        raise ValueError("max_proposals must be a nonnegative integer safety cap")
    max_proposals = int(max_proposals)
    for deadline in (cpu_budget_seconds, wall_budget_seconds):
        if deadline is not None and (not math.isfinite(deadline) or deadline < 0):
            raise ValueError("deadline allowances must be finite and nonnegative")
    if isinstance(seed, bool) or not isinstance(seed, numbers.Integral) or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    state = BalancedSwapState(adjacency, incumbent, vertex_priority=vertex_priority)
    if incumbent_cost is not None:
        if isinstance(incumbent_cost, bool) or not isinstance(incumbent_cost, numbers.Integral):
            raise ValueError("incumbent_cost must be an exact integer")
        if int(incumbent_cost) != state.cost:
            raise ValueError("shared incumbent_cost disagrees with the actual cut")
    rng = np.random.default_rng(int(seed))
    n, k = state.n, state.k
    best_cost, best_subset = state.cost, state.inside.copy()
    trace_cpu, trace_wall, trace_cut = [0.0], [0.0], [best_cost]
    trace_masks, trace_work, trace_stage = [_packed_subset(best_subset, n)], [0], ["given_free"]
    counters = {"delta_evaluations": 0, "full_restart_costs": 0,
                "full_cost_evaluations_including_setup": 1, "accepted_swaps": 0,
                "vectorized_scans": 0, "perturbations": 0, "uniform_restarts": 0}
    work = 0
    stop_reason = None

    def remember():
        nonlocal best_cost, best_subset
        if state.cost < best_cost:
            best_cost, best_subset = state.cost, state.inside.copy()

    def checkpoint(stage):
        nonlocal stop_reason
        packed = _packed_subset(best_subset, n)
        elapsed_cpu, elapsed_wall = time.process_time() - cpu_start, time.perf_counter() - wall_start
        trace_cpu.append(elapsed_cpu)
        trace_wall.append(elapsed_wall)
        trace_cut.append(best_cost)
        trace_masks.append(packed)
        trace_work.append(work)
        trace_stage.append(stage)
        if cpu_budget_seconds is not None and elapsed_cpu >= cpu_budget_seconds:
            stop_reason = "cpu_deadline"
        elif wall_budget_seconds is not None and elapsed_wall >= wall_budget_seconds:
            stop_reason = "wall_deadline"
        return stop_reason is not None

    # Graph-derived temperature; no optimization target or fitted parameter.
    positive_edges = state.adjacency[state.adjacency > 0]
    mean_weight = float(positive_edges.mean()) if len(positive_edges) else 1.0
    mean_neighbours = float(np.count_nonzero(state.adjacency, axis=1).mean())
    temperature_high = max(1.0, mean_weight * math.sqrt(max(1.0, mean_neighbours)))
    temperature_low = max(0.05, mean_weight / 20.0)
    epoch_length, chunk_length = 8 * n, 32
    epoch = 0
    checkpoint("setup")
    while stop_reason is None and work < max_proposals:
        # Batched stochastic proposals, still exact O(N) accepted-state updates.
        epoch_used = 0
        while epoch_used < epoch_length and work < max_proposals and stop_reason is None:
            chunk = min(chunk_length, epoch_length - epoch_used, max_proposals - work)
            for _ in range(chunk):
                i, j = int(rng.integers(k)), int(rng.integers(k))
                change = state.delta(i, j)
                fraction = epoch_used / max(1, epoch_length - 1)
                temperature = temperature_high * (temperature_low / temperature_high) ** fraction
                if change <= 0 or rng.random() < math.exp(-change / temperature):
                    state.swap(i, j, change)
                    counters["accepted_swaps"] += 1
                    remember()
                epoch_used += 1
                work += 1
                counters["delta_evaluations"] += 1
            checkpoint("anneal")
        if stop_reason is not None or work >= max_proposals:
            break

        # Complete K^2 batches only; a batch finishing late receives no early credit.
        for _ in range(n):
            if max_proposals - work < k * k:
                break
            deltas = state.all_deltas()
            index = int(np.argmin(deltas))
            i, j = divmod(index, k)
            change = int(deltas[i, j])
            work += k * k
            counters["delta_evaluations"] += k * k
            counters["vectorized_scans"] += 1
            if change < 0:
                state.swap(i, j, change)
                counters["accepted_swaps"] += 1
                remember()
            checkpoint("full_scan")
            if stop_reason is not None or change >= 0:
                break
        if stop_reason is not None or work >= max_proposals:
            break

        epoch += 1
        if epoch % 4 == 0:
            subset = state.canonical_order[rng.permutation(n)[:k]]
            state.load(subset)
            work += 1
            counters["full_restart_costs"] += 1
            counters["full_cost_evaluations_including_setup"] += 1
            counters["uniform_restarts"] += 1
            remember()
            checkpoint("uniform_restart")
        else:
            # Resetting to a known best uses no discovery, but its O(NK) CPU is paid.
            state.load(best_subset)
            counters["full_cost_evaluations_including_setup"] += 1
            count = min(k, max(2, k // 3), max_proposals - work)
            inside_positions = rng.choice(k, size=count, replace=False)
            outside_positions = rng.choice(k, size=count, replace=False)
            for i, j in zip(inside_positions, outside_positions):
                state.swap(int(i), int(j))
                work += 1
                counters["delta_evaluations"] += 1
                counters["accepted_swaps"] += 1
                remember()
            counters["perturbations"] += 1
            checkpoint("perturb_best")

    if stop_reason is None:
        stop_reason = "max_proposals"
    # Convert compact arrays while still charging search compute; JSON is later.
    trace = {"cpu_seconds": np.asarray(trace_cpu, dtype=np.float64),
             "wall_seconds": np.asarray(trace_wall, dtype=np.float64),
             "best_cut": np.asarray(trace_cut, dtype=np.int64),
             "best_subset_packbits_little": np.asarray(trace_masks, dtype=np.uint8),
             "proposal_count": np.asarray(trace_work, dtype=np.int64),
             "stage": trace_stage}
    eligible = _eligible_prefix(trace["cpu_seconds"], trace["wall_seconds"],
                                cpu_budget_seconds, wall_budget_seconds)
    eligible_subset = _unpacked_subset(trace["best_subset_packbits_little"][eligible], n)
    overall_subset = np.sort(best_subset)
    compute_cpu = time.process_time() - cpu_start
    compute_wall = time.perf_counter() - wall_start
    cap_hit = work >= max_proposals
    cap_before_cpu = cap_hit and cpu_budget_seconds is not None and trace_cpu[-1] < cpu_budget_seconds
    wall_before_cpu = (stop_reason == "wall_deadline" and cpu_budget_seconds is not None
                       and compute_cpu < cpu_budget_seconds)
    return {"algorithm": "P49_incremental_anneal_scan_multistart_v1", "n": n,
            "seed": int(seed), "max_proposals": max_proposals,
            "cpu_budget_seconds": cpu_budget_seconds, "wall_budget_seconds": wall_budget_seconds,
            "initial_cut": int(trace_cut[0]), "best_cut": int(trace_cut[eligible]),
            "best_subset": eligible_subset,
            "eligible_checkpoint_index": eligible,
            "eligible_checkpoint_cpu_seconds": float(trace_cpu[eligible]),
            "eligible_checkpoint_wall_seconds": float(trace_wall[eligible]),
            "overall_completed_best_cut": best_cost,
            "overall_completed_best_subset": overall_subset,
            "last_completed_checkpoint_index": len(trace_cpu) - 1,
            "compute_cpu_seconds": compute_cpu, "compute_wall_seconds": compute_wall,
            "cpu_overrun_seconds": max(0.0, compute_cpu - cpu_budget_seconds) if cpu_budget_seconds is not None else 0.0,
            "wall_overrun_seconds": max(0.0, compute_wall - wall_budget_seconds) if wall_budget_seconds is not None else 0.0,
            "stop_reason": stop_reason, "cap_hit": cap_hit,
            "early_cap_inconclusive": bool(cap_before_cpu),
            "early_wall_inconclusive": bool(wall_before_cpu),
            "proposal_count": work, "counters": counters, "trace": trace,
            "timing_convention": "validation/setup/search/compact-trace CPU+wall; serialization excluded",
            "proposal_cap_is_cost_equivalent": False}


def json_safe_result(result):
    """Convert arrays AFTER measured compute; caller owns all file writes."""
    if isinstance(result, np.ndarray):
        return result.tolist()
    if isinstance(result, np.generic):
        return result.item()
    if isinstance(result, dict):
        return {key: json_safe_result(value) for key, value in result.items()}
    if isinstance(result, (list, tuple)):
        return [json_safe_result(value) for value in result]
    return result
