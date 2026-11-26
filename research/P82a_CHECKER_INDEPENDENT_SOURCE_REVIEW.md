# P82a independent checker: pre-execution source review

26 November 2026. **Verdict: no material source blocker found for the fixed
21-item synthetic qualification.** This is a static source-gate review,
not a qualification pass or authorization of the recorded-data main.
The latter still requires its separately reviewed postseal input binding.

## Exact reviewed source and coverage

Checker freeze: `34c9513072d385373805215dba6679ffb5686ab9`, clean worktree
`.local/p66-dark-barrier`. All six newly frozen files were read completely:
1,638 lines. No primary B result, manifest, log or experiment output was
opened, including after the primary execution became possible.

| File | Lines | SHA-256 |
|---|---:|---|
| `research/P82a_independent_raw_audit.py` | 1146 | `f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529` |
| `tests/test_p82a_independent_raw_audit.py` | 280 | `7dc3dfabbe78d9e515098d6eb91cc0446cbe588ed92e0ab103c2fce4b59b84c6` |
| `research/P82a_independent_audit_spec.json` | 51 | `6fd8c3639aa8bc2c4db407b15d3124d4289a585e507992ab6f07a45be9db8fc9` |
| `research/P82a_independent_audit_preflight_contract.json` | 21 | `c048b2f3e926d512e67fcbef8e0d0518f5b851a3d0364f4751d65fa42f6ec660` |
| `research/P82a_independent_audit_main_TEMPLATE.json` | 22 | `b3696e6f6bcd8ed25f97d8f3c37286acef788dc8f369877544375b74e11edc7a` |
| `research/P82a_INDEPENDENT_AUDIT_BINDING.md` | 118 | `3f531b50e9a58039537efeca263a6fe78bf4a14e7fcefd8da40bd7db36777406` |

The reviewed producer authority remains `94f80b94`, source SHA-256
`7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc`.
Relevant emission/dependency methods of that already reviewed source were
revisited as text solely for format correspondence. No primary function
was imported or executed. This checker review does not repeat the prior
3,024-line producer review or claim a new producer qualification.

## Independent finite reconstruction

The checker imports standard-library modules only at module load. It imports
no P82a/P43/P50 algorithm function, Perceval or exqalibur. Its own scalar
unordered-edge sum checks every B score, all feasible masks and all control
candidate cuts without reusing the producer's delta arithmetic.

Mask balance/padding, rank-zero complement orientation, duplicate neighbors,
tie order, at-most-two warmstart scans and the one-scan best-scored quench
are reconstructed explicitly. A scan cap is not relabeled a local-optimum
certificate. Reset/current/chain-best/all-paid-best states are separately
checked; chronological score credit includes rejected and repeated neighbors.

Postseal-only replay reconstructs the frozen graphs, weights, priority/reset
orders, source/target/phase marks, integer split draws and repair streams.
It is mark/input reconstruction, not a second optimizer or native draw. The
request, observation and outcome streams retain all removal cardinalities,
raw count multiplicities and deterministic zero/full-repair branches.
The complete-case event count of 197 is consistent with three resets, 48
four-event attempts, a start and a case result. Complete counts require
96 requests/completions and 768 injected/completed modeled photons.

The F4 Fourier convention and Q/A/J calculation use independent Fraction
complex arithmetic. Fixed residual checks compare archived rounded features
with those references. H is reconstructed from the archived rounded J and
preceding archived phasors in the actual summation order; its zero test is
exact, not a tolerance-based substitution of a theoretical zero. The eta-zero
branch requires exact zero fields and unchanged initial roots. The assembled
W, Gram, flatness and occupied-frame guards use the predeclared absolute
`3e-12` tolerance with no relative or clock tolerance.

## Typed clocks and decision reconstruction

Factory reports resolve distinct observed, reported and derived records.
The checker verifies immutable helper references, unpaid report/outer status,
unknown setup CPU/endpoints, nonnegative un-clipped residuals and one-time
charging. Direct paid spans are checked for overlap against one another and
against containing factory/native spans. Unknown factory CPU is not inferred
from WALL. Grant summation follows the recorded paid order.

