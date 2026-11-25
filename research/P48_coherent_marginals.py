"""Analytic coherent-control PMF/CDFs with SUBUNIT isometry row mass.

Pure stdlib. Input q is never normalized to1. No graph or photon sampling.
Continuous phases and r+1-root count laws are equivalent; four roots need not be.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import math


def _fraction(value):
    if isinstance(value,float):
        return Fraction.from_float(value)
    return Fraction(value)


def _d(value):
    return Decimal(value.numerator)/Decimal(value.denominator)


def _context_inputs(precision):
    if not isinstance(precision,int) or precision < 40:
        raise ValueError("At least40 Decimal digits are required")


def _finish(raw,coefficients,mu,r,precision,model,extra=None):
    zero,one=Decimal(0),Decimal(1)
    tolerance=Decimal(10)**(-(precision-20))
    raw=tuple(raw)
    total,minimum=sum(raw,zero),min(raw)
    if minimum < -tolerance or abs(total-one) > tolerance:
        raise ArithmeticError("PMF exceeds the explicit Decimal error budget")
    nonnegative=tuple(max(zero,p) for p in raw)
    normalizer=sum(nonnegative,zero)
    if normalizer <= 0:
        raise ArithmeticError("Nonpositive PMF sum")
    pmf=tuple(p/normalizer for p in nonnegative)
    raw_cdf=[];running=zero
    for p in pmf:
        running+=p;raw_cdf.append(running)
    if any(p < -tolerance or p > one+tolerance for p in raw_cdf):
        raise ArithmeticError("CDF exceeds its explicit error budget")
    cdf=tuple(min(one,max(zero,p)) for p in raw_cdf[:-1])+(one,)
    if any(b < a for a,b in zip(cdf,cdf[1:])):
        raise ArithmeticError("Nonmonotone CDF")
    result={"model":model,"r":r,"N":r,"mu":mu,"precision":precision,
            "pmf":pmf,"cdf":cdf,"shift_pgf_coefficients":tuple(coefficients),
            "raw_minimum_pmf":minimum,"raw_pmf_sum":total,
            "pmf_correction_L1":sum((abs(a-b) for a,b in zip(pmf,raw)),zero),
            "cdf_roundoff_correction_max":max(abs(a-b) for a,b in zip(cdf,raw_cdf)),
            "input_normalization_L1":zero,"arithmetic_tolerance":tolerance,
            "empirical_calibration_used":False,"interval_certified":False}
    if extra:
        result.update(extra)
    return result


def fixed_phase_marginal(q,*,precision=80):
    """r=len(q) photons; q>=0, mu=sum(q)<=1, with no row renormalization."""
    _context_inputs(precision)
    exact=tuple(_fraction(value) for value in q)
    exact_mu=sum(exact,Fraction(0))
    if any(value < 0 for value in exact) or exact_mu > 1:
        raise ValueError("Nonnegative subunit q required; no input normalization is performed")
    r=len(exact)
    with localcontext() as ctx:
        ctx.prec=precision
        zero,one=Decimal(0),Decimal(1)
        weights=tuple(_d(value) for value in exact)
        mu=_d(exact_mu)
        if r == 0 or exact_mu == 0:
            return _finish((one,)+(zero,)*r,(one,)+(zero,)*r,mu,r,precision,
                           "fixed_phase_continuous_or_r_plus_one_roots")
        polynomial=[one]+[zero]*r
        for weight in weights:
            single=[one]
            for h in range(1,r+1):
                single.append(single[-1]*weight/Decimal(h*h))
            polynomial=[sum((polynomial[j]*single[h-j] for j in range(h+1)),zero)
                        for h in range(r+1)]
        coefficients=[one]
        for h in range(1,r+1):
            falling=math.factorial(r)//math.factorial(r-h)
            coefficients.append(Decimal(falling*math.factorial(h))*polynomial[h]/Decimal(r**h))
        raw=[sum((Decimal((-1)**(h-j)*math.comb(h,j))*coefficients[h]
                  for h in range(j,r+1)),zero) for j in range(r+1)]
        return _finish(raw,coefficients,mu,r,precision,
                       "fixed_phase_continuous_or_r_plus_one_roots")


def spherical_marginal(mu,r,*,precision=80):
    """r photons in a Haar complex-sphere coherent state; positive mixture PMF."""
    _context_inputs(precision)
    if not isinstance(r,int) or r < 0:
        raise ValueError("Nonnegative integer r required")
    exact_mu=_fraction(mu)
    if not 0 <= exact_mu <= 1 or (r == 0 and exact_mu != 0):
        raise ValueError("mu must be subunit and zero when r=0")
    with localcontext() as ctx:
        ctx.prec=precision
        zero,one=Decimal(0),Decimal(1)
        mass=_d(exact_mu)
        coefficients=[one]
        for h in range(r):
            coefficients.append(coefficients[-1]*Decimal(r-h)*mass/Decimal(r+h))
        if r == 0 or exact_mu == 0:
            return _finish((one,)+(zero,)*r,coefficients,mass,r,precision,"spherical_coherent")
        if r == 1:
            return _finish((one-mass,mass),coefficients,mass,r,precision,"spherical_coherent")
        mixture=[Decimal(r-1)/Decimal(2*r-1)]
        for active in range(r):
            mixture.append(mixture[-1]*Decimal(r-active)/Decimal(2*r-2-active))
        if exact_mu == 1:
            raw=mixture
        else:
            raw=[sum((mixture[active]*Decimal(math.comb(active,j))*mass**j
                       *(one-mass)**(active-j) for active in range(j,r+1)),zero)
                 for j in range(r+1)]
        return _finish(raw,coefficients,mass,r,precision,"spherical_coherent",
                       {"positive_beta_binomial_mixture":True,
                        "mixture_weights":tuple(mixture),"mixture_weight_sum":sum(mixture,zero)})
