# P69 accepted: a low-rank optical transport obstruction

25 November 2026. **Accept the exact scoped theorem after independent
reconstruction and exact-hash review.** Positive optimizer CLAIM-042 remains
OPEN; novelty is not established.

Author original frozen atf7f802f/SHA0dc37fe3...17e177. ROOT's single local
clarification4832130 explicitly excludes equal-cost bad states from the
uphill set. Current `research/P69_low_rank_transport_obstruction.md` SHA256:
**`37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`**.
ROOT read all414 original lines, the clarification and current argument.
The author's unavailable worktree index was preserved; exact original bytes
and copy provenance are retained in `reports/P69_STATIC_PROOF_PROVENANCE.json`.

A different agent froze a428-line rederivation BEFORE reading the author:
originale5477a74/root85a29b2,
`theory/P69_independent_low_rank_transport.md`, SHA256
`fb4f7f828bcba0ad644971ba8851c219599dc73a20d45071d7f63bddc3a2b620`.
Its later315-line exact-hash review, original1e2e69d7/root808d8ea,
`theory/P69_AUTHOR_EXACT_HASH_REVIEW.md`, SHA256
`5acd021641ed586f7916d6f3199749121236d0e65bb2346ca00deb85bd04511f`,
concludes **proved as written**, without correction. ROOT read both complete
files and independently checked the crucial algebra. Both agents received
ROOT's candidate formulas and suggested route: independent derivation/audit,
not independent discovery. No numerical experiment or external theorem leaf
is a premise; Gaussian moments and permanent identities are proved internally.

## Accepted optical theorem

For an integer L>=2, split4L vertex modes into two blocks of2L. The source has L
distinct singly occupied modes in each block; the two target states have
one photon in every mode of one whole block. For ANY net passive unitary
whose cross-block rank is at most integer r, define, for1<=r<=2L,

```text
a(L,r) = min(1, r(r+1)...(r+L-1)/L^L)
b(L,r) = ((L+r)/(2r))^r ((L+r)/(2L))^L   if r<L
         1                                if r>=L
p(L,r) = min(1, 2 a(L,r) b(L,r)).
```

The raw probability of either full-block CF target is at most p(L,r).
For r=0 it is exactly zero. Collisions and all other outputs remain in the
normalization. Source preparation, rerouting, filters or conditioning cannot
be inserted without changing the model and accounting for their resources.

Unitarity forces equal cross-block ranks and intertwines DIFFERENT input
and output dark projectors. Source/target supports then give a two-sided
amplitude bound. A normalized source projection permanent is bounded using
an auxiliary complex-Gaussian identity and AM-GM. The full-CF target has
PGF `per(I+sP)<= (1-s)^(-r)`, yielding b by Chernoff. These auxiliary Gaussian
integrals do not claim a classical sampler for the full optical law.

For fixed r, p is bounded by a polynomial in L times(2e)^(-L). More generally
for any fixed0<alpha<1, r<=alpha*L gives

```text
p(L,r) <= min(1, 2 exp(-L I(alpha)))
I(alpha) = (1+alpha)log2 - (1+alpha)log(1+alpha) + alpha log(alpha) > 0.
```

For positive r=o(L), the stronger combined estimate is
`p<=exp[-L log(2e)+o(L)]`. These are bounds, not achievable rates.

## Mechanism and graph consequences

On P66's explicit four-clique shared-warmstart family (including connected
weighted graphs), only the two targets improve the cut. Thus a zero-
temperature collision-counted optical update has success<=T*p after T raw
attempts, uniformly over arbitrary marked histories and random choices of
U, provided EACH realized NET unitary respects the same physical rank bound.
Unlike P66/P68, exact covariance or fixed dark spaces across attempts is
unnecessary. Finite-beta exits require the stated gap/expectation terms;
actual P65 annealing and generic starts are not excluded.

Ranks of coherently composed cross blocks are subadditive. A sequence of
rank-one cross layers with total count below alpha*L is therefore subject
to the bound; arbitrary block-local unitaries can be interleaved. A parallel
layer with many independent cross couplers can have large rank, so this is
not an unrestricted physical circuit-depth lower bound.

For a single Cayley transform of ANY Hermitian H, Schur elimination gives
`rank(U_AB)<=rank(H_AB)`, with equality at nonzero t. Even arbitrary within-
block corrections/current potentials cannot remove a rank-one bottleneck
of that resolvent. A generic exponential `exp(itH)` can have higher cross
rank than H: the explicit two-by-two-block example in the proof has
`det(U_AB)=-t^4 (x1-x2)(y1-y2)/12+O(t^5)`. ROOT and the peer checked this
sign by hand. The Cayley corollary cannot be transferred to arbitrary
Hamiltonian time evolution.

Independent D particles have another bound `min(1,2(r/L)^L)` from trace and
AM-GM; comparing upper bounds gives no B/D ordering. The graph family is
classically easy by the heavy-clique/six-union certificate. This theorem
neither proves balanced partitioning hard nor establishes a universal
photonic impossibility, actual hardware resource bound or novel priority.

## Remaining work

P70 separately isolates a possible explicit bosonic transport enhancement,
with decisive classical and unrestricted-D falsifiers; its independent
derivation is pending. P66's exact finite diagnostic has passed its nine
tiny qualification fixtures at88a0573/rawdcb3aba (27.86s pytest,28.553662s
runner). Main has NOT run; independent static checker review is pending.
Latest combined executable regression1144PASS remains applicable because
all root changes since it are proof/review/state documents. No paper/main,
held-out or QPU change follows from the accepted obstruction.
