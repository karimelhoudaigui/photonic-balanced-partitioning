"""P46 DEV veto: hollow-unitary bulk transfer with marginal-PIT completion.

No optimum oracle, device access, held-out graph or accepted positive claim.
P45 A/P43 helpers are immutable inputs; all new operations live in this file.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linear_sum_assignment
from scipy.special import ndtr

import P43_global_gain_probe as base
import P45_adaptive_probe as adaptive

MODELS = ("bosonic", "distinguishable", "species4", "gaussian_Bcov",
          "iid_uniform", "conditional_phase")
BASELINES = ("anneal", "spectral_swap", "KL_collective", "block_matching")


def emit(stream, row):
    stream.write(json.dumps(row, allow_nan=False)+"\n")


def block_unitary(w, transfer_p):
    """cos(t)I-i sin(t)H; H=[[0,W],[W*,0]], H²=I, sin²(t)=p."""
    k = len(w)
    if w.shape != (k, k) or not 0 < transfer_p < 1:
        raise ValueError("Invalid hollow block")
    eye = np.eye(k)
    c, s = math.sqrt(1-transfer_p), math.sqrt(transfer_p)
    return np.block([[c*eye, -1j*s*w], [-1j*s*w.conj().T, c*eye]])


def build_network(a, inside, outside, delta, zeta, transfer_p):
    k, m = len(inside), len(a)
    j = np.eye(k)-np.ones((k, k))/k
    centered = j@delta@j
    norm = float(np.linalg.norm(centered, 2))
    perturbation = centered/norm if norm > 1e-12 else np.zeros_like(centered)
    ii = np.arange(k)
    fourier = np.exp(2j*np.pi*ii[:, None]*ii[None, :]/k)/math.sqrt(k)
    polar_input = fourier+1j*zeta*perturbation
    left, singular, right = np.linalg.svd(polar_input)
    w = left@right
    if singular.min() < 1-zeta-2e-12:
        raise ArithmeticError("Polar invertibility certificate failed")
    u_block = block_unitary(w, transfer_p)
    order = list(inside)+list(outside)
    u = np.zeros((m, m), dtype=complex)
    u[np.ix_(order, order)] = u_block
    residual = float(abs(u.conj().T@u-np.eye(m)).max())
    if residual > 3e-12:
        raise ArithmeticError("Nonunitary hollow circuit")
    v = u[:, inside]
    probabilities = abs(v)**2
    mu = probabilities.sum(axis=1)
    projection = v@v.conj().T
    cov = np.diag(mu)+abs(projection)**2-2*probabilities@probabilities.T
    cov = (cov+cov.T)/2
    eigenvalues, vectors = np.linalg.eigh(cov)
    if eigenvalues.min() < -1e-10:
        raise ArithmeticError("Negative B covariance")
    factor = vectors*np.sqrt(np.maximum(eigenvalues, 0))[None, :]
    target_variance = np.diag(cov).copy()
    # Phi must use the variance of the ACTUAL sampled factor after clipping,
    # not the target covariance diagonal before that numerical operation.
    effective_variance = np.sum(factor**2, axis=1)
    effective_covariance_residual = float(abs(factor@factor.T-cov).max())
    # Fixed diagnostics are recorded for EVERY graph, never used as filters.
    quartets = np.einsum("ia,jb,ja,ib->ijab", w, w, w.conj(), w.conj())
    distinct = ((np.arange(k)[:, None, None, None] != np.arange(k)[None, :, None, None])
                & (np.arange(k)[None, None, :, None] != np.arange(k)[None, None, None, :]))
    off_quartets = quartets[distinct]
    return {"u":u, "v":v, "probabilities":probabilities, "mu":mu,
            "cov":cov, "factor":factor, "variance":effective_variance,
            "target_variance":target_variance,
            "Gaussian_factor_covariance_residual":effective_covariance_residual,
            "Gaussian_variance_residual":float(abs(effective_variance-target_variance).max()), "w":w,
            "centered_delta_norm":norm, "polar_singular_min":float(singular.min()),
            "centered_stable_rank":float(np.linalg.norm(centered, "fro")**2/norm**2) if norm > 1e-12 else 0.,
            "W_minus_F_frobenius_squared":float(np.linalg.norm(w-fourier, "fro")**2),
            "W_I4":float(np.sum(abs(w)**4)),
            "W_quartet_real_min":float(off_quartets.real.min()) if off_quartets.size else 0.,
            "W_quartet_real_max":float(off_quartets.real.max()) if off_quartets.size else 0.,
            "W_quartet_abs_imag_max":float(abs(off_quartets.imag).max()) if off_quartets.size else 0.,
            "unitary_residual":residual, "inside":list(inside), "outside":list(outside),
            "p":transfer_p, "zeta":zeta}


def marginal_pmf(probabilities, bosonic):
    """E z^n=Σ_r(r! for B,1 for D)e_r(p)(z-1)^r; 80-digit coefficient arithmetic."""
    n = len(probabilities)
    with localcontext() as ctx:
        ctx.prec = 80
        elementary = [Decimal(1)]+[Decimal(0)]*n
        for index, probability in enumerate(probabilities):
            value = Decimal.from_float(float(probability))
            if not Decimal(0) <= value <= Decimal(1)+Decimal("1e-12"):
                raise ArithmeticError("Invalid one-particle probability")
            for r in range(index+1, 0, -1):
                elementary[r] += value*elementary[r-1]
        coefficients = [value*(math.factorial(r) if bosonic else 1)
                        for r, value in enumerate(elementary)]
        result = [sum((Decimal((-1)**(r-s)*math.comb(r, s))*coefficients[r]
                       for r in range(s, n+1)), Decimal(0)) for s in range(n+1)]
    pmf = np.asarray([float(value) for value in result])
    if pmf.min() < -1e-12 or abs(pmf.sum()-1) > 1e-12:
        raise ArithmeticError("Invalid marginal distribution")
    pmf = np.maximum(pmf, 0)
    return pmf/pmf.sum()


def all_marginals(context, species_order):
    start = time.perf_counter()
    p = context["probabilities"]
    k, m = p.shape[1], p.shape[0]
    tables, seconds = {}, {}
    for model, bosonic in (("bosonic", True), ("distinguishable", False)):
        t0 = time.perf_counter()
        tables[model] = np.asarray([marginal_pmf(row, bosonic) for row in p])
        seconds[model] = time.perf_counter()-t0
    t0 = time.perf_counter()
    input_index = {vertex:index for index, vertex in enumerate(context["inside"])}
    groups = [[input_index[v] for v in species_order[i:i+4]] for i in range(0, k, 4)]
    group_table = []
    for i in range(m):
        pmf = np.ones(1)
        for group in groups:
            pmf = np.convolve(pmf, marginal_pmf(p[i, group], True))
        group_table.append(pmf/pmf.sum())
    tables["species4"] = np.asarray(group_table)
    seconds["species4"] = time.perf_counter()-t0
    for table in tables.values():
        for i in context["inside"]:
            table[i] = 0
            table[i, 0], table[i, 1] = context["p"], 1-context["p"]
    return tables, seconds, time.perf_counter()-start


def pit(counts, pmf, jitter):
    original = np.asarray(counts)
    counts = np.asarray(counts, dtype=int)
    if not np.all(original == counts):
        raise ValueError("Noninteger counts")
    if len(counts) != len(pmf) or np.any(counts < 0) or np.any(counts >= pmf.shape[1]):
        raise ValueError("Counts outside marginal support")
    jitter = np.asarray(jitter, dtype=float)
    if jitter.shape != counts.shape or np.any(jitter < 0) or np.any(jitter >= 1):
        raise ValueError("Jitter must be one independent [0,1) value per mode")
    cumulative = np.cumsum(pmf, axis=1)
    index = np.arange(len(counts))
    mass = pmf[index, counts]
    left = np.where(counts > 0, cumulative[index, np.maximum(counts-1, 0)], 0.)
    u = left+jitter*mass
    if u.min() < -1e-12 or u.max() > 1+1e-12:
        raise ArithmeticError("Invalid randomized PIT")
    return np.clip(u, 0., 1.)


def conditional_phase_sampler(context, seed):
    """Exact old Bernoulli pattern, coherent-phase multinomial on transferred inputs."""
    seeds = [base.seed_for(seed, role) for role in ("transfer_mask", "phase", "new_counts")]
    if len(set(seeds)) != len(seeds):
        raise ArithmeticError("Conditional-control component seed collision")
    mask_rng, phase_rng, counts_rng = [np.random.default_rng(s) for s in seeds]
    inside, outside = context["inside"], context["outside"]
    k, m, p = len(inside), len(context["u"]), context["p"]
    transfer = context["u"][np.ix_(outside, inside)]/math.sqrt(p)
    def draw():
        active = mask_rng.random(k) < p
        counts = np.zeros(m, dtype=int)
        counts[inside] = ~active
        number = int(active.sum())
        if number:
            phase = phase_rng.choice((1., -1., 1j, -1j), size=number)
            field = transfer[:, active]@phase
            probabilities = abs(field)**2/number
            if abs(probabilities.sum()-1) > 2e-12:
                raise ArithmeticError("Conditional field lost normalization")
            counts[outside] = counts_rng.multinomial(number, probabilities/probabilities.sum())
        return counts
    return draw


def calibrate_phase(context, seed, samples, confidence_failure):
    start = time.perf_counter()
    draw = conditional_phase_sampler(context, seed)
    m, k = len(context["u"]), len(context["inside"])
    histogram = np.zeros((m, k+1), dtype=np.int64)
    for _ in range(samples):
        counts = draw()
        histogram[np.arange(m), counts] += 1
    pmf = histogram/samples
    # Old outputs are exactly Bernoulli for this stronger control, not estimated.
    for i in context["inside"]:
        pmf[i] = 0
        pmf[i, 0], pmf[i, 1] = context["p"], 1-context["p"]
    return pmf, {"seed":seed, "samples":samples, "histogram":histogram.tolist(),
                 "old_marginals_exact":True, "new_marginals_empirical":True,
                 "per_new_mode_DKW_radius":math.sqrt(math.log(2/confidence_failure)/(2*samples)),
                 "per_new_mode_TV_union_Hoeffding_radius":math.sqrt(
                     ((k+1)*math.log(2)+math.log(1/confidence_failure))/(2*samples)),
                 "per_new_mode_failure":confidence_failure,
                 "calibration_is_global_unconditional_A":True,
                 "joint_copula_error_certified":False,
                 "calibration_seconds":time.perf_counter()-start,
                 "objective_scores":0, "photon_attempts":0}


def make_field(context, species_order, model, seed, tables):
    jitter_rng = np.random.default_rng(base.seed_for(seed, "PIT_jitter"))
    noise_rng = np.random.default_rng(base.seed_for(seed, "continuous_noise"))
    k, m = len(context["inside"]), len(context["u"])
    sample = None
    if model in ("bosonic", "distinguishable", "species4"):
        source = species_order if model == "species4" else context["inside"]
        primitive, _ = base.make_optical_sampler(context["u"], source, model,
                                                base.seed_for(seed, "physical_counts"))
        sample = lambda: primitive()[0]
    elif model == "conditional_phase":
        sample = conditional_phase_sampler(context, base.seed_for(seed, "phase_counts"))
    def draw():
        if sample is not None:
            counts = sample()
            if counts.sum() != k or np.any(counts < 0):
                raise ArithmeticError("Invalid full count sample")
            jitter = jitter_rng.random(m)
            u = pit(counts, tables[model], jitter)
            return u-.5, counts, {"pit_jitter":jitter.tolist()}
        if model == "gaussian_Bcov":
            raw = context["factor"]@noise_rng.normal(size=m)
            positive = context["variance"] > 0
            u = jitter_rng.random(m)
            u[positive] = ndtr(raw[positive]/np.sqrt(context["variance"][positive]))
            return u-.5, None, {"gaussian_raw":raw.tolist()}
        if model == "iid_uniform":
            return noise_rng.random(m)-.5, None, {}
        raise ValueError(model)
    return draw


class TimedBaselineStream:
    """Preserve immutable helper output plus per-query elapsed times for joint frontiers."""
    def __init__(self, stream):
        self.stream, self.started, self.rows = stream, time.perf_counter(), []
    def write(self, text):
        row = json.loads(text)
        row["baseline_elapsed_seconds"] = time.perf_counter()-self.started
        self.rows.append((row["baseline_elapsed_seconds"], row["cut"]))
        emit(self.stream, row)
        return len(text)


def block_matching(a, source, inside, outside, delta, reference, seed, budget, stream, tag):
    """Fixed-anchor nonlocal baseline using ALL shared swap information.

    Selected inside vertices transfer with alternating p=.25/.5. A rectangular
    Hungarian assignment selects distinct destinations using the already shared
    delta table. Every resulting feasible partition is scored and charged once.
    The actual simultaneous-move cut can differ from the summed single deltas.
    """
    rng = np.random.default_rng(seed)
    started = time.perf_counter()
    best = reference
    for step in range(budget):
        p = (.25, .5)[step % 2]
        selected = np.flatnonzero(rng.random(len(inside)) < p)
        if len(selected):
            row, column = linear_sum_assignment(delta[selected])
            removed = [inside[int(selected[r])] for r in row]
            added = [outside[int(c)] for c in column]
        else:
            removed, added = [], []
        subset = sorted((set(source)-set(removed))|set(added))
        value = base.cut(a, subset)
        best = min(best, value)
        emit(stream, dict(tag, model="block_matching", step=step, seed=seed,
                          p=p, removed=removed, added=added, subset=subset,
                          cut=value, best_cut=best))
    return {"model":"block_matching", "candidate_scores":budget,
            "initial_cut":reference, "best_cut":best,
            "search_and_scoring_seconds":time.perf_counter()-started,
            "anchor_is_fixed_S0":True, "all_delta_scores_shared":True}


def prepare(case, spec, stream, output):
    case_id, k = case["id"], case["k"]
    started = time.perf_counter()
    a = base.make_graph(case)
    source, anchor = base.prepare_anchor(a, base.seed_for(461010, case_id),
                                        spec["anchor_max_scans"], stream, case_id)
    inside = np.random.default_rng(base.seed_for(461020, case_id)).permutation(source).tolist()
    outside = np.random.default_rng(base.seed_for(461030, case_id)).permutation(
        [i for i in range(len(a)) if i not in source]).tolist()
    priority = np.random.default_rng(base.seed_for(461040, case_id)).permutation(len(a)).tolist()
    species = np.random.default_rng(base.seed_for(461050, case_id)).permutation(inside).tolist()
    ell = a.sum(axis=1)-2*a[:, source].sum(axis=1)
    delta = np.zeros((k, k))
    candidates = [(base.cut(a, source), source)]
    front_units = anchor["candidate_scores_including_initial"]
    front_feasible_scores, front_marginals = front_units, 0
    for i, old in enumerate(inside):
        for j, new in enumerate(outside):
            subset = sorted((set(source)-{old})|{new})
            value = base.cut(a, subset)
            delta[i, j] = ell[new]-ell[old]+2*a[old, new]
            if value-candidates[0][0] != delta[i, j]:
                raise ArithmeticError("Swap feature orientation mismatch")
            emit(stream, {"stage":"common_swap", "case":case_id, "old":old,
                          "new":new, "subset":subset, "cut":value,
                          "delta":float(delta[i, j])})
            candidates.append((value, subset)); front_units += 1; front_feasible_scores += 1
    graph_swap_seconds = time.perf_counter()-started
    contexts, saved_networks = [], []
    for index, (transfer_p, zeta) in enumerate(spec["network_grid_p_zeta"]):
        t0 = time.perf_counter()
        context = build_network(a, inside, outside, delta, zeta, transfer_p)
        network_seconds = time.perf_counter()-t0
        tables, pmf_seconds, all_pmf_seconds = all_marginals(context, species)
        phase_table, calibration = calibrate_phase(context, base.seed_for(461060, case_id, index),
            spec["phase_calibration_samples"], spec["phase_DKW_failure_per_mode"])
        tables["conditional_phase"] = phase_table
        context.update({"tables":tables, "network_seconds":network_seconds,
                        "pmf_seconds":pmf_seconds, "all_pmf_seconds":all_pmf_seconds,
                        "phase_calibration":calibration})
        contexts.append(context)
        saved_networks.append({"p":transfer_p, "zeta":zeta,
            "u_real":context["u"].real.tolist(), "u_imag":context["u"].imag.tolist(),
            "mu":context["mu"].tolist(), "covariance_B":context["cov"].tolist(),
            "Gaussian_target_variance":context["target_variance"].tolist(),
            "Gaussian_effective_factor_variance":context["variance"].tolist(),
            "Gaussian_factor_covariance_residual":context["Gaussian_factor_covariance_residual"],
            "Gaussian_variance_residual":context["Gaussian_variance_residual"],
            "marginal_pmfs":{model:table.tolist() for model, table in tables.items()},
            "pmf_computation_seconds":pmf_seconds, "phase_calibration":calibration,
            "unitary_residual":context["unitary_residual"],
            "polar_singular_min":context["polar_singular_min"],
            "centered_delta_norm":context["centered_delta_norm"],
            "centered_stable_rank":context["centered_stable_rank"],
            "W_minus_F_frobenius_squared":context["W_minus_F_frobenius_squared"],
            "W_I4":context["W_I4"],
            "W_quartet_real_min":context["W_quartet_real_min"],
            "W_quartet_real_max":context["W_quartet_real_max"],
            "W_quartet_abs_imag_max":context["W_quartet_abs_imag_max"],
            "network_seconds":network_seconds})
    decoder_start = time.perf_counter()
    for label, q in (("zero", (k+1)//2), ("pure_greedy", 0)):
        result = adaptive.complete(a, np.zeros(len(a)), k, 0, priority, q)
        emit(stream, dict(stage="frontend_decoder", case=case_id, label=label, **result))
        candidates.append((result["cut"], result["subset"])); front_units += result["score_units"]
        front_feasible_scores += 1; front_marginals += result["marginal_evaluations"]
    for index, context in enumerate(contexts):
        for model, table in context["tables"].items():
            field = pit(np.zeros(len(a), dtype=int), table, np.full(len(a), .5))-.5
            for lam in spec["decoder_lambda"]:
                result = adaptive.complete(a, field, k, lam, priority, (k+1)//2)
                emit(stream, dict(stage="frontend_decoder", case=case_id,
                    label="vacuum_mid_PIT", network=index, model=model, lam=lam, **result))
                candidates.append((result["cut"], result["subset"])); front_units += result["score_units"]
                front_feasible_scores += 1; front_marginals += result["marginal_evaluations"]
    cref, reference = min(candidates, key=lambda row:(row[0], row[1]))
    common = {"anchor":anchor, "source_S0":source, "inside_order":inside,
              "outside_order":outside, "vertex_priority":priority, "species_order":species,
              "Cref":cref, "reference_subset":reference,
              "frontend_score_units":front_units, "graph_and_swaps_seconds":graph_swap_seconds,
              "frontend_feasible_cut_scores":front_feasible_scores,
              "frontend_partial_marginal_scores":front_marginals,
              "decoder_frontend_seconds":time.perf_counter()-decoder_start,
              "total_common_preprocessing_seconds":time.perf_counter()-started}
    saved = dict(common, adjacency=a.tolist(), delta_swap=delta.tolist(), networks=saved_networks)
    (output/f"context_{case_id}.json").write_text(json.dumps(saved, indent=2)+"\n")
    return a, contexts, common, delta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    if (spec["models"] != list(MODELS) or spec["positive_acceptance_allowed"]
            or spec["baseline_models"] != list(BASELINES)
            or spec["network_grid_p_zeta"] != [[.25,0.],[.25,.25],[.5,0.],[.5,.25]]
            or spec["decoder_lambda"] != [0,1] or spec["trial_seeds"] != [0,1]
            or spec["draws_per_tuple"] != 4 or spec["phase_calibration_samples"] != 4096
            or [(c["m"],c["k"],c["seed"]) for c in spec["cases"]]
               != [(24,12,4602401),(24,12,4602402),(28,14,4602801),(28,14,4602802)]):
        raise ValueError("Frozen veto population mismatch")
    args.output.mkdir(parents=True, exist_ok=False)
    start_cpu, start_wall = time.process_time(), time.perf_counter()
    records, commons = [], {}
    totals = {model:np.zeros(8) for model in MODELS}
    raw_path = args.output/"raw.jsonl.gz"
    with raw_path.open("xb") as raw_file, gzip.GzipFile(fileobj=raw_file, mode="wb", mtime=0, compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped, encoding="utf8") as stream:
            for case in spec["cases"]:
                case_id, k = case["id"], case["k"]
                a, contexts, common, delta = prepare(case, spec, stream, args.output)
                commons[case_id] = common
                priority, cref = common["vertex_priority"], common["Cref"]
                q = (k+1)//2
                marginal_units = sum(len(a)-r for r in range(q, k))
                expected_units = marginal_units+1
                for replicate in spec["trial_seeds"]:
                    key = f"{case_id}:{replicate}"
                    time_budgets = defaultdict(float)
                    for model in MODELS:
                        for index, context in enumerate(contexts):
                            for lam_index, lam in enumerate(spec["decoder_lambda"]):
                                setting = 2*index+lam_index
                                seed = base.seed_for(461100, key, model, setting)
                                setting_start = time.perf_counter()
                                setup_start = time.perf_counter()
                                draw = make_field(context, common["species_order"], model, seed, context["tables"])
                                setup_seconds = time.perf_counter()-setup_start
                                sample_seconds = decoder_seconds = 0.
                                gains, best, score_units = [], cref, 0
                                for shot in range(spec["draws_per_tuple"]):
                                    t0 = time.perf_counter()
                                    field, counts, extra = draw()
                                    sample_seconds += time.perf_counter()-t0
                                    t0 = time.perf_counter()
                                    result = adaptive.complete(a, field, k, lam, priority, q)
                                    decoder_seconds += time.perf_counter()-t0
                                    if result["score_units"] != expected_units:
                                        raise ArithmeticError("Decoder marginal budget changed")
                                    gain = max(0, cref-result["cut"])
                                    gains.append(gain); best = min(best, result["cut"])
                                    score_units += result["score_units"]
                                    emit(stream, dict(stage="development", case=key, model=model,
                                        setting=setting, shot=shot, seed=seed, Cref=cref, gain=gain,
                                        field=field.tolist(), counts=None if counts is None else counts.tolist(),
                                        transferred=None if counts is None else int(counts[context["outside"]].sum()),
                                        **extra, **result))
                                totals[model][setting] += sum(gains)
                                setting_seconds = time.perf_counter()-setting_start
                                time_budgets[model] += setting_seconds
                                records.append({"case":key, "model":model, "setting":setting,
                                    "proposals":len(gains), "score_units":score_units, "sum_gain":sum(gains),
                                    "best_cut":best, "setup_seconds":setup_seconds,
                                    "field_sampling_and_PIT_seconds":sample_seconds,
                                    "decoder_seconds":decoder_seconds,
                                    "observed_setting_seconds_including_recording":setting_seconds})
                    budget = 8*spec["draws_per_tuple"]*expected_units
                    # PMF/calibration work was charged ONCE to the common frontend
                    # which used those tables to score and share vacuum candidates.
                    for baseline in spec["baseline_models"]:
                        timed = TimedBaselineStream(stream)
                        tag = {"stage":"classical_search", "case":key}
                        seed = base.seed_for(461200, key, baseline)
                        if baseline == "KL_collective":
                            result = adaptive.kl_collective(a, common["reference_subset"], seed, budget, timed, tag)
                        elif baseline == "block_matching":
                            result = block_matching(a, common["source_S0"], common["inside_order"],
                                common["outside_order"], delta, cref, seed, budget, timed, tag)
                        else:
                            result = base.classical_search(a, common["reference_subset"], baseline, seed, budget, timed, tag)
                        if result["candidate_scores"] != budget or len(timed.rows) != budget:
                            raise ArithmeticError("Classical baseline score population changed")
                        # A prefix can only be used at a time budget actually observed here.
                        frontiers = {}
                        for model in MODELS:
                            limit = time_budgets[model]
                            eligible = [value for elapsed, value in timed.rows if elapsed <= limit]
                            frontiers[model] = {"observed_model_seconds":limit,
                                "baseline_scores_within_time_and_score_caps":len(eligible),
                                "best_cut_within_joint_caps":min([cref]+eligible),
                                "score_ceiling":budget}
                        records.append(dict(tag, **result, joint_observed_time_frontiers=frontiers))
                stream.flush()
                zipped.flush()
                raw_file.flush()
                if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > spec["maximum_new_output_bytes"]-2097152:
                    raise RuntimeError("New scientific data approached output cap; retain partial run")
    selected = {model:int(np.argmax(values)) if values.max() > 0 else None
                for model, values in totals.items()}
    attempts = {model:sum(r.get("proposals", 0) for r in records if r["model"] == model) for model in MODELS}
    if set(attempts.values()) != {256}:
        raise ArithmeticError("Frozen sample population changed")
    summary = {"status":"EXPLORATORY_DEV_VETO_ONLY", "positive_accepted":False,
        "actual_QPU_calls":0, "actual_QPU_photons":0, "simulated_eta":1.,
        "heldout_graphs_opened":False, "optimum_used":False,
        "attempts_per_model":attempts, "selected_independently":selected,
        "primary_resource_ledger":{model:{
            "decoded_proposals":attempts[model],
            "simulated_optical_attempts":attempts[model] if model in ("bosonic","distinguishable","species4") else 0,
            "simulated_injected_photons":sum(c["k"]*64 for c in spec["cases"]) if model in ("bosonic","distinguishable","species4") else 0,
            "classical_field_samples":0 if model in ("bosonic","distinguishable","species4") else attempts[model],
            "online_partial_marginal_scores":sum(64*sum(c["m"]-r for r in range((c["k"]+1)//2,c["k"])) for c in spec["cases"]),
            "online_final_cut_scores":attempts[model]}
            for model in MODELS},
        "shared_phase_calibration_draws":len(spec["cases"])*len(spec["network_grid_p_zeta"])*spec["phase_calibration_samples"],
        "setting_total_gains":{m:x.tolist() for m,x in totals.items()},
        "common_frontend":commons, "records":records,
        "cpu_seconds_inside_main":time.process_time()-start_cpu,
        "wall_seconds_inside_main":time.perf_counter()-start_wall,
        "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
        "simulation_time_is_QPU_time":False}
    (args.output/"summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > spec["maximum_new_output_bytes"]:
        raise RuntimeError("Scientific data exceeded output cap; do not accept run")
    print(json.dumps({key:value for key,value in summary.items() if key not in ("records", "common_frontend")}))


if __name__ == "__main__":
    main()
