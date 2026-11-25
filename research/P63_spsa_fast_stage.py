"""P63 B + fixed FAST DEV veto only; no accepted positive or QPU interface.

Execution requires a separately reviewed, frozen source/contract and numerical
slot. Importing this module never constructs a graph, circuit, RNG or sampler.
The only project dependencies are the immutable P43 optical factory and P50
from-raw search. Native Perceval construction occurs only in a requested batch.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from fractions import Fraction
import gzip
import hashlib
import io
import json
import math
import os
from pathlib import Path
import time

THREAD_VARIABLES = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                    "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
for _variable in THREAD_VARIABLES:
    os.environ[_variable] = "1"
_IMPORT_WALL, _IMPORT_CPU = time.perf_counter(), time.process_time()
import networkx as nx
import numpy as np
import P43_global_gain_probe as base
import P50_fast_from_scratch as fast
SCIENCE_IMPORT_TIMING = {"wall_seconds": time.perf_counter() - _IMPORT_WALL,
                         "cpu_seconds": time.process_time() - _IMPORT_CPU}

D, N, K = 6, 18, 9
PARAMETERS = tuple((b, i) for b in (1, 2) for i in range(1, 6))
ARMS = ("bosonic", "j_aligned", "continuous_phase", "distinguishable",
        "independent_B_marginals", "uniform_subset", "phase_average")
TRAINED_ARMS = ARMS[:3]
FAST_MODES = ("random", "spectral")
NAMESPACES = {"embedding": 6318000, "direction": 6320000,
              "batch": 6330000, "FAST": 6340000}
TOLERANCE = 3e-12
FAST_MAX_PROPOSALS = 10000


class RetainedFailure(RuntimeError):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = {} if evidence is None else evidence


class Meter:
    def __init__(self):
        self.wall = self.cpu = 0.0

    @contextmanager
    def measure(self):
        wall, cpu = time.perf_counter(), time.process_time()
        try:
            yield
        finally:
            self.wall += time.perf_counter() - wall
            self.cpu += time.process_time() - cpu

    def record(self):
        return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}


def seed_for(*parts):
    """Same immutable SHA256/first-four/little-endian convention as P43/P50."""
    return int.from_bytes(hashlib.sha256("/".join(map(str, parts)).encode()).digest()[:4], "little")


def expected_spec():
    return {
        "phase": "P63_B_FAST_STAGE1", "positive_acceptance_allowed": False,
        "d": 6, "N": 18, "K": 9, "source": [1]*18, "ideal_transmission_eta": 1,
        "parameters": [list(p) for p in PARAMETERS], "initial_theta": ["0"]*10,
        "mixer_ports": [0, 6], "mixer_numerators": [[3, -4], [4, 3]], "mixer_denominator": 5,
        "cases": [{"id": "n18_ER_6301801", "family": "ER", "seed": 6301801},
                  {"id": "n18_RR_6301802", "family": "RR", "seed": 6301802}],
        "ER_p": "6/17", "RR_degree": 6, "weights": [1, 5],
        "arms_seed_frozen": list(ARMS), "trained_arms": list(TRAINED_ARMS),
        "seed_namespaces": dict(NAMESPACES), "seed_recipe": "P43_SHA256_first4_little",
        "steps": 3, "a": "1/2", "c": "1/4", "training_draws_per_sign": 4,
        "common_delta_across_signs": True, "fresh_trials": 2, "fresh_draws_per_trial": 8,
        "flat_control_future_batches": 5, "flat_control_future_draws_per_batch": 8,
        "continuous_phase_law": "z_j=exp(i*phi_j)/sqrt(18),iidUniform[0,2pi);Multinomial(18,abs(Uz)^2)",
        "PNR_law": "abs(per(W[z|x]))^2/(prod(z!)*prod(x!))",
        "C6_support": "sum_i i*M_i == 0 mod6; P(1^18)=0; all collisions retained",
        "numerical_tolerance": TOLERANCE, "clock_tolerance_seconds": 1e-8,
        "FAST_modes": list(FAST_MODES), "FAST_max_proposals": FAST_MAX_PROPOSALS,
        "planned_B_draws": 80, "planned_B_photons": 1440, "planned_native_batches": 16,
        "max_unique_networks_per_case": 7, "maximum_cpu_seconds": 60,
        "maximum_wall_seconds": 90, "maximum_threads": 1,
        "maximum_new_output_bytes": 33554432, "output_reserve_bytes": 1048576,
        "maximum_planned_workspace_bytes": 268435456,
        "optional_models_executed": False, "zero_failed_retries": True,
    }


def batch_plan(arm):
    if arm not in ARMS:
        raise ValueError("Unknown frozen arm")
    if arm in TRAINED_ARMS:
        return [("training", step, sign, 0, 4) for step in range(3) for sign in ("plus", "minus")] + [
            ("evaluation", 3, "final", trial, 8) for trial in range(2)]
    return [("fixed_fresh", 0, "flat", trial, 8) for trial in range(5)]


def batch_seed_roles(case_id, arm, stage, step, sign, trial, draws):
    master = seed_for(NAMESPACES["batch"], case_id, arm, stage, step, sign, trial)
    roles = {"master": master, "observation": seed_for(master, "observation")}
    for shot in range(draws):
        roles[f"priority/{shot}"] = seed_for(master, "priority", shot)
        if arm == "continuous_phase":
            for role in ("coherent_coefficients", "coherent_multinomial"):
                roles[f"{role}/{shot}"] = seed_for(master, role, shot)
        if arm == "phase_average":
            for role, copies in (("F6_source", 3), ("tritter", 6)):
                for copy in range(copies):
                    roles[f"{role}/{shot}/{copy}"] = seed_for(master, role, shot, copy)
    return roles


def seed_namespaces(spec):
    """Metadata only, covering every later arm before any B observation."""
    owners = {}
    def register(label, value):
        if value in owners.values():
            previous = next(key for key, old in owners.items() if old == value)
            raise RetainedFailure("Global seed collision", {"first": previous, "second": label, "seed": value})
        owners[label] = value
    for case in spec["cases"]:
        cid = case["id"]
        register((cid, "graph"), case["seed"])
        register((cid, "weights"), seed_for(case["seed"], "weights"))
        register((cid, "embedding"), seed_for(NAMESPACES["embedding"], cid))
        for mode in FAST_MODES:
            register((cid, "FAST", mode), seed_for(NAMESPACES["FAST"], cid, mode))
        for arm in ARMS:
            if arm in TRAINED_ARMS:
                for step in range(3):
                    register((cid, arm, "direction", step), seed_for(NAMESPACES["direction"], cid, arm, step))
            for stage, step, sign, trial, draws in batch_plan(arm):
                for role, value in batch_seed_roles(cid, arm, stage, step, sign, trial, draws).items():
                    register((cid, arm, stage, step, sign, trial, role), value)
    return owners


def compile_base():
    """One graph-blind compilation, charged one half to each planned case."""
    return tuple(np.asarray([[complex(math.cos(2*math.pi*i*j/m), math.sin(2*math.pi*i*j/m))/math.sqrt(m)
                              for j in range(m)] for i in range(m)], dtype=np.complex128) for m in (3, 6))


def exact_theta(theta):
    if len(theta) != 10 or any(isinstance(t, (bool, float, np.floating)) for t in theta):
        raise ValueError("Ten exact rational angles required")
    return tuple(Fraction(t) for t in theta)


def circuit(theta, base_matrices):
    theta = exact_theta(theta)
    f3, f6 = base_matrices
    phases = {(b, i): complex(math.cos(float(t)), math.sin(float(t))) for (b, i), t in zip(PARAMETERS, theta)}
    u = np.empty((N, N), dtype=np.complex128)
    for a in range(3):
        for i in range(D):
            for b in range(3):
                for j in range(D):
                    u[a*D+i, b*D+j] = f3[a, b]*phases.get((b, i), 1)*f6[i, j]
    row0, row6 = u[0].copy(), u[6].copy()
    u[0], u[6] = (3*row0-4*row6)/5, (4*row0+3*row6)/5
    return u


def expected_q():
    q = np.full((N, N), 1/18)
    q[0] = np.repeat(np.asarray([1, 37, 37])/450, D)
    q[6] = np.repeat(np.asarray([49, 13, 13])/450, D)
    return q


def phase_matrix_diagnostics(u):
    u = np.asarray(u)
    if u.shape != (N, N) or not np.all(np.isfinite(u)):
        raise RetainedFailure("Invalid circuit entries", {"U": u})
    q = abs(u)**2
    column_shift = [b*D+(j+1) % D for b in range(3) for j in range(D)]
    row_phases = np.exp(2j*math.pi*np.tile(np.arange(D), 3)/D)
    receipt = {"q": q, "row_gram_residual": float(abs(u@u.conj().T-np.eye(N)).max()),
               "column_gram_residual": float(abs(u.conj().T@u-np.eye(N)).max()),
               "q_residual": float(abs(q-expected_q()).max()),
               "row_mass_residual": float(abs(q.sum(axis=1)-1).max()),
               "column_mass_residual": float(abs(q.sum(axis=0)-1).max()),
               "C6_matrix_residual": float(abs(u[:, column_shift]-row_phases[:, None]*u).max())}
    if any(value > TOLERANCE for key, value in receipt.items() if key != "q"):
        raise RetainedFailure("Circuit physics diagnostic failed", {"U": u, **receipt})
    return receipt


def c6_support(counts):
    counts = np.asarray(counts)
    if (counts.shape != (N,) or counts.dtype.kind not in "iu" or np.any(counts < 0)
            or np.any(counts > N) or int(counts.sum()) != N):
        return False
    return sum(i*int(counts[a*D+i]) for a in range(3) for i in range(D)) % D == 0


def rank_counts(counts, priority_order, mapping):
    counts = np.asarray(counts)
    n = len(counts)
    if (counts.ndim != 1 or n < 2 or n % 2 or counts.dtype.kind not in "iu" or np.any(counts < 0)
            or sorted(priority_order) != list(range(n)) or sorted(mapping) != list(range(n))):
        raise ValueError("Integer counts and two permutations required")
    priority = {int(port): rank for rank, port in enumerate(priority_order)}
    physical = sorted(range(n), key=lambda port: (-int(counts[port]), priority[port]))[:n//2]
    return sorted(physical), sorted(int(mapping[port]) for port in physical)


def normalized_batch_loss(cuts, total_weight):
    if (not cuts or isinstance(total_weight, bool) or not isinstance(total_weight, (int, np.integer))
            or total_weight <= 0 or any(isinstance(c, (bool, float, np.floating)) or int(c) != c
                                       or not 0 <= c <= total_weight for c in cuts)):
        raise ValueError("Nonempty exact cuts and positive integer total weight required")
    return Fraction(sum(int(c) for c in cuts), len(cuts)*int(total_weight))


def paired_probes(theta, delta, c=Fraction(1, 4)):
    theta = exact_theta(theta)
    if (not isinstance(c, Fraction) or c != Fraction(1, 4) or len(delta) != 10
            or any(x not in (-1, 1) or isinstance(x, bool) for x in delta)):
        raise ValueError("One ten-coordinate Rademacher direction required")
    return tuple(t+c*d for t, d in zip(theta, delta)), tuple(t-c*d for t, d in zip(theta, delta))


def spsa_update(theta, delta, pluscuts, minuscuts, total_weight, a=Fraction(1, 2), c=Fraction(1, 4)):
    theta = exact_theta(theta)
    paired_probes(theta, delta, c)
    if (len(pluscuts) != 4 or len(minuscuts) != 4 or not isinstance(a, Fraction)
            or not isinstance(c, Fraction) or a != Fraction(1, 2) or c != Fraction(1, 4)):
        raise ValueError("Frozen four-shot paired SPSA convention required")
    plusloss, minusloss = (normalized_batch_loss(cuts, total_weight) for cuts in (pluscuts, minuscuts))
    gradient = tuple((plusloss-minusloss)/(2*c)*int(d) for d in delta)
    updated = tuple(t-a*g for t, g in zip(theta, gradient))
    return updated, gradient, plusloss, minusloss


def factory_setup_accounting(total_wall, total_cpu, backend_wall, diagnostic_wall):
    values = (total_wall, total_cpu, backend_wall, diagnostic_wall)
    if any(not math.isfinite(t) or t < 0 for t in values) or backend_wall+diagnostic_wall > total_wall+1e-8:
        raise RetainedFailure("Invalid disjoint setup clocks", {"times": values})
    return {"classical_wall": max(0., total_wall-backend_wall-diagnostic_wall),
            "total_setup_cpu": total_cpu, "factory_total_cpu": total_cpu,
            "backend_wall": backend_wall, "diagnostic_wall": diagnostic_wall,
            "backend_cpu": None, "classical_cpu": None, "CPU_split_available": False}


def configure_native_threads(xq):
    before = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    return {"interface": "exqalibur.Config.compute_max_thread_count", "before": before,
            "requested": 1, "configured_before_work": native_thread_readback(xq)}


def native_thread_readback(xq):
    value = int(xq.Config.compute_max_thread_count)
    if value != 1:
        raise RetainedFailure("Native maximum-thread readback failed", {"observed": value})
    return value


def validated_graph(raw):
    a = np.asarray(raw)
    if (a.ndim != 2 or a.shape[0] != a.shape[1] or len(a) < 2 or len(a) % 2 or a.dtype.kind not in "iu"
            or np.any(a < 0) or np.any(np.diag(a)) or not np.array_equal(a, a.T)):
        raise ValueError("Even symmetric nonnegative integer adjacency required")
    if int(a.max()) > np.iinfo(np.int64).max // (4*len(a)*len(a)):
        raise ValueError("Unsafe graph weight")
    return np.array(a, dtype=np.int64, order="C", copy=True)


def make_graph(case):
    graph = (nx.gnp_random_graph(N, 6/17, seed=case["seed"]) if case["family"] == "ER"
             else nx.random_regular_graph(6, N, seed=case["seed"]))
    rng = np.random.Generator(np.random.PCG64(seed_for(case["seed"], "weights")))
    a = np.zeros((N, N), dtype=np.int64)
    for i, j in sorted(graph.edges()):
        a[i, j] = a[j, i] = int(rng.integers(1, 6))
    return a


def prepare_arm(raw, case, compiler_share):
    preparation = Meter()
    with preparation.measure():
        a = validated_graph(raw)
        if a.shape != (N, N):
            raise ValueError("P63 requires exactly 18 modes")
        denominator = int(a.sum(dtype=np.int64))//2
        if denominator == 0:
            raise RetainedFailure("Zero-weight frozen graph", {"case": case, "adjacency": a})
        mapping_seed = seed_for(NAMESPACES["embedding"], case["id"])
        mapping = np.random.Generator(np.random.PCG64(mapping_seed)).permutation(N).tolist()
        arm = {"case": case["id"], "a": a, "denominator": denominator,
               "mapping": mapping, "mapping_seed": mapping_seed, "networks": {},
               "paid_best": None, "paid_wall": compiler_share, "completed_shots": 0, "attempted_shots": 0}
    arm["preparation"] = preparation.record()
    arm["compiler_shared_wall"] = compiler_share
    arm["paid_wall"] += preparation.wall
    return arm


def serial(value):
    if isinstance(value, np.ndarray):
        return {"real": value.real.tolist(), "imag": value.imag.tolist()} if np.iscomplexobj(value) else value.tolist()
    if isinstance(value, np.generic):
        return serial(value.item())
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    return value


def emit(stream, row):
    stream.write(json.dumps(serial(row), allow_nan=False)+"\n")
    stream.flush()


def save_json(path, value):
    with Path(path).open("x", encoding="utf8") as stream:
        json.dump(serial(value), stream, allow_nan=False, indent=2)
        stream.write("\n")


def write_failure(output, stage, exc, partial):
    value = {"stage": stage, "failure": {"message": str(exc), "error": repr(exc),
             "evidence": getattr(exc, "evidence", {})}, "partial": partial}
    save_json(Path(output)/"failure.json", value)
    return value


def run_batch(arm, theta, label, draws, stream, base_matrices):
    stage, step, sign, trial = label
    setup, diagnostics, factory, generation, post, aggregation = (Meter() for _ in range(6))
    counts, cuts, new_network, roles = None, [], False, {}
    try:
        with setup.measure():
            roles = batch_seed_roles(arm["case"], "bosonic", stage, step, sign, trial, draws)
            key = exact_theta(theta)
            if key not in arm["networks"]:
                if len(arm["networks"]) >= 7:
                    raise RetainedFailure("Unexpected extra phase network")
                u = circuit(key, base_matrices)
                with diagnostics.measure():
                    receipt = phase_matrix_diagnostics(u)
                arm["networks"][key] = {"id": len(arm["networks"]), "theta": key, "U": u, "diagnostics": receipt}
                new_network = True
            context = arm["networks"][key]
            source = list(range(N))
        if new_network:
            emit(stream, {"record_type": "network", "case": arm["case"], **context})
        with setup.measure(), factory.measure():
            draw, backend_wall = base.make_optical_sampler(context["U"], source, "bosonic", roles["observation"])
        if not math.isfinite(backend_wall) or backend_wall < 0 or backend_wall > factory.wall+1e-8:
            raise RetainedFailure("Invalid immutable factory inner WALL", {"factory": factory.record(), "backend_wall": backend_wall})
        accounting = factory_setup_accounting(setup.wall, setup.cpu, backend_wall, diagnostics.wall)
        accounting["factory_total_cpu"] = factory.cpu
        arm["paid_wall"] += accounting["classical_wall"]
        tag = {"case": arm["case"], "arm": "bosonic", "stage": stage, "step": step, "sign": sign,
               "trial": trial, "theta": key, "network_id": context["id"], "seed_roles": roles}
        emit(stream, {"record_type": "batch_setup", **tag, "setup": setup.record(), "factory_total": factory.record(),
                      "accounting": accounting, "matrix_diagnostics": diagnostics.record()})
        for shot in range(draws):
            with post.measure():
                arm["attempted_shots"] += 1
            emit(stream, {"record_type": "shot_requested", **tag, "shot": shot})
            with generation.measure():
                counts, fallback = draw()
            with diagnostics.measure():
                if fallback or not c6_support(counts) or not bool(np.any(np.asarray(counts) > 1)):
                    raise RetainedFailure("Invalid complete ideal PNR/C6/collision result", {"counts": counts, "fallback": fallback})
                totals = [sum(int(counts[a*D+i]) for a in range(3)) for i in range(D)]
            with post.measure():
                priority_seed = roles[f"priority/{shot}"]
                order = np.random.Generator(np.random.PCG64(priority_seed)).permutation(N).tolist()
                physical, subset = rank_counts(counts, order, arm["mapping"])
                value = base.cut(arm["a"], subset)
                cuts.append(value)
                arm["completed_shots"] += 1
                if arm["paid_best"] is None or value < arm["paid_best"]["cut"]:
                    arm["paid_best"] = {"cut": value, "subset": subset, "physical_subset": physical,
                                        "stage": stage, "step": step, "sign": sign, "trial": trial, "shot": shot}
            emit(stream, {"record_type": "shot", **tag, "shot": shot, "counts": counts,
                          "total_count": N, "color_totals": totals, "C6_residue": 0, "collision": True,
                          "priority_order": order, "physical_subset": physical, "subset": subset, "cut": value})
        with aggregation.measure():
            loss = normalized_batch_loss(cuts, arm["denominator"])
        arm["paid_wall"] += post.wall+aggregation.wall
        record = {**tag, "proposals": draws, "cuts": cuts, "normalized_mean": loss,
                  "setup": setup.record(), "factory_total": factory.record(), "setup_accounting": accounting,
                  "count_generation": generation.record(), "physics_diagnostics": diagnostics.record(),
                  "postprocessing": post.record(), "aggregation": aggregation.record()}
        emit(stream, {"record_type": "batch_complete", **record})
        return record
    except Exception as error:
        evidence = {"case": arm["case"], "label": label, "theta": theta, "seed_roles": roles,
                    "counts": counts, "completed_cuts": cuts, "setup": setup.record(), "factory_total": factory.record(),
                    "count_generation": generation.record(), "physics_diagnostics": diagnostics.record(),
                    "postprocessing": post.record(), "error": repr(error), "cause_evidence": getattr(error, "evidence", {})}
        emit(stream, {"record_type": "failed_batch", **evidence})
        raise RetainedFailure("First batch failure; no resampling", evidence) from error


def run_trajectory(arm, stream, base_matrices, guard):
    theta, records, trajectory = (Fraction(0),)*10, [], []
    for step in range(3):
        direction_time = Meter()
        with direction_time.measure():
            direction_seed = seed_for(NAMESPACES["direction"], arm["case"], "bosonic", step)
            delta = (2*np.random.Generator(np.random.PCG64(direction_seed)).integers(0, 2, size=10)-1).tolist()
            plus, minus = paired_probes(theta, delta)
        arm["paid_wall"] += direction_time.wall
        emit(stream, {"record_type": "paired_probe", "case": arm["case"], "step": step,
                      "theta": theta, "delta": delta, "direction_seed": direction_seed,
                      "plus_theta": plus, "minus_theta": minus, "direction_compute": direction_time.record()})
        paired = []
        for sign, probe in (("plus", plus), ("minus", minus)):
            guard()
            row = run_batch(arm, probe, ("training", step, sign, 0), 4, stream, base_matrices)
            records.append(row)
            paired.append(row)
        update = Meter()
        with update.measure():
            updated, gradient, lp, lm = spsa_update(theta, delta, paired[0]["cuts"], paired[1]["cuts"], arm["denominator"])
            item = {"step": step, "theta_before": theta, "delta": delta, "plus_loss": lp,
                    "minus_loss": lm, "gradient": gradient, "theta_after": updated}
            trajectory.append(item)
            theta = updated
        arm["paid_wall"] += update.wall
        item["compute"] = update.record()
        emit(stream, {"record_type": "update", "case": arm["case"], **item})
    emit(stream, {"record_type": "frozen_final_theta", "case": arm["case"], "theta": theta,
                  "trajectory": trajectory, "selected_iterate": 3, "frozen_before_fresh": True})
    for trial in range(2):
        guard()
        records.append(run_batch(arm, theta, ("evaluation", 3, "final", trial), 8, stream, base_matrices))
    final = Meter()
    with final.measure():
        fresh_cuts = [cut for row in records if row["stage"] == "evaluation" for cut in row["cuts"]]
        fresh_mean = normalized_batch_loss(fresh_cuts, arm["denominator"])
        result = {"case": arm["case"], "B_paid_best": arm["paid_best"]["cut"], "B_paid_best_record": arm["paid_best"],
                  "B_fresh_normalized_mean": fresh_mean, "trajectory": trajectory, "theta_final": theta,
                  "records": records, "completed_shots": arm["completed_shots"], "FAST": {}}
    arm["paid_wall"] += final.wall
    result["B_classical_wall"] = arm["paid_wall"]
    result["final_aggregation"] = final.record()
    return result


def fast_summary(result):
    budget = result["cpu_budget_seconds"]
    timestamp = result["eligible_checkpoint_cpu_seconds"]
    best = result["best_cut"]
    prefix = (result["has_eligible_result"] and best is not None and timestamp is not None
              and math.isfinite(timestamp) and 0 <= timestamp <= budget and result["best_snapshot_cached_online"])
    acceptance = (prefix and result["comparison_acceptance_eligible"] and not result["early_cap_inconclusive"]
                  and not result["early_wall_inconclusive"] and result["first_scan_completed_before_deadline"])
    return {"prefix_eligible_for_veto": bool(prefix), "comparison_acceptance_eligible": bool(acceptance),
            "best_cut": best if prefix else None, "first_scan_completed_before_deadline": result["first_scan_completed_before_deadline"],
            "eligible_checkpoint_cpu_seconds": timestamp, "cpu_budget_seconds": budget,
            "early_cap_inconclusive": result["early_cap_inconclusive"], "early_wall_inconclusive": result["early_wall_inconclusive"]}


def fast_comparison(raw, case_id, B_classical_wall, mode):
    adapter = Meter()
    with adapter.measure():
        seed = seed_for(NAMESPACES["FAST"], case_id, mode)
        allowance = float(B_classical_wall)
        max_proposals = FAST_MAX_PROPOSALS
    solver_allowance = max(0., allowance-adapter.cpu)
    result = fast.solve_from_raw(raw, seed=seed, initialization=mode,
                                 cpu_budget_seconds=solver_allowance, max_proposals=max_proposals)
    if len(result["trace"]["cpu_seconds"]) > FAST_MAX_PROPOSALS:
        raise RetainedFailure("Unexpected FAST trace bound", {"case": case_id, "mode": mode})
    return {**fast_summary(result), "case": case_id, "mode": mode, "seed": seed,
            "B_classical_WALL_allowance": allowance, "adapter": adapter.record(), "solver_CPU_allowance": solver_allowance,
            "result": result, "optical_latency_assumed_seconds": 0, "serialization_granted_seconds": 0,
            "other_arm_seconds_granted": 0, "hardware_time_measured": False}


def classify_stage1(graph_records):
    complete = (len(graph_records) == 2 and len({row["case"] for row in graph_records}) == 2
                and all(set(row["FAST"]) == set(FAST_MODES) for row in graph_records))
    vetoes = [mode for mode in FAST_MODES if complete and all(
        row["FAST"][mode]["prefix_eligible_for_veto"] and row["FAST"][mode]["best_cut"] is not None
        and row["FAST"][mode]["best_cut"] <= row["B_paid_best"] for row in graph_records)]
    eligible = complete and all(row["FAST"][mode]["comparison_acceptance_eligible"]
                                for row in graph_records for mode in FAST_MODES)
    status = ("DEV_REJECTED_FIXED_FAST" if vetoes else "INCONCLUSIVE_FAST_ELIGIBILITY" if not eligible
              else "STAGE1_OPTIONAL_CONTROLS_REQUIRED")
    return {"status": status, "positive_accepted": False, "fixed_FAST_veto_modes": vetoes,
            "FAST_all_comparison_eligible": bool(eligible), "optional_controls_passed": False,
            "optional_models": {arm: "NOT_RUN_DUE_FAST_VETO" if vetoes else "NOT_RUN_STAGE1_SCOPE" for arm in ARMS[1:]}}


def check_output(output):
    if sum(path.stat().st_size for path in Path(output).rglob("*") if path.is_file()) > 33554432-1048576:
        raise RetainedFailure("Scientific output reserve exhausted; no retry")


def execute(spec, output):
    output = Path(output)
    if spec != expected_spec():
        raise ValueError("Frozen P63 stage1 spec differs")
    output.mkdir(parents=True, exist_ok=False)
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    arms, graphs, results, native, graph_generation = {}, {}, [], {}, {}
    failure, stage = None, "metadata"
    raw_path = output/"raw.jsonl.gz"
    def guard():
        check_output(output)
        if time.perf_counter()-_IMPORT_WALL >= 90 or time.process_time()-_IMPORT_CPU >= 60:
            raise RetainedFailure("Frozen resource cap reached")
    with raw_path.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped, encoding="utf8") as stream:
            try:
                owner_table = seed_namespaces(spec)
                save_json(output/"seed_namespaces.json", [{"role": list(key), "seed": value} for key, value in owner_table.items()])
                stage = "native_configuration"
                native_import = Meter()
                with native_import.measure():
                    import exqalibur as xq
                native = configure_native_threads(xq)
                native["exqalibur_import"] = native_import.record()
                perceval_import = Meter()
                with perceval_import.measure():
                    import perceval as _pcvl  # Import separately; no circuit, source or draw.
                native["perceval_import"] = perceval_import.record()
                native["readback_after_imports"] = native_thread_readback(xq)
                stage = "shared_compiler"
                compiler = Meter()
                with compiler.measure():
                    base_matrices = compile_base()
                for case in spec["cases"]:
                    guard()
                    stage = f"graph/{case['id']}"
                    supplied = Meter()
                    with supplied.measure():
                        graphs[case["id"]] = make_graph(case)
                    graph_generation[case["id"]] = supplied.record()
                    emit(stream, {"record_type": "supplied_graph", "case": case, "adjacency": graphs[case["id"]],
                                  "excluded_graph_generation": supplied.record()})
                    stage = f"B/{case['id']}"
                    arm = prepare_arm(graphs[case["id"]], case, compiler.wall/2)
                    arms[case["id"]] = arm
                    save_json(output/f"context_{case['id']}.json", {"case": case, "adjacency": arm["a"],
                              "mode_to_vertex": arm["mapping"], "mapping_seed": arm["mapping_seed"],
                              "compiler": compiler.record(), "compiler_share": compiler.wall/2,
                              "preparation": arm["preparation"]})
                    results.append(run_trajectory(arm, stream, base_matrices, guard))
                aggregate = Meter()
                with aggregate.measure():
                    global_fresh_mean = sum((row["B_fresh_normalized_mean"] for row in results), Fraction(0))/2
                for result in results:
                    arms[result["case"]]["paid_wall"] += aggregate.wall/2
                    result["B_classical_wall"] = arms[result["case"]]["paid_wall"]
                    result["B_global_mean_aggregation_share"] = aggregate.wall/2
                    save_json(output/f"B_{result['case']}.json", result)
                emit(stream, {"record_type": "B_equal_graph_fresh_mean", "mean": global_fresh_mean,
                              "paid_compute": aggregate.record(), "cost_share_per_case": aggregate.wall/2})
                for result in results:
                    for mode in FAST_MODES:
                        guard()
                        stage = f"FAST/{result['case']}/{mode}"
                        comparison = fast_comparison(graphs[result["case"]], result["case"], result["B_classical_wall"], mode)
                        result["FAST"][mode] = comparison
                        save_json(output/f"FAST_{result['case']}_{mode}.json", comparison)
                guard()
                summary = classify_stage1(results)
                summary.update(B_equal_graph_fresh_normalized_mean=global_fresh_mean,
                               B_global_mean_aggregation=aggregate.record())
            except Exception as error:
                failure = {"stage": stage, "error": repr(error), "evidence": getattr(error, "evidence", {})}
                emit(stream, {"record_type": "first_failure", **failure})
                write_failure(output, stage, error, {"completed_result_cases": [row["case"] for row in results],
                              "FAST_saved_modes": {row["case"]: list(row["FAST"]) for row in results},
                              "completed_shots": {cid: arm["completed_shots"] for cid, arm in arms.items()},
                              "attempted_shots": {cid: arm["attempted_shots"] for cid, arm in arms.items()}})
                summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "failure": failure}
            if native:
                try:
                    native["readback_after_work"] = native_thread_readback(xq)
                except Exception as error:
                    native["readback_failure"] = repr(error)
                    if failure is None:
                        failure = {"stage": "native_readback", "error": repr(error), "evidence": getattr(error, "evidence", {})}
                        emit(stream, {"record_type": "first_failure", **failure})
                        write_failure(output, "native_readback", error,
                                      {"completed_result_cases": [row["case"] for row in results]})
                        summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "failure": failure}
    summary.update(results=results, native_threads=native, supplied_graph_generation_excluded=graph_generation,
                   science_import_excluded=SCIENCE_IMPORT_TIMING,
                   completed_B_shots=sum(arm["completed_shots"] for arm in arms.values()),
                   attempted_B_shots=sum(arm["attempted_shots"] for arm in arms.values()),
                   simulated_injected_B_photons=N*sum(arm["attempted_shots"] for arm in arms.values()),
                   B_paid_best_cached_online={cid: arm["paid_best"] for cid, arm in arms.items()},
                   B_paid_classical_wall={cid: arm["paid_wall"] for cid, arm in arms.items()},
                   cpu_seconds_inside_execute=time.process_time()-started_cpu,
                   wall_seconds_inside_execute=time.perf_counter()-started_wall,
                   raw_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   actual_QPU_calls=0, actual_QPU_photons=0, heldout_opened=False, optimum_used=False,
                   other_models_executed=False, B_CPU_split_available=False,
                   hardware_runtime_measured=False, diagnostics_and_IO_granted_to_FAST=False)
    # Size the last duplicated trace rendering BEFORE writing any final status.
    # A lean failure summary fits the already reserved MiB; raw/per-call files
    # retain all completed evidence, without duplicating it into failure.json.
    final_bytes = len((json.dumps(serial(summary), allow_nan=False, indent=2)+"\n").encode("utf8"))
    existing_bytes = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    if existing_bytes+final_bytes > 33554432-1048576:
        if failure is None:
            error = RetainedFailure("Final summary would exhaust scientific-output reserve",
                                    {"existing_bytes": existing_bytes, "summary_bytes": final_bytes})
            failure = write_failure(output, "finalization", error,
                                    {"completed_B_shots": summary["completed_B_shots"], "raw_path": raw_path.name})
        summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "failure": failure,
                   "completed_B_shots": summary["completed_B_shots"], "raw_sha256": summary["raw_sha256"],
                   "full_summary_omitted_due_output_cap": True, "completed_evidence_retained_in_raw_and_per_call_files": True}
    if failure is None:
        save_json(output/"failure.json", {"failure": None})
    save_json(output/"summary.json", summary)
    return summary, failure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    summary, failure = execute(spec, args.output)
    print(json.dumps({"status": summary["status"], "completed_B_shots": summary["completed_B_shots"], "positive_accepted": False}))
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
