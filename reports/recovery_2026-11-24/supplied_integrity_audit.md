# Scientific Integrity Audit Report

**Date**: 2026-11-22  
**Branch**: scientific-recovery-publication  
**Base Commit**: 6154b46  
**Audit Scope**: Complete repository audit for collision-free vs fixed-photon-number confusion

---

## Executive Summary

This audit identifies all locations in the repository where **fixed total photon number** (∑n_i = k) is incorrectly treated as equivalent to **collision-free occupations** (n_i ∈ {0,1}). This is a fundamental physics error: bosonic linear optics with fixed total photon number does NOT restrict evolution to the collision-free subspace.

**Key Physics**: 
- Full Fock sector ℋ_k: span{|n₁,…,n_m⟩ : ∑n_i = k}, dimension = C(m+k-1, k)
- Collision-free sector ℋ_k^CF: span{|n₁,…,n_m⟩ : ∑n_i = k, n_i ∈ {0,1}}, dimension = C(m, k)
- For m=4, k=2: Full = 10 states, CF = 6 states, Collision states = 4 (|2,0,0,0⟩, |0,2,0,0⟩, |0,0,2,0⟩, |0,0,0,2⟩)
- Hong-Ou-Mandel effect: 50:50 BS with |1,1⟩ → P_CF = 0 (all probability in collision states)

---

## 1. Source Code Files with Collision-Free Assumptions

### 1.1 `src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py`

**Status**: ✅ **CORRECTED** - Full Fock space implementation

**Historical Issues (now fixed)**:
- Line 71-75 (old): `measure_collision_free_probability()` returned 1.0
- Line 100-110 (old): `_apply_unitary()` only enumerated k-subsets (collision-free)
- Line 140-150 (old): `sample()` only sampled from collision-free states
- Line 160-170 (old): `compute_energy()` assumed collision-free

**Current Implementation (CORRECT)**:
- Full Fock space dimension: `math.comb(n + k - 1, k)` (line 47)
- CF dimension: `math.comb(n, k)` (line 48)
- All states enumerated via `_fock_states()` (weak compositions)
- `output_state()` returns full Fock amplitudes with normalization check
- `collision_free_probabilities()` returns unconditioned CF probabilities
- `measure_collision_free_probability()` returns actual P_CF ≤ 1
- `sample()` includes collision states, marks `is_valid=False` for collisions
- `compute_energy()` returns conditional energy E[C|CF] (returns ∞ if P_CF=0)
- `compute_success_probability()` computes P_success = Σ p(s) for s∈CF with C(s)=C*

**Validation**: All 264 tests pass, Perceval cross-validation PASS (max error 1.7e-15)

---

### 1.2 `src/photonic_balanced_partitioning/photonic/collision_aware.py`

**Status**: ✅ **CORRECTED** - Explicit collision handling

**Historical Issues (now fixed)**:
- Line 40-45 (old): `compute_collision_probability()` returned 0.0
- Line 50-60 (old): `expected_objective()` assumed P_CF = 1

**Current Implementation (CORRECT)**:
- `compute_collision_probability()` returns actual 1 - P_CF
- `sample()` preserves collision shots with `has_collision=True`
- `expected_objective()` uses full Fock distribution with `distribution_metrics()`
- `optimize()` uses exact distribution, reports zero physical shots

---

### 1.3 `src/photonic_balanced_partitioning/photonic/penalty_obliq.py`

**Status**: ✅ **CORRECTED** - Explicitly labeled as classical baseline

**Current Implementation**:
- Renamed to `PenaltyProductBernoulli` with `model_name = "classical_product_bernoulli"`
- Deprecated `PenaltyObliq` alias emits DeprecationWarning
- Explicitly does NOT implement ObliQ optical dynamics
- Full binary space {0,1}^n with penalty λ(∑x_i - k)²
- All 2^n outcomes retain support for finite logits

---

### 1.4 `src/photonic_balanced_partitioning/photonic/cvar_fixed_photon.py`

**Status**: ✅ **CORRECTED** - Uses full Fock distribution

**Current Implementation**:
- `compute_cvar_energy()` uses full Fock distribution via `conditional_cvar()`
- `sample()` filters valid samples correctly
- `optimize()` uses exact distribution, reports zero physical shots

---

### 1.5 `src/photonic_balanced_partitioning/photonic/structured_search.py`

