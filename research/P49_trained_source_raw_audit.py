"""Post-hoc stdlib consistency audit of the immutable P49 run; no resampling."""
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


def independent_rotation(r,theta,phi):
    c,s=math.cos(theta),math.sin(theta)
    phase=complex(math.cos(phi),math.sin(phi))
    even=[[complex(i==j) for j in range(r)] for i in range(r)]
    odd=[[complex(i==j) for j in range(r)] for i in range(r)]
    for matrix,start in ((even,0),(odd,1)):
        for i in range(start,r-1,2):
            matrix[i][i]=matrix[i+1][i+1]=c
            matrix[i][i+1]=-phase*s;matrix[i+1][i]=phase.conjugate()*s
    return [[sum(even[i][k]*odd[k][j] for k in range(r)) for j in range(r)] for i in range(r)]


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
            elif index==1:
                norm=spectral["laplacian_norm"]; marks=spectral["marks"]
                degree=[sum(row) for row in a]
                eigen_residual=0.
                for column in range(r):
                    for i in range(n):
                        laplacian=(degree[i]*v[i][column]-sum(a[i][j]*v[j][column] for j in range(n)))/norm if norm else 0j
                        value=laplacian+.001*marks[i]*v[i][column]-eigenvalues[column]*v[i][column]
                        eigen_residual=max(eigen_residual,abs(value))
                assert eigen_residual<=3e-12
            else:
                reference=context["networks"][1]
                e=[[complex(x,y) for x,y in zip(real,imag)] for real,imag in zip(reference["v_real"],reference["v_imag"])]
                phi=0. if index==2 else math.pi/2
                rotation=independent_rotation(r,math.pi/4,phi)
                saved_rotation=[[complex(x,y) for x,y in zip(real,imag)] for real,imag in zip(network["source_rotation_real"],network["source_rotation_imag"])]
                assert max(abs(rotation[i][j]-saved_rotation[i][j]) for i in range(r) for j in range(r))<2e-12
                assert max(abs(sum(e[i][b]*rotation[b][a] for b in range(r))-v[i][a]) for i in range(n) for a in range(r))<3e-12
                eigen_residual=None
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
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    started=time.perf_counter();run=Path("experiments/P49_trained_source/run_001")
    manifest=json.loads((run/"manifest.json").read_text());assert manifest["run"]["status"]=="completed"
    observed={r["path"]:hashlib.sha256(Path(r["path"]).read_bytes()).hexdigest()
              for r in manifest["outputs"] if r["kind"]=="result"}
    assert len(observed)==10
    assert all(observed[r["path"]]==r["sha256"] for r in manifest["outputs"] if r["kind"]=="result")
    data=run/"data";summary=json.loads((data/"summary.json").read_text())
    spec=json.loads(Path("research/P49_trained_source_spec.json").read_text())
    assert summary["full_frozen_population_completed"] and summary["selection_frozen_before_evaluation"]
    contexts={p.name[8:-5]:json.loads(p.read_text()) for p in data.glob("context_*.json")}
    assert len(contexts)==4
    stages=Counter();cache={};samples=Counter();collisions=Counter();groups=defaultdict(list)
    gen_times=defaultdict(float);post_times=defaultdict(float);legacy=defaultdict(list)
    common_min={case:min(row["cut"] for row in context["anchor"]["trace"]) for case,context in contexts.items()}
    common_stages={"common_anchor","common_swap","common_spectral_rounding","common_preparation_rounding","frontend_decoder"}
    first_training=None;last_training=first_evaluation=None
    primary_decoders=front_decoders=count_PIT=gaussian_PIT=prep_checks=signed_checks=0

    def cost(case,subset):
        key=(case,tuple(sorted(subset)))
        if key not in cache:
            a=contexts[case]["adjacency"];chosen=set(subset)
            cache[key]=sum(int(a[i][j]) for i in chosen for j in range(len(a)) if j not in chosen)
        return cache[key]

    def decoder(row,context,field,lam,q):
        a=context["adjacency"];n=len(a);k=n//2;rank={v:i for i,v in enumerate(context["vertex_priority"])}
        selected=set(sorted(range(n),key=lambda i:(-field[i],rank[i]))[:q])
        assert sorted(selected)==row["seed_vertices"]
        positive=[x for line in a for x in line if x>0];scale=sum(positive)/len(positive) if positive else 1.
        inspected=0
        for step in row["completion"]:
            remaining=[i for i in range(n) if i not in selected]
            margins={i:sum(a[i])-2*sum(a[i][j] for j in selected) for i in remaining}
            vertex=min(remaining,key=lambda i:(margins[i]-lam*scale*field[i],rank[i]))
            assert vertex==step["vertex"] and margins[vertex]==step["exact_marginal"]
            assert len(remaining)==step["candidate_marginals"]
            assert abs(margins[vertex]-lam*scale*field[vertex]-step["field_biased_marginal"])<1e-10
            inspected+=len(remaining);selected.add(vertex)
        assert sorted(selected)==row["subset"] and len(selected)==k
        assert inspected==row["marginal_evaluations"] and inspected+1==row["score_units"]

    with gzip.open(data/"raw.jsonl.gz","rt") as stream:
        for index,line in enumerate(stream):
            row=json.loads(line);stage=row["stage"];stages[stage]+=1
            case=row["case"];context=contexts[case];n=len(context["adjacency"]);k=n//2
            subset=row.get("subset")
            if stage=="common_anchor":
                source=context["anchor"]["trace"][row["scan"]]["source"]
                subset=sorted((set(source)-{row["removed"]})|{row["added"]})
            assert subset is not None and len(subset)==len(set(subset))==k and cost(case,subset)==row["cut"]
            if stage in common_stages:
                assert first_training is None
                common_min[case]=min(common_min[case],row["cut"])
                rank={v:i for i,v in enumerate(context["vertex_priority"])}
                if stage=="common_spectral_rounding":
                    values=[line[row["column"]] for line in context["spectral"]["rounding_vectors_real"]]
                    sign=-1 if row["direction"]=="top" else 1
                    assert sorted(sorted(range(n),key=lambda i:(sign*values[i],rank[i]))[:k])==row["subset"]
                    signed_checks+=1
                elif stage=="common_preparation_rounding":
                    network=context["networks"][row["basis"]];q=network["one_particle_probabilities"]
                    if row["label"]=="labelled_max_product_assignment":
                        ports=row["assignment_source_ports"];vertices=row["assignment_output_vertices"]
                        assert sorted(ports)==list(range(k)) and sorted(vertices)==row["subset"]
                        assert row["assignment_probability_floor"]==1e-300
                        value=sum(-math.log(max(q[v][port],1e-300)) for v,port in zip(vertices,ports))
                        assert abs(value-row["assignment_negative_log_product"])<1e-10
                        assert sum(x<1e-300 for line in q for x in line)==row["assignment_floor_entries"]
                    else:
                        values=network["mu"] if row["label"]=="mu" else [line[row["source_port"]] for line in q]
                        sign=-1 if row["direction"]=="top" else 1
                        assert sorted(sorted(range(n),key=lambda i:(sign*values[i],rank[i]))[:k])==row["subset"]
                    prep_checks+=1
                elif stage=="frontend_decoder":
                    if row["label"]=="vacuum_mid_PIT":
                        table=context["networks"][row["basis"]]["marginal_pmfs"][row["model"]]
                        field=[.5*line[0]-.5 for line in table];lam=row["lam"];seed_q=(k+1)//2
                    else:
                        field=[0.]*n;lam=0;seed_q=0 if row["label"]=="pure_greedy" else (k+1)//2
                    decoder(row,context,field,lam,seed_q);front_decoders+=1
            elif stage in ("training","evaluation"):
                if stage=="training":
                    assert first_evaluation is None
                    if first_training is None:first_training=index
                    last_training=index
                elif first_evaluation is None:first_evaluation=index
                model=row["model"];policy=spec["policy_grids"][model][row["policy"]]
                assert row["basis"]==policy["basis"] and row["lam"]==policy["lambda"]
                assert row["Cref"]==context["Cref"]
                denominator=max(1,sum(sum(line) for line in context["adjacency"])//2)
                assert denominator==row["weight_denominator"]==context["weight_denominator"]
                assert abs(row["normalized_cut"]-row["cut"]/denominator)<1e-15
                assert row["gain"]==max(0,context["Cref"]-row["cut"])
                namespace=491100 if stage=="training" else 491200
                seed=int.from_bytes(hashlib.sha256(f"{namespace}/{case}/{model}/{row['policy']}/{row['trial']}".encode()).digest()[:4],"little")
                assert seed==row["seed"]
                if stage=="evaluation":
                    assert row["policy"]==summary["selected_policies"][model] and row["trial"] in (0,1)
                else:assert row["trial"]==0
                key=(stage,case,model,row["policy"],row["trial"])
                groups[key].append(row["cut"]);samples[(model,stage)]+=1
                gen_times[key]+=row["observation_generation_wall_seconds"]
                post_times[key]+=row["classical_postprocessing_wall_seconds"]
                assert row["observation_generation_wall_seconds"]>=0 and row["classical_postprocessing_wall_seconds"]>=0
                field=row["field"];assert all(-.5-1e-12<=x<=.5+1e-12 for x in field)
                decoder(row,context,field,row["lam"],(k+1)//2);primary_decoders+=1
                if row["counts"] is not None:
                    counts=row["counts"];assert len(counts)==n and sum(counts)==k and min(counts)>=0
                    collisions[model]+=max(counts)>1
                    table=context["networks"][row["basis"]]["marginal_pmfs"][model]
                    for i,(count,jitter) in enumerate(zip(counts,row["pit_jitter"])):
                        assert 0<=jitter<1
                        assert abs(field[i]-(sum(table[i][:count])+jitter*table[i][count]-.5))<2e-12
                    count_PIT+=1
                elif model=="gaussian_Bcov":
                    variance=context["networks"][row["basis"]]["Gaussian_effective_factor_variance"]
                    for raw,var,value in zip(row["gaussian_raw"],variance,field):
                        if var>0:assert abs(value-(.5*math.erfc(-raw/math.sqrt(2*var))-.5))<2e-12
                        else:assert raw==0
                    gaussian_PIT+=1
            elif stage=="legacy_classical_search":
                legacy[(case,row["model"],row["trial"])].append(row["cut"])
            else:raise AssertionError("Unexpected raw stage")
    assert last_training<first_evaluation and sum(stages.values())<=200000
    assert all(common_min[case]==context["Cref"] for case,context in contexts.items())
    for batch in summary["primary_batches"]:
        key=(batch["stage"],batch["case"],batch["model"],batch["policy"],batch["trial"]);cuts=groups[key]
        assert cuts==batch["cuts"] and sum(cuts)==batch["sum_cuts"] and len(cuts)==batch["proposals"]
        assert abs(gen_times[key]-batch["observation_generation_wall_seconds"])<1e-12
        assert abs(post_times[key]-batch["classical_postprocessing_wall_seconds"])<1e-12
        for clock in ("wall","cpu"):
            total=batch[f"observation_setup_{clock}_seconds"]
            assert abs(total-batch[f"backend_setup_{clock}_seconds"]-batch[f"classical_postprocessing_setup_{clock}_seconds"])<1e-8
    for model,policies in spec["policy_grids"].items():
        losses={}
        for policy in policies:
            values=[]
            for case,context in contexts.items():
                cuts=groups[("training",case,model,policy["id"],0)]
                assert len(cuts)==policy["training_draws"]
                values.append(Fraction(sum(cuts),len(cuts)*context["weight_denominator"]))
            loss=sum(values,Fraction(0))/4;losses[policy["id"]]=loss
            assert str(loss)==summary["training_global_losses"][model][str(policy["id"])]["exact_fraction"]
        assert min(losses,key=lambda i:(losses[i],i))==summary["selected_policies"][model]
        evaluation=[]
        for case,context in contexts.items():
            cuts=[cut for trial in (0,1) for cut in groups[("evaluation",case,model,summary["selected_policies"][model],trial)]]
            assert len(cuts)==32;evaluation.append(Fraction(sum(cuts),32*context["weight_denominator"]))
            training_cuts=[cut for key,values in groups.items() if key[0]=="training" and key[1]==case and key[2]==model for cut in values]
            incumbent=summary["paid_model_specific_incumbents"][model][case]
            train=min([context["Cref"]]+training_cuts);test=min([context["Cref"]]+cuts)
            assert incumbent["paid_training_best_cut"]==train and incumbent["fresh_evaluation_only_best_cut"]==test
            assert incumbent["paid_total_deployment_best_cut"]==min(train,test)
            for label in ("paid_training","fresh_evaluation_only","paid_total_deployment"):
                assert cost(case,incumbent[label+"_best_subset"])==incumbent[label+"_best_cut"]
        assert str(sum(evaluation,Fraction(0))/4)==summary["chosen_policy_fresh_evaluation_normalized_means"][model]["exact_fraction"]
        assert samples[(model,"training")]==samples[(model,"evaluation")]==128
    for row in summary["legacy_baselines"]:
        key=(row["case"],row["model"],row["trial"]);values=legacy[key]
        assert len(values)==row["candidate_scores"]==(3200 if row["case"].startswith("n26") else 5536)
        assert min([contexts[row["case"]]["Cref"]]+values)==row["best_cut"]
    trace_points=0;fast_best={}
    for case,context in contexts.items():
        payload=json.loads((data/f"fast_{case}.json").read_text());result=payload["result"];trace=result["trace"]
        b=[row for row in summary["primary_batches"] if row["case"]==case and row["model"]=="bosonic"]
        classical=sum(row["classical_postprocessing_wall_seconds"]+row["classical_postprocessing_setup_wall_seconds"] for row in b)
        selection=summary["experimental_spending_and_eval_policy_ledgers"]["bosonic"]["selection_wall_seconds"]/4
        grant=context["classical_compute_wall_seconds"]+classical+selection
        assert abs(payload["total_CPU_allowance_including_adapter"]-grant)<1e-12
        assert payload["optical_simulation_setup_or_count_seconds_granted"]==payload["audit_JSON_seconds_granted"]==0
        assert abs(result["cpu_budget_seconds"]-max(0,grant-payload["adapter_cpu_seconds"]))<1e-12
        assert result["wall_budget_seconds"] is None
        cpu=trace["cpu_seconds"];wall=trace["wall_seconds"];cuts=trace["best_cut"];work=trace["proposal_count"]
        assert all(y>=x for x,y in zip(cpu,cpu[1:])) and all(y>=x for x,y in zip(wall,wall[1:]))
        assert all(y<=x for x,y in zip(cuts,cuts[1:])) and all(y>=x for x,y in zip(work,work[1:]))
        subsets=[];n=len(context["adjacency"])
        for packed,cut in zip(trace["best_subset_packbits_little"],cuts):
            subset=[i for i in range(n) if (packed[i//8]>>(i%8))&1]
            assert len(subset)==n//2 and cost(case,subset)==cut;subsets.append(subset)
        eligible=max(i for i,value in enumerate(cpu) if value<=result["cpu_budget_seconds"])
        assert eligible==result["eligible_checkpoint_index"]
        assert cuts[eligible]==result["best_cut"]==payload["eligible_best_cut"]
        assert subsets[eligible]==result["best_subset"]==payload["eligible_best_subset"]
        assert payload["comparison_acceptance_eligible"]==(not (result["early_cap_inconclusive"] or result["early_wall_inconclusive"]))
        trace_points+=len(cuts);fast_best[case]=result["best_cut"]
    diagnostics=geometry_checks(contexts)
    assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest()==sha for path,sha in observed.items())
    receipt={"status":"PASS_READ_ONLY_RAW_TRAIN_EVAL_FAST_CONSISTENCY","new_scientific_experiment":False,
        "source_run":str(run),"result_hashes_before_and_after":observed,"all_inputs_unchanged":True,
        "all_feasible_cuts_independently_recomputed":sum(stages.values()),"distinct_cut_cache_entries":len(cache),
        "stage_counts":dict(stages),"primary_decoders":primary_decoders,"frontend_decoders":front_decoders,
        "count_PIT_fields":count_PIT,"Gaussian_PIT_fields":gaussian_PIT,"preparation_candidates":prep_checks,
        "signed_roundings":signed_checks,"collision_samples":dict(collisions),
        "exact_all_shot_equal_graph_losses_and_selections_match":True,"fresh_evaluation_roles_and_policies_match":True,
        "private_paid_incumbents_match":True,"classical_setup_accounted_and_optical_JSON_excluded":True,
        "FAST_trace_points_checked":trace_points,"FAST_deadline_eligible_best":fast_best,
        "geometry":diagnostics,"wall_seconds":time.perf_counter()-started,
        "non_claims":["No new sampling or independent distribution replication","No statistical positive or interval certificate","Timing consistency does not certify optimized hardware price"]}
    (args.output/"receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({key:value for key,value in receipt.items() if key not in ("result_hashes_before_and_after","geometry")}))


if __name__=="__main__":
    main()
