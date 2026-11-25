"""P50 prospective DEV discriminator with arm-local preparation and cheap ranking.

No optimum, reference partition, PIT, greedy completion, remote client or
accepted positive. Immutable P43/P48/P49 helpers supply seeds, local optical
sampling, Fourier coordinates and the frozen two-layer source rotation only.
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
import time

import networkx as nx
import numpy as np

import P49_trained_source_probe as prior
import P50_fast_from_scratch as fast

base = prior.base
p48 = prior.p48
MODELS = ("bosonic", "distinguishable", "species4", "continuous_phase",
          "gaussian_Bcov", "independent_final_variance", "independent_B_marginals", "spherical_coherent",
          "static_preparation", "pure_jitter")
OPTICAL = ("bosonic", "distinguishable", "species4")
BASES = ("Fourier_blind", "spectral_E", "spectral_R_phi0", "spectral_R_phi90")
FAST_INITIALIZATIONS = ("random", "spectral")
TIE_WIDTH = 1e-12


class ComputeMeter:
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
        return {"wall_seconds": self.wall, "cpu_seconds": self.cpu}


def serial(value):
    """Formatting occurs outside scientific compute/search clocks."""
    if isinstance(value, np.ndarray):
        if np.iscomplexobj(value):
            return {"real": value.real.tolist(), "imag": value.imag.tolist()}
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {key: serial(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [serial(item) for item in value]
    return value


def emit(stream, row):
    stream.write(json.dumps(serial(row), allow_nan=False) + "\n")


def policies(model):
    if model not in MODELS:
        raise ValueError(model)
    if model == "pure_jitter":
        return [{"id": index, "basis": None, "alpha": None, "beta": beta,
                 "training_draws": 16} for index, beta in enumerate((0., .1))]
    bases = (0, 1) if model in ("spherical_coherent", "static_preparation") else range(4)
    draws = 4 if model in ("spherical_coherent", "static_preparation") else 2
    return [{"id": index, "basis": basis, "alpha": alpha, "beta": beta,
             "training_draws": draws}
            for index, (basis, alpha, beta) in enumerate(
                (basis, alpha, beta) for basis in bases for alpha in (0, 1) for beta in (0., .1))]


def make_graph(case):
    """P43 sorted-edge/seeded-weight convention with the P50 density and weights."""
    n, seed = case["m"], case["seed"]
    if case["family"] not in ("ER", "RR"):
        raise ValueError("Unknown frozen graph family")
    rng = np.random.default_rng(base.seed_for(seed, "weights"))
    graph = (nx.gnp_random_graph(n, 8 / (n - 1), seed=seed)
             if case["family"] == "ER" else nx.random_regular_graph(8, n, seed=seed))
    a = np.zeros((n, n), dtype=np.int64)
    for i, j in sorted(graph.edges()):
        a[i, j] = a[j, i] = int(rng.integers(1, 6))
    return a


def validated_graph(raw):
    raw = np.asarray(raw)
    if (raw.ndim != 2 or raw.shape[0] != raw.shape[1] or raw.shape[0] < 2
            or raw.shape[0] % 2 or raw.dtype.kind not in "iu"
            or np.any(raw < 0) or np.any(np.diag(raw) != 0)
            or not np.array_equal(raw, raw.T)):
        raise ValueError("A nonnegative integer simple graph of positive even order is required")
    n = len(raw)
    if int(raw.max()) > np.iinfo(np.int64).max // (4 * n * n):
        raise ValueError("Unsafe integer graph weights")
    return np.array(raw, dtype=np.int64, order="C", copy=True)


def diffusion(a, alpha):
    if alpha not in (0, 1):
        raise ValueError("Frozen diffusion alpha required")
    n = len(a)
    degree = a.sum(axis=1)
    maximum = int(degree.max())
    if alpha == 0 or maximum == 0:
        return np.eye(n)
    return np.eye(n) - (np.diag(degree) - a) / maximum


def rank_balanced(field, priority, k, width=TIE_WIDTH):
    """Fixed max-anchored half-up buckets, then ascending carried rank.

    Translation invariant in exact arithmetic. Floating behavior on a bucket
    boundary is not a universal relabeling theorem; dedicated fixtures stay
    away from those boundaries and separately check both boundary sides.
    """
    field = np.asarray(field, dtype=float)
    priority = np.asarray(priority)
    n = len(field)
    if (field.shape != (n,) or priority.shape != (n,) or not np.all(np.isfinite(field))
            or priority.dtype.kind not in "iu" or sorted(priority.tolist()) != list(range(n))
            or not 0 <= k <= n or width != TIE_WIDTH):
        raise ValueError("Invalid ranking input")
    return _rank_prevalidated(field, priority, k)


def _rank_prevalidated(field, priority, k):
    """Main loop uses the arm's already-validated, fixed carried priority."""
    shifted = (field - field.max()) / TIE_WIDTH
    if not np.all(np.isfinite(shifted)) or np.any(abs(shifted) >= 2**52):
        raise p48.NumericalInconclusive("Ranking bucket loses integer resolution")
    bucket = np.floor(shifted + .5).astype(np.int64)
    order = np.lexsort((priority, -bucket))
    return np.sort(order[:k]), bucket


