# QPU Experiment Protocol — Photonic Balanced Partitioning

**Status**: READY FOR SUBMISSION  
**Target Hardware**: Quandela Belenos (or equivalent)  
**Modes**: n=4,6,8 (start with n=4)  
**Photons**: k=n/2 indistinguishable photons  

---

## 1. Scientific Hypothesis

> **H₁**: A variationally optimized Clements mesh interferometer achieves higher physical success probability P_success = P_CF × P_opt|CF than (a) Haar-random interferometers and (b) penalty-based QUBO encodings, at equal physical sampling cost.

**Falsification criterion**: If measured P_success on QPU does not exceed Haar baseline by >5% or penalty baseline by >2x at equal shots, H₁ is rejected.

---

## 2. Required Hardware Capabilities

| Capability | Requirement | Verification |
|------------|-------------|--------------|
| Modes | n=4,6,8 | Belenos supports up to 12 |
| Photon number | k=n/2 indistinguishable | HOM test validates |
| Input state | |1^k 0^(n-k)⟩ | Standard preparation |
| Unitary control | Clements mesh (n(n-1)/2 BS + n PS) | Native |
| Detection | Photon-number-resolving (PNR) | Required for CF detection |
| Shots | 10,000–100,000 per circuit | Standard |

---

## 3. Experimental Protocol

### Phase A: Calibration (Day 1)
1. **HOM test**: Prepare |1,1,0,0⟩ on modes 0,1; apply 50:50 BS; measure P_CF
   - Expected: P_CF < 0.01 (ideal: 0)
   - Validates indistinguishability and PNR detection
2. **Loss characterization**: Measure transmission per mode
3. **Dark count rate**: Measure with vacuum input

### Phase B: Haar Baseline (Day 1-2)
For each n ∈ {4,6,8}:
1. Generate 100 Haar-random unitaries (seeded)
2. For each unitary:
   - Prepare |1^k 0^(n-k)⟩
   - Apply unitary
   - Measure 1000 shots
   - Record: P_CF, P_success, P_opt|CF
4. Compute mean/std of P_CF, P_success
5. Compare to theoretical Haar prediction: E[P_CF] = C(n,k)/C(n+k-1,k)

### Phase C: Variational Optimization (Day 2-3)
For each graph family × n:
1. **Graph families**: path, cycle, complete, bipartite, star, ER(p=0.5), RR(d=3), planted
2. **Optimization**:
   - Parametrize Clements mesh (depth=n)
   - Objective: Maximize P_success (exact distribution, no shots)
   - Optimizer: COBYLA, 200 evaluations
   - Seed: 42 (reproducible)
3. **Validation**: Evaluate optimized circuit with 10,000 shots
4. **Record**: P_CF, P_success, P_opt|CF, expected shots

### Phase D: Baseline Comparisons (Day 3-4)
For each optimized circuit:
1. **Penalty baseline**: Same graph, λ=10, 200 random logit evaluations, 10,000 shots each
2. **Distinguishable control**: Same optimized unitary, distinguishable photons (simulated or via temporal distinguishability)
3. **Uniform feasible**: Random balanced partitions (classical)

### Phase E: Data Collection
For each experiment, record:
- Raw shot data (occupation numbers per shot)
- P_CF, P_success, P_opt|CF with Wilson 95% CI
- Expected shots = 1/P_success with CI
- Circuit parameters (mesh angles)

---

## 4. Graph Instances (Pre-computed)

### n=4 (k=2)
| Family | Edges | Optimal Energy | Optimal Partition |
|--------|-------|----------------|-------------------|
| path | (0,1),(1,2),(2,3) | 1.0 | {0,1} |
| cycle | (0,1),(1,2),(2,3),(3,0) | 2.0 | {0,1} |
| complete | all pairs | 4.0 | {0,1} |
| bipartite | (0,2),(0,3),(1,2),(1,3) | 4.0 | {0,1} |
| star | (0,1),(0,2),(0,3) | 2.0 | {1,2} |