**Status**: ✅ **CORRECT** - Explicit about collision handling

**Current Implementation**:
- `pair_unitary()` creates disjoint 2×2 rotations → exact CF=1 classical product sampler
- `LocalBlockProposal.distribution()` includes collision mass explicitly
- `statistics()` computes `p_cf` explicitly from probabilities

---

### 1.6 `src/photonic_balanced_partitioning/photonic/threshold_budget.py`

**Status**: ✅ **CORRECT** - Explicit threshold decoding with collisions

**Current Implementation**:
- `ThresholdEvaluator` maps full Fock → binary via threshold x_i = 1[n_i > 0]
- `fock_probabilities()` supports both 'bosonic' and 'distinguishable' models
- `probabilities()` includes loss model with threshold decoding
- `metrics()` computes p_feasible, p_success, conditional_energy correctly

---

### 1.7 `src/photonic_balanced_partitioning/photonic/comparison.py`

**Status**: ✅ **CORRECT** - Independent CF evaluator

**Current Implementation**:
- `CollisionFreeEvaluator` enumerates CF events only WITHOUT renormalizing
- `probabilities()` supports 'bosonic', 'distinguishable', 'multinomial' models
- `cf_metrics()` computes p_cf, p_success, p_opt_given_cf, conditional_energy correctly

---

### 1.8 `src/photonic_balanced_partitioning/photonic/density_certificate.py`

**Status**: ✅ **CORRECT** - Explicit about collision bounds

**Current Implementation**:
- Computes `expected_collision_pairs` (M) and `dominant_support_leakage` (δ)
- Bounds TV distance with `cycle_envelope()` function
- Explicitly states: "Sufficient absolute-TV certificate only; not a success ratio, sampler speedup or hardness test"

---

### 1.9 `src/photonic_balanced_partitioning/photonic/optical_penalty.py`

**Status**: ✅ **CORRECT** - Static ObliQ component only

**Current Implementation**:
- Reproduces only static pair kernel, NOT full ObliQ variational training
- Explicitly states: "no remote processor or QPU access"
- `component_validation()` compares against Perceval SLOS
- `convergence` sweep on one weighted-regular graph only

---

## 2. Test Files - Validation of Corrections

### 2.1 `tests/test_fixed_photon.py` ✅ **VALIDATES CORRECTIONS**

Key tests validating corrections:
- `test_fock_dimension()`: Verifies full_dimension=10, cf_dimension=6 for n=4,k=2
- `test_collision_states_exist()`: Verifies 4 collision states exist for n=4,k=2
- `test_measure_collision_free_probability()`: Asserts 0 ≤ P_CF ≤ 1 (NOT 1.0)
- `test_collision_states_exist()`: Verifies collision states have mode with 2 photons
- `test_hom_effect_two_photons()`: Verifies P_CF ≈ 0 for HOM
- `test_hom_amplitude_distribution()`: Verifies all probability in collision states for HOM

### 2.2 `tests/test_hom.py` ✅ **VALIDATES HOM EFFECT**

Key tests:
- `test_hom_effect_two_photons()`: P_CF < 1e-10 for 50:50 BS
- `test_hom_amplitude_distribution()`: All probability in collision states for HOM
- `test_hom_complex_amplitudes_and_distinguishable_coincidence()`: Verifies bosonic vs distinguishable

### 2.3 `tests/test_permanent_normalization.py` ✅ **VALIDATES PHYSICS**

Key tests:
- `test_ryser_against_explicit_permutations()`: Ryser vs explicit permutations
- `test_full_distribution_raw_normalization_and_cf_subset()`: Raw norm = 1, CF subset matches
- `test_three_photon_phase_is_not_global_sign_flipped()`: Odd photon phases correct
- `test_collisional_input_multinomial()`: Collisional input matches multinomial
- `test_identity_matches_documented_input_basis()`: Identity preserves input

### 2.4 `tests/test_perceval_cross_validation.py` ✅ **VALIDATES AGAINST PERCEVAL**

- 125 input/circuit cases, 8464 Fock outcomes
- Max probability error: 1.78e-15
- Max amplitude error: 2.14e-15
- Max norm error: 4.22e-15

### 2.5 `tests/test_objectives.py` ✅ **VALIDATES OBJECTIVE CORRECTIONS**

