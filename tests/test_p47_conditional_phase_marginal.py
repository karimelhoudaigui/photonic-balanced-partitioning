"""Independent EXACT rational fixtures; no graph, NumPy or physical sampler."""
from decimal import Decimal, localcontext
from fractions import Fraction as Q
import importlib.util
import itertools
import math
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p47_cdf", ROOT/"research/P47_conditional_phase_marginal.py")
oracle = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oracle)


def exact_phase_squared(phase_indices, amplitudes, order):
    """Rational cyclotomic norms for roots of orders2,3,4 only."""
    if order == 2:
        real = sum((amp*((-1)**index) for amp,index in zip(amplitudes,phase_indices)), Q(0))
        return real*real
    if order == 3:
        # omega²=-1-omega, |a+b omega|²=a²-ab+b².
        basis = ((1,0),(0,1),(-1,-1))
        a = sum((amp*basis[index][0] for amp,index in zip(amplitudes,phase_indices)), Q(0))
        b = sum((amp*basis[index][1] for amp,index in zip(amplitudes,phase_indices)), Q(0))
        return a*a-a*b+b*b
    if order == 4:
        basis = ((1,0),(0,1),(-1,0),(0,-1))
        a = sum((amp*basis[index][0] for amp,index in zip(amplitudes,phase_indices)), Q(0))
        b = sum((amp*basis[index][1] for amp,index in zip(amplitudes,phase_indices)), Q(0))
        return a*a+b*b
    raise AssertionError("Fixture only supports l<=3")


def exhaustive_reference(amplitudes, squared_scale, p):
    """All Bernoulli A, all l+1-root phase tuples, exact binomial probabilities."""
    n = len(amplitudes)
    result = [Q(0)]*(n+1)
    for mask in itertools.product((0,1),repeat=n):
        active = [a for a,selected in zip(amplitudes,mask) if selected]
        l = len(active)
        mask_probability = p**l*(1-p)**(n-l)
        if l == 0:
            result[0] += mask_probability
            continue
        root_order = l+1
        for phase in itertools.product(range(root_order),repeat=l):
            probability = squared_scale*exact_phase_squared(phase,active,root_order)/l
            assert 0 <= probability <= 1
            phase_weight = mask_probability/Q(root_order**l)
            for count in range(l+1):
                result[count] += phase_weight*math.comb(l,count)*probability**count*(1-probability)**(l-count)
    assert sum(result) == 1
    return result


def assert_exact_fixture(amplitudes, squared_scale, p):
    q = [squared_scale*a*a for a in amplitudes]
    result = oracle.conditional_phase_marginal(q,p)
    expected = exhaustive_reference(amplitudes,squared_scale,p)
    with localcontext() as ctx:
        ctx.prec = 90
        target = [Decimal(value.numerator)/Decimal(value.denominator) for value in expected]
        assert max(abs(a-b) for a,b in zip(result["pmf"],target)) < Decimal("1e-60")
        assert abs(sum(result["pmf"])-1) < Decimal("1e-60")
        assert result["cdf"][-1] == 1
        if q:
            mean = sum(Decimal(i)*prob for i,prob in enumerate(result["pmf"]))
            assert abs(mean-Decimal(p.numerator)/Decimal(p.denominator)) < Decimal("1e-60")
    assert result["pmf_correction_L1"] < Decimal("1e-60")


@pytest.mark.parametrize("p", [Q(0),Q(1,4),Q(1,2),Q(1)])
@pytest.mark.parametrize("n", [0,1,2,3])
def test_all_active_sets_and_root_phases_for_uniform_row(n,p):
    assert_exact_fixture([Q(1)]*n,Q(1,n) if n else Q(1),p)


@pytest.mark.parametrize("p", [Q(1,4),Q(1,2),Q(1)])
def test_nonuniform_rational_amplitude_row(p):
    assert_exact_fixture([Q(1,3),Q(2,3),Q(2,3)],Q(1),p)


@pytest.mark.parametrize("p", [Q(0),Q(1,4),Q(1,2),Q(1)])
def test_pointmass_row_includes_other_active_inputs_in_multinomial_size(p):
    assert_exact_fixture([Q(1),Q(0),Q(0)],Q(1),p)
    actual = oracle.conditional_phase_marginal([1,0],p)["pmf"]
    with localcontext() as ctx:
        ctx.prec = 90
        expected = [1-p+p*p/4,p-p*p/2,p*p/4]
        target = [Decimal(v.numerator)/Decimal(v.denominator) for v in expected]
        assert max(abs(a-b) for a,b in zip(actual,target)) < Decimal("1e-60")


def test_invalid_inputs_and_explicit_tiny_row_normalization():
    for q,p in (([.2,.2],.5),([-1,2],.5),([1],-1),([1],2),([float("nan")],.5)):
        with pytest.raises((ValueError,ArithmeticError)):
            oracle.conditional_phase_marginal(q,p)
    result = oracle.conditional_phase_marginal([Decimal("1.000000000000001")],Q(1,2))
    assert 0 < result["input_row_normalization_L1"] < Decimal("1e-12")
    assert result["pmf"] == (Decimal(".5"),Decimal(".5"))
    with pytest.raises(ValueError):
        oracle.conditional_phase_marginal([1],.5,precision=20)
