"""P45-A development veto: graph completion of count/continuous fields.

No device access, optimum oracle, held-out graphs or accepted positive result.
Run only in the coordinator's single numerical slot via the bounded runner.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.linalg import expm

import P43_global_gain_probe as base


def emit(stream, row):
    stream.write(json.dumps(row)+"\n")


def complete(a, field, k, lam, priority, q=None):
    """Explicitly charge each inspected unbalanced cut marginal and final cut."""
    m = len(a)
    field = np.asarray(field, dtype=float)
    if field.shape != (m,) or not np.all(np.isfinite(field)):
        raise ValueError("Invalid cavity field")
    q = (k+1)//2 if q is None else q
    rank = {vertex: index for index, vertex in enumerate(priority)}
    order = sorted(range(m), key=lambda i: (-float(field[i]), rank[i]))
    selected = set(order[:q])
    seeds = sorted(selected)
    degree = a.sum(axis=1)
    marginal = degree-2*a[:, seeds].sum(axis=1) if seeds else degree.copy()
    positive = a[a > 0]
    weight_scale = float(positive.mean()) if len(positive) else 1.
    steps, inspected = [], 0
    while len(selected) < k:
        remaining = [i for i in range(m) if i not in selected]
        inspected += len(remaining)
        vertex = min(remaining, key=lambda i: (float(marginal[i]-lam*weight_scale*field[i]), rank[i]))
        steps.append({"vertex": vertex, "exact_marginal": float(marginal[vertex]),
                      "field_biased_marginal": float(marginal[vertex]-lam*weight_scale*field[vertex]),
                      "candidate_marginals": len(remaining)})
        selected.add(vertex)
        marginal -= 2*a[:, vertex]
    subset = sorted(selected)
    return {"subset": subset, "cut": base.cut(a, subset), "seed_vertices": seeds,
            "completion": steps, "marginal_evaluations": inspected,
            "feasible_scores": 1, "score_units": inspected+1}


def network(a, source, t_over_pi, kappa, eta):
    x = np.zeros(len(a)); x[source] = 1
    ell = a.sum(axis=1)-2*a@x
    ell -= ell.mean()
    if abs(ell).max():
        ell /= abs(ell).max()
    h = base.unit_norm(base.unit_norm(a)+kappa*np.diag(ell))
    u = expm(-1j*np.pi*t_over_pi*h)
    if not np.allclose(u.conj().T@u, np.eye(len(a)), atol=3e-12, rtol=0):
        raise ArithmeticError("Nonunitary graph network")
    v = u[:, source]
    p = abs(v)**2
    mu = p.sum(axis=1)
    projector = v@v.conj().T
    cov = eta*np.diag(mu)+eta**2*(abs(projector)**2-2*p@p.T)
    cov = (cov+cov.T)/2
    eigenvalues, vectors = np.linalg.eigh(cov)
    if eigenvalues.min() < -1e-10:
        raise ArithmeticError("Bosonic covariance has significant negative eigenvalue")
    factor = vectors*np.sqrt(np.maximum(eigenvalues, 0))[None, :]
    variance = np.maximum(np.diag(cov), 0)
    sigma = np.sqrt(np.maximum(variance, 1e-12))
    return {"u": u, "v": v, "mu": mu, "cov": cov, "factor": factor,
            "variance": variance, "sigma": sigma, "eigenvalue_min": float(eigenvalues.min())}


def field_sampler(context, source, model, seed, eta):
    """Every randomness component has a separate seed, including hybrid counts."""
    component_seeds = [base.seed_for(seed, role) for role in ("field", "loss", "categorical", "counts")]
    if len(set(component_seeds)) != len(component_seeds):
        raise ArithmeticError("A component-seed hash collision prevents independence")
    rng = np.random.default_rng(component_seeds[0])
    loss_rng = np.random.default_rng(component_seeds[1])
    categorical_rng = np.random.default_rng(component_seeds[2])
    u, v, mu = context["u"], context["v"], context["mu"]
    m, nphotons = len(u), len(source)
    count_sampler = None
    if model in ("bosonic", "distinguishable", "species4", "moment_hybrid"):
        primitive = "distinguishable" if model == "moment_hybrid" else model
        count_sampler, _ = base.make_optical_sampler(u, source, primitive, component_seeds[3])

    def draw():
        counts = None
        if count_sampler is not None:
            full, _ = count_sampler()
            if full.shape != (m,) or np.any(full < 0) or int(full.sum()) != nphotons:
                raise ArithmeticError("The ideal full-sector primitive lost or duplicated a photon")
            counts = loss_rng.binomial(full, eta)
            raw = counts-eta*mu
        if model in ("moment_hybrid", "phase_multinomial"):
            phases = rng.choice((1, -1, 1j, -1j), size=nphotons)
            intensity = abs(v@phases)**2
            if model == "moment_hybrid":
                raw = raw+eta*(intensity-mu)
            else:
                probabilities = eta*intensity/nphotons
                loss_probability = 1-float(probabilities.sum())
                if loss_probability < -1e-12:
                    raise ArithmeticError("Mean-field probabilities not normalized")
                all_probabilities = np.append(probabilities, max(0., loss_probability))
                all_probabilities /= all_probabilities.sum()  # Numerical roundoff, never postselection.
                counts = categorical_rng.multinomial(nphotons, all_probabilities)[:-1]
                raw = counts-eta*mu
        elif model == "gaussian_Bcov":
            raw = context["factor"]@rng.normal(size=m)
        elif model == "iid_variance":
            raw = np.sqrt(context["variance"])*rng.normal(size=m)
        elif model not in ("bosonic", "distinguishable", "species4"):
            raise ValueError("Unknown field model")
        return raw/context["sigma"], counts, raw

    return draw


def kl_collective(a, source, seed, budget, stream, tag):
    """Full candidate accounting; uphill locked pair passes and scored restarts."""
    rng = np.random.default_rng(seed)
    m, k = len(a), len(source)
    current = set(source)
    best_set, best = set(source), base.cut(a, source)
    initial = best
    calls = passes = 0
    start = time.perf_counter()
    while calls < budget:
        if passes and passes % 2 == 0:
            current = set(rng.choice(m, k, replace=False).tolist())
            value = base.cut(a, current); calls += 1
            if value < best:
                best, best_set = value, set(current)
            emit(stream, dict(tag, model="KL_collective", kind="restart", seed=seed,
                              score_index=calls-1, subset=sorted(current), cut=value, best_cut=best))
            if calls == budget:
                break
        locked = set()
        for _ in range(k):
            candidates = []
            for i in sorted(current-locked):
                for j in [j for j in range(m) if j not in current and j not in locked]:
                    proposed = (current-{i})|{j}
                    value = base.cut(a, proposed); calls += 1
                    candidates.append((value, i, j, proposed))
                    if value < best:
                        best, best_set = value, set(proposed)
                    emit(stream, dict(tag, model="KL_collective", kind="candidate", seed=seed,
                                      score_index=calls-1, subset=sorted(proposed), cut=value, best_cut=best))
                    if calls == budget:
                        break
                if calls == budget:
                    break
            if not candidates:
                break
            _, i, j, current = min(candidates, key=lambda item: item[:3])
            locked.update((i, j))
            if calls == budget:
                break
        current = set(best_set)
        passes += 1
    return {"model": "KL_collective", "candidate_scores": calls, "initial_cut": initial,
            "best_cut": best, "search_and_scoring_seconds": time.perf_counter()-start,
            "completed_or_partial_passes": passes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    contract = json.loads(args.contract.read_text())
    if contract["positive_acceptance_allowed"] or contract["eta"] != 1.:
        raise ValueError("This frozen veto supports ideal eta1 only and accepts no positive")
    expected_models = ["bosonic", "distinguishable", "phase_multinomial", "moment_hybrid",
                       "gaussian_Bcov", "iid_variance", "species4"]
    if (contract["models"] != expected_models or len(contract["cases"]) != 4
            or contract["trial_seeds"] != [0, 1] or contract["draws_per_tuple"] != 4
            or len(contract["network_grid_t_over_pi_kappa"]) != 4
            or contract["decoder_lambda"] != [0, 1]):
        raise ValueError("Changing the frozen population or budget requires a new implementation")
    args.output.mkdir(parents=True, exist_ok=True)
    cpu_start, wall_start = time.process_time(), time.perf_counter()
    records, common = [], {}
    totals = {model: np.zeros(8) for model in contract["models"]+["bosonic_permuted"]}
    with (args.output/"raw.jsonl").open("x") as stream:
        for case in contract["cases"]:
            case_id, k = case["id"], case["k"]
            if case["m"] != 2*k:
                raise ValueError("Balanced m2k required")
            preprocessing_start = time.perf_counter()
            a = base.make_graph(case)
            source, anchor = base.prepare_anchor(a, base.seed_for(451010, case_id),
                                                 contract["anchor_max_scans"], stream, case_id)
            priority = np.random.default_rng(base.seed_for(451020, case_id)).permutation(len(a)).tolist()
            species_order = np.random.default_rng(base.seed_for(451030, case_id)).permutation(source).tolist()
            contexts = [network(a, source, t, kap, contract["eta"])
                        for t, kap in contract["network_grid_t_over_pi_kappa"]]
            compiled_seconds = time.perf_counter()-preprocessing_start
            known = [(base.cut(a, source), source)]
            frontend_units = anchor["candidate_scores_including_initial"]
            decoder_start = time.perf_counter()
            for label, field, q, lam in [("zero", np.zeros(len(a)), None, 0),
                                         ("pure_greedy", np.zeros(len(a)), 0, 0)]:
                result = complete(a, field, k, lam, priority, q)
                emit(stream, dict(stage="frontend_decoder", case=case_id, label=label, **result))
                known.append((result["cut"], result["subset"]))
                frontend_units += result["score_units"]
            for opt_index, context in enumerate(contexts):
                field = -contract["eta"]*context["mu"]/context["sigma"]
                for lam in contract["decoder_lambda"]:
                    result = complete(a, field, k, lam, priority)
                    emit(stream, dict(stage="frontend_decoder", case=case_id, label="vacuum",
                                      network=opt_index, lam=lam, **result))
                    known.append((result["cut"], result["subset"]))
                    frontend_units += result["score_units"]
            reference_cost, reference_source = min(known, key=lambda item: (item[0], item[1]))
            common[case_id] = {"anchor": anchor, "optical_source_S0": source,
                               "reference_source": reference_source, "Cref": reference_cost,
                               "frontend_total_score_units": frontend_units,
                               "graph_anchor_and_network_seconds": compiled_seconds,
                               "decoder_frontend_seconds": time.perf_counter()-decoder_start}
            saved = dict(common[case_id], adjacency=a.tolist(), vertex_priority=priority,
                         species_order=species_order,
                         networks=[{"mu": ctx["mu"].tolist(), "covariance_B": ctx["cov"].tolist(),
                                    "sigma": ctx["sigma"].tolist(), "u_real": ctx["u"].real.tolist(),
                                    "u_imag": ctx["u"].imag.tolist()} for ctx in contexts])
            with (args.output/f"context_{case_id}.json").open("x") as context_stream:
                json.dump(saved, context_stream, indent=2)
            for replicate in contract["trial_seeds"]:
                case_key = f"{case_id}:{replicate}"
                for model in contract["models"]:
                    for opt_index, context in enumerate(contexts):
                        for lam_index, lam in enumerate(contract["decoder_lambda"]):
                            setting = 2*opt_index+lam_index
                            sample_seed = base.seed_for(451100, case_key, model, setting)
                            setup_start = time.perf_counter()
                            model_source = species_order if model == "species4" else source
                            draw = field_sampler(context, model_source, model, sample_seed, contract["eta"])
                            setup_seconds = time.perf_counter()-setup_start
                            permutation_rng = np.random.default_rng(base.seed_for(451110, case_key, setting))
                            gains, best, units = [], reference_cost, 0
                            permuted_gains, permuted_best = [], reference_cost
                            sample_seconds = decoder_seconds = paired_seconds = 0.
                            loop_start = time.perf_counter()
                            for shot in range(contract["draws_per_tuple"]):
                                step_start = time.perf_counter()
                                field, counts, raw_field = draw()
                                sample_seconds += time.perf_counter()-step_start
                                step_start = time.perf_counter()
                                result = complete(a, field, k, lam, priority)
                                decoder_seconds += time.perf_counter()-step_start
                                gain = max(0, reference_cost-result["cut"])
                                gains.append(gain); units += result["score_units"]
                                best = min(best, result["cut"])
                                tag = {"stage": "development", "case": case_key, "model": model,
                                       "setting": setting, "shot": shot, "seed": sample_seed}
                                emit(stream, dict(tag, counts=None if counts is None else counts.tolist(),
                                                  raw_field=raw_field.tolist(), field=field.tolist(),
                                                  gain=gain, Cref=reference_cost, **result))
                                if model == "bosonic":
                                    step_start = time.perf_counter()
                                    permutation = permutation_rng.permutation(len(a))
                                    shuffled = complete(a, field[permutation], k, lam, priority)
                                    paired_seconds += time.perf_counter()-step_start
                                    shuffled_gain = max(0, reference_cost-shuffled["cut"])
                                    permuted_gains.append(shuffled_gain)
                                    permuted_best = min(permuted_best, shuffled["cut"])
                                    emit(stream, dict(tag, model="bosonic_permuted", paired_primary=True,
                                                      permutation=permutation.tolist(), gain=shuffled_gain,
                                                      Cref=reference_cost, **shuffled))
                            totals[model][setting] += sum(gains)
                            records.append({"case": case_key, "model": model, "setting": setting,
                                            "proposals": len(gains), "sum_gain": sum(gains), "best_cut": best,
                                            "score_units": units, "setup_seconds": setup_seconds,
                                            "field_sampling_seconds": sample_seconds,
                                            "primary_decoder_seconds": decoder_seconds,
                                            "paired_ablation_seconds": paired_seconds,
                                            "sampling_decoding_and_paired_ablation_seconds": time.perf_counter()-loop_start})
                            if model == "bosonic":
                                totals["bosonic_permuted"][setting] += sum(permuted_gains)
                                records.append({"case": case_key, "model": "bosonic_permuted", "setting": setting,
                                                "proposals": len(gains), "sum_gain": sum(permuted_gains),
                                                "best_cut": permuted_best, "score_units": units,
                                                "decoder_seconds": paired_seconds,
                                                "additional_photon_attempts": 0})
                marginal_count = sum(len(a)-r for r in range((k+1)//2, k))
                baseline_budget = 8*contract["draws_per_tuple"]*(marginal_count+1)
                for baseline in contract["baseline_models"]:
                    tag = {"stage": "classical_search", "case": case_key}
                    baseline_seed = base.seed_for(451200, case_key, baseline)
                    if baseline == "KL_collective":
                        row = kl_collective(a, reference_source, baseline_seed, baseline_budget, stream, tag)
                    else:
                        row = base.classical_search(a, reference_source, baseline, baseline_seed,
                                                    baseline_budget, stream, tag)
                    records.append(dict(tag, **row))
    selection_start = time.perf_counter()
    selected = {model: int(np.argmax(values)) if values.max() > 0 else None
                for model, values in totals.items()}
    selection_seconds = time.perf_counter()-selection_start
    attempts = {model: sum(row.get("proposals", 0) for row in records if row["model"] == model)
                for model in contract["models"]}
    assert set(attempts.values()) == {contract["raw_attempts_per_model"]}
    k_by_case = {case["id"]: case["k"] for case in contract["cases"]}
    modeled_photons = {model: sum(row["proposals"]*k_by_case[row["case"].split(":")[0]]
                                for row in records if row["model"] == model)
                       for model in ("bosonic", "distinguishable", "species4")}
    summary = {"status": "EXPLORATORY_DEV_VETO_ONLY", "positive_accepted": False,
               "B_attempts": 256, "paired_B_permutation_extra_attempts": 0,
               "attempts_per_primary_model": 256, "actual_QPU_calls": 0,
               "actual_proposal_counts": attempts, "modeled_injected_photons": modeled_photons,
               "heldout_graphs_opened": False, "optimum_used": False,
               "all_tuning_candidates_count": True, "common_frontend": common,
               "selected_independently": selected,
               "setting_total_gains": {model: values.tolist() for model, values in totals.items()},
               "records": records, "cpu_seconds_inside_main": time.process_time()-cpu_start,
               "global_selection_wall_seconds": selection_seconds,
               "wall_seconds_inside_main": time.perf_counter()-wall_start,
               "simulation_time_is_QPU_time": False,
               "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "contract_sha256": hashlib.sha256(args.contract.read_bytes()).hexdigest()}
    with (args.output/"summary.json").open("x") as summary_stream:
        json.dump(summary, summary_stream, indent=2)
    print(json.dumps({key: value for key, value in summary.items() if key != "records"}))


if __name__ == "__main__":
    main()
