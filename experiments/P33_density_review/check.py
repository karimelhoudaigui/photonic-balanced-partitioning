"""Bounded independent audit: exact two-photon laws, plus roundoff witness.

Run with the project's Python; no package sampler or certificate is used to
define the exact laws. The imported certificate is tested only at the end.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import importlib.util
import json
import math
import platform

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/photonic_balanced_partitioning/photonic/density_certificate.py"


def exact_case(t):
    # Rational Pythagorean rotation; physical amplitudes are r[group,a]/sqrt(2).
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    r = ((c, -s), (s, c))
    q = [[r[i//2][a]**2 / 2 for a in range(2)] for i in range(4)]
    laws = []
    moment = F(0)
    for i, j in combinations_with_replacement(range(4), 2):
        numerator = (r[i//2][0]*r[j//2][1] + r[i//2][1]*r[j//2][0])/2
        pb = numerator**2 / (2 if i == j else 1)
        pd = (q[i][0]*q[j][1] + q[i][1]*q[j][0]) / (2 if i == j else 1)
        if i == j:
            moment += pb
        laws.append({"rows": [i, j], "pb": str(pb), "pd": str(pd)})
    pb_sum = sum(F(x["pb"]) for x in laws)
    pd_sum = sum(F(x["pd"]) for x in laws)
    tv = sum(abs(F(x["pb"])-F(x["pd"])) for x in laws)/2
    means = [sum(row) for row in q]
    delta = sum(a-max(row) for a, row in zip(means, q))
    pairs = sum(a*a-sum(x*x for x in row) for a, row in zip(means, q))
    assert pb_sum == pd_sum == 1
    assert min(means) == F(1, 2)
    assert delta == 2*s*s
    assert tv == pairs == moment == 2*c*c*s*s == delta*(1-delta/2)
    # For k=2 the finite N1/N2 quantity is B12^2/2, no square roots needed.
    assert (2*c*s)**2/2 == tv
    return {"t": str(t), "delta": str(delta), "M": str(pairs), "TV": str(tv),
            "small_M_branch": pairs < F(1, 8), "laws": laws}


def main():
    cases = [exact_case(F(0)), exact_case(F(1, 1000)), exact_case(F(1, 100)),
             exact_case(F(1, 10)), exact_case(F(1, 3))]
    import numpy as np
    spec = importlib.util.spec_from_file_location("audited_density", SOURCE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    theta = 1e-10
    c, s = math.cos(theta), math.sin(theta)
    frame = np.array([[c, -s], [c, -s], [s, c], [s, c]]) / math.sqrt(2)
    result = mod.density_certificate(frame)
    witness = {"theta": theta, "analytic_family_TV": 2*c*c*s*s,
               "orthogonality_residual": float(np.linalg.norm(frame.T@frame-np.eye(2))),
               "returned": result}
    assert result["density_cycle_tv_bound"] == 0
    assert witness["analytic_family_TV"] > 0
    record = {"purpose": "Finite exact arithmetic audit and floating-point limitation; not a universal proof",
              "base_commit": "75e5831a34b7bbf82ae21bb88894a2c12d4a6d47",
              "python": platform.python_version(), "numpy": np.__version__,
              "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "exact_cases": cases, "roundoff_witness": witness}
    out = Path(__file__).with_name("receipt.json")
    out.write_text(json.dumps(record, indent=2)+"\n")
    print(json.dumps({"exact_cases": len(cases), "fock_outcomes": 10*len(cases),
                      "roundoff_witness": witness, "receipt_sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
