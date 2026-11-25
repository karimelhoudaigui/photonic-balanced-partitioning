# P68 joint graph/current covariance: exact proof checkpoint

25 November 2026. **Accept the scoped current-dependent extension.**
Positive optimizer CLAIM-042 remains OPEN.

ROOT's candidate was independently rederived in
`research/P68_current_covariance_rank_two_audit.md`. Its original bytes were
sealed at1f12a8a/SHA0c587b01...f264b after ROOT read all229 lines; the
author's unavailable worktree index was preserved. The original provenance
is in `reports/P68_STATIC_PROOF_PROVENANCE.json`.

A different agent reconstructed the stabilizer action, normalized Fock
overlaps, target tensor moments, boundary cases, conditional histories,
expected photon scope and D upper bound, without relying on the first
agent's verdict. Exact original review: original0c7fa52, integratedb3c8310,
`theory/P68_independent_current_covariance_review.md`, SHA256
`fe2cafd8ed2fd9b4cea81cf9bb847c121094b08a00345d951a9c2484c348a197`.
ROOT read its entire292-line argument. This is independent reconstruction
after seeing the proof, not blind discovery or physical replication.

ROOT made one explicit local clarification5904e6f: subsets outside the bad
set B and target set G are uphill; OTHER members of B have equal cost.
No bound or model changed. The separate exact-delta peer addendum30361da/
rootca0ee84, SHA256
`29b7990bbf8e7ec16434d8a2d59fbb993abe46e31bb271a9522f45b4c311b451`,
checks the current proof SHA256
**`8a4bd9cfd751f1e8fd3d55bf2a6325d90fa10f52ed49882c5b2a588ef8e78235`**
and retains **proved as written**. ROOT read the full addendum and rechecked
the source/target projection, PGF and all constants. Original versions remain
in Git. No empirical data was modified.

## Exact accepted implication

On P66's four-clique bad-warmstart family, a deterministic one-particle
unitary exactly covariant JOINTLY in the graph and current selected subset
commutes with the two independent matching-pair permutation stabilizers.
They leave a rank-two bright space per block. Only the TOTAL block-dark
photon number is preserved; separate clique-dark conservation is unnecessary
and would be false in this larger class.

For every current bad state, every realized allowed unitary has raw good-
target probability at most

```text
a'_L = L!/L^L
b'_L = min(1, (L+2)^2/16 * ((L+2)/(2L))^L)
p'_L = min(1, 2*a'_L*b'_L)
     <= e^3 L(L+2)^2 (2e)^(-L)/8.
```

At L=2 this gives p'=1, explicitly vacuous. Fixed-rank asymptotic decay
does not assert useful constants for every small instance. The target
bright PGF factorizes over the two clique Fock factors, not over individual
photons. The source's second bright mode is empty, giving exactly a',
without an extra rank-two factor.

The zero-temperature success bound is min(1,T*p') for T raw attempts.
Finite-temperature first exits retain the same uphill gap and conditional-
expectation restrictions as P66. Expected K/p' injected photons refers only
to an execution continuing until success, not a capped or aborted run.
Separately optimized independent D photons obey another upper bound
min(1,2L^(-L)); comparing two upper bounds gives no B/D advantage claim.

## Limits and continuation

Exact joint covariance must hold for EACH realized selected map. Covariance
in law, individually marked past counts/random vertex marks, nonunitary
source filters, alternative sources/readout and arbitrary current-history
functions are outside this theorem. A controller selecting among admissible
maps remains covered. The graph family and initial four-state trap are
explicit; typical graphs/starts and actual P65 annealing are not ruled out.
The elementary classical graph certificate remains available.

No novelty claim or new physical simulation follows. P69 is a separate
proposed rank-of-transport obstruction that may remove exact covariance;
both fresh derivations are still being written. The finite P66 diagnostic
is CODE ONLY pending source/contract review and qualification. Latest
executable regression remains1144PASS; subsequent integration is documents
only. Paper/main, held-out and QPU gates remain unchanged.
