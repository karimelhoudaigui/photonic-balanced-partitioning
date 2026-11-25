# P49 FAST control: exact-source static review

2026-11-25. Target adaptive commit
`0bc492e2442e9b5146fa52e275ed058dbfa9832e`, parent
`9765ff9091610bce2889ade91603f89b8f870907`.
`research/P49_fast_classical.py` SHA256:
`018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff`.
`tests/test_p49_fast_classical.py` SHA256:
`50bb0c50234934260ccd88cf065dd9752b959a7f447f81fda1a63c132f437621`.
Both inspected files match the commit (scoped working diff empty).

Verdict: **statically consistent, conditional on the named 15-test
qualification and correct caller integration**. No blocking algebraic or
late-credit defect was found. No qualification, runtime benchmark, DEV
graph, primary P49 code or numerical experiment was executed/read here.
This is review independent of the FAST author, within same-team/model
limitations, not a new performance or optimality result.

## State, deltas and finite arithmetic

The int64 symmetric nonnegative loop-free graph and balanced unique subset
validation are appropriate. The conservative max-weight bound protects
degree sums, cut sums and signed updates from int64 overflow. For
x=1_inside, ell=degree-2Ax and cut C=x^T L x,

    C(x-e_a+e_b)-C(x)=ell_b-ell_a+2A_ab,
    ell' =ell+2A[:,a]-2A[:,b].

The scalar/vectorized formulas and swap updates implement these identities.
Replacing the corresponding inside/outside slots exchanges one vertex
each way, preserving balance, uniqueness and complementarity. Perturbations
choose distinct inside/outside positions, so their successive swaps are
valid; every intermediate improvement is retained and charged. Resets and
uniform restarts rebuild the exact state. Re-sorting after every accepted
swap is not needed for correctness or carried-label covariance: slot
identities evolve covariantly under the same initial priority and RNG.

The work counter is delta evaluations plus full NEW restart costs. Known-
best resets recompute their cost/load without new discovery, but their CPU
and explicit full-cost counter remain charged. max_proposals is a safety
guard, not a matched quantum/cut price. Anneal chunks, complete K^2 scans,
restarts and perturbations all respect its remaining ceiling; no partial
scan is treated as an exhaustive local-minimum certificate. N2 and zero
weights have valid progress/temperature branches. No optimum/target is input.

## Deadline prefixes and the exact integration contract

CPU/wall clocks start BEFORE validation/setup. The supplied common incumbent
is legitimately given-free at time0; setup, input conversion inside the
function, trajectory and compact-trace creation are paid. Each checkpoint
packs its best subset and THEN timestamps the completed batch. A late
batch remains in the trace but is excluded by _eligible_prefix. Eligibility
requires BOTH active CPU/wall inequalities; the last eligible cumulative
best cannot include a discovery from a later batch. A batch that straddles
the deadline can lose credit for an earlier internal improvement, which
is conservative for the classical baseline and explicitly its completed-
batch convention, not a false early timestamp.

The caller MUST use returned **best_cut/best_subset** for comparisons.
overall_completed_best_cut/subset are audit fields and may include late
work; they must not be substituted. The recorded eligible checkpoint,
last checkpoint, overruns, stop reason and compact mask trace distinguish
the two. Final array conversion/unpacking is included in compute timings;
JSON conversion/serialization is a separate callable with no disk I/O
inside solve_balanced. The module does not emit per-candidate JSON.

cap_hit tracks the ceiling. early_cap_inconclusive is deliberately tied
to a PROVIDED CPU budget and whether the cap checkpoint finishes before
that allowance. early_wall_inconclusive likewise identifies a wall stop
while CPU remains. For the intended true-CPU comparison the caller must
provide cpu_budget_seconds, obey those flags and retain all overshoot data.
A False flag in fixed-count or wall-only mode is NOT certification that
a CPU envelope was exhausted. Passing a measured B postprocessing WALL
allowance as the classical CPU allowance is possible and conservative,
but must be labeled as such, not described as a CPU measurement of B.

vertex_priority is a distinct VALUE/RANK FOR EACH VERTEX, not the ordered
list of vertices. If the primary caller has order, construct rank with
rank[order]=arange(N) before calling. Under relabeling carry values by
vertex. The module's argsort/argsort produces exactly this interpretation;
its trajectory relabeling fixture uses that contract. Input graph int64
conversion must also be charged by the caller if done outside this function.
BLAS/thread limits are caller/runner responsibilities, not hard enforcement
supplied by this module.

## Fixtures and interpretation boundary

The 15 parametrized cases were read, not run: exhaustive balanced-state
integer cuts/deltas on fixed N6/10 fixtures, 100-step update checks,
fixed-count reproducibility and trace feasibility, carried priorities,
small caps, synthetic prefix clocks, late batches, early cap/wall flags,
input/cost validation and N2/zero graphs. The fixture RNG seeds are separate
from the P49 DEV population and no primary graph generator is imported.
Virtual clocks test bookkeeping, not hardware throughput. A passing finite
qualification would not prove solver quality or globally best use of CPU.

The algorithm is a legitimate local/annealing/multistart comparator, not
an exact classical optimizer. Its returned deadline-eligible incumbent
and paid costs can veto a practical claim; failure to improve would not
prove a bosonic advantage. A cap or wall guard truncating an unspent CPU
allowance is inconclusive for accepting a positive. Primary integration,
actual budget grants and performance remain to be reviewed separately.

Actual commands: read-only git-show/diff, shasum and full numbered source/
test reads, plus direct algebra and deadline-control reconstruction. No
NumPy import, test, timer benchmark, graph scoring or file modification in
the adaptive worktree occurred. This receipt alone is committed in the
isolated replication branch.
