# Research Log

Latest continuation: P90a independently audited NO_POSITIVE_SIGNAL; P96
independently reviewed classical theorem plus exact/native finite validation
PASS; P98 whole-law hierarchy proved under a certified trace gap. Positive
graph optimization target remains OPEN; higher-degree experiment CODE ONLY.
Current evidence:
reports/P82a_ROOT_FINAL_CHECKPOINT.md,
reports/P90_P91_P92_ROOT_THEORY_CHECKPOINT.md and
research/P90a_INDEPENDENT_RECORDED_AUDIT_RECEIPT.md and
research/P45_LIVE_STATE.md. Earlier entries retain their historical state.

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

## Experiment QWEN-N4-001 — 2026-11-21

Question: Does the existing collision-aware n4 training protocol establish a
useful interference-dependent mechanism after accounting for collisions?

Hypothesis: Any proposed benefit must survive reoptimized distinguishable
controls,fresh seeds and serious feasible classical cost accounting.

Protocol: Astra supplied three fixed graphs,two statistics,the same paired starts,
32 exact COBYLA objective calls per run,and a fresh-seed replication. Loss is
conditional cut+2*(1-P_CF);the optimum is diagnostic only. No physical shots.
Qwen ran the commands in an isolated worktree. The critic failed to finish;
Astra independently performed the adversarial/numerical audit. This is not
recorded as a successfully completed autonomous Qwen research cycle.

Code: scripts/qwen_n4_probe.py;independent checker scripts/audit_qwen_n4.py;
bounded controller scripts/run_research_cycle.py.

Seed(s): 20261121..20261123;replication20261221..20261223.

Raw data: results/qwen_n4_supervisor/{initial,replication}/raw.json;original
locations and hashes in provenance.json. Execution records:
results/qwen_cycles/20261121T002702Z-cycle/,
20261121T003401Z-cycle-resume/,20261121T004103Z-supervised-replication/.

Timestamp/Git: first start2026-11-21T00:27:02.423071+00:00;
scientific source base15b97653cb88beb65b77f7425846ad4a41541324.
Canonical independent computation manifest:results/qwen_n4_supervisor/audit/manifest.json,
status completed and validator PASS;source and raw hashes retained.

Result: 36runs/1152evaluations independently checked;18best bosonic circuits
agree with Perceval to3.33e-16. Initial cycle success .988357bosonic/.974014
distinguishable reverses to .715280/.984862 on fresh seeds. Path also reverses
ordering;weighted favors distinguishable in both batches. No population inference.

Interpretation: INCONCLUSIVE for useful interference-dependent optimization;
REJECT advancement to QPU/paper. Keep the finite calculations. Qwen's narrative
invented uncertainty and mixed labels;it is preserved unchanged and rejected.

Alternative explanation: ordinary finite-budget optimization in either model;
n4 can be solved by six feasible classical cut evaluations. Equal exact loss-call
counts do not establish equal physical-shot or total classical cost.

Decision: KEEP raw evidence;REJECT narrative/advancement;FOLLOW-UP only a changed
optimum-blind mechanism. Overall research goal remains open. Paper untouched.

## Infrastructure checkpoint — 2026-11-21

Machine audit,model selection,seven agent definitions and a bounded sequential
worktree orchestrator are committed as external research infrastructure. Basic
Qwen read/test/report smoke PASS. Native subagents/Agent Team FAIL;configuration
flags are not execution evidence. No paid fallback or larger model download.
Reports:AGENT_INFRASTRUCTURE.md,LOCAL_MODEL_SELECTION.md,
QWEN_INFRASTRUCTURE_VALIDATION.md,ASTRA_QWEN_FIRST_CYCLE_AUDIT.md.
Full current working-tree pytest:192passed;42tests belong to earlier Phase2
drafts preserved outside the scoped infrastructure change. No scientific gate opened.


## Phase3 audited checkpoint — 2026-11-22

Scope: improve the scientific basis, not the manuscript. Zero physical shots.
Fixed scientific seed20261121 where stochastic, explicit source conventions.

- P30, authentic static optical component: archive SHA8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948;
  10 coincidence checks, 48 convergence checks and nine archive-unitary checks,
  plus a separate81-occupation reconstruction. Literal/corrected angle variants
  remain distinct. KEEP finite component validation; full ObliQ algorithm OPEN.
  Commitc3b83ef; experiments/P30_optical_component/manifest.json;
  reports/PHASE3_OPTICAL_PENALTY.md.
- P31, penalty washout: 972 unitary,36 Fock and36 limit-gap checks. Exact
  fixed-input/order proof independently reconstructed, including an exact
  decoder-limit tie obstruction. KEEP restricted theorem; REJECT interpretation
  as an optimization lower bound or universal two-candidate decoder.
  Commiteda41e9 plus review6fcfc94;
  experiments/P31_washout_bound_audit/run_001/manifest.json;
  reports/PHASE3_WASHOUT_INDEPENDENT_REVIEW.md. Generic washout is known;
  exact-kernel attribution remains OPEN.
- P32, resource accounting: 195 rational cases,965 click values,120 circuits.
  KEEP corrected operational distinctions; REJECT inferring graph benefit or
  a universal photon optimum from Haar feasibility. Commit2ed2e7d;
  experiments/P32_threshold_audit/run/manifest.json;
  reports/PHASE3_THRESHOLD_AUDIT.md. Original draft loss formulas were retained
  after independent agreement; counterexamples concern unqualified extensions.
- Occupation objective: 32 complete-distribution circuits, eight Perceval
  comparisons; exact moment and nonnegative same-frame mean-gap identities.
  KEEP theorem; REJECT expecting a bosonic mean-energy improvement for this
  nonnegative quadratic occupation objective. Success-tail ordering does not
  follow. Commit98e4ecc; experiments/occupation_objective_validation/run/manifest.json;
  theory/phase3_occupation_dominance.md.
- P33 success scope: seven exact rational cases plus a zero-CF guard. KEEP
  conditional-TV bound with max acceptance denominator; REJECT vanishing-TV
  implies vanishing rare-success ratio. The factor-two toy has an explicitly
  stronger correlated classical control. Commit385293e;
  experiments/P33_density_success_scope/run/manifest.json.
- P33 exact density theorem: independent review at75e5831 proves the stated
  dominant-support/density implication and sharp leading refined coefficient.
  Review4420e17 includes five rational cases/50 occupations and found a genuine
  floating cancellation witness. Fix77a8588 replaces subtraction by positive
  sums and a stable series; estimates remain NOT interval certified. KEEP exact
  proof, no automatic novelty or hardware inference. Attribution report66141f5
  identifies N1/N2 as prior-art consequences; new composition attribution OPEN.
- Low-rank threshold expectation route: primary sources already contain the
  proposed permanent DP. REJECT novelty; preserve proof/source dictionary at
  28f096c. Cheap evaluation does not imply easy optimization or quantum benefit.
- P21 classical search control integrated2996904:2880 searches,120 scored queries
  each,345600 charged queries; spectral setup is charged. The original untracked
  P20 drafts remain separate pending review.

Each manifest retains its own observed timestamp, actual argv, recorded base
commit and before/after/output hashes; historical inputs are checked at those
revisions. No original raw result was rewritten to match a later checkpoint.

## Qwen native scientific-cycle failures and changed interface — 2026-11-22

First density native cycle20261121T202352Z: all seven roles were observed but
replication failed because the model omitted --output. Primary data and the
failed replication manifest remain at branch272c3fd; not accepted as a completed
cycle. Second20261121T205203Z (77a8588): only six roles; the runner used Bash
for a Python file and then an unavailable interpreter. No scientific command
completed. KEEP failures; distinguish parent exit0 from workflow INCONCLUSIVE.

Changed bottleneck: b1ff914 introduces four local parameterless MCP actions that
construct fixed argv under a pinned Python, preserve data, enforce time limits
and prohibit transport replay of scientific writes. Basic bridge protocol and
all264 current working-tree tests pass. Native action smoke and then the full
nine-dispatch/seven-role workflow are under verification. Qwen's generated
narrative is never sufficient scientific evidence. Native saved-Workflow
subagents have passed earlier independent two-child handoff validation;
experimental Agent Team lifecycle remains FAIL. Paper/QPU gates remain closed.

Two untracked root P33 directories with unresolved provenance are preserved and
excluded from accepted evidence, per reports/P33_UNATTRIBUTED_ROOT_DATA.md.


## P33 completed native replication — 2026-11-22

QUESTION: does the fixed density/collision certificate survive both complete-law
grids and the declared obstructions? Same fixed contract, numerical correction
77a8588; no optimizer or paper writing. Source/controller85b3414, start
2026-11-22T01:48:22.554784Z. Seven Qwen roles, nine distinct sequential contexts,
four real typed MCP actions. Both manifests completed; runtime287.93sec total.
Primary/replication seed offsets0/100000, no overlap. All300 full-grid circuits
m4..12,14 sharpness cases,12 factorized dilute controls and72 certificate-only
cases retained. No full Fock simulation beyondm12. Physical shots0.

Astra independently checks every basis, raw normalization, TV, CF mass and
pair moment, plus12 selected circuits with spectral-frame reconstruction,
Perceval and a separate labelled DP. Maximum new crosscheck error6.67e-16.
Finite bound checks use1e-9 tolerance; positive excess2.23e-16 is retained,
not called an interval certificate. No sampling confidence intervals invented.
The worker tree passes248 tests; current root264 includes16 untracked drafts.

Raw origin commitfe7d616; root preserved/hash-mapped evidence, audit and figures
commitb8b04ac. Canonical computation manifest:
results/P33_density_supervised/20261122T014822Z/audit/manifest.json, completed.
Native raw receipts, exact handoffs and supervisor_decision.json:
results/qwen_cycles/20261122T014822Z-workflow/.

DECISION: SUPPORTED finite assertions within tolerance; KEEP execution/data;
REJECT Qwen narrative that changed k/m to1, misstated c>=M, confused large
certificate-only cases with full simulation, or introduced nonexistent training.
Complete audit: reports/ASTRA_P33_COMPLETED_CYCLE_REVIEW.md. Exact theorem
independently reviewed4420e17, novelty OPEN; original algorithm benefit OPEN;
paper/QPU closed. This is a successful supervised execution cycle, not proof
of reliable autonomous scientific reasoning.

## P34 adaptive replacement consequence — 2026-11-22

QUESTION: can a per-circuit absolute-TV condition control a finite classically
adaptive fresh-input transcript at equal attempts? Coordinator derives ordinary
sequential coupling product and history-sensitive bounds, with charged
classical reference costs. Primary source Levin–Peres §4.2/Prop4.7 extracted.
Four exact rational policies and an initial-identity control preserve all Fock
outcomes and histories; bounds pass. T3 TV0.02900506 versus product0.16186482
and expected-budget0.03149941. Initial TV0 does not control later adaptive steps.
Code/proof/raw42d9eff, experiments/P34_adaptive_replacement/run/manifest.json,
completed. No random draws, noise or physical shots. KEEP conditional consequence;
fresh independent proof review deferred by quota; no new coupling novelty.

