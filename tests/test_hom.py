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


def test_identity_interferometer():
    """Test identity interferometer preserves input state."""
    solver = FixedPhotonObliq(4, 2)
    
    U = np.eye(4, dtype=complex)
    psi = solver.output_state(U)
    
    # Input state is |1,1,0,0⟩ which is at index 8 in the enumeration
    # For identity, output should equal input
    input_idx = 8  # (1,1,0,0)
    assert np.isclose(np.abs(psi[input_idx]), 1.0, atol=1e-10)


def test_phase_shifter():
    """Test phase shifter adds phase to specific mode."""
    solver = FixedPhotonObliq(4, 2)
    
    # Phase shifter on mode 0
    phi = np.pi / 2
    U = np.eye(4, dtype=complex)
    U[0, 0] = np.exp(1j * phi)
    
    psi = solver.output_state(U)
    
    # Should still be normalized
    assert np.isclose(np.sum(np.abs(psi) ** 2), 1.0, atol=1e-10)


def test_permanent_normalization():
    """Test that permanent computation is correct."""
    solver = FixedPhotonObliq(4, 2)
    
    # Test with simple 2x2 matrix
    M = np.array([[1, 0], [0, 1]])
    perm = solver._permanent(M)
    assert np.isclose(perm, 1.0)
    
    # Test with swap matrix
    M = np.array([[0, 1], [1, 0]])
    perm = solver._permanent(M)
    assert np.isclose(perm, 1.0)
