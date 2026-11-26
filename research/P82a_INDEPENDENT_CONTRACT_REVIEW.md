# P82a: independent exact-contract review before implementation

26 November 2026. **Primary verdict: incomplete, with material clock and
factory-ledger blockers requiring a separately frozen pre-execution
clarification.** The original147-line contract is substantially more
specific than the P82 design and resolves several earlier obligations.
It is not yet a common-budget veto as written. No implementation, tiny
qualification or main is authorized by this review.

Only this review is written. No scientific import, AST, test, RNG, seed
derivation, graph, matrix numerics, probability/native call, benchmark,
QPU or manuscript action occurred. The new clock-addendum draft was NOT
read and its author was NOT contacted. Findings concern the original
frozen source, not presumed contents of an unseen correction.

## 1. Exact sources and independence

All147 lines of `research/P82a_DEV_VETO_CONTRACT.md` were read at clean
`.local/p65-independent-audit` commit
`4a90c0d9ce06329115b6c8182fd45c28397f0fab`, SHA256
`d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9`.
Compared against the complete145-line parent P82 source, commit
`f7cb5d99fa35b6ab9e6ff60839f985d81ea87001`, SHA256
`c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723`,
and this reviewer's prior `research/P82_INDEPENDENT_DESIGN_REVIEW.md`,
commit `ae900edcd6e8b0a1d67523cb44fc65057be0dd6c`, SHA256
`59b478c051bc825155e153be6de6aceded7d118b1ff1d3d4c885eca2dbbca342`.
Neither source is changed.

The actual P43 factory and its module boundary, and the entire P50 solver,
were inspected statically in their pinned local source:

- `research/P43_global_gain_probe.py`, SHA256
  `b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777`;
- `research/P50_fast_from_scratch.py`, SHA256
  `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86`.

This is an independent-agent AFTER-SOURCE contract audit. ROOT supplied
the audit questions and separately identified the clock issue; agreement
is not independent discovery or mathematical evidence by itself. All
conclusions below come from the literal contract and source, not outputs.

## 2. What the card now specifies correctly

The two NEW unplanted anchors, fixed graph/weight streams, no connectivity
filter/replacement, K8/n16 and fixed rho1/eta1/2/two sweeps are explicit.
The listed odds/probabilities agree algebraically with d4's centered profile.
Three resets times16 steps per anchor gives48 attempts per anchor and96
overall; eight modeled source photons per attempt gives768 if complete.
An r=0 branch still consumes its source attempt, and r=1..8 must retain
actual full receiving counts, not only supports or favorable sectors.

Compiler and marks precede observing R. The exact eta=0 branch explicitly
sets J/H to zero and preserves initial phases, so the earlier floating
near-zero/arg hazard is addressed in the contract. F4's literal roots
avoid using transcendental evaluations at exact quarter turns. Split and
repair rules, unused-stream recording and no native retry/fallback are
specified. These are source requirements, not qualified implementations.

Canonicalization by a fixed private rank makes Q(X)=Q(X^c). Q returns its
BEST scored state including the input; every scanned neighbor receives
paid-best credit. The chain-current, reset, chain-best and global-paid-best
policies are distinct. A raw r=8 complement is thus not promoted into a
new optical improvement through a differing complement quench. Seeds and
private preparations prevent gifting B features to classical controls.

Tier1 is a fixed mode-major panel: FAST_RANDOM then FAST_SPECTRAL, each
on ER and RR, and all four calls must return normally before a veto.
Tier2 runs only after no Tier1 veto and adequate Tier1 eligibility. A
winner is one fixed mode on BOTH anchors; no free per-graph portfolio is
created. Guard-limited absence of a winner is inconclusive. Every terminal
status keeps positive_accepted=false; no D/species or held-out run follows
automatically. This is a negative-only DEV screen, not a positive gate.

The actual listed custom modes are frontier, phase-hyperplane, continued
descent and multiswap. This review does not silently equate them to every
earlier shorthand baseline name (including sketch) or expand the portfolio.
If a future report calls a broader panel tested, it must supply that exact
mapping or explicitly defer the extra comparator. A valid single-mode
negative witness does not require inventing another mode.

## 3. Material blocker M1: WALL allowance versus CPU eligibility