Key tests:
- `test_collision_leakage_cannot_improve_conditional_objective()`: Shows conditional energy invariant to P_CF scaling
- `test_zero_cf_is_never_free_energy()`: Zero CF → infinite conditional energy
- `test_collision_wrapper_reports_hom_and_preserves_shots()`: HOM → P_CF=0, infinite objective
- `test_cvar_sample_keeps_partition_after_rejection()`: CVaR handles rejection correctly

### 2.5 `tests/test_penalty.py` ✅ **VALIDATES PENALTY BASELINE**

- `test_qubo_matches_direct_energy_on_entire_cube()`: QUBO matches direct energy
- `test_full_cube_has_feasible_and_infeasible_support()`: Full {0,1}^n support
- `test_real_penalty_changes_ground_state_feasibility()`: λ controls feasibility
- `test_old_name_warns_instead_of_claiming_obliq()`: Deprecation warning works

### 2.6 `tests/test_mesh_comparison.py` ✅ **VALIDATES MESH**

- `test_independent_permutation_sum_matches_full_ryser()`: CF evaluator matches full Ryser
- `test_distinguishable_against_labelled_enumeration()`: Distinguishable matches labelled enum
- `test_oracle_permutation_and_no_interference()`: Permutation gives P_CF=1, P_opt|CF=1
- `test_perceval_mesh_circuit()`: Mesh matches Perceval

### 2.7 `tests/test_structured_search.py` ✅ **VALIDATES STRUCTURED SEARCH**

- `test_pair_control_is_collision_free_and_classical()`: pair_unitary → CF=1, classical
- `test_independent_classical_block_replacement_is_exact()`: Classical matches bosonic for r≤3
- `test_genuine_interference_can_enrich_but_classical_controls_match_or_beat()`: Classical controls match/beat bosonic

### 2.8 `tests/test_density_certificate.py` ✅ **VALIDATES DENSITY CERTIFICATE**

- `test_disjoint_probabilistic_orbitals_are_classical_without_deterministic_photons()`: Disjoint → classical
- `test_dilute_balanced_spectators_do_not_yield_a_false_small_certificate()`: Dilute counterexample TV=1/2
- `test_small_angle_does_not_lose_collision_mass_by_subtraction()`: Small angle collision mass preserved

### 2.9 `tests/test_qpu_gate.py` ✅ **VALIDATES QPU GATE CLOSED**

- All old QPU entrypoints return status 2 (closed)

---

## 3. Documentation Files - Status

### 3.1 `README.md` ✅ **CORRECT**
- States: "The tested generic-mesh route currently gives **NO-GO for a benefit claim**"
- "The manuscript is frozen and hardware execution is disabled"
- Links to RESEARCH_CYCLE_2026-11-20.md, CLAIMS.md, OPEN_QUESTIONS.md

### 3.2 `STATUS.md` ✅ **CORRECT**
- "PAPER_READY = FALSE. QPU_GATE = CLOSED."
- "The tested generic bosonic mesh remains NO-GO as computational-benefit evidence."

### 3.3 `CLAIMS.md` ✅ **CORRECT**
- CLAIM-001: Photon number conservation (PROVEN, known background)
- CLAIM-002: P_CF = 1 in fixed-photon subspace → **REJECTED**
- CLAIM-003: Collision-free = balanced partitions (PROVEN, definitional)
- CLAIM-004: Variational optimization beats Haar (NUMERICALLY_SUPPORTED)
- CLAIM-005: Bosonic advantage (NUMERICALLY_SUPPORTED, conditional)

### 3.4 `RESEARCH_LOG.md` ✅ **COMPLETE**
- Documents all experiments E01-E09, P20-P39
- Each experiment: Question, Hypothesis, Protocol, Code, Seeds, Raw data, Result, Interpretation, Decision
- Decisions: KEEP, REJECT, FOLLOW-UP

### 3.5 `RESEARCH_CYCLE_2026-11-20.md` ✅ **CORRECT**
- "Decision: NO-GO for a photonic computational-benefit claim and QPU preparation"
- "PAPER_READY = FALSE"
- Documents all negative results honestly

### 3.6 `RESEARCH_CHECKPOINT_P39.md` ✅ **CORRECT**
- "PAPER_READY=FALSE. QPU_GATE=CLOSED."
- "The original optimum-blind graph-optimization benefit and novelty remain OPEN."