def gaussian_factor(v, tolerance=1e-10):
    """B covariance; exact structural rows masked in F BEFORE diffusion."""
    q = abs(v)**2
    mu = q.sum(axis=1)
    projection = v @ v.conj().T
    covariance = np.diag(mu) + abs(projection)**2 - 2 * q @ q.T
    covariance = (covariance + covariance.T) / 2
    values, vectors = np.linalg.eigh(covariance)
    if float(values.min()) < -tolerance:
        raise p48.NumericalInconclusive("Significantly non-PSD B covariance")
    factor = vectors * np.sqrt(np.maximum(values, 0))[None, :]
    empty = np.count_nonzero(q, axis=1) == 0
    one_hot = (np.count_nonzero(q, axis=1) == 1) & np.any(q == 1, axis=1)
    mask = empty | one_hot
    pre_variance = np.sum(factor**2, axis=1)
    factor[mask] = 0
    return {"covariance": covariance, "factor": factor, "structural_mask": mask,
            "pre_mask_variance": pre_variance, "covariance_eigenvalues": values}


def final_independent_variance(h, factor):
    """The row squared norm of the ACTUAL propagated factor, never target diag."""
    return np.sum((h @ factor)**2, axis=1)


def _spectral_frame(a, marks, priority, r):
    laplacian = np.diag(a.sum(axis=1)) - a
    norm = float(np.linalg.norm(laplacian, 2))
    scaled = laplacian / norm if norm else np.zeros_like(laplacian, dtype=float)
    marked = scaled + .001 * np.diag(marks)
    values, vectors = np.linalg.eigh(marked)
    vectors = np.asarray(vectors, dtype=complex)
    # Only occupied columns need a gauge; every remaining column is vacuum.
    pivots = []
    for column in range(r):
        magnitude = abs(vectors[:, column])
        candidates = np.flatnonzero(magnitude >= magnitude.max() - 1e-12)
        pivot = min(candidates, key=lambda i: priority[int(i)])
        vectors[:, column] *= np.conj(vectors[pivot, column]) / magnitude[pivot]
        pivots.append(int(pivot))
    return vectors, {"marked_matrix": marked, "eigenvalues": values,
                     "marks": marks, "gauge_pivots": pivots, "laplacian_norm": norm}


