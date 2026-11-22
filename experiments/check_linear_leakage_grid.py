"""Independent physical controls for the finite P36 grid, not a general proof."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import perceval as pcvl


def main(source,output):
    raw=json.loads(source.read_text());records=raw['records'];assert len(records)==256
    selected=[];collective=[];maxima={'normalization':0.,'tv_recompute':0.,'delta_recompute':0.}
    for row in records:
        m,k=row['m'],row['k'];basis=raw['full_fock_bases'][f'{m},{k}']
        assert len(basis)==math.comb(m+k-1,k) and len({tuple(t) for t in basis})==len(basis)
        assert all(sum(t)==k and all(isinstance(x,int) and x>=0 for x in t) for t in basis)
        u=np.array(row['unitary_real'])+1j*np.array(row['unitary_imag'])
        assert np.max(abs(u.conj().T@u-np.eye(m)))<1e-12
        b=np.array(row['bosonic_probabilities']);d=np.array(row['distinguishable_probabilities'])
        assert len(b)==len(d)==len(basis) and min(b.min(),d.min())>=0
        q=abs(u[:,:k])**2;q[np.arange(m),np.argmax(q,axis=1)]=0.
        delta=float(q.sum());tv=float(abs(b-d).sum()/2)
        maxima['normalization']=max(maxima['normalization'],abs(b.sum()-1),abs(d.sum()-1))
        maxima['tv_recompute']=max(maxima['tv_recompute'],abs(tv-row['tv']))
        maxima['delta_recompute']=max(maxima['delta_recompute'],abs(delta-row['delta']))
        assert max(maxima.values())<1e-9
        if row['family']=='collective_rank_one':
            assert m==k
            c=np.exp(1j*row['strength'])-1
            amplitude=sum(math.factorial(m)//math.factorial(m-s)*(c/m)**s for s in range(m+1))
            diagonal=abs(1+c/m)**2;off=abs(c/m)**2
            pd=sum(math.factorial(m)//math.factorial(m-s)*(diagonal-off)**(m-s)*off**s for s in range(m+1))
            index=basis.index([1]*m)
            eb=abs(b[index]-abs(amplitude)**2);ed=abs(d[index]-pd)
            assert max(eb,ed)<1e-12
            collective.append(dict(m=m,strength=row['strength'],bosonic_cf_error=float(eb),distinguishable_cf_error=float(ed)))
        chosen=(row['family']=='collective_rank_one' and row['strength']==.5) or (
            m==2*k and row['seed']==2026112200+100*m+4 and row['strength']==.15)
        if not chosen:continue
        backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
        backend.set_input_state(pcvl.BasicState([1]*k+[0]*(m-k)))
        reference=backend.prob_distribution()
        error=max(abs(pb-reference.get(pcvl.BasicState(t),0.)) for t,pb in zip(basis,b))
        assert error<1e-11
        selected.append(dict(m=m,k=k,family=row['family'],seed=row['seed'],strength=row['strength'],perceval_error=float(error)))
    assert len(selected)==12 and len(collective)==16
    payload={'status':'FINITE_GRID_PHYSICS_CHECKS_PASS_GENERAL_CONJECTURE_OPEN',
        'raw_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':256,'raw_checks':maxima,
        'perceval_checks':selected,'collective_closed_formula_checks':collective,'physical_shots':0,
        'non_claim':'No proof of TV<=delta, no independent fresh-agent audit, no interval or advantage result.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as f:json.dump(payload,f,indent=2)
    print(json.dumps({'status':payload['status'],'perceval_circuits':12,'collective_checks':16,
                      'max_perceval_error':max(r['perceval_error'] for r in selected)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);a=parser.parse_args();main(a.source,a.output)