### 3.7 `RESEARCH_CHECKPOINT_FINAL.md` ⚠️ **CONTRADICTS OTHER DOCS**
- Claims "PAPER_READY=TRUE (conditional on QPU validation). QPU_GATE=OPEN"
- Claims "Answer: YES" to benefit question
- **CONTRADICTION**: This document appears to be an aspirational draft that contradicts the actual scientific status documented in RESEARCH_CYCLE_2026-11-20.md, RESEARCH_CHECKPOINT_P39.md, STATUS.md, QPU_READINESS.md, and LAURENT_HANDOFF.md

### 3.8 `EXPERIMENTAL_SUMMARY.md` ⚠️ **CONTRADICTS OTHER DOCS**
- Claims "All experiments complete, ready for paper/QPU"
- Claims "PAPER_READY=TRUE" implicitly
- **CONTRADICTION**: Same issue as RESEARCH_CHECKPOINT_FINAL.md

### 3.9 `QPU_PROTOCOL.md` ⚠️ **ASPIRATIONAL**
- Well-written protocol but labeled "READY FOR SUBMISSION"
- Contains simulated results labeled as "reference"
- Should be labeled "DRAFT PROTOCOL - NOT AUTHORIZED"

### 3.10 `QPU_READINESS.md` ✅ **CORRECT**
- "Hardware gates — CLOSED"
- "PAPER_READY=FALSE. No QPU execution authorized or performed."
- All gates show current evidence honestly

### 3.11 `LAURENT_HANDOFF.md` ✅ **CORRECT**
- "WITHDRAWN — no hardware handoff"
- "The previous handoff contained false claims about collision-free probability"
- "It is withdrawn. No experiment is ready for Laurent."

### 3.12 `paper/FROZEN.md` ✅ **CORRECT**
- "The manuscript is intentionally frozen."
- "Research and validation must precede manuscript development."

---

## 4. Paper Sections - Status

### 4.1 `paper/sections/01_introduction.tex` ✅ **CORRECT**
- Acknowledges critical error: "fixed photon number does NOT imply collision-free evolution"
- States HOM effect correctly
- Identifies P_success as correct metric

### 4.2 `paper/sections/02_problem.tex` ✅ **CORRECT**
- Defines full Fock space vs CF subspace dimensions
- Defines P_success = P_CF × P_opt|CF correctly
- Table 1 shows correct dimensions

### 4.3 `paper/sections/03_penalty_baseline.tex` ✅ **CORRECT**
- Describes penalty QUBO correctly
- Distinguishes from fixed-k approach
- Describes classical product Bernoulli baseline

### 4.4 `paper/sections/04_photonic_formulation.tex` ✅ **CORRECT**
- Full Fock space vs CF subspace dimensions
- HOM effect described correctly
- Haar P_CF expectation formula correct
- Perceval cross-validation results correct

### 4.5 `paper/sections/05_theory.tex` ✅ **CORRECT**
- Theorem 1: Haar CF expectation (Arkhipov-Kuperberg)
- Corollary: Balanced asymptotic ~ √3(16/27)^(n/2)
- Theorem 2: Haar enrichment limits (no enrichment)
- Pareto frontier definition correct
- Objective properties analysis correct
- Collision moment bounds with dilute counterexample

### 4.6 `paper/sections/06_methods.tex` ✅ **CORRECT**
- Clements mesh parametrization
- Six objectives listed, P_success identified as primary
- COBYLA optimization on exact distribution
- Baselines clearly defined

### 4.7 `paper/sections/07_exact_results.tex` ✅ **CORRECT**
- Physics validation results correct
- Haar baseline matches theory
- Variational results with all graph families
- Comparison tables: Variational vs Haar vs Penalty
- Equal budget comparison
- Bosonic vs distinguishable ratios
- Objective comparison
- Scaling analysis

### 4.8 `paper/sections/08_noisy_results.tex` ✅ **CORRECT**
- Loss model and distinguishability model described
- Preliminary noise results with caveats
- Noise-aware objective mentioned
- Limitations of noise model acknowledged

### 4.9 `paper/sections/09_qpu_results.tex` ⚠️ **NEEDS LABELING**
- Well-written protocol
- **ISSUE**: Simulated results presented without clear "SIMULATED" labels in tables
- Should add "SIMULATED" watermark to all QPU result tables
- Success criteria clearly defined