def prepare_arm(raw, case, model):
    """Each arm pays only its own work; no cross-arm context cache or search."""
    if model not in MODELS:
        raise ValueError(model)
    input_meter = ComputeMeter()
    with input_meter.measure():
        a = validated_graph(raw)
        n, r, case_id = len(a), case["r"], case["id"]
        if case["m"] != n or case["k"] != n // 2 or not 1 <= r < n // 2:
            raise ValueError("P50 separates photon count r from target K=N/2")
        priority_seed = base.seed_for(5040002, case_id)
        order = np.random.default_rng(priority_seed).permutation(n)
        priority = np.argsort(order)
        denominator = max(1, int(np.triu(a, 1).sum()))
    h_meter = ComputeMeter()
    with h_meter.measure():
        hs = {} if model == "pure_jitter" else {0: diffusion(a, 0), 1: diffusion(a, 1)}
    contexts, frames, family_times, spectral = {}, {}, {}, None
    if model != "pure_jitter":
        fourier_meter = ComputeMeter()
        with fourier_meter.measure():
            frames[0] = p48.fourier_basis(n, n, order.tolist())
        family_times["Fourier_blind"] = fourier_meter.record()
        spectral_meter = ComputeMeter()
        with spectral_meter.measure():
            marks_seed = base.seed_for(5040001, case_id)
            marks = np.random.default_rng(marks_seed).random(n)
            frames[1], spectral = _spectral_frame(a, marks, priority, r)
        family_times["spectral_E"] = spectral_meter.record()
        bases = sorted({p["basis"] for p in policies(model)})
        for basis in bases:
            meter = ComputeMeter()
            with meter.measure():
                frame = frames[0 if basis == 0 else 1]
                v = frame[:, :r].copy()
                if basis in (2, 3):
                    phi = 0. if basis == 2 else math.pi / 2
                    v = v @ prior.source_rotation(r, math.pi / 4, phi)
                q = abs(v)**2
                context = {"basis": basis, "v": v, "q": q, "mu": q.sum(axis=1)}
                if model in OPTICAL:
                    # The already-computed orthogonal vacuum complement is
                    # free of occupied/source columns; its gauge is irrelevant.
                    context["u"] = np.column_stack((v, frame[:, r:]))
                if model in ("gaussian_Bcov", "independent_final_variance"):
                    context.update(gaussian_factor(v))
                    context["final_variances"] = {
                        alpha: final_independent_variance(hs[alpha], context["factor"])
                        for alpha in (0, 1)}
                if model == "independent_B_marginals":
                    pmfs, repairs = [], []
                    for row in q:
                        repaired_row, row_receipt = p48.repair_probability_row(row)
                        pmf, pgf_receipt = p48.factorial_marginal(repaired_row, True)
                        if (pmf.shape != (r+1,) or np.any(pmf < 0)
                                or abs(float(pmf.sum())-1) > 3e-12):
                            raise p48.NumericalInconclusive("Invalid independent B marginal")
                        pmfs.append(pmf)
                        repairs.append({"row_repair":row_receipt,"pgf":pgf_receipt})
                    context["independent_pmf"] = np.asarray(pmfs)
                    raw_cdf = np.cumsum(context["independent_pmf"], axis=1)
                    context["independent_cdf_final_mass_correction"] = 1.-raw_cdf[:, -1].copy()
                    cdf = np.minimum(1., np.maximum.accumulate(raw_cdf, axis=1))
                    cdf[:, -1] = 1.
                    context["independent_cdf_roundoff_correction_max"] = float(abs(cdf-raw_cdf).max())
                    if context["independent_cdf_roundoff_correction_max"] > 3e-12:
                        raise p48.NumericalInconclusive("Independent marginal CDF repair too large")
                    context["independent_cdf"] = cdf
                    context["independent_marginal_repairs"] = repairs
                contexts[basis] = context
            context["basis_compute"] = meter.record()
    # Validation and reporting diagnostics do NOT inflate B's classical cost.
    diagnostics = {"status": "PASS", "source_residuals": {}, "unitary_residuals": {}}
    if spectral is not None:
        gaps = np.diff(spectral["eigenvalues"])
        marked = spectral["marked_matrix"]
        e = frames[1]
        eigen_residual = float(abs(marked @ e - e * spectral["eigenvalues"][None, :]).max())
        diagnostics.update(all_gaps=gaps, guarded_gaps=gaps[:r], boundary_gap=float(gaps[r-1]),
                           eigen_residual=eigen_residual)
        if float(gaps[:r].min()) <= 1e-12 or eigen_residual > 3e-12:
            diagnostics["status"] = "INCONCLUSIVE"
    for basis, context in contexts.items():
        v = context["v"]
        source_residual = float(abs(v.conj().T @ v - np.eye(r)).max())
        diagnostics["source_residuals"][str(basis)] = source_residual
        if source_residual > 3e-12 or np.any(context["mu"] > 1 + 3e-12):
            diagnostics["status"] = "INCONCLUSIVE"
        if "u" in context:
            residual = float(abs(context["u"].conj().T @ context["u"] - np.eye(n)).max())
            diagnostics["unitary_residuals"][str(basis)] = residual
            if residual > 3e-12:
                diagnostics["status"] = "INCONCLUSIVE"
        if "factor" in context:
            f = context["factor"]
            context["factor_covariance_residual"] = float(abs(f @ f.T - context["covariance"]).max())
    prep_wall = input_meter.wall + h_meter.wall + sum(t["wall_seconds"] for t in family_times.values())
    prep_cpu = input_meter.cpu + h_meter.cpu + sum(t["cpu_seconds"] for t in family_times.values())
    prep_wall += sum(c["basis_compute"]["wall_seconds"] for c in contexts.values())
    prep_cpu += sum(c["basis_compute"]["cpu_seconds"] for c in contexts.values())
    return {"case": case_id, "model": model, "a": a, "r": r, "k": n // 2,
            "priority": priority, "fourier_row_order": order,
            "priority_seed": priority_seed, "marks_seed": base.seed_for(5040001, case_id),
            "weight_denominator": denominator, "H": hs, "contexts": contexts,
            "spectral": spectral, "diagnostics": diagnostics,
            "input_compute": input_meter.record(), "H_compute": h_meter.record(),
            "source_family_compute": family_times,
            "classical_preparation_wall_seconds": prep_wall,
            "classical_preparation_cpu_seconds": prep_cpu,
            "other_arm_contexts_used": False, "diagnostics_enter_B_allowance": False}


