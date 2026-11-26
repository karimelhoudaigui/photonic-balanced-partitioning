# P82a: exact-source review of the pre-execution clock addendum

26 November 2026. **Primary verdict: proved as written for closure of the
two identified contract blockers. No material blocker remains at this
card level.** This verdict concerns the corrected negative-only proxy
comparison, not the correctness of future source, a completed qualification,
a main authorization, matched B/C CPU cost or a hard-deadline API return.
ROOT must separately decide whether to commission implementation.

Only this review is written. No implementation, import, AST, test, RNG,
graph/seed derivation, numerical computation, benchmark, native probability,
DEV/P79 output, QPU or manuscript action occurred. All source checks are
text/hash reads. Earlier artifacts are unchanged.

## 1. Exact reviewed artifacts and provenance

All69 lines of `research/P82a_PREEXEC_CLOCK_ADDENDUM.md` were read at
clean `.local/p65-independent-audit` commit
`43218ab508beb84c46a8575c28411b34f8570a79`, SHA256
`1b548885d05fe6a42487c77b12ac00292ebd8bd379c4074e6ce3a49ceb93a8d4`.
Compared against the original147-line contract at
`4a90c0d9ce06329115b6c8182fd45c28397f0fab`, SHA256
`d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9`,
and the complete preceding246-line independent review at
`7e84262dbffee84571761153e99bc305b69db500`, SHA256
`74d061b397e46aeab1ad8bad554b3acd86bd22fcd2ba6dd10065ee90825b0233`.
The original card remains an archived source with its earlier defects;
the addendum explicitly supersedes those descriptions without erasing them.

The unchanged helper bytes were checked again, and their relevant raw
clock/cache passages were reread:

- P50 source SHA256
  `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86`;
- P43 source SHA256
  `b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777`.

ROOT supplied the review target and independently found the original
issues. This is an AFTER-SOURCE independent-agent exact-contract review,
not a blind derivation, runtime experiment or external certification.

## 2. M1 closed: literal dual-clock precedence

For each case the allowance remains G, reconstructed from B's paid WALL
ledger. Every classical mode separately receives its OWN WHOLE G, with
no division by the number of modes or pooling across anchors. The
adapter's CPU a_C and WALL a_W are both measured before mode-specific
work; neither is inferred from the other. A snapshot qualifies iff

    a_C+c_j<=G AND a_W+w_j<=G.

The non-strict comparisons have no extra tolerance, floor or post-outcome
expansion. The P50 CPU-budget argument max(0,G-a_C) controls its internal
run only; it is not a replacement for either eligibility inequality.
Thus a CPU-timely but wall-late winner cannot veto. Adapter costs cannot
be omitted or subtracted twice, and one anchor's time cannot subsidize
the other. Custom modes use exactly this same dual rule online.

This is the previously missing common-WALL restriction, with an additional
CPU cap against the SAME scalar. It still does not show C_CPU<=B_CPU:
B's factory CPU partition is unknown. Nor does it convert simulator
runtime into a QPU latency or equalize total physical preparation costs.
The addendum states these limitations directly. Its zero-optical-latency
comparison is an optimistic first-screen proxy for B, not a hardware result.

## 3. Archived P50 prefixes: the source supports the selected object

The pinned checkpoint source creates a complete sorted subset, cut snapshot
and independently packed mask BEFORE _clock(). The returned clocks follow
that ready candidate; the lists then retain that same mask and cut. Future
state updates do not mutate the packed historical bytes. Final NumPy trace
export represents these earlier objects, not newly optimized candidates.

The addendum now freezes the selector prospectively: validate associated
trace lengths and monotone finite nonnegative clocks, retain chronological
order, and choose the LARGEST index satisfying both inequalities. Monotone
clocks make the qualifying records a prefix. Selection is by chronology,
not by sorting cuts, inspecting late candidates or a favorable outcome.
The archived running-best value at that index is already available there.

The wrapper copies those prepared packed bytes and their stored cut.
Later unpacking/scalar checking may VALIDATE that selected witness; it
cannot generate a better mask or replace a disagreeing stored score.
The selected index, source hash, both adapter and solver clocks and both
totals are required evidence. A separate raw audit cannot upgrade clock
eligibility after the run. This is not late-prefix reconstruction from
overall_completed_best_*.

The source's has_eligible_result, comparison_acceptance_eligible,
early_wall_inconclusive=False and first-scan fields are not dual-clock
certificates. The addendum expressly prevents them from bypassing its
selector. A well-formed empty/no-qualifying trace is ineligible, while
malformed association, nonmonotone clocks or absent source/mask provenance
are first failure; no fallback to a late overall winner exists.

