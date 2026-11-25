# Negative Results Log

Current disposition (2026-11-24): the tested bosonic optimization benefit is not demonstrated. Read reports/NUMERICAL_RECONCILIATION.md and the recovery section below. Early entries are historical working notes, not automatically verified evidence. In particular Entry2 is explicitly withdrawn: fixed photon number does NOT imply collision-free output; HOM and full-Fock validation refute it. Its original text is preserved to expose the earlier error, not endorse it.

Format:
- Hypothesis
- Protocol
- Result
- Likely reason
- Decision

## Logged Results

### Entry 1
- Hypothesis: Random interferometer achieves good balance
- Protocol: Sample 1000 shots from random U(4)
- Result: Average energy = 1.5 (vs optimal 1.0)
- Likely reason: Random unitary explores full energy landscape
- Decision: Need optimization, not random sampling

### Entry 2 — WITHDRAWN physical claim
- Hypothesis: Fixed-photon subspace has P_CF = 1
- Protocol: Measure collision probability
- Result: Confirmed - no collisions in fixed-photon subspace
- Likely reason: By construction
- Decision: This is the key advantage

### Entry 3
- Hypothesis: Penalty-based approach matches fixed-photon
- Protocol: Compare energies with same interferometer
- Result: Pending
- Likely reason: Pending
- Decision: Continue testing

## 2026-11-20 research restart: corrections to historical entries

- Entry 1: UNVERIFIED. No raw run/seed supports the reported 1.5; it must not be used as evidence.
- Entry 2: REJECTED. Its claimed confirmation was false. Full Fock includes collisions; HOM has P_CF=0. Historical text is retained above to document the error.
- Entry 3: OPEN historical proposal, not an executed comparison. The old PenaltyObliq never implemented optical ObliQ dynamics.

## E03 — rejection rewards the defective objective

Hypothesis: minimizing the subnormalized CF cut moment improves optimization.
Protocol: nine objectives, n4, six families, two graph seeds, three training seeds, budget120.
Result: bad-moment objective mean P_CF=.013038 and physical success=.013005.
Likely reason: discarded events drive the objective toward zero.
Decision: REJECT; retained as an explicitly labelled negative control only.
Raw data: experiments/E03_objectives_pareto/runs.jsonl.

## E05b — no tested bosonic computational benefit

Hypothesis: multiphoton interference improves unknown-optimum search at equal attempts.
Protocol: 756 runs, six families, n4/6/8; every run120x256 training+4096heldout actual ideal draws.
Result: n8 final mean success .067873 bosonic vs .137707 distinguishable; median first optimum89 vs27; uniform feasible median17.5. Every model run had already found an optimum during training.
Likely reason: collisions, optimizer landscape and classical discovery cost; observations do not isolate a unique mechanism.
Decision: REJECT benefit claim for this route; no global impossibility inferred.
Raw data: experiments/E05b_exact_equal_budget/runs.jsonl.

## E06 — implementation failure preserved

Hypothesis: collision-pair identity gives valid upper/lower bounds.
Protocol: full Fock random circuits, original E06.
Result: assertion failed because a chained comparison cancelled the upper tolerance.
Likely reason: implementation bug in the check, not false physics.
Decision: FOLLOW-UP E06b fixes only the assertion and passes; both manifests retained.

## E07/E09 — anchors and shallow reachability

Hypothesis: high hybrid/shallow success demonstrates useful bosonic interference.
Protocol: spectral anchors plus meshes; label-control on12 n6 graph slots with5labelings.
Result: spectral alone solves27/36 slots;5/48 shuffled depth2 slots have unreachable optima.
Likely reason: classical preprocessing and label-dependent ansatz support.
Decision: REJECT that inference; retain all graph slots.

## E08 — low collisions do not imply closeness to distinguishable statistics

Hypothesis: vanishing collision probability implies TV to independent distinguishable particles vanishes uniformly in system size.
Protocol: exact balanced spectator construction, independently reviewed proof;9rational cases, full Fock n4/8/12.
Result: delta=2/(k+2)->0 while TV=1/2.
Likely reason: delocalized two-photon block retains interference while its collision rate shrinks.
Decision: REJECT hypothesis. The example itself is easy to sample classically.

## Penalty version sensitivity

Identical seeded COBYLA protocols give different trajectories under SciPy1.13.1 and1.17.1. Both datasets are retained in experiments/validation/objective_penalty_audit*.json; only the pinned .venv run is canonical. High feasibility can coexist with no observed optimum (see PENALTY_BASELINE_AUDIT.md).


