# QPU Readiness Assessment

## Status: NOT READY FOR LAURENT

## Reasons

1. **Physics verification incomplete**: Need to verify HOM effect on actual QPU
2. **Optimization objective incorrect**: Currently optimizing E_valid, should optimize P_success
3. **Collision handling**: Raw collision outcomes must be preserved in QPU output
4. **No optimized interferometer**: Random interferometer gives poor results

## Required Before QPU Access

- [ ] Fix optimization objective to maximize P_success
- [ ] Add HOM benchmark test
- [ ] Verify collision state preservation in run_qpu.py
- [ ] Implement success probability optimization
- [ ] Measure P_CF for optimized circuits

## The HOM Challenge

For two photons in different modes:
- 50:50 beam splitter → P_CF ≈ 0
- This is the Hong-Ou-Mandel effect
- Must be verified on actual hardware

## Next Experiment

Run the n=4 feasibility test with:
1. Optimized interferometer (maximizing P_success)
2. HOM benchmark verification
3. Collision state preservation check

## When Ready

Update this file to:
```
READY
```

And ensure:
- All physics tests pass
- Optimization objective is correct
- HOM effect verified
- Collision states preserved in QPU output
