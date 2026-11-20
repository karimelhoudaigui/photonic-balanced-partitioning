"""Reproducible objective regressions and classical full-cube penalty audit.

Run from repository root:
    PYTHONPATH=src python3 experiments/validation/objective_penalty_audit.py
No QPU, network, or quantum baseline is used. The Gibbs sweep is exact
exponential enumeration. Training is noisy and retains all physical attempts.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
import numpy as np
import scipy
from photonic_balanced_partitioning.photonic.penalty_obliq import PenaltyProductBernoulli
from photonic_balanced_partitioning.photonic.objectives import (
    distribution_metrics,objective_value,weighted_lower_cvar,
    wilson_interval,expected_shots_interval,
)

ROOT=Path(__file__).resolve().parents[2]
INPUTS=[Path(__file__).relative_to(ROOT),*map(Path,[
    'src/photonic_balanced_partitioning/photonic/objectives.py',
    'src/photonic_balanced_partitioning/photonic/penalty_obliq.py',
])]

def hashes():
    return {str(p):hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS}

def run():
    start=time.perf_counter()
    before=hashes()
    rows=[]
    qubo_max_residual=0.
    for n in (4,6,8):
        edges=[(i,i+1,1.) for i in range(n-1)]
        for lam in (0.,.1,.5,1.,2.,4.,10.):
            s=PenaltyProductBernoulli(n,lam=lam)
            p=s.gibbs_probabilities(edges,beta=1.)
            cut=s.cut_energies(edges);e=s.energies(edges);feasible=s.feasible
            q=s.qubo_coefficients(edges)
            predicted=q['offset'] + s.bitstrings@q['linear'] + np.einsum('bi,ij,bj->b',s.bitstrings,q['quadratic'],s.bitstrings)
            residual=float(np.max(np.abs(predicted-e)))
            qubo_max_residual=max(qubo_max_residual,residual)
            assert residual < 1e-10
            optimal=feasible & np.isclose(cut,cut[feasible].min(),atol=1e-10,rtol=0)
            rows.append({'n':n,'lambda':lam,'beta':1.,'gibbs_p_feasible':float(p[feasible].sum()),
                'gibbs_p_success':float(p[optimal].sum()),'all_penalized_minimizers_feasible':bool(np.all(feasible[np.isclose(e,e.min())])),
                'qubo_density':q['coupling_density'],'coefficient_abs_range':q['coefficient_abs_range'],
                'min_coefficient':q['coefficient_min'],'max_coefficient':q['coefficient_max'],
                'obliq_circuit_depth':None,'qubo_max_residual':residual})
    training=[]
    for n in (4,6,8):
        edges=[(i,i+1,1.) for i in range(n-1)]
        for lam in (.1,1.,10.):
            for seed in (101,102,103):
                s=PenaltyProductBernoulli(n,lam=lam)
                r=s.optimize(edges,num_iterations=80,seed=seed,method='COBYLA',shots_per_evaluation=256)
                draws=s.sample(r['best_params'],4096,edges,seed=seed+10000)
                valid=[x.energy for x in draws if x.is_valid]
                successes=sum(x.is_valid and abs(x.energy-1.)<1e-10 for x in draws)
                shot_bounds=expected_shots_interval(successes,len(draws))
                training.append({'n':n,'lambda':lam,'seed':seed,'max_evaluations':80,
                    'evals':r['n_evaluations'],'training_shots':r['n_shots'],
                    'evaluation_shots':len(draws),'evaluation_seed':seed+10000,
                    'observed_feasible':len(valid),'observed_successes':successes,
                    'success_wilson_95':wilson_interval(successes,len(draws)),
                    'expected_shots_wilson_95':[None if math.isinf(x) else x for x in shot_bounds],
                    'best_valid_energy':min(valid) if valid else None,
                    'exact_p_feasible':r['metrics']['p_feasible'],'exact_p_success':r['metrics']['p_success'],
                    'parameter_trace':[x.tolist() for x in r['parameter_trace']],
                    'objective_trace':r['energies'],'best_params':r['best_params'].tolist()})
    states=[(1,1,0,0),(1,0,1,0),(2,0,0,0)]
    edges=[(0,1,1.),(1,2,1.),(2,3,1.)]
    pathology=[]
    for p in ([.5,.5,0.],[.05,.05,.9],[.01,0.,.99],[.9,0.,.1]):
        m=distribution_metrics(p,states,edges,1.)
        cfweights=np.asarray(p)[:2]
        pathology.append({'probabilities':p,**m.__dict__,
            'collision_aware_mu1':objective_value(m,'collision_aware',mu=1.),
            'log_barrier_gamma1':objective_value(m,'log_barrier',gamma=1.),
            'conditional_cvar_alpha_half':weighted_lower_cvar([1.,3.],cfweights,.5)})
    after=hashes()
    assert before == after,'Input changed while running; rerun required'
    data={'schema':'objective_penalty_audit/v1','status':'completed',
        'assertion_tested':'Full-cube QUBO identity on paths n=4,6,8, lambda sweep; 27 seeded noisy classical training runs; conditional objective pathologies',
        'non_claims':['No authentic optical ObliQ dynamics','No efficient Gibbs preparation','No quantum or hardware performance conclusion','No equal-cost comparison from early-converged training runs'],
        'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'dirty_state':subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True).splitlines(),
        'argv':sys.argv,'reproduction_command':'PYTHONPATH=src python3 experiments/validation/objective_penalty_audit.py',
        'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform(),
        'input_hashes_before':before,'input_hashes_after':after,
        'qubo_max_residual':qubo_max_residual,'gibbs_diagnostic':rows,'training':training,
        'objective_pathologies':pathology,'runtime_seconds':time.perf_counter()-start}
    out=ROOT/'experiments/validation/objective_penalty_audit.json'
    out.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'completed','output':str(out.relative_to(ROOT)),
        'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'training_runs':len(training),
        'qubo_max_residual':qubo_max_residual,'runtime_seconds':data['runtime_seconds']},indent=2))

if __name__ == '__main__':
    run()
