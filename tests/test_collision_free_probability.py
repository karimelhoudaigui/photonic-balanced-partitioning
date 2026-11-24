"""Test collision-free probability measurement."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


def test_pcf_range():
    """P_CF should always be in [0, 1]."""
    solver = FixedPhotonObliq(4, 2)
    
    for seed in range(10):
        U = solver.random_interferometer(seed=seed)
        p_cf = solver.measure_collision_free_probability(U)
        assert 0 <= p_cf <= 1.0, f"P_CF = {p_cf} not in [0,1]"


def test_pcf_identity():
    """Identity interferometer preserves input CF state."""
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf == 1.0


def test_pcf_hom():
    """HOM gives P_CF = 0."""
    solver = FixedPhotonObliq(4, 2)
    U = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    U = np.block([[U, np.zeros((2,2))], [np.zeros((2,2)), np.eye(2)]])
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf < 1e-10


def test_pcf_permutation():
    """Permutation preserves P_CF = 1."""
    solver = FixedPhotonObliq(4, 2)
    perm = [3, 0, 2, 1]
    U = np.eye(4, dtype=complex)[:, perm]
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf == 1.0


def test_pcf_phase_shifter():
    """Phase shifter preserves P_CF."""
    solver = FixedPhotonObliq(4, 2)
    phi = np.pi / 3
    U = np.eye(4, dtype=complex)
    U[0, 0] = np.exp(1j * phi)
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf == 1.0


def test_pcf_haar_average():
    """Haar average P_CF matches theory."""
    solver = FixedPhotonObliq(4, 2)
    p_cf_vals = []
    for i in range(100):
        U = solver.random_interferometer(seed=20261120 + i)
        p_cf_vals.append(solver.measure_collision_free_probability(U))
    
    mean_pcf = np.mean(p_cf_vals)
    theory = 6/10  # C(4,2)/C(5,2) = 6/10 = 0.6
    assert abs(mean_pcf - theory) < 0.05  # Within sampling error


def test_pcf_bounds():
    """P_CF bounds for various n,k."""
    test_cases = [
        (4, 2, 0.6),   # C(4,2)/C(5,2) = 6/10
        (6, 3, 20/56), # C(6,3)/C(8,3) = 20/56
        (8, 4, 70/330),# C(8,4)/C(11,4) = 70/330
    ]
    
    for n, k, theory in test_cases:
        solver = FixedPhotonObliq(n, k)
        p_cf_vals = []
        for i in range(50):
            U = solver.random_interferometer(seed=20261120 + i)
            p_cf_vals.append(solver.measure_collision_free_probability(U))
        mean_pcf = np.mean(p_cf_vals)
        assert abs(mean_pcf - theory) < 0.05, f"n={n}, k={k}: {mean_pcf} vs {theory}"


def test_pcf_cf_probabilities_sum():
    """collision_free_probabilities sum equals measure_collision_free_probability."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_cf_total = solver.measure_collision_free_probability(U)
    p_cf_array = solver.collision_free_probabilities(U)
    p_cf_sum = float(p_cf_array.sum())
    
    assert abs(p_cf_total - p_cf_sum) < 1e-12


def test_pcf_cf_probabilities_order():
    """collision_free_probabilities matches _enumerate_cf_states order."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_cf_array = solver.collision_free_probabilities(U)
    cf_states = solver._enumerate_cf_states()
    
    # Manually compute CF probabilities from full distribution
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    cf_indices = [solver._state_index[s] for s in cf_states]
    manual_p_cf = probs[cf_indices]
    
    np.testing.assert_allclose(p_cf_array, manual_p_cf, atol=1e-12, rtol=0)


def test_pcf_zero_for_bunched_input():
    """Bunched input through identity has P_CF = 0."""
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    
    # Input |2,0,0,0⟩ is collision state
    psi = solver.output_state(U, input_occupation=(2,0,0,0))
    probs = np.abs(psi) ** 2
    cf_mask = np.all((np.array(solver._enumerate_all_fock_states()) == 0) | 
                     (np.array(solver._enumerate_all_fock_states()) == 1), axis=1)
    p_cf = probs[cf_mask].sum()
    assert p_cf == 0.0


def test_pcf_one_for_cf_input():
    """CF input through identity has P_CF = 1."""
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    
    # Input |1,1,0,0⟩ is CF state
    psi = solver.output_state(U, input_occupation=(1,1,0,0))
    probs = np.abs(psi) ** 2
    cf_mask = np.all((np.array(solver._enumerate_all_fock_states()) == 0) | 
                     (np.array(solver._enumerate_all_fock_states()) == 1), axis=1)
    p_cf = probs[cf_mask].sum()
    assert p_cf == 1.0


def test_pcf_cf_probabilities_sum():
    """collision_free_probabilities sum equals measure_collision_free_probability."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_cf_total = solver.measure_collision_free_probability(U)
    p_cf_array = solver.collision_free_probabilities(U)
    p_cf_sum = float(p_cf_array.sum())
    
    assert abs(p_cf_total - p_cf_sum) < 1e-12


def test_pcf_cf_probabilities_order():
    """collision_free_probabilities matches _enumerate_cf_states order."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_cf_array = solver.collision_free_probabilities(U)
    cf_states = solver._enumerate_cf_states()
    
    # Manually compute CF probabilities from full distribution
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    cf_indices = [solver._state_index[s] for s in cf_states]
    manual_p_cf = probs[cf_indices]
    
    np.testing.assert_allclose(p_cf_array, manual_p_cf, atol=1e-12, rtol=0)


def test_pcf_zero_for_bunched_input_via_output_state():
    """Bunched input through identity has P_CF = 0 (via output_state)."""
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    
    # Input |2,0,0,0⟩ is collision state
    psi = solver.output_state(U, input_occupation=(2,0,0,0))
    probs = np.abs(psi) ** 2
    cf_mask = np.all((np.array(solver._enumerate_all_fock_states()) == 0) | 
                     (np.array(solver._enumerate_all_fock_states()) == 1), axis=1)
    p_cf = probs[cf_mask].sum()
    assert p_cf == 0.0


def test_pcf_one_for_cf_input_via_output_state():
    """CF input through identity has P_CF = 1 (via output_state)."""
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    
    # Input |1,1,0,0⟩ is CF state
    psi = solver.output_state(U, input_occupation=(1,1,0,0))
    probs = np.abs(psi) ** 2
    cf_mask = np.all((np.array(solver._enumerate_all_fock_states()) == 0) | 
                     (np.array(solver._enumerate_all_fock_states()) == 1), axis=1)
    p_cf = probs[cf_mask].sum()
    assert p_cf == 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
