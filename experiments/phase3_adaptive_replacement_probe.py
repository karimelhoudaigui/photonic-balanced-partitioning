"""Exact finite history check, including all collisions and adaptive strengths."""
import argparse
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json
from pathlib import Path

BASIS=list(combinations_with_replacement(range(4),2))
SUCCESS={j for j,(a,b) in enumerate(BASIS) if a!=b and a//2==b//2}


def law(t,bosonic):
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);cross=c*c*s*s
    probabilities=[]
    for a,b in BASIS:
        if a==b:p=cross/(2 if bosonic else 4)
        elif a//2==b//2:p=cross/(1 if bosonic else 2)
        else:p=((c*c-s*s)**2 if bosonic else c**4+s**4)/4
        probabilities.append(p)
    assert sum(probabilities)==1 and min(probabilities)>=0
    return probabilities


def tv(b,d):return sum(abs(x-y) for x,y in zip(b,d))/2


def fraction(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}


def experiment(steps,initial=F(1,20),stop=False):
    b={():F(1)};d=dict(b);expected_budget=F(0);product=F(1);uniform=[]
    for step in range(steps):
        bn={};dn={};largest=F(0)
        for h in b:
            stopped=stop and any(i in SUCCESS for i in h)
            if stopped:lb=ld=[F(0)]*10+[F(1)]
            else:
                t=initial if not h else F(1,10) if BASIS[h[-1]][0]==BASIS[h[-1]][1] else F(1,40)
                lb=law(t,True);ld=law(t,False)
            epsilon=tv(lb,ld);largest=max(largest,epsilon)
            expected_budget+=b[h]*epsilon
            for index,(pb,pd) in enumerate(zip(lb,ld)):
                bn[h+(index,)]=b[h]*pb;dn[h+(index,)]=d[h]*pd
        b,d=bn,dn;uniform.append(largest);product*=1-largest
    assert sum(b.values())==sum(d.values())==1
    actual=tv(list(b.values()),list(d.values()))
    product_bound=1-product;expectation_bound=min(F(1),expected_budget)
    assert actual<=product_bound and actual<=expectation_bound
    pb=sum(p for h,p in b.items() if any(i in SUCCESS for i in h))
    pd=sum(p for h,p in d.items() if any(i in SUCCESS for i in h))
    assert abs(pb-pd)<=actual
    return {'steps':steps,'stop_on_first_success':stop,'initial_rotation_t':fraction(initial),
        'transcript_tv':fraction(actual),'product_coupling_bound':fraction(product_bound),
        'bosonic_expected_epsilon_sum_bound':fraction(expectation_bound),
        'uniform_one_step_epsilons':[fraction(e) for e in uniform],
        'bosonic_any_success':fraction(pb),'distinguishable_any_success':fraction(pd),
        'complete_histories':[{'history':h,'bosonic':fraction(p),'distinguishable':fraction(d[h])} for h,p in b.items()]}


def main(output):
    runs=[experiment(t) for t in [1,2,3]]+[experiment(3,stop=True)]
    changed=experiment(2,initial=F(0))
    assert changed['uniform_one_step_epsilons'][0]['numerator']=='0'
    assert int(changed['transcript_tv']['numerator'])>0
    raw={'assertion_tested':'Sequential product and history-sensitive coupling bounds survive exact adaptive three-step photonic histories.',
        'conventions':'Four modes, two photons, pair-supported rational rotation; complete ten-outcome Fock law; no optimizer, no shots.',
        'outcome_pair_basis':BASIS,'success_indices':sorted(SUCCESS),'runs':runs,
        'initial_certificate_only_counterexample':changed,
        'review_provenance':'Coordinator self-review; fresh agent review deferred by quota',
        'physical_shots':0,'novelty':'Ordinary sequential coupling is known; no novelty claimed',
        'non_claims':['No algorithmic advantage','No independent proof audit','No numerical interval issue: this finite check uses exact fractions']}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as stream:json.dump(raw,stream,separators=(',',':'))
    print(json.dumps({'exact_runs':len(runs),'control_runs':1,'all_bounds_passed':True,
        'initial_zero_certificate_does_not_control_adaptive_transcript':True,'physical_shots':0}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    main(parser.parse_args().output)
