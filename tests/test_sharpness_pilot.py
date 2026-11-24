"""Audit P40's frozen exports; these tests do not rerun its 45-cell experiment."""
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
import math
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/"results/validated/P40_sharpness_pilot_2026-11-24"


@pytest.fixture(scope="module")
def exported():
    raw = [json.loads(line) for line in (OUTPUT/"raw.jsonl").read_text().splitlines()]
    circuits = json.loads((OUTPUT/"circuits.json").read_text())
    summary = json.loads((OUTPUT/"summary.json").read_text())
    manifest = json.loads((OUTPUT/"manifest.json").read_text())
    return raw,circuits,summary,manifest


def law(rows):
    return {tuple(row["occupation"]):row["probability"] for row in rows}


def test_contract_precedes_run_and_all_fixed_cells_are_retained(exported):
    raw, circuits, summary, manifest = exported
    assert manifest["contract_commit"] == "efd1718a6a8b8e8ffac1ad84360566bf4346648a"
    contract_hash = hashlib.sha256((ROOT/"research/P40_SHARPNESS_PILOT_CONTRACT.md").read_bytes()).hexdigest()
    assert contract_hash == manifest["contract_sha256"] == "30dbbdae5aa2d0c89eb936f7700e5808cde49f215c5118011f10f8fd2e70c4a2"
    expected = set(product(("0","1/20","1/10","1/5","1/3"),("1","9/10","1/2"),("0","1/2","1")))
    assert len(raw) == 45 and len(circuits) == 5
    assert {(r["r"],r["eta"],r["x"]) for r in raw} == expected
    assert len({r["cell_id"] for r in raw}) == 45
    assert summary["result"] == "PASS" and summary["cell_rejections"] == 0
    assert all(r["status"] == "PASS" for r in raw)


def test_exported_full_laws_and_metric_predictions_independently(exported):
    raw, _, _, _ = exported
    for row in raw:
        r,eta,x = (F(row[name]) for name in ("r","eta","x"))
        c,s = (1-r*r)/(1+r*r),2*r/(1+r*r)
        M = 2*c*c*s*s
        partial,control = law(row["noisy_partial_law"]),law(row["noisy_distinguishable_law"])
        assert len(partial) == len(control) == 15
        assert set(map(sum,partial)) == {0,1,2}
        assert all(value>=0 for value in partial.values())
        assert abs(sum(partial.values())-1)<1e-10
        assert abs(sum(control.values())-1)<1e-10
        assert abs(partial[(0,0,0,0)]-float((1-eta)**2))<1e-10
        for n in (0,1,2):
            assert abs(sum(p for t,p in partial.items() if sum(t)==n)-float(math.comb(2,n)*eta**n*(1-eta)**(2-n)))<1e-10
        observed_tv=sum(abs(partial[t]-control[t]) for t in partial)/2
        collision=sum(p for t,p in partial.items() if max(t)>=2)
        success=partial[(1,1,0,0)]+partial[(0,0,1,1)]
        assert abs(observed_tv-float(eta**2*x*M))<1e-10
        assert abs(collision-float(eta**2*(1+x)*M/2))<1e-10
        assert abs(success-float(eta**2*(1+x)*M/2))<1e-10
        if not r:
            assert row["same_unitary_success_ratio"] is None
        else:
            assert abs(row["same_unitary_success_ratio"]-float(1+x))<1e-10


def test_five_compiled_circuits_angles_and_actual_slos_exports(exported):
    _,circuits,_,_ = exported
    for circuit in circuits:
        r=F(circuit["r"])
        u=np.array(circuit["unitary_real"])+1j*np.array(circuit["unitary_imag"])
        assert u.shape==(4,4)
        assert np.max(abs(u.conj().T@u-np.eye(4)))<1e-10
        assert abs(circuit["angles"]["mix_Rx"]-4*math.atan(float(r)))<1e-15
        assert circuit["gate_list"][1]["permutation"]==[0,2,1,3]
        assert circuit["perceval_serialization"].startswith(":PCVL:")
        assert json.loads(circuit["canonical_gate_serialization"])==circuit["gate_list"]
        computed,reference=law(circuit["ideal_bosonic_law"]),law(circuit["perceval_slos_law"])
        assert len(computed)==len(reference)==10
        assert max(abs(computed[t]-reference[t]) for t in computed)<1e-10


def test_countercontrols_avoid_a_same_unitary_advantage_claim(exported):
    _,_,summary,_ = exported
    assert len(summary["countercontrols"])==3
    for control in summary["countercontrols"]:
        eta=F(control["eta"])
        uniform,identity=law(control["uniform_law"]),law(control["identity_law"])
        good=((1,1,0,0),(0,0,1,1))
        assert abs(sum(uniform.get(t,0) for t in good)-float(eta**2/3))<1e-10
        assert abs(sum(identity.get(t,0) for t in good)-float(eta**2))<1e-10
    assert "not an algorithmic advantage" in summary["interpretation"]


def test_recorded_hashes_and_resource_limits(exported):
    _,_,summary,manifest = exported
    assert manifest["run"]["status"]=="completed" and manifest["run"]["exit_status"]==0
    assert manifest["run"]["cpu_seconds"]<60 and manifest["run"]["runtime_seconds"]<90
    assert manifest["run"]["resource_limits"]["max_threads"]==1
    assert manifest["randomness"]["used"] is False
    assert all(e<1e-10 for e in summary["maximum_errors"].values())
    for artifact in manifest["outputs"]:
        assert hashlib.sha256((ROOT/artifact["path"]).read_bytes()).hexdigest()==artifact["sha256"]
    for artifact in manifest["input_artifacts"]:
        assert artifact["sha256"]==artifact["sha256_after"]
        assert hashlib.sha256((ROOT/artifact["path"]).read_bytes()).hexdigest()==artifact["sha256"]


def test_existing_output_refused_before_any_pilot_execution():
    spec=importlib.util.spec_from_file_location("p40_frozen_pilot",ROOT/"experiments/scripts/validate_sharpness_pilot.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUTPUT.iterdir()}
    with pytest.raises(FileExistsError,match="immutable"):
        module.run_validation()
    assert {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUTPUT.iterdir()}==before