## Cross-field attribution refinement — 2026-11-22

A second coordinator search strategy links row leakage to MAP/Bayes error and
physical pair moments to a differently weighted quadratic impurity. Rioul2023,
DOI10.3390/e25070978, equations3/5/75/76, authenticated and translated with the
weight distinction explicit. Row inequalities are prior-art consequences, not
new discoveries. Full photonic composition attribution remains OPEN; no global
novelty inference from absent hits. See research/phase3_density_crossfield_novelty.md.


## Fresh reviews and integration — 2026-11-22

P34 fresh review3c43eda found the original missing e_t range; correctedb3b0219
now has an explicit independent proved-as-written addendum. Both verdicts are
retained. Reproductionde77a14 has identical exact data hash to the initial run,
with the corrected proof pinned separately; old manifests are not rewritten.

P33 numeric review9e8bd82 documents finite roundoff/subnormal limits. Its original
manual manifest has an empty declared-results list and is NOT valid v2 evidence.
Its report/source/outputs remain inspectable; the separate coordinator rational
underflow run64ad463 has valid failed/completed records. Literature review715143f
finds row-max nonnegative-Stiefel rounding and the Gram perturbation step known;
full photonic composition attribution stays OPEN. Optional theory dependencies
now pin mpmath1.3.0 as well as SymPy1.14.0; historical pyproject input hashes are
validated at their frozen revisions, not silently replaced by later metadata.

P20: both historical archives validate against unchanged sources. Fresh review
8cb20c2 (maina4d4745) checked labels/metrics/frozen parameters and32 count spot
checks without rerunning the campaigns. Initial16 focused tests pass. Archives
and original sources are integrated5dbdbc3. Both campaigns choose zero interaction;
no tested quantum optimization signal. Source drivers overwrite fixed outputs:
ARCHIVE_NOTE.md warns against in-place replay. Budgets and bootstrap are scoped
in the independent report; equality of replacement counts is constructed.

## P35 executable classical threshold baseline — 2026-11-22

QUESTION: can the known rank1/2 vacuum DP match full physical threshold moments
and original QUBO means without computing its own full outcome law? Source678f79d;
raw/reportc6c1807. Exact Gaussian-rational coefficient arithmetic, physical frame
validation by default; binary encoding explicitly carries no physical guarantee.
Twelve seeds20261122..33, six exact physical frames and six encoded QR frames,
including N=m. All six rational full-Fock comparisons are exact equalities;
12Perceval comparisons give mean/pair error5.56e-16 and energy error7.11e-15.
Manifest experiments/P35_threshold_marginal/run/manifest.json completed/valid.
Whole repository271tests pass. KEEP as a known classical control, not novelty,
full training reproduction or hardware benefit. No physical shots.

## P36 stronger leakage conjecture — 2026-11-22

QUESTION: can TV<=min(1,delta) replace the looser proved P33 envelope? Protocol
bfa5a22 retains all256 full occupation circuits. Initial run failed before math
on an output-directory conflict; fresh run_002 completed in1.834s with no
counterexample. Twelve fresh Perceval and16 collective closed-form checks pass,
max Perceval error4.44e-16. Exact algebra closes the sharp k2 case and refutes
per(B)-1<=2delta with a physical k3 witness, without refuting the TV conjecture.
All records/proof/source draft retained224327c; general k>=3 remains OPEN.
The literature review was quota interrupted before commit; its retained draft
is explicitly marked. Physics messages were reconstructed, not called a final
independent review.

P36b: frozen phase-sensitive search3f7f7b3 completed17856 calls under bounded
single-thread budgets. No falsifier; all8 cells and all16 stored winners audited,
Perceval max error8.89e-16. All traces retained. This changes the attack to
nongeneric phase-sensitive frames but does not prove the conjecture. Its missing
phase-cancellation implication remains open; no unchanged rerun is justified.
Paper remains frozen; QPU_GATE=CLOSED; original optimization benefit unestablished.

## P37 loss-aware Haar source phase diagram — 2026-11-22

QUESTION: how do uniform losses change threshold feasibility per attempt and
per injected photon? HYPOTHESIS: two/four source candidates suffice. PROTOCOL:
research/P37_LOSS_SOURCE_CONTRACT.md, source/proof frozen1d65279. CODE:
experiments/phase3_loss_source_probe.py. No random seeds: exact Fraction sums.
RAW: experiments/P37_loss_source/run/data/, completed valid v2 manifest;
retainedd402374. All112 cells,1610 source probabilities and36 root brackets
pass; independent positive-sum formulas coincide. Runtime0.397s, zero full
Fock simulations and zero physical shots, including large m.

ADVERSARIAL CHECK: separate coordinator implementation uses a normalized Polya
urn, de Casteljau transform and recurrent endpoint weights. Every value, cost,
maximizer, sign and trace matches exactly; runtime0.478s. Valid completed record:
experiments/P37_loss_source/review/manifest.json. This is self-review, not a
fresh agent. Proof self-review checks endpoint ties, size bias, root order and
peak-normalized tails. At m128 critical scaled losses are .992156 and
.953327/1.953726/2.938557 versus self-reviewed limits1 and1/2/3.

RESULT: finite phase theorem and boundary limit survive self-review.
INTERPRETATION: exact resource corollary of known Haar counting, not graph
enrichment. Waiting cost requires refreshed Haar draws. ALTERNATIVE EXPLANATION:
known counting and elementary signs suffice; novelty unassessed. DECISION:
SUPPORTED finite assertions; KEEP resource audit, FOLLOW-UP fresh proof/source
review. Original optimization goal OPEN; paper/QPU closed.

P37 fresh review: after quotas reset, /root/physics independently reconstructed
the frozen proof without reading coordinator verdict/numeric probe. Verdict
proved as written; commit94b5099 integrated7729b91. Ratios, size-bias indices,
global maxima, ordered roots and peak-normalized asymptotic checked. Independent
m8 polynomials, endpoints and40-step rational brackets pass;0.582s CPU. Valid
manifest experiments/P37_independent_review/manifest.json; source proof unchanged.
This supersedes the pending-proof-review state, not the open novelty/gain gates.

## P35 separate review and guard correction — 2026-11-22

Reviewer6258cd5, integrated56a34d0, derives the Gaussian-rational DP invariant
and extraction separately. All190 one/two-output marginals on12 archived frames
match an independent exact Gram/Ryser reference. Seven original tests pass;
three manifests valid against the pre-fix worktree. Reviewer proposed the API
earlier but did not implement the component: independence limit explicit.
An invalid NaN cap silently bypassed limits; retained in original audit data.
Coordinator fixb5d2888 requires integer finite caps, rejecting bool/float/NaN,
with23 focused and287 total tests passing, six cache warnings. Old-source
manifests remain frozen; no scientific numbers were rewritten or campaign rerun.

## Late-2026 source audit — 2026-11-22

Source reviewer4981832, integrated538e67b, checks exact primary versions of
Angrisani–Mhiri2611.08444v1 and Lim2611.01434v1. Fixed-loss Haar approximate
sampling statements and near-full weighted-L2/reference constants are extracted,
with key local proof/dependency passages checked and unaudited leaves explicit.
No full source theorem independently reproved or sampler implemented. Pure-loss
reference exactly matches the known binomial/Haar mixture. Fixed trained U and
eta=1-lambda/m do not follow. Finite constants can already be trivial at m64;
no blanket numerical QPU NO-GO. PDF/text hashes retained in ignored worker cache;
only the source report is versioned. KEEP as a scoped source-dependent audit.

P35 post-fix review13aa5de integrated5375202:50 invalid-input checks pass before
frame access. Separate operational receipt preserves its initial overly tight
fixture failure; original pre-fix scientific records are unchanged.

## P38 phase-preserving pinching route — 2026-11-22

QUESTION: does retaining internal group states give a sharper provable upper
bound for measured TV at k3? HYPOTHESIS: D_pinched<=delta might be sufficient.
PROTOCOL/code/proof frozen197af80. Physics proposed the finite cone reduction
before quota; Astra reconstructed its proof and implemented the pending run.
SEEDS20261201..03, rational strengths1/40,1/5,1/2,1, all36 frames retained.
RAW: experiments/P38_pinching_probe/run/, completed valid v2 record,0.501s.
Twenty-one cases have delta<5/6; six Perceval checks max1.11e-16. Zero shots.

SEPARATE CHECK: explicit ordered-tensor density blocks, no Gram square roots,
on all36 cases; runtime16.876s, pinching error9.50e-14, probability error2.23e-16.
Three exact Rayleigh controls equal the sharp rational k2 targets. Manifest
experiments/P38_pinching_probe/review/manifest.json valid/completed. Self-review,
not a fresh agent. Worker15-frame diagnostic and exact family drafts retained
with original hashes under experiments/P36_interrupted_phase_attempt/; original
worker manifest validates. Literature draft is explicitly interrupted, with its
complex-k3 cone caveat corrected in the prefix rather than silently overwritten.

RESULT: no finite refutation; exact structural/variational reductions and cone
proof. INTERPRETATION: stronger upper metric, not the observed law. DECISION:
KEEP reduction/checks; general pinched and measured inequalities OPEN.

## P38b/c compact-effect falsification — 2026-11-22

QUESTION: does the new three-effect domain yield a counterexample? Two target
deltas1/5,3/5 and seeds20261210/11, four cells. Frozen22b0a74;2076 calls,2.183s,
all solvers stop at25 iterations. Follow-up dfbd99f changes that bottleneck:
warm-start all four recorded points,120 iterations, smaller difference step.
8714 additional calls,6.019s; three iteration caps and one line-search failure.
Total10790 calls, none hidden; no certified refutation. RAW: experiments/
P38_effect_search/{run,refinement}/, both completed valid v2 manifests.
Each refinement best point has exact repaired PSD/dominance/sum-I checks and
Rayleigh lower witnesses. These are not upper certificates or global optima.
DECISION: INCONCLUSIVE. No unchanged SLSQP rerun; zero shots or new Fock trials.

Self-review also refutes a finite-witness subgoal at delta0: the correct dual
infimum0 cannot be attained by finite witnesses. Keep direct endpoint reasoning
and limiting witnesses distinct; see theory/phase3_pinching_dual_boundary.md.

## P39 exact auxiliary-envelope counterexample — 2026-11-22

