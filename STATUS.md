# Project Status

## Current Phase: Implementation (Corrected)

### Completed
- [x] Project structure created
- [x] Core problem module (min_bisection.py)
- [x] Fixed-photon interferometer implementation (CORRECTED)
- [x] Collision-aware solver
- [x] Penalty-based ObliQ
- [x] CVaR solver
- [x] Classical baselines
- [x] Unit tests (35 passing)
- [x] Documentation updated

### In Progress
- [ ] Feasibility test (n=4, k=2) - CORRECTED
- [ ] Exact solver validation
- [ ] Photonic simulation validation

### Next Steps
1. Run corrected feasibility test
2. Measure P_CF for optimized interferometers
3. Compare with baselines
4. Create reports/feasibility_n4.md

## Key Metrics to Track

- P_CF (collision-free probability) - MUST BE MEASURED
- P_opt|CF (probability of optimal given collision-free)
- Expected shots to optimum
- Energy gap from optimal

## Decision Point

**CONDITIONAL-GO**: The physics is corrected but collision probability must be measured and optimized.

See `reports/feasibility_n4.md` for the decision criteria.

## Physics Correction Applied

The initial implementation incorrectly assumed P_CF = 1.0. This has been corrected:
- Full Fock space simulation implemented
- Collision states properly enumerated
- P_CF must be measured, not assumed
- Cardinality constraint is satisfied conditioned on CF