def observation_components(arm, model, policy, seed):
    """Only local optical backend setup is excluded from the classical clock."""
    n, r = len(arm["a"]), arm["r"]
    context = None if policy["basis"] is None else arm["contexts"][policy["basis"]]
    seeds = {name: base.seed_for(seed, name) for name in ("jitter", "observation")}
    if len(set(seeds.values())) != len(seeds):
        raise ArithmeticError("Namespace collision")
    jitter_rng = np.random.default_rng(seeds["jitter"])
    observation_rng = np.random.default_rng(seeds["observation"])
    backend = ComputeMeter()
    if model in OPTICAL:
        with backend.measure():
            primitive, _ = base.make_optical_sampler(context["u"], list(range(r)), model,
                                                      seeds["observation"])

        def sample():
            counts, fallback = primitive()
            if fallback:
                raise ArithmeticError("No optical fallback is authorized")
            return {"counts": np.asarray(counts, dtype=np.int64)}
    elif model in ("continuous_phase", "spherical_coherent"):

        def sample():
            if model == "continuous_phase":
                angles = observation_rng.uniform(0., 2 * math.pi, r)
                coefficients = np.exp(1j * angles) / math.sqrt(r)
            else:
                coefficients = observation_rng.normal(size=r) + 1j * observation_rng.normal(size=r)
                norm = float(np.linalg.norm(coefficients))
                if norm == 0:
                    raise p48.NumericalInconclusive("Zero spherical Gaussian draw")
                coefficients /= norm
            probabilities = abs(context["v"] @ coefficients)**2
            mass = float(probabilities.sum())
            if abs(mass - 1) > 3e-12:
                raise p48.NumericalInconclusive("Invalid coherent categorical mass")
            probabilities /= mass
            counts = observation_rng.multinomial(r, probabilities)
            return {"counts": counts, "coherent_coefficients": coefficients,
                    "coherent_probability_mass_correction": 1. - mass}
    elif model in ("gaussian_Bcov", "independent_final_variance"):

        def sample():
            return {"gaussian_standard_noise": observation_rng.normal(size=n)}
    elif model == "independent_B_marginals":

        def sample():
            uniforms = observation_rng.random(n)
            counts = np.sum(uniforms[:, None] >= context["independent_cdf"], axis=1)
            return {"counts":counts,"independent_marginal_uniforms":uniforms,
                    "independent_total_count_not_conditioned":True}
    elif model in ("static_preparation", "pure_jitter"):

        def sample():
            return {}
    else:
        raise ValueError(model)

    def process(observation):
        jitter = jitter_rng.uniform(-1., 1., n)
        if model == "pure_jitter":
            before_jitter = np.zeros(n)
        else:
            h = arm["H"][policy["alpha"]]
            if model == "gaussian_Bcov":
                before_jitter = h @ (context["factor"] @ observation["gaussian_standard_noise"])
            elif model == "independent_final_variance":
                before_jitter = (np.sqrt(context["final_variances"][policy["alpha"]])
                                 * observation["gaussian_standard_noise"])
            elif model == "static_preparation":
                before_jitter = -(h @ context["mu"])
            else:
                counts = observation["counts"]
                before_jitter = h @ (counts - context["mu"])
        field = before_jitter + policy["beta"] * jitter
        subset, buckets = _rank_prevalidated(field, arm["priority"], arm["k"])
        value = base.cut(arm["a"], subset)
        return field, before_jitter, jitter, subset, buckets, value

    return sample, process, backend.record(), seeds