QUESTION (post hoc): can the sharp k2 curve upper-bound the k3 pinched metric?
HYPOTHESIS/contract frozen2b22cd4 with d19/25,e3/25. Complete exact27-sector
Rayleigh enumeration gives lower0.490108163... above curve288/625=.4608 at
delta18/25. Exact numerator/denominator retained. Physical9mode/3photon frame
has one full-law Perceval comparison, maxerror2.78e-17 over165 outcomes; measured
TV≈.265153. Completion seed20261220, no graph/parameter selection from that seed.
RAW: experiments/P39_pinched_envelope/run/, completed valid v2 manifest,0.041s.

DIFFERENT ANALYTIC CHECK: monotone scalar eigenvalue equations give the simpler
strict lower24493/50000, with exact positive residuals at43/400 and7/50. Gap
to curve1453/50000>0. All27 weight classes checked without eigensolvers or
Rayleigh code;0.003s, valid completed review manifest. Proof/raw33328e4 and
theory/phase3_pinched_envelope_counterexample.md. Both arguments are by Astra;
fresh independent review is unavailable after the new agent quota interruption.
RESULT: REJECT only the curved pinched-state extension. Neither measured
linear/curved inequality nor the linear pinched lemma is refuted. No novelty,
graph benefit, manuscript writing or QPU progression. KEEP the exact obstruction.


## 2026-11-24 — scientific recovery and concrete publication/pilot deliverables

Request: restore rigorous science, rebuild the article and prepare a real offline Laurent dossier without QPU execution or external transmission. Branch scientific-recovery-publication; starting6154b46. Initial803-file hashes and supplied audit copy preserved before edits;356-test baseline executed. Focused independent graph/anti-oracle tests pass.

Three real isolated worker lanes delivered physics/noise (d36e2d2, integrated52e983f), numerical reconciliation (18ba18b, integratedbb09283), and offline Quandela/Perceval engineering (9e75b53, integrated3392103). Review, raw evidence and command receipts were inspected before integration. A source-hash census distinguishes43 verified completed outputs,2 source gaps,3 failed captures and2 excluded root P33 copies.

E05b756 runs/90,720 objective batches/26,320,896 ideal attempts reconstruct. No trained bosonic advantage over distinguishable means; all find optimum in training; shot order within batches unavailable. New public training losses accept no optimum, and exact-reference setup remains charged classical information. No historical optimizer campaign rerun or archived raw rewrite.

New physical noise model retains all sectors/vacuum and pure internal Gram phases. Seven-command offline pipeline independently reproduced by supervisor to results/validated/offline_pilot_2026-11-24_supervisor/. It uses explicit local_synthetic counts, known/unknown attempt cases and source hashes, zero credits and zero hardware shots. Integrated code suite at this stage455PASS; final publication-inclusive count/build/referee outcomes are recorded in reports/RECOVERY_EXECUTION_REPORT.md.

Primary thesis chosen: density-qualified replacement plus resource accounting, full exact proofs, known-ingredient attribution and open complete novelty. Article rewritten under the user's explicit authorization; old unsupported figures/claims withdrawn and retained in Git. Mathematical/physical/statistical reviews, final generated artifacts and build receipts are separate evidence. See reports/PUBLICATION_READINESS.md. Original useful-search objective and actual QPU compatibility remain open.


Release verification:484PASS in a freshly installed37-pin Python environment;16-page compiled PDF and three source-review perspectives delivered. Portable P40 replay on the integration branch reproduces all45 laws;602 historical scientific files remain unchanged. Detailed commands, hashes, review limits and unresolved publication/QPU gates: reports/RECOVERY_EXECUTION_REPORT.md.

## 2026-11-24 — P41 discovery and P42 loss-spectrum obstruction

QUESTION: can a new optimum-blind mechanism escape E05b, or can a materially
broader approach class be ruled out? Contract f09c7ec, base2744395. Three
isolated lanes explored chiral exchange, grouped encodings and new objectives.

P41/R1: a positive classical proposal reproduces the genuine cubic exchange
current with a TV remainder.72 declared cells pass sparse-Fock/Ryser checks;
favorable B-versus-D cells do not beat the proxy. P41/R2: random-wave feasible
sampling dominates grouped physical subprobabilities, independently derived
and reviewed.1260 Fock outcomes/two Perceval comparisons retained. The core
phase-twirl/Glynn ingredients are known; adaptive-history and matched-realized-
score extensions are not inferred. P41/R3: a connected L1 example refutes an
overbroad convex extension of the old quadratic mean ordering.384 exact
identities/64 graph cases pass. The fixed-k collision gap is not an optimizer.

P42 ANALYSIS: a loss-mixture spectrum and support-projector rank bound every
permitted graph/history-dependent passive controller. With cap b,
L=ceil(nQ/nC), L*binom(2k,k)*b<=1 implies uniform feasible search stochastically
dominates best newly measured cost. Source/internal-state proofs frozen525e254
pass exact-hash independent reconstruction/audit. No Haar assumption or oracle.

EXECUTION:462 exact table rows,2375 source-partition rows,80 optical checks,
CPU3.550s. Independent freeze c4a178d before execution; separate normalized
spatial/internal source and partial trace, no primary/production imports, fresh
seeds2026112471/72:42 configurations/168 laws/2880 support checks, CPU0.368s.
All finite assertions pass at1e-10; maximum residual1.4433e-15. Original
completed v2 manifests, commands, source hashes and immutable raw are versioned.

FALSIFICATION: bunched input, partial internal species and nonmonotone N refute
naive extensions. The corrected ordered block-trace bound is retained. The N8
species counterexample has an analytic derivation, not an independent N8 run.

DECISION: KEEP scoped P42 theorem/replication; REJECT identified extensions and
leading/grouped advantage arguments. Positive optimizer target/novelty OPEN.
P43 investigates global finite-angle statistics and local L1 evaluation.
No paper edit/QPU call.521PASS; five manifests valid;602 historical files and
paper unchanged. Full evidence: reports/P42_DISCOVERY_CHECKPOINT.md and
reports/P42_validation/verification.json.

## 2026-11-24 — P43 new mechanism rejected; P44 broader obstruction

P43 QUESTION: can a graph-dependent finite-angle phase-gradient echo exploit
global incumbent improvement beyond the known local-mean oracle? Design1811ad7,
code7794798, corrected strong spectral control1db2038, pre-run529PASS. Actual
sourcec062f2f, bounded runner CPU60/wall90/threads1; completed17.533394s.
Four unique weighted ER/RR graphs at16/20 modes,8/10 identical photons,8 settings,
2 seeds,896 B attempts. Gains were ZERO for B,D,phase-field andspecies4, with
CF counts373/531/896/463. All selected identity, so optical relabel draws were
NOT executed. All5 classical searches completed896+128 scores each. Anneal/
spectral find156->135 and45->37 on the20-mode graph anchors. No optimum computed.
Independent stdlib audit924b814 reconstructs all9952 raw rows, costs, anchor
scans, hashes, seeds and choices. DECISION: REJECT this family/budget, no heldout
opening, no unchanged rerun or hardware preparation. Full P43 result/raw retained.

P44 HYPOTHESIS: CF Fock normal-ordered moments are bounded by their auxiliary
thermal/permanental envelope, then by a transfer spectral norm. Rootproofb87e677:
Pr(all targetk modes click)<=E product n_i<=||T[:,A]||^(2k), including nonuniform
passive loss. Card-only physics reconstruction2d15012 predates reading the author;
exact-hash review9b240c3 proves the source as written. Any single candidate drawn
only from real clicks inherits the cap; additional/outside clicks are harmless.
Arbitrary internals under commonT use separate k! cap. P42's fixed-target budget
argument yields domination when L*binom(2k,k)*b<=1, hence identical eta0<=1/4
suffices at equal counts. Mean transmission is NOT a spectral norm calibration.

FRESH FINITE VALIDATION: isolated prereg0687912,190 explicit passive-dilation
configurations/1240 support rows, new seeds2026112483/84, stdlib+NumPy only.
All system/environment occupations, losses/vacuum and product/correlated internal
states retained. FINITE_CHECK_PASS at1e-10, max residual1.333e-15, CPU0.355s,
runnerwall0.618s. These are float checks, not interval proofs or device data.
Source audit identifies known moment/Cauchy–Binet/norm ingredients and leaves
complete adaptive-application novelty OPEN. KEEP the scoped mathematical
obstruction; positive unrestricted optimization target OPEN. Paper/P33/P37/E05b
unchanged, zero QPU calls. Resume from research/ACTIVE_DISCOVERY_STATE.md.

## 2026-11-25 — P45–P49 preserved, P50 changed decoder prospective

Research continuation source8f83f2b on research/p45-positive-discovery preserves
P33/P37/E05b and P44; the user's target is a POSITIVE optimizer result, not
completion by obstruction. P45 full-Fock and cavity completions, P46 hollow
transfer/PIT, P47 directed graph polar map and P48 spectral source all fail
their declared DEV control gates. Full source/raw/manifests and scope are linked
from research/P45_LIVE_STATE.md; no rejected grid is silently discarded.

P49 QUESTION: can coherent spectral-source mixing, trained on ALL feasible
cuts instead of a proxy, reveal a useful fresh gain? Root7b791bf/dc85fa5;
pre-run source3d6a1f2 after independent setup-cost correction;42PASS preflight.
One clean32615d1 main completed24.299721s,1792 draws, four new N26/34 DEV graphs,
no optimum/optimal masks/postselection, all collisions decoded. Training and
fresh evaluation are separated. B paid best173/54/365/72 loses to independently
qualified FAST158/49/359/63 on all four; sphere fresh mean is also better than
B. A B>D mean contrast survives but is insufficient. DECISION: REJECT this
hybrid/budget. d61b8c6 limits the CPU veto to the shared-frontend pipeline;
removing optional overhead would also remove the gifted Cref initialization.
No retrospective cost change strengthens or rescues the result. Data9074386,
result7f5536e; root integration d66c46a. Raw SHA256
f890601b3237e329df883fddee8f8ca4a81ec9055d2539332ecfc11a736b6f26.
Read-only consistency audit184326 cuts/14207 classical checkpoints is not
independent distribution replication. Root677PASS, four current manifests
validate,602 historical files/PDF unchanged. reports/P49_validation/.

P50 ROOT card f9689d2 fixes a new all-count graph diffusion/topK decoder,
four fresh N50/100 DEV graphs with13/17 photons, nine separately tuned models,
B-only classical accounting and strong from-raw-graph descent-FIRST controls.
No graph/data opened; implementation/review only at this checkpoint. A distinct
ideal cost-phase/Johnson route yields a favorable sign but an exact weak-order
classical control, not a validated photonic optimizer. All positive/novelty,
held-out/independent replication and hardware gates remain OPEN/CLOSED as
appropriate; no manuscript change, QPU call or Laurent message.

## 2026-11-25 — P50 minimal-cost decoder also rejected

