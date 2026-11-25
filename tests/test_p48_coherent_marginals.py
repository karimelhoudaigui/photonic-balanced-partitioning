"""24 independent exact fixtures; no NumPy, graph, eigensolver or sampler."""
from decimal import Decimal,localcontext
from fractions import Fraction as Q
import importlib.util
import itertools
import math
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("p48_marginal",ROOT/"research/P48_coherent_marginals.py")
helper=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(helper)


def phase_norm(indices,amplitudes,order):
    if order == 2:
        value=sum((a*(-1)**i for a,i in zip(amplitudes,indices)),Q(0))
        return value*value
    basis=((1,0),(0,1),(-1,-1)) if order == 3 else ((1,0),(0,1),(-1,0),(0,-1))
    a=sum((weight*basis[i][0] for weight,i in zip(amplitudes,indices)),Q(0))
    b=sum((weight*basis[i][1] for weight,i in zip(amplitudes,indices)),Q(0))
    return a*a-a*b+b*b if order == 3 else a*a+b*b


def phase_reference(amplitudes,squared_scale):
    r=len(amplitudes)
    if r == 0:
        return [Q(1)]
    expected=[Q(0)]*(r+1)
    for phases in itertools.product(range(r+1),repeat=r):
        probability=squared_scale*phase_norm(phases,amplitudes,r+1)/r
        assert 0 <= probability <= 1
        for n in range(r+1):
            expected[n]+=Q(math.comb(r,n),(r+1)**r)*probability**n*(1-probability)**(r-n)
    return expected


def sphere_reference(mu,r):
    """Exact integral of Binom(r,mu*x) against (r-1)(1-x)^(r-2)."""
    if r == 0:
        return [Q(1)]
    if r == 1:
        return [1-mu,mu]
    expected=[]
    for n in range(r+1):
        integral=Q(0)
        # Direct monomial integrals; no beta-binomial mixture or source formula.
        for j in range(r-n+1):
            for h in range(r-1):
                integral+=Q((-1)**(j+h)*math.comb(r-n,j)*math.comb(r-2,h),n+j+h+1)*mu**j
        expected.append(math.comb(r,n)*mu**n*(r-1)*integral)
    return expected


def compare(result,expected,mu):
    assert sum(expected) == 1 and min(expected) >= 0
    with localcontext() as ctx:
        ctx.prec=100
        target=[Decimal(p.numerator)/Decimal(p.denominator) for p in expected]
        assert max(abs(a-b) for a,b in zip(result["pmf"],target)) < Decimal("1e-60")
        assert abs(sum(Decimal(i)*p for i,p in enumerate(result["pmf"]))
                   -Decimal(mu.numerator)/Decimal(mu.denominator)) < Decimal("1e-60")
        assert result["cdf"][-1] == 1
        assert all(a <= b for a,b in zip(result["cdf"],result["cdf"][1:]))
        assert result["input_normalization_L1"] == 0
        assert result["pmf_correction_L1"] < Decimal("1e-60")


PHASE_CASES=[([],Q(1))]
PHASE_CASES += [([Q(1)]*r,mu/r) for r in (1,2,3) for mu in (Q(0),Q(1,4),Q(1))]
PHASE_CASES += [([Q(1),Q(0)],Q(1,2)),([Q(1,3),Q(2,3),Q(2,3)],Q(3,4))]


@pytest.mark.parametrize("amplitudes,scale",PHASE_CASES)
def test_phase_against_all_exact_root_assignments(amplitudes,scale):
    q=[scale*a*a for a in amplitudes]
    compare(helper.fixed_phase_marginal(q),phase_reference(amplitudes,scale),sum(q,Q(0)))


SPHERE_CASES=[(Q(0),0)]
SPHERE_CASES += [(mu,1) for mu in (Q(0),Q(1,4),Q(1))]
SPHERE_CASES += [(mu,r) for r in (2,3) for mu in (Q(0),Q(1,4),Q(1,2),Q(1))]


@pytest.mark.parametrize("mu,r",SPHERE_CASES)
def test_sphere_against_exact_beta_integral(mu,r):
    compare(helper.spherical_marginal(mu,r),sphere_reference(mu,r),mu)


def test_no_row_normalization_and_mu1_is_not_always_a_pointmass():
    phase=helper.fixed_phase_marginal([Q(1,8),Q(1,8)])
    compare(phase,[Q(99,128),Q(26,128),Q(3,128)],Q(1,4))
    assert helper.fixed_phase_marginal([1,0])["pmf"] == (Decimal(".25"),Decimal(".5"),Decimal(".25"))
    compare(helper.spherical_marginal(1,2),[Q(1,3)]*3,Q(1))


def test_invalid_rows_and_vacuum_parameters_rejected():
    for q in ([-1,1],[1,1],[float("nan")]):
        with pytest.raises((ValueError,ArithmeticError,OverflowError)):
            helper.fixed_phase_marginal(q)
    for mu,r in ((-1,2),(2,2),(1,0),(.5,-1)):
        with pytest.raises((ValueError,ArithmeticError)):
            helper.spherical_marginal(mu,r)
