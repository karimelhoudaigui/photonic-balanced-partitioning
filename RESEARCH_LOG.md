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

## Research restart checkpoint

2026-11-20. Base Git:847d7a0e05cdf7fa8ca50c68f51f8d7e03158508. Previous completion claims above were preliminary and are superseded by executed records below. Manuscript frozen; no QPU access.

## Experiment E-000-PHYSICS

Question: Are the independent Fock amplitudes physically correct?

Hypothesis: Full amplitudes, including collisions and odd photon numbers, agree with Perceval.

Protocol: 60 Haar circuits,125 input/circuit cases,8464 full Fock outcomes; analytic identity/permutation/phase/BS/HOM/vacuum tests.

Code: `experiments/validation/run_physics_validation.py`

Seed(s): Internal fixed seeds listed per raw circuit.

Raw data: `experiments/validation/`; manifest `experiments/validation/manifest.json`.

Timestamp: 2026-11-20T17:41:41.374351+00:00; source Git: `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`; status: completed; hashes before/after and outputs in the manifest.

Result: Full normalization error4.219e-15; probability mismatch1.776e-15; tol1e-10.

Interpretation: PASS for the documented ideal small cases.

Alternative explanation: Agreement of numerical simulators alone is not hardware validation.

Decision: KEEP

## Experiment E-001

Question: What is the Haar collision-free baseline at balanced density?

Hypothesis: The known exact expectation d_CF/D_full predicts the ensemble mean.

Protocol: 1000 draws each n4/6/8,250 draws n10; fixed input |1^k 0...>.

Code: `experiments/run_research.py haar`

Seed(s): 20261120+n*100000+index

Raw data: `experiments/E01_haar_collision_baseline/`; manifest `experiments/E01_haar_collision_baseline/manifest.json`.

Timestamp: 2026-11-20T17:48:06.811843+00:00; source Git: `c7876adeffe7031f77e1ab71a14e3108c4f657cd`; status: completed; hashes before/after and outputs in the manifest.

Result: Means .598496/.358447/.212118/.125882; all four P_CF marginal95%intervals contain the prediction.

Interpretation: Known Haar law reproduced; not a new contribution or an optimized-circuit bound.

Alternative explanation: A marginal confidence interval can miss its value among many metrics; no simultaneous inference.

Decision: KEEP

## Experiment E-002

Question: Does mesh optimization beat equally budgeted Haar search, and do bosons help?

Hypothesis: A genuine interference benefit must survive reoptimization of distinguishable photons.

Protocol: Six families, two instance seeds, three initial seeds; n4/6/8; success-oracle COBYLA and best-of120 Haar, three models.

Code: `experiments/run_research.py optimization`

Seed(s): Graph:20261120+10000*n+instance; train:20261120+100000*n+1000*instance+repeat; sampling train seed+77.

Raw data: `experiments/E02_ideal_optimization/`; manifest `experiments/E02_ideal_optimization/manifest.json`.

Timestamp: 2026-11-20T17:48:43.362609+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: n8 bosonic mean success .294974, distinguishable .691744; bosonic Haar .034819.

Interpretation: Optimization helps state preparation; no bosonic benefit established.

Alternative explanation: C* is supplied; success improvement over the first circuit is partly imposed by best-so-far selection.

Decision: REJECT

## Experiment E-003

Question: Which losses suppress acceptance or concentrate real success?

Hypothesis: The unnormalized moment has a rejection loophole; conditional energy/CVaR need collision accounting.

Protocol: Nine losses, n4, six families,2 instance seeds,3 starts, budget120.

Code: `experiments/run_research.py optimization`

Seed(s): Same deterministic graph/initial seed formulas as E02.

Raw data: `experiments/E03_objectives_pareto/`; manifest `experiments/E03_objectives_pareto/manifest.json`.

Timestamp: 2026-11-20T17:48:44.408210+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: Bad moment meanP_CF=.013038; success=.013005. Collision-aware success=.960115; lower-CVaR=.457878.

Interpretation: Reject bad objective; physical success and factorization are mathematically the same objective.

Alternative explanation: Conditional lower-tail saturation and finite-budget optimizer effects are not a universal Pareto theorem.

Decision: REJECT

## Experiment E-004

