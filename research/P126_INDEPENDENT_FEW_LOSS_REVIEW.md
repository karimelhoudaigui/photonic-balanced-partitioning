# P126 — Independent fixed-few-loss proof review

2026-11-26. Reviewer: P66; non-author of P126, author of dependency P123.
Target: research/P126_FEW_LOSS_POSITIVE_SAMPLER_ROUTE.md, ALL 231 lines,
commit 194be199179e3e16c8da2d1fe5b93577d95a1451, SHA256
7dd13002498e0e582be85e7a7b8636cdac97425409b964cb1db10b70720f4736.
Own parent: d8654f2f4756ecd4021d1910f670ea02276fbde5.
Method: proof-audit, manual reconstruction; original bytes were not edited.

## Claim and primary verdict

For each FIXED nonnegative integer r0, a supplied rational nonnegative
m-by-K contraction A and a fresh collision-free K-photon source admit an
additive-TV sampler of every signal occupation with total K-r0,...,K,
and ONE aggregate FAIL for all lower totals, in polynomial worst-case bit
resources in the full encoded input and inverse error, under the stated primitives.
Collisions are retained. This is a count-law statement, not state simulation.

**Primary verdict: conditional on a named input.** The internal P126 reduction
passes as written under the accepted P123 rational permanent/conditional-transfer
interface, whose external leaf is Chen/Guo/Vigoda/Yang 2609.20717v2,
Theorem 1/Section 8.4 for zero/one permanents. I found no additional material gap.
The conditional label records that theorem dependency; it does not reopen it or
infer P126 from another reviewer's agreement. The old arbitrary-real unit-cost
weighted corollary is not sufficient and need not be used.

Read ROOT's reports/P123_ROOT_FINITE_BIT_CHECKPOINT.md completely. It accepts
the rational weighted interface via the exact binary-path gadget and self-reduction,
with bounded randomness, output bits and abort error. I did not independently
re-referee that external preprint here. My authorship of P123 is disclosed;
this is an independent reconstruction of P126's new reduction relative to that leaf.

## Dependency graph and obligation matrix

CF Fock source + passive vacuum dilation -> environmental Gram compression ->
positive proposal with bounded rejection -> top-moment mass approximation ->
non-oracular omission/selection -> capped approximate trials -> raw-TV guarantee.
The only non-elementary computational leaf is the named positive rational
counting/normalized-transfer interface. No experiment supports this proof.

| Obligation | Target locator | Result |
| --- | --- | --- |
| Physical p_N and all factorials | 20-43, Eq. (1) | passed |
| PSD contraction bound on L_r | 32-43, Eq. (2) | passed |
| q_N normalization and rejection | 47-62, Eq. (3) | passed |
| Top moments, inversion, B_r | 66-91, Eq. (4) | passed |
| Sector weights without a P_N oracle | 95-119, Eq. (5) | passed |
| Additive Rayleigh error through cancellation | 123-155, Eqs. (6)-(7) | passed |
| Capped work and global error | 159-190, Eq. (8) | passed |
| Rational weighted primitives, all m/N | 50, 138-155, 183-189 | named leaf |
| Boundary cases and resource scope | 195-225 | passed |
| Practical speed, novelty, optimizer/QPU | 227-231 | out of scope |

## Reconstruction of the physical law and proposal

Let b_i and e_i denote the signal and environment creation operators for source
column i. Expand product_i(b_i^dagger+e_i^dagger)|vac> by the surviving source
subset S. For signal occupation n, its coefficient is
per(A_(n,S))/sqrt(product_j n_j!). No source factorial occurs because the
initial occupied modes are distinct. Each environment vector is the unnormalized
creation product for Sbar. Tracing all environmental occupations contributes
per((E^dagger E)_(Tbar,Sbar)), including their own repeated-mode factorials.
Since H=I-A^T A is real symmetric, this gives Eq. (1), with no extra r! or D_r.

More strongly, let J map the normalized r-photon CF basis into Sym^r(C^K).
Then the complement-indexed L_r equals J^dagger Gamma_r(H) J. Diagonalizing
0<=H<=I makes every eigenvalue of Gamma_r(H) a product of r eigenvalues in
[0,1]. Thus 0<=L_r<=I. Bounding the separate environmental vector norms alone
would not prove this matrix inequality; the compression argument does.
The isometry is only a mathematical dilation: no square root of H is computed.

For each S, summing per(A_(n,S))^2/n! over all |n|=N gives per(G_(S,S)).
Hence the proposed subset mixture normalizes to Q_N and has density q_N/Q_N.
The contraction inequality gives p_N<=q_N pointwise. Multiplying that proposal
by (a^T L_r a)/(a^T a) yields exactly p_N(n)/Q_N, not p_N(n).
This distinction and the possibly nonphysical normalizer Q_N>1 are handled correctly.
The conditional positive-transfer primitive samples the normalized A_S law;
it must not repeatedly simulate physical survival of A_S.

## Mass selection and finite-trial coupling

