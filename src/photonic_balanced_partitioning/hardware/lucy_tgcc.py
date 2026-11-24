"""Explicit single-job Lucy/TGCC adapter; planning never imports a remote client.

The historical offline pilot is unchanged. Real execution uses the CEA's
QuandelaQPU/MyQLMHelper route inside ccc-quantum, not Quandela Cloud credentials.
See docs/LUCY_TGCC.md for acquisition semantics and unverified hardware gates.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import signal
import subprocess
import sys

from . import offline

ROOT = Path(__file__).resolve().parents[3]
FROZEN = ROOT / "qpu/offline_pilot_20261124_v1/run-v1"
PLAN_SCHEMA = "pbp.lucy-plan.v1"
AUTH_SCHEMA = "pbp.lucy-authorization.v1"
MAX_SHOTS = 10_000


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    """Exclusive creation: neither raw captures nor receipts are overwritten."""
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")


def metadata():
    versions = {}
    for name in ("perceval-quandela", "perceval-interop", "qlmaas", "myqlm", "numpy"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    try:
        git = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                             text=True, capture_output=True, check=False, timeout=5)
        commit = git.stdout.strip() if git.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        commit = None
    return {"created_utc": datetime.now(timezone.utc).isoformat(),
            "git_commit": commit,
            "adapter_sha256": sha(__file__), "python": sys.version.split()[0],
            "packages": versions, "credential_values_recorded": False}


def positive(value, label, maximum):
    if type(value) is not int or not 1 <= value <= maximum:
        raise ValueError(f"{label} must be an integer in [1, {maximum}]")
    return value


def create_plan(output, circuit_id="identity", max_shots=1000,
                max_samples=1000, wall_seconds=600):
    positive(max_shots, "max_shots", MAX_SHOTS)
    positive(max_samples, "max_samples", max_shots)
    positive(wall_seconds, "wall_seconds", 3600)
    circuits, circuits_sha = offline.read_bundle(FROZEN / "circuits")
    _, reference_sha = offline.read_bundle(FROZEN / "reference")
    records = [r for r in circuits["circuits"] if r["circuit_id"] == circuit_id]
    if len(records) != 1:
        raise ValueError("Choose identity, hom or pair_mixing")
    plan = {"schema": PLAN_SCHEMA, "target": "Lucy/TGCC",
            "route": "qlmaas.qpus.QuandelaQPU", "command": "sample_count",
            "circuit_id": circuit_id, "circuit": records[0],
            "circuits_artifact_sha256": circuits_sha,
            "reference_artifact_sha256": reference_sha,
            "max_jobs": 1, "max_shots": max_shots, "max_samples": max_samples,
            "wall_seconds": wall_seconds,
            "parameters": {"min_detected_photons": 1,
                           "use_photon_recycling": False, "final_mode_number": 4},
            "shot_unit": "provider nonempty detection event; not an emission attempt",
            "physical_attempts": None, "evidence_kind": "local_plan",
            "network_used": False, "authorization": False}
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "plan.json", plan)
    write_json(output / "provenance.json", metadata())
    return output / "plan.json"


def read_plan(path):
    path = Path(path)
    plan = json.loads(path.read_text())
    circuits, circuits_sha = offline.read_bundle(FROZEN / "circuits")
    _, reference_sha = offline.read_bundle(FROZEN / "reference")
    expected = next((c for c in circuits["circuits"]
                     if c["circuit_id"] == plan.get("circuit_id")), None)
    fixed = {"schema": PLAN_SCHEMA, "target": "Lucy/TGCC",
             "route": "qlmaas.qpus.QuandelaQPU", "command": "sample_count",
             "max_jobs": 1, "circuits_artifact_sha256": circuits_sha,
             "reference_artifact_sha256": reference_sha,
             "parameters": {"min_detected_photons": 1,
                            "use_photon_recycling": False, "final_mode_number": 4},
             "physical_attempts": None, "evidence_kind": "local_plan",
             "network_used": False, "authorization": False}
    if expected is None or offline.canonical(plan.get("circuit")) != offline.canonical(expected):
        raise ValueError("Circuit differs from the sealed n4k2 pilot")
    if any(offline.canonical(plan.get(key)) != offline.canonical(value) for key, value in fixed.items()):
        raise ValueError("Unsupported or modified Lucy acquisition plan")
    positive(plan.get("max_shots"), "max_shots", MAX_SHOTS)
    positive(plan.get("max_samples"), "max_samples", plan["max_shots"])
    positive(plan.get("wall_seconds"), "wall_seconds", 3600)
    return plan


def check_authorization(path, plan_path, plan):
    auth = json.loads(Path(path).read_text())
    if (auth.get("schema") != AUTH_SCHEMA or auth.get("authorized") is not True
            or auth.get("target") != "Lucy/TGCC"
            or auth.get("plan_sha256") != sha(plan_path)
            or type(auth.get("max_jobs")) is not int or auth["max_jobs"] != 1):
        raise ValueError("An explicit authorization for this exact Lucy plan is required")
    for key in ("max_shots", "max_samples"):
        positive(auth.get(key), key, MAX_SHOTS)
        if plan[key] > auth[key]:
            raise ValueError(f"Plan exceeds authorized {key}")
    for key in ("calibration_reviewed", "pnr_confirmed", "routing_reviewed",
                "filtering_and_recycling_reviewed", "no_unreported_output_filtering"):
        if auth.get(key) is not True:
            raise ValueError("Operator confirmation required: " + key)
    for key in ("operator", "approval_reference", "capability_evidence", "expected_provider_name"):
        if not isinstance(auth.get(key), str) or not auth[key].strip() or "REPLACE" in auth[key]:
            raise ValueError("Specify " + key)
    return auth


def load_runtime():
    # This function is never called by environment/plan or without explicit flags.
    import perceval as pcvl
    from perceval_interop import MyQLMHelper
    from qlmaas.qpus import QuandelaQPU
    return pcvl, MyQLMHelper, QuandelaQPU


@contextmanager
def bounded_wait(seconds):
    """Bound this process's wait, not remote hardware execution or cancellation."""
    if not hasattr(signal, "SIGALRM"):
        raise RuntimeError("Use the Unix TGCC environment for bounded execution")
    def expired(signum, frame):
        raise TimeoutError("Local wait expired; inspect the existing TGCC job; do not resubmit")
    old = signal.signal(signal.SIGALRM, expired)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def retrieve_specs(qpu, helper):
    hardware = qpu.get_specs()
    specs = helper.retrieve_specs(hardware)
    return {"specs": specs, "performances": helper.retrieve_perf(hardware),
            "provider_type": helper.retrieve_type(hardware),
            "provider_name": helper.retrieve_name(hardware)
                if callable(getattr(helper, "retrieve_name", None)) else None}


