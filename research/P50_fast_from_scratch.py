"""P50 paid-from-raw balanced search: descent before annealing, no free best.

NumPy only. The two initialization modes have independent CPU budgets; callers
must not interpret their free best-of as one algorithm. Serialization is later.
"""
from __future__ import annotations

import math
import numbers
import time

import numpy as np


def _clock():
    return time.process_time(), time.perf_counter()


def _validated_graph(adjacency):
    raw = np.asarray(adjacency)
    if raw.ndim != 2 or raw.shape[0] != raw.shape[1] or raw.shape[0] < 2 or raw.shape[0] % 2:
        raise ValueError("adjacency must be square with even N>=2")
    if raw.dtype.kind not in "biuf" or not np.all(np.isfinite(raw)):
        raise ValueError("adjacency must contain finite real integer weights")
    if raw.dtype.kind == "f" and not np.all(raw == np.floor(raw)):
        raise ValueError("fractional graph weights are not accepted")
    if np.any(raw < 0) or np.any(np.diag(raw) != 0) or not np.array_equal(raw, raw.T):
        raise ValueError("graph must be nonnegative, symmetric and loop-free")
    n = raw.shape[0]
    # Python int conversion BEFORE int64 casting also handles unsigned/float.
    if int(raw.max()) > np.iinfo(np.int64).max // (4 * n * n):
        raise ValueError("edge weight exceeds conservative exact-int64 bound")
    return np.ascontiguousarray(raw, dtype=np.int64)


class _SwapState:
    """Internal exact cached state on already validated inputs."""
    def __init__(self, adjacency, subset, order, degree):
        self.a, self.n = adjacency, len(adjacency)
        self.k = self.n // 2
        self.order, self.rank, self.degree = order, np.argsort(order), degree
        self.load(subset)

    def load(self, subset):
        self.inside = np.asarray(subset, dtype=np.int64).copy()
        self.inside = self.inside[np.argsort(self.rank[self.inside], kind="stable")]
        self.membership = np.zeros(self.n, dtype=bool)
        self.membership[self.inside] = True
        self.outside = self.order[~self.membership[self.order]].copy()
        self.cost = int(self.a[np.ix_(self.inside, self.outside)].sum(dtype=np.int64))
        self.ell = self.degree - 2 * self.a[:, self.inside].sum(axis=1, dtype=np.int64)

    def delta(self, i, j):
        a, b = int(self.inside[i]), int(self.outside[j])
        return int(self.ell[b] - self.ell[a] + 2 * self.a[a, b])

    def all_deltas(self):
        return (self.ell[self.outside][None, :] - self.ell[self.inside][:, None]
                + 2 * self.a[np.ix_(self.inside, self.outside)])

    def swap(self, i, j, change=None):
        a, b = int(self.inside[i]), int(self.outside[j])
        change = self.delta(i, j) if change is None else int(change)
        self.cost += change
        self.ell += 2 * self.a[:, a] - 2 * self.a[:, b]
        self.membership[a], self.membership[b] = False, True
        self.inside[i], self.outside[j] = b, a


def _pack(subset, n):
    mask = np.zeros(n, dtype=np.uint8)
    mask[subset] = 1
    return np.packbits(mask, bitorder="little")


def _unpack(mask, n):
    return np.flatnonzero(np.unpackbits(mask, count=n, bitorder="little")).astype(np.int64)


def _initial_subset(a, degree, order, rng, initialization):
    n, k = len(a), len(a) // 2
    details = {"mode": initialization, "own_priority_order": order.copy(),
               "own_priority_by_vertex": np.argsort(order)}
    if initialization == "random":
        return order[rng.permutation(n)[:k]], details
    dmax = int(degree.max())
    laplacian = np.diag(degree) - a
    marked = laplacian / dmax if dmax else np.zeros((n, n), dtype=float)
    marks = rng.random(n)
    marked = marked + 1e-3 * np.diag(marks)
    values, vectors = np.linalg.eigh(marked)
    vector = vectors[:, 1].copy()
    if not np.all(np.isfinite(values)) or not np.all(np.isfinite(vector)):
        raise ArithmeticError("nonfinite independent spectral initialization")
    rank = np.argsort(order)
    maximum = float(abs(vector).max())
    pivot = min(np.flatnonzero(abs(vector) >= maximum - 1e-12), key=lambda v: rank[v])
    if vector[pivot] < 0:
        vector *= -1
    subset = np.lexsort((rank, -vector))[:k]
    details.update(own_marks=marks, marker_coefficient=1e-3,
                   spectral_normalizer=dmax, spectral_eigenvalue=float(values[1]),
                   spectral_rounding_vector=vector, spectral_pivot=int(pivot))
    return subset, details


