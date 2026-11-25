"""ROOT audit of sealed P79 records; no science engine or random draws.

Only stored arithmetic, row completeness, hashes, histograms and cost sums
are checked. This is not independent physical-probability replication.
"""
import hashlib
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "research/P79_even_loop_main/run_001"
rows = Counter()
dims, exact, terms, native_counts = {}, {}, defaultdict(list), Counter()
hist, totals = defaultdict(Counter), defaultdict(Counter)
max_photons, zero_counts, branches = Counter(), Counter(), Counter()
max_error = max_error_ratio = max_unitarity = max_reconstruction = 0.0
module_count = 0
hash_mismatches = []
seen_bins = set()
for line in (RUN / "data/records.jsonl").open():
    r = json.loads(line)
    kind = r["kind"]
    rows[kind] += 1
    case = r.get("case")
    if kind == "case_definition":
        assert case not in dims
        dims[case] = len(r["Z"])
        assert Fraction(r["normalizer"]["determinant_Q"]) > 0
        assert all(Fraction(x) > 0 for x in r["normalizer"]["leading_minors"])
    elif kind == "exact_point":
        key = case, tuple(r["occupation"])
        assert key not in exact and r["exact_equal"]
        assert Fraction(r["hafnian_coefficient"]) == Fraction(r["loop_coefficient"])
        exact[key] = r["raw_probability"]
        zero_counts["exact_zero"] += Fraction(r["hafnian_coefficient"]) == 0
    elif kind == "native_runtime":
        m = r["metadata"]
        assert m["threads"] == 1
        assert m["versions"] == {"numpy": "2.4.6", "scipy": "1.17.1",
                                  "perceval-quandela": "1.3.0", "exqalibur": "1.4.2"}
        for name, entry in m["loaded_module_files"].items():
            module_count += 1
            if hashlib.sha256(Path(entry["path"]).read_bytes()).hexdigest() != entry["sha256"]:
                hash_mismatches.append(name)
    elif kind == "native_decomposition":
        max_unitarity = max(max_unitarity, r["left_unitarity_residual"], r["right_unitarity_residual"])
        max_reconstruction = max(max_reconstruction, r["pair_reconstruction_residual"])
    elif kind == "native_amplitude":
        key = case, tuple(r["target"])
        term = complex(*r["coherent_term"])
        assert abs(term - r["source_coefficient"] * complex(*r["native_amplitude"])) < 1e-14
        assert r["source_zero"] == (r["source_coefficient"] == 0)
        terms[key].append(term)
        zero_counts["source_coefficient_zero"] += r["source_zero"]
        zero_counts["native_amplitude_literal_zero"] += complex(*r["native_amplitude"]) == 0
    elif kind == "native_point":
        key = case, tuple(r["occupation"])
        assert native_counts[key] == 0
        native_counts[key] += 1
        assert len(terms[key]) == r["source_terms"]
        assert abs(sum(terms[key]) - complex(*r["coherent_sum"])) < 1e-14
        assert exact[key] == r["reference"]
        err = abs(r["raw_probability"] - r["reference"])
        assert err == r["absolute_error"] and r["passed"] and err <= r["tolerance"]
        max_error = max(max_error, err)
        max_error_ratio = max(max_error_ratio, err / r["tolerance"])
        branches[r["tolerance_branch"]] += 1
        zero_counts["native_reference_zero"] += r["reference_zero"]
        zero_counts["native_probability_literal_zero"] += r["raw_probability"] == 0
    elif kind == "draw":
        t = totals[case]
        assert r["draw"] == t["draws"] + 1 and r["seed"] == 7910000 + int(case[1:])
        assert len(r["counts"]) == dims[case]
        assert all(isinstance(v, int) and v >= 0 for v in r["counts"])
        assert r["total_photons"] == sum(r["counts"]) and r["total_photons"] % 2 == 0
        assert 0 <= r["accepted_loops"] <= r["proposed_loops"]
        assert r["proposed_steps"] >= r["total_photons"]
        assert r["proposed_steps"] >= 2 * r["proposed_loops"]
        key = tuple(r["counts"]) if r["total_photons"] <= 6 else "TAIL_GT6"
        hist[case][key] += 1
        t.update(draws=1, photons=r["total_photons"], steps=r["proposed_steps"],
                 loops=r["proposed_loops"], accepted_loops=r["accepted_loops"])
        max_photons[case] = max(max_photons[case], r["total_photons"])
    elif kind == "descriptive_costs":
        t = totals[case]
        assert r["draws"] == t["draws"] == 20000
        assert r["totals"] == {k: t[k] for k in ("photons", "steps", "loops", "accepted_loops")}
        assert r["observed_mean_photons"] == t["photons"] / t["draws"]
        assert r["observed_mean_proposed_steps"] == t["steps"] / t["draws"]
        assert r["mean_confidence_interval"] is None
    elif kind == "bin":
        occ = r["occupation"] if isinstance(r["occupation"], str) else tuple(r["occupation"])
        key = case, occ
        assert key not in seen_bins
        seen_bins.add(key)
        assert r["count"] == hist[case][occ] and r["trials"] == 20000
        assert r["family_size"] == 272 and r["family_alpha"] == .01
        ref, tol = r["raw_reference"], r["floating_reference_tolerance"]
        assert tol == 1e-12 and 0 <= ref <= 1
        assert r["covered"] == (r["cp_low"] - tol <= ref <= r["cp_high"] + tol)
        assert r["covered"]
        if occ != "TAIL_GT6":
            assert exact[key] == ref
        zero_counts["bin_zero_observed"] += r["count"] == 0
        zero_counts["bin_zero_reference"] += ref == 0
    else:
        raise AssertionError(kind)
