"""Command-line interface for Photonic Balanced Partitioning."""

from __future__ import annotations

import argparse
import sys


def cmd_doctor(args: argparse.Namespace) -> int:
    """Check dependencies, environment configuration, and available hardware."""
    print("Photonic Balanced Partitioning - Environment Check")
    print("=" * 50)
    
    import sys
    print(f"Python: {sys.version}")
    
    try:
        import numpy as np
        print(f"NumPy: {np.__version__}")
    except ImportError:
        print("NumPy: NOT INSTALLED")
        return 1
    
    try:
        import scipy
        print(f"SciPy: {scipy.__version__}")
    except ImportError:
        print("SciPy: NOT INSTALLED")
        return 1
    
    try:
        import matplotlib
        print(f"Matplotlib: {matplotlib.__version__}")
    except ImportError:
        print("Matplotlib: NOT INSTALLED (optional)")
    
    try:
        import perceval
        print(f"Perceval: {perceval.__version__}")
    except ImportError:
        print("Perceval: NOT INSTALLED (optional for QPU)")
    
    print("\nAll core dependencies satisfied.")
    return 0


def cmd_test(args: argparse.Namespace) -> int:
    """Run the feasibility test for n=4, k=2."""
    print("Running feasibility test (n=4, k=2)...")
    
    from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    import numpy as np
    
    # Create a simple test graph: 4 nodes, path graph
    edges = [(0, 1, 1.0), (1, 2, 1.0), (2, 3, 1.0)]
    n = 4
    k = 2
    
    problem = BalancedGraphPartitioning(n, edges)
    
    # Get exact optimum
    exact_result = problem.solve_exact()
    print(f"Exact optimum: {exact_result.energy}")
    print(f"Optimal partition: {exact_result.partition}")
    
    # Test fixed-photon interferometer
    solver = FixedPhotonObliq(n, k)
    
    U = solver.random_interferometer(seed=42)
    
    p_cf = solver.measure_collision_free_probability(U)
    print(f"Collision-free probability: {p_cf:.4f}")
    
    samples = solver.sample(U, num_shots=1000, edges=edges, seed=43)
    valid_count = sum(1 for s in samples if s.is_valid)
    print(f"Valid samples: {valid_count}/{len(samples)}")
    
    if valid_count > 0:
        avg_energy = np.mean([s.energy for s in samples if s.is_valid])
        print(f"Average energy of valid samples: {avg_energy:.4f}")
    
    print("\nFeasibility test complete.")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    """Run a demonstration of the photonic optimization."""
    print("Photonic Balanced Partitioning Demo")
    print("=" * 50)
    
    from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning
    from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
    import numpy as np
    
    # Create a 6-node cycle graph
    n = 6
    edges = [(i, (i+1) % n, 1.0) for i in range(n)]
    k = n // 2
    
    print(f"\nGraph: {n} nodes, cycle graph")
    print(f"Constraint: balanced partition with k={k}")
    
    problem = BalancedGraphPartitioning(n, edges)
    exact_result = problem.solve_exact()
    print(f"Exact optimum: {exact_result.energy}")
    print(f"Optimal partition: {exact_result.partition}")
    
    print("\n--- Comparing Solvers ---")
    
    solver = FixedPhotonObliq(n, k)
    U = solver.random_interferometer(seed=42)
    p_cf = solver.measure_collision_free_probability(U)
    print(f"Fixed-photon interferometer: P_CF = {p_cf:.4f}")
    
    return 0


def cmd_qpu(args: argparse.Namespace) -> int:
    """Run QPU experiment."""
    print("REFUSED: hardware gate closed; no authorized QPU implementation exists.")
    print("See reports/QPU_READINESS.md")
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pbp",
        description="Constraint-Preserving Photonic Quantum Optimization for Balanced Graph Partitioning"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    doctor_parser = subparsers.add_parser("doctor", help="Check environment and dependencies")
    doctor_parser.set_defaults(func=cmd_doctor)
    
    test_parser = subparsers.add_parser("test", help="Run feasibility test")
    test_parser.set_defaults(func=cmd_test)
    
    demo_parser = subparsers.add_parser("demo", help="Run demonstration")
    demo_parser.set_defaults(func=cmd_demo)
    
    qpu_parser = subparsers.add_parser("qpu", help="Run QPU experiment")
    qpu_parser.add_argument("--backend", required=True, help="QPU backend name")
    qpu_parser.add_argument("--config", required=True, help="Configuration file")
    qpu_parser.set_defaults(func=cmd_qpu)
    
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
