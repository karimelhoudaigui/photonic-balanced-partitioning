"""P45-B DEV-only stars/bars circuit test. No optimum oracle or remote calls.

All preprocessing candidates are credited to every control. Every ideal Fock
sample is decoded, including collisions. Loss is not simulated in this pilot.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy.linalg import expm

from P43_global_gain_probe import cut, make_graph, seed_for, classical_search

MODELS = ("bosonic", "distinguishable", "phase_multinomial",
          "source_multinomial", "source_polya", "inclusion_walk")
SEARCHES = ("uniform", "two_swap", "swap_descent", "anneal", "spectral_swap",
            "gap_descent", "gap_anneal")


def emit(stream, record):
    stream.write(json.dumps(record, sort_keys=True, allow_nan=False)+"\n")


def decode(occupation, order):
    """Fixed stars/bars bijection; order maps bit positions to graph vertices."""
    n = np.asarray(occupation)
    k = (len(order))//2
    if len(order) != 2*k or len(n) != k+1 or int(n.sum()) != k:
        raise ValueError("Wrong photon/mode/vertex count")
    if np.any(n < 0) or not np.all(n == n.astype(int)):
        raise ValueError("Nonintegral or negative occupation")
    bits = []
    for i, value in enumerate(n):
        bits.extend([1]*int(value))
        if i != k:
            bits.append(0)
    if len(bits) != 2*k or sum(bits) != k:
        raise ArithmeticError("Invalid stars/bars word")
    return sorted(int(order[i]) for i, bit in enumerate(bits) if bit)


def encode(subset, order):
    selected = set(subset)
    k = len(order)//2
    if len(selected) != k or not selected <= set(order):
        raise ValueError("Invalid balanced subset")
    result = [0]
    for vertex in order:
        if vertex in selected:
            result[-1] += 1
        else:
            result.append(0)
    if len(result) != k+1:
        raise ArithmeticError("Invalid inverse stars/bars map")
    return np.asarray(result, dtype=int)


def prepare(a, case_id, spec, stream):
    """Exactly declared scored front end; no iterative reanchoring."""
    started = time.perf_counter()
    nv, k = len(a), len(a)//2
    rng = np.random.default_rng(seed_for("P45B", case_id, "anchor"))
    candidates = []
    for index in range(spec["anchor_uniform_draws"]):
        subset = sorted(rng.choice(nv, k, replace=False).tolist())
        value = cut(a, subset)
        candidates.append((value, tuple(subset), index))
        emit(stream, {"stage":"common_anchor", "case":case_id, "index":index,
                      "subset":subset, "cut":value})
    c0, anchor, anchor_index = min(candidates)
    anchor = list(anchor)
    rng = np.random.default_rng(seed_for("P45B", case_id, "order"))
    left = rng.permutation(anchor).tolist()
    right = rng.permutation([v for v in range(nv) if v not in anchor]).tolist()
    order = [v for pair in zip(left, right) for v in pair]
    source = np.asarray([1]*k+[0], dtype=int)
    if decode(source, order) != sorted(anchor):
        raise ArithmeticError("Source/anchor mismatch")
    delta = np.full((k+1, k+1), np.nan)
    front_candidates = list(candidates)
    for j in range(k):
        for i in range(k+1):
            if i == j:
                continue
            n = source.copy()
            n[i] += 1
            n[j] -= 1
            subset = decode(n, order)
            value = cut(a, subset)
            delta[i, j] = value-c0
            front_candidates.append((value, tuple(subset), len(front_candidates)))
            emit(stream, {"stage":"common_gap_hop", "case":case_id,
                          "to_mode":i, "from_mode":j, "occupation":n.tolist(),
                          "subset":subset, "cut":value, "delta_from_anchor":value-c0})
    front, best_subset, _ = min(front_candidates)
    scale = max(1., float(np.median(abs(delta[np.isfinite(delta)]))))
    # Physical source remains the original anchor, even when the frontend improves it.
    return {"adjacency":a.tolist(), "anchor":anchor, "anchor_cut":c0,
            "anchor_index":anchor_index, "order":order, "source":source.tolist(),
            "delta":np.nan_to_num(delta).tolist(),
            "delta_valid":np.isfinite(delta).tolist(), "delta_scale":scale,
            "front_cut":front, "front_subset":list(best_subset),
            "common_scores":len(front_candidates),
            "preprocessing_seconds":time.perf_counter()-started}


def generator(context, kappa):
    delta = np.asarray(context["delta"])
    scale, m = context["delta_scale"], len(delta)
    k = m-1
    h = np.zeros((m, m), dtype=complex)
    for i in range(m):
        for j in range(i+1, m):
            if j == k:
                symmetric = delta[k, i]/scale
                phase = 0.
            else:
                symmetric = (delta[i, j]+delta[j, i])/(2*scale)
                phase = kappa*math.tanh((delta[j, i]-delta[i, j])/(2*scale))
            amplitude = 2/(1+math.exp(float(np.clip(symmetric, -8., 8.))))
            h[i, j] = amplitude*np.exp(1j*phase)
            h[j, i] = h[i, j].conjugate()
    norm = float(np.linalg.norm(h, 2))
    if not norm > 0:
        raise ArithmeticError("Zero graph generator")
    return h/norm, norm


def make_sampler(u, h, t, k, model, seed, event_cap):
    rng = np.random.default_rng(seed)
    m = len(u)
    columns = u[:, :k]
    p = abs(columns)**2
    mean_p = p.sum(axis=1)/k
    mean_p /= mean_p.sum()
    if model == "bosonic":
        import perceval as pcvl
        from perceval.backends import Clifford2017Backend
        pcvl.random_seed(seed)
        backend = Clifford2017Backend()
        backend.set_circuit(pcvl.Circuit(m).add(0, pcvl.Unitary(pcvl.Matrix(u))))
        backend.set_input_state(pcvl.BasicState([1]*k+[0]))
        return lambda: (np.asarray(list(backend.sample()), dtype=int), {})
    if model == "distinguishable":
        return lambda: (np.bincount([rng.choice(m, p=p[:, j]/p[:, j].sum())
                                    for j in range(k)], minlength=m), {})
    if model == "source_multinomial":
        return lambda: (rng.multinomial(k, mean_p), {})
    if model == "source_polya":
        positive = mean_p > 0
        def polya():
            weights = np.zeros(m)
            weights[positive] = rng.dirichlet(k*mean_p[positive])
            return rng.multinomial(k, weights), {}
        return polya
    if model == "phase_multinomial":
        def phase():
            field = columns @ rng.choice((1., -1., 1j, -1j), size=k)
            weights = abs(field)**2
            weights /= weights.sum()
            return rng.multinomial(k, weights), {}
        return phase
    if model == "inclusion_walk":
        q = abs(h)**2
        def inclusion():
            n = np.asarray([1]*k+[0], dtype=int)
            elapsed, events = 0., 0
            while True:
                rates = (n[:, None]+1)*n[None, :]*q
                np.fill_diagonal(rates, 0)
                total = float(rates.sum())
                if total <= 0:
                    break
                elapsed += rng.exponential(1/total)
                if elapsed > t*t:
                    break
                if events >= event_cap:
                    raise RuntimeError("INCONCLUSIVE: inclusion event cap")
                index = int(rng.choice(m*m, p=rates.ravel()/total))
                i, j = divmod(index, m)
                n[i] += 1
                n[j] -= 1
                events += 1
            return n, {"inclusion_events":events}
        return inclusion
    raise ValueError(model)


def run_batch(context, a, order, theta, model, seed, count, stream, tag, event_cap):
    started = time.perf_counter()
    t, kappa = theta
    h, h_norm = generator(context, kappa)
    u = expm(-1j*t*h)
    residual = float(abs(u.conj().T@u-np.eye(len(u))).max())
    if residual > 2e-12:
        raise ArithmeticError("Nonunitary circuit")
    sample = make_sampler(u, h, t, len(a)//2, model, seed, event_cap)
    setup = time.perf_counter()-started
    started = time.perf_counter()
    costs, gains = [], []
    collisions = 0
    for shot in range(count):
        n, extra = sample()
        subset = decode(n, order)
        value = cut(a, subset)
        gain = max(0, context["front_cut"]-value)
        collisions += int(np.any(n > 1))
        costs.append(value)
        gains.append(gain)
        emit(stream, dict(tag, model=model, seed=seed, shot=shot,
                         occupation=n.tolist(), subset=subset, cut=value,
                         gain_below_common_front=gain, **extra))
    stream.flush()
    return dict(tag, model=model, attempts=count, candidate_scores=count,
                modeled_injected_photons=count*(len(a)//2) if model in
                ("bosonic", "distinguishable") else 0, actual_injected_photons=0,
                cut_sum=sum(costs), mean_cut=float(np.mean(costs)),
                gain_sum=sum(gains), mean_gain=float(np.mean(gains)),
                improving_draws=sum(g > 0 for g in gains),
                best_cut=min([context["front_cut"]]+costs),
                collisional_occupations=collisions, rejected_occupations=0,
                generator_norm_before_scaling=h_norm, unitary_residual=residual,
                setup_seconds=setup, sampling_decode_score_seconds=time.perf_counter()-started)


def gap_search(a, context, model, seed, budget, stream, case_id):
    rng = np.random.default_rng(seed)
    order = context["order"]
    n = encode(context["front_subset"], order)
    current = best = context["front_cut"]
    pending = []
    started = time.perf_counter()
    for step in range(budget):
        if model == "gap_descent":
            if not pending:
                pending = [(i, j) for j in np.flatnonzero(n) for i in range(len(n)) if i != j]
                rng.shuffle(pending)
            i, j = pending.pop()
        else:
            j = int(rng.choice(len(n), p=n/n.sum()))
            i = int(rng.choice([i for i in range(len(n)) if i != j]))
        proposal = n.copy()
        proposal[i] += 1
        proposal[j] -= 1
        subset = decode(proposal, order)
        value = cut(a, subset)
        change = value-current
        temperature = max(.05, float(a.sum()/max(1, np.count_nonzero(a))))
        temperature = temperature*(1-step/max(1, budget))**2+.05
        accept = change <= 0 or (model == "gap_anneal" and
                                 rng.random() < math.exp(-change/temperature))
        if accept:
            n, current, pending = proposal, value, []
        best = min(best, value)
        emit(stream, {"stage":"classical", "case":case_id, "model":model,
                      "seed":seed, "step":step, "occupation":proposal.tolist(),
                      "subset":subset, "cut":value, "accepted":bool(accept), "best_cut":best})
    return {"stage":"classical", "case":case_id, "model":model,
            "candidate_scores":budget, "best_cut":best,
            "search_and_scoring_seconds":time.perf_counter()-started}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    args.output.mkdir(parents=True, exist_ok=False)
    cpu = time.process_time()
    closure = [Path(__file__), args.spec, Path(__file__).with_name("P43_global_gain_probe.py"),
               Path(__file__).with_name("P45_encoding_contract.md"),
               Path(__file__).with_name("P45_POSITIVE_TARGET.md")]
    provenance = {"git_revision":subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
                  "argv":sys.argv, "closure_sha256":{str(p):hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in closure}, "versions":{name:importlib.metadata.version(name) for name in
                  ("numpy", "scipy", "networkx", "perceval-quandela", "exqalibur")},
                  "simulation_only":True, "held_out_graphs_opened":False}
    (args.output/"provenance.json").write_text(json.dumps(provenance, indent=2)+"\n")
    rows, contexts = [], {}
    totals = {model:np.zeros(len(spec["theta_grid"])) for model in MODELS}
    rawmeans = {model:np.zeros(len(spec["theta_grid"])) for model in MODELS}
    with (args.output/"raw.jsonl").open("x") as stream:
        for case in spec["cases"]:
            graph_start = time.perf_counter()
            a = make_graph(case)
            graph_seconds = time.perf_counter()-graph_start
            context = prepare(a, case["id"], spec, stream)
            context["graph_generation_seconds"] = graph_seconds
            contexts[case["id"]] = context
            for model in MODELS:
                for index, theta in enumerate(spec["theta_grid"]):
                    row = run_batch(context, a, context["order"], theta, model,
                        seed_for("P45B", case["id"], "train", model, index),
                        spec["draws_per_theta"], stream,
                        {"stage":"development", "case":case["id"], "theta_index":index},
                        spec["inclusion_event_cap"])
                    totals[model][index] += row["mean_gain"]/max(1, context["front_cut"])
                    rawmeans[model][index] += row["mean_cut"]/max(1, context["front_cut"])
                    rows.append(row)
        selected = {model:min(range(len(spec["theta_grid"])),
                    key=lambda i:(-totals[model][i], rawmeans[model][i], i)) for model in MODELS}
        selection = {"selected_theta_independently":selected,
                     "sum_normalized_mean_gains":{m:totals[m].tolist() for m in MODELS},
                     "sum_normalized_raw_means":{m:rawmeans[m].tolist() for m in MODELS},
                     "development_raw_prefix_sha256":hashlib.sha256((args.output/"raw.jsonl").read_bytes()).hexdigest(),
                     "held_out_graphs_opened":False}
        (args.output/"selection.json").write_text(json.dumps(selection, indent=2)+"\n")
        for case in spec["cases"]:
            case_id = case["id"]
            context = contexts[case_id]
            original = np.asarray(context["adjacency"])
            for probe in range(spec["fresh_batches"]):
                rng = np.random.default_rng(seed_for("P45B", case_id, "relabel", probe))
                permutation = np.arange(len(original)) if probe == 0 else rng.permutation(len(original))
                inverse = np.argsort(permutation)
                a = original[np.ix_(permutation, permutation)]
                order = inverse[context["order"]].tolist()
                emit(stream, {"stage":"relabel_map", "case":case_id, "probe":probe,
                              "permutation_new_to_original":permutation.tolist(), "order":order})
                for model in MODELS:
                    index = selected[model]
                    rows.append(run_batch(context, a, order, spec["theta_grid"][index], model,
                        seed_for("P45B", case_id, "fresh", probe, model), spec["fresh_draws"], stream,
                        {"stage":"fresh_dev", "case":case_id, "probe":probe, "theta_index":index},
                        spec["inclusion_event_cap"]))
            budget = spec["draws_per_theta"]*len(spec["theta_grid"])+spec["fresh_batches"]*spec["fresh_draws"]
            for model in SEARCHES:
                seed = seed_for("P45B", case_id, "classical", model)
                if model.startswith("gap_"):
                    rows.append(gap_search(original, context, model, seed, budget, stream, case_id))
                else:
                    rows.append(dict(case=case_id, **classical_search(original, context["front_subset"],
                        model, seed, budget, stream, {"stage":"classical", "case":case_id})))
            rng = np.random.default_rng(seed_for("P45B", case_id, "uniform_polya"))
            costs = []
            started = time.perf_counter()
            for shot in range(budget):
                n = rng.multinomial(len(original)//2, rng.dirichlet(np.ones(len(original)//2+1)))
                subset = decode(n, context["order"])
                value = cut(original, subset)
                costs.append(value)
                emit(stream, {"stage":"classical", "case":case_id, "model":"uniform_polya",
                              "shot":shot, "occupation":n.tolist(), "subset":subset, "cut":value})
            rows.append({"stage":"classical", "case":case_id, "model":"uniform_polya",
                         "candidate_scores":budget, "best_cut":min([context["front_cut"]]+costs),
                         "search_and_scoring_seconds":time.perf_counter()-started})
    per_case = defaultdict(dict)
    for row in rows:
        case, model = row["case"], row["model"]
        previous = per_case[case].get(model, contexts[case]["front_cut"])
        per_case[case][model] = min(previous, row["best_cut"])
    summary = {"contexts":contexts, "rows":rows, "selected":selected,
               "best_all_stages_including_common_front":dict(per_case),
               "cpu_seconds":time.process_time()-cpu, "simulated_loss_transmission":1.,
               "verdict":"DEV_ONLY; no advantage, novelty or hardware claim", "held_out_graphs_opened":False}
    (args.output/"summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status":"completed", "cpu_seconds":summary["cpu_seconds"],
                      "best_by_case_model":dict(per_case)}, sort_keys=True))


if __name__ == "__main__":
    main()
