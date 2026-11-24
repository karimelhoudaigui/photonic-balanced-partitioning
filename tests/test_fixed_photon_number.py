"""Test fixed photon number conservation."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.threshold_budget import ThresholdEvaluator


def test_total_photon_number_conserved():
    """Total photon number is conserved in output distribution."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    psi = solver.output_state(U)
    
    # All states in distribution have exactly k photons
    for state, amp in zip(solver._enumerate_all_fock_states(), psi):
        prob = abs(amp) ** 2
        if prob > 1e-12:
            assert sum(state) == 2, f"State {state} has {sum(state)} photons, expected 2"


def test_total_photon_number_conserved_for_all_nk():
    """Test photon number conservation for various n,k (n must be even)."""
    for n in range(2, 8, 2):  # Only even n
        for k in range(1, n+1):
            solver = FixedPhotonObliq(n, k)
            U = solver.random_interferometer(seed=42)
            psi = solver.output_state(U)
            
            for state, amp in zip(solver._enumerate_all_fock_states(), psi):
                prob = abs(amp) ** 2
                if prob > 1e-12:
                    assert sum(state) == k, f"n={n}, k={k}: state {state} has {sum(state)} photons"


def test_input_photon_number():
    """Input state has exactly k photons."""
    for n in range(2, 8, 2):  # Only even n
        for k in range(0, n+1):
            solver = FixedPhotonObliq(n, k)
            psi_in = solver.input_state()
            
            # Input state should have exactly k photons
            for state, amp in zip(solver._enumerate_all_fock_states(), psi_in):
                prob = abs(amp) ** 2
                if prob > 1e-12:
                    assert sum(state) == k


def test_photon_number_conserved_through_unitary():
    """Photon number conserved through any unitary."""
    solver = FixedPhotonObliq(6, 3)
    
    # Test various unitaries
    for seed in [42, 123, 456, 789]:
        U = solver.random_interferometer(seed=seed)
        psi = solver.output_state(U)
        
        # Check normalization
        norm = np.sum(np.abs(psi) ** 2)
        assert np.isclose(norm, 1.0, atol=1e-9)
        
        # Check photon number
        for state, amp in zip(solver._enumerate_all_fock_states(), psi):
            prob = abs(amp) ** 2
            if prob > 1e-12:
                assert sum(state) == 3


def test_photon_number_conserved_with_loss():
    """Test photon number with loss model (threshold_budget)."""
    evaluator = ThresholdEvaluator(4, 2)
    U = np.eye(4, dtype=complex)
    
    # No loss: total probability = 1
    p = evaluator.fock_probabilities(U, model='bosonic')
    assert abs(p.sum() - 1.0) < 1e-9
    
    # With loss: total probability still 1 (loss before thresholding)
    p_loss = evaluator.probabilities(U, model='bosonic', eta=0.8)
    assert abs(p_loss.sum() - 1.0) < 1e-9
    
    # After thresholding: probabilities sum to 1
    p_thresh = evaluator.probabilities(U, model='bosonic', eta=0.8)
    assert abs(p_thresh.sum() - 1.0) < 1e-9


def test_photon_number_in_collision_states():
    """Collision states also have correct photon number."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    cf_states = set(solver._enumerate_cf_states())
    collision_states = [s for s in all_states if s not in cf_states]
    
    for state in collision_states:
        assert sum(state) == 2
        assert any(c > 1 for c in state)


def test_photon_number_conserved_in_sampling():
    """Sampled states have correct photon number."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    
    samples = solver.sample(U, num_shots=1000, edges=edges, seed=42)
    
    for sample in samples:
        assert sum(sample.occupation_numbers) == 2


def test_vacuum_state():
    """Vacuum state (k=0) has 0 photons."""
    solver = FixedPhotonObliq(4, 0)
    assert solver.k == 0
    assert solver.full_dimension == 1
    assert solver.cf_dimension == 1
    
    U = np.eye(4, dtype=complex)
    psi = solver.output_state(U)
    assert len(psi) == 1
    assert abs(psi[0] - 1.0) < 1e-12
    
    # Vacuum is CF
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf == 1.0


def test_photon_number_conserved_with_phase_shifters():
    """Phase shifters preserve photon number."""
    solver = FixedPhotonObliq(4, 2)
    
    # Random phases
    phases = np.random.default_rng(42).uniform(0, 2*np.pi, 4)
    U = np.diag(np.exp(1j * phases))
    
    psi = solver.output_state(U)
    for state, amp in zip(solver._enumerate_all_fock_states(), psi):
        prob = abs(amp) ** 2
        if prob > 1e-12:
            assert sum(state) == 2


def test_photon_number_conserved_with_permutation():
    """Permutation preserves photon number."""
    solver = FixedPhotonObliq(6, 3)
    perm = [3, 5, 1, 0, 2, 4]
    U = np.eye(6, dtype=complex)[:, perm]
    
    psi = solver.output_state(U)
    for state, amp in zip(solver._enumerate_all_fock_states(), psi):
        prob = abs(amp) ** 2
        if prob > 1e-12:
            assert sum(state) == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
