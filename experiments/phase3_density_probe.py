#!/usr/bin/env python3
"""P33 fixed-grid falsification of a density/collision certificate, no training."""
import argparse
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import time
import numpy as np
from scipy.linalg import expm

from photonic_balanced_partitioning.photonic.density_certificate import density_certificate
from photonic_balanced_partitioning.photonic.optical_penalty import _fock_amplitudes
from photonic_balanced_partitioning.photonic.threshold_budget import ThresholdEvaluator


def pair_unitary(m):
    k=m//2;u=np.zeros((m,m),complex)
    for a in range(k):
        u[2*a:2*a+2,a]=1/np.sqrt(2)
        u[2*a:2*a+2,k+a]=np.array([1.,-1.])/np.sqrt(2)
    return u


def frame_case(m,seed,strength):
    rng=np.random.default_rng(seed);h=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m));h=(h+h.conj().T)/2
    h/=np.max(abs(np.linalg.eigvalsh(h)))
    return expm(1j*strength*h)@pair_unitary(m)


def flat_frame_case(m,seed,strength):
    """All output intensities exactly 1/2, with globally interacting orbitals."""
    k=m//2;rng=np.random.default_rng(seed)
    h=rng.normal(size=(k,k))+1j*rng.normal(size=(k,k));h=(h+h.conj().T)/2
    h/=np.max(abs(np.linalg.eigvalsh(h)))
    right=np.eye(m,dtype=complex);right[:k,:k]=expm(1j*strength*h)
    return pair_unitary(m)@right


def component_size(gram):
    unseen=set(range(len(gram)));largest=0
    while unseen:
        todo=[unseen.pop()];count=0
        while todo:
            a=todo.pop();count+=1;neighbors={b for b in unseen if gram[a,b]>1e-12}
            unseen-=neighbors;todo.extend(neighbors)
        largest=max(largest,count)
    return largest


def complete_check(u,seed,strength,perceval_check=False):
    m=len(u);k=m//2;source=(1,)*k+(0,)*(m-k);certificate=density_certificate(u[:,:k])
    amplitudes=_fock_amplitudes(u,source,20000)
    states=sorted(amplitudes);pb=np.array([abs(amplitudes[t])**2 for t in states])
    evaluator=ThresholdEvaluator(m,k);pd0=evaluator.fock_probabilities(u,'distinguishable')
    lookup={tuple(t):p for t,p in zip(evaluator.occupations,pd0)}
    pd=np.array([lookup[t] for t in states]);occupations=np.array(states)
    norm_error=max(abs(pb.sum()-1),abs(pd.sum()-1));assert norm_error<1e-9
    tv=float(abs(pb-pd).sum()/2);collision_pairs=np.sum(occupations*(occupations-1)/2,axis=1)
    measured_pairs=float(pb@collision_pairs)
    assert abs(measured_pairs-certificate['expected_collision_pairs'])<1e-9
    for bound in ['direct_gram_tv_bound','support_cycle_tv_bound','density_cycle_tv_bound',
                  'refined_density_cycle_tv_bound','support_state_tv_bound']:
        assert tv<=certificate[bound]+1e-9,(m,seed,strength,bound,tv,certificate[bound])
    cf=np.max(occupations,axis=1)<=1
    q=abs(u[:,:k])**2;gram=np.sqrt(q).T@np.sqrt(q)
    record=dict(certificate=certificate,seed=seed,strength=strength,actual_tv=tv,
                raw_norm_error=float(norm_error),collision_pairs_from_full_fock=measured_pairs,
                p_cf_bosonic=float(pb[cf].sum()),p_cf_distinguishable=float(pd[cf].sum()),
                largest_occupied_overlap_component=component_size(gram),full_fock_outcomes=len(states),
                bosonic_probabilities=pb.tolist(),distinguishable_probabilities=pd.tolist())
    if perceval_check:
        import perceval as pcvl
        backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
        backend.set_input_state(pcvl.BasicState(source));reference=backend.prob_distribution()
        error=float(max(abs(p-reference.get(pcvl.BasicState(t),0.)) for t,p in zip(states,pb)))
        assert error<1e-10;record['perceval_max_probability_error']=error
    return record,states


