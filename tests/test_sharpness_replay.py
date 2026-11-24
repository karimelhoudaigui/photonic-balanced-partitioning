"""Read the one real replay and verify its guard without new optical runs."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
REPLAY=ROOT/"results/validated/P40_replay_2026-11-24"
ARCHIVE=ROOT/"results/validated/P40_sharpness_pilot_2026-11-24"


def _law(rows):
    return {tuple(row["occupation"]):row["probability"] for row in rows}


def test_fresh_replay_artifact_matches_archive():
    old={r["cell_id"]:r for r in map(json.loads,(ARCHIVE/"raw.jsonl").read_text().splitlines())}
    new=[json.loads(line) for line in (REPLAY/"raw.jsonl").read_text().splitlines()]
    summary=json.loads((REPLAY/"summary.json").read_text())
    manifest=json.loads((REPLAY/"manifest.json").read_text())
    assert len(new)==len(old)==45 and {r["cell_id"] for r in new}==set(old)
    assert summary["result"]=="REPLAY_MATCH" and summary["matching_cells"]==45
    assert summary["circuits"]==5 and all(e<1e-10 for e in summary["maximum_errors"].values())
    assert manifest["artifact_type"]=="P40_REPLAY"
    assert manifest["run"]["status"]=="completed" and manifest["run"]["exit_status"]==0
    assert manifest["run"]["cpu_seconds"]<60 and manifest["run"]["runtime_seconds"]<90
    assert manifest["repository_context"]["historical_ancestry_required"] is False
    assert manifest["repository_context"]["historical_gitlog_required"] is False
    assert manifest["original_run"]["chronology_reproduced"] is False
    for row in new:
        assert row["record_type"]=="P40_REPLAY" and row["archive_match"]
        for key in ("noisy_partial_law","noisy_distinguishable_law"):
            actual,expected=_law(row[key]),_law(old[row["cell_id"]][key])
            assert set(actual)==set(expected) and len(actual)==15
            assert max(abs(actual[t]-expected[t]) for t in actual)<1e-10
            assert abs(sum(actual.values())-1)<1e-10
    for artifact in manifest["outputs"]:
        assert hashlib.sha256((ROOT/artifact["path"]).read_bytes()).hexdigest()==artifact["sha256"]
    for artifact in manifest["input_artifacts"]:
        assert artifact["sha256"]==artifact["sha256_after"]
        assert hashlib.sha256((ROOT/artifact["path"]).read_bytes()).hexdigest()==artifact["sha256"]
    assert hashlib.sha256((ROOT/"experiments/scripts/validate_sharpness_pilot.py").read_bytes()).hexdigest()=="2e9dba7c14beafd37901dc1917f59a7354a84dbfa0d45ccdfee09adb4d0c01d0"


def test_existing_or_historical_destination_rejected_before_physics(tmp_path,monkeypatch):
    spec=importlib.util.spec_from_file_location("portable_p40_replay",ROOT/"scripts/replay_sharpness_pilot.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    calls=[]
    def forbidden(*args):
        calls.append(True)
        raise AssertionError("Physics must not execute for a rejected destination")
    # Only the NEW worker is instrumented. Historical guards are never imported,
    # patched or called, and historical files are not written.
    monkeypatch.setattr(module,"_execute_replay",forbidden)
    before=set(tmp_path.iterdir())
    with pytest.raises(FileExistsError,match="fresh"):
        module.replay(tmp_path)
    assert set(tmp_path.iterdir())==before and not calls
    forbidden_child=ARCHIVE/"forbidden_replay_child"
    assert not forbidden_child.exists()
    with pytest.raises(ValueError,match="historical"):
        module.replay(forbidden_child)
    assert not forbidden_child.exists() and not calls