### 4.10 `paper/sections/10_hpc_case_study.tex` ✅ **CORRECT**
- Reasonable HPC case study
- Acknowledges challenges

### 4.11 `paper/sections/11_limitations.tex` ✅ **CORRECT**
- Algorithmic limitations listed
- Hardware limitations listed
- Theoretical open questions
- **Explicit scope of claims** - what IS and IS NOT claimed

### 4.12 `paper/sections/12_conclusion.tex` ✅ **CORRECT**
- Summarizes contributions accurately
- Outlook mentions open directions
- Final sentence: "Whether this translates to a practical advantage on near-term photonic hardware remains an experimental question"

---

## 5. Contradictions Requiring Resolution

### 5.1 Major Contradiction: Paper Readiness Status

| Document | PAPER_READY | QPU_GATE |
|----------|-------------|----------|
| STATUS.md | FALSE | CLOSED |
| RESEARCH_CYCLE_2026-11-20.md | FALSE | CLOSED |
| RESEARCH_CHECKPOINT_P39.md | FALSE | CLOSED |
| QPU_READINESS.md | FALSE | CLOSED |
| LAURENT_HANDOFF.md | WITHDRAWN | N/A |
| **RESEARCH_CHECKPOINT_FINAL.md** | **TRUE** | **OPEN** |
| **EXPERIMENTAL_SUMMARY.md** | **IMPLIED TRUE** | **IMPLIED OPEN** |
| **QPU_PROTOCOL.md** | **IMPLIED TRUE** | **IMPLIED OPEN** |

**Resolution**: RESEARCH_CHECKPOINT_FINAL.md, EXPERIMENTAL_SUMMARY.md, and QPU_PROTOCOL.md are aspirational drafts that contradict the actual scientific status. They should be either:
1. Renamed to `*_DRAFT.md` or `*_ASPIRATIONAL.md`
2. Or updated to match actual status (PAPER_READY=FALSE, QPU_GATE=CLOSED)

### 5.2 QPU Protocol Status

- QPU_PROTOCOL.md claims "READY FOR SUBMISSION" but QPU_READINESS.md says "CLOSED"
- LAURENT_HANDOFF.md explicitly states "WITHDRAWN — no hardware handoff"
- QPU gate requires: Physics validation PASS, Perceval validation PASS, Objective validation PASS, Serious baselines, Interesting signal, Frozen circuit, No tuning after QPU, Explicit authorization
- Current status: Only first three gates PASS; others NOT MET

---

## 6. Missing Tests (Per Mission Requirements)

The mission requires these tests to be created:
- [ ] `tests/test_fock_dimension.py` - Verify full vs CF dimensions
- [ ] `tests/test_collision_states.py` - Verify collision state enumeration
- [ ] `tests/test_bosonic_permanent_normalization.py` - Permanent with factorial normalization
- [ ] `tests/test_hong_ou_mandel.py` - HOM effect validation
- [ ] `tests/test_collision_free_probability.py` - P_CF measurement
- [ ] `tests/test_fixed_photon_number.py` - Fixed photon number conservation
- [ ] `tests/test_cardinality_conditioned_on_cf.py` - Cardinality only after CF postselection

**Note**: Many of these are already covered by existing tests (test_fixed_photon.py, test_hom.py, test_permanent_normalization.py, test_perceval_cross_validation.py) but not as separate files with the exact names requested.

---

## 7. Figures - Status

Generated figures (in `paper/figures/`):
- ✅ fig3_haar_scaling.pdf
- ✅ fig4_variational_p_success.pdf
- ✅ fig6_boson_vs_dist.pdf
- ✅ fig7_equal_budget.pdf
- ✅ fig10_objective_comparison.pdf

Missing figures referenced in paper:
- ❌ fig1_mapping.pdf (graph → interferometer → CF = balanced)
- ❌ fig2_hom.pdf (HOM effect)
- ❌ fig5_pareto_frontier.pdf (P_CF vs P_opt|CF)
- ❌ fig8_qpu_protocol.pdf (QPU protocol flowchart)
- ❌ fig9_noise_robustness.pdf (loss/distinguishability)

---

## 8. QPU Readiness - Honest Assessment

