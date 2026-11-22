"""Independent bounded numerical adversarial audit of revision 77a8588.

No large-N probabilities, local model, QPU, or production mutation. Reference
scalar envelopes and physical two-photon laws use 800-digit mpmath arithmetic.
"""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (120, 120))
import datetime
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import time

import mpmath as mp
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SOURCE = ROOT / "src/photonic_balanced_partitioning/photonic/density_certificate.py"
mp.mp.dps = 800


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_number(x):
    return mp.nstr(x, 40)


def reference_envelope(s):
    s = mp.mpf(s)
    return min(mp.mpf(1), mp.expm1(-s-mp.log1p(-s))/2) if s < 1 else mp.mpf(1)


def main():
    start = time.monotonic()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    inputs = {str(SOURCE.relative_to(ROOT)): digest(SOURCE),
              str(Path(__file__).relative_to(ROOT)): digest(Path(__file__))}
    spec = importlib.util.spec_from_file_location("audited_density", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    grid = {0., 1., float(np.nextafter(1., 2.))}
    grid.update(float(x) for x in np.logspace(-323, -1, 160))
    grid.update(10.**(-i) for i in range(1, 324))
    grid.update(float(x) for x in np.linspace(.1, .99, 60))
    grid.update(1.-10.**(-i) for i in range(1, 18))
    for center in (.1, 1.):
        left = right = center
        for _ in range(8):
            left = float(np.nextafter(left, -math.inf))
            right = float(np.nextafter(right, math.inf))
            grid.update((left, right))
    scalars = []
    for s in sorted(grid):
        value = module.cycle_envelope(s)
        ref = reference_envelope(s)
        gap = mp.mpf(value)-ref
        scalars.append({"sigma": s, "value": value, "reference": text_number(ref),
                        "signed_error": text_number(gap), "below_reference": bool(gap < 0)})
    descents = [{"left": a, "right": b} for a, b in zip(scalars, scalars[1:])
                if a["value"] > b["value"]]
    invalid = []
    for x in (-1., math.inf, -math.inf, math.nan):
        try:
            module.cycle_envelope(x)
        except ValueError:
            invalid.append(str(x))
        else:
            raise AssertionError("Invalid sigma accepted")
    families = []
    for theta in [0., .01, .2, math.pi/4] + [10.**(-p) for p in range(1, 171)]:
        c, s = math.cos(theta), math.sin(theta)
        frame = np.array([[c, -s], [c, -s], [s, c], [s, c]])/math.sqrt(2)
        result = module.density_certificate(frame)
        exact_tv = 2*mp.cos(mp.mpf(theta))**2*mp.sin(mp.mpf(theta))**2
        exact_delta = 2*mp.sin(mp.mpf(theta))**2
        assert result["numerical_semantics"] == "FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED"
        bounds = {key: result[key] for key in result if key.endswith("tv_bound")}
        gaps = {key: text_number(mp.mpf(value)-exact_tv) for key, value in bounds.items()}
        families.append({"theta": theta, "physical_family_TV": text_number(exact_tv),
                         "physical_family_delta": text_number(exact_delta), "result": result,
                         "bound_minus_physical_TV": gaps,
                         "underestimates": [key for key, value in bounds.items() if mp.mpf(value)<exact_tv]})
    special = {}
    for name, frame in {"unary": np.array([[1.], [0.]]),
                        "tiny_positive_row": np.array([[1.], [1e-170]])}.items():
        special[name] = module.density_certificate(frame)
    report = {"base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "precision_decimal_digits": mp.mp.dps, "scalar_cases": scalars,
              "scalar_descents": descents, "invalid_sigma_rejections": invalid,
              "physical_family_cases": families, "special_cases": special}
    receipt = HERE / "receipt.json"
    receipt.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    summary = {"scalar_case_count": len(scalars),
               "scalar_underestimate_count": sum(x["below_reference"] for x in scalars),
               "scalar_descents": descents,
               "physical_family_case_count": len(families),
               "family_cases_with_underestimate": sum(bool(x["underestimates"]) for x in families),
               "first_family_underestimate": next((x for x in families if x["underestimates"]), None),
               "theta_1e_10": next(x for x in families if x["theta"] == 1e-10),
               "receipt_sha256": digest(receipt), "wall_seconds": time.monotonic()-start,
               "cpu_seconds": time.process_time()}
    (HERE / "summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    manifest = {"schema_version": 2, "claim_id": "P33-density-float-independent-review",
        "repository": {"commit": report["base_commit"], "dirty": True},
        "command": ["/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python", "experiments/P33_density_float_review/check.py"],
        "environment": {"software": [{"name": "Python", "version": platform.python_version()},
            {"name": "NumPy", "version": np.__version__}, {"name": "mpmath", "version": mp.__version__}],
            "hardware": platform.platform()+" "+platform.machine()},
        "mathematics": {"assertion_tested": "Compare deterministic scalar envelope grid and two-photon rotation family to 800-digit reference; preserve all observed underestimates",
            "coefficient_domain": "float64 versus 800-decimal-digit mpmath", "conventions": "Halved TV, all Fock outcomes; ideal physical rotation parameter equals exact binary64 theta",
            "inputs": list(inputs), "bounds": {"cpu_seconds": 120, "m": 4, "k": 2, "scalar_cases": len(scalars), "family_cases": len(families)},
            "non_claims": ["No interval certification", "No universal numerical error bound", "No large-N probabilities", "No novelty or QPU claim"]},
        "randomness": {"used": False, "generator": "none", "seed": None},
        "run": {"started_at": started, "runtime_seconds": time.monotonic()-start, "exit_status": 0,
            "status": "completed", "resource_limits": {"memory_bytes": None, "cpu_seconds": 120, "max_cores": 1, "max_threads": 1}},
        "outputs": [{"path": str(p.relative_to(ROOT)), "sha256": digest(p), "kind": "result"} for p in (receipt, HERE/"summary.json")],
        "checks": ["Invalid scalar rejection", "Every family result carries explicit non-interval semantics", "Production source hashes unchanged before/after"],
        "result": "Finite numerical limitations reproduced; see summary and report",
        "residual_risks": ["800 digits are high precision, not interval arithmetic", "Floating frame approximates ideal normalized family", "Finite grid is not exhaustive"],
        "input_artifacts": [{"path": path, "sha256": before, "sha256_after": digest(ROOT/path)} for path, before in inputs.items()],
        "declared_results": []}
    assert all(x["sha256"] == x["sha256_after"] for x in manifest["input_artifacts"])
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