Question: Do depth and optimizer produce a robust mechanism?

Hypothesis: A shallow mesh can appear strong because of finite budget or label reachability.

Protocol: n4/6, six families,one instance seed,three starts; full/depth2;COBYLA,Nelder-Mead,SPSA,random mesh.

Code: `experiments/run_research.py optimization`

Seed(s): Fixed E02 seed formulas; actual calls retained.

Raw data: `experiments/E04_optimizers_depths/`; manifest `experiments/E04_optimizers_depths/manifest.json`.

Timestamp: 2026-11-20T17:51:19.162490+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: Optimization results vary strongly; shallow support excludes many balanced outcomes.

Interpretation: No general optimizer/depth winner inferred; triggers label falsification E09.

Alternative explanation: Natural path/community labels favor consecutive occupied input modes.

Decision: FOLLOW-UP

## Experiment E-005

Question: Does the original shot protocol establish equal-cost search?

Hypothesis: Maximum budgets alone are insufficient if models stop early or uniform batches are analytic allocations.

Protocol: Same graph grid; conditional collision-aware shot loss, penalties, heldout counts.

Code: `experiments/run_research.py shots`

Seed(s): Same E02 seed formulas; distinct heldout seeds.

Raw data: `experiments/E05_equal_shots/`; manifest `experiments/E05_equal_shots/manifest.json`.

Timestamp: 2026-11-20T17:48:45.641691+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: Raw outputs completed, but penalty calls stop early and uniform training batches were not drawn.

Interpretation: Superseded by E05b for all equal-cost and discovery claims.

Alternative explanation: Valid final probabilities do not make allocated training shots observed draws.

Decision: REJECT

## Experiment E-005b

Question: At exactly equal ideal attempts, does a trained bosonic sampler improve actual discovery?

Hypothesis: A benefit must persist after every training draw and first optimum are charged.

Protocol: 756 model runs:120x256 actual training draws+4096 heldout per run, seven variants;26,320,896 ideal attempts.

Code: `experiments/run_equal_budget.py`

Seed(s): Base20261120; same graph/train seed formulas as E02; PCG64; raw per-evaluation parameters/counts.

Raw data: `experiments/E05b_exact_equal_budget/`; manifest `experiments/E05b_exact_equal_budget/manifest.json`.

Timestamp: 2026-11-20T17:52:00.456331+00:00; source Git: `af0978455258bb44ef51d328e9ac977546eb2331`; status: completed; hashes before/after and outputs in the manifest.

Result: n8 final means .067873 boson/.137707 distinguishable; median first optimum89/27/uniform17.5; all756 runs found optimum during training.

Interpretation: NO-GO benefit claim for this tested route; final waiting time is not discovery cost.

Alternative explanation: Limited graph population, shot optimizer sensitivity, tiny exact-enumerable sizes; not an impossibility result.

Decision: REJECT

## Experiment E-006

Question: Do the collision moment bounds hold numerically?

Hypothesis: The pair-moment identity supplies valid upper/lower bounds.

Protocol: Original full Fock checker; tolerance was written as one chained assertion.

Code: `experiments/run_research.py structure at commitc7876ad`

Seed(s): Base20261120+n*10000+index

Raw data: `experiments/E06_structural_checks/`; manifest `experiments/E06_structural_checks/manifest.json`.

Timestamp: 2026-11-20T17:48:07.317948+00:00; source Git: `c7876adeffe7031f77e1ab71a14e3108c4f657cd`; status: failed; hashes before/after and outputs in the manifest.

Result: Failed:upper tolerance was accidentally cancelled; traceback and failed manifest preserved.

Interpretation: Implementation failure, not theorem counterexample.

Alternative explanation: Roundoff at k2 analytic equality triggers a tolerance-free upper comparison.

Decision: FOLLOW-UP

## Experiment E-006b

Question: Does the corrected tolerated check pass?

Hypothesis: Separating upper/lower tolerated assertions fixes the diagnostic without changing physics.

Protocol: 120 Haar circuits n4/6/8/10+4 disjoint-support controls.

Code: `experiments/run_research.py structure`

Seed(s): Base20261120+n*10000+index

Raw data: `experiments/E06b_structural_checks/`; manifest `experiments/E06b_structural_checks/manifest.json`.