RAM readiness, trace archival, final array export and disk serialization
are distinct events. The mask exists before its clocks even though trace
append/export or evidence writing can finish later. Consequently the
claim is an archived timely discovery WITNESS, not that the full solver
API returned or delivered serialized output by G. The addendum makes
that boundary explicit instead of fabricating an observer disk timestamp.

## 4. First scan, guards and veto precedence

The non-veto/surviving eligibility check must locate the actual initial_scan
checkpoint and apply BOTH adapter-plus-solver sums. An old CPU-only scan
boolean cannot certify that condition. Likewise no code may infer adequate
dual-budget search merely from the old helper's CPU-based early-guard flag.
If a work-guard stop's clock adequacy cannot be established under the frozen
binding, a no-winner outcome must remain conservatively inconclusive.
This cannot be used to upgrade a limited search to successful coverage.

A valid earlier candidate can still be a strict negative witness even
when a later work guard stops, including a timely initialization before
the first full scan. The ordering remains: first source/resource failure
has precedence; otherwise test genuine dual-timely fixed-mode winners;
if there is no such winner, missing timely scans/early guards/ineligibility
remain inconclusive. CPU-only final-return flags cannot erase or invent
a witness in either direction.

All96 B attempts and all four normal Tier1 calls are required before an
accepted FAST veto. The SAME fixed mode must win strictly on EACH anchor.
Tier2 remains conditional on the original no-veto/eligibility ordering,
with unchanged whole per-mode allowances and10000-work guards. There is
no favorable per-graph portfolio. Custom modes prepare/cache their own
complete masks before recording eligibility, stop starting work after
either limit, and retain late completed units only as raw audit evidence.

## 5. M2 closed: explicit typed duration accounting

The helper gives a setup WALL duration, not its internal absolute endpoints
or setup CPU. The correction distinguishes three record types:

- OBSERVED_SPAN has actual outer CPU/WALL endpoints, durations and unique
  owner/event ID. A factory outer span is a containing record, not a
  wholesale paid contribution.
- REPORTED_DURATION retains the helper's scalar and its outer/source
  references, with unobserved endpoints and setup CPU explicitly None.
- DURATION_DIFF records outer WALL minus reported setup WALL, formula
  and record references. Its separate endpoints/allocated CPU remain None.
  It is prefix-plus-return overhead, not a contiguous measured prefix.

Finite0<=reported<=outer is mandatory; inconsistent subtraction fails
without clipping. The measured outer CPU is retained but not mixed with
the WALL scalar. r=0 uses NOT_CALLED and its genuinely zero factory work,
not an invented measurement interval.

The corrected G is the sum of disjoint directly paid WALL spans plus
each referenced factory residual ONCE. Direct paid spans lie outside
factory outer intervals and excluded sampling/IO spans; serial factory
outers are distinct. Their containing spans/reported children do not
also enter the paid sum. Unique owners and explicit references make
double counting inspectable without pretending every summand has observed
timestamps. Excluded setup/sample/import/graph/IO and whole-run/case
records remain separately retained. No old helper edit is required.

## 6. Prospective binding obligations and final disposition

The listed deterministic qualification cases exercise the actual changes:
CPU-only timely/dual-late candidates, earlier dual-eligible archived masks,
empty eligible prefixes, chronological ties, late first scans, malformed
clocks, custom online caching, duration references and no double counting.
They are prospective checks, not tests executed by this review. The final
source/spec must pin their exact fixture/engine populations and encode the
revised rules literally, including the conservative no-winner guard rule
where actual stop-clock association is unavailable.

The two documents together preserve the graphs, settings, seeds,96 shots,
768 modeled photons, work guards, resource caps, raw-output policy and
positive_accepted=false. The original contract is not retroactively called
correct. The addendum removes M1/M2 by narrowing the claimed comparison and
typing its evidence, without touching any experimental outcome.

There is no new material card-level blocker to ROOT's prospective CODE-ONLY
assignment. That is not approval of nonexistent/unreviewed implementation:
full code/test/spec/input closure, independent source audit, separately
authorized tiny qualification with raw-first review, then a separate main
decision remain necessary. No runtime eligibility, DEV rejection, positive
optimizer result, physical/QPU cost guarantee or manuscript update follows
from this static contract pass. Paper and QPU remain frozen.
