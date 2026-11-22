"""Exact self-review using monotone scalar roots, independent of Rayleigh code."""
import argparse
from fractions import Fraction as F
from itertools import permutations, product
import json
from pathlib import Path
import time


def q(x):return F(int(x['numerator']),int(x['denominator']))
def enc(x):
    if isinstance(x,F):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}
    raise TypeError(type(x).__name__)


def check(raw_path,output):
    output.mkdir(parents=True,exist_ok=False);started=time.monotonic();raw=json.loads(raw_path.read_text())
    d,e=F(19,25),F(3,25);p=[[d if g==a else e for a in range(3)] for g in range(3)]
    assert all(sum(p[g][a] for g in range(3))==1 for a in range(3))
    assert [[q(x) for x in row] for row in raw['p']]==p
    classes={1:sorted([d*e*e]*6),2:sorted([d*d*e]*2+[d*e*e]*2+[e**3]*2),
             3:sorted([d**3]+[d*e*e]*3+[e**3]*2)}
    rows=[];counts={1:0,2:0,3:0};pp=list(permutations(range(3)))
    for record,groups in zip(raw['sectors'],product(range(3),repeat=3)):
        weights=[]
        for perm in pp:
            w=F(1)
            for g,a in zip(groups,perm):w*=p[g][a]
            weights.append(w)
        kind=len(set(groups));counts[kind]+=1
        assert sorted(weights)==classes[kind] and [q(w) for w in record['weights']]==weights
        assert list(groups)==record['groups']
        rows.append({'groups':groups,'class':kind})
    assert len(raw['sectors'])==27 and counts=={1:3,2:18,3:6}
    residual_a=sum((w/(F(43,400)+w) for w in classes[2]),F(0))-1
    residual_b=sum((w/(F(7,50)+w) for w in classes[3]),F(0))-1
    assert residual_a>0 and residual_b>0
    strict_lower=F(5,2)*d*e*e+3*F(43,400)+F(7,50);delta=6*e;curve=delta-delta*delta/2
    assert strict_lower==F(24493,50000) and strict_lower-curve==F(1453,50000)
    assert q(raw['summary']['exact_rayleigh_lower'])>strict_lower>curve
    summary={'status':'EXACT_SCALAR_ROOT_COUNTEREXAMPLE_CHECK_PASS','review_provenance':'ASTRA_SELF_REVIEW_DIFFERENT_ARGUMENT',
             'residual_repeated':residual_a,'residual_distinct':residual_b,'strict_lower':strict_lower,
             'curved_envelope':curve,'strict_gap':strict_lower-curve,'sectors_checked':len(rows),
             'physical_shots':0,'runtime_seconds':time.monotonic()-started,
             'non_claims':['No linear-bound or measured-TV refutation','No fresh independent review or novelty claim']}
    (output/'receipt.json').write_text(json.dumps({'summary':summary,'sectors':rows},default=enc,indent=2)+'\n')
    print(json.dumps(summary,default=enc))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--raw',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();check(a.raw,a.output)