def run_batch(arm, model, policy, stage, trial, draws, stream):
    if stage not in ("training", "evaluation"):
        raise ValueError("Frozen training or evaluation stage required")
    namespace = 5020001 if stage == "training" else 5030001
    setup, generation, post = ComputeMeter(), ComputeMeter(), ComputeMeter()
    with setup.measure():
        seed = base.seed_for(namespace, arm["case"], model, policy["id"], trial)
        sample, process, backend, component_seeds = observation_components(arm, model, policy, seed)
    if (backend["wall_seconds"] > setup.wall + 1e-8
            or backend["cpu_seconds"] > setup.cpu + 1e-8):
        raise ArithmeticError("Backend nested clock exceeds total setup")
    classical_setup_wall = max(0., setup.wall - backend["wall_seconds"])
    classical_setup_cpu = max(0., setup.cpu - backend["cpu_seconds"])
    cuts, best, best_subset, collisions = [], None, None, 0
    for shot in range(draws):
        generation_wall, post_wall = generation.wall, post.wall
        with generation.measure():
            observation = sample()
        # Scientific integrity diagnostics, not part of B's decoding allowance.
        if "counts" in observation:
            counts = observation["counts"]
            if (counts.shape != (len(arm["a"]),) or counts.dtype.kind not in "iu"
                    or np.any(counts < 0)
                    or (model != "independent_B_marginals" and int(counts.sum()) != arm["r"])
                    or (model == "independent_B_marginals" and np.any(counts > arm["r"]))):
                raise ArithmeticError("Invalid/all-photons-discarded occupation")
        collision = bool("counts" in observation and np.any(observation["counts"] > 1))
        collisions += int(collision)
        with post.measure():
            field, before_jitter, jitter, subset, buckets, value = process(observation)
            cuts.append(value)
            if best is None or value < best:
                best, best_subset = value, subset.copy()
        emit(stream, {"stage": stage, "case": arm["case"], "model": model,
                      "policy": policy["id"], "basis": policy["basis"],
                      "alpha": policy["alpha"], "beta": policy["beta"],
                      "trial": trial, "shot": shot, "seed": seed,
                      "component_seeds": component_seeds, "cut": value,
                      "weight_denominator": arm["weight_denominator"],
                      "subset": subset, "field": field, "field_before_jitter": before_jitter,
                      "jitter": jitter, "buckets": buckets, "collision": collision,
                      "observation_generation_wall_seconds": generation.wall-generation_wall,
                      "classical_postprocessing_wall_seconds": post.wall-post_wall,
                      **observation})
    aggregation = ComputeMeter()
    with aggregation.measure():
        cut_sum = sum(cuts)
        exact_mean = Fraction(cut_sum, draws*arm["weight_denominator"])
    return {"stage": stage, "case": arm["case"], "model": model, "policy": policy["id"],
            "basis": policy["basis"], "alpha": policy["alpha"], "beta": policy["beta"],
            "trial": trial, "seed": seed, "component_seeds": component_seeds,
            "proposals": draws, "cuts": cuts, "sum_cuts": cut_sum,
            "weight_denominator": arm["weight_denominator"],
            "exact_mean_normalized_cut": str(exact_mean),
            "best_cut": best, "best_subset": best_subset, "collision_samples": collisions,
            "observation_setup_wall_seconds": setup.wall, "observation_setup_cpu_seconds": setup.cpu,
            "backend_setup_wall_seconds": backend["wall_seconds"],
            "backend_setup_cpu_seconds": backend["cpu_seconds"],
            "classical_setup_wall_seconds": classical_setup_wall,
            "classical_setup_cpu_seconds": classical_setup_cpu,
            "observation_generation_wall_seconds": generation.wall,
            "observation_generation_cpu_seconds": generation.cpu,
            "classical_generation_wall_seconds": 0. if model in OPTICAL else generation.wall,
            "classical_generation_cpu_seconds": 0. if model in OPTICAL else generation.cpu,
            "classical_postprocessing_wall_seconds": post.wall,
            "classical_postprocessing_cpu_seconds": post.cpu,
            "classical_aggregation_wall_seconds": aggregation.wall,
            "classical_aggregation_cpu_seconds": aggregation.cpu,
            "backend_and_count_generation_are_subtotals_not_extra_costs": True,
            "serialization_excluded": True}


def select_policies(training, cases, model_subset=MODELS):
    """Exact ALL-shot equal-graph loss; no eval, minimum, incumbent or success input."""
    if not cases or any(row["stage"] != "training" for row in training):
        raise ValueError("Training only on the full frozen population")
    case_ids = [case["id"] for case in cases]
    if len(set(case_ids)) != len(case_ids) or any(model not in MODELS for model in model_subset):
        raise ValueError("Invalid population/model")
    denominators = {case["id"]: case["weight_denominator"] for case in cases}
    selected, losses = {}, {}
    for model in model_subset:
        exact = {}
        for policy in policies(model):
            rows = [row for row in training if row["model"] == model and row["policy"] == policy["id"]]
            if sorted(row["case"] for row in rows) != sorted(case_ids):
                raise ValueError("All frozen graphs exactly once per training policy")
            values = []
            for row in rows:
                if (row["proposals"] != policy["training_draws"]
                        or len(row["cuts"]) != row["proposals"]
                        or row["sum_cuts"] != sum(row["cuts"])
                        or row["weight_denominator"] != denominators[row["case"]]):
                    raise ValueError("Allocation or all-shot normalization changed")
                values.append(Fraction(row["sum_cuts"], row["proposals"]*row["weight_denominator"]))
            exact[policy["id"]] = sum(values, Fraction(0)) / len(cases)
        selected[model] = min(exact, key=lambda p: (exact[p], p))
        losses[model] = exact
    return selected, losses


def evaluate_fixed(arm, model, policy, stream):
    return [run_batch(arm, model, policy, "evaluation", trial, 16, stream) for trial in (0, 1)]


