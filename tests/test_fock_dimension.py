"""Test Fock space dimension calculations: full vs collision-free."""

import pytest
import math
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq


@pytest.mark.parametrize('n,k,full_dim,cf_dim', [
    (2, 1, 2, 2),      # C(2,1)=2, C(2,1)=2
    (2, 2, 3, 1),      # C(3,2)=3, C(2,2)=1
    (4, 2, 10, 6),     # C(5,2)=10, C(4,2)=6
    (4, 3, 20, 4),     # C(6,3)=20, C(4,3)=4
    (6, 3, 56, 20),    # C(8,3)=56, C(6,3)=20
    (8, 4, 330, 70),   # C(11,4)=330, C(8,4)=70
    (10, 5, 2002, 252), # C(14,5)=2002, C(10,5)=252
    (12, 6, 12376, 924), # C(17,6)=12376, C(12,6)=924
])
def test_fock_dimensions(n, k, full_dim, cf_dim):
    """Test that full and collision-free dimensions match theoretical values."""
    solver = FixedPhotonObliq(n, k)
    assert solver.full_dimension == full_dim, f"n={n}, k={k}: full_dim={solver.full_dimension} != {full_dim}"
    assert solver.cf_dimension == cf_dim, f"n={n}, k={k}: cf_dim={solver.cf_dimension} != {cf_dim}"


def test_fock_dimension_formula():
    """Test dimension formula directly."""
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import _fock_states
    
    # Test small cases exhaustively
    for n in range(2, 8):
        for k in range(0, n+1):
            states = _fock_states(n, k)
            expected_full = math.comb(n + k - 1, k) if k > 0 else 1
            expected_cf = math.comb(n, k) if k <= n else 0
            assert len(states) == expected_full, f"n={n}, k={k}: {len(states)} != {expected_full}"
            
            # Count CF states
            cf_count = sum(1 for s in states if all(c <= 1 for c in s))
            assert cf_count == expected_cf, f"n={n}, k={k}: CF={cf_count} != {expected_cf}"


def test_collision_states_count():
    """Test that collision states = full - CF."""
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import _fock_states
    
    for n in range(2, 8):
        for k in range(1, n+1):
            states = _fock_states(n, k)
            full = len(states)
            cf = sum(1 for s in states if all(c <= 1 for c in s))
            collision = full - cf
            
            # For k=2, collision states should have exactly one mode with 2 photons
            if k == 2:
                assert collision == n, f"n={n}, k=2: collision={collision} != n={n}"
                # Verify each collision state has exactly one mode with 2 photons
                for s in _fock_states(n, k):
                    if any(c > 1 for c in s):
                        assert sum(1 for c in s if c > 1) == 1
                        assert max(s) == 2


def test_balanced_partition_dimension():
    """Test that CF dimension equals number of balanced partitions."""
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    from itertools import combinations
    
    for n in [4, 6, 8, 10]:
        k = n // 2
        solver = FixedPhotonObliq(n, k)
        expected_partitions = math.comb(n, k)
        assert solver.cf_dimension == expected_partitions
        
        # Verify each CF state corresponds to a unique balanced partition
        cf_states = solver._enumerate_cf_states()
        partitions = set()
        for state in cf_states:
            partition = tuple(i for i, c in enumerate(state) if c == 1)
            partitions.add(partition)
        assert len(partitions) == expected_partitions


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