assert rows == {"case_definition": 6, "exact_point": 266, "native_runtime": 1,
                "native_decomposition": 6, "native_amplitude": 650, "native_point": 105,
                "draw": 120000, "descriptive_costs": 6, "bin": 272}
assert sum(rows.values()) == 121312 and module_count == 1781 and not hash_mismatches
assert len(terms) == 105 and sum(map(len, terms.values())) == 650
summary = json.loads((RUN / "data/summary.json").read_text())
assert summary["status"] == "FINITE_VALIDATION_PASSED"
assert summary["global_proposed_steps"] == sum(t["steps"] for t in totals.values()) == 105142
assert json.loads((RUN / "data/failure.json").read_text()) is None
record_hash = hashlib.sha256((RUN / "data/records.jsonl").read_bytes()).hexdigest()
assert record_hash == summary["records_sha256"] == "44792b9dc1ad772a9c3651ed6a97c159940b842cf6abea4848ef22f484be1431"
result = {"scope": "stored-row consistency only; no new science engine/RNG/CI quantiles",
          "status": "PASS", "raw_producer_commit": "1286ecf02730cef6aa7ba6938f5f05087f05300d",
          "raw_seal_commit": "b8e8fea16d02c27082d55b2c1ed577193e804fc9",
          "records_sha256": record_hash, "rows": dict(rows), "total_rows": sum(rows.values()),
          "module_files_checked": module_count, "module_hash_mismatches": hash_mismatches,
          "zero_counts": dict(zero_counts), "tolerance_branches": dict(branches),
          "maximum_recorded_absolute_error": max_error, "maximum_error_tolerance_ratio": max_error_ratio,
          "maximum_unitarity_residual": max_unitarity, "maximum_pair_reconstruction_residual": max_reconstruction,
          "by_case": {c: {"totals": dict(totals[c]), "max_photons": max_photons[c],
                          "vacuum": hist[c][(0,) * dims[c]], "tail_gt6": hist[c]["TAIL_GT6"]}
                      for c in sorted(dims)}}
(Path(__file__).parent / "recorded_inspection.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "by_case"}, sort_keys=True))
