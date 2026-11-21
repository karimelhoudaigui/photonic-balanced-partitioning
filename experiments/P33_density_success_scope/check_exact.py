"""Fixed exact two-photon examples for TV/conditioning/rare-success scope.

No sweep, random sampling, training, physical device or new source module.
The five Pythagorean rotations and two endpoints are declared in the note.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path


def laws(A,scale_squared):
    """Exact probabilities for V=sqrt(scale_squared)*A, two distinct inputs.

    Work directly from the two-photon permanent, with output factorial 2 for
    a collision. All ten Fock outcomes, including zeros, are retained.
    """
    m=len(A);r=scale_squared
    gram=[[r*sum(A[i][a]*A[i][b] for i in range(m)) for b in range(2)] for a in range(2)]
    assert gram==[[F(1),F(0)],[F(0),F(1)]]
    p={};q={}
    for i in range(m):
        for j in range(i,m):
            state=tuple(int(a==i)+int(a==j) for a in range(m))
            if i==j:
                product=A[i][0]*A[i][1]
                p[state]=2*r*r*product*product;q[state]=r*r*product*product
            else:
                x=A[i][0]*A[j][1];y=A[i][1]*A[j][0]
                p[state]=r*r*(x+y)**2;q[state]=r*r*(x*x+y*y)
    assert sum(p.values())==sum(q.values())==1
    return p,q


def tv(p,q):return sum((abs(p.get(t,0)-q.get(t,0)) for t in set(p)|set(q)),F(0))/2


def conditional(p,event):
    mass=sum((p[t] for t in event),F(0))
    if mass==0:raise ValueError('Conditional law undefined at zero acceptance mass')
    return {t:p[t]/mass for t in event}


def group_control(groups,m):
    """Supplied groups only; neither graph costs nor C* enter this sampler law."""
    return {tuple(int(i in group) for i in range(m)):F(1,len(groups)) for group in groups}


def density_envelope_diagnostic(M,c=F(1,2)):
    """Floating evaluation of the named 75e envelope, not interval arithmetic."""
    mf,cf=float(M),float(c)
    refined=M<c*c/2
    delta=mf/(cf+math.sqrt(cf*cf-2*mf)) if refined else mf/cf
    rho=2*math.sqrt(delta)+delta
    eps=min(1.,.5*math.expm1(-rho-math.log1p(-rho))) if rho<1 else 1.
    return dict(refined_small_M_branch=refined,delta_bound_float=delta,rho_float=rho,
        epsilon_float=eps,certified_interval_arithmetic=False)


def inspect(name,A,r,M_expected):
    p,q=laws(A,r);states=sorted(p);CF={t for t in states if max(t)<=1}
    # Retrospective path scoring only, not an optimizer/control input.
    cut=lambda t:sum(abs(t[i]-t[j]) for i,j in [(0,1),(1,2),(2,3)])
    optimum=min(cut(t) for t in CF);target={t for t in CF if cut(t)==optimum}
    assert target=={(1,1,0,0),(0,0,1,1)}
    qia=[[r*x*x for x in row] for row in A]
    densities=[sum(row) for row in qia]
    assert densities==[F(1,2)]*4
    M=sum((sum(row)**2-sum(x*x for x in row) for row in qia),F(0))
    pair_mean=sum((p[t]*sum(n*(n-1)//2 for n in t) for t in states),F(0))
    assert M==M_expected==pair_mean==tv(p,q)
    ps=sum((p[t] for t in target),F(0));qs=sum((q[t] for t in target),F(0))
    pf=sum((p[t] for t in CF),F(0));qf=sum((q[t] for t in CF),F(0))
    assert ps==M and qs==M/2 and pf==1-M and qf==1-M/2
    pc,qc=conditional(p,CF),conditional(q,CF)
    cv=tv(pc,qc);bound=tv(p,q)/max(pf,qf)
    assert cv<=bound and cv==M/((1-M)*(2-M))
    psc=sum((pc[t] for t in target),F(0));qsc=sum((qc[t] for t in target),F(0))
    assert psc==M/(1-M) and qsc==M/(2-M)
    classical=group_control(((0,1),(2,3)),4)
    assert sum(classical.values())==1
    assert sum((classical.get(t,0) for t in target),F(0))==1
    envelope=density_envelope_diagnostic(M)
    assert envelope['epsilon_float']>=float(M)-1e-13
    return dict(name=name,scaled_frame=A,scale_squared=r,densities=densities,M=M,
        raw_tv=tv(p,q),bosonic_success=ps,distinguishable_success=qs,
        relative_success_ratio=ps/qs if qs else None,
        bosonic_CF=pf,distinguishable_CF=qf,conditional_tv=cv,
        exact_conditional_bound=bound,conditional_bound_is_equality=cv==bound,
        bosonic_conditional_success=psc,distinguishable_conditional_success=qsc,
        conditional_success_ratio=psc/qsc if qsc else None,
        expected_raw_attempts_bosonic=1/ps if ps else None,
        expected_raw_attempts_distinguishable=1/qs if qs else None,
        zero_success_waiting_time='infinite' if not ps else 'finite',
        classical_group_success=F(1),classical_control_draws_to_success=F(1),
        density_envelope_diagnostic=envelope,
        complete_probabilities=[dict(occupation=t,bosonic=p[t],distinguishable=q[t]) for t in states])


def encode(value):
    if isinstance(value,F):return str(value)
    if isinstance(value,dict):return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):return [encode(v) for v in value]
    return value


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Refusing to overwrite evidence')
    rows=[]
    for denominator in (8,32,128,512,2048):
        t=F(1,denominator);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
        rows.append(inspect(f'Pythagorean_t_1_over_{denominator}',[[c,-s],[c,-s],[s,c],[s,c]],F(1,2),2*c*c*s*s))
    rows.append(inspect('zero_angle',[[F(1),F(0)],[F(1),F(0)],[F(0),F(1)],[F(0),F(1)]],F(1,2),F(0)))
    rows.append(inspect('fully_mixed_endpoint_rational_frame',[[F(1,2),F(-1,2)],[F(1,2),F(-1,2)],[F(1,2),F(1,2)],[F(1,2),F(1,2)]],F(1),F(1,2)))
    assert rows[-1]['conditional_tv']==F(2,3) and rows[-1]['conditional_bound_is_equality']
    p,q=laws([[F(1),F(-1)],[F(1),F(1)],[F(0),F(0)],[F(0),F(0)]],F(1,2))
    CF={t for t in p if max(t)<=1}
    try:conditional(p,CF)
    except ValueError:pass
    else:raise AssertionError('Undefined bosonic HOM conditional was accepted')
    guard=dict(case='HOM_zero_CF',M=F(1),bosonic_CF=sum(p[t] for t in CF),
        distinguishable_CF=sum(q[t] for t in CF),undefined_conditional_rejected=True)
    result=dict(status='completed',domain='Five declared rational rotations + two endpoints + one zero-CF guard; no sweep',
        exact_cases=len(rows),physical_shots=0,training_evaluations=0,random_sampling=False,
        assertions=['Two-photon permanent and distinguishable laws normalize exactly','M=TV and event/CF formulas hold exactly','Conditioning max-denominator bound and closed form agree','Zero-acceptance conditional is rejected','Supplied-group classical control has success one only for this constructed path'],
        limitations=['No independent validation or novelty audit of density certificate75e','Floating density envelope diagnostic is not interval-certified','Known source/graph alignment makes classical control favorable; no algorithmic benchmark'],
        rows=rows,zero_CF_guard=guard)
    args.output.write_text(json.dumps(encode(result),indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(status='completed',exact_cases=len(rows),zero_CF_guards=1,
        maximum_density=float(rows[0]['densities'][0]),
        smallest_M=str(rows[-3]['M']),endpoint_conditional_tv=str(rows[-1]['conditional_tv']),
        physical_shots=0,random_sampling=False),indent=2))

if __name__=='__main__':main()
