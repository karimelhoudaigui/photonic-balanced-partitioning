# Current research status — 2026-11-22

PAPER_READY = FALSE. QPU_GATE = CLOSED. Original optimization goal remains OPEN.
The tested generic bosonic mesh remains NO-GO as computational-benefit evidence.
No hardware request or noise campaign was executed. The manuscript is frozen.

The [2026-11-20 scientific checkpoint](reports/RESEARCH_CYCLE_2026-11-20.md)
retains the full historical E01–E09 evidence. Subsequent checkpoints below add
results; they do not turn earlier negative experiments into positive evidence.

Accepted Phase3 checkpoints:

- P30: the authenticated static ObliQ optical kernel agrees with its archive,
  explicit Fock calculations and Perceval. Its known Rx angle discrepancy is
  retained as separate literal/corrected variants. This is a component, not the
  complete original training/source-selection/prefix-decoder algorithm.
  See [optical audit](reports/PHASE3_OPTICAL_PENALTY.md), c3b83ef.
- P31: fixed-input, fixed-order static penalty washout has a restricted exact
  proof and independent reconstruction, with 972 unitary and 36 Fock checks.
  It bounds distinguishability of optical states, not optimization time or
  information already supplied to the classical graph-aware decoder.
  See [independent review](reports/PHASE3_WASHOUT_INDEPENDENT_REVIEW.md), 6fcfc94.
- P32: exact threshold/photon-budget checks show that per-attempt, per-photon,
  finite-budget and all-photons-detected criteria can select different sources.
  195 rational cases and 120 circuit checks pass. Haar feasibility is not graph
  optimization. See [threshold audit](reports/PHASE3_THRESHOLD_AUDIT.md), 2ed2e7d.
- Occupation objective: exact low-order mean costs are classically polynomial
  to evaluate. For nonnegative weights and collision penalty mu>=0, the bosonic
  mean is at least the distinguishable mean on every identical occupied frame.
  This does not order success tails; a retained small example reverses those.
  See [derivation](theory/phase3_occupation_dominance.md), 98e4ecc.
- P33: the exact density/expected-collision theorem at75e5831 passed a fresh
  independent proof audit, integrated4420e17. A positive intensity floor c,
  expected collision-pair count M, and dominant-support leakage give sufficient
  absolute-TV bounds; the refined leading coefficient M/(2c) is sharp in a
  balanced two-photon family. Collision probability alone is insufficient.
  See [proof review](reports/PHASE3_DENSITY_INDEPENDENT_REVIEW.md).
  The improved floating implementation77a8588 is explicitly not interval
  certified. The corrected native primary/replication cycle passed its separate finite audit (300 grid circuits); see reports/ASTRA_P33_COMPLETED_CYCLE_REVIEW.md.
- Absolute-TV control need not remove a rare-event success ratio: the exact
  retained family has a factor-two ratio while both expected waiting times
  diverge, and a disclosed correlated classical control solves the toy case.
  See [success scope](theory/phase3_density_success_scope.md), 385293e.
- P34: corrected adaptive replacement b3b0219 passed independent review3c43eda.
  Uniform conditional majorants lie in [0,1]; the original missing-range defect
  is retained. Standard coupling does not control rare-event ratios or erase cost.
- P35: known rank1/2 threshold DP now has exact-rational code. Six physical
  rational frames match full-Fock arithmetic exactly;12 Perceval comparisons
  pass, max energy error7.11e-15. This is a classical mean-objective control,
  not a novel algorithm or sampler/training equivalence. Report: P35_THRESHOLD_BASELINE.md.
- P36: sharp two-photon TV<=delta-delta²/2 has a complete coordinator proof.
  General TV<=min(1,delta) remains OPEN after256 circuits and17856 search calls.
  An exact physical witness refutes a positive-Gram shortcut, not the conjecture.
- P37: Haar-loss source maxima reduce to two choices per attempt and four per
  photon, with ordered unique transitions. Proof/boundary scaling passed fresh
  independent review7729b91. All1610 probabilities and36 rational root
  brackets pass a separate exact implementation. No large Fock simulation or
  graph-quality gain. See reports/P37_LOSS_SOURCE_SELECTION.md.
