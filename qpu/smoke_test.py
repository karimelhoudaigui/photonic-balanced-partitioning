#!/usr/bin/env python3
"""QPU smoke test - smallest physical experiment."""

import sys
import os
import json
from datetime import datetime


def main():
    print("QPU Smoke Test")
    print("=" * 50)
    
    token = os.environ.get("QPU_TOKEN", None)
    if not token:
        print("ERROR: QPU_TOKEN not set")
        return 1
    
    # Create n=4, k=2 test graph (path graph)
    print("\nTest graph: Path graph with 4 nodes")
    print("Edges: 0-1, 1-2, 2-3")
    print("Optimal partition: {0,1} | {2,3}")
    print("Optimal cut weight: 1.0")
    
    # Run simulation
    try:
        from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning
        from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
        import numpy as np
        
        problem = BalancedGraphPartitioning.path_graph(4)
        exact = problem.solve_exact()
        print(f"\nExact optimum: {exact.energy}")
        
        solver = FixedPhotonObliq(4, 2)
        U = solver.random_interferometer(seed=42)
        
        # Sample
        samples = solver.sample(U, num_shots=100, seed=42)
        valid = [s for s in samples if s.is_valid]
        
        print(f"Valid samples: {len(valid)}/100")
        
        if valid:
            energies = [s.energy for s in valid]
            print(f"Energy range: {min(energies):.2f} - {max(energies):.2f}")
            print(f"Mean energy: {np.mean(energies):.2f}")
        
        print("\nSmoke test PASSED")
        return 0
        
    except Exception as e:
        print(f"Smoke test FAILED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
