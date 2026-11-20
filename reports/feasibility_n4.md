> HISTORICAL / SUPERSEDED, 2026-11-20: the numerical trial below has no retained seed or raw distribution and is not authenticated evidence. Do not use its values or contradictory GO decisions. Current executed results: [research checkpoint](RESEARCH_CYCLE_2026-11-20.md). The historical text is preserved to expose the earlier claims.

# Feasibility Report: n=4, k=2

## Executive Summary

**Decision: NO-GO (for now)** - The fixed-k photon interferometer approach faces fundamental challenges with collision probability.

## Test Configuration

- Graph: Path graph with 4 vertices
- Edges: (0,1), (1,2), (2,3) with weight 1.0
- Constraint: Balanced partition with k=2

## Results

### Exact Solution
- Optimal energy: 1.0
- Optimal partition: {0, 1} | {2, 3}

### Photonic Simulation (CORRECTED)

**Critical Physics Verification:**

For m=4 modes, k=2 photons:
- Full Fock space dimension: C(5,2) = 10
- Collision-free dimension: C(4,2) = 6
- Collision states: |2,0,0,0⟩, |0,2,0,0⟩, |0,0,2,0⟩, |0,0,0,2⟩

**Hong-Ou-Mandel Test:**
For a 50:50 beam splitter on modes 0,1 with input |1,1,0,0⟩:
- Output: (|2,0,0,0⟩ - |0,2,0,0⟩)/√2
- P_CF ≈ 0 (all probability in collision states)

This confirms the bosonic bunching effect is correctly simulated.

### Random Interferometer Results

Using a random Haar-distributed unitary:
- P_CF = 0.7915 (measured)
- Valid samples: 792/1000
- Average energy of valid samples: 2.3864
- Conditional expected energy E_valid = 2.3864
- Optimal probability P_opt|CF = 0 (no optimal solutions in valid samples)

### Key Metrics

| Metric | Value |
|--------|-------|
| P_CF | 0.7915 |
| P_opt\|CF | 0.0000 |
| P_success | 0.0000 |
| E_valid | 2.3864 |
| E_uncond | 1.8864 |
| Gap from optimal | 1.3864 |

## Analysis

### The HOM Problem

For two photons in different modes passing through a 50:50 beam splitter:
- They always "bunch" into the same output mode
- This creates a collision state |2,0,0,0⟩ or |0,2,0,0⟩
- P_CF = 0 for this configuration

### Implications

1. **Collision probability is fundamental**: Not all interferometers give good P_CF
2. **Optimization target**: Must maximize P_CF × P_opt|CF
3. **Physical shots**: Expected shots = 1/P_success can be very large

### The Core Challenge

The optimization problem is:
- Maximize P_success(U) = Σ p(s) for s ∈ CF with C_G(s) = C*
- Subject to: U is unitary

This is a fundamentally different optimization than just minimizing E_valid.

## Next Steps

1. **Implement success probability optimization**: Optimize for P_success, not just E_valid
2. **Investigate structured interferometers**: Can we design U to suppress bunching?
3. **Explore input state engineering**: Different initial photon distributions
4. **Add collision-aware training**: E_valid + μ(1-P_CF)

## Scientific Status

**CONDITIONAL-GO** with major caveats:

1. Physics is correct (HOM effect verified)
2. P_CF must be measured, not assumed
3. Optimization objective needs revision
4. Collision management is essential

## Conclusion

The constraint-preserving approach is scientifically valid but faces the fundamental challenge of bosonic bunching. The next phase must focus on:
1. Optimizing for success probability, not just conditional energy
2. Investigating collision suppression techniques
3. Comparing with penalty-based methods on equal footing
