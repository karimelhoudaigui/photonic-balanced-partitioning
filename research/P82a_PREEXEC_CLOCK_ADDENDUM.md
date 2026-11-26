# P82a pre-execution clock correction

26 November 2026. **Corrective addendum, before implementation or execution.** The original contract's CPU-only witness test did not bound classical WALL time. Its factory difference was also a derived duration, not an observed contiguous prefix interval. The rules below supersede those two descriptions; the original 147-line card is preserved.

Original: research/P82a_DEV_VETO_CONTRACT.md at commit 4a90c0d9ce06329115b6c8182fd45c28397f0fab, SHA-256 d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9. Parent design remains f7cb5d99fa35b6ab9e6ff60839f985d81ea87001 / c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723. This addendum changes no graph, seed, setting, shot count, work guard or resource cap.

## 1. Dual-clock witness definition

For a case let $G$ be its frozen, ledger-derived B classical WALL allowance. For each fixed classical mode measure adapter CPU $a_C$ and WALL $a_W$ from before its first mode-specific work until the solver API entry. The raw-graph solver starts its own CPU/WALL clocks at API entry, before its preparation. Both adapter durations must be nonnegative, finite and retained; neither is estimated from the other.

P50 may still receive its immutable CPU-budget argument $\max(0,G-a_C)$. That controls its internal execution only. It is NOT the witness eligibility rule. A checkpoint $j$ with solver-elapsed clocks $(c_j,w_j)$ qualifies only when
  \[
  a_C+c_j\le G\quad\hbox{AND}\quad a_W+w_j\le G.
  \]
Use the recorded values and exact non-strict comparisons, with no extra timing tolerance or post-outcome enlargement.

A qualifying candidate is an **archived timely RAM-prefix witness**: its complete cut, subset and packed mask were already computed before the checkpoint clocks were read. Archival/export can occur later. This is not a promise that the solver returned, serialized or delivered a result before $G$.

The two classical clocks are bounded by this common B-WALL-derived scalar proxy. This does not prove equality of B/C CPU usage, and does not imply that classical CPU is at most B's separately allocated classical CPU. B's factory CPU split is unknown. It also supplies no matched total physical/QPU cost comparison.

## 2. Exact immutable P50 source and chronological selection

Read as text: research/P50_fast_from_scratch.py, SHA-256 6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86. In checkpoint(), the source constructs the best-cut/subset snapshot and packed mask BEFORE _clock(); then it stores the two elapsed times and appends that same cut/mask to the trace. Later array export does not optimize or reconstruct a winner. This exact source supports the archived-prefix interpretation. The record is not claimed to have been written to disk at its timestamp.

For P50, the wrapper must:

1. Retain the original trace order. Validate equal record lengths, finite nonnegative clocks, nondecreasing CPU and WALL times, and matching cut/mask records.
2. Apply the dual-clock test to each chronological checkpoint. Choose the **largest qualifying index**, solely by index and clocks. With monotone clocks the eligible records form a prefix. Never sort checkpoints by cut or choose a cheaper later record.
3. Copy the archived cut and already prepared packed bytes at that index. Do not create a new cut, search/unpack later masks, or recover a candidate from overall_completed_best_* or another late best. Any later unpacking/scalar score check in this comparison adapter is evidence validation of the SELECTED pre-existing mask only; disagreement fails rather than replaces its stored score. A separately scoped raw audit may inspect all records, but cannot upgrade their clock eligibility.
4. Record selected index, both solver clocks, both adapter clocks, both sums, packed mask, stored cut, source hash and provenance as an archived RAM-prefix witness. No qualifying index means no eligible candidate.

P50's returned best_cut/best_subset, has_eligible_result, first-scan timing and comparison_acceptance_eligible are CPU-based fields, not dual-clock certificates. They remain raw evidence, but cannot bypass this test. In particular early_wall_inconclusive=False from that helper is not a wall-time guarantee. Missing/mismatched source hash, malformed trace association or absent pre-clock-mask provenance is INCONCLUSIVE_FIRST_FAILURE and stops the main. A well-formed trace with no qualifying index is an ineligible comparison under the original status ordering. There is no fallback to a late overall winner.

