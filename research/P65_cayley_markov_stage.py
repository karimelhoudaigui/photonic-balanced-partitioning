"""P65 B80 then fixed FAST veto; no optional execution, positive or QPU call.

Import constructs no graph, RNG, matrix, source or native backend. Scientific
execution needs the separately reviewed frozen closure and numerical slot.
Only immutable P43/P50 helpers are project dependencies.
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
SCIENCE_IMPORT_TIMING = {"wall_seconds": time.perf_counter()-_IMPORT_WALL,
                         "cpu_seconds": time.process_time()-_IMPORT_CPU}

N, K = 20, 10
OPTICAL_ARMS = ("bosonic", "distinguishable", "species4")
OPTIONAL_ARMS = ("distinguishable", "species4", "r2", "r3")
FAST_MODES = ("random", "spectral")
CANDIDATES = tuple((t, lam) for t in (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2))
                   for lam in (Fraction(0), Fraction(1, 4)))
ROOTS = {"start": 65100000, "count": 65200000, "coin": 65300000,
         "replacement": 65400000, "FAST": 65500000}
SPEC_SHA256 = "6993da4efe018c80b7fd9021451fad301dd665b1c86c4eac8adab2b1904eeee4"
SPEC_PATH = Path(__file__).with_name("P65_cayley_markov_dev_spec.json")
TOLERANCE, CLOCK_TOLERANCE = 3e-12, 1e-8
FAST_MAX_PROPOSALS, FAST_MAX_CHECKPOINTS = 10000, 20002
MAX_OUTPUT, OUTPUT_RESERVE = 33554432, 1048576


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
            self.wall += time.perf_counter()-wall
            self.cpu += time.process_time()-cpu

    def record(self):
        return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}


def charge(arm, label, wall, cpu=None):
    """Evidence bookkeeping outside algorithm meters; no invented CPU split."""
    if not math.isfinite(wall) or wall < 0 or (cpu is not None and (not math.isfinite(cpu) or cpu < 0)):
        raise RetainedFailure("invalid paid component", {"label": label, "wall": wall, "cpu": cpu})
    record = {"label": label, "wall_seconds": wall, "cpu_seconds": cpu}
    arm.setdefault("paid_components", []).append(record)
    arm["paid_wall"] += wall
    return record


def read_spec(path=SPEC_PATH):
    payload = Path(path).read_bytes()
    if hashlib.sha256(payload).hexdigest() != SPEC_SHA256:
        raise ValueError("Frozen P65 design spec bytes differ")
    return json.loads(payload)


def seed_for(*parts):
    return base.seed_for(*parts)


def attempt_roles(case, arm, stage, parameter, chain, step):
    if arm not in OPTICAL_ARMS + ("r2", "r3"):
        raise ValueError("unknown frozen arm")
    labels = (case, arm, stage, parameter, chain, step)
    roles = {"coin": seed_for(ROOTS["coin"], *labels)}
    roles["count" if arm in OPTICAL_ARMS else "replacement"] = seed_for(
        ROOTS["count"] if arm in OPTICAL_ARMS else ROOTS["replacement"], *labels)
    return roles


def seed_namespaces(spec):
    """Metadata only, ALL five arms; common starts are deliberate references."""
    table, used = {}, {}
    def register(label, value, native=False):
        if value in used or (native and value == 0):
            raise RetainedFailure("Seed collision or zero native seed", {
                "first": used.get(value), "second": label, "seed": value})
        used[value] = label
        table[label] = value
    for case in spec["cases"]:
        cid = case["id"]
        register((cid, "graph"), case["seed"])
        register((cid, "weights"), seed_for(case["seed"], "weights"))
        register((cid, "start", "training", 0), seed_for(ROOTS["start"], cid, "training", 0))
        for chain in range(5):
            register((cid, "start", "fresh", chain), seed_for(ROOTS["start"], cid, "fresh", chain))
        for arm in OPTICAL_ARMS + ("r2", "r3"):
            labels = ([("training", p, 0, j) for p in range(8) for j in range(2)] +
                      [("fresh", "selected", c, j) for c in range(3) for j in range(8)]
                      if arm in OPTICAL_ARMS else
                      [("fresh", "fixed", c, j) for c in range(5) for j in range(8)])
            for stage, parameter, chain, step in labels:
                for role, value in attempt_roles(cid, arm, stage, parameter, chain, step).items():
                    register((cid, arm, stage, parameter, chain, step, role), value,
                             native=(role == "count"))
        for mode in FAST_MODES:
            register((cid, "FAST", mode), seed_for(ROOTS["FAST"], cid, mode))
    return table


def validated_graph(raw):
    a = np.asarray(raw)
    if (a.ndim != 2 or a.shape[0] != a.shape[1] or len(a) < 2 or len(a) % 2
            or a.dtype.kind not in "iu" or np.any(a < 0) or np.any(np.diag(a))
            or not np.array_equal(a, a.T)):
        raise ValueError("even symmetric nonnegative integer adjacency required")
    if int(a.max()) > np.iinfo(np.int64).max // (4*len(a)**2):
        raise ValueError("unsafe graph weights")
    return np.array(a, dtype=np.int64, order="C", copy=True)


def make_graph(case):
    graph = (nx.gnp_random_graph(N, 6/19, seed=case["seed"]) if case["family"] == "ER"
             else nx.random_regular_graph(6, N, seed=case["seed"]))
    rng = np.random.Generator(np.random.PCG64(seed_for(case["seed"], "weights")))
    a = np.zeros((N, N), dtype=np.int64)
    for i, j in sorted((min(u, v), max(u, v)) for u, v in graph.edges()):
        a[i, j] = a[j, i] = int(rng.integers(1, 6))
    return a


def cayley_matrix(a, t, lam):
    """Small synthetic sizes allowed; MAIN validates N20 separately."""
    t, lam = Fraction(t), Fraction(lam)
    if t < 0 or lam < 0:
        raise ValueError("nonnegative frozen Cayley parameters required")
    n = len(a)
    degrees = np.asarray(a).sum(axis=1, dtype=np.int64)
    scale = max(Fraction(1), Fraction(int(degrees.max())) + lam*(n-1))
    h = (np.asarray(a, dtype=float) + float(lam)*(np.ones((n, n))-np.eye(n))) / float(scale)
    eye = np.eye(n, dtype=np.complex128)
    u = np.linalg.solve(eye-1j*float(t)*h, eye+1j*float(t)*h)
    return u, {"t": t, "lambda": lam, "weighted_degrees": degrees,
               "denominator": scale, "H": h}


def matrix_diagnostics(u):
    u = np.asarray(u)
    if u.ndim != 2 or u.shape[0] != u.shape[1] or not np.all(np.isfinite(u)):
        raise RetainedFailure("invalid circuit entries", {"U": u})
    q, eye = abs(u)**2, np.eye(len(u))
    result = {"Udagger_U": float(abs(u.conj().T@u-eye).max()),
              "U_Udagger": float(abs(u@u.conj().T-eye).max()),
              "transpose_symmetry": float(abs(u-u.T).max()),
              "q_row_mass": float(abs(q.sum(axis=1)-1).max()),
              "q_column_mass": float(abs(q.sum(axis=0)-1).max())}
    if any(not math.isfinite(value) or value > TOLERANCE for value in result.values()):
        raise RetainedFailure("Cayley diagnostics failed; no repair", {"residuals": result, "U": u})
    return result


def validated_source(source, n=N, k=K):
    source = list(source)
    if (len(source) != k or any(isinstance(i, (bool, np.bool_)) or not isinstance(i, (int, np.integer))
                              for i in source) or source != sorted(source)
            or len(set(source)) != k or any(not 0 <= int(i) < n for i in source)):
        raise RetainedFailure("invalid distinct sorted current source", {"source": source})
    return [int(i) for i in source]


def classify_counts(counts, fallback, n=N, k=K):
    counts = np.asarray(counts)
    if (bool(fallback) or counts.shape != (n,) or counts.dtype.kind not in "iu"
            or np.any(counts < 0) or np.any(counts > k) or int(counts.sum()) != k):
        raise RetainedFailure("invalid complete eta1 PNR result", {"counts": counts, "fallback": fallback})
    collision = bool(np.any(counts > 1))
    subset = None if collision else [int(i) for i in np.flatnonzero(counts)]
    return counts, collision, subset


def normalized_mean(cuts, total_weight):
    if (not cuts or type(total_weight) is not int or total_weight <= 0
            or any(type(c) is not int or not 0 <= c <= total_weight for c in cuts)):
        raise RetainedFailure("invalid exact normalized cuts", {"cuts": cuts, "W": total_weight})
    return Fraction(sum(cuts), len(cuts)*total_weight)


def choose_candidate(fitnesses):
    if len(fitnesses) != 8 or any(not isinstance(value, Fraction) for value in fitnesses):
        raise ValueError("eight exact Fraction fitnesses required")
    return min(range(8), key=lambda index: (fitnesses[index], index))


def factory_accounting(total_wall, total_cpu, backend_wall):
    if (any(not math.isfinite(value) or value < 0 for value in (total_wall, total_cpu, backend_wall))
            or backend_wall > total_wall+CLOCK_TOLERANCE):
        raise RetainedFailure("invalid factory inner WALL", {
            "total_wall": total_wall, "total_cpu": total_cpu, "returned_backend_wall": backend_wall})
    return {"classical_prefix_wall": max(0., total_wall-backend_wall),
            "factory_total_cpu": total_cpu, "factory_total_wall": total_wall,
            "returned_backend_wall": backend_wall, "backend_cpu": None,
            "classical_prefix_cpu": None, "CPU_split_available": False}


def serial(value):
    if isinstance(value, np.ndarray):
        return serial({"real": value.real.tolist(), "imag": value.imag.tolist()}
                      if np.iscomplexobj(value) else value.tolist())
    if isinstance(value, np.generic):
        return serial(value.item())
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return {"nonfinite_float": repr(value)}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return {"unsupported_evidence_type": type(value).__name__, "repr": repr(value)}


def emit(stream, value):
    stream.write(json.dumps(serial(value), allow_nan=False)+"\n")
    stream.flush()


def save_json(path, value):
    with Path(path).open("x", encoding="utf8") as stream:
        json.dump(serial(value), stream, allow_nan=False, indent=2)
        stream.write("\n")


def score(arm, subset, kind, label):
    value = base.cut(arm["a"], subset)
    if type(value) is not int or not 0 <= value <= arm["W"]:
        raise RetainedFailure("invalid exact cut", {"subset": subset, "cut": value})
    arm["score_counts"][kind] += 1
    if arm["paid_best"] is None or value < arm["paid_best"]["cut"]:
        arm["paid_best"] = {"cut": value, "subset": list(subset), "label": label, "score_kind": kind}
    return value


def uniform_start(arm, stage, chain):
    seed = seed_for(ROOTS["start"], arm["case"], stage, chain)
    source = sorted(np.random.Generator(np.random.PCG64(seed)).permutation(N)[:K].tolist())
    return validated_source(source), seed


def prepare_arm(raw, case, stream):
    preparation, compilation, diagnostics = Meter(), Meter(), Meter()
    with preparation.measure():
        a = validated_graph(raw)
        if a.shape != (N, N):
            raise RetainedFailure("main requires N20")
        total_weight = int(a.sum(dtype=np.int64))//2
        if total_weight <= 0:
            raise RetainedFailure("zero-weight frozen case; no replacement")
        arm = {"case": case["id"], "model": "bosonic", "a": a, "W": total_weight,
               "networks": [], "paid_wall": 0., "paid_best": None,
               "attempted": 0, "completed": 0, "score_counts": {"initial": 0, "proposal": 0, "current": 0}}
    for index, (t, lam) in enumerate(CANDIDATES):
        with compilation.measure():
            u, construction = cayley_matrix(a, t, lam)
            network = {"id": index, "U": u, "construction": construction}
            arm["networks"].append(network)
        with diagnostics.measure():
            receipt = matrix_diagnostics(u)
        emit(stream, {"record_type": "candidate_network", "case": arm["case"],
                      **network, "diagnostics": receipt})
    charge(arm, ("preparation",), preparation.wall, preparation.cpu)
    charge(arm, ("compilation",), compilation.wall, compilation.cpu)
    arm["preparation"] = preparation.record()
    arm["compilation"] = compilation.record()
    arm["excluded_matrix_diagnostics"] = diagnostics.record()
    return arm


def run_attempt(arm, chain_state, candidate, labels, beta, stream, factory=None, coin_draw=None):
    """Injectable only for synthetic qualification; MAIN passes immutable P43."""
    factory = base.make_optical_sampler if factory is None else factory
    setup, native_setup, generation, post = (Meter() for _ in range(4))
    counts, fallback, backend_wall, accounting, roles = None, None, None, None, {}
    event = {}
    try:
        with setup.measure():
            stage, parameter, chain, step = labels
            source = validated_source(chain_state["current"])
            source_before = list(source)
            if not 0 <= candidate < 8 or not math.isfinite(beta) or beta < 0:
                raise RetainedFailure("invalid candidate or beta")
            roles = attempt_roles(arm["case"], arm["model"], stage, parameter, chain, step)
            arm["attempted"] += 1
            current_before = chain_state["current_cut"]
        tag = {"case": arm["case"], "arm": arm["model"], "stage": stage,
               "parameter_seed_label": parameter, "candidate": candidate, "chain": chain,
               "step": step, "source": source_before, "seed_roles": roles, "beta": beta}
        emit(stream, {"record_type": "attempt_requested", **tag, "photons": K})
        with native_setup.measure():
            draw, backend_wall = factory(arm["networks"][candidate]["U"], source,
                                         arm["model"], roles["count"])
        with post.measure():
            accounting = factory_accounting(native_setup.wall, native_setup.cpu, backend_wall)
        emit(stream, {"record_type": "factory_setup", **tag, "accounting": accounting})
        with generation.measure():
            counts, fallback = draw()
        with post.measure():
            counts, collision, proposed = classify_counts(counts, fallback)
            coin, acceptance, proposed_cut, accepted = None, None, None, False
            if not collision:
                proposed_cut = score(arm, proposed, "proposal", labels)
                acceptance = 1. if proposed_cut <= current_before else math.exp(-beta*(proposed_cut-current_before))
                coin = (float(np.random.Generator(np.random.PCG64(roles["coin"])).random())
                        if coin_draw is None else coin_draw(roles["coin"]))
                if not math.isfinite(coin) or not 0 <= coin < 1:
                    raise RetainedFailure("invalid fresh coin", {"coin": coin})
                accepted = coin < acceptance
                if accepted:
                    chain_state["current"] = list(proposed)
            # Intentionally actual paid current-cut call even on self-loops.
            current_cut = score(arm, chain_state["current"], "current", labels)
            chain_state["current_cut"] = current_cut
            chain_state["best_cut"] = min(chain_state["best_cut"], current_cut)
            chain_state["current_cuts"].append(current_cut)
            arm["completed"] += 1
            event = {**tag, "counts": counts, "fallback": bool(fallback), "collision": collision,
                     "proposal": proposed, "proposal_cut": proposed_cut,
                     "coin": coin, "coin_seed_used": not collision,
                     "acceptance_probability": acceptance, "accepted": accepted,
                     "current_before_cut": current_before, "current": list(chain_state["current"]),
                     "current_cut": current_cut, "chain_best_cut": chain_state["best_cut"],
                     "all_paid_best_cut": arm["paid_best"]["cut"]}
    except Exception as error:
        evidence = {"labels": labels, "candidate": candidate, "beta": beta, "seed_roles": roles,
                    "counts": counts, "fallback": fallback, "chain_state": chain_state,
                    "setup": setup.record(), "factory": native_setup.record(),
                    "generation": generation.record(), "postprocessing": post.record(),
                    "returned_backend_wall": backend_wall, "cause": repr(error),
                    "cause_evidence": getattr(error, "evidence", {})}
        emit(stream, {"record_type": "failed_attempt", "case": arm["case"], **evidence})
        raise RetainedFailure("first attempt failure; no retry", evidence) from error
    finally:
        charge(arm, ("attempt_setup", *labels), setup.wall, setup.cpu)
        charge(arm, ("attempt_postprocessing", *labels), post.wall, post.cpu)
        if accounting is not None:
            charge(arm, ("factory_classical_prefix", *labels), accounting["classical_prefix_wall"])
    event.update(setup=setup.record(), factory_total=native_setup.record(),
                 factory_accounting=accounting, excluded_count_generation=generation.record(),
                 postprocessing=post.record())
    emit(stream, {"record_type": "attempt", **event})
    return event


def run_chain(arm, start, start_cut, candidate, stage, parameter, chain, steps,
              stream, guard, factory=None, coin_draw=None):
    reset = Meter()
    with reset.measure():
        source = validated_source(start)
        state = {"current": source, "current_cut": start_cut, "best_cut": start_cut,
                 "current_cuts": []}
    charge(arm, ("chain_reset", stage, parameter, chain), reset.wall, reset.cpu)
    emit(stream, {"record_type": "chain_start", "case": arm["case"], "stage": stage,
                  "chain": chain, "candidate": candidate, "source": source,
                  "initial_cut": start_cut, "reset_compute": reset.record()})
    rows, beta_records = [], []
    for step in range(steps):
        guard()
        beta_time = Meter()
        with beta_time.measure():
            beta = float(Fraction(4*N, arm["W"])) if stage == "training" else (N/arm["W"])*2**(step/2)
        charge(arm, ("beta", stage, parameter, chain, step), beta_time.wall, beta_time.cpu)
        beta_records.append(beta_time.record())
        emit(stream, {"record_type": "beta_preparation", "case": arm["case"], "stage": stage,
                      "parameter_seed_label": parameter, "chain": chain, "step": step,
                      "beta": beta, "beta_compute": beta_time.record()})
        rows.append(run_attempt(arm, state, candidate, (stage, parameter, chain, step), beta,
                                stream, factory=factory, coin_draw=coin_draw))
    final = Meter()
    with final.measure():
        result = {"stage": stage, "chain": chain, "candidate": candidate,
                  "initial": list(start), "initial_cut": start_cut, "final": list(state["current"]),
                  "final_current_cut": state["current_cut"], "chain_best_cut": state["best_cut"],
                  "gain_from_start": start_cut-state["best_cut"], "current_cuts": state["current_cuts"],
                  "attempts": rows, "reset_compute": reset.record(), "beta_compute": beta_records}
    charge(arm, ("chain_final", stage, parameter, chain), final.wall, final.cpu)
    result["final_aggregation"] = final.record()
    emit(stream, {"record_type": "chain_complete", "case": arm["case"], **result})
    return result


def run_arm(arm, stream, guard, factory=None, coin_draw=None):
    start_time = Meter()
    with start_time.measure():
        training_start, training_seed = uniform_start(arm, "training", 0)
        training_cut = score(arm, training_start, "initial", ("training_start",))
    charge(arm, ("training_start",), start_time.wall, start_time.cpu)
    emit(stream, {"record_type": "common_training_start", "case": arm["case"],
                  "source": training_start, "seed": training_seed, "cut": training_cut,
                  "start_compute": start_time.record()})
    training_start_compute = start_time.record()
    training, fitnesses = [], []
    for candidate in range(8):
        row = run_chain(arm, training_start, training_cut, candidate, "training", candidate, 0,
                        2, stream, guard, factory, coin_draw)
        fitness_time = Meter()
        with fitness_time.measure():
            fitness = normalized_mean(row["current_cuts"], arm["W"])
            fitnesses.append(fitness)
            training.append(row)
        charge(arm, ("fitness", candidate), fitness_time.wall, fitness_time.cpu)
        row["fitness_compute"] = fitness_time.record()
        emit(stream, {"record_type": "candidate_fitness", "case": arm["case"],
                      "candidate": candidate, "fitness": fitness, "fitness_compute": fitness_time.record()})
    selection = Meter()
    with selection.measure():
        selected = choose_candidate(fitnesses)
    charge(arm, ("selection",), selection.wall, selection.cpu)
    emit(stream, {"record_type": "selected_before_fresh", "case": arm["case"],
                  "candidate": selected, "fitnesses": fitnesses, "parameters": CANDIDATES[selected],
                  "selection_compute": selection.record()})
    fresh = []
    for chain in range(3):
        start_time = Meter()
        with start_time.measure():
            source, start_seed = uniform_start(arm, "fresh", chain)
            start_cut = score(arm, source, "initial", ("fresh_start", chain))
        charge(arm, ("fresh_start", chain), start_time.wall, start_time.cpu)
        emit(stream, {"record_type": "fresh_start", "case": arm["case"], "chain": chain,
                      "source": source, "seed": start_seed, "cut": start_cut,
                      "sampling_with_replacement": True, "start_compute": start_time.record()})
        row = run_chain(arm, source, start_cut, selected, "fresh", "selected", chain,
                        8, stream, guard, factory, coin_draw)
        row["start_compute"] = start_time.record()
        fresh.append(row)
    final = Meter()
    with final.measure():
        mean = normalized_mean([row["chain_best_cut"] for row in fresh], arm["W"])
        if (arm["attempted"] != 40 or arm["completed"] != 40 or arm["score_counts"]["initial"] != 4
                or arm["score_counts"]["current"] != 40):
            raise RetainedFailure("trajectory attempt/score accounting failed", arm["score_counts"])
        result = {"case": arm["case"], "selected_candidate": selected,
                  "selected_parameters": CANDIDATES[selected], "fitnesses": fitnesses,
                  "training": training, "fresh": fresh, "B_fresh_chain_best_normalized_mean": mean,
                  "B_paid_best": arm["paid_best"]["cut"], "B_paid_best_record": arm["paid_best"],
                  "score_counts": dict(arm["score_counts"]), "FAST": {},
                  "training_start_compute": training_start_compute,
                  "selection_compute": selection.record(), "paid_components": arm["paid_components"]}
    charge(arm, ("arm_final",), final.wall, final.cpu)
    result["final_aggregation"] = final.record()
    result["B_classical_wall"] = arm["paid_wall"]
    emit(stream, {"record_type": "arm_complete", "case": arm["case"],
                  "B_classical_wall": arm["paid_wall"], "paid_components": arm["paid_components"],
                  "final_aggregation": final.record()})
    return result


def fast_summary(result):
    budget, timestamp = result["cpu_budget_seconds"], result["eligible_checkpoint_cpu_seconds"]
    best = result["best_cut"]
    prefix = (result["has_eligible_result"] and best is not None and timestamp is not None
              and math.isfinite(timestamp) and 0 <= timestamp <= budget and result["best_snapshot_cached_online"])
    acceptance = (prefix and result["comparison_acceptance_eligible"] and not result["early_cap_inconclusive"]
                  and not result["early_wall_inconclusive"] and result["first_scan_completed_before_deadline"])
    return {"prefix_eligible_for_veto": bool(prefix), "comparison_acceptance_eligible": bool(acceptance),
            "best_cut": best if prefix else None, "cpu_budget_seconds": budget,
            "eligible_checkpoint_cpu_seconds": timestamp,
            "first_scan_completed_before_deadline": result["first_scan_completed_before_deadline"],
            "early_cap_inconclusive": result["early_cap_inconclusive"],
            "early_wall_inconclusive": result["early_wall_inconclusive"]}


def fast_comparison(raw, case, allowance, mode):
    adapter = Meter()
    with adapter.measure():
        if mode not in FAST_MODES or not math.isfinite(allowance) or allowance < 0:
            raise RetainedFailure("invalid FAST mode or allowance")
        seed = seed_for(ROOTS["FAST"], case, mode)
        max_proposals = FAST_MAX_PROPOSALS
        allowance = float(allowance)
    budget = max(0., allowance-adapter.cpu)
    result = fast.solve_from_raw(raw, seed=seed, initialization=mode,
                                 cpu_budget_seconds=budget, max_proposals=max_proposals)
    if len(result["trace"]["cpu_seconds"]) > FAST_MAX_CHECKPOINTS:
        raise RetainedFailure("FAST trace guard exceeded")
    return {**fast_summary(result), "case": case, "mode": mode, "seed": seed,
            "B_classical_WALL_allowance": allowance, "adapter": adapter.record(),
            "solver_CPU_allowance": budget, "result": result,
            "other_arm_seconds_granted": 0, "optical_latency_assumed_seconds": 0,
            "hardware_runtime_measured": False}


def classify_stage1(rows, failed=False):
    complete = (not failed and len(rows) == 2 and len({row["case"] for row in rows}) == 2
                and all(set(row["FAST"]) == set(FAST_MODES) for row in rows))
    vetoes = [mode for mode in FAST_MODES if complete and all(
        row["FAST"][mode]["prefix_eligible_for_veto"] and row["FAST"][mode]["best_cut"] is not None
        and row["FAST"][mode]["best_cut"] <= row["B_paid_best"] for row in rows)]
    eligible = complete and all(row["FAST"][mode]["comparison_acceptance_eligible"]
                                for row in rows for mode in FAST_MODES)
    status = ("INCONCLUSIVE_FIRST_FAILURE" if failed else "DEV_REJECTED_FIXED_FAST" if vetoes
              else "INCONCLUSIVE_FAST_ELIGIBILITY" if not eligible else "STAGE1_OPTIONAL_CONTROLS_REQUIRED")
    return {"status": status, "positive_accepted": False, "fixed_FAST_veto_modes": vetoes,
            "FAST_all_comparison_eligible": bool(eligible),
            "optional_controls": {arm: "NOT_RUN_DUE_FAST_VETO" if vetoes else "NOT_RUN_STAGE1_SCOPE"
                                  for arm in OPTIONAL_ARMS}}


def configure_native_threads(xq):
    before = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    return {"interface": "exqalibur.Config.compute_max_thread_count", "before": before,
            "requested": 1, "readback_before_work": native_readback(xq)}


def native_readback(xq):
    value = int(xq.Config.compute_max_thread_count)
    if value != 1:
        raise RetainedFailure("native maximum readback failed", {"observed": value})
    return value


def check_output(output):
    size = sum(path.stat().st_size for path in Path(output).rglob("*") if path.is_file())
    if size > MAX_OUTPUT-OUTPUT_RESERVE:
        raise RetainedFailure("scientific output reserve exhausted", {"bytes": size})


def execute(spec, output):
    if spec != read_spec():
        raise ValueError("parsed spec differs from frozen bytes")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    start_wall, start_cpu = time.perf_counter(), time.process_time()
    arms, graphs, results, native, graph_times = {}, {}, [], {}, {}
    failure, stage, xq = None, "metadata", None
    raw_path = output/"raw.jsonl.gz"
    def guard():
        check_output(output)
        if time.perf_counter()-_IMPORT_WALL >= 90 or time.process_time()-_IMPORT_CPU >= 60:
            raise RetainedFailure("frozen resource cap reached")
    with raw_path.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped, encoding="utf8") as stream:
            try:
                owners = seed_namespaces(spec)
                save_json(output/"seed_namespaces.json", [{"role": list(key), "seed": value} for key, value in owners.items()])
                stage = "native_configuration"
                importing = Meter()
                with importing.measure():
                    import exqalibur as xq
                native = configure_native_threads(xq)
                native["excluded_exqalibur_import"] = importing.record()
                importing = Meter()
                with importing.measure():
                    import perceval as _pcvl
                native["excluded_perceval_import"] = importing.record()
                native["readback_after_imports"] = native_readback(xq)
                for case in spec["cases"]:
                    guard()
                    cid = case["id"]
                    stage = "graph/"+cid
                    timer = Meter()
                    with timer.measure():
                        graphs[cid] = make_graph(case)
                    graph_times[cid] = timer.record()
                    emit(stream, {"record_type": "supplied_graph", "case": case,
                                  "adjacency": graphs[cid], "excluded_generation": timer.record()})
                    stage = "B/"+cid
                    arms[cid] = prepare_arm(graphs[cid], case, stream)
                    save_json(output/f"context_{cid}.json", {
                        "case": case, "adjacency": arms[cid]["a"], "W": arms[cid]["W"],
                        "networks": arms[cid]["networks"], "preparation": arms[cid]["preparation"],
                        "compilation": arms[cid]["compilation"],
                        "excluded_matrix_diagnostics": arms[cid]["excluded_matrix_diagnostics"]})
                    results.append(run_arm(arms[cid], stream, guard))
                aggregate = Meter()
                with aggregate.measure():
                    mean = sum((row["B_fresh_chain_best_normalized_mean"] for row in results), Fraction(0))/2
                for row in results:
                    charge(arms[row["case"]], ("global_aggregation_share",), aggregate.wall/2, aggregate.cpu/2)
                    row["B_classical_wall"] = arms[row["case"]]["paid_wall"]
                    row["global_mean_aggregation_share"] = aggregate.wall/2
                    save_json(output/f"B_{row['case']}.json", row)
                emit(stream, {"record_type": "B_equal_graph_fresh_mean", "mean": mean,
                              "paid_aggregation": aggregate.record(),
                              "cost_share_per_case": aggregate.wall/2})
                for row in results:
                    for mode in FAST_MODES:
                        guard()
                        stage = f"FAST/{row['case']}/{mode}"
                        comparison = fast_comparison(graphs[row["case"]], row["case"], row["B_classical_wall"], mode)
                        save_json(output/f"FAST_{row['case']}_{mode}.json", comparison)
                        row["FAST"][mode] = {key: value for key, value in comparison.items() if key != "result"}
                guard()
                summary = classify_stage1(results)
                summary["B_equal_graph_fresh_chain_best_mean"] = mean
            except Exception as error:
                failure = {"stage": stage, "error": repr(error), "evidence": getattr(error, "evidence", {})}
                emit(stream, {"record_type": "first_failure", **failure})
                summary = classify_stage1(results, failed=True)
            if xq is not None:
                try:
                    native["readback_after_work"] = native_readback(xq)
                except Exception as error:
                    native["readback_failure"] = repr(error)
                    if failure is None:
                        failure = {"stage": "native_readback", "error": repr(error),
                                   "evidence": getattr(error, "evidence", {})}
                        emit(stream, {"record_type": "first_failure", **failure})
                    summary = classify_stage1(results, failed=True)
    summary.update(results=results, failure=failure, native_threads=native,
                   excluded_science_import=SCIENCE_IMPORT_TIMING, excluded_graph_generation=graph_times,
                   attempted_B_shots=sum(arm["attempted"] for arm in arms.values()),
                   completed_B_shots=sum(arm["completed"] for arm in arms.values()),
                   simulated_injected_B_photons=K*sum(arm["attempted"] for arm in arms.values()),
                   simulated_completed_B_photons=K*sum(arm["completed"] for arm in arms.values()),
                   photon_accounting="ten modeled photons charged per requested B attempt; actual QPU photons0",
                   B_paid_best_cached_online={cid: arm["paid_best"] for cid, arm in arms.items()},
                   B_paid_classical_wall={cid: arm["paid_wall"] for cid, arm in arms.items()},
                   B_paid_components={cid: arm["paid_components"] for cid, arm in arms.items()},
                   wall_seconds_inside_execute=time.perf_counter()-start_wall,
                   cpu_seconds_inside_execute=time.process_time()-start_cpu,
                   raw_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                   source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   actual_QPU_calls=0, actual_QPU_photons=0, optimum_used=False, heldout_opened=False,
                   optional_models_executed=False, hardware_runtime_measured=False,
                   internal_factory_CPU_split_available=False, IO_or_other_arm_seconds_granted=False)
    final_bytes = len((json.dumps(serial(summary), allow_nan=False, indent=2)+"\n").encode())
    existing_bytes = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    if final_bytes+existing_bytes > MAX_OUTPUT-OUTPUT_RESERVE:
        failure = failure or {"stage": "finalization", "error": "summary exceeds output reserve",
                              "evidence": {"existing_bytes": existing_bytes, "summary_bytes": final_bytes}}
        summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False,
                   "failure": failure, "completed_B_shots": summary["completed_B_shots"],
                   "raw_sha256": summary["raw_sha256"], "full_summary_omitted_due_output_cap": True}
    save_json(output/"failure.json", {"failure": failure})
    save_json(output/"summary.json", summary)
    return summary, failure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, failure = execute(read_spec(args.spec), args.output)
    print(json.dumps({"status": summary["status"], "positive_accepted": False,
                      "completed_B_shots": summary["completed_B_shots"]}))
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