def dilute_counterexample(k):
    m=2*k;active=k+2;v=np.zeros((m,k),complex)
    v[:active,0]=1/np.sqrt(active)
    v[:active,1]=np.r_[np.ones(active//2),-np.ones(active//2)]/np.sqrt(active)
    for a in range(2,k):v[active+a-2,a]=1
    certificate=density_certificate(v);pb=[];pd=[]
    for i,j in combinations_with_replacement(range(active),2):
        if i==j:
            pb.append(2*abs(v[i,0]*v[i,1])**2);pd.append(abs(v[i,0]*v[i,1])**2)
        else:
            pb.append(abs(v[i,0]*v[j,1]+v[j,0]*v[i,1])**2)
            pd.append(abs(v[i,0]*v[j,1])**2+abs(v[j,0]*v[i,1])**2)
    tv=float(np.sum(abs(np.array(pb)-np.array(pd)))/2)
    assert abs(tv-.5)<1e-12 and abs(sum(pb)-1)<1e-12 and abs(sum(pd)-1)<1e-12
    assert certificate['density_cycle_tv_bound']==1
    return dict(certificate=certificate,active_modes=active,actual_tv=tv,
                analytic_p_collision=2/active,
                active_bosonic_probabilities=pb,active_distinguishable_probabilities=pd,
                interpretation='Exact deterministic spectator factorization; small mean collisions alone is insufficient.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seed-offset',type=int,default=0);args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=False);started=time.monotonic();records=[];bases={}
    progress=(args.output/'progress.jsonl').open('w')
    def checkpoint(kind,record):
        light={key:value for key,value in record.items() if 'probabilities' not in key}
        progress.write(json.dumps(dict(kind=kind,record=light),allow_nan=False)+'\n');progress.flush()
    for m in [4,6,8,10,12]:
        for repeat in range(3):
            seed=2026112100+100*m+repeat+args.seed_offset
            for family,builder in [('global_output_mix',frame_case),('flat_fixed_projector',flat_frame_case)]:
                for scale in [0.,.02,.06,.2,.6]:
                    strength=scale/np.sqrt(m//2)
                    record,states=complete_check(builder(m,seed,strength),seed,float(strength),repeat==0 and scale==.06)
                    record['family']=family;records.append(record);bases[str(m)]=states;checkpoint('complete_fock',record)
    scalable=[]
    for m in [32,64,128]:
        for repeat in range(3):
            seed=2026112100+100*m+repeat+args.seed_offset
            for scale in [.02,.06,.2,.6]:
                strength=float(scale/np.sqrt(m//2));u=frame_case(m,seed,strength)
                certificate=density_certificate(u[:,:m//2]);gram=abs(u[:,:m//2]).T@abs(u[:,:m//2])
                scalable.append(dict(certificate=certificate,seed=seed,strength=strength,
                    largest_occupied_overlap_component=component_size(gram),
                    unitary_sha256=hashlib.sha256(u.tobytes()).hexdigest(),
                    full_distribution_executed=False))
                checkpoint('certificate_only',scalable[-1])
    counterexamples=[dilute_counterexample(k) for k in [2,4,8,16,32,64]]
    for record in counterexamples:checkpoint('dilute_factorized',record)
    sharpness=[]
    for angle in [0.,.001,.003,.01,.03,.1,.3]:
        right=np.eye(4,dtype=complex);c,s=np.cos(angle),np.sin(angle)
        right[:2,:2]=[[c,-s],[s,c]]
        record,_=complete_check(pair_unitary(4)@right,0,angle)
        expected=2*c*c*s*s
        assert abs(record['actual_tv']-expected)<1e-12
        assert abs(record['certificate']['dominant_support_leakage']-2*s*s)<1e-12
        assert abs(record['certificate']['expected_collision_pairs']-expected)<1e-12
        record['analytic_tv']=float(expected);sharpness.append(record);checkpoint('balanced_sharpness',record)
    progress.close()
    raw=dict(question='Does the candidate density certificate survive complete-distribution checks and the known dilute obstruction?',
        seed_offset=args.seed_offset,physical_shots=0,full_fock_bases=bases,full_checks=records,
        scalable_certificate_only=scalable,dilute_counterexamples=counterexamples,balanced_sharpness=sharpness,
        runtime_seconds=time.monotonic()-started,
        hypothesis_status='FINITE_CHECKS_SUPPORTED_PROOF_AND_NOVELTY_REVIEW_REQUIRED',
        non_claims=['No training or optimization improvement','No full-distribution validation at m32/64/128',
                   'No general bound from collision probability alone','No QPU or hardware evidence',
                   'A trivial certificate does not establish hardness or quantum advantage'])
    (args.output/'raw.json').write_text(json.dumps(raw,allow_nan=False,separators=(',',':'))+'\n')
    summary=dict(full_cases=len(records),full_fock_probability_pairs=sum(r['full_fock_outcomes'] for r in records),
        scalable_certificate_only_cases=len(scalable),dilute_counterexamples=len(counterexamples),
        balanced_sharpness_cases=len(sharpness),physical_shots=0,
        max_raw_normalization_error=max(r['raw_norm_error'] for r in records),
        max_collision_moment_error=max(abs(r['collision_pairs_from_full_fock']-r['certificate']['expected_collision_pairs']) for r in records),
        max_perceval_probability_error=max(r.get('perceval_max_probability_error',0.) for r in records),
        nontrivial_support_certificates=sum(r['certificate']['support_cycle_tv_bound']<1 for r in records),
        all_bounds_passed=True,scientific_acceptance='PENDING_PROOF_AND_NOVELTY_REVIEW')
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':main()
