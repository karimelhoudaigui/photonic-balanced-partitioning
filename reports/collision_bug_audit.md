> HISTORICAL AUDIT: paths and line numbers below refer to the earlier defective implementation. Corrections and executed checks are documented in [PHYSICS_VALIDATION.md](PHYSICS_VALIDATION.md) and [RESEARCH_CYCLE_2026-11-20.md](RESEARCH_CYCLE_2026-11-20.md).

# Collision Bug Audit Report

## Critical Physics Error Identified

**FALSE CLAIM:** "P_CF = 1.0 (no collisions in fixed-photon subspace)"

**CORRECT PHYSICS:** A fixed total photon number does NOT imply collision-free occupations.

### The Error

The implementation incorrectly assumes that:
- Fixed photon number (∑n_i = k) 
- Is equivalent to
- Collision-free occupations (n_i ∈ {0,1})

This is FALSE for bosonic linear optics.

### Correct Distinction

1. **Full Fock sector** H_k: span{|n₁,…,n_m⟩ : ∑n_i = k}
   - Dimension: C(m+k-1, k)
   - Includes collision states like |2,0,0,0⟩

2. **Collision-free sector** H_k^CF: span{|n₁,…,n_m⟩ : ∑n_i = k, n_i ∈ {0,1}}
   - Dimension: C(m, k)
   - Only balanced partitions

## Affected Files and Statements

### Source Files

1. **src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py**
   - Line 71-75: `measure_collision_free_probability()` returns 1.0
   - Line 100-110: `_apply_unitary()` only enumerates k-subsets (collision-free)
   - Line 140-150: `sample()` only samples from collision-free states
   - Line 160-170: `compute_energy()` assumes collision-free

2. **src/photonic_balanced_partitioning/photonic/collision_aware.py**
   - Line 40-45: `compute_collision_probability()` returns 0.0
   - Line 50-60: `expected_objective()` assumes P_CF = 1

3. **src/photonic_balanced_partitioning/photonic/penalty_obliq.py**
   - Uses fixed-photon subspace incorrectly

4. **src/photonic_balanced_partitioning/photonic/cvar_fixed_photon.py**
   - Same issue

### Test Files

5. **tests/test_fixed_photon.py**
   - Line 55-60: `test_output_state()` checks normalization
   - Line 75-80: `test_measure_collision_free_probability()` expects 1.0

### Documentation Files

6. **README.md** - Implies constraint preservation via photon number
7. **paper/sections/04_photonic_formulation.tex** - Incorrect theorem statement
8. **paper/sections/07_exact_results.tex** - Reports P_CF = 1.0
9. **paper/sections/09_qpu_results.tex** - Same issue
10. **reports/feasibility_n4.md** - Reports P_CF = 1.0
11. **CLAIMS.md** - CLAIM-002 states "P_CF = 1.0"
12. **LAURENT_HANDOFF.md** - Same incorrect claim

### QPU Files

13. **qpu/run_qpu.py** - Assumes collision-free sampling
14. **qpu/smoke_test.py** - Same issue

## Required Fixes

1. Implement full Fock space simulation
2. Add collision state enumeration
3. Fix amplitude computation with proper normalization
4. Recompute P_CF for all experiments
5. Add HOM test validation
6. Update all documentation

## Dimension Verification Needed

For m=4 modes, k=2 photons:
- Full Fock dimension: C(4+2-1, 2) = C(5,2) = 10
- Collision-free dimension: C(4,2) = 6
- Collision states: |2,0,0,0⟩, |0,2,0,0⟩, |0,0,2,0⟩, |0,0,0,2⟩

## Next Steps

1. Fix state space implementation
2. Add physics tests
3. Recompute all results
4. Update documentation
