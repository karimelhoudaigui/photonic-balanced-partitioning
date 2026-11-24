"""Lucy boundaries with real local Perceval payloads and a fake remote transport.

No test constructs a QLMaas client or sends a job. Fake captures are explicitly
local_mock/local_synthetic, including tests of interruption and raw preservation.
"""
import copy
import json
from pathlib import Path
import socket
from types import SimpleNamespace

import pytest

from photonic_balanced_partitioning.hardware import lucy_tgcc as lucy
from photonic_balanced_partitioning.hardware import offline


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def deny(*args, **kwargs):
        pytest.fail("Lucy unit test attempted a network connection")
    monkeypatch.setattr(socket.socket, "connect", deny)
    monkeypatch.setattr(socket, "create_connection", deny)
    monkeypatch.setattr(socket, "getaddrinfo", deny)


def authorize(plan_path, destination):
    plan = lucy.read_plan(plan_path)
    auth = {"schema": lucy.AUTH_SCHEMA, "authorized": True, "target": "Lucy/TGCC",
            "plan_sha256": lucy.sha(plan_path), "max_jobs": 1,
            "max_shots": plan["max_shots"], "max_samples": plan["max_samples"],
            "calibration_reviewed": True, "pnr_confirmed": True,
            "routing_reviewed": True, "filtering_and_recycling_reviewed": True,
            "no_unreported_output_filtering": True,
            "expected_provider_name": "UNIT-TEST-LUCY",
            "operator": "UNIT TEST ONLY", "approval_reference": "fake-transport-only",
            "capability_evidence": "synthetic test fixture, no hardware capabilities asserted"}
    lucy.write_json(destination, auth)
    return destination


def test_planning_without_remote_dependencies_and_no_overwrite(tmp_path, monkeypatch):
    monkeypatch.setattr(lucy, "load_runtime", lambda: pytest.fail("remote import during planning"))
    path = lucy.create_plan(tmp_path / "plan")
    plan = lucy.read_plan(path)
    assert plan["authorization"] is False and plan["physical_attempts"] is None
    assert plan["parameters"]["use_photon_recycling"] is False
    with pytest.raises(FileExistsError):
        lucy.create_plan(path.parent)


@pytest.mark.parametrize("kwargs", [dict(max_shots=0), dict(max_shots=10_001),
    dict(max_samples=1001), dict(wall_seconds=3601), dict(max_shots=True)])
def test_budget_rejected_before_files_or_clients(tmp_path, kwargs):
    with pytest.raises(ValueError):
        lucy.create_plan(tmp_path / "bad", **kwargs)
    assert not list(tmp_path.iterdir())


def test_tampering_and_missing_authorization_never_load_runtime(tmp_path):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    plan = json.loads(path.read_text())
    plan["parameters"]["use_photon_recycling"] = True
    path.write_text(json.dumps(plan))
    with pytest.raises(ValueError):
        lucy.execute(path, auth, tmp_path / "capture",
                     runtime_factory=lambda: pytest.fail("unauthorized client import"))
    assert not (tmp_path / "capture").exists()


@pytest.mark.parametrize("change", [{"authorized": False}, {"pnr_confirmed": False},
    {"plan_sha256": "wrong"}, {"max_shots": 10}, {"max_jobs": True},
    {"no_unreported_output_filtering": False}])
def test_authorization_is_exact_plan_and_operator_scoped(tmp_path, change):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    data = json.loads(auth.read_text()) | change
    auth.write_text(json.dumps(data))
    with pytest.raises(ValueError):
        lucy.execute(path, auth, tmp_path / "capture",
                     runtime_factory=lambda: pytest.fail("unauthorized client import"))
    assert not (tmp_path / "capture").exists()


def mock_runtime(*, fail_submit=False, anomalous=False, incompatible=False):
    pcvl = offline.local_perceval()
    state = pcvl.BasicState([3, 0, 0, 0] if anomalous else [1, 1, 0, 0])
    data = {"results": pcvl.BSCount({state: 4}), "physical_perf": .0004}
    calls = []

    class Job:
        def dump(self, path):
            Path(path).write_bytes(b"SYNTHETIC-REQUEST-NOT-A-QPU-JOB")

    class Result:
        meta_data = {"fixture": "SYNTHETIC-NATIVE-RESULT-NOT-HARDWARE"}
        def dump(self, path):
            Path(path).write_bytes(b"SYNTHETIC-NATIVE-RESULT-NOT-HARDWARE")

    class Helper:
        @staticmethod
        def make_job(command, experiment, **kwargs):
            # Use the actual pinned Perceval serializer: validate parameter placement.
            payload = pcvl.PayloadGenerator.generate_payload(command, experiment, **kwargs)
            calls.append(("payload", payload))
            return Job()
        @staticmethod
        def retrieve_specs(hw):
            return {"constraints": {"min_mode_count": 1, "max_mode_count": 2 if incompatible else 24,
                    "min_photon_count": 1, "max_photon_count": 12}}
        @staticmethod
        def retrieve_perf(hw):
            return {"fixture": "no physical calibration"}
        @staticmethod
        def retrieve_type(hw):
            return "physical"
        @staticmethod
        def retrieve_name(hw):
            return "UNIT-TEST-LUCY"
        @staticmethod
        def retrieve_results(result):
            return data

    class QPU:
        def get_specs(self):
            calls.append(("specs", None))
            return None
        def submit(self, job):
            calls.append(("submit", None))
            if fail_submit:
                raise ConnectionError("synthetic interruption after possibly accepting job")
            return SimpleNamespace(join=lambda: Result(),
                get_info=lambda: SimpleNamespace(id="UNIT-TEST-JOB-NOT-REAL"))

    return lambda: (pcvl, Helper, QPU), calls


