# Paper Outline — Constraint-Preserving Photonic Quantum Optimization for Balanced Graph Partitioning

**Status**: READY TO WRITE (all results in hand)  
**Target Venue**: Physical Review X / Nature Physics / PRX Quantum  
**Estimated Length**: 12 pages + supplementary  

---

## Title Options

1. **Primary**: "Variational Collision-Aware Photonic Optimization Beats Penalty Encodings for Cardinality-Constrained Graph Partitioning"
2. **Alternative**: "Fixed-Particle-Number Photonic Quantum Optimization for Balanced Graph Partitioning: A Variational Approach"
3. **Short**: "Photonic Quantum Optimization of Balanced Graph Partitioning with Collision Management"

---

## Abstract (250 words)

We investigate whether fixed-particle-number photonic quantum optimization can solve cardinality-constrained combinatorial problems more efficiently than penalty-based encodings. The Minimum Bisection problem — partitioning n vertices into two equal sets while minimizing cut weight — maps naturally to n-mode, k=n/2 photon interferometry: collision-free detection events correspond exactly to balanced partitions.

We identify a critical error in prior work: fixed photon number does NOT imply collision-free evolution. The full Fock space has dimension C(n+k-1,k), while the collision-free subspace has dimension C(n,k). For n=8, k=4: 330 vs 70 states. Hong-Ou-Mandel bunching forces P_CF → 0 for generic interferometers.

We develop a variational algorithm using a Clements mesh interferometer, optimizing the physical success probability P_success = P_CF × P_opt|CF — the probability per physical shot of obtaining an optimal collision-free solution. Across n=4,6,8,10,12 and 8 graph families (path, cycle, complete, bipartite, star, Erdős-Rényi, random regular, planted partition), variational optimization achieves P_success 5×–227× higher than Haar-random interferometers and 1.1×–10× higher than penalty-based QUBO at equal classical evaluation budget.

Crucially, bosonic interference provides a measurable advantage over distinguishable photons for n≥8 on structured graphs (random regular, planted), with P_success ratios up to 4.8×. The variational approach beats the combinatorial decay of Haar P_CF ~ (16/27)^(n/2).

We define a complete QPU protocol for experimental validation on a Quandela Belenos processor, including HOM calibration, Haar baseline, variational optimization, and penalty/distinguishable baselines. All simulation code is open-source and validated against Perceval.

---

## Paper Structure

### 1. Introduction (1.5 pages)
- Minimum Bisection / Balanced Partitioning: NP-hard, cardinality constraint
- Quantum approaches: QAOA (XY mixers, Dicke states), photonic (ObliQ, BBS)
- **Gap**: Prior photonic work assumed P_CF=1; we show this is false
- **Our contribution**: Variational collision-aware optimization with correct metric P_success

### 2. Problem Formulation (1 page)
- Minimum Bisection: min C_G(x) s.t. Σx_i = k, x ∈ {0,1}^n
- Photonic mapping: n modes, k photons, collision-free → balanced partition
- **Key distinction**: H_k (full Fock) vs H_k^CF (collision-free)
- Correct metric: P_success = Σ_{s∈CF, C(s)=C*} p(s)

### 3. Photonic Physics (1.5 pages)
- Passive linear optics: U ∈ U(n), Γ_k(U) on Sym^k(C^n)
- Transition amplitude: Per(U_{t,s}) / √(∏s_i! ∏t_j!)
- Full Fock dimension: C(n+k-1,k); CF dimension: C(n,k)
- **HOM effect**: 50:50 BS + |1,1⟩ → P_CF=0 (verified)
- Haar P_CF expectation: E[P_CF] = C(n,k)/C(n+k-1,k) (Arkhipov-Kuperberg)
- Balanced asymptotic: P_CF ~ √3(16/27)^(n/2)

### 4. Variational Algorithm (2 pages)
- Clements mesh parametrization: n(n-1)/2 BS + n PS
- Objective: Maximize P_success = Σ_{s∈CF, C(s)=C*} p(s)
- Optimizer: COBYLA on exact distribution (no shot noise in training)
- Graph-informed initialization: spectral/anchor optional
- **Key insight**: P_success directly maximizes what hardware cares about

### 5. Numerical Results (3 pages)
#### 5.1 Physics Validation
- Perceval cross-validation: 8464 outcomes, max error 1.7e-15
- HOM test: P_CF < 1e-10 for 50:50 BS
- Full Fock normalization: error < 1e-14

#### 5.2 Haar Baseline
- n=4,6,8,10,12: E[P_CF] matches theory exactly
- P_success decays as (16/27)^(n/2)

#### 5.3 Variational Optimization
- **P_success vs Haar**: 5×–227× improvement
- **P_success vs Penalty**: 1.1×–10× at equal eval budget
- **Scaling**: Beats combinatorial decay

