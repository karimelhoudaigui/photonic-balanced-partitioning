#!/usr/bin/env python3
"""Bounded ideal research runs. No QPU, no automatic noise study.

Run from repository root with PYTHONPATH=src .venv/bin/python.
Output directories must be new, or a fresh directory owned by the Mathbox
provenance runner. Raw traces include every objective evaluation.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from itertools import combinations
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.optimize import minimize
from scipy.stats import t

from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh, partition_permutation
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator, cf_metrics
from photonic_balanced_partitioning.photonic.objectives import weighted_lower_cvar, wilson_interval, expected_shots_interval
from photonic_balanced_partitioning.photonic.penalty_obliq import PenaltyProductBernoulli
from photonic_balanced_partitioning.classical.baselines import spectral_partitioning
from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning as Graph


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, np.ndarray)):
        return [clean(v) for v in value]
    if isinstance(value, (float, np.floating)):
        return float(value) if np.isfinite(value) else None
    if isinstance(value, np.integer):
        return int(value)
    return value


def save(path, value):
    path.write_text(json.dumps(clean(value), indent=2, allow_nan=False) + "\n")


def mean_ci(values):
    x = np.asarray(values, dtype=float)
    mean = float(np.mean(x))
    half = float(t.ppf(.975, len(x)-1)*np.std(x, ddof=1)/np.sqrt(len(x))) if len(x)>1 else 0.
    return dict(n=len(x), mean=mean, ci95=[mean-half, mean+half],
                median=float(np.median(x)), minimum=float(x.min()), maximum=float(x.max()))


def graph(n, family, seed):
    if family == "path":
        return Graph.path_graph(n)
    if family == "cycle":
        return Graph.cycle_graph(n)
    if family == "regular":
        return Graph.random_regular(n, min(3, n-1), seed)
    if family == "erdos_renyi":
        return Graph.erdos_renyi(n, .5, seed)
    if family == "weighted":
        return Graph.erdos_renyi(n, .7, seed, (.25, 2.0))
    if family == "planted":
        return Graph.planted_partition(n, n//2, seed=seed)
    raise ValueError(family)


def haar(args):
    rows, summary = [], []
    for n, count in [(4, args.haar_samples), (6, args.haar_samples),
                     (8, args.haar_samples), (10, args.haar_n10)]:
        ev, solver = CollisionFreeEvaluator(n), FixedPhotonObliq(n)
        energies = ev.energies(Graph.path_graph(n).edges)
        optimum = float(energies.min())
        for index in range(count):
            seed = args.seed + n*100000 + index
            U = solver.random_interferometer(seed)
            metrics = cf_metrics(ev.probabilities(U), energies, optimum)
            # Independent full Fock normalization check at the first unitary.
            if index == 0:
                full = solver.output_state(U)
                assert abs(np.vdot(full, full).real - 1) < 1e-10
                assert np.max(abs(ev.probabilities(U)-solver.collision_free_probabilities(U))) < 1e-10
            rows.append(dict(n=n, index=index, seed=seed, **metrics))
        subset = rows[-count:]
        prediction = math.comb(n,n//2)/math.comb(n+n//2-1,n//2)
        record = dict(n=n, k=n//2, samples=count, haar_prediction=prediction,
                      mean_success_prediction=int(np.isclose(energies,optimum).sum())/solver.full_dimension,
                      conditional_success_prediction=float(np.isclose(energies,optimum).mean()),
                      conditional_energy_prediction=n/(2*(n-1))*(n-1),
                      **{key: mean_ci([r[key] for r in subset]) for key in
                         ["p_cf","p_success","p_opt_given_cf","conditional_energy"]})
        summary.append(record)
        print(f"E01 n={n} samples={count} mean P_CF={record['p_cf']['mean']:.8f} theory={prediction:.8f}", flush=True)
    with (args.output / "raw.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    save(args.output / "summary.json", {"experiment":"E01 Haar, ideal lossless", "seed":args.seed,
         "uncertainty":"Student t intervals across independent Haar circuits; marginal, not simultaneous",
         "physical_shots":0, "results":summary})
    return summary


def loss(probabilities, energies, optimum, name, mu=1., alpha=.25):
    metrics = cf_metrics(probabilities, energies, optimum)
    mass, expectation = metrics['p_cf'], metrics['conditional_energy']
    if name == "success": return -metrics['p_success']
    if name == "factorized": return -mass*(metrics['p_opt_given_cf'] or 0.)
    if name == "p_cf": return -mass
    if name == "conditional_success": return -(metrics['p_opt_given_cf'] or 0.) if mass>1e-14 else 1e6
    if name == "bad": return metrics['unconditional_cf_energy']
    if expectation is None: return 1e6
    if name == "conditional": return expectation
    if name == "collision": return expectation+mu*(1-mass)
    if name == "barrier": return expectation-mu*np.log(mass+1e-12)
    if name == "cvar": return weighted_lower_cvar(energies, probabilities, alpha)
    raise ValueError(name)


def optimize(ev, energies, mesh, initial, model, objective, budget, seed,
             method="COBYLA", shots=0, mu=1., anchor=None):
    rng = np.random.default_rng(seed)
    traces, candidates, unitary_candidates = [], [], []
    # Fock input phases are unobservable. Freeze these n null directions and
    # optimize only two-mode parameters; saved circuits retain all parameters.
    initial_active = initial[:-mesh.n].copy()
    best_value, best_parameters = math.inf, np.r_[initial_active, np.zeros(mesh.n)]
    class StopBudget(Exception): pass
    def fun(params):
        nonlocal best_value,best_parameters
        if len(traces) >= budget: raise StopBudget()
        full_params = np.r_[params, np.zeros(mesh.n)]
        U=(FixedPhotonObliq(ev.n).random_interferometer(seed+13*len(traces))
           if method=="haar" else mesh.unitary(full_params, anchor))
        p = ev.probabilities(U, model)
        exact = cf_metrics(p, energies, float(energies.min()))
        counts = None
        if shots:
            physical_p = np.append(p, max(0.,1-float(p.sum())))
            physical_p /= physical_p.sum()  # checked CF mass; roundoff only
            counts = rng.multinomial(shots, physical_p)
            p = counts[:-1]/shots
        value = loss(p, energies, float(energies.min()), objective, mu)
        traces.append(dict(evaluation=len(traces)+1, loss=float(value), exact=exact,
                           counts=counts.tolist() if counts is not None else None,
                           parameters=full_params.tolist()))
        candidates.append(full_params.copy())
        unitary_candidates.append(U.copy())
        if value < best_value:
            best_value,best_parameters = value,full_params.copy()
        return value
    start=time.perf_counter()
    if method in ["random","haar"]:
        fun(initial_active)
        for _ in range(budget-1): fun(rng.uniform(-np.pi,np.pi,len(initial_active)))
    elif method == "SPSA":
        theta=initial_active.copy(); fun(theta)
        iteration=0
        while len(traces)+2 <= budget:
            delta=rng.choice([-1.,1.],size=len(theta))
            c=.15/(iteration+1)**.101
            a=.2/(iteration+5)**.602
            plus,minus=fun(theta+c*delta),fun(theta-c*delta)
            theta-=a*(plus-minus)/(2*c)*delta
            iteration+=1
        if len(traces)<budget: fun(theta)
    else:
        options={"maxiter":budget,"rhobeg":.35,"tol":1e-7} if method=="COBYLA" else {"maxfev":budget,"maxiter":budget}
        try: minimize(fun,initial_active,method=method,options=options)
        except StopBudget: pass
    elapsed=time.perf_counter()-start
    best_index=int(np.argmin([r['loss'] for r in traces]))
    return dict(parameters=best_parameters.tolist(), trace=traces, n_evaluations=len(traces),
                best_unitary_real=unitary_candidates[best_index].real.tolist(),
                best_unitary_imag=unitary_candidates[best_index].imag.tolist(),
                training_shots=shots*len(traces), runtime_seconds=elapsed,
                selected_evaluation=best_index+1, best_loss=best_value,
                before=traces[0]['exact'], after=traces[best_index]['exact'])


def optimization(args):
    rows=[]; out=args.output
    with (out/"runs.jsonl").open("w") as raw:
        for n in args.sizes:
            ev=CollisionFreeEvaluator(n)
            for family in args.families:
                for instance in range(args.instances):
                    gseed=args.seed+10000*n+instance
                    g=graph(n,family,gseed); energies=ev.energies(g.edges)
                    optimum=float(energies.min())
                    uniform_success=float(np.isclose(energies,optimum,atol=1e-9,rtol=0).mean())
                    anchor_result=spectral_partitioning(n,list(g.edges))
                    anchor=partition_permutation(n,anchor_result.partition)
                    for repeat in range(args.repeats):
                        seed=args.seed+100000*n+1000*instance+repeat
                        for depth in args.depths:
                            mesh=RectangularMesh(n,n if depth==0 else depth)
                            initial=np.random.default_rng(seed+mesh.num_parameters).uniform(-np.pi,np.pi,mesh.num_parameters)
                            if args.anchor:
                                initial=np.zeros(mesh.num_parameters)
                            for model in args.models:
                                for objective in args.objectives:
                                    for method in args.methods:
                                        fitted=optimize(ev,energies,mesh,initial,model,objective,args.budget,seed+77,
                                                        method=method,mu=args.mu,anchor=anchor if args.anchor else None)
                                        finalU=np.asarray(fitted['best_unitary_real'])+1j*np.asarray(fitted['best_unitary_imag'])
                                        controls={m:cf_metrics(ev.probabilities(finalU,m),energies,optimum)
                                                  for m in ["bosonic","distinguishable","multinomial"]}
                                        record=dict(n=n,family=family,instance=instance,graph_seed=gseed,seed=seed,
                                                    initialization="spectral_anchor" if args.anchor else "random",
                                                    anchor_classical_objective_evaluations=1,
                                                    depth=mesh.depth or n,model=model,objective=objective,method=method,
                                                    optimum=optimum, edges=g.edges,uniform_balanced_success=uniform_success,
                                                    anchor_classical_energy=anchor_result.energy,
                                                    anchor_metrics=cf_metrics(ev.probabilities(anchor),energies,optimum),
                                                    oracle_permutation_success=1.0,
                                                    same_final_circuit_controls=controls, **fitted)
                                        raw.write(json.dumps(clean(record),allow_nan=False)+"\n"); raw.flush()
                                        rows.append({k:v for k,v in record.items() if k not in ['trace','parameters','edges','best_unitary_real','best_unitary_imag']})
                    print(f"ideal n={n} family={family} instance={instance} runs={len(rows)}",flush=True)
    groups=[]
    keys=["n","model","objective","method","depth"]
    for group in sorted(set(tuple(r[k] for k in keys) for r in rows)):
        subset=[r for r in rows if tuple(r[k] for k in keys)==group]
        groups.append(dict(zip(keys,group), runs=len(subset),
                      after=mean_ci([r['after']['p_success'] for r in subset]),
                      improvement=mean_ci([r['after']['p_success']-r['before']['p_success'] for r in subset]),
                      uniform_comparison=mean_ci([r['after']['p_success']-r['uniform_balanced_success'] for r in subset])))
    save(out/"summary.json",dict(experiment="ideal optimizer diagnostics; oracle C* is available for success loss",
         comparisons_are_not_hardware_budget_claims=True,physical_shots=0,
         total_evaluations=sum(r['n_evaluations'] for r in rows),results=groups))
    return groups


def shot_benchmark(args):
    rows=[]
    with (args.output/"runs.jsonl").open("w") as raw:
        for n in args.sizes:
            ev=CollisionFreeEvaluator(n); mesh=RectangularMesh(n)
            for family in args.families:
                for instance in range(args.instances):
                    gseed=args.seed+10000*n+instance
                    g=graph(n,family,gseed); energies=ev.energies(g.edges); optimum=float(energies.min())
                    for repeat in range(args.repeats):
                        seed=args.seed+100000*n+1000*instance+repeat
                        initial=np.random.default_rng(seed+mesh.num_parameters).uniform(-np.pi,np.pi,mesh.num_parameters)
                        candidates=[]
                        for model in ["bosonic","distinguishable","multinomial"]:
                            fitted=optimize(ev,energies,mesh,initial,model,"collision",args.budget,seed+77,shots=args.shots,mu=args.mu)
                            candidates.append(dict(name=model,metrics=fitted['after'],fitted=fitted))
                        for lam in args.lambdas:
                            penal=PenaltyProductBernoulli(n,lam=lam)
                            fitted=penal.optimize(list(g.edges),args.budget,seed+77,shots_per_evaluation=args.shots)
                            metrics=penal.metrics(fitted['best_params'],list(g.edges),optimum)
                            metrics['p_cf']=metrics['p_feasible']
                            candidates.append(dict(name=f"classical_penalty_lambda_{lam:g}",metrics=metrics,fitted=fitted))
                        uniform=float(np.isclose(energies,optimum,atol=1e-9,rtol=0).mean())
                        candidates.append(dict(name="random_balanced",metrics=dict(p_cf=1.,p_success=uniform,
                            conditional_energy=float(energies.mean()),expected_shots=1/uniform),
                            fitted=dict(n_evaluations=args.budget,training_shots=args.budget*args.shots,
                                        runtime_seconds=None,description="same number of batches; independent uniform balanced draws")))
                        for candidate_index,candidate in enumerate(candidates):
                            # Fresh independent RNG for each fixed-circuit heldout experiment.
                            rng=np.random.default_rng(seed+9000000+candidate_index)
                            shots=args.heldout; ps=candidate['metrics']['p_success']
                            successes=int(rng.binomial(shots,min(1.,max(0.,ps))))
                            fit=candidate['fitted']
                            record=dict(n=n,family=family,instance=instance,graph_seed=gseed,seed=seed,
                                edges=g.edges,optimum=optimum,model=candidate['name'],metrics=candidate['metrics'],
                                training=fit,heldout_shots=shots,heldout_successes=successes,
                                heldout_success_ci95=wilson_interval(successes,shots),
                                expected_shots_ci95=expected_shots_interval(successes,shots),
                                total_shots=fit['training_shots']+shots if 'training_shots' in fit else fit['n_shots']+shots)
                            raw.write(json.dumps(clean(record),allow_nan=False)+"\n");raw.flush()
                            rows.append({k:v for k,v in record.items() if k not in ["training","edges"]})
                    print(f"shots n={n} {family} instance={instance} records={len(rows)}",flush=True)
    groups=[]
    for n in args.sizes:
        for model in sorted(set(r['model'] for r in rows)):
            sub=[r for r in rows if r['n']==n and r['model']==model]
            groups.append(dict(n=n,model=model,runs=len(sub),
                p_success=mean_ci([r['metrics']['p_success'] for r in sub]),
                mean_total_shots=float(np.mean([r['total_shots'] for r in sub])),
                minimum_total_shots=min(r['total_shots'] for r in sub),maximum_total_shots=max(r['total_shots'] for r in sub)))
    save(args.output/"summary.json",dict(experiment="finite-shot ideal training + independent heldout sampling",
        budget=args.budget,shots_per_evaluation=args.shots,heldout_shots=args.heldout,
        training_loss="conditional energy + mu*(1-P_CF); no optimum oracle in training",mu=args.mu,
        uncertainty="Wilson fixed-circuit intervals; marginal t summaries mix family/instance/repeat, descriptive only",
        note="Matched MAXIMUM budgets. Actual calls/shots retained if any optimizer stops early. No ObliQ hardware baseline.",results=groups))
    return groups


def structure(args):
    rows=[]
    for n in [4,6,8,10]:
        solver=FixedPhotonObliq(n); states=np.asarray(solver._enumerate_all_fock_states())
        M=(states*(states-1)/2).sum(axis=1)
        for index in range(30):
            seed=args.seed+n*10000+index; U=solver.random_interferometer(seed)
            p=abs(solver.output_state(U))**2
            B=abs(U[:,:n//2])**2
            Q=sum(float(np.sum(B[:,a]*B[:,b])) for a,b in combinations(range(n//2),2))
            collision=float(p[M>0].sum()); mean_pairs=float(p @ M)
            assert abs(mean_pairs-2*Q)<1e-10
            assert 2*Q/math.comb(n//2,2) <= collision+1e-10 <= 2*Q+1e-10
            rows.append(dict(n=n,seed=seed,Q=Q,collision=collision,mean_collision_pairs=mean_pairs))
    # Disjoint two-mode supports: random nontrivial partitions, zero collisions.
    for n in [4,6,8,10]:
        meshU=np.eye(n,dtype=complex)
        for a in range(n//2):
            pair=[a,a+n//2]; theta=.17*(a+1)
            meshU[np.ix_(pair,pair)]=RectangularMesh.gate(theta,.3*a)
        ev=CollisionFreeEvaluator(n)
        bosonic,dist=ev.probabilities(meshU),ev.probabilities(meshU,"distinguishable")
        assert abs(bosonic.sum()-1)<1e-12
        assert max(abs(bosonic-dist))<1e-12
        rows.append(dict(n=n,case="disjoint_support",p_cf=float(bosonic.sum()),max_bosonic_dist_difference=float(max(abs(bosonic-dist)))))
    save(args.output/"summary.json",dict(experiment="pair-moment identity, collision bounds, disjoint-support falsification",
        haar_cases=120,disjoint_cases=4,physical_shots=0,results=rows))
    print("Structural checks: 120 Haar cases + 4 disjoint-support controls PASS",flush=True)
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment",choices=["haar","optimization","shots","structure"])
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--seed",type=int,default=20261120)
    parser.add_argument("--sizes",type=int,nargs="+",default=[4,6,8])
    parser.add_argument("--families",nargs="+",default=["path","cycle","regular","erdos_renyi","weighted","planted"])
    parser.add_argument("--instances",type=int,default=2)
    parser.add_argument("--repeats",type=int,default=3)
    parser.add_argument("--models",nargs="+",default=["bosonic","distinguishable","multinomial"])
    parser.add_argument("--objectives",nargs="+",default=["success"])
    parser.add_argument("--methods",nargs="+",default=["COBYLA"])
    parser.add_argument("--depths",type=int,nargs="+",default=[0])
    parser.add_argument("--anchor",action="store_true",help="Classical spectral permutation + identity-initialized mesh")
    parser.add_argument("--budget",type=int,default=120)
    parser.add_argument("--shots",type=int,default=256)
    parser.add_argument("--heldout",type=int,default=4096)
    parser.add_argument("--mu",type=float,default=2.)
    parser.add_argument("--lambdas",type=float,nargs="+",default=[.1,1.,10.])
    parser.add_argument("--haar-samples",type=int,default=1000)
    parser.add_argument("--haar-n10",type=int,default=250)
    args=parser.parse_args()
    for value in [args.instances,args.repeats,args.budget,args.shots,args.heldout,args.haar_samples,args.haar_n10]:
        if value<1: parser.error("counts must be positive")
    args.output.mkdir(parents=True,exist_ok=True)
    if any(p.name not in ["stdout.txt","stderr.txt"] for p in args.output.iterdir()):
        parser.error("Output directory must be new (raw data are never overwritten)")
    start=time.perf_counter()
    {"haar":haar,"optimization":optimization,"shots":shot_benchmark,"structure":structure}[args.experiment](args)
    print(f"Completed {args.experiment} in {time.perf_counter()-start:.3f}s",flush=True)


if __name__ == "__main__": main()