def fast_comparison(raw, case_id, b_arm, b_records, selection_share, initialization, max_proposals):
    if initialization not in FAST_INITIALIZATIONS:
        raise ValueError("Frozen from-scratch initialization")
    if any(row["model"] != "bosonic" or row["case"] != case_id for row in b_records):
        raise ValueError("Only THIS B arm may fund the classical allowance")
    allowance = b_arm["classical_preparation_wall_seconds"] + selection_share
    allowance += sum(row["classical_setup_wall_seconds"]
                     + row["classical_postprocessing_wall_seconds"]
                     + row["classical_aggregation_wall_seconds"] for row in b_records)
    adapter = ComputeMeter()
    with adapter.measure():
        seed = base.seed_for(5050001, case_id, initialization)
    result = fast.solve_from_raw(raw, seed=seed, initialization=initialization,
                                 cpu_budget_seconds=max(0., allowance-adapter.cpu),
                                 max_proposals=max_proposals)
    eligible = (result["has_eligible_result"] and result["comparison_acceptance_eligible"]
                and not result["early_cap_inconclusive"])
    if result.get("early_wall_inconclusive", False):
        eligible = False
    return {"case": case_id, "initialization": initialization, "seed": seed,
            "total_CPU_allowance_including_adapter": allowance,
            "adapter_compute": adapter.record(), "solver_CPU_allowance": max(0., allowance-adapter.cpu),
            "B_only_preparation_wall_grant": b_arm["classical_preparation_wall_seconds"],
            "B_only_classical_setup_and_decode_wall_grant": sum(
                row["classical_setup_wall_seconds"]+row["classical_postprocessing_wall_seconds"]
                +row["classical_aggregation_wall_seconds"]
                for row in b_records),
            "B_selection_wall_share": selection_share,
            "other_model_preparation_or_diagnostic_seconds_granted": 0.,
            "optical_backend_or_count_seconds_granted": 0., "serialization_seconds_granted": 0.,
            "initial_reference_or_priority_given": False,
            "comparison_acceptance_eligible": bool(eligible),
            "eligible_best_cut": result["best_cut"], "eligible_best_subset": result["best_subset"],
            "result": result}


def arm_incumbents(records):
    """Only actually sampled/scored partitions, with no free Cref."""
    result = {}
    for model in MODELS:
        result[model] = {}
        for case_id in sorted({row["case"] for row in records}):
            chosen = [row for row in records if row["case"] == case_id and row["model"] == model]
            result[model][case_id] = {}
            for label, stages in (("training", ("training",)), ("fresh_evaluation", ("evaluation",)),
                                  ("paid_total", ("training", "evaluation"))):
                rows = [row for row in chosen if row["stage"] in stages]
                if rows:
                    winner = min(rows, key=lambda row: row["best_cut"])
                    result[model][case_id][label] = {"cut": winner["best_cut"],
                                                    "subset": winner["best_subset"]}
    return result


def check_output_budget(output, limit, reserve=0):
    size = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    if size > limit-reserve:
        raise RuntimeError("P50 output cap approached; retain partial run without retry")


def save_gzip_json(path, payload):
    with path.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as compressed:
        with io.TextIOWrapper(compressed, encoding="utf8") as text:
            json.dump(serial(payload), text, allow_nan=False)


