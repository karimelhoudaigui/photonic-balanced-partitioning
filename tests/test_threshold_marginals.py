"""Independent physical and exact permanent controls for the classical baseline."""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
import math
import pytest
from photonic_balanced_partitioning.photonic.threshold_marginals import (
    GaussianRational as G, ThresholdMarginals, encode_binary_frame, vacuum_probability,
)


def exact_fock_law(frame):
    m=len(frame);n=len(frame[0]);frame=[[x if isinstance(x,G) else G(x) for x in row] for row in frame]
    result={}
    for outputs in combinations_with_replacement(range(m),n):
        occupation=tuple(outputs.count(i) for i in range(m));amplitude=G()
        for assignment in permutations(range(n)):
            product=G(1)
            for i,a in zip(outputs,assignment):product=product*frame[i][a]
            amplitude=amplitude+product
        probability=(amplitude.real**2+amplitude.imag**2)/math.prod(math.factorial(x) for x in occupation)
        result[occupation]=probability
    assert sum(result.values())==1
    return result


def rational_unitary(m):
    u=[[G(int(i==j)) for j in range(m)] for i in range(m)]
    for number,(i,j) in enumerate([(a,a+1) for a in range(m-1)]+[(0,m-1)]):
        c,s=F(3,5),F(4,5);a,b=u[i][:],u[j][:]
        if number%2:
            u[i]=[c*x+G(0,s)*y for x,y in zip(a,b)]
            u[j]=[G(0,s)*x+c*y for x,y in zip(a,b)]
        else:
            u[i]=[c*x-s*y for x,y in zip(a,b)]
            u[j]=[s*x+c*y for x,y in zip(a,b)]
    return u


def test_exact_hom_vacuum_and_clicks_include_bunching():
    a,b=G(F(1,2),F(1,2)),G(F(1,2),F(-1,2))
    evaluator=ThresholdMarginals([[a,b],[b,a]])
    assert evaluator.vacuum((0,))==F(1,2)
    assert evaluator.vacuum((0,1))==0
    assert evaluator.click_means()==[F(1,2)]*2
    assert evaluator.pair_moments()==[[F(1,2),0],[0,F(1,2)]]
    assert evaluator.qubo_expectation([[-1,3],[3,2]])==F(1,2)


@pytest.mark.parametrize('m,n',[(4,2),(4,4),(6,3)])
def test_all_threshold_moments_and_qubo_match_exact_routing_permanents(m,n):
    frame=[row[:n] for row in rational_unitary(m)]
    evaluator=ThresholdMarginals(frame);law=exact_fock_law(frame)
    means=evaluator.click_means();pairs=evaluator.pair_moments()
    for i in range(m):
        assert means[i]==sum(p for t,p in law.items() if t[i]>0)
        for j in range(m):assert pairs[i][j]==sum(p for t,p in law.items() if t[i]>0 and t[j]>0)
    q=[[F((i+1)*(j+1)%7-3) for j in range(m)] for i in range(m)]
    expected=sum(p*sum(q[i][j] for i in range(m) for j in range(m) if t[i]>0 and t[j]>0) for t,p in law.items())
    assert evaluator.qubo_expectation(q)==expected


def test_vacuum_and_unary_conventions():
    assert vacuum_probability([])==vacuum_probability([[],[]])==1
    empty=ThresholdMarginals([[],[]]);assert empty.click_means()==[0,0]
    unary=ThresholdMarginals([[F(3,5)],[G(0,F(4,5))]])
    assert unary.click_means()==[F(9,25),F(16,25)]
    assert unary.pair_moments()[0][1]==0


def test_exact_physical_validation_and_explicit_binary_encoding():
    with pytest.raises(TypeError):ThresholdMarginals([[.6],[.8]])
    encoded=encode_binary_frame([[.6],[.8]])
    with pytest.raises(ValueError,match='exactly orthonormal'):ThresholdMarginals(encoded)
    formal=ThresholdMarginals(encoded,check_orthonormal=False)
    assert formal.physical_input_validated is False
    assert 'FORMAL_POLYNOMIAL' in formal.input_semantics
    with pytest.raises(ValueError):ThresholdMarginals([[1,1],[0,0]])
    with pytest.raises(ValueError):encode_binary_frame([[float('nan')]])


def test_rejects_unsupported_shapes_and_respects_resource_caps():
    with pytest.raises(ValueError):vacuum_probability([[1],[0],[0]])
    with pytest.raises(ValueError):vacuum_probability([[1],[0,0]])
    with pytest.raises(RuntimeError,match='budget'):vacuum_probability([[F(1,2),F(1,2)]],max_transitions=0)
    with pytest.raises(RuntimeError,match='budget'):vacuum_probability([[F(1,2)],[F(1,3)]],max_states=1)
    e=ThresholdMarginals([[1],[0]])
    with pytest.raises(ValueError):e.vacuum((0,0))
    with pytest.raises(ValueError):e.qubo_expectation([[1,2],[3,4]])


@pytest.mark.parametrize('name',['max_states','max_transitions'])
@pytest.mark.parametrize('invalid',[float('nan'),float('inf'),float('-inf'),1.0,F(1,2),'4',None,True])
def test_resource_limits_reject_noninteger_values_before_computation(name,invalid):
    options={name:invalid}
    with pytest.raises(ValueError,match=name):
        vacuum_probability([[F(1,2),F(1,2)]],**options)
    with pytest.raises(ValueError,match=name):
        ThresholdMarginals([[1],[0]],**options)
