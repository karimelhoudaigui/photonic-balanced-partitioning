"""Analytic one-mode law of the CONTINUOUS conditional-phase control.

Not the four-root control used in P46. Given active A, phases must be uniform
on the circle, or independent (|A|+1)-th roots for equivalent count laws.
Pure stdlib; no photon/graph sampling, credentials or device operations.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import math


def _decimal(value):
    if isinstance(value, Decimal):
        return value
    if isinstance(value, Fraction):
        return Decimal(value.numerator)/Decimal(value.denominator)
    if isinstance(value, float):
        return Decimal.from_float(value)
    return Decimal(value)


def conditional_phase_marginal(q, transfer_p, *, precision=80, input_tolerance="1e-12"):
    """Return Decimal PMF/CDF plus explicit arithmetic and input corrections.

    q[a]=|W*[j,a]|², sum q=1, A~Bernoulli(transfer_p)^N. Conditional on A,
    l=|A| particles sample the shared continuous-phase field by multinomial.
    N=0 and l=0 give delta0. Tiny row-sum errors are explicitly normalized;
    errors above input_tolerance and gross negative PMFs are rejected.
    The model is analytic; Decimal80 is not an interval certificate.
    """
    if not isinstance(precision, int) or precision < 40:
        raise ValueError("At least40 decimal digits are required")
    q = tuple(q)
    with localcontext() as ctx:
        ctx.prec = precision
        one, zero = Decimal(1), Decimal(0)
        p, tolerance = _decimal(transfer_p), _decimal(input_tolerance)
        if not p.is_finite() or not zero <= p <= one:
            raise ValueError("Invalid Bernoulli transfer probability")
        if not tolerance.is_finite() or not zero <= tolerance <= Decimal("1e-8"):
            raise ValueError("Invalid input-row tolerance")
        weights = tuple(_decimal(value) for value in q)
        if any(not value.is_finite() or value < 0 for value in weights):
            raise ValueError("Nonnegative finite row weights required")
        n = len(weights)
        row_sum = sum(weights, zero)
        input_adjustment = zero
        if n:
            if abs(row_sum-one) > tolerance or row_sum == 0:
                raise ValueError("Row weights do not sum to1 within the declared tolerance")
            adjusted = tuple(value/row_sum for value in weights)
            input_adjustment = sum((abs(a-b) for a,b in zip(weights,adjusted)), zero)
            weights = adjusted
        arithmetic_tolerance = Decimal(10)**(-(precision-20))
        dp = [[zero]*(n+1) for _ in range(n+1)]
        dp[0][0] = one
        for used, weight in enumerate(weights):
            series = [one]
            for h in range(1,n+1):
                series.append(series[-1]*weight/Decimal(h*h))
            updated = [[zero]*(n+1) for _ in range(n+1)]
            for active in range(used+1):
                for degree in range(n+1):
                    mass = dp[active][degree]
                    if not mass:
                        continue
                    updated[active][degree] += (one-p)*mass
                    selected_mass = p*mass
                    if selected_mass:
                        for h in range(n-degree+1):
                            if series[h]:
                                updated[active+1][degree+h] += selected_mass*series[h]
            dp = updated
        coefficients = [one]
        for r in range(1,n+1):
            value = zero
            for active in range(r,n+1):
                falling = math.factorial(active)//math.factorial(active-r)
                value += Decimal(falling*math.factorial(r))*dp[active][r]/Decimal(active**r)
            coefficients.append(value)
        # c0 is separately1; no l=0 division and no 0**0 convention is needed.
        raw_pmf = [sum((Decimal((-1)**(r-j)*math.comb(r,j))*coefficients[r]
                        for r in range(j,n+1)), zero) for j in range(n+1)]
        raw_sum, raw_minimum = sum(raw_pmf,zero), min(raw_pmf)
        if raw_minimum < -arithmetic_tolerance or abs(raw_sum-one) > arithmetic_tolerance:
            raise ArithmeticError("PMF inversion exceeded the recorded Decimal error budget")
        positive = [max(zero,value) for value in raw_pmf]
        normalizer = sum(positive,zero)
        if normalizer <= 0:
            raise ArithmeticError("Nonpositive PMF normalization")
        pmf = tuple(value/normalizer for value in positive)
        correction = sum((abs(a-b) for a,b in zip(pmf,raw_pmf)), zero)
        cdf, running = [], zero
        for value in pmf:
            running += value
            cdf.append(running)
        if abs(cdf[-1]-one) > arithmetic_tolerance or any(value > one+arithmetic_tolerance for value in cdf):
            raise ArithmeticError("CDF endpoint exceeded the recorded Decimal error budget")
        cdf_adjustment = max((abs(min(one,value)-value) for value in cdf), default=zero)
        cdf = tuple(min(one,value) for value in cdf[:-1])+(one,)
        if any(b < a for a,b in zip(cdf,cdf[1:])):
            raise ArithmeticError("Nonmonotone corrected CDF")
        active_pmf = tuple(dp[active][0] for active in range(n+1))
        if abs(sum(active_pmf,zero)-one) > arithmetic_tolerance:
            raise ArithmeticError("Active-sector weights do not normalize")
        return {"model":"conditional_phase_continuous_or_active_plus_one_roots",
                "N":n, "transfer_p":p, "precision":precision,
                "pmf":pmf, "cdf":cdf, "shift_pgf_coefficients":tuple(coefficients),
                "active_count_pmf":active_pmf,
                "input_row_sum_before":row_sum,
                "input_row_normalization_L1":input_adjustment,
                "input_tolerance":tolerance,
                "arithmetic_tolerance":arithmetic_tolerance,
                "raw_minimum_pmf":raw_minimum, "raw_pmf_sum":raw_sum,
                "pmf_correction_L1":correction, "cdf_roundoff_correction_max":cdf_adjustment,
                "sampling_or_empirical_calibration_used":False,
                "interval_certified":False}
