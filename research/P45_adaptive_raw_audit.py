"""Stdlib-only reconstruction of the saved P45-A pilot, not another experiment."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def score(a, subset):
    selected = set(subset)
    return sum(int(a[i][j]) for i in selected for j in range(len(a)) if j not in selected)


def audit_completion(a, field, k, lam, priority, row, q=None):
    # Naive scalar marginals, independent of the production vector-update code.
    q = (k+1)//2 if q is None else q
    ranks = {i: rank for rank, i in enumerate(priority)}
    selected = set(sorted(range(len(a)), key=lambda i: (-field[i], ranks[i]))[:q])
    assert sorted(selected) == row["seed_vertices"]
    edges = [a[i][j] for i in range(len(a)) for j in range(i+1,len(a)) if a[i][j] > 0]
    scale = sum(edges)/len(edges) if edges else 1.
    calls = 0
    for step in row["completion"]:
        remaining = [i for i in range(len(a)) if i not in selected]
        marginals = {i: sum(a[i])-2*sum(a[i][j] for j in selected) for i in remaining}
        vertex = min(remaining, key=lambda i: (marginals[i]-lam*scale*field[i], ranks[i]))
        calls += len(remaining)
        assert step["vertex"] == vertex
        assert step["candidate_marginals"] == len(remaining)
        assert abs(step["exact_marginal"]-marginals[vertex]) < 1e-10
        assert abs(step["field_biased_marginal"]-(marginals[vertex]-lam*scale*field[vertex])) < 1e-10
        selected.add(vertex)
    assert len(selected) == k and sorted(selected) == row["subset"]
    assert row["cut"] == score(a, selected)
    assert row["marginal_evaluations"] == calls
    assert row["feasible_scores"] == 1 and row["score_units"] == calls+1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    root = run.parents[2]
    manifest = json.loads((run/"manifest.json").read_text())
    summary = json.loads((run/"summary.json").read_text())
    contract = json.loads((root/"research/P45_adaptive_contract.json").read_text())
    assert manifest["run"]["status"] == "completed" and manifest["run"]["exit_status"] == 0
    for item in manifest["input_artifacts"]:
        assert sha(root/item["path"]) == item["sha256"] == item["sha256_after"]
    for item in manifest["outputs"]:
        assert sha(root/item["path"]) == item["sha256"]
    contexts = {case["id"]: json.loads((run/f'context_{case["id"]}.json').read_text())
                for case in contract["cases"]}
    models = contract["models"]+["bosonic_permuted"]
    settings = {model: [0]*8 for model in models}
    batches = defaultdict(lambda: {"proposals": 0, "sum_gain": 0, "score_units": 0, "best_cut": 10**9})
    per_case = defaultdict(lambda: {"proposals": 0, "sum_gain": 0, "score_units": 0, "best_cut": 10**9,
                                    "CF_counts": 0, "collisional_counts": 0, "improving_candidates": 0})
    classical = defaultdict(lambda: {"scores": 0, "best_cut": 10**9})
    anchor_rows, frontend_rows = defaultdict(list), defaultdict(list)
    primary_b = {}
    raw_lines = 0
    with (run/"raw.jsonl").open() as stream:
        for raw_lines, line in enumerate(stream, 1):
            row = json.loads(line)
            case_key = row["case"]
            graph_id = case_key.split(":")[0]
            context = contexts[graph_id]
            a, source = context["adjacency"], context["optical_source_S0"]
            k = len(source)
            if row["stage"] == "common_anchor":
                anchor_rows[graph_id].append(row)
                continue
            if row["stage"] == "frontend_decoder":
                lam, q = row.get("lam", 0), 0 if row["label"] == "pure_greedy" else None
                if row["label"] == "vacuum":
                    net = context["networks"][row["network"]]
                    field = [-mean/sigma for mean,sigma in zip(net["mu"],net["sigma"])]
                else:
                    field = [0.]*len(a)
                audit_completion(a, field, k, lam, context["vertex_priority"], row, q)
                frontend_rows[graph_id].append(row)
                continue
            if row["stage"] == "classical_search":
                group = classical[(case_key,row["model"])]
                ordinal = row.get("score_index",row.get("step"))
                assert ordinal == group["scores"]
                group["scores"] += 1
                assert len(set(row["subset"])) == k and row["cut"] == score(a, row["subset"])
                group["best_cut"] = min(group["best_cut"], context["Cref"], row["cut"])
                assert row["best_cut"] == group["best_cut"]
                continue
            assert row["stage"] == "development"
            model, setting = row["model"], row["setting"]
            lam = contract["decoder_lambda"][setting % 2]
            net = context["networks"][setting//2]
            b_key = (case_key,setting,row["shot"])
            if model == "bosonic_permuted":
                primary = primary_b[b_key]
                assert primary["seed"] == row["seed"] and row["paired_primary"]
                permutation = row["permutation"]
                assert sorted(permutation) == list(range(len(a)))
                field = [primary["field"][i] for i in permutation]
            else:
                field = row["field"]
                assert all(abs(raw/sigma-normalized) < 1e-10 for raw,sigma,normalized in
                           zip(row["raw_field"],net["sigma"],field))
                counts = row["counts"]
                if counts is not None:
                    assert len(counts) == len(a) and sum(counts) == k and all(n >= 0 for n in counts)
                if model in ("bosonic","distinguishable","species4","phase_multinomial"):
                    assert all(abs(raw-(n-mu)) < 1e-10 for raw,n,mu in zip(row["raw_field"],counts,net["mu"]))
                if model == "bosonic":
                    primary_b[b_key] = row
            audit_completion(a, field, k, lam, context["vertex_priority"], row)
            assert row["Cref"] == context["Cref"]
            assert row["gain"] == max(0,context["Cref"]-row["cut"])
            batch = batches[(case_key,model,setting)]
            assert row["shot"] == batch["proposals"]
            for target in (batch,per_case[(case_key,model)]):
                target["proposals"] += 1
                target["sum_gain"] += row["gain"]
                target["score_units"] += row["score_units"]
                target["best_cut"] = min(target["best_cut"],context["Cref"],row["cut"])
            if model != "bosonic_permuted" and row["counts"] is not None:
                field_group = per_case[(case_key,model)]
                cf = all(n <= 1 for n in row["counts"])
                field_group["CF_counts"] += int(cf)
                field_group["collisional_counts"] += int(not cf)
            per_case[(case_key,model)]["improving_candidates"] += int(row["gain"] > 0)
            settings[model][setting] += row["gain"]

    for graph_id, context in contexts.items():
        a = context["adjacency"]
        scans = defaultdict(list)
        for row in anchor_rows[graph_id]:
            scans[row["scan"]].append(row)
        selected = {row["removed"] for row in scans[0]}
        current, initial = score(a,selected),score(a,selected)
        for scan_index in range(len(scans)):
            rows = scans[scan_index]
            expected = {(i,j) for i in selected for j in range(len(a)) if j not in selected}
            assert len(rows) == len(expected) and {(r["removed"],r["added"]) for r in rows} == expected
            for row in rows:
                target = (selected-{row["removed"]})|{row["added"]}
                assert row["cut"] == score(a,target) and row["delta"] == row["cut"]-current
            best = min(rows,key=lambda r:(r["cut"],r["removed"],r["added"]))
            if best["cut"] < current:
                selected = (selected-{best["removed"]})|{best["added"]}
                current = best["cut"]
            else:
                assert scan_index == len(scans)-1
        assert sorted(selected) == context["optical_source_S0"]
        assert context["anchor"]["initial_cut"] == initial and context["anchor"]["final_cut"] == current
        assert context["anchor"]["candidate_scores_including_initial"] == len(anchor_rows[graph_id])+1
        reference = min([current]+[r["cut"] for r in frontend_rows[graph_id]])
        assert context["Cref"] == reference == score(a,context["reference_source"])
        units = len(anchor_rows[graph_id])+1+sum(r["score_units"] for r in frontend_rows[graph_id])
        assert context["frontend_total_score_units"] == units
        assert summary["common_frontend"][graph_id]["frontend_total_score_units"] == units
        assert len(frontend_rows[graph_id]) == 10
    for row in summary["records"]:
        if "setting" in row:
            group = batches[(row["case"],row["model"],row["setting"])]
            for key in ("proposals","sum_gain","score_units","best_cut"):
                assert row[key] == group[key]
            assert row["proposals"] == 4
        else:
            group = classical[(row["case"],row["model"])]
            assert row["candidate_scores"] == group["scores"] and row["best_cut"] == group["best_cut"]
    chosen = {model: values.index(max(values)) if max(values) > 0 else None for model,values in settings.items()}
    assert settings == summary["setting_total_gains"] and chosen == summary["selected_independently"]
    assert len(batches) == 4*2*8*8 and len(classical) == 4*2*3
    totals = {}
    for model in models:
        groups = [value for (case_key,name),value in per_case.items() if name == model]
        totals[model] = {metric: sum(row[metric] for row in groups) for metric in
                         ("proposals","sum_gain","score_units","CF_counts","collisional_counts","improving_candidates")}
        assert totals[model]["proposals"] == 256 and totals[model]["score_units"] == 13952
    for (case_key,model), group in classical.items():
        m = len(contexts[case_key.split(":")[0]]["adjacency"])
        assert group["scores"] == (1376 if m == 16 else 2112)
    report = {"audit_status":"COMPLETED_RAW_RECONSTRUCTION_NO_PHYSICS_RERUN",
              "auditor_code_sha256":sha(Path(__file__)),"raw_sha256":sha(run/"raw.jsonl"),
              "manifest_sha256":sha(run/"manifest.json"),"source_revision":manifest["repository"]["commit"],
              "all_manifest_hashes_match":True,"raw_lines":raw_lines,"totals":totals,
              "selected":chosen,"setting_gains":settings,
              "per_case":[dict(case=case_key,model=model,**values) for (case_key,model),values in sorted(per_case.items())],
              "classical":[dict(case=case_key,model=model,**values) for (case_key,model),values in sorted(classical.items())],
              "frontend":[{"case":g,"source_cut":ctx["anchor"]["final_cut"],"Cref":ctx["Cref"],
                           "units":ctx["frontend_total_score_units"],
                           "best_frontend_labels":[r["label"] for r in frontend_rows[g] if r["cut"] == ctx["Cref"]]}
                          for g,ctx in contexts.items()],
              "decision":"REJECT_P45A_FROZEN_FAMILY_B_ZERO_GAIN", "positive_accepted":False,
              "scope":"four development graphs, fixed source/network/decoder; unrestricted target remains open"}
    with args.output.open("x") as stream:
        json.dump(report,stream,indent=2);stream.write("\n")
    print(json.dumps({"decision":report["decision"],"raw_lines":raw_lines,"totals":totals,
                      "frontend":report["frontend"]},indent=2))


if __name__ == "__main__":
    main()
