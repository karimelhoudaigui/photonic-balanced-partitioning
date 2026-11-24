"""Development-only finite-angle photonic proposal test; never an optimum oracle.

All candidates, collisions, baseline deltas and setup/simulation times are kept.
Physical attempts, feasible scores and simulation time are distinct resources.
No device/client module is used. Fixed anchors do not adapt within this pilot.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import networkx as nx
import numpy as np
from scipy.linalg import expm

MODELS = ("bosonic", "distinguishable", "phase_field", "species4")
CLASSICAL = ("uniform", "two_swap", "swap_descent", "anneal", "spectral_swap")


def seed_for(*parts):
    return int.from_bytes(hashlib.sha256("/".join(map(str, parts)).encode()).digest()[:4], "little")


def cut(a, subset):
    x = np.zeros(len(a), dtype=bool)
    x[list(subset)] = True
    return int(a[np.ix_(x, ~x)].sum())


def make_graph(case):
    m, seed = case["m"], case["seed"]
    rng = np.random.default_rng(seed_for(seed, "weights"))
    graph = (nx.gnp_random_graph(m, .35, seed=seed)
             if case["family"] == "ER" else nx.random_regular_graph(4, m, seed=seed))
    a = np.zeros((m, m), dtype=np.float64)
    for i, j in sorted(graph.edges()):
        a[i, j] = a[j, i] = int(rng.integers(1, 10))
    return a


def unit_norm(h):
    norm = float(np.linalg.norm(h, 2))
    return h / norm if norm else h


def echo(a, source, theta):
    """Graph-covariant W* exp(-i alpha D) W, with genuine finite mixing angles."""
    m = len(a)
    x = np.zeros(m)
    x[list(source)] = 1
    same = x[:, None] == x[None, :]
    intra = unit_norm(a * same)
    cross = unit_norm(a * ~same)
    gradient = a.sum(axis=1) - 2 * (a @ x)
    gradient -= gradient.mean()  # Remove an irrelevant global phase.
    gradient_norm = float(abs(gradient).max())
    if gradient_norm:
        gradient /= gradient_norm
    alpha, beta, gamma = theta
    w = expm(-1j * gamma * intra) @ expm(-1j * beta * cross)
    u = w.conj().T @ (np.exp(-1j * alpha * gradient)[:, None] * w)
    if not np.allclose(u.conj().T @ u, np.eye(m), atol=2e-12, rtol=0):
        raise ArithmeticError("Nonunitary finite-angle circuit")
    return u


def weighted_subset(weights, k, rng):
    """Exact fixed-size product-weight DP in real arithmetic; float64 here."""
    weights = np.asarray(weights, dtype=float)
    m = len(weights)
    if not 0 <= k <= m or np.any(weights < 0) or not np.all(np.isfinite(weights)):
        raise ValueError("Invalid weighted-subset input")
    total = weights.sum()
    if total <= 0:
        return None
    weights = weights / total
    table = np.zeros((m+1, k+1))
    table[:, 0] = 1
    for i in range(m-1, -1, -1):
        for r in range(1, min(k, m-i)+1):
            table[i, r] = table[i+1, r] + weights[i]*table[i+1, r-1]
    if table[0, k] <= 0:
        return None
    selected = []
    r = k
    for i in range(m):
        if not r:
            break
        denominator = table[i, r]
        probability = weights[i]*table[i+1, r-1]/denominator if denominator else 0.
        if not -1e-12 <= probability <= 1+1e-12:
            raise ArithmeticError("Invalid DP transition probability")
        if rng.random() < min(1., max(0., probability)):
            selected.append(i)
            r -= 1
    if r:
        raise ArithmeticError("Incomplete fixed-cardinality draw")
    return selected


def make_optical_sampler(u, source, model, seed):
    """Only local exqalibur/Perceval objects, never a remote Processor."""
    rng = np.random.default_rng(seed)
    m, k = len(u), len(source)
    if len(set(source)) != k or not all(0 <= i < m for i in source):
        raise ValueError("Distinct valid source inputs are required")
    setup_start = time.perf_counter()
    if model in ("bosonic", "species4"):
        import perceval as pcvl
        from perceval.backends import Clifford2017Backend
        pcvl.random_seed(seed)
        groups = [source] if model == "bosonic" else [source[i:i+4] for i in range(0, k, 4)]
        backends = []
        for group in groups:
            backend = Clifford2017Backend()
            backend.set_circuit(pcvl.Circuit(m).add(0, pcvl.Unitary(pcvl.Matrix(u))))
            occupation = [int(i in group) for i in range(m)]
            backend.set_input_state(pcvl.BasicState(occupation))
            backends.append(backend)

        def sample():
            counts = np.zeros(m, dtype=int)
            for backend in backends:
                counts += np.asarray(list(backend.sample()), dtype=int)
            return counts, False
    elif model == "distinguishable":
        probabilities = abs(u[:, source])**2

        def sample():
            modes = [rng.choice(m, p=probabilities[:, j]) for j in range(k)]
            return np.bincount(modes, minlength=m), False
    elif model == "phase_field":
        columns = u[:, source]

        def sample():
            field = columns @ rng.choice((1, -1, 1j, -1j), size=k)
            subset = weighted_subset(abs(field)**2, k, rng)
            fallback = subset is None
            if fallback:
                subset = rng.choice(m, k, replace=False).tolist()  # Charged uniform fallback.
            counts = np.zeros(m, dtype=int)
            counts[subset] = 1
            return counts, fallback
    else:
        raise ValueError("Unknown physical/control model")
    return sample, time.perf_counter()-setup_start


def optical_batch(a, source, theta, model, seed, count, stream, tag):
    k = len(source)
    initial = cut(a, source)
    start = time.perf_counter()
    u = echo(a, source, theta)
    circuit_seconds = time.perf_counter()-start
    sample, setup_seconds = make_optical_sampler(u, source, model, seed)
    gains, costs = [], []
    cf = fallbacks = 0
    start = time.perf_counter()
    for shot in range(count):
        occupation, fallback = sample()
        if int(sum(occupation)) != k or np.any(occupation < 0):
            raise ArithmeticError("Invalid full-sector ideal sample")
        valid = bool(np.all(occupation <= 1))
        fallbacks += int(fallback)
        if valid:
            subset = np.flatnonzero(occupation).tolist()
            cost = cut(a, subset)
            cf += 1
            swaps = k-len(set(source) & set(subset))
        else:
            cost, swaps = None, None
        gain = max(0, initial-cost) if cost is not None else 0
        gains.append(gain)
        if cost is not None:
            costs.append(cost)
        stream.write(json.dumps(dict(tag, model=model, shot=shot, seed=seed,
            occupation=occupation.tolist(), feasible=valid, cut=cost, gain=gain,
            swapped_photons=swaps, field_fallback=fallback))+'\n')
    return {"model": model, "attempts":count,
        "modeled_injected_photons":0 if model == "phase_field" else count*k,
        "actual_injected_photons":0,
        "feasible_scores":cf, "collisions":count-cf, "field_fallbacks":fallbacks,
        "initial_cut":initial, "best_cut":min([initial]+costs),
        "sum_gain":sum(gains), "mean_gain":float(np.mean(gains)),
        "improving_draws":sum(g>0 for g in gains),
        "circuit_seconds":circuit_seconds, "sampler_setup_seconds":setup_seconds,
        "sampling_and_scoring_seconds":time.perf_counter()-start}


def classical_search(a, source, model, seed, budget, stream, tag):
    """Every evaluated proposed cut/delta consumes one candidate-score unit."""
    rng = np.random.default_rng(seed)
    m, k = len(a), len(source)
    current = set(source)
    initial = current_cost = best = cut(a, current)
    calls = 0
    spectral = None
    start = time.perf_counter()
    if model == "spectral_swap":
        _, vectors = np.linalg.eigh(np.diag(a.sum(axis=1))-a)
        spectral = vectors[:, 1]
        spectral /= max(1e-12, float(np.std(spectral)))
    setup_seconds = time.perf_counter()-start
    start = time.perf_counter()
    pending_swaps = []
    for step in range(budget):
        if model == "uniform" or (model == "anneal" and step == budget//2):
            proposal = set(rng.choice(m, k, replace=False).tolist())
        elif model == "two_swap":
            removed = set(rng.choice(sorted(current),2,replace=False).tolist())
            added = set(rng.choice([i for i in range(m) if i not in current],2,replace=False).tolist())
            proposal = (current-removed)|added
        elif model == "spectral_swap" and step < min(16, budget):
            scale = (0., .1, .3, 1.)[step % 4]
            vector = spectral + scale*rng.normal(size=m)
            proposal = set(np.argsort(vector)[:k].tolist())
        elif model in ("swap_descent", "spectral_swap"):
            if not pending_swaps:
                pending_swaps = [(i,j) for i in sorted(current) for j in range(m) if j not in current]
                rng.shuffle(pending_swaps)
            i,j = pending_swaps.pop()
            proposal = (current-{i})|{j}
        else:
            i = rng.choice(sorted(current))
            j = rng.choice([j for j in range(m) if j not in current])
            proposal = (current-{int(i)})|{int(j)}
        proposed_cost = cut(a, proposal)
        calls += 1
        difference = proposed_cost-current_cost
        accept = difference <= 0
        if model == "anneal":
            temperature = max(.05, float(a.sum()/max(1, np.count_nonzero(a)))) * (1-step/max(1,budget))**2 + .05
            accept = accept or rng.random() < math.exp(-difference/temperature)
        if model == "uniform":
            accept = proposed_cost < current_cost
        if accept:
            current, current_cost = proposal, proposed_cost
            pending_swaps = []
        best = min(best, proposed_cost)
        stream.write(json.dumps(dict(tag, model=model, step=step, seed=seed,
            subset=sorted(proposal), cut=proposed_cost, accepted=bool(accept), best_cut=best))+'\n')
    return {"model":model, "candidate_scores":calls, "initial_cut":initial,
        "best_cut":best, "setup_seconds":setup_seconds,
        "search_and_scoring_seconds":time.perf_counter()-start}


def prepare_anchor(a, seed, scans, stream, case_id):
    """Common charged best-swap front end; never claim a capped scan is certified."""
    rng = np.random.default_rng(seed)
    m, k = len(a), len(a)//2
    source = set(rng.choice(m,k,replace=False).tolist())
    current = cut(a, source)
    initial = current
    score_count = 1
    start = time.perf_counter()
    trace = [{"source":sorted(source),"cut":current}]
    certified = False
    for scan in range(scans):
        candidates = []
        for i in sorted(source):
            for j in range(m):
                if j in source:
                    continue
                proposal = (source-{i})|{j}
                value = cut(a,proposal)
                score_count += 1
                candidates.append((value,i,j,proposal))
                stream.write(json.dumps({"stage":"common_anchor", "case":case_id,
                    "scan":scan,"removed":i,"added":j,"cut":value,"delta":value-current})+'\n')
        value,i,j,proposal = min(candidates,key=lambda c:c[:3])
        if value >= current:
            certified = True
            break
        source,current = proposal,value
        trace.append({"source":sorted(source),"cut":current,"removed":i,"added":j})
    return sorted(source), {"initial_cut":initial,"final_cut":current,
        "candidate_scores_including_initial":score_count,"max_scans":scans,
        "one_swap_local_minimum_certified":certified,
        "stopping_reason":"exhaustive_no_strict_improvement" if certified else "scan_cap",
        "wall_seconds":time.perf_counter()-start,"trace":trace}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    cpu_start = time.process_time()
    theta_grid = [tuple(row) for row in spec["theta_grid"]]
    records, contexts = [], {}
    anchors = {}
    totals = {model:np.zeros(len(theta_grid)) for model in MODELS}
    with (args.output/'raw.jsonl').open('x') as stream:
        for case in spec["cases"]:
            graph_start = time.perf_counter()
            a = make_graph(case)
            graph_seconds = time.perf_counter()-graph_start
            source, anchor_receipt = prepare_anchor(a,seed_for(430010,case["id"]),
                spec["anchor_max_scans"],stream,case["id"])
            anchors[case["id"]] = dict(anchor_receipt,source_order=source,
                graph_generation_seconds=graph_seconds, adjacency=a.tolist())
            species_rng = np.random.default_rng(seed_for(430011,case["id"]))
            species_order = species_rng.permutation(source).tolist()
            for trial_seed in spec["trial_seeds"]:
                key = f'{case["id"]}:{trial_seed}'
                contexts[key] = {"adjacency":a.tolist(), "source_order":source, "case":case,
                    "species_order":species_order,"common_anchor_id":case["id"],
                    "common_graph_generation_seconds":graph_seconds,
                    "common_anchor_scores":anchor_receipt["candidate_scores_including_initial"],
                    "initial_cut":cut(a,source)}
                initial = cut(a, source)
                for model in MODELS:
                    for index, theta in enumerate(theta_grid):
                        tag = {"stage":"development", "case":key, "theta":index}
                        model_source = species_order if model == "species4" else source
                        row = optical_batch(a, model_source, theta, model, seed_for(430100,key,model,index),
                                            spec["draws_per_theta"], stream, tag)
                        totals[model][index] += row["mean_gain"]
                        records.append(dict(tag,**row))
                for model in CLASSICAL:
                    tag = {"stage":"development", "case":key}
                    row = classical_search(a, source, model, seed_for(key, model),
                        spec["draws_per_theta"]*len(theta_grid), stream, tag)
                    records.append(dict(tag,**row))
        # Freeze all choices before generating or scoring any relabeled outcome.
        chosen = {model:int(np.argmax(totals[model])) if np.max(totals[model]) > 0 else None
                  for model in MODELS}
        stream.flush()
        with (args.output/'selection.json').open('x') as f:
            json.dump({"selected_theta_independently":chosen,
                "development_total_means":{m:v.tolist() for m,v in totals.items()},
                "development_raw_prefix_sha256":hashlib.sha256((args.output/'raw.jsonl').read_bytes()).hexdigest(),
                "code_sha256_before_probe":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "spec_sha256_before_probe":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
                "held_out_graphs_opened":False}, f, indent=2);f.write('\n')
        for case_id in spec["relabel_case_ids"]:
            for trial_seed in spec["probe_seeds"]:
                key = f'{case_id}:probe{trial_seed}'
                context = contexts[f'{case_id}:{spec["trial_seeds"][0]}']
                a = np.asarray(context["adjacency"])
                source = context["source_order"]
                rng = np.random.default_rng(seed_for(430150,case_id))
                permutation = rng.permutation(len(a))  # new index -> original index
                inverse = np.argsort(permutation)
                relabeled = a[np.ix_(permutation,permutation)]
                new_source = inverse[source].tolist()
                context["probe_permutation_new_to_old"] = permutation.tolist()
                for model in MODELS:
                    index = chosen[model]
                    if index is None:
                        records.append({"stage":"fresh_relabel","case":key,"model":model,
                            "theta":None,"identity_selected":True,"attempts":0,"feasible_scores":0,
                            "best_cut":cut(a,source),"initial_cut":cut(a,source),"mean_gain":0.,
                            "sum_gain":0,"improving_draws":0})
                        continue
                    # This algebraic covariance check has no graph-score query.
                    old = echo(a,source,theta_grid[index])
                    new = echo(relabeled,new_source,theta_grid[index])
                    error = float(abs(new-old[np.ix_(permutation,permutation)]).max())
                    if error > 1e-11:
                        raise ArithmeticError("Architecture is not relabel-covariant")
                    tag = {"stage":"fresh_relabel", "case":key, "theta":index}
                    model_source = inverse[context["species_order"]].tolist() if model == "species4" else new_source
                    row = optical_batch(relabeled,model_source,theta_grid[index],model,
                        seed_for(430200,key,model),spec["probe_draws"],stream,tag)
                    records.append(dict(tag, covariance_error=error,**row))
                for model in CLASSICAL:
                    tag = {"stage":"fresh_relabel", "case":key}
                    row = classical_search(relabeled,new_source,model,seed_for(key,model,"probe"),
                        spec["probe_draws"],stream,tag)
                    records.append(dict(tag,**row))
    summary = {"result":"EXPLORATORY_DEVELOPMENT_ONLY", "records":records,
        "selected_theta_independently":chosen, "cpu_seconds":time.process_time()-cpu_start,
        "training_uses_optimum":False, "held_out_graphs_opened":False,
        "qpu_calls":0, "simulation_time_is_hardware_time":False,
        "positive_advantage_accepted":False,
        "common_anchor_ledger":anchors,
        "graph_processing_is_charged_separately":True}
    for name, data in [('summary.json',summary),('contexts.json',contexts)]:
        with (args.output/name).open('x') as f:
            json.dump(data,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='records'}))


if __name__ == '__main__':
    main()
