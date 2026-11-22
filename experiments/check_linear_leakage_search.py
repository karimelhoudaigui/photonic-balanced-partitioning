"""Post-run audit of every saved search score and all eight pairs of winners."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import perceval as pcvl
from phase3_linear_leakage_adversarial import ckm, qr_frame, evaluator


def main(source,output):
    raw=json.loads((source/'raw.json').read_text());groups={}
    with (source/'evaluations.jsonl').open() as stream:
        for line in stream:
            row=json.loads(line);key=(row['family'],row['seed'],row['target'])
            cell=groups.setdefault(key,{'calls':0,'excess':-math.inf,'score':-math.inf})
            cell['calls']+=1
            assert row['evaluation']==cell['calls']
            assert abs(row['excess']-(row['tv']-min(1.,row['delta'])))<1e-14
            assert abs(row['score']-(row['excess']-10*(row['delta']-row['target'])**2))<1e-14
            assert max(row['normalization_error'],row['orthogonality_residual'])<1e-11
            cell['excess']=max(cell['excess'],row['excess']);cell['score']=max(cell['score'],row['score'])
    expected={(f,s,t) for f in ['three_mode','six_mode'] for s in [20261140,20261141] for t in [.25,.75]}
    assert set(groups)==expected and sum(c['calls'] for c in groups.values())==raw['total_evaluations']<=18000
    checks=[]
    for result in raw['results']:
        key=(result['family'],result['seed'],result['target']);cell=groups[key]
        assert cell['calls']==result['calls']
        assert cell['excess']==result['best_excess']['excess'] and cell['score']==result['best_penalized_score']['score']
        build=ckm if result['family']=='three_mode' else qr_frame
        for kind in ['best_excess','best_penalized_score']:
            record=result[kind];v=build(record['parameters']);m=len(v)
            delta,tv,_,_,pb,pd=evaluator(m)[0](v)
            assert max(abs(delta-record['delta']),abs(tv-record['tv']))<1e-12
            # Completing QR may change occupied column phases; single-photon
            # Fock input probabilities are invariant under those column phases.
            u=np.linalg.qr(v,mode='complete')[0]
            overlap=v.conj().T@u[:,:3]
            assert np.max(abs(overlap-np.diag(np.diag(overlap))))<1e-12
            assert np.max(abs(abs(np.diag(overlap))-1))<1e-12
            backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
            backend.set_input_state(pcvl.BasicState([1]*3+[0]*(m-3)))
            reference=backend.prob_distribution()
            lists=evaluator(m)[1];states=[tuple(list(t).count(i) for i in range(m)) for t in lists]
            error=max(abs(p-reference.get(pcvl.BasicState(t),0.)) for p,t in zip(pb,states))
            assert error<1e-11
            checks.append({'family':key[0],'seed':key[1],'target':key[2],'winner':kind,
                'delta':delta,'tv':tv,'perceval_error':float(error),'perceval_outcome_count':len(states)})
    assert len(checks)==16
    payload={'status':'SEARCH_TRACE_AND_WINNER_PHYSICS_VERIFIED_GENERAL_CONJECTURE_OPEN',
        'evaluations':raw['total_evaluations'],'all_search_cells':len(groups),
        'winner_checks':checks,'physical_shots':0,
        'non_claim':'Post-run audit of all stored winners; no universal theorem or statistical guarantee.'}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as f:json.dump(payload,f,indent=2)
    print(json.dumps({'status':payload['status'],'evaluations':raw['total_evaluations'],
        'perceval_checks':16,'max_perceval_error':max(r['perceval_error'] for r in checks)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);a=parser.parse_args();main(a.source,a.output)
