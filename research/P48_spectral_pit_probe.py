"""P48-B DEV veto: fixed graph spectral CF input basis, seven fair controls.

No optimum oracle, postselection, device access, heldout or positive acceptance.
P43/P45 helpers and the separately frozen coherent-marginal helper are inputs.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
import gzip
import hashlib
import io
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.linalg import null_space
from scipy.optimize import linear_sum_assignment
from scipy.special import ndtr

import P43_global_gain_probe as base
import P45_adaptive_probe as adaptive
import P48_coherent_marginals as coherent

MODELS=("bosonic","distinguishable","species4","gaussian_Bcov","iid_uniform",
        "continuous_phase","spherical_coherent")
BASELINES=("anneal","spectral_swap","KL_collective","block_matching",
           "spectral_coherent_rounding")


def emit(stream,row):
    stream.write(json.dumps(row,allow_nan=False)+"\n")


def decimal_json(value):
    if isinstance(value,Decimal):
        return str(value)
    if isinstance(value,dict):
        return {key:decimal_json(item) for key,item in value.items()}
    if isinstance(value,(tuple,list)):
        return [decimal_json(item) for item in value]
    return value


class NumericalInconclusive(RuntimeError):
    """Retain a numerical failure without substituting another graph/basis."""


def spectral_data(a,marks,priority,r,gap_tolerance=1e-12,residual_tolerance=3e-12):
    n=len(a)
    if (np.asarray(marks).shape!=(n,) or not 0<=r<n or sorted(priority)!=list(range(n))
            or np.any(np.asarray(marks)<0) or np.any(np.asarray(marks)>1)):
        raise ValueError("Invalid spectral input")
    laplacian=np.diag(a.sum(axis=1))-a
    norm=float(np.linalg.norm(laplacian,2))
    scaled=laplacian/norm if norm>0 else np.zeros_like(laplacian)
    marked=scaled+1e-3*np.diag(marks)
    values,vectors=np.linalg.eigh(marked)
    vectors=np.asarray(vectors,dtype=complex)
    # Column gauges are physically null; fixing them makes carried-label
    # fixtures reproducible without a hidden source-basis rotation.
    rank={vertex:i for i,vertex in enumerate(priority)}
    pivots=[]
    for column in range(n):
        magnitude=abs(vectors[:,column]); maximum=float(magnitude.max())
        pivot=min(np.flatnonzero(magnitude>=maximum-1e-12),key=lambda i:rank[int(i)])
        vectors[:,column]*=np.conj(vectors[pivot,column])/abs(vectors[pivot,column])
        pivots.append(int(pivot))
    gaps=np.diff(values)
    eigen_residual=float(abs(marked@vectors-vectors*values[None,:]).max())
    orthogonal_residual=float(abs(vectors.conj().T@vectors-np.eye(n)).max())
    # Internal occupied gaps AND boundary; vacuum-complement degeneracies do
    # not alter a CF state whose source columns are already fixed.
    guarded=gaps[:r]
    valid=(not len(guarded) or guarded.min()>gap_tolerance)
    valid=valid and eigen_residual<=residual_tolerance and orthogonal_residual<=residual_tolerance
    return {"v":vectors[:,:r],"rounding_vectors":vectors[:,:r+1],
        "eigenvalues":values,"all_gaps":gaps,"guarded_gaps":guarded,
        "boundary_gap":float(gaps[r-1]) if r else None,
        "laplacian_norm":norm,"marks":np.asarray(marks),"gauge_pivots":pivots,
        "eigen_residual":eigen_residual,"orthogonal_residual":orthogonal_residual,
        "gap_tolerance":gap_tolerance,"residual_tolerance":residual_tolerance,
        "numerical_status":"PASS" if valid else "INCONCLUSIVE"}


def fourier_basis(n,r,order):
    if sorted(order)!=list(range(n)) or not 0<=r<=n:
        raise ValueError("Invalid blind Fourier frame")
    indices=np.arange(n)
    ordered=np.exp(2j*np.pi*indices[:,None]*np.arange(r)[None,:]/n)/math.sqrt(n)
    v=np.zeros((n,r),dtype=complex)
    v[order]=ordered
    return v


def build_network(v,encoder,residual_tolerance=3e-12):
    n,r=v.shape
    source_residual=float(abs(v.conj().T@v-np.eye(r)).max()) if r else 0.
    if source_residual>residual_tolerance:
        raise NumericalInconclusive("Occupied columns fail orthogonality")
    vacuum=null_space(v.conj().T,rcond=1e-12) if r else np.eye(n,dtype=complex)
    if vacuum.shape!=(n,n-r):
        raise NumericalInconclusive("Vacuum-complement rank mismatch")
    u=np.column_stack((v,vacuum))
    residual=float(abs(u.conj().T@u-np.eye(n)).max())
    if residual>residual_tolerance:
        raise NumericalInconclusive("Unitary-completion residual exceeded")
    probabilities=abs(v)**2
    mu=probabilities.sum(axis=1)
    projection=v@v.conj().T
    cov=np.diag(mu)+abs(projection)**2-2*probabilities@probabilities.T
    cov=(cov+cov.T)/2
    eigenvalues,vectors=np.linalg.eigh(cov)
    if eigenvalues.min() < -1e-10:
        raise NumericalInconclusive("Negative numerical B covariance")
    factor=vectors*np.sqrt(np.maximum(eigenvalues,0))[None,:]
    # Exact CF-deterministic rows have count0 (empty) or count1 (one-hot1).
    # Do not magnify eigensolver leakage there into order-one correlations.
    # mu==1 ALONE is insufficient: a spread row can have bosonic variance.
    empty_rows=np.count_nonzero(probabilities,axis=1)==0
    occupied_deterministic=(np.count_nonzero(probabilities,axis=1)==1)&np.any(probabilities==1,axis=1)
    deterministic=empty_rows|occupied_deterministic
    pre_mask_variances=np.sum(factor**2,axis=1)
    factor[deterministic]=0
    effective=np.sum(factor**2,axis=1)
    return {"v":v,"u":u,"encoder":encoder,"source_ports":list(range(r)),
        "probabilities":probabilities,"mu":mu,"projection":projection,
        "cov":cov,"factor":factor,"variance":effective,
        "target_variance":np.diag(cov).copy(),
        "Gaussian_structurally_empty_rows":np.flatnonzero(empty_rows).tolist(),
        "Gaussian_structurally_occupied_deterministic_rows":np.flatnonzero(occupied_deterministic).tolist(),
        "Gaussian_deterministic_mask_pre_variance":pre_mask_variances.tolist(),
        "Gaussian_deterministic_mask_removed_factor_L2":float(np.sqrt(pre_mask_variances[deterministic].sum())),
        "Gaussian_factor_covariance_residual":float(abs(factor@factor.T-cov).max()),
        "Gaussian_variance_residual":float(abs(effective-np.diag(cov)).max()),
        "source_orthogonality_residual":source_residual,"unitary_residual":residual,
        "projector_offdiagonal_frobenius_squared":float(np.sum(abs(projection-np.diag(mu))**2))}


def repair_probability_row(row):
    """Only repair a tiny >1 roundoff excess; NEVER scale a subunit row to1."""
    values=[Fraction.from_float(float(x)) for x in row]
    if any(x<0 for x in values):
        raise NumericalInconclusive("Negative one-particle probability")
    before=sum(values,Fraction(0)); correction=Fraction(0)
    if before>1:
        correction=before-1
        if correction>Fraction(3,10**12) or not values:
            raise NumericalInconclusive("Row probability exceeds1 beyond tolerance")
        index=max(range(len(values)),key=lambda i:values[i])
        values[index]-=correction
    after=sum(values,Fraction(0))
    return tuple(values),{"raw_mu":str(before),"used_mu":str(after),
                         "input_roundoff_repair_L1":str(correction),
                         "subunit_row_rescaled_to1":False}


def factorial_marginal(row,bosonic):
    n=len(row)
    with localcontext() as ctx:
        ctx.prec=80
        elementary=[Decimal(1)]+[Decimal(0)]*n
        for index,value in enumerate(row):
            value=Decimal(value.numerator)/Decimal(value.denominator)
            for degree in range(index+1,0,-1):
                elementary[degree]+=value*elementary[degree-1]
        coefficients=[value*(math.factorial(i) if bosonic else 1) for i,value in enumerate(elementary)]
        raw=[sum((Decimal((-1)**(h-s)*math.comb(h,s))*coefficients[h]
                  for h in range(s,n+1)),Decimal(0)) for s in range(n+1)]
        if min(raw)<Decimal("-1e-12") or abs(sum(raw)-1)>Decimal("1e-12"):
            raise NumericalInconclusive("Invalid factorial marginal")
        positive=[max(Decimal(0),x) for x in raw]; total=sum(positive)
        repaired=[x/total for x in positive]
        correction=sum(abs(x-y) for x,y in zip(raw,repaired))
        return np.asarray([float(x) for x in repaired]),{
            "precision":80,"raw_minimum_pmf":str(min(raw)),"raw_pmf_sum":str(sum(raw)),
            "pmf_correction_L1":str(correction),"shift_pgf_coefficients":[str(x) for x in coefficients]}


def all_marginals(context,species_order):
    started=time.perf_counter()
    probabilities=context["probabilities"]; n,r=probabilities.shape
    if sorted(species_order)!=list(range(r)):
        raise ValueError("Species source ports must form a permutation")
    rows=[]; repairs=[]
    for row in probabilities:
        values,diagnostic=repair_probability_row(row)
        rows.append(values); repairs.append(diagnostic)
    tables={}; diagnostics={}; seconds={}
    for model,bosonic in (("bosonic",True),("distinguishable",False)):
        t0=time.perf_counter(); outputs=[factorial_marginal(row,bosonic) for row in rows]
        tables[model]=np.asarray([x[0] for x in outputs]); diagnostics[model]=[x[1] for x in outputs]
        seconds[model]=time.perf_counter()-t0
    t0=time.perf_counter(); group_tables=[]; group_diagnostics=[]
    for row in rows:
        pmf=np.ones(1); meta=[]
        for index in range(0,r,4):
            group=species_order[index:index+4]
            part,record=factorial_marginal(tuple(row[j] for j in group),True)
            pmf=np.convolve(pmf,part); meta.append(record)
        total=float(pmf.sum())
        group_tables.append(pmf/total)
        group_diagnostics.append({"groups":meta,"pre_normalization_sum":total,
                                  "normalization_L1":abs(total-1)})
    tables["species4"]=np.asarray(group_tables); diagnostics["species4"]=group_diagnostics
    seconds["species4"]=time.perf_counter()-t0
    for model in ("continuous_phase","spherical_coherent"):
        t0=time.perf_counter(); outputs=[]; meta=[]
        for row in rows:
            if model=="continuous_phase":
                result=coherent.fixed_phase_marginal(row,precision=80)
            else:
                mu=sum(row,Fraction(0))
                result=coherent.spherical_marginal(mu,r,precision=80)
            outputs.append([float(x) for x in result["pmf"]]); meta.append(decimal_json(result))
        tables[model]=np.asarray(outputs); diagnostics[model]=meta
        seconds[model]=time.perf_counter()-t0
    for table in tables.values():
        if table.shape!=(n,r+1) or np.any(table<0) or abs(table.sum(axis=1)-1).max()>2e-12:
            raise NumericalInconclusive("Invalid coherent or count marginal table")
    return tables,{"row_repairs":repairs,"per_model":diagnostics},seconds,time.perf_counter()-started


def pit(counts,pmf,jitter):
    original=np.asarray(counts); counts=np.asarray(counts,dtype=int)
    jitter=np.asarray(jitter,dtype=float)
    if (not np.all(original==counts) or len(counts)!=len(pmf) or np.any(counts<0)
            or np.any(counts>=pmf.shape[1]) or jitter.shape!=counts.shape
            or np.any(jitter<0) or np.any(jitter>=1)):
        raise ValueError("Invalid count/PIT input")
    cumulative=np.cumsum(pmf,axis=1); index=np.arange(len(counts))
    left=np.where(counts>0,cumulative[index,np.maximum(counts-1,0)],0.)
    values=left+jitter*pmf[index,counts]
    if values.min() < -1e-12 or values.max()>1+1e-12:
        raise NumericalInconclusive("PIT outside[0,1]")
    return np.clip(values,0,1)


def coherent_counts(context,model,seed):
    field_rng=np.random.default_rng(base.seed_for(seed,"coherent_coefficients"))
    count_rng=np.random.default_rng(base.seed_for(seed,"coherent_multinomial"))
    v=context["v"]; n,r=v.shape
    def draw():
        if r==0:
            return np.zeros(n,dtype=int),{"coherent_probability_sum":0.,"sampler_roundoff_normalization_L1":0.}
        if model=="continuous_phase":
            z=np.exp(2j*np.pi*field_rng.random(r))/math.sqrt(r)
        elif model=="spherical_coherent":
            z=(field_rng.normal(size=r)+1j*field_rng.normal(size=r))/math.sqrt(2)
            norm=float(np.linalg.norm(z))
            if not norm>0:
                raise NumericalInconclusive("Zero Gaussian coherent norm")
            z/=norm
        else:
            raise ValueError(model)
        probabilities=abs(v@z)**2; total=float(probabilities.sum())
        if abs(total-1)>3e-12:
            raise NumericalInconclusive("Coherent norm lost through isometry")
        return count_rng.multinomial(r,probabilities/total),{
            "coherent_probability_sum":total,"sampler_roundoff_normalization_L1":abs(total-1),
            "coherent_coefficient_norm":float(np.linalg.norm(z))}
    return draw


def make_field(context,species_order,model,seed,tables):
    roles=("PIT_jitter","continuous_noise","physical_counts","coherent_counts")
    seeds=[base.seed_for(seed,role) for role in roles]
    if len(set(seeds))!=len(seeds):
        raise ArithmeticError("Seed role collision")
    jitter_rng=np.random.default_rng(seeds[0]); noise_rng=np.random.default_rng(seeds[1])
    n,r=context["v"].shape; sample=None
    if model in ("bosonic","distinguishable","species4"):
        source=species_order if model=="species4" else list(range(r))
        primitive,_=base.make_optical_sampler(context["u"],source,model,seeds[2])
        sample=lambda:(primitive()[0],{})
    elif model in ("continuous_phase","spherical_coherent"):
        sample=coherent_counts(context,model,seeds[3])
    def draw():
        if sample is not None:
            counts,sampling_meta=sample()
            if counts.sum()!=r or np.any(counts<0):
                raise NumericalInconclusive("Invalid full count observation")
            jitter=jitter_rng.random(n)
            return pit(counts,tables[model],jitter)-.5,counts,dict(sampling_meta,pit_jitter=jitter.tolist())
        if model=="gaussian_Bcov":
            raw=context["factor"]@noise_rng.normal(size=n)
            positive=context["variance"]>0; values=jitter_rng.random(n)
            values[positive]=ndtr(raw[positive]/np.sqrt(context["variance"][positive]))
            return values-.5,None,{"gaussian_raw":raw.tolist()}
        if model=="iid_uniform":
            return noise_rng.random(n)-.5,None,{}
        raise ValueError(model)
    return draw


class TimedBaselineStream:
    """Preserve immutable helper output plus per-query elapsed times for joint frontiers."""
    def __init__(self, stream):
        self.stream, self.started, self.rows = stream, time.perf_counter(), []
    def write(self, text):
        row = json.loads(text)
        row["baseline_elapsed_seconds"] = time.perf_counter()-self.started
        self.rows.append((row["baseline_elapsed_seconds"], row["cut"]))
        emit(self.stream, row)
        return len(text)


def block_matching(a, source, inside, outside, delta, reference, seed, budget, stream, tag):
    """Fixed-anchor nonlocal baseline using ALL shared swap information.

    Selected inside vertices transfer with alternating p=.25/.5. A rectangular
    Hungarian assignment selects distinct destinations using the already shared
    delta table. Every resulting feasible partition is scored and charged once.
    The actual simultaneous-move cut can differ from the summed single deltas.
    """
    rng = np.random.default_rng(seed)
    started = time.perf_counter()
    best = reference
    for step in range(budget):
        p = (.25, .5)[step % 2]
        selected = np.flatnonzero(rng.random(len(inside)) < p)
        if len(selected):
            row, column = linear_sum_assignment(delta[selected])
            removed = [inside[int(selected[r])] for r in row]
            added = [outside[int(c)] for c in column]
        else:
            removed, added = [], []
        subset = sorted((set(source)-set(removed))|set(added))
        value = base.cut(a, subset)
        best = min(best, value)
        emit(stream, dict(tag, model="block_matching", step=step, seed=seed,
                          p=p, removed=removed, added=added, subset=subset,
                          cut=value, best_cut=best))
    return {"model":"block_matching", "candidate_scores":budget,
            "initial_cut":reference, "best_cut":best,
            "search_and_scoring_seconds":time.perf_counter()-started,
            "anchor_is_fixed_S0":True, "all_delta_scores_shared":True}


def spectral_coherent_rounding(a,contexts,priority,reference,seed,budget,stream,tag):
    """Round continuous phase/spherical fields, then at most two best-swap scans.

    Cycles alternate blind/phase, blind/sphere, graph/phase, graph/sphere.
    Every rounded support and every inspected swap consumes one score unit.
    """
    rng=np.random.default_rng(seed); n=len(a); k=n//2
    rank={vertex:index for index,vertex in enumerate(priority)}
    calls=cycles=0; best=reference; started=time.perf_counter()
    while calls<budget:
        encoder=(cycles//2)%len(contexts); spherical=bool(cycles%2)
        v=contexts[encoder]["v"]; r=v.shape[1]
        if r:
            if spherical:
                z=(rng.normal(size=r)+1j*rng.normal(size=r))/math.sqrt(2)
                norm=float(np.linalg.norm(z))
                if norm<=0:
                    raise NumericalInconclusive("Zero baseline coherent norm")
                z/=norm
            else:
                z=np.exp(2j*np.pi*rng.random(r))/math.sqrt(r)
            intensity=abs(v@z)**2
        else:
            intensity=np.zeros(n)
        intensity_sum=float(intensity.sum())
        if r and abs(intensity_sum-1)>3e-12:
            raise NumericalInconclusive("Baseline coherent isometry norm failed")
        current=set(sorted(range(n),key=lambda i:(-float(intensity[i]),rank[i]))[:k])
        value=base.cut(a,current); calls+=1; best=min(best,value)
        emit(stream,dict(tag,model="spectral_coherent_rounding",kind="rounding",
            step=calls-1,seed=seed,cycle=cycles,encoder=contexts[encoder]["encoder"],
            coefficient_law="sphere" if spherical else "continuous_phase",
            coherent_intensity_sum=intensity_sum,
            intensity=intensity.tolist(),subset=sorted(current),cut=value,best_cut=best))
        for scan in range(2):
            if calls>=budget:
                break
            candidates=[]
            for old in sorted(current,key=lambda i:rank[i]):
                for new in sorted(set(range(n))-current,key=lambda i:rank[i]):
                    subset=(current-{old})|{new}; proposed=base.cut(a,subset)
                    calls+=1; best=min(best,proposed)
                    candidates.append((proposed,rank[old],rank[new],subset))
                    emit(stream,dict(tag,model="spectral_coherent_rounding",kind="candidate",
                        step=calls-1,seed=seed,cycle=cycles,scan=scan,subset=sorted(subset),
                        cut=proposed,best_cut=best))
                    if calls>=budget:
                        break
                if calls>=budget:
                    break
            if not candidates:
                break
            proposed,_,_,subset=min(candidates,key=lambda row:row[:3])
            if proposed>=value:
                break
            current,value=set(subset),proposed
        cycles+=1
    return {"model":"spectral_coherent_rounding","candidate_scores":calls,
        "initial_cut":reference,"best_cut":best,"rounding_cycles":cycles,
        "max_best_swap_scans_per_rounding":2,
        "search_and_scoring_seconds":time.perf_counter()-started}


def pack_spectral(spectral):
    return {"eigenvalues":spectral["eigenvalues"].tolist(),
        "all_gaps":spectral["all_gaps"].tolist(),"guarded_gaps":spectral["guarded_gaps"].tolist(),
        "boundary_gap":spectral["boundary_gap"],"laplacian_norm":spectral["laplacian_norm"],
        "marks":spectral["marks"].tolist(),"gauge_pivots":spectral["gauge_pivots"],
        "eigen_residual":spectral["eigen_residual"],"orthogonal_residual":spectral["orthogonal_residual"],
        "gap_tolerance":spectral["gap_tolerance"],"residual_tolerance":spectral["residual_tolerance"],
        "numerical_status":spectral["numerical_status"],
        "rounding_vectors_real":spectral["rounding_vectors"].real.tolist(),
        "rounding_vectors_imag":spectral["rounding_vectors"].imag.tolist()}


def pack_network(context):
    return {"encoder":context["encoder"],"source_ports":context["source_ports"],
        "v_real":context["v"].real.tolist(),"v_imag":context["v"].imag.tolist(),
        "u_real":context["u"].real.tolist(),"u_imag":context["u"].imag.tolist(),
        "mu":context["mu"].tolist(),"one_particle_probabilities":context["probabilities"].tolist(),
        "projector_real":context["projection"].real.tolist(),"projector_imag":context["projection"].imag.tolist(),
        "covariance_B":context["cov"].tolist(),
        "Gaussian_target_variance":context["target_variance"].tolist(),
        "Gaussian_effective_factor_variance":context["variance"].tolist(),
        "Gaussian_factor_covariance_residual":context["Gaussian_factor_covariance_residual"],
        "Gaussian_variance_residual":context["Gaussian_variance_residual"],
        "Gaussian_structurally_empty_rows":context["Gaussian_structurally_empty_rows"],
        "Gaussian_structurally_occupied_deterministic_rows":context["Gaussian_structurally_occupied_deterministic_rows"],
        "Gaussian_deterministic_mask_pre_variance":context["Gaussian_deterministic_mask_pre_variance"],
        "Gaussian_deterministic_mask_removed_factor_L2":context["Gaussian_deterministic_mask_removed_factor_L2"],
        "source_orthogonality_residual":context["source_orthogonality_residual"],
        "unitary_residual":context["unitary_residual"],
        "projector_offdiagonal_frobenius_squared":context["projector_offdiagonal_frobenius_squared"],
        "marginal_pmfs":{model:table.tolist() for model,table in context["tables"].items()},
        "marginal_diagnostics":context["marginal_diagnostics"],
        "pmf_computation_seconds":context["pmf_seconds"],
        "all_pmf_seconds":context["all_pmf_seconds"],"network_seconds":context["network_seconds"]}


def preparation_candidates(context,priority,k):
    """Cheap intensity discoveries, including labelled max-product matching.

    No graph-cut objective is read here. Every returned support is scored and
    shared by the caller before any field/photon proposal. Matching maximizes
    ONE labelled intensity product, not the permanent/sum D support mass.
    """
    probabilities=context["probabilities"]; n,r=probabilities.shape
    if k!=r or sorted(priority)!=list(range(n)):
        raise ValueError("P48 preparation contract requires r=K and carried priority")
    rank={vertex:index for index,vertex in enumerate(priority)}
    features=[("mu",None,context["mu"])]+[
        ("source_column_intensity",column,probabilities[:,column]) for column in range(r)]
    for label,column,values in features:
        for direction in ("top","bottom"):
            sign=-1 if direction=="top" else 1
            ordered=sorted(range(n),key=lambda i:(sign*float(values[i]),rank[i]))
            yield label,sorted(ordered[:k]),{"direction":direction,"source_port":column}
    started=time.perf_counter()
    # Reorder rows by a carried priority before deterministic tie handling.
    ordered=probabilities[priority]
    clipped=np.maximum(ordered,1e-300)
    costs=-np.log(clipped)
    rows,columns=linear_sum_assignment(costs)
    selected=[priority[int(row)] for row in rows]
    yield "labelled_max_product_assignment",sorted(selected),{
        "assignment_source_ports":[int(column) for column in columns],
        "assignment_output_vertices":selected,
        "assignment_negative_log_product":float(costs[rows,columns].sum()),
        "assignment_probability_floor":1e-300,
        "assignment_floor_entries":int(np.count_nonzero(ordered<1e-300)),
        "assignment_construction_seconds":time.perf_counter()-started,
        "optimizes_exact_D_support_probability":False}


def prepare(case,spec,stream,output):
    case_id,n,k,r=case["id"],case["m"],case["k"],case["r"]
    started=time.perf_counter(); a=base.make_graph(case)
    source,anchor=base.prepare_anchor(a,base.seed_for(481010,case_id),
                                     spec["anchor_max_scans"],stream,case_id)
    priority=np.random.default_rng(base.seed_for(481040,case_id)).permutation(n).tolist()
    rank={v:i for i,v in enumerate(priority)}
    inside=sorted(source,key=lambda i:rank[i])
    outside=sorted(set(range(n))-set(source),key=lambda i:rank[i])
    species=np.random.default_rng(base.seed_for(481050,case_id)).permutation(r).tolist()
    fourier_order=np.random.default_rng(base.seed_for(481030,case_id)).permutation(n).tolist()
    marks=np.random.default_rng(base.seed_for(481020,case_id)).random(n)
    ell=a.sum(axis=1)-2*a[:,source].sum(axis=1); delta=np.zeros((k,k))
    candidates=[(base.cut(a,source),source)]
    units=feasible=anchor["candidate_scores_including_initial"]; marginals=0
    for i,old in enumerate(inside):
        for j,new in enumerate(outside):
            subset=sorted((set(source)-{old})|{new}); value=base.cut(a,subset)
            delta[i,j]=ell[new]-ell[old]+2*a[old,new]
            if value-candidates[0][0]!=delta[i,j]:
                raise ArithmeticError("Shared swap orientation mismatch")
            emit(stream,dict(stage="common_swap",case=case_id,old=old,new=new,
                             subset=subset,cut=value,delta=float(delta[i,j])))
            candidates.append((value,subset)); units+=1; feasible+=1
    graph_swap_seconds=time.perf_counter()-started
    spectral_started=time.perf_counter()
    spectral=spectral_data(a,marks,priority,r,spec["gap_tolerance"],spec["residual_tolerance"])
    spectral_seconds=time.perf_counter()-spectral_started
    common={"anchor":anchor,"source_S0":source,"inside_order":inside,"outside_order":outside,
        "vertex_priority":priority,"species_order_source_ports":species,
        "fourier_vertex_order":fourier_order,"spectral":pack_spectral(spectral),
        "graph_and_swaps_seconds":graph_swap_seconds,"spectral_preprocessing_seconds":spectral_seconds,
        "optical_source_depends_on_anchor":False,"optical_source_ports":list(range(r))}
    contexts=[]
    if spectral["numerical_status"]=="PASS":
        for column in range(r+1):
            vector=spectral["rounding_vectors"][:,column].real
            for direction in ("top","bottom"):
                ordered=sorted(range(n),key=lambda i:((-float(vector[i]) if direction=="top" else float(vector[i])),rank[i]))
                subset=sorted(ordered[:k]); value=base.cut(a,subset)
                emit(stream,dict(stage="common_spectral_rounding",case=case_id,column=column,
                                 direction=direction,subset=subset,cut=value))
                candidates.append((value,subset)); units+=1; feasible+=1
        try:
            for encoder,v in (("Fourier_blind",fourier_basis(n,r,fourier_order)),
                              ("spectral_graph",spectral["v"])):
                t0=time.perf_counter(); context=build_network(v,encoder,spec["residual_tolerance"])
                context["network_seconds"]=time.perf_counter()-t0
                tables,diagnostics,seconds,total=all_marginals(context,species)
                context.update(tables=tables,marginal_diagnostics=diagnostics,
                               pmf_seconds=seconds,all_pmf_seconds=total)
                contexts.append(context)
        except (NumericalInconclusive,ArithmeticError,ValueError) as error:
            # Retain the whole graph as incomplete. No replacing basis/marks.
            common["numerical_error"]=f"{type(error).__name__}: {error}"
            common["failed_encoder"]=encoder
            common["failed_occupied_columns_real"]=v.real.tolist()
            common["failed_occupied_columns_imag"]=v.imag.tolist()
            common["numerical_status"]="INCONCLUSIVE"
    else:
        common["numerical_status"]="INCONCLUSIVE"
        common["numerical_error"]="Occupied/internal or boundary gap/residual guard"
    if common.get("numerical_status")!="INCONCLUSIVE":
        preparation_started=time.perf_counter()
        for index,context in enumerate(contexts):
            for label,subset,metadata in preparation_candidates(context,priority,k):
                value=base.cut(a,subset)
                emit(stream,dict(stage="common_preparation_rounding",case=case_id,
                    encoder=index,label=label,subset=subset,cut=value,**metadata))
                candidates.append((value,subset)); units+=1; feasible+=1
        common["direct_preparation_rounding_seconds"]=time.perf_counter()-preparation_started
        decoder_started=time.perf_counter()
        for label,q in (("zero",(k+1)//2),("pure_greedy",0)):
            result=adaptive.complete(a,np.zeros(n),k,0,priority,q)
            emit(stream,dict(stage="frontend_decoder",case=case_id,label=label,**result))
            candidates.append((result["cut"],result["subset"])); units+=result["score_units"]
            feasible+=1; marginals+=result["marginal_evaluations"]
        for index,context in enumerate(contexts):
            for model,table in context["tables"].items():
                field=pit(np.zeros(n,dtype=int),table,np.full(n,.5))-.5
                for lam in spec["decoder_lambda"]:
                    result=adaptive.complete(a,field,k,lam,priority,(k+1)//2)
                    emit(stream,dict(stage="frontend_decoder",case=case_id,label="vacuum_mid_PIT",
                                     encoder=index,model=model,lam=lam,**result))
                    candidates.append((result["cut"],result["subset"])); units+=result["score_units"]
                    feasible+=1; marginals+=result["marginal_evaluations"]
        common["decoder_frontend_seconds"]=time.perf_counter()-decoder_started
        common["numerical_status"]="PASS"
    cref,reference=min(candidates,key=lambda row:(row[0],row[1]))
    common.update(Cref=cref,reference_subset=reference,frontend_score_units=units,
        frontend_feasible_cut_scores=feasible,frontend_partial_marginal_scores=marginals,
        total_common_preprocessing_seconds=time.perf_counter()-started)
    saved=dict(common,adjacency=a.tolist(),delta_swap=delta.tolist(),
               networks=[pack_network(context) for context in contexts])
    (output/f"context_{case_id}.json").write_text(json.dumps(saved,indent=2)+"\n")
    if common["numerical_status"]!="PASS":
        emit(stream,dict(stage="numerical_inconclusive",case=case_id,error=common["numerical_error"]))
        contexts=None
    return a,contexts,common,delta


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(); spec=json.loads(args.spec.read_text())
    expected_cases=[(26,13,13,"ER",4802601),(26,13,13,"RR",4802602),
                    (34,17,17,"ER",4803401),(34,17,17,"RR",4803402)]
    if (spec["models"]!=list(MODELS) or spec["baseline_models"]!=list(BASELINES)
            or spec["positive_acceptance_allowed"] or spec["ideal_transmission_eta"]!=1.
            or spec["encoders"]!=["Fourier_blind","spectral_graph"]
            or spec["decoder_lambda"]!=[0,1] or spec["trial_seeds"]!=[0,1]
            or spec["draws_per_tuple"]!=8 or spec["marker_coefficient"]!=1e-3
            or spec["gap_tolerance"]!=1e-12 or spec["residual_tolerance"]!=3e-12
            or spec["coherent_phase_law"]!="continuous_uniform"
            or spec["coherent_rounding_best_swap_scans_per_round"]!=2
            or spec["assignment_probability_floor"]!=1e-300
            or [(c["m"],c["k"],c["r"],c["family"],c["seed"]) for c in spec["cases"]]!=expected_cases):
        raise ValueError("Frozen P48-B population or physical convention changed")
    args.output.mkdir(parents=True,exist_ok=False)
    start_cpu,start_wall=time.process_time(),time.perf_counter()
    records=[]; commons={}; complete_cases=[]
    totals={model:np.zeros(4) for model in MODELS}; raw_path=args.output/"raw.jsonl.gz"
    with raw_path.open("xb") as raw_file,gzip.GzipFile(fileobj=raw_file,mode="wb",mtime=0,compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped,encoding="utf8") as stream:
            for case in spec["cases"]:
                case_id,k=case["id"],case["k"]
                a,contexts,common,delta=prepare(case,spec,stream,args.output)
                commons[case_id]=common
                if contexts is None:
                    stream.flush(); zipped.flush(); raw_file.flush()
                    if sum(p.stat().st_size for p in args.output.rglob("*") if p.is_file())>spec["maximum_new_output_bytes"]-2097152:
                        raise RuntimeError("Inconclusive data approached cap; retain partial run")
                    continue
                complete_cases.append(case)
                priority,cref=common["vertex_priority"],common["Cref"]
                q=(k+1)//2; expected_units=sum(len(a)-i for i in range(q,k))+1
                for replicate in spec["trial_seeds"]:
                    key=f"{case_id}:{replicate}"; time_budgets=defaultdict(float)
                    for model in MODELS:
                        for index,context in enumerate(contexts):
                            for lam_index,lam in enumerate(spec["decoder_lambda"]):
                                setting=2*index+lam_index; seed=base.seed_for(481100,key,model,setting)
                                setting_start=time.perf_counter(); setup_start=time.perf_counter()
                                draw=make_field(context,common["species_order_source_ports"],model,seed,context["tables"])
                                setup_seconds=time.perf_counter()-setup_start
                                sample_seconds=decoder_seconds=0.; gains=[]; best=cref; score_units=0
                                for shot in range(spec["draws_per_tuple"]):
                                    t0=time.perf_counter(); field,counts,extra=draw()
                                    sample_seconds+=time.perf_counter()-t0
                                    t0=time.perf_counter(); result=adaptive.complete(a,field,k,lam,priority,q)
                                    decoder_seconds+=time.perf_counter()-t0
                                    if result["score_units"]!=expected_units:
                                        raise ArithmeticError("Decoder informative score budget changed")
                                    gain=max(0,cref-result["cut"]); gains.append(gain)
                                    best=min(best,result["cut"]); score_units+=result["score_units"]
                                    emit(stream,dict(stage="development",case=key,model=model,
                                        setting=setting,shot=shot,seed=seed,Cref=cref,gain=gain,
                                        field=field.tolist(),counts=None if counts is None else counts.tolist(),
                                        **extra,**result))
                                setting_seconds=time.perf_counter()-setting_start
                                time_budgets[model]+=setting_seconds; totals[model][setting]+=sum(gains)
                                records.append({"case":key,"model":model,"setting":setting,
                                    "proposals":len(gains),"score_units":score_units,"sum_gain":sum(gains),
                                    "best_cut":best,"setup_seconds":setup_seconds,
                                    "field_sampling_and_PIT_seconds":sample_seconds,"decoder_seconds":decoder_seconds,
                                    "observed_setting_seconds_including_recording":setting_seconds})
                    budget=4*spec["draws_per_tuple"]*expected_units
                    for baseline in BASELINES:
                        timed=TimedBaselineStream(stream); tag={"stage":"classical_search","case":key}
                        seed=base.seed_for(481200,key,baseline)
                        if baseline=="KL_collective":
                            result=adaptive.kl_collective(a,common["reference_subset"],seed,budget,timed,tag)
                        elif baseline=="block_matching":
                            result=block_matching(a,common["source_S0"],common["inside_order"],
                                common["outside_order"],delta,cref,seed,budget,timed,tag)
                        elif baseline=="spectral_coherent_rounding":
                            result=spectral_coherent_rounding(a,contexts,priority,cref,seed,budget,timed,tag)
                        else:
                            result=base.classical_search(a,common["reference_subset"],baseline,seed,budget,timed,tag)
                        if result["candidate_scores"]!=budget or len(timed.rows)!=budget:
                            raise ArithmeticError("Classical informative score population changed")
                        frontiers={}
                        for model in MODELS:
                            limit=time_budgets[model]
                            eligible=[value for elapsed,value in timed.rows if elapsed<=limit]
                            frontiers[model]={"observed_model_seconds":limit,
                                "baseline_scores_within_time_and_score_caps":len(eligible),
                                "best_cut_within_joint_caps":min([cref]+eligible),"score_ceiling":budget}
                        records.append(dict(tag,**result,joint_observed_time_frontiers=frontiers))
                stream.flush(); zipped.flush(); raw_file.flush()
                if sum(p.stat().st_size for p in args.output.rglob("*") if p.is_file())>spec["maximum_new_output_bytes"]-2097152:
                    raise RuntimeError("Scientific data approached cap; retain partial run")
    attempts={model:sum(r.get("proposals",0) for r in records if r["model"]==model) for model in MODELS}
    expected_attempts=64*len(complete_cases)
    if set(attempts.values())!={expected_attempts}:
        raise ArithmeticError("Tested sample population changed")
    population_complete=len(complete_cases)==len(spec["cases"])
    selected={model:int(np.argmax(values)) if values.max()>0 else None for model,values in totals.items()}
    ledger={}
    for model in MODELS:
        arm=[r for r in records if r["model"]==model]
        optical=model in ("bosonic","distinguishable","species4")
        ledger[model]={"decoded_proposals":attempts[model],
            "simulated_optical_attempts":attempts[model] if optical else 0,
            "simulated_injected_photons":sum(c["r"]*64 for c in complete_cases) if optical else 0,
            "classical_field_samples":0 if optical else attempts[model],
            "online_partial_marginal_scores":sum(r["score_units"]-r["proposals"] for r in arm if "proposals" in r),
            "online_final_cut_scores":attempts[model]}
    summary={"status":"EXPLORATORY_DEV_VETO_ONLY" if population_complete else "NUMERICAL_INCONCLUSIVE_POPULATION",
        "positive_accepted":False,"full_frozen_population_completed":population_complete,
        "actual_QPU_calls":0,"actual_QPU_photons":0,"simulated_eta":1.,
        "heldout_graphs_opened":False,"optimum_used":False,"attempts_per_model":attempts,
        "selected_independently_on_tested_DEV_only":selected,"primary_resource_ledger":ledger,
        "empirical_calibration_draws":0,"analytic_coherent_marginals":True,
        "coherent_phase_sampler":"continuous_uniform_all_production_arms_and_rounding",
        "setting_total_gains":{model:values.tolist() for model,values in totals.items()},
        "common_frontend":commons,"records":records,
        "cpu_seconds_inside_main":time.process_time()-start_cpu,
        "wall_seconds_inside_main":time.perf_counter()-start_wall,
        "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
        "simulation_time_is_QPU_time":False,
        "score_units_are_informative_evaluations_not_every_repeated_call":True}
    (args.output/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    if sum(p.stat().st_size for p in args.output.rglob("*") if p.is_file())>spec["maximum_new_output_bytes"]:
        raise RuntimeError("Scientific data exceeded cap; do not accept run")
    print(json.dumps({key:value for key,value in summary.items() if key not in ("common_frontend","records")}))


if __name__=="__main__":
    main()
