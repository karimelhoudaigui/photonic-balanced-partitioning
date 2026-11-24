"""Portable P40 reproduction into a REQUIRED fresh output directory.

This is a new replay, not the historical execution or a new calibration study.
The frozen driver's ancestry/path guards are neither called nor modified.
"""
from __future__ import annotations

import argparse
import datetime
from fractions import Fraction as F
import hashlib
import importlib.metadata
from itertools import product
import json
import math
import os
from pathlib import Path
import platform
import resource
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT/"results/validated/P40_sharpness_pilot_2026-11-24"
ORIGINAL_HASHES = {
    "research/P40_SHARPNESS_PILOT_CONTRACT.md": "30dbbdae5aa2d0c89eb936f7700e5808cde49f215c5118011f10f8fd2e70c4a2",
    "experiments/scripts/validate_sharpness_pilot.py": "2e9dba7c14beafd37901dc1917f59a7354a84dbfa0d45ccdfee09adb4d0c01d0",
    "results/validated/P40_sharpness_pilot_2026-11-24/raw.jsonl": "b3189ac6143c31654d97d06209a94494281b25c43b37c5cd33782014bd277658",
    "results/validated/P40_sharpness_pilot_2026-11-24/circuits.json": "f945154043ff220ca18d105a9528a9a404664a992da107707ab9c0927036e598",
    "results/validated/P40_sharpness_pilot_2026-11-24/summary.json": "852a43b4ff28d855c3822f13e7060e7c773f445b74eb3b4d9d48e6878d285e53",
    "results/validated/P40_sharpness_pilot_2026-11-24/manifest.json": "d29fd7a401d6415e18ddd49cf070bbd7ac3e5f1072182d74abba8b2c5bc68b84",
}
R = (F(0), F(1,20), F(1,10), F(1,5), F(1,3))
ETAS = (F(1), F(9,10), F(1,2))
OVERLAPS = (F(0), F(1,2), F(1))
TOL = 1e-10
OUTPUTS = ("raw.jsonl", "circuits.json", "summary.json")


def _sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def validate_destination(output):
    """Check before physics, source imports or directory creation."""
    path = Path(output).expanduser().resolve()
    if path.exists():
        raise FileExistsError(f"Replay output must be fresh: {path}")
    if "P40_sharpness_pilot_2026-11-24" in path.parts:
        raise ValueError("Replay output cannot be inside historical P40 data")
    for protected in ("experiments", "src", "paper", "research", "docs", "reports", ".git", ".qwen"):
        base = (ROOT/protected).resolve()
        if path == base or base in path.parents:
            raise ValueError(f"Replay output cannot be inside protected source/history: {base}")
    # Existing campaign directories beneath results are historical data.
    # results/ and results/validated/ are containers where a NEW sibling is OK.
    for ancestor in path.parents:
        if ancestor.name == "results":
            containers = {ancestor, ancestor/"validated"}
            for parent in path.parents:
                if ancestor in parent.parents and parent.exists() and parent not in containers:
                    raise ValueError(f"Replay output is below existing historical data: {parent}")
    return path


def authenticate_archive():
    """Identity checks precede reading archived laws; no Git ancestry needed."""
    for relative, expected in ORIGINAL_HASHES.items():
        if _sha(ROOT/relative) != expected:
            raise ValueError(f"Historical P40 source/archive hash mismatch: {relative}")


def _git(*args):
    value = subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True)
    return value.stdout.strip() if value.returncode == 0 else None


def _law(rows):
    return {tuple(row["occupation"]):float(row["probability"]) for row in rows}


def _export(law):
    return [{"occupation":list(t),"probability":float(law[t])} for t in sorted(law)]


def _difference(a,b):
    return max(abs(a.get(t,0)-b.get(t,0)) for t in set(a)|set(b))


def _write(path,value):
    with path.open("x") as stream:
        json.dump(value,stream,indent=2,allow_nan=False);stream.write("\n")


def _wall_timeout(signum,frame):
    raise TimeoutError("Replay exceeded the90-second wall budget")


