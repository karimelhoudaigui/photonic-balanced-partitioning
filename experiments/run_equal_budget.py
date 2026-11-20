#!/usr/bin/env python3
"""Exactly equal ideal-attempt budgets, including discovery during training.

Unlike E05's analytic uniform control, every baseline here actually samples
all training batches. No true optimum is available to the training loss.
The optimum is used solely for retrospective scoring and first-hit metrics.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.optimize import minimize
from run_research import graph, clean, save, mean_ci
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator, cf_metrics
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh
from photonic_balanced_partitioning.photonic.penalty_obliq import PenaltyProductBernoulli
from photonic_balanced_partitioning.photonic.objectives import wilson_interval, expected_shots_interval


def train(model,n,edges,seed,budget,shots,mu,lam=None):
    setup_start=time.perf_counter()
    rng=np.random.default_rng(seed+77)
    ev=CollisionFreeEvaluator(n); costs_cf=ev.energies(edges)
    optimum=float(costs_cf.min())  # scoring only; never referenced by objective
    mesh=RectangularMesh(n)
    penalty=PenaltyProductBernoulli(n,lam=lam) if lam is not None else None
    if penalty is not None:
        costs=penalty.cut_energies(edges); feasible=penalty.feasible
        total=penalty.energies(edges)
        initial=np.random.default_rng(seed+n).normal(0,.25,n)
    else:
        costs=np.r_[costs_cf,np.nan]
        feasible=np.r_[np.ones(len(costs_cf),dtype=bool),False]
        initial=np.random.default_rng(seed+mesh.num_parameters).uniform(-np.pi,np.pi,mesh.num_parameters-n)
    if model=='random_balanced':
        costs=costs_cf; feasible=np.ones(len(costs),dtype=bool)
        initial=np.empty(0)
    def distribution(params):
        if penalty is not None: return penalty.probabilities(params)
        if model=='random_balanced': return np.full(len(costs_cf),1/len(costs_cf))
        p=ev.probabilities(mesh.unitary(np.r_[params,np.zeros(n)]),model)
        q=np.r_[p,max(0.,1-float(p.sum()))]
        return q/q.sum()
    trace=[]; best_loss=math.inf; best_parameters=initial.copy()
    first_hit=None; best_seen=math.inf; feasible_seen=successes_seen=0
    class StopBudget(Exception): pass
    def fun(params):
        nonlocal best_loss,best_parameters,first_hit,best_seen,feasible_seen,successes_seen
        if len(trace)>=budget: raise StopBudget
        probs=distribution(params)
        draws=rng.choice(len(probs),size=shots,p=probs)
        counts=np.bincount(draws,minlength=len(probs))
        valid=feasible[draws]
        sampled_costs=costs[draws]
        if penalty is not None:
            value=float(counts @ total / shots)
        else:
            # Training uses observed costs only, without C* or optimal mask.
            value=(float(np.mean(sampled_costs[valid]))+mu*(1-float(valid.mean()))
                   if valid.any() else float(sum(abs(w) for _,_,w in edges)+mu+1))
        # Retrospective diagnostics happen AFTER the training value is fixed.
        hits=np.flatnonzero(valid & np.isclose(sampled_costs,optimum,atol=1e-9,rtol=0))
        if first_hit is None and len(hits): first_hit=len(trace)*shots+int(hits[0])+1
        if valid.any(): best_seen=min(best_seen,float(sampled_costs[valid].min()))
        feasible_seen+=int(valid.sum());successes_seen+=len(hits)
        trace.append(dict(evaluation=len(trace)+1,loss=value,parameters=np.asarray(params).tolist(),
                          counts=counts.tolist(),feasible_count=int(valid.sum()),optimal_count=len(hits),
                          best_valid_cost_so_far=best_seen,first_optimum_attempt_so_far=first_hit))
        if value<best_loss: best_loss=value;best_parameters=np.asarray(params).copy()
        return value
    setup_elapsed=time.perf_counter()-setup_start
    start=time.perf_counter();fallback=0
    if model=='random_balanced':
        for _ in range(budget): fun(initial)
    else:
        try: minimize(fun,initial,method='COBYLA',options=dict(maxiter=budget,rhobeg=.35,tol=1e-7))
        except StopBudget: pass
        # Predetermined completion rule, identical for all fitted models:
        # spend remaining calls on local proposals around the selected point.
        while len(trace)<budget:
            fallback+=1
            fun(best_parameters+rng.normal(0,.1,size=len(best_parameters)))
    elapsed=time.perf_counter()-start
    p=distribution(best_parameters)
    ps=float(p[feasible & np.isclose(costs,optimum,atol=1e-9,rtol=0)].sum())
    pf=float(p[feasible].sum())
    # Independent heldout draw stream; training shots already count in cost.
    heldout_rng=np.random.default_rng(seed+9000000)
    heldout_draws=heldout_rng.choice(len(p),size=4096,p=p)
    heldout_counts=np.bincount(heldout_draws,minlength=len(p))
    heldout_valid=feasible[heldout_draws]
    heldout_hits=np.flatnonzero(heldout_valid & np.isclose(costs[heldout_draws],optimum,atol=1e-9,rtol=0))
    if first_hit is None and len(heldout_hits): first_hit=budget*shots+int(heldout_hits[0])+1
    if heldout_valid.any(): best_seen=min(best_seen,float(costs[heldout_draws][heldout_valid].min()))
    return dict(model=model,lambda_value=lam,optimum=optimum,parameters=best_parameters.tolist(),trace=trace,
        fallback_evaluations=fallback,n_evaluations=len(trace),training_shots=budget*shots,heldout_shots=4096,
        total_shots=budget*shots+4096,training_runtime_seconds=elapsed,
        sample_score_lookups=budget*shots+4096,
        reference_cost_table_size=len(costs),reference_optimum_for_scoring_only=True,
        setup_runtime_seconds=setup_elapsed,
        final_p_feasible=pf,final_p_success=ps,final_expected_shots=1/ps if ps>0 else None,
        final_conditional_energy=float(p[feasible] @ costs[feasible]/pf) if pf>0 else None,
        first_optimum_attempt=first_hit,best_valid_cost=best_seen,training_feasible_count=feasible_seen,
        training_optimal_count=successes_seen,heldout_counts=heldout_counts.tolist(),
        heldout_optimal_count=len(heldout_hits),success_ci95=wilson_interval(len(heldout_hits),4096),
        expected_shots_ci95=expected_shots_interval(len(heldout_hits),4096))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seed',type=int,default=20261120)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    if any(p.name not in ['stdout.txt','stderr.txt'] for p in args.output.iterdir()):
        parser.error('Refusing to overwrite data')
    rows=[]
    with (args.output/'runs.jsonl').open('w') as stream:
        for n in [4,6,8]:
            for family in ['path','cycle','regular','erdos_renyi','weighted','planted']:
                for instance in range(2):
                    graph_seed=args.seed+10000*n+instance
                    g=graph(n,family,graph_seed)
                    for repeat in range(3):
                        seed=args.seed+100000*n+1000*instance+repeat
                        for model,lam in [('bosonic',None),('distinguishable',None),('multinomial',None),
                                          ('classical_penalty',.1),('classical_penalty',1.),('classical_penalty',10.),
                                          ('random_balanced',None)]:
                            result=train(model,n,g.edges,seed,120,256,2.,lam)
                            record=dict(n=n,family=family,instance=instance,graph_seed=graph_seed,seed=seed,
                                        edges=g.edges,**result)
                            stream.write(json.dumps(clean(record),allow_nan=False)+'\n');stream.flush()
                            rows.append({k:v for k,v in record.items() if k not in ['trace','edges','heldout_counts','parameters']})
                print(f'exact-budget n={n} {family}: {len(rows)} model runs',flush=True)
    groups=[]
    for n in [4,6,8]:
        for model,lam in [('bosonic',None),('distinguishable',None),('multinomial',None),
                          ('classical_penalty',.1),('classical_penalty',1.),('classical_penalty',10.),('random_balanced',None)]:
            subset=[r for r in rows if r['n']==n and r['model']==model and r['lambda_value']==lam]
            first=[r['first_optimum_attempt'] for r in subset if r['first_optimum_attempt'] is not None]
            groups.append(dict(n=n,model=model,lambda_value=lam,runs=len(subset),
                final_p_success=mean_ci([r['final_p_success'] for r in subset]),
                found_optimum_runs=len(first),censored_runs=len(subset)-len(first),
                median_first_attempt_given_found=float(np.median(first)) if first else None,
                mean_runtime_seconds=float(np.mean([r['training_runtime_seconds'] for r in subset]))))
    save(args.output/'summary.json',dict(experiment='E05b exact ideal attempt budgets',seed=args.seed,
         n_evaluations=120,training_shots=30720,heldout_shots=4096,total_shots_per_run=34816,
         total_model_runs=len(rows),total_simulated_attempts=34816*len(rows),physical_qpu_attempts=0,
         common_fallback='if COBYLA stops early, Gaussian proposals scale .1 around selected point until budget exhausted',
         training='photonic: sampled E_CF+2*(1-P_CF); penalty: sampled QUBO energy; optimum never enters loss',
         uncertainty='Wilson heldout fixed-circuit intervals; pooled t summaries descriptive only, not population significance',
         limitations=['Ideal simulated attempts omit emission/detection losses',
                      'Full probabilities enumerated exponentially to simulate shots; simulator wall time is not hardware time',
                      'Every lambda separate; selecting a winning lambda costs all its training',
                      'No genuine optical ObliQ baseline; no matched number of trainable parameters',
                      'Cut scoring and raw counts saved; successful batch count is not wall-clock time to solution'],results=groups))


if __name__=='__main__': main()
