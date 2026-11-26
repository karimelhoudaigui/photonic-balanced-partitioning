"""P96 deterministic finite validation. Import performs no scientific computation."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib
import importlib.metadata as metadata
from itertools import combinations, permutations
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python"
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS")
VERSIONS = {"numpy": "2.4.6", "scipy": "1.17.1", "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
OUTPUT = "research/P96_column_loss_main/run_001/data"
CAP, RESERVE, TOL = 8388608, 131072, 1e-11


def insist(value, message):
    if not value:
        raise AssertionError(message)


def cases():
    """Literal population only; no RNG, native state or outcome-dependent choice."""
    return [("V0", [[]], True, True), ("U1", [["1/2"]], True, True),
            ("H2", [["1/4", "1/4"], ["1/4", "-1/4"]], True, True),
            ("D3", [["1/4", 0, 0], [0, "1/4", 0], [0, 0, "1/4"]], True, False),
            ("R3a", [["1/4"] * 3], True, True), ("R3b", [["1/8"] * 3], True, False),
            ("S3", [["1/8", "1/4", "-1/8"], ["1/4", 0, "1/8"]], True, False),
            ("B4", [["1/4"] * 4, ["1/4"] * 4], True, True),
            ("D4", [["1/4" if i == j else 0 for j in range(4)] for i in range(4)], True, False),
            ("Z4", [[0] * 4, [0] * 4], True, False), ("R4", [["1/4"] * 4], True, False),
            ("C3", [["1/2", 0, 0], [0, "1/2", 0]], True, False),
            ("X4", [["1/2"] * 4], False, False)]


def matrix(rows):
    insist(1 <= len(rows) <= 4 and len(rows[0]) <= 4, "finite matrix dimensions")
    insist(all(len(row) == len(rows[0]) for row in rows), "ragged matrix")
    return [[F(x) for x in row] for row in rows]


def occupations(total, modes):
    insist(total >= 0 and modes >= 1, "occupation domain")
    if modes == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in occupations(total - first, modes - 1):
                yield (first,) + tail


def multiply(left, right):
    out = {}
    for x, a in left.items():
        for y, b in right.items():
            n = tuple(i + j for i, j in zip(x, y))
            out[n] = out.get(n, F(0)) + a * b
    return {n: p for n, p in out.items() if p}


def exact_law(t):
    """Expand per(I + T^t (diag(z)-I) T) by permutations, independently of q."""
    m, k = len(t), len(t[0])
    zero = (0,) * m
    entries = [[{zero: F(int(i == j)) - sum(t[a][i] * t[a][j] for a in range(m))}
                for j in range(k)] for i in range(k)]
    for i in range(k):
        for j in range(k):
            for a in range(m):
                n = tuple(int(b == a) for b in range(m))
                entries[i][j][n] = t[a][i] * t[a][j]
    law = {n: F(0) for total in range(k + 1) for n in occupations(total, m)}
    for permutation in permutations(range(k)):
        term = {zero: F(1)}
        for i, j in enumerate(permutation):
            term = multiply(term, entries[i][j])
        for n, p in term.items():
            law[n] += p
    insist(all(p >= 0 for p in law.values()) and sum(law.values()) == 1, "exact physical raw law")
    return law


def surrogate(t):
    m, k = len(t), len(t[0])
    lam = [sum((x*x for x in row), F(0)) for row in t]
    c = [sum((t[j][i]**2 for j in range(m)), F(0)) for i in range(k)]
    g = [[lam[j]*lam[l] + sum(t[j][i]*t[l][i] for i in range(k))**2
          - 2*sum(t[j][i]**2*t[l][i]**2 for i in range(k)) for l in range(m)] for j in range(m)]
    q = {(0,)*m: 1-sum(c)+sum(map(sum, g))/2}
    for j in range(m):
        if k >= 1:
            q[tuple(int(a == j) for a in range(m))] = lam[j]-sum(g[j])
        if k >= 2:
            q[tuple(2*int(a == j) for a in range(m))] = g[j][j]/2
            for l in range(j+1, m):
                q[tuple(int(a == j)+int(a == l) for a in range(m))] = g[j][l]
    return q, lam, g, c


def audit(t, valid=True):
    p = exact_law(t)
    q, lam, g, c = surrogate(t)
    mu = sum(c, F(0))
    insist(mu <= 1, "finite fixtures certify contraction by trace<=1")
    for j in range(len(t)):
        insist(sum(p[n]*n[j] for n in p) == lam[j], "exact first moment")
        for l in range(len(t)):
            insist(sum(p[n]*n[j]*(n[l]-int(j == l)) for n in p) == g[j][l], "exact factorial pair moment")
    result = {"p": p, "q": q, "mu": mu, "column_intensities": c, "lambda": lam, "g2": g}
    if not valid:
        insist(mu == 1 and q[(1,)] == F(-1, 2), "expected physical outside-domain witness")
        return result | {"status": "EXPECTED_OUTSIDE_DOMAIN", "positive_q": False, "theorem_applied": False}
    insist(mu <= F(1, 2) and all(v >= 0 for v in q.values()) and sum(q.values()) == 1, "positive normalized q")
    for j in range(len(t)):
        insist(sum(v*n[j] for n, v in q.items()) == lam[j], "q first moment")
        for l in range(len(t)):
            insist(sum(v*n[j]*(n[l]-int(j == l)) for n, v in q.items()) == g[j][l], "q second moment")
    tv = sum((abs(p[n]-q.get(n, F(0))) for n in p), F(0))/2
    tail = sum((p[n]*(sum(n)-1)**2 for n in p if sum(n) >= 3), F(0))
    factorial3 = sum((p[n]*sum(n)*(sum(n)-1)*(sum(n)-2) for n in p), F(0))
    e3 = sum((math.prod(c[i] for i in indices) for indices in combinations(range(len(c)), 3)), F(0))
    insist(tv == tail <= F(2, 3)*factorial3 <= 24*e3 <= 4*mu**3, "raw TV equality and factorial24 bound")
    return result | {"status": "EXACT_PASS", "tv": tv, "weighted_tail": tail, "factorial3": factorial3,
                     "e3": e3, "bound24": 24*e3, "bound4": 4*mu**3, "positive_q": True}


def digest(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def clean(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, (list, tuple)):
        return [clean(x) for x in value]
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    return value


class Evidence:
    def __init__(self, directory):
        directory.mkdir(exist_ok=False)
        self.directory, self.used = directory, 0
        self.records = (directory/"records.jsonl").open("x", encoding="ascii")
    def emit(self, row):
        payload = json.dumps(clean(row), sort_keys=True, allow_nan=False)+"\n"
        if self.used+len(payload.encode("ascii")) > CAP-RESERVE:
            raise RuntimeError("scientific-output cap; final receipt reserve retained")
        self.records.write(payload)
        self.records.flush()
        self.used += len(payload.encode("ascii"))
    def finish(self, summary, failure):
        self.records.close()
        payloads = [json.dumps(clean(x), sort_keys=True, allow_nan=False)+"\n" for x in (summary, failure)]
        insist(self.used+sum(len(x.encode("ascii")) for x in payloads) <= CAP, "aggregate output cap")
        for name, text in zip(("summary.json", "failure.json"), payloads):
            with (self.directory/name).open("x", encoding="ascii") as handle:
                handle.write(text)


def threads(xq):
    observed = {key: os.environ.get(key) for key in THREADS}
    value = int(xq.Config.compute_max_thread_count)
    insist(value == 1 and set(observed.values()) == {"1"}, "native/environment thread readback")
    return {"native": value, "environment": observed}


def native_stack(provenance, spec):
    import exqalibur as xq
    provenance["native_before_configuration"] = int(xq.Config.compute_max_thread_count)
    xq.Config.compute_max_thread_count = 1
    provenance["configured"] = threads(xq)
    import numpy as np
    import perceval as pcvl
    from perceval.backends import NaiveBackend
    provenance["after_imports"] = threads(xq)
    loaded = {}
    for name in ("exqalibur.exqalibur", "numpy", "numpy.linalg._linalg", "numpy.linalg._umath_linalg",
                 "numpy._core._multiarray_umath", "perceval", "perceval.backends._naive", "perceval.backends._abstract_backends"):
        path = Path(importlib.import_module(name).__file__).resolve()
        loaded[name] = {"path": str(path), "sha256": digest(path)}
    for pin in spec["external_artifacts"]:
        if pin.get("module") in loaded:
            insist(loaded[pin["module"]]["sha256"] == pin["sha256"], "actually loaded critical module pin")
    provenance["actually_loaded"] = loaded
    return np, pcvl, NaiveBackend, xq


def native_case(name, t, law, stack, writer, guard, state):
    np, pcvl, backend_type, xq = stack
    m, k = len(t), len(t[0])
    array = np.array([[float(x) for x in row] for row in t])
    def root(matrix):
        values, vectors = np.linalg.eigh(matrix)
        insist(float(values.min()) >= 0, "positive Halmos square-root operand; no clipping")
        return (vectors*np.sqrt(values))@vectors.T
    u = np.eye(m) if k == 0 else np.block([[array, root(np.eye(m)-array@array.T)],
                                                         [root(np.eye(k)-array.T@array), -array.T]])
    residual = max(float(np.max(np.abs(u.T@u-np.eye(m+k)))), float(np.max(np.abs(u@u.T-np.eye(m+k)))))
    insist(residual <= TOL, "Halmos unitarity absolute tolerance")
    backend = backend_type()
    backend.set_circuit(pcvl.Circuit(m+k).add(0, pcvl.Unitary(pcvl.Matrix(u))))
    backend.set_input_state(pcvl.BasicState([1]*k+[0]*m))
    writer.emit({"kind": "native_setup", "case": name, "T": t, "U": u.tolist(), "unitarity_residual": residual,
                 "input": [1]*k+[0]*m, "threads": threads(xq)})
    marginal = {n: 0.0 for n in law}
    count = 0
    for full in occupations(k, m+k):
        guard()
        before = threads(xq)
        writer.emit({"kind": "native_attempt", "case": name, "counts": full, "threads_before": before})
        state["native_calls_attempted"] += 1
        state["last_native_after"] = None
        try:
            amplitude = complex(backend.prob_amplitude(pcvl.BasicState(list(full))))
            state["native_calls"] += 1
        finally:
            state["last_native_after"] = threads(xq)
        probability = abs(amplitude)**2
        writer.emit({"kind": "native_raw", "case": name, "counts": full, "signal": full[:m], "loss": sum(full[m:]),
                     "amplitude": [amplitude.real, amplitude.imag], "probability": probability,
                     "threads_before": before, "threads_after": state["last_native_after"]})
        marginal[full[:m]] += probability
        count += 1
    errors = []
    for n in law:
        error = abs(marginal[n]-float(law[n]))
        writer.emit({"kind": "native_marginal", "case": name, "signal": n, "expected_exact": law[n],
                     "observed": marginal[n], "absolute_error": error})
        errors.append(error)
    insist(max(errors) <= TOL and abs(sum(marginal.values())-1) <= TOL, "native unconditional signal marginal")
    insist(count == math.comb(m+2*k-1, k), "complete native occupation population")
    return count


def checked_profile(spec, binding, contract_path, binding_path):
    insist(Path(sys.executable).absolute() == Path(PYTHON) and sys.version_info[:3] == (3, 11, 15), "persistent Python3.11.15")
    insist(binding["binding_state"] == "SEALED_ROOT_AUTHORIZED", "separate ROOT main authorization required")
    insist(binding["static_contract_path"] == contract_path and digest(ROOT/contract_path) == binding["static_contract_sha256"], "frozen static contract")
    insist(set(spec["execution_artifacts"]) <= set(binding["execution_artifacts"]), "complete static input closure")
    insist(binding_path in binding["execution_artifacts"], "active binding is a real input")
    for key in THREADS:
        os.environ[key] = "1"
    provenance = {"python": sys.version, "executable": sys.executable, "interpreter_sha256": digest(Path(sys.executable).resolve()),
                  "versions": {name: metadata.version(name) for name in VERSIONS}, "inputs": [], "external_before": []}
    insist(provenance["versions"] == VERSIONS, "pinned software versions")
    for name in binding["execution_artifacts"]:
        path = Path(name)
        insist(not path.is_absolute() and ".." not in path.parts and all(not (ROOT/Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts)+1)), "relative regular input")
        observed = digest(ROOT/path)
        if name in spec["execution_artifacts"]:
            insist(observed == binding["frozen_static_inputs"][name], "qualified static input hash")
        provenance["inputs"].append({"path": name, "sha256": observed})
    proof = binding["theory_binding"]
    insist(proof["bound"] and proof["path"] in binding["execution_artifacts"], "theory is a real bound input")
    insist(digest(ROOT/proof["path"]) == proof["sha256"], "theory source hash")
    for pin in spec["external_artifacts"]:
        insist(digest(pin["path"]) == pin["sha256"], "preimport external pin")
        provenance["external_before"].append(pin)
    insist(provenance["interpreter_sha256"] == next(pin["sha256"] for pin in spec["external_artifacts"] if pin["role"] == "physical_interpreter"), "actually running interpreter hash")
    return provenance


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    start, writer, failure, state = (time.process_time(), time.perf_counter()), None, None, {"phase": "PREIMPORT"}
    try:
        resource.setrlimit(resource.RLIMIT_FSIZE, (CAP, CAP))
        resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
        insist(args.output == OUTPUT, "fixed output path")
        for relative in (args.contract, args.binding, args.output):
            path = Path(relative)
            insist(not path.is_absolute() and ".." not in path.parts, "safe project-relative path")
            insist(all(not (ROOT/Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts)+1)), "no output/input symlink")
        spec = json.loads((ROOT/args.contract).read_text(encoding="utf-8"))
        insist(args.binding == spec["planned_binding_path"], "fixed future separate binding path")
        binding = json.loads((ROOT/args.binding).read_text(encoding="utf-8"))
        provenance = checked_profile(spec, binding, args.contract, args.binding)
        state["provenance"] = provenance
        writer = Evidence(ROOT/args.output)
        def guard():
            insist(time.process_time()-start[0] <= 60 and time.perf_counter()-start[1] <= 90, "CPU/wall resource allowance")
        writer.emit({"kind": "provenance", "observations": provenance, "RLIMIT_FSIZE": resource.getrlimit(resource.RLIMIT_FSIZE)})
        state.update(phase="EXACT", valid_cases=0, invalid_cases=0, exact_points=0, native_calls=0, native_calls_attempted=0)
        native = []
        for name, rows, valid, use_native in cases():
            guard()
            state["case"] = name
            t = matrix(rows)
            writer.emit({"kind": "exact_case_start", "case": name, "T": t, "expected_domain": valid})
            report = audit(t, valid)
            for n, p in report["p"].items():
                writer.emit({"kind": "exact_raw", "case": name, "signal": n, "loss": len(t[0])-sum(n), "p": p, "q": report["q"].get(n, F(0))})
                state["exact_points"] += 1
            writer.emit({"kind": "exact_audit", "case": name, **{key: value for key, value in report.items() if key not in ("p", "q")}})
            state["valid_cases" if valid else "invalid_cases"] += 1
            if name in ("R3a", "R3b"):
                insist(report["tv"] == report["bound24"], "sharp coefficient24 rank-one fixture")
            if use_native:
                native.append((name, t, report["p"]))
        insist((state["valid_cases"], state["invalid_cases"], state["exact_points"]) == (12, 1, 167), "exact population completion")
        state["phase"] = "NATIVE"
        stack = native_stack(provenance, spec)
        writer.emit({"kind": "native_provenance", "observations": provenance})
        for name, t, law in native:
            state["case"] = name
            native_case(name, t, law, stack, writer, guard, state)
        insist((state["native_calls"], state["native_calls_attempted"]) == (159, 159), "all five native cases and159 full occupations")
        provenance["final_threads"] = threads(stack[3])
        for row in provenance["inputs"]:
            insist(digest(ROOT/row["path"]) == row["sha256"], "input unchanged")
        for pin in spec["external_artifacts"]:
            insist(digest(pin["path"]) == pin["sha256"], "external input unchanged")
        guard()
        state.update(phase="COMPLETE", status="FINITE_VALIDATION_PASS", positive_accepted=False, provenance=provenance)
    except Exception as error:
        failure = {"type": type(error).__name__, "repr": repr(error), "traceback": traceback.format_exc(), "prefix": dict(state)}
        state.update(status="INCONCLUSIVE_FIRST_FAILURE", positive_accepted=False)
        if writer is None:
            sys.stderr.write(json.dumps(failure)+"\n")
    finally:
        if writer is not None:
            state["runtime"] = {"cpu": time.process_time()-start[0], "wall": time.perf_counter()-start[1]}
            writer.finish(state, failure or {"status": "NO_FAILURE"})
    return int(failure is not None)


if __name__ == "__main__":
    raise SystemExit(main())
