"""Test collision state enumeration and properties."""

import pytest
import numpy as np
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


def test_collision_states_exist_for_k2():
    """For k=2, collision states have exactly one mode with 2 photons."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    cf_states = set(solver._enumerate_cf_states())
    collision_states = [s for s in all_states if s not in cf_states]
    
    # For n=4, k=2: 4 collision states
    assert len(collision_states) == 4
    
    # Each collision state has exactly one mode with 2 photons
    for state in collision_states:
        assert sum(1 for c in state if c > 1) == 1
        assert max(state) == 2
        assert sum(state) == 2


def test_collision_states_exist_for_k3():
    """For k=3, collision states have various collision patterns."""
    solver = FixedPhotonObliq(4, 3)
    all_states = solver._enumerate_all_fock_states()
    cf_states = set(solver._enumerate_cf_states())
    collision_states = [s for s in all_states if s not in cf_states]
    
    # For n=4, k=3: full=20, CF=4, collision=16
    assert len(collision_states) == 16
    
    # Collision patterns for k=3:
    # - One mode with 3 photons: |3,0,0,0⟩ etc (4 states)
    # - One mode with 2, one with 1: |2,1,0,0⟩ etc (12 states)
    for state in collision_states:
        assert sum(state) == 3
        assert any(c > 1 for c in state)


def test_collision_states_general():
    """Test collision state properties for various n,k."""
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import _fock_states
    
    for n in range(2, 8):
        for k in range(1, n+1):
            states = _fock_states(n, k)
            cf_states = [s for s in states if all(c <= 1 for c in s)]
            collision_states = [s for s in states if any(c > 1 for c in s)]
            
            # All states accounted for
            assert len(states) == len(cf_states) + len(collision_states)
            
            # CF states have only 0/1
            for s in cf_states:
                assert all(c in (0, 1) for c in s)
                assert sum(s) == k
            
            # Collision states have at least one c > 1
            for s in collision_states:
                assert any(c > 1 for c in s)
                assert sum(s) == k


def test_collision_state_enumeration_order():
    """Test that collision states are properly ordered in enumeration."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    
    # Lexicographic order for weak compositions
    expected_order = [
        (0, 0, 0, 2),
        (0, 0, 1, 1),
        (0, 0, 2, 0),
        (0, 1, 0, 1),
        (0, 1, 1, 0),
        (0, 2, 0, 0),
        (1, 0, 0, 1),
        (1, 0, 1, 0),
        (1, 1, 0, 0),
        (2, 0, 0, 0),
    ]
    assert all_states == expected_order


def test_collision_free_states_are_balanced_partitions():
    """CF states correspond exactly to balanced partitions."""
    solver = FixedPhotonObliq(6, 3)
    cf_states = solver._enumerate_cf_states()
    
    # Each CF state has exactly 3 ones and 3 zeros
    for state in cf_states:
        assert sum(state) == 3
        assert all(c in (0, 1) for c in state)
        assert state.count(1) == 3
    
    # Number of CF states = C(6,3) = 20
    assert len(cf_states) == 20
    
    # Each corresponds to a unique 3-element subset
    partitions = set()
    for state in cf_states:
        partition = tuple(i for i, c in enumerate(state) if c == 1)
        assert len(partition) == 3
        partitions.add(partition)
    assert len(partitions) == 20


def test_collision_state_indexing():
    """Test that collision states have correct indices."""
    solver = FixedPhotonObliq(4, 2)
    all_states = solver._enumerate_all_fock_states()
    
    # Collision states should be at specific indices
    collision_indices = [i for i, s in enumerate(all_states) if any(c > 1 for c in s)]
    assert collision_indices == [0, 2, 5, 9]  # |2,0,0,0⟩, |0,0,2,0⟩, |0,2,0,0⟩, |2,0,0,0⟩


def test_collision_probability_computation():
    """Test that collision probability is computed correctly."""
    solver = FixedPhotonObliq(4, 2)
    
    # Identity: input is CF, so P_CF = 1
    U = np.eye(4, dtype=complex)
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf == 1.0
    
    # HOM: P_CF = 0
    U = np.array([[1, -1], [1, 1]], dtype=complex) / np.sqrt(2)
    U = np.block([[U, np.zeros((2,2))], [np.zeros((2,2)), np.eye(2)]])
    p_cf = solver.measure_collision_free_probability(U)
    assert p_cf < 1e-10


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
