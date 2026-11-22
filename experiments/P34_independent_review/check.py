"""Exact bounded three-attempt Fock/adaptive check, not a proof substitute."""
import resource
resource.setrlimit(resource.RLIMIT_CPU, (60, 60))
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import datetime
import platform
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ABSORB = (-1, -1)
DECLARED_RESULTS = [str((OUT/name).relative_to(ROOT)) for name in ("receipt.json", "transcripts.json")]


def laws(t):
    # V_ia=r[group(i),a]/sqrt(2), rational Pythagorean rotation.
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    r = ((c, -s), (s, c))
    b, d = {}, {}
    for i, j in combinations_with_replacement(range(4), 2):
        amplitude = (r[i//2][0]*r[j//2][1]+r[i//2][1]*r[j//2][0])/2
        divisor = 2 if i == j else 1
        b[i, j] = amplitude**2/divisor
        d[i, j] = ((r[i//2][0]*r[j//2][1])**2+(r[i//2][1]*r[j//2][0])**2)/4/divisor
    assert sum(b.values()) == sum(d.values()) == 1
    return b, d


def tv(b, d):
    return sum(abs(b.get(x, 0)-d.get(x, 0)) for x in b.keys()|d.keys())/2


def kernels(seed, history):
    if (0, 0) in history or ABSORB in history:
        return {ABSORB: F(1)}, {ABSORB: F(1)}
    step = len(history)
    if history and history[-1][0] == history[-1][1]:
        strength = F(1, 4+seed)
    else:
        strength = F(1, 12+step+seed)
    return laws(strength)


def run():
    start = time.process_time()
    wall_start = time.monotonic()
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    input_paths = [ROOT/"theory/phase3_adaptive_replacement.md", Path(__file__)]
    input_hashes = [hashlib.sha256(p.read_bytes()).hexdigest() for p in input_paths]
    # Include the classical policy's one shared fair random bit in the transcript.
    B = D = equal = {(seed, ()): F(1, 2) for seed in (0, 1)}
    et, eb, first_mismatch = [], [], []
    for step in range(3):
        NB, ND, NE = defaultdict(F), defaultdict(F), defaultdict(F)
        max_error = expectation = mismatch = F(0)
        for key in B.keys()|D.keys()|equal.keys():
            seed, h = key
            b, d = kernels(seed, h)
            epsilon = tv(b, d)
            max_error = max(max_error, epsilon)
            expectation += B.get(key, 0)*epsilon
            mismatch += equal.get(key, 0)*epsilon
            for y in b.keys()|d.keys():
                nextkey = seed, h+(y,)
                NB[nextkey] += B.get(key, 0)*b.get(y, 0)
                ND[nextkey] += D.get(key, 0)*d.get(y, 0)
                NE[nextkey] += equal.get(key, 0)*min(b.get(y, 0), d.get(y, 0))
        B, D, equal = dict(NB), dict(ND), dict(NE)
        assert sum(B.values()) == sum(D.values()) == 1
        assert all(equal[x] <= B[x] for x in equal)
        assert mismatch <= expectation
        et.append(max_error); eb.append(expectation); first_mismatch.append(mismatch)
    product = F(1)
    for e in et:
        product *= 1-e
    transcript_tv = tv(B, D)
    coupling_failure = 1-sum(equal.values())
    assert coupling_failure == sum(first_mismatch)
    assert transcript_tv <= coupling_failure <= 1-product <= sum(et)
    assert transcript_tv <= min(1, sum(eb))
    success_b = sum(p for (_, h), p in B.items() if (0, 0) in h)
    success_d = sum(p for (_, h), p in D.items() if (0, 0) in h)
    assert abs(success_b-success_d) <= transcript_tv
    # Initial-circuit-only control: exact zero first-step error, positive second.
    initial_b, initial_d = laws(F(0))
    later_b, later_d = laws(F(1, 5))
    control_b = {(x, y): p*q for x, p in initial_b.items() for y, q in later_b.items()}
    control_d = {(x, y): p*q for x, p in initial_d.items() for y, q in later_d.items()}
    assert tv(initial_b, initial_d) == 0 < tv(control_b, control_d)
    # Literal missing e_t range: identical deterministic physical kernels, e=3.
    assert 1-(1-F(3))*(1-F(3)) == -3
    result = {"assertion_tested": "Exact rational three-step adaptive same-policy comparison including random bit and absorbing stopping; all complete two-photon Fock outcomes",
        "base_commit": "e201f1c337cb780225bdcdd0a806cfd7d20d2fe2",
        "states": len(B), "T": 3, "m": 4, "k": 2,
        "transcript_TV": str(transcript_tv), "transcript_TV_float": float(transcript_tv),
        "maximal_prefix_coupling_failure": str(coupling_failure),
        "product_bound": str(1-product), "expected_B_bound": str(sum(eb)),
        "expected_B_bound_float": float(sum(eb)), "deterministic_errors": list(map(str, et)),
        "expected_B_errors": list(map(str, eb)), "first_mismatch_masses": list(map(str, first_mismatch)),
        "success_difference": str(abs(success_b-success_d)),
        "initial_only_control_TV": str(tv(control_b, control_d)),
        "missing_range_counterexample": {"T": 2, "m": 1, "k": 1, "epsilon": [0, 0], "e": [3, 3], "actual_TV": 0, "claimed_product_RHS": -3},
        "randomness": "one exact fair policy bit enumerated; no Monte Carlo or seed selection",
        "cpu_seconds": time.process_time()-start,
        "proof_sha256": hashlib.sha256((ROOT/"theory/phase3_adaptive_replacement.md").read_bytes()).hexdigest()}
    # Full transcript laws retained as rational strings.
    transcript = [{"policy_bit": seed, "outcomes": h, "B": str(B[seed, h]), "D": str(D[seed, h]), "equal_prefix_mass": str(equal[seed, h])} for seed, h in sorted(B)]
    (OUT/"transcripts.json").write_text(json.dumps(transcript, indent=2)+"\n")
    result["transcripts_sha256"] = hashlib.sha256((OUT/"transcripts.json").read_bytes()).hexdigest()
    (OUT/"receipt.json").write_text(json.dumps(result, indent=2)+"\n")
    manifest = {"schema_version": 2, "claim_id": "P34-independent-adaptive-finite-check",
        "repository": {"commit": result["base_commit"], "dirty": True},
        "command": ["/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python", "experiments/P34_independent_review/check.py"],
        "environment": {"software": [{"name": "Python", "version": platform.python_version()}], "hardware": platform.platform()+" "+platform.machine()},
        "mathematics": {"assertion_tested": result["assertion_tested"], "coefficient_domain": "exact rational numbers (Fraction)",
            "conventions": "Halved TV; all ten Fock outcomes; a policy random bit is part of the transcript; stopped histories absorb",
            "inputs": [str(p.relative_to(ROOT)) for p in input_paths], "bounds": {"T": 3, "m": 4, "k": 2, "transcript_states": len(B)},
            "non_claims": ["No universal theorem follows from finite checks", "No timing or hardware advantage", "No QPU"]},
        "randomness": {"used": False, "generator": "Exact enumeration of policy bit", "seed": None},
        "run": {"started_at": started_at, "runtime_seconds": time.monotonic()-wall_start, "exit_status": 0, "status": "completed",
            "resource_limits": {"memory_bytes": None, "cpu_seconds": 60, "max_cores": 1, "max_threads": 1}},
        "outputs": [{"path": str(p.relative_to(ROOT)), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "kind": "result"} for p in (OUT/"receipt.json", OUT/"transcripts.json")],
        "checks": ["Normalized exact laws", "Equal-prefix submeasure dominated by B", "Product and E_B bounds", "Stopping success event", "Initial-only control", "Missing e_t domain counterexample"],
        "result": "All restricted finite implications passed; literal missing-range counterexample retained",
        "residual_risks": ["Finite check is not proof; source and coupling audit are separate"],
        "input_artifacts": [{"path": str(p.relative_to(ROOT)), "sha256": before, "sha256_after": hashlib.sha256(p.read_bytes()).hexdigest()} for p, before in zip(input_paths, input_hashes)],
        "declared_results": DECLARED_RESULTS}
    assert all(p["sha256"] == p["sha256_after"] for p in manifest["input_artifacts"])
    (OUT/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    run()