def check_constraints(snapshot, expected_provider_name):
    if str(snapshot["provider_type"]).lower() not in {"qpu", "physical"}:
        raise ValueError("Live provider does not identify a physical QPU")
    if snapshot["provider_name"] != expected_provider_name:
        raise ValueError("Live provider name differs from the explicitly authorized provider")
    constraints = snapshot["specs"]["constraints"]
    for label, value in (("mode", 4), ("photon", 2)):
        lower, upper = (constraints.get(f"{bound}_{label}_count") for bound in ("min", "max"))
        if type(lower) is not int or type(upper) is not int or not lower <= value <= upper:
            raise ValueError(f"Live {label} constraints do not confirm this n4k2 pilot")


def query_specs(output, runtime_factory=load_runtime):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    _, helper, factory = runtime_factory()
    with bounded_wait(60):
        snapshot = retrieve_specs(factory(), helper)
    from perceval.serialization import serialize
    write_json(output / "specs.json", serialize(snapshot))
    write_json(output / "provenance.json", metadata())
    return snapshot


def normalized_counts(decoded, plan, *, evidence_kind):
    """Only number-resolving, unmitigated counts within the declared k<=2 model.

    Unknown emission attempts stay unknown; no lower-sector counts are inferred.
    Unexpected data fail normalization *after* the native result is preserved.
    """
    rows = []
    seen = set()
    for state, count in decoded["results"].items():
        occupation = list(state)
        if (len(occupation) != 4 or any(type(n) is not int or n < 0 for n in occupation)
                or not 1 <= sum(occupation) <= 2
                or type(count) is not int or count < 0
                or tuple(occupation) in seen):
            raise ValueError("Out-of-model counts; preserve and audit native data separately")
        seen.add(tuple(occupation))
        rows.append({"occupation": occupation, "count": count})
    if sum(row["count"] for row in rows) > plan["max_samples"]:
        raise ValueError("Provider returned counts beyond the sample cap")
    return {"schema": "pbp.pnr-counts.v1", "evidence_kind": evidence_kind,
            "reference_artifact_sha256": plan["reference_artifact_sha256"],
            "records": [{"circuit_id": plan["circuit_id"],
                         "input_occupation": [1, 1, 0, 0], "detector": "pnr",
                         "physical_attempts": None, "attempts_source": None,
                         "filtering": {"kind": "min_detected_photons", "minimum": 1,
                                       "discarded_attempts": None},
                         "counts": sorted(rows, key=lambda row: row["occupation"])}]}


