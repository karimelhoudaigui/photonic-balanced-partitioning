# P82a typed-duration correction: independent delta review

26 November 2026. Static delta review only; no import, AST, collection, test,
RNG, graph, native/backend call, benchmark or scientific execution.

**VERDICT: the corrected frozen source closes R1 and R2 of the independent
892 review. No remaining material source blocker was found in this delta.**
This is a source-gate decision, not a measured qualification pass or a main
authorization. The separately authorized qualification remains the fixed
27-item batch with 183 registered two-photon native points.

## Exact scope

Base: `892ea9651d0f489f3dbdc79c6679567ac4735b75`.
Corrected producer commit: `94f80b94f75317524c202ce9ef5bf932d78ddc5e`,
`.local/p65-independent-audit`, observed clean.
The complete three-file diff was read: 121 insertions and 9 deletions.
No unchanged 3,024-line population was represented as a second full reading.
The earlier full review is `research/P82a_INDEPENDENT_SOURCE_REVIEW.md` at
`5f9bb4cc257de6a9c7c83e175d76eb56ca910d9e`, SHA-256
`eb3c3e1a69ba7e109c33e5cc296b865354ad2f480d63bdfe5f2363842f03b6c0`.

| Corrected file | SHA-256 |
|---|---|
| `research/P82a_split_scatter_veto.py` | `7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc` |
| `tests/test_p82a_split_scatter_veto.py` | `e70b74c2915632cf62677c80f40ebeea8e67c669116660096426101542794861` |
| `research/P82a_IMPLEMENTATION_POPULATION.md` | `9080adee7e67189731cdbcbd297c0b419748337025135f85cf7406bee5c1a4ba` |

## R1: factory operand provenance is now explicit

`Ledger.factory_residual()` now creates an unpaid `REPORTED_DURATION` record
with its own ledger ID, case owner, helper path, immutable P43 source hash,
reported WALL scalar and `outer_ref`. Setup CPU and all interval endpoints are
explicitly null. It retains this record before the paid difference.

`duration_difference()` now takes that record, checks its type/unpaid status,
case association and unknown fields, then validates the same finite nested
duration inequality as before. Its result resolves both `outer_ref` and
`reported_ref`. The B factory report also references the reported record and
the difference. The unchanged observed outer event retains the chain/step
context, so the reference chain identifies the attempt without fabricated
internal timestamps.

The added deterministic assertions check ID uniqueness, record kinds, source
references, null fields, case/outer association, matching scalar operands and
the reference chain from B factory reports. Rejection fixtures retain negative,
inconsistent and nonfinite values and add malformed typed records.
This supplies the missing explicit artifact; it does not reinterpret an old
untyped scalar as a retrospectively equivalent record.

## R2: FAST reported operand now resolves unambiguously

The control header now contains `reported_compute_duration`, an unpaid
`REPORTED_DURATION` with an explicit case/mode-derived ID, immutable P50
helper path/hash, both returned compute duration scalars and null endpoints.
The conservative difference's `reported_ref` points to that ID instead of a
literal field-name string. Its other references identify the observed outer
and observed direct-adapter operands in the same header.

The P50 reported record does not repeat an `outer_ref` field. This is sufficient
for this frozen population: one header owns the three identified operands and
its difference explicitly links all of them; the fixed case/mode calls make
the IDs unique. No ambiguity is created by omitting a redundant reverse link.
The strengthened scripted fixture checks all three resolutions, the helper
source, values, null endpoints and both difference formulas. A new direct
`outer_ref` inside that reported operand is not required to close R2.

Unlike the factory setup CPU, P50's helper-reported compute CPU is a known
duration scalar and remains present. Neither record invents an absolute
internal endpoint or turns a derived difference into an observed interval.

## Unchanged scientific and execution boundary

The added factory record is unpaid. `Ledger.grant()` and the paid difference
formula are unchanged, so the new record is not a second charge. Adding an
identifier advances later event IDs only; it adds no scientific clock read,
draw, score or optical point. The FAST correction changes record association,
not either conservative subtraction, the grant, the charged adapter, checkpoint
selection or solver budget. The new recording work is outside the originally
timed algorithm spans and does not create an extra allowance term.

The diff changes no graph, seed, compiler phase, split profile, native sampler,
repair law, candidate score, attempt count, photon count, comparison mode,
guard, tolerance, output cap, dependency pin or planned command. Fixture
assertions are strengthened inside existing items; the 27-item/183-point
population is unchanged. The execution spec and both runner contracts are
unchanged. The documentation now states accurately that the qualification is
one fixed batch without `-x`, while main has a first-failure rule and requires
separate authorization. A failed item remains a failure; this is not a retry.

No new positive-result claim follows. The zero-optical-latency screen remains
a favorable classical cost proxy rather than matched physical/QPU resources.
The manuscript, old negative results, immutable helpers and QPU state are
unchanged by this correction or review.

## Disposition

The explicit pre-data recording correction is accepted at the static source
gate. ROOT may now consider its separate authorization of the already bounded
qualification. Actual collection, assertions, native readbacks, artifacts and
resource/status outcomes still require observation and cannot be inferred from
this delta review. Main remains separately gated after qualification review.
