#!/usr/bin/env python3
"""Coordinator audit: raw sums, independent labelled DP and fresh Perceval checks."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np


def reconstructed_unitary(m,seed,strength,family):
    k=m//2;size=m if family=='global_output_mix' else k
    rng=np.random.default_rng(seed)
    z=rng.standard_normal((size,size))+1j*rng.standard_normal((size,size))
    h=(z+z.conj().T)/2
    values,vectors=np.linalg.eigh(h)
    rotation=(vectors*np.exp(1j*strength*values/max(abs(values))))@vectors.conj().T
    pair=np.zeros((m,m),complex)
    for i in range(m):
        pair[i,i//2]=1/math.sqrt(2)
        pair[i,k+i//2]=(-1)**i/math.sqrt(2)
    if family=='global_output_mix':return rotation@pair
    block=np.eye(m,dtype=complex);block[:k,:k]=rotation
    return pair@block


def independent_labelled_dp(v,basis):
    m,k=v.shape;law={(0,)*m:1.}
    for a in range(k):
        following={}
        for occupation,weight in law.items():
            for i in range(m):
                target=list(occupation);target[i]+=1;target=tuple(target)
                following[target]=following.get(target,0.)+weight*abs(v[i,a])**2
        law=following
    return np.array([law[tuple(t)] for t in basis])


def audit(root,output):
    import perceval as pcvl
    preservation=json.loads((root/'preservation.json').read_text())
    for item in preservation['files']:
        assert hashlib.sha256(Path(item['preserved']).read_bytes()).hexdigest()==item['sha256']
    batches=[];seeds=[];selected=[]
    for mode,offset in [('primary',0),('replication',100000)]:
        path=root/mode/'data/raw.json';raw=json.loads(path.read_text())
        assert raw['seed_offset']==offset and raw['physical_shots']==0
        rows=raw['full_checks'];assert len(rows)==150
        expected={(m,f,2026112100+100*m+r+offset,round(s/math.sqrt(m//2),12))
                  for m in [4,6,8,10,12] for f in ['global_output_mix','flat_fixed_projector']
                  for r in range(3) for s in [0.,.02,.06,.2,.6]}
        observed={(r['certificate']['m'],r['family'],r['seed'],round(r['strength'],12)) for r in rows}
        assert observed==expected and len(observed)==len(rows)
        seeds.append({r['seed'] for r in rows})
        maxima=dict(normalization=0.,tv_recalculation=0.,bosonic_pair_moment=0.,
                    distinguishable_pair_moment=0.,collision_free_mass=0.,bound_excess=0.)
        count=0
        for row in rows+raw['balanced_sharpness']:
            m=row['certificate']['m'];k=m//2;basis=raw['full_fock_bases'][str(m)]
            assert len(basis)==math.comb(m+k-1,k) and len({tuple(t) for t in basis})==len(basis)
            assert all(all(isinstance(x,int) and x>=0 for x in t) and sum(t)==k for t in basis)
            b=np.array(row['bosonic_probabilities']);d=np.array(row['distinguishable_probabilities'])
            assert len(b)==len(d)==len(basis) and min(b.min(),d.min())>=0
            occupations=np.array(basis);pairs=np.sum(occupations*(occupations-1)/2,axis=1)
            cf=np.max(occupations,axis=1)<=1;tv=float(np.abs(b-d).sum()/2)
            maxima['normalization']=max(maxima['normalization'],abs(b.sum()-1),abs(d.sum()-1))
            maxima['tv_recalculation']=max(maxima['tv_recalculation'],abs(tv-row['actual_tv']))
            moment=row['certificate']['expected_collision_pairs']
            maxima['bosonic_pair_moment']=max(maxima['bosonic_pair_moment'],abs(b@pairs-moment))
            maxima['distinguishable_pair_moment']=max(maxima['distinguishable_pair_moment'],abs(d@pairs-moment/2))
            maxima['collision_free_mass']=max(maxima['collision_free_mass'],
                abs(b[cf].sum()-row['p_cf_bosonic']),abs(d[cf].sum()-row['p_cf_distinguishable']))
            assert row['certificate']['numerical_semantics']=='FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED'
            for name,value in row['certificate'].items():
                if name.endswith('_tv_bound'):maxima['bound_excess']=max(maxima['bound_excess'],tv-value)
            assert max(maxima.values())<1e-9
        for row in rows:
            m=row['certificate']['m'];k=m//2;count+=row['full_fock_outcomes']
            if not (m in [4,6,8] and row['seed']==2026112100+100*m+2+offset and
                    abs(row['strength']-.2/math.sqrt(k))<1e-15):continue
            u=reconstructed_unitary(m,row['seed'],row['strength'],row['family'])
            basis=raw['full_fock_bases'][str(m)]
            backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
            backend.set_input_state(pcvl.BasicState([1]*k+[0]*(m-k)));reference=backend.prob_distribution()
            pb=np.array([reference.get(pcvl.BasicState(t),0.) for t in basis])
            pd=independent_labelled_dp(u[:,:k],basis)
            eb=float(np.max(abs(pb-np.array(row['bosonic_probabilities']))))
            ed=float(np.max(abs(pd-np.array(row['distinguishable_probabilities']))))
            assert max(eb,ed)<1e-10
            selected.append(dict(mode=mode,m=m,seed=row['seed'],strength=row['strength'],
                family=row['family'],perceval_error=eb,independent_labelled_dp_error=ed))
        assert len(raw['balanced_sharpness'])==7 and len(raw['dilute_counterexamples'])==6
        assert all(abs(r['actual_tv']-.5)<1e-12 and r['certificate']['density_cycle_tv_bound']==1
                   for r in raw['dilute_counterexamples'])
        assert len(raw['scalable_certificate_only'])==36
        assert all(r['full_distribution_executed'] is False for r in raw['scalable_certificate_only'])
        assert len((root/mode/'data/progress.jsonl').read_text().splitlines())==199
        batches.append(dict(mode=mode,full_grid_cases=len(rows),complete_outcome_pairs=count,
            maxima=maxima,raw_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    assert not seeds[0]&seeds[1] and len(selected)==12
    result=dict(verdict='IMPLEMENTATION_AND_FINITE_ASSERTION_VERIFIED_WITHIN_STATED_FLOAT_TOLERANCES',
        review_provenance='COORDINATOR_INDEPENDENT_CODE_PATHS; not a fresh-agent or interval audit',
        batches=batches,fresh_perceval_and_labelled_dp_checks=selected,
        source_reconstruction='eigh spectral rotation, independent of production scipy.expm',
        all_collisions_retained=True,physical_shots=0,novelty='OPEN',PAPER_READY=False,QPU_GATE='CLOSED')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({'verdict':result['verdict'],'full_cases':300,'fresh_cross_checks':len(selected),
                      'max_perceval_error':max(r['perceval_error'] for r in selected),
                      'max_labelled_dp_error':max(r['independent_labelled_dp_error'] for r in selected)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--evidence-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    audit(args.evidence_root,args.output)
