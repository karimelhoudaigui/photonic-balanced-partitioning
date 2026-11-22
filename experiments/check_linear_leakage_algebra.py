"""Exact rational checks for the P36 sharp family and failed Gram shortcut."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def encode(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}


def main(output):
    t=F(65,68);d=F(50,51);e=F(1,102);delta=F(1,17);b=F(7,34)
    pb=[6*d*e*e,2*e*(2*t+1)**2/9,(64*t**3+24*t*t-24*t+17)/81]
    pd=[d*e*e,e*(d*d+d*e+e*e),d**3+3*d*e*e+2*e**3];multiplicities=[3,6,1]
    assert sum(n*p for n,p in zip(multiplicities,pb))==1
    assert sum(n*p for n,p in zip(multiplicities,pd))==1
    tv=sum(n*abs(p-q) for n,p,q in zip(multiplicities,pb,pd))/2
    excess=3*b*b+2*b**3-2*delta
    assert excess==F(265,9826)>0 and tv<=delta
    family=[]
    for parameter in [F(0),F(1,100),F(1,20),F(1,10),F(1,4),F(1,3),F(2,5)]:
        cosine=(1-parameter**2)/(1+parameter**2);sine=2*parameter/(1+parameter**2)
        assert cosine**2+sine**2==1 and cosine>=sine>=0
        leakage=2*sine**2;actual=2*cosine**2*sine**2
        assert actual==leakage-leakage**2/2
        family.append({'rotation_parameter':encode(parameter),'delta':encode(leakage),'tv':encode(actual)})
    payload={'review_provenance':'Physics proposed witness; coordinator supplied and checked complete exact reconstruction. Not an independent proof audit.',
        'gram_shortcut':{'delta':encode(delta),'off_diagonal_gram':encode(b),
            'positive_permanent_excess_over_2delta':encode(excess),'actual_tv':encode(tv),
            'bosonic_group_probabilities':[encode(x) for x in pb],
            'distinguishable_group_probabilities':[encode(x) for x in pd],'multiplicities':multiplicities,
            'conclusion':'REFUTES_PERMANENT_SHORTCUT_NOT_LINEAR_TV_CONJECTURE'},
        'sharp_two_photon_family':family,'general_linear_bound':'CONJECTURAL_FOR_K_GE_3','physical_shots':0}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as f:json.dump(payload,f,indent=2)
    print(json.dumps({'gram_shortcut_refuted':True,'actual_tv':float(tv),'delta':float(delta),
        'two_photon_exact_sharp_cases':len(family),'general_conjecture_proved':False}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);main(parser.parse_args().output)