def _execute_replay(output, archived, archived_circuits):
    """Exactly45 new Gram/loss laws and five local SLOS calculations."""
    import numpy as np
    import perceval as pcvl
    from perceval.serialization import serialize
    from photonic_balanced_partitioning.noise import noisy_distribution

    raw_records, circuits = [], []
    errors = {name:0. for name in ("partial_archive", "distinguishable_archive",
        "metric_archive", "formula", "normalization", "unitarity", "unitary_archive", "slos_archive", "slos_recomputed_ideal")}
    with (output/"raw.jsonl").open("x") as stream:
        for r in R:
            circuit = pcvl.Circuit(4)
            angle = 4*math.atan(float(r))
            for start,gate in [(0,pcvl.BS.Rx(theta=angle)),(0,pcvl.PERM([0,2,1,3])),
                               (0,pcvl.BS.Rx(theta=math.pi/2)),(2,pcvl.BS.Rx(theta=math.pi/2))]:
                circuit.add(start,gate)
            u = np.asarray(circuit.compute_unitary(),dtype=complex)
            old = archived_circuits[str(r)]
            old_u = np.array(old["unitary_real"])+1j*np.array(old["unitary_imag"])
            errors["unitarity"] = max(errors["unitarity"],float(np.max(abs(u.conj().T@u-np.eye(4)))))
            errors["unitary_archive"] = max(errors["unitary_archive"],float(np.max(abs(u-old_u))))
            slos = pcvl.SLOSBackend();slos.set_circuit(circuit)
            slos.set_input_state(pcvl.BasicState([1,1,0,0]))
            reference = slos.prob_distribution()
            b_reference = {t:float(reference.get(pcvl.BasicState(t),0)) for t in _law(old["ideal_bosonic_law"])}
            errors["slos_archive"] = max(errors["slos_archive"],_difference(b_reference,_law(old["ideal_bosonic_law"])))
            circuits.append({"r":str(r),"mix_angle":angle,"split_angle":math.pi/2,
                "unitary_real":u.real.tolist(),"unitary_imag":u.imag.tolist(),
                "perceval_serialization":serialize(circuit,compress=False),"slos_ideal_law":_export(b_reference)})
            c,s = (1-r*r)/(1+r*r),2*r/(1+r*r)
            M=2*c*c*s*s
            for eta in ETAS:
                d_control = None
                for x in OVERLAPS:
                    gram = np.array([[1,math.sqrt(float(x))],[math.sqrt(float(x)),1]])
                    new = noisy_distribution(u,[0,1],gram,eta=float(eta))
                    if x==0:d_control=dict(new)
                    cell_id=f"r={r};eta={eta};x={x}"
                    old_cell=archived[cell_id]
                    old_partial,old_d = _law(old_cell["noisy_partial_law"]),_law(old_cell["noisy_distinguishable_law"])
                    actual={"tv_to_same_unitary_distinguishable":math.fsum(abs(new[t]-d_control[t]) for t in new)/2,
                        "collision_probability":math.fsum(p for t,p in new.items() if max(t)>=2),
                        "path_success_probability":new[(1,1,0,0)]+new[(0,0,1,1)]}
                    predicted={"tv_to_same_unitary_distinguishable":eta**2*x*M,
                        "collision_probability":eta**2*(1+x)*M/2,"path_success_probability":eta**2*(1+x)*M/2}
                    comparison={"partial_archive":_difference(new,old_partial),
                        "distinguishable_archive":_difference(d_control,old_d),
                        "metric_archive":max(abs(actual[k]-old_cell["measured"][k]) for k in actual),
                        "formula":max(abs(actual[k]-float(predicted[k])) for k in actual),
                        "normalization":abs(math.fsum(new.values())-1)}
                    for name,value in comparison.items():errors[name]=max(errors[name],value)
                    if eta==1 and x==1:
                        errors["slos_recomputed_ideal"]=max(errors["slos_recomputed_ideal"],_difference(new,b_reference))
                    record={"record_type":"P40_REPLAY","cell_id":cell_id,"r":str(r),"eta":str(eta),"x":str(x),
                        "archive_match":all(v<TOL for v in comparison.values()),"comparison_errors":comparison,
                        "measured":actual,"predictions_exact":{k:str(v) for k,v in predicted.items()},
                        "noisy_partial_law":_export(new),"noisy_distinguishable_law":_export(d_control),
                        "numerical_semantics":new.numerical_semantics}
                    raw_records.append(record);stream.write(json.dumps(record,allow_nan=False)+"\n");stream.flush()
    _write(output/"circuits.json",circuits)
    return raw_records,circuits,errors