### n=6 (k=3)
| Family | Optimal Energy |
|--------|----------------|
| path | 1.0 |
| cycle | 2.0 |
| complete | 9.0 |
| bipartite | 9.0 |
| star | 3.0 |
| ER(p=0.5) | varies |
| RR(d=3) | varies |
| planted | varies |

### n=8 (k=4)
| Family | Optimal Energy |
|--------|----------------|
| path | 1.0 |
| cycle | 2.0 |
| complete | 16.0 |
| bipartite | 8.0 |
| star | 4.0 |
| ER(p=0.5) | varies |
| RR(d=3) | varies |
| planted | varies |

---

## 5. Success Metrics

| Metric | Definition | Target (from simulation) |
|--------|------------|-------------------------|
| P_CF | Σ p(s) for s ∈ CF | n=4: ~1.0, n=6: ~0.99, n=8: ~0.73 |
| P_success | Σ p(s) for s ∈ CF, C(s)=C* | n=4: ~1.0, n=6: ~0.98, n=8: ~0.54 |
| P_opt|CF | P_success / P_CF | n=4: ~1.0, n=6: ~0.99, n=8: ~0.73 |
| Expected shots | 1 / P_success | n=4: ~1, n=6: ~1, n=8: ~2 |

**Hardware success**: Measured P_success > Haar baseline + 5% AND > 2× penalty baseline

---

## 6. Data Format

### Raw Shots (CSV)
```csv
shot_id,circuit_id,graph_family,n,k,occupation_numbers,is_cf,is_optimal,energy
```

### Circuit Parameters (JSON)
```json
{
  "circuit_id": "var_path_n8_seed42",
  "graph_family": "path",
  "n": 8,
  "k": 4,
  "mesh_params": [...],
  "mesh_depth": 8,
  "optimizer": "COBYLA",
  "n_evaluations": 200,
  "seed": 42
}
```

### Summary Metrics (JSON)
```json
{
  "circuit_id": "...",
  "n_shots": 10000,
  "p_cf": 0.7331,
  "p_cf_ci95": [0.72, 0.74],
  "p_success": 0.5369,
  "p_success_ci95": [0.52, 0.55],
  "p_opt_given_cf": 0.7324,
  "expected_shots": 1.86,
  "expected_shots_ci95": [1.8, 1.9]
}
```

---

## 7. Resource Estimate

| Phase | Circuits | Shots/Circuit | Total Shots | Time (est.) |
|-------|----------|---------------|-------------|-------------|
| Calibration | 1 | 10,000 | 10,000 | 1 hr |
| Haar baseline | 300 (3n×100) | 1,000 | 300,000 | 6 hrs |
| Variational | 24 (8 graphs × 3n) | 10,000 | 240,000 | 8 hrs |
| Penalty baseline | 24 | 10,000 | 240,000 | 8 hrs |
| Distinguishable | 24 | 10,000 | 240,000 | 8 hrs |
| **Total** | **597** | | **1,030,000** | **~31 hrs** |

---

## 8. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Low indistinguishability | HOM test validates; if P_CF > 0.05, abort |
| High loss | Characterize per-mode; if >3dB, reduce n |
| PNR saturation | Use low photon flux; verify linearity |
| Optimization stuck | Multiple random restarts (3 seeds) |
| QPU downtime | Prioritize n=4,6; n=8 optional |

---

## 9. Submission Checklist

- [x] Protocol defined and simulated
- [x] Graph instances pre-computed
- [x] Success metrics defined with targets
- [x] Data format specified
- [x] Resource estimate provided
- [x] Risk mitigation documented
- [ ] **Submit to Laurent/Quandela for Belenos allocation**
- [ ] Schedule QPU time
- [ ] Execute protocol
- [ ] Analyze and compare to simulation

---

## 10. Contact

**Principal Investigator**: [Your Name]  
**Repository**: https://github.com/karimelhoudaigui/photonic-balanced-partitioning  
**Protocol Version**: 1.0 (2026-11-22)  
**Git Commit**: `$(git rev-parse HEAD)`
