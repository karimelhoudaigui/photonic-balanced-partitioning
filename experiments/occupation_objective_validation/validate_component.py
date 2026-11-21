"""Bounded full-Fock and local Perceval audit; no training or device access."""
from __future__ import annotations
import argparse
from datetime import datetime,timezone
import importlib.metadata
from itertools import combinations
import json
from pathlib import Path
import platform
import time
import numpy as np
import perceval as pcvl
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.optical_penalty import _fock_amplitudes
from photonic_balanced_partitioning.photonic.occupation_objective import (
    occupation_cost,occupation_moments,occupation_expectation,occupation_statistics_gap,
)


def independent_distribution(columns):
    table={(0,)*len(columns):1.}
    for column in columns.T:
        new={}
        for t,p in table.items():
            for i,q in enumerate(column):
                s=list(t);s[i]+=1;s=tuple(s)
                new[s]=new.get(s,0.)+p*q
        table=new
    assert abs(sum(table.values())-1)<1e-11
    return table


def moments(table):
    states=np.array(list(table),dtype=float);p=np.array(list(table.values()))
    return dict(mean=p@states,second=np.einsum('s,si,sj->ij',p,states,states),
        pairs=float(p@np.sum(states*(states-1)/2,axis=1)))


def mean_cost(table,edges,mu):
    return float(sum(p*(sum(w*(t[i]-t[j])**2 for i,j,w in edges)
        +mu*sum(x*(x-1)/2 for x in t)) for t,p in table.items()))


