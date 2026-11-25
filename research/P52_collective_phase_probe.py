"""P52 fixed-low-moment phase discriminator; no graph or optimizer positive.

Full compact Fock laws, exact finite tie integration, all b4 regroupings and
predeclared phase Monte Carlo. No permanent pruning or hardware interface.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.optimize import linprog, OptimizeWarning

from P43_global_gain_probe import seed_for

THETAS = (0., math.pi/4, math.pi/2, 3*math.pi/4)
DRAW_COUNT = 262144
BATCH_SIZE = 4096
UNION_COORDINATES = 392
CONFIDENCE_FAILURE = .01
SOURCE_TOLERANCE = 5e-11
NULL_TOLERANCE = 5e-10
FIT_TOLERANCE = 1e-9


def serial(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key):serial(item) for key,item in value.items()}
    if isinstance(value, (list,tuple)):
        return [serial(item) for item in value]
    return value


def compositions(m, total):
    if m == 1:
        yield (total,)
    else:
        for first in range(total+1):
            for rest in compositions(m-1,total-first):
                yield (first,)+rest


class FockSpace:
    """Only C(m+t-1,t) states per level, with scalar base-(r+1) KEYS.

    A key is not an index in a (r+1)^m array. Sorted compact key vectors and
    searchsorted provide mappings, including the bounded 330x330 convolution.
    """
    def __init__(self,m,maximum):
        if not 1 <= m <= 8 or not 0 <= maximum <= 8:
            raise ValueError("Bounded P52 Fock space requires m<=8,r<=8")
        self.m,self.maximum = m,maximum
        self.powers = (maximum+1)**np.arange(m,dtype=np.int64)
        self.counts = [np.asarray(list(compositions(m,t)),dtype=np.int16) for t in range(maximum+1)]
        self.keys = [counts@self.powers for counts in self.counts]
        self.sorters = [np.argsort(keys) for keys in self.keys]
        self.sorted_keys = [keys[order] for keys,order in zip(self.keys,self.sorters)]
        self.transitions,self.factors = [],[]
        for total in range(maximum):
            keys = self.keys[total][:,None]+self.powers[None,:]
            self.transitions.append(self.lookup_keys(keys,total+1).astype(np.int32))
            self.factors.append(np.sqrt(self.counts[total]+1.))

    def lookup_keys(self,keys,total):
        positions=np.searchsorted(self.sorted_keys[total],keys)
        if (np.any(positions >= len(self.sorted_keys[total]))
                or np.any(self.sorted_keys[total][positions] != keys)):
            raise ArithmeticError("A compact Fock key was missing")
        return self.sorters[total][positions]

    def convolution_map(self,first,second):
        if first+second>self.maximum:
            raise ValueError("Convolution outside compact total")
        return self.lookup_keys(self.keys[first][:,None]+self.keys[second][None,:],first+second).astype(np.int32)


def creation_law(u,sources,space):
    """Normalized Fock creation recurrence, CF inputs only, no amplitude pruning."""
    sources=tuple(sources)
    if (u.shape != (space.m,space.m) or len(sources)>space.maximum
            or len(set(sources)) != len(sources)
            or any(not 0 <= source < space.m for source in sources)):
        raise ValueError("Distinct valid CF input labels are required")
    amplitude=np.ones(1,dtype=np.complex128)
    for total,source in enumerate(sources):
        contributions=(amplitude[:,None]*u[:,source][None,:]*space.factors[total]).ravel()
        updated=np.zeros(len(space.counts[total+1]),dtype=np.complex128)
        np.add.at(updated,space.transitions[total].ravel(),contributions)
        amplitude=updated
    probability=abs(amplitude)**2
    mass=float(probability.sum())
    if not np.all(np.isfinite(probability)) or abs(mass-1.)>SOURCE_TOLERANCE:
        raise ArithmeticError("Creation recurrence does not give a normalized source law")
    return amplitude,probability


def w4():
    return np.asarray([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]],dtype=float)/2


def interferometer(theta):
    w=w4()
    dw=np.exp(1j*np.arange(4)*theta)[:,None]*w
    return np.block([[w,dw],[w,-dw]])/math.sqrt(2)


def all_groupings():
    """Each of 35 unordered complementary 4+4 splits appears once, with 0 first."""
    return [(tuple((0,)+other),tuple(i for i in range(8) if i not in (0,)+other))
            for other in itertools.combinations(range(1,8),3)]


def grouping_permutation():
    permutation=np.asarray([0,1,2,3,6,7,4,5])
    groupings=all_groupings()
    index={first:i for i,(first,_) in enumerate(groupings)}
    return np.asarray([index[tuple(sorted(permutation[list(first)]))] for first,_ in groupings],dtype=np.int64)


class RankDecoder:
    """Analytic uniform tie pushforward, represented in float64, never sampled."""
    def __init__(self,counts,k):
        self.counts=np.asarray(counts)
        self.m=self.counts.shape[1]
        if not 1 <= k <= self.m:
            raise ValueError("Nonempty balanced-ranking size required")
        self.subsets=list(itertools.combinations(range(self.m),k))
        self.masks=np.asarray([sum(1<<i for i in subset) for subset in self.subsets],dtype=np.int64)
        index={int(mask):i for i,mask in enumerate(self.masks)}
        self.membership=np.asarray([[int(i in subset) for i in range(self.m)] for subset in self.subsets],dtype=np.int8)
        self.edges=np.asarray(list(itertools.combinations(range(self.m),2)),dtype=np.int16)
        self.crossing=np.asarray([np.logical_xor(self.membership[:,i],self.membership[:,j])
                                 for i,j in self.edges],dtype=float).T
        self.push=np.zeros((len(counts),len(self.subsets)),dtype=float)
        self.tie_denominators=np.empty(len(counts),dtype=np.int16)
        for state,row in enumerate(self.counts):
            threshold=np.sort(row)[-k]
            high=tuple(np.flatnonzero(row>threshold))
            tied=tuple(np.flatnonzero(row==threshold))
            choices=list(itertools.combinations(tied,k-len(high)))
            denominator=len(choices)
            self.tie_denominators[state]=denominator
            fixed=sum(1<<int(i) for i in high)
            for choice in choices:
                mask=fixed+sum(1<<int(i) for i in choice)
                self.push[state,index[mask]]=1./denominator

    def apply(self,probabilities):
        decoded=np.asarray(probabilities)@self.push
        return decoded,decoded@self.crossing


def factorial_moments(probabilities,counts,maximum=3):
    labels=[label for total in range(maximum+1) for label in compositions(counts.shape[1],total)]
    moments=[]
    for label in labels:
        value=np.ones(len(counts))
        for i,power in enumerate(label):
            for offset in range(power):
                value*=counts[:,i]-offset
        moments.append(np.asarray(probabilities)@value)
    return np.asarray(labels,dtype=np.int8),np.asarray(moments).T


def collective_fourth(counts,probabilities):
    first=(counts[:,0]-counts[:,4])**2-counts[:,0]-counts[:,4]
    second=(counts[:,1]-counts[:,5])**2-counts[:,1]-counts[:,5]
    return np.asarray(probabilities)@(first.astype(np.float64)*second)


def crossing_row_sums(kernel,edges,m):
    kernel=np.asarray(kernel)
    rows=np.zeros(kernel.shape[:-1]+(m,))
    for coordinate,(i,j) in enumerate(edges):
        rows[...,i]+=kernel[...,coordinate]
        rows[...,j]+=kernel[...,coordinate]
    return rows


def phase_counts(u,rng,size,total):
    """Vectorized categorical trials conditional on continuous input phases."""
    m=len(u)
    angles=rng.uniform(0.,2*math.pi,(size,m))
    coefficient=np.exp(1j*angles)/math.sqrt(m)
    probability=abs(coefficient@u.T)**2
    mass=probability.sum(axis=1)
    maximum_error=float(abs(mass-1.).max())
    if maximum_error>5e-12:
        raise ArithmeticError("Invalid phase-field probability mass")
    probability=probability/mass[:,None]
    raw_cdf=np.cumsum(probability,axis=1)
    cdf=np.minimum(1.,raw_cdf)
    cdf[:,-1]=1.
    correction=float(abs(cdf-raw_cdf).max())
    uniforms=rng.random((size,total))
    modes=np.sum(uniforms[:,:,None]>=cdf[:,None,:],axis=2)
    counts=np.zeros((size,m),dtype=np.uint8)
    np.add.at(counts,(np.repeat(np.arange(size),total),modes.ravel()),1)
    return counts,{"angles_sha256":hashlib.sha256(angles.astype("<f8").tobytes()).hexdigest(),
                   "categorical_uniforms_sha256":hashlib.sha256(uniforms.astype("<f8").tobytes()).hexdigest(),
                   "counts_sha256":hashlib.sha256(counts.tobytes()).hexdigest(),
                   "maximum_raw_probability_mass_error":maximum_error,
                   "maximum_CDF_roundoff_correction":correction}


def phase_histogram(u,space,index,stream,draws=DRAW_COUNT,batch_size=BATCH_SIZE):
    if draws != DRAW_COUNT or batch_size != BATCH_SIZE:
        raise ValueError("Frozen P52 MC effort required")
    seed=seed_for(5201001,index)
    rng=np.random.Generator(np.random.PCG64(seed))
    histogram=np.zeros(len(space.counts[8]),dtype=np.int64)
    records=[]
    for batch in range(draws//batch_size):
        state_before=hashlib.sha256(json.dumps(rng.bit_generator.state,sort_keys=True).encode()).hexdigest()
        counts,digests=phase_counts(u,rng,batch_size,8)
        positions=space.lookup_keys(counts@space.powers,8)
        raw_histogram=np.bincount(positions,minlength=len(histogram)).astype(np.int64)
        histogram+=raw_histogram
        row={"theta_index":index,"seed":seed,"batch":batch,"draws":batch_size,
             "first_draw":batch*batch_size,"state_before_sha256":state_before,
             "state_after_sha256":hashlib.sha256(json.dumps(rng.bit_generator.state,sort_keys=True).encode()).hexdigest(),
             "batch_histogram_sha256":hashlib.sha256(raw_histogram.astype("<i8").tobytes()).hexdigest(),**digests}
        stream.write(json.dumps(row,allow_nan=False)+"\n")
        records.append(row)
    if int(histogram.sum())!=draws:
        raise ArithmeticError("Missing phase-calibration trials")
    return histogram,records


def phase_epsilon():
    return math.sqrt(math.log(2*UNION_COORDINATES/CONFIDENCE_FAILURE)/(2*DRAW_COUNT))


def native_single_thread_check():
    """Pinned SciPy bundled HiGHS options, no external highspy dependency."""
    import scipy.optimize._highspy._core as native
    solver=native._Highs()
    options=native.HighsOptions()
    options.threads=1
    options.parallel="off"
    options.random_seed=5201001
    options.time_limit=1.
    if solver.passOptions(options)!=native.HighsStatus.kOk:
        raise RuntimeError("Native HiGHS refused fixed options")
    readback={}
    for key,expected in (("threads",1),("parallel","off"),("random_seed",5201001),("time_limit",1.)):
        status,value=solver.getOptionValue(key)
        if status!=native.HighsStatus.kOk or value!=expected:
            raise RuntimeError("Native HiGHS option readback mismatch")
        readback[key]=value
    return readback


def verify_coefficients(raw,library,target,mc_start=None,epsilon=0.):
    raw=np.asarray(raw,dtype=float)
    library=np.asarray(library,dtype=float)
    target=np.asarray(target,dtype=float)
    if (raw.shape!=(len(library),) or not np.all(np.isfinite(raw))
            or raw.min() < -FIT_TOLERANCE or abs(float(raw.sum())-1.)>FIT_TOLERANCE):
        return {"verified":False,"raw_coefficients":[float(x) if np.isfinite(x) else str(x) for x in raw],
                "reason":"invalid_simplex_candidate"}
    weights=np.maximum(raw,0.)
    if weights.sum()<=0:
        return {"verified":False,"reason":"zero_simplex_mass"}
    weights/=weights.sum()
    reconstructed=weights@library
    residual=float(abs(reconstructed-target).max())
    mc_weight=float(weights[mc_start:].sum()) if mc_start is not None else 0.
    return {"verified":bool(weights.min()>=0 and abs(float(weights.sum())-1.)<=5e-13),
            "raw_coefficients":raw.tolist(),"used_coefficients":weights.tolist(),
            "raw_minimum":float(raw.min()),"raw_sum_error":float(raw.sum()-1.),
            "projection_L1":float(abs(weights-raw).sum()),"used_minimum":float(weights.min()),
            "used_sum_error":float(weights.sum()-1.),"reconstructed_crossing":reconstructed.tolist(),
            "verified_Linfty_residual":residual,"MC_mixture_weight":mc_weight,
            "MC_uniform_bound_term":mc_weight*epsilon,
            "total_residual_plus_MC_term":residual+mc_weight*epsilon,
            "deterministic_roundoff_not_interval_certified":True}


def convex_fit(library,target,mc_start=None,epsilon=0.):
    """Finite numerical mean fit, never a full-law or separating certificate."""
    started_wall,started_cpu=time.perf_counter(),time.process_time()
    options={"time_limit":1.,"threads":1,"parallel":False,"random_seed":5201001,
             "presolve":True,"dual_feasibility_tolerance":1e-9,"primal_feasibility_tolerance":1e-9}
    try:
        native=native_single_thread_check()
        library,target=np.asarray(library,dtype=float),np.asarray(target,dtype=float)
        columns=len(library)
        objective=np.r_[np.zeros(columns),1.]
        matrix=np.vstack((np.column_stack((library.T,-np.ones(28))),
                          np.column_stack((-library.T,-np.ones(28)))))
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always",OptimizeWarning)
            result=linprog(objective,A_ub=matrix,b_ub=np.r_[target,-target],
                           A_eq=np.r_[np.ones(columns),0.][None,:],b_eq=[1.],
                           bounds=[(0.,None)]*(columns+1),method="highs-ds",options=options)
        messages=[str(warning.message) for warning in seen]
        invalid=[warning for warning in seen if not (
            issubclass(warning.category,OptimizeWarning)
            and str(warning.message).startswith("Unrecognized options detected: ")
            and str(warning.message).endswith("These will be passed to HiGHS verbatim."))]
        if invalid:
            raise RuntimeError("Native invalid/ignored HiGHS option: "+" | ".join(str(w.message) for w in invalid))
        verified=({"verified":False,"reason":"no_solver_candidate"} if result.x is None else
                  verify_coefficients(result.x[:columns],library,target,mc_start,epsilon))
        matched=verified["verified"] and verified["verified_Linfty_residual"]<=FIT_TOLERANCE
        status=("MC_APPROXIMATE_MEAN_CANDIDATE" if mc_start is not None and verified["verified"] else
                ("NUMERICAL_MEAN_MATCH" if matched else "NO_VERIFIED_TOLERANCE_MATCH"))
        return {"status":status,"solver_status":int(result.status),"solver_success":bool(result.success),
                "solver_message":str(result.message),"solver_objective":None if result.fun is None else float(result.fun),
                "options":options,"native_options_readback":native,"warnings":messages,
                "verification":verified,"wall_seconds":time.perf_counter()-started_wall,
                "cpu_seconds":time.process_time()-started_cpu,
                "nonmatch_is_NOT_separation_or_optimization_advantage":True}
    except (ImportError,AttributeError,TypeError,ValueError,RuntimeError) as error:
        return {"status":"INCONCLUSIVE_SOLVER","error":repr(error),"options":options,
                "wall_seconds":time.perf_counter()-started_wall,"cpu_seconds":time.process_time()-started_cpu}


def save_npz(path,**arrays):
    with path.open("xb") as stream:
        np.savez_compressed(stream,**arrays)


def check_output(output,limit,reserve=0):
    if sum(path.stat().st_size for path in output.rglob("*") if path.is_file())>limit-reserve:
        raise RuntimeError("P52 output cap approached; preserve partial results without retry")


def validate_spec(spec):
    if (spec["modes"]!=8 or spec["photons"]!=8 or spec["target_size"]!=4
            or spec["theta_pi_multipliers"]!=[0.,.25,.5,.75]
            or spec["phase_draws_per_theta"]!=DRAW_COUNT or spec["phase_batch_size"]!=BATCH_SIZE
            or spec["phase_seed_root"]!=5201001 or spec["confidence_failure"]!=CONFIDENCE_FAILURE
            or spec["simultaneous_phase_coordinates"]!=UNION_COORDINATES
            or spec["source_tolerance"]!=SOURCE_TOLERANCE or spec["null_tolerance"]!=NULL_TOLERANCE
            or spec["fit_tolerance"]!=FIT_TOLERANCE or spec["LP_seconds_per_fit"]!=1.
            or spec["include_optional_MC_fits"] is not True or spec["positive_acceptance_allowed"] is not False
            or spec["maximum_cpu_seconds"]!=60 or spec["maximum_wall_seconds"]!=90
            or spec["maximum_threads"]!=1 or spec["maximum_planned_arrays_bytes"]!=268435456
            or spec["maximum_new_output_bytes"]!=33554432):
        raise ValueError("Frozen P52 discriminator changed")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args();spec=json.loads(args.spec.read_text());validate_spec(spec)
    args.output.mkdir(parents=True,exist_ok=False)
    start_wall,start_cpu=time.perf_counter(),time.process_time()
    space=FockSpace(8,8)
    decoder=RankDecoder(space.counts[8],4)
    convolution=space.convolution_map(4,4).ravel()
    groups=list(itertools.combinations(range(8),4));group_index={group:i for i,group in enumerate(groups)}
    splits=all_groupings()
    if (len(space.counts[8]),len(space.counts[4]),len(decoder.subsets),len(groups),len(splits))!=(6435,330,70,70,35):
        raise ArithmeticError("The complete P52 state/group population changed")
    save_npz(args.output/"geometry.npz",occupations8=space.counts[8],occupations4=space.counts[4],
             subsets=np.asarray(decoder.subsets),subset_masks=decoder.masks,edges=decoder.edges,
             membership=decoder.membership,tie_denominators=decoder.tie_denominators,
             groups=np.asarray(groups),splits=np.asarray(splits),convolution_map=convolution)
    bosonic,b4,decoded_b,decoded_b4,cross_b,cross_b4,source_rows=[],[],[],[],[],[],[]
    for index,theta in enumerate(THETAS):
        u=interferometer(theta)
        amplitude,probability=creation_law(u,range(8),space)
        group_probability=np.asarray([creation_law(u,group,space)[1] for group in groups])
        mixed=[]
        for first,second in splits:
            weights=np.multiply.outer(group_probability[group_index[first]],group_probability[group_index[second]]).ravel()
            mixed.append(np.bincount(convolution,weights=weights,minlength=len(probability)))
        mixed=np.asarray(mixed)
        b_rank,b_cross=decoder.apply(probability)
        b4_rank,b4_cross=decoder.apply(mixed)
        q=abs(u)**2;mu=q.sum(axis=1);projection=u@u.conj().T
        covariance=np.diag(mu)+abs(projection)**2-2*q@q.T
        row={"theta_index":index,"theta":theta,"B_mass_error":float(probability.sum()-1.),
             "maximum_b4_mass_error":float(abs(mixed.sum(axis=1)-1).max()),
             "unitary_residual":float(abs(u.conj().T@u-np.eye(8)).max()),
             "Q_flat_residual":float(abs(q-1/8).max()),"mu_residual":float(abs(mu-1).max()),
             "covariance_residual":float(abs(covariance-(2*np.eye(8)-np.ones((8,8))/4)).max()),
             "B_rank_mass_error":float(b_rank.sum()-1.)}
        source_rows.append(row)
        if max(abs(row[key]) for key in ("B_mass_error","maximum_b4_mass_error","unitary_residual",
                                        "Q_flat_residual","mu_residual","covariance_residual","B_rank_mass_error"))>SOURCE_TOLERANCE:
            raise ArithmeticError("Invalid physical/numerical P52 source invariant")
        save_npz(args.output/f"theta_{index}.npz",u=u,B_amplitudes=amplitude,B_probability=probability,
                 group_probability=group_probability,b4_probability=mixed,
                 B_rank=b_rank,B_crossing=b_cross,b4_rank=b4_rank,b4_crossing=b4_cross,
                 Q=q,mu=mu,covariance=covariance)
        bosonic.append(probability);b4.append(mixed);decoded_b.append(b_rank);decoded_b4.append(b4_rank)
        cross_b.append(b_cross);cross_b4.append(b4_cross)
        check_output(args.output,spec["maximum_new_output_bytes"],2097152)
    bosonic,b4,decoded_b,decoded_b4,cross_b,cross_b4=map(np.asarray,(bosonic,b4,decoded_b,decoded_b4,cross_b,cross_b4))
    labels,moments=factorial_moments(bosonic,space.counts[8],3)
    fourth=collective_fourth(space.counts[8],bosonic)
    fourth_expected=np.asarray([.5+math.cos(theta)**2 for theta in THETAS])
    one_mode_pmf=np.asarray([[np.bincount(space.counts[8][:,mode],weights=probability,minlength=9)
                              for mode in range(8)] for probability in bosonic])
    nulls={"B_theta3_equals_theta1_full_law":float(abs(bosonic[3]-bosonic[1]).max()),
           "Walsh_theta0_B_crossing_equals4over7":float(abs(cross_b[0]-4/7).max()),
           "b4_theta3_mapped_theta1_full_laws":float(abs(b4[3]-b4[1][grouping_permutation()]).max()),
           "canonical_b4_full_law_invariance":float(abs(b4[:,0]-b4[0,0]).max()),
           "all_total_order_le3_moment_invariance":float(abs(moments-moments[0]).max()),
           "one_mode_PMF_phase_and_mode_invariance":float(abs(one_mode_pmf-one_mode_pmf[0,0]).max()),
           "collective_fourth_analytic_fixture_error":float(abs(fourth-fourth_expected).max()),
           "B_crossing_sum_equals16":float(abs(cross_b.sum(axis=1)-16).max()),
           "b4_crossing_sum_equals16":float(abs(cross_b4.sum(axis=2)-16).max()),
           "B_crossing_row_sums_equal4":float(abs(crossing_row_sums(cross_b,decoder.edges,8)-4).max()),
           "b4_crossing_row_sums_equal4":float(abs(crossing_row_sums(cross_b4,decoder.edges,8)-4).max()),
           "tie_pushforward_row_mass":float(abs(decoder.push.sum(axis=1)-1).max())}
    phase_histograms,phase_decoded,phase_crossing,phase_records=[],[],[],[]
    with (args.output/"phase_batches.jsonl.gz").open("xb") as raw,gzip.GzipFile(fileobj=raw,mode="wb",mtime=0,compresslevel=3) as zipped:
        with io.TextIOWrapper(zipped,encoding="utf8") as stream:
            for index,theta in enumerate(THETAS):
                histogram,records=phase_histogram(interferometer(theta),space,index,stream)
                phase_probability=histogram/DRAW_COUNT
                rank,crossing=decoder.apply(phase_probability)
                save_npz(args.output/f"phase_theta_{index}.npz",histogram=histogram,
                         phase_rank=rank,phase_crossing=crossing)
                phase_histograms.append(histogram);phase_decoded.append(rank);phase_crossing.append(crossing)
                phase_records.extend(records)
                stream.flush();zipped.flush();raw.flush()
                check_output(args.output,spec["maximum_new_output_bytes"],2097152)
    phase_decoded,phase_crossing=np.asarray(phase_decoded),np.asarray(phase_crossing)
    epsilon=phase_epsilon()
    uniform_rank=np.full(70,1/70)
    uniform_crossing=uniform_rank@decoder.crossing
    nulls.update(uniform_crossing_equals4over7=float(abs(uniform_crossing-4/7).max()),
                 phase_rank_mass=float(abs(phase_decoded.sum(axis=1)-1).max()),
                 phase_crossing_row_sums_equal4=float(abs(crossing_row_sums(phase_crossing,decoder.edges,8)-4).max()))
    library=np.vstack((cross_b4.reshape((-1,28)),uniform_crossing[None,:]))
    library_labels=[{"kind":"b4","theta_index":t,"grouping_index":g,
                     "source_groups":splits[g]} for t in range(4) for g in range(35)]+[{"kind":"uniform70"}]
    fits=[]
    for index in range(4):
        fits.append({"target_theta_index":index,"library":"deterministic_b4_and_uniform",
                     **convex_fit(library,cross_b[index])})
    augmented=np.vstack((library,phase_crossing))
    for index in range(4):
        fits.append({"target_theta_index":index,"library":"deterministic_plus_phase_MC",
                     **convex_fit(augmented,cross_b[index],len(library),epsilon)})
    closure={"deterministic_library_labels":library_labels,"deterministic_library_crossing":library,
             "augmented_MC_theta_indices":list(range(4)),"augmented_MC_crossing":phase_crossing,
             "target_B_crossing":cross_b,"fits":fits,"phase_epsilon":epsilon,
             "confidence_failure":CONFIDENCE_FAILURE,"source_errors_not_interval_certified":True,
             "no_full_law_or_tail_certificate":True,"no_graph_or_separating_hyperplane_selected":True}
    (args.output/"closure.json").write_text(json.dumps(serial(closure),indent=2,allow_nan=False)+"\n")
    summary={"status":"FINITE_DISCRIMINATOR_ONLY","positive_accepted":False,"actual_QPU_calls":0,
             "graph_generated":False,"optimum_or_known_partition_used":False,
             "all_occupations_retained":True,"source_diagnostics":source_rows,
             "null_residuals":nulls,"nulls_within_tolerance":all(value<=NULL_TOLERANCE for value in nulls.values()),
             "factorial_moment_labels":labels,"factorial_moments_order_le3":moments,
             "B_one_mode_PMF_all_modes_and_phases":one_mode_pmf,
             "collective_fourth":fourth,"collective_fourth_analytic":fourth_expected,
             "uniform_rank":uniform_rank,"uniform_crossing":uniform_crossing,
             "exact_uniform_rank_controls":["distinguishable","sphere","Gaussian_Bcov","independent_variance",
                                             "product_one_mode_B","static","jitter"],
             "uniform_rank_justification":"exchangeability_and_uniform_independent_ties;not_simulated_duplicate_models",
             "B_crossing":cross_b,"B_rank":decoded_b,"phase_crossing":phase_crossing,"phase_rank":phase_decoded,
             "phase_draws_per_theta":DRAW_COUNT,"phase_total_draws":4*DRAW_COUNT,
             "phase_batch_count":len(phase_records),"phase_coordinate_union":UNION_COORDINATES,
             "phase_epsilon":epsilon,"phase_confidence_failure":CONFIDENCE_FAILURE,
             "phase_bound_applies_to_70_subsets_28_edges_NOT_6435_bins_or_TV":True,
             "phase_duplicate_law_not_same_seed":True,
             "phase_theta3_theta1_max_subset_or_edge_difference":float(max(abs(phase_decoded[3]-phase_decoded[1]).max(),
                                                                          abs(phase_crossing[3]-phase_crossing[1]).max())),
             "phase_theta3_theta1_within_2epsilon":bool(max(abs(phase_decoded[3]-phase_decoded[1]).max(),
                                                            abs(phase_crossing[3]-phase_crossing[1]).max())<=2*epsilon),
             "phase_Walsh_theta0_crossing_max_error":float(abs(phase_crossing[0]-4/7).max()),
             "phase_Walsh_theta0_crossing_within_epsilon":bool(abs(phase_crossing[0]-4/7).max()<=epsilon),
             "Walsh_theta0_uniform_crossing_does_NOT_imply_uniform70_rank":True,
             "fourth_phase_cell_is_symmetry_calibration_not_independent_direction":True,
             "fit_summaries":[{key:fit[key] for key in ("target_theta_index","library","status")} for fit in fits],
             "CPU_seconds_inside_main":time.process_time()-start_cpu,
             "wall_seconds_inside_main":time.perf_counter()-start_wall,
             "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             "spec_sha256":hashlib.sha256(args.spec.read_bytes()).hexdigest(),
             "simulation_cost_is_NOT_QPU_cost":True,"feasible70_state_classical_enumeration_trivial":True,
             "heldout_replication_total_resources_hardware_goal_remains_open":True}
    (args.output/"summary.json").write_text(json.dumps(serial(summary),indent=2,allow_nan=False)+"\n")
    check_output(args.output,spec["maximum_new_output_bytes"])
    print(json.dumps({key:serial(summary[key]) for key in ("status","positive_accepted","nulls_within_tolerance",
                      "null_residuals","phase_epsilon","fit_summaries","CPU_seconds_inside_main","wall_seconds_inside_main")}))


if __name__=="__main__":
    main()
