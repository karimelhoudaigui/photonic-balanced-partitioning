"""P35: validate a known exact classical mean-objective baseline, no training."""
import argparse
from dataclasses import asdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
import json
import math
from pathlib import Path
import random
import time
import numpy as np
import perceval as pcvl
from photonic_balanced_partitioning.photonic.threshold_marginals import (
    GaussianRational as G, ThresholdMarginals, encode_binary_frame,
)


def fraction(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}


def gaussian(z):return {'real':fraction(z.real),'imag':fraction(z.imag)}


def rational_unitary(m,seed):
    rng=random.Random(seed);u=[[G(int(i==j)) for j in range(m)] for i in range(m)]
    for _ in range(3*m):
        i,j=rng.sample(range(m),2);a,b=u[i][:],u[j][:]
        ca,sa,den=rng.choice([(3,4,5),(5,12,13),(8,15,17)])
        c,s=F(ca,den),F(sa,den)*rng.choice([-1,1])
        if rng.randrange(2):
            u[i]=[c*x+G(0,s)*y for x,y in zip(a,b)]
            u[j]=[G(0,s)*x+c*y for x,y in zip(a,b)]
        else:
            u[i]=[c*x-s*y for x,y in zip(a,b)];u[j]=[s*x+c*y for x,y in zip(a,b)]
    return u


def complete_exact_law(frame,basis):
    n=len(frame[0]);law=[]
    for t in basis:
        outputs=[i for i,count in enumerate(t) for _ in range(count)];permanent=G()
        for assignment in permutations(range(n)):
            term=G(1)
            for i,a in zip(outputs,assignment):term=term*frame[i][a]
            permanent=permanent+term
        law.append((permanent.real**2+permanent.imag**2)/math.prod(math.factorial(x) for x in t))
    assert sum(law)==1 and min(law)>=0
    return law


def main(output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();records=[]
    dimensions=[(4,2),(4,4),(6,3)]*2+[(4,2),(4,4),(6,3),(8,4),(4,4),(6,3)]
    for index,(m,n) in enumerate(dimensions):
        seed=20261122+index;exact=index<6;before=time.monotonic()
        if exact:
            unitary=rational_unitary(m,seed);frame=[row[:n] for row in unitary]
            u=np.array([[complex(z) for z in row] for row in unitary])
        else:
            rng=np.random.default_rng(seed);z=rng.normal(size=(m,m))+1j*rng.normal(size=(m,m))
            u,_=np.linalg.qr(z);frame=encode_binary_frame(u[:,:n])
        evaluator=ThresholdMarginals(frame,check_orthonormal=exact)
        means=evaluator.click_means();pairs=evaluator.pair_moments()
        q=[[F(((i+1)*(j+1)+seed)%11-5) for j in range(m)] for i in range(m)]
        energy=evaluator.qubo_expectation(q)
        backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
        backend.set_input_state(pcvl.BasicState([1]*n+[0]*(m-n)));distribution=backend.prob_distribution()
        basis=sorted(tuple(outputs.count(i) for i in range(m))
                     for outputs in combinations_with_replacement(range(m),n))
        reference=[float(distribution.get(pcvl.BasicState(t),0.)) for t in basis]
        clicks=np.array(basis)>0;values=np.array(reference)
        mean_ref=values@clicks;pair_ref=clicks.T@(values[:,None]*clicks)
        energy_ref=sum(p*sum(q[i][j] for i in range(m) for j in range(m) if t[i]>0 and t[j]>0)
                       for t,p in zip(basis,reference))
        mean_error=max(abs(float(x)-y) for x,y in zip(means,mean_ref))
        pair_error=max(abs(float(pairs[i][j])-pair_ref[i,j]) for i in range(m) for j in range(m))
        energy_error=abs(float(energy)-float(energy_ref))
        assert max(mean_error,pair_error,energy_error,abs(sum(reference)-1))<1e-10
        exact_law=None
        if exact:
            exact_law=complete_exact_law(frame,basis)
            for i in range(m):
                assert means[i]==sum(p for t,p in zip(basis,exact_law) if t[i]>0)
                for j in range(m):assert pairs[i][j]==sum(p for t,p in zip(basis,exact_law) if t[i]>0 and t[j]>0)
            exact_energy=sum(p*sum(q[i][j] for i in range(m) for j in range(m) if t[i]>0 and t[j]>0)
                             for t,p in zip(basis,exact_law))
            assert energy==exact_energy
        record={'m':m,'photons':n,'seed':seed,'exact_physical_frame':exact,
            'input_semantics':evaluator.input_semantics,'frame':[[gaussian(z) for z in row] for row in frame],
            'unitary_real':u.real.tolist(),'unitary_imag':u.imag.tolist(),
            'input_float_orthogonality_residual':float(np.max(abs(u.conj().T@u-np.eye(m)))),
            'click_means':[fraction(x) for x in means],
            'pair_moments':[[fraction(x) for x in row] for row in pairs],
            'qubo':[[fraction(x) for x in row] for row in q],'qubo_expectation':fraction(energy),
            'fock_basis':basis,'perceval_probabilities':reference,
            'exact_fock_probabilities':[fraction(x) for x in exact_law] if exact_law is not None else None,
            'max_perceval_mean_error':float(mean_error),'max_perceval_pair_error':float(pair_error),
            'perceval_energy_error':float(energy_error),'work':asdict(evaluator.stats),
            'wall_seconds_including_reference':time.monotonic()-before}
        records.append(record)
    payload={'status':'FINITE_BASELINE_CHECKS_PASS','known_algorithm':True,'records':records,
        'physical_shots':0,'runtime_seconds':time.monotonic()-start,
        'non_claims':['No optimizer or quantum advantage','No full-output sampler from the marginal DP',
          'Encoded binary frames are formal polynomial inputs, not certified physical unitaries',
          'No independent fresh-agent review of this coordinator implementation']}
    (output/'raw.json').write_text(json.dumps(payload,separators=(',',':'))+'\n')
    summary={'status':payload['status'],'circuits':12,'exact_rational_circuits':6,'perceval_circuits':12,
        'physical_shots':0,'runtime_seconds':payload['runtime_seconds'],
        'max_mean_error':max(r['max_perceval_mean_error'] for r in records),
        'max_pair_error':max(r['max_perceval_pair_error'] for r in records),
        'max_energy_error':max(r['perceval_energy_error'] for r in records)}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);main(parser.parse_args().output)
