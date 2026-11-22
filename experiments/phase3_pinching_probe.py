"""P38: a new stronger-lemma discriminator, not a rerun of measured-TV search."""
import argparse
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
import json
import math
from pathlib import Path
import random
import time
import numpy as np
import perceval as pcvl
from photonic_balanced_partitioning.photonic.threshold_marginals import GaussianRational as C


def encode(x):
    if isinstance(x,F):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
    if isinstance(x,C):return {'real':encode(x.real),'imag':encode(x.imag)}
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


def frame(m,seed,t):
    width=m//3
    placement=[g*width for g in range(3)]
    placement += [i for i in range(m) if i not in placement]
    u=[[C(int(i==placement[j])) for j in range(m)] for i in range(m)]
    for g in range(3):
        start=g*width;old=[row[:] for row in u[start:start+width]]
        if width==2: block=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
        elif width==3: block=[[F(1,3),F(2,3),F(2,3)],[F(2,3),F(1,3),F(-2,3)],[F(2,3),F(-2,3),F(1,3)]]
        else:continue
        for a in range(width):
            u[start+a]=[sum((block[a][b]*old[b][j] for b in range(width)),C()) for j in range(m)]
    rng=random.Random(seed);pairs=list(combinations(range(m),2));rng.shuffle(pairs)
    for i,j in pairs:
        h=t*F(rng.choice((-3,-2,-1,1,2,3)),5);v=F(rng.choice((-5,-3,-1,1,3,5)),11)
        c=(1-h*h)/(1+h*h);s=2*h/(1+h*h)
        phase=C((1-v*v)/(1+v*v),2*v/(1+v*v));a,b=u[i][:],u[j][:]
        u[i]=[c*x-phase.conjugate()*s*y for x,y in zip(a,b)]
        u[j]=[phase*s*x+c*y for x,y in zip(a,b)]
    return u


def exact_domain(v):
    k=len(v[0]);owners=[];delta=F(0)
    for a in range(k):
        for b in range(k):
            assert sum((row[a].conjugate()*row[b] for row in v),C())==C(int(a==b))
    for row in v:
        q=[z.real*z.real+z.imag*z.imag for z in row]
        owners.append(max(range(k),key=lambda a:q[a]));delta+=sum(q)-max(q)
    return owners,delta


def fine_laws(v):
    m,k=v.shape;assignments=list(permutations(range(k)));basis=[];boson=[];labelled=[]
    for outputs in combinations_with_replacement(range(m),k):
        occupation=tuple(outputs.count(i) for i in range(m));factorial=math.prod(math.factorial(x) for x in occupation)
        amplitudes=[math.prod(v[i,a] for i,a in zip(outputs,p)) for p in assignments]
        basis.append(occupation);boson.append(abs(sum(amplitudes))**2/factorial)
        labelled.append(sum(abs(a)**2 for a in amplitudes)/factorial)
    b,d=np.array(boson),np.array(labelled)
    assert max(abs(b.sum()-1),abs(d.sum()-1))<1e-9
    assert len(basis)==math.comb(m+k-1,k)
    return basis,b,d


def pinch(v,owners):
    k=v.shape[1];pp=list(permutations(range(k)));n=len(pp);kernel=np.ones((n,n))-np.eye(n)
    effects=[v[np.array(owners)==g].conj().T@v[np.array(owners)==g] for g in range(k)]
    sectors=[];gram_sum=np.zeros((n,n),complex);distance=trace_norm=trace_sum=0.;minimum=0.
    for groups in product(range(k),repeat=k):
        gram=np.array([[math.prod(effects[g][a,b] for g,a,b in zip(groups,p,q)) for q in pp] for p in pp])
        gram=(gram+gram.conj().T)/2;gram_sum+=gram
        values,vectors=np.linalg.eigh(gram);minimum=min(minimum,float(values[0]));assert values[0]>-1e-9
        root=(vectors*np.sqrt(np.maximum(values,0)))@vectors.conj().T
        hermitian=root@kernel@root;hermitian=(hermitian+hermitian.conj().T)/2
        eigenvalues,eigenvectors=np.linalg.eigh(hermitian)
        assert sum(eigenvalues>1e-9)<=1
        positive=max(0.,float(eigenvalues[-1]));distance+=positive/n
        trace_norm+=float(abs(eigenvalues).sum())/(2*n);trace_sum+=float(eigenvalues.sum())/n
        inverse=(vectors*np.where(values>max(1e-30,values[-1]*1e-13),1/np.sqrt(np.maximum(values,1e-300)),0))@vectors.conj().T
        y=inverse@eigenvectors[:,-1]
        sectors.append({'groups':groups,'eigenvalues':eigenvalues.tolist(),
                        'rayleigh_real':y.real.tolist(),'rayleigh_imag':y.imag.tolist()})
    assert np.max(abs(gram_sum-np.eye(n)))<1e-8
    assert max(abs(distance-trace_norm),abs(trace_sum))<1e-8
    return distance,sectors,minimum,trace_sum


