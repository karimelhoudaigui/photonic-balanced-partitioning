# Complete Experimental Summary

**Generated**: 2026-11-22  
**Git Commit**: `$(git rev-parse HEAD)`  
**Status**: All experiments complete, ready for paper/QPU

---

## Experiment Inventory

| Exp ID | Name | Status | Key Result |
|--------|------|--------|------------|
| E01 | Haar Collision Baseline | ✅ PASS | E[P_CF] = C(n,k)/C(n+k-1,k) exact |
| E02 | Ideal Optimization | ✅ COMPLETE | Variational beats Haar 5×–227× |
| E03 | Objectives Pareto | ✅ COMPLETE | P_success optimal |
| E04 | Optimizers/Depths | ✅ COMPLETE | COBYLA best |
| E05 | Equal Shots | ❌ REJECTED | Flawed protocol |
| E05b | Exact Equal Budget | ✅ COMPLETE | Variational 1.1×–10× better |
| E06 | Structural Checks | ✅ PASS | Moment identities verified |
| E07 | Spectral Hybrid | ❌ REJECTED | Classical preprocessing |
| E08 | Coherence Certificate | ✅ PASS | TV bounds verified |
| E09 | Label Control | ✅ FOLLOW-UP | Reachability artifact |
| P20 | Structured Probe | ✅ COMPLETE | Pair unitary = classical |
| P21 | Classical Search | ✅ COMPLETE | Baselines established |
| P30 | Optical Component | ✅ COMPLETE | ObliQ static verified |
| P31 | Washout Bound | ✅ COMPLETE | Bounds verified |
| P32 | Threshold Audit | ✅ COMPLETE | Threshold decoding verified |
| P33 | Density Probe | ✅ COMPLETE | Certificate validated |
| P33b | Density Replication | ✅ COMPLETE | Independent seeds PASS |
| P34 | Adaptive Replacement | ✅ COMPLETE | Local search verified |
| P35 | Component Review | ✅ COMPLETE | 190 marginals exact |
| P36 | Adversarial | ✅ COMPLETE | No certified refutation |
| P37 | Loss Source | ✅ COMPLETE | Haar loss marginals |
| P38 | Effect Search | ✅ COMPLETE | Pinching bounds |
| P39 | Pinched Envelope | ✅ COMPLETE | Counterexample found |

---

## Key Numerical Results Summary

### Haar Baseline (E01)
| n | k | Theory P_CF | Simulated P_CF | Theory P_success | Simulated P_success |
|---|---|-------------|----------------|------------------|---------------------|
| 4 | 2 | 0.6000 | 0.5985 | 0.2000 | 0.2052 |
| 6 | 3 | 0.3571 | 0.3584 | 0.0357 | 0.0349 |
| 8 | 4 | 0.2121 | 0.2121 | 0.0061 | 0.0059 |
| 10 | 5 | 0.1259 | 0.1259 | 0.0010 | 0.0010 |
| 12 | 6 | 0.0750 | — | 0.00015 | — |

### Variational Optimization (E02 + extensions)
| n | Graph | P_CF | P_success | P_opt|CF | E_CF | Shots |
|---|-------|------|-----------|--------|------|-------|
| 4 | path | 1.000 | 1.000 | 1.000 | 1.00 | 1.0 |
| 4 | cycle | 1.000 | 0.999 | 0.999 | 2.00 | 1.0 |
| 6 | path | 0.993 | 0.982 | 0.989 | 1.03 | 1.0 |
| 6 | cycle | 0.333 | 0.290 | 0.870 | 2.29 | 3.5 |
| 8 | path | 0.733 | 0.537 | 0.732 | 1.55 | 1.9 |
| 8 | cycle | 0.322 | 0.209 | 0.651 | 3.00 | 4.8 |
| 10 | path | 0.165 | 0.112 | 0.679 | 2.22 | 8.9 |
| 12 | path | 0.095 | 0.034 | 0.363 | 2.99 | 29.1 |

### Equal Budget Comparison (200 evals)
| n | Graph | Variational P_success | Penalty P_success | Ratio |
|---|-------|----------------------|-------------------|-------|
| 6 | path | 0.982 | 0.195 | 5.0× |
| 6 | cycle | 0.290 | 0.257 | 1.1× |
| 8 | path | 0.537 | 0.082 | 6.6× |
| 8 | cycle | 0.209 | 0.131 | 1.6× |
| 10 | path | 0.112 | 0.015 | 7.3× |
| 12 | path | 0.034 | 0.003 | 10.2× |

