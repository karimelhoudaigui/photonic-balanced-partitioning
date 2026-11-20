#!/usr/bin/env python3
"""Test spatial-overlap TV certificates and a balanced-density falsifier."""
import argparse
from fractions import Fraction
from itertools import combinations
import math
from pathlib import Path
import numpy as np
from scipy.linalg import expm, null_space
from run_research import save
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh


def distinguishable(U, solver):
    states=solver._enumerate_all_fock_states()
    rows=np.array([np.repeat(np.arange(solver.n),s) for s in states])
    matrix=abs(U[rows,:solver.k])**2
    masks=np.arange(1,1<<solver.k)
    subsets=((masks[:,None] >> np.arange(solver.k)) & 1).astype(float)
    signs=(-1.)**(solver.k-subsets.sum(axis=1))
    p=np.prod(matrix @ subsets.T,axis=1) @ signs
    p/=np.array([math.prod(math.factorial(c) for c in s) for s in states])
    assert p.min()>-1e-12 and abs(p.sum()-1)<1e-10
    return p


def derangements(r):
    if r==0:return 1
    if r==1:return 0
    a,b=1,0
    for j in range(2,r+1):a,b=b,(j-1)*(a+b)
    return b


def polynomial(k,S):
    return sum(derangements(r)/math.factorial(r)*S**(r/2) for r in range(2,k+1))


def inspect(U):
    n=len(U);k=n//2;solver=FixedPhotonObliq(n)
    p=abs(solver.output_state(U))**2;d=distinguishable(U,solver)
    tv=float(abs(p-d).sum()/2)
    B=abs(U[:,:k]).T @ abs(U[:,:k]);S=float(np.sum((B-np.eye(k))**2))
    permanent=float(solver._permanent(B).real)
    states=np.asarray(solver._enumerate_all_fock_states())
    delta=float(p[np.any(states>1,axis=1)].sum())
    Q=sum(float(np.sum(abs(U[:,a])**2*abs(U[:,b])**2)) for a,b in combinations(range(k),2))
    exact_bound=min(1.,max(0.,(permanent-1)/2))
    poly_bound=min(1.,polynomial(k,S)/2)
    collision_bound=min(1.,polynomial(k,n*math.comb(k,2)*delta)/2)
    assert tv<=exact_bound+1e-10
    assert tv<=poly_bound+1e-10
    assert exact_bound<=poly_bound+1e-10
    assert S<=n*math.comb(k,2)*delta+1e-10
    assert tv<=collision_bound+1e-10
    return dict(n=n,k=k,tv=tv,collision_probability=delta,S=S,Q=Q,
                permanent_bound=exact_bound,polynomial_bound=poly_bound,
                collision_only_bound=collision_bound,normalization_error=max(abs(p.sum()-1),abs(d.sum()-1)))


def counterexample(k):
    n=2*k;L=k+2
    u=np.ones(L)/np.sqrt(L)
    v=np.r_[np.ones(L//2),-np.ones(L//2)]/np.sqrt(L)
    active=np.c_[u,v,null_space(np.stack([u,v]))]
    U=np.zeros((n,n),dtype=complex)
    U[:L,:2]=active[:,:2]
    U[:L,k:]=active[:,2:]
    for j in range(k-2):U[L+j,2+j]=1
    np.testing.assert_allclose(U.conj().T @ U,np.eye(n),atol=1e-12)
    return U


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    if any(p.name not in ['stdout.txt','stderr.txt'] for p in args.output.iterdir()):parser.error('Refusing overwrite')
    rows=[]
    for n in [4,6,8]:
        for seed in range(10):
            rng=np.random.default_rng(20261120+100*n+seed)
            H=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));H=(H+H.conj().T)/(2*np.sqrt(n))
            U0=np.eye(n,dtype=complex)
            for a in range(n//2):
                pair=[a,a+n//2];U0[np.ix_(pair,pair)]=RectangularMesh.gate(.17*(a+1),.3*a)
            for tau in [0.,.0001,.001,.01,.05,.1,.3,1.]:
                rows.append(dict(seed=20261120+100*n+seed,tau=tau,**inspect(expm(1j*tau*H) @ U0)))
    examples=[]
    for k in [2,4,6,8,10,20,50,100,1000]:
        L=k+2
        # Exact arithmetic, including output multiplicities, independent of
        # the floating Fock simulator. Spectator photons add no randomness.
        types=[(L,Fraction(2,L*L),Fraction(1,L*L)),
               (L*(L-2)//4,Fraction(4,L*L),Fraction(2,L*L)),
               (L*L//4,Fraction(0),Fraction(2,L*L))]
        assert sum(count*p for count,p,d in types)==1
        assert sum(count*d for count,p,d in types)==1
        tv=sum(count*abs(p-d) for count,p,d in types)/2
        assert tv==Fraction(1,2)
        record=dict(n=2*k,k=k,active_modes=L,exact_tv=str(tv),exact_collision_probability=str(Fraction(2,L)),
                    p_cf=float(1-Fraction(2,L)),outcome_classes=[dict(count=c,p=str(p),d=str(d)) for c,p,d in types])
        if k<=6:
            U=counterexample(k);result=inspect(U)
            assert abs(result['tv']-.5)<1e-10
            assert abs(result['collision_probability']-2/L)<1e-10
            record.update(full_fock_check=result,unitary_real=U.real.tolist(),unitary_imag=U.imag.tolist())
        examples.append(record)
    save(args.output/'counterexamples.json',dict(examples=examples,setting='balanced m=2k, ideal full Fock, no postselection'))
    save(args.output/'summary.json',dict(experiment='E08 overlap certificate and balanced counterexample',
        seed=20261120,interpolation_cases=len(rows),counterexample_cases=len(examples),
        full_fock_counterexample_sizes=[4,8,12],
        max_normalization_error=max(r['normalization_error'] for r in rows),
        nonvacuous_permanent_certificates=sum(r['permanent_bound']<1 for r in rows),
        nonvacuous_polynomial_certificates=sum(r['polynomial_bound']<1 for r in rows),
        assertion='TV inequalities verified within 1e-10 in finite cases; exact rational TV=1/2 counterexamples',
        novelty='OPEN; numerical validity and independent proof review do not establish novelty',results=rows))
    print(f'Certificate checks PASS: {len(rows)} circuits, {len(examples)} rational counterexamples, full Fock n=4/8/12',flush=True)


if __name__=='__main__': main()