## 2026-11-22 retained obstructions and failed execution

- Native schema/action probes20261122T013524Z/014132Z/014349Z failed completion;
  the actual local health call passed but synthetic structured_output was absent
  in observed model tool schemas. Failed/cancelled contexts are preserved.
- The successful seven-role cycle20261122T014822Z still produced false prose
  (mean intensity1 instead of1/2, incorrect inequality and scope descriptions).
  Reject that reasoning; accept only independently checked raw calculations.
- Float-positive-sum fixes do not prevent all underflow: the exact rational
  rotation t=2^-600 has positive TV while rounded estimates are0. The model is
  explicitly not interval certified. See64ad463; the initial missing-PYTHONPATH
  audit failure is retained alongside the corrected completed run.
- P34's initial-identity control has first-circuit TV0 and positive later
  transcript TV. Initial-only certification cannot justify adaptive replacement.
- Cross-field source checking rejects novelty for standalone row Bayes/Gini
  inequalities. Exact composition attribution remains OPEN, not disproved.

## P34/P36 proof failures and resource limits — 2026-11-22

P34's original product bound omitted e_t in [0,1]; e1=e2=3 makes its RHS
negative. Correctedb3b0219 adds the range and passes independent review;
the defect does not refute the corrected theorem.

P36's tempting per(B)-1<=2delta shortcut is physically false: an exact
three-mode rank-one witness has excess265/9826. Its actual full-law TV
still lies below delta. This refutes the proof route, not the TV conjecture.
No counterexample in the bounded fixed/targeted searches is no universal proof.

P20 archived campaigns select zero interaction. Retain the small bosonic
enrichment over the matched distinguishable product, the stronger classical
correlated control and unequal total training costs. No algorithmic gain.

P37 improves Haar resource accounting only: accepted ensemble subsets remain
uniform. Higher feasibility alone supplies no graph-quality signal or paper gate.

P35 review56a34d0 found NaN state/transition caps disabled the old guard.
Archived scientific calls used finite integer defaults and are unaffected.
Repairb5d2888 validates integer inputs at both entry points;287 tests pass.
The failed guard probe remains in the frozen pre-fix review data.

P38b/c: all four compact-effect SLSQP cells fail convergence at the declared
caps/line-search condition, even after a targeted warm-start refinement. Keep
10790 calls and exact repaired lower witnesses; none proves a global bound.

At delta0 the proposed finite-dual-witness subgoal is unattainable: each
nonzero sector has true cost0 but strictly positive cost for every finite
dual witness. Use a direct endpoint proof or an infimum/limit, not `min`.

P39 exact counterexample rejects only extending the k2 curved bound to the
larger pinched metric at k3: D_pinched>.48986 while the curve is.4608.
Measured TV≈.265153, so neither measured linear/curved hypothesis is refuted.
This is a post-hoc auxiliary obstruction, not evidence of graph advantage.


## Recovery reconciliation — 2026-11-24

Every E05b run is retained. Bosonic final means .6523129783/.2795490911/.0678727604 are below distinguishable .7132846817/.5366140370/.1377071293 at n4/6/8. All756 runs discover an optimum during training. The no-benefit conclusion is restricted to the measured grid/budgets, not all photonic algorithms.

Only9/9/10 unique labeled weighted graphs arise from twelve nominal slots per size. Graph-cluster intervals are descriptive; exact within-batch first-hit order is missing. P21 classical controls use scored cut queries, not equal physical attempts. Authentic ObliQ training/source/decoding remains incomplete. Oracle-preparation gains cannot support autonomous search.

The unsupported n10/12 and4.8× advantage tables, K4 Haar0.2, K2,2 optimum4, identity-uniform claim and noisy.381 value are withdrawn. Original versions remain in Git6154b46. Full claim dispositions: reports/SCIENTIFIC_INTEGRITY_AUDIT.md. First TeX cache/missing-table setup failures are build failures, not scientific negative experiments.

## P41/P42 falsification — 2026-11-24

- Weak-angle chiral exchange has a real interference term, but a positive
  classical feasible proxy reproduces its leading current.72 finite cells
  support the calculation, not a new optimizer advantage.
- Grouped feasible probabilities have a classical random-wave cover. A naive
  all-CF extension fails normalization (exact mass913/625); pointwise dominance
  alone also fails for divergent adaptive histories. Both failures are retained.
- The old quadratic mean obstruction does not extend to every convex cost:
  the connected L1 example has bosonic mean lower by3/16. A failed proof
  shortcut does not establish computational benefit.
