# P49 efficient classical control — prospective API

25-Nov-2026. New control only; no DEV graph or numerical result opened here.
Parent card: `research/P49_TRAINED_SPECTRAL_SOURCE.md`, ROOT `7b791bf`.

Module `research/P49_fast_classical.py` exports

```python
solve_balanced(adjacency, incumbent, *, seed, max_proposals,
               cpu_budget_seconds=None, wall_budget_seconds=None,
               incumbent_cost=None, vertex_priority=None)
json_safe_result(result)  # conversion AFTER the measured solve
```

The adjacency is symmetric nonnegative `int64`, zero diagonal, with conservative
overflow validation. The incumbent is a balanced distinct vertex subset. Its
cost, if supplied, is verified; this shared starting discovery is given free.
No optimum, optimal-state mask or target cut is an input.

For membership in the current subset, `ell = degree - 2*A[:, inside].sum(1)`.
Swapping inside `a` for outside `b` costs `ell[b]-ell[a]+2*A[a,b]`; update
`ell += 2*A[:,a]-2*A[:,b]`. The control combines annealing, vectorized full
cross-pair descent, perturbations of its best state and balanced restarts. Its
temperature schedule and randomness depend on counts/seed, never clock time.
Optional carried vertex priorities fix scan ties under relabeling.

Both CPU and wall clocks include validation, setup, search and in-memory compact
traces, but exclude JSON conversion or file writes. Checkpoints are emitted only
after a completed chunk/scan/restart. Work finishing after a deadline cannot
improve the returned pre-deadline incumbent. Return the eligible best subset/cut,
actual timings/overruns, proposal counters, stop reason, and arrays of completed
checkpoint times, best cuts and packed membership masks. Also retain the final
completed state for audit, even when it misses a deadline. No per-proposal I/O.

`max_proposals` limits evaluated swap deltas plus restart candidates as a safety
cap, not a CPU-equivalent price. Hitting this cap before a requested CPU allowance
ends makes a positive comparison INCONCLUSIVE. A wall safeguard ending before
the CPU allowance has the same limitation. The caller can conservatively grant
CPU allowance equal to the measured common-frontend plus B classical-training,
PIT/decoder/evaluation/selection **wall** time, excluding optical simulation and
per-query audit serialization. This convention must remain explicit.

Qualification will check cuts and all deltas by independent scalar edge sums on
N6/N10 fixtures, incremental swap sequences, valid monotone trace incumbents,
deadline-prefix selection and seed reproducibility at fixed proposal counts.
No timing threshold, DEV graph, photonic result or advantage claim is involved.
Code, tests and bounded-run contract will be frozen before numerical execution.