def execute(plan_path, authorization, output, *, runtime_factory=load_runtime,
            evidence_kind="hardware_capture_unverified"):
    plan_path = Path(plan_path).resolve()
    plan = read_plan(plan_path)
    auth = check_authorization(authorization, plan_path, plan)
    output = Path(output).resolve()
    # A plan can cause at most one submission, including interrupted/failed calls.
    claim_path = plan_path.parent / "submission-claim.json"
    if claim_path.exists():
        raise FileExistsError("Plan already claimed; inspect that job instead of resubmitting")
    output.mkdir(parents=True, exist_ok=False)
    write_json(output / "request.json", {"plan": plan, "plan_sha256": sha(plan_path),
               "authorization_sha256": sha(authorization), "operator": auth["operator"],
               "approval_reference": auth["approval_reference"], "provenance": metadata()})
    stage = "before_remote_contact"
    try:
        with bounded_wait(plan["wall_seconds"]):
            pcvl, helper, factory = runtime_factory()
            circuit = pcvl.Circuit(4)
            for gate in plan["circuit"]["gates"]:
                if gate["kind"] == "BS_Rx":
                    circuit.add(gate["mode"], pcvl.BS.Rx(theta=gate["theta"]))
                elif gate["kind"] == "PERM":
                    circuit.add(0, pcvl.PERM(gate["permutation"]))
                else:
                    raise ValueError("Unsupported optical gate")
            experiment = pcvl.Experiment(m_circuit=circuit)
            import numpy as np
            error = offline.phase_error(offline.decode_matrix(plan["circuit"]["unitary"]),
                                        np.asarray(circuit.compute_unitary(), dtype=complex))
            if error > 1e-10:
                raise ArithmeticError("Installed Perceval disagrees with sealed circuit unitary")
            experiment.with_input(pcvl.BasicState([1, 1, 0, 0]))
            experiment.min_detected_photons_filter(1)
            job = helper.make_job("sample_count", experiment,
                                  params=dict(plan["parameters"]),
                                  max_shots=plan["max_shots"], max_samples=plan["max_samples"])
            job.dump(str(output / "request.job"))
            stage = "querying_live_specs"
            qpu = factory()
            snapshot = retrieve_specs(qpu, helper)
            from perceval.serialization import serialize
            write_json(output / "live-specs.json", serialize(snapshot))
            check_constraints(snapshot, auth["expected_provider_name"])
            write_json(claim_path, {"plan_sha256": sha(plan_path), "output": str(output),
                                   "created_utc": datetime.now(timezone.utc).isoformat(),
                                   "status": "submission_may_have_occurred_do_not_retry"})
            stage = "submission_may_have_occurred"
            pending = qpu.submit(job)  # The only hardware submission in this adapter.
            if callable(getattr(pending, "get_info", None)):
                try:
                    info = pending.get_info()
                    identifiers = {name: str(getattr(info, name)) for name in ("id", "job_id", "uid")
                                   if getattr(info, name, None) is not None}
                except Exception as error:
                    identifiers = {"status": "unavailable", "exception_type": type(error).__name__}
                write_json(output / "job-identifiers.json", identifiers)
            stage = "waiting_for_existing_job"
            result = pending.join() if callable(getattr(pending, "join", None)) else pending
            # Native unmodified binary result precedes all decoding/analysis.
            result.dump(str(output / "vendor-result.res"))
            write_json(output / "vendor-metadata.json", dict(result.meta_data or {}))
            stage = "native_result_preserved"
            decoded = helper.retrieve_results(result)
            write_json(output / "perceval-result.json", serialize(decoded))
            try:
                counts = normalized_counts(decoded, plan, evidence_kind=(
                    "local_synthetic" if evidence_kind == "local_mock" else "hardware_pnr"))
                write_json(output / "normalized-counts.json", counts)
                normalization = "PASS_under_operator_confirmed_PNR_and_filtering"
            except (KeyError, ValueError, TypeError) as error:
                normalization = "FAIL: " + str(error)
            files = {p.name: sha(p) for p in output.iterdir() if p.is_file()}
            receipt = {"status": "CAPTURED", "evidence_kind": evidence_kind,
                       "normalization": normalization, "files": files,
                       "physical_attempts": None, "physical_success_claim": False,
                       "hardware_compatibility_independently_verified": False}
            write_json(output / "receipt.json", receipt)
            return receipt
    except BaseException as error:
        write_json(output / "interruption.json", {"stage": stage,
                   "exception_type": type(error).__name__, "automatic_retry": False,
                   "instruction": "Inspect existing TGCC job; never infer failure means no submission"})
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("environment", help="Local package versions only; no client import")
    plan = commands.add_parser("plan", help="Seal one fixed circuit without network")
    plan.add_argument("--output", required=True, type=Path)
    plan.add_argument("--circuit", choices=("identity", "hom", "pair_mixing"), default="identity")
    plan.add_argument("--max-shots", type=int, default=1000)
    plan.add_argument("--max-samples", type=int, default=1000)
    plan.add_argument("--wall-seconds", type=int, default=600)
    specs = commands.add_parser("specs", help="Query TGCC specs only; never submit")
    specs.add_argument("--allow-remote-query", required=True, action="store_true")
    specs.add_argument("--output", required=True, type=Path)
    run = commands.add_parser("run", help="One explicitly authorized physical QPU job")
    run.add_argument("--execute-qpu", required=True, action="store_true")
    run.add_argument("--plan", required=True, type=Path)
    run.add_argument("--authorization", required=True, type=Path)
    run.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "environment":
        result = metadata() | {"network_used": False, "hardware_access_verified": False}
    elif args.command == "plan":
        result = {"plan": str(create_plan(args.output, args.circuit, args.max_shots,
                                          args.max_samples, args.wall_seconds)),
                  "network_used": False, "submission": False}
    elif args.command == "specs":
        query_specs(args.output)
        result = {"specs_saved": str(args.output), "submission": False}
    else:
        result = execute(args.plan, args.authorization, args.output)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
