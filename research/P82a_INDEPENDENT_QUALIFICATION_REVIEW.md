# P82a independent static qualification and physics review

**Outcome: audited, not executed.** No physical-law or fixture/API
blocker was found in the prescribed 27-item deterministic qualification.
One explicit provenance-schema reservation remains: the factory's
reported setup scalar is retained, but lacks the separately typed
`REPORTED_DURATION` identity and `reported_ref` required by the clock
addendum. Complete that record typing before execution, freeze the
change and review its exact delta. This is not an error in the current
grant arithmetic or a request to change a scientific setting.

This review authorizes no import, qualification, main, CI execution,
DEV result, manuscript change or QPU call. ROOT must separately decide
the next bounded slot after the source revision is reviewable. No test
or native observation has been produced by this audit.

## 1. Exact source and complete coverage

Reviewed producer revision: **`892ea9651d0f489f3dbdc79c6679567ac4735b75`**,
clean `.local/p65-independent-audit`. All six new files were read in full:

| Artifact | Lines | SHA256 |
| --- | ---: | --- |
| `research/P82a_split_scatter_veto.py` | 1328 | `c40d7ef84d9b8ceb833a28f91aaf2ff43bb5eaf3fffcad6e99447eeb72f54257` |
| `tests/test_p82a_split_scatter_veto.py` | 961 | `893fdb25598e407ce96f0e81b9691f9eb6f6352968d25e375a728ffe2f0fd0a3` |
| `research/P82a_execution_spec.json` | 74 | `8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838` |
| `research/P82a_IMPLEMENTATION_POPULATION.md` | 215 | `68b249e450ff2af1db16e41c3daa36b1ea91cf58bd5066eca1c286012e45e544` |
| `research/P82a_split_scatter_preflight_contract.json` | 243 | `209696de0b0170ff4099cdfd77b6acdaec3c4f78e04e86631047008c13517c0d` |
| `research/P82a_split_scatter_execution_contract.json` | 203 | `dca509b4fee65b652227fb395cfc982b4426a9c8ae0da05de75f825493cc5f20` |

Total coverage is **3024 lines**, including every fixture, hook, native
test, source function, spec field and runner command. Producer-file and
committed-blob hashes were independently checked for all six files.
An initially truncated combined contract read was completed with smaller
reads; no claim of full coverage relies on truncated output.

The frozen 145-line P82 design, 147-line DEV card, 69-line clock addendum
and 180-line exact clock-addendum review were also read completely.
The earlier 246-line contract review was only partially visible in an
initial combined read and is **not** claimed as fully audited here.
The original card's superseded CPU-only/prefix wording is interpreted
through the frozen addendum and prospective binding supplement.

Helper coverage: the full P43 factory and its preceding imports/setup
were read, plus its main guard; the P50 solver, clocks, checkpoint,
initialization, search, export and result-field implementation were read,
with the complete P50 API card. P43's unrelated optimization experiment
was not audited. Installed Clifford and Naive Python backends and the
native seed bridge were read completely; abstract circuit/input-state
and strong-backend setup passages were inspected. Binary internals and
all transitive package source files were not audited.

The applicable `AGENTS.md`, `mathbox:computation-audit` checklist,
proof-audit and self-proofreading instructions were used. Only this
review is written in isolated `.local/p81-exact-review`. There was no
direct contact with the producer or P66 auditor before this freeze.
After the complete 3024-line read, ROOT relayed that the other audit
also requested explicit factory report typing. That relayed point is
not presented as blinded independent confirmation.

## 2. Exact finite assertion and non-claims

Qualification selects 27 literal pytest nodes without parameterization.
There is one provenance item, 25 pure/scripted items and one native item.
The native population is exactly

    3 HOM outputs + 3 phases * 6 removed pairs * 10 occupations = 183.

Only two or four receiver modes and exactly two photons are sent to
Naive. No native stochastic sample, real K8 matrix/source, DEV graph,
DEV start, PCG construction or role-seed digest is required by these
fixtures. Main-size workflow tests are scripts, not physical runs.

The fixed test batch intentionally has no `-x`: each declared item is
part of one bounded qualification, not a retry. The native item stops
its query loop on its own first exception/nonfinite observation and
preserves preceding data. The main's separate first-failure stop policy
must not be confused with pytest's finite batch behavior. A qualification
failure cannot be called a DEV failure or repaired by an unregistered
rerun. A qualification pass does not authorize main.

Main remains only a prospective negative screen: two fixed unplanted
n16/K8 anchors, three resets and sixteen steps per anchor, 96 completed
attempts and 768 modeled source photons if complete. No outcome accepts
advantage. The same fixed classical mode must produce a timely strictly
cheaper candidate on both anchors; a per-graph portfolio is disallowed.
Reoptimized D/species, fresh seeds, relabeling, held-outs and matched
physical-resource validation remain later obligations.

## 3. Physical source, compiler and count reconstruction

The design's complete occupied columns are `[C;i W D]`, with diagonal
splitter factors and unitary flat W. Kept output rows force their
original input columns in the permanent. Therefore the complete law is

    P(R,y)=product_(i in R)p_i product_(i notin R)(1-p_i)
             * |per W[y,R]|^2 / product_a y_a!.

