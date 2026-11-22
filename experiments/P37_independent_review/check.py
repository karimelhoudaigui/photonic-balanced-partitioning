"""Small exact P37 audit, independent of the coordinator's numerical probe."""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
from fractions import Fraction as F
from math import comb
from pathlib import Path
import datetime
import hashlib
import json
import platform
import time
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PROOF = ROOT / "theory/phase3_loss_source_selection.md"
DECLARED = [str((OUT/"receipt.json").relative_to(ROOT))]


def h(m, ell):
    k = m//2
    return F(comb(m, k)*comb(ell-1, k-1), comb(m+ell-1, ell)) if ell >= k else F(0)


def normalized_polynomial(poly, eta, k):
    divided = sp.Poly(sp.cancel(poly/eta**k), eta)
    def value(point):
        return F(divided.eval(sp.Rational(point.numerator, point.denominator)))
    assert value(F(0)) > 0 and value(F(1)) < 0
    lo, hi = F(0), F(1)
    for _ in range(40):
        mid = (lo+hi)/2
        if value(mid) > 0:
            lo = mid
        else:
            hi = mid
    assert value(lo) > 0 and value(hi) < 0
    return {"factorization": str(sp.factor(poly)), "lower": str(lo), "upper": str(hi),
            "lower_float": float(lo), "upper_float": float(hi),
            "lower_sign": str(value(lo)), "upper_sign": str(value(hi))}


def main():
    cpu_start, wall_start = time.process_time(), time.monotonic()
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    files = [PROOF, Path(__file__)]
    hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in files]
    eta = sp.symbols("eta")
    m, k = 8, 4
    H = [h(m, ell) for ell in range(m+1)]
    S = {N: sp.expand(sum(sp.Rational(h(m, ell).numerator, h(m, ell).denominator)*comb(N, ell)*eta**ell*(1-eta)**(N-ell) for ell in range(N+1))) for N in range(k, m+1)}
    attempt_root = normalized_polynomial(S[m]-S[m-1], eta, k)
    photon_roots = {str(j): normalized_polynomial(S[j+1]/(j+1)-S[j]/j, eta, k) for j in (m-3, m-2, m-1)}
    assert F(photon_roots["7"]["upper"]) < F(photon_roots["6"]["lower"])
    assert F(photon_roots["6"]["upper"]) < F(photon_roots["5"]["lower"])
    for N in range(k, m-1):
        coeffs = [h(m, ell+1)-h(m, ell) for ell in range(N+1)]
        assert min(coeffs) >= 0 and max(coeffs) > 0
    assert H[6] == H[7] > H[8]
    assert [i for i in range(k,m+1) if H[i] == max(H[k:])] == [6,7]
    assert [i for i in range(k,m+1) if H[i]/i == max(H[j]/j for j in range(k,m+1))] == [5]
    assert all(poly.subs(eta, 0) == 0 for poly in S.values())
    M, ell = sp.symbols("M ell", positive=True)
    ratio_h = ell*(ell+1)/((ell-M/2+1)*(M+ell))
    ratio_g = ell**2/((ell-M/2+1)*(M+ell))
    assert sp.simplify(ratio_h-1-(M/2)*(M-2-ell)/((ell-M/2+1)*(M+ell))) == 0
    zero_g = sp.solve(sp.together(ratio_g-1), ell)[0]
    assert sp.simplify(zero_g-(M-4+8/(M+2))) == 0
    lambda0 = {}
    for s in range(1,5):
        ah = sp.limit(M*(ratio_h.subs(ell, M-s)-1), M, sp.oo)
        ag = sp.limit(M*(ratio_g.subs(ell, M-s)-1), M, sp.oo)
        assert ah == sp.Rational(s-2, 2) and ag == sp.Rational(s-4, 2)
        lambda0[str(s)] = {"h_first_coefficient": str(ah), "g_first_coefficient": str(ag)}
    receipt = {"base_commit": "d402374b21a812de1d1b5658fac37d294a20a035", "proof_sha256": hashes[0],
        "assertion_tested": "Exact m8 endpoint candidates and disjoint root brackets; symbolic h/g ratios and lambda0 first coefficients; not an asymptotic proof",
        "m8_h": list(map(str,H)), "m8_S_polynomials": {str(N): str(sp.factor(p)) for N,p in S.items()},
        "m8_attempt_root": attempt_root, "m8_photon_roots": photon_roots,
        "lambda0_checks": lambda0, "cpu_seconds": time.process_time()-cpu_start}
    output = OUT/"receipt.json"
    output.write_text(json.dumps(receipt, indent=2)+"\n")
    manifest = {"schema_version": 2, "claim_id": "P37-independent-small-check",
        "repository": {"commit": receipt["base_commit"], "dirty": True},
        "command": ["/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python", "experiments/P37_independent_review/check.py"],
        "environment": {"software": [{"name": "Python", "version": platform.python_version()}, {"name": "SymPy", "version": sp.__version__}], "hardware": platform.platform()+" "+platform.machine()},
        "mathematics": {"assertion_tested": receipt["assertion_tested"], "coefficient_domain": "rational polynomials; symbolic limits",
            "conventions": "m8,k4,source cap N<=8; all physical attempts charged", "inputs": [str(p.relative_to(ROOT)) for p in files],
            "bounds": {"m": 8, "root_bracket_bisections": 40}, "non_claims": ["Finite checks are not proofs of uniqueness or asymptotic limits", "No graph enrichment, novelty or advantage claim"]},
        "randomness": {"used": False, "generator": "none", "seed": None},
        "run": {"started_at": started, "runtime_seconds": time.monotonic()-wall_start, "exit_status": 0, "status": "completed",
            "resource_limits": {"memory_bytes": None, "cpu_seconds": 30, "max_cores": 1, "max_threads": 1}},
        "outputs": [{"path": str(output.relative_to(ROOT)), "sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "kind": "result"}],
        "checks": ["m8 endpoints", "Adjacent root order", "Lossless ratio identities", "lambda0 coefficients"],
        "result": "All exact finite checks passed", "residual_risks": ["Universal proof audit is recorded separately"],
        "input_artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": digest, "sha256_after": hashlib.sha256(p.read_bytes()).hexdigest()} for p,digest in zip(files,hashes)],
        "declared_results": DECLARED}
    assert all(x["sha256"] == x["sha256_after"] for x in manifest["input_artifacts"])
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