Root card f9689d2 with PRE-DATA addenda fixes new sparse ER/RR N50/100 graphs,
13/17photons,10 separately trained models and from-raw descent-FIRST controls.
New independent B-marginal arm addresses a discrete-marginal confound BEFORE
outcomes; its preparation never enters B's cost. No Cref, PIT, greedy decoder,
optimum or postselection. Code0fbe635, independent physics2e83846/callerd6ce9fc,
FAST21PASS19044e1, primary74PASS5310257; DOCONLY dense-H correction precedes run.
ONE main clean5310257 completed21.615873s, all2560draws,19 unchanged inputs,
14 regular results,18,687,071bytes, CPU60/wall90/thread1, no retry/exclusions.
Datafb5a36e preserved before audit. B fresh mean.407747668 loses to static
preparation.362821548; this mean comparison does not imply every static minimum
beats B. EACH raw classical mode beats paid B203/217/353/403 on all four graphs:
random138/181/254/297, spectral138/175/244/280, under B-only measured grants.
No free Cref/features, only online completed deadline-admissible snapshots;
trace export/total overrun explicit. DECISION: REJECT this lean pipeline/budget,
not all passive sources/decoders. Root751PASS and preservation602/PDF PASS.
Post-hoc independent-code consistency audit is in preparation, not blind or
physical replication. RawSHA256c19f8cc9f890ece810dad0549c0ca8b3d7785ed6a41f210ef51d10b4f54dc77b.

Separate exact analysis: no-leakage passive whole-CF evolution is monomial
(root336a9f8, independent8ac8754); continuous nonconstant balanced cut oracle
cannot use that shortcut, with isolated-pi and dualrail/conditional exceptions.
H4 fourth-order rank response (b710d21) survives fixed low moments, but decoded
law has an exact O(1) classical mixture (4c5b071), and b4 is exact. No positive
goal achieved. P51 invariant/loss extension is analytical only and unresolved;
no graph/experiment opened. Paper/P33/P37/E05b unchanged; QPU gate CLOSED.

## 2026-11-25 — P52 collective phase is real but its tested means are replaced

Prospective6df6e1c/bec2097/0b79400, independently reviewed source67db4a1 with
conservative solved-status correctiond7f8e2f, qualification45PASS2e57ccd.
ONE main on clean2e57ccd completed2.107155runnerwall/1.287146CPU,
11 unchanged inputs and12 regular results/2,393,180 bytes. All4 complete
6435-occupation laws, all35 b4 regroupings/cell,1,048,576 classical phase draws
and8 LP calls completed. No graph, known optimum, training or postselection.
Full low moments through3 are invariant, but both the fourth-order witness
and the28 cut-edge means change with phase. All4 mean kernels have verified
numerical convex replacements using endpoint b4 kernels plus uniform70;
max residual1.56e-15, all actual optional MC weights0. KEEP physical phase
response; REJECT this finite mean mechanism as an optimization positive.
No full-law/tail/continuous-theta or runtime-dominance theorem is inferred.
Original data762877a/root8934725, report8845ae6/roote08a218.
Root796PASS at a78f91a,602 historical files/PDF unchanged.

Independent Perceval Naive validation has preserved administrative failures
001/002, then actual API qualification003 (7 guards/11 checks PASS, native
limit unverified). Read-only official Config metadata enabled a documented
native maximum1 with before/after readbacks; qualification004 now passes
8 guards/11 checks (max error2.01e-16). The full25740 comparison remains a
separately gated run, not assumed from these small checks.

P51 flat-unitary/loss proofs have ROOT's separate same-team reconstruction;
bounded primary-source comparison leaves novelty OPEN. P53 is a new exact
continuous-phase replacement question, card87abe69/APIef476a4, sourcea8f93a0,
support-only adversarial test deltae8fe48d. Three static reviews precede18
targeted tests and any main construction. Exact rational proof data, not a
small floating residual, will be required. No actual certificate exists yet.
Positive optimizer, held-out confirmation and QPU gates remain unfulfilled;
paper/P33/P37/E05b unchanged. Continue new falsifiable research routes.

## 2026-11-25 — independent P52 probabilities pass; P53 remains inconclusive

Full Perceval Naive run on clean d7f49f5 completed2.872489s/1.841588CPU,
11 unchanged inputs, all25740 complex amplitudes, no collision/zero filtering,
renormalization or phase alignment. All4 cells pass; max amplitude difference
9.8121e-17, max probability9.5410e-18. Data3cde959/root3e348a1 and
research/P52_NAIVE_COMPLETE_REPLICATION_REVIEW.md supersede the prior PENDING
state. This independent-engine/matrix-enumeration check knew P52's reported
sign and is not blind, external, held-out or optimizer replication.

P53 qualification18PASS e6283dc preceded ONE bounded main:1.746802runnerwall,
0.975028CPU,12 unchanged inputs, all4 exact source/library/attempt/summary
outputs retained. All20 LPs solved status0, but only extreme Bernstein
controls exactified. INCONCLUSIVE_BERNSTEIN_OR_SUPPORT: no continuous convex
identity, no proof of curve nonmembership, no positive inferred. Preserve
data bce6e2d/root111be95, including every failed support. New questions require
separate mathematical design, not an automatic favorable rescan.

Root full822PASS24.89s, official native maximum1, four newly integrated
manifests v2PASS;602 historical files and every paper byte unchanged.
reports/P53_validation/ records exact commands and checks. P54 ROOT proof
4d6826d falsifies the LEADING weak full-input sqrt(weight) graph-hopping
mechanism: topK favors crossing weighted edges and increases expected cut,
with a cheap classical mixture at that order. Separate reconstruction pending;
not a general no-go, finite-angle result or completion of the positive target.

P54 proof status update: physics froze43b35f9 before reading ROOT's proof,
then focused exact-hash review91fb868 confirms PROVED_AS_WRITTEN. ROOT also
rechecks the separate general-covariance N4 counterexample by hand. This
supports the explicitly scoped local theorem only; novelty and a useful
finite-strength mechanism remain OPEN. No executable experiment or paper edit.
P53b now prospectively fixes x=1/4 and two bounded LP proposals with exact
point certificates (carda0a6881/1dbb3f9), implementation only; no value opened.
P55 neutral-count decoder is a distinct analytical proposal, not an experiment
or an accepted gain. Github research checkpointa9a5897 CI succeeded in run
45609474034; remote main remains2744395. Continue beyond these negatives.

## 2026-11-25 — exact P53b counterexample; P55 decoder is operational

P53b's sole predeclared x1/4 was not another favorable scan. Sourcebb0ba2d,
ROOT/physicsbb1539a static reviews and20 syntheticPASSfa3eb9a preceded one
2.072363s main,13 unchanged inputs, exactly two solved LP proposals. Data
a2cf5d9 stores an exact dual (X04-X15)/2: all71 ENDPOINT controls have mean0,
B has -767/327680. Nonnegative posthoc graph gives normalizedgap767/4587520.
Independent stdlib checker018641eb/PASScc4c73b reconstructs the target with
direct powers, checks all71/28 coordinates and graph/gates exactly. ROOT reads
actual results and validates both manifests. This rejects the ENDPOINT71
continuous replacement hypothesis; P53's earlier failed Bernstein search
alone did not. Same-team/posthoc independence, no source rederivation or
held-out optimizer replication. theory/P53b_endpoint_mean_counterexample.md.

P53c next falsifier is frozen28e0fc5: all35 SAME-phase b4 controls at pi/3,
retaining the original71 and fixed graph diagnostic. Exact Eisenstein ring,
4-photon Fock probabilities and4+4 convolution;106-control membership/dual
still unevaluated. Implementation only authorized, no silent old-library
scope extension or paper update.

P55 is a new all-attempt neutral photon-count decoder, not another ranked
decoder. Carde22d563 and independent72c9bb99 derive uniform DP sampling and
the favorable but classically reproduced leading drift.96-line prototype
4812e881, one qualification3f8ed4ad:29PASS, all1000 N2/4/6 count vectors and
all ranks, plus bigint/loss/vacuum/odd/resource cases,6 unchanged inputs.
No physical graph pilot followed. A bounded finite-coherence N20 proposal
is being designed with independently retuned D/inclusion/b4/phase/marginals
and paid strong classical controls. The broad positive target remains OPEN.

## 2026-11-25 — completed P55 finite pilot and independent checks

The finite P55 proposal subsequently passed45 actual synthetic qualifications,
including596 unique role seeds, exact mixed PGFs, retained direct-time CTMC
failures and the paid immutable-factory prefix correction. Its ONE main,
clean45d115a6, completed480 draws/96batches/18unchanged inputs in33.331807s.
All attempts decode; no C*, known partition, opt mask or held-out graph is used.
B paid39/38 loses to EACH separately costed fixed FAST11/22. Independently
selected D and inclusion have lower fresh equal-graph means. Preserve the
negative and finite-grid/zero-optical-latency-envelope limits; no broader
impossibility is inferred. Primary8049fa37/root716d3af, report8ac10da/root2afccde.

The independently prepared sparse-GF/inverse-rank checker c89e674 was fully
read by ROOT before its exclusive run. It imports no production sampler,
replays only fixed graph/group/rank recipes, and checks all480 events, all
Fraction selections/paid incumbents/B-only clocks/FAST eligible snapshots.
All11guards PASS; the verdict DEV_REJECTED_FIXED_FAST agrees. Unique audit
4352d25/rootd824232, runner0.460269s,12unchanged inputs, validated v2 manifest.
This is recorded-data independence, not new optical sampling or hidden-timing
proof. research/P55_INDEPENDENT_RAW_AUDIT_RECEIPT.md gives actual provenance.

P53c's complete separate direct-permanent engine now independently verifies
all70 group laws/35 convolutions and the strict fixed106-control witness:
aa7d6f3/rootb9a9612. P53d extends the SAME B/w/graph to all real b4 phases in
one exact primary candidate312a22d/root006ce2f: all35 triangle certificates
strict, signed bound57/32768, normalized graph57/458752. Independent exact
coefficient reconstruction is still pending; no optimizer claim is inferred.

Root full956PASS24.09s pytest, six new manifests v2PASS,602 historical files
and paper bytes unchanged. Receipts reports/P55_validation/. P56/P57 continue
with different encodings/multi-swap mechanisms, first checking symmetry and
classical replacements. Main/paper remain unchanged; no QPU/held-out opening.

## 2026-11-25 — continuous control theorem; broader fixed-phase replication

P53d's independent checker passed13 prospective guards, then its separately
authorized replay7611d76/root967bb07 reconstructed23,100 permanent patterns,
300300 Laurent entries,6435 direct decoder states,108900 matrix entries,
35 spectra/triangles and105 anchors. It confirms the SAME fixed B/w/graph's
strict57/32768 mean gap over all35 b4 groupings at EVERY real control phase;
old normalized graph bound57/458752. Exact scoped statement is extracted in
theory/P53d_uniform_phase_b4_mean_separation.md. No optimizer claim is inferred.