The squared norm of the source with signal creation amplitudes multiplied by
sqrt(z) is per(H+zG). Its Fock number decomposition is the total-number PGF.
In per(I+tG), identity-selected indices force the corresponding permutation
points to be fixed, leaving each principal permanent exactly once. Therefore
M_l=E binom(N_signal,l), and coefficient extraction gives the signed inversion.
Using binom(l,N)binom(K,l)=binom(K,N)binom(K-N,l-N) proves
B_r=2^r binom(K,r). Each principal permanent is <=1 by the same CF contraction
norm argument, so relative theta errors imply the claimed absolute mass errors.

On the precomputation good event, max(0,e_r-Delta) lies between
max(0,P_N-2Delta) and P_N. The retained weights are genuine submasses.
A dropped sector has P_N<tau+2Delta; a retained sector loses <=2Delta.
The total omitted physical mass is <=s*tau+2s*Delta=epsilon/4, moved to FAIL.
This uses no exact P_N oracle and does not claim conditional accuracy in a
dropped sector. Invalid total weights/fallback branches are confined to the
explicit precomputation bad-event probability.

For retained r, P_N>=tau and Q_N<=D_r give acceptance >=tau/D_r.
The stated J_r makes the ideal cap-abort probability <=zeta; base-2 logarithms
only make that bound conservative. In the ideal iid rejection loop, conditioning
on any first-acceptance trial leaves the same p_N/P_N law. Finite capping adds
only an abort mass at FAIL, not an uncharged change in the accepted density.

If ||hat_a-a||<=delta||a||, the two normalized vectors differ by <=2delta:
insert hat_a/||a|| and use reverse triangle inequality. Since ||L_r||<=1,
the two Rayleigh values differ by <=4delta. Signed numerator cancellation
therefore requires no relative approximation of a near-zero p_N(n).
The rational computed quotient remains in [0,1] for every nonzero real hat_a.
Fresh per-query randomness gives the D_r*b failure union uniformly after
adaptive proposals; it is not conditioning the final output on all queries succeeding.

Conditioned on any good precomputation, subset-mixture TV is <=theta/(1-theta).
Add its normalized-transfer error, Rayleigh error, amplitude-failure union and
capped categorical/coin error to obtain Eq. (7). Couple successive kernels up
to first disagreement; at most J_r trials give zeta+J_r*e_trial. Sector mixing
needs the largest such bound, not their sum. Adding precomputation failure,
omission, rejection abort, trial coupling and selector error gives
epsilon/8+epsilon/4+epsilon/8+epsilon/8+epsilon/8=3epsilon/4.
The five displayed precision choices each contribute <=epsilon/(40*Jmax).

## Bit model, zero cases and limits

G and H are exact rationals of polynomial encoded length. Fixed-r permanents
of signed H, D_r-by-D_r matrix construction and rational Rayleigh arithmetic
have polynomial bit work, including denominators of all bounded-bit estimates.
Top minors and repeated-row amplitude matrices are nonnegative rational inputs
to the accepted weighted interface, even though H itself need not be nonnegative.
Each proposed occupation has total <=K and polynomial encoding; no outcome-space
enumeration or environment basis construction is used. Integer comparisons can
implement the cap/threshold choices without an ideal real-log oracle.

There are polynomially many principal queries and at most polynomially many
trial queries for fixed r0. Requested inverse accuracies are polynomial, with
the union/coin caps charged as stated. The positive primitive's exact support
test and finite nonnegative output/fallback conventions are part of its interface.
Gram per(G_(S,S)) vanishes exactly when some source column in S is zero:
otherwise its positive diagonal-product term already prevents zero.
Thus a sector with P_N>=tau cannot lose all usable proposal subsets on a good event.

The interface must allow m<N; the accepted matching construction does, unlike
a direct invocation limited to n<m in Anand's normalized theorem. Repeated signal
rows and full bunches cause no new signed counting query. N=0 uses the empty
signal permanent one; r=K<=r0 is then constant size. K=0 and A=0 have the direct
vacuum/FAIL branches stated in the source. Singular H/G and G=I cause no division
by zero or endless loop: true zero sectors receive zero selection weight.

Hand checks reconstructed: A=[1/2,1/2] gives (P0,P1,P2)=(5/8,1/4,1/8),
where deleting off-diagonal H terms gives a false P1. A=J2/2 gives
(1/2,0,1/2), although Q1=1. These confirm the sign/factor bookkeeping, not the
universal theorem by themselves. The contraction/combinatorial arguments above
are the universal justification.

No polynomial conclusion is supported for growing r0, nor for all-loss output
when K grows. No free rare-event conditioning, resolved environment, unknown gauge,
hidden optical memory, quantum-state sampler or hardware account is supplied.
The K physical photons/losses remain paid; internal N-photon proposals do not
reduce them. All classical preparation/counting/rejected trials are real work.

## Remaining obligation and provenance

There is no further internal proof correction requested. The strongest safe
statement is the stated fixed-r0 raw-count sampler under the accepted finite-bit
leaf and exact certified source/contraction promises. An implementation would
need separate code/contracts, independent source review and bounded validation;
none is authorized or claimed by this report. P127's bounded prior comparison
does not establish priority or novelty of this extension.

Full target and ROOT checkpoint were read before this verdict. Source identity
was checked by Git-blob SHA256; only text reads and metadata/Git operations were
used. No scientific imports/AST, numerical program, RNG, tests or raw-data access,
native backend, QPU or manuscript change. This is independent of P126's author,
not independent of my own P123 dependency. All previous negative results remain.
