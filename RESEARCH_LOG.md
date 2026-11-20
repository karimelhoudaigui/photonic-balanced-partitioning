# Research Log

## 2026-11-20 - Physics Correction

### Issue Identified
Fixed photon number (∑n_i = k) does NOT imply collision-free occupations (n_i ∈ {0,1}).

### Correction Applied
1. Full Fock space simulation implemented
2. Collision states properly enumerated
3. P_CF must be measured, not assumed
4. HOM effect verified: 50:50 BS gives P_CF ≈ 0

### Objective Function Error
The original `compute_energy()` was incorrect. It should return:
- E_valid = Σ p(s)C_G(s) / P_CF (conditional expected energy)
- P_success = Σ p(s) for s ∈ CF with C_G(s) = C* (physical success probability)

### Next Experiments
1. Haar baseline: Sample many random interferometers, measure P_CF, P_opt|CF, P_success
2. Optimization: Compare different objectives
3. Perceval cross-validation
