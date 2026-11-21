#!/usr/bin/env python3
"""P21: optimum-blind feasible classical searches and optical landscape probes.

Reproduce from repository root with the pinned environment:
    OPENBLAS_NUM_THREADS=1 PYTHONPATH=src .venv/bin/python experiments/phase2_classical_search.py --output experiments/P21_classical_search
All chosen partitions, costs, seeds, and setup/search times are retained.
Nothing here accesses hardware. Existing output evidence is never overwritten.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
import numpy as np
import scipy
from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning as Graph
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

ROOT=Path(__file__).resolve().parents[1]
SOURCE_PATHS=[Path(__file__).relative_to(ROOT),Path('pyproject.toml'),
    *[Path('src/photonic_balanced_partitioning')/p for p in (
    '__init__.py','problems/min_bisection.py','photonic/__init__.py',
    'photonic/comparison.py','photonic/mesh.py','photonic/fixed_photon_obliq.py',
    'photonic/collision_aware.py','photonic/cvar_fixed_photon.py',
    'photonic/penalty_obliq.py','photonic/objectives.py')]]


def clean(value):
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,np.ndarray)):return [clean(v) for v in value]
    if isinstance(value,(float,np.floating)):return float(value) if math.isfinite(value) else None
    if isinstance(value,np.integer):return int(value)
    return value


def dump(path,value):
    path.write_text(json.dumps(clean(value),indent=2,allow_nan=False)+'\n')


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def make_graph(n,family,seed):
    if family=='path':return Graph.path_graph(n)
    if family=='cycle':return Graph.cycle_graph(n)
    if family=='regular':return Graph.random_regular(n,min(3,n-1),seed)
    if family=='erdos_renyi':return Graph.erdos_renyi(n,.5,seed)
    if family=='weighted':return Graph.erdos_renyi(n,.7,seed,(.25,2.))
    if family=='planted':return Graph.planted_partition(n,n//2,seed=seed)
    raise ValueError(family)


def cut(partition,edges):
    selected=set(partition)
    return float(sum(w for i,j,w in edges if (i in selected)!=(j in selected)))


def relabel_edges(edges,permutation):
    return tuple(sorted((min(permutation[i],permutation[j]),max(permutation[i],permutation[j]),float(w)) for i,j,w in edges))


def exact_reference(n,edges):
    """Complete enumeration, counted as C(n,n/2) score queries; no free oracle."""
    start=time.perf_counter()
    states=list(combinations(range(n),n//2))
    values=np.array([cut(S,edges) for S in states])
    optimum=float(values.min());mask=np.isclose(values,optimum,atol=1e-9,rtol=0)
    return dict(optimum=optimum,worst=float(values.max()),query_count=len(values),
        optimal_count=int(mask.sum()),first_optimum_query=int(np.flatnonzero(mask)[0])+1,
        complete_runtime_seconds=time.perf_counter()-start,
        partitions=states,energies=values.tolist())


def feasible_search(n,edges,algorithm,budget,seed):
    """Training has no optimum/reference input and never uses oracle stopping.

    One query scores one feasible partition; every evaluated proposal counts,
    including rejected swaps and repeated partitions. The best evaluated state
    is retained. Spectral setup is timed separately and its first cut is query 1.
    """
    if n<2 or n%2 or budget<1:raise ValueError('Require even n>=2 and positive budget')
    rng=np.random.default_rng(seed+77)
    k=n//2;trace=[];best=float('inf');best_partition=None
    start=time.perf_counter();eigensolves=0
    def random_partition():return tuple(sorted(rng.choice(n,k,replace=False).tolist()))
    def evaluate(part,stage):
        nonlocal best,best_partition
        part=tuple(sorted(part))
        assert len(part)==k and len(set(part))==k and all(0<=i<n for i in part)
        energy=cut(part,edges)
        if energy<best:best,best_partition=energy,part
        trace.append(dict(query=len(trace)+1,partition=part,cost=energy,stage=stage,
                          best_cost_so_far=best))
        return energy
    if algorithm=='spectral_swap_local':
        lap=np.zeros((n,n))
        for i,j,w in edges:
            lap[i,i]+=w;lap[j,j]+=w;lap[i,j]-=w;lap[j,i]-=w
        _,vectors=np.linalg.eigh(lap);eigensolves=1
        # Fixed-cardinality median rounding; sign reversal gives the complement.
        current=tuple(sorted(np.argsort(vectors[:,1],kind='stable')[:k].tolist()))
    else:current=random_partition()
    setup_seconds=time.perf_counter()-start
    search_start=time.perf_counter()
    if algorithm=='random_feasible':
        for _ in range(budget):evaluate(random_partition(),'independent_uniform')
    elif algorithm=='swap_anneal':
        current_energy=evaluate(current,'initial_uniform')
        weight_scale=max(float(np.mean([abs(w) for _,_,w in edges])) if edges else 1.,1e-12)
        for query in range(1,budget):
            chosen=set(current)
            a=int(rng.choice(sorted(chosen)))
            b=int(rng.choice(sorted(set(range(n))-chosen)))
            proposed=tuple(sorted((chosen-{a})|{b}))
            energy=evaluate(proposed,'swap_proposal')
            temperature=weight_scale*(.02**(query/max(budget-1,1)))
            delta=energy-current_energy
            accept=delta<=0 or rng.random()<math.exp(-delta/temperature)
            trace[-1]['accepted']=bool(accept)
            trace[-1]['temperature']=temperature
            if accept:current,current_energy=proposed,energy
    elif algorithm=='spectral_swap_local':
        current_energy=evaluate(current,'spectral_start')
        while len(trace)<budget:
            inside=set(current);outside=set(range(n))-inside
            swaps=[(i,j) for i in sorted(inside) for j in sorted(outside)]
            rng.shuffle(swaps)
            next_energy,next_part=current_energy,current
            for i,j in swaps:
                if len(trace)>=budget:break
                proposed=tuple(sorted((inside-{i})|{j}))
                value=evaluate(proposed,'best_improvement_scan')
                if value<next_energy:next_energy,next_part=value,proposed
            if next_energy<current_energy:
                current,current_energy=next_part,next_energy
            elif len(trace)<budget:
                # Fixed restart rule, no knowledge of C*. A restart cut is charged.
                current=random_partition();current_energy=evaluate(current,'uniform_restart')
    else:raise ValueError(algorithm)
    return dict(algorithm=algorithm,seed=seed,n_queries=len(trace),trace=trace,
        best_cost=best,best_partition=best_partition,setup_runtime_seconds=setup_seconds,
        search_runtime_seconds=time.perf_counter()-search_start,eigensolves=eigensolves,
        physical_photonic_attempts=0,score_queries=budget)


def retrospective(result,reference):
    opt=reference['optimum'];trace=result['trace']
    hits=[r['query'] for r in trace if abs(r['cost']-opt)<=1e-9]
    return dict(first_optimum_query=hits[0] if hits else None,
        found_optimum=bool(hits),optimal_query_count=len(hits),
        best_normalized_gap=(result['best_cost']-opt)/(reference['worst']-opt)
            if reference['worst']>opt+1e-12 else 0.,
        discovery_by_query={str(q):any(t<=q for t in hits) for q in (1,5,10,20,40,70,120) if q<=len(trace)})


def landscape_probes(seed):
    rank_results=[];invariance=[]
    for n in (4,6,8):
        ev=CollisionFreeEvaluator(n);mesh=RectangularMesh(n)
        for repeat in range(3):
            local_seed=seed+5000000+n*100+repeat
            theta=np.random.default_rng(local_seed).uniform(-1.2,1.2,mesh.num_parameters)
            for step in (1e-5,5e-6):
                columns=[]
                for index in range(mesh.num_parameters-n):
                    shift=np.zeros_like(theta);shift[index]=step
                    columns.append((ev.probabilities(mesh.unitary(theta+shift))-ev.probabilities(mesh.unitary(theta-shift)))/(2*step))
                jac=np.array(columns).T;s=np.linalg.svd(jac,compute_uv=False)
                rank=int(np.sum(s>max(s[0]*1e-7,1e-9)))
                record=dict(n=n,k=n//2,seed=local_seed,step=step,
                    active_parameters=mesh.num_parameters-n,cf_outcomes=len(ev.partitions),
                    singular_values=s.tolist(),rank_threshold=max(s[0]*1e-7,1e-9),numerical_rank=rank)
                if n==4:
                    fullsolver=FixedPhotonObliq(n);columns=[]
                    for index in range(mesh.num_parameters-n):
                        shift=np.zeros_like(theta);shift[index]=step
                        columns.append((abs(fullsolver.output_state(mesh.unitary(theta+shift)))**2-abs(fullsolver.output_state(mesh.unitary(theta-shift)))**2)/(2*step))
                    sv=np.linalg.svd(np.array(columns).T,compute_uv=False)
                    record['full_fock_singular_values']=sv.tolist()
                    record['full_fock_numerical_rank']=int(np.sum(sv>max(sv[0]*1e-7,1e-9)))
                rank_results.append(record)
            rng=np.random.default_rng(local_seed+11);u=mesh.unitary(theta)
            pin=np.diag(np.exp(1j*rng.uniform(-np.pi,np.pi,n)))
            pout=np.diag(np.exp(1j*rng.uniform(-np.pi,np.pi,n)))
            p=ev.probabilities(u)
            invariance.append(dict(n=n,seed=local_seed,
                input_phase_max_difference=float(np.max(abs(ev.probabilities(u@pin)-p))),
                output_phase_max_difference=float(np.max(abs(ev.probabilities(pout@u)-p)))))
    n=6;mesh=RectangularMesh(n);ev=CollisionFreeEvaluator(n)
    targets=((0,3,4),(1,2,5));edges=[(i,j,1.) for S in targets for i,j in combinations(S,2)]
    costs=ev.energies(edges);optimal=np.isclose(costs,costs.min(),atol=1e-9,rtol=0)
    rng=np.random.default_rng(seed+6000000)
    gate_angles=rng.uniform(.3,.8,len(mesh.pairs));phase_direction=rng.choice((-1.,1.),len(mesh.pairs))
    phase_results=[]
    for scale in (.01,.05,.1,.3,1.):
        rows=[]
        for phase in np.linspace(-np.pi,np.pi,41):
            parameters=np.zeros(mesh.num_parameters)
            parameters[:2*len(mesh.pairs):2]=scale*gate_angles
            parameters[1:2*len(mesh.pairs):2]=phase*phase_direction
            u=mesh.unitary(parameters)
            pb,pd=ev.probabilities(u),ev.probabilities(u,'distinguishable')
            rows.append(dict(phase=float(phase),bosonic_success=float(pb[optimal].sum()),
                distinguishable_success=float(pd[optimal].sum()),p_cf=float(pb.sum()),
                conditional_cut=float(pb@costs/pb.sum()) if pb.sum() else None))
        # Preregistered phase pair, not the most favorable pair selected from grid.
        a,b=rows[20],rows[30];delta=b['bosonic_success']-a['bosonic_success']
        variance=sum(r['bosonic_success']*(1-r['bosonic_success']) for r in (a,b))
        phase_results.append(dict(scale=scale,rows=rows,phase_pair=[a['phase'],b['phase']],
            absolute_phase_pair_contrast=abs(delta),shots_per_phase_unit_snr=variance/delta**2 if abs(delta)>0 else None,
            grid_min_success=min(r['bosonic_success'] for r in rows),grid_max_success=max(r['bosonic_success'] for r in rows),
            gate_angles=gate_angles.tolist(),phase_direction=phase_direction.tolist()))
    return dict(jacobian=rank_results,phase_gauge_invariance=invariance,
        rare_success_phase_probe=dict(n=6,edges=edges,targets=targets,records=phase_results,
            interpretation='Exploratory fixed phase grid; unit-SNR variance heuristic is not a power calculation; no optimizer and no physical shots'))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seed',type=int,default=20261120)
    parser.add_argument('--instances',type=int,default=4)
    parser.add_argument('--repeats',type=int,default=4)
    parser.add_argument('--budget',type=int,default=120)
    args=parser.parse_args()
    if any(x<1 for x in (args.instances,args.repeats,args.budget)):parser.error('positive counts required')
    args.output.mkdir(parents=True,exist_ok=True)
    if any(p.name not in ('stdout.txt','stderr.txt') for p in args.output.iterdir()):parser.error('Refusing to overwrite evidence')
    before={str(p):digest(ROOT/p) for p in SOURCE_PATHS}
    started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
    graphs=[];summaries=[];algorithms=('random_feasible','swap_anneal','spectral_swap_local')
    with (args.output/'runs.jsonl').open('w') as raw:
        for n in (4,6,8,10,12):
            for family in ('path','cycle','regular','erdos_renyi','weighted','planted'):
                for instance in range(args.instances):
                    gseed=args.seed+10000*n+instance;g=make_graph(n,family,gseed)
                    for label_id in (0,1):
                        label_seed=gseed+7000000
                        perm=np.arange(n) if label_id==0 else np.random.default_rng(label_seed).permutation(n)
                        edges=relabel_edges(g.edges,perm)
                        reference=exact_reference(n,edges)
                        gid=f'n{n}-{family}-i{instance}-L{label_id}'
                        graphs.append(dict(graph_id=gid,n=n,family=family,instance=instance,graph_seed=gseed,
                            label_id=label_id,label_seed=label_seed,label_permutation=perm.tolist(),edges=edges,
                            exact_reference=reference))
                        for repeat in range(args.repeats):
                            seed=args.seed+100000*n+1000*instance+repeat
                            for algorithm in algorithms:
                                fit=feasible_search(n,edges,algorithm,args.budget,seed)
                                metrics=retrospective(fit,reference)
                                record=dict(graph_id=gid,n=n,family=family,instance=instance,label_id=label_id,
                                    repeat=repeat,graph_seed=gseed,**fit,**metrics)
                                assert fit['n_queries']==args.budget and len(fit['trace'])==args.budget
                                assert fit['best_cost']>=reference['optimum']-1e-9
                                raw.write(json.dumps(clean(record),allow_nan=False)+'\n')
                                summaries.append({k:v for k,v in record.items() if k!='trace'})
                print(f'P21 n={n} family={family}: {len(summaries)} runs',flush=True)
    dump(args.output/'graphs.json',graphs)
    dump(args.output/'landscape_probes.json',landscape_probes(args.seed))
    groups=[]
    for n in (4,6,8,10,12):
        for algorithm in algorithms:
            for label_id in (0,1):
                subset=[r for r in summaries if r['n']==n and r['algorithm']==algorithm and r['label_id']==label_id]
                first=[r['first_optimum_query'] for r in subset if r['found_optimum']]
                groups.append(dict(n=n,algorithm=algorithm,label_id=label_id,runs=len(subset),
                    found_optimum_runs=len(first),censored_runs=len(subset)-len(first),
                    optimum_found_fraction=len(first)/len(subset),
                    median_first_optimum_query_given_found=float(np.median(first)) if first else None,
                    mean_best_normalized_gap=float(np.mean([r['best_normalized_gap'] for r in subset])),
                    mean_setup_seconds=float(np.mean([r['setup_runtime_seconds'] for r in subset])),
                    mean_search_seconds=float(np.mean([r['search_runtime_seconds'] for r in subset])),
                    discovery_fraction_by_query={str(q):float(np.mean([r['discovery_by_query'][str(q)] for r in subset])) for q in (1,5,10,20,40,70,120) if q<=args.budget}))
    dump(args.output/'summary.json',dict(experiment='P21 optimum-blind feasible classical query search',
        base_seed=args.seed,instances=args.instances,repeats=args.repeats,budget=args.budget,
        total_runs=len(summaries),total_scored_search_partitions=len(summaries)*args.budget,
        label_controls='original labels plus one fixed seeded permutation of every graph',
        uniform_graph_sampling=False,description='All families/instances/failed searches retained; graph duplicates intentionally not filtered',
        uncertainty='Descriptive finite-grid fractions only; repeated graph slots and seeds are dependent',
        exact_reference_evaluations=sum(g['exact_reference']['query_count'] for g in graphs),
        physical_photonic_attempts=0,results=groups))
    after={str(p):digest(ROOT/p) for p in SOURCE_PATHS}
    inputs_unchanged=before==after
    outputs=['runs.jsonl','graphs.json','landscape_probes.json','summary.json']
    manifest=dict(schema_version=2,claim_id='P21_classical_search',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip())),
        command=[sys.executable,*sys.argv],
        environment=dict(software=[dict(name='Python',version=platform.python_version()),dict(name='NumPy',version=np.__version__),dict(name='SciPy',version=scipy.__version__)],hardware=platform.platform()),
        mathematics=dict(assertion_tested='Finite optimum-blind balanced search, exact reference, phase-invariance and Jacobian rank probes on declared domain',
            coefficient_domain='float64/complex128',conventions='One score query evaluates one feasible balanced partition; no optimum or stopping oracle in training',
            inputs=['n=4,6,8,10,12; path/cycle/nonuniform random regular/Erdos-Renyi/weighted/planted; original and seeded labels'],
            bounds=dict(instances=args.instances,repeats=args.repeats,budget=args.budget,seed=args.seed),
            non_claims=['No quantum hardware or advantage','Cut queries are not optical objective evaluations','Finite-grid rates are not iid population inference','Jacobian ranks are numerical local observations']),
        randomness=dict(used=True,generator='NumPy default_rng PCG64',seed=args.seed),
        run=dict(started_at=started,runtime_seconds=time.perf_counter()-start,exit_status=0 if inputs_unchanged else 1,
            status='completed' if inputs_unchanged else 'inputs-changed',resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),
        outputs=[dict(path=str((args.output/name).relative_to(ROOT) if args.output.is_absolute() else args.output/name),sha256=digest(args.output/name),kind='result') for name in outputs],
        checks=[dict(check='input hashes unchanged',passed=inputs_unchanged),dict(check='all searches use declared query count and cannot beat exact reference',passed=True)],
        result='Finite assertion verified in declared domain' if inputs_unchanged else 'Inputs changed; provenance requires rerun',
        residual_risks=['Manual v2 recorder; no process-wide timeout or memory cap applied','Thread environment cap may be ignored by numerical libraries','Graph slots repeat isomorphic graphs and share seed streams'],
        input_artifacts=[dict(path=p,sha256=before[p],sha256_after=after[p]) for p in before],
        declared_results=[str((args.output/name).relative_to(ROOT) if args.output.is_absolute() else args.output/name) for name in outputs])
    dump(args.output/'manifest.json',manifest)
    if not inputs_unchanged:raise SystemExit('Inputs changed during run')
    print(f'P21 complete {len(summaries)} runs, {len(summaries)*args.budget} scored search partitions in {time.perf_counter()-start:.3f}s',flush=True)

if __name__=='__main__':main()