@pytest.mark.parametrize("circuit", ["identity", "hom", "pair_mixing"])
def test_fake_capture_uses_real_payload_and_preserves_unknown_attempts(tmp_path, circuit):
    path = lucy.create_plan(tmp_path / "plan", circuit_id=circuit)
    auth = authorize(path, tmp_path / "auth.json")
    runtime, calls = mock_runtime()
    out = tmp_path / "capture"
    receipt = lucy.execute(path, auth, out, runtime_factory=runtime, evidence_kind="local_mock")
    assert receipt["evidence_kind"] == "local_mock"
    assert receipt["physical_success_claim"] is False
    payload = next(value for key, value in calls if key == "payload")["payload"]
    assert payload["parameters"]["use_photon_recycling"] is False
    assert payload["parameters"]["min_detected_photons"] == 1
    assert payload["max_shots"] == payload["max_samples"] == 1000
    assert len([c for c in calls if c[0] == "submit"]) == 1
    counts = json.loads((out / "normalized-counts.json").read_text())
    assert counts["evidence_kind"] == "local_synthetic"
    record = counts["records"][0]
    assert record["physical_attempts"] is record["attempts_source"] is None
    # The fake provider's physical_perf is deliberately not an emission counter.
    reference, reference_sha = offline.read_bundle(lucy.FROZEN / "reference")
    report = offline.analyze(copy.deepcopy(reference), out / "normalized-counts.json", reference_sha)
    assert report["records"][0]["p_cf_per_physical_attempt"] is None
    assert (out / "vendor-result.res").read_bytes() == b"SYNTHETIC-NATIVE-RESULT-NOT-HARDWARE"
    assert all(lucy.sha(out / name) == digest for name, digest in receipt["files"].items())
    with pytest.raises(FileExistsError, match="already claimed"):
        lucy.execute(path, auth, tmp_path / "second", runtime_factory=runtime)
    assert not (tmp_path / "second").exists()


def test_ambiguous_submit_failure_cannot_repeat_a_job(tmp_path):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    runtime, calls = mock_runtime(fail_submit=True)
    with pytest.raises(ConnectionError):
        lucy.execute(path, auth, tmp_path / "failed", runtime_factory=runtime, evidence_kind="local_mock")
    failure = json.loads((tmp_path / "failed/interruption.json").read_text())
    assert failure["stage"] == "submission_may_have_occurred"
    assert failure["automatic_retry"] is False
    with pytest.raises(FileExistsError):
        lucy.execute(path, auth, tmp_path / "repeat", runtime_factory=runtime)
    assert sum(key == "submit" for key, _ in calls) == 1


def test_out_of_model_data_preserves_native_result_without_normalization(tmp_path):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    runtime, _ = mock_runtime(anomalous=True)
    out = tmp_path / "anomalous"
    receipt = lucy.execute(path, auth, out, runtime_factory=runtime, evidence_kind="local_mock")
    assert receipt["normalization"].startswith("FAIL")
    assert (out / "vendor-result.res").exists() and (out / "perceval-result.json").exists()
    assert not (out / "normalized-counts.json").exists()


def test_live_constraints_prevent_submission(tmp_path):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    runtime, calls = mock_runtime(incompatible=True)
    with pytest.raises(ValueError, match="constraints"):
        lucy.execute(path, auth, tmp_path / "capture", runtime_factory=runtime, evidence_kind="local_mock")
    assert not any(key == "submit" for key, _ in calls)
    assert not (path.parent / "submission-claim.json").exists()


def test_cli_run_cannot_omit_explicit_execution_flag(tmp_path):
    with pytest.raises(SystemExit) as error:
        lucy.main(["run", "--plan", "missing", "--authorization", "missing", "--output", str(tmp_path)])
    assert error.value.code == 2


def test_provider_identity_must_match_operator_authorization(tmp_path):
    path = lucy.create_plan(tmp_path / "plan")
    auth = authorize(path, tmp_path / "auth.json")
    values = json.loads(auth.read_text()) | {"expected_provider_name": "DIFFERENT-PROVIDER"}
    auth.write_text(json.dumps(values))
    runtime, calls = mock_runtime()
    with pytest.raises(ValueError, match="provider name"):
        lucy.execute(path, auth, tmp_path / "capture", runtime_factory=runtime, evidence_kind="local_mock")
    assert not any(key == "submit" for key, _ in calls)
