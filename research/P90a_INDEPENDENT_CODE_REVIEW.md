# P90a independent exact-freeze code review

26 November 2026. **Verdict: no material source blocker found for a separately
authorized qualification of the frozen population.** This is a static review,
not an executed test, permission to run main, positive result or QPU gate.

## Exact revision and complete reading

Producer: `.local/p65-independent-audit`, clean commit
`82d7b63d35f2f0495df6ed9c0d86999b649c44ff`.
All seven files below were read completely: 3,851 lines. An initially truncated
combined contract/population output was replaced with complete bounded rereads.
No completeness claim relies on that truncated output.

| File | Lines | SHA-256 |
|---|---:|---|
| `research/P90a_source_bound_nonflat_veto.py` | 1254 | `95fa65c6c04a0d48bb29c5d38b4bb1cac1cfdc22170191ee49a280f2995098e1` |
| `tests/test_p90a_source_bound_nonflat_veto.py` | 1592 | `9fba751e5bc2970e77e63a1d45a751c4a3e788f64b2f718fb7b26d8fee6dc9ec` |
| `research/P90a_execution_spec.json` | 71 | `87dda967c662b0507c364d216f2c1a937d6a83e8616b536b7a0330bd90be0e7f` |
| `research/P90a_IMPLEMENTATION_API.md` | 144 | `8c153fc538dd8b789239e25f814126e2e37c9a422778bed1bbd45b60a9645ca5` |
| `research/P90a_preflight_contract.json` | 154 | `16e8ee28db9a26215fb22a12df8dcb3941ac957bc2c76ce1606ee1e0d3bfdfd7` |
| `research/P90a_execution_contract.json` | 179 | `0ed33b3d86e25eaa2e946506c52dcc510c89b633eabb61d68da7ed4e2d58b707` |
| `research/P90a_IMPLEMENTATION_POPULATION.md` | 457 | `54e69aad02836d0e3f6c48de9b3cbbabd3f66117a20b9e3391ae92a0455b1e9f` |

The card14d8/review20986 and unchanged P90 design/exact review remain the
scientific authorities. Existing helper reviews were reused at their exact
pins; P43, dependency/instruction files, P50 API and literature context were
also read as text. No external source was browsed or novelty claim reaudited.

## Physical and causal implementation

The exact swap batch is inside-major/target-minor. `m_matrix` transposes it
to the declared target-row/source-column M. Its delta sign and `2*w_st`
correction match the scalar cut. The Hermitian symmetrization, spectral scale
and `expm(-iH/d)` implement the fixed initializer; no P93 surrogate, changed
centering or fitted angle has been introduced. Numerical failures retain the
observed matrices rather than orthogonalizing them or selecting a new circuit.

V exists before either port permutation and before the split coins. W is the
same labeled matrix under those permutations. Its Gram and occupied-frame
guard implement `[I;iW]/sqrt(2)`, with no flatness rejection. Conditional P43
sampling at the transferred columns gives the intended lossless raw law;
the omitted common `i^r` phase does not affect its PNR probabilities.

The source uses one serial sample from a new local immutable P43 factory for
nonempty R. It makes no Processor/remote call. Empty R is analytic but still
costs twelve modeled source photons. Counts are archived before fallback/
integer/dimension/total validation. Repair cannot hide a lost photon: sum r
is required before completion, then full counts sum to K. Deterministic
empty/full repair branches consume no repair permutation.

All removal cardinalities, collisions, monomial/null matrices and repeated
states remain. The compiler sees current graph costs, not an optimum/mask;
its actual 144 classical discoveries are recorded and credited as such.

## Actual pre-clock candidates and state credit

`CutBatch` stores actual signed-int64 cuts and uint32 canonical masks.
The production overflow guard is conservative for the fixed graph domain.
`ScoreBook.batch` validates all entries, computes the first minimum and updates
global/chain/compiler bests before the owning span ends. Crediting that first
minimum is equivalent to chronological credit of all materialized candidates;
the count and complete arrays still include every duplicate/rejected score.

`ScalarEvent`/`BatchEvent` defer only audit-dictionary construction. Their flush
does not call a scorer, derive a new candidate, reselect a best or synthesize a
missing mask. The dedicated scripted fixture inspects arrays and min/sequence
before the end-clock read and forbids those operations during flushing.

Resets, current, own-chain scored best, endpoint best, compiler-only best and
global paid best remain distinct. Compiler candidates never update current.
Only the capped proposal quench can strictly improve it; ties keep the prior
state. Scan caps do not become local-minimum certificates.

## Grant, FAST and timing interpretation

Direct paid B spans are outside factory/sample/IO intervals. Factory observed,
reported and derived records have unique IDs and both operand links. Reported
setup WALL and residual CPU/endpoints remain unknown where unobserved; the
containing outer CPU is retained separately. No WALL-to-CPU allocation or
negative-gap clipping occurs, and reports are not paid a second time.