def exact_lower(v,owners,sectors):
    k=len(v[0]);pp=list(permutations(range(k)));n=len(pp)
    effects=[[[sum((row[a].conjugate()*row[b] for i,row in enumerate(v) if owners[i]==g),C())
               for b in range(k)] for a in range(k)] for g in range(k)]
    lower=F(0);witness=[]
    for record in sectors:
        groups=record['groups']
        gram=[[math.prod((effects[g][a][b] for g,a,b in zip(groups,p,q)),start=C(1)) for q in pp] for p in pp]
        y=[C(F.from_float(a),F.from_float(b)) for a,b in zip(record['rayleigh_real'],record['rayleigh_imag'])]
        gy=[sum((entry*z for entry,z in zip(row,y)),C()) for row in gram]
        den=sum((z.conjugate()*w for z,w in zip(y,gy)),C());assert den.imag==0 and den.real>=0
        total=sum(gy,C());num=total.real**2+total.imag**2-sum(z.real**2+z.imag**2 for z in gy)
        value=max(F(0),num/den.real) if den.real else F(0)
        lower+=value/n;witness.append({'groups':groups,'vector':y,'rayleigh_lower':value})
    return lower,witness


def main(output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();records=[];candidates=[]
    controls=[]
    for k in (2,3):
        v=np.eye(k,dtype=complex);distance,_,_,_=pinch(v,list(range(k)))
        assert distance<1e-12;controls.append({'control':'identity','k':k,'distance':distance})
    for t in (F(1,10),F(1,5),F(1,3)):
        c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        w=[[C(F(3,5)),C()],[C(F(4,5)),C()],[C(),C(F(3,5))],[C(),C(F(4,5))]]
        v=[[c*a+s*b,-s*a+c*b] for a,b in w];owners,delta=exact_domain(v)
        distance,_,_,_=pinch(np.array([[complex(z) for z in row] for row in v]),owners)
        assert abs(distance-float(delta-delta*delta/2))<1e-10
        controls.append({'control':'sharp_k2','t':t,'delta':delta,'distance':distance})
    with (output/'progress.jsonl').open('x') as progress:
        for m in (3,6,9):
            for seed in (20261201,20261202,20261203):
                for t in (F(1,40),F(1,5),F(1,2),F(1)):
                    u=frame(m,seed,t);v=[row[:3] for row in u];owners,delta=exact_domain(v)
                    array=np.array([[complex(z) for z in row] for row in u]);numeric=array[:,:3]
                    distance,sectors,minimum,trace=pinch(numeric,owners)
                    basis,b,d=fine_laws(numeric);tv=float(abs(b-d).sum()/2)
                    assert tv<=distance+1e-8 and distance<=F(5,6)+1e-8
                    reference=None;error=None
                    if seed==20261201 and t in (F(1,5),F(1,2)):
                        backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(array)))
                        backend.set_input_state(pcvl.BasicState([1]*3+[0]*(m-3)))
                        law=backend.prob_distribution();reference=[float(law.get(pcvl.BasicState(x),0)) for x in basis]
                        error=float(max(abs(np.array(reference)-b)));assert error<1e-10
                    lower=witness=None
                    if distance>float(delta)+1e-9:
                        lower,witness=exact_lower(v,owners,sectors)
                        candidates.append({'record':len(records),'certified':lower>delta,'lower_bound':lower,'delta':delta,'witness':witness})
                    record={'m':m,'seed':seed,'strength':t,'frame':v,'owners':owners,'delta':delta,
                            'pinched_distance':distance,'fine_tv':tv,'pinched_minus_delta':distance-float(delta),
                            'sectors':sectors,'min_gram_eigenvalue':minimum,'trace_residual':trace,
                            'fock_basis':basis,'bosonic_probabilities':b.tolist(),'distinguishable_probabilities':d.tolist(),
                            'perceval_probabilities':reference,'perceval_max_error':error}
                    records.append(record);progress.write(json.dumps(record,default=encode)+'\n');progress.flush()
    certified=[c['record'] for c in candidates if c['certified']]
    summary={'status':'EXACT_COUNTEREXAMPLE_TO_STRONGER_LEMMA' if certified else 'FINITE_ONLY_NO_CERTIFIED_REFUTATION',
             'circuits':len(records),'controls':len(controls),'perceval_checks':sum(r['perceval_max_error'] is not None for r in records),
             'numeric_candidates':len(candidates),'certified_counterexample_indices':certified,
             'max_pinched_minus_delta':max(r['pinched_minus_delta'] for r in records),
             'max_fine_minus_pinched':max(r['fine_tv']-r['pinched_distance'] for r in records),
             'max_perceval_error':max(r['perceval_max_error'] or 0 for r in records),
             'physical_shots':0,'runtime_seconds':time.monotonic()-start,
             'numeric_semantics':'FLOAT64_NOT_INTERVAL_CERTIFIED; exact lower witnesses only on numeric candidates'}
    assert len(records)==36 and summary['perceval_checks']==6
    (output/'raw.json').write_text(json.dumps({'summary':summary,'controls':controls,'records':records,'candidates':candidates},default=encode,separators=(',',':'))+'\n')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
