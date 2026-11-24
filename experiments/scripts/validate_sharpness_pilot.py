"""Run the frozen P40 pilot once, with immutable new outputs and no QPU.

The 45 noise-module cells are primary calculations. Pair-formula predictions,
five SLOS ideal controls and classical countercontrols remain separate checks.
Imports of Perceval are local; no Processor or remote API is constructed.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import datetime
from fractions import Fraction as F
import hashlib
import importlib.metadata
from itertools import combinations_with_replacement, product
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

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "research/P40_SHARPNESS_PILOT_CONTRACT.md"
CONTRACT_COMMIT = "efd1718a6a8b8e8ffac1ad84360566bf4346648a"
CONTRACT_HASH = "30dbbdae5aa2d0c89eb936f7700e5808cde49f215c5118011f10f8fd2e70c4a2"
DEFAULT_OUTPUT = ROOT / "results/validated/P40_sharpness_pilot_2026-11-24"
R_VALUES = (F(0), F(1, 20), F(1, 10), F(1, 5), F(1, 3))
ETA_VALUES = (F(1), F(9, 10), F(1, 2))
X_VALUES = (F(0), F(1, 2), F(1))
TOLERANCE = 1e-10
OPTIMAL_STATES = ((1, 1, 0, 0), (0, 0, 1, 1))
OUTPUT_NAMES = ("raw.jsonl", "circuits.json", "summary.json")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _write_new(path, value):
    with Path(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def export_law(law):
    return [{"occupation": list(t), "probability": float(law[t])} for t in sorted(law)]


def independent_unitary(r):
    """Analytic propagation product; no Perceval builder used here."""
    import numpy as np
    c, s = float((1-r*r)/(1+r*r)), float(2*r/(1+r*r))
    mix = np.eye(4, dtype=complex)
    mix[:2, :2] = [[c, 1j*s], [1j*s, c]]
    perm = np.eye(4)[[0, 2, 1, 3]]
    split = np.zeros((4, 4), dtype=complex)
    split[:2, :2] = split[2:, 2:] = np.array([[1, 1j], [1j, 1]])/math.sqrt(2)
    return split @ perm @ mix


def pair_formula(u, x, eta):
    """Independent full two-photon formula and its uniform-loss lower sectors."""
    q = abs(u[:, :2])**2
    answer = {(0, 0, 0, 0): (1-eta)**2}
    for i in range(4):
        state = tuple(int(j == i) for j in range(4))
        answer[state] = eta*(1-eta)*float(q[i].sum())
    for i, j in combinations_with_replacement(range(4), 2):
        state = tuple(int(a == i)+int(a == j) for a in range(4))
        if i == j:
            probability = (1+x)*q[i, 0]*q[i, 1]
        else:
            interference = u[i, 0]*u[j, 1]*(u[i, 1]*u[j, 0]).conjugate()
            probability = q[i, 0]*q[j, 1]+q[i, 1]*q[j, 0]+2*x*interference.real
        answer[state] = eta**2*float(probability)
    return answer


def _max_law_error(a, b):
    return max(abs(float(a.get(t, 0))-float(b.get(t, 0))) for t in set(a)|set(b))


def _metrics(law, distinguishable):
    return {
        "tv_to_same_unitary_distinguishable": math.fsum(abs(law.get(t, 0)-distinguishable.get(t, 0)) for t in set(law)|set(distinguishable))/2,
        "collision_probability": math.fsum(p for t, p in law.items() if max(t) >= 2),
        "path_success_probability": math.fsum(law.get(t, 0) for t in OPTIMAL_STATES),
    }


def _timeout(signum, frame):
    raise TimeoutError("P40 wall limit of90 seconds exceeded")


def run_validation(output_dir=DEFAULT_OUTPUT):
    """Refuse existing outputs; save all cells, including failures, exactly once."""
    output_dir = Path(output_dir).resolve()
    if output_dir.exists():
        raise FileExistsError(f"P40 outputs are immutable: {output_dir}")
    if output_dir != DEFAULT_OUTPUT.resolve():
        raise ValueError("Frozen P40 output path may not be changed")
    if sha(CONTRACT) != CONTRACT_HASH:
        raise ValueError("Frozen P40 contract hash changed")
    subprocess.run(["git", "merge-base", "--is-ancestor", CONTRACT_COMMIT, "HEAD"], cwd=ROOT, check=True)
    actual_contract_commit = subprocess.check_output(["git", "log", "-1", "--format=%H", "--", str(CONTRACT.relative_to(ROOT))], cwd=ROOT, text=True).strip()
    if actual_contract_commit != CONTRACT_COMMIT:
        raise ValueError("Contract revision is not the pre-execution frozen commit")
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name] = "1"
    os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/pasqal-mpl-noise")
    resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
    old_alarm = signal.signal(signal.SIGALRM, _timeout)
    signal.setitimer(signal.ITIMER_REAL, 90)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    wall, cpu = time.monotonic(), time.process_time()
    input_paths = [CONTRACT, Path(__file__).resolve(),
        ROOT/"src/photonic_balanced_partitioning/noise/__init__.py",
        ROOT/"src/photonic_balanced_partitioning/noise/physical.py"]
    before = {str(p.relative_to(ROOT)): sha(p) for p in input_paths}
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    output_dir.mkdir(parents=True, exist_ok=False)
    result, manifest_status, exit_status, error = "REJECT", "failed", 1, None
    circuits, records, countercontrols = [], [], []
    errors = defaultdict(float)
    versions = {"Python": platform.python_version()}
    try:
        import numpy as np
        import perceval as pcvl
        from perceval.serialization import serialize, deserialize
        from photonic_balanced_partitioning.noise import (
            apply_independent_loss, noisy_distribution,
            partial_distinguishability_distribution,
        )
        versions.update({name: importlib.metadata.version(name) for name in ("numpy", "scipy", "perceval-quandela", "exqalibur")})
        feasible = {tuple(int(i in pair) for i in range(4)): 1/6 for pair in combinations_with_replacement(range(4), 2) if pair[0] != pair[1]}
        # These controls do not use an optimum-discovery policy.
        for eta in ETA_VALUES:
            uniform = apply_independent_loss(feasible, float(eta))
            identity = noisy_distribution(np.eye(4), [0, 1], eta=float(eta))
            uniform_success = sum(uniform.get(t, 0) for t in OPTIMAL_STATES)
            identity_success = sum(identity.get(t, 0) for t in OPTIMAL_STATES)
            control_error = max(abs(uniform_success-float(eta**2/3)), abs(identity_success-float(eta**2)))
            errors["countercontrol_error"] = max(errors["countercontrol_error"], control_error)
            countercontrols.append({"eta": str(eta), "uniform_feasible_success": uniform_success,
                "uniform_prediction_exact": str(eta**2/3), "uniform_law": export_law(uniform),
                "known_optimum_identity_success": identity_success,
                "identity_prediction_exact": str(eta**2), "identity_law": export_law(identity),
                "maximum_error": control_error})
        with (output_dir/"raw.jsonl").open("x") as raw:
            for r in R_VALUES:
                angle = 4*math.atan(float(r))
                circuit = pcvl.Circuit(4)
                circuit.add(0, pcvl.BS.Rx(theta=angle))
                circuit.add(0, pcvl.PERM([0, 2, 1, 3]))
                circuit.add(0, pcvl.BS.Rx(theta=math.pi/2))
                circuit.add(2, pcvl.BS.Rx(theta=math.pi/2))
                u = np.asarray(circuit.compute_unitary(), dtype=complex)
                native = serialize(circuit, compress=False)
                restored = np.asarray(deserialize(native).compute_unitary(), dtype=complex)
                unitary_error = float(np.max(abs(u.conj().T@u-np.eye(4))))
                build_error = float(np.max(abs(u-independent_unitary(r))))
                roundtrip_error = float(np.max(abs(u-restored)))
                c, s = (1-r*r)/(1+r*r), 2*r/(1+r*r)
                ideal_moment = 2*c*c*s*s
                ideal_b = partial_distinguishability_distribution(u, [0, 1])
                ideal_d = pair_formula(u, 0., 1.)
                ideal_d = {t:p for t,p in ideal_d.items() if sum(t) == 2}
                backend = pcvl.SLOSBackend()
                backend.set_circuit(circuit)
                backend.set_input_state(pcvl.BasicState([1, 1, 0, 0]))
                reference = backend.prob_distribution()
                slos = {t:float(reference.get(pcvl.BasicState(t), 0)) for t in ideal_b}
                slos_error = _max_law_error(ideal_b, slos)
                errors["unitarity_error"] = max(errors["unitarity_error"], unitary_error)
                errors["builder_error"] = max(errors["builder_error"], build_error)
                errors["serialization_roundtrip_error"] = max(errors["serialization_roundtrip_error"], roundtrip_error)
                errors["perceval_bosonic_error"] = max(errors["perceval_bosonic_error"], slos_error)
                errors["perceval_normalization_error"] = max(errors["perceval_normalization_error"], abs(sum(slos.values())-1))
                gates = [{"kind":"BS.Rx","modes":[0,1],"theta":angle},
                    {"kind":"PERM","modes":[0,1,2,3],"permutation":[0,2,1,3]},
                    {"kind":"BS.Rx","modes":[0,1],"theta":math.pi/2},
                    {"kind":"BS.Rx","modes":[2,3],"theta":math.pi/2}]
                circuits.append({"r":str(r),"c_exact":str(c),"s_exact":str(s),
                    "M_ideal_exact":str(ideal_moment),"delta_ideal_exact":str(2*s*s),
                    "angles":{"mix_Rx":angle,"split_Rx":math.pi/2},"input_modes":[0,1],
                    "output_groups":[[0,1],[2,3]],"gate_list":gates,
                    "canonical_gate_serialization":json.dumps(gates,sort_keys=True,separators=(",",":")),
                    "perceval_serialization":native,
                    "unitary_real":u.real.tolist(),"unitary_imag":u.imag.tolist(),
                    "unitarity_error":unitary_error,"independent_builder_error":build_error,
                    "serialization_roundtrip_error":roundtrip_error,
                    "ideal_bosonic_law":export_law(ideal_b),"perceval_slos_law":export_law(slos),
                    "ideal_distinguishable_pair_law":export_law(ideal_d),"perceval_error":slos_error})
                for eta, x in product(ETA_VALUES, X_VALUES):
                    cell = {"cell_id":f"r={r};eta={eta};x={x}","r":str(r),"eta":str(eta),"x":str(x)}
                    try:
                        gram = np.array([[1,math.sqrt(float(x))],[math.sqrt(float(x)),1]],complex)
                        law = noisy_distribution(u, [0,1], gram, eta=float(eta))
                        distinguishable = noisy_distribution(u, [0,1], np.eye(2), eta=float(eta))
                        measured = _metrics(law, distinguishable)
                        expected = {"tv_to_same_unitary_distinguishable":eta**2*x*ideal_moment,
                            "collision_probability":eta**2*(1+x)*ideal_moment/2,
                            "path_success_probability":eta**2*(1+x)*ideal_moment/2}
                        metric_errors = {name:abs(measured[name]-float(prediction)) for name,prediction in expected.items()}
                        pair_error = _max_law_error(law, pair_formula(u,float(x),float(eta)))
                        d_error = _max_law_error(distinguishable, pair_formula(u,0.,float(eta)))
                        normalization_error = max(abs(sum(law.values())-1),abs(sum(distinguishable.values())-1),abs(law.raw_total_probability-1),abs(distinguishable.raw_total_probability-1))
                        error_values = list(metric_errors.values())+[pair_error,d_error,normalization_error,unitary_error,build_error,roundtrip_error,slos_error]
                        passed = all(value < TOLERANCE for value in error_values)
                        for name,value in metric_errors.items():errors[name+"_error"]=max(errors[name+"_error"],value)
                        errors["independent_pair_law_error"]=max(errors["independent_pair_law_error"],pair_error)
                        errors["independent_distinguishable_error"]=max(errors["independent_distinguishable_error"],d_error)
                        errors["normalization_error"]=max(errors["normalization_error"],normalization_error)
                        cell.update({"status":"PASS" if passed else "REJECT","measured":measured,
                            "predictions_exact":{name:str(value) for name,value in expected.items()},
                            "absolute_errors":metric_errors,"full_pair_law_error":pair_error,
                            "full_distinguishable_law_error":d_error,"normalization_error":normalization_error,
                            "noisy_partial_law":export_law(law),"noisy_distinguishable_law":export_law(distinguishable),
                            "sectors":law.sector_probabilities(),"raw_total_probability":law.raw_total_probability,
                            "roundoff_clipped_mass":law.roundoff_clipped_mass,
                            "maximum_imaginary_residual":law.maximum_imaginary_residual,
                            "numerical_semantics":law.numerical_semantics,
                            "uniform_feasible_success":float(eta**2/3),"known_optimum_identity_success":float(eta**2),
                            "same_unitary_success_ratio":measured["path_success_probability"]/sum(distinguishable.get(t,0) for t in OPTIMAL_STATES) if r else None})
                    except Exception as exc:
                        cell.update({"status":"REJECT","error":f"{type(exc).__name__}: {exc}"})
                    records.append(cell)
                    raw.write(json.dumps(cell,allow_nan=False)+"\n");raw.flush()
        _write_new(output_dir/"circuits.json",circuits)
        if len(records)==45 and len(circuits)==5 and all(r["status"]=="PASS" for r in records) and all(e<TOLERANCE for e in errors.values()):
            result,manifest_status,exit_status="PASS","completed",0
    except Exception as exc:
        error=f"{type(exc).__name__}: {exc}"
    finally:
        signal.setitimer(signal.ITIMER_REAL,0)
        signal.signal(signal.SIGALRM,old_alarm)
    after={str(p.relative_to(ROOT)):sha(p) for p in input_paths}
    if after!=before:
        result,manifest_status,exit_status="REJECT","inputs-changed",1
    summary={"result":result,"cells":len(records),"circuits":len(circuits),
        "cell_passes":sum(r["status"]=="PASS" for r in records),"cell_rejections":sum(r["status"]!="PASS" for r in records),
        "tolerance":TOLERANCE,"maximum_errors":dict(errors),"countercontrols":countercontrols,
        "exception":error,"interpretation":"Known-model calibration predictions only; same-U interference is not an algorithmic advantage"}
    _write_new(output_dir/"summary.json",summary)
    output_records=[{"path":str((output_dir/name).relative_to(ROOT)),"sha256":sha(output_dir/name),"kind":"result"} for name in OUTPUT_NAMES if (output_dir/name).is_file()]
    manifest={"schema_version":2,"claim_id":"P40-frozen-sharpness-pilot",
        "repository":{"commit":commit,"dirty":dirty},
        "command":[sys.executable,*sys.argv],"contract_commit":CONTRACT_COMMIT,"contract_sha256":CONTRACT_HASH,
        "environment":{"software":[{"name":k,"version":v} for k,v in versions.items()],"hardware":platform.platform()+" "+platform.machine(),
            "thread_environment":{name:os.environ[name] for name in ("OPENBLAS_NUM_THREADS","OMP_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS")}},
        "mathematics":{"assertion_tested":"Frozen45cell two-photon Gram/loss sharpness predictions; complete laws, five ideal SLOS circuits, independent pair formulas and classical countercontrols",
            "coefficient_domain":"Float64 complex probabilities with exact rational predictions","conventions":"Halved TV; full Fock and all loss sectors; two optimal path occupations; no postselection",
            "inputs":list(before),"bounds":{"m":4,"k":2,"cells":45,"circuits":5,"tolerance":TOLERANCE},
            "non_claims":["No device calibration supplied","No novel theorem","No optimizer or quantum advantage","No QPU execution","No lost-moment application of an ideal fixed-N certificate"]},
        "randomness":{"used":False,"generator":"none","seed":None},
        "run":{"started_at":started,"runtime_seconds":time.monotonic()-wall,"cpu_seconds":time.process_time()-cpu,"exit_status":exit_status,"status":manifest_status,
            "resource_limits":{"memory_bytes":None,"cpu_seconds":60,"wall_seconds":90,"max_cores":1,"max_threads":1}},
        "outputs":output_records,"declared_results":[str((output_dir/name).relative_to(ROOT)) for name in OUTPUT_NAMES],
        "checks":["All45cells retained","Complete law normalization","Unitary builder and serialization roundtrip","SLOS ideal B check","Independent pair D and partial formula","TV/collision/path identities","Uniform feasible and known-optimum countercontrols"],
        "result":result,"residual_risks":["Float64 is not interval arithmetic","Eta and overlap are assumptions, not measured Belenos parameters","PNR/QPU availability unknown"],
        "input_artifacts":[{"path":path,"sha256":value,"sha256_after":after[path]} for path,value in before.items()]}
    _write_new(output_dir/"manifest.json",manifest)
    print(json.dumps({"result":result,"cells":len(records),"circuits":len(circuits),"maximum_errors":dict(errors),"cpu_seconds":manifest["run"]["cpu_seconds"],"wall_seconds":manifest["run"]["runtime_seconds"],"output":str(output_dir),"exception":error},indent=2))
    return exit_status


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir",type=Path,default=DEFAULT_OUTPUT)
    args=parser.parse_args()
    return run_validation(args.output_dir)


if __name__=="__main__":
    raise SystemExit(main())
