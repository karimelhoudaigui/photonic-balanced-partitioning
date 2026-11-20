"""Unit tests for fixed-photon interferometer - CORRECTED VERSION."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import (
    FixedPhotonObliq,
    FixedPhotonResult,
)


def test_initialization():
    """Test solver initialization."""
    solver = FixedPhotonObliq(4, 2)
    assert solver.n == 4
    assert solver.k == 2
    assert solver.full_dimension == 10  # C(4+2-1, 2) = C(5,2) = 10
    assert solver.cf_dimension == 6      # C(4,2) = 6


def test_odd_n_rejected():
    """Test that odd n raises an error."""
    with pytest.raises(ValueError):
        FixedPhotonObliq(5, 2)


def test_default_k():
    """Test default k = n/2."""
    solver = FixedPhotonObliq(6)
    assert solver.k == 3


def test_random_interferometer_is_unitary():
    """Test that random interferometer is unitary."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    I = U @ U.conj().T
    np.testing.assert_allclose(I, np.eye(4), atol=1e-10)


def test_input_state():
    """Test input state generation."""
    solver = FixedPhotonObliq(4, 2)
    psi = solver.input_state()
    
    assert psi.shape == (solver.full_dimension,)
    assert psi[0] == 1.0
    assert np.sum(np.abs(psi) ** 2) == 1.0


def test_output_state():
    """Test output state generation."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    psi_out = solver.output_state(U)
    
    assert psi_out.shape == (solver.full_dimension,)
    # Check normalization with tolerance for floating point
    norm = np.sum(np.abs(psi_out) ** 2)
    assert np.isclose(norm, 1.0, atol=1e-10)


def test_measure_collision_free_probability():
    """Test collision-free probability measurement.
    
    CRITICAL: P_CF should be <= 1, not necessarily 1.
    """
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    p_cf = solver.measure_collision_free_probability(U)
    assert 0 <= p_cf <= 1.0


def test_sample():
    """Test sampling from full Fock space."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    samples = solver.sample(U, num_shots=100, edges=edges, seed=42)
    
    assert len(samples) == 100
    for sample in samples:
        assert isinstance(sample, FixedPhotonResult)
        assert sum(sample.occupation_numbers) == 2  # k photons
        assert sample.is_balanced  # Always True for fixed-k


def test_sample_probabilities():
    """Test sample probabilities."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    samples = solver.sample(U, num_shots=1000, edges=edges, seed=42)
    
    for s in samples:
        assert 0 <= s.probability <= 1


def test_compute_energy():
    """Test energy computation."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    energy = solver.compute_energy(U, edges)
    assert energy >= 0


def test_optimize():
    """Test optimization."""
    solver = FixedPhotonObliq(4, 2)
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    result = solver.optimize(edges, num_iterations=10, seed=42)
    
    assert "best_energy" in result
    assert "best_interferometer" in result
    assert "energies" in result
    assert len(result["energies"]) == 11


def test_fock_dimension():
    """Test Fock space dimension calculation."""
    # m=4 modes, k=2 photons
    # Full dimension: C(4+2-1, 2) = C(5,2) = 10
    # CF dimension: C(4,2) = 6
    solver = FixedPhotonObliq(4, 2)
    assert solver.full_dimension == 10
    assert solver.cf_dimension == 6


def test_collision_states_exist():
    """Test that collision states are properly enumerated."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    cf_states = solver._enumerate_cf_states()
    
    # Check that collision states exist
    collision_states = [s for s in all_states if s not in cf_states]
    
    # For m=4 modes, k=2 photons:
    # Full dimension: C(5,2) = 10
    # CF dimension: C(4,2) = 6
    # Collision states: 10 - 6 = 4
    # But wait - let's enumerate properly
    
    # Collision states have at least one mode with n_i >= 2
    # For k=2, this means exactly one mode has 2 photons
    # States: |2,0,0,0⟩, |0,2,0,0⟩, |0,0,2,0⟩, |0,0,0,2⟩
    
    # Actually, let's verify the counts
    assert len(all_states) == 10
    assert len(cf_states) == 6
    assert len(collision_states) == 4
    
    # Verify collision states have a mode with 2 photons
    for state in collision_states:
        assert 2 in state, f"State {state} should have a mode with 2 photons"


def test_permanent_computation():
    """Test permanent computation."""
    solver = FixedPhotonObliq(4, 2)
    
    M = np.array([[1, 0], [0, 1]])
    perm = solver._permanent(M)
    assert perm == 1.0
    
    M = np.array([[0, 1], [1, 0]])
    perm = solver._permanent(M)
    assert perm == 1.0


def test_reproducibility():
    """Test that same seed gives same results."""
    solver = FixedPhotonObliq(4, 2)
    
    U1 = solver.random_interferometer(seed=42)
    U2 = solver.random_interferometer(seed=42)
    
    np.testing.assert_array_equal(U1, U2)


def test_different_seeds():
    """Test that different seeds give different results."""
    solver = FixedPhotonObliq(4, 2)
    
    U1 = solver.random_interferometer(seed=42)
    U2 = solver.random_interferometer(seed=43)
    
    assert not np.array_equal(U1, U2)
