"""Hong-Ou-Mandel effect validation tests."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


def test_hom_effect_two_photons():
    """Test Hong-Ou-Mandel effect for two photons in different modes."""
    solver = FixedPhotonObliq(4, 2)
    
    # Create 50:50 beam splitter on modes 0,1
    U = np.eye(4, dtype=complex)
    theta = np.pi / 4
    U[0, 0] = np.cos(theta)
    U[0, 1] = -np.sin(theta)
    U[1, 0] = np.sin(theta)
    U[1, 1] = np.cos(theta)
    
    # Input: |1,1,0,0⟩
    # Expected output: (|2,0,0,0⟩ - |0,2,0,0⟩)/√2
    
    p_cf = solver.measure_collision_free_probability(U)
    
    # HOM effect: P_CF should be essentially 0
    assert p_cf < 1e-10, f"HOM effect failed: P_CF = {p_cf}, expected ~0"


def test_hom_amplitude_distribution():
    """Test that HOM produces only collision states."""
    solver = FixedPhotonObliq(4, 2)
    
    U = np.eye(4, dtype=complex)
    theta = np.pi / 4
    U[0, 0] = np.cos(theta)
    U[0, 1] = -np.sin(theta)
    U[1, 0] = np.sin(theta)
    U[1, 1] = np.cos(theta)
    
    psi = solver.output_state(U)
    all_states = solver._enumerate_all_fock_states()
    cf_states = set(solver._enumerate_cf_states())
    
    # Check that all probability is in collision states
    total_cf_prob = 0.0
    total_collision_prob = 0.0
    
    for j, state in enumerate(all_states):
        prob = np.abs(psi[j]) ** 2
        if state in cf_states:
            total_cf_prob += prob
        else:
            total_collision_prob += prob
    
    assert np.isclose(total_cf_prob, 0.0, atol=1e-10)
    assert np.isclose(total_collision_prob, 1.0, atol=1e-10)


def test_hom_complex_amplitudes_and_distinguishable_coincidence():
    """Real BS convention: |11> -> (-|20>+|02>)/sqrt(2)."""
    solver = FixedPhotonObliq(2, 2)
    u = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    states = solver._enumerate_all_fock_states()
    psi = solver.output_state(u)
    assert abs(psi[states.index((2, 0))] + 1 / np.sqrt(2)) < 1e-12
    assert abs(psi[states.index((0, 2))] - 1 / np.sqrt(2)) < 1e-12
    assert abs(psi[states.index((1, 1))]) < 1e-12
    # Independent labeled-particle calculation has coincidence probability 1/2.
    p_distinct = abs(u[0, 0] * u[1, 1]) ** 2 + abs(u[0, 1] * u[1, 0]) ** 2
    assert abs(p_distinct - .5) < 1e-12


def test_hom_with_different_phases():
    """Test HOM with phase shifters."""
    solver = FixedPhotonObliq(4, 2)
    
    # BS with phase on mode 0
    phi = np.pi / 3
    U = np.eye(4, dtype=complex)
    theta = np.pi / 4
    U[0, 0] = np.cos(theta) * np.exp(1j * phi)
    U[0, 1] = -np.sin(theta) * np.exp(1j * phi)
    U[1, 0] = np.sin(theta)
    U[1, 1] = np.cos(theta)
    
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf < 1e-10


def test_hom_with_loss():
    """Test HOM with loss (should still have P_CF=0 for ideal BS)."""
    # Loss doesn't change the fact that HOM bunches photons
    # This is a conceptual test - loss model is in threshold_budget
    pass


def test_hom_with_distinguishable_photons():
    """Distinguishable photons don't bunch."""
    from photonic_balanced_partitioning.photonic.threshold_budget import ThresholdEvaluator
    
    evaluator = ThresholdEvaluator(2, 2)
    u = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    
    # Bosonic: P_CF = 0
    p_bos = evaluator.fock_probabilities(u, model='bosonic')
    states = evaluator.occupations
    cf = np.all((states == 0) | (states == 1), axis=1)
    p_cf_bos = float(p_bos[cf].sum())
    assert p_cf_bos < 1e-10
    
    # Distinguishable: P_CF = 0.5 (coincidence)
    p_dist = evaluator.fock_probabilities(u, model='distinguishable')
    p_cf_dist = float(p_dist[cf].sum())
    assert abs(p_cf_dist - 0.5) < 1e-10


def test_hom_preserves_total_photon_number():
    """HOM preserves total photon number."""
    solver = FixedPhotonObliq(4, 2)
    U = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    U = np.block([[U, np.zeros((2,2))], [np.zeros((2,2)), np.eye(2)]])
    
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    
    # All output states should have 2 photons
    for state, prob in zip(solver._enumerate_all_fock_states(), probs):
        if prob > 1e-12:
            assert sum(state) == 2


def test_hom_preserves_normalization():
    """HOM output is normalized."""
    solver = FixedPhotonObliq(4, 2)
    U = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    U = np.block([[U, np.zeros((2,2))], [np.zeros((2,2)), np.eye(2)]])
    
    psi = solver.output_state(U)
    norm = np.sum(np.abs(psi) ** 2)
    assert np.isclose(norm, 1.0, atol=1e-10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
