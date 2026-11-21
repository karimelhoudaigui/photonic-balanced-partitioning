"""New static optical component: analytic physics, original loss and Perceval."""
from itertools import product
import numpy as np
import pytest
import perceval as pcvl

from photonic_balanced_partitioning.photonic.optical_penalty import (
    OpticalPenaltyAnchor, coupling_angle, penalty_qubo, rx_beamsplitter)


@pytest.mark.parametrize('a', [0.,.25,.5,.75,1.])
@pytest.mark.parametrize('variant', ['literal_archive','corrected_physics'])
def test_two_photon_coincidence_and_complete_distribution(a, variant):
    anchor=OpticalPenaltyAnchor([[0.,a],[a,1.]],repeats=1,variant=variant)
    probabilities=anchor.fock_probabilities()
    expected=.5*(1+np.sqrt(1-a)) if variant=='literal_archive' else 1-a
    assert probabilities[(1,1)]==pytest.approx(expected,abs=1e-12)
    assert probabilities[(2,0)]==pytest.approx((1-expected)/2,abs=1e-12)
    assert probabilities[(0,2)]==pytest.approx((1-expected)/2,abs=1e-12)
    assert sum(probabilities.values())==pytest.approx(1.,abs=1e-12)
    beta=coupling_angle(a,1,variant)
    np.testing.assert_allclose(rx_beamsplitter(beta),np.asarray(pcvl.BS.Rx(theta=beta).compute_unitary(),complex),atol=1e-12)


@pytest.mark.parametrize('repeats', [1,2,10])
@pytest.mark.parametrize('variant', ['literal_archive','corrected_physics'])
def test_complete_static_component_against_perceval(repeats,variant):
    q=np.array([[0.,-2.,.2,1.],[-2.,0.,.7,.4],[.2,.7,0.,-.8],[1.,.4,-.8,0.]])
    anchor=OpticalPenaltyAnchor(q,repeats,variant)
    circuit=anchor.to_perceval()
    np.testing.assert_allclose(anchor.unitary(),np.asarray(circuit.compute_unitary(),complex),atol=1e-12)
    backend=pcvl.SLOSBackend();backend.set_circuit(circuit)
    for source in [(1,1,1,1),(2,0,1,0),(0,0,0,0)]:
        backend.set_input_state(pcvl.BasicState(source));reference=backend.prob_distribution()
        actual=anchor.fock_probabilities(source)
        assert sum(actual.values())==pytest.approx(1.,abs=1e-12)
        for state,p in actual.items():assert p==pytest.approx(reference.get(pcvl.BasicState(state),0.),abs=1e-11)
        assert sum(anchor.threshold_probabilities(source).values())==pytest.approx(1.,abs=1e-12)


def test_penalty_qubo_retains_original_cut_and_cardinality_on_entire_cube():
    adjacency=np.array([[0.,1.,0.,2.],[1.,0.,3.,0.],[0.,3.,0.,.5],[2.,0.,.5,0.]])
    q,constant=penalty_qubo(adjacency,17.)
    for bits in product((0,1),repeat=4):
        x=np.array(bits);cut=sum(adjacency[i,j] for i in range(4) for j in range(i+1,4) if bits[i]!=bits[j])
        assert x@q@x+constant==pytest.approx(cut+17*(sum(bits)-2)**2)
    anchor=OpticalPenaltyAnchor(q,repeats=2)
    independent=sum(p*(np.asarray(bits)@q@np.asarray(bits)) for bits,p in anchor.threshold_probabilities().items())
    assert anchor.expected_original_qubo()==pytest.approx(independent,abs=1e-12)


def test_endpoint_mismatch_is_not_silently_corrected():
    archive=OpticalPenaltyAnchor([[0.,1.],[1.,0.]],1,'literal_archive')
    corrected=OpticalPenaltyAnchor([[0.,1.],[1.,0.]],1,'corrected_physics')
    assert archive.fock_probabilities()[(1,1)]==pytest.approx(.5)
    assert corrected.fock_probabilities()[(1,1)]==pytest.approx(0.,abs=1e-12)
