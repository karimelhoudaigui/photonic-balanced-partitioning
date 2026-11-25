"""Post-hoc stdlib consistency audit of the immutable P48 run; no resampling."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
import time


def geometry_checks(contexts):
    """Independent scalar complex arithmetic; no NumPy/eigensolver/sampler."""
    diagnostics={}
    for case,context in contexts.items():
        assert context["numerical_status"]=="PASS"
        a=context["adjacency"]; n=len(a); r=n//2
        spectral=context["spectral"]; eigenvalues=spectral["eigenvalues"]
        assert all(abs((y-x)-gap)<1e-15 for x,y,gap in zip(eigenvalues,eigenvalues[1:],spectral["all_gaps"]))
        assert len(spectral["all_gaps"])==n-1 and len(spectral["guarded_gaps"])==r
        assert min(spectral["guarded_gaps"])>1e-12
        result=[]
        for index,network in enumerate(context["networks"]):
            v=[[complex(x,y) for x,y in zip(real,imag)] for real,imag in zip(network["v_real"],network["v_imag"])]
            u=[[complex(x,y) for x,y in zip(real,imag)] for real,imag in zip(network["u_real"],network["u_imag"])]
            assert network["source_ports"]==list(range(r))
            assert max(abs(u[i][j]-v[i][j]) for i in range(n) for j in range(r))==0
            residual=max(abs(sum(u[k][i].conjugate()*u[k][j] for k in range(n))-(i==j))
                         for i in range(n) for j in range(n))
            assert residual<=3e-12
            q=network["one_particle_probabilities"]; mu=network["mu"]
            assert max(abs(abs(v[i][j])**2-q[i][j]) for i in range(n) for j in range(r))<2e-12
            assert max(abs(sum(q[i])-mu[i]) for i in range(n))<2e-12
            offdiagonal=0.; covariance_residual=0.
            for i in range(n):
                for j in range(n):
                    gram=sum(v[i][column]*v[j][column].conjugate() for column in range(r))
                    saved=complex(network["projector_real"][i][j],network["projector_imag"][i][j])
                    assert abs(gram-saved)<3e-12
                    if i!=j:
                        offdiagonal+=abs(gram)**2
                    covariance=(mu[i] if i==j else 0)+abs(gram)**2-2*sum(q[i][column]*q[j][column] for column in range(r))
                    covariance_residual=max(covariance_residual,abs(covariance-network["covariance_B"][i][j]))
            assert covariance_residual<3e-12
            assert abs(offdiagonal-network["projector_offdiagonal_frobenius_squared"])<1e-10
            if network["encoder"]=="Fourier_blind":
                order=context["fourier_vertex_order"]
                assert max(abs(v[vertex][column]-complex(math.cos(2*math.pi*row*column/n),math.sin(2*math.pi*row*column/n))/math.sqrt(n))
                           for row,vertex in enumerate(order) for column in range(r))<3e-12
                eigen_residual=None
            else:
                norm=spectral["laplacian_norm"]; marks=spectral["marks"]
                degree=[sum(row) for row in a]
                eigen_residual=0.
                for column in range(r):
                    for i in range(n):
                        laplacian=(degree[i]*v[i][column]-sum(a[i][j]*v[j][column] for j in range(n)))/norm if norm else 0j
                        value=laplacian+.001*marks[i]*v[i][column]-eigenvalues[column]*v[i][column]
                        eigen_residual=max(eigen_residual,abs(value))
                assert eigen_residual<=3e-12
            repairs=network["marginal_diagnostics"]["row_repairs"]
            repair_max=max(float(Fraction(row["input_roundoff_repair_L1"])) for row in repairs)
            assert repair_max<=3e-12 and all(not row["subunit_row_rescaled_to1"] for row in repairs)
            for table in network["marginal_pmfs"].values():
                for i,row in enumerate(table):
                    assert min(row)>=0 and abs(sum(row)-1)<2e-12
                    assert abs(sum(k*p for k,p in enumerate(row))-float(Fraction(repairs[i]["used_mu"])))<3e-12
            result.append({"encoder":network["encoder"],"independent_unitary_residual":residual,
                "independent_source_eigen_residual":eigen_residual,"max_probability_row_repair_L1":repair_max,
                "independent_covariance_residual":covariance_residual,
                "projector_offdiagonal_frobenius_squared":network["projector_offdiagonal_frobenius_squared"],
                "Gaussian_variance_residual":network["Gaussian_variance_residual"],
                "Gaussian_empty_rows":network["Gaussian_structurally_empty_rows"],
                "Gaussian_occupied_deterministic_rows":network["Gaussian_structurally_occupied_deterministic_rows"]})
        diagnostics[case]={"minimum_guarded_gap":min(spectral["guarded_gaps"]),"encoders":result}
    return diagnostics


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter()
    run=Path("experiments/P48_spectral_pit/run_001")
    manifest=json.loads((run/"manifest.json").read_text())
    assert manifest["run"]["status"]=="completed"
    observed={r["path"]:hashlib.sha256(Path(r["path"]).read_bytes()).hexdigest()
              for r in manifest["outputs"] if r["kind"]=="result"}
    assert len(observed)==6
    assert all(observed[r["path"]]==r["sha256"] for r in manifest["outputs"] if r["kind"]=="result")
    data=run/"data"
    summary=json.loads((data/"summary.json").read_text())
    assert summary["full_frozen_population_completed"]
    contexts={p.name[8:-5]:json.loads(p.read_text()) for p in data.glob("context_*.json")}
    assert len(contexts)==4
    cache={}; stages=Counter(); samples=Counter(); gains=Counter(); collisions=Counter()
    successes=Counter(); best={}; queries=defaultdict(list)
    setting_gains={model:[0]*4 for model in summary["attempts_per_model"]}
    common_min={case:min(r["cut"] for r in c["anchor"]["trace"]) for case,c in contexts.items()}
    checked=pit_checked=gaussian_checked=decoder_checked=frontend_decoder_checked=0
    preparation_checked=spectral_rounding_checked=0
    common_witnesses=defaultdict(list)

    def cost(case,subset):
        key=(case,tuple(sorted(subset)))
        if key not in cache:
            a=contexts[case]["adjacency"]; chosen=set(subset)
            cache[key]=sum(int(a[i][j]) for i in chosen for j in range(len(a)) if j not in chosen)
        return cache[key]

    def decoder_check(row,context,q_override=None,lam_override=None):
        a=context["adjacency"]; field=row["field"]; m=len(a); k=m//2
        q=(k+1)//2 if q_override is None else q_override
        priority={v:i for i,v in enumerate(context["vertex_priority"])}
        selected=set(sorted(range(m),key=lambda i:(-field[i],priority[i]))[:q])
        assert sorted(selected)==row["seed_vertices"]
        positive=[x for line in a for x in line if x>0]
        scale=sum(positive)/len(positive) if positive else 1.
        lam=row["setting"]%2 if lam_override is None else lam_override
        inspected=0
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
            if row["stage"] in ("common_anchor","common_swap","frontend_decoder","common_spectral_rounding","common_preparation_rounding"):
                common_min[case]=min(common_min[case],row["cut"])
                if row["cut"]==context["Cref"]:
                    common_witnesses[case].append({"stage":row["stage"],"label":row.get("label"),
                        "encoder":row.get("encoder"),"column":row.get("column"),"direction":row.get("direction")})
                priority={vertex:i for i,vertex in enumerate(context["vertex_priority"])}
                if row["stage"]=="common_spectral_rounding":
                    values=[line[row["column"]] for line in context["spectral"]["rounding_vectors_real"]]
                    sign=-1 if row["direction"]=="top" else 1
                    expected=sorted(sorted(range(m),key=lambda i:(sign*values[i],priority[i]))[:k])
                    assert expected==row["subset"]; spectral_rounding_checked+=1
                elif row["stage"]=="common_preparation_rounding":
                    network=context["networks"][row["encoder"]]; q=network["one_particle_probabilities"]
                    if row["label"]=="labelled_max_product_assignment":
                        ports=row["assignment_source_ports"]; vertices=row["assignment_output_vertices"]
                        assert sorted(ports)==list(range(k)) and sorted(vertices)==row["subset"]
                        assert row["assignment_probability_floor"]==1e-300
                        value=sum(-math.log(max(q[vertex][port],1e-300)) for vertex,port in zip(vertices,ports))
                        assert abs(value-row["assignment_negative_log_product"])<1e-10
                        assert sum(x<1e-300 for line in q for x in line)==row["assignment_floor_entries"]
                    else:
                        values=network["mu"] if row["label"]=="mu" else [line[row["source_port"]] for line in q]
                        sign=-1 if row["direction"]=="top" else 1
                        expected=sorted(sorted(range(m),key=lambda i:(sign*values[i],priority[i]))[:k])
                        assert expected==row["subset"]
                    preparation_checked+=1
                elif row["stage"]=="frontend_decoder":
                    if row["label"]=="vacuum_mid_PIT":
                        table=context["networks"][row["encoder"]]["marginal_pmfs"][row["model"]]
                        field=[.5*line[0]-.5 for line in table]; lam=row["lam"]; seed_q=(k+1)//2
                    else:
                        field=[0.]*m; lam=0; seed_q=0 if row["label"]=="pure_greedy" else (k+1)//2
                    decoder_check(dict(row,field=field),context,seed_q,lam)
                    frontend_decoder_checked+=1
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
                    collisions[model]+=max(counts)>1
                    table=network["marginal_pmfs"][model]
                    for i,(count,jitter) in enumerate(zip(counts,row["pit_jitter"])):
                        assert 0<=jitter<1
                        value=sum(table[i][:count])+jitter*table[i][count]-.5
                        assert abs(row["field"][i]-value)<2e-12
                    pit_checked+=1
                elif model=="gaussian_Bcov":
                    for raw,variance,field in zip(row["gaussian_raw"],network["Gaussian_effective_factor_variance"],row["field"]):
                        if variance>0:
                            assert abs(field-(.5*math.erfc(-raw/math.sqrt(2*variance))-.5))<2e-12
                        else:
                            assert raw==0 and -.5<=field<=.5
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
    diagnostics=geometry_checks(contexts)
    assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha for path,sha in observed.items())
    receipt={"status":"PASS_READ_ONLY_RAW_CONSISTENCY","new_scientific_experiment":False,
        "source_run":str(run),"primary_results_sha256_before_and_after":observed,
        "all_inputs_unchanged":True,"all_feasible_cuts_independently_recomputed":checked,
        "distinct_cut_cache_entries":len(cache),"stage_counts":dict(stages),"sample_counts":dict(samples),
        "all_settings_total_gain":dict(gains),"positive_improvement_events":dict(successes),
        "collision_samples":dict(collisions),"saved_PIT_count_fields_reconstructed":pit_checked,
        "saved_Gaussian_factor_PIT_fields_reconstructed":gaussian_checked,
        "full_decoders_independently_reconstructed":decoder_checked,
        "frontend_decoders_independently_reconstructed":frontend_decoder_checked,
        "direct_preparation_candidates_verified":preparation_checked,
        "signed_spectral_roundings_verified":spectral_rounding_checked,
        "Cref_witnesses":dict(common_witnesses),
        "all_classical_query_counts_and_time_frontiers_match":True,"common_incumbents_match":True,
        "spectral_geometry_diagnostics":diagnostics,"wall_seconds":time.perf_counter()-started,
        "non_claims":["No resampling or independent distribution replication","No theorem or statistical positive acceptance","Score units count informative evaluations; known initial cuts can be recomputed inside measured wall time","No numerical interval or joint empirical-PIT certificate"]}
    (args.output/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k not in ("primary_results_sha256_before_and_after","spectral_geometry_diagnostics")}))


if __name__=="__main__":
    main()