def solve_from_raw(adjacency, *, seed, initialization="random",
                   cpu_budget_seconds, max_proposals=100_000_000):
    """Charge all raw-input preparation, then return completed eligible best.

    best_cut/best_subset are None when no initialization finishes in time.
    A late scan/initialization remains in trace/overall_completed fields only.
    max_proposals is a guard, not a resource-equivalent score budget. Insufficient
    guard for a complete required scan stops search before any annealing there.
    """
    cpu_start, wall_start = _clock()
    if initialization not in ("random", "spectral"):
        raise ValueError("initialization must be random or spectral")
    if isinstance(seed, bool) or not isinstance(seed, numbers.Integral) or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    if isinstance(max_proposals, bool) or not isinstance(max_proposals, numbers.Integral) or max_proposals < 1:
        raise ValueError("max_proposals must be an integer guard>=1")
    if isinstance(cpu_budget_seconds, bool) or not isinstance(cpu_budget_seconds, numbers.Real):
        raise ValueError("CPU allowance must be a finite nonnegative real")
    cpu_budget_seconds = float(cpu_budget_seconds)
    if not math.isfinite(cpu_budget_seconds) or cpu_budget_seconds < 0:
        raise ValueError("CPU allowance must be a finite nonnegative real")
    max_proposals = int(max_proposals)
    a = _validated_graph(adjacency)
    n, k = len(a), len(a) // 2
    validation_cpu, validation_wall = _clock()
    validation_cpu -= cpu_start; validation_wall -= wall_start
    counters = {"input_conversions_and_validations": 1, "initial_cut_scores": 0,
                "delta_evaluations": 0, "full_restart_cut_scores": 0,
                "full_cost_evaluations": 0, "accepted_swaps": 0,
                "vectorized_scans": 0, "anneal_proposals": 0,
                "perturbations": 0, "uniform_restarts": 0}
    times_cpu, times_wall, cuts, masks, work_trace, stages = [], [], [], [], [], []
    best_cost = best_subset = initial_cost = initial_subset = state = None
    details = {"mode": initialization}
    work = 0
    stop_reason = None
    guard_blocked_scan = False
    first_scan_index = initial_descent_end_index = None

    def remember():
        nonlocal best_cost, best_subset
        if best_cost is None or state.cost < best_cost:
            best_cost, best_subset = state.cost, state.inside.copy()

    def checkpoint(stage):
        nonlocal stop_reason
        packed = _pack(best_subset, n)
        now_cpu, now_wall = _clock()
        elapsed_cpu, elapsed_wall = now_cpu - cpu_start, now_wall - wall_start
        times_cpu.append(elapsed_cpu); times_wall.append(elapsed_wall)
        cuts.append(best_cost); masks.append(packed); work_trace.append(work); stages.append(stage)
        if elapsed_cpu >= cpu_budget_seconds:
            stop_reason = "cpu_deadline"

    def descend(initial=False):
        nonlocal work, stop_reason, guard_blocked_scan, first_scan_index, initial_descent_end_index
        while stop_reason is None:
            if max_proposals - work < k * k:
                guard_blocked_scan = True
                stop_reason = "proposal_guard_before_full_scan"
                return
            deltas = state.all_deltas()
            index = int(np.argmin(deltas)); i, j = divmod(index, k)
            change = int(deltas[i, j])
            work += k * k
            counters["delta_evaluations"] += k * k
            counters["vectorized_scans"] += 1
            if change < 0:
                state.swap(i, j, change); counters["accepted_swaps"] += 1; remember()
            checkpoint("initial_scan" if first_scan_index is None else "descent_scan")
            if first_scan_index is None:
                first_scan_index = len(times_cpu) - 1
            if change >= 0:
                if initial:
                    initial_descent_end_index = len(times_cpu) - 1
                return

    if validation_cpu >= cpu_budget_seconds:
        stop_reason = "cpu_deadline_during_validation"
    else:
        rng = np.random.default_rng(int(seed))
        order = rng.permutation(n)
        degree = a.sum(axis=1, dtype=np.int64)
        subset, details = _initial_subset(a, degree, order, rng, initialization)
        state = _SwapState(a, subset, order, degree)
        initial_cost, initial_subset = state.cost, np.sort(state.inside.copy())
        work = 1
        counters["initial_cut_scores"] = counters["full_cost_evaluations"] = 1
        remember(); checkpoint("initialization")
        if stop_reason is None:
            descend(initial=True)

    if stop_reason is None and work >= max_proposals:
        stop_reason = "max_proposals"
    if stop_reason is None:
        # Deliberately AFTER the initial descent; no annealing setup delays it.
        positive = a[a > 0]
        mean_weight = float(positive.mean()) if len(positive) else 1.
        mean_degree = float(np.count_nonzero(a, axis=1).mean())
        high = max(1., mean_weight * math.sqrt(max(1., mean_degree)))
        low = max(.05, mean_weight / 20.)
        epoch_length, chunk_length, cycle = 8 * n, 32, 0
        checkpoint("anneal_setup")
        while stop_reason is None:
            used = 0
            while used < epoch_length and stop_reason is None:
                chunk = min(chunk_length, epoch_length - used, max_proposals - work)
                if chunk <= 0:
                    stop_reason = "max_proposals"
                    break
                for _ in range(chunk):
                    i, j = int(rng.integers(k)), int(rng.integers(k))
                    change = state.delta(i, j)
                    temperature = high * (low / high) ** (used / max(1, epoch_length - 1))
                    if change <= 0 or rng.random() < math.exp(-change / temperature):
                        state.swap(i, j, change); counters["accepted_swaps"] += 1; remember()
                    used += 1; work += 1
                    counters["delta_evaluations"] += 1; counters["anneal_proposals"] += 1
                checkpoint("anneal")
            if stop_reason is not None:
                break
            descend()
            if stop_reason is not None:
                break
            cycle += 1
            if cycle % 4 == 0:
                if work >= max_proposals:
                    stop_reason = "max_proposals"; break
                state.load(order[rng.permutation(n)[:k]])
                work += 1; counters["full_restart_cut_scores"] += 1
                counters["full_cost_evaluations"] += 1; counters["uniform_restarts"] += 1
                remember(); checkpoint("uniform_restart")
            else:
                state.load(best_subset); counters["full_cost_evaluations"] += 1
                count = min(k, max(2, k // 3), max_proposals - work)
                if count <= 0:
                    stop_reason = "max_proposals"; break
                ins = rng.choice(k, size=count, replace=False)
                outs = rng.choice(k, size=count, replace=False)
                for i, j in zip(ins, outs):
                    state.swap(int(i), int(j)); work += 1
                    counters["delta_evaluations"] += 1; counters["accepted_swaps"] += 1; remember()
                counters["perturbations"] += 1; checkpoint("perturb_best")
            if stop_reason is None:
                descend()

    trace = {"cpu_seconds": np.asarray(times_cpu, dtype=float),
             "wall_seconds": np.asarray(times_wall, dtype=float),
             "best_cut": np.asarray(cuts, dtype=np.int64),
             "best_subset_packbits_little": np.asarray(masks, dtype=np.uint8).reshape((-1, (n + 7) // 8)),
             "proposal_count": np.asarray(work_trace, dtype=np.int64), "stage": stages}
    eligible = np.flatnonzero(trace["cpu_seconds"] <= cpu_budget_seconds)
    eligible_index = int(eligible[-1]) if len(eligible) else None
    eligible_subset = _unpack(trace["best_subset_packbits_little"][eligible_index], n) if eligible_index is not None else None
    overall_subset = np.sort(best_subset) if best_subset is not None else None
    end_cpu, end_wall = _clock()
    compute_cpu, compute_wall = end_cpu - cpu_start, end_wall - wall_start
    guard_stopped = guard_blocked_scan or stop_reason == "max_proposals"
    last_checkpoint_cpu = times_cpu[-1] if times_cpu else validation_cpu
    early_guard = guard_stopped and last_checkpoint_cpu < cpu_budget_seconds
    first_scan_timely = first_scan_index is not None and times_cpu[first_scan_index] <= cpu_budget_seconds
    initial_descent_timely = initial_descent_end_index is not None and times_cpu[initial_descent_end_index] <= cpu_budget_seconds
    return {"algorithm": "P50_from_raw_descent_first_v1", "initialization": initialization,
            "n": n, "seed": int(seed), "cpu_budget_seconds": cpu_budget_seconds,
            "max_proposals": max_proposals, "best_cut": int(cuts[eligible_index]) if eligible_index is not None else None,
            "best_subset": eligible_subset, "has_eligible_result": eligible_index is not None,
            "comparison_acceptance_eligible": eligible_index is not None and not early_guard,
            "eligible_checkpoint_index": eligible_index,
            "eligible_checkpoint_cpu_seconds": times_cpu[eligible_index] if eligible_index is not None else None,
            "eligible_checkpoint_wall_seconds": times_wall[eligible_index] if eligible_index is not None else None,
            "initial_cut": initial_cost, "initial_subset": initial_subset,
            "initialization_completed_before_deadline": bool(times_cpu and times_cpu[0] <= cpu_budget_seconds),
            "first_scan_completed_before_deadline": first_scan_timely,
            "initial_descent_completed_before_deadline": initial_descent_timely,
            "overall_completed_best_cut": best_cost, "overall_completed_best_subset": overall_subset,
            "last_completed_checkpoint_index": len(times_cpu) - 1 if times_cpu else None,
            "stop_reason": stop_reason, "cap_hit": work >= max_proposals,
            "guard_blocked_full_scan": guard_blocked_scan, "early_cap_inconclusive": early_guard,
            "early_wall_inconclusive": False, "proposal_count": work, "counters": counters,
            "compute_cpu_seconds": compute_cpu, "compute_wall_seconds": compute_wall,
            "cpu_overrun_seconds": max(0., compute_cpu - cpu_budget_seconds),
            "validation_cpu_seconds": validation_cpu, "validation_wall_seconds": validation_wall,
            "initialization_details": details, "trace": trace,
            "free_incumbent_used": False, "external_features_used": False,
            "proposal_cap_is_cost_equivalent": False,
            "timing_convention": "API entry: raw conversion/validation/own features/init/descent/search/compact traces; JSON+I/O excluded"}


def json_safe_result(value):
    """Explicitly outside measured solve; this helper never writes files."""
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: json_safe_result(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_safe_result(item) for item in value]
    return value
