# P50 from-raw classical control — API/algorithm freeze for review

25-Nov-2026. Implementation proposal under ROOT P50_EXECUTION_CARD.md
`f9689d2`. No source implementation, test execution or DEV graph generated yet.

```python
solve_from_raw(adjacency, *, seed, initialization="random",
               cpu_budget_seconds, max_proposals=100_000_000)
json_safe_result(result)  # serialization conversion AFTER measured compute
```

New module `research/P50_fast_from_scratch.py`, new independent tests
`tests/test_p50_fast_from_scratch.py`. Valid initialization is `random` or
`spectral`. Each mode is a SEPARATELY invoked, separately budgeted algorithm;
no free portfolio. There is NO incumbent/Cref/priority/marks/eigensystem input.
The caller supplies its frozen B-only wall-derived CPU allowance; the helper
does not estimate, select or enlarge this allowance.

CPU/perf clocks begin at API entry, before conversion/validation/features/RNGs.
Accept an even square raw numeric adjacency with exact nonnegative integer
weights, symmetric/zero-diagonal; validate before int64 casting and enforce
conservative overflow bounds. Generate OWN seeded priority/rank. Random mode
draws one balanced subset. Spectral mode constructs weighted L/dmax (zero if
dmax0), adds1e-3*diag(own iid uniform marks), computes its second eigenvector,
and rounds its topK with own priority. Signs give complementary balanced cuts;
no better-of-two selection or free spectral feature. Every preparation cost
and initial actual cut are timed. No candidate exists for free at time0.

Run complete vectorized K² best-pair descent BEFORE any anneal proposal, until
no strict improvement or a deadline/guard. Then alternate geometrically cooled
8N anneal epochs, best-pair descent, best-state perturbations and seeded random
restarts (one in four cycles); refinements start with descent again. Cached
integer ell/deltas use the independently checked P49 formulas. Do not call its
whole solver, which assumes a given-free incumbent and starts with annealing.

Only completed checkpoints count, timestamped after work/compact mask creation.
If initialization or a later batch completes after the CPU deadline, retain it
for audit but exclude it from the eligible prefix. `best_cut/best_subset` are
None if NO feasible candidate completed before the deadline. Return actual
CPU/wall/overrun, initial/overall-late best, counters, initial-scan/initialization
flags, and compact checkpoint times/cuts/packed masks. JSON and file writes are
outside measured solve. No sampler/backend timing is inferred here.

Guard count includes the first cut, restart candidates and evaluated deltas;
max_proposals>=1. If insufficient guard remains for a required full scan, stop
explicitly rather than starting annealing before that scan. Any such early
guard truncation, or missing eligible candidate, prevents accepting a positive.
Report cap-hit and blocked-scan separately; score counts are not CPU prices.

Qualification: independent scalar cuts/deltas on fixed small fixtures, swap
updates, fixed-count reproducibility using an effectively inactive synthetic
deadline, random/spectral preparation ownership, first-scan-before-annealing,
virtual-clock late initialization/batch exclusion, guard and invalid-input
cases. No elapsed-runtime performance assertions or DEV graph generation.
Implementation/tests/contract will be committed again before root review and
an explicitly authorized bounded qualification; this card alone permits no run.