P58 separately froze the SAME-angle ALL127 bipartition falsifier before code
or evaluation. Its source/card/contract had ROOT/physics full static review.
One clean isolated runcc58f9a/root89e882d,2.012950s,7 guards,5unchanged inputs,
all255 exact source laws/157183 states and6435 tie scalars retained. All127
1+7/2+6/3+5/4+4 controls have larger signed mean; minimum gap649/327680 at
groups03/12/47/56. All raw data sealed before the receipt. No new graph/angle.

Independent engine code db573dd/rootb6388c6 passed actual6+5 qualification
66d5dcf/root49ca757 before ONE authorized full native check. Rawa3ce1dc/
root7743372 sealed before analysisa4bfa3e/rootdb5f717: all157183 Naive permanent
amplitudes agree (max1.873501354e-16), all6435 threshold-hypergeometric ties
and127 base16 convolutions agree exactly. ChildCPU6.689109s/wall7.37463125s,
runner7.702003s;11 unchanged inputs/v2PASS. Numerical source corroboration,
posthoc/nonblind team, not exact interval source proof or physical randomness.
Finer partitions/all phases remain outside this assertion. No advantage.

P56 Diță C5 symmetry proves a38-dimensional mean projection, orbit bound,
and a nonnegative graph counterexample. An antiunitary identity excludes its
proposed N8 within-color U2 escape. P57's5-source collective cycle really
responds, but an explicit O(L) parity sampler reproduces its FULL law; the
graph example also loses to retimed D/direct permutation. ROOT caught and
preserved separate MPS-phase indexing and reviewer gain-arithmetic errors.
Final gain is(15-5cosPhi)/512; these corrections do not change its rejection.

P59 now fixes a DIFFERENT odd N6 family, one real output mixer, one phase,
q/marginals/moments<=3 invariant. Before code, the separate adaptive derivation
and ROOT reconstruct a nonzero individual-PNR derivative -124sqrt3/421875.
That is not a decoded-mean result: all15 responses require the full462-state
aggregation and all20 ties. Cards/derivations9f5b7ea+b7341f9/59dc56e precede
implementation; no graph, opt mask, calibration or sample has run yet.

Root969PASS25.46s atba0e066 and manifest/archive/paper checks are recorded in
reports/P58_validation/. No paper/main/Git release change or hardware call.

## 2026-11-25 — battery recovery: P59 replicated, P62 accepted, P63 pending

P59's predeclared six-mode response is now independently reconstructed in
exact arithmetic:2928 checks, zero disagreements;12/15 edge slopes nonzero,
all42 complete marginal bins and83 joint moments through degree3 unchanged.
Primary ea2e6a9/rootcf1f30d; separate quadratic/hypergeometric replay3972641/
rooteb203aa. Both raw runs were sealed before interpretation. This verifies
a physical decoded response, not an optimization or classical-cost advantage.
The extracted statement and its conditional optimum-blind descent rule are
theory/P59_exact_decoded_response_checkpoint.md. The small finite law has
the explicit P60 phase-average/rejection replacement, with costs unpaid until
an actual implementation is measured. Full998PASS and four current v2
manifests/archive/paper checks are retained in reports/P59_validation/.

ACCEPT P62 at the exact reviewed proof SHA after before-reading independent
reconstructionf301920 and focused audite312909. Mapping-averaged best-of-T
dominance uses up to2^s paid classical candidates, not equal wall time or a
selected fixed mapping. Scalar P61 has s3 and is analytically vetoed in that
scope; its optimizer pilot was not run. The bounded three-primary-source
literature check retains novelty OPEN and attributes elementary ingredients.

P63 changes the premise to ten phase controls acting on15 of18 outputs.
Static physics reviewb4bceeb/root6c9ab0d confirms the fixed-q/moment claims,
species control and the need for SAME perturbation direction on paired SPSA
signs. Stage1 implementation is being prepared before any DEV graph/draw:
80 B attempts total, four independent from-scratch FAST calls, prospectively
limited to10000 proposals each. A fixed FAST mode winning both eligible
prefixes vetoes the route; missing eligibility is inconclusive, never positive.

P64 supplies a different complete fixed-phase classical sampler: sample the
joint conserved color totals, restore every compatible coherent source term,
then condition sequentially through six tritters. The exact source support
is at most80, and compatible width at most6400, not an exponential full-PNR
table. ROOT read the complete derivation and checked its coherent suffix
trace and counting bounds. This ideal-arithmetic construction is not a measured
runtime/precision certificate, a growing-size efficiency theorem or novelty.

The battery interruption lost no sealed result. Continue research from these
artifacts; the positive optimizer objective remains OPEN. Original main,
paper/ and602 protected historical scientific files remain preserved. No
held-out graph, hardware circuit freeze, Laurent message or QPU call.

## 2026-11-25 — P63 actually executed; fixed classical gate rejects it

The frozen code8b20dca passed46 synthetic guards and separate adverse static
review83996a9. ONE main on cleanfad8a05,19.495067s runner, completed80B and
four independent FAST calls; raw sealedbf2034d before interpretation. B's
all40-attempt/case best81/60 loses to EACH fixed random/spectral FAST54/42.
All four online eligible prefixes are timely, with no early guard. Per-case
B-only classical wall grants4.941689/2.982009ms excluded all simulator,
import, diagnostics and evidence IO work; this is a favorable zero-optical-
latency envelope, not hardware timing. All collisions retained, no C*/optimum.
All six optional models are NOT_RUN_DUE_FAST_VETO, and no wider sweep or
held-out rescue was performed. Primary interpretation is in
research/P63_STAGE1_MAIN_RECEIPT.md; independently authored raw audit pending.
The complete existing P63 regression passed1044 in25.26s pytest.

P64's static independent reviewc59baf9 found a concrete small-law/CDF
normalization coverage gap. It was corrected prospectively677348b BEFORE
the first qualification; all old versions remain. ONE corrected qualification
22PASS/.54s pytest/.793044s runner,8 unchanged inputs, exact462-row source
table and4*462 candidate/reference probabilities sealed4ee15ab first. Source
support68 strengthens the finite compatible-width bound to4624; the complete
ideal law construction and rounded finite implementation remain distinct.
Maximum N6 probability error1.2143e-16, no N18 random draw, no certified
global N18 TV or throughput. Existing P64 regression1020PASS; ROOT is checking
the combined integration. research/P64_QUALIFICATION_RECEIPT.md has scope.

A separately frozen N18 point/permanent cross-check is being designed, while
P65 examines genuinely changed mechanisms and their adverse controls. No
arbitrary algorithmic success is inferred from the source support or test
count. Positive optimizer OPEN, paper/main preserved, hardware gate closed.

## 2026-11-25 — independent audit, N18 cross-check, new P65 dynamics

P63 checkerce69e3c froze without reading the outputs, passed8 fixtures, then
bound the13 sealed files without code changes. ONE audit5624ff6/root43f33ef
completes7183 checks, zero discrepancy, all80 counts/14matrices/6updates/
365FAST checkpoints. Both fixed-mode vetoes are independently reconstructed.
Limits: recorded consistency only, no new physical counts, likelihood or
authentic clock measurement; topology/edge assignment not regenerated.
Existing1052PASS. research/P63_INDEPENDENT_RAW_AUDIT_RECEIPT.md.

P64 separate F6 paired-quadratic engine agrees on all462 signed coefficients
and weights. After22 small guards, ONE clean N18 runbbd86a3 sealed6c51113
checks14 fixed points against Naive: maxabs5.468657e-20. ALL14 tolerances are
absolute-dominated; CF exact0/native1e-35 residuals yieldmaxrelative1. No
global TV, N18 sampling, optimizer or throughput claim. Existing1042PASS.
research/P64_NAIVE18_POINT_RECEIPT.md preserves every point and limitation.

P65 changes to global Cayley--Metropolis proposals from the current subset,
all collisions as paid self-loops. Its analytical barrier fixture already
loses to an obvious classical two-swap. Section4's uniform-collision-average
monomial theorem43dd873 has independent focused proof audit1cc5dfc; ROOT
accepts only that exact scope, with novelty OPEN and no equal-cost assertion.
reports/P65_UNIFORM_COLLISION_PROOF_CHECKPOINT.md gives acceptance/limits.

P65 N20/K10 B80/FAST card022962e is fixed BEFORE data; code is being prepared.
Independent card review clarifies repeated random subsets are retained and
degrees mean weighted row sums. No P65 graph/start/kernel/canary/count has
been evaluated. Positive optimizer OPEN; paper/main and602 old files preserved.


Integration checkpoint:1096PASS/40.84s pytest after both new independent
checkers, seven current v2 manifests validate and602 protected historical
files/paper bytes are unchanged. reports/P63_P65_combined_validation/ retains
observed commands and checks; P65 code/qualification/main are still pending.

## 2026-11-25 — P65 negative independently audited; P66 static route

P65 source da4d418 passed39 prospective qualification tests, then ONE B80
main at clean74ad849 sealeda1a62cc before interpretation. All80 attempts,
46CF/34collisions and800 modeled photons retained; B all-paid82/79 loses to
EACH fixed random/spectral FAST50/45 in eligible own-cost prefixes. All8
training fitnesses tie on each case; selected(t1/4,lambda0) is the frozen
first-tie choice. Fresh local gains do not improve the paid global incumbent.
No unchanged retuning or optional-control execution followed the veto.

Independent checker0d7224f froze before author raw access; ROOT read all707
lines/9 fixtures/contracts before qualification.9PASS, immutable13-artifact
binding, one audit397e241:9251 checks/80counts/16matrices/398costcomponents/
414FAST snapshots, zero discrepancies. Recorded evidence consistency only,
not physical replication or true-clock certification. Receipts:
research/P65_STAGE1_MAIN_RECEIPT.md and P65_INDEPENDENT_RAW_AUDIT_RECEIPT.md.
Worker1092PASS; combined ROOT1144PASS/42.50s pytest/43.685357125s total.
Four new v2 manifests validate at root;602 protected files/paper unchanged.
reports/P65_integration_validation/ preserves observed commands and hashes.

P66 changes to analytical falsification of a collective-move mechanism:
bright/dark occupation conservation on a four-clique shared-warmstart family,
including a connected weighted extension. Separate author/peer derivations
are being frozen; ROOT has not accepted an exact-hash final proof yet.
No numerical P66 run has occurred. A degree-based chiral extension has an
immediate static falsifier on these regular graphs, not a failed simulation.
The stronger positive target CLAIM-042 remains OPEN; paper/main stay frozen,
held-out graphs unopened, no QPU call or hardware freeze.

