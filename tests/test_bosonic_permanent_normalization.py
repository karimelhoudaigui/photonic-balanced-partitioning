"""Test bosonic permanent with factorial normalization for collisions."""

import pytest
import numpy as np
import math
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


def test_permanent_with_factorial_normalization():
    """Test that permanent includes factorial normalization for repeated rows/cols."""
    solver = FixedPhotonObliq(4, 2)
    
    # Input: |1,1,0,0⟩, Output: |2,0,0,0⟩
    # Rows: [0,0], Cols: [0,1]
    # M = [[U[0,0], U[0,1]], [U[0,0], U[0,1]]]
    # Per(M) = U[0,0]*U[0,1] - U[0,1]*U[0,0] = 0
    # Norm = sqrt(1!*1! * 2!*0!) = sqrt(2)
    # Amplitude = 0 / sqrt(2) = 0
    
    U = np.eye(4, dtype=complex)
    amp = solver._compute_amplitude(U, (1,1,0,0), (2,0,0,0))
    assert abs(amp) < 1e-12


def test_permanent_normalization_collision_output():
    """Test normalization for collision output states."""
    solver = FixedPhotonObliq(4, 2)
    
    # Input: |1,1,0,0⟩, Output: |1,1,0,0⟩ (CF)
    # Rows: [0,1], Cols: [0,1]
    # M = [[U[0,0], U[0,1]], [U[1,0], U[1,1]]]
    # Norm = sqrt(1!*1! * 1!*1!) = 1
    
    U = np.eye(4, dtype=complex)
    amp = solver._compute_amplitude(U, (1,1,0,0), (1,1,0,0))
    assert abs(amp - 1.0) < 1e-12


def test_permanent_normalization_three_photons():
    """Test normalization for three photons with collisions."""
    solver = FixedPhotonObliq(4, 3)
    
    # Input: |1,1,1,0⟩, Output: |3,0,0,0⟩
    # Rows: [0,0,0], Cols: [0,1,2]
    # M = 3x3 with rows all [U[0,0], U[0,1], U[0,2]]
    # Per(M) = 0 (rows identical)
    # Norm = sqrt(1!*1!*1! * 3!*0!*0!) = sqrt(6)
    
    U = np.eye(4, dtype=complex)
    amp = solver._compute_amplitude(U, (1,1,1,0), (3,0,0,0))
    assert abs(amp) < 1e-12


def test_permanent_normalization_collision_to_collision():
    """Test normalization for collision-to-collision transition with identity.
    
    For input |2,0,0,0⟩ and output |2,0,0,0⟩ with identity:
    - The state is unchanged, so amplitude should be 1.0
    - The permanent formula with repeated rows gives 0, but the actual
      output_state method handles this correctly via _amplitudes.
    """
    solver = FixedPhotonObliq(4, 2)
    U = np.eye(4, dtype=complex)
    amp = solver._compute_amplitude(U, (2,0,0,0), (2,0,0,0))
    # For identity, the state is unchanged, so amplitude = 1.0
    assert abs(amp - 1.0) < 1e-12


def test_hom_permanent_normalization():
    """Test HOM effect with correct normalization.
    
    For 50:50 BS: U = [[1,-1],[1,1]]/sqrt(2)
    Input: |1,1⟩, Output: |2,0⟩
    Rows: [0,0], Cols: [0,1]
    M = [[1/sqrt(2), -1/sqrt(2)], [1/sqrt(2), -1/sqrt(2)]]
    Per(M) = (1/sqrt(2))*(-1/sqrt(2)) - (-1/sqrt(2))*(1/sqrt(2)) = -1/2 + 1/2 = 0
    Norm = sqrt(1!*1! * 2!*0!) = sqrt(2)
    Amplitude = 0
    
    Output |0,2⟩:
    Rows: [1,1], Cols: [0,1]
    Same permanent = 0
    
    The HOM effect: P_CF = 0 (no |1,1⟩ output), but collision states
    |2,0⟩ and |0,2⟩ each have amplitude 1/√2.
    """
    solver = FixedPhotonObliq(2, 2)
    u = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    
    # Test that collision-free probability is 0
    p_cf = solver.measure_collision_free_probability(u)
    assert p_cf < 1e-12
    
    # Test that collision states have correct amplitudes
    psi = solver.output_state(u)
    states = solver._enumerate_all_fock_states()
    probs = np.abs(psi) ** 2
    
    # |2,0⟩ and |0,2⟩ should each have probability 0.5
    idx_20 = states.index((2, 0))
    idx_02 = states.index((0, 2))
    assert abs(probs[idx_20] - 0.5) < 1e-12
    assert abs(probs[idx_02] - 0.5) < 1e-12
    
    # |1,1⟩ should have probability 0
    idx_11 = states.index((1, 1))
    assert probs[idx_11] < 1e-12


def test_full_distribution_normalization():
    """Test that full distribution sums to 1."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    assert abs(probs.sum() - 1.0) < 1e-9


def test_cf_subset_normalization():
    """Test that CF subset probabilities match collision_free_probabilities."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_full = np.abs(solver.output_state(U)) ** 2
    p_cf = solver.collision_free_probabilities(U)
    
    cf_indices = [solver._state_index[s] for s in solver._enumerate_cf_states()]
    p_cf_from_full = p_full[cf_indices]
    
    np.testing.assert_allclose(p_cf, p_cf_from_full, atol=1e-12, rtol=0)


def test_three_photon_phase_normalization():
    """Test that three-photon phase doesn't have global sign flip."""
    solver = FixedPhotonObliq(4, 3)
    phases = np.array([.17, -.3, .61, .8])
    U = np.diag(np.exp(1j * phases))
    
    actual = solver.output_state(U)
    expected = solver.input_state() * np.exp(1j * phases[:3].sum())
    np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)


def test_collisional_input_multinomial():
    """Test collisional input gives multinomial distribution."""
    solver = FixedPhotonObliq(4, 3)
    U = solver.random_interferometer(seed=19)
    
    p = abs(solver.output_state(U, input_occupation=(3, 0, 0, 0))) ** 2
    for state, prob in zip(solver._enumerate_all_fock_states(), p):
        expected = math.factorial(3) / math.prod(math.factorial(c) for c in state)
        expected *= math.prod(abs(U[j, 0]) ** (2 * state[j]) for j in range(4))
        assert abs(prob - expected) < 1e-12


def test_identity_normalization():
    """Test identity interferometer preserves normalization."""
    for n, k in [(4, 2), (6, 3)]:
        solver = FixedPhotonObliq(n, k)
        psi = solver.output_state(np.eye(n, dtype=complex))
        assert abs(np.sum(np.abs(psi) ** 2) - 1.0) < 1e-12


def test_invalid_unitary_rejected():
    """Test that invalid unitaries are rejected, not silently renormalized."""
    solver = FixedPhotonObliq(4, 2)
    
    with pytest.raises(ValueError):
        solver.output_state(np.zeros((4, 4)))
    
    with pytest.raises(ValueError):
        solver.output_state(np.eye(3))
    
    with pytest.raises(ValueError):
        solver.output_state(np.full((4, 4), np.nan))


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
