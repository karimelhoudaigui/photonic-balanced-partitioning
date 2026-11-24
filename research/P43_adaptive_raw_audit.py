"""Independent stdlib-only audit of saved P43 data; does not run the physics."""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import subprocess

REVISION = "c062f2fcf48a83f301742900e53a8e8759a29d3e"
OPTICAL = ("bosonic", "distinguishable", "phase_field", "species4")
CLASSICAL = ("uniform", "two_swap", "swap_descent", "anneal", "spectral_swap")


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def frozen(root, path):
    return subprocess.check_output(["git", "-C", str(root), "show", f"{REVISION}:{path}"])


def seed(*parts):
    blob = "/".join(str(p) for p in parts).encode()
    return int.from_bytes(hashlib.sha256(blob).digest()[:4], "little")


def score(adjacency, subset):
    # Independent edge-crossing loop; not the production matrix slicing path.
    selected = set(subset)
    return sum(int(adjacency[i][j]) for i in range(len(adjacency))
               for j in range(i+1, len(adjacency)) if (i in selected) != (j in selected))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, run = args.root.resolve(), args.run.resolve()
    manifest = json.loads((run/"manifest.json").read_text())
    summary = json.loads((run/"summary.json").read_text())
    contexts = json.loads((run/"contexts.json").read_text())
    selection = json.loads((run/"selection.json").read_text())
    spec = json.loads(frozen(root, "research/P43_execution_spec.json"))
    assert manifest["repository"]["commit"] == REVISION
    assert manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    assert not manifest["run"]["missing_results"] and not manifest["run"]["invalid_results"]
    for item in manifest["input_artifacts"]:
        observed = digest(frozen(root, item["path"]))
        assert observed == item["sha256"] == item["sha256_after"], item["path"]
    for item in manifest["outputs"]:
        assert digest((root/item["path"]).read_bytes()) == item["sha256"], item["path"]
    assert selection["code_sha256_before_probe"] == digest(frozen(root, "research/P43_global_gain_probe.py"))
    assert selection["spec_sha256_before_probe"] == digest(frozen(root, "research/P43_execution_spec.json"))

    raw = (run/"raw.jsonl").read_bytes()
    groups = defaultdict(list)
    anchor_rows = defaultdict(list)
    prefix = hashlib.sha256()
    probes_started = False
    first_probe_line = None
    line_count = 0
    for line_count, line in enumerate(raw.splitlines(keepends=True), 1):
        row = json.loads(line)
        if row["stage"] == "fresh_relabel":
            if not probes_started:
                first_probe_line = line_count
            probes_started = True
        else:
            assert not probes_started, "non-probe data after probe stage"
            prefix.update(line)
        if row["stage"] == "common_anchor":
            anchor_rows[row["case"]].append(row)
        else:
            groups[(row["stage"], row["case"], row["model"], row.get("theta"))].append(row)
    assert prefix.hexdigest() == selection["development_raw_prefix_sha256"]

    cases = {case["id"]: case for case in spec["cases"]}
    anchors = {}
    matrices = {}
    for graph_id, case in cases.items():
        adjacency = contexts[f"{graph_id}:0"]["adjacency"]
        matrices[graph_id] = adjacency
        m, k = case["m"], case["k"]
        assert len(adjacency) == m and all(len(row) == m for row in adjacency)
        assert all(adjacency[i][j] == adjacency[j][i] for i in range(m) for j in range(m))
        assert all(adjacency[i][i] == 0 for i in range(m))
        scans = defaultdict(list)
        for row in anchor_rows[graph_id]:
            scans[row["scan"]].append(row)
        assert sorted(scans) == list(range(len(scans))) and len(scans) <= spec["anchor_max_scans"]
        source = {row["removed"] for row in scans[0]}
        initial = current = score(adjacency, source)
        trace = [{"source": sorted(source), "cut": current}]
        certified = False
        for scan in range(len(scans)):
            rows = scans[scan]
            assert len(source) == k and len(rows) == k*k
            expected_pairs = {(i, j) for i in source for j in range(m) if j not in source}
            assert {(row["removed"], row["added"]) for row in rows} == expected_pairs
            for row in rows:
                candidate = (source-{row["removed"]})|{row["added"]}
                assert row["cut"] == score(adjacency, candidate)
                assert row["delta"] == row["cut"]-current
            best = min(rows, key=lambda row: (row["cut"], row["removed"], row["added"]))
            if best["cut"] >= current:
                assert scan == len(scans)-1
                certified = True
            else:
                source = (source-{best["removed"]})|{best["added"]}
                current = best["cut"]
                trace.append({"source": sorted(source), "cut": current,
                              "removed": best["removed"], "added": best["added"]})
        anchor = {"initial_cut": initial, "final_cut": current,
                  "candidate_scores_including_initial": 1+len(anchor_rows[graph_id]),
                  "max_scans": spec["anchor_max_scans"],
                  "one_swap_local_minimum_certified": certified,
                  "stopping_reason": "exhaustive_no_strict_improvement" if certified else "scan_cap",
                  "trace": trace, "source_order": sorted(source)}
        for key, value in anchor.items():
            assert summary["common_anchor_ledger"][graph_id][key] == value, (graph_id, key)
        for rep in spec["trial_seeds"]:
            context = contexts[f"{graph_id}:{rep}"]
            assert context["adjacency"] == adjacency and context["source_order"] == sorted(source)
            assert context["initial_cut"] == current
            assert sorted(context["species_order"]) == sorted(source)
            assert context["species_order"] == contexts[f"{graph_id}:0"]["species_order"]
        anchors[graph_id] = anchor

    summary_groups = {(r["stage"], r["case"], r["model"], r.get("theta")): r
                      for r in summary["records"]}
    assert len(summary_groups) == len(summary["records"])
    reconstructed = []
    theta_gain = {model: [0]*len(spec["theta_grid"]) for model in OPTICAL}
    aggregate = defaultdict(lambda: {"attempts_or_scores": 0, "feasible": 0,
                                   "collisions": 0, "gain_sum": 0, "improving_draws": 0})
    for key, rows in sorted(groups.items()):
        stage, case_key, model, theta = key
        graph_id = case_key.split(":")[0]
        adjacency = matrices[graph_id]
        initial = anchors[graph_id]["final_cut"]
        k = cases[graph_id]["k"]
        if stage == "fresh_relabel":
            permutation = contexts[f"{graph_id}:0"]["probe_permutation_new_to_old"]
            assert sorted(permutation) == list(range(len(adjacency)))
            adjacency = [[adjacency[i][j] for j in permutation] for i in permutation]
        expected_seed = (seed(430100, case_key, model, theta) if model in OPTICAL and stage == "development"
                         else seed(430200, case_key, model) if model in OPTICAL
                         else seed(case_key, model) if stage == "development"
                         else seed(case_key, model, "probe"))
        assert {row["seed"] for row in rows} == {expected_seed}, key
        current = {"stage": stage, "case": case_key, "model": model, "theta": theta,
                   "attempts_or_scores": len(rows), "feasible": 0, "collisions": 0,
                   "gain_sum": 0, "improving_draws": 0, "best_cut": initial,
                   "field_fallbacks": 0}
        ordinal = "shot" if model in OPTICAL else "step"
        assert [row[ordinal] for row in rows] == list(range(len(rows))), key
        for row in rows:
            if model in OPTICAL:
                occupation = row["occupation"]
                assert len(occupation) == len(adjacency)
                assert all(isinstance(n, int) and n >= 0 for n in occupation) and sum(occupation) == k
                feasible = all(n <= 1 for n in occupation)
                assert row["feasible"] == feasible
                value = score(adjacency, [i for i, n in enumerate(occupation) if n]) if feasible else None
                assert row["cut"] == value
                gain = max(0, initial-value) if feasible else 0
                assert row["gain"] == gain
                current["field_fallbacks"] += int(row["field_fallback"])
            else:
                subset = row["subset"]
                assert len(set(subset)) == len(subset) == k
                value = score(adjacency, subset)
                assert row["cut"] == value
                feasible, gain = True, max(0, initial-value)
            current["feasible"] += int(feasible)
            current["collisions"] += int(not feasible)
            current["gain_sum"] += gain
            current["improving_draws"] += int(gain > 0)
            current["best_cut"] = min(current["best_cut"], value if value is not None else initial)
            if model in CLASSICAL:
                assert row["best_cut"] == current["best_cut"]
        saved = summary_groups[key]
        assert saved["initial_cut"] == initial and saved["best_cut"] == current["best_cut"]
        if model in OPTICAL:
            assert len(rows) == (spec["draws_per_theta"] if stage == "development" else spec["probe_draws"])
            for left, right in (("attempts", "attempts_or_scores"), ("feasible_scores", "feasible"),
                                ("collisions", "collisions"), ("sum_gain", "gain_sum"),
                                ("improving_draws", "improving_draws"), ("field_fallbacks", "field_fallbacks")):
                assert saved[left] == current[right], (key, left)
            assert abs(saved["mean_gain"]-current["gain_sum"]/len(rows)) < 1e-12
            if stage == "development":
                theta_gain[model][theta] += current["gain_sum"]
        else:
            assert len(rows) == (112 if stage == "development" else 32)
            assert saved["candidate_scores"] == len(rows)
        for metric in aggregate[(stage, model)]:
            aggregate[(stage, model)][metric] += current[metric]
        reconstructed.append(current)

    chosen = {model: values.index(max(values)) if max(values) > 0 else None
              for model, values in theta_gain.items()}
    assert chosen == selection["selected_theta_independently"] == summary["selected_theta_independently"]
    for model in OPTICAL:
        expected_means = [value/spec["draws_per_theta"] for value in theta_gain[model]]
        assert selection["development_total_means"][model] == expected_means
    for graph_id in cases:
        for rep in spec["trial_seeds"]:
            for model in OPTICAL:
                for theta in range(8):
                    assert ("development", f"{graph_id}:{rep}", model, theta) in groups
            for model in CLASSICAL:
                assert ("development", f"{graph_id}:{rep}", model, None) in groups
    synthetic_identity_rows = []
    for graph_id in spec["relabel_case_ids"]:
        for rep in spec["probe_seeds"]:
            case_key = f"{graph_id}:probe{rep}"
            for model in CLASSICAL:
                assert ("fresh_relabel", case_key, model, None) in groups
            for model in OPTICAL:
                saved = summary_groups[("fresh_relabel", case_key, model, chosen[model])]
                if chosen[model] is None:
                    assert saved["identity_selected"] and saved["attempts"] == saved["feasible_scores"] == 0
                    assert saved["best_cut"] == anchors[graph_id]["final_cut"]
                    synthetic_identity_rows.append({"case": case_key, "model": model})
                else:
                    assert saved["covariance_error"] <= 1e-11
    assert len(summary_groups) == len(groups)+len(synthetic_identity_rows)

    decision = "REJECT_TESTED_FAMILY_NO_SIGNAL_AT_PILOT_BUDGET" if all(
        chosen[model] is None for model in OPTICAL) else "FOLLOW_UP_REQUIRES_CARD_REVIEW"
    report = {"audit": "independent_stdlib_raw_reconstruction_no_physics_rerun",
              "code_revision": REVISION, "auditor_code_sha256": digest(Path(__file__).read_bytes()),
              "run_manifest_sha256": digest((run/"manifest.json").read_bytes()),
              "raw_sha256": digest(raw), "raw_lines": line_count,
              "manifest_status": manifest["run"]["status"],
              "all_declared_input_output_hashes_checked": True,
              "manifest_repository_dirty": manifest["repository"]["dirty"],
              "selection_prefix_hash_verified": prefix.hexdigest(),
              "first_probe_line": first_probe_line,
              "anchors_reconstructed_from_complete_raw_scans": anchors,
              "aggregates": [dict(stage=stage, model=model, **values)
                             for (stage, model), values in sorted(aggregate.items())],
              "by_case_and_tuple": reconstructed, "theta_raw_gain_totals": theta_gain,
              "selected_theta": chosen, "identity_probe_rows_no_optical_samples": synthetic_identity_rows,
              "gamma_zero_duplicate_pairs": [[0,4],[2,6]],
              "gamma_zero_law_equality": "preproved_not_inferred_from_equal_sample_counts",
              "optical_fresh_seed_and_covariance_probe": "NOT_EXERCISED_ALL_IDENTITIES" if all(
                  v is None for v in chosen.values()) else "recorded_covariance_errors_checked_only",
              "classical_fresh_seeds_verified": True,
              "summary_consistency": "ALL_CHECKED_NUMERIC_FIELDS_MATCH_RAW",
              "decision": decision,
              "scope": "four_unique_development_graphs_fixed_anchor_and_grid_only_no_global_advantage_or_obstruction"}
    with args.output.open("x") as stream:
        json.dump(report, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"decision": decision, "raw_lines": line_count, "aggregates": report["aggregates"],
                      "anchors": {g: {k: a[k] for k in ("initial_cut", "final_cut", "candidate_scores_including_initial")}
                                  for g, a in anchors.items()},
                      "selected_theta": chosen}, indent=2))


if __name__ == "__main__":
    main()
