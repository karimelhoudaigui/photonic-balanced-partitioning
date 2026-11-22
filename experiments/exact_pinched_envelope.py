"""Exact auxiliary-envelope falsifier; not a measured-TV or linear-bound claim."""
import argparse
from fractions import Fraction as F
from itertools import permutations,product
import importlib.util
import json
from pathlib import Path
import sys
import time
import numpy as np
import perceval as pcvl


def rayleigh(weights,r):
    y=[1/(r+p) for p in weights]
    py=[p*z for p,z in zip(weights,y)]
    numerator=sum(py)**2-sum(z*z for z in py)
    denominator=sum(p*z*z for p,z in zip(weights,y))
    assert denominator>0
    return numerator/denominator,y,numerator,denominator


def encode(x):
    if isinstance(x,F):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
    raise TypeError(type(x).__name__)


def run(output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();e,d=F(3,25),F(19,25)
    assert d+2*e==1 and d>e
    p=[[d if a==g else e for a in range(3)] for g in range(3)]
    pp=list(permutations(range(3)));sectors=[];total=F(0);counts={1:0,2:0,3:0}
    for groups in product(range(3),repeat=3):
        weights=[np.prod([p[g][a] for g,a in zip(groups,perm)]) for perm in pp]
        # numpy.prod of object Fractions is exact; ensure no coercion occurred.
        assert all(isinstance(w,F) for w in weights)
        kind=len(set(groups));counts[kind]+=1
        if kind==1:
            y=[F(1)]*6;num=sum(weights)**2-sum(w*w for w in weights);den=sum(weights);value=num/den
            assert value==5*d*e*e
        else:
            r=F(27,250) if kind==2 else F(7,50)
            value,y,num,den=rayleigh(weights,r)
        total+=value/6
        sectors.append({'groups':groups,'weights':weights,'vector':y,'numerator':num,'denominator':den,'lower':value})
    assert counts=={1:3,2:18,3:6}
    repeated=rayleigh([d*d*e]*2+[d*e*e]*2+[e**3]*2,F(27,250))[0]
    distinct=rayleigh([d**3]+[d*e*e]*3+[e**3]*2,F(7,50))[0]
    grouped=F(5,2)*d*e*e+3*repeated+distinct;assert total==grouped
    delta=6*e;curved=delta-delta*delta/2;assert curved==F(288,625)
    assert total>curved and total<delta
    # A separate physical full-law sanity check, not a proof leaf.
    fourier=np.exp(2j*np.pi*np.outer(np.arange(3),np.arange(3))/3)/np.sqrt(3)
    v=np.vstack([fourier*np.sqrt(np.array([float(x) for x in row])) for row in p])
    assert np.linalg.norm(v.conj().T@v-np.eye(3))<1e-12
    rng=np.random.default_rng(20261220);completion=rng.normal(size=(9,6))+1j*rng.normal(size=(9,6))
    u,_=np.linalg.qr(np.column_stack((v,completion)))
    for a in range(3):
        phase=np.vdot(u[:,a],v[:,a]);u[:,a]*=phase/abs(phase)
    assert np.max(abs(u[:,:3]-v))<1e-12
    spec=importlib.util.spec_from_file_location('p38_physical_probe',Path('experiments/phase3_pinching_probe.py'))
    core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core;spec.loader.exec_module(core)
    owners=[g for g in range(3) for _ in range(3)];pinched,_,_,_=core.pinch(v,owners)
    basis,b,dist=core.fine_laws(v)
    backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
    backend.set_input_state(pcvl.BasicState([1]*3+[0]*6));law=backend.prob_distribution()
    reference=[float(law.get(pcvl.BasicState(t),0)) for t in basis]
    error=float(max(abs(np.array(reference)-b)));assert error<1e-10 and len(basis)==165
    fine_tv=float(abs(b-dist).sum()/2);assert fine_tv<=pinched+1e-10 and float(total)<=pinched+1e-10
    summary={'status':'EXACT_COUNTEREXAMPLE_TO_CURVED_PINCHED_ENVELOPE','delta':delta,'curved_envelope':curved,
             'exact_rayleigh_lower':total,'exact_gap':total-curved,'physical_frame_modes':9,'photons':3,
             'pinched_distance_for_display':pinched,'fine_tv_for_display':fine_tv,'perceval_max_error':error,
             'physical_shots':0,'runtime_seconds':time.monotonic()-start,
             'non_claims':['Does not refute D_pinched<=delta','Does not refute measured-TV<=delta or its curved variant',
                           'Post-hoc auxiliary counterexample, no novelty or optimization advantage']}
    raw={'summary':summary,'p':p,'sectors':sectors,'grouped_lower':grouped,
         'frame_real':v.real.tolist(),'frame_imag':v.imag.tolist(),'unitary_real':u.real.tolist(),'unitary_imag':u.imag.tolist(),
         'fock_basis':basis,'bosonic_probabilities':b.tolist(),'distinguishable_probabilities':dist.tolist(),'perceval_probabilities':reference}
    (output/'raw.json').write_text(json.dumps(raw,default=encode,separators=(',',':'))+'\n')
    (output/'summary.json').write_text(json.dumps(summary,default=encode,indent=2)+'\n')
    print(json.dumps(summary,default=encode))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);run(p.parse_args().output)
