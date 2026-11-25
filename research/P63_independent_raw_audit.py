"""Frozen-format P63 recorded-data audit; no primary/helper imports or sampling.

CODE ONLY until ROOT freezes this checker, binds immutable files by hash and
authorizes a bounded run. NumPy is used for PCG64 role replay and small matrix
identities. This does not regenerate a graph, bosonic count or FAST proposal.
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

SOURCE_SHA = "7f60cb437a9936323851d926ca18f16c7899b16a8d5353c69df88cf21a03d5d6"
SOURCE_COMMIT = "8b20dca7bbe476a2eed75433b31e5ca582809484"
CASES = (("n18_ER_6301801", "ER", 6301801), ("n18_RR_6301802", "RR", 6301802))
ARMS = ("bosonic", "j_aligned", "continuous_phase", "distinguishable",
        "independent_B_marginals", "uniform_subset", "phase_average")
MODES = ("random", "spectral")
PLAN = tuple(("training", t, sign, 0, 4) for t in range(3) for sign in ("plus", "minus")) + (
    ("evaluation", 3, "final", 0, 8), ("evaluation", 3, "final", 1, 8))
TOL, TIME_TOL = 3e-12, 1e-8
MAX_INPUT_BYTES, MAX_RAW_TEXT, MAX_REPORT = 33554432, 8388608, 4194304
KNOWN_INPUTS = {
    "research/P63_spsa_fast_stage.py": SOURCE_SHA,
    "tests/test_p63_spsa_fast_stage.py": "1bf5baac5740e75a37096dd841c10d4b5486691811259062bd15a569f7d2bd9b",
    "research/P63_spsa_fast_stage_spec.json": "5eea4f4c46789effa5102f6f1d5f71bb9de6d2c8b050c3cb3920bef2a67877dd",
    "research/P63_spsa_fast_stage_contract.md": "74262584762abda98b6e9e627b332817b2fa8aa11c210e75b9f65dd2737604e3",
    "research/P63_spsa_fast_stage_preflight_contract.json": "9fa288deeb562e31516fac0b8d2f1ba331c25c9dad448dbe44a2f80f0683dea6",
    "research/P63_spsa_fast_stage_execution_contract.json": "5232bf44880b092cce603b242391882b0ec3a63f0c0577fd2dde98697d343482",
    "research/P63_STAGE1_PRE_DATA_AMENDMENT.md": "08214cc0c05760359ffc637318fac60f7deb1cf683675e637008c1f63b1e53b4",
    "research/P43_global_gain_probe.py": "b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777",
    "research/P50_fast_from_scratch.py": "6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86",
}
PRIMARY_CLOSURE = set(KNOWN_INPUTS) | {
    "AGENTS.md", "research/P63_EXTENSIVE_PHASE_ARCHITECTURE_CARD.md",
    "theory/P63_extensive_phase_structural_checks.md", "research/P63_INDEPENDENT_STATIC_PHYSICS_REVIEW.md",
    "research/P50_FAST_FROM_RAW_API_CARD.md", "research/P50_fast_from_scratch_contract.json",
    "research/P55_PRE_DATA_AMENDMENT.md", "pyproject.toml", "requirements-research-lock.txt"}


class InvalidEvidence(RuntimeError):
    pass


class Audit:
    def __init__(self):
        self.checks, self.failures, self.examples = Counter(), Counter(), []

    def check(self, name, condition, detail=""):
        self.checks[name] += 1
        if not bool(condition):
            self.failures[name] += 1
            if len(self.examples) < 32:
                self.examples.append({"check": name, "detail": str(detail)[:240]})
        return bool(condition)

    def require(self, name, condition, detail=""):
        if not self.check(name, condition, detail):
            raise InvalidEvidence(name + ": " + str(detail)[:240])

    def close(self, name, actual, expected, tolerance=TIME_TOL):
        return self.check(name, finite(actual) and finite(expected)
                          and abs(float(actual)-float(expected)) <= tolerance, (actual, expected))


def finite(x):
    return type(x) in (int, float) and math.isfinite(x)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def json_read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise InvalidEvidence("Duplicate JSON key: " + key)
            result[key] = value
        return result
    with Path(path).open(encoding="utf8") as stream:
        return json.load(stream, object_pairs_hook=unique,
                         parse_constant=lambda x: (_ for _ in ()).throw(InvalidEvidence("Nonfinite JSON: " + x)))


def seed(*parts):
    return int.from_bytes(hashlib.sha256("/".join(str(x) for x in parts).encode()).digest()[:4], "little")


def integers(audit, values, n, name):
    audit.require(name, isinstance(values, list) and len(values) == n and all(type(x) is int for x in values))
    return values


def fraction(value):
    if type(value) not in (int, str):
        raise InvalidEvidence("Exact integer/Fraction string required")
    return Fraction(value)


def angles(value):
    if not isinstance(value, list) or len(value) != 10:
        raise InvalidEvidence("Ten exact phase coordinates required")
    return tuple(fraction(x) for x in value)


def scalar_cut(adjacency, subset):
    selected = set(subset)
    return sum(adjacency[i][j] for i in range(len(adjacency)) for j in range(i+1, len(adjacency))
               if (i in selected) != (j in selected))


def unpack_mask(mask, n=18):
    if (not isinstance(mask, list) or len(mask) != (n+7)//8
            or any(type(x) is not int or not 0 <= x <= 255 for x in mask)
            or (n % 8 and mask[-1] >> (n % 8))):
        raise InvalidEvidence("Invalid little-endian packed membership")
    return [i for i in range(n) if (mask[i//8] >> (i % 8)) & 1]


def decode(counts, order, mapping):
    rank = {port: position for position, port in enumerate(order)}
    physical = sorted(sorted(range(18), key=lambda i: (-counts[i], rank[i]))[:9])
    return physical, sorted(mapping[i] for i in physical)


def spsa(theta, delta, plus, minus, total):
    lp, lm = Fraction(sum(plus), len(plus)*total), Fraction(sum(minus), len(minus)*total)
    gradient = tuple(2*(lp-lm)*d for d in delta)
    return tuple(t-g/2 for t, g in zip(theta, gradient)), gradient, lp, lm


def metric(audit, value, label):
    audit.require("clock_record", isinstance(value, dict), label)
    for clock in ("wall_seconds", "cpu_seconds"):
        audit.require("clock_finite_nonnegative", finite(value.get(clock)) and value[clock] >= 0, (label, clock))
    return value["wall_seconds"]


def batch_roles(cid, arm, stage, step, sign, trial, draws):
    master = seed(6330000, cid, arm, stage, step, sign, trial)
    result = {"master": master, "observation": seed(master, "observation")}
    for shot in range(draws):
        result["priority/"+str(shot)] = seed(master, "priority", shot)
        if arm == "continuous_phase":
            for role in ("coherent_coefficients", "coherent_multinomial"):
                result[role+"/"+str(shot)] = seed(master, role, shot)
        if arm == "phase_average":
            for role, copies in (("F6_source", 3), ("tritter", 6)):
                for copy in range(copies):
                    result[f"{role}/{shot}/{copy}"] = seed(master, role, shot, copy)
    return result


def namespace_table():
    out = {}
    for cid, _, graph_seed in CASES:
        out[(cid, "graph")] = graph_seed
        out[(cid, "weights")] = seed(graph_seed, "weights")
        out[(cid, "embedding")] = seed(6318000, cid)
        for mode in MODES:
            out[(cid, "FAST", mode)] = seed(6340000, cid, mode)
        for arm in ARMS:
            if arm in ARMS[:3]:
                for step in range(3):
                    out[(cid, arm, "direction", step)] = seed(6320000, cid, arm, step)
                plan = PLAN
            else:
                plan = tuple(("fixed_fresh", 0, "flat", t, 8) for t in range(5))
            for stage, step, sign, trial, draws in plan:
                for role, value in batch_roles(cid, arm, stage, step, sign, trial, draws).items():
                    out[(cid, arm, stage, step, sign, trial, role)] = value
    return out


def rebuild_matrix(theta):
    # Independent tensor-product construction, unlike the producer's four loops.
    f3 = np.exp(2j*math.pi*np.outer(np.arange(3), np.arange(3))/3)/math.sqrt(3)
    f6 = np.exp(2j*math.pi*np.outer(np.arange(6), np.arange(6))/6)/math.sqrt(6)
    phase = np.zeros((3, 6))
    phase[1, 1:], phase[2, 1:] = [float(t) for t in theta[:5]], [float(t) for t in theta[5:]]
    middle = np.diag(np.exp(1j*phase.reshape(18)))
    mixer = np.eye(18)
    mixer[np.ix_([0, 6], [0, 6])] = np.asarray([[3., -4.], [4., 3.]])/5
    return mixer @ np.kron(f3, np.eye(6)) @ middle @ np.kron(np.eye(3), f6)


def matrix_check(audit, row):
    theta = angles(row["theta"])
    stored = row["U"]
    audit.require("U_complex_serialization", isinstance(stored, dict) and set(stored) == {"real", "imag"})
    u = np.asarray(stored["real"], dtype=float)+1j*np.asarray(stored["imag"], dtype=float)
    expected = rebuild_matrix(theta)
    audit.require("U_shape_finite", u.shape == (18, 18) and bool(np.all(np.isfinite(u))))
    audit.check("U_independent_tensor_reconstruction", float(np.max(abs(u-expected))) <= TOL)
    q = abs(u)**2
    analytic = np.full((18, 18), 1/18)
    analytic[0] = np.repeat(np.asarray([1., 37., 37.])/450, 6)
    analytic[6] = np.repeat(np.asarray([49., 13., 13.])/450, 6)
    order = [6*b+(j+1) % 6 for b in range(3) for j in range(6)]
    diagonal = np.exp(2j*math.pi*np.tile(np.arange(6), 3)/6)
    checks = {"row_gram_residual": np.max(abs(u@u.conj().T-np.eye(18))),
              "column_gram_residual": np.max(abs(u.conj().T@u-np.eye(18))),
              "q_residual": np.max(abs(q-analytic)), "row_mass_residual": np.max(abs(q.sum(axis=1)-1)),
              "column_mass_residual": np.max(abs(q.sum(axis=0)-1)),
              "C6_matrix_residual": np.max(abs(u[:, order]-diagonal[:, None]*u))}
    receipt = row["diagnostics"]
    audit.check("U_recorded_q", np.asarray(receipt["q"]).shape == (18, 18)
                and bool(np.all(abs(np.asarray(receipt["q"])-q) <= TOL)))
    for name, residual in checks.items():
        audit.check("U_"+name, residual <= TOL)
        audit.close("recorded_"+name, receipt[name], float(residual), TOL)
    return theta


def safe_path(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise InvalidEvidence("Project-relative path required")
    candidate = root/relative
    if not candidate.is_file() or candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
        raise InvalidEvidence("Bound input is not a regular project file: " + relative)
    return candidate


class BoundInputs:
    def __init__(self, audit, root, binding_path):
        self.audit, self.root = audit, root
        audit.require("binding_size", binding_path.stat().st_size <= 65536)
        binding = json_read(binding_path)
        audit.require("binding_schema", binding.get("schema_version") == 1
                      and binding.get("primary_source_sha256") == SOURCE_SHA
                      and binding.get("primary_source_commit") == SOURCE_COMMIT
                      and binding.get("checker_source_sha256") == sha(Path(__file__)))
        self.binding = binding
        paths = binding["artifacts"]
        audit.require("binding_file_bound", isinstance(paths, list) and 1 <= len(paths) <= 13)
        self.paths, self.hashes = {}, {}
        for row in paths:
            path = safe_path(root, row["path"])
            audit.require("binding_unique", row["path"] not in self.paths)
            audit.require("input_hash_before", sha(path) == row["sha256"], row["path"])
            self.paths[row["path"]], self.hashes[row["path"]] = path, row["sha256"]
        audit.require("input_total_bytes", sum(p.stat().st_size for p in self.paths.values()) <= MAX_INPUT_BYTES)
        self.data = binding["data_directory"].rstrip("/")
        audit.require("binding_data_path", not Path(self.data).is_absolute() and ".." not in Path(self.data).parts)
        self.manifest_path = binding["producer_manifest"]
        audit.require("manifest_bound", self.manifest_path in self.paths)
        allowed = {"raw.jsonl.gz", "seed_namespaces.json", "failure.json", "summary.json"}
        for cid, _, _ in CASES:
            allowed |= {f"context_{cid}.json", f"B_{cid}.json"}
            allowed |= {f"FAST_{cid}_{mode}.json" for mode in MODES}
        data_paths = {key for key in self.paths if key != self.manifest_path}
        audit.require("bound_data_whitelist", all(Path(k).parent.as_posix() == self.data and Path(k).name in allowed for k in data_paths))
        directory = root/self.data
        actual = ({p.relative_to(root).as_posix() for p in directory.iterdir() if p.is_file()}
                  if directory.is_dir() else set())
        audit.require("all_existing_data_bound", actual == data_paths)
        self.all_names = allowed

    def path(self, name):
        return self.paths.get(self.data+"/"+name)

    def read(self, name):
        path = self.path(name)
        if path is None:
            return None
        try:
            return json_read(path)
        except (json.JSONDecodeError, UnicodeError):
            if not getattr(self, "allow_partial", False):
                raise
            self.unreadable.append(name)
            return None

    def unchanged(self):
        for relative, path in self.paths.items():
            self.audit.check("input_hash_after", sha(path) == self.hashes[relative], relative)


def manifest_check(audit, inputs):
    manifest = json_read(inputs.paths[inputs.manifest_path])
    audit.require("producer_v2", manifest.get("schema_version") == 2)
    audit.require("producer_commit_bound", manifest["repository"]["commit"] == inputs.binding["producer_commit"])
    audit.check("producer_claim", manifest["claim_id"] == "P63-B-FAST-STAGE1-DEV-VETO")
    recorded = {row["path"]: row for row in manifest["input_artifacts"]}
    audit.require("producer_closure_exact", len(recorded) == len(manifest["input_artifacts"])
                  and set(recorded) == PRIMARY_CLOSURE
                  and set(manifest["execution_artifacts"]) == PRIMARY_CLOSURE)
    for path, row in recorded.items():
        audit.check("producer_input_unchanged", row["sha256"] == row["sha256_after"], path)
    for path, expected in KNOWN_INPUTS.items():
        audit.check("producer_known_source_hash", recorded[path]["sha256"] == expected, path)
    outputs = {row["path"]: row for row in manifest["outputs"] if row.get("kind") == "result"}
    for path, expected in inputs.hashes.items():
        if path != inputs.manifest_path:
            audit.check("producer_output_hash", path in outputs and outputs[path]["sha256"] == expected, path)
    audit.check("producer_no_positive_contract", "No accepted positive" in " ".join(manifest["mathematics"]["non_claims"]))
    return manifest


def context_check(audit, value, cid, family, graph_seed):
    expected_case = {"id": cid, "family": family, "seed": graph_seed}
    audit.require("context_case", value["case"] == expected_case)
    adjacency = value["adjacency"]
    audit.require("graph_rows", isinstance(adjacency, list) and len(adjacency) == 18)
    for i, row in enumerate(adjacency):
        integers(audit, row, 18, "graph_integer_row")
        audit.require("graph_weight_range", all(0 <= x <= 5 for x in row) and row[i] == 0)
    audit.require("graph_symmetric", all(adjacency[i][j] == adjacency[j][i] for i in range(18) for j in range(18)))
    if family == "RR":
        audit.check("RR_degree6", all(sum(x != 0 for x in row) == 6 for row in adjacency))
    rng = np.random.Generator(np.random.PCG64(seed(graph_seed, "weights")))
    weights = [adjacency[i][j] for i in range(18) for j in range(i+1, 18) if adjacency[i][j]]
    generated_weights = [int(rng.integers(1, 6)) for _ in weights]
    # NetworkX edge orientation/insertion order is not serialized in A.
    # Do not silently replace sorted(graph.edges()) by a canonical i<j order.
    audit.check("weight_PCG64_multiset_only", Counter(weights) == Counter(generated_weights))
    mapping_seed = seed(6318000, cid)
    mapping = np.random.Generator(np.random.PCG64(mapping_seed)).permutation(18).tolist()
    audit.check("mapping_seed", value["mapping_seed"] == mapping_seed)
    audit.check("mapping_PCG64_replay", value["mode_to_vertex"] == mapping)
    metric(audit, value["compiler"], "compiler")
    metric(audit, value["preparation"], "preparation")
    audit.close("compiler_equal_share", value["compiler_share"], value["compiler"]["wall_seconds"]/2)
    return {"context": value, "a": adjacency, "mapping": mapping,
            "total": sum(adjacency[i][j] for i in range(18) for j in range(i+1, 18)),
            "networks": {}, "batches": [], "active": None, "theta": (Fraction(0),)*10,
            "probe": None, "updates": [], "directions_wall": 0., "updates_wall": 0.,
            "batch_wall": 0., "best": None, "completed": 0, "requested": 0, "frozen": False}


def tag_check(audit, row, setup):
    for name in ("case", "arm", "stage", "step", "sign", "trial", "theta", "network_id", "seed_roles"):
        audit.require("batch_tag_"+name, row.get(name) == setup[name])


def raw_audit(audit, inputs, states, primary_completed):
    path = inputs.path("raw.jsonl.gz")
    if path is None and not primary_completed:
        return {"events": {}, "first_failure": None, "truncated": True, "graphs": {}, "global": None}
    audit.require("raw_available", path is not None)
    events, terminal, truncated, graph_records, global_record = Counter(), False, False, {}, None
    first_failure_record = None
    failed_batch_pending = False
    try:
        with gzip.open(path, "rt", encoding="utf8") as stream:
            total_bytes = 0
            for line in iter(lambda: stream.readline(1048577), ""):
                total_bytes += len(line.encode("utf8"))
                audit.require("raw_text_bound", total_bytes <= MAX_RAW_TEXT and len(line) <= 1048576)
                row = json.loads(line, parse_constant=lambda x: (_ for _ in ()).throw(InvalidEvidence("Nonfinite raw JSON")))
                kind = row["record_type"]
                audit.require("no_event_after_first_failure", not terminal)
                audit.require("no_retry_after_failed_batch", not failed_batch_pending or kind == "first_failure")
                events[kind] += 1
                if kind == "first_failure":
                    terminal = True
                    first_failure_record = {key: value for key, value in row.items() if key != "record_type"}
                    continue
                if kind == "B_equal_graph_fresh_mean":
                    audit.require("one_global_mean", global_record is None)
                    global_record = row
                    metric(audit, row["paid_compute"], "global_mean")
                    audit.close("global_mean_cost_share", row["cost_share_per_case"], row["paid_compute"]["wall_seconds"]/2)
                    continue
                cid = row["case"]["id"] if kind == "supplied_graph" else row["case"]
                audit.require("known_raw_case", cid in {x[0] for x in CASES})
                if kind == "supplied_graph":
                    audit.require("one_supplied_graph", cid not in graph_records)
                    graph_records[cid] = row
                    metric(audit, row["excluded_graph_generation"], "graph_generation")
                    if cid in states:
                        audit.check("raw_context_graph", row["adjacency"] == states[cid]["a"]
                                    and row["case"] == states[cid]["context"]["case"])
                    continue
                audit.require("raw_has_context", cid in states and cid in graph_records, cid)
                state = states[cid]
                if kind == "network":
                    network_theta = matrix_check(audit, row)
                    audit.require("network_id_sequential", row["id"] == len(state["networks"]) < 7)
                    audit.require("network_exact_key_unique", network_theta not in state["networks"].values())
                    state["networks"][row["id"]] = network_theta
                elif kind == "paired_probe":
                    step = len(state["updates"])
                    audit.require("probe_order", step < 3 and row["step"] == step and state["active"] is None
                                  and (state["probe"] is None or state["probe"]["step"] < step))
                    theta = angles(row["theta"])
                    direction_seed = seed(6320000, cid, "bosonic", step)
                    delta = (2*np.random.Generator(np.random.PCG64(direction_seed)).integers(0, 2, 10)-1).tolist()
                    audit.require("probe_center", theta == state["theta"])
                    audit.check("direction_seed_and_PCG64", row["direction_seed"] == direction_seed and row["delta"] == delta)
                    audit.check("common_signed_delta", angles(row["plus_theta"]) == tuple(t+Fraction(d, 4) for t, d in zip(theta, delta))
                                and angles(row["minus_theta"]) == tuple(t-Fraction(d, 4) for t, d in zip(theta, delta)))
                    state["probe"] = row
                    state["directions_wall"] += metric(audit, row["direction_compute"], "direction")
                elif kind == "batch_setup":
                    index = len(state["batches"])
                    audit.require("batch_plan_not_exceeded", index < 8 and state["active"] is None)
                    stage, step, sign, trial, draws = PLAN[index]
                    audit.require("batch_plan_order", row["arm"] == "bosonic"
                                  and (row["stage"], row["step"], row["sign"], row["trial"]) == (stage, step, sign, trial))
                    if stage == "training":
                        audit.require("batch_has_probe", state["probe"] is not None and state["probe"]["step"] == step)
                        expected_theta = angles(state["probe"][sign+"_theta"])
                    else:
                        audit.require("fresh_after_final_freeze", state["frozen"])
                        expected_theta = state["theta"]
                    audit.require("batch_exact_theta", angles(row["theta"]) == expected_theta
                                  and state["networks"].get(row["network_id"]) == expected_theta)
                    audit.check("batch_all_seed_roles", row["seed_roles"] == batch_roles(cid, "bosonic", stage, step, sign, trial, draws))
                    setup = metric(audit, row["setup"], "setup")
                    factory = metric(audit, row["factory_total"], "factory")
                    diagnostic = metric(audit, row["matrix_diagnostics"], "matrix_diagnostics")
                    acc = row["accounting"]
                    audit.require("backend_clock_finite", finite(acc["backend_wall"]) and 0 <= acc["backend_wall"] <= factory+TIME_TOL)
                    audit.check("setup_disjoint_clock_bound", factory+diagnostic <= setup+TIME_TOL)
                    audit.close("setup_classical_paid", acc["classical_wall"], max(0., setup-acc["backend_wall"]-diagnostic))
                    audit.close("setup_cpu_recorded", acc["total_setup_cpu"], row["setup"]["cpu_seconds"])
                    audit.close("factory_cpu_recorded", acc["factory_total_cpu"], row["factory_total"]["cpu_seconds"])
                    audit.close("matrix_diag_excluded", acc["diagnostic_wall"], diagnostic)
                    audit.check("CPU_split_unknown", acc["backend_cpu"] is None and acc["classical_cpu"] is None and acc["CPU_split_available"] is False)
                    state["active"] = {"setup": row, "draws": draws, "requested": 0, "cuts": []}
                elif kind in ("shot_requested", "shot", "batch_complete"):
                    active = state["active"]
                    audit.require("event_has_active_batch", active is not None)
                    tag_check(audit, row, active["setup"])
                    if kind == "shot_requested":
                        audit.require("request_sequential_no_retry", row["shot"] == active["requested"] == len(active["cuts"]) < active["draws"])
                        active["requested"] += 1
                        state["requested"] += 1
                    elif kind == "shot":
                        shot = len(active["cuts"])
                        audit.require("shot_matches_one_request", row["shot"] == shot and active["requested"] == shot+1)
                        counts = integers(audit, row["counts"], 18, "complete_integer_counts")
                        audit.require("count_conservation_C6_collisions", all(0 <= x <= 18 for x in counts) and sum(counts) == 18
                                      and sum((i % 6)*x for i, x in enumerate(counts)) % 6 == 0 and max(counts) > 1)
                        order = np.random.Generator(np.random.PCG64(row["seed_roles"][f"priority/{shot}"])).permutation(18).tolist()
                        audit.check("fresh_priority_PCG64_replay", row["priority_order"] == order)
                        physical, subset = decode(counts, order, state["mapping"])
                        cut = scalar_cut(state["a"], subset)
                        audit.check("physical_rank_then_mapping", row["physical_subset"] == physical and row["subset"] == subset)
                        audit.require("exact_actual_cut", type(row["cut"]) is int and row["cut"] == cut)
                        audit.check("count_receipt", row["total_count"] == 18 and row["C6_residue"] == 0 and row["collision"] is True
                                    and row["color_totals"] == [sum(counts[6*a+i] for a in range(3)) for i in range(6)])
                        active["cuts"].append(cut)
                        state["completed"] += 1
                        if state["best"] is None or cut < state["best"]["cut"]:
                            state["best"] = {name: row[name] for name in ("cut", "subset", "physical_subset", "stage", "step", "sign", "trial", "shot")}
                    else:
                        cuts = active["cuts"]
                        audit.require("complete_batch_draws", len(cuts) == active["requested"] == active["draws"] == row["proposals"])
                        audit.check("batch_cuts_and_exact_loss", row["cuts"] == cuts and fraction(row["normalized_mean"]) == Fraction(sum(cuts), len(cuts)*state["total"]))
                        audit.check("batch_setup_duplicate", row["setup"] == active["setup"]["setup"] and row["factory_total"] == active["setup"]["factory_total"]
                                    and row["setup_accounting"] == active["setup"]["accounting"])
                        metric(audit, row["count_generation"], "count_generation")
                        metric(audit, row["physics_diagnostics"], "physics_diagnostics")
                        state["batch_wall"] += (row["setup_accounting"]["classical_wall"]
                                                 + metric(audit, row["postprocessing"], "postprocessing")
                                                 + metric(audit, row["aggregation"], "batch_mean"))
                        state["batches"].append({key: value for key, value in row.items() if key != "record_type"})
                        state["active"] = None
                elif kind == "update":
                    step = len(state["updates"])
                    audit.require("update_after_pair", step < 3 and len(state["batches"]) == 2*(step+1) and state["active"] is None)
                    audit.require("update_identity", row["step"] == step and angles(row["theta_before"]) == state["theta"] and row["delta"] == state["probe"]["delta"])
                    theta, gradient, lp, lm = spsa(state["theta"], row["delta"], state["batches"][-2]["cuts"], state["batches"][-1]["cuts"], state["total"])
                    audit.check("Fraction_SPSA_all_four", angles(row["theta_after"]) == theta and angles(row["gradient"]) == gradient
                                and fraction(row["plus_loss"]) == lp and fraction(row["minus_loss"]) == lm)
                    state["theta"] = theta
                    state["updates_wall"] += metric(audit, row["compute"], "update")
                    state["updates"].append({key: value for key, value in row.items() if key not in ("case", "record_type")})
                elif kind == "frozen_final_theta":
                    audit.require("final_theta_before_fresh", not state["frozen"] and len(state["updates"]) == 3 and len(state["batches"]) == 6)
                    audit.check("final_iterate_only", angles(row["theta"]) == state["theta"] and row["selected_iterate"] == 3
                                and row["frozen_before_fresh"] is True and row["trajectory"] == state["updates"])
                    state["frozen"] = True
                elif kind == "failed_batch":
                    audit.check("failed_batch_partial_cuts", row["completed_cuts"] == (state["active"]["cuts"] if state["active"] else []))
                    failed_batch_pending = True
                else:
                    audit.require("known_raw_record_type", False, kind)
    except (EOFError, OSError, UnicodeError, json.JSONDecodeError) as error:
        truncated = True
        audit.check("completed_raw_closed_and_parseable", not primary_completed, type(error).__name__)
    return {"events": dict(events), "first_failure": first_failure_record, "truncated": truncated,
            "graphs": graph_records, "global": global_record}


def B_check(audit, inputs, states, raw, summary):
    verified, loaded = {}, {}
    for cid, _, _ in CASES:
        value = inputs.read(f"B_{cid}.json")
        if value is None and isinstance(summary, dict):
            candidates = [row for row in summary.get("results", []) if row["case"] == cid]
            if len(candidates) == 1:
                value = dict(candidates[0])
                value["FAST"] = {}
        if value is None:
            continue
        audit.require("B_has_context", cid in states)
        state = states[cid]
        audit.require("B_complete_before_summary", len(state["batches"]) == 8 and state["completed"] == state["requested"] == 40)
        fresh = [cut for row in state["batches"][6:] for cut in row["cuts"]]
        mean = Fraction(sum(fresh), 16*state["total"])
        audit.check("B_case_and_all_paid_minimum", value["case"] == cid and value["B_paid_best_record"] == state["best"]
                    and value["B_paid_best"] == state["best"]["cut"] and value["completed_shots"] == 40)
        audit.check("B_records_updates_final", value["records"] == state["batches"] and value["trajectory"] == state["updates"]
                    and angles(value["theta_final"]) == state["theta"] and value["FAST"] == {})
        audit.check("B_fresh_mean", fraction(value["B_fresh_normalized_mean"]) == mean)
        final_wall = metric(audit, value["final_aggregation"], "B_final_mean")
        global_share = raw["global"]["paid_compute"]["wall_seconds"]/2 if raw["global"] else 0.
        paid = (state["context"]["preparation"]["wall_seconds"]+state["context"]["compiler_share"]
                +state["directions_wall"]+state["updates_wall"]+state["batch_wall"]+final_wall+global_share)
        audit.close("B_own_clock_sum", value["B_classical_wall"], paid)
        if raw["global"] is not None:
            audit.close("B_global_aggregation_share", value["B_global_mean_aggregation_share"], global_share)
        verified[cid] = {"mean": mean, "best": state["best"]["cut"], "paid": paid}
        loaded[cid] = value
    if len(verified) == 2 and raw["global"] is not None:
        audit.check("equal_graph_fresh_mean", fraction(raw["global"]["mean"]) == sum((v["mean"] for v in verified.values()), Fraction(0))/2)
        contexts = [states[cid]["context"] for cid, _, _ in CASES]
        audit.check("same_once_compiler", contexts[0]["compiler"] == contexts[1]["compiler"])
    return verified, loaded


def fast_check(audit, value, cid, mode, state, paid):
    result, trace = value["result"], value["result"]["trace"]
    audit.check("FAST_independent_identity", value["case"] == cid and value["mode"] == mode and value["seed"] == seed(6340000, cid, mode)
                and result["seed"] == value["seed"] and result["initialization"] == mode and result["n"] == 18)
    metric(audit, value["adapter"], "FAST_adapter")
    allowance = max(0., paid-value["adapter"]["cpu_seconds"])
    audit.close("FAST_B_only_WALL_grant", value["B_classical_WALL_allowance"], paid)
    audit.close("FAST_adapter_CPU_subtraction", value["solver_CPU_allowance"], allowance)
    audit.close("FAST_inner_CPU_allowance", result["cpu_budget_seconds"], allowance)
    budget = result["cpu_budget_seconds"]
    audit.require("FAST_recorded_budget_finite", finite(budget) and budget >= 0)
    audit.check("FAST_no_external_features_or_prices", result["free_incumbent_used"] is False and result["external_features_used"] is False
                and result["proposal_cap_is_cost_equivalent"] is False and value["optical_latency_assumed_seconds"] == 0
                and value["serialization_granted_seconds"] == value["other_arm_seconds_granted"] == 0 and value["hardware_time_measured"] is False)
    names = ("cpu_seconds", "wall_seconds", "best_cut", "best_subset_packbits_little", "proposal_count", "stage")
    length = len(trace["cpu_seconds"])
    audit.require("FAST_trace_shapes_and_guard", length <= 10000 and all(len(trace[name]) == length for name in names)
                  and result["max_proposals"] == 10000)
    masks, eligible = [], []
    previous_cpu = previous_wall = previous_work = 0
    previous_cut, anneal_setup = math.inf, 0
    for index in range(length):
        cpu, wall, work, cut = (trace[name][index] for name in ("cpu_seconds", "wall_seconds", "proposal_count", "best_cut"))
        stage = trace["stage"][index]
        audit.require("FAST_trace_clock_work_type", finite(cpu) and finite(wall) and cpu >= previous_cpu and wall >= previous_wall
                      and type(work) is int and previous_work <= work <= 10000 and type(cut) is int)
        subset = unpack_mask(trace["best_subset_packbits_little"][index])
        audit.require("FAST_balanced_recorded_best", len(subset) == 9)
        audit.check("FAST_each_scalar_cut", scalar_cut(state["a"], subset) == cut)
        audit.check("FAST_monotone_best", cut <= previous_cut)
        if index == 0:
            audit.check("FAST_initial_checkpoint", stage == "initialization" and work == 1)
        elif stage == "anneal_setup":
            anneal_setup += 1
            audit.check("FAST_only_zero_work_setup", anneal_setup == 1 and work == previous_work and work >= 82)
        else:
            audit.check("FAST_positive_checkpoint_work", work > previous_work)
        if stage in ("initial_scan", "descent_scan"):
            audit.check("FAST_full_scan_work", work-previous_work == 81)
        audit.check("FAST_known_stage", stage in {"initialization", "initial_scan", "descent_scan", "anneal_setup", "anneal", "uniform_restart", "perturb_best"})
        if cpu <= budget:
            eligible.append(index)
        masks.append(subset)
        previous_cpu, previous_wall, previous_work, previous_cut = cpu, wall, work, cut
    selected = eligible[-1] if eligible else None
    best = trace["best_cut"][selected] if selected is not None else None
    audit.check("FAST_exact_eligible_index", result["eligible_checkpoint_index"] == selected and result["has_eligible_result"] == (selected is not None))
    audit.check("FAST_exact_eligible_cut_subset", result["best_cut"] == best
                and result["best_subset"] == (masks[selected] if selected is not None else None))
    for clock in ("cpu", "wall"):
        expected = trace[clock+"_seconds"][selected] if selected is not None else None
        audit.check("FAST_eligible_"+clock, result["eligible_checkpoint_"+clock+"_seconds"] == expected)
        for field in ("compute_", "online_search_", "finalization_"):
            audit.require("FAST_clock_nonnegative", finite(result[field+clock+"_seconds"]) and result[field+clock+"_seconds"] >= 0)
        audit.close("FAST_clock_export_sum", result["compute_"+clock+"_seconds"], result["online_search_"+clock+"_seconds"]+result["finalization_"+clock+"_seconds"])
        audit.check("FAST_last_checkpoint_before_export", not length or trace[clock+"_seconds"][-1] <= result["online_search_"+clock+"_seconds"]+TIME_TOL)
    scan_indices = [i for i, stage in enumerate(trace["stage"]) if stage == "initial_scan"]
    audit.check("FAST_one_initial_scan", len(scan_indices) <= 1)
    scan_timely = bool(scan_indices and trace["cpu_seconds"][scan_indices[0]] <= budget)
    last_cpu = trace["cpu_seconds"][-1] if length else result["validation_cpu_seconds"]
    early_cap = (result["guard_blocked_full_scan"] or result["stop_reason"] == "max_proposals") and last_cpu < budget
    prefix = selected is not None
    acceptance = prefix and not early_cap and scan_timely
    audit.check("FAST_cap_and_scan_eligibility", result["proposal_count"] == previous_work and result["cap_hit"] == (previous_work >= 10000)
                and result["early_cap_inconclusive"] == early_cap and result["early_wall_inconclusive"] is False
                and result["first_scan_completed_before_deadline"] == scan_timely and result["comparison_acceptance_eligible"] == (prefix and not early_cap))
    audit.check("FAST_caller_prefix_and_gate", value["prefix_eligible_for_veto"] == prefix and value["comparison_acceptance_eligible"] == acceptance
                and value["best_cut"] == best and result["best_snapshot_cached_online"] is True)
    audit.check("FAST_caller_receipt_fields", value["cpu_budget_seconds"] == budget
                and value["eligible_checkpoint_cpu_seconds"] == result["eligible_checkpoint_cpu_seconds"]
                and value["first_scan_completed_before_deadline"] == scan_timely
                and value["early_cap_inconclusive"] == early_cap and value["early_wall_inconclusive"] is False)
    audit.check("FAST_initialization_timely", result["initialization_completed_before_deadline"]
                == bool(length and trace["cpu_seconds"][0] <= budget))
    counters = result["counters"]
    audit.require("FAST_integer_counters", all(type(v) is int and v >= 0 for v in counters.values()))
    scan_count, anneal_work, perturb_work, restarts, perturbations = 0, 0, 0, 0, 0
    for index, stage in enumerate(trace["stage"]):
        change = trace["proposal_count"][index]-(trace["proposal_count"][index-1] if index else 0)
        scan_count += stage in ("initial_scan", "descent_scan")
        anneal_work += change if stage == "anneal" else 0
        perturb_work += change if stage == "perturb_best" else 0
        restarts += stage == "uniform_restart"
        perturbations += stage == "perturb_best"
    audit.check("FAST_recorded_work_counters", counters["input_conversions_and_validations"] == 1
                and counters["initial_cut_scores"] == int(bool(length)) and counters["vectorized_scans"] == scan_count
                and counters["anneal_proposals"] == anneal_work and counters["uniform_restarts"] == restarts
                and counters["full_restart_cut_scores"] == restarts and counters["perturbations"] == perturbations
                and counters["delta_evaluations"] == 81*scan_count+anneal_work+perturb_work
                and previous_work == int(bool(length))+counters["delta_evaluations"]+restarts)
    audit.check("FAST_stop_and_algorithm", result["algorithm"] == "P50_from_raw_descent_first_v1"
                and result["stop_reason"] in {"cpu_deadline", "cpu_deadline_during_validation", "max_proposals", "proposal_guard_before_full_scan"}
                and result["guard_blocked_full_scan"] == (result["stop_reason"] == "proposal_guard_before_full_scan"))
    if length:
        audit.check("FAST_late_audit_snapshot", result["overall_completed_best_cut"] == trace["best_cut"][-1]
                    and result["overall_completed_best_subset"] == masks[-1]
                    and result["initial_cut"] == trace["best_cut"][0] and result["initial_subset"] == masks[0])
    audit.close("FAST_CPU_overrun", result["cpu_overrun_seconds"], max(0., result["compute_cpu_seconds"]-budget))
    return {"prefix": prefix, "acceptance": acceptance, "best": best, "checkpoints": length}


def gate(B, fast):
    complete = len(B) == 2 and set(fast) == {(cid, mode) for cid, _, _ in CASES for mode in MODES}
    vetoes = [mode for mode in MODES if complete and all(fast[cid, mode]["prefix"]
               and fast[cid, mode]["best"] <= B[cid]["best"] for cid, _, _ in CASES)]
    eligible = complete and all(v["acceptance"] for v in fast.values())
    return ("DEV_REJECTED_FIXED_FAST" if vetoes else "INCONCLUSIVE_FAST_ELIGIBILITY" if not eligible
            else "STAGE1_OPTIONAL_CONTROLS_REQUIRED"), vetoes, bool(eligible)


def run_audit(audit, inputs):
    manifest = manifest_check(audit, inputs)
    producer_completed = manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    inputs.allow_partial, inputs.unreadable = not producer_completed, []
    summary, failure_file = inputs.read("summary.json"), inputs.read("failure.json")
    table = inputs.read("seed_namespaces.json")
    if table is not None:
        actual = {tuple(row["role"]): row["seed"] for row in table}
        expected = namespace_table()
        audit.check("all_seven_role_metadata", len(actual) == len(table) and actual == expected and len(set(actual.values())) == len(actual))
    states = {}
    for cid, family, graph_seed in CASES:
        value = inputs.read(f"context_{cid}.json")
        if value is not None:
            states[cid] = context_check(audit, value, cid, family, graph_seed)
            audit.require("positive_weight_total", states[cid]["total"] > 0)
    raw = raw_audit(audit, inputs, states, producer_completed)
    if raw["first_failure"] is not None and failure_file is not None:
        recorded = raw["first_failure"]
        audit.check("first_failure_file_identity", failure_file["stage"] == recorded["stage"]
                    and failure_file["failure"]["error"] == recorded["error"]
                    and failure_file["failure"]["evidence"] == recorded["evidence"])
    B, B_files = B_check(audit, inputs, states, raw, summary)
    fast, checkpoints = {}, 0
    for cid, _, _ in CASES:
        for mode in MODES:
            value = inputs.read(f"FAST_{cid}_{mode}.json")
            if value is not None:
                audit.require("FAST_has_complete_B", cid in B)
                fast[cid, mode] = fast_check(audit, value, cid, mode, states[cid], B[cid]["paid"])
                checkpoints += fast[cid, mode]["checkpoints"]
                if summary is not None and "results" in summary:
                    matching = [row for row in summary["results"] if row["case"] == cid]
                    audit.check("FAST_summary_duplicate", len(matching) == 1 and matching[0]["FAST"].get(mode) == value)
    replayed, vetoes, eligible = gate(B, fast)
    source_complete = (producer_completed and summary is not None and table is not None and failure_file == {"failure": None}
                       and set(Path(path).name for path in inputs.paths if path != inputs.manifest_path) == inputs.all_names
                       and len(B) == 2 and len(fast) == 4 and not raw["first_failure"] and not raw["truncated"])
    if producer_completed:
        audit.require("completed_primary_full_closure", source_complete)
        audit.check("completed_shot_batch_totals", sum(s["completed"] for s in states.values()) == 80
                    and sum(s["requested"] for s in states.values()) == 80 and raw["events"].get("batch_complete") == 16)
    if summary is not None:
        audit.check("summary_positive_always_false", summary["positive_accepted"] is False)
        completed = sum(s["completed"] for s in states.values())
        audit.check("summary_completed_shots", summary["completed_B_shots"] == completed)
        audit.check("summary_raw_digest", summary["raw_sha256"] == inputs.hashes[inputs.data+"/raw.jsonl.gz"])
        if "attempted_B_shots" in summary:
            audit.check("summary_requested_and_photons", summary["attempted_B_shots"] == sum(s["requested"] for s in states.values())
                        and summary["simulated_injected_B_photons"] == 18*summary["attempted_B_shots"])
            audit.check("summary_no_QPU_or_optimum", summary["actual_QPU_calls"] == summary["actual_QPU_photons"] == 0
                        and summary["heldout_opened"] is False and summary["optimum_used"] is False
                        and summary["other_models_executed"] is False and summary["hardware_runtime_measured"] is False
                        and summary["B_CPU_split_available"] is False and summary["diagnostics_and_IO_granted_to_FAST"] is False)
            audit.check("summary_source_hash", summary["source_sha256"] == SOURCE_SHA)
        if source_complete:
            audit.check("fixed_mode_two_graph_gate", summary["status"] == replayed and summary["fixed_FAST_veto_modes"] == vetoes
                        and summary["FAST_all_comparison_eligible"] == eligible and summary["optional_controls_passed"] is False)
            audit.check("optional_models_not_executed", summary["optional_models"] == {arm: "NOT_RUN_DUE_FAST_VETO" if vetoes else "NOT_RUN_STAGE1_SCOPE" for arm in ARMS[1:]})
            audit.check("summary_equal_graph_mean", fraction(summary["B_equal_graph_fresh_normalized_mean"]) == sum((v["mean"] for v in B.values()), Fraction(0))/2)
            native = summary["native_threads"]
            audit.check("native_thread_receipts", native["requested"] == native["configured_before_work"]
                        == native["readback_after_imports"] == native["readback_after_work"] == 1)
            audit.check("summary_case_coverage", len(summary["results"]) == 2 and {v["case"] for v in summary["results"]} == set(B))
            for row in summary["results"]:
                saved = dict(row)
                saved["FAST"] = {}
                audit.check("B_summary_duplicate", saved == B_files[row["case"]])
                audit.close("summary_B_clock", summary["B_paid_classical_wall"][row["case"]], B[row["case"]]["paid"])
                audit.check("summary_online_B_best", summary["B_paid_best_cached_online"][row["case"]] == states[row["case"]]["best"])
                audit.check("summary_graph_generation_excluded", summary["supplied_graph_generation_excluded"][row["case"]]
                            == raw["graphs"][row["case"]]["excluded_graph_generation"])
        else:
            if raw["first_failure"] is not None:
                audit.check("retained_first_failure_summary", summary["status"] == "INCONCLUSIVE_FIRST_FAILURE"
                            and summary["failure"] == raw["first_failure"])
            # A runner kill after summary creation may leave a nominal label.
            # Its unsuccessful manifest overrides that label; no veto is accepted.
    return {"producer_run_status": manifest["run"]["status"], "producer_completed": producer_completed,
            "complete_comparison": source_complete, "raw_events": raw["events"],
            "completed_B_shots": sum(s["completed"] for s in states.values()),
            "requested_B_shots": sum(s["requested"] for s in states.values()), "FAST_checkpoints": checkpoints,
            "primary_summary_status": summary["status"] if summary is not None else None,
            "replayed_stage1_status": replayed if source_complete else "INCONCLUSIVE_PARTIAL_PRIMARY",
            "fixed_FAST_veto_modes": vetoes if source_complete else [],
            "truncated_raw_prefix": raw["truncated"], "unreadable_partial_JSON_files": inputs.unreadable}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--binding", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.output.exists() or not args.output.resolve().is_relative_to(root):
        raise InvalidEvidence("Audit output must be a new file inside the project")
    start, audit, inputs, details, fatal = time.process_time(), Audit(), None, {}, None
    try:
        binding = args.binding.resolve()
        audit.require("binding_inside_project", binding.is_relative_to(root) and not args.binding.is_symlink())
        inputs = BoundInputs(audit, root, binding)
        audit.require("output_does_not_replace_input", args.output.resolve() not in {p.resolve() for p in inputs.paths.values()} | {binding}
                      and not args.output.exists() and args.output.resolve().is_relative_to(root))
        details = run_audit(audit, inputs)
    except Exception as error:
        fatal = f"{type(error).__name__}: {error}"[:500]
        audit.check("fatal_or_unchecked_evidence", False, fatal)
    if inputs is not None:
        try:
            inputs.unchanged()
        except Exception as error:
            audit.check("input_hash_after_unavailable", False, type(error).__name__)
    verified = not audit.failures and details.get("complete_comparison", False)
    status = ("PASS_RECORDED_CONSISTENCY" if verified else "FAIL_RECORDED_CONSISTENCY" if audit.failures
              else "PARTIAL_CONSISTENCY_INCONCLUSIVE")
    report = {"status": status, "checks": dict(audit.checks), "failures": dict(audit.failures),
              "first_failure_examples": audit.examples, "fatal": fatal, **details,
              "complete_comparison_verified": verified,
              "accepted_recorded_fixed_FAST_veto_modes": details.get("fixed_FAST_veto_modes", []) if verified else [],
              "inputs_sha256": inputs.hashes if inputs else {}, "checker_sha256": sha(Path(__file__)),
              "software_observed": {"Python": ".".join(map(str, sys.version_info[:3])), "numpy": np.__version__},
              "CPU_seconds_inside_audit": time.process_time()-start,
              "primary_imports_used": False, "new_bosonic_samples_or_graphs": False, "positive_accepted": False,
              "limitations": ["Recorded-data consistency only; no independent physical sampling or bosonic likelihood verification.",
                  "PCG64 embedding/direction/priority streams and the weight multiset are checked deterministically; native observations are not redrawn.",
                  "Neither NetworkX topology nor edge-order weight assignment is regenerated; only RR degree, weight range and PCG64 weight multiset are checked.",
                  "Recorded timing sums/deadlines are checked; real timing authenticity, online causality and hardware prices are not measured.",
                  "FAST recorded best masks/cuts/prefixes are checked, not unrecorded proposals, deltas, RNG trajectory or optimum.",
                  "Floating matrix identities use absolute3e-12, not interval or relative-tail certification.",
                  "A failed/truncated primary remains an inconclusive checked prefix; accepted recorded veto requires both complete cases and all four FAST calls."]}
    encoded = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if len(encoded.encode("utf8")) > MAX_REPORT:
        raise RuntimeError("Frozen audit output cap exceeded")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf8") as stream:
        stream.write(encoded)
    print(json.dumps({"status": status, "checks": sum(audit.checks.values()), "failure_categories": dict(audit.failures),
                      "complete_comparison_verified": verified, "fatal": fatal}))
    return 1 if audit.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