Each of four ordered FAST calls owns its raw copy, role and whole case grant.
P50 receives no B incumbent, priority, feature/cache or sample. Returned clock
operands and the full compact trace are preserved before gap/trace validation.
The wrapper charges both derived entry/return gaps conservatively and selects
the last existing dual-timely mask. It validates only that selected witness's
scalar cut. CPU-only returned bests and stop flags cannot replace this test.

First-scan timeliness and early guard adequacy are separate. Any inadequate
normal panel is inconclusive; any failed strict comparison in a fully adequate
panel yields NO_POSITIVE_SIGNAL. Passing all four yields only FOLLOWUP_REQUIRED.
Every summary, including capacity fallbacks, keeps positive_accepted false.
Exceptions/resources precede panel interpretation and stop subsequent work.

This reconstructs a favorable zero-optical-latency WALL-derived proxy, not
matched B/C CPU, a hard API-return deadline or total hardware cost. Derived
gap endpoints and factory CPU allocations genuinely remain unknown.

## Bounded evidence and launch contract

One complete column-array trace per control retains all stages, masks and
clocks, without trace duplication in summaries. The reviewed immutable P50
work/epoch/chunk structure supports the declared bound31254<40000; a guard
does not silently trim exported data. The 64/256 MiB amounts remain plans,
not measured RSS or native-allocation certificates.

Production `EvidenceWriter` reserves capacity before ordinary writes, enforces
32 MiB total and 4 MiB per object, and precomputes final sizes before writing.
Oversized final objects use explicit inconclusive fallbacks. Existing raw files
are not overwritten. `finish_attempted` is set before finalization; main does
not call finish again if workflow finalization already failed. Physical IO
failure may leave incomplete files; runner/raw validation must retain and
reject that prefix rather than promise an atomic eight-file completion.

The JUnit is separately bounded: the literal `-B -c` launcher sets soft AND
hard `RLIMIT_FSIZE=33554432` before importing pytest through runpy. It fixes
the argv, legacy JUnit properties, no cache and no outcome filter. The native
observations precede assertions. This is a per-file XML limit, not production
JSON reserve enforcement or an aggregate temporary-file/RSS claim.

The project closure has exactly18 unique regular nonsymlink files and matches
spec/qualification/main in the same order. Both contracts copy all18 critical
external pins exactly. Their actual hashes and all immutable hashes matched;
these hashes were read without importing a package. Main checks them before
scientific imports and then checks actual loaded critical module identities.
Qualification deliberately uses portable observed identities rather than the
Mac-specific CLI interpreter/binary guard.

Both fresh output parents were absent at review. All declared results are
strict descendants, nonreserved and outside the input closure, matching the
installed v2 runner's path rules. The planned inherited plugin/thread variables
must be applied by the eventual launch; this review has not observed them in
a running child. No conftest or alternate pytest configuration file was found;
the pinned pyproject supplies the project configuration.

## Exact qualification and what it cannot prove

The test file has30 test functions: one parameterized population of254 and
29 ordinary items, giving283 planned items. All254 literal IDs are unique
and match the inventory in exact order. Manual enumeration rules give
3 HOM +60 flat F4 +191 nonempty toy points, max4 receiving modes/photons;
vacuum is analytic. No collection or generator was executed for this review.

Independent Fraction-pair permanents retain complex phases and output
factorials; distinguishable routes and group convolution are separate laws.
All16 toy R and uniform fills are included, giving -5/192 versus D and exact
group2 equality. That toy cannot pass its group2 advantage gate. Flat tests
explicitly avoid asserting equality of the joint(R,Y) or quench-history laws.

The numeric compiler test is a tiny 2x2 closed-form Pauli comparison. Full-size
workflow tests use scripted adjacency, scores, matrices, sampler, clocks and
seed hooks; production hash/RNG/scorer/compiler/native hooks are forbidden.
They exercise96 attempts/1152 modeled photons and four calls without a real
K12 optical matrix, graph generator, P43 factory or P50 solver replay.

Native fixture setup, each point, the final test and teardown archive current
environment/configuration readbacks. Returned amplitudes, zeros, provenance
and exception representations precede numeric/thread/version assertions. A
passing exit code alone is insufficient: all283 items,254 observations and
their properties/caps/provenance still require inspection after raw seal.

A pass would not qualify a K12 Clifford output distribution, full Born law,
TV error, growing-sector benefit, held-out replication, matched total resource
advantage, novelty or Lucy input/PNR/loss capability. Main remains separately
authorized and all D/species/feature/control/held-out/hardware followups remain
NOT_RUN. Even a future FOLLOWUP_REQUIRED is not positive research acceptance.

Review provenance: separate static reader of the exact frozen files and input
bindings, with no producer edits or delegation. Only text reads, metadata
counts/comparisons, file hashes/statistics and isolated report/Git operations
were used. No import, AST/bytecode pass, collection, test, role/seed evaluation,
RNG, graph, scientific numeric/native query, runner, validator, CI push, B-data
interpretation, QPU or manuscript action occurred. No experiment was run.