- P38: phase-preserving pinching/variational/cone reductions have a complete
  coordinator derivation. All36 new rational circuits and a direct tensor-state
  audit pass; six Perceval checks max1.11e-16. General pinched linear bound OPEN.
  Compact-effect searches total10790 calls, no converged solver or certified
  refutation. Do not call these global optimization certificates.
- P39: exact auxiliary counterexample at delta18/25 refutes the curved pinched
  envelope: D_pinched>24493/50000>288/625. Two rational proof paths and one
  full-law Perceval check pass. Actual measured TV≈.265153 remains below the
  curve, so the measured conjecture is not refuted. No novelty/gain claim.

Novelty: spatial-Gram N1 is a formal corollary of earlier boson-sampling analysis;
N2 follows from known permanent/cycle machinery. Low-rank threshold expectation
DP is already in primary literature. The exact dominant-support/density
composition and restricted optical-kernel specialization retain unresolved
attribution, not a novelty certificate. See research/phase3_density_novelty.md,
research/phase3_lowrank_sources.md and research/phase3_washout_novelty.md.

Infrastructure: official Qwen Code0.28.0, Ollama0.32.0 and one local Qwen3.5-1.9B
Q4 model are installed on the measured M2/8GiB host. Native saved Workflows
have demonstrated distinct sequential subagents and real handoff. The separate
native Agent Team lifecycle remains FAIL. A typed local stdio scientific bridge
is connected; a nine-dispatch/seven-role cycle completed with real primary/replication and three exact handoffs. Model scientific prose remains unreliable and was rejected. No paid
inference or larger automatic download is enabled. Reports and raw receipts,
not model prose, determine acceptance.

Current working-tree tests: 287 passed, six Perceval cache-permission warnings;
P20 sources/16 tests integrated; P35 has23 focused tests after its resource
guard repairb5d2888. Separate review56a34d0 verifies190 exact marginals and
retains the pre-fix NaN defect. SymPy1.14.0 and mpmath1.3.0
are pinned in the optional theory extra. Historical manifests are validated at their
recorded input revisions, not against later metadata changes.

Next: continue exact novelty/operational interpretation checks, attack the
remaining P36 phase-cancellation gap, and require a changed mechanism before any
broader optimization sweep. Full authentic ObliQ
training/hybrid input/decoder and a useful optimum-blind algorithmic advantage
remain unresolved. Details: OPEN_QUESTIONS.md, CLAIMS.md and RESEARCH_LOG.md.


Latest accepted native Qwen execution: b8b04ac, original worker fe7d616. All300 complete-grid
cases and886440 outcome probability pairs retained, plus14 sharpness cases,
12 factorized dilute controls and72 certificate-only cases. Twelve additional
independent Perceval/labelled-DP comparisons differ by at most6.67e-16. Full-law
checks stop at m12. Figures and portable supervisor audit are in
results/P33_density_supervised/20261122T014822Z/.

P20 archives5dbdbc3 and reviewa4d4745 reject the tested fixed proposal mechanism:
selected interaction is zero. These are fixed-anchor IID probes, not executed
adaptive searches or equal-total-resource proofs. Original drivers overwrite
fixed paths: heed experiments/P20_structured_probe/ARCHIVE_NOTE.md.

P33 numeric review9e8bd82 retains subnormal/roundoff limits; its original manual
manifest is not valid v2 evidence. Separate coordinator rational underflow runs
have valid failed/completed records. Matrix-geometry review715143f identifies
row-max rounding and its norm step as known. Full composition attribution OPEN.

Late-2026 source audit538e67b authenticates fixed-loss Haar-typical simulation
theorems and the near-full reference/error constants. They do not cover every
trained U or eta=1-lambda/m; their finite bound can be trivial at m64,eta=.9.
See research/LATE2026_LOSS_SOURCE_AUDIT.md for exact dependencies and limits.

Current full handoff: reports/RESEARCH_CHECKPOINT_P39.md. Reviewers delivered
real P35/P37/loss packets before another quota interruption; partial P36 files
are preserved with original hashes. Astra completed P38/P39; no interrupted
review is relabeled complete. Paper and QPU remain closed.
