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
  certified. The corrected native primary/replication cycle is still pending.
- Absolute-TV control need not remove a rare-event success ratio: the exact
  retained family has a factor-two ratio while both expected waiting times
  diverge, and a disclosed correlated classical control solves the toy case.
  See [success scope](theory/phase3_density_success_scope.md), 385293e.

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
is connected; its full scientific workflow remains under verification. No paid
inference or larger automatic download is enabled. Reports and raw receipts,
not model prose, determine acceptance.

Current working-tree tests: 264 passed, nine Perceval cache-permission warnings;
includes 16 tests in preserved untracked Phase2 drafts. SymPy1.14.0 is pinned
in an optional theory extra. Historical manifests are validated at their
recorded input revisions, not against later metadata changes.

Next: finish and independently inspect the bounded native primary/replication
cycle; continue exact novelty/operational interpretation checks; require a
changed mechanism before any broader optimization sweep. Full authentic ObliQ
training/hybrid input/decoder and a useful optimum-blind algorithmic advantage
remain unresolved. Details: OPEN_QUESTIONS.md, CLAIMS.md and RESEARCH_LOG.md.
