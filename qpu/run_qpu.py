#!/usr/bin/env python3
"""Run QPU experiment."""

import argparse
import sys
import os
import json
import yaml
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run QPU experiment")
    parser.add_argument("--backend", required=True, help="QPU backend name")
    parser.add_argument("--config", required=True, help="Configuration file")
    parser.add_argument("--resume", help="Resume from run_id")
    args = parser.parse_args()
    
    print(f"QPU Experiment Runner")
    print(f"Backend: {args.backend}")
    print(f"Config: {args.config}")
    print("=" * 50)
    
    # Load config
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    print(f"Graph: n={config['n']}, k={config['k']}")
    print(f"Shots: {config['shots']}")
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = args.resume or f"{timestamp}_run"
    output_dir = Path(f"results/qpu/{run_id}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save config
    with open(output_dir / "config.yaml", "w") as f:
        yaml.dump(config, f)
    
    # Save git commit
    import subprocess
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        with open(output_dir / "git_commit.txt", "w") as f:
            f.write(commit)
    except:
        pass
    
    # Save environment
    import sys
    with open(output_dir / "environment.txt", "w") as f:
        f.write(f"Python: {sys.version}\n")
        f.write(f"Platform: {sys.platform}\n")
    
    # Run simulation (placeholder for actual QPU run)
    print("\nRunning simulation...")
    
    try:
        from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning
        from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
        import numpy as np
        
        n = config["n"]
        k = config["k"]
        shots = config["shots"]
        
        # Create graph
        if config.get("graph_family") == "cycle":
            problem = BalancedGraphPartitioning.cycle_graph(n)
        else:
            problem = BalancedGraphPartitioning.path_graph(n)
        
        exact = problem.solve_exact()
        
        # Run photonic solver
        solver = FixedPhotonObliq(n, k)
        U = solver.random_interferometer(seed=config.get("seed", 42))
        samples = solver.sample(U, num_shots=shots, seed=config.get("seed", 42))
        
        # Process results
        valid_samples = [s for s in samples if s.is_valid]
        energies = [s.energy for s in valid_samples]
        
        results = {
            "config": config,
            "exact_energy": exact.energy,
            "num_shots": shots,
            "num_valid": len(valid_samples),
            "p_valid": len(valid_samples) / shots,
            "mean_energy": float(np.mean(energies)) if energies else None,
            "min_energy": float(min(energies)) if energies else None,
            "max_energy": float(max(energies)) if energies else None,
        }
        
        # Save results
        with open(output_dir / "raw_samples.json", "w") as f:
            json.dump([{
                "partition": list(s.partition),
                "energy": s.energy,
                "probability": s.probability
            } for s in samples], f, indent=2)
        
        with open(output_dir / "processed_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        with open(output_dir / "analysis.json", "w") as f:
            json.dump({
                "p_cf": 1.0,  # In fixed-photon subspace
                "p_opt": len([s for s in valid_samples if s.energy == exact.energy]) / shots if valid_samples else 0,
                "gap": (results["mean_energy"] - exact.energy) / (results["max_energy"] - exact.energy) if results["max_energy"] != results["mean_energy"] else 0
            }, f, indent=2)
        
        print(f"\nResults saved to: {output_dir}")
        print(f"Valid samples: {results['num_valid']}/{shots}")
        print(f"Mean energy: {results['mean_energy']:.4f}")
        print(f"Exact energy: {exact.energy:.4f}")
        
        return 0
        
    except Exception as e:
        print(f"Experiment FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
