# Feasibility Report: n=4, k=2

## Executive Summary

**Decision: CONDITIONAL-GO** - The fixed-k photon interferometer approach is scientifically valid but requires collision management.

## Test Configuration

- Graph: Path graph with 4 vertices
- Edges: (0,1), (1,2), (2,3) with weight 1.0
- Constraint: Balanced partition with k=2

## Results

### Exact Solution
- Optimal energy: 1.0
- Optimal partition: {0, 1} | {2, 3}

### Photonic Simulation (CORRECTED)

**CRITICAL CORRECTION**: Fixed photon number does NOT imply collision-free outcomes.

For m=4 modes, k=2 photons:
- Full Fock space dimension: C(5,2) = 10
- Collision-free dimension: C(4,2) = 6
- Collision states: |2,0,0,0⟩, |0,2,0,0⟩, |0,0,2,0⟩, |0,0,0,2⟩

### Physics Verification

1. **Photon number conservation**: P(N_out = k) = 1.0 ✓
2. **Collision probability**: P_CF < 1.0 (measured, not assumed)
3. **Cardinality constraint**: P(cardinality violation | CF) = 0 ✓

## Key Findings

1. **Photon number conservation**: Fixed photon number (∑n_i = k) is preserved by passive linear optics
2. **Collision probability**: P_CF < 1 for generic interferometers (must be measured)
3. **Constraint enforcement**: Cardinality constraint is satisfied conditioned on collision-free detection
4. **Energy computation**: Expected energy computed over full Fock space, conditioned on CF for valid partitions

## Next Steps

1. Implement interferometer optimization
2. Measure P_CF for optimized interferometers
3. Compare with classical baselines
4. Add noise model
5. Investigate collision suppression techniques

## Scientific Status

The constraint-preserving approach is scientifically valid. The key insight is that:
- Photon number conservation restricts evolution to the k-photon Fock sector
- Collision-free detection maps exactly onto balanced partitions
- P_CF must be measured, not assumed

## Conclusion

The project continues with corrected understanding of the physics. The next phase is to optimize interferometers and measure collision probabilities.
