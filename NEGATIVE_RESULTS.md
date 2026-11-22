# Negative Results Log

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

### Entry 2
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
