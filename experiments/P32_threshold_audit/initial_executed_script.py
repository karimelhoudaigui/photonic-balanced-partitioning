#!/usr/bin/env python3
"""Bounded independent audit of the principal checkout's P2-A threshold drafts.

From this isolated worktree:
  PYTHONPATH=src ../../../.venv/bin/python -B experiments/phase3_threshold_audit.py --output /private/tmp/pasqal-phase3-threshold-audit.json
The saved JSON is evidence; selected values and its complete text are retained
in reports/PHASE3_THRESHOLD_AUDIT.md. No principal-checkout file is modified.
"""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import importlib.metadata
import importlib.util
import itertools
import json
import math
from pathlib import Path
import platform
import subprocess
import sys
import time
import traceback
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_DRAFT_ROOT=ROOT.parents[2] if ROOT.parent.name=='worktrees' else ROOT


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def clean(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,np.ndarray)):return [clean(v) for v in value]
    if isinstance(value,(float,np.floating)):return float(value) if math.isfinite(value) else None
    if isinstance(value,np.integer):return int(value)
    return value


@lru_cache(None)
def haar(m,N,k):
    if N==0:return F(int(k==0))
    if not 1<=k<=min(m,N):return F(0)
    return F(math.comb(m,k)*math.comb(N-1,k-1),math.comb(m+N-1,N))


@lru_cache(None)
def loss_mix(m,N,k,eta):
    return sum((F(math.comb(N,L))*eta**L*(1-eta)**(N-L)*haar(m,L,k) for L in range(N+1)),F(0))


def compositions(N,m):
    if m==1:
        yield (N,)
    else:
        for first in range(N+1):
            for tail in compositions(N-first,m-1):yield (first,)+tail


def exact_click_thinning(m,N,eta):
    """Uniform Fock occupations, explicit independent-mode click polynomials.

    Does not call either mixture or coefficient identity.
    """
    accum=[F(0)]*(m+1)
    count=0
    for state in compositions(N,m):
        poly=[F(1)]
        for t in state:
            no=(1-eta)**t
            result=[F(0)]*(len(poly)+1)
            for j,p in enumerate(poly):
                result[j]+=p*no;result[j+1]+=p*(1-no)
            poly=result
        assert sum(poly)==1
        accum=[x+y for x,y in zip(accum,poly)];count+=1
    assert count==math.comb(m+N-1,N)
    return [p/count for p in accum]


def exact_coefficient(m,N,k,eta):
    if k==0:return (1-eta)**N
    if k>N or k>m:return F(0)
    coefficient=sum((F(math.comb(k+j-1,j)*math.comb(m+N-k-j-1,N-k-j))*(1-eta)**(N-k-j) for j in range(N-k+1)),F(0))
    return F(math.comb(m,k),math.comb(m+N-1,N))*eta**k*coefficient


def maximizers(values):
    best=max(values.values())
    return [N for N,v in values.items() if v==best],best


