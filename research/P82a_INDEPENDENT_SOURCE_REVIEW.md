# P82a independent consolidated-source review

26 November 2026. Static review by the independent P66/P84 audit worker,
before qualification, graph generation or any numerical execution.

## Primary verdict

**REQUIRES PRE-DATA CORRECTION: explicit typed reported-duration provenance.**
The implementation does not yet implement the addendum's required
`REPORTED_DURATION` record and its reference from the factory
`DURATION_DIFF`. This is a material source/contract recording discrepancy,
not evidence of an incorrect measured allowance or an accepted false veto.
Correct it explicitly, freeze the changed bytes, and review that correction
before authorizing qualification. An implicit equivalence between an untyped
scalar field and the required referenced record should not be accepted.

No other material blocker was found in the complete static reading described
below. This verdict neither qualifies the software nor authorizes a run. No
test, import, AST pass, probability calculation, RNG, backend call or timing
benchmark was performed by this reviewer.

## Exact reviewed population

Producer worktree: `.local/p65-independent-audit`; clean source commit
`892ea9651d0f489f3dbdc79c6679567ac4735b75`.
All six files were read completely, not selected excerpts: 3,024 lines total.

| File | Lines | SHA-256 |
|---|---:|---|
| `research/P82a_split_scatter_veto.py` | 1328 | `c40d7ef84d9b8ceb833a28f91aaf2ff43bb5eaf3fffcad6e99447eeb72f54257` |
| `research/P82a_execution_spec.json` | 74 | `8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838` |
| `tests/test_p82a_split_scatter_veto.py` | 961 | `893fdb25598e407ce96f0e81b9691f9eb6f6352968d25e375a728ffe2f0fd0a3` |
| `research/P82a_split_scatter_preflight_contract.json` | 243 | `209696de0b0170ff4099cdfd77b6acdaec3c4f78e04e86631047008c13517c0d` |
| `research/P82a_split_scatter_execution_contract.json` | 203 | `dca509b4fee65b652227fb395cfc982b4426a9c8ae0da05de75f825493cc5f20` |
| `research/P82a_IMPLEMENTATION_POPULATION.md` | 215 | `68b249e450ff2af1db16e41c3daa36b1ea91cf58bd5066eca1c286012e45e544` |

Dependencies compared with the source are the frozen 145-line design at
`f7cb5d99fa35b6ab9e6ff60839f985d81ea87001`, the 147-line DEV contract at
`4a90c0d9ce06329115b6c8182fd45c28397f0fab`, and the 69-line corrective
addendum at `43218ab508beb84c46a8575c28411b34f8570a79`. Their SHA-256 values
are respectively `c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723`,
`d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9`, and
`1b548885d05fe6a42487c77b12ac00292ebd8bd379c4074e6ce3a49ceb93a8d4`.

This review also uses the earlier independent design, DEV-card and clock
reviews at `ae900ed`, `7e84262` and `6aa5a2c`. The immutable P43/P50 source
and the P50 from-raw API card were inspected as text. No draft from another
reviewer or any P82a outcome was read. No outcomes exist for this review.

## R1 — material recording correction required before qualification

The addendum section 3 requires three distinct record kinds, including a
helper-reported setup duration with helper/source and outer-event references,
unknown endpoints and unknown setup CPU. It requires the derived difference
to reference both its observed and its reported operand.

At source lines 440–452, `duration_difference()` records the outer-event ID
and an inline `reported_setup_wall_seconds`, but no `reported_ref`.
At lines 588–593, `Ledger.factory_residual()` appends only this derived record.
At lines 715–721, the caller emits an untyped `factory_report` containing
`backend_setup_wall`, `outer_ref` and the difference ID. That report has no
unique event ID and is not the required `REPORTED_DURATION` record. It does
not explicitly expose the helper/source reference or the unknown endpoint and
setup-CPU fields at that record.

The numerical operands are retained and the subtraction is reconstructable.
The current code checks finite nonnegative nested durations, retains the
observed outer CPU, uses null endpoints/allocated CPU for the difference, and
adds only the residual once to the paid allowance. Thus this finding does
**not** assert a wrong subtraction, a fabricated CPU allocation or hidden
double counting. It is the exact provenance structure promised before data
that is missing.

