"""Post-hoc stdlib consistency audit of the immutable P47 run; no resampling."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from pathlib import Path
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    run=Path("experiments/P47_directed_pit/run_001")
    manifest=json.loads((run/"manifest.json").read_text())
    assert manifest["run"]["status"]=="completed"
    observed={r["path"]:hashlib.sha256(Path(r["path"]).read_bytes()).hexdigest()
              for r in manifest["outputs"] if r["kind"]=="result"}
    assert len(observed)==6
    assert all(observed[r["path"]]==r["sha256"] for r in manifest["outputs"] if r["kind"]=="result")
    data=run/"data"
    summary=json.loads((data/"summary.json").read_text())
    contexts={p.name[8:-5]:json.loads(p.read_text()) for p in data.glob("context_*.json")}
    assert len(contexts)==4
    cache={}; stages=Counter(); samples=Counter(); gains=Counter(); collisions=Counter()
    successes=Counter(); best={}; queries=defaultdict(list)
    setting_gains={model:[0]*8 for model in summary["attempts_per_model"]}
    common_min={case:min(r["cut"] for r in c["anchor"]["trace"]) for case,c in contexts.items()}
    checked=pit_checked=gaussian_checked=decoder_checked=0

    def cost(case,subset):
        key=(case,tuple(sorted(subset)))
        if key not in cache:
            a=contexts[case]["adjacency"]; chosen=set(subset)
            cache[key]=sum(int(a[i][j]) for i in chosen for j in range(len(a)) if j not in chosen)
        return cache[key]

    def decoder_check(row,context):
        a=context["adjacency"]; field=row["field"]; m=len(a); k=m//2; q=(k+1)//2
        priority={v:i for i,v in enumerate(context["vertex_priority"])}
        selected=set(sorted(range(m),key=lambda i:(-field[i],priority[i]))[:q])
        assert sorted(selected)==row["seed_vertices"]
        positive=[x for line in a for x in line if x>0]
        scale=sum(positive)/len(positive) if positive else 1.
        lam=row["setting"]%2; inspected=0
        for step in row["completion"]:
            remaining=[i for i in range(m) if i not in selected]
            margins={i:sum(a[i])-2*sum(a[i][j] for j in selected) for i in remaining}
            chosen=min(remaining,key=lambda i:(margins[i]-lam*scale*field[i],priority[i]))
            assert chosen==step["vertex"] and len(remaining)==step["candidate_marginals"]
            assert margins[chosen]==step["exact_marginal"]
            assert abs(margins[chosen]-lam*scale*field[chosen]-step["field_biased_marginal"])<1e-10
            inspected+=len(remaining); selected.add(chosen)
        assert sorted(selected)==row["subset"] and len(selected)==k
        assert inspected==row["marginal_evaluations"] and inspected+1==row["score_units"]

    with gzip.open(data/"raw.jsonl.gz","rt") as stream:
        for line in stream:
            row=json.loads(line); stages[row["stage"]]+=1
            case=row["case"].split(":")[0]; context=contexts[case]
            m=len(context["adjacency"]); k=m//2; subset=row.get("subset")
            if row["stage"]=="common_anchor":
                source=context["anchor"]["trace"][row["scan"]]["source"]
                subset=sorted((set(source)-{row["removed"]})|{row["added"]})
            assert subset is not None and len(subset)==len(set(subset))==k
            assert cost(case,subset)==row["cut"]; checked+=1
            if row["stage"] in ("common_anchor","common_swap","frontend_decoder"):
                common_min[case]=min(common_min[case],row["cut"])
            elif row["stage"]=="development":
                model=row["model"]; samples[model]+=1
                gain=max(0,context["Cref"]-row["cut"])
                assert row["Cref"]==context["Cref"] and row["gain"]==gain
                gains[model]+=gain; successes[model]+=gain>0
                setting_gains[model][row["setting"]]+=gain
                assert all(-.5-1e-12<=x<=.5+1e-12 for x in row["field"])
                decoder_check(row,context); decoder_checked+=1
                network=context["networks"][row["setting"]//2]
                if row["counts"] is not None:
                    counts=row["counts"]
                    assert len(counts)==m and sum(counts)==k and min(counts)>=0
                    assert all(counts[i] in (0,1) for i in context["inside_order"])
                    assert row["transferred"]==sum(counts[i] for i in context["outside_order"])
                    collisions[model]+=max(counts)>1
                    table=network["marginal_pmfs"][model]
                    for i,(count,jitter) in enumerate(zip(counts,row["pit_jitter"])):
                        assert 0<=jitter<1
                        value=sum(table[i][:count])+jitter*table[i][count]-.5
                        assert abs(row["field"][i]-value)<2e-12
                    pit_checked+=1
                elif model=="gaussian_Bcov":
                    for raw,variance,field in zip(row["gaussian_raw"],network["Gaussian_effective_factor_variance"],row["field"]):
                        assert variance>0
                        assert abs(field-(.5*math.erfc(-raw/math.sqrt(2*variance))-.5))<2e-12
                    gaussian_checked+=1
                key=(case,model); best[key]=min(best.get(key,context["Cref"]),row["cut"])
            elif row["stage"]=="classical_search":
                queries[(row["case"],row["model"])].append((row["baseline_elapsed_seconds"],row["cut"]))
            else:
                raise AssertionError("Unknown raw stage")
    assert dict(samples)==summary["attempts_per_model"]
    assert sum(stages.values())<=200000
    assert all([float(x) for x in setting_gains[model]]==summary["setting_total_gains"][model] for model in setting_gains)
    assert all(common_min[case]==c["Cref"] for case,c in contexts.items())
    for record in summary["records"]:
        if record.get("stage")!="classical_search":
            continue
        case=record["case"].split(":")[0]; cref=contexts[case]["Cref"]
        rows=queries[(record["case"],record["model"])]
        expected=3200 if case.startswith("n26") else 5536
        assert len(rows)==record["candidate_scores"]==expected
        assert record["best_cut"]==min([cref]+[value for _,value in rows])
        for frontier in record["joint_observed_time_frontiers"].values():
            within=[value for elapsed,value in rows if elapsed<=frontier["observed_model_seconds"]]
            assert len(within)==frontier["baseline_scores_within_time_and_score_caps"]
            assert min([cref]+within)==frontier["best_cut_within_joint_caps"]
    diagnostics={}
    for case,context in contexts.items():
        delta=context["delta_swap"]; k=len(delta); inside=context["inside_order"]; outside=context["outside_order"]
        diagnostic=[]
        for network in context["networks"]:
            # Independent graph-index reconstruction of the physical W intensity.
            total=0.
            for i,old in enumerate(inside):
                for j,new in enumerate(outside):
                    intensity=(network["u_real"][old][new]**2+network["u_imag"][old][new]**2)/network["p"]
                    total+=delta[i][j]*(intensity-1/k)
            normalized=network["normalized_proxy_after"]-network["normalized_proxy_before"]
            assert abs(total-network["centered_delta_norm"]*normalized)<1e-9
            assert normalized<=network["finite_proxy_decrease_bound"]+3e-11
            for model,table in network["marginal_pmfs"].items():
                assert all(min(row)>=0 and abs(sum(row)-1)<2e-12 for row in table)
            hist=network["phase_calibration"]["histogram"]
            assert all(sum(row)==4096 for row in hist)
            diagnostic.append({"p":network["p"],"guided":network["guided"],
                "normalized_proxy_change":normalized,"W_minus_F_frobenius_squared":network["W_minus_F_frobenius_squared"],
                "proxy_tangent_frobenius_squared":network["proxy_tangent_frobenius_squared"]})
        diagnostics[case]=diagnostic
    assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha for path,sha in observed.items())
    receipt={"status":"PASS_READ_ONLY_RAW_CONSISTENCY","new_scientific_experiment":False,
        "source_run":str(run),"primary_results_sha256_before_and_after":observed,
        "all_inputs_unchanged":True,"all_feasible_cuts_independently_recomputed":checked,
        "distinct_cut_cache_entries":len(cache),"stage_counts":dict(stages),"sample_counts":dict(samples),
        "all_settings_total_gain":dict(gains),"positive_improvement_events":dict(successes),
        "collision_samples":dict(collisions),"saved_PIT_count_fields_reconstructed":pit_checked,
        "saved_Gaussian_factor_PIT_fields_reconstructed":gaussian_checked,
        "full_decoders_independently_reconstructed":decoder_checked,
        "all_classical_query_counts_and_time_frontiers_match":True,"common_incumbents_match":True,
        "routing_proxy_diagnostics":diagnostics,"wall_seconds":time.perf_counter()-started,
        "non_claims":["No resampling or independent distribution replication","No theorem or statistical positive acceptance","Score units count informative evaluations; known initial cuts can be recomputed inside measured wall time","No numerical interval or joint empirical-PIT certificate"]}
    (args.output/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k not in ("primary_results_sha256_before_and_after","routing_proxy_diagnostics")}))


if __name__=="__main__":
    main()
