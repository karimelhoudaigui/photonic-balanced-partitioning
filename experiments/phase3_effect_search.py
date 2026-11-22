"""P38b compact-domain falsification, with exact post-checks on any candidate."""
import argparse
from fractions import Fraction as F
from itertools import permutations, product
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.optimize import minimize
from photonic_balanced_partitioning.photonic.threshold_marginals import GaussianRational as C

PP=np.array(list(permutations(range(3))));K=np.ones((6,6))-np.eye(6);GROUPS=list(product(range(3),repeat=3))
PAIRS=((0,1),(0,2),(1,2))


def encode(x):
    if isinstance(x,F):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
    if isinstance(x,C):return {'real':encode(x.real),'imag':encode(x.imag)}
    if isinstance(x,np.generic):return x.item()
    raise TypeError(type(x).__name__)


def decode(x):
    effects=[]
    for chunk in (x[:9],x[9:]):
        e=np.diag(chunk[:3]).astype(complex)
        for (a,b),r,i in zip(PAIRS,chunk[3::2],chunk[4::2]):e[a,b]=r+1j*i;e[b,a]=r-1j*i
        effects.append(e)
    return np.array([*effects,np.eye(3)-effects[0]-effects[1]])


def constraints(e):
    eigen=np.concatenate([np.linalg.eigvalsh(x) for x in e])
    dominant=np.array([e[g,g,g].real-e[g,a,a].real for g in range(3) for a in range(3) if a!=g])
    return eigen,dominant,3-sum(e[g,g,g].real for g in range(3))


def distance(e,vectors=False):
    value=0.;witness=[]
    for groups in GROUPS:
        gram=np.ones((6,6),complex)
        for j,g in enumerate(groups):gram*=e[g][PP[:,j,None],PP[None,:,j]]
        gram=(gram+gram.conj().T)/2;ev,u=np.linalg.eigh(gram)
        root=(u*np.sqrt(np.maximum(ev,0)))@u.conj().T;h=root@K@root;h=(h+h.conj().T)/2
        vals,w=np.linalg.eigh(h);value+=max(0.,float(vals[-1]))/6
        if vectors:
            inverse=(u*np.where(ev>max(1e-30,ev[-1]*1e-13),1/np.sqrt(np.maximum(ev,1e-300)),0))@u.conj().T
            y=inverse@w[:,-1];witness.append((groups,y))
    return value,witness


def exact_valid(e):
    for g,a in enumerate(e):
        if any(a[i][i].imag or a[i][i].real<0 for i in range(3)):return False
        if any(a[g][g].real<a[i][i].real for i in range(3)):return False
        for i,j in PAIRS:
            if a[i][i].real*a[j][j].real-a[i][j].real**2-a[i][j].imag**2<0:return False
        determinant=C()
        for p in permutations(range(3)):
            sign=(-1)**sum(p[i]>p[j] for i,j in PAIRS)
            determinant+=sign*math.prod((a[i][p[i]] for i in range(3)),start=C(1))
        if determinant.imag or determinant.real<0:return False
    return True


def exact_witness(e):
    numeric=np.array([[[complex(z) for z in row] for row in a] for a in e]);_,vectors=distance(numeric,True)
    lower=F(0);witness=[]
    for groups,yfloat in vectors:
        gram=[[math.prod((e[g][a][b] for g,a,b in zip(groups,p,q)),start=C(1)) for q in PP] for p in PP]
        y=[C(F.from_float(float(z.real)),F.from_float(float(z.imag))) for z in yfloat]
        gy=[sum((a*b for a,b in zip(row,y)),C()) for row in gram]
        denominator=sum((a.conjugate()*b for a,b in zip(y,gy)),C());assert denominator.imag==0 and denominator.real>=0
        total=sum(gy,C());numerator=total.real**2+total.imag**2-sum(z.real**2+z.imag**2 for z in gy)
        rayleigh=max(F(0),numerator/denominator.real) if denominator.real else F(0)
        lower+=rayleigh/6;witness.append({'groups':groups,'vector':y,'lower':rayleigh})
    return lower,witness


