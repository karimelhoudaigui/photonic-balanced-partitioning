"""Offline n=4 pilot. Rows of U are outputs; columns are input modes.

Only trusted, locally generated Perceval circuit strings are deserialized.
The CLI denies socket access and isolates Perceval persistence before import.
No credentials, account APIs, remote processors, or submission code are used.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch

import numpy as np

from ..photonic.fixed_photon_obliq import FixedPhotonObliq

SCHEMA = "pbp.offline.v1"
DEFAULT_CONFIG = {
    "schema": SCHEMA, "n": 4, "k": 2, "seed": 20261124,
    "graphs": ["path", "K4", "K2_2"],
    "circuits": ["identity", "hom", "pair_mixing"],
    "input_occupation": [1, 1, 0, 0], "max_physical_attempts": 1000,
    "detector_required": "pnr", "filtering": {"kind": "none"},
}


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


@contextmanager
def network_denied():
    def deny(*args, **kwargs):
        raise RuntimeError("Network access is forbidden in the offline pilot")
    with patch.object(socket.socket, "connect", deny), \
         patch.object(socket.socket, "connect_ex", deny), \
         patch.object(socket, "create_connection", deny), \
         patch.object(socket, "getaddrinfo", deny):
        yield


_PCVL = None
_PCVL_CACHE = None


def local_perceval():
    global _PCVL, _PCVL_CACHE
    if _PCVL is None:
        # Always override an existing persistent path, without inspecting it.
        # Keep the temporary directory alive while Perceval globals reference it.
        _PCVL_CACHE = tempfile.TemporaryDirectory(prefix="pbp-offline-perceval-")
        with patch.dict(os.environ, {
            "PCVL_PERSISTENT_PATH": _PCVL_CACHE.name,
            "MPLCONFIGDIR": str(Path(_PCVL_CACHE.name) / "matplotlib"),
            "XDG_CACHE_HOME": str(Path(_PCVL_CACHE.name) / "cache"),
        }), network_denied():
            import perceval
            _PCVL = perceval
    return _PCVL


def environment():
    versions = {}
    for name in ("numpy", "scipy", "perceval-quandela", "exqalibur", "pytest"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    expected = {"numpy": "2.4.6", "scipy": "1.17.1", "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
    return {"python": platform.python_version(), "packages": versions,
            "expected_local_packages": expected,
            "pinned_local_versions_match": all(versions[n] == v for n, v in expected.items()),
            "local_simulation_dependencies_present": all(versions[n] for n in
                ("numpy", "scipy", "perceval-quandela", "exqalibur")),
            "credential_inspection": False, "network_used": False,
            "backend_access_verified": False, "remote_ready": False}


def provenance():
    root = Path(__file__).resolve().parents[3]
    def git(*args):
        try:
            p = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                               text=True, check=False, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            return None
        return p.stdout.strip() if p.returncode == 0 else None
    paths = sorted(Path(__file__).parent.glob("*.py")) + [root / "src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py"]
    commit, status = git("rev-parse", "HEAD"), git("status", "--porcelain", "--untracked-files=normal")
    return {"created_utc": datetime.now(timezone.utc).isoformat(),
            "git_commit": commit, "git_dirty": bool(status) if status is not None else None,
            "git_metadata_status": "available" if commit is not None and status is not None else "unavailable",
            "code_sha256": {str(p.relative_to(root)): digest(p.read_bytes()) for p in paths},
            "environment": environment()}


def write_bundle(destination, payload):
    """Create once, never overwrite; manifest authenticates the exact payload bytes.

    A crash leaves a visibly incomplete destination. Resume into a new directory,
    rather than mutating or silently completing an old bundle.
    """
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=False)
    data = canonical(payload) + b"\n"
    (destination / "artifact.json").write_bytes(data)
    manifest = {"schema": SCHEMA, "evidence_kind": "offline_only", "sealed": True,
                "files": {"artifact.json": digest(data)}, "provenance": provenance(),
                "network_used": False, "authorization": False, "credits_consumed": 0}
    (destination / "manifest.json").write_bytes(canonical(manifest) + b"\n")
    return manifest


def read_bundle(path):
    path = Path(path)
    manifest = json.loads((path / "manifest.json").read_text())
    if manifest.get("schema") != SCHEMA or manifest.get("sealed") is not True:
        raise ValueError("Unsupported or incomplete bundle")
    if manifest.get("files", {}).keys() != {"artifact.json"}:
        raise ValueError("Unexpected manifest file set")
    data = (path / "artifact.json").read_bytes()
    if digest(data) != manifest["files"]["artifact.json"]:
        raise ValueError("Bundle hash mismatch")
    return json.loads(data), digest(data)


def config_from(path=None):
    config = json.loads(Path(path).read_text()) if path else dict(DEFAULT_CONFIG)
    if set(config) != set(DEFAULT_CONFIG):
        raise ValueError("Pilot configuration keys must match the documented v1 schema")
    for key in ("n", "k", "seed", "max_physical_attempts"):
        integer(config[key], key, 1 if key != "seed" else 0)
    if (config["n"], config["k"]) != (4, 2):
        raise ValueError("This validated pilot supports only n=4, k=2")
    if (config["input_occupation"] != [1, 1, 0, 0]
            or any(type(x) is not int for x in config["input_occupation"])):
        raise ValueError("Pilot input must be |1,1,0,0>")
    if config["detector_required"] != "pnr" or config["filtering"] != {"kind": "none"}:
        raise ValueError("Pilot preparation requires unfiltered PNR records")
    for key in ("graphs", "circuits"):
        if config[key] != DEFAULT_CONFIG[key]:
            raise ValueError(f"The fixed pilot requires {key}={DEFAULT_CONFIG[key]}")
    return config


def encode_matrix(u):
    return [[[float(z.real), float(z.imag)] for z in row] for row in u]


def decode_matrix(data):
    a = np.asarray(data, dtype=float)
    if a.shape != (4, 4, 2) or not np.all(np.isfinite(a)):
        raise ValueError("Expected finite 4x4 complex-pair matrix")
    return a[..., 0] + 1j * a[..., 1]


def phase_error(expected, actual):
    overlap = np.vdot(expected, actual)
    phase = overlap / abs(overlap) if abs(overlap) else 1
    return float(np.max(np.abs(actual - phase * expected)))


def recipes():
    bs = lambda mode: {"kind": "BS_Rx", "mode": mode, "theta": math.pi / 2}
    swap = {"kind": "PERM", "permutation": [0, 2, 1, 3]}
    return {"identity": [], "hom": [bs(0)],
            "pair_mixing": [swap, bs(0), bs(2), swap]}


def recipe_unitary(gates):
    u = np.eye(4, dtype=complex)
    for gate in gates:
        g = np.eye(4, dtype=complex)
        if gate["kind"] == "BS_Rx":
            i, theta = gate["mode"], gate["theta"]
            c, s = math.cos(theta / 2), 1j * math.sin(theta / 2)
            g[i:i+2, i:i+2] = [[c, s], [s, c]]
        elif gate["kind"] == "PERM":
            g = np.eye(4, dtype=complex)[:, gate["permutation"]]
        else:
            raise ValueError("Unsupported local primitive")
        u = g @ u
    return u


def compile_recipe(gates):
    p = local_perceval()
    c = p.Circuit(4)
    for gate in gates:
        if gate["kind"] == "BS_Rx":
            c.add(gate["mode"], p.BS.Rx(theta=gate["theta"]))
        elif gate["kind"] == "PERM":
            c.add(0, p.PERM(gate["permutation"]))
        else:
            raise ValueError("Unsupported local primitive")
    return c


def generate(config):
    local_perceval()
    from perceval.serialization import serialize
    records = []
    for cid, gates in recipes().items():
        circuit = compile_recipe(gates)
        u = recipe_unitary(gates)
        err = phase_error(u, np.asarray(circuit.compute_unitary(), dtype=complex))
        if err > 1e-10:
            raise ArithmeticError("Local circuit compilation mismatch")
        records.append({"circuit_id": cid, "input_occupation": config["input_occupation"],
                        "gates": gates, "unitary": encode_matrix(u),
                        "perceval_serialized": serialize(circuit),
                        "local_compile_max_error_up_to_global_phase": err})
    graphs = {
        "path": [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
        "K4": [[i, j, 1] for i, j in itertools.combinations(range(4), 2)],
        "K2_2": [[i, j, 1] for i in (0, 1) for j in (2, 3)],
    }
    return {"schema": SCHEMA, "stage": "generate_circuits", "config": config,
            "config_sha256": digest(canonical(config)), "graphs": graphs,
            "circuits": records, "conventions": {
                "unitary": "rows=outputs, columns=inputs; gates left multiply in listed order",
                "BS_Rx": "[[cos(theta/2), i sin(theta/2)], [i sin(theta/2), cos(theta/2)]]",
                "compilation": "local BS/PERM gate construction only; no backend compilation verified",
                "probabilities": "full lossless Fock distribution without filtering or renormalization"}}


def boson_two(u):
    """Independent closed-form two distinct input photon reference."""
    states = FixedPhotonObliq(4, 2)._enumerate_all_fock_states()
    values = []
    for state in states:
        rows = [i for i, count in enumerate(state) for _ in range(count)]
        i, j = rows
        amp = u[i, 0] * u[j, 1] + u[i, 1] * u[j, 0]
        values.append(float(abs(amp) ** 2 / (2 if i == j else 1)))
    return states, values


def distinguishable(u, states):
    probs = {tuple(s): 0. for s in states}
    for i, j in itertools.product(range(4), repeat=2):
        state = tuple(int(a == i) + int(a == j) for a in range(4))
        probs[state] += float(abs(u[i, 0]) ** 2 * abs(u[j, 1]) ** 2)
    return [probs[tuple(s)] for s in states]


def cut(state, edges):
    return float(sum(w for i, j, w in edges if bool(state[i]) != bool(state[j])))


def metrics(states, probs, edges):
    cf = [all(c <= 1 for c in s) and sum(s) == 2 for s in states]
    best = min(cut(s, edges) for s, valid in zip(states, cf) if valid)
    pc = sum(p for p, valid in zip(probs, cf) if valid)
    ps = sum(p for s, p, valid in zip(states, probs, cf) if valid and cut(s, edges) == best)
    return {"optimal_cost": best, "p_cf": pc, "p_collision": 1 - pc,
            "p_success": ps, "p_opt_given_cf": ps / pc if pc > 1e-14 else None,
            "expected_cost_given_cf": sum(p * cut(s, edges) for s, p, valid in
                zip(states, probs, cf) if valid) / pc if pc > 1e-14 else None,
            "expected_ideal_attempts_to_success": 1 / ps if ps > 1e-14 else None}


def simulate(payload):
    p = local_perceval()
    from perceval.serialization import deserialize
    solver = FixedPhotonObliq(4, 2)
    for c in payload["circuits"]:
        u = decode_matrix(c["unitary"])
        states, values = boson_two(u)
        backend = p.SLOSBackend()
        backend.set_circuit(deserialize(c["perceval_serialized"]))
        backend.set_input_state(p.BasicState(c["input_occupation"]))
        reference = backend.prob_distribution()
        slos = [float(reference.get(p.BasicState(s), 0)) for s in states]
        ryser = np.abs(solver.output_state(u)) ** 2
        errors = {"manual_vs_slos": float(np.max(np.abs(np.array(values) - slos))),
                  "manual_vs_ryser": float(np.max(np.abs(np.array(values) - ryser))),
                  "normalization": abs(sum(values) - 1)}
        if max(errors.values()) > 1e-10:
            raise ArithmeticError(f"Reference mismatch: {errors}")
        d = distinguishable(u, states)
        c["reference"] = {"states": states, "bosonic": values, "distinguishable": d,
            "perceval_slos": slos, "validation_errors": errors,
            "full_fock_dimension": len(states),
            "outcomes": [{"occupation": s, "collision_free": max(s) <= 1,
                           "partition": [i for i, n in enumerate(s) if n] if max(s) <= 1 else None,
                           "costs": {g: cut(s, e) if max(s) <= 1 else None for g, e in payload["graphs"].items()}}
                          for s in states],
            "metrics": {g: {"bosonic": metrics(states, values, e),
                            "distinguishable": metrics(states, d, e)}
                        for g, e in payload["graphs"].items()}}
    payload["stage"] = "simulate_reference"
    return payload


def validate_compilation(payload):
    local_perceval()
    from perceval.serialization import deserialize, serialize
    checks = []
    for c in payload["circuits"]:
        target = decode_matrix(c["unitary"])
        built = compile_recipe(c["gates"])
        restored = deserialize(c["perceval_serialized"])
        again = deserialize(serialize(restored))
        errors = {label: phase_error(target, np.asarray(v.compute_unitary(), complex))
                  for label, v in (("gate_recipe", built), ("export", restored), ("roundtrip", again))}
        errors["unitarity"] = float(np.max(np.abs(target.conj().T @ target - np.eye(4))))
        if max(errors.values()) > 1e-10:
            raise ArithmeticError(f"Compilation failed: {errors}")
        checks.append({"circuit_id": c["circuit_id"], "errors": errors, "pass": True})
    payload["local_compilation"] = {"checks": checks, "tolerance": 1e-10,
        "scope": "local gate recipes, full complex U and Perceval serialization up to one global phase",
        "hardware_native_compilation": "UNKNOWN", "remote_ready": False}
    payload["stage"] = "validate_compilation"
    return payload


def validate_physics(config):
    local_perceval()
    payload = simulate(generate(config))
    refs = {c["circuit_id"]: c["reference"] for c in payload["circuits"]}
    expected = {"identity": (1., 1.), "hom": (0., .5), "pair_mixing": (1., 1.)}
    for cid, (b, d) in expected.items():
        values = refs[cid]["metrics"]["path"]
        if abs(values["bosonic"]["p_cf"] - b) > 1e-10 or abs(values["distinguishable"]["p_cf"] - d) > 1e-10:
            raise ArithmeticError("Identity/HOM/pair-mixing invariant failed")
    payload["stage"] = "validate_physics"
    payload["physics_validation"] = {"pass": True, "independent_references":
        ["two-photon closed formula", "project Ryser amplitudes", "Perceval SLOS"],
        "hom_note": "ideal CF=0 for bosons, 1/2 for distinguishable; no hardware calibration inferred"}
    return payload


def prepare_job(payload):
    if "local_compilation" not in payload or any("reference" not in c for c in payload["circuits"]):
        raise ValueError("Prepare requires simulated reference AND validated local compilation")
    attempts = payload["config"]["max_physical_attempts"]
    payload["stage"] = "prepare_qpu_job"
    payload["job"] = {"status": "OFFLINE_DRAFT_NOT_SUBMITTED", "authorization": False,
        "submission_implemented": False, "credits_consumed": 0, "credit_budget_authorized": 0,
        "backend_requested": "qpu:belenos (unverified identifier; no connection)",
        "backend_specs": "UNKNOWN", "backend_access": "UNKNOWN", "calibration": "UNKNOWN",
        "backend_compilation": "UNKNOWN", "detector": "PNR REQUIRED, availability UNKNOWN",
        "request": {"command": "sample_count", "max_physical_attempts_per_circuit": attempts,
                    "total_max_physical_attempts": attempts * len(payload["circuits"]),
                    "filtering": {"kind": "none"}, "photon_recycling": "must be disabled and confirmed",
                    "max_returned_samples": None},
        "remaining_gates": ["explicit QPU authorization and credit limit", "authenticated backend specs",
                            "input routing and primitive/native compilation", "PNR and unfiltered counts contract",
                            "physical attempt denominator and filtering metadata", "calibration and noise model"],
        "results_contract": "docs/LAURENT_HANDOFF.md: pbp.pnr-counts.v1; not a vendor API payload"}
    return payload


def wilson(successes, trials, z=1.959963984540054):
    if trials == 0:
        return None
    p = successes / trials
    den = 1 + z*z/trials
    center = (p + z*z/(2*trials)) / den
    radius = z * math.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / den
    return [0. if successes == 0 else max(0., center-radius),
            1. if successes == trials else min(1., center+radius)]


def estimate(successes, trials):
    return {"successes": successes, "denominator": trials,
            "estimate": successes / trials if trials else None,
            "wilson95": wilson(successes, trials)}


def analyze(payload, raw_path, reference_sha):
    """Read counts only. Never reinterpret returned samples as physical attempts."""
    path = Path(raw_path)
    raw_bytes = path.read_bytes()
    raw = json.loads(raw_bytes)
    if raw.get("schema") != "pbp.pnr-counts.v1" or raw.get("reference_artifact_sha256") != reference_sha:
        raise ValueError("Results schema or reference hash mismatch")
    if raw.get("evidence_kind") not in ("hardware_pnr", "local_synthetic"):
        raise ValueError("Explicit evidence_kind required")
    records = raw.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("At least one count record required")
    circuits = {c["circuit_id"]: c for c in payload["circuits"]}
    reports, seen = [], set()
    for record in records:
        cid = record["circuit_id"]
        if cid in seen or cid not in circuits or record.get("detector") != "pnr":
            raise ValueError("Unknown/duplicate circuit or non-PNR detection")
        seen.add(cid)
        c = circuits[cid]
        if (record.get("input_occupation") != c["input_occupation"]
                or any(type(x) is not int for x in record["input_occupation"])):
            raise ValueError("Input mismatch")
        if not isinstance(record.get("counts"), list):
            raise ValueError("Counts must be an explicit list")
        counts = {}
        for row in record["counts"]:
            s = row["occupation"]
            if not isinstance(s, list) or len(s) != 4:
                raise ValueError("Expected four PNR occupations")
            for x in s:
                integer(x, "occupation")
            if sum(s) > 2:
                raise ValueError("More than two photons: outside pilot model; retain raw data for separate audit")
            s = tuple(s)
            if s in counts:
                raise ValueError("Duplicate count occupation")
            counts[s] = integer(row["count"], "count")
        returned = sum(counts.values())
        filt = record.get("filtering", {})
        kind = filt.get("kind")
        if kind == "none":
            if set(filt) != {"kind", "discarded_attempts"}:
                raise ValueError("Undocumented filtering fields")
            threshold = 0
        elif kind == "min_detected_photons":
            if set(filt) != {"kind", "minimum", "discarded_attempts"}:
                raise ValueError("Undocumented filtering fields")
            threshold = integer(filt.get("minimum"), "filter minimum")
            if threshold > 2 or any(sum(s) < threshold for s in counts):
                raise ValueError("Unsupported/inconsistent photon filter")
        else:
            raise ValueError("Filter must be explicitly none or min_detected_photons")
        if "physical_attempts" not in record or "attempts_source" not in record:
            raise ValueError("Physical attempts and their provenance must be explicitly known or null")
        attempts = record["physical_attempts"]
        discarded = filt.get("discarded_attempts")
        if attempts is not None:
            integer(attempts, "physical_attempts")
            if not isinstance(record.get("attempts_source"), str) or not record["attempts_source"].strip():
                raise ValueError("Known attempts require an explicit provenance source")
            integer(discarded, "discarded_attempts")
            if attempts != returned + discarded or (kind == "none" and discarded != 0):
                raise ValueError("Physical attempts/counts/filter bookkeeping mismatch")
        elif discarded is not None:
            raise ValueError("Discard count cannot be known while physical attempts remain unknown")
        cf_count = sum(n for s, n in counts.items() if sum(s) == 2 and max(s) <= 1)
        collision_count = sum(n for s, n in counts.items() if max(s) > 1)
        report = {"circuit_id": cid, "returned_samples": returned, "physical_attempts": attempts,
                  "filtering": filt, "p_cf_per_physical_attempt": estimate(cf_count, attempts) if attempts is not None else None,
                  "p_cf_given_returned": estimate(cf_count, returned),
                  "p_collision_per_physical_attempt": estimate(collision_count, attempts) if attempts is not None else None,
                  "graphs": {}}
        for gid, edges in payload["graphs"].items():
            best = c["reference"]["metrics"][gid]["bosonic"]["optimal_cost"]
            success = sum(n for s, n in counts.items() if sum(s) == 2 and max(s) <= 1 and cut(s, edges) == best)
            physical = estimate(success, attempts) if attempts is not None else None
            ci = physical["wilson95"] if physical else None
            report["graphs"][gid] = {"optimal_cost": best,
                "success_per_physical_attempt": physical, "optimal_given_cf": estimate(success, cf_count),
                "ideal_reference_success": c["reference"]["metrics"][gid]["bosonic"]["p_success"],
                "attempts_to_first_success_geometric_iid": {
                    "estimate": attempts / success if attempts is not None and success else None,
                    "ci95": [1/ci[1], 1/ci[0] if ci[0] > 0 else None] if ci else None,
                    "upper_unbounded": bool(ci and ci[0] == 0)} if attempts is not None else None}
        # Raw empirical TV only has the physical interpretation when no samples are filtered.
        if kind == "none" and returned:
            states = [s for photons in range(3) for s in FixedPhotonObliq(4, photons)._enumerate_all_fock_states()]
            ref = dict(zip(map(tuple, c["reference"]["states"]), c["reference"]["bosonic"]))
            empirical_tv = .5 * sum(abs(counts.get(tuple(s), 0)/returned - ref.get(tuple(s), 0)) for s in states)
            # Hoeffding+union bound on all S categories; valid conservative TV radius under iid.
            radius = min(1., len(states)/2 * math.sqrt(math.log(2*len(states)/.05)/(2*returned)))
            report["conformity"] = {"reference": "ideal lossless bosons, NOT calibrated hardware",
                "empirical_tv": empirical_tv, "tv_radius95_hoeffding_union": radius,
                "tv_interval95": [max(0., empirical_tv-radius), min(1., empirical_tv+radius)],
                "pointwise_wilson95": [{"occupation": s, **estimate(counts.get(tuple(s), 0), returned),
                    "ideal_probability": ref.get(tuple(s), 0)} for s in states]}
        else:
            report["conformity"] = {"status": "not computed for filtered or empty records"}
        reports.append(report)
    return {"schema": SCHEMA, "stage": "analyze_qpu_results", "raw_sha256": digest(raw_bytes),
            "reference_artifact_sha256": reference_sha, "evidence_kind": raw["evidence_kind"],
            "records": reports, "missing_circuits": sorted(set(circuits)-seen),
            "assumptions": ["Wilson intervals are pointwise, iid Bernoulli; no drift correction",
                            "No physical denominator inferred from postselected samples",
                            "Geometric attempt estimates assume stationary independent attempts",
                            "Null means unknown/undefined; no hardware advantage claim"],
            "raw_modified": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    for name in ("check_environment", "validate_physics", "generate_circuits", "simulate_reference",
                 "validate_compilation", "prepare_qpu_job", "analyze_qpu_results"):
        sub = subs.add_parser(name)
        sub.add_argument("--output", required=True, help="New immutable bundle directory; must not exist")
        if name in ("validate_physics", "generate_circuits"):
            sub.add_argument("--config")
        if name in ("simulate_reference", "validate_compilation", "prepare_qpu_job", "analyze_qpu_results"):
            sub.add_argument("--bundle", required=True, help="Trusted local source bundle")
        if name == "analyze_qpu_results":
            sub.add_argument("--results", required=True, help="Read-only PNR count JSON")
    args = parser.parse_args(argv)
    try:
        if Path(args.output).exists():
            raise FileExistsError("Output already exists; use a new destination")
        with network_denied():
            if args.command == "check_environment":
                payload = {"schema": SCHEMA, "stage": args.command, **environment()}
                if not payload["local_simulation_dependencies_present"] or not payload["pinned_local_versions_match"]:
                    raise RuntimeError("Pinned local simulation dependencies missing or mismatched")
            elif args.command in ("generate_circuits", "validate_physics"):
                config = config_from(args.config)
                local_perceval()
                payload = generate(config) if args.command == "generate_circuits" else validate_physics(config)
            else:
                payload, parent_sha = read_bundle(args.bundle)
                if args.command == "analyze_qpu_results":
                    payload = analyze(payload, args.results, parent_sha)
                else:
                    payload = {"simulate_reference": simulate, "validate_compilation": validate_compilation,
                               "prepare_qpu_job": prepare_job}[args.command](payload)
                payload["parent_artifact_sha256"] = parent_sha
            manifest = write_bundle(args.output, payload)
        print(json.dumps({"status": "OFFLINE_ONLY", "bundle": str(Path(args.output).resolve()),
                          "artifact_sha256": manifest["files"]["artifact.json"], "credits_consumed": 0}))
        return 0
    except (ValueError, OSError, RuntimeError, ArithmeticError, KeyError, TypeError) as exc:
        print(f"Offline pilot failed: {exc}", file=sys.stderr)
        return 2