def inspect_case(n,seed,perceval):
    solver=FixedPhotonObliq(n);k=n//2;U=solver.random_interferometer(seed);V=U[:,:k]
    edges=[(i,j,.2+((i+2*j+seed)%7)/5) for i,j in combinations(range(n),2) if (i+j+seed)%3]
    mu=sum(w for _,_,w in edges)+.5
    bosonic={t:float(abs(a)**2) for t,a in _fock_amplitudes(U,(1,)*k+(0,)*(n-k),1000).items()}
    dist=independent_distribution(abs(V)**2)
    assert abs(sum(bosonic.values())-1)<1e-11
    references={'bosonic':bosonic,'distinguishable':dist}
    records={}
    for model,table in references.items():
        reference=moments(table);actual=occupation_moments(V,model)
        e=mean_cost(table,edges,mu);formula=occupation_expectation(V,edges,mu,model)
        error=max(float(np.max(abs(reference['mean']-actual.mean))),
            float(np.max(abs(reference['second']-actual.second))),abs(reference['pairs']-actual.collision_pairs))
        assert error<2e-11 and abs(formula-e)<2e-10
        records[model]=dict(reference_mean=reference['mean'].tolist(),
            reference_second=reference['second'].tolist(),reference_pairs=reference['pairs'],
            reference_mean_cost=e,formula_mean_cost=formula,max_moment_error=error,
            mean_cost_error=abs(formula-e),probabilities=[dict(occupation=list(t),p=float(p)) for t,p in sorted(table.items())])
    gap=occupation_statistics_gap(V,edges,mu)
    empirical=records['bosonic']['reference_mean_cost']-records['distinguishable']['reference_mean_cost']
    covgap=moments(bosonic)['second']-moments(dist)['second']
    mineig=float(np.linalg.eigvalsh(covgap).min())
    assert mineig>-2e-11 and abs(empirical-gap.total)<2e-10 and gap.total>=0
    pv=None
    if perceval:
        backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Circuit(n).add(0,pcvl.Unitary(pcvl.Matrix(U))))
        backend.set_input_state(pcvl.BasicState([1]*k+[0]*(n-k)))
        pv_b={t:float(backend.probability(pcvl.BasicState(list(t)))) for t in solver._enumerate_all_fock_states()}
        columns=np.empty((n,k))
        for a in range(k):
            source=[0]*n;source[a]=1;backend.set_input_state(pcvl.BasicState(source))
            for i in range(n):
                output=[0]*n;output[i]=1
                columns[i,a]=float(backend.probability(pcvl.BasicState(output)))
        pv_d=independent_distribution(columns)
        errors={}
        for model,table in [('bosonic',pv_b),('distinguishable',pv_d)]:
            assert abs(sum(table.values())-1)<2e-11
            errors[model]=max(abs(table[t]-references[model][t]) for t in table)
            assert errors[model]<2e-11
            ref=moments(table);formula=occupation_moments(V,model)
            assert np.max(abs(ref['second']-formula.second))<2e-11
        pv=dict(max_probability_errors=errors,
            bosonic_full_fock=[dict(occupation=list(t),p=float(p)) for t,p in sorted(pv_b.items())],
            distinguishable_control='Convolution of labelled independent local-Perceval one-photon outputs',
            single_photon_probability_columns=columns.tolist())
    return dict(n=n,k=k,seed=seed,edges=edges,mu=mu,unitary_real=U.real.tolist(),unitary_imag=U.imag.tolist(),
        distributions=records,gap=dict(graph=gap.graph,collision=gap.collision,total=gap.total,
            from_full_distribution=empirical,error=abs(empirical-gap.total)),
        min_covariance_gap_eigenvalue=mineig,perceval=pv)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Refusing to overwrite evidence')
    started=datetime.now(timezone.utc).isoformat();start=time.perf_counter();rows=[]
    for n in (4,6):
        for i in range(12):rows.append(inspect_case(n,20261121+100*n+i,False))
        for i in range(4):rows.append(inspect_case(n,90100+100*n+i,True))
    U=np.array([[1,1,1,1],[1,1,-1,-1],[1,-1,1,-1],[1,-1,-1,1]])/2
    b={t:float(abs(a)**2) for t,a in _fock_amplitudes(U,(1,1,0,0),100).items()}
    d=independent_distribution(abs(U[:,:2])**2);edges=[(0,1,1.),(1,2,1.),(2,3,1.)]
    target={(1,1,0,0),(0,0,1,1)}
    walsh=dict(mu=4.,bosonic_mean=mean_cost(b,edges,4.),distinguishable_mean=mean_cost(d,edges,4.),
        bosonic_success=sum(p for t,p in b.items() if t in target),
        distinguishable_success=sum(p for t,p in d.items() if t in target),
        bosonic_full_fock=[dict(occupation=list(t),p=p) for t,p in sorted(b.items())],
        distinguishable_full_fock=[dict(occupation=list(t),p=p) for t,p in sorted(d.items())])
    assert abs(walsh['bosonic_mean']-5.5)<1e-12 and abs(walsh['distinguishable_mean']-4)<1e-12
    assert abs(walsh['bosonic_success']-.5)<1e-12 and abs(walsh['distinguishable_success']-.25)<1e-12
    max_moment=max(r['distributions'][m]['max_moment_error'] for r in rows for m in ('bosonic','distinguishable'))
    max_energy=max(r['distributions'][m]['mean_cost_error'] for r in rows for m in ('bosonic','distinguishable'))
    max_pv=max(r['perceval']['max_probability_errors'][m] for r in rows if r['perceval'] for m in ('bosonic','distinguishable'))
    summary=dict(status='completed',started_at_utc=started,runtime_seconds=time.perf_counter()-start,
        cases=len(rows),perceval_circuits=sum(r['perceval'] is not None for r in rows),
        max_moment_error=max_moment,max_energy_error=max_energy,max_perceval_probability_error=max_pv,
        max_positive_gap_error=max(r['gap']['error'] for r in rows),
        minimum_covariance_gap_eigenvalue=min(r['min_covariance_gap_eigenvalue'] for r in rows),
        physical_shots=0,training_evaluations=0,
        environment=dict(python=platform.python_version(),numpy=np.__version__,
            scipy=importlib.metadata.version('scipy'),perceval=importlib.metadata.version('perceval-quandela')),
        interpretation='Bounded implementation checks, not a numerical proof or novelty certificate',
        rows=rows,walsh_counterexample=walsh)
    args.output.write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('rows','walsh_counterexample')},indent=2))

if __name__=='__main__':main()