For FAST, the reported compute operand resolves in its header with both
observed operands. The whole entry-plus-return residual is derived separately
in CPU and WALL, with null endpoints, then charged conservatively to every
prefix. Direct selection is diagnostic. Binding selection is the latest
existing chronological checkpoint satisfying both charged inequalities.

Custom scores receive independent full cuts and their work-indexed cached
best lineage is checked at each checkpoint. The selected checkpoint already
contains its complete mask and cut. Private custom policies are deliberately
not rerun; their public recorded scores/cache/clocks are the asserted scope.

Decision reconstruction requires a same fixed mode strictly better than
B's all-paid best on both anchors. It preserves the fixed call order, four
normal FAST returns, Tier-2 branch population and NOT_RUN outcomes. Timely
negative witnesses precede no-winner eligibility rejection; missing scans and
early guards do not become evidence of B survival. Primary failure or a
noncompleted runner prefix prevents `FINITE_RECORDED_DATA_AUDIT_PASSED` and
cannot become an accepted veto. All audit outputs keep `positive_accepted`
false. Malformed partial data may additionally receive an audit error; that
is a consistency failure, not a negative physics or optimization result.

## Qualification and provenance gates

The 21 unparameterized test functions were read, including their literal
expected values and failure branches. They use hardcoded synthetic graphs,
integer/Fraction calculations, scripted tiny fields/counts/clocks and temporary
files. Manual checks confirm the toy cut/complement/tie fixtures, collision
mapping, exact F4 entry `(-1+i)/6`, `J01=5/18`, binomial identity and derived
ledger grant. No fixture contains a generated DEV graph, production seed
evaluation, valid MainReplay constructor, PCG object, native query or solver
replay. Tests of the authorization gate fail before the numerical import/
version boundary. This static reading is not a report that they pass.

The qualification contract binds 11 relative local inputs and its executing
interpreter command. Its population is unchanged by this review. Main's
larger TEMPLATE deliberately names future assembled producer/binding inputs;
its unbound state is rejected before main seeds, numerical imports and raw
paths. Successful postseal authorization is necessary before the checker can
instantiate the pinned NumPy/NetworkX reconstruction object.

The later binding must resolve the frozen checker hash, exact producer source/
spec/input closure, manifest, existing scientific paths, opaque byte sizes and
hashes. The checker validates relative nonsymlink paths, producer before/after
input hashes, declared result hashes, execution commit and runner caps. Missing
files on failed prefixes remain missing. The final runner contract must bind
the actual complete repeated input closure and its after-run hashes; the
TEMPLATE alone does not demonstrate that future binding. Output is fresh and
outside sealed scientific input directories.

## Reservations, resources and disposition

No material correction is requested before synthetic qualification. The
remaining main input binding is intentionally unresolved, not an implicit
permission to open primary data. Recheck only that opaque binding when it is
created; do not tune behavior or tolerances from data.

The checker limits are explicit: one worker, environment threads one,
30 CPU/60 WALL seconds, 32 MiB raw scientific input, per-object/row limits,
fixed trace/work bounds, 512 KiB audit outputs, 4 MiB logs and zero retries.
The 256 MiB memory figure is a logical plan, not hard RSS or affinity.
Observed resource outcomes still need the later runner receipt.

Compiler-before-R causality, IO exclusion and pre-clock snapshot preparation
are partly source-bound where no separate physical endpoints exist. This is
stated rather than fabricated. A recorded-data pass cannot certify a Born
law, distributional TV, physical photons, matched QPU cost, replication,
advantage or novelty. No outcome from the 96 adaptive samples is inferred.

Review provenance: independent source reviewer, separate from the checker
author, reading frozen code before any checker execution or B-data access.
Only text reads, hashes and isolated report/Git operations were performed.
No import, AST, bytecode compilation, collection, test, RNG/role evaluation,
graph generation, probability/native call, backend, QPU or manuscript edit
was performed. Producer and checker files remain unchanged by this review.