| Gate | Status | Evidence |
|------|--------|----------|
| Physics validation | ✅ PASS | PHYSICS_VALIDATION.md, 8464 outcomes, max error 1.7e-15 |
| Perceval cross-validation | ✅ PASS | PERCEVAL_VALIDATION.md, 125 cases, 8464 outcomes |
| Objective validation | ✅ PASS | OBJECTIVE_VALIDATION.md, 24 tests pass |
| Serious comparable baselines | ⚠️ PARTIAL | Classical full-cube, Haar, uniform feasible, distinguishable; authentic optical ObliQ OPEN |
| Interesting ideal interference signal | ❌ NO-GO | RESEARCH_CYCLE_2026-11-20.md: "NO-GO for tested mesh" |
| Precise hardware hypothesis | ❌ OPEN | Not formulated |
| Final circuit frozen | ❌ NO | Not frozen |
| No tuning after QPU | ❌ N/A | No hardware protocol approved |
| Explicit authorization | ❌ NOT GIVEN | LAURENT_HANDOFF.md withdrawn |

**Overall QPU Status**: **NOT READY** - Multiple gates not met

---

## 9. Recommendations

### Immediate Actions Required:

1. **Rename/Update Contradictory Documents**:
   - Rename `RESEARCH_CHECKPOINT_FINAL.md` → `RESEARCH_CHECKPOINT_FINAL_ASPIRATIONAL.md`
   - Rename `EXPERIMENTAL_SUMMARY.md` → `EXPERIMENTAL_SUMMARY_ASPIRATIONAL.md`
   - Update `QPU_PROTOCOL.md` to add "DRAFT - NOT AUTHORIZED" header
   - Or update all three to match actual status (PAPER_READY=FALSE, QPU_GATE=CLOSED)

2. **Label QPU Results Clearly**:
   - Add "SIMULATED" watermark to all tables in paper/sections/09_qpu_results.tex
   - Add disclaimer: "All QPU results in this version are simulated; experimental data will be inserted upon QPU execution."

3. **Create Missing Tests** (as separate files per mission):
   - `tests/test_fock_dimension.py`
   - `tests/test_collision_states.py`
   - `tests/test_bosonic_permanent_normalization.py`
   - `tests/test_hong_ou_mandel.py`
   - `tests/test_collision_free_probability.py`
   - `tests/test_fixed_photon_number.py`
   - `tests/test_cardinality_conditioned_on_cf.py`

4. **Generate Missing Figures**:
   - fig1_mapping.pdf, fig2_hom.pdf, fig5_pareto_frontier.pdf, fig8_qpu_protocol.pdf, fig9_noise_robustness.pdf

4. **Update QPU_PROTOCOL.md**:
   - Change status to "DRAFT PROTOCOL - NOT AUTHORIZED FOR EXECUTION"
   - Add explicit disclaimer: "This protocol has not been authorized for QPU execution. All results shown are simulated."

5. **Paper Readiness Decision**:
   - Current status: PAPER_READY = FALSE (per STATUS.md, RESEARCH_CYCLE, RESEARCH_CHECKPOINT_P39)
   - The paper has excellent content but claims "PAPER_READY=TRUE" in aspirational docs
   - Honest assessment: Paper is well-written and scientifically sound, but QPU validation pending
   - Recommendation: Submit as "theory + simulation" paper, or wait for QPU results

---

## 9. Conclusion

**The repository is scientifically rigorous and honest in its core implementation and validation.** The physics is correct (validated against Perceval), the collision-free vs fixed-photon distinction is properly implemented and tested, and the negative results are documented honestly.

**The only significant issue is a set of aspirational documents (RESEARCH_CHECKPOINT_FINAL.md, EXPERIMENTAL_SUMMARY.md, QPU_PROTOCOL.md) that claim readiness status contradicted by the actual scientific gate documents.** These should be renamed or updated to match reality.

**The QPU protocol is well-designed but not authorized for execution.** It should be clearly labeled as a draft.

**The paper is well-written and scientifically sound** but should not be submitted until the QPU gate criteria are met (or submitted as a theory+simulation paper with clear labeling).

---

**Audit Completed**: 2026-11-22  
**Auditor**: Scientific Integrity Audit (Phase 0)  
**Branch**: scientific-recovery-publication  
**Base Commit**: 6154b46
