from fractions import Fraction
import math
import numpy as np
import pytest
from photonic_balanced_partitioning.photonic.threshold_budget import (
    ThresholdEvaluator,haar_click_probability,haar_click_probability_loss,
    haar_loss_coefficient_formula,optimal_photon_numbers)


@pytest.mark.parametrize('m,N',[(2,0),(2,2),(4,2),(4,4),(6,6),(8,5)])
def test_exact_occupancy_law_normalizes(m,N):
    assert sum(haar_click_probability(m,N,k) for k in range(m+1))==1


@pytest.mark.parametrize('m',[4,6,8,10,12,20])
def test_balanced_haar_photon_optimum_and_central_binomial(m):
    k=m//2
    assert optimal_photon_numbers(m,k)==(m-2,m-1)
    assert haar_click_probability(m,m,k)==Fraction(math.comb(m,k)**2,math.comb(2*m,m))


@pytest.mark.parametrize('eta',[0.,.1,.5,.9,1.])
def test_two_independent_loss_formulae(eta):
    for m in [2,4,6]:
        for N in range(m+1):
            values=[haar_click_probability_loss(m,N,k,eta) for k in range(m+1)]
            assert abs(sum(values)-1)<1e-12
            np.testing.assert_allclose(values,[haar_loss_coefficient_formula(m,N,k,eta) for k in range(m+1)],atol=1e-12)


def test_threshold_identity_and_hom_collisions_are_not_discarded():
    ev=ThresholdEvaluator(4,4)
    p=ev.probabilities(np.eye(4))
    assert p[-1]==1 and p.sum()==1
    U=np.kron(np.eye(2),np.array([[1.,-1.],[1.,1.]])/np.sqrt(2))
    b,d=ev.probabilities(U),ev.probabilities(U,'distinguishable')
    balanced=ev.bitstrings.sum(axis=1)==2
    assert abs(b[balanced].sum()-1)<1e-12
    assert abs(d[balanced].sum()-.25)<1e-12
    assert np.count_nonzero(b>1e-12)==4


def test_loss_transition_independently_of_coefficient_average():
    ev=ThresholdEvaluator(4,2)
    for eta in [.2,.6,.95]:
        p=ev.probabilities(np.eye(4),eta=eta)
        # Separate independently surviving occupied modes; initially no photons
        # in modes2/3. Binary indices1100=12,1000=8,0100=4,0000=0.
        expected=np.zeros(16);expected[12]=eta**2
        expected[8]=expected[4]=eta*(1-eta);expected[0]=(1-eta)**2
        np.testing.assert_allclose(p,expected,atol=1e-14)


def test_perceval_threshold_full_occupation_crosscheck():
    pcvl=pytest.importorskip('perceval')
    ev=ThresholdEvaluator(4,4);U=ev.solver.random_interferometer(55215)
    backend=pcvl.SLOSBackend()
    backend.set_circuit(pcvl.Circuit(4).add(0,pcvl.Unitary(pcvl.Matrix(U))))
    backend.set_input_state(pcvl.BasicState([1,1,1,1]))
    expected=np.array([float(backend.probability(pcvl.BasicState(list(t)))) for t in ev.occupations])
    np.testing.assert_allclose(ev.fock_probabilities(U),expected,atol=1e-11)
    np.testing.assert_allclose(ev.probabilities(U),np.bincount(ev.binary_indices,weights=expected,minlength=16),atol=1e-11)
