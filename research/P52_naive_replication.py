"""P52 finite probability replication; stdlib-only until an authorized mode runs.

NaiveBackend calls exqalibur.permanent_cx, whereas the archived primary uses
creation-operator recurrence. No primary project module is imported. Floating
agreement is a finite numerical cross-check, never an interval certificate.
"""
from __future__ import annotations

import argparse
import cmath
import hashlib
import importlib.metadata
import inspect
import itertools
import json
import math
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = Path("experiments/P52_collective_phase/run_001")
REFERENCE_COMMIT = "762877a65125e5411e10906ccdb7f64ff280d840"
PINNED = {
    "manifest.json": "d580e0c0473a763257d6e8fecb3be5a7e27b0596d573c6af49b4bb738d7fe1b7",
    "data/geometry.npz": "379a53775b2b1b15ceb299692404a0a6afbec5ac62a7aff2c8efabae1ae1c715",
    "data/theta_0.npz": "405b805d09495775d2f49c71426c163ba49a00b188cb938cac99c804b906a542",
    "data/theta_1.npz": "48cafbcb659f51e6d4c155c03bfa4ed27f6914f5f64ee1bae873108c2a8e3c07",
    "data/theta_2.npz": "0617ada35f36fd968e1b7c91ca2110f9188465d2e9bc3d47d93ca7bb05d7a9d8",
    "data/theta_3.npz": "d9faf7085a9a1eab44fddb8681d586a24a98e5c80de92e83a28e9024044e6154",
}
ABS_TOL = 5e-10
MATRIX_TOL = 5e-12
THREAD_VARIABLES = (
    "OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS",
)
MAX_OUTPUT = 4 * 1024 * 1024


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def occupations(m=8, n=8):
    """Multisets of labelled slots, converted to histograms independently."""
    result = []
    for slots in itertools.combinations_with_replacement(range(m), n):
        row = [0] * m
        for slot in slots:
            row[slot] += 1
        result.append(tuple(row))
    return result


def scalar_unitary(index):
    """U[out,input], without block-array construction or project imports."""
    if index not in range(4):
        raise ValueError("phase index outside frozen grid")
    theta = index * math.pi / 4
    rows = []
    for output in range(8):
        half_out, j = divmod(output, 4)
        row = []
        for input_port in range(8):
            half_in, a = divmod(input_port, 4)
            walsh_sign = -1 if (((j & 1) * (a >> 1) + (j >> 1) * (a & 1)) % 2) else 1
            row.append(walsh_sign * (-1) ** (half_out * half_in)
                       * cmath.exp(1j * half_in * j * theta) / math.sqrt(8))
        rows.append(row)
    return rows


def check_reference(root=ROOT):
    found = {}
    for name, expected in PINNED.items():
        path = root / REFERENCE / name
        if path.is_symlink() or sha(path) != expected:
            raise ValueError(f"reference hash/symlink mismatch: {name}")
        found[str(REFERENCE / name)] = expected
    return found


def fresh_output(path, root=ROOT):
    path = Path(path).absolute()
    root = root.resolve()
    if ".." in path.parts or not path.is_relative_to(root) or path.exists():
        raise ValueError("output must be fresh and inside the project")
    # Refuse all historical data, including nonexistent descendants.
    historical = (root / REFERENCE).resolve()
    if path == historical or path.is_relative_to(historical):
        raise ValueError("historical reference is immutable")
    current = path
    while current != root:
        if current.is_symlink():
            raise ValueError("symlink output ancestor")
        current = current.parent
    return path


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def check_record(name, observed, expected):
    """Normalize scalar types at the JSON boundary, including foreign booleans."""
    residual = abs(observed - expected)
    actual, target = complex(observed), complex(expected)
    return {"name": str(name), "observed": [actual.real, actual.imag],
            "expected": [target.real, target.imag],
            "absolute_error": float(residual), "pass": bool(residual <= ABS_TOL)}


