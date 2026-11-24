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