- The distinct-input P42 cap fails for a bunched input: two-click probability
  2167/80000>1/100 at eta0.1. Independent physical replication retains it.
- Partial distinguishability need not reduce each useful probability: the
  DFT6-plus-spectators two-species construction violates the naive identical
  envelope. The corrected general bound uses ordered ranks and block traces.
- The source cap is nonmonotone: b_(5,3)>b_(6,3) for0<eta<1/3. Checking only
  Nmax would be invalid.

No positive new graph benchmark, hardware efficiency or guaranteed device cost
is fabricated. Immutable runs and interpretation: reports/P42_DISCOVERY_CHECKPOINT.md.

## P43 finite-angle global objective — 2026-11-24

The new full8/10-photon echo does not improve its charged common anchors in896
B attempts (373 CF/523 collisions), nor do independently selected D/field/b4
settings. Anneal/spectral controls improve both20-mode anchors at their frozen
score budgets. No C* is required to exhibit these lower-cost classical candidates.
The all-zero selection cancels optical probes; do not call their absence a passed
relabel or fresh-seed test. Independent full raw audit agrees. Preserve all four
graphs and the negative; reject only this family and budget. No held-out fishing.

The P44 cap has distinct hypotheses: bunched spatial inputs, falsely identifying
mean/column transmission with the spectral norm, or reusing the identical cap
for arbitrary internal states are invalid extensions. The prior DFT6 example
physically violates eta^k under partial distinguishability at small eta. The
corrected k! bound and declared CF source preserve those scope distinctions.

## P55 finite-coherence neutral decoder — 2026-11-25

The qualified all-count neutral decoder changes the weak-order direction, but
its one frozen two-graph pilot still fails. All480 draws/96batches complete;
the B paid minima39/38 lose to random-first AND separately budgeted
spectral-first classical search11/22. The independently selected D and
inclusion controls have lower observed fresh equal-graph means. The sample
does not support population ranking or a claim about every possible lean
implementation. The full cost envelope, raw counts, exact ranks, seed roles,
failures(null), selections and FAST eligible traces are retained in
experiments/P55_finite_neutrality/run_001/ and
research/P55_finite_neutrality_result.md. Independent recorded-data audit
4352d25 confirms all480 observations and the veto. No held-out graph was
opened to rescue this pilot; no QPU or manuscript update follows from it.

## P61 scalar extension: analytical veto before a pilot — 2026-11-25

The proposed single-phase N18 extension changes only output ports1,7,13.
Under independent uniform physical embeddings, a paid classical frontier of
at most8 feasible completions stochastically dominates decoded best-of-T
costs; the independent P62 theorem states the exact hypotheses and scope.
No scalar P61 graph/counterexample pilot was run, and no negative numerical
measurement is fabricated. Equal wall time is not proved. P63 changes the
controlled support to15 outputs, so that specific constant-size envelope
does not settle it. P59's real six-mode mean response remains valid and
has a small exact-law classical replacement; neither is an accepted optimizer.

## P63 extensive phases: the registered DEV gate failed — 2026-11-25

The changed N18/ten-phase/15-active-output circuit completed all80 B attempts
and all four separately costed FAST searches. B's all-paid minima81/60 on
ER6301801/RR6301802 lose to random FAST54/42 AND spectral FAST54/42. Each
fixed mode wins both graphs, without a free portfolio or B incumbent. Eligible
online results are within the prospectively defined B-only classical WALL
allowance minus adapter CPU; no early cap was hit. Optical latency was assumed
zero, and imports/backend/diagnostics/IO did not fund classical search.

The final iterate's fresh normalized means55/104 and633/1184 are retained,
as are all training counts/cuts/updates. Every collision was decoded; no
optimum or known partition was used. The primary run and raw data were sealed
bf2034d before interpretation; v2 manifest completed with18 unchanged inputs.
Source qualification46PASS and separate existing regression1044PASS. See
research/P63_STAGE1_MAIN_RECEIPT.md for full costs/provenance. The independent
recorded-data audit remains pending; no new physical replication is asserted.

All optional models are NOT_RUN_DUE_FAST_VETO. They were not passed, measured
as negatives or silently dropped after a positive. No retuning, replacement
graph, unchanged wider sweep, held-out rescue, manuscript revision or QPU call
followed. This rejects the specified finite pilot, not all extensive or global
photonic architectures. P65 seeks a changed mechanism; the positive goal OPEN.
