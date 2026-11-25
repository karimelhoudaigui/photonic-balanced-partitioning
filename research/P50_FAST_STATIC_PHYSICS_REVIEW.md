# P50 from-raw FAST: independent static review

2026-11-25. Target adaptive source commit
`5f6cce8d025fc1b438788619c2cbde2078d6a8fd`; ROOT copy commit
`c86fd63b79859b281dd69227f68c195656f93e8c` has identical checked bytes.

- research/P50_fast_from_scratch.py SHA256:
  `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86`.
- tests/test_p50_fast_from_scratch.py SHA256:
  `d70a3a37856312177c0c8c6f905a5504ff2cd776d70de2e08bf663a941381aa8`.

**Verdict: no blocking static defect found in the stated from-raw anytime
CPU-prefix comparator.** The coordinator reports qualification21 PASS in
19044e1; this receipt does not reproduce or independently certify that run.
I read the entire source, its corrective diff, API card and all21 fixtures.
No import, test, numerical benchmark, DEV graph or hardware call was executed.
This is independent of the helper author, within the same-team limitations;
I previously reviewed P49 FAST and P50's prospective physical cards.

## State, preparation and search

The API takes only raw A, seed, initialization, CPU allowance and proposal
guard. It cannot receive an incumbent, priority, marks or eigensystem. The
clock starts BEFORE validation/conversion and all owned initialization.
Finite integral symmetric nonnegative loop-free weights are checked before
int64 conversion; the conservative weight bound protects cut/degree/delta
arithmetic. Input A is not mutated. Own RNG generates priority and, for the
spectral variant, marks and a separately computed eigensystem/rounding.
The actual initial balanced cut is computed and paid; none is free at time0.

With ell=degree-2A x, the code implements

    Delta(a->b)=ell_b-ell_a+2A_ab,
    ell'=ell+2A[:,a]-2A[:,b].

Swapping corresponding inside/outside slots preserves balance and uniqueness;
cached integer costs and updates agree with direct edge accounting. Resetting
a known best incurs CPU/full-cost work even without a new proposal discovery.
Random restarts and perturbation intermediate candidates are paid and retained.

The FIRST operation after timely initialization is complete vectorized K^2
best-pair descent, repeated until no strict improvement or deadline/guard.
Only then is anneal setup performed. Anneal epochs, subsequent descent,
perturbations and one-in-four uniform restarts follow the declared algorithm.
An insufficient guard for any required full scan explicitly stops instead
of bypassing it for annealing. Work includes the initial cut, deltas and new
restart scores; it is a guard counter, not a matched quantum resource price.

## Online deadline snapshots and cost scopes

Every checkpoint creates a NEW dictionary and a sorted COPY of the current
best subset, packs its mask, then reads its timestamp. Thus a complete RAM
candidate exists before the clock used to determine eligibility. The saved
eligible_snapshot is replaced only by a timely checkpoint; later state
mutation or a late overall_snapshot cannot modify its subset or best cost.
No winner is reconstructed by unpacking final traces. Late initialization
has no eligible result; late scans do not improve an earlier eligible result.
At exact equality with the CPU allowance, the completed checkpoint is eligible
and stops further search. This matches the stated <= convention.

The export boundary separates online search from trace-array construction;
compute_cpu/wall include that export, and cpu_overrun retains it. Returned
eligibility is an anytime RAM prefix, not a claim that final trace/result
assembly, JSON or function return completed before the deadline. Final scalar
report construction follows the last measured clock; serialization/I/O are
outside solve. The timing convention explicitly disclaims a hard-return
guarantee. It must not be restated as one in a primary report.

Early proposal guard or blocked scan with unspent allowance makes comparison
ineligible. Missing eligible initialization is also ineligible. Callers must
use best_cut/best_subset and comparison_acceptance_eligible, never the late
overall_completed fields. A timely initial candidate with a later overdue
scan remains an initial-only anytime result, with the scan flags retained;
this is not a certificate that descent finished. Two initialization modes
are two separately budgeted algorithms, not a free portfolio. B-only allowance
construction, caller adapter costs and result use require the primary audit.

The fixtures cover exhaustive scalar deltas on small fixed graphs, update
sequences, paid spectral ownership, initial descent order, missing/late
initialization, late scans, online snapshot caching, guards and input bounds.
Synthetic clocks check semantics, not achieved throughput or solver quality.
No optimum or positive optimization result is proved by this source review.

Actual commands were read-only git-show/stat, complete sed source/test/card
reads, rg and shasum. No adaptive or ROOT file/raw/registry was changed;
this new receipt alone is committed in the replication worktree.