### Bosonic vs Distinguishable (P_success ratio)
| n | Graph | Bosonic/Distinguishable |
|---|-------|------------------------|
| 4 | all | 1.00 |
| 6 | cycle | 1.39 |
| 8 | ER | 2.37 |
| 10 | RR | 1.97 |
| 12 | RR | 4.81 |

### Objective Comparison (n=8, path)
| Objective | P_CF | P_success | P_opt|CF | E_CF | Shots |
|-----------|------|-----------|--------|------|-------|
| p_success | 0.733 | 0.537 | 0.732 | 1.55 | 1.86 |
| p_cf | 0.852 | 0.043 | 0.050 | 4.53 | 23.5 |
| p_opt|CF | 0.178 | 0.124 | 0.694 | 1.80 | 8.1 |
| conditional_E | 0.143 | 0.120 | 0.840 | 1.47 | 8.3 |
| collision_aware | 0.312 | 0.302 | 0.967 | 1.09 | 3.3 |
| log_barrier | 0.315 | 0.283 | 0.898 | 1.26 | 3.5 |

---

## Physics Validation Summary

| Test | Result | Tolerance |
|------|--------|-----------|
| HOM effect (50:50 BS) | P_CF = 0 | < 1e-10 |
| Identity | Returns input state | < 1e-12 |
| Permutation | Routes photons correctly | < 1e-12 |
| Phase shifter | Preserves prob, adds phase | < 1e-12 |
| Single photon BS | Analytic amplitudes | < 1e-12 |
| 3-photon phase | No global sign flip | < 1e-12 |
| Collisional input | Multinomial distribution | < 1e-12 |
| Vacuum | Amplitude = 1 | < 1e-12 |
| Perceval cross-val | 8464 outcomes | max err 1.7e-15 |
| Full Fock norm | 1.0 | < 1e-9 |

---

## Theoretical Results

| Result | Status | Reference |
|--------|--------|-----------|
| Haar E[P_CF] = C(n,k)/C(n+k-1,k) | PROVEN | Arkhipov-Kuperberg |
| Balanced asymptotic P_CF ~ √3(16/27)^(n/2) | PROVEN | Stirling |
| Haar E[P_A] = M/D, E[P_A|CF] = M/d | PROVEN | Symmetry |
| Moment identities | VERIFIED | Numerical |
| TV bounds | VERIFIED | Numerical + proof |
| Pinched envelope counterexample | FOUND | n=2k, k=2 |

---

## Code Quality

| Metric | Value |
|--------|-------|
| Total tests | 264 |
| Tests passing | 264 |
| Test coverage | Core modules 100% |
| Physics tests | 15 (HOM, permanent, Perceval) |
| Objective tests | 12 |
| Penalty tests | 6 |
| Mesh tests | 5 |
| Structured search tests | 8 |
| Audit regression tests | 3 |
| Density certificate tests | 5 |
| QPU gate tests | 1 |

---

## Reproducibility

All experiments use:
- Fixed seeds (20261120 + n*10000 + index)
- Pinned dependencies (numpy 2.4.6, scipy 1.17.1, perceval 1.3.0)
- Manifest files with SHA256 hashes
- Exact command lines recorded

Example reproduction:
```bash
# Physics validation
PYTHONPATH=src .venv/bin/python experiments/validation/run_physics_validation.py

# Haar baseline
PYTHONPATH=src .venv/bin/python experiments/run_research.py haar

# Variational optimization
PYTHONPATH=src .venv/bin/python experiments/run_research.py optimization

# Equal budget
PYTHONPATH=src .venv/bin/python experiments/run_equal_budget.py
```

---

## Ready for Paper/QPU

✅ Physics validated  
✅ Objectives correct (P_success)  
✅ Variational optimization working  
✅ Equal budget comparison done  
✅ Bosonic vs distinguishable tested  
✅ All graph families, n=4–12  
✅ QPU protocol defined  
✅ Paper outline ready  
✅ Code open and reproducible  

**Next action**: Submit QPU protocol to Laurent/Quandela, begin paper writing.
