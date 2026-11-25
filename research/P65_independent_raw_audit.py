"""P65 independent recorded replay. CODE ONLY until frozen/bound/authorized.

No production P43/P50/P65 import, topology regeneration, permanent or sampler.
PCG64 recipes, small spectral Cayley matrices and archived state transitions
are replayed only by a separately authorized audit after immutable binding.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

for _key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_key] = "1"
import numpy as np

SOURCE_COMMIT = "da4d41800819f35dd8ea299395435ca0bdb8157b"
SOURCE_SHA = "a115929779ea50ecd6987f8c63646e95bebc6cc739df3760e6ccbffba0961a4b"
SPEC_SHA = "6993da4efe018c80b7fd9021451fad301dd665b1c86c4eac8adab2b1904eeee4"
CASES = (("n20_ER_6502001", "ER", 6502001), ("n20_RR_6502002", "RR", 6502002))
MODES, OPTICAL, OPTIONAL = ("random", "spectral"), ("bosonic", "distinguishable", "species4"), ("distinguishable", "species4", "r2", "r3")
CANDIDATES = tuple((t, lam) for t in (Fraction(1, 4), Fraction(1, 2), Fraction(1), Fraction(2)) for lam in (Fraction(0), Fraction(1, 4)))
TOL, TIME_TOL = 3e-12, 1e-8
MAX_INPUT, MAX_RAW, MAX_REPORT = 33554432, 8388608, 4194304
CLOSURE = {"AGENTS.md", "research/P65_cayley_markov_stage.py", "research/P65_cayley_markov_dev_spec.json",
           "research/P65_CAYLEY_MARKOV_DEV_CARD.md", "research/P65_PRE_DATA_AMENDMENT.md",
           "research/P65_CARD_INDEPENDENT_PHYSICS_REVIEW.md", "research/P65_cayley_markov_stage_contract.md",
           "research/P65_cayley_markov_stage_preflight_contract.json", "research/P65_cayley_markov_stage_execution_contract.json",
           "theory/P65_collision_counted_photonic_markov_kernel.md", "research/P43_global_gain_probe.py",
           "research/P50_fast_from_scratch.py", "research/P50_FAST_FROM_RAW_API_CARD.md",
           "research/P50_fast_from_scratch_contract.json", "pyproject.toml", "requirements-research-lock.txt",
           "tests/test_p65_cayley_markov_stage.py"}
KNOWN = {"research/P65_cayley_markov_stage.py": SOURCE_SHA, "research/P65_cayley_markov_dev_spec.json": SPEC_SHA,
         "research/P43_global_gain_probe.py": "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777",
         "research/P50_fast_from_scratch.py": "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86"}


class InvalidEvidence(RuntimeError):
    pass


class Audit:
    def __init__(self):
        self.checks, self.failures, self.examples = Counter(), Counter(), []

    def check(self, name, ok, detail=""):
        self.checks[name] += 1
        if not bool(ok):
            self.failures[name] += 1
            if len(self.examples) < 32:
                self.examples.append({"check": name, "detail": str(detail)[:240]})
        return bool(ok)

    def need(self, name, ok, detail=""):
        if not self.check(name, ok, detail):
            raise InvalidEvidence(name+": "+str(detail)[:240])

    def close(self, name, value, expected, tol=TIME_TOL):
        return self.check(name, finite(value) and finite(expected) and abs(float(value)-float(expected)) <= tol, (value, expected))


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise InvalidEvidence("Duplicate JSON key: "+key)
        result[key] = value
    return result


def parse(text):
    return json.loads(text, object_pairs_hook=pairs_unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(InvalidEvidence("Nonfinite JSON: "+x)))


def seed(*parts):
    return int.from_bytes(hashlib.sha256("/".join(map(str, parts)).encode()).digest()[:4], "little")


def fraction(value):
    if type(value) not in (int, str):
        raise InvalidEvidence("Exact Fraction string/integer required")
    return Fraction(value)


def subset(value, n=20, k=10):
    if not isinstance(value, list) or len(value) != k or any(type(i) is not int for i in value) or value != sorted(set(value)) or any(not 0 <= i < n for i in value):
        raise InvalidEvidence("Invalid sorted feasible current source")
    return value


def cut(adjacency, selected):
    inside = set(selected)
    return sum(adjacency[i][j] for i in range(len(adjacency)) for j in range(i+1, len(adjacency)) if (i in inside) != (j in inside))


def unpack(mask, n=20):
    if not isinstance(mask, list) or len(mask) != (n+7)//8 or any(type(b) is not int or not 0 <= b < 256 for b in mask) or (n % 8 and mask[-1] >> (n % 8)):
        raise InvalidEvidence("Invalid packed mask/padding")
    return [i for i in range(n) if (mask[i//8] >> (i % 8)) & 1]


def clock(audit, value, name):
    audit.need("meter_type", isinstance(value, dict), name)
    audit.need("meter_finite", all(finite(value.get(key)) and value[key] >= 0 for key in ("wall_seconds", "cpu_seconds")), name)
    return value


def component(audit, state, label, meter, cpu_unknown=False):
    if cpu_unknown:
        audit.need("prefix_WALL_finite", finite(meter) and meter >= 0)
        wall, cpu = meter, None
    else:
        value = clock(audit, meter, label)
        wall, cpu = value["wall_seconds"], value["cpu_seconds"]
    state["ledger"].append({"label": list(label), "wall_seconds": wall, "cpu_seconds": cpu})


def roles(cid, arm, stage, parameter, chain, step):
    tail = (cid, arm, stage, parameter, chain, step)
    return {"coin": seed(65300000, *tail), "count" if arm in OPTICAL else "replacement": seed(65200000 if arm in OPTICAL else 65400000, *tail)}


def namespace_table():
    table = {}
    for cid, _, graph_seed in CASES:
        table[cid, "graph"] = graph_seed
        table[cid, "weights"] = seed(graph_seed, "weights")
        table[cid, "start", "training", 0] = seed(65100000, cid, "training", 0)
        for chain in range(5):
            table[cid, "start", "fresh", chain] = seed(65100000, cid, "fresh", chain)
        for arm in OPTICAL+("r2", "r3"):
            plan = ([("training", p, 0, j) for p in range(8) for j in range(2)] + [("fresh", "selected", c, j) for c in range(3) for j in range(8)]
                    if arm in OPTICAL else [("fresh", "fixed", c, j) for c in range(5) for j in range(8)])
            for stage, parameter, chain, step in plan:
                for role, value in roles(cid, arm, stage, parameter, chain, step).items():
                    table[cid, arm, stage, parameter, chain, step, role] = value
        for mode in MODES:
            table[cid, "FAST", mode] = seed(65500000, cid, mode)
    return table


def reference_cayley(adjacency, t, lam):
    """Independent spectral functional calculus, never production linear solve."""
    n = len(adjacency)
    degrees = [sum(row) for row in adjacency]
    scale = max(Fraction(1), max(degrees)+lam*(n-1))
    h = np.asarray([[float((Fraction(adjacency[i][j])+lam*int(i != j))/scale) for j in range(n)] for i in range(n)])
    eigenvalues, vectors = np.linalg.eigh(h)
    phases = (1+1j*float(t)*eigenvalues)/(1-1j*float(t)*eigenvalues)
    return (vectors*phases)@vectors.T, h, scale, degrees


def verify_network(audit, row, state):
    p = row["id"]
    audit.need("candidate_network_order", type(p) is int and p == len(state["networks"]) < 8)
    t, lam = CANDIDATES[p]
    u = np.asarray(row["U"]["real"], dtype=float)+1j*np.asarray(row["U"]["imag"], dtype=float)
    audit.need("U_shape_finite", u.shape == (20, 20) and bool(np.all(np.isfinite(u))))
    expected, h, scale, degrees = reference_cayley(state["a"], t, lam)
    construction = row["construction"]
    audit.check("Cayley_parameters_weighted_degree", fraction(construction["t"]) == t and fraction(construction["lambda"]) == lam
                and fraction(construction["denominator"]) == scale and construction["weighted_degrees"] == degrees)
    stored_h = np.asarray(construction["H"])
    audit.check("H_independent_exact_normalization", stored_h.shape == (20, 20) and bool(np.all(abs(stored_h-h) <= TOL)))
    audit.check("Cayley_spectral_vs_solve", float(abs(u-expected).max()) <= TOL)
    q, eye = abs(u)**2, np.eye(20)
    residuals = {"Udagger_U": float(abs(u.conj().T@u-eye).max()), "U_Udagger": float(abs(u@u.conj().T-eye).max()),
                 "transpose_symmetry": float(abs(u-u.T).max()), "q_row_mass": float(abs(q.sum(axis=1)-1).max()), "q_column_mass": float(abs(q.sum(axis=0)-1).max())}
    for name, value in residuals.items():
        audit.check("matrix_"+name, value <= TOL)
        audit.close("recorded_matrix_"+name, row["diagnostics"][name], value, TOL)
    state["networks"].append({key: value for key, value in row.items() if key not in ("case", "record_type", "diagnostics")})


class Inputs:
    def __init__(self, audit, root, binding_path):
        self.audit, self.root, self.partial, self.unreadable = audit, root, False, []
        audit.need("binding_size", binding_path.stat().st_size <= 65536)
        self.binding = parse(binding_path.read_text())
        b = self.binding
        audit.need("binding_schema", b["schema_version"] == 1 and b["primary_source_commit"] == SOURCE_COMMIT
                   and b["primary_source_sha256"] == SOURCE_SHA and b["checker_source_sha256"] == sha(Path(__file__)))
        audit.need("binding_artifact_bound", 1 <= len(b["artifacts"]) <= 13)
        self.paths, self.hashes = {}, {}
        for row in b["artifacts"]:
            relative, expected = row["path"], row["sha256"]
            audit.need("relative_input", isinstance(relative, str) and not Path(relative).is_absolute() and ".." not in Path(relative).parts)
            path = root/relative
            audit.need("regular_unique_input", path.is_file() and not path.is_symlink() and path.resolve().is_relative_to(root) and relative not in self.paths)
            audit.need("input_hash_before", sha(path) == expected, relative)
            self.paths[relative], self.hashes[relative] = path, expected
        audit.need("input_byte_cap", sum(p.stat().st_size for p in self.paths.values()) <= MAX_INPUT)
        self.data, self.manifest = b["data_directory"].rstrip("/"), b["producer_manifest"]
        audit.need("relative_data_and_bound_manifest", not Path(self.data).is_absolute() and ".." not in Path(self.data).parts and self.manifest in self.paths)
        names = {"raw.jsonl.gz", "seed_namespaces.json", "summary.json", "failure.json"}
        for cid, _, _ in CASES:
            names |= {f"context_{cid}.json", f"B_{cid}.json"} | {f"FAST_{cid}_{mode}.json" for mode in MODES}
        bound = {p for p in self.paths if p != self.manifest}
        audit.need("bound_whitelist", all(Path(p).parent.as_posix() == self.data and Path(p).name in names for p in bound))
        directory = root/self.data
        actual = {p.relative_to(root).as_posix() for p in directory.iterdir() if p.is_file()} if directory.is_dir() else set()
        audit.need("all_existing_data_bound", actual == bound)
        self.all_names = names

    def read(self, name):
        path = self.paths.get(self.data+"/"+name)
        if path is None:
            return None
        try:
            return parse(path.read_text())
        except (UnicodeError, json.JSONDecodeError):
            if not self.partial:
                raise
            self.unreadable.append(name)
            return None

    def unchanged(self):
        for name, path in self.paths.items():
            self.audit.check("input_hash_after", sha(path) == self.hashes[name], name)


def provenance(audit, inputs):
    manifest = parse(inputs.paths[inputs.manifest].read_text())
    audit.need("producer_v2", manifest["schema_version"] == 2 and manifest["repository"]["commit"] == inputs.binding["producer_commit"])
    audit.check("producer_claim", manifest["claim_id"] == "P65-CAYLEY-MARKOV-B80-FAST-DEV-VETO")
    recorded = {r["path"]: r for r in manifest["input_artifacts"]}
    audit.need("producer_17_input_closure", set(recorded) == CLOSURE and len(recorded) == len(manifest["input_artifacts"])
               and set(manifest["execution_artifacts"]) == CLOSURE)
    for path, row in recorded.items():
        audit.check("producer_inputs_unchanged", row["sha256"] == row["sha256_after"], path)
    for path, expected in KNOWN.items():
        audit.check("producer_known_hash", recorded[path]["sha256"] == expected, path)
    results = {r["path"]: r["sha256"] for r in manifest["outputs"] if r.get("kind") == "result"}
    for path, expected in inputs.hashes.items():
        if path != inputs.manifest:
            audit.check("producer_output_hash", results.get(path) == expected, path)
    completed = manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    inputs.partial = not completed
    return manifest, completed


def graph_state(audit, case, adjacency, context):
    cid, family, graph_seed = next(c for c in CASES if c[0] == case["id"])
    audit.need("case_identity", case == {"id": cid, "family": family, "seed": graph_seed})
    audit.need("N20_integer_graph", isinstance(adjacency, list) and len(adjacency) == 20 and all(isinstance(r, list) and len(r) == 20
               and all(type(w) is int and 0 <= w <= 5 for w in r) for r in adjacency))
    audit.need("graph_symmetry_no_loops", all(adjacency[i][i] == 0 for i in range(20)) and all(adjacency[i][j] == adjacency[j][i] for i in range(20) for j in range(20)))
    if family == "RR":
        audit.check("RR_degree6", all(sum(w != 0 for w in row) == 6 for row in adjacency))
    rng = np.random.Generator(np.random.PCG64(seed(graph_seed, "weights")))
    for i in range(20):
        for j in range(i+1, 20):
            if adjacency[i][j]:
                audit.check("canonical_edge_weight_PCG64", adjacency[i][j] == int(rng.integers(1, 6)))
    W = sum(adjacency[i][j] for i in range(20) for j in range(i+1, 20))
    state = {"a": adjacency, "W": W, "case": cid, "context": context, "networks": [], "ledger": [], "training": [], "fresh": [],
             "fitnesses": [], "chain": None, "selected": None, "training_start": None, "fresh_start": None, "fresh_starts": [], "pending": None,
             "best": None, "scores": {"initial": 0, "proposal": 0, "current": 0}, "requested": 0, "completed": 0, "arm_complete": None}
    if context is not None:
        audit.check("raw_context_graph", context["case"] == case and context["adjacency"] == adjacency and context["W"] == W)
        component(audit, state, ("preparation",), context["preparation"])
        component(audit, state, ("compilation",), context["compilation"])
        clock(audit, context["excluded_matrix_diagnostics"], "excluded_matrix")
    return state


def score(audit, state, selected, kind, label):
    selected = subset(selected)
    value = cut(state["a"], selected)
    state["scores"][kind] += 1
    if state["best"] is None or value < state["best"]["cut"]:
        state["best"] = {"cut": value, "subset": list(selected), "label": list(label), "score_kind": kind}
    return value


def transition(adjacency, current, best, counts, beta, coin):
    """Pure independent Markov state calculation; all labels/timing checked outside."""
    if len(counts) != len(adjacency) or any(type(x) is not int or not 0 <= x <= len(current) for x in counts) or sum(counts) != len(current):
        raise InvalidEvidence("Invalid complete PNR counts")
    collision = max(counts) > 1
    proposal = None if collision else [i for i, value in enumerate(counts) if value]
    before = cut(adjacency, current)
    proposed_cut = None if collision else cut(adjacency, proposal)
    probability = None if collision else (1. if proposed_cut <= before else math.exp(-beta*(proposed_cut-before)))
    if collision:
        if coin is not None:
            raise InvalidEvidence("Collision consumed a coin")
        accepted = False
    else:
        if not finite(coin) or not 0 <= coin < 1:
            raise InvalidEvidence("Every CF branch requires a fresh coin")
        accepted = coin < probability
    after = list(proposal) if accepted else list(current)
    current_cut = cut(adjacency, after)
    return {"collision": collision, "proposal": proposal, "proposal_cut": proposed_cut, "coin": coin,
            "coin_seed_used": not collision, "acceptance_probability": probability, "accepted": accepted,
            "current_before_cut": before, "current": after, "current_cut": current_cut, "chain_best_cut": min(best, current_cut)}


def chain_label(chain):
    return (chain["stage"], chain["candidate"] if chain["stage"] == "training" else "selected", chain["chain"])


def choose_fitness(values):
    if len(values) != 8 or any(not isinstance(v, Fraction) for v in values):
        raise InvalidEvidence("Eight exact fitnesses required")
    return min(range(8), key=lambda p: (values[p], p))


def tag_check(audit, row, requested):
    for key in ("case", "arm", "stage", "parameter_seed_label", "candidate", "chain", "step", "source", "seed_roles", "beta"):
        audit.need("attempt_tag_"+key, row.get(key) == requested[key])


def raw_replay(audit, inputs, completed):
    states, events, global_mean, failure, failed_attempt = {}, Counter(), None, None, False
    path = inputs.paths.get(inputs.data+"/raw.jsonl.gz")
    if path is None and not completed:
        return states, {"events": {}, "global": None, "failure": None, "truncated": True}
    audit.need("raw_available", path is not None)
    truncated = False
    try:
        with gzip.open(path, "rt", encoding="utf8") as stream:
            size = 0
            for line in iter(lambda: stream.readline(1048577), ""):
                size += len(line.encode("utf8"))
                audit.need("raw_byte_line_cap", size <= MAX_RAW and len(line) <= 1048576)
                row = parse(line); kind = row["record_type"]
                audit.need("no_event_after_failure", failure is None and (not failed_attempt or kind == "first_failure"))
                events[kind] += 1
                if kind == "first_failure":
                    failure = {k: v for k, v in row.items() if k != "record_type"}; continue
                if kind == "B_equal_graph_fresh_mean":
                    audit.need("one_global_mean", global_mean is None and len(states) == 2)
                    global_mean = row; meter = clock(audit, row["paid_aggregation"], "global")
                    audit.close("global_equal_share", row["cost_share_per_case"], meter["wall_seconds"]/2)
                    for state in states.values():
                        component(audit, state, ("global_aggregation_share",), {k: v/2 for k, v in meter.items()})
                    continue
                if kind == "supplied_graph":
                    cid = row["case"]["id"]
                    audit.need("one_known_case_graph", cid in {c[0] for c in CASES} and cid not in states)
                    context = inputs.read(f"context_{cid}.json")
                    states[cid] = graph_state(audit, row["case"], row["adjacency"], context)
                    states[cid]["graph_generation"] = clock(audit, row["excluded_generation"], "excluded_graph")
                    continue
                cid = row["case"]; audit.need("raw_known_case", cid in states)
                state = states[cid]
                if kind == "candidate_network":
                    verify_network(audit, row, state)
                elif kind in ("common_training_start", "fresh_start"):
                    stage, chain = ("training", 0) if kind == "common_training_start" else ("fresh", row["chain"])
                    audit.need("start_order", state["chain"] is None and state["pending"] is None)
                    if stage == "training":
                        audit.need("single_training_start", state["training_start"] is None and len(state["networks"]) == 8)
                    else:
                        audit.need("fresh_after_selection", state["selected"] is not None and chain == len(state["fresh"]) < 3)
                        audit.need("one_fresh_start_per_chain", len(state["fresh_starts"]) == chain)
                        audit.check("starts_with_replacement", row["sampling_with_replacement"] is True)
                    start_seed = seed(65100000, cid, stage, chain)
                    selected = sorted(np.random.Generator(np.random.PCG64(start_seed)).permutation(20)[:10].tolist())
                    audit.check("start_seed_and_subset", row["seed"] == start_seed and row["source"] == selected)
                    expected_cut = score(audit, state, row["source"], "initial", ("training_start",) if stage == "training" else ("fresh_start", chain))
                    audit.check("start_actual_cut", row["cut"] == expected_cut)
                    component(audit, state, ("training_start",) if stage == "training" else ("fresh_start", chain), row["start_compute"])
                    state["training_start" if stage == "training" else "fresh_start"] = row
                    if stage == "fresh": state["fresh_starts"].append(row)
                elif kind == "chain_start":
                    audit.need("no_overlapping_chain", state["chain"] is None and state["pending"] is None)
                    stage = row["stage"]; p = len(state["training"]) if stage == "training" else state["selected"]
                    audit.need("chain_grid_order", stage in ("training", "fresh") and row["candidate"] == p
                               and row["chain"] == (0 if stage == "training" else len(state["fresh"])) and state["arm_complete"] is None
                               and ((p < 8 and len(state["fitnesses"]) == p) if stage == "training" else (p is not None and len(state["fresh"]) < 3)))
                    start = state["training_start" if stage == "training" else "fresh_start"]
                    audit.need("chain_reset_own_start", start is not None and row["source"] == start["source"] and row["initial_cut"] == start["cut"])
                    active = {"stage": stage, "candidate": p, "chain": row["chain"], "initial": list(row["source"]), "initial_cut": row["initial_cut"],
                              "current": list(row["source"]), "best": row["initial_cut"], "attempts": [], "cuts": [], "betas": [], "reset": row["reset_compute"]}
                    state["chain"] = active
                    component(audit, state, ("chain_reset", *chain_label(active)), row["reset_compute"])
                elif kind == "beta_preparation":
                    active = state["chain"]; audit.need("beta_active_chain", active is not None and state["pending"] is None)
                    step = len(active["attempts"]); label = (*chain_label(active), step)
                    audit.need("beta_order", (row["stage"], row["parameter_seed_label"], row["chain"], row["step"]) == label and len(active["betas"]) == step)
                    expected = float(Fraction(80, state["W"])) if active["stage"] == "training" else (20/state["W"])*2**(step/2)
                    audit.close("beta_schedule", row["beta"], expected, TOL)
                    active["beta"] = row["beta"]; active["betas"].append(row["beta_compute"])
                    component(audit, state, ("beta", *label), row["beta_compute"])
                elif kind == "attempt_requested":
                    active = state["chain"]; audit.need("request_has_chain", active is not None and state["pending"] is None)
                    step = len(active["attempts"]); label = (*chain_label(active), step)
                    audit.need("request_current_source_and_plan", row["arm"] == "bosonic" and row["candidate"] == active["candidate"]
                               and row["source"] == active["current"] and row["photons"] == 10
                               and (row["stage"], row["parameter_seed_label"], row["chain"], row["step"]) == label
                               and step < (2 if active["stage"] == "training" else 8) and len(active["betas"]) == step+1)
                    subset(row["source"]); audit.check("request_beta", row["beta"] == active["beta"])
                    audit.check("owned_count_coin_roles", row["seed_roles"] == roles(cid, "bosonic", *label))
                    state["pending"] = {"request": row, "factory": None}; state["requested"] += 1
                elif kind == "factory_setup":
                    pending = state["pending"]; audit.need("one_fresh_factory", pending is not None and pending["factory"] is None)
                    tag_check(audit, row, pending["request"]); pending["factory"] = row["accounting"]
                elif kind == "attempt":
                    pending, active = state["pending"], state["chain"]
                    audit.need("attempt_has_request_factory", pending is not None and pending["factory"] is not None)
                    tag_check(audit, row, pending["request"])
                    counts = row["counts"]; audit.need("PNR_N20_list", isinstance(counts, list) and len(counts) == 20 and row["fallback"] is False)
                    collision = any(type(x) is int and x > 1 for x in counts)
                    coin = None if collision else float(np.random.Generator(np.random.PCG64(row["seed_roles"]["coin"])).random())
                    expected = transition(state["a"], active["current"], active["best"], counts, row["beta"], coin)
                    for field, value in expected.items():
                        if field == "acceptance_probability" and value is not None:
                            audit.close("Metropolis_probability", row[field], value, TOL)
                        else:
                            audit.check("transition_"+field, row[field] == value)
                    label = (*chain_label(active), row["step"])
                    if not expected["collision"]:
                        score(audit, state, expected["proposal"], "proposal", label)
                    score(audit, state, expected["current"], "current", label)
                    audit.check("all_paid_best_at_attempt", row["all_paid_best_cut"] == state["best"]["cut"])
                    active["current"], active["best"] = expected["current"], expected["chain_best_cut"]
                    active["cuts"].append(expected["current_cut"])
                    acc = row["factory_accounting"]; factory = clock(audit, row["factory_total"], "factory_total")
                    audit.check("factory_receipt_duplicate", acc == pending["factory"])
                    audit.need("factory_inner_WALL", finite(acc["returned_backend_wall"]) and 0 <= acc["returned_backend_wall"] <= factory["wall_seconds"]+TIME_TOL)
                    audit.close("factory_prefix_paid", acc["classical_prefix_wall"], max(0., factory["wall_seconds"]-acc["returned_backend_wall"]))
                    audit.close("factory_total_WALL", acc["factory_total_wall"], factory["wall_seconds"])
                    audit.close("factory_total_CPU", acc["factory_total_cpu"], factory["cpu_seconds"])
                    audit.check("factory_CPU_split_unknown", acc["backend_cpu"] is None and acc["classical_prefix_cpu"] is None and acc["CPU_split_available"] is False)
                    clock(audit, row["excluded_count_generation"], "excluded_count_generation")
                    component(audit, state, ("attempt_setup", *label), row["setup"])
                    component(audit, state, ("attempt_postprocessing", *label), row["postprocessing"])
                    component(audit, state, ("factory_classical_prefix", *label), acc["classical_prefix_wall"], True)
                    active["attempts"].append({k: v for k, v in row.items() if k != "record_type"})
                    state["completed"] += 1; state["pending"] = None
                elif kind == "chain_complete":
                    active = state["chain"]; audit.need("complete_chain_exists", active is not None and state["pending"] is None)
                    audit.need("chain_complete_steps", len(active["attempts"]) == (2 if active["stage"] == "training" else 8))
                    expected = {"stage": active["stage"], "chain": active["chain"], "candidate": active["candidate"], "initial": active["initial"], "initial_cut": active["initial_cut"],
                                "final": active["current"], "final_current_cut": active["cuts"][-1], "chain_best_cut": active["best"], "gain_from_start": active["initial_cut"]-active["best"],
                                "current_cuts": active["cuts"], "attempts": active["attempts"], "reset_compute": active["reset"], "beta_compute": active["betas"]}
                    audit.check("chain_complete_full_record", {k: v for k, v in row.items() if k not in ("record_type", "case", "final_aggregation")} == expected)
                    component(audit, state, ("chain_final", *chain_label(active)), row["final_aggregation"])
                    state["training" if active["stage"] == "training" else "fresh"].append({k: v for k, v in row.items() if k not in ("record_type", "case")})
                    state["chain"] = None
                elif kind == "candidate_fitness":
                    p = len(state["fitnesses"]); audit.need("fitness_order", row["candidate"] == p and len(state["training"]) == p+1 and state["chain"] is None)
                    value = Fraction(sum(state["training"][-1]["current_cuts"]), 2*state["W"])
                    audit.check("exact_two_current_fitness", fraction(row["fitness"]) == value)
                    state["fitnesses"].append(value); state["training"][-1]["fitness_compute"] = row["fitness_compute"]
                    component(audit, state, ("fitness", p), row["fitness_compute"])
                elif kind == "selected_before_fresh":
                    audit.need("select_after_eight_before_fresh", len(state["fitnesses"]) == 8 and state["selected"] is None and not state["fresh"])
                    selected = choose_fitness(state["fitnesses"])
                    audit.check("exact_selection_ties_first", row["candidate"] == selected and [fraction(v) for v in row["fitnesses"]] == state["fitnesses"]
                                and tuple(fraction(v) for v in row["parameters"]) == CANDIDATES[selected])
                    state["selected"] = selected; state["selection_meter"] = row["selection_compute"]
                    component(audit, state, ("selection",), row["selection_compute"])
                elif kind == "arm_complete":
                    audit.need("complete_B_case", state["completed"] == state["requested"] == 40 and len(state["fresh"]) == 3 and state["arm_complete"] is None)
                    component(audit, state, ("arm_final",), row["final_aggregation"])
                    audit.check("arm_198_components", len(state["ledger"]) == 198 and row["paid_components"] == state["ledger"])
                    audit.close("arm_component_sum", row["B_classical_wall"], math.fsum(v["wall_seconds"] for v in state["ledger"]))
                    state["arm_complete"] = row
                elif kind == "failed_attempt":
                    failed_attempt = True
                else:
                    audit.need("known_record_type", False, kind)
    except (EOFError, OSError, UnicodeError, json.JSONDecodeError) as error:
        truncated = True; audit.check("completed_raw_parseable", not completed, type(error).__name__)
    return states, {"events": dict(events), "global": global_mean, "failure": failure, "truncated": truncated}


def audit_B(audit, inputs, states, raw, summary):
    verified, files = {}, {}
    for cid, _, _ in CASES:
        value = inputs.read(f"B_{cid}.json")
        if value is None and summary is not None:
            choices = [r for r in summary.get("results", []) if r["case"] == cid]
            if len(choices) == 1:
                value = dict(choices[0]); value["FAST"] = {}
        if value is None:
            continue
        state = states[cid]; audit.need("B_file_after_arm_complete", state["arm_complete"] is not None)
        audit.check("context_network_duplicate", state["context"] is not None and state["context"]["networks"] == state["networks"])
        fresh = []
        for chain, row in enumerate(state["fresh"]):
            copied = dict(row)
            # The source adds start_compute after emitting chain_complete.
            start_seed = seed(65100000, cid, "fresh", chain)
            start = sorted(np.random.Generator(np.random.PCG64(start_seed)).permutation(20)[:10].tolist())
            audit.check("fresh_chain_own_start", copied["initial"] == start)
            copied["start_compute"] = state["fresh_starts"][chain]["start_compute"]
            fresh.append(copied)
        metric = Fraction(sum(row["chain_best_cut"] for row in state["fresh"]), 3*state["W"])
        audit.check("B_complete_scored_statistics", value["case"] == cid and value["selected_candidate"] == state["selected"]
                    and tuple(fraction(v) for v in value["selected_parameters"]) == CANDIDATES[state["selected"]]
                    and [fraction(v) for v in value["fitnesses"]] == state["fitnesses"] and value["training"] == state["training"] and value["fresh"] == fresh
                    and fraction(value["B_fresh_chain_best_normalized_mean"]) == metric and value["B_paid_best_record"] == state["best"]
                    and value["B_paid_best"] == state["best"]["cut"] and value["score_counts"] == state["scores"] and value["FAST"] == {})
        audit.check("actual_score_calls", state["scores"] == {"initial": 4, "proposal": state["scores"]["proposal"], "current": 40})
        audit.check("B_exact_component_ledger", value["paid_components"] == state["ledger"])
        if raw["global"] is not None:
            audit.check("B_199_components", len(state["ledger"]) == 199)
            audit.close("B_global_cost_share", value["global_mean_aggregation_share"], raw["global"]["cost_share_per_case"])
        paid = math.fsum(v["wall_seconds"] for v in state["ledger"])
        audit.close("B_paid_clock_sum", value["B_classical_wall"], paid)
        audit.check("B_meter_duplicates", value["training_start_compute"] == state["training_start"]["start_compute"]
                    and value["selection_compute"] == state["selection_meter"] and value["final_aggregation"] == state["arm_complete"]["final_aggregation"])
        verified[cid] = {"best": state["best"]["cut"], "paid": paid, "metric": metric}; files[cid] = value
    if len(verified) == 2 and raw["global"] is not None:
        audit.check("equal_graph_chain_best_mean", fraction(raw["global"]["mean"]) == sum((r["metric"] for r in verified.values()), Fraction(0))/2)
    return verified, files


def audit_FAST(audit, row, cid, mode, state, B):
    result, trace = row["result"], row["result"]["trace"]
    audit.check("FAST_owned_identity", row["case"] == cid and row["mode"] == mode and row["seed"] == seed(65500000, cid, mode)
                and result["seed"] == row["seed"] and result["initialization"] == mode and result["n"] == 20)
    adapter = clock(audit, row["adapter"], "FAST_adapter")
    audit.close("FAST_B_grant", row["B_classical_WALL_allowance"], B["paid"])
    audit.close("FAST_adapter_CPU_subtraction", row["solver_CPU_allowance"], max(0., B["paid"]-adapter["cpu_seconds"]))
    budget = result["cpu_budget_seconds"]; audit.need("FAST_budget_nonnegative", finite(budget) and budget >= 0)
    audit.close("FAST_inner_budget", budget, row["solver_CPU_allowance"])
    audit.check("FAST_no_free_features", result["free_incumbent_used"] is False and result["external_features_used"] is False and result["proposal_cap_is_cost_equivalent"] is False
                and row["other_arm_seconds_granted"] == row["optical_latency_assumed_seconds"] == 0 and row["hardware_runtime_measured"] is False)
    names = ("cpu_seconds", "wall_seconds", "proposal_count", "best_cut", "best_subset_packbits_little", "stage")
    n = len(trace["cpu_seconds"]); audit.need("FAST_shape_guard", n <= 20002 and all(len(trace[k]) == n for k in names) and result["max_proposals"] == 10000)
    previous_cpu = previous_wall = previous_work = 0.; previous_cut = math.inf
    masks, eligible, scans, anneal_work, perturb_work, restarts, perturbations, setups = [], [], 0, 0, 0, 0, 0, 0
    for i in range(n):
        cpu, wall, work, value, stage = (trace[k][i] for k in ("cpu_seconds", "wall_seconds", "proposal_count", "best_cut", "stage"))
        audit.need("FAST_time_work_types", finite(cpu) and finite(wall) and cpu >= previous_cpu and wall >= previous_wall and type(work) is int and previous_work <= work <= 10000 and type(value) is int)
        selected = unpack(trace["best_subset_packbits_little"][i]); audit.need("FAST_K10_mask", len(selected) == 10)
        audit.check("FAST_scalar_cut_monotone", cut(state["a"], selected) == value and value <= previous_cut)
        change = work-previous_work
        if i == 0:
            audit.check("FAST_initial_checkpoint", stage == "initialization" and work == 1)
        elif stage == "anneal_setup":
            setups += 1; audit.check("FAST_setup_zero_work", setups == 1 and change == 0 and work >= 101)
        else:
            audit.check("FAST_positive_work", change > 0)
        if stage in ("initial_scan", "descent_scan"):
            scans += 1; audit.check("FAST_full100_scan", change == 100)
        anneal_work += change if stage == "anneal" else 0; perturb_work += change if stage == "perturb_best" else 0
        restarts += stage == "uniform_restart"; perturbations += stage == "perturb_best"
        audit.check("FAST_known_stage", stage in {"initialization", "initial_scan", "descent_scan", "anneal_setup", "anneal", "uniform_restart", "perturb_best"})
        if cpu <= budget: eligible.append(i)
        masks.append(selected); previous_cpu, previous_wall, previous_work, previous_cut = cpu, wall, work, value
    index = eligible[-1] if eligible else None; best = trace["best_cut"][index] if index is not None else None
    audit.check("FAST_exact_eligible_snapshot", result["eligible_checkpoint_index"] == index and result["has_eligible_result"] == (index is not None)
                and result["best_cut"] == best and result["best_subset"] == (masks[index] if index is not None else None) and result["best_snapshot_cached_online"] is True)
    for name in ("cpu", "wall"):
        audit.check("FAST_eligible_"+name, result["eligible_checkpoint_"+name+"_seconds"] == (trace[name+"_seconds"][index] if index is not None else None))
        for part in ("compute_", "online_search_", "finalization_"):
            audit.need("FAST_nonnegative_clock", finite(result[part+name+"_seconds"]) and result[part+name+"_seconds"] >= 0)
        audit.close("FAST_clock_sum", result["compute_"+name+"_seconds"], result["online_search_"+name+"_seconds"]+result["finalization_"+name+"_seconds"])
        audit.check("FAST_trace_before_export", not n or trace[name+"_seconds"][-1] <= result["online_search_"+name+"_seconds"]+TIME_TOL)
    first = [i for i, stage in enumerate(trace["stage"]) if stage == "initial_scan"]
    timely = bool(first and trace["cpu_seconds"][first[0]] <= budget); audit.check("FAST_single_first_scan", len(first) <= 1)
    last = trace["cpu_seconds"][-1] if n else result["validation_cpu_seconds"]
    early = (result["guard_blocked_full_scan"] or result["stop_reason"] == "max_proposals") and last < budget
    prefix, acceptance = index is not None, index is not None and timely and not early
    expected = {"prefix_eligible_for_veto": prefix, "comparison_acceptance_eligible": acceptance, "best_cut": best, "cpu_budget_seconds": budget,
                "eligible_checkpoint_cpu_seconds": result["eligible_checkpoint_cpu_seconds"], "first_scan_completed_before_deadline": timely,
                "early_cap_inconclusive": bool(early), "early_wall_inconclusive": False}
    audit.check("FAST_caller_receipts", all(row[k] == v for k, v in expected.items()))
    audit.check("FAST_inner_flags", result["first_scan_completed_before_deadline"] == timely and result["early_cap_inconclusive"] == early
                and result["early_wall_inconclusive"] is False and result["comparison_acceptance_eligible"] == (prefix and not early)
                and result["proposal_count"] == previous_work and result["cap_hit"] == (previous_work >= 10000))
    audit.check("FAST_algorithm_and_initialization", result["algorithm"] == "P50_from_raw_descent_first_v1"
                and result["initialization_completed_before_deadline"] == bool(n and trace["cpu_seconds"][0] <= budget)
                and result["guard_blocked_full_scan"] == (result["stop_reason"] == "proposal_guard_before_full_scan"))
    counters = result["counters"]
    audit.check("FAST_work_counter_reconciliation", counters["initial_cut_scores"] == int(bool(n)) and counters["vectorized_scans"] == scans
                and counters["anneal_proposals"] == anneal_work and counters["perturbations"] == perturbations and counters["uniform_restarts"] == restarts
                and counters["full_restart_cut_scores"] == restarts and counters["delta_evaluations"] == 100*scans+anneal_work+perturb_work
                and previous_work == int(bool(n))+counters["delta_evaluations"]+restarts)
    if n:
        audit.check("FAST_audit_and_initial_snapshots", result["initial_cut"] == trace["best_cut"][0] and result["initial_subset"] == masks[0]
                    and result["overall_completed_best_cut"] == trace["best_cut"][-1] and result["overall_completed_best_subset"] == masks[-1])
    audit.close("FAST_overrun", result["cpu_overrun_seconds"], max(0., result["compute_cpu_seconds"]-budget))
    return {"prefix": prefix, "acceptance": acceptance, "best": best, "checkpoints": n}


def gate(B, fast, failed=False):
    complete = not failed and len(B) == 2 and set(fast) == {(cid, mode) for cid, _, _ in CASES for mode in MODES}
    vetoes = [mode for mode in MODES if complete and all(fast[cid, mode]["prefix"] and fast[cid, mode]["best"] <= B[cid]["best"] for cid, _, _ in CASES)]
    eligible = complete and all(row["acceptance"] for row in fast.values())
    status = "INCONCLUSIVE_FIRST_FAILURE" if failed else "DEV_REJECTED_FIXED_FAST" if vetoes else "INCONCLUSIVE_FAST_ELIGIBILITY" if not eligible else "STAGE1_OPTIONAL_CONTROLS_REQUIRED"
    return status, vetoes, bool(eligible)


def run(audit, inputs):
    manifest, completed = provenance(audit, inputs)
    summary, failure_file, table = inputs.read("summary.json"), inputs.read("failure.json"), inputs.read("seed_namespaces.json")
    if table is not None:
        actual = {tuple(r["role"]): r["seed"] for r in table}; expected = namespace_table()
        audit.check("all820_role_recipes", actual == expected and len(actual) == len(table) == 820 and len(set(actual.values())) == 820
                    and all(v != 0 for k, v in actual.items() if k[-1] == "count"))
    states, raw = raw_replay(audit, inputs, completed)
    B, files = audit_B(audit, inputs, states, raw, summary); fast, count = {}, 0
    for cid, _, _ in CASES:
        for mode in MODES:
            row = inputs.read(f"FAST_{cid}_{mode}.json")
            if row is None: continue
            audit.need("FAST_has_complete_B", cid in B)
            fast[cid, mode] = audit_FAST(audit, row, cid, mode, states[cid], B[cid]); count += fast[cid, mode]["checkpoints"]
            if summary is not None and "results" in summary:
                match = [r for r in summary["results"] if r["case"] == cid]
                audit.check("FAST_compact_summary_duplicate", len(match) == 1 and match[0]["FAST"].get(mode) == {k: v for k, v in row.items() if k != "result"})
    status, vetoes, eligible = gate(B, fast)
    complete = (completed and summary is not None and summary.get("failure") is None and table is not None and failure_file == {"failure": None}
                and {Path(p).name for p in inputs.paths if p != inputs.manifest} == inputs.all_names and len(B) == 2 and len(fast) == 4
                and raw["failure"] is None and not raw["truncated"])
    shots, requested = sum(s["completed"] for s in states.values()), sum(s["requested"] for s in states.values())
    if completed:
        audit.need("complete_primary_full_evidence", complete)
        audit.check("full80attempts_factories", shots == requested == raw["events"].get("factory_setup") == raw["events"].get("attempt") == 80)
    if summary is not None:
        audit.check("no_positive_and_completed_count", summary["positive_accepted"] is False and summary["completed_B_shots"] == shots)
        audit.check("raw_digest", summary["raw_sha256"] == inputs.hashes.get(inputs.data+"/raw.jsonl.gz"))
        if "attempted_B_shots" in summary:
            audit.check("requested_photon_accounting", summary["attempted_B_shots"] == requested and summary["simulated_injected_B_photons"] == 10*requested and summary["simulated_completed_B_photons"] == 10*shots)
            audit.check("no_optimum_QPU_optional_prices", summary["actual_QPU_calls"] == summary["actual_QPU_photons"] == 0 and summary["optimum_used"] is False
                        and summary["heldout_opened"] is False and summary["optional_models_executed"] is False and summary["hardware_runtime_measured"] is False
                        and summary["internal_factory_CPU_split_available"] is False and summary["IO_or_other_arm_seconds_granted"] is False and summary["source_sha256"] == SOURCE_SHA)
        if raw["failure"] is not None:
            audit.check("first_failure_identity", summary["status"] == "INCONCLUSIVE_FIRST_FAILURE" and summary["failure"] == raw["failure"]
                        and (failure_file is None or failure_file == {"failure": raw["failure"]}))
        if complete:
            audit.check("stage1_same_fixed_mode_gate", summary["status"] == status and summary["fixed_FAST_veto_modes"] == vetoes and summary["FAST_all_comparison_eligible"] == eligible)
            audit.check("unrun_optional_controls", summary["optional_controls"] == {arm: "NOT_RUN_DUE_FAST_VETO" if vetoes else "NOT_RUN_STAGE1_SCOPE" for arm in OPTIONAL})
            audit.check("global_chain_best_mean", fraction(summary["B_equal_graph_fresh_chain_best_mean"]) == sum((r["metric"] for r in B.values()), Fraction(0))/2)
            audit.need("summary_two_unique_cases", len(summary["results"]) == 2 and {r["case"] for r in summary["results"]} == set(B))
            for row in summary["results"]:
                cid = row["case"]; saved = dict(row); saved["FAST"] = {}
                audit.check("B_summary_duplicate", saved == files[cid])
                audit.check("summary_full_ledger", summary["B_paid_components"][cid] == states[cid]["ledger"] and summary["B_paid_best_cached_online"][cid] == states[cid]["best"])
                audit.close("summary_B_grant", summary["B_paid_classical_wall"][cid], B[cid]["paid"])
                audit.check("graph_generation_excluded", summary["excluded_graph_generation"][cid] == states[cid]["graph_generation"])
            native = summary["native_threads"]
            audit.check("native_configuration_receipts", native["requested"] == native["readback_before_work"] == native["readback_after_imports"] == native["readback_after_work"] == 1)
    return {"producer_status": manifest["run"]["status"], "complete_comparison": complete, "completed_B_attempts": shots, "requested_B_attempts": requested,
            "raw_events": raw["events"], "FAST_checkpoints": count, "raw_truncated": raw["truncated"], "unreadable_partial_files": inputs.unreadable,
            "replayed_stage1_status": status if complete else "INCONCLUSIVE_PARTIAL_PRIMARY", "recorded_fixed_FAST_veto_modes": vetoes if complete else []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(".")); parser.add_argument("--binding", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); root = args.root.resolve()
    if args.output.exists() or not args.output.resolve().is_relative_to(root):
        raise InvalidEvidence("Output must be new and inside project")
    started, audit, inputs, detail, fatal = time.process_time(), Audit(), None, {}, None
    try:
        binding = args.binding.resolve(); audit.need("binding_inside_project", binding.is_relative_to(root) and not args.binding.is_symlink())
        inputs = Inputs(audit, root, binding)
        audit.need("output_separate", args.output.resolve() not in {p.resolve() for p in inputs.paths.values()} | {binding})
        detail = run(audit, inputs)
    except Exception as error:
        fatal = f"{type(error).__name__}: {error}"[:500]; audit.check("fatal_or_unchecked_evidence", False, fatal)
    if inputs is not None:
        try: inputs.unchanged()
        except Exception as error: audit.check("input_after_unavailable", False, type(error).__name__)
    verified = not audit.failures and detail.get("complete_comparison", False)
    status = "PASS_RECORDED_CONSISTENCY" if verified else "FAIL_OR_UNCHECKED_EVIDENCE" if audit.failures else "PARTIAL_CONSISTENCY_INCONCLUSIVE"
    report = {"status": status, "checks": dict(audit.checks), "failures": dict(audit.failures), "examples": audit.examples, "fatal": fatal, **detail,
              "complete_comparison_verified": verified, "accepted_recorded_fixed_FAST_veto_modes": detail.get("recorded_fixed_FAST_veto_modes", []) if verified else [],
              "positive_accepted": False, "primary_imports_used": False, "new_graphs_or_optical_samples": False,
              "input_sha256": inputs.hashes if inputs else {}, "checker_sha256": sha(Path(__file__)), "cpu_seconds_inside_audit": time.process_time()-started,
              "software_observed": {"Python": ".".join(map(str, sys.version_info[:3])), "numpy": np.__version__},
              "limitations": ["Recorded data/role replay only, not independent physical counts, bosonic likelihoods, full PNR distribution or optimum verification.",
                  "Topology is not regenerated with NetworkX; canonical edge weight assignment, RR degree and archived B/FAST adjacency are checked.",
                  "Recorded paid ledgers/deadlines are reconciled; authentic elapsed time, online causality, hardware cost and unrecorded FAST moves are not verified.",
                  "Spectral Cayley comparison uses absolute3e-12, not exact or interval probabilities.",
                  "Failed/truncated primaries remain inconclusive prefixes; accepted recorded veto requires complete80B/fourFAST and unchanged hash-bound inputs."]}
    encoded = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if len(encoded.encode()) > MAX_REPORT: raise InvalidEvidence("Audit report cap exceeded")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf8") as stream: stream.write(encoded)
    print(json.dumps({"status": status, "checks": sum(audit.checks.values()), "failures": dict(audit.failures), "fatal": fatal}))
    return 1 if audit.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
