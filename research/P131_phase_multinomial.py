"""P131 bounded finite-bit control. No RNG, producer dependency, or import-time run.

Supported input: explicit Gaussian-rational contraction, 0 <= K <= 7 (M <= 8).
Call build_model, then sample_counts with a caller-owned fair_bits(bit_count).
The sampling guarantee assumes uniform independent callback blocks in
[0, 2**bit_count). Range checking does not certify fairness. No provider is
supplied implicitly. Qualification exhausts weights without any random draw.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from math import isqrt

EPSILON = F(1, 1024)
MAX_K = 7


class UnsupportedScope(ValueError):
    """Unsupported inputs are rejected before any bit callback is consulted."""


def rational(value):
    if type(value) not in (int, str, F):
        raise TypeError("exact rational required: " + repr(value))
    return F(value)


def gaussian(value):
    if isinstance(value, (tuple, list)):
        if len(value) != 2:
            raise ValueError("Gaussian pair required: " + repr(value))
        return rational(value[0]), rational(value[1])
    return rational(value), F(0)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def multiply(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def conjugate(a):
    return a[0], -a[1]


def norm2(a):
    return a[0]*a[0] + a[1]*a[1]


def matrix(rows):
    if not isinstance(rows, (tuple, list)) or not rows:
        raise ValueError("at least one explicit signal row required")
    if not all(isinstance(row, (tuple, list)) for row in rows):
        raise TypeError("explicit rows required")
    k = len(rows[0])
    if k > MAX_K:
        raise UnsupportedScope({"status": "UNSUPPORTED", "K": k, "max_K": MAX_K, "bits_read": 0})
    if any(len(row) != k for row in rows):
        raise ValueError("rectangular matrix required")
    return tuple(tuple(gaussian(value) for value in row) for row in rows)


def contraction_certificate(t, eta=F(1)):
    """Exact Hermitian Schur certificate for eta*I - T^dagger T >= 0.

    A zero diagonal of a PSD matrix forces that entire residual row to zero.
    Otherwise the positive pivot and its Schur complement are equivalent to PSD.
    No numerical eigenvalue or tolerance is used, including at eta=1 endpoints.
    """
    eta = rational(eta)
    if not 0 <= eta <= 1:
        raise ValueError("eta outside [0,1]: " + repr(eta))
    k = len(t[0])
    work = []
    for i in range(k):
        row = []
        for j in range(k):
            gram = (F(0), F(0))
            for signal in t:
                gram = add(gram, multiply(conjugate(signal[i]), signal[j]))
            row.append((eta*int(i == j)-gram[0], -gram[1]))
        work.append(row)
    pivots = []
    for i in range(k):
        pivot = work[i][i]
        if pivot[1] != 0 or pivot[0] < 0:
            raise ValueError("non-PSD contraction pivot: " + repr((i, pivot, work)))
        pivots.append(pivot[0])
        if not pivot[0]:
            if any(work[i][j] != (0, 0) or work[j][i] != (0, 0) for j in range(i+1, k)):
                raise ValueError("zero pivot with nonzero row: " + repr((i, work)))
            continue
        for j in range(i+1, k):
            for h in range(i+1, k):
                product = multiply(work[j][i], work[i][h])
                work[j][h] = (work[j][h][0]-product[0]/pivot[0],
                              work[j][h][1]-product[1]/pivot[0])
    return tuple(pivots)


def phase_table(k, epsilon=EPSILON):
    """Certified inward roots for M=1,2,4,8 only; never a generic-M claim.

    For M=8, a=floor(scale/sqrt(2))/scale. Integer square-root certificates
    give a<=1/sqrt(2)<a+1/scale. The four diagonal root errors squared are
    <2/scale**2<=delta**2, and every root lies in the closed unit disk.
    Axis roots are exact. scale is fixed prospectively, not precision-rescued.
    """
    epsilon = rational(epsilon)
    if type(k) is not int or not 0 <= k <= MAX_K or not 0 < epsilon < 1:
        raise ValueError("bounded phase input required: " + repr((k, epsilon)))
    if k == 0:
        return ((F(1), F(0)),), {"M": 1, "delta": F(0), "scale": 1, "error_squared_bound": F(0)}
    m = 1
    while m <= k:
        m *= 2
    delta, scale = epsilon/(4*k), 1
    while F(2, scale) > delta:
        scale *= 2
    lower = isqrt((scale*scale)//2)
    a = F(lower, scale)
    roots8 = ((F(1), F(0)), (a, a), (F(0), F(1)), (-a, a),
              (F(-1), F(0)), (-a, -a), (F(0), F(-1)), (a, -a))
    table = tuple(roots8[r*(8//m)] for r in range(m))
    if not (2*lower*lower <= scale*scale < 2*(lower+1)*(lower+1)):
        raise ArithmeticError("integer square-root branch certificate: " + repr((k, m, scale, lower)))
    error_bound = F(2, scale*scale) if m == 8 else F(0)
    if any(norm2(z) > 1 for z in table) or error_bound > delta*delta:
        raise ArithmeticError("inward root/error certificate: " + repr((table, delta, scale, error_bound)))
    proof = {"M": m, "delta": delta, "scale": scale, "diagonal_numerator": lower,
             "lower_residual": scale*scale-2*lower*lower,
             "upper_residual": 2*(lower+1)*(lower+1)-scale*scale,
             "error_squared_bound": error_bound}
    return table, proof


@dataclass(frozen=True)
class Model:
    t: tuple
    roots: tuple
    epsilon: F
    denominator: int
    categorical_bits: int
    phase_bits: int
    root_proof: dict
    pivots: tuple

    @property
    def k(self):
        return len(self.t[0])

    @property
    def m(self):
        return len(self.t)

    @property
    def bit_count(self):
        return self.k*(self.phase_bits+self.categorical_bits)


def build_model(rows, epsilon=EPSILON):
    t, epsilon = matrix(rows), rational(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("epsilon in (0,1) required")
    pivots = contraction_certificate(t)
    roots, proof = phase_table(len(t[0]), epsilon)
    denominator, bits = 1, 0
    if t[0]:
        while denominator*epsilon < 2*len(t[0])*len(t):
            denominator *= 2
            bits += 1
    return Model(t, roots, epsilon, denominator, bits, (len(roots)-1).bit_length(), proof, pivots)


def context_weights(model, labels):
    """Return integer weights [signal rows...,loss], summing exactly to D."""
    labels = tuple(labels)
    if len(labels) != model.k or any(type(r) is not int or not 0 <= r < len(model.roots) for r in labels):
        raise ValueError("complete bounded phase labels required: " + repr(labels))
    if not model.k:
        return (0,)*model.m + (1,)
    weights = []
    for row in model.t:
        amplitude = (F(0), F(0))
        for coefficient, label in zip(row, labels):
            amplitude = add(amplitude, multiply(coefficient, model.roots[label]))
        rate = norm2(amplitude)/model.k
        scaled = model.denominator*rate
        weights.append(scaled.numerator//scaled.denominator)
    loss = model.denominator-sum(weights)
    if loss < 0 or any(w < 0 for w in weights):
        raise ArithmeticError("invalid exact loss residual: " + repr((labels, weights, loss)))
    return tuple(weights)+(loss,)


def sample_counts(model, fair_bits):
    """Fixed call counts; fair_bits is explicit. No retry or alternate sampler.

    A malformed callback raises with its observed value; it is never clipped.
    K=0 makes no callback call. A receipt records the exact labels and integers.
    """
    if not 0 <= model.k <= MAX_K:
        raise UnsupportedScope({"status": "UNSUPPORTED", "K": model.k, "max_K": MAX_K, "bits_read": 0})
    observed = []
    def take(bits):
        value = fair_bits(bits)
        observed.append((bits, value))
        if type(value) is not int or not 0 <= value < 2**bits:
            raise ValueError("invalid fair-bit return: " + repr(observed))
        return value
    labels = tuple(take(model.phase_bits) for unused in range(model.k))
    weights = context_weights(model, labels)
    counts = [0]*model.m
    for unused in range(model.k):
        ticket = take(model.categorical_bits)
        cumulative = 0
        for j, weight in enumerate(weights):
            cumulative += weight
            if ticket < cumulative:
                if j < model.m:
                    counts[j] += 1
                break
        else:
            raise ArithmeticError("integer CDF failed: " + repr((ticket, weights)))
    receipt = {"phase_labels": labels, "weights": weights, "bit_calls": tuple(observed),
               "bits": sum(bits for bits, value in observed)}
    if receipt["bits"] != model.bit_count:
        raise ArithmeticError("fixed-bit accounting failure: " + repr(receipt))
    return tuple(counts), receipt