There is no missing factorial or collision-free denominator. A fixed R
has normalized receiving law by unitarity. The r0 branch is deterministic
zero receiving counts with all eight photons kept. Every other r has
one fresh serial P43 bosonic factory and one `sample()` call; the
bosonic helper creates one Clifford backend group. No parallel
`samples(count)`, remote Processor, fallback or count retry is used.

The code's literal F4 roots give the intended Fourier convention.
Its W has top/bottom signs, with graph phases in the second input half
before their final balanced mixing. Q uses plus ports first and minus
ports last, and `A=F diag(odds) F^dagger`; `J=Q|A|^2` has the required
rectangle contrast. Sequential phase updates maximize the corresponding
single-coordinate classical cosine objective, with exact floating-zero
retention and recorded H/before/after values. This feature is exposed
to a later paid classical hyperplane control, not claimed irreducibly
quantum.

Every phase compilation and its guards precede the split draws. No lucky
removed set enters compilation. The repeated exact profile matches the
spec; split comparisons use integers below rational denominators.
Runtime guards check W's Gram matrix, flat intensities and the occupied
frame isometry, without reorthogonalization. An isometry check is not
an empirical full-square unitary or many-photon TV certificate.

`decode_counts` retains bunching and zeros, checks integer dimension,
total and port partition, restores kept counts, and uniformly fills the
support deficit. Deterministic empty/full fills make no repair call.
It preserves full port counts, vertex counts, R and repair usage. This
is classical feasible decoding, not physical loss correction; malformed
counts fail instead of becoming simulated loss or another draw.

## 4. Independent small-physics fixtures and the exact null

The native reference is a separate two-by-two Fraction complex-pair
implementation: it explicitly sums the two permanent products and divides
by the occupation factorial. It calls neither the production compiler
nor primary probability logic. All six input pairs and all ten outputs
are retained at each of roots `1,i,-1`, including bunched and zero
events. HOM has the three 20/11/02 outputs with 1/2,0,1/2 probabilities.
The tolerance is absolute probability error `2e-12`, relative zero;
actual complex amplitudes are archived separately.

The raw r2 prequench mean fixture uses the correct d2 probabilities
1/3 and 3/5, each repeated twice. It sums every removed-pair weight,
every receiving occupation and every uniform repair. The one-edge
receiving graph consequently has phase0-minus-phasepi difference
`-8/225`, with the middle phase at the arithmetic mean. This is a raw
sector contribution; it is not a conditioned all-sector mean, a basin
advantage or a DEV graph result.

The eta0 compiler branch sets A analytically to rho times identity,
sets J/H exactly to zero and preserves initial phase roots. W is then
graph independent even though its unused recorded Q can change.
Independent uniform receiver-port marks imply uniform support labels
conditional on support size h; uniform completion gives any particular
r-subset probability

    binom(r,h)/[binom(K,h) binom(K-h,r-h)] = 1/binom(K,r).

Thus the graph-blind decoded null holds for every r under those mark
and equivariant-repair assumptions, regardless of the underlying count
law. Qualification's small exact identity enumeration supports its
implementation convention, not a new universal proof by sampling.
The separate ordered D-draw enumeration gives each K4 receiving pair
probability 1/6 and each receiver inclusion 1/2. The equal-loading r2
cancellation fixture retains conditional phase dependence and the
uniform-source average correctly.

## 5. Every scored candidate and the scripted workflows

The exact swap formula is
`ell_added-ell_removed+2 w_removed,added`, with
`ell_v=d_v-2 sum_(u in S)w_vu`. All 64 integer values and candidate
masks are materialized and recorded in rank order, then credited by
the scoreboard. These are actual evaluated exact deltas/costs, not 64
unevaluated guesses or 64 independently recomputed full cuts. A separate
scalar unordered-edge fixture checks the formula and masks.

The one-scan Q returns the best scored state including its input;
warmstart has at most two completed scans. A cap is not local-optimality
evidence. Canonical orientation by the fixed rank-zero vertex couples
global complements without another quench. Strict acceptance, first
discovery on ties, own reset/chain state and all-paid best remain distinct.
No chain is restarted for free at the global all-paid incumbent.

All main-sized workflow hooks were traced: fake graph construction,
fake compiler returning a string placeholder, fake sampler, scalar
scores, scans, private seed methods and scripted clocks. They never
instantiate NativeDependencies or call the real P43 factory. This is
essential because P43 itself creates a NumPy RNG before its internal
setup timer, even for its bosonic branch; mocking only the returned
sampler would have violated the qualification boundary. No actual
K8 circuit/source is built by these hooks.

The scripts cover the 96-attempt schedule, all r bins, collisions,
current refresh, every scored neighbor, four mode-major FAST returns,
fixed-mode versus mixed-mode witnesses, native fallback and control
exception precedence. Custom-mode guard and late-score scripts also
use only a literal fake RNG policy. No public hook signature mismatch
was found by text inspection. Parsing, collection and execution are
still unperformed; this is not a prediction of 27 actual passes.