def certify(x,target):
    first=[]
    for chunk in (x[:9],x[9:]):
        a=[[C() for _ in range(3)] for _ in range(3)]
        for i in range(3):a[i][i]=C(F.from_float(float(chunk[i])))
        for (i,j),r,s in zip(PAIRS,chunk[3::2],chunk[4::2]):
            a[i][j]=C(F.from_float(float(r)),F.from_float(float(s)));a[j][i]=a[i][j].conjugate()
        first.append(a)
    original=[*first,[[C(int(i==j))-first[0][i][j]-first[1][i][j] for j in range(3)] for i in range(3)]]
    for power in range(30,-1,-1):
        eps=F(1,2**power)
        e=[[( [(1-eps)*original[g][i][j]+eps*C((1-target/3 if i==g else target/6) if i==j else 0)
                for j in range(3)] ) for i in range(3)] for g in range(3)]
        if exact_valid(e):break
    else:raise ArithmeticError('Strict reference must give a valid repair')
    assert all(sum((e[g][i][j] for g in range(3)),C())==C(int(i==j)) for i in range(3) for j in range(3))
    delta=3-sum(e[g][g][g].real for g in range(3));lower,witness=exact_witness(e)
    return {'repair_epsilon':eps,'effects':e,'delta':delta,'rayleigh_lower':lower,'certified':lower>delta,'witness':witness}


def run(output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();calls=0;cells=[];candidates=[]
    c,s=F(12,13),F(5,13);u=[[C(c),C(-s),C()],[C(s),C(c),C()],[C(),C(),C(1)]]
    control=[[[row[a].conjugate()*row[b] for b in range(3)] for a in range(3)] for row in u]
    assert exact_valid(control);control_lower,_=exact_witness(control);control_target=2*c*c*s*s
    assert 0<=control_lower<=control_target and float(control_target-control_lower)<1e-10
    with (output/'evaluations.jsonl').open('x') as trace:
        for target in (F(1,5),F(3,5)):
            for seed in (20261210,20261211):
                rng=np.random.default_rng(seed);x=np.zeros(18)
                for g in range(2):
                    x[9*g:9*g+3]=[float(1-target/3 if i==g else target/6) for i in range(3)]
                    x[9*g+3:9*g+9]=rng.normal(scale=.004,size=6)
                best=None;before=calls
                def objective(parameters):
                    nonlocal calls,best
                    calls+=1
                    if calls>4000:raise RuntimeError('Declared4000-call budget exceeded')
                    e=decode(parameters);eig,dom,delta=constraints(e);near=min(eig)>=-1e-8 and min(dom)>=-1e-8
                    d=distance(e)[0] if min(eig)>=-1e-8 else None
                    score=-d if d is not None else 100+1000*float(np.minimum(eig,0)@np.minimum(eig,0))
                    row={'call':calls,'seed':seed,'target':str(target),'parameters':parameters.tolist(),
                         'effect_eigenvalues':eig.tolist(),'dominance_margins':dom.tolist(),'delta':delta,
                         'pinched_distance':d,'near_feasible':bool(near),'objective':score}
                    trace.write(json.dumps(row)+'\n');trace.flush()
                    if near and (best is None or d-delta>best['excess']):best={'parameters':parameters.copy(),'excess':d-delta,'distance':d,'delta':delta,'call':calls}
                    return score
                result=minimize(objective,x,method='SLSQP',constraints=[
                    {'type':'ineq','fun':lambda a:np.concatenate(constraints(decode(a))[:2])},
                    {'type':'eq','fun':lambda a:constraints(decode(a))[2]-float(target)}],
                    options={'maxiter':25,'ftol':1e-9,'eps':2e-6})
                if best and best['excess']>1e-8:
                    candidates.append({'cell':len(cells),'certificate':certify(best['parameters'],target)})
                cells.append({'target':str(target),'seed':seed,'calls':calls-before,'success':bool(result.success),
                              'message':str(result.message),'iterations':int(result.nit),'parameters':result.x.tolist(),
                              'best':{**best,'parameters':best['parameters'].tolist()} if best else None})
    certified=[c['cell'] for c in candidates if c['certificate']['certified']]
    summary={'status':'EXACT_STRONGER_LEMMA_REFUTATION' if certified else 'BOUNDED_SEARCH_NO_CERTIFIED_REFUTATION',
             'cells':len(cells),'objective_calls':calls,'numeric_candidate_cells':len(candidates),
             'certified_counterexample_cells':certified,'max_near_feasible_excess':max(c['best']['excess'] for c in cells if c['best']),
             'solver_successes':sum(c['success'] for c in cells),'physical_shots':0,'new_fock_simulations':0,
             'runtime_seconds':time.monotonic()-start,'non_claims':['No global optimality','No measured-TV refutation from stronger lemma','No graph advantage or hardware']}
    (output/'raw.json').write_text(json.dumps({'summary':summary,'cells':cells,'candidates':candidates,
        'control_exact_lower':control_lower,'control_target':control_target},default=encode,separators=(',',':'))+'\n')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