## 2026-11-25 — independently audited transport obstructions and new mechanism

P66 author2bcf84b and independent before-reading proofeae1dda agree on
the raw bright/dark barrier, including connected weighted graphs. A later
exact-hash review7f0096c2 verifies all392authorlines. P67 also rejects the
weak degree-flux route analytically: regular-family phase degeneration,
odd-t cancellation and retimed-D/classical leading-pair controls. No pilot.

P68 extends to joint graph/current covariance with rank-two bright spaces.
Independent review0c7fa52 and separate source clarification/addendum30361da
verify currentSHA8a4bd9cf. The L2 probability bound is vacuous. Random marked
histories and covariance only in law remain excluded from this statement.

P69 changes the invariant itself: INPUT and OUTPUT dark projectors differ
and intertwine. Gaussian permanent/moment and PGF estimates yield a raw
full-block transfer bound for ANY unitary of bounded optical cross rank,
even arbitrarily marked/history-dependent ones. Independent428-line proof
e5477a74 froze BEFORE author access;315-line exact review1e2e69d7 verifies
currentSHA37e59633. The growing-rank and Cayley composition consequences
are proved, with a symbolic counterexample to the generic exp(itH) shortcut.
No numerical source or external theorem leaf is needed for these proofs.

P70 is a different explicit bright-mode transfer proposal, frozen55b208d:
candidate bosonic event enhancement versus all rank-one D, with immediate
classical and higher-rank D falsifiers. Independent rederivation is pending.
No positive optimizer acceptance or novelty follows. Boundaries/source hashes
and audits: reports/P66_ROOT_PROOF_CHECKPOINT.md, P68_ROOT_PROOF_CHECKPOINT.md,
P69_ROOT_PROOF_CHECKPOINT.md. Bounded primary-source comparisonP66 is adjacent
only; a separate P69/P70 attribution check is in progress.

P66 finite diagnostic88a0573 passed nine prospective tiny tests, including
five local HOM amplitude points. Rawdcb3aba sealed first;9PASS/27.86s pytest/
28.553662s runner,10 unchanged inputs, manifestv2valid, all observations
in JUnit despite its retained compatibility warning. The main remains
unexecuted until independent source review. No new graph optimizer, random
count, held-out or QPU call occurred; manuscript/main remain frozen.

## 2026-11-25 — P66 complete finite validation and 1153-test tree

Independent full-source reviewSHA440afb11 finds no material blocker at
source88a0573; it opened no outputs. Qualification9PASS and actual JUnit
size527874bytes/logs1768bytes verified, then review/pre-main receipt sealed
a5ea2b9. ONE main at that cleancommit sealed rawdaf728d before interpretation:
PASS_FINITE_ASSERTION,4902assertions,32matrices,256B+256Dpoints,128unions,
all1988cuts,7PGFpairs and32frozenNaiveBpoints. Runner33.850853s/bodyCPU8.987306s,
10unchangedinputs/3results/v2PASS, withinoriginalCPU60/wall90/thread1 caps.
No retry, sample, optimizer or hardware call.112exactzeros per model retained.
Native maxabs2.439454888092385e-19/maxrelativeobserved7.09e-15;16relative-
dominated and16absolute-dominated mixed tests, not a global/interval claim.

Full existing1153PASS/43.15s pytest/44.247098458s total atdaf728d. ROOT's
entire trackedPython/pinnedpackage tree is identical after integration;
test globs touch no changed proof/report paths, so no redundant full rerun.
Both new manifests validate atroot,602oldfiles/paper unchanged. Exact
receipt and checks: research/P66_EXACT_FINITE_RECEIPT.md and
reports/P66_integration_validation/. This verifies finite conventions;
universal P66/P68/P69 claims remain proof-based and positive goalOPEN.

P71 approximate-rank proofSHAc320f925 is frozen pending fresh audit. P72
follows the genuinely changed exp(itH) route past P69's exact-rank
counterexample, by bounding effective cross rank at finite normalized time.
No numerical P71/P72 calculation has started. P70's restricted bosonic
mechanism has a separate before-reading derivation17c3f5c; exact author
comparison is underway. Its strong classical and higher-rank D vetoes
remain decisive regardless of the restricted event separation.

## 2026-11-25 — Linux regression fixed; P70–P73 independently reconciled

The P66 portability failure is preserved: GitHub45707404987 gave1152PASS/
1FAIL at a Mac absolute-path guard before native HOM physics. Minimal fix
b272df1 keeps the experiment CLI contract strict and makes the native unit
loader portable. The unchanged frozen HOM fixture and two new infrastructure
regressions run the real native backend. Local1155PASS/42.24s pytest;
GitHub3ed8441/run45709046742 is GREEN,1155PASS/16.09s plus archive and
publication/manuscript checks. Historical P66 v1 data/source88a0573 remain
untouched and validate against worker4925feb. Source v2fb3cf959 is not claimed
to have produced that grid. ReviewSHAa0d802e8 and validation reports preserve
the failed and successful checks, including Linux module-file-hash limits.

ROOT has now read all author/independent/exact-review artifacts for P70,
P71, P72 and P73. The four checkpoint reports link exact hashes and scopes.
P70 is a real rank-one B>D event separation with a decisive classical
whole-clique countercontrol, so not the requested optimizer win. P71 makes
the rank obstruction stable to a bounded singular tail. P72 controls the
tail of low-cross-rank static Hamiltonian evolution at finite normalized
time. P73 changes to active complementary Gaussian sources: a favorable
weak conditional cut tilt is classically reproduced, the next coherence
term is cheap matching variance, and raw background/source costs are paid.
No universal Gaussian no-go, matched total-cost win or novel priority follows.

P74's nonlinear heralded-cost route and P75's Gaussian CF probability cap
are separate static/code-preparation questions. The P75 four-mode cap is
analytically resolved before any planned search: no numerical data exist
for that canceled scope. A prospective six-mode falsifier is CODE ONLY,
pending exact source/contract review; no main authorization. No numerical
worker is active at this checkpoint. P76 investigates a weak-filter route
and its classical replacement as a distinct static continuation.

All old negative results, including E05b and P65, remain evidence. The
positive optimum-blind optimizer/held-out/independent physical-replication
objective remains OPEN. No paper/main revision or hardware/QPU call occurred.

P74 later reconciliation: source379lines/SHA0b4b4bbc copied byte-identically
0b3c1f8; independent330line proof3a3016c and exact276line review2a3b4f6
integrated48ea005/8e330e5. ROOT read all985 lines. The conditional raw-count
screen is accepted, including protected deferred flags and a concrete
postselection failure-reentry counterexample (two-block p1, not1/81).
One primary Knill profile and six local source hashes support the static
2/27 instrument statement; no numerical gate or hardware experiment ran.
reports/P74_ROOT_RESOURCE_CHECKPOINT.md records exact limits and OPEN weak-
phase/recovery/joint-block escapes. No equal-clock or all-QAOA result follows.

## 2026-11-25 — finite P75b no-hit, source regression and weak-filter obstruction

P75b source5b2b52d/SHAb86f2c69 had full ROOT/independent243line source
review before any execution. One nine-item tiny qualification rawaa16e2d
passed, then separate authorization allowed ONE main atclean00256fc2.
Raw4a5254c sealed first;1033 evaluations/6terminations, no trigger/certificate,
global best only the analytic three-pair baseline. Three seeds returned
ZERO optimizer iterations under the raw-probability absolute gtol. The
remaining three exhausted300 calls. This is a materially weak no-hit,
not strong numerical support for a universal Gaussian cap. No B rerun,
posthoc seed selection, precision change or suppressed failure occurred.
Root recorded-row audit validates counts/fields/inputs without recomputing
probabilities. Main runner1.227817s/bodyCPU0.79351s/3277339scientificbytes;
both v2 records validate in the matching producer and integrated root.

Integrated root0672098 passes1164 tests/42.91s pytest/44.308535667total,
environment/nativecfg1.602 protected files unchanged, paper bytes match
main2744395, PDF remains271946c9. reports/P75b_integration_validation/ and
P75b_ROOT_FINITE_CHECKPOINT.md preserve actual checks and limitations.
A separate P75c logarithmic-loss source is prospectively being prepared
to address the observed scale failure with fresh seeds; no qualification
or main is authorized by this checkpoint.

P76 changes to weak nonlinear projected filters. Source357lines/bd1d73a6
and before-author independent301line proof/f1242c16 were fully read by ROOT;
247line exact review29f71877 agrees. The independent original index failed
mapping and was preserved; its exact bytes were centrally frozen75e579f
BEFORE author access, with no invented original commit. Final reviewa44f8b7.
The vacuum-flag physical shortcut fails, and the abstract protected diagonal
model has a classical latent record construction. Uniform feasible draws
also dominate raw proposal counts from the stipulated uniform source.
Actual total costs/nonmonomial mixing/changed sources remain OPEN.

P77 is a new static finite-strength positive-hafnian control and range
certificate, frozen851a0cc while independent reconstruction is underway.
It does not assume the global P75 cap. No P76/P77 numerical experiment,
held-out opening, paper/main revision or QPU call occurred. The original
positive optimum-blind optimizer objective remains OPEN.

## 2026-11-26 — audited full-PNR loop construction and preserved P75c no-hit

P75c source51deeed/ea9f8c6a had765line ROOT review and independent199line
reviewe490d226 before one tiny11PASS qualification, rawf343302. Separately
authorized ONE main atclean f02e471, rawf082dd60 sealed BEFORE interpretation,
receipt85da02a.7145 evaluations=baseline1+1144+five1200; no trigger/exact
certificate, best only analytic1/64. One normal return has24 iterations;
other budgets are not convergence. All43 zero/floor float rows retained.
ROOT reconciled every recorded row and exact cached final point1102 without
new physical probability/RNG computation. Both v2 manifests validate in
producer and integrated ROOT; all12 inputs fixed. Main runner2.99137s,
CPU2.529067s,22693852 scientific bytes; no retry or further P75 search.

Root716d8a2 passes1175 tests/43.21s pytest/44.221019500s total, nativecfg1/
env1.602 protected files unchanged; paper bytes still match main2744395,
PDF271946c9. reports/P75c_integration_validation/ retains observed checks.
Previous GitHubee5850a/run45715830953 is GREEN/1164PASS14.22s; newer1175
source is locally checked, remote validation remains a subsequent observation.

P75's sharp small-case Gaussian bounds have an independent232line exact
auditc532655; general6 remains open. P77 current clarificationf6470ae/
SHA2a05e676 is accepted with original independent199line f0abf682,
exact111line d12c432 and separate34line addendum8cd425c. Its exact
four-matching control and finite-strength/range screen count all rejections.

