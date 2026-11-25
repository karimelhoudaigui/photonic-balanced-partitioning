"""P49 prospective training on ALL feasible cuts, then fresh fixed-policy DEV.

Imports P48 and FAST helpers unchanged. No optimum, QPU or accepted positive.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from fractions import Fraction
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.special import ndtr

import P48_spectral_pit_probe as p48
import P49_fast_classical as fast

base=p48.base
adaptive=p48.adaptive
MODELS=("bosonic","distinguishable","species4","gaussian_Bcov",
        "continuous_phase","spherical_coherent","iid_uniform")
BASES=("Fourier_blind","spectral_E","spectral_R_phi0","spectral_R_phi90")
LEGACY=tuple(p48.BASELINES)


def emit(stream,row):
    stream.write(json.dumps(row,allow_nan=False)+"\n")


class ComputeMeter:
    """Wall/CPU of explicitly bracketed compute; raw/context JSON is outside."""
    def __init__(self):
        self.wall=self.cpu=0.
    @contextmanager
    def measure(self):
        started_wall,started_cpu=time.perf_counter(),time.process_time()
        try:
            yield
        finally:
            self.wall+=time.perf_counter()-started_wall
            self.cpu+=time.process_time()-started_cpu


def two_mode(theta,phi):
    c,s=math.cos(theta),math.sin(theta)
    return np.asarray([[c,-np.exp(1j*phi)*s],[np.exp(-1j*phi)*s,c]],dtype=complex)


def source_rotation(r,theta,phi):
    """R=G_even @ G_odd; rightmost odd layer acts FIRST on the source."""
    even=np.eye(r,dtype=complex); odd=np.eye(r,dtype=complex)
    g=two_mode(theta,phi)
    for first in range(0,r-1,2):
        pair=[first,first+1]; even[np.ix_(pair,pair)]=g
    for first in range(1,r-1,2):
        pair=[first,first+1]; odd[np.ix_(pair,pair)]=g
    return even@odd


def policies(model):
    if model not in MODELS:
        raise ValueError(model)
    bases=[None] if model=="iid_uniform" else ([0,1] if model=="spherical_coherent" else list(range(4)))
    draws=16 if model=="iid_uniform" else (8 if model=="spherical_coherent" else 4)
    return [{"id":index,"basis":basis,"lambda":lam,"training_draws":draws}
            for index,(basis,lam) in enumerate((basis,lam) for basis in bases for lam in (0,1))]


def total_weight(a):
    return max(1,int(np.triu(a,1).sum()))


def select_policies(training,cases,model_subset=MODELS):
    """Exact equally weighted graph means of ALL normalized feasible cuts.

    This function has no evaluation argument, incumbent/optimum mask or gain.
    Missing graphs/policies are errors, never an accepted surviving subset.
    """
    if not cases or any(row.get("stage","training")!="training" for row in training):
        raise ValueError("Selection accepts training rows on a nonempty population only")
    selected={}; losses={}
    case_ids=[case["id"] for case in cases]
    if len(case_ids)!=len(set(case_ids)) or any(model not in MODELS for model in model_subset):
        raise ValueError("Invalid selection population/model")
    denominators={case["id"]:case.get("weight_denominator") for case in cases}
    for model in model_subset:
        loss_by_policy={}
        for policy in policies(model):
            rows=[row for row in training if row["model"]==model and row["policy"]==policy["id"]]
            if sorted(row["case"] for row in rows)!=sorted(case_ids):
                raise ValueError("Training policy does not cover every frozen graph exactly once")
            values=[]
            for row in rows:
                if row["proposals"]!=policy["training_draws"]:
                    raise ValueError("Training allocation changed")
                expected=denominators[row["case"]]
                if expected is not None and row["weight_denominator"]!=expected:
                    raise ValueError("Graph-weight normalization changed")
                values.append(Fraction(row["sum_cuts"],row["proposals"]*row["weight_denominator"]))
            loss_by_policy[policy["id"]]=sum(values,Fraction(0))/len(cases)
        winner=min(loss_by_policy,key=lambda i:(loss_by_policy[i],i))
        selected[model]=winner
        losses[model]={str(i):{"exact_fraction":str(value),"float":float(value)} for i,value in loss_by_policy.items()}
    return selected,losses


def charged_anchor(a,seed,scans,meter,stream,case_id):
    """Same capped best-swap rule as P43, with JSON OUTSIDE compute clocks."""
    with meter.measure():
        rng=np.random.default_rng(seed); n=len(a); k=n//2
        source=set(rng.choice(n,k,replace=False).tolist()); current=base.cut(a,source)
        initial=current; trace=[{"source":sorted(source),"cut":current}]
        count=1; certified=False
    for scan in range(scans):
        with meter.measure():
            candidates=[]
            for old in sorted(source):
                for new in range(n):
                    if new not in source:
                        subset=(source-{old})|{new}; value=base.cut(a,subset)
                        candidates.append((value,old,new,subset)); count+=1
            previous=current
            value,old,new,subset=min(candidates,key=lambda row:row[:3])
            if value>=current:
                certified=True
            else:
                source,current=set(subset),value
                trace.append({"source":sorted(source),"cut":current,"removed":old,"added":new})
        for value,old,new,_ in candidates:
            emit(stream,{"stage":"common_anchor","case":case_id,"scan":scan,
                         "removed":old,"added":new,"cut":value,"delta":value-previous})
        if certified:
            break
    return sorted(source),{"initial_cut":initial,"final_cut":current,
        "candidate_scores_including_initial":count,"max_scans":scans,
        "one_swap_local_minimum_certified":certified,
        "stopping_reason":"exhaustive_no_strict_improvement" if certified else "scan_cap",
        "trace":trace}


def observation_components(context,model,seed):
    """Backend/count timing and PIT/postprocessing are measured separately."""
    roles=("PIT_jitter","raw_noise","physical_counts","coherent_counts")
    seeds=[base.seed_for(seed,role) for role in roles]
    if len(set(seeds))!=len(seeds):
        raise ArithmeticError("RNG role collision")
    n=context["v"].shape[0] if context is not None else None
    jitter_rng=np.random.default_rng(seeds[0]); noise_rng=np.random.default_rng(seeds[1])
    if model in ("bosonic","distinguishable","species4"):
        r=context["v"].shape[1]
        primitive,_=base.make_optical_sampler(context["u"],list(range(r)),model,seeds[2])
        sample=lambda:(primitive()[0],{})
    elif model in ("continuous_phase","spherical_coherent"):
        sample=p48.coherent_counts(context,model,seeds[3])
    elif model=="gaussian_Bcov":
        sample=lambda:(context["factor"]@noise_rng.normal(size=n),{})
    elif model=="iid_uniform":
        raise ValueError("IID requires observation_components_iid(n,seed)")
    else:
        raise ValueError(model)
    def postprocess(observation):
        value,metadata=observation
        if model=="gaussian_Bcov":
            raw=value; uniform=jitter_rng.random(n); positive=context["variance"]>0
            uniform[positive]=ndtr(raw[positive]/np.sqrt(context["variance"][positive]))
            return uniform-.5,None,{"gaussian_raw":raw}
        counts=value; r=context["v"].shape[1]
        if counts.sum()!=r or np.any(counts<0):
            raise p48.NumericalInconclusive("Invalid all-count observation")
        jitter=jitter_rng.random(n)
        field=p48.pit(counts,context["tables"][model],jitter)-.5
        return field,counts,dict(metadata,pit_jitter=jitter)
    return sample,postprocess


def observation_components_iid(n,seed):
    rng=np.random.default_rng(base.seed_for(seed,"raw_noise"))
    return (lambda:(rng.random(n),{})),(lambda observation:(observation[0]-.5,None,{}))


def prepare(case,spec,stream,output):
    """All four bases/preparation discoveries BEFORE any training observation."""
    started=time.perf_counter(); meter=ComputeMeter()
    case_id,n,k,r=case["id"],case["m"],case["k"],case["r"]
    with meter.measure():
        # Conversion paid here and shared; FAST receives the required int64.
        a=np.ascontiguousarray(base.make_graph(case),dtype=np.int64)
        priority=np.random.default_rng(base.seed_for(491040,case_id)).permutation(n).tolist()
        rank={v:i for i,v in enumerate(priority)}
        marks=np.random.default_rng(base.seed_for(491020,case_id)).random(n)
        order=np.random.default_rng(base.seed_for(491030,case_id)).permutation(n).tolist()
        denominator=total_weight(a)
    source,anchor=charged_anchor(a,base.seed_for(491010,case_id),spec["anchor_max_scans"],meter,stream,case_id)
    with meter.measure():
        inside=sorted(source,key=lambda i:rank[i]); outside=sorted(set(range(n))-set(source),key=lambda i:rank[i])
        ell=a.sum(axis=1)-2*a[:,source].sum(axis=1); delta=np.zeros((k,k))
        candidates=[(base.cut(a,source),source)]; swaps=[]
        units=feasible=anchor["candidate_scores_including_initial"]; marginals=0
        for i,old in enumerate(inside):
            for j,new in enumerate(outside):
                subset=sorted((set(source)-{old})|{new}); value=base.cut(a,subset)
                delta[i,j]=ell[new]-ell[old]+2*a[old,new]
                if value-candidates[0][0]!=delta[i,j]:
                    raise ArithmeticError("Shared delta mismatch")
                swaps.append({"stage":"common_swap","case":case_id,"old":old,"new":new,
                              "subset":subset,"cut":value,"delta":float(delta[i,j])})
                candidates.append((value,subset)); units+=1; feasible+=1
        spectral=p48.spectral_data(a,marks,priority,r,spec["gap_tolerance"],spec["residual_tolerance"])
    for row in swaps:
        emit(stream,row)
    common={"case_id":case_id,"anchor":anchor,"source_S0":source,"inside_order":inside,"outside_order":outside,
        "vertex_priority":priority,"fourier_vertex_order":order,"spectral":p48.pack_spectral(spectral),
        "species_order_source_ports":list(range(r)),"b4_groups":"contiguous_at_most4",
        "optical_source_ports":list(range(r)),"optical_source_uses_frontend_partition":False,
        "weight_denominator":denominator}
    common["vertex_priority_by_vertex"]=np.argsort(priority).tolist()
    contexts=[]; status=spectral["numerical_status"]
    if status=="PASS":
        with meter.measure():
            signed=[]
            for column in range(r+1):
                vector=spectral["rounding_vectors"][:,column].real
                for direction in ("top","bottom"):
                    sign=-1 if direction=="top" else 1
                    subset=sorted(sorted(range(n),key=lambda i:(sign*float(vector[i]),rank[i]))[:k])
                    value=base.cut(a,subset); candidates.append((value,subset)); units+=1; feasible+=1
                    signed.append(dict(stage="common_spectral_rounding",case=case_id,column=column,
                                       direction=direction,subset=subset,cut=value))
        for row in signed:
            emit(stream,row)
        try:
            for index,name in enumerate(BASES):
                before_wall,before_cpu=meter.wall,meter.cpu
                with meter.measure():
                    t0=time.perf_counter()
                    if index==0:
                        rotation=np.eye(r,dtype=complex); v=p48.fourier_basis(n,r,order)
                    elif index==1:
                        rotation=np.eye(r,dtype=complex); v=spectral["v"].copy()
                    else:
                        phi=0. if index==2 else math.pi/2
                        rotation=source_rotation(r,math.pi/4,phi); v=spectral["v"]@rotation
                    context=p48.build_network(v,name,spec["residual_tolerance"])
                    context["network_seconds"]=time.perf_counter()-t0
                    # MUST recompute q, every non-spherical law, covariance/mask.
                    # We also calculate the spherical tables afresh numerically.
                    tables,diagnostics,seconds,total=p48.all_marginals(context,list(range(r)))
                    context.update(tables=tables,marginal_diagnostics=diagnostics,
                                   pmf_seconds=seconds,all_pmf_seconds=total)
                    context["source_rotation"]=rotation
                    context["rotation_residual"]=float(abs(rotation.conj().T@rotation-np.eye(r)).max())
                    reference=spectral["v"]@spectral["v"].conj().T
                    context["projector_difference_to_E"]=float(abs(context["projection"]-reference).max()) if index else None
                    context["mu_difference_to_E"]=float(abs(context["mu"]-np.diag(reference).real).max()) if index else None
                    if context["rotation_residual"]>spec["residual_tolerance"]:
                        raise p48.NumericalInconclusive("Nonunitary source rotation")
                context["basis_preparation_compute_wall_seconds"]=meter.wall-before_wall
                context["basis_preparation_compute_cpu_seconds"]=meter.cpu-before_cpu
                contexts.append(context)
        except (p48.NumericalInconclusive,ArithmeticError,ValueError) as error:
            status="INCONCLUSIVE"; common["numerical_error"]=f"{type(error).__name__}: {error}"
            common["failed_basis"]=name
    if status=="PASS":
        for index,context in enumerate(contexts):
            generator=p48.preparation_candidates(context,priority,k)
            while True:
                with meter.measure():
                    try:
                        label,subset,metadata=next(generator)
                    except StopIteration:
                        break
                    value=base.cut(a,subset); candidates.append((value,subset)); units+=1; feasible+=1
                emit(stream,dict(stage="common_preparation_rounding",case=case_id,basis=index,
                                 label=label,subset=subset,cut=value,**metadata))
        for label,q in (("zero",(k+1)//2),("pure_greedy",0)):
            with meter.measure():
                result=adaptive.complete(a,np.zeros(n),k,0,priority,q)
                candidates.append((result["cut"],result["subset"])); units+=result["score_units"]
                feasible+=1; marginals+=result["marginal_evaluations"]
            emit(stream,dict(stage="frontend_decoder",case=case_id,label=label,**result))
        for index,context in enumerate(contexts):
            for model,table in context["tables"].items():
                for lam in (0,1):
                    with meter.measure():
                        field=p48.pit(np.zeros(n,dtype=int),table,np.full(n,.5))-.5
                        result=adaptive.complete(a,field,k,lam,priority,(k+1)//2)
                        candidates.append((result["cut"],result["subset"])); units+=result["score_units"]
                        feasible+=1; marginals+=result["marginal_evaluations"]
                    emit(stream,dict(stage="frontend_decoder",case=case_id,label="vacuum_mid_PIT",
                                     basis=index,model=model,lam=lam,**result))
    else:
        common.setdefault("numerical_error","Occupied-gap/boundary or residual guard")
        emit(stream,dict(stage="numerical_inconclusive",case=case_id,error=common["numerical_error"]))
    with meter.measure():
        cref,reference=min(candidates,key=lambda row:(row[0],row[1]))
    common.update(Cref=cref,reference_subset=reference,numerical_status=status,
        frontend_score_units=units,frontend_feasible_cut_scores=feasible,frontend_partial_marginal_scores=marginals,
        classical_compute_wall_seconds=meter.wall,classical_compute_cpu_seconds=meter.cpu,
        compute_clock_excludes_raw_context_JSON=True,
        compute_clock_includes_numeric_diagnostic_construction=True,
        total_frontend_wall_before_context_serialization=time.perf_counter()-started)
    serial_started=time.perf_counter()
    packed=[]
    for context in contexts:
        data=p48.pack_network(context)
        data.update(source_rotation_real=context["source_rotation"].real.tolist(),
            source_rotation_imag=context["source_rotation"].imag.tolist(),rotation_residual=context["rotation_residual"],
            projector_difference_to_E=context["projector_difference_to_E"],mu_difference_to_E=context["mu_difference_to_E"],
            basis_preparation_compute_wall_seconds=context["basis_preparation_compute_wall_seconds"],
            basis_preparation_compute_cpu_seconds=context["basis_preparation_compute_cpu_seconds"])
        packed.append(data)
    data=dict(common,adjacency=a.tolist(),delta_swap=delta.tolist(),networks=packed)
    (output/f"context_{case_id}.json").write_text(json.dumps(data,indent=2)+"\n")
    common["context_serialization_wall_seconds"]=time.perf_counter()-serial_started
    return a,contexts if status=="PASS" else None,common,delta


def json_arrays(value):
    """Audit formatting is intentionally OUTSIDE postprocessing clocks."""
    if isinstance(value,np.ndarray):
        return value.tolist()
    if isinstance(value,np.generic):
        return value.item()
    if isinstance(value,dict):
        return {key:json_arrays(item) for key,item in value.items()}
    if isinstance(value,(list,tuple)):
        return [json_arrays(item) for item in value]
    return value


def run_batch(a,contexts,common,model,policy,stage,trial,draws,stream):
    if stage not in ("training","evaluation"):
        raise ValueError("Only frozen train/evaluation stages are allowed")
    case_id=common["case_id"]; n=len(a); k=n//2
    basis=policy["basis"]; context=None if basis is None else contexts[basis]
    namespace=491100 if stage=="training" else 491200
    seed=base.seed_for(namespace,case_id,model,policy["id"],trial)
    setup=ComputeMeter(); generation=ComputeMeter(); post=ComputeMeter()
    with setup.measure():
        if model=="iid_uniform":
            sample,process=observation_components_iid(n,seed)
        else:
            sample,process=observation_components(context,model,seed)
    cref=common["Cref"]; best=cref; best_subset=common["reference_subset"]
    denominator=common["weight_denominator"]; values=[]; units=0
    q=(k+1)//2; expected_units=sum(n-i for i in range(q,k))+1
    for shot in range(draws):
        before_generation=generation.wall; before_post=post.wall
        with generation.measure():
            observation=sample()
        with post.measure():
            field,counts,metadata=process(observation)
            result=adaptive.complete(a,field,k,policy["lambda"],common["vertex_priority"],q)
            if len(result["subset"])!=k or len(set(result["subset"]))!=k:
                raise ArithmeticError("Non-feasible decoder output")
            value=int(result["cut"]); values.append(value); units+=result["score_units"]
            if result["score_units"]!=expected_units:
                raise ArithmeticError("Feasible-decoder informative cost changed")
            if value<best:
                best,best_subset=value,result["subset"]
            normalized=value/denominator
        # Never include JSON/list conversion or file writing in FAST allowance.
        emit(stream,json_arrays(dict(stage=stage,case=case_id,model=model,policy=policy["id"],
            basis=basis,lam=policy["lambda"],trial=trial,shot=shot,seed=seed,Cref=cref,
            weight_denominator=denominator,normalized_cut=normalized,gain=max(0,cref-value),
            observation_generation_wall_seconds=generation.wall-before_generation,
            classical_postprocessing_wall_seconds=post.wall-before_post,
            field=field,counts=counts,**metadata,**result)))
    return {"stage":stage,"case":case_id,"model":model,"policy":policy["id"],
        "basis":basis,"lambda":policy["lambda"],"trial":trial,"seed":seed,"proposals":draws,
        "cuts":values,"sum_cuts":sum(values),"weight_denominator":denominator,
        "mean_normalized_cut":sum(values)/(draws*denominator),
        "exact_mean_normalized_cut":str(Fraction(sum(values),draws*denominator)),
        "best_cut":best,"best_subset":best_subset,"score_units":units,
        "observation_setup_wall_seconds":setup.wall,"observation_setup_cpu_seconds":setup.cpu,
        "observation_generation_wall_seconds":generation.wall,"observation_generation_cpu_seconds":generation.cpu,
        "classical_postprocessing_wall_seconds":post.wall,"classical_postprocessing_cpu_seconds":post.cpu,
        "count_backend_setup_excluded_from_FAST_allowance":True,
        "raw_JSON_excluded_from_postprocessing_clock":True}


def evaluate_fixed_policy(a,contexts,common,model,policy,stream):
    """Selection is an immutable input; only fresh evaluation role seeds used."""
    return [run_batch(a,contexts,common,model,policy,"evaluation",trial,16,stream) for trial in (0,1)]


def arm_incumbents(records,commons):
    """Paid training incumbents stay MODEL-SPECIFIC, never update common Cref."""
    output={}
    for model in MODELS:
        output[model]={}
        for case,common in commons.items():
            training=[row for row in records if row["model"]==model and row["case"]==case and row["stage"]=="training"]
            evaluation=[row for row in records if row["model"]==model and row["case"]==case and row["stage"]=="evaluation"]
            initial=(common["Cref"],common["reference_subset"])
            train=min([initial]+[(row["best_cut"],row["best_subset"]) for row in training],key=lambda item:(item[0],item[1]))
            test=min([initial]+[(row["best_cut"],row["best_subset"]) for row in evaluation],key=lambda item:(item[0],item[1]))
            deployed=min((train,test),key=lambda item:(item[0],item[1]))
            output[model][case]={"common_Cref":common["Cref"],
                "paid_training_best_cut":train[0],"paid_training_best_subset":train[1],
                "fresh_evaluation_only_best_cut":test[0],"fresh_evaluation_only_best_subset":test[1],
                "paid_total_deployment_best_cut":deployed[0],"paid_total_deployment_best_subset":deployed[1]}
    return output


def fast_comparison(a,common,b_records,selection_wall_share,spec):
    """CPU grant from measured B classical WALL; optical latency is set to0."""
    if a.dtype!=np.dtype("int64"):
        raise ValueError("FAST conversion must be paid in common preprocessing")
    post=sum(row["classical_postprocessing_wall_seconds"] for row in b_records)
    allowance=common["classical_compute_wall_seconds"]+post+selection_wall_share
    adapter_cpu=time.process_time(); adapter_wall=time.perf_counter()
    seed=base.seed_for(491400,common["case_id"])
    priority=common["vertex_priority_by_vertex"]
    cpu_adapter=time.process_time()-adapter_cpu; wall_adapter=time.perf_counter()-adapter_wall
    remaining=max(0.,allowance-cpu_adapter)
    result=fast.solve_balanced(a,common["reference_subset"],seed=seed,
        max_proposals=spec["fast_max_proposals"],cpu_budget_seconds=remaining,
        wall_budget_seconds=None,incumbent_cost=int(common["Cref"]),vertex_priority=priority)
    # Only admissible prefix, NEVER overall_completed_best after a deadline.
    eligible_cut=int(result["best_cut"]); eligible_subset=result["best_subset"]
    safe=not (result["early_cap_inconclusive"] or result["early_wall_inconclusive"])
    return {"case":common["case_id"],"model":"FAST_incremental",
        "eligible_best_cut":eligible_cut,"eligible_best_subset":eligible_subset,
        "comparison_acceptance_eligible":safe,"grant_convention":"CPU seconds granted from measured B classical WALL, optical setup/count latency=0",
        "common_classical_wall_grant":common["classical_compute_wall_seconds"],
        "training_and_eval_postprocessing_wall_grant":post,"global_B_selection_wall_share":selection_wall_share,
        "total_CPU_allowance_including_adapter":allowance,"adapter_cpu_seconds":cpu_adapter,
        "adapter_wall_seconds":wall_adapter,"solver_CPU_allowance":remaining,
        "optical_simulation_setup_or_count_seconds_granted":0.,"audit_JSON_seconds_granted":0.,
        "result":result}


def check_output_budget(output,limit,reserve=0):
    size=sum(p.stat().st_size for p in output.rglob("*") if p.is_file())
    if size>limit-reserve:
        raise RuntimeError("Scientific output cap approached; preserve partial P49 run")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(); spec=json.loads(args.spec.read_text())
    expected=[(26,13,13,"ER",4902601),(26,13,13,"RR",4902602),
              (34,17,17,"ER",4903401),(34,17,17,"RR",4903402)]
    if (spec["positive_acceptance_allowed"] or spec["models"]!=list(MODELS)
            or spec["ideal_transmission_eta"]!=1. or spec["marker_coefficient"]!=.001
            or spec["assignment_probability_floor"]!=1e-300
            or spec["b4_groups"]!="contiguous_source_ports_at_most4"
            or spec["coherent_phase_law"]!="continuous_uniform"
            or spec["bases"]!=list(BASES) or spec["legacy_baselines"]!=list(LEGACY)
            or spec["gap_tolerance"]!=1e-12 or spec["residual_tolerance"]!=3e-12
            or spec["anchor_max_scans"]!=8 or spec["training_trial"]!=0
            or spec["evaluation_trials"]!=[0,1] or spec["evaluation_draws_per_trial"]!=16
            or spec["fast_max_proposals"]!=100000000
            or spec["FAST_wall_budget_seconds"] is not None or spec["legacy_trials"]!=[0,1]
            or spec["policy_grids"]!={model:policies(model) for model in MODELS}
            or [(c["m"],c["k"],c["r"],c["family"],c["seed"]) for c in spec["cases"]]!=expected):
        raise ValueError("Frozen P49 training/evaluation population changed")
    args.output.mkdir(parents=True,exist_ok=False)
    start_cpu,start_wall=time.process_time(),time.perf_counter()
    commons={}; prepared={}; records=[]; training=[]; selections={}; losses={}; selection_times={}
    legacy_records=[]; fast_records=[]; raw_path=args.output/"raw.jsonl.gz"
    with raw_path.open("xb") as raw_file,gzip.GzipFile(fileobj=raw_file,mode="wb",mtime=0,compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped,encoding="utf8") as stream:
            # Every common discovery is frozen BEFORE the first training shot.
            for case in spec["cases"]:
                a,contexts,common,delta=prepare(case,spec,stream,args.output)
                commons[case["id"]]=common; prepared[case["id"]]=(a,contexts,delta)
                stream.flush(); zipped.flush(); raw_file.flush()
                check_output_budget(args.output,spec["maximum_new_output_bytes"],2097152)
            population_complete=all(common["numerical_status"]=="PASS" for common in commons.values())
            if population_complete:
                for case in spec["cases"]:
                    case_id=case["id"]; a,contexts,_=prepared[case_id]; common=commons[case_id]
                    for model in MODELS:
                        for policy in policies(model):
                            row=run_batch(a,contexts,common,model,policy,"training",0,policy["training_draws"],stream)
                            training.append(row); records.append(row)
                selection_cases=[{"id":case["id"],"weight_denominator":commons[case["id"]]["weight_denominator"]}
                                 for case in spec["cases"]]
                for model in MODELS:
                    meter=ComputeMeter()
                    with meter.measure():
                        choice,model_losses=select_policies(training,selection_cases,(model,))
                    selections[model]=choice[model]; losses[model]=model_losses[model]
                    selection_times[model]={"wall_seconds":meter.wall,"cpu_seconds":meter.cpu}
                # Selection result is never refreshed after any evaluation cut.
                for case in spec["cases"]:
                    case_id=case["id"]; a,contexts,_=prepared[case_id]; common=commons[case_id]
                    for model in MODELS:
                        policy=policies(model)[selections[model]]
                        records.extend(evaluate_fixed_policy(a,contexts,common,model,policy,stream))
                    stream.flush(); zipped.flush(); raw_file.flush()
                    check_output_budget(args.output,spec["maximum_new_output_bytes"],2097152)
                # Legacy informative-score units remain diagnostics, not CPU prices.
                for case in spec["cases"]:
                    case_id=case["id"]; a,contexts,delta=prepared[case_id]; common=commons[case_id]
                    n,k=len(a),case["k"]; q=(k+1)//2
                    half_budget=32*(sum(n-i for i in range(q,k))+1)
                    for baseline in LEGACY:
                        for trial in (0,1):
                            timed=p48.TimedBaselineStream(stream)
                            tag={"stage":"legacy_classical_search","case":case_id,"trial":trial}
                            seed=base.seed_for(491300,case_id,baseline,trial)
                            if baseline=="KL_collective":
                                result=adaptive.kl_collective(a,common["reference_subset"],seed,half_budget,timed,tag)
                            elif baseline=="block_matching":
                                result=p48.block_matching(a,common["source_S0"],common["inside_order"],
                                    common["outside_order"],delta,common["Cref"],seed,half_budget,timed,tag)
                            elif baseline=="spectral_coherent_rounding":
                                result=p48.spectral_coherent_rounding(a,contexts,common["vertex_priority"],
                                    common["Cref"],seed,half_budget,timed,tag)
                            else:
                                result=base.classical_search(a,common["reference_subset"],baseline,seed,half_budget,timed,tag)
                            if result["candidate_scores"]!=half_budget or len(timed.rows)!=half_budget:
                                raise ArithmeticError("Legacy score population changed")
                            legacy_records.append(dict(tag,**result,informative_scores_not_CPU_price=True))
                    # Optical observation setup and generation contribute ZERO grant.
                    b_records=[row for row in records if row["case"]==case_id and row["model"]=="bosonic"]
                    comparison=fast_comparison(a,common,b_records,selection_times["bosonic"]["wall_seconds"]/4,spec)
                    serial_started=time.perf_counter()
                    payload=fast.json_safe_result(comparison)
                    (args.output/f"fast_{case_id}.json").write_text(json.dumps(payload,indent=2)+"\n")
                    compact=dict(payload)
                    compact["result"]={key:value for key,value in payload["result"].items() if key!="trace"}
                    compact["audit_serialization_wall_seconds"]=time.perf_counter()-serial_started
                    fast_records.append(compact)
                    stream.flush(); zipped.flush(); raw_file.flush()
                    check_output_budget(args.output,spec["maximum_new_output_bytes"],2097152)
            else:
                for case in spec["cases"]:
                    (args.output/f"fast_{case['id']}.json").write_text(json.dumps({
                        "status":"NOT_RUN_NUMERICAL_INCONCLUSIVE_POPULATION","case":case["id"]})+"\n")
    counts={model:{stage:sum(row["proposals"] for row in records if row["model"]==model and row["stage"]==stage)
                   for stage in ("training","evaluation")} for model in MODELS}
    expected_count=128 if population_complete else 0
    if any(counts[model][stage]!=expected_count for model in MODELS for stage in ("training","evaluation")):
        raise ArithmeticError("Full paid population changed")
    incumbents=arm_incumbents(records,commons) if population_complete else {}
    eval_means={}; ledger={}; deployable={}
    for model in MODELS:
        arm=[row for row in records if row["model"]==model]
        if population_complete:
            graph_means=[]
            for case in spec["cases"]:
                rows=[row for row in arm if row["case"]==case["id"] and row["stage"]=="evaluation"]
                graph_means.append(Fraction(sum(row["sum_cuts"] for row in rows),32*commons[case["id"]]["weight_denominator"]))
            value=sum(graph_means,Fraction(0))/4
            eval_means[model]={"exact_fraction":str(value),"float":float(value)}
        optical=model in ("bosonic","distinguishable","species4")
        ledger[model]={"training_proposals":counts[model]["training"],"evaluation_proposals":counts[model]["evaluation"],
            "simulated_injected_photons":3840 if optical and population_complete else 0,
            "training_simulated_injected_photons":1920 if optical and population_complete else 0,
            "evaluation_simulated_injected_photons":1920 if optical and population_complete else 0,
            "actual_QPU_photons":0,"informative_score_units":sum(row["score_units"] for row in arm),
            "observation_setup_wall_seconds":sum(row["observation_setup_wall_seconds"] for row in arm),
            "observation_generation_wall_seconds":sum(row["observation_generation_wall_seconds"] for row in arm),
            "classical_postprocessing_wall_seconds":sum(row["classical_postprocessing_wall_seconds"] for row in arm),
            "selection_wall_seconds":selection_times.get(model,{}).get("wall_seconds",0.),
            "paid_training_is_part_of_experimental_spending":True,
            "fresh_evaluation_only_policy_costs":{
                key:sum(row[key] for row in arm if row["stage"]=="evaluation") for key in (
                    "observation_setup_wall_seconds","observation_generation_wall_seconds","classical_postprocessing_wall_seconds")}}
        if population_complete:
            policy=policies(model)[selections[model]]
            deployable[model]={"selected_policy":policy,"training_repeated_for_fresh_evaluation":False,
                "evaluation_samples_per_graph":32,"evaluation_simulated_photons":1920 if optical else 0,
                "policy_sampling_costs_observed_only":ledger[model]["fresh_evaluation_only_policy_costs"],
                "setup_and_frontend_bounds_by_graph":{}}
            for case in spec["cases"]:
                case_id=case["id"]; context=None if policy["basis"] is None else prepared[case_id][1][policy["basis"]]
                deployable[model]["setup_and_frontend_bounds_by_graph"][case_id]={
                    "full_shared_frontend_compute_wall_seconds":commons[case_id]["classical_compute_wall_seconds"],
                    "selected_basis_all_models_setup_wall_upper_bound":context["basis_preparation_compute_wall_seconds"] if context else 0.,
                    "selected_model_PMF_wall_observed":context["pmf_seconds"].get(model,0.) if context else 0.,
                    "selected_basis_bound_is_subset_of_shared_frontend_not_added_twice":True,
                    "timings_are_current_implementation_not_minimal_optimized_costs":True}
    fast_complete=population_complete and all(row["comparison_acceptance_eligible"] for row in fast_records)
    status="EXPLORATORY_DEV_VETO_ONLY" if fast_complete else ("FAST_CONTROL_INCONCLUSIVE" if population_complete else "NUMERICAL_INCONCLUSIVE_POPULATION")
    summary={"status":status,"positive_accepted":False,"full_frozen_population_completed":population_complete,
        "FAST_envelope_comparisons_untruncated":fast_complete,"actual_QPU_calls":0,"heldout_graphs_opened":False,
        "optimum_used":False,"source_loaded_from_training_incumbent":False,
        "selection_frozen_before_evaluation":True,"training_loss_includes_ALL_feasible_cuts":True,
        "selected_policies":selections,"training_global_losses":losses,
        "chosen_policy_fresh_evaluation_normalized_means":eval_means,"proposal_counts":counts,
        "paid_model_specific_incumbents":incumbents,"experimental_spending_and_eval_policy_ledgers":ledger,
        "retrospective_deployable_policy_ledgers":deployable,
        "shared_frontend_compute_charged_once":{"wall_seconds":sum(c["classical_compute_wall_seconds"] for c in commons.values()),
            "cpu_seconds":sum(c["classical_compute_cpu_seconds"] for c in commons.values()),"shared_with_all_controls":True},
        "common_frontend":commons,"primary_batches":records,"legacy_baselines":legacy_records,"FAST_comparisons":fast_records,
        "cpu_seconds_inside_main":time.process_time()-start_cpu,"wall_seconds_inside_main":time.perf_counter()-start_wall,
        "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
        "FAST_module_sha256":hashlib.sha256(Path("research/P49_fast_classical.py").read_bytes()).hexdigest(),
        "simulation_time_is_QPU_time":False,"legacy_scores_are_not_CPU_equivalents":True}
    (args.output/"summary.json").write_text(json.dumps(json_arrays(summary),indent=2)+"\n")
    check_output_budget(args.output,spec["maximum_new_output_bytes"])
    print(json.dumps({key:json_arrays(value) for key,value in summary.items() if key not in (
        "common_frontend","primary_batches","legacy_baselines","FAST_comparisons","paid_model_specific_incumbents",
        "retrospective_deployable_policy_ledgers")}))


if __name__=="__main__":
    main()