Required correction:

1. Emit a distinct `REPORTED_DURATION` with a unique ID, case/attempt owner,
   immutable P43/helper-source reference and observed outer-event ID.
2. Retain its setup WALL scalar, explicitly null start/end CPU/WALL endpoints
   and setup CPU, and mark it unpaid. Do not invent an internal timestamp.
3. Give the derived `DURATION_DIFF` both `outer_ref` and `reported_ref` pointing
   to the retained records. Preserve its label, formula, unknown endpoints and
   unknown allocated CPU. Pay that difference once; do not additionally pay
   the reported or containing observed record.
4. Add a deterministic schema/association check for unique IDs, both resolvable
   references, unknown fields and the one-time allowance inclusion. Freeze
   changed source, fixtures and contract hashes before qualification.

This is a localized pre-data correction. It requires no new graph, seed,
optical point, budget, result-dependent setting or immutable-helper edit.

## R2 — same explicit operand binding for the conservative FAST supplement

At lines 784–843 the outer and direct-adapter spans are retained with actual
timestamps. The conservative call gap correctly subtracts the reported helper
compute duration from these containing measurements, checks each CPU/WALL
operand and rejects a negative difference without clipping.

However, line 802 uses the literal field-name string
`P50.compute_cpu_seconds/compute_wall_seconds` as `reported_ref`. It is not a
unique reference to a typed retained helper-duration record. The numeric
values are retained in the later compact result, and case/mode context makes
the arithmetic reconstructable; that is still an implicit association.

As part of R1's small provenance correction, create an explicit uniquely
identified P50 reported-compute record and bind this reference to that ID.
Retain its helper/source, case/mode and containing outer-event reference.
These helper-reported CPU and WALL durations are known scalars, unlike the
unknown setup CPU of the P43 factory report. Their internal absolute endpoints
remain unknown. Do not turn either derived difference into an observed span.
Give the conservative difference its own unambiguous ID if referenced later.

This is a recording requirement, not an objection to the approved conservative
formula. Charging the entire nonnegative entry-plus-return residual to every
candidate prefix can exclude a genuinely timely witness; it cannot make a
late witness timely. The record must continue to say that it is a conservative
derived charge rather than a measured contiguous prefix interval.

## Static findings supporting the remaining source gate

### Causal optical experiment and scored states

The graph/current/marks compiler finishes before the removed-set draw. The
phase sweeps use the declared cost-derived two-photon merit and preserve the
frozen setting; they do not query an optimum or known optimal-state mask.
The literal F4, splitter profile, relative phase architecture and source-column
checks agree with the proposed passive construction. The eta-zero branch
records the analytic null and retains its initial phases.

For each attempt all eight split coins are drawn and recorded. The zero-removal
branch is a real no-factory/no-sampling branch; nonzero branches use the
registered serial P43 conditional sampler, including removal count eight.
Requested/completed attempts, all raw counts, collisions, repairs and role
seeds are retained. Malformed counts or fallback flags fail rather than
silently replace the outcome. There is no fixed-removal-sector selection.
Completeness is required for all 96 attempts and 768 injected photons before
an accepted veto; interrupted prefixes remain explicitly incomplete.

The 64 swap candidates are genuinely evaluated through exact integer swap
deltas and each cost/mask is materialized and credited. This is not 64 separate
full scalar-cut calls, nor does it claim to be. The independent fixture checks
those deltas against scalar cuts. Canonical complement handling, first-tie
best-state retention, chain resets and strict current improvement are explicit.
No later best state is silently substituted for an earlier scored state.

### Allowance and temporal witnesses

Paid algorithm spans are disjoint from containing factory spans, sampling and
evidence IO. Factory residuals enter the B WALL grant once; the total factory
and native sampling records remain excluded. No observed CPU split is inferred
from the setup WALL scalar. The missing typed report is R1, not a second
allowance term that should be added.

