"""Bounded, read-only P35 audit: independent rational Gram/Ryser calculations.

No new circuit generation, optimization, physical sampling, or P35 campaign run.
The reference complex arithmetic uses independent Fraction pairs, not the
component's GaussianRational operators or coefficient recurrence.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse
import json
from pathlib import Path
import time
import importlib.util
import sys
# Load only the reviewed stdlib component, avoiding unrelated package imports.
module_path=Path('src/photonic_balanced_partitioning/photonic/threshold_marginals.py').resolve()
spec=importlib.util.spec_from_file_location('_p35_reviewed_component',module_path)
component=importlib.util.module_from_spec(spec);sys.modules[spec.name]=component
spec.loader.exec_module(component)
G=component.GaussianRational;MarginalStats=component.MarginalStats
ThresholdMarginals=component.ThresholdMarginals;vacuum_probability=component.vacuum_probability

ZERO=(F(0),F(0));ONE=(F(1),F(0))
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a):return (a[0],-a[1])
def frac(x):return F(int(x['numerator']),int(x['denominator']))
def pair(x):return (frac(x['real']),frac(x['imag']))
def serial(x):return {'numerator':str(x.numerator),'denominator':str(x.denominator)}

def permanent_ryser(matrix):
    n=len(matrix)
    if n==0:return ONE
    total=ZERO
    for subset in range(1,1<<n):
        product=ONE
        for row in matrix:
            row_sum=ZERO
            for j in range(n):
                if subset>>j&1:row_sum=add(row_sum,row[j])
            product=mul(product,row_sum)
        total=add(total,product if (n-subset.bit_count())%2==0 else neg(product))
    return total


def gram_permanent(rows,n):
    matrix=[]
    for a in range(n):
        row=[]
        for b in range(n):
            gram=ZERO
            for v in rows:gram=add(gram,mul(conj(v[a]),v[b]))
            row.append(add(ONE if a==b else ZERO,neg(gram)))
        matrix.append(row)
    answer=permanent_ryser(matrix)
    assert answer[1]==0
    return answer[0]


def main(output):
    start=time.monotonic()
    if output.exists():raise FileExistsError('Refusing evidence overwrite')
    raw=json.loads(Path('experiments/P35_threshold_marginal/run/data/raw.json').read_text())
    summary=json.loads(Path('experiments/P35_threshold_marginal/run/data/summary.json').read_text())
    records=[];comparisons=0;max_reference_error=F(0)
    assert len(raw['records'])==12
    assert [r['seed'] for r in raw['records']]==list(range(20261122,20261134))
    for record in raw['records']:
        m,n=record['m'],record['photons'];v=[[pair(z) for z in row] for row in record['frame']]
        evaluator=ThresholdMarginals([[G(*z) for z in row] for row in v],
                                     check_orthonormal=record['exact_physical_frame'])
        means=[frac(x) for x in record['click_means']]
        pairs=[[frac(x) for x in row] for row in record['pair_moments']]
        vacua={}
        for indices in list(combinations(range(m),1))+list(combinations(range(m),2)):
            independent=gram_permanent([v[i] for i in indices],n)
            actual=evaluator.vacuum(indices)
            max_reference_error=max(max_reference_error,abs(actual-independent))
            assert actual==independent,(record['seed'],indices,actual,independent)
            vacua[indices]=independent;comparisons+=1
        for i in range(m):
            assert means[i]==1-vacua[(i,)]
            assert pairs[i][i]==means[i]
            for j in range(i+1,m):
                assert pairs[i][j]==pairs[j][i]==1-vacua[(i,)]-vacua[(j,)]+vacua[(i,j)]
        q=[[frac(x) for x in row] for row in record['qubo']]
        independent_energy=sum(q[i][j]*pairs[i][j] for i in range(m) for j in range(m))
        assert independent_energy==frac(record['qubo_expectation'])==evaluator.qubo_expectation(q)
        states=record['fock_basis'];law=record['perceval_probabilities']
        assert len(states)==len(law)==len(set(tuple(t) for t in states))
        assert all(len(t)==m and sum(t)==n and min(t)>=0 for t in states)
        import math
        assert len(states)==math.comb(m+n-1,n)
        assert min(law)>=0 and abs(sum(law)-1)<1e-12
        mean_error=max(abs(float(means[i])-sum(p for t,p in zip(states,law) if t[i])) for i in range(m))
        pair_error=max(abs(float(pairs[i][j])-sum(p for t,p in zip(states,law) if t[i] and t[j]))
                       for i in range(m) for j in range(m))
        energy_ref=sum(p*float(sum(q[i][j] for i in range(m) for j in range(m) if t[i] and t[j]))
                       for t,p in zip(states,law))
        energy_error=abs(float(independent_energy)-energy_ref)
        assert max(mean_error,pair_error,energy_error)<1e-10
        if record['exact_physical_frame']:
            exact=[frac(x) for x in record['exact_fock_probabilities']]
            assert sum(exact)==1 and min(exact)>=0
            for indices,prob in vacua.items():
                assert prob==sum(p for t,p in zip(states,exact) if all(t[i]==0 for i in indices))
        # Sparse-pruning counters are bounded above by the dense equal-degree table.
        t1=n*(n+1)//2;t2=n*(n+1)**2*(n+2)//12
        work=record['work'];assert work['calls']==m+m*(m-1)//2
        assert work['state_visits']<=m*t1+m*(m-1)//2*t2
        assert work['transitions']<=m*t1+4*(m*(m-1)//2)*t2
        assert work['peak_states']<=(n+1)*(n+2)*(2*n+3)//6
        assert evaluator.stats.state_visits==work['state_visits']
        assert evaluator.stats.transitions==work['transitions']
        assert evaluator.stats.max_integer_bits==work['max_integer_bits']
        records.append(dict(seed=record['seed'],m=m,photons=n,exact_physical=record['exact_physical_frame'],
                            reference_vacua_compared=len(vacua),expected_energy=serial(independent_energy),
                            gram_ryser_equals_component_exactly=True,
                            max_saved_perceval_mean_error=mean_error,max_saved_perceval_pair_error=pair_error,
                            saved_perceval_energy_error=energy_error,work=work))
    # Three additional formal row inputs, not physical circuits, stress complex
    # off-diagonal states and input-column permutation invariance.
    formal=[[(F(1,2),F(1,3)),(F(2,5),F(-1,7)),(F(-1,3),F(1,4))],
            [(F(0),F(1,2)),(F(1,3),F(0)),(F(2,7),F(1,5))]]
    formal_controls=[]
    for rows in (formal[:1],formal,[list(reversed(row)) for row in formal]):
        expected=gram_permanent(rows,3);actual=vacuum_probability([[G(*z) for z in row] for row in rows])
        assert actual==expected
        formal_controls.append(dict(rank=len(rows),value=serial(actual)))
    assert formal_controls[1]['value']==formal_controls[2]['value']
    hom=[[(F(1,2),F(1,2)),(F(1,2),F(-1,2))],
         [(F(1,2),F(-1,2)),(F(1,2),F(1,2))]]
    assert gram_permanent(hom[:1],2)==F(1,2) and gram_permanent(hom,2)==0
    assert vacuum_probability([[G(*z) for z in hom[0]]])==F(1,2)
    assert vacuum_probability([[G(*z) for z in row] for row in hom])==0
    assert vacuum_probability([])==vacuum_probability([[],[]])==1
    assert vacuum_probability([[F(3,5)]])==F(16,25)
    # Nonphysical exact entries must be rejected by physical validation, while
    # unvalidated evaluation must remain unclipped and explicitly formal.
    try:ThresholdMarginals([[2]])
    except ValueError:physical_rejected=True
    else:physical_rejected=False
    assert physical_rejected
    formal_bad=ThresholdMarginals([[2]],check_orthonormal=False)
    assert formal_bad.vacuum((0,))==-3 and formal_bad.click_means()==[4]
    # Public resource guards currently accept NaN. Preserve this defect rather
    # than making it disappear behind a successful scientific assertion.
    guard_probes=[]
    for kwargs in ({'max_states':float('nan')},{'max_transitions':float('nan')}):
        stats=MarginalStats()
        try:result=vacuum_probability([[F(1,2),F(1,2)]],stats=stats,**kwargs)
        except (TypeError,ValueError):rejected=True;result=None
        else:rejected=False
        guard_probes.append(dict(keyword=next(iter(kwargs)),nan_rejected=rejected,
                                 result=serial(result) if result is not None else None,
                                 transitions=stats.transitions,peak_states=stats.peak_states))
    payload=dict(status='EXACT_CHECKS_PASS_WITH_RESOURCE_GUARD_DEFECT',raw_records_audited=12,
                 exact_physical_records=6,gram_ryser_marginals_compared=comparisons,
                 max_exact_probability_difference=serial(max_reference_error),records=records,
                 formal_controls=formal_controls,hom_vacuum_single=serial(F(1,2)),hom_vacuum_both=serial(F(0)),
                 resource_guard_probes=guard_probes,new_circuits_generated=0,physical_shots=0,
                 runtime_seconds=time.monotonic()-start,
                 non_claims=['No new Perceval campaign; archived full-law probabilities only',
                             'No performance benchmark, optimizer or physical-input calibration guarantee',
                             'Ryser uses exponential subset enumeration as a small reference, not as the baseline'])
    output.write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('records','non_claims')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();main(a.output)
