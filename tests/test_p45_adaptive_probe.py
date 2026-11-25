"""Small independent references for P45; no development graph is generated."""
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("p45_adaptive", ROOT/"research/P45_adaptive_probe.py")
p45 = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(ROOT/"research"))
try:
    SPEC.loader.exec_module(p45)
finally:
    sys.path.pop(0)


def graph():
    return np.array([[0,2,3,0],[2,0,1,4],[3,1,0,5],[0,4,5,0]], dtype=float)


def test_completion_charges_every_partial_marginal_and_fills_unclicked_vertices():
    # Empty detector support is allowed, and cannot contain this decoded k-set.
    result = p45.complete(graph(), np.zeros(4), 2, 0, [3,1,0,2])
    assert len(result["subset"]) == 2
    assert result["marginal_evaluations"] == 3
    assert result["score_units"] == 4 and result["feasible_scores"] == 1
    subset = set(result["subset"])
    expected = sum(graph()[i,j] for i in range(4) for j in range(i+1,4)
                   if (i in subset) != (j in subset))
    assert result["cut"] == expected
    assert p45.complete(np.zeros((16,16)), np.zeros(16), 8, 1, list(range(16)))["score_units"] == 43
    assert p45.complete(np.zeros((20,20)), np.zeros(20), 10, 1, list(range(20)))["score_units"] == 66


def test_completion_is_relabel_covariant_including_ties():
    a, field, priority = graph(), np.array([1.,1.,0.,-.3]), [1,3,0,2]
    original = p45.complete(a, field, 2, 1, priority)
    permutation = np.array([2,0,3,1])
    inverse = np.argsort(permutation)
    relabeled = p45.complete(a[np.ix_(permutation,permutation)], field[permutation], 2, 1,
                            inverse[priority].tolist())
    assert relabeled["subset"] == sorted(inverse[original["subset"]].tolist())
    assert relabeled["cut"] == original["cut"]


def test_bosonic_covariance_and_hybrid_match_independent_fock_and_phase_enumeration():
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    context = p45.network(graph(), [0,1], .25, 1, 1.)
    reference = FixedPhotonObliq(4,2)
    states = np.array(reference._enumerate_all_fock_states())
    probability = abs(reference.output_state(context["u"], (1,1,0,0)))**2
    mean = probability@states
    covariance = (states-mean).T@(probability[:,None]*(states-mean))
    assert np.allclose(mean, context["mu"], atol=1e-12)
    assert np.allclose(covariance, context["cov"], atol=1e-12)
    v = context["v"]
    intensities = np.array([abs(v@z)**2 for z in itertools.product((1,-1,1j,-1j), repeat=2)])
    phase_mean = intensities.mean(axis=0)
    phase_cov = (intensities-phase_mean).T@(intensities-phase_mean)/len(intensities)
    # Independently enumerate the two labelled particles, without a covariance formula.
    d_states, d_probability = [], []
    for i,j in itertools.product(range(4), repeat=2):
        d_states.append(np.bincount([i,j], minlength=4))
        d_probability.append(abs(v[i,0])**2*abs(v[j,1])**2)
    d_states, d_probability = np.array(d_states), np.array(d_probability)
    d_mean = d_probability@d_states
    d_cov = (d_states-d_mean).T@(d_probability[:,None]*(d_states-d_mean))
    assert np.allclose(phase_mean, mean, atol=1e-12)
    assert np.allclose(d_cov+phase_cov, covariance, atol=1e-12)


def test_finite_phase_multinomial_envelope_against_independent_fock_probabilities():
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    context = p45.network(graph(), [0,1], .5, 1, 1.)
    reference = FixedPhotonObliq(4,2)
    states = reference._enumerate_all_fock_states()
    exact = abs(reference.output_state(context["u"], (1,1,0,0)))**2
    q = np.zeros(len(states))
    phases = list(itertools.product((1,-1,1j,-1j), repeat=2))
    for phase in phases:
        categorical = abs(context["v"]@phase)**2/2
        for index, occupation in enumerate(states):
            coefficient = 2/math.prod(math.factorial(n) for n in occupation)
            q[index] += coefficient*math.prod(p**n for p,n in zip(categorical,occupation))/len(phases)
    assert abs(q.sum()-1) < 1e-12
    assert np.min(q-.5*exact) >= -1e-12
