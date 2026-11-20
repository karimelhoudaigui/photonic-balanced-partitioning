# QPU Readiness Assessment

## Status: NOT READY FOR LAURENT

## Reasons

1. **Physics tests incomplete**: Need to verify HOM behavior and bosonic normalization
2. **P_CF measurement**: Must be validated against Perceval
3. **Collision handling**: Raw collision outcomes must be preserved in QPU output
4. **Optimization**: No optimized interferometer exists yet

## Required Before QPU Access

- [ ] Add HOM test validation
- [ ] Validate against Perceval for small circuits
- [ ] Verify collision state preservation in run_qpu.py
- [ ] Implement interferometer optimization
- [ ] Measure P_CF for optimized circuits

## Next Experiment

Run the n=4 feasibility test with optimized interferometer and measure:
- P_CF (collision-free probability)
- P_opt|CF (probability of optimal given collision-free)
- P_success = P_CF × P_opt|CF
- Expected shots to optimum

## When Ready

Update this file to:
```
READY
```

And ensure all tests pass with correct physics.