def _validate_spec(spec):
    expected = [("n50_ER_5005001",50,25,13,"ER",5005001), ("n50_RR_5005002",50,25,13,"RR",5005002),
                ("n100_ER_5010001",100,50,17,"ER",5010001), ("n100_RR_5010002",100,50,17,"RR",5010002)]
    if (spec["positive_acceptance_allowed"] or spec["ideal_transmission_eta"] != 1.
            or spec["models"] != list(MODELS) or spec["bases"] != list(BASES)
            or spec["policy_grids"] != {model: policies(model) for model in MODELS}
            or spec["tie_width"] != TIE_WIDTH
            or spec["tie_definition"] != "floor((y-max(y))/width+.5),descending_bucket_then_carried_rank"
            or spec["graph_ER_mean_degree"] != 8 or spec["graph_RR_degree"] != 8
            or spec["graph_weight_low_inclusive"] != 1 or spec["graph_weight_high_inclusive"] != 5
            or spec["marker_coefficient"] != .001 or spec["gap_tolerance"] != 1e-12
            or spec["residual_tolerance"] != 3e-12 or spec["covariance_PSD_tolerance"] != 1e-10
            or spec["fast_initializations"] != list(FAST_INITIALIZATIONS)
            or spec["fast_max_proposals"] != 100000000
            or spec["evaluation_trials"] != [0,1] or spec["evaluation_draws_per_trial"] != 16
            or spec["seed_namespaces"] != {"training":5020001,"evaluation":5030001,
                "marks":5040001,"priority_and_Fourier_row_order":5040002,"FAST":5050001}
            or spec["maximum_planned_arrays_bytes"] != 268435456
            or spec["maximum_cpu_seconds"] != 60 or spec["maximum_wall_seconds"] != 90
            or spec["maximum_threads"] != 1 or spec["maximum_new_output_bytes"] != 33554432
            or [(c["id"],c["m"],c["k"],c["r"],c["family"],c["seed"]) for c in spec["cases"]] != expected):
        raise ValueError("Frozen P50 protocol changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    _validate_spec(spec)
    args.output.mkdir(parents=True, exist_ok=False)
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    graphs, arms, records, selections, losses, selection_times = {}, {}, [], {}, {}, {}
    training_by_model = {model:[] for model in MODELS}
    failures, fast_records = [], []
    raw_path = args.output/"raw.jsonl.gz"
    with raw_path.open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped, encoding="utf8") as stream:
            for case in spec["cases"]:
                case_id = case["id"]
                graphs[case_id] = make_graph(case)  # Supplied-instance generation excluded symmetrically.
                arms[case_id] = {}
                for model in MODELS:
                    try:
                        arm = prepare_arm(graphs[case_id], case, model)
                        arms[case_id][model] = arm
                        if arm["diagnostics"]["status"] != "PASS":
                            failures.append({"case":case_id,"model":model,"reason":"numerical_guard"})
                        emit(stream, {"stage":"preparation_diagnostic","case":case_id,"model":model,
                                      "diagnostics":arm["diagnostics"]})
                    except (p48.NumericalInconclusive, np.linalg.LinAlgError) as error:
                        failure = {"case":case_id,"model":model,"reason":repr(error)}
                        failures.append(failure)
                        emit(stream, {"stage":"preparation_failure",**failure})
                save_gzip_json(args.output/f"context_{case_id}.json.gz", {"case":case,
                               "supplied_adjacency":graphs[case_id],"arms":arms[case_id]})
                stream.flush(); zipped.flush(); raw.flush()
                check_output_budget(args.output, spec["maximum_new_output_bytes"], 2097152)
            population_complete = not failures and all(len(arms[c["id"]]) == len(MODELS) for c in spec["cases"])
            if population_complete:
                for case in spec["cases"]:
                    for model in MODELS:
                        arm = arms[case["id"]][model]
                        for policy in policies(model):
                            row = run_batch(arm,model,policy,"training",0,policy["training_draws"],stream)
                            training_by_model[model].append(row); records.append(row)
                selection_cases = [{"id":case["id"],"weight_denominator":arms[case["id"]]["bosonic"]["weight_denominator"]}
                                   for case in spec["cases"]]
                for model in MODELS:
                    meter = ComputeMeter()
                    with meter.measure():
                        choice, model_losses = select_policies(training_by_model[model],selection_cases,(model,))
                        selections[model] = choice[model]
                    selection_times[model] = meter.record()
                    # Exact Fraction computation/selection is paid; JSON-oriented
                    # string/float formatting is outside the allowance.
                    losses[model] = {str(p):{"exact_fraction":str(value),"float":float(value)}
                                     for p,value in model_losses[model].items()}
                for case in spec["cases"]:
                    for model in MODELS:
                        records.extend(evaluate_fixed(arms[case["id"]][model],model,
                                                       policies(model)[selections[model]],stream))
                    stream.flush(); zipped.flush(); raw.flush()
                    check_output_budget(args.output,spec["maximum_new_output_bytes"],2097152)
            for case in spec["cases"]:
                case_id = case["id"]
                for initialization in FAST_INITIALIZATIONS:
                    path = args.output/f"fast_{initialization}_{case_id}.json.gz"
                    if population_complete:
                        b_records = [row for row in records if row["case"]==case_id and row["model"]=="bosonic"]
                        comparison = fast_comparison(graphs[case_id],case_id,arms[case_id]["bosonic"],b_records,
                                                     selection_times["bosonic"]["wall_seconds"]/4,
                                                     initialization,spec["fast_max_proposals"])
                        save_gzip_json(path,fast.json_safe_result(comparison))
                        compact = dict(comparison)
                        compact["result"] = {key:value for key,value in comparison["result"].items() if key!="trace"}
                        fast_records.append(compact)
                    else:
                        save_gzip_json(path,{"status":"NOT_RUN_INCOMPLETE_POPULATION","case":case_id,
                                             "initialization":initialization})
                    check_output_budget(args.output,spec["maximum_new_output_bytes"],2097152)
    counts = {model:{stage:sum(row["proposals"] for row in records if row["model"]==model and row["stage"]==stage)
                     for stage in ("training","evaluation")} for model in MODELS}
    expected = 128 if population_complete else 0
    if any(counts[model][stage] != expected for model in MODELS for stage in ("training","evaluation")):
        raise ArithmeticError("P50 full paid population changed")
    evaluation_means, spending, deployment = {}, {}, {}
    for model in MODELS:
        chosen = [row for row in records if row["model"]==model]
        if population_complete:
            means=[]
            for case in spec["cases"]:
                rows=[row for row in chosen if row["case"]==case["id"] and row["stage"]=="evaluation"]
                means.append(Fraction(sum(row["sum_cuts"] for row in rows),32*rows[0]["weight_denominator"]))
            mean=sum(means,Fraction(0))/4
            evaluation_means[model]={"exact_fraction":str(mean),"float":float(mean)}
        spending[model]={"proposals":counts[model],"actual_QPU_photons":0,
                         "simulated_injected_photons":3840 if model in OPTICAL and population_complete else 0,
                         "preparation_by_graph":{case["id"]:{key:arm[key] for key in (
                             "classical_preparation_wall_seconds","classical_preparation_cpu_seconds")}
                             for case in spec["cases"] if (arm:=arms[case["id"]].get(model)) is not None},
                         "batch_components":{key:sum(row[key] for row in chosen) for key in (
                             "backend_setup_wall_seconds","backend_setup_cpu_seconds",
                             "classical_setup_wall_seconds","classical_setup_cpu_seconds",
                             "observation_generation_wall_seconds","observation_generation_cpu_seconds",
                             "classical_generation_wall_seconds","classical_generation_cpu_seconds",
                             "classical_postprocessing_wall_seconds","classical_postprocessing_cpu_seconds",
                             "classical_aggregation_wall_seconds","classical_aggregation_cpu_seconds")},
                         "selection":selection_times.get(model,{})}
        if population_complete:
            policy=policies(model)[selections[model]]
            deployment[model]={"selected_policy":policy,"evaluation_shots_per_graph":32,
                               "training_repeated":False,"evaluation_batches":[row for row in chosen if row["stage"]=="evaluation"],
                               "selected_basis_observed_setup_by_graph":{}}
            for case in spec["cases"]:
                arm=arms[case["id"]][model]; basis=policy["basis"]
                family=None if basis is None else ("Fourier_blind" if basis==0 else "spectral_E")
                deployment[model]["selected_basis_observed_setup_by_graph"][case["id"]]={
                    "input_compute":arm["input_compute"],"both_H_compute_upper_bound":arm["H_compute"],
                    "required_source_family_compute":{} if family is None else arm["source_family_compute"][family],
                    "basis_compute":{} if basis is None else arm["contexts"][basis]["basis_compute"],
                    "observed_subtotals_not_added_to_experimental_cost_twice":True,
                    "not_an_optimized_minimal_or_hardware_cost":True}
    fast_complete=population_complete and all(row["comparison_acceptance_eligible"] for row in fast_records)
    summary={"status":"EXPLORATORY_DEV_ONLY" if fast_complete else "INCONCLUSIVE_CONTROL_OR_NUMERICS",
             "positive_accepted":False,"full_frozen_population_completed":population_complete,
             "actual_QPU_calls":0,"heldout_opened":False,"optimum_used":False,
             "source_loaded_from_training_partition":False,"reference_partition_used":False,
             "selection_frozen_before_evaluation":True,"all_shots_in_selection":True,
             "failures":failures,"selected_policies":selections,"training_losses":losses,
             "fresh_evaluation_normalized_means":evaluation_means,"proposal_counts":counts,
             "private_paid_incumbents":arm_incumbents(records),"spending":spending,
             "selected_policy_deployment_ledgers":deployment,"primary_batches":records,
             "FAST_comparisons":fast_records,"FAST_all_eligible":fast_complete,
             "Fourier_static_law_duplicates_pure_jitter_both_alphas":True,
             "no_general_diffusion_cut_improvement_asserted":True,
             "cpu_seconds_inside_main":time.process_time()-start_cpu,
             "wall_seconds_inside_main":time.perf_counter()-start_wall,
             "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
             "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
             "FAST_module_sha256":hashlib.sha256(Path("research/P50_fast_from_scratch.py").read_bytes()).hexdigest(),
             "simulation_time_is_QPU_time":False,"timing_envelope_is_hardware_advantage":False}
    (args.output/"summary.json").write_text(json.dumps(serial(summary),indent=2,allow_nan=False)+"\n")
    check_output_budget(args.output,spec["maximum_new_output_bytes"])
    print(json.dumps({key:serial(summary[key]) for key in ("status","positive_accepted",
                      "full_frozen_population_completed","selected_policies","fresh_evaluation_normalized_means",
                      "cpu_seconds_inside_main","wall_seconds_inside_main","raw_sha256")}))


if __name__ == "__main__":
    main()