Timestamp: 2026-11-20T17:51:21.278337+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: PASS:moment identity, collision bounds, disjoint-support boson/distinguishable equality.

Interpretation: Finite evidence matches the separately audited proof.

Alternative explanation: Numerics cannot prove the universal characterization.

Decision: KEEP

## Experiment E-007

Question: Does an anchor hide classical solution discovery?

Hypothesis: Strong spectral/hybrid results can arise before any multiphoton interference.

Protocol: All36 graph slots;2 models,2 objectives,3 starts;zero-angle mesh after spectral permutation.

Code: `experiments/run_research.py optimization --anchor`

Seed(s): Same deterministic E02 formulas; spectral is deterministic per actual graph.

Raw data: `experiments/E07_spectral_hybrid/`; manifest `experiments/E07_spectral_hybrid/manifest.json`.

Timestamp: 2026-11-20T17:51:20.124601+00:00; source Git: `5ce1dc127a95c092a433f6b5a4ea6ed7b8865f38`; status: completed; hashes before/after and outputs in the manifest.

Result: Spectral alone solves27/36 graph slots; the other9 can show zero-start plateaus.

Interpretation: High hybrid success is largely a classical preprocessing result.

Alternative explanation: Eigensolve cost and label effects must be charged; an optimizer plateau is not a representation obstruction.

Decision: REJECT

## Experiment E-008

Question: Does low collision probability force a classical independent-particle approximation?

Hypothesis: A spatial-overlap certificate can hold while collision-only dimension-uniform inference fails.

Protocol: 240 full-Fock interpolations;9 rational balanced examples; full-Fock construction n4/8/12; independent proof audit.

Code: `experiments/run_coherence_check.py`

Seed(s): 20261120+100*n+seed for interpolation; rational examples deterministic.

Raw data: `experiments/E08_coherence_certificate/`; manifest `experiments/E08_coherence_certificate/manifest.json`.

Timestamp: 2026-11-20T17:53:09.212575+00:00; source Git: `72681fb2af275823de2b62d3a549168e826fecd7`; status: completed; hashes before/after and outputs in the manifest.

Result: TV<=min(1,(Per(B)-1)/2) and cycle bound pass; balanced delta=2/(k+2)->0 butTV=.5.

Interpretation: Proof-backed diagnostic obstruction; novelty OPEN. The example itself is classically easy.

Alternative explanation: Spectator construction isolates only two interfering photons; it does not establish a many-body computational effect.

Decision: KEEP

## Experiment E-009

Question: Is shallow success an invariant property of the underlying graph?

Hypothesis: Changing labels can make optimal bisections unreachable with a depth2 mesh.

Protocol: 12 n6 graph slots, original+4 seeded permutations,depth2/full,2 models,120-call oracle training;240 runs.

Code: `experiments/run_label_control.py`

Seed(s): Graphseed as E02; permutations graphseed+99000+label; same circuit start across labels.

Raw data: `experiments/E09_label_control/`; manifest `experiments/E09_label_control/manifest.json`.

Timestamp: 2026-11-20T17:56:57.525765+00:00; source Git: `37a4a5029fbba8c0e24d9347e3733dac82af6702`; status: completed; hashes before/after and outputs in the manifest.

Result: Bosonic shallow .875 original/.802 shuffled;5/48 shuffled slots structurally exclude all optimum targets.

Interpretation: A label/reachability artifact exists; enrichment does not universally vanish.

Alternative explanation: Single training seed per label slot; full depth also has finite-budget sensitivity.

Decision: FOLLOW-UP

## Proof and review checkpoint

Theorem proofs:theory/proven_results.md and theory/near_collisionless_bound.md. Independent reviews:reports/THEORY_AUDIT.md (supplementary independent reconstruction by objectives agent recorded in DECISIONS), reports/NEAR_COLLISIONLESS_INDEPENDENT_REVIEW.md; execution/protocol audit reports/EXPERIMENT_PROTOCOL_AUDIT.md; full output/source checks reports/RESULTS_AUDIT.json. Novelty OPEN. Current scientific decision:NO-GO tested benefit route, GO only for bounded mathematical/literature follow-up; PAPER_READY=FALSE; QPU closed.