The first full-scan condition used for a NON-veto/surviving comparison is checked at the chronological initial_scan checkpoint under BOTH sums. A timely initialization may still be a valid negative witness. The original10000-work guards and status ordering remain; an ordinary guard stop cannot erase a valid earlier cheap candidate, while a missing timely scan/early guard without a winner remains inconclusive. All96 B attempts and the four normal Tier1 calls are still required before an accepted FAST veto; first failure/resource failure takes precedence.

Custom modes must prepare their best-cut/mask snapshot, then read both clocks and cache eligibility ONLINE with the same dual test. They stop starting work after either limit, and retain late completed units only for audit. The same fixed mode must supply an eligible witness on EACH anchor; no best-of-mode portfolio is introduced.

## 3. Factory subtraction is a duration difference

The immutable P43 helper, SHA-256 b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777, returns a backend-setup WALL duration from an internal clock. An outer caller measures the entire factory call, including work before that internal timer and overhead after its final reading. Therefore
  \[
  d_f=W_{\mathrm{factory,outer}}-W_{\mathrm{setup,reported}}
  \]
is a **PREFIX-PLUS-RETURN RESIDUAL DURATION**. Its two pieces need not be contiguous, and their endpoints are not observed separately.

The ledger must distinguish:

| Kind | Required fields and interpretation |
|---|---|
| OBSERVED_SPAN | Actual start/end CPU and WALL clocks, durations, owner/event ID; an outer factory span is retained as a containing span, not added wholesale to paid G. |
| REPORTED_DURATION | Helper's setup WALL scalar, helper/source reference and outer event ID; start/end endpoints UNKNOWN/None and setup CPU UNKNOWN/None. |
| DURATION_DIFF | Value d_f, explicit formula, references to outer and reported records; start/end endpoints UNKNOWN/None and allocated CPU UNKNOWN/None. Label as the prefix-plus-return residual, not a continuous observed prefix. |

Require finite $0\le W_{\mathrm{setup,reported}}\le W_{\mathrm{factory,outer}}$. Negative/inconsistent differences are first failure; no clipping or clock fabrication. Retain measured outer factory CPU, but do not subtract a WALL scalar from it or invent its setup/prefix allocation. For r=0 record NOT_CALLED with zero defined factory work, not a fictitious span.

The corrected allowance is
  \[
  G=\sum_{\ell\in\mathcal D}W_{\ell,\mathrm{direct,paid}}
      +\sum_{f\in\mathcal F}d_f.
  \]
Direct paid spans are pairwise disjoint and OUTSIDE every factory outer span and excluded sampling/IO span. Serial factory outer spans are distinct; each duration difference is included once. Thus direct intervals and derived overhead durations compose G without pretending that every summand has separate timestamps. No paid interval may also cover the outer factory call.

Keep the reported setup duration, observed native sample CPU/WALL, native imports/configuration, graph construction, full case/run clocks and evidence IO in their separate excluded/simulation ledger. The subtraction partitions duration accounting, not observed CPU or an invented physical timeline. Zero optical latency remains a deliberately favorable first-screen proxy for B, not QPU timing.

## 4. Required prospective checks and preserved boundary

The later tiny, deterministic qualification must add scripted-clock cases for CPU-timely/WALL-late candidates, a CPU-only returned winner with an earlier dual-timely archived witness, no dual-timely witness, ties selected by chronology rather than cost, a late first scan, malformed/nonmonotone trace clocks, and custom online caching. It must also check the DURATION_DIFF references/unknown endpoints/unknown CPU, outer-vs-reported validation and no double counting. These are future tests, not runs made here.

No timing benchmark, RNG, graph, probability query, native canary, source implementation or experiment was performed. Only this addendum is written. The147-line contract, frozen design and immutable helpers remain unchanged. Code/qualification/main remain unauthorized until ROOT and the separate reviewer accept this exact correction.
