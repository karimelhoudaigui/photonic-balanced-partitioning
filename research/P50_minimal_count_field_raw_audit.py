"""Post-hoc P50 consistency audit. No primary imports, RNG draws or new graphs.

The author received a negative-sign summary before this source freeze. This
is not blinded/preregistered evidence or independent physical replication.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np

MODELS = ("bosonic", "distinguishable", "species4", "continuous_phase", "gaussian_Bcov",
          "independent_final_variance", "independent_B_marginals", "spherical_coherent",
          "static_preparation", "pure_jitter")
OPTICAL = {"bosonic", "distinguishable", "species4"}
CASES = (("n50_ER_5005001", 50, 13, "ER", 5005001), ("n50_RR_5005002", 50, 13, "RR", 5005002),
         ("n100_ER_5010001", 100, 17, "ER", 5010001), ("n100_RR_5010002", 100, 17, "RR", 5010002))
MODES = ("random", "spectral")
EXPECTED_SOURCE = "6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf"
GEOMETRY_TOL = 1e-10
FIELD_TOL = 1e-10
PGF_TOL = 1e-10
TIME_TOL = 1e-8
TIE_WIDTH = 1e-12


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def seed_for(*parts):
    return int.from_bytes(hashlib.sha256("/".join(map(str, parts)).encode()).digest()[:4], "little")


def array(value, dtype=None):
    if isinstance(value, dict) and set(value) == {"real", "imag"}:
        return np.asarray(value["real"]) + 1j*np.asarray(value["imag"])
    return np.asarray(value, dtype=dtype)


def read_json(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf8") as stream:
        return json.load(stream)


class Audit:
    def __init__(self):
        self.checks = Counter(); self.failures = Counter(); self.examples = []
    def check(self, name, condition, detail=None):
        self.checks[name] += 1
        if not bool(condition):
            self.failures[name] += 1
            if len(self.examples) < 64:
                self.examples.append({"check": name, "detail": str(detail)[:400]})
    def near(self, name, actual, expected, tolerance=GEOMETRY_TOL, detail=None):
        left, right = array(actual), array(expected)
        valid = left.shape == right.shape and np.all(np.isfinite(left)) and np.all(np.isfinite(right))
        difference = float(np.max(abs(left-right))) if valid and left.size else (0. if valid else math.inf)
        self.check(name, valid and difference <= tolerance, (detail, difference))


def policies(model):
    if model == "pure_jitter":
        return [{"id": i, "basis": None, "alpha": None, "beta": b, "draws": 16}
                for i, b in enumerate((0., .1))]
    bases = (0, 1) if model in ("spherical_coherent", "static_preparation") else range(4)
    draws = 4 if model in ("spherical_coherent", "static_preparation") else 2
    return [{"id": i, "basis": b, "alpha": a, "beta": j, "draws": draws}
            for i, (b, a, j) in enumerate((b, a, j) for b in bases for a in (0, 1) for j in (0., .1))]


def scalar_cut(a, subset):
    """Independent scalar edge sum, not a primary NumPy cut/helper call."""
    chosen = set(map(int, subset))
    return sum(a[i][j] for i in chosen for j in range(len(a)) if j not in chosen)


def scalar_rank(field, rank):
    maximum = max(map(float, field))
    buckets = [math.floor((float(x)-maximum)/TIE_WIDTH + .5) for x in field]
    chosen = sorted(sorted(range(len(field)), key=lambda i: (-buckets[i], int(rank[i])))[:len(field)//2])
    return chosen, buckets


def rotation(r, phi):
    c = 1/math.sqrt(2)
    pair = np.array([[c, -np.exp(1j*phi)*c], [np.exp(-1j*phi)*c, c]])
    even, odd = np.eye(r, dtype=complex), np.eye(r, dtype=complex)
    for offset, matrix in ((0, even), (1, odd)):
        for start in range(offset, r-1, 2):
            matrix[np.ix_([start, start+1], [start, start+1])] = pair
    return even @ odd


def verify_pmf(audit, context, detail):
    q, pmf, cdf = context["q"], context["independent_pmf"], context["independent_cdf"]
    n, r = q.shape
    audit.check("independent_pmf_shape", pmf.shape == cdf.shape == (n, r+1), detail)
    audit.check("independent_pmf_nonnegative", np.all(pmf >= 0), detail)
    audit.near("independent_pmf_mass", pmf.sum(axis=1), np.ones(n), 3e-12, detail)
    audit.near("independent_cdf", cdf, np.cumsum(pmf, axis=1), 3e-12, detail)
    audit.check("independent_cdf_valid", np.all(np.diff(cdf, axis=1) >= 0) and np.all(cdf[:, -1] == 1), detail)
    # Independent POSITIVE moment identity, no reuse of the author's inversion:
    # [t^h]G(1+t) = E binom(n,h) = h! e_h(q).
    for row, probabilities in zip(q, pmf):
        elementary = [1.] + [0.]*r
        for value in row:
            for h in range(r, 0, -1):
                elementary[h] += float(value)*elementary[h-1]
        expected = [math.factorial(h)*elementary[h] for h in range(r+1)]
        actual = [sum(float(probabilities[t])*math.comb(t, h) for t in range(h, r+1)) for h in range(r+1)]
        audit.near("independent_pgf_binomial_moments", actual, expected, PGF_TOL, detail)


def load_context(audit, path, case):
    identifier, n, r, family, graph_seed = case
    payload = read_json(path); adjacency = payload["supplied_adjacency"]
    raw = np.asarray(adjacency)
    audit.check("adjacency_shape_integer", raw.shape == (n, n) and raw.dtype.kind in "iu", identifier)
    audit.check("adjacency_simple_weights", np.all(raw >= 0) and np.all(raw <= 5)
                and np.array_equal(raw, raw.T) and not np.any(np.diag(raw)), identifier)
    if family == "RR":
        audit.check("RR_degree8", np.all(np.count_nonzero(raw, axis=1) == 8), identifier)
    audit.check("case_identity", payload["case"] == {"id": identifier, "m": n, "k": n//2,
                "r": r, "family": family, "seed": graph_seed}, identifier)
    denominator = max(1, sum(adjacency[i][j] for i in range(n) for j in range(i+1, n)))
    degree = raw.sum(axis=1); laplacian = np.diag(degree)-raw
    maximum = int(degree.max())
    hs = {0: np.eye(n), 1: np.eye(n)-laplacian/maximum if maximum else np.eye(n)}
    norm = float(np.linalg.eigvalsh(laplacian.astype(float))[-1]) if maximum else 0.
    output = {"adjacency": adjacency, "denominator": denominator, "arms": {}}
    first_order = first_marks = expected_eigenvalues = None
    audit.check("ten_context_arms", set(payload["arms"]) == set(MODELS), identifier)
    for model in MODELS:
        arm = payload["arms"][model]; rank = array(arm["priority"], int)
        order = array(arm["fourier_row_order"], int)
        label = (identifier, model)
        audit.check("arm_identity", arm["case"] == identifier and arm["model"] == model
                    and arm["r"] == r and arm["k"] == n//2, label)
        audit.check("arm_no_shared_search", not arm["other_arm_contexts_used"]
                    and not arm["diagnostics_enter_B_allowance"] and "Cref" not in arm, label)
        audit.check("arm_raw_adjacency", arm["a"] == adjacency and arm["weight_denominator"] == denominator, label)
        audit.check("owned_priority", sorted(rank.tolist()) == list(range(n))
                    and np.array_equal(np.argsort(order), rank), label)
        if first_order is None: first_order = order.copy()
        audit.check("same_carried_priority_roles", np.array_equal(order, first_order), label)
        audit.check("context_seeds", arm["priority_seed"] == seed_for(5040002, identifier)
                    and arm["marks_seed"] == seed_for(5040001, identifier), label)
        audit.check("preparation_numerics", arm["diagnostics"]["status"] == "PASS", label)
        prep_parts = [arm["input_compute"], arm["H_compute"]] + list(arm["source_family_compute"].values())
        prep_parts += [context["basis_compute"] for context in arm["contexts"].values()]
        for clock in ("wall", "cpu"):
            expected = sum(part[clock+"_seconds"] for part in prep_parts)
            audit.near("preparation_component_sum", arm["classical_preparation_"+clock+"_seconds"], expected, TIME_TOL, label)
        contexts = {}
        for key, source in arm["contexts"].items():
            basis = int(key); v = array(source["v"]); q = array(source["q"]); mu = array(source["mu"])
            audit.near("source_isometry", v.conj().T @ v, np.eye(r), GEOMETRY_TOL, (label, basis))
            audit.near("source_q", q, abs(v)**2, GEOMETRY_TOL, (label, basis))
            audit.near("source_mu", mu, q.sum(axis=1), GEOMETRY_TOL, (label, basis))
            if "u" in source:
                u = array(source["u"])
                audit.near("unitary_first_columns", u[:, :r], v, GEOMETRY_TOL, (label, basis))
                audit.near("unitary_geometry", u.conj().T @ u, np.eye(n), GEOMETRY_TOL, (label, basis))
            current = {"v": v, "q": q, "mu": mu}
            if "factor" in source:
                factor = array(source["factor"]); projection = v @ v.conj().T
                covariance = np.diag(mu)+abs(projection)**2-2*q@q.T
                audit.near("Gaussian_covariance_formula", source["covariance"], covariance, GEOMETRY_TOL, (label, basis))
                audit.near("Gaussian_actual_factor", factor@factor.T, covariance, 2e-9, (label, basis))
                mask = (np.count_nonzero(q, axis=1) == 0) | ((np.count_nonzero(q, axis=1) == 1) & np.any(q == 1, axis=1))
                audit.check("Gaussian_preH_mask", source["structural_mask"] == mask.tolist()
                            and np.all(factor[mask] == 0), (label, basis))
                current["factor"] = factor; current["final_variances"] = {}
                for alpha in (0, 1):
                    variance = np.sum((hs[alpha] @ factor)**2, axis=1)
                    audit.near("actual_HF_variance", source["final_variances"][str(alpha)], variance, GEOMETRY_TOL, (label, basis, alpha))
                    current["final_variances"][alpha] = variance
            if "independent_pmf" in source:
                for name in ("independent_pmf", "independent_cdf"):
                    current[name] = array(source[name])
                verify_pmf(audit, current, (label, basis))
                audit.check("independent_repairs_retained", len(source["independent_marginal_repairs"]) == n, (label, basis))
            if model == "bosonic":
                audit.check("B_no_other_calibration", not any(name in source for name in (
                    "factor", "covariance", "independent_pmf", "independent_cdf", "tables")), (label, basis))
            contexts[basis] = current
        expected_bases = {policy["basis"] for policy in policies(model)} - {None}
        audit.check("arm_basis_grid", set(contexts) == expected_bases, label)
        if model == "pure_jitter":
            audit.check("jitter_no_sources_or_H", not contexts and not arm["H"] and not arm["source_family_compute"], label)
        else:
            for alpha in (0, 1):
                audit.near("H_rebuilt", arm["H"][str(alpha)], hs[alpha], GEOMETRY_TOL, (label, alpha))
            row_rank = np.argsort(order)
            fourier = np.exp(2j*math.pi*row_rank[:, None]*np.arange(r)[None, :]/n)/math.sqrt(n)
            audit.near("Fourier_coordinates", contexts[0]["v"], fourier, GEOMETRY_TOL, label)
            spectral = arm["spectral"]; marks = array(spectral["marks"])
            if first_marks is None: first_marks = marks.copy()
            audit.check("same_mark_roles", np.array_equal(marks, first_marks)
                        and np.all((marks >= 0) & (marks <= 1)), label)
            marked = laplacian/norm + .001*np.diag(marks) if norm else .001*np.diag(marks)
            audit.near("spectral_marked_graph", spectral["marked_matrix"], marked, GEOMETRY_TOL, label)
            audit.near("spectral_norm", spectral["laplacian_norm"], norm, GEOMETRY_TOL, label)
            values = array(spectral["eigenvalues"]); e = contexts[1]["v"]
            if expected_eigenvalues is None: expected_eigenvalues = np.linalg.eigvalsh(marked)
            audit.near("ordered_marked_eigenvalues", values, expected_eigenvalues, GEOMETRY_TOL, label)
            audit.near("occupied_eigenvectors", marked @ e, e*values[:r][None, :], GEOMETRY_TOL, label)
            audit.check("occupied_gap_guard", np.all(np.diff(values)[:r] > 1e-12), label)
            for column in range(r):
                magnitude = abs(e[:, column]); candidates = np.flatnonzero(magnitude >= magnitude.max()-1e-12)
                pivot = min(candidates, key=lambda i: rank[int(i)])
                audit.check("occupied_gauge", pivot == spectral["gauge_pivots"][column]
                            and abs(e[pivot, column].imag) < GEOMETRY_TOL and e[pivot, column].real >= 0, (label, column))
            for basis, phi in ((2, 0.), (3, math.pi/2)):
                if basis in contexts:
                    audit.near("source_right_rotation", contexts[basis]["v"], e@rotation(r, phi), GEOMETRY_TOL, (label, basis))
        output["arms"][model] = {"r": r, "rank": rank, "contexts": contexts, "H": hs,
            "prep_wall": arm["classical_preparation_wall_seconds"],
            "prep_cpu": arm["classical_preparation_cpu_seconds"]}
    return output


def audit_raw(audit, path, contexts):
    batches = {}; event_count = 0; diagnostic_count = 0
    with gzip.open(path, "rt", encoding="utf8") as stream:
        for line in stream:
            row = json.loads(line); stage = row["stage"]
            if stage == "preparation_diagnostic":
                diagnostic_count += 1
                audit.check("raw_preparation_PASS", row["diagnostics"]["status"] == "PASS")
                continue
            audit.check("raw_stage", stage in ("training", "evaluation"), stage)
            if stage not in ("training", "evaluation"):
                continue
            case, model, policy_id, trial = row["case"], row["model"], row["policy"], row["trial"]
            context = contexts[case]; arm = context["arms"][model]; n = len(context["adjacency"])
            policy = policies(model)[policy_id]; basis, alpha, beta = policy["basis"], policy["alpha"], policy["beta"]
            source = None if basis is None else arm["contexts"][basis]
            label = (stage, case, model, policy_id, trial, row["shot"])
            key = (stage, case, model, policy_id, trial)
            batch = batches.setdefault(key, {"cuts": [], "subsets": [], "collisions": 0,
                "generation_wall": 0., "post_wall": 0.})
            audit.check("raw_policy_labels", (row["basis"], row["alpha"], row["beta"]) == (basis, alpha, beta), label)
            audit.check("raw_shot_order", row["shot"] == len(batch["cuts"]), label)
            namespace = 5020001 if stage == "training" else 5030001
            seed = seed_for(namespace, case, model, policy_id, trial)
            audit.check("fresh_role_seed", row["seed"] == seed and row["component_seeds"] == {
                "jitter": seed_for(seed, "jitter"), "observation": seed_for(seed, "observation")}, label)
            audit.check("stage_trial", trial == 0 if stage == "training" else trial in (0, 1), label)
            counts = None
            if "counts" in row:
                audit.check("raw_count_integer", len(row["counts"]) == n and all(type(x) is int and x >= 0 for x in row["counts"]), label)
                counts = array(row["counts"], np.int64)
                if model == "independent_B_marginals":
                    audit.check("product_counts_unconditioned", np.all(counts <= arm["r"])
                                and row["independent_total_count_not_conditioned"] is True, label)
                    uniforms = array(row["independent_marginal_uniforms"])
                    audit.check("product_uniforms", uniforms.shape == (n,) and np.all((uniforms >= 0) & (uniforms < 1)), label)
                    predicted = np.sum(uniforms[:, None] >= source["independent_cdf"], axis=1)
                    audit.check("product_marginal_decode", np.array_equal(counts, predicted), label)
                else:
                    audit.check("physical_count_conservation", int(counts.sum()) == arm["r"], label)
            audit.check("counts_present_for_count_arm", (counts is not None) == (model in OPTICAL or model in (
                "continuous_phase", "spherical_coherent", "independent_B_marginals")), label)
            collision = bool(counts is not None and np.any(counts > 1))
            audit.check("raw_collision", row["collision"] == collision, label)
            jitter = array(row["jitter"])
            audit.check("jitter_range", jitter.shape == (n,) and np.all(np.isfinite(jitter))
                        and np.all((jitter >= -1) & (jitter <= 1)), label)
            if model == "pure_jitter": before = np.zeros(n)
            elif model == "gaussian_Bcov": before = arm["H"][alpha] @ (source["factor"] @ array(row["gaussian_standard_noise"]))
            elif model == "independent_final_variance": before = np.sqrt(source["final_variances"][alpha])*array(row["gaussian_standard_noise"])
            elif model == "static_preparation": before = -(arm["H"][alpha] @ source["mu"])
            else: before = arm["H"][alpha] @ (counts-source["mu"])
            if model in ("continuous_phase", "spherical_coherent"):
                coefficient = array(row["coherent_coefficients"])
                audit.near("coherent_coefficient_norm", np.vdot(coefficient, coefficient).real, 1., GEOMETRY_TOL, label)
                if model == "continuous_phase":
                    audit.near("continuous_phase_magnitude", abs(coefficient), np.full(arm["r"], 1/math.sqrt(arm["r"])), GEOMETRY_TOL, label)
                mass = float(np.sum(abs(source["v"]@coefficient)**2))
                audit.near("coherent_mass_receipt", row["coherent_probability_mass_correction"], 1.-mass, GEOMETRY_TOL, label)
            audit.near("field_before_jitter", row["field_before_jitter"], before, FIELD_TOL, label)
            audit.near("field_reconstruction", row["field"], before+beta*jitter, FIELD_TOL, label)
            chosen, bucket = scalar_rank(row["field"], arm["rank"])
            audit.check("scalar_bucket_decoder", row["buckets"] == bucket and row["subset"] == chosen, label)
            audit.check("balanced_subset", len(chosen) == n//2 and len(set(chosen)) == n//2, label)
            cost = scalar_cut(context["adjacency"], chosen)
            audit.check("scalar_cut", row["cut"] == cost and row["weight_denominator"] == context["denominator"], label)
            audit.check("raw_times_nonnegative", row["observation_generation_wall_seconds"] >= 0
                        and row["classical_postprocessing_wall_seconds"] >= 0, label)
            batch["cuts"].append(cost); batch["subsets"].append(tuple(chosen)); batch["collisions"] += int(collision)
            batch["generation_wall"] += row["observation_generation_wall_seconds"]
            batch["post_wall"] += row["classical_postprocessing_wall_seconds"]
            event_count += 1
    audit.check("primary_event_count", event_count == 2560, event_count)
    audit.check("preparation_event_count", diagnostic_count == 40, diagnostic_count)
    return batches, event_count


def audit_summary(audit, summary, contexts, batches):
    audit.check("summary_frozen_positive_ban", summary["positive_accepted"] is False
                and summary["full_frozen_population_completed"] is True and not summary["failures"]
                and summary["actual_QPU_calls"] == 0 and summary["heldout_opened"] is False
                and not summary["optimum_used"] and not summary["reference_partition_used"]
                and not summary["source_loaded_from_training_partition"], None)
    primary = {}; selections = {}
    for row in summary["primary_batches"]:
        key = (row["stage"], row["case"], row["model"], row["policy"], row["trial"])
        audit.check("batch_unique", key not in primary, key); primary[key] = row
        observed = batches[key]; cuts = observed["cuts"]
        audit.check("batch_raw_cuts", row["cuts"] == cuts and row["sum_cuts"] == sum(cuts)
                    and row["proposals"] == len(cuts), key)
        denominator = contexts[row["case"]]["denominator"]
        expected_seed = seed_for(5020001 if row["stage"] == "training" else 5030001,
                                 row["case"], row["model"], row["policy"], row["trial"])
        audit.check("batch_role_seed", row["seed"] == expected_seed and row["component_seeds"] == {
            "jitter":seed_for(expected_seed,"jitter"), "observation":seed_for(expected_seed,"observation")}, key)
        audit.check("batch_fraction", Fraction(row["exact_mean_normalized_cut"]) == Fraction(sum(cuts), len(cuts)*denominator), key)
        minimum = min(cuts); argmins = {s for c, s in zip(cuts, observed["subsets"]) if c == minimum}
        audit.check("batch_paid_best", row["best_cut"] == minimum and tuple(row["best_subset"]) in argmins
                    and row["collision_samples"] == observed["collisions"], key)
        for clock in ("wall", "cpu"):
            audit.near("setup_time_partition", row["observation_setup_"+clock+"_seconds"],
                row["backend_setup_"+clock+"_seconds"]+row["classical_setup_"+clock+"_seconds"], TIME_TOL, key)
            expected = 0. if row["model"] in OPTICAL else row["observation_generation_"+clock+"_seconds"]
            audit.near("classical_generation_partition", row["classical_generation_"+clock+"_seconds"], expected, TIME_TOL, key)
        audit.near("raw_batch_generation_wall", row["observation_generation_wall_seconds"], observed["generation_wall"], TIME_TOL, key)
        audit.near("raw_batch_post_wall", row["classical_postprocessing_wall_seconds"], observed["post_wall"], TIME_TOL, key)
    audit.check("all_batches_raw_match", set(primary) == set(batches), None)
    for model in MODELS:
        losses = {}
        for policy in policies(model):
            values = []
            for case, *_ in CASES:
                key = ("training", case, model, policy["id"], 0); batch = batches[key]
                audit.check("frozen_training_allocation", len(batch["cuts"]) == policy["draws"], key)
                values.append(Fraction(sum(batch["cuts"]), policy["draws"]*contexts[case]["denominator"]))
            loss = sum(values, Fraction(0))/4; losses[policy["id"]] = loss
            audit.check("exact_policy_loss", Fraction(summary["training_losses"][model][str(policy["id"])]["exact_fraction"]) == loss, (model, policy["id"]))
        selected = min(losses, key=lambda p: (losses[p], p)); selections[model] = selected
        audit.check("independent_global_selection", summary["selected_policies"][model] == selected, model)
        eval_means = []
        for case, *_ in CASES:
            totals = []
            for trial in (0, 1):
                key = ("evaluation", case, model, selected, trial)
                audit.check("fresh_evaluation_allocation", len(batches[key]["cuts"]) == 16, key)
                totals += batches[key]["cuts"]
            eval_means.append(Fraction(sum(totals), 32*contexts[case]["denominator"]))
            for label, stages in (("training", {"training"}), ("fresh_evaluation", {"evaluation"}), ("paid_total", {"training", "evaluation"})):
                all_pairs = [(c, s) for key, batch in batches.items() if key[1] == case and key[2] == model and key[0] in stages
                             for c, s in zip(batch["cuts"], batch["subsets"])]
                minimum = min(c for c, _ in all_pairs); argmins = {s for c, s in all_pairs if c == minimum}
                declared = summary["private_paid_incumbents"][model][case][label]
                audit.check("private_paid_incumbent", declared["cut"] == minimum and tuple(declared["subset"]) in argmins, (case, model, label))
        audit.check("fresh_evaluation_Fraction", Fraction(summary["fresh_evaluation_normalized_means"][model]["exact_fraction"]) == sum(eval_means, Fraction(0))/4, model)
        for stage in ("training", "evaluation"):
            count = sum(len(batch["cuts"]) for key, batch in batches.items() if key[0] == stage and key[2] == model)
            audit.check("paid_128_each_stage", count == 128 and summary["proposal_counts"][model][stage] == count, (model, stage))
        spending = summary["spending"][model]
        audit.check("spending_proposals_photons", spending["proposals"] == summary["proposal_counts"][model]
                    and spending["actual_QPU_photons"] == 0
                    and spending["simulated_injected_photons"] == (3840 if model in OPTICAL else 0), model)
        model_rows = [row for row in primary.values() if row["model"] == model]
        for name, value in spending["batch_components"].items():
            audit.near("spending_batch_components", value, sum(row[name] for row in model_rows), TIME_TOL, (model, name))
        for case, *_ in CASES:
            for clock in ("wall", "cpu"):
                audit.near("spending_owned_preparation", spending["preparation_by_graph"][case]["classical_preparation_"+clock+"_seconds"],
                    contexts[case]["arms"][model]["prep_"+clock], TIME_TOL, (case, model))
    # No stray evaluation policy can be hidden by otherwise valid chosen batches.
    audit.check("all_evaluation_policies_frozen", all(key[0] != "evaluation" or key[3] == selections[key[2]] for key in batches), None)
    return primary


def unpack_subset(packed, n):
    return [i for i in range(n) if int(packed[i//8]) & (1 << (i % 8))]


def audit_fast(audit, data, summary, contexts, primary):
    compact = {(row["case"], row["initialization"]): row for row in summary["FAST_comparisons"]}
    audit.check("eight_separate_FAST_rows", len(compact) == len(summary["FAST_comparisons"]) == 8, None)
    all_safe = True
    for identifier, n, _, _, _ in CASES:
        context = contexts[identifier]
        b_rows = [row for key, row in primary.items() if key[1] == identifier and key[2] == "bosonic"]
        selection_share = summary["spending"]["bosonic"]["selection"]["wall_seconds"]/4
        allowance = context["arms"]["bosonic"]["prep_wall"] + selection_share
        allowance += sum(row["classical_setup_wall_seconds"]+row["classical_postprocessing_wall_seconds"]
                         +row["classical_aggregation_wall_seconds"] for row in b_rows)
        for mode in MODES:
            row = read_json(data/f"fast_{mode}_{identifier}.json.gz"); result = row["result"]
            label = (identifier, mode); trace = result["trace"]
            audit.check("FAST_raw_ownership", row["initial_reference_or_priority_given"] is False
                        and result["free_incumbent_used"] is False and result["external_features_used"] is False, label)
            audit.check("FAST_role", row["initialization"] == result["initialization"] == mode
                        and row["seed"] == result["seed"] == seed_for(5050001, identifier, mode), label)
            audit.near("FAST_B_only_allowance", row["total_CPU_allowance_including_adapter"], allowance, TIME_TOL, label)
            remaining = max(0., allowance-row["adapter_compute"]["cpu_seconds"])
            audit.near("FAST_remaining_budget", result["cpu_budget_seconds"], remaining, TIME_TOL, label)
            audit.check("FAST_no_extra_grant", all(row[name] == 0 for name in (
                "other_model_preparation_or_diagnostic_seconds_granted", "optical_backend_or_count_seconds_granted", "serialization_seconds_granted")), label)
            cpu, wall, cuts = trace["cpu_seconds"], trace["wall_seconds"], trace["best_cut"]
            length = len(cpu)
            audit.check("FAST_trace_lengths", all(len(trace[name]) == length for name in (
                "wall_seconds", "best_cut", "best_subset_packbits_little", "proposal_count", "stage")), label)
            audit.check("FAST_monotone_times_best", all(x >= 0 for x in cpu+wall)
                        and all(x <= y for x, y in zip(cpu, cpu[1:])) and all(x <= y for x, y in zip(wall, wall[1:]))
                        and all(x >= y for x, y in zip(cuts, cuts[1:])), label)
            subsets = []
            for i, packed in enumerate(trace["best_subset_packbits_little"]):
                chosen = unpack_subset(packed, n); subsets.append(chosen)
                audit.check("every_FAST_mask_cut", len(chosen) == n//2 and scalar_cut(context["adjacency"], chosen) == cuts[i], (label, i))
            timely = [i for i, value in enumerate(cpu) if value <= result["cpu_budget_seconds"]]
            eligible = timely[-1] if timely else None
            audit.check("FAST_online_snapshot_semantics", result["best_snapshot_cached_online"] is True
                        and result["comparison_is_anytime_prefix"] is True and result["eligible_checkpoint_index"] == eligible, label)
            expected_cut = cuts[eligible] if eligible is not None else None
            expected_subset = subsets[eligible] if eligible is not None else None
            audit.check("FAST_nullable_eligible_best", result["has_eligible_result"] == (eligible is not None)
                        and result["best_cut"] == row["eligible_best_cut"] == expected_cut
                        and result["best_subset"] == row["eligible_best_subset"] == expected_subset, label)
            audit.check("FAST_initial_not_free", not length or (trace["stage"][0] == "initialization"
                        and result["initial_cut"] == cuts[0] and result["initial_subset"] == subsets[0]), label)
            audit.check("FAST_late_retained_only", result["overall_completed_best_cut"] == (cuts[-1] if length else None)
                        and result["overall_completed_best_subset"] == (subsets[-1] if length else None), label)
            if "anneal" in trace["stage"]:
                audit.check("FAST_descent_first", "initial_scan" in trace["stage"]
                            and trace["stage"].index("initial_scan") < trace["stage"].index("anneal")
                            and result["initial_descent_completed_before_deadline"], label)
            counters = result["counters"]
            audit.check("FAST_guard_accounting", result["proposal_count"] == counters["initial_cut_scores"]
                        +counters["delta_evaluations"]+counters["full_restart_cut_scores"]
                        and result["proposal_count"] <= 100000000, label)
            for clock in ("cpu", "wall"):
                audit.near("FAST_compute_export_partition", result["compute_"+clock+"_seconds"],
                    result["online_search_"+clock+"_seconds"]+result["finalization_"+clock+"_seconds"], TIME_TOL, label)
            safe = bool(eligible is not None and result["comparison_acceptance_eligible"]
                        and not result["early_cap_inconclusive"] and not result["early_wall_inconclusive"])
            audit.check("FAST_acceptance_flags", row["comparison_acceptance_eligible"] == safe, label)
            all_safe &= safe
            reduced = dict(row); reduced["result"] = {key:value for key,value in result.items() if key != "trace"}
            audit.check("FAST_summary_matches_file", compact[label] == reduced, label)
    audit.check("summary_FAST_eligibility", summary["FAST_all_eligible"] == all_safe, None)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); audit = Audit(); start = time.process_time()
    files = [args.data/"summary.json", args.data/"raw.jsonl.gz", args.data.parent/"manifest.json"]
    files += [args.data/f"context_{case[0]}.json.gz" for case in CASES]
    files += [args.data/f"fast_{mode}_{case[0]}.json.gz" for case in CASES for mode in MODES]
    hashes = {}; events = 0; fatal = None
    try:
        missing = [str(path) for path in files if not path.is_file()]
        if missing:
            raise FileNotFoundError("Incomplete immutable inputs: "+repr(missing))
        hashes = {str(path):sha(path) for path in files}
        summary = read_json(args.data/"summary.json"); manifest = read_json(args.data.parent/"manifest.json")
        audit.check("main_manifest_completed", manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
                    and manifest["repository"]["dirty"] is False, None)
        audit.check("source_hash", summary["code_sha256"] == EXPECTED_SOURCE, None)
        audit.check("raw_hash", summary["raw_sha256"] == hashes[str(args.data/"raw.jsonl.gz")], None)
        outputs = {Path(row["path"]).name:row["sha256"] for row in manifest["outputs"] if row["kind"] == "result"}
        for path in files:
            if path.name != "manifest.json":
                audit.check("main_manifest_result_hash", outputs.get(path.name) == hashes[str(path)], path.name)
        audit.check("main_inputs_unchanged", all(row["sha256"] == row["sha256_after"] for row in manifest["input_artifacts"]), None)
        contexts = {case[0]:load_context(audit, args.data/f"context_{case[0]}.json.gz", case) for case in CASES}
        batches, events = audit_raw(audit, args.data/"raw.jsonl.gz", contexts)
        primary = audit_summary(audit, summary, contexts, batches)
        audit_fast(audit, args.data, summary, contexts, primary)
    except Exception as error:
        fatal = f"{type(error).__name__}: {error}"
        audit.check("fatal_or_missing_check", False, fatal)
    report = {"status":"PASS_CONSISTENCY" if not audit.failures else "FAIL_OR_INCOMPLETE",
              "audit_scope":"POSTHOC consistency after receipt of negative-sign summary; not blinded/preregistered or independent physical replication",
              "new_samples_graphs_or_budgets":False, "primary_imports_used":False,
              "primary_events":events, "checks":dict(audit.checks), "failures":dict(audit.failures),
              "first_failure_examples":audit.examples, "fatal":fatal, "input_sha256":hashes,
              "tolerances":{"geometry_absolute":GEOMETRY_TOL,"field_absolute":FIELD_TOL,
                            "PGF_binomial_moment_absolute":PGF_TOL,"time_sum_absolute":TIME_TOL},
              "limitations":["Recorded RNG seeds/roles and data relations are checked; random trajectories are NOT redrawn.",
                  "Graph generation realization and timing authenticity are not independently replayed or profiled.",
                  "Source/PMF checks are floating identity checks, not interval, exact-tail or general sampler certification.",
                  "FAST trace masks/cuts/prefix eligibility are checked, not every unrecorded proposal/delta or external timing call.",
                  "No hypothesis test, held-out gate, novelty claim, hardware cost or advantage follows."],
              "cpu_seconds_inside_audit":time.process_time()-start}
    encoded = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if len(encoded.encode()) > 4194304:
        raise RuntimeError("Audit report exceeds frozen4MiB bound")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf8") as stream:
        stream.write(encoded)
    print(json.dumps({"status":report["status"],"primary_events":events,
                      "checks":sum(audit.checks.values()),"failures":dict(audit.failures),"fatal":fatal}))
    return 0 if not audit.failures else 1


if __name__ == "__main__":
    sys.exit(main())