def replay(output):
    output=validate_destination(output)
    authenticate_archive()
    for name in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS"):
        os.environ[name]="1"
    os.environ.setdefault("MPLCONFIGDIR","/private/tmp/pasqal-mpl-noise")
    sys.path.insert(0,str(ROOT/"src"))
    resource.setrlimit(resource.RLIMIT_CPU,(60,60))
    prior=signal.signal(signal.SIGALRM,_wall_timeout);signal.setitimer(signal.ITIMER_REAL,90)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();wall=time.monotonic();cpu=time.process_time()
    evidence_root=Path(os.path.commonpath([str(ROOT),str(output)]))
    inputs=[ROOT/name for name in ORIGINAL_HASHES]+[Path(__file__).resolve(),
        ROOT/"src/photonic_balanced_partitioning/noise/__init__.py",ROOT/"src/photonic_balanced_partitioning/noise/physical.py"]
    before={str(p.relative_to(evidence_root)):_sha(p) for p in inputs}
    context={"project_root":str(ROOT),"invocation_cwd":str(Path.cwd()),"worktree_root":_git("rev-parse","--show-toplevel"),
        "commit":_git("rev-parse","HEAD"),"branch":_git("branch","--show-current"),
        "git_common_directory":_git("rev-parse","--git-common-dir"),"dirty":bool(_git("status","--porcelain")),
        "historical_ancestry_required":False,"historical_gitlog_required":False}
    output.mkdir(parents=True,exist_ok=False)
    rows,compiled,errors=[],[],{}
    result,status,exit_status,exception="REPLAY_REJECT","failed",1,None
    try:
        originals=[json.loads(line) for line in (ARCHIVE/"raw.jsonl").read_text().splitlines()]
        indexed={r["cell_id"]:r for r in originals}
        old_circuits={r["r"]:r for r in json.loads((ARCHIVE/"circuits.json").read_text())}
        if len(originals)!=45 or len(indexed)!=45 or len(old_circuits)!=5:
            raise ValueError("Frozen archive population differs from45cells/five circuits")
        rows,compiled,errors=_execute_replay(output,indexed,old_circuits)
        if len(rows)==45 and len(compiled)==5 and all(r["archive_match"] for r in rows) and all(v<TOL for v in errors.values()):
            result,status,exit_status="REPLAY_MATCH","completed",0
    except Exception as exc:
        exception=f"{type(exc).__name__}: {exc}"
        if (output/"raw.jsonl").is_file():
            rows=[json.loads(line) for line in (output/"raw.jsonl").read_text().splitlines()]
        if (output/"circuits.json").is_file():
            compiled=json.loads((output/"circuits.json").read_text())
    finally:
        signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,prior)
    after={str(p.relative_to(evidence_root)):_sha(p) for p in inputs}
    if before!=after:result,status,exit_status="REPLAY_REJECT","inputs-changed",1
    summary={"artifact_type":"P40_REPLAY","result":result,"cells":len(rows),"circuits":len(compiled),
        "matching_cells":sum(r["archive_match"] for r in rows),"maximum_errors":errors,"tolerance":TOL,
        "exception":exception,"original_chronology_reproduced":False,"new_scientific_campaign":False,
        "interpretation":"Reproduction of the frozen P40 model calculation only; no new calibration, discovery, hardware evidence or advantage claim"}
    _write(output/"summary.json",summary)
    software=[{"name":"Python","version":platform.python_version()}]
    for name in ("numpy","scipy","perceval-quandela","exqalibur"):
        try:software.append({"name":name,"version":importlib.metadata.version(name)})
        except importlib.metadata.PackageNotFoundError:pass
    manifest={"schema_version":2,"artifact_type":"P40_REPLAY","claim_id":"P40-portable-reproduction",
        "repository":{"commit":context["commit"],"dirty":context["dirty"]},"repository_context":context,
        "evidence_root":str(evidence_root),"command":[sys.executable,*sys.argv],
        "original_run":{"archive_path":str(ARCHIVE),"authenticated_hashes":ORIGINAL_HASHES,
            "original_contract_commit_reference":"efd1718a6a8b8e8ffac1ad84360566bf4346648a","chronology_reproduced":False},
        "environment":{"software":software,"hardware":platform.platform()+" "+platform.machine(),"thread_environment":{n:os.environ[n] for n in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS")}},
        "mathematics":{"assertion_tested":"Replay the unchanged45cell P40 calibration calculation and five SLOS controls; compare all recomputed complete laws to the authenticated archive",
            "coefficient_domain":"complex float64 with rational fixed parameters","conventions":"Full Fock/loss sectors, halved TV, distinct inputs; original math contract unchanged",
            "inputs":list(before),"bounds":{"m":4,"k":2,"cells":45,"circuits":5,"tolerance":TOL},
            "non_claims":["Not the original execution chronology","No new scientific campaign","No physical calibration or QPU result","No advantage or novelty claim"]},
        "randomness":{"used":False,"generator":"none","seed":None},
        "run":{"started_at":started,"runtime_seconds":time.monotonic()-wall,"cpu_seconds":time.process_time()-cpu,
            "exit_status":exit_status,"status":status,"resource_limits":{"memory_bytes":None,"cpu_seconds":60,"wall_seconds":90,"max_cores":1,"max_threads":1}},
        "outputs":[{"path":str((output/name).relative_to(evidence_root)),"sha256":_sha(output/name),"kind":"result"} for name in OUTPUTS if (output/name).is_file()],
        "declared_results":[str((output/name).relative_to(evidence_root)) for name in OUTPUTS],
        "checks":["Original contract/driver/archive authenticated before reading","Fresh destination checked before physics","45 noise laws and five SLOS controls recomputed","Every full law compared to archived laws","Historical bytes unchanged before/after"],
        "result":result,"residual_risks":["Float64 estimates, not interval certification","Same mathematical/source-model assumptions as original P40","No new independent validation of authored noise code"],
        "input_artifacts":[{"path":name,"sha256":value,"sha256_after":after[name]} for name,value in before.items()]}
    _write(output/"manifest.json",manifest)
    print(json.dumps({"result":result,"cells":len(rows),"circuits":len(compiled),"maximum_errors":errors,
        "cpu_seconds":manifest["run"]["cpu_seconds"],"wall_seconds":manifest["run"]["runtime_seconds"],"output":str(output),"exception":exception},indent=2))
    return exit_status


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True,help="Fresh destination; never inside historical data")
    return replay(parser.parse_args().output)


if __name__=="__main__":raise SystemExit(main())