def finite_budget(probabilities,B):
    stationary={N:1-(1-p)**(B//N) for N,p in probabilities.items() if N<=B}
    stationary_N,stationary_best=maximizers(stationary)
    fail=[F(1)]*(B+1);choice=[None]*(B+1)
    for b in range(1,B+1):
        feasible={N:(1-p)*fail[b-N] for N,p in probabilities.items() if N<=b}
        if feasible:
            best=min(feasible.values());fail[b]=best
            choice[b]=next(N for N,v in feasible.items() if v==best)
    remaining=B;plan=[]
    while choice[remaining] is not None:
        N=choice[remaining];plan.append(N);remaining-=N
    assert sum(plan)<=B
    assert math.prod((1-probabilities[N] for N in plan),start=F(1))==fail[B]
    assert 1-fail[B]>=stationary_best
    return dict(B=B,stationary_optimal_N=stationary_N,stationary_success=stationary_best,
        variable_N_success=1-fail[B],variable_N_plan=plan,unused_photons=remaining)


def independent_fock_probabilities(U,N,model):
    """Brute permutation formula, independent of the draft's Ryser path."""
    states=list(compositions(N,len(U)));probs=[]
    permutations=list(itertools.permutations(range(N)))
    for state in states:
        rows=np.repeat(np.arange(len(U)),state)
        sub=U[np.ix_(rows,np.arange(N))]
        if model=='bosonic':
            amplitude=sum((math.prod(sub[j,p[j]] for j in range(N)) for p in permutations),0j)
            probability=abs(amplitude)**2
        else:
            probability=sum((math.prod(abs(sub[j,p[j]])**2 for j in range(N)) for p in permutations),0.)
        probability/=math.prod(math.factorial(t) for t in state)
        probs.append(float(probability))
    assert abs(sum(probs)-1)<1e-10
    return states,np.array(probs)


def independent_detected_distribution(U,N,eta,model):
    states,p=independent_fock_probabilities(U,N,model)
    detected=np.zeros(2**len(U))
    for state,probability in zip(states,p):
        for outcome in itertools.product(*(range(t+1) for t in state)):
            weight=F(1)
            for t,s in zip(state,outcome):
                weight*=math.comb(t,s)*eta**s*(1-eta)**(t-s)
            binary=0
            for s in outcome:binary=(binary<<1)+int(s>0)
            detected[binary]+=probability*float(weight)
    assert abs(detected.sum()-1)<1e-10
    return detected


def audit(draft,result):
    exact_rows=[];checks=0;max_formula_error=0.
    for m in range(1,7):
        for N in range(m+3):
            for eta in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
                actual=exact_click_thinning(m,N,eta)
                expected=[loss_mix(m,N,k,eta) for k in range(m+1)]
                coefficient=[exact_coefficient(m,N,k,eta) for k in range(m+1)]
                assert sum(expected)==1 and actual==expected==coefficient
                for k,reference in enumerate(expected):
                    assert draft.haar_click_probability(m,N,k)==haar(m,N,k)
                    for function in (draft.haar_click_probability_loss,draft.haar_loss_coefficient_formula):
                        error=abs(function(m,N,k,float(eta))-float(reference))
                        max_formula_error=max(max_formula_error,error)
                        assert error<1e-12
                    checks+=1
                exact_rows.append(dict(m=m,N=N,eta=eta,exact_click_probabilities=actual))
    result['exact_loss_checks']=dict(occupation_cases=len(exact_rows),click_values=checks,
        maximum_draft_float_error=max_formula_error,rows=exact_rows)
    maxima=[]
    for m in range(4,41,2):
        k=m//2;values={N:haar(m,N,k) for N in range(k,4*m+1)}
        per_attempt,_=maximizers(values)
        per_photon,_=maximizers({N:v/N for N,v in values.items()})
        expected=[2] if m==4 else [3,4] if m==6 else [m-3]
        assert per_attempt==[m-2,m-1] and per_photon==expected
        assert tuple(per_attempt)==draft.optimal_photon_numbers(m,k,4*m)
        assert tuple(per_photon)==draft.optimal_photon_numbers(m,k,4*m,True)
        maxima.append(dict(m=m,search_cap=4*m,per_attempt_N=per_attempt,per_photon_N=per_photon))
    result['lossless_maxima']=maxima
    grid=[]
    for m in (4,6,8,10,12):
        for eta in (F(1,4),F(1,2),F(3,4),F(9,10),F(1)):
            for cap in (m,4*m):
                values={N:loss_mix(m,N,m//2,eta) for N in range(m//2,cap+1)}
                by_attempt,p=maximizers(values)
                by_photon,eff=maximizers({N:p/N for N,p in values.items()})
                grid.append(dict(m=m,eta=eta,N_cap=cap,per_attempt_N=by_attempt,per_attempt_probability=p,
                    expected_photon_optimal_N=by_photon,optimal_success_per_photon=eff,
                    optimal_expected_photons=1/eff,
                    minimum_encoding_success_per_photon=values[m//2]/(m//2),
                    finite_budget=[finite_budget(values,B) for B in (2*m,3*m,6*m)]))
    result['operational_grid']=grid
    fixed=[];max_loss_error=0.;max_fock_error=0.
    for N in range(5):
        ev=draft.ThresholdEvaluator(4,N)
        for seed in (20261121,20261122,20261123):
            U=ev.solver.random_interferometer(seed)
            for model in ('bosonic','distinguishable'):
                states,reference_fock=independent_fock_probabilities(U,N,model)
                actual_fock=ev.fock_probabilities(U,model)
                assert states==[tuple(t) for t in ev.occupations]
                fock_error=float(np.max(abs(reference_fock-actual_fock)))
                max_fock_error=max(max_fock_error,fock_error);assert fock_error<1e-10
                for eta in (F(1,4),F(1,2),F(3,4),F(1)):
                    reference=independent_detected_distribution(U,N,eta,model)
                    actual=ev.probabilities(U,model,float(eta))
                    error=float(np.max(abs(reference-actual)))
                    max_loss_error=max(max_loss_error,error);assert error<1e-10
                    fixed.append(dict(m=4,N=N,seed=seed,model=model,eta=eta,
                        independent_binary_distribution=reference.tolist(),max_draft_difference=error))
    result['fixed_circuit_checks']=dict(cases=len(fixed),max_fock_error=max_fock_error,
        max_threshold_loss_error=max_loss_error,rows=fixed)
    for N in (5,6):
        try:draft.ThresholdEvaluator(4,N)
        except ValueError:pass
        else:raise AssertionError('Distinct-input evaluator unexpectedly accepts N>m')
    m4={N:loss_mix(4,N,2,F(1,2)) for N in (2,3,4)}
    assert m4=={2:F(3,20),3:F(3,10),4:F(57,140)}
    full_gate={N:F(1,2)**N*haar(4,N,2) for N in (2,3,4)}
    assert full_gate[4]==F(9,280) and full_gate[4]<full_gate[2]
    B=30;prob={N:haar(8,N,4) for N in range(4,9)}
    stationary={N:1-(1-p)**(B//N) for N,p in prob.items()}
    assert maximizers({N:p/N for N,p in prob.items()})[0]==[5]
    assert maximizers(stationary)[0]==[6]
    identity={N:F(math.comb(N,2),2**N) for N in (2,3,4)}
    assert maximizers({N:p/N for N,p in identity.items()})[0]==[2,3]
    result['counterexamples']=dict(loss_plateau_m4_eta_half=m4,
        all_N_detected_m4_eta_half=full_gate,
        finite_budget_m8_eta_one_B30=dict(photon_optimal_N=[5],stationary_optimal_N=[6],
            stationary_success_N5=stationary[5],stationary_success_N6=stationary[6],
            advantage_N6=stationary[6]-stationary[5]),
        fixed_identity_m4_eta_half=dict(probabilities=identity,per_photon_N=[2,3]),
        nonuniform_detector_m2_N2_k2=dict(efficiencies=[1,0],true_probability=0,
            incorrect_average_efficiency_prediction=loss_mix(2,2,2,F(1,2))))
    result['m4_phase_diagram']=dict(per_attempt_switch=(21-math.sqrt(21))/20,
        per_photon_switch_4_to_3=(28-math.sqrt(154))/30,per_photon_switch_3_to_2=.75)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--draft-root',type=Path,default=DEFAULT_DRAFT_ROOT)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.draft_root=args.draft_root.resolve()
    if args.output.exists():parser.error('Refusing to overwrite evidence')
    source=args.draft_root/'src/photonic_balanced_partitioning/photonic/threshold_budget.py'
    paths=[Path(__file__).resolve(),ROOT/'research/phase3_threshold_contract.md',
        ROOT/'src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py',
        args.draft_root/'theory/phase2_candidates.md',source,args.draft_root/'tests/test_threshold_budget.py']
    before={str(p):sha(p) for p in paths}
    name='photonic_balanced_partitioning.photonic._phase3_threshold_draft'
    spec=importlib.util.spec_from_file_location(name,source)
    draft=importlib.util.module_from_spec(spec);spec.loader.exec_module(draft)
    started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
    result=dict(status='running',assertion_tested='Exact Haar-loss occupancy identities; criteria-specific photon maxima; independent bounded Fock/loss channel checks',
        non_claims=['No novelty or quantum/optimization advantage','No performance claim for a fixed or trained U from Haar averages','N>m theorem domain requires a different source than the current evaluator'],
        protocol=dict(exact_m=list(range(1,7)),exact_N='0 through m+2',etas=['0','1/4','1/2','3/4','1'],
            circuit_modes=4,circuit_photons=list(range(5)),circuit_seeds=[20261121,20261122,20261123],
            numeric_tolerance=1e-10),
        provenance=dict(started_at_utc=started,command=[sys.executable,*sys.argv],
            worktree_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            worktree_dirty_state=subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True).splitlines(),
            python=sys.version,numpy=np.__version__,scipy=importlib.metadata.version('scipy'),
            perceval=importlib.metadata.version('perceval-quandela'),hardware=platform.platform(),
            input_hashes_before=before))
    code=0
    try:
        audit(draft,result);result['status']='completed'
    except Exception as exc:
        result['status']='failed';result['error']=repr(exc);result['traceback']=traceback.format_exc();code=1
    after={str(p):sha(p) for p in paths};result['provenance']['input_hashes_after']=after
    result['provenance']['runtime_seconds']=time.perf_counter()-start
    if before!=after:result['status']='inputs-changed';code=1
    args.output.write_text(json.dumps(clean(result),indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'],output=str(args.output),sha256=sha(args.output),
        runtime_seconds=result['provenance']['runtime_seconds']),indent=2))
    raise SystemExit(code)

if __name__=='__main__':main()