Section5 defines G_case as B's disjoint paid WALL durations after excluding
native setup/sample work. Section6 grants every classical mode G_case
seconds of CPU, subtracts adapter_CPU, and accepts a cached prefix when
adapter_CPU+solver_CPU<=G_case. These are different resource measures.

Neither C_CPU<=G_case implies C_WALL<=G_case, nor is G_case a measurement
of B's paid CPU. Descheduling or waits can separate CPU from wall in
either run. Even with configured one native thread, CPU is not defined
to equal wall. A control could have C_CPU<=G_case but C_WALL>G_case and
still qualify in the original rule. It would not be a same-WALL witness;
nor is a same-CPU witness established because B's factory-prefix CPU is
explicitly unknown. Giving B zero optical latency does not fix that gap.

Before source is authored, select and freeze one defensible interpretation:

* A common paid-WALL veto can require BOTH adapter_WALL+checkpoint_WALL
  <=G_case and adapter_CPU+checkpoint_CPU<=G_case. The CPU cap then is
  an additional guard, not proof that C_CPU<=B_CPU. Timeliness must refer
  to the actual pre-existing candidate snapshot, with each adapter charge
  included once. This is still only the optimistic zero-optical-latency
  DEV implementation comparison, not matched total physical costs.
* A common-CPU veto instead needs an actually measured B CPU allowance
  and a justified factory CPU decomposition. The current P43 return value
  does not provide that decomposition. Do not infer it from wall durations.
* Keeping the original mixed-clock rule requires labeling the result an
  explicitly hybrid-clock heuristic screen. It cannot be reported as the
  same-budget B-favorable rejection requested in the parent design.

This choice cannot be made after outcomes. ROOT has requested a separate
pre-execution addendum; its unsealed content is not assumed to resolve M1.

## 4. Material blocker M2: a duration difference is not an observed span

P43.make_optical_sampler creates its local RNG and validates the source
BEFORE its internal setup_start clock. The returned setup duration then
includes imports, seeding, construction and setup up to its internal return
clock. The outer factory interval also contains function-entry prefix and
post-clock return overhead.

Consequently outer_total_wall-returned_setup_wall is a legitimate derived
duration residual, including prefix/return overhead, but the helper does
NOT return its internal absolute clock endpoints. The caller cannot invent
observed start/end timestamps for one contiguous paid-prefix interval.
This conflicts with the card's blanket statement that every paid component
is an observed nonoverlapping span reconstructible without a nested residual.

Safe binding: archive the observed outer endpoints and reported inner
duration; explicitly label the subtraction DURATION_DIFF with those record
references. Do not add both parent and residual to G_case. Check finite
0<=inner<=outer, retain unknown factory CPU as None, and distinguish an
observed timeline span from a derived accounting quantity. No reinterpreted
CPU ratio or fabricated internal timestamps are acceptable. P43 need not
and must not be edited to implement that description.

## 5. P50 prefix evidence: strong, but choose the actual cached object

The immutable solver starts CPU/wall before input validation, owns its raw
preparation and RNG, and stores an anytime eligible CPU snapshot. In its
checkpoint function it creates the sorted best subset, full snapshot and
packed mask BEFORE reading both clocks. It then appends each cut/mask and
timestamp to the trace. Final trace-array export is separately timed; it
does not reconstruct a winner from a late final candidate.

Thus there are two safe prospective binding options for a dual-clock rule:

1. Define an EX ANTE selector on the recorded checkpoint sequence, using
   adapter CPU/wall plus both checkpoint clocks, and select only an already
   created archived RAM candidate/mask. Reading that pre-existing snapshot
   is different from generating a new prefix candidate from the late best.
   This is an anytime discovery WITNESS, not a promise the whole API returned
   by a hard deadline. Log the chosen checkpoint index and both totals.
2. More conservatively, accept only the existing returned eligible CPU-cache
   snapshot if its additional wall criterion also passes. If an earlier
   timely snapshot cannot be recovered defensibly under the frozen selector,
   return inconclusive; never substitute overall_completed_best_subset.

The old helper is immutable. Any selector must be a separately frozen and
audited adapter rule, not source mutation or a clock override. A late score
cannot be laundered through an earlier timestamp. CPU/wall/adapter offset
fixtures must distinguish these cases explicitly.

