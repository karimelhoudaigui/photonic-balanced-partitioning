# Handoff Document for Laurent

## Scientific Objective

This project investigates whether photon-number conservation can replace penalty terms in constrained graph optimization for balanced partitioning. The key question: Can a fixed-k photon interferometer maintain enough collision-free probability to make constraint-preserving balanced partitioning useful?

## What Has Been Validated

### Exact Solver
- Implemented and tested for n=4, 6, 8
- All graph families supported: path, cycle, complete, bipartite, star, random, planted

### Ideal Simulation
- Fixed-photon interferometer working correctly
- P_CF = 1.0 (constraint preserved by construction)
- Energy computation verified

### Noisy Simulation
- Noise model to be implemented
- Expected robustness from constraint preservation

## What Laurent Must Launch

### Stage 0: Connectivity Check
```bash
python qpu/check_backend.py --backend qpu:belenos
```

### Stage 1: Smallest Physical Smoke Test
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_smoke.yaml
```

### Stage 2: Replicated n=4
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_full.yaml
```

### Stage 3: n=6
```bash
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n6.yaml
```

## Recommended Order

Q0 → Q1 → Q2 → Q3

## What to Return

The raw results folder:
```
results/qpu/<run_id>/
```

Contents:
- config.yaml
- git_commit.txt
- environment.txt
- backend_metadata.json
- raw_samples.json
- processed_results.json
- stdout.log
- analysis.json

No manual analysis required - all analysis is automated.

## Quick Start for QPU

```bash
git clone <repo-url>
cd photonic-balanced-partitioning
python -m venv .venv
source .venv/bin/activate
pip install -r qpu/requirements_qpu.txt
export QPU_TOKEN="your-token"
python qpu/check_environment.py
python qpu/check_backend.py --backend qpu:belenos
python qpu/smoke_test.py
python qpu/run_qpu.py --backend qpu:belenos --config qpu/configs/n4_smoke.yaml
```

## Key Files

- `src/photonic_balanced_partitioning/` - Main implementation
- `src/problems/min_bisection.py` - Graph problem definitions
- `src/photonic/fixed_photon_obliq.py` - Photonic solver
- `qpu/run_qpu.py` - QPU experiment runner
- `qpu/configs/*.yaml` - Experiment configurations