#### 5.4 Bosonic vs Distinguishable
- n=4,6: No advantage (P_CF≈1)
- n=8,10,12: Advantage on structured graphs (RR, planted)
- Max ratio: 4.8× (n=12, random regular)

#### 5.5 Objective Comparison
- P_success optimal: directly maximizes hardware metric
- p_cf, p_opt|CF, conditional_energy suboptimal

#### 5.6 Equal Budget Comparison
- 200 evaluations: Variational 1.1×–10× better than penalty

### 6. QPU Protocol (1 page)
- HOM calibration → Haar baseline → Variational → Penalty/Distinguishable
- n=4,6,8 on Belenos
- Metrics: P_CF, P_success, P_opt|CF with Wilson CI
- Expected shots = 1/P_success

### 7. Discussion (1.5 pages)
- **Why it works**: Variational optimization navigates Pareto frontier (P_CF, P_opt|CF)
- **Bosonic advantage**: Emerges when P_CF < 1 and interference concentrates probability
- **Limitations**: Combinatorial decay still limits n; loss/distinguishability untested
- **Future**: Graph-informed initialization, noise-aware objectives, n>12

### 8. Conclusion (0.5 pages)
- Fixed-particle photonic optimization with collision management beats penalty encodings
- P_success is the correct metric for hardware
- QPU protocol ready for experimental validation

---

## Supplementary Material

1. **Full numerical tables** for all n, graphs, objectives
2. **Perceval validation details** (8464 outcomes)
3. **Derivation of Haar P_CF asymptotic**
4. **Pareto frontier analysis** (P_CF vs P_opt|CF)
5. **QPU protocol full specification**
6. **Code availability**: GitHub repository with reproduction scripts

---

## Figures

| Figure | Description |
|--------|-------------|
| Fig 1 | Photonic mapping: graph → interferometer → collision-free = balanced partition |
| Fig 2 | HOM effect: P_CF=0 for 50:50 BS |
| Fig 3 | Haar P_CF vs n: theory vs simulation |
| Fig 4 | Variational P_success vs n: beats Haar and Penalty |
| Fig 5 | Pareto frontier: P_CF vs P_opt|CF for different objectives |
| Fig 6 | Bosonic vs Distinguishable P_success ratio vs n |
| Fig 7 | Equal budget comparison: Variational vs Penalty |
| Fig 8 | QPU protocol flowchart |

---

## Tables

| Table | Description |
|-------|-------------|
| Table 1 | Fock space dimensions: C(n+k-1,k) vs C(n,k) for n=4,6,8,10,12 |
| Table 2 | Haar P_CF predictions vs simulation |
| Table 3 | Variational P_success for all n, graphs |
| Table 4 | Equal budget comparison (200 evals) |
| Table 5 | Bosonic vs Distinguishable P_success ratios |
| Table 6 | Objective comparison (P_success optimal) |
| Table 7 | QPU protocol resource estimate |

---

## References (Key)

1. Arkhipov & Kuperberg, "The bosonic birthday paradox" (2011) — Haar P_CF
2. Clements et al., "Optimal design for universal multiport interferometers" (2016) — Mesh
3. Wang et al., "Bosonic Binary Solver" (2023) — Photonic QUBO
4. Hadfield et al., "QAOA with XY mixers" (2019) — Cardinality constraints
5. Perceval documentation — SLOS backend validation
6. Quandela Belenos specs — Hardware capabilities

---

## Writing Timeline

| Week | Task |
|------|------|
| 1 | Write Introduction, Problem Formulation, Photonic Physics |
| 2 | Write Variational Algorithm, Numerical Results |
| 3 | Write QPU Protocol, Discussion, Conclusion |
| 4 | Prepare Figures, Tables, Supplementary |
| 5 | Internal review, co-author feedback |
| 6 | Final polish, submit |

---

## Co-authors & Contributions

| Author | Contribution |
|--------|--------------|
| [You] | Concept, algorithm design, numerical experiments, QPU protocol |
| [Co-author 1] | Theory: Haar P_CF, Pareto analysis |
| [Co-author 2] | Perceval validation, HOM verification |
| [Co-author 3] | QPU protocol design, hardware interface |

---

## Open Questions for Discussion Section

1. **Loss & distinguishability**: How much advantage survives 10% loss?
2. **Scaling to n=14,16**: Can graph-informed initialization help?
3. **Noise-aware objectives**: Should we optimize P_success(η) directly?
4. **Comparison to QAOA**: Photonic vs qubit cardinality-constrained QAOA
5. **Classical simulability**: Is the variational circuit classically simulable?

---

## Submission Checklist

- [x] All numerical results generated and validated
- [x] Physics validated against Perceval
- [x] QPU protocol defined and simulated
- [x] Code open-sourced with reproduction scripts
- [ ] Figures generated in publication quality
- [ ] Tables formatted
- [ ] Supplementary material prepared
- [ ] Co-author review
- [ ] Submit to target journal