## 6. Clocks, the conservative supplement and the remaining reservation

B's grant is the sum of disjoint paid WALL spans plus each factory
outer-minus-reported setup residual once. Factory/sample spans themselves
are excluded and retained, not added wholesale. CPU allocation for the
factory residual remains null; no WALL scalar is subtracted from CPU.
Invalid nesting fails without clipping. All are zero-optics first-screen
proxies, not measured QPU latency or equality of B/C total costs.

For P50, the pinned source constructs its complete cut/subset/mask before
the checkpoint clock. The wrapper keeps chronological trace order,
validates association, monotone clocks and masks, and chooses the latest
dual-timely archived index. It validates only the selected existing mask;
it never substitutes a later overall best. A timely initialization can
be a negative witness; missing timely full scans without a winner remain
inconclusive. Source exceptions override partial apparent vetoes.

The new prospective binding computes each CPU/WALL residual as observed
outer total minus direct adapter minus reported helper compute. Charging
all entry-plus-return overhead to every checkpoint is conservative.
Its operands/differences are finite nonnegative, endpoints remain null,
and the direct result remains diagnostic. Final witness selection uses
both charged CPU and WALL sums against unchanged G. No hard solver-return
deadline or equality with B's unknown CPU allocation is inferred.

**Reservation R1: complete the literal reported-duration record typing.**
At this frozen revision, `factory_report` retains `outer_ref`, the scalar
`backend_setup_wall` and `duration_difference_ref`. The derived ledger
record has its own id and outer ref but only embeds the reported scalar;
it has no `reported_ref`. There is no separate typed `REPORTED_DURATION`
record with an id, helper/source reference and explicit null unobserved
endpoints/CPU, as required by the addendum's table.

The scalar needed for G is present, and the current subtraction is
correct; this is not missing physical data or an invented measured
interval. Nevertheless the explicit record contract should be completed
before any run: give the reported scalar an identity and type, connect
the residual to it, preserve unknown endpoints/CPU, and make the scripted
ledger test check those relationships. No graph, seed, phase, shot,
budget, veto rule or scientific result should change. Review that exact
predata delta rather than retroactively call the current schema complete.

## 7. Provenance, input closure and resource boundaries

The two runner JSONs and spec repeat the same ordered 15 project inputs,
including both contracts and the population MD. Both commands/output
paths and result inventories are explicit. Qualification declares one
JUnit result; main declares eight scientific files. Runner output
directories must be fresh, with no automatic follow-on or retry.

The ten external file pins were independently hashed by this static
review and match the spec: five installed Python backend/seed files,
the exqalibur extension, two distribution METADATA files, pyvenv.cfg
and the physical Python binary. P43 and P50 hashes also match their
immutable pins. This is a read-time identity check, not execution
provenance or a hash closure over every loaded package file.

Main checks all ten external pins and all seven declared software
versions before scientific imports, enforces the persistent interpreter
and sets environment thread variables. It imports exqalibur first,
sets native configuration to one, reads back, then imports Perceval
and reads back again, with later case/final readbacks. The installed
Clifford API directly delegates one serial sample; Naive computes the
permanent divided by the Fock factorial square root.

Portable qualification intentionally uses its executing interpreter.
Its provenance fixture checks the two critical distribution versions
and five Python file hashes, and archives discovered native/interpreter
hashes and errors before assertions. It does not impose the workstation's
ten absolute pins or claim all-package-file closure. The native item
retains every observation, zero/tiny value, attempted-query count, first
exception repr, nonfinite repr and thread readback in JUnit properties
before any native value assertion; JSON NaN is not emitted.

The caps remain CPU60/WALL90, one worker, environment/native maximum1,
zero failed retries, 4MiB runner logs and 32MiB uncompressed scientific
output with 1MiB final reserve. The writer checks before append and
preserves earlier streams on cap failure, with compact failure/summary
records. Full traces are not duplicated in summaries. Logical256MiB is
a plan, not hard RSS. No timing run, affinity check, descendant-aggregate
CPU guarantee or actual runtime performance has been established here.

## 8. Disposition and next permitted review

The scientific and fixture logic is statically coherent at this exact
revision, subject to the explicitly bounded floating/native dependencies.
R1 is a small pre-execution provenance-schema completion, not a reason
to alter the prospective experiment. Freeze and review that correction
before ROOT decides one deterministic qualification. Even a future
qualification pass leaves main separately unauthorized and requires
inspection of the sealed observations and the actual runner status.

No current run manifest, JUnit result, native observation or DEV raw
result exists as evidence from this review. No simulation success,
strict classical veto, positive optimizer, hardware capability, novelty,
equal total-resource comparison or manuscript update is claimed.

Evidence operations were full text reads, path searches, line counts,
committed-blob/worktree and external `shasum -a 256`, commit metadata
and isolated document/Git operations only. No import, AST/bytecode,
collection, test, RNG, seed evaluation, generated graph, numerical
matrix/probability calculation, native query, QPU or manuscript action
was performed. The new review was self-proofread; author source changes
and author mathematical-token changes are both none.
