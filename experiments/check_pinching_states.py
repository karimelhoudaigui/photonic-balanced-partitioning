"""P38 self-review by explicit tensor-sector density matrices, no Gram square roots."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import importlib.util
from itertools import permutations, product
import json
import math
from pathlib import Path
import sys
import time
import numpy as np


def fraction(x):return F(int(x['numerator']),int(x['denominator']))


def exact_frame(record):
    v=[[(fraction(z['real']),fraction(z['imag'])) for z in row] for row in record['frame']]
    for a in range(3):
        for b in range(3):
            real=sum(x[a][0]*x[b][0]+x[a][1]*x[b][1] for x in v)
            imag=sum(x[a][0]*x[b][1]-x[a][1]*x[b][0] for x in v)
            assert real==int(a==b) and imag==0
    delta=F(0);owners=[]
    for row in v:
        probabilities=[a*a+b*b for a,b in row];g=max(range(3),key=lambda a:probabilities[a])
        owners.append(g);delta+=sum(probabilities)-probabilities[g]
    assert delta==fraction(record['delta']) and owners==record['owners']
    return np.array([[complex(float(a),float(b)) for a,b in row] for row in v])


def check(raw_path,output):
    output.mkdir(parents=True,exist_ok=False);start=time.monotonic();raw=json.loads(raw_path.read_text())
    pp=list(permutations(range(3)));records=[];seen=set();prob_error=pinch_error=trace_error=0.
    for record in raw['records']:
        m=record['m'];seed=record['seed'];strength=fraction(record['strength']);seen.add((m,seed,strength))
        v=exact_frame(record);owners=record['owners'];blocks=defaultdict(list);b=defaultdict(float);d=defaultdict(float)
        for outputs in product(range(m),repeat=3):
            amplitudes=np.array([math.prod(v[i,a] for i,a in zip(outputs,p)) for p in pp])
            blocks[tuple(owners[i] for i in outputs)].append(amplitudes)
            occupation=tuple(outputs.count(i) for i in range(m))
            b[occupation]+=float(abs(amplitudes.sum())**2/6)
            d[occupation]+=float((abs(amplitudes)**2).sum()/6)
        trace_distance=trace=0.;largest_block=0
        for block in blocks.values():
            a=np.array(block);summed=a.sum(axis=1);difference=(np.outer(summed,summed.conj())-a@a.conj().T)/6
            values=np.linalg.eigvalsh((difference+difference.conj().T)/2)
            trace_distance+=float(abs(values).sum()/2);trace+=float(values.sum());largest_block=max(largest_block,len(block))
        bp=np.array([b[tuple(t)] for t in record['fock_basis']]);dp=np.array([d[tuple(t)] for t in record['fock_basis']])
        error=max(float(max(abs(bp-record['bosonic_probabilities']))),float(max(abs(dp-record['distinguishable_probabilities']))))
        prob_error=max(prob_error,error);pinch_error=max(pinch_error,abs(trace_distance-record['pinched_distance']))
        trace_error=max(trace_error,abs(trace));assert max(error,abs(trace),abs(trace_distance-record['pinched_distance']))<1e-9
        assert max(abs(bp.sum()-1),abs(dp.sum()-1))<1e-9
        tv=float(abs(bp-dp).sum()/2);assert abs(tv-record['fine_tv'])<1e-10 and tv<=trace_distance+1e-9
        if record['perceval_probabilities'] is not None:
            assert max(abs(bp-record['perceval_probabilities']))<1e-10
        records.append({'m':m,'seed':seed,'strength':str(strength),'direct_pinched_trace_distance':trace_distance,
                        'fine_tv':tv,'max_probability_error':error,'largest_tensor_sector_dimension':largest_block})
    expected={(m,s,t) for m in (3,6,9) for s in (20261201,20261202,20261203) for t in (F(1,40),F(1,5),F(1,2),F(1))}
    assert seen==expected and len(records)==36
    assert [json.loads(x) for x in (raw_path.parent/'progress.jsonl').read_text().splitlines()]==raw['records']
    # Exercise the previously untriggered exact witness branch on known sharp k2 values.
    source=Path('experiments/phase3_pinching_probe.py');spec=importlib.util.spec_from_file_location('p38_frozen_probe',source)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    witnesses=[]
    for control in raw['controls']:
        if control['control']!='sharp_k2':continue
        t=fraction(control['t']);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);C=module.C
        w=[[C(F(3,5)),C()],[C(F(4,5)),C()],[C(),C(F(3,5))],[C(),C(F(4,5))]]
        v=[[c*a+s*b,-s*a+c*b] for a,b in w];owners,delta=module.exact_domain(v)
        _,sectors,_,_=module.pinch(np.array([[complex(z) for z in row] for row in v]),owners)
        lower,_=module.exact_lower(v,owners,sectors);target=delta-delta*delta/2
        assert 0<=lower<=target and float(target-lower)<1e-10
        witnesses.append({'t':str(t),'target':str(target),'exact_lower':str(lower),'gap':str(target-lower)})
    assert len(witnesses)==3
    summary={'status':'DIRECT_TENSOR_STATE_REVIEW_PASS','review_provenance':'ASTRA_SELF_REVIEW_DISTINCT_IMPLEMENTATION',
             'circuits':len(records),'exact_rayleigh_controls':len(witnesses),'new_perceval_calls':0,'physical_shots':0,
             'max_probability_error':prob_error,'max_pinched_distance_error':pinch_error,'max_trace_residual':trace_error,
             'runtime_seconds':time.monotonic()-start,'non_claims':['No universal proof','No fresh independent reviewer','Float eigensolvers are not interval certificates']}
    (output/'raw.json').write_text(json.dumps({'summary':summary,'records':records,'rayleigh_controls':witnesses},indent=2)+'\n')
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--raw',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();check(args.raw,args.output)
