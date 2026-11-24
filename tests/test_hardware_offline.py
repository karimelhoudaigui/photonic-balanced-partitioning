"""Independent n=4 checks, network denied, no account or QPU dependencies."""
import copy
import hashlib
import json
import math
from pathlib import Path
import socket

import numpy as np
import pytest

from photonic_balanced_partitioning.hardware import offline as h


@pytest.fixture(autouse=True)
def forbid_network(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("Offline pilot attempted network access")
    monkeypatch.setattr(socket.socket, "connect", forbidden)
    monkeypatch.setattr(socket, "create_connection", forbidden)
    monkeypatch.setattr(socket, "getaddrinfo", forbidden)


@pytest.fixture(scope="module")
def simulated():
    # No RemoteProcessor, RemoteConfig or provider session is instantiated.
    h.local_perceval()
    return h.simulate(h.generate(h.config_from()))


def raw_record(cid="identity", attempts=100, filtering=None, counts=None):
    return {"circuit_id": cid, "input_occupation": [1, 1, 0, 0], "detector": "pnr",
            "physical_attempts": attempts, "attempts_source": "synthetic fixed trigger counter",
            "filtering": filtering or {"kind": "none", "discarded_attempts": 0 if attempts is not None else None},
            "counts": counts or [{"occupation": [1, 1, 0, 0], "count": 100}]}


def analyze(tmp_path, simulated, record):
    path = tmp_path / "raw.json"
    path.write_text(json.dumps({"schema": "pbp.pnr-counts.v1", "evidence_kind": "local_synthetic",
        "reference_artifact_sha256": "reference", "records": [record]}))
    before = path.read_bytes()
    result = h.analyze(copy.deepcopy(simulated), path, "reference")
    assert path.read_bytes() == before
    return result["records"][0]


def test_local_import_uses_isolated_persistence(monkeypatch):
    # The helper never opens the user's credential store.
    p = h.local_perceval()
    assert p.__version__ == "1.3.0"
    assert h._PCVL_CACHE.name.startswith("/" )
    assert not list(Path(h._PCVL_CACHE.name).glob("**/*token*"))


def test_analytic_hom_and_identity(simulated):
    byid = {c["circuit_id"]: c["reference"] for c in simulated["circuits"]}
    hom = byid["hom"]
    pb = dict(zip(map(tuple, hom["states"]), hom["bosonic"]))
    pd = dict(zip(map(tuple, hom["states"]), hom["distinguishable"]))
    assert len(pb) == 10
    assert pb[(2, 0, 0, 0)] == pytest.approx(.5)
    assert pb[(0, 2, 0, 0)] == pytest.approx(.5)
    assert pb[(1, 1, 0, 0)] == pytest.approx(0, abs=1e-28)
    assert pd[(1, 1, 0, 0)] == pytest.approx(.5)
    identity = byid["identity"]
    assert identity["metrics"]["path"]["bosonic"]["p_success"] == pytest.approx(1)
    assert hom["metrics"]["path"]["bosonic"]["p_opt_given_cf"] is None


def test_pair_mixing_distribution_and_graph_optima(simulated):
    ref = simulated["circuits"][2]["reference"]
    p = dict(zip(map(tuple, ref["states"]), ref["bosonic"]))
    for state in [(1,1,0,0), (1,0,0,1), (0,1,1,0), (0,0,1,1)]:
        assert p[state] == pytest.approx(.25)
    assert ref["bosonic"] == pytest.approx(ref["distinguishable"])
    assert {g: ref["metrics"][g]["bosonic"]["optimal_cost"] for g in ref["metrics"]} == {
        "path": 1, "K4": 4, "K2_2": 2}
    assert ref["metrics"]["K2_2"]["bosonic"]["p_success"] == pytest.approx(.5)


def test_compilation_global_phase_and_export(simulated):
    result = h.validate_compilation(copy.deepcopy(simulated))
    assert all(c["pass"] for c in result["local_compilation"]["checks"])
    u = h.decode_matrix(simulated["circuits"][2]["unitary"])
    assert h.phase_error(u, np.exp(.71j)*u) < 1e-14
    changed = u.copy()
    changed[0] *= -1  # relative output phase is not one common global phase
    assert h.phase_error(u, changed) > .5


def test_prepare_has_no_submit_or_authorization(simulated):
    with pytest.raises(ValueError):
        h.prepare_job(copy.deepcopy(simulated))
    p = h.prepare_job(h.validate_compilation(copy.deepcopy(simulated)))
    assert p["job"]["authorization"] is False
    assert p["job"]["submission_implemented"] is False
    assert p["job"]["credits_consumed"] == 0
    assert p["job"]["request"]["total_max_physical_attempts"] == 3000


def test_immutable_bundle_and_tamper_detection(tmp_path):
    out = tmp_path / "sealed"
    h.write_bundle(out, {"hello": "world"})
    assert h.read_bundle(out)[0] == {"hello": "world"}
    with pytest.raises(FileExistsError):
        h.write_bundle(out, {"overwritten": True})
    (out / "artifact.json").write_text("{}")
    with pytest.raises(ValueError, match="hash mismatch"):
        h.read_bundle(out)


def test_known_physical_counts_wilson_and_raw_unchanged(tmp_path, simulated):
    report = analyze(tmp_path, simulated, raw_record())
    p = report["graphs"]["path"]["success_per_physical_attempt"]
    assert p["estimate"] == 1
    assert p["denominator"] == 100
    assert p["wilson95"][0] == pytest.approx(.9630065017930143)
    assert report["conformity"]["empirical_tv"] == 0


def test_filtered_samples_never_become_attempts(tmp_path, simulated):
    record = raw_record(attempts=None, filtering={"kind": "min_detected_photons", "minimum": 2,
                                                 "discarded_attempts": None})
    report = analyze(tmp_path, simulated, record)
    assert report["physical_attempts"] is None
    assert report["p_cf_per_physical_attempt"] is None
    assert report["graphs"]["path"]["success_per_physical_attempt"] is None
    assert report["graphs"]["path"]["optimal_given_cf"]["estimate"] == 1
    assert "empirical_tv" not in report["conformity"]


def test_filtered_known_attempts_include_discards_as_failures(tmp_path, simulated):
    record = raw_record(attempts=1000, filtering={"kind": "min_detected_photons", "minimum": 2,
                                               "discarded_attempts": 900})
    report = analyze(tmp_path, simulated, record)
    assert report["graphs"]["path"]["success_per_physical_attempt"]["estimate"] == .1
    assert report["p_cf_given_returned"]["estimate"] == 1


@pytest.mark.parametrize("change", [
    {"detector": "threshold"}, {"physical_attempts": 99}, {"attempts_source": ""},
    {"counts": [{"occupation": [1,1,0,0], "count": True}]},
    {"counts": [{"occupation": [3,0,0,0], "count": 1}]},
    {"filtering": {"kind": "unknown"}},
    {"filtering": {"kind": "none", "discarded_attempts": 0, "undocumented_cf_filter": True}},
    {"filtering": {"kind": "min_detected_photons", "minimum": 3, "discarded_attempts": 0}},
    {"counts": [{"occupation": [1,1,0,0], "count": 50}]*2},
])
def test_invalid_count_contract_fails(tmp_path, simulated, change):
    record = raw_record()
    record.update(change)
    with pytest.raises(ValueError):
        analyze(tmp_path, simulated, record)


def test_loss_is_failure_not_cf(tmp_path, simulated):
    record = raw_record(counts=[{"occupation": [1,1,0,0], "count": 20},
                               {"occupation": [1,0,0,0], "count": 30},
                               {"occupation": [0,0,0,0], "count": 50}])
    report = analyze(tmp_path, simulated, record)
    assert report["p_cf_per_physical_attempt"]["estimate"] == .2
    assert report["conformity"]["empirical_tv"] == pytest.approx(.8)


def test_recovery_partial_records_and_empty_counts(tmp_path, simulated):
    record = raw_record(attempts=0, counts=[{"occupation": [1,1,0,0], "count": 0}])
    report = analyze(tmp_path, simulated, record)
    assert report["graphs"]["path"]["optimal_given_cf"]["estimate"] is None
    assert report["graphs"]["path"]["success_per_physical_attempt"]["wilson95"] is None


def test_cli_end_to_end_and_resume_new_destination(tmp_path, capsys):
    def run(command, *args):
        out = tmp_path / command
        assert h.main([command, "--output", str(out), *map(str, args)]) == 0
        return out
    run("check_environment")
    run("validate_physics")
    generated = run("generate_circuits")
    reference = run("simulate_reference", "--bundle", generated)
    compiled = run("validate_compilation", "--bundle", reference)
    job = run("prepare_qpu_job", "--bundle", compiled)
    assert h.read_bundle(job)[0]["job"]["status"] == "OFFLINE_DRAFT_NOT_SUBMITTED"
    raw = tmp_path / "raw.json"
    _, sha = h.read_bundle(reference)
    raw.write_text(json.dumps({"schema": "pbp.pnr-counts.v1", "evidence_kind": "local_synthetic",
                              "reference_artifact_sha256": sha, "records": [raw_record()]}))
    first = run("analyze_qpu_results", "--bundle", reference, "--results", raw)
    original = (first / "artifact.json").read_bytes()
    assert h.main(["analyze_qpu_results", "--bundle", str(reference), "--results", str(raw),
                   "--output", str(first)]) == 2
    assert (first / "artifact.json").read_bytes() == original
    assert h.main(["analyze_qpu_results", "--bundle", str(reference), "--results", str(raw),
                   "--output", str(tmp_path / "analysis-resume")]) == 0


@pytest.mark.parametrize("n,k", [(6,3), (4,1)])
def test_no_unvalidated_dimensions(tmp_path, n, k):
    config = copy.deepcopy(h.DEFAULT_CONFIG)
    config.update(n=n, k=k)
    path = tmp_path / "bad-config.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        h.config_from(path)


def test_network_guard_fails_closed():
    with h.network_denied(), pytest.raises(RuntimeError, match="forbidden"):
        socket.create_connection(("example.invalid", 443))


def test_git_metadata_timeout_is_unknown_not_clean(monkeypatch):
    def timeout(*args, **kwargs):
        raise h.subprocess.TimeoutExpired("git", 5)
    monkeypatch.setattr(h.subprocess, "run", timeout)
    p = h.provenance()
    assert p["git_commit"] is None
    assert p["git_dirty"] is None
    assert p["git_metadata_status"] == "unavailable"
    assert p["code_sha256"]
