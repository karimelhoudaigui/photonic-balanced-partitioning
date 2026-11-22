"""Bounded counterexample search in two genuinely phase-sensitive frame classes."""
import argparse
from itertools import combinations_with_replacement, permutations
import json
import math
from pathlib import Path
import time
import numpy as np
from scipy.optimize import differential_evolution, minimize


def ckm(parameters):
    a,b,c,phase=parameters;c12,s12=np.cos(a),np.sin(a);c13,s13=np.cos(b),np.sin(b)
    c23,s23=np.cos(c),np.sin(c);z=np.exp(1j*phase)
    return np.array([[c12*c13,s12*c13,s13/z],
        [-s12*c23-c12*s23*s13*z,c12*c23-s12*s23*s13*z,s23*c13],
        [s12*s23-c12*c23*s13*z,-c12*s23-s12*c23*s13*z,c23*c13]],complex)


def qr_frame(parameters):
    z=np.asarray(parameters);base=np.zeros((6,3),complex)
    for a in range(3):base[2*a:2*a+2,a]=1/math.sqrt(2)
    candidate=base+.4*(z[:18].reshape(6,3)+1j*z[18:].reshape(6,3))
    return np.linalg.qr(candidate)[0]


def evaluator(m):
    outputs=np.array(list(combinations_with_replacement(range(m),3)))
    assignments=np.array(list(permutations(range(3))))
    factorials=np.array([math.prod(math.factorial(list(row).count(i)) for i in range(m)) for row in outputs])
    def evaluate(v):
        paths=np.prod(v[outputs[:,None,:],assignments[None,:,:]],axis=2)
        b=abs(paths.sum(axis=1))**2/factorials;d=(abs(paths)**2).sum(axis=1)/factorials
        orth=float(np.max(abs(v.conj().T@v-np.eye(3))))
        norm=float(max(abs(b.sum()-1),abs(d.sum()-1)))
        assert max(orth,norm)<1e-11
        q=abs(v)**2;q[np.arange(m),np.argmax(q,axis=1)]=0
        delta=float(q.sum());tv=float(abs(b-d).sum()/2)
        return delta,tv,orth,norm,b,d
    return evaluate,outputs


def main(output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();total=0;results=[]
    with (output/'evaluations.jsonl').open('x') as trace:
        for family,builder,m in [('three_mode',ckm,3),('six_mode',qr_frame,6)]:
            evaluate,outputs=evaluator(m)
            for seed in [20261140,20261141]:
                for target in [.25,.75]:
                    best_excess=None;best_score=None;calls=0
                    def objective(parameters):
                        nonlocal total,calls,best_excess,best_score
                        total+=1;calls+=1
                        if total>18000:raise RuntimeError('Global evaluation cap exceeded')
                        v=builder(parameters);delta,tv,orth,norm,b,d=evaluate(v)
                        excess=tv-min(1.,delta);score=excess-10*(delta-target)**2
                        row={'family':family,'seed':seed,'target':target,'evaluation':calls,
                            'parameters':np.asarray(parameters).tolist(),'delta':delta,'tv':tv,
                            'excess':excess,'score':score,'orthogonality_residual':orth,'normalization_error':norm}
                        trace.write(json.dumps(row,separators=(',',':'))+'\n')
                        if calls%100==0:trace.flush()
                        if best_excess is None or excess>best_excess['excess']:
                            best_excess=dict(row,frame_real=v.real.tolist(),frame_imag=v.imag.tolist(),
                                bosonic_probabilities=b.tolist(),distinguishable_probabilities=d.tolist())
                        if best_score is None or score>best_score['score']:best_score=row
                        return -score
                    if family=='three_mode':
                        result=differential_evolution(objective,[(0,np.pi/2)]*3+[(0,2*np.pi)],
                            popsize=6,maxiter=60,tol=0,atol=0,polish=False,workers=1,
                            rng=np.random.default_rng(seed),updating='immediate')
                    else:
                        x=np.random.default_rng(seed).normal(0,.2,36)
                        result=minimize(objective,x,method='Nelder-Mead',
                            options={'maxfev':3000,'xatol':1e-10,'fatol':1e-12})
                    results.append({'family':family,'seed':seed,'target':target,'calls':calls,
                        'optimizer_terminated_successfully':bool(result.success),'optimizer_message':str(result.message),
                        'best_excess':best_excess,'best_penalized_score':best_score,'basis_output_lists':outputs.tolist()})
                    trace.flush()
    candidates=[r for r in results if r['best_excess']['excess']>1e-8]
    payload={'status':'CANDIDATE_REQUIRES_INDEPENDENT_CHECK' if candidates else 'BOUNDED_SEARCH_NO_REFUTATION',
        'results':results,'total_evaluations':total,'runtime_seconds':time.monotonic()-start,
        'physical_shots':0,'general_conjecture':'OPEN','candidate_count':len(candidates),
        'non_claims':['No proof from failed search','No graph optimization or quantum advantage','No interval certification']}
    (output/'raw.json').write_text(json.dumps(payload,indent=2)+'\n')
    summary={k:payload[k] for k in ['status','total_evaluations','runtime_seconds','physical_shots','candidate_count']}
    summary['largest_excess']=max(r['best_excess']['excess'] for r in results)
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);main(parser.parse_args().output)
