# Photonic Balanced Partitioning

**Constraint-Preserving Photonic Quantum Optimization for Balanced Graph Partitioning**

> Can photon-number conservation replace penalty terms in constrained graph optimization?

## Quick Start

```bash
python3.11 -m pip install -e '.[test]'
pbp doctor
pbp test
pbp demo
```

## Project Structure

```
photonic-balanced-partitioning/
├── src/photonic_balanced_partitioning/
│   ├── problems/           # Graph problem definitions
│   ├── photonic/           # Photonic quantum algorithms
│   └── classical/          # Classical baseline solvers
├── tests/                   # 35 passing unit tests
├── theory/                  # Mathematical formulations
├── experiments/             # Experiment scripts and results
├── paper/                   # LaTeX manuscript
├── qpu/                     # QPU experiment package
├── reports/                 # Analysis reports
└── LAURENT_HANDOFF.md       # QPU handoff document
```

## Key Components

### Problem Module (`problems/min_bisection.py`)
- `BalancedGraphPartitioning` - Main problem class
- Graph families: path, cycle, complete, bipartite, star, random, planted
- Exact solver via enumeration (n ≤ 12)

### Photonic Module (`photonic/`)
- `FixedPhotonObliq` - Constraint-preserving fixed-k photon interferometer
- `CollisionAwareSolver` - Handles boson collisions explicitly
- `PenaltyObliq` - Penalty-based approach for comparison
- `CVaRFixedPhoton` - CVaR-based robust optimization

### Important Physics Note

**CRITICAL:** Fixed photon number (∑n_i = k) does NOT imply collision-free occupations (n_i ∈ {0,1}).

For m modes and k photons:
- Full Fock space dimension: C(m+k-1, k)
- Collision-free dimension: C(m, k)

Collision states like |2,0,0,0⟩ must be properly handled.

## Research Questions

1. Can we optimize interferometers to maximize P_CF × P_opt|CF?
2. Does constraint-preserving optimization outperform penalty-based methods?
3. What is the quantum advantage (if any) for balanced partitioning?

## License

MIT License
