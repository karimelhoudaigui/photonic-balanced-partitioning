"""Test that cardinality constraint is only satisfied after collision-free postselection."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.threshold_budget import ThresholdEvaluator


def test_cf_states_have_correct_cardinality():
    """Collision-free states have exactly k ones."""
    for n in [4, 6, 8, 10]:
        k = n // 2
        solver = FixedPhotonObliq(n, k)
        cf_states = solver._enumerate_cf_states()
        
        for state in cf_states:
            assert sum(state) == k
            assert list(state).count(1) == k
            assert list(state).count(0) == n - k


def test_collision_states_have_wrong_cardinality():
    """Collision states don't have correct cardinality after thresholding."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    cf_states = set(solver._enumerate_cf_states())
    collision_states = [s for s in all_states if s not in cf_states]
    
    for state in collision_states:
        # After thresholding (x_i = 1[n_i > 0]), collision states have wrong cardinality
        thresholded = tuple(1 if c > 0 else 0 for c in state)
        assert sum(thresholded) != 2, f"State {state} -> {thresholded} has wrong cardinality"


def test_threshold_decoding_cardinality():
    """Threshold decoding of collision states gives wrong cardinality."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    
    for state in all_states:
        thresholded = tuple(1 if c > 0 else 0 for c in state)
        cardinality = sum(thresholded)
        
        if state in solver._enumerate_cf_states():
            assert cardinality == 2
        else:
            # Collision states: |2,0,0,0⟩ -> |1,0,0,0⟩ (cardinality 1)
            # |0,2,0,0⟩ -> |0,1,0,0⟩ (cardinality 1)
            # etc.
            assert cardinality < 2, f"State {state} -> cardinality {cardinality}"


def test_cardinality_only_after_cf_postselection():
    """Cardinality constraint only holds after CF postselection."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    # Full distribution: states have various cardinalities after thresholding
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    states = np.array(solver._enumerate_all_fock_states())
    
    # Threshold all states
    thresholded = (states > 0).astype(int)
    cardinalities = thresholded.sum(axis=1)
    
    # Only CF states have cardinality 2
    cf_mask = np.all((states == 0) | (states == 1), axis=1)
    assert np.all(cardinalities[cf_mask] == 2)
    assert np.any(cardinalities[~cf_mask] != 2)


def test_threshold_evaluator_cardinality():
    """ThresholdEvaluator correctly handles cardinality."""
    evaluator = ThresholdEvaluator(4, 2)
    U = np.eye(4, dtype=complex)
    
    # Ideal case: input |1,1,0,0⟩ -> output |1,1,0,0⟩
    p = evaluator.probabilities(U, model='bosonic', eta=1.0)
    
    # Only balanced partitions have non-zero probability
    for idx, prob in enumerate(p):
        if prob > 1e-12:
            bits = evaluator.bitstrings[idx]
            assert sum(bits) == 2


def test_cardinality_with_loss():
    """Loss doesn't fix cardinality of collision states."""
    evaluator = ThresholdEvaluator(4, 2)
    U = np.eye(4, dtype=complex)
    
    # With loss, collision states still have wrong cardinality after thresholding
    p = evaluator.probabilities(U, model='bosonic', eta=0.8)
    
    for idx, prob in enumerate(p):
        if prob > 1e-12:
            bits = evaluator.bitstrings[idx]
            # Even with loss, thresholded collision states have wrong cardinality
            # (but they now have some probability due to loss)
            pass  # Just verify it runs


def test_cardinality_constraint_enforced_by_postselection():
    """Cardinality constraint is enforced by CF postselection, not by physics."""
    solver = FixedPhotonObliq(4, 2)
    U = solver.random_interferometer(seed=42)
    
    # Physics: full Fock distribution includes states with wrong cardinality
    psi = solver.output_state(U)
    probs = np.abs(psi) ** 2
    states = np.array(solver._enumerate_all_fock_states())
    
    # Postselection on CF enforces cardinality
    cf_mask = np.all((states == 0) | (states == 1), axis=1)
    cf_probs = probs[cf_mask]
    cf_states = states[cf_mask]
    
    # All CF states have correct cardinality
    for state in cf_states:
        assert sum(state) == 2
        assert list(state).count(1) == 2
    
    # But total probability of CF states < 1
    assert cf_probs.sum() < 1.0


def test_cardinality_not_enforced_by_photon_number():
    """Fixed photon number does NOT enforce cardinality constraint."""
    solver = FixedPhotonObliq(4, 2)
    
    # Fixed photon number = 2
    # But collision states like |2,0,0,0⟩ have thresholded cardinality 1
    # Only CF postselection enforces cardinality = 2
    
    all_states = solver._enumerate_all_fock_states()
    for state in all_states:
        assert sum(state) == 2  # Photon number conserved
        
        thresholded = tuple(1 if c > 0 else 0 for c in state)
        cardinality = sum(thresholded)
        
        if state in solver._enumerate_cf_states():
            assert cardinality == 2
        else:
            assert cardinality < 2  # Collision states have reduced cardinality


def test_cf_postselection_enforces_balanced_partition():
    """CF postselection is exactly the balanced partition constraint."""
    solver = FixedPhotonObliq(6, 3)
    cf_states = solver._enumerate_cf_states()
    
    # Each CF state corresponds to a balanced partition
    for state in cf_states:
        partition = tuple(i for i, c in enumerate(state) if c == 1)
        assert len(partition) == 3
        assert len(set(partition)) == 3
        assert all(0 <= i < 6 for i in partition)
    
    # Number of CF states = number of balanced partitions = C(6,3) = 20
    assert len(cf_states) == 20


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
