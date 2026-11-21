"""Explicit photon budget and threshold-click decoding, including collisions.

The Haar click law is known (Bouland et al., arXiv:2312.00286, Lemma 1).
Resource comparisons below must name both input photons N and target clicks k.
No class in this module accesses a device or represents full ObliQ dynamics.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
import math
from numbers import Integral
import numpy as np

from .fixed_photon_obliq import FixedPhotonObliq, _ryser_subsets


def haar_click_probability(m: int, photons: int, clicks: int) -> Fraction:
    """Exact Haar mean; any fixed normalized N-photon input independent of U."""
    if any(not isinstance(v, Integral) for v in (m, photons, clicks)) or m < 1 or photons < 0 or clicks < 0:
        raise ValueError('Require integer m>=1, N>=0, k>=0')
    if photons == 0:
        return Fraction(int(clicks == 0))
    if not 1 <= clicks <= min(m, photons):
        return Fraction(0)
    return Fraction(math.comb(m, clicks)*math.comb(photons-1, clicks-1),
                    math.comb(m+photons-1, photons))


def haar_click_probability_loss(m, photons, clicks, eta):
    """Haar mean under independent uniform photon survival, with all attempts.

    Loss occurs before thresholding. Outputs with fewer than N detections remain
    legitimate binary candidates; no 'all N detected' gate is silently imposed.
    eta includes only independent uniform loss, not dark counts or impurity.
    """
    haar_click_probability(m, photons, clicks)  # domain validation
    if not np.isfinite(eta) or not 0 <= eta <= 1:
        raise ValueError('eta must lie in [0,1]')
    if eta == 0:
        return float(clicks == 0)
    if eta == 1:
        return float(haar_click_probability(m, photons, clicks))
    total = 0.
    for survivors in range(photons+1):
        mass = math.comb(photons, survivors)*eta**survivors*(1-eta)**(photons-survivors)
        total += mass*float(haar_click_probability(m, survivors, clicks))
    return total


def optimal_photon_numbers(m, clicks, maximum=None, per_photon=False):
    """Exact maximizers under an explicit photon cap, for lossless Haar draws.

    Per-attempt f_(N+1)/f_N = N(N+1)/[(N-k+1)(m+N)]. Per-photon efficiency
    replaces numerator by N^2. Arithmetic maximization avoids rounding at ties.
    """
    maximum = m if maximum is None else maximum
    if not isinstance(maximum, Integral) or maximum < clicks or clicks < 1 or clicks > m:
        raise ValueError('Require 1<=k<=m and N_max>=k')
    scored = [(N, haar_click_probability(m,N,clicks)/(N if per_photon else 1))
              for N in range(clicks,maximum+1)]
    best = max(value for _,value in scored)
    return tuple(N for N,value in scored if value == best)


def haar_loss_coefficient_formula(m, photons, clicks, eta):
    """Independent coefficient formula for the loss-mixture identity.

    C(m,k)*eta^k/D_N * [z^(N-k)] (1-z)^(-k) (1-(1-eta)z)^(-m).
    This branch covers k>=1. It uses a different finite sum from the mixture.
    """
    haar_click_probability(m,photons,clicks)
    if not 0 <= eta <= 1:
        raise ValueError('eta must lie in [0,1]')
    if clicks == 0:
        return (1-eta)**photons
    if photons < clicks or clicks > m:
        return 0.
    coefficient = sum(math.comb(clicks+j-1,j)*math.comb(m+photons-clicks-j-1,photons-clicks-j)
                      *(1-eta)**(photons-clicks-j) for j in range(photons-clicks+1))
    return math.comb(m,clicks)*eta**clicks*coefficient/math.comb(m+photons-1,photons)


class ThresholdEvaluator:
    """Full Fock to full binary map, first N inputs singly occupied.

    Enumeration is exponential; this is a transparent small-instance reference.
    All collision occupations enter threshold x_i=1[t_i>0] instead of rejection.
    Bitstring order matches itertools.product((0,1),repeat=m).
    """
    def __init__(self, m, photons):
        self.m, self.photons = m, photons
        self.solver = FixedPhotonObliq(m,photons)
        self.occupations = np.asarray(self.solver._enumerate_all_fock_states(),dtype=int)
        self.bitstrings = np.asarray(list(product((0,1),repeat=m)),dtype=int)
        self.weights = 1 << np.arange(m-1,-1,-1)
        self.binary_indices = (self.occupations>0) @ self.weights
        self._rows = np.array([np.repeat(np.arange(m),t) for t in self.occupations],dtype=int)
        self._factorials = np.array([math.prod(math.factorial(c) for c in t) for t in self.occupations])

    def fock_probabilities(self,U,model='bosonic'):
        if model == 'bosonic':
            return abs(self.solver.output_state(U))**2
        U = self.solver._validate_unitary(U)
        if model != 'distinguishable':
            raise ValueError('Unknown model')
        if self.photons == 0:
            return np.ones(1)
        subsets, signs = _ryser_subsets(self.photons)
        result = np.empty(len(self.occupations))
        # Limit transient tensor storage; numerical roundoff is checked below.
        for start in range(0,len(result),256):
            rows = self._rows[start:start+256]
            matrices = abs(U[rows,:self.photons])**2
            result[start:start+256] = np.prod(matrices @ subsets.T,axis=1) @ signs
        result /= self._factorials
        if result.min() < -1e-11 or abs(result.sum()-1)>1e-9:
            raise ArithmeticError('Distinguishable distribution failed positivity/normalization')
        return np.maximum(result,0.)

    def probabilities(self,U,model='bosonic',eta=1.):
        if not np.isfinite(eta) or not 0 <= eta <= 1:
            raise ValueError('eta must lie in [0,1]')
        p = self.fock_probabilities(U,model)
        if eta == 1:
            return np.bincount(self.binary_indices,weights=p,minlength=2**self.m)
        if eta == 0:
            result=np.zeros(2**self.m);result[0]=1.;return result
        no_click=(1-eta)**self.occupations
        result=np.empty(2**self.m)
        for idx,bits in enumerate(self.bitstrings):
            result[idx]=float(p @ np.prod(np.where(bits,1-no_click,no_click),axis=1))
        if abs(result.sum()-1)>1e-9:
            raise ArithmeticError('Loss/theshold channel failed normalization')
        return result

    def metrics(self,U,edges,k,model='bosonic',eta=1.):
        p=self.probabilities(U,model,eta)
        costs=np.zeros(len(p))
        for i,j,w in edges:costs+=w*(self.bitstrings[:,i] != self.bitstrings[:,j])
        valid=self.bitstrings.sum(axis=1)==k
        optimum=float(costs[valid].min())
        best=valid & np.isclose(costs,optimum,atol=1e-9,rtol=0)
        feasible=float(p[valid].sum());success=float(p[best].sum())
        return dict(p_feasible=feasible,p_success=success,
                    conditional_energy=float(p[valid] @ costs[valid]/feasible) if feasible>1e-14 else None,
                    p_opt_given_feasible=success/feasible if feasible>1e-14 else None,
                    optimum=optimum,photons=self.photons,eta=eta)