P78 now proves an exact full raw PNR loop construction for nonnegative real
pair matrices, including collisions, vacuum and all number sectors, in an
explicit IDEAL real-arithmetic sampling model. Author183lines/118c8827,
before-author independent360lines05b10613/e00cf6fd and exact227line
reviewefd402ab/86ae24e2 were read by ROOT. Proposed transitions<=m*nbar;
Perron/precision/setup/random bits and actual clocks remain separate costs.
Three-primary-source check8798379 authenticates established Le Jan loop
ingredients and an explicit doubled-kernel translation; no novelty claim.
reports/P78_ROOT_SAMPLER_CHECKPOINT.md records exact limits and attribution.

P79 is CODE ONLY finite validation with exact bunched coefficients,
Perceval passive-sector amplitudes and declared raw count simulations;
no P79 qualification or main yet. P80 studies rational setup without a
Perron oracle and controlled finite-bit error; neither extension is accepted
from a proposal. Numeric slot FREE after the root regression, subject to
later explicit reservation. The positive optimum-blind optimizer target,
held-out/independent positive replication, manuscript and hardware gates
remain OPEN/CLOSED as before. No QPU call or paper/main mutation occurred.

## P79/P80/P81 audited continuation after battery interruption

P79 sole main1286ecf/rawb8e8fea passes its registered finite population:
266 exact coefficients,650 passive native amplitudes/105 points,120000
raw draws,272 bins. Independent ROOT streaming consistency checks cover
all121312 rows and1781 module hashes, not a second physical replication.
Qualification and main manifests v2 valid at matching ROOT/producer.
Receiptc2a22ed and reports/P79_ROOT_FINITE_CHECKPOINT.md preserve zeros,
collisions/tails/rejections/warnings/caps and the absence of global-TV claims.

P80 rational-resolvent/killed-loop source2c9810 and finite-bit bridge57b3ecc
are accepted after full ROOT/257+246-line exact audits. P78 and the rational
bound S<=m²*nbar discharge the bridge's explicit A/B dependencies. Finite-bit
flagged approximation is proved mathematically, not implemented by P79.
P81 before-other-author sources0a51544/13ce814 and exact reviewf915cf9
establish full-balanced-average dual-rail leakage stability and its exact
rigidity/N2 exception. Scope/quantifiers/cost and novelty limitations are
retained in their ROOT checkpoints. No positive optimization result follows.

Integrated code c360b36:1187PASS43.89s pytest/44.879216292s wrapper,
env+native1.602 old files and all manuscript bytes unchanged. Prior GitHub
6346647 GREEN1175PASS12.12s observed from actual job log. Positive target
OPEN, paper/main/QPU frozen. P82 now designs a genuinely changed physical
mechanism; P83 studies where positive-loop simulation stops. Both STATIC,
no new numerical experiment authorized and no favorable rerun of old data.

## P83 phase boundary and remote P79 verification

Accepted source d1749a1/ec6a88bc and exact review48939d6/3313e1a8 after
ROOT full338+294-line reconstruction. Gauge-congruence leaves complete
counts invariant; all-even-WALK support criterion includes odd-cycle
compatibility/loops. SignedC4 has log coefficient1111=-2t4 and no positive
compound-Poisson representation, not arbitrary classical hardness or an
optimization advantage. No numerical P83/P82 job ran. GitHub9572bc6 is
observed GREEN1187PASS18.53s/602 archived files from actual job logs.
P82 static design remains active; P84 cost-phase obstruction is under
independent reconstruction. Paper/main/QPU and positive-result gate unchanged.

## P84/P85/P86 and prospective P82a

P84 exactsourcea47e275/cdb0892f, independent5706815/e2098c99 and exact
review2b015e6/de627da7 accepted after ROOT full303+275+259-line audit.
P86 ROOTdaf49c6/a8074fd2, independent36ff604/cf156f61 and exactreview
93139b4/88b3df74 accepted after171+256+299-line read. These obstruct a
specified all-balanced-basis passive cost-phase oracle, not every graph
optimizer. P87 sharper first-order candidate is frozen but pending audit.

P85 two-primary check2c45237/02150f2d identifies direct2020 raw nonnegative
GBS overlap; no first broad dequantization claim. ROOT separately checked
its physical thermal cofactor counterexample and actual primary PDF sign
step, while pure nonnegative marginal closure survives by Schur identity.
P78/P80 exact internal proofs and priority limitations are preserved.

P82's145-line physical designf7cb5d9/c008f601 is frozen. Uniform-loading
r2 mean cancels; nonuniform−q0E phase term survives but has a polynomial
classical control. Higher-order basin improvement is OPEN. A separately
frozen K8/n16 card and independent audit must precede any code or canary.
Numerical slot FREE, no new simulation/main, paper/main/QPU untouched.

## P87 sharp obstruction accepted; P82a pre-data clock defects corrected

P87 ROOT6436860/f4934640, independently frozen17ba1d4/c23638c0 and exact
reviewb77c8c0/22cfcb7f accepted after ROOT full168+308+344-line audit.
The optimized passive all-balanced coherent phase error at fixedN has
limitR/2, the same as identity. Scope/cost/observability/novelty limits
are retained; it is not a general optimizer no-go.

P82 exact eta0 null source153e807/bc5943fa and designaudit ae900ed/59b478c0
have full ROOT reads. Complete decoded law becomes flatD afterindependent
portmarks; counts/costs neednotmatch. AnalyticJ/H0 preventsroundoff→arg
falseeffects. Nonuniform high-order gain remainsOPEN.

P82a147line4a90c0d card had M1 WALL/CPU and M2 fabricatedspan issues,
recorded by246line7e84262 review. Separate69line43218ab correction and
180line6aa5a2c exactreview nowcloseboth PRE-DATA; ROOTreadall. Keeporiginal
artifacts and semantics. CODEONLY commissioned; primarysource/spec/tests/
contracts notyetfrozen, no import/AST/pytest/RNG/graph/native allowed.
Independent306line raw-audit plan1f8f0ce frozenbeforedataset exists; checker
awaits exactschema and separatecommission. No newmain/qual/heldout/QPU.

P82a next predata checkpoint: six-file code freeze892ea965 now exists;
ROOT read the entire3024-line population. P66/P81 independently read that
same source. Factory timing needs an explicit typed reported-duration
reference before qualification, although scalar operands are retained.
P63 is preparing its independent recorded-data checker CODE ONLY. No
scientific execution, import/AST/RNG/graph/native has occurred.

P82a unique qualification94f80b94 now completed: raw8e6ba066 sealed
beforeinterpretation, receipt39b61bb9;27PASS/183Naive observations,
65zero refs/nativezeros, maxabs2.22e-16. ROOT frozenstdlibinspector6d5f823
independentlyrecalculatesall183; v2manifestvalid. IntegratedCI9ba543c
observedGREEN1214PASS19.57s/602historicalfilesunchanged. NoDEVmain yet;
independentchecker must freeze before those data. NumericalworkerFREE.

P89 sourcef775f682/e99a1e32 and exactaudit68baaeb8/eef75599 accepted
afterROOTfull215+149lines and own handreconstruction. The current ideal
source-blind rawkernel has uniform removals independentofY at fixedr,
forallη; exactrawcostmean isolatesinducedT/crossmarginals. No quench/
trajectory/generalclassicalsimulation/optimizeradvantage conclusion.
Source-awarecoupling/loading escapesarebeingdesignedSTATIConly; P82
frozen pilot, paper/main/QPU and all negative evidence remain unchanged.

## P82a recorded audit complete; changed P90a implementation

The sole primary96-attempt main remains inconclusive: B46/22 and each fixed
FAST mode46/22, with all four early work guards. No optimizer advantage,
strict eligible veto, D/Tier2 result or unchanged B rerun is claimed. Original
raw seal561410b3 precedes interpretation; ROOTdebd823 is a later integration.

Independent predata checker34c95130 has two preserved administrative failures:
prelaunch output nesting, then valid90.0 rejected by a strict integer check.
The separately revieweda965e08d correction changes only that timeout type,
not scientific logic. Freshqualification00322PASS precedes separately
authorized51-input audit002. Rawb7a19df before reading, separate143-line
receipt302ae135+07438069: FINITE_RECORDED_DATA_AUDIT_PASSED,96counts,7014cuts
and912FAST checkpoints agree. No native physics or optimizer was replayed.
Old input closure preserved on research/p82a-audit-v1-evidence@b4aa0f3.
Frozen launcher2f858e6 executes complete1236PASS/44.09s local tests; logs
26d18f3 sealed before interpretation. See reports/P82a_ROOT_FINAL_CHECKPOINT.md.

P90 source-labelled nonflat mechanism and exact review accepted scoped:
itsK4toy raw-mean response is real but two-photon groups reproduce its whole
law. P90a prospective n24/K12 card14d8dbdd and exactreview20986ff4 are now
CODE ONLY commissioning, with isolated parent/source and children/tests/contracts.
No import/AST/collection/seed/graph/native until whole freeze and exact-source
reviews; no qualification/main authorized. P91 conditional spectral-loss
replacement and P92 every-column calibration counterexample accepted with
independent hand reviews; novelty, calibrated Lucy and measured costs OPEN.
P93 rank-two initializer surrogate awaits independent exact-source review.
Paper/main/QPU/held-out remain frozen, CLAIM-042OPEN, all negatives retained.

## P90a qualification complete before any DEV data

The changed source-aware/nonflat compiler is frozen82d7b63,7files3851lines,
source95fa65c6. ROOTfullread and independent174-line reviewe7ce3474 precede
separateauthorizatione9e1150. The sole qualification's raw929f752 was sealed
BEFORE reading; ROOTcopy5ab76ae is later. Separate159-line receipt82d74145
+b2f9af31 has SHAd43f6d8b.283PASS/6warnings28.34s pytest,29.103454s runner,
CPU60/WALL90/env1/native1,18input hashes unchanged, v2validproducerANDROOT.
IndependentROOT integer-DP inspector5a0de0d reproduces254amplitudes/probabilities,
181zeros,maxprobabilityerror2.220446049250313e-16,allcaps/paths/actualpins/readbacks.
JUnit1,530,960B,rawtotal1,546,437B; initialnativeconfig0 retained beforeconfigured1.
All native work max4receiver modes/4photons; the96-attempt/controlworkflow is
SCRIPTED, not actualB/FAST data. No DEV/productionrolehash/PCG/P43/P50 call.
Full integratedsuite1519PASS44.61s,wall45.633968s,env/native1,rawlogsb0d90be
before reading. IntegrationCPU120/WALL180 differs from scientificcaps.
See reports/P90a_ROOT_QUALIFICATION_CHECKPOINT.md. IndependentP63 recorded
checker is CODEONLY authoring beforeBdata; primaryDEVmain remainsunautorized.
P93 conditional surrogate source159+independentreview130 accepted, noactual
smallresidual/sampler/optimizerobstruction inferred; P90aH unchanged.
CLAIM-042OPEN, paper/main/QPU/held-out frozen, negative evidence unchanged.