P50 selection validates clock/work monotonicity, record association, balanced
packed masks and bounds. It chooses the largest chronological index satisfying
both charged CPU and charged WALL inequalities. It does not sort by cut or
reconstruct a witness from late overall-best fields. Only the selected existing
mask is unpacked and independently scored for evidence validation.

Both clocks are used for first-scan eligibility and custom online caching. The
custom search prepares its cached cut/mask before reading its checkpoint
clocks, keeps late units for audit and starts no new unit after its guard.
Each fixed classical mode receives the whole per-case grant independently;
there is no selected per-graph mode portfolio. Tier 1 is complete before its
fixed-mode decision; Tier 2 is reached only under the declared status order.
An earlier timely strict classical witness is not erased by a subsequent guard.
First failure/resource failure and incomplete B/control panels prevent an
accepted veto.

The old P50 `early_cap_inconclusive` is CPU-based. Its use as an additional
negative gate is conservative: it may force an otherwise no-winner comparison
to be inconclusive, while the independent selected-witness path still permits
an already timely negative witness. It must not be described as an observed
dual-clock guard expiry. This is a nonblocking interpretation clarification.

The allowance remains a favorable zero-optical-latency first-screen proxy. It
is not matched B/C CPU, an actual API-return deadline or matched QPU cost.
The conservative FAST supplement does not change those boundaries.

### Closure and resources

The two contracts use the same 15 relative execution inputs, covering all six
new files, the frozen design/card/addendum, P43/P50, their API card, AGENTS and
the dependency pins. The CLI checks the declared immutable helper/card hashes,
external source/binary/metadata pins, package versions and persistent Python
before scientific imports. The ten absolute external pins are checked by this
CLI, not by an unsupported claim that the runner hashes their absolute paths.
Scientific imports and native initialization are lazy with respect to module
import. Configuration readback is present for the actual native sampling path.

The source and contracts retain one worker, six thread-environment variables
at one, native configuration one, 60 CPU/90 WALL seconds, 32 MiB scientific
outputs, 4 MiB logs, reserve space, fixed work guards and zero retries. The
256 MiB logical memory plan is not presented as a hard RSS/affinity limit.
Exclusive output creation and retained failure prefixes are implemented.
All declared summary paths keep `positive_accepted` false.

### Qualification population and its exact interpretation

There are 27 explicit registered test items, including deterministic rational
two-photon laws, collision/repair behavior, equal-loading cancellation, the
eta-zero identity, exact deltas/complement/quench behavior, scripted dual-clock
prefixes, control status precedence and complete/incomplete workflow counts.
Scripted main-flow tests use fake dependencies; their eight-photon placeholders
do not create an eight-photon native circuit or draw a DEV graph.

The native item plans exactly 183 Naive points: three fixed HOM points and
180 fixed four-mode/two-photon comparisons. It records returned observations
and errors before the final accuracy assertion. The portable provenance item
records the actual interpreter/native artifact without asserting the author's
Mac interpreter path. No production PCG draw, CC sample or DEV graph is in
the qualification population.

The qualification command intentionally runs the bounded 27-item batch without
`-x`. This is not a retry: failed items remain failed, and no parameter/point is
changed or rerun. A finite native accuracy mismatch can be asserted after all
registered native observations have been retained. The main's first-failure
stop is a separate rule. Documentation should state that distinction explicitly;
the lack of `-x` is not a blocker. Any qualification failure still blocks main.

Soft scientific-output capacity failures and process-level resource failures
can have different inconclusive status labels in this implementation. Both
preserve the prefix and prevent an accepted result. This is not evidence of
a successful resource-bound run; actual status must be reported after execution.

## Disposition and independent scope

Return the frozen source to its author for R1/R2's explicit provenance patch,
then review the changed records/fixtures/contracts before the separately
authorized tiny qualification. No further route, seed, device, point or budget
change is requested by this review. All other conclusions here are static
source checks, not measured passes.

This reviewer has not modified producer files, executed its source, contacted
the producer about an unfrozen review, read other reviewer drafts, or changed
the manuscript/QPU configuration. No positive optimization benefit, novelty,
held-out replication or hardware validation follows from this review.