def configure_matplotlib_cache():
    """Preserve explicit settings; otherwise use a writable persistent cache."""
    if "MPLCONFIGDIR" in os.environ:
        value = os.environ["MPLCONFIGDIR"]
        return {"path": value, "set_by_validator": False, "preexisting": Path(value).exists()}
    path = ROOT / ".local/mplconfig"
    preexisting = path.exists()
    path.mkdir(parents=True, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = str(path)
    return {"path": str(path), "set_by_validator": True, "preexisting": preexisting,
            "interpretation": "persistent configuration/cache only; no warm/cold performance claim"}


def thread_snapshot():
    """Observational process-thread listing; not a native-thread guarantee."""
    try:
        completed = subprocess.run(
            ["ps", "-M", "-p", str(os.getpid())], text=True, capture_output=True,
            timeout=2, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"available": False, "error_type": type(error).__name__,
                "errno": getattr(error, "errno", None), "error": str(error)}
    return {"available": completed.returncode == 0,
            "returncode": completed.returncode, "stdout": completed.stdout,
            "stderr": completed.stderr}


def platform_snapshot():
    """Platform metadata is optional observability, never a physics precondition."""
    try:
        return platform.platform()
    except OSError as error:
        return {"available": False, "error_type": type(error).__name__,
                "errno": error.errno, "error": str(error)}


def load_backend():
    import numpy as np
    import exqalibur as xq
    from perceval.backends import NaiveBackend
    from perceval.components import Unitary
    from perceval.utils import FockState
    return np, xq, NaiveBackend, Unitary, FockState


def make_backend(matrix, api):
    np, _, NaiveBackend, Unitary, FockState = api
    backend = NaiveBackend()
    backend.set_circuit(Unitary(np.asarray(matrix, dtype=complex)))
    backend.set_input_state(FockState([1] * len(matrix)))
    return backend


def package_provenance(api):
    np, xq, NaiveBackend, Unitary, FockState = api
    paths = {"NaiveBackend": inspect.getfile(NaiveBackend),
             "Unitary": inspect.getfile(Unitary), "exqalibur_binary": xq.__file__}
    # xq.__file__ can be a package initializer. Include the compiled module too.
    for name, module in tuple(sys.modules.items()):
        file = getattr(module, "__file__", None)
        if name.startswith("exqalibur") and file and file.endswith((".so", ".pyd")):
            paths[name] = file
    try:
        signature = str(inspect.signature(xq.permanent_cx))
    except (TypeError, ValueError) as error:
        signature = f"UNAVAILABLE: {type(error).__name__}: {error}"
    return {
        "versions": {name: importlib.metadata.version(name)
                     for name in ("numpy", "perceval-quandela", "exqalibur", "pytest")},
        "python": sys.version, "platform": platform_snapshot(),
        "files": {key: {"path": value, "sha256": sha(value)} for key, value in paths.items()},
        "permanent_signature": signature,
        "permanent_doc": xq.permanent_cx.__doc__,
        "thread_named_exports": [name for name in dir(xq) if "thread" in name.lower()],
        "thread_environment": {name: os.environ.get(name) for name in THREAD_VARIABLES},
        "native_thread_control": "NOT_ESTABLISHED: no unsupported keyword or vendor patch used; ps samples and environment limits do not prove one native worker",
        "backend": "local NaiveBackend.prob_amplitude; no masks/iterator/pruning/remote processor",
    }


def qualify(api):
    np, xq, _, _, FockState = api
    checks = []

    def check(name, observed, expected):
        checks.append(check_record(name, observed, expected))

    hom = np.array([[1, 1j], [1j, 1]], complex) / math.sqrt(2)
    backend = make_backend(hom, api)
    check("HOM_collision_free", backend.prob_amplitude(FockState([1, 1])), 0)
    check("HOM_bunched_factorial", backend.prob_amplitude(FockState([2, 0])), 1j / math.sqrt(2))
    phi = .37
    unitary = np.diag([cmath.exp(1j * phi), 1]) @ np.array([[.6, -.8], [.8, .6]])
    backend = make_backend(unitary, api)
    check("complex_input_output_orientation", backend.prob_amplitude(FockState([2, 0])),
          -math.sqrt(2) * .48 * cmath.exp(2j * phi))
    check("complex_permanent_CF", backend.prob_amplitude(FockState([1, 1])),
          (-.28) * cmath.exp(1j * phi))
    # A single eight-photon identity amplitude qualifies the requested API size.
    backend = make_backend(np.eye(8), api)
    check("identity_8_CF", backend.prob_amplitude(FockState([1] * 8)), 1)
    backend.set_input_state(FockState([0] * 8))
    check("vacuum", backend.prob_amplitude(FockState([0] * 8)), 1)
    check("native_known_complex_permanent",
          xq.permanent_cx(np.array([[1 + 1j, 2], [3j, 4 - 1j]], complex)), 5 + 9j)
    states = occupations()
    if len(states) != 6435 or len(set(states)) != 6435 or any(sum(n) != 8 for n in states):
        raise AssertionError("independent enumeration")
    for index in range(4):
        u = np.asarray(scalar_unitary(index))
        check(f"independent_unitary_{index}", np.max(np.abs(u.conj().T @ u - np.eye(8))), 0)
    return checks


def full_replication(api, output):
    np, _, _, _, FockState = api
    rows = occupations()
    own = {n: i for i, n in enumerate(rows)}
    with np.load(ROOT / REFERENCE / "data/geometry.npz", allow_pickle=False) as geometry:
        reference_rows = [tuple(int(x) for x in row) for row in geometry["occupations8"]]
    if len(reference_rows) != len(own) or set(reference_rows) != set(own):
        raise AssertionError("complete occupation sets differ")
    archived_index = {n: i for i, n in enumerate(reference_rows)}
    if len(archived_index) != len(reference_rows):
        raise AssertionError("duplicate archived occupation")
    alignment = np.array([archived_index[n] for n in rows], dtype=np.int64)
    np.save(output / "occupations.npy", np.asarray(rows, dtype=np.int16), allow_pickle=False)
    summaries = []
    for index in range(4):
        with np.load(ROOT / REFERENCE / f"data/theta_{index}.npz", allow_pickle=False) as archive:
            archived_u = archive["u"]
            reference_a = archive["B_amplitudes"][alignment]
            reference_p = archive["B_probability"][alignment]
        independent_u = np.asarray(scalar_unitary(index))
        matrix_error = float(np.max(np.abs(archived_u - independent_u)))
        unitary_error = float(np.max(np.abs(independent_u.conj().T @ independent_u - np.eye(8))))
        if matrix_error > MATRIX_TOL or unitary_error > MATRIX_TOL:
            raise AssertionError("matrix alignment/unitarity failed before permanent calls")
        backend = make_backend(archived_u, api)
        amplitudes = np.empty(len(rows), dtype=complex)
        for i, n in enumerate(rows):
            amplitudes[i] = backend.prob_amplitude(FockState(list(n)))
        probability = np.abs(amplitudes) ** 2
        amp_error = np.abs(amplitudes - reference_a)
        prob_error = np.abs(probability - reference_p)
        # Complete, unfiltered vectors; no renormalization or phase fitting.
        np.savez(output / f"replica_theta_{index}.npz", u=archived_u,
                 independent_u=independent_u, amplitudes=amplitudes, probability=probability,
                 reference_amplitudes=reference_a, reference_probability=reference_p)
        item = {
            "phase_index": index, "theta_radians": index * math.pi / 4,
            "permanent_calls": len(rows), "matrix_absolute_error": matrix_error,
            "unitarity_absolute_error": unitary_error,
            "max_amplitude_absolute_error": float(np.max(amp_error)),
            "max_probability_absolute_error": float(np.max(prob_error)),
            "worst_amplitude_occupation": rows[int(np.argmax(amp_error))],
            "worst_probability_occupation": rows[int(np.argmax(prob_error))],
            "probability_sum": float(np.sum(probability)),
            "reference_probability_sum": float(np.sum(reference_p)),
            "TV_numerical": float(np.sum(prob_error) / 2),
            "pass": bool(np.all(np.isfinite(amplitudes)) and np.all(np.isfinite(probability))
                         and np.max(amp_error) <= ABS_TOL and np.max(prob_error) <= ABS_TOL
                         and abs(np.sum(probability) - 1) <= ABS_TOL),
        }
        summaries.append(item)
        write_json(output / "progress.json", {"completed_phases": summaries, "complete": len(summaries) == 4})
    return summaries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("qualify", "full"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    # Refuse existing destinations and verify historical bytes BEFORE numpy/Perceval.
    output = fresh_output(args.output)
    inputs_before = check_reference()
    output.mkdir(parents=True)
    started_wall, started_cpu = time.monotonic(), time.process_time()
    report = {"mode": args.mode, "reference_data_commit": REFERENCE_COMMIT,
              "source_sha256": sha(__file__), "input_hashes_before": inputs_before,
              "amplitude_probability_absolute_tolerance": ABS_TOL, "matrix_tolerance": MATRIX_TOL,
              "source_state": "8 distinct single photons, no loss, all occupations retained",
              "independence": "scalar U and multiset enumeration independently implemented; archival geometry used only for tuple alignment; no primary project import",
              "status": "INCOMPLETE", "thread_snapshot_before_import": thread_snapshot()}
    exit_code = 1
    try:
        report["matplotlib_cache"] = configure_matplotlib_cache()
        if args.mode == "qualify":
            # Same bounded child: seven guards plus eleven small analytic checks.
            os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
            import pytest
            guard_status = int(pytest.main([
                "-q", str(ROOT / "tests/test_p52_naive_replication.py"),
                "--junitxml=" + str(output / "guard_junit.xml"),
            ]))
            report["guard_pytest_exit_code"] = guard_status
            if guard_status:
                raise AssertionError("administrative guard qualification failed")
        api = load_backend()
        report["software"] = package_provenance(api)
        report["thread_snapshot_after_import"] = thread_snapshot()
        if args.mode == "qualify":
            report["checks"] = qualify(api)
            passed = all(item["pass"] for item in report["checks"])
            report["status"] = "API_QUALIFICATION_PASS_NATIVE_THREADS_UNVERIFIED" if passed else "QUALIFICATION_FAIL"
        else:
            report["phases"] = full_replication(api, output)
            passed = len(report["phases"]) == 4 and all(item["pass"] for item in report["phases"])
            report["status"] = "FINITE_FLOAT64_AGREEMENT" if passed else "DISAGREEMENT"
        exit_code = 0 if passed else 1
    except Exception as error:
        report["exception"] = {"type": type(error).__name__, "message": str(error)}
    finally:
        report["thread_snapshot_after_work"] = thread_snapshot()
        report["input_hashes_after"] = check_reference()
        report["resources"] = {"process_cpu_seconds": time.process_time() - started_cpu,
                               "wall_seconds": time.monotonic() - started_wall,
                               "max_rss_native_units": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                               "rss_unit": "bytes on Darwin; KiB on Linux"}
        report["outputs"] = {str(p.relative_to(output)): {"sha256": sha(p), "bytes": p.stat().st_size}
                             for p in sorted(output.iterdir()) if p.is_file()}
        write_json(output / "report.json", report)
        if sum(p.stat().st_size for p in output.iterdir() if p.is_file()) > MAX_OUTPUT:
            raise RuntimeError("output exceeds frozen 4MiB cap")
    print(json.dumps({"status": report["status"], "output": str(output)}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