## P90a changed source-aware/nonflat DEV cycle: independently audited negative

Base source82d7b63, actual clean mainb2f9af31, original raw seald3962d5 before
interpretation, separate receipt8bf3296b. Fixed ER9002401/RR9002402,
root90026001, n24/K12,96 attempts and1152 modeled photons. Full collision/
repair records retained. B111/28 loses to EACH fixed FAST random/spectral
104/27, with adequate first scans, normal returns and no early guard.
Both B best discoveries first occur in classical compiler_M. Decision:
REJECT this frozen pilot as NO_POSITIVE_SIGNAL; no unchanged B/guard rerun.

The independent pre-B checker60995930 qualified29PASS and its62-input opaque
binding received separate metadata review3cbdbc65 and ROOT authorization48270f7.
ONE replay completed4.952918s, raw seal0c9a8f1 BEFORE reading, separate
receipt7b1c3fd: FINITE_RECORDED_DATA_AUDIT_PASSED,29478 cuts/96 counts/7790
FAST checkpoints agree.62 input hashes unchanged; official v2PASS.
Clock arithmetic is checked, not timing authenticity or independent physics.
D/Tier2/fresh seeds/labels/held-outs/physical replication remain NOT_RUN.
The favorable-to-B grants are not matched total resource measurements.

Integrated1548 local testsPASS; GitHub535b778 actual1548PASS14.94s and602-file
archivePASS. reports/P90a_ROOT_FINAL_CHECKPOINT.md holds exact provenance.
P33/P37/E05b/main/paper bytes preserved; positive target remains OPEN.
P94 now investigates changed parity/code, collective-block and dissipative
mechanisms. Mathematical/prior-art audit precedes any new pilot. No QPU.

Administrative continuation: a fresh full checkout failed for disk space and
Git rolled it back. Only our completed clean fixtures checkout was removed,
after verifying its integrated bytes and preserving original Git refs. An
existing clean isolated checkout was reused for P94. No original raw data,
model, manuscript or user .DS_Store was deleted or silently changed.


## P94 changed decoder: audited scoped obstruction, not a positive pilot

Balanced paired Walsh spins make every count (even vacuum) a feasible code
partition. Exact raw parity means have a bounded signed classical permanent
oracle, and every ideal lossless parity support point is deterministically
preparable with at most HOM pairs. Thus the proposed expressivity witness
fails the independently reoptimized group2 control. Coarse block amplification
also retains a finite paid classical latent frontier. Efficient sampling of
mixture weights, quenched endpoints and fully costed adaptive search remain open.

Sourceb2b15069/120l, independent proof10d189d1/151l, primary checke3b1e6e/124l
all fully read by ROOT. Known Gurvits/binned-characteristic/parity-feedback
ingredients are attributed, not claimed new. No numerical test or pilot ran.
reports/P94_ROOT_PARITY_CHECKPOINT.md. P95 filter and P96 column-budget
surrogate continue mathematically before any new DEV run. CLAIM-042 OPEN.


## P95 dissipative-filter discriminator, analytical checkpoint

Sourcef145aca1/128l and independent proof6e2da25e/167l fully read at ROOT.
Exact raw-PNR+total-loss PGF yields vanishing first B-D derivative, a complete
quadratic pair stencil, full cubic pair/cycle terms, and a hard CPTP remainder.
A same-channel group2-mixture claim fails on the triangle; cubic magnetic flux
can already use only two occupied sources through an empty third mode.
For collision/loss self-loops and strict one-swap minima, improvement first
becomes possible at order>=beta4, with explicit paid fixed-r CF frontiers.
No favorable optimization sign or measured cost ordering follows. KEEP the
scoped derivation; finite-strength route OPEN, not globally ruled out.
No experiment ran; paper/main/QPU unchanged. P96 proceeds independently.
reports/P95_ROOT_FILTER_CHECKPOINT.md.


## P96 certified-column low-count surrogate: independently proved

Known CF inputs, passive vacuum channel, explicit T and trace mu<=1/2:
construct positive normalized correlated classical q supported0/1/2 photons
from exact first/second factorial moments. Exact TV=E[(N-1)^2;N>=3]
<=24e3(c)<=4mu³;24 attained exactly by a K3 rank-one physical channel,
4 sharp only via stated sequential limits. Complex T/repeated outputs and
all raw loss/collision/vacuum branches are covered analytically.

Source6f4e7fb9/169l, independent proof40d2e6a5/157l, primary-source
check8b5e9120/124l, all fully read at ROOT. Known moment-inversion and lossy
simulation ingredients are attributed; exact composition priority UNVERIFIED.
No finite-bit implementation/cost or photonic optimizer claim. Hypothetical
K12*.02 error.04224 is not Lucy calibration;96-trial union bound vacuous.
The real-rational/small159-native-point validation remains CODE ONLY, needing
full source review, qualification and separate execution authority. No run
or numerical success is asserted. reports/P96_ROOT_THEORY_CHECKPOINT.md.


## P96 predata code review checkpoint; no execution

Originalac67650/550l integrated97eb7c0; ROOT full source/tests/contracts/
population reviewe925879. IndependentP62 fullread finds nominal mathematics
coherent, but failure provenance can omit rejected nonfinite amplitudes,
actual drifting thread values, and rejected construction spectra/U/Gram.
This is a static review finding, not a failed experiment or false positive.
A code-only guard correction and two pure diagnostic tests (9->11) are being
frozen before any qualification;167/159/28 physical population, tolerances
and caps unchanged. No import/AST/collection/native/runner/QPU occurred.

P97 analytical card457e49c +35e1cf9 is read fully at ROOT. The corrected
complement statement assumes unweighted simple graphs. Variance bounds hold
for the stated estimator but fixed coefficient1 need not reduce variance.
After crediting the low-sector feasible frontier, I2h=0 for the direct
improvement statistic, so this CV leaves that rare-event estimator unchanged.
This rejects an automatic benefit, not every tail policy or other CV.
No new optimizer pilot is justified; goal OPEN and paper/main/QPU frozen.
Latest confirmed remote ROOTed7d24f includes P95/P96 theory+original refs;
unqualified local code is not pushed to CI.


## P96 completed finite validation and P98 accepted hierarchy

P96 main originalsource0eabdad, executionad8fd53, raw240c7e5 BEFORE reading:
FINITE_VALIDATION_PASS,12valid+1outside-domain case,167 exact bins,
159 deterministic full-PNR Perceval amplitudes/28 unconditional marginals.
Initial nativeconfig0 is preserved;configured/import/final and all159 before/
after readbacks1. Main35 inputs unchanged, officialv2PASS. No RNG/graph/QPU.
Independent scalar checker d1a3875 executes once on sealed raw, audit ea84490
BEFORE reading,43 inputs unchanged/v2PASS. All567 records and159 amplitudes
checked by independent pair-moment/subset-DP/scalar-Gram arithmetic; max
probabilitydifference2.22e-16,marginal/Gram1.4433e-15. Separate receipt2c1d712.
The11 pure qualification and corrected1559 full tests are separately receipted.
First integration FSIZE4MiB fixture-copy failure remains preserved; only its
wrapper changed to32MiB for existing17MiB P33 data, no scientific cap change.

P98 source8a01023f160l, independent audit77811d2a97l and bounded primary
check9cad69d5140l fully read/accepted at ROOT. Signed factorial truncation
plus proved positive repair yields whole-lawTV<=2^s(s+1)!e_(s+1)<=mu(2mu)^s.
Fixed certified rho<1/2 and fixed epsilon give polynomial dimension work;
inversepoly accuracy/polynomial transcripts generally quasi-polynomial.
Exact rational/fair-bit construction is stated with encoded rational epsilon;
a changed physical T requires a raw-law xi certificate. No actual Lucy
certificate, PRNG implementation, measured speed or optimizer result follows.
Established inversion/lossy-correlation ingredients are attributed; exact
combined priority remains UNVERIFIED, not newly discovered by failed search.
A bounded exact-only hierarchy/negative-coefficient experiment is CODE ONLY,
including one explicit16-source rank-one algebraic law. No native16-photon
calculation, optimizer, graph, RNG or QPU is authorized by that design.
Reports P96_ROOT_FINITE_CHECKPOINT.md and P98_ROOT_HIERARCHY_CHECKPOINT.md.


## P98 finite hierarchy and P99 scoped weak-passive obstruction

P98 source52070f1a/179lines plus passive contract/population fully reviewed
at ROOT235lines and independently80lines. Predata metadata adds descriptive
mathematics.inputs in separate authorized binding9fbdaeb only. The sole run
finishes0.136543s/exit0; six raw files sealed4c4b1cb BEFORE interpretation.
All25 input hashes unchanged, officialv2PASS.14 cases,184 moments,68 pairs,
1054 dense coefficients,1321 records; R16 negative coefficients/repair and
physical X4 mu1 outside-domain retained. Separate receiptb4536af and report
P98_ROOT_FINITE_CHECKPOINT.md. Finite rational consistency, not optimizer gain,
categorical sampling execution or independent physical replication.

P99 sourcea8e80a10/198l, non-author proof2ff020a0/173l, bounded primary
attribution49a7b0c5/135l fully read at ROOT. For fixed real dense H with fresh
orientation, K2..12 and admitted2t, an explicit weak interval gives D(2t)
off-diagonal dominance over B(t). Common fixed finite-temperature Metropolis
orders forms/Rayleigh and stationary-outside hitting means, not every-start
or best-of-T quality, annealing or total wall cost. Explicit counterexamples
protect those exclusions. KEEP scoped obstruction, change architecture;
reports/P99_ROOT_WEAK_PASSIVE_CHECKPOINT.md. No priority or broad no-go claim.

## P102 mission continuation: primary-literature transfers and new portfolio

User26-Nov mission read in full from attachment4ed38ab8: preserve foundations,
research-first new mechanism, deep neighboring sources, strong D/classical/
fresh-graph/relabel/resource/independent gates before QPU and article. The
target is durably fixed in research/P102_MISSION_TARGET.md, not silently
replaced by passing tests. P100 complex inverse-sign lift frozenf7d3ba9/203l
has exact stationary/cubic/loss-memory analysis but no positive signal;
independent audit pending. Its cubic term already has a polynomial classical
mirror. P101 finite magnetic/all-output route is being derived separately.
ROOT P104 transfers authenticated nonnegative matching/counting results into
a coarse full-K-or-FAIL transcript; candidate proof awaiting independent audit.
The distinction from retained partial-loss counts is explicit. No new DEV,
held-out opening, hardware preparation, paper/main edit or QPU call. Goal OPEN.
