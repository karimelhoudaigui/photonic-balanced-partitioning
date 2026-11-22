"""Bounded falsification of a new conjecture, not an optimization experiment."""
import argparse
import json
import math
from pathlib import Path
import time
import numpy as np
from photonic_balanced_partitioning.photonic.optical_penalty import _fock_amplitudes
from photonic_balanced_partitioning.photonic.density_certificate import density_certificate


def labelled_law(v,states):
    m,k=v.shape;law={(0,)*m:1.}
    for a in range(k):
        nxt={}
        for t,p in law.items():
            for i in range(m):
                x=list(t);x[i]+=1;x=tuple(x)
                nxt[x]=nxt.get(x,0.)+p*abs(v[i,a])**2
        law=nxt
    return np.array([law[t] for t in states])


def inspect(u,k,label,seed,strength,bases):
    m=len(u);source=[1]*k+[0]*(m-k)
    amplitudes=_fock_amplitudes(u,source,30000);states=sorted(amplitudes)
    b=np.array([abs(amplitudes[t])**2 for t in states]);d=labelled_law(u[:,:k],states)
    assert len(states)==math.comb(m+k-1,k)
    normalization=max(abs(b.sum()-1),abs(d.sum()-1));assert normalization<1e-9
    certificate=density_certificate(u[:,:k]);delta=certificate['dominant_support_leakage']
    tv=float(abs(b-d).sum()/2)
    assert tv<=certificate['support_cycle_tv_bound']+1e-9
    bases[f'{m},{k}']=states
    return {'m':m,'k':k,'family':label,'seed':seed,'strength':strength,'delta':delta,
        'tv':tv,'linear_bound_excess':tv-min(1.,delta),'normalization_error':float(normalization),
        'unitary_real':u.real.tolist(),'unitary_imag':u.imag.tolist(),
        'bosonic_probabilities':b.tolist(),'distinguishable_probabilities':d.tolist(),
        'existing_support_cycle_estimate':certificate['support_cycle_tv_bound']}


def main(output):
    output.mkdir(parents=True,exist_ok=False);started=time.monotonic();records=[];bases={}
    for m,k in [(3,3),(4,4),(6,6),(8,8),(4,2),(6,3),(8,4),(10,5)]:
        for repeat in range(5):
            seed=2026112200+100*m+repeat;rng=np.random.default_rng(seed)
            z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m));h=(z+z.conj().T)/2
            values,vectors=np.linalg.eigh(h);values/=max(abs(values))
            starts=[('coordinate_random',np.eye(m,dtype=complex))]
            if m==2*k:
                pair=np.zeros((m,m),complex)
                for i in range(m):pair[i,i//2]=1/math.sqrt(2);pair[i,k+i//2]=(-1)**i/math.sqrt(2)
                starts.append(('paired_random',pair))
            for label,base in starts:
                for strength in [.03,.15,.5,1.]:
                    u=((vectors*np.exp(1j*strength*values))@vectors.conj().T)@base
                    records.append(inspect(u,k,label,seed,strength,bases))
        if m==k:
            for strength in [.03,.15,.5,1.]:
                u=np.eye(m,dtype=complex)+(np.exp(1j*strength)-1)*np.ones((m,m))/m
                records.append(inspect(u,k,'collective_rank_one',None,strength,bases))
    assert len(records)==256
    candidates=[i for i,r in enumerate(records) if r['linear_bound_excess']>1e-9]
    raw={'conjecture':'Full-law TV <= min(1,dominant_support_leakage)',
        'status':'NUMERIC_COUNTEREXAMPLE_PENDING_INDEPENDENT_CHECK' if candidates else 'FINITE_GRID_ONLY_NO_REFUTATION',
        'records':records,'full_fock_bases':bases,'candidate_counterexample_indices':candidates,
        'physical_shots':0,'runtime_seconds':time.monotonic()-started,
        'non_claims':['No universal proof from finite checks','No optimization or quantum advantage','No hardware or interval certification']}
    (output/'raw.json').write_text(json.dumps(raw,separators=(',',':'))+'\n')
    summary={k:raw[k] for k in ['status','candidate_counterexample_indices','physical_shots','runtime_seconds']}
    summary.update(cases=len(records),max_linear_bound_excess=max(r['linear_bound_excess'] for r in records),
        max_normalization_error=max(r['normalization_error'] for r in records))
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
