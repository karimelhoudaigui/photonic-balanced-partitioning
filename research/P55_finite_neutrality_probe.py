"""P55 finite full-CF neutrality DEV veto; never a QPU or optimum oracle.

Immutable P43/P48/P50/P55 helpers supply local counts, Decimal80 marginals,
from-raw search and exact decoding. Only the old P45 CTMC source initializer
is adapted: every one of the N inputs now has one photon. No old data changes.
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
from pathlib import Path
import random
import time

import networkx as nx
import numpy as np

import P48_spectral_pit_probe as p48
import P50_fast_from_scratch as fast
from P55_neutrality_decoder import NeutralityDecoder

base = p48.base
MODELS = ("bosonic", "distinguishable", "species4", "continuous_phase",
          "independent_B_marginals", "inclusion_walk")
FAST_MODES = ("random", "spectral")
TOLERANCE = 3e-12
NAMESPACES = {"group0": 551010, "group1": 551011, "training": 552000,
              "evaluation": 553000, "FAST": 554000}


class Meter:
    def __init__(self):
        self.wall = self.cpu = 0.

    @contextmanager
    def measure(self):
        wall, cpu = time.perf_counter(), time.process_time()
        try:
            yield
        finally:
            self.wall += time.perf_counter() - wall
            self.cpu += time.process_time() - cpu

    def record(self):
        record = {"wall_seconds": self.wall, "cpu_seconds": self.cpu}
        if hasattr(self, "factory_total"):
            record.update(factory_total=self.factory_total, CPU_split_available=False,
                          backend_wall_source="immutable_factory_reported_backend_seconds")
        return record


class RetainedFailure(RuntimeError):
    def __init__(self, message, evidence=None):
        super().__init__(message)
        self.evidence = {} if evidence is None else evidence


def serial(value):
    if isinstance(value, np.ndarray):
        return {"real": value.real.tolist(), "imag": value.imag.tolist()} if np.iscomplexobj(value) else value.tolist()
    if isinstance(value, np.generic):
        return serial(value.item())
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    return value


def emit(stream, row):
    stream.write(json.dumps(serial(row), allow_nan=False) + "\n")


def save_json(path, value, compressed=False):
    with Path(path).open("xb") as raw:
        if compressed:
            with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped:
                zipped.write(json.dumps(serial(value), allow_nan=False).encode())
        else:
            raw.write((json.dumps(serial(value), allow_nan=False, indent=2) + "\n").encode())


def policies(model):
    if model not in MODELS:
        raise ValueError("Unknown frozen model")
    if model == "inclusion_walk":
        return [{"id": i, "network": None, "t": None, "group": None, "horizon_tau": tau,
                 "training_draws": 4} for i, tau in enumerate((1, 2, 4, 8, 16, 32))]
    times = [("1", 1.), ("2", 2.), ("4", 4.)]
    if model == "distinguishable":
        times = [("1", 1.), ("sqrt2", math.sqrt(2)), ("2", 2.),
                 ("2sqrt2", 2*math.sqrt(2)), ("4", 4.), ("4sqrt2", 4*math.sqrt(2))]
    pairs = [(label, t, group) for label, t in times
             for group in ((0, 1) if model == "species4" else (None,))]
    return [{"id": i, "network": label, "t": t, "group": group, "horizon_tau": None,
             "training_draws": 4 if model in ("distinguishable", "species4") else 8}
            for i, (label, t, group) in enumerate(pairs)]


def expected_spec():
    return {"phase": "P55_FINITE_NEUTRALITY_DEV_VETO", "positive_acceptance_allowed": False,
            "ideal_transmission_eta": 1, "cases": [
                {"id": "n20_ER_5502001", "m": 20, "k": 10, "r": 20, "family": "ER", "seed": 5502001},
                {"id": "n20_RR_5502002", "m": 20, "k": 10, "r": 20, "family": "RR", "seed": 5502002}],
            "models": list(MODELS), "policy_grids": {m: policies(m) for m in MODELS},
            "graph_mean_degree": 4, "graph_RR_degree": 4, "weight_low": 1, "weight_high": 5,
            "seed_namespaces": NAMESPACES, "training_batch_draws": 4,
            "evaluation_trials": [0, 1], "evaluation_draws_per_trial": 8,
            "numerical_tolerance": TOLERANCE, "PGF_precision": 80,
            "PGF_mixed_exact_row": "q_i=i/210,i=1..20",
            "CTMC_horizon_convention": "direct_horizon_tau_never_squared",
            "full_source_raw_mean_guard_both_sides": True,
            "FAST_followup_requires_first_scan": True, "FAST_veto_accepts_paid_initialization": True,
            "CTMC_event_cap_per_shot": 4096, "FAST_modes": list(FAST_MODES),
            "FAST_max_proposals": 100000000, "planned_total_draws": 480,
            "planned_B_draws": 80, "maximum_cpu_seconds": 60, "maximum_wall_seconds": 90,
            "maximum_threads": 1, "maximum_new_output_bytes": 33554432,
            "maximum_planned_workspace_bytes": 268435456}


def validated_graph(raw):
    a = np.asarray(raw)
    if (a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] < 2 or a.shape[0] % 2
            or a.dtype.kind not in "iu" or np.any(a < 0) or np.any(np.diag(a))
            or not np.array_equal(a, a.T)):
        raise ValueError("Nonnegative symmetric integer adjacency with even N required")
    if int(a.max()) > np.iinfo(np.int64).max // (4*len(a)*len(a)):
        raise ValueError("Unsafe graph weight")
    return np.array(a, dtype=np.int64, order="C", copy=True)


def make_graph(case):
    n, seed = case["m"], case["seed"]
    if case["family"] not in ("ER", "RR"):
        raise ValueError("Unknown graph family")
    g = (nx.gnp_random_graph(n, 4/(n-1), seed=seed) if case["family"] == "ER"
         else nx.random_regular_graph(4, n, seed=seed))
    rng = np.random.default_rng(base.seed_for(seed, "weights"))
    a = np.zeros((n, n), dtype=np.int64)
    for i, j in sorted(g.edges()):
        a[i, j] = a[j, i] = int(rng.integers(1, 6))
    return a


def product_marginals(q):
    tables, receipts = [], []
    for row in q:
        repaired, row_info = p48.repair_probability_row(row)
        pmf, info = p48.factorial_marginal(repaired, True)
        if (abs(Fraction(row_info["raw_mu"]) - 1) > Fraction(3, 10**12)
                or Fraction(row_info["input_roundoff_repair_L1"]) > Fraction(3, 10**12)
                or Fraction(info["pmf_correction_L1"]) > Fraction(3, 10**12)
                or np.any(pmf < 0) or abs(float(pmf.sum()) - 1) > TOLERANCE):
            raise RetainedFailure("Independent B marginal numerical guard", {"row": row_info, "PGF": info})
        tables.append(pmf)
        receipts.append({"row": row_info, "PGF": info})
    pmf = np.asarray(tables)
    raw_cdf = np.cumsum(pmf, axis=1)
    cdf = np.minimum(1., np.maximum.accumulate(raw_cdf, axis=1))
    cdf[:, -1] = 1.
    correction = float(abs(cdf - raw_cdf).max())
    if correction > TOLERANCE:
        raise RetainedFailure("Independent B CDF numerical guard", {"correction_max": correction})
    return {"pmf": pmf, "cdf": cdf, "receipts": receipts,
            "cdf_correction_max": correction, "total_count_conditioned": False}


def prepare_arm(raw, case, model):
    meter = Meter()
    with meter.measure():
        a = validated_graph(raw)
        n = len(a)
        if case["m"] != n or case["k"] != n//2 or case["r"] != n:
            raise ValueError("P55 requires full CF input and balanced output")
        h = np.sqrt(a.astype(float))
        values, vectors = np.linalg.eigh(h)
        rho = float(abs(values).max())
        hbar, scaled = (h/rho, values/rho) if rho else (h, values)
        residual = float(abs(hbar@vectors - vectors*scaled[None, :]).max())
        if not np.all(np.isfinite(scaled)) or residual > TOLERANCE:
            raise RetainedFailure("Graph-generator eigensystem guard", {"residual": residual})
        contexts = {}
        for policy in policies(model):
            key = policy["network"]
            if key is None or key in contexts:
                continue
            u = (vectors*np.exp(1j*policy["t"]*scaled)[None, :])@vectors.T
            defect = float(abs(u.conj().T@u - np.eye(n)).max())
            row_defect = float(abs(u@u.conj().T - np.eye(n)).max())
            raw_mu = (abs(u)**2).sum(axis=1)
            if (not np.all(np.isfinite(u)) or max(defect, row_defect) > TOLERANCE
                    or float(abs(raw_mu - 1).max()) > TOLERANCE):
                raise RetainedFailure("Full-source unitary/mass guard", {"network": key,
                                      "column_gram_residual": defect, "row_gram_residual": row_defect,
                                      "raw_mu": raw_mu})
            contexts[key] = {"u": u, "column_gram_residual": defect,
                             "row_gram_residual": row_defect, "raw_mu": raw_mu}
            if model == "independent_B_marginals":
                contexts[key].update(product_marginals(abs(u)**2))
        groups = {}
        if model == "species4":
            groups = {i: np.random.default_rng(base.seed_for(NAMESPACES[f"group{i}"], case["id"])).permutation(n).tolist()
                      for i in (0, 1)}
        arm = {"case": case["id"], "model": model, "a": a, "Hbar": hbar,
               "rho": rho, "generator_residual": residual, "contexts": contexts,
               "groupings": groups, "denominator": max(1, int(np.triu(a, 1).sum())), "paid_best": None}
        if model == "inclusion_walk":
            arm["inclusion_rates_base"] = abs(hbar)**2
    arm["classical_preparation"] = meter.record()
    return arm


def native_thread_readback(xq):
    value = int(xq.Config.compute_max_thread_count)
    if value != 1:
        raise RetainedFailure("Native maximum CPU threads differs from one", {"actual": value})
    return value


def configure_native_threads(xq):
    before = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    return {"interface": "exqalibur.Config.compute_max_thread_count", "before": before,
            "requested": 1, "configured_before_work": native_thread_readback(xq),
            "scope": "documented maximum; OS scheduling not measured"}


def inclusion_draw(q, horizon_tau, rng, event_cap=4096):
    """P45 rates/Gillespie semantics; sole physical adaptation is fullCF source."""
    n = np.ones(len(q), dtype=np.int64)
    elapsed, events = 0., 0
    while True:
        rates = (n[:, None] + 1)*n[None, :]*q
        np.fill_diagonal(rates, 0)
        total = float(rates.sum())
        next_event = elapsed + rng.exponential(1/total) if total > 0 else None
        if next_event is None or next_event > horizon_tau:
            return n, {"inclusion_events": events, "last_event_time": elapsed,
                       "proposed_next_event_time": next_event, "horizon_tau": horizon_tau, "horizon_completed": True}
        if events >= event_cap:
            raise RetainedFailure("INCONCLUSIVE inclusion event cap", {"counts": n.copy(),
                                  "inclusion_events": events, "elapsed": elapsed,
                                  "rate_total": total, "last_event_time": elapsed,
                                  "proposed_next_event_time": next_event, "horizon_tau": horizon_tau,
                                  "horizon_completed": False})
        index = int(rng.choice(len(q)*len(q), p=rates.ravel()/total))
        i, j = divmod(index, len(q))
        n[i] += 1
        n[j] -= 1
        elapsed, events = next_event, events + 1


def independent_counts(cdf, rng):
    uniforms = rng.random(len(cdf))
    return np.sum(uniforms[:, None] >= cdf, axis=1), {"marginal_uniforms": uniforms,
                                                   "total_count_conditioned": False}


def observation_components(arm, policy, seed, backend):
    """Classical caller setup is outside the narrowly bracketed optical setup."""
    model, n = arm["model"], len(arm["a"])
    roles = {role: base.seed_for(seed, role) for role in ("observation", "neutral_rank")}
    rank_rng = random.Random(roles["neutral_rank"])
    if model == "continuous_phase":
        roles.update({role: base.seed_for(roles["observation"], name) for role, name in
                      (("phase_coefficients", "coherent_coefficients"), ("phase_multinomial", "coherent_multinomial"))})
    if len(set(roles.values())) != len(roles):
        raise RetainedFailure("Random role namespace collision", roles)
    context = arm["contexts"].get(policy["network"])
    if model in ("bosonic", "species4", "distinguishable"):
        source = arm["groupings"][policy["group"]] if model == "species4" else list(range(n))
        if model in ("bosonic", "species4"):
            factory = Meter()
            with factory.measure():
                primitive, backend_seconds = base.make_optical_sampler(context["u"], source, model, roles["observation"])
            if not math.isfinite(backend_seconds) or backend_seconds < 0 or backend_seconds > factory.wall + 1e-8:
                raise RetainedFailure("Invalid immutable factory backend WALL", {"factory": factory.record(), "backend_seconds": backend_seconds})
            # The immutable helper starts its WALL clock AFTER RNG/source validation.
            # Its pre-clock prefix remains CLASSICAL; CPU has no matching inner clock.
            backend.wall, backend.cpu = backend_seconds, None
            backend.factory_total = factory.record()
        else:
            primitive, _ = base.make_optical_sampler(context["u"], source, model, roles["observation"])
        def draw():
            counts, fallback = primitive()
            if fallback:
                raise RetainedFailure("Unauthorized optical fallback")
            return counts, {}
    elif model == "continuous_phase":
        draw = p48.coherent_counts({"v": context["u"]}, model, roles["observation"])
    else:
        rng = np.random.default_rng(roles["observation"])
        if model == "independent_B_marginals":
            draw = lambda: independent_counts(context["cdf"], rng)
        else:
            draw = lambda: inclusion_draw(arm["inclusion_rates_base"], horizon_tau=policy["horizon_tau"], rng=rng)
    return draw, rank_rng, roles


def decode_observation(a, counts, rank_rng, model):
    counts = np.asarray(counts)
    n = len(a)
    if (counts.shape != (n,) or counts.dtype.kind not in "iu" or np.any(counts < 0)
            or np.any(counts > n) or (model != "independent_B_marginals" and int(counts.sum()) != n)):
        raise RetainedFailure("Invalid photon multiplicities", {"counts": counts, "model": model})
    decoder = NeutralityDecoder(counts)
    rank = rank_rng.randrange(decoder.ways)
    subset = decoder.unrank(rank)
    value = base.cut(a, subset)
    return {"counts": counts, "total_count": decoder.total, "subset": subset, "cut": value,
            "uniform_rank": rank, "ways": decoder.ways, "target_sums": decoder.target_sums,
            "target_ways": decoder.target_ways, "minimum_imbalance": decoder.minimum_imbalance,
            "DP_cells": decoder.cells}


def classical_setup(total, backend):
    if backend["wall_seconds"] > total["wall_seconds"] + 1e-8:
        raise RetainedFailure("Nested backend clock exceeds total setup")
    wall = max(0., total["wall_seconds"] - backend["wall_seconds"])
    if backend["cpu_seconds"] is None:
        return {"wall_seconds": wall, "cpu_seconds": None, "CPU_split_available": False,
                "scope": "total setup CPU observed separately; factory CPU cannot be split honestly"}
    if backend["cpu_seconds"] > total["cpu_seconds"] + 1e-8:
        raise RetainedFailure("Nested backend CPU exceeds total setup")
    return {"wall_seconds": wall, "cpu_seconds": max(0., total["cpu_seconds"] - backend["cpu_seconds"])}


def run_batch(arm, policy, stage, trial, draws, stream):
    if stage not in ("training", "evaluation"):
        raise ValueError("Invalid stage")
    setup, backend, generation, post, aggregation = (Meter() for _ in range(5))
    with setup.measure():
        seed = base.seed_for(NAMESPACES[stage], arm["case"], arm["model"], policy["id"], trial)
        draw, rank_rng, roles = observation_components(arm, policy, seed, backend)
    classical = classical_setup(setup.record(), backend.record())
    tag = {"case": arm["case"], "model": arm["model"], "policy": policy["id"],
           "stage": stage, "trial": trial, "seed": seed, "seed_roles": roles}
    cuts, best_cut, best_subset = [], None, None
    for shot in range(draws):
        counts = extra = None
        try:
            with generation.measure():
                counts, extra = draw()
            with post.measure():
                event = decode_observation(arm["a"], counts, rank_rng, arm["model"])
                cuts.append(event["cut"])
                if best_cut is None or event["cut"] < best_cut:
                    best_cut, best_subset = event["cut"], event["subset"]
                if arm["paid_best"] is None or event["cut"] < arm["paid_best"]["cut"]:
                    arm["paid_best"] = {"cut": event["cut"], "subset": event["subset"]}
        except Exception as error:
            failed = {**tag, "record_type": "failed_shot", "shot": shot, "counts": counts,
                      "completed_cuts": cuts, "error": repr(error),
                      "evidence": getattr(error, "evidence", {}), "extra": extra,
                      "setup": setup.record(), "backend": backend.record(),
                      "generation": generation.record(), "postprocessing": post.record()}
            emit(stream, failed)
            stream.flush()
            raise RetainedFailure("First failed batch; no resampling", failed) from error
        emit(stream, {**tag, "record_type": "shot", "shot": shot, **event, **extra,
                      "collision": bool(np.any(counts > 1)),
                      "defect_mass_twice": sum(abs(int(x) - 1) for x in counts)})
    with aggregation.measure():
        cut_sum = sum(cuts)
        mean = Fraction(cut_sum, draws*arm["denominator"])
    stream.flush()
    return {**tag, "proposals": draws, "cuts": cuts, "sum_cuts": cut_sum,
            "best_cut": best_cut, "best_subset": best_subset,
            "weight_denominator": arm["denominator"], "exact_mean_normalized_cut": mean,
            "setup": setup.record(), "backend": backend.record(), "classical_setup": classical,
            "count_generation": generation.record(), "postprocessing": post.record(),
            "aggregation": aggregation.record(), "serialization_granted": False}


def select_policy(training, cases, model):
    if not cases or any(row["stage"] != "training" for row in training):
        raise ValueError("Selection accepts training only")
    if len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Duplicate selection graph")
    losses = {}
    for policy in policies(model):
        rows = [row for row in training if row["model"] == model and row["policy"] == policy["id"]]
        expected = sorted((case["id"], trial) for case in cases for trial in range(policy["training_draws"]//4))
        if sorted((row["case"], row["trial"]) for row in rows) != expected:
            raise ValueError("Missing/duplicate frozen training batch")
        means = []
        for case in cases:
            subset = [row for row in rows if row["case"] == case["id"]]
            if any(row["proposals"] != 4 or len(row["cuts"]) != 4 or row["sum_cuts"] != sum(row["cuts"])
                   or row["weight_denominator"] != case["weight_denominator"] for row in subset):
                raise ValueError("Training effort or ALL-shot normalization changed")
            means.append(Fraction(sum(row["sum_cuts"] for row in subset),
                                  policy["training_draws"]*case["weight_denominator"]))
        losses[policy["id"]] = sum(means, Fraction(0))/len(cases)
    return min(losses, key=lambda p: (losses[p], p)), losses


def B_allowance(arm, records, selection_share):
    if arm["model"] != "bosonic" or any(row["model"] != "bosonic" or row["case"] != arm["case"] for row in records):
        raise ValueError("Only THIS B arm can fund classical search")
    return arm["classical_preparation"]["wall_seconds"] + selection_share + sum(
        row[name]["wall_seconds"] for row in records for name in ("classical_setup", "postprocessing", "aggregation"))


def fast_comparison(raw, arm, rows, selection_share, mode):
    allowance, adapter = B_allowance(arm, rows, selection_share), Meter()
    with adapter.measure():
        seed = base.seed_for(NAMESPACES["FAST"], arm["case"], mode)
    solver_allowance = max(0., allowance - adapter.cpu)
    result = fast.solve_from_raw(raw, seed=seed, initialization=mode,
                                 cpu_budget_seconds=solver_allowance, max_proposals=100000000)
    veto_eligible = result["has_eligible_result"] and result["best_cut"] is not None
    eligible = (veto_eligible and result["comparison_acceptance_eligible"]
                and not result["early_cap_inconclusive"] and not result["early_wall_inconclusive"]
                and result["first_scan_completed_before_deadline"])
    return {"case": arm["case"], "mode": mode, "seed": seed, "total_CPU_allowance": allowance,
            "adapter": adapter.record(), "solver_CPU_allowance": solver_allowance,
            "comparison_acceptance_eligible": bool(eligible), "prefix_eligible_for_veto": bool(veto_eligible),
            "first_scan_completed_before_deadline": result["first_scan_completed_before_deadline"],
            "eligible_best_cut": result["best_cut"],
            "eligible_best_subset": result["best_subset"], "result": result,
            "optical_or_other_model_seconds_granted": 0., "serialization_seconds_granted": 0.,
            "allowance_convention": "B_own_classical_WALL_to_FAST_CPU_minus_actual_adapter_CPU; optical_latency_zero; not_hardware_timing"}


def summarize(records, cases, fast_rows):
    fresh, incumbents, proposals = {}, {}, {}
    for model in MODELS:
        fresh[model], incumbents[model], proposals[model] = {}, {}, {}
        for case in cases:
            rows = [row for row in records if row["model"] == model and row["case"] == case["id"]]
            evaluation = [row for row in rows if row["stage"] == "evaluation"]
            if sum(row["proposals"] for row in rows) != 40 or sum(row["proposals"] for row in evaluation) != 16:
                raise ValueError("Incomplete prospective population")
            fresh[model][case["id"]] = Fraction(sum(row["sum_cuts"] for row in evaluation), 16*case["weight_denominator"])
            incumbents[model][case["id"]] = {label: min(c for row in rows if row["stage"] in stages for c in row["cuts"])
                for label, stages in (("training", ("training",)), ("fresh", ("evaluation",)), ("paid_total", ("training", "evaluation")))}
            proposals[model][case["id"]] = {stage: sum(row["proposals"] for row in rows if row["stage"] == stage)
                                           for stage in ("training", "evaluation")}
        fresh[model]["equal_graph_mean"] = sum(fresh[model].values(), Fraction(0))/len(cases)
    pairs = {(row["case"], row["mode"]) for row in fast_rows}
    complete = (len(fast_rows) == len(pairs) == 2*len(cases)
                and pairs == {(case["id"], mode) for case in cases for mode in FAST_MODES})
    eligible = complete and all(row["comparison_acceptance_eligible"] for row in fast_rows)
    veto = [mode for mode in FAST_MODES if all(any(row["case"] == case["id"] and row["mode"] == mode
            and row["prefix_eligible_for_veto"] and row["eligible_best_cut"] is not None
            and row["eligible_best_cut"] <= incumbents["bosonic"][case["id"]]["paid_total"] for row in fast_rows) for case in cases)]
    worse_means = [m for m in MODELS[1:] if fresh["bosonic"]["equal_graph_mean"] >= fresh[m]["equal_graph_mean"]]
    all_graphs_clear = eligible and all(incumbents["bosonic"][row["case"]]["paid_total"] < row["eligible_best_cut"] for row in fast_rows)
    all_graphs_clear = all_graphs_clear and all(fresh["bosonic"][c["id"]] < fresh[m][c["id"]] for c in cases for m in MODELS[1:])
    required_mean_vetoes = [m for m in ("distinguishable", "inclusion_walk") if m in worse_means]
    status = ("INCONCLUSIVE_FAST_ELIGIBILITY" if not complete else "DEV_REJECTED_FIXED_FAST" if veto
              else "DEV_REJECTED_REQUIRED_CONTROL_MEAN" if required_mean_vetoes
              else "INCONCLUSIVE_FAST_ELIGIBILITY" if not eligible
              else "FOLLOW_UP_ONLY" if all_graphs_clear else "INCONCLUSIVE_MIXED_DEV")
    return {"status": status, "positive_accepted": False, "fresh_evaluation_means": fresh,
            "private_paid_incumbents": incumbents, "proposal_counts": proposals,
            "fixed_FAST_veto_algorithms": veto, "required_control_mean_vetoes": required_mean_vetoes,
            "controls_not_beaten_in_global_fresh_mean": worse_means,
            "FAST_all_eligible": eligible, "actual_QPU_calls": 0, "optimum_used": False,
            "heldout_opened": False, "simulated_B_attempts": 80, "simulated_B_injected_photons": 1600,
            "simulated_attempts_by_physical_model": {m: 80 for m in ("bosonic", "distinguishable", "species4")},
            "simulated_injected_photons_by_physical_model": {m: 1600 for m in ("bosonic", "distinguishable", "species4")}}


def check_output(output):
    if sum(path.stat().st_size for path in output.rglob("*") if path.is_file()) > 33554432 - 1048576:
        raise RetainedFailure("Output reserve exhausted; preserve first run")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    if spec != expected_spec():
        raise ValueError("Frozen P55 execution card changed")
    args.output.mkdir(parents=True, exist_ok=False)
    started_wall, started_cpu = time.perf_counter(), time.process_time()
    arms, graphs, records, selected, losses, selection_times, fast_rows = {}, {}, [], {}, {}, {}, []
    training = {model: [] for model in MODELS}
    cases, failure, native = [], None, {}
    raw_path = args.output/"raw.jsonl.gz"
    with raw_path.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped, encoding="utf8") as stream:
            try:
                import exqalibur as xq
                native = configure_native_threads(xq)
                for case in spec["cases"]:
                    case_id = case["id"]
                    graphs[case_id] = make_graph(case)  # Supplied instances, excluded symmetrically.
                    emit(stream, {"record_type": "supplied_graph", "case": case, "adjacency": graphs[case_id]})
                    stream.flush()
                    arms[case_id] = {model: prepare_arm(graphs[case_id], case, model) for model in MODELS}
                    cases.append({"id": case_id, "weight_denominator": arms[case_id]["bosonic"]["denominator"]})
                    save_json(args.output/f"context_{case_id}.json.gz", {"case": case, "arms": arms[case_id]}, True)
                    check_output(args.output)
                for case in cases:
                    for model in MODELS:
                        for policy in policies(model):
                            for trial in range(policy["training_draws"]//4):
                                row = run_batch(arms[case["id"]][model], policy, "training", trial, 4, stream)
                                records.append(row)
                                training[model].append(row)
                                check_output(args.output)
                for model in MODELS:
                    meter = Meter()
                    with meter.measure():
                        selected[model], losses[model] = select_policy(training[model], cases, model)
                    selection_times[model] = meter.record()
                save_json(args.output/"selection.json", {"selected": selected, "losses": losses,
                          "selection_compute": selection_times, "frozen_before_fresh": True})
                for case in cases:
                    for model in MODELS:
                        policy = policies(model)[selected[model]]
                        for trial in (0, 1):
                            records.append(run_batch(arms[case["id"]][model], policy, "evaluation", trial, 8, stream))
                            check_output(args.output)
                for case in cases:
                    own = [row for row in records if row["case"] == case["id"] and row["model"] == "bosonic"]
                    for mode in FAST_MODES:
                        fast_rows.append(fast_comparison(graphs[case["id"]], arms[case["id"]]["bosonic"], own,
                                                        selection_times["bosonic"]["wall_seconds"]/len(cases), mode))
                summary = summarize(records, cases, fast_rows)
            except Exception as error:
                failure = {"error": repr(error), "evidence": getattr(error, "evidence", {})}
                emit(stream, {"record_type": "first_failure", **failure})
                stream.flush()
                summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "failure": failure}
            if native:
                try:
                    native["readback_after_work"] = native_thread_readback(xq)
                except Exception as error:
                    native["readback_failure"] = repr(error)
                    if failure is None:
                        failure = {"error": repr(error), "evidence": getattr(error, "evidence", {})}
                        emit(stream, {"record_type": "first_failure", **failure})
                        summary = {"status": "INCONCLUSIVE_FIRST_FAILURE", "positive_accepted": False, "failure": failure}
    save_json(args.output/"failure.json", {"failure": failure})
    summary.update(primary_batches=records, selected_policies=selected, training_losses=losses,
                   selection_compute=selection_times, FAST_comparisons=fast_rows, native_threads=native,
                   completed_shots=sum(row["proposals"] for row in records) +
                       (len(failure["evidence"].get("completed_cuts", [])) if failure else 0),
                   classical_preparation={c: {m: a["classical_preparation"] for m, a in models.items()} for c, models in arms.items()},
                   paid_best_cached_online={c: {m: a["paid_best"] for m, a in models.items()} for c, models in arms.items()},
                   cpu_seconds_inside_main=time.process_time() - started_cpu,
                   wall_seconds_inside_main=time.perf_counter() - started_wall,
                   raw_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                   code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   spec_sha256=hashlib.sha256(args.spec.read_bytes()).hexdigest(),
                   simulation_time_is_QPU_time=False, B_cost_excludes_other_models=True,
                   actual_QPU_calls=0, actual_QPU_photons=0, heldout_opened=False,
                   optimum_used=False, source_from_previous_solution=False,
                   B_setup_CPU_split_available=False, B_factory_prefix_WALL_is_charged=True)
    save_json(args.output/"summary.json", summary)
    check_output(args.output)
    print(json.dumps({"status": summary["status"], "completed_shots": summary["completed_shots"], "positive_accepted": False}))
    return 1 if failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