A timely complete candidate, even from initialization, can give a valid
strictly lower cut before an eventual work guard. P50's broad
comparison_acceptance_eligible flag is false after an early work guard;
that must NOT erase a genuine timely negative witness. Conversely a late
overall winner or an eligible index with no complete mask is not a witness.
If no fixed winner exists, incomplete first scans/early guards remain
inconclusive. All96 B attempts and all four normal Tier1 returns remain
required, and first source/resource failure takes precedence as specified.

## 6. P43 reuse, native separation and portable fixtures

The actual helper has NO persistent-Mac-interpreter assertion, no remote
Processor and no module-level graph, seed draw, sampler or experimental
canary. Its top-level NetworkX/NumPy/SciPy imports can initialize libraries;
they must occur inside the later controlled import boundary with thread
environment set. Its main() is only called under __main__.

The bosonic factory calls Perceval's explicit seed function and creates a
Clifford2017Backend; the returned closure requests one sample, not a batch,
and returns fallback=false. The caller still must reject malformed counts
and exceptions and enforce/check native configuration1 before/after calls.
The helper itself does not authenticate pinned versions or set that native
thread cap, so the future binding must do so without weakening portability.

Qualification must NOT call the real P43 stochastic factory: constructing
it creates/seeds random streams even before its closure samples. Real
physics fixtures are the separately declared Naive amplitudes; full-size
workflow fixtures must use the declared scripted engine hooks. No main
K8 native source, generated DEV graph or Clifford canary belongs in them.
Executing-interpreter test imports and a main-only persistent CLI guard
avoid copying a Mac-only check into otherwise portable unit fixtures.

Both PCG64 role streams and explicit native seeds need their complete
literal tuple table in the later JSON spec, including exact case/arm/role
strings and all -1/index0 fields. Native seeding resets legacy globals,
not separately constructed explicit Generator streams. All potential seeds,
including r=0's unused native role, are checked once before graphs; a
collision stops without rehash/reseed. No seed was derived during this audit.

## 7. Qualification mathematics and remaining binding obligations

The K4/r2 witness is correct with its stated d2 odds1/2,3/2 and repeated
probabilities1/3,3/5. Hand algebra gives q0=16/225 and, for receiving
rectangle contrast+1, phase-dependent sector mean -4*cos(delta)/225.
Therefore mean(delta0)-mean(deltapi)=-8/225. The implementation must freeze
that direction of subtraction and the actual plus-plus one-edge labeling.
At0,pi/2,pi the four-mode receiving entries can be exact rational complex
numbers; no eight-photon matrix is needed to verify this identity.

The uniform-repair identity follows from
binom(K,h)binom(K-h,r-h)=binom(K,r)binom(r,h). It supports the all-r
eta=0 decoded law after independent uniform receiving marks, without
claiming equality of physical full-count laws/costs. The analytic zero
branch, complement canonicalization and best-vs-last fixtures address the
earlier design review. Source must archive fixed Naive observations before
assertions, preserve repr/exception information on nonfinite failure, and
never silently drop zero probabilities.

The prospective source/tests/spec must still pin exact pytest-item and
native-query populations (the card specifies shapes, not their final count),
seed-role literals, engine-hook boundaries, timer ownership and full v2
input closure. Runtime W/isometry/flatness guards are finite tolerances,
not many-photon TV certification. Qualification, raw review and main require
their distinct ROOT decisions after full source/binding review.

The32MiB uncompressed scientific cap,1MiB summary/failure reserve,4MiB
logs, CPU60/wall90, one worker, environment/native1 and logical256MiB PLAN
are prospective limits, not measured resource guarantees. Partial B/control
panels cannot become negative evidence by substituting zeros for missing
events. No guards, graphs, seeds, caps or algorithms may be retuned after
outcomes. Every raw directory is sealed before interpretation. No future
P82a implementation/binding was read; its correctness is not assumed here.

## 8. Final decision on the ORIGINAL card

Keep the explicit negative-only algorithm/population/controller policy.
Block author implementation/main on M1/M2 until the original is supplemented
by a separately frozen common-clock/accounting rule and that rule is audited.
Do not overwrite or silently reinterpret this147-line artifact. The next
review is of that addendum and then actual source, not an experiment now.
No passed DEV panel, interference advantage, D victory, hardware feasibility
or paper revision is established. Paper and QPU remain frozen.
