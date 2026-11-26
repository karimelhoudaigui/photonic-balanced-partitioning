# P123: independent finite-bit gadget and coarse-law proof review

26 November 2026. **PROVED AS WRITTEN for the epsilon-approximate full-K/
aggregate-FAIL interface, using the explicitly named0/1 finite-bit primary
primitive.** No material missing reduction was found. The scopes and two
non-exact-coin wording cautions below are essential to this verdict.
This is not an implementation, measured runtime or optimizer/hardware result.

Exact target read FULL278 lines: research/P123_RATIONAL_MATCHING_BRIDGE.md,
commitbfef3aa3514cd60ea3ae3d8676a2bdd1070284e0, SHA256
d1dd7ed244558c27ab743797c90a80b958c4593c9bd15eebf210bd4451150232.
Author status: I authored P124's external-source leaf, NOT P123's gadget or
probability proof. I reconstructed the gadget, latent law and error budget
before reading P125. Afterwards I read FULL197-line P125 at
ec5a835690f83afefe3eb88d43f607cb907bc310, SHA256
852c98a529ab51fe3f72050c3f4a6dc53598dc7e5570821a06865ca9b141d112,
as context only. Its independent probability reduction agrees; its primitive
bit guarantees were conditional. Neither actor agreement nor P124's reuse
is a second independent proof of the external62-page algorithm.

## Claim card, dependencies and disposition

Input is a SUPPLIED rational A>=0 of size m by K, with A^T A<=I and a
certified diagonal-phase gauge for the physical transfer T. A fresh known
CF source occupies K distinct inputs. The observed alphabet is full-K
signal counts INCLUDING collisions, or ONE FAIL for every smaller total.
For epsilon in(0,1), target TV<=epsilon with worst-case bit time, fair bits
and output length polynomial in m,K,total input encoding and1/epsilon.
Certification/search for A or its gauge is not supplied for free.

| Obligation | Disposition |
|---|---|
| Denominator clearing, fixed Gram/minor bit sizes | Passed |
| Binary path counts, zero/one weights, directed diagonal gadgets | Passed |
| Parsimonious cycle-cover bijection and0/1 size | Passed |
| Gram-permutation law and collision factorial | Passed |
| Legal adaptive self-reduction, fresh-count confidence | Passed |
| Expanded primitive output and capped rational coins | Passed under named primitive |
| Success mass, rare Z, complete TV budget | Passed |
| Coarse observation/adaptive/gauge scope | Passed with stated promises |
| Exact bounded-bit non-dyadic coins / full partial-loss law | Not claimed by the accepted interface |

Dependency graph: finite-bit Count01 -> integer gadget -> relative minor
estimates -> weighted matching -> positive Gram labels -> conditional
boson occupation. An independent normalizer estimate plus a finite Bernoulli
restores raw success mass. Polynomial-bit bookkeeping and conditional
couplings connect these arrows; no weighted real-arithmetic oracle remains.

## 1. Integer gadget reconstructed without a counting shortcut

Let D=product of all input denominators, P=DA and M=P^T P. Then log2 D<=B
for total encoding B; P entries have O(B) bits and M entries O(B+log(m+1)).
C=M/D^2 and Z=per(M)/D^(2K). Subsequent matrices are SUBMATRICES of M,
not quotients/products of previous conditional estimates.

For binary w=1b1...bs, the fresh vertices p,v0,u1,v1,...,us,vs have
N0=1 and Nk=2N_(k-1)+bk paths from p to vk. The two continuations from
v_(k-1) are its direct edge and its detour through uk; the optional p->vk
adds one path. Thus2+2s vertices realize exactly w paths, without parallel
edges. w=0 has no gadget; w=1 has only its one p->v0 path.

Replace original i->j by i->p,...,vs->j and give EVERY internal vertex
one self-loop. Original vertices receive NO extra self-loops. If the gadget
is entered, its entrance cannot loop; every reached vertex has its unique
incoming edge already occupied and must continue. Internal non-loop edges
are acyclic, so it reaches the sole exit. A second disjoint active path is
impossible: tracing it backward would require a second entrance/outgoing
edge at p. Any unused internal vertex must loop; a non-loop choice would
trace back to the original entrance. Hence all inactive completion is unique.

Contracting active paths gives exactly one outgoing and incoming selected
edge at EACH original vertex. Conversely each original cycle cover and one
of its w paths per selected edge determines one expanded cover. Diagonal
i->i gadgets simply close back to i; there is no free original-loop option.
Therefore per(H_M)=per(M), with NO cycle rotation, K! or unused-gadget factor.

Hand boundary checks: a1x1 matrix[w] gives w covers; [0] gives none; empty
minor gives1. For [[0,u],[v,0]] there are exactly uv covers, not2uv.
For a nonprincipal minor, identify its ordered ROW/COLUMN positions with
abstract vertex indices before this construction; equality of their original
labels is unnecessary. H_M is just a square0/1 matrix. Its diagonal ones
are ordinary edges between row/column copies in the bipartite interpretation.

Expanded dimension N=O(K^2(1+B+log(m+1))); even the dense N-by-N encoding
is polynomial. Huge integer VALUES never cause unary expansion. Exact
support matching handles zero minors; no relative estimate of zero is needed.

## 2. Latent law: no independent-photon or factorial mistake

For a matching sigma and ordered signal labels j1,...,jK the joint law is

    q(sigma,j)=product_i P_(j_i,i)P_(j_i,sigma(i))/per(M).

Summing labels first gives matching weight product_i M_(i,sigma(i))/per(M).
Conditional label denominators M_(i,sigma(i)) are positive for legal support
and each numerator sum is exactly that denominator. Summing sigma instead
gives product_i P_(j_i,i)*per(P_j)/per(M). For occupation n,

    sum_(j:count(j)=n) product_i P_(j_i,i)=per(P_n)/n!,
    Pr(n)=per(P_n)^2/[n!per(M)]=per(A_n)^2/[n!Z].

The n! identical-row multiplicity is divided ONCE. No K! is introduced.
For K1 this is the squared-column categorical law; for m1,K2, the two
matching permutations have equal weights and both labels are forced1,
so n=(2) with probability1. For A=[1/2,1/2], its raw mass is Z=1/8,
consistent with per(A_n)^2/2!=1/8. Rank deficiency and m<K are harmless.
These are latent classical variables, not observable distinguishable paths.

## 3. Adaptive matching and confidence on every actual history

For each current square residual, EXACT feasible-edge tests precede calls.
An edge is eligible only if positive and its remaining minor has a perfect
matching. All-zero bad estimates choose a fixed feasible edge, so even
unlucky histories retain positive support and defined label kernels.
No retry until a good estimate and no conditioning on a final good event occurs.

On a good batch, summing absolute weight errors gives TV<=delta/(1-delta).
On any fixed past history, fresh estimation coins give bad-batch probability
at most the number of queried minors times eta. Coupling these actual row
kernels for K stages gives K*delta/(1-delta)+K^2*eta, not a bound obtained
by pretending estimates were independent AFTER selecting favorable histories.
The later label/count kernel contracts this matching error.

Median amplification also passes: for r=8u+1, E[3^F]<=(3/2)^r; Markov
gives failure<=(sqrt(3)/2)^r<=exp(-r/8)<=2^-u<=eta.
All r trials are fresh and capped, including for adaptive input minors.
Comparing dyadic outputs is exact polynomial-bit work, not a real oracle.

## 4. Uniform worst-case bit, output and coin bounds

The primary is Chen/Guo/Vigoda/Yang [2609.20717v2,16-Oct-2026](https://arxiv.org/html/2609.20717v2),
Theorem1/Section8.4,0/1 ONLY. P1245b68c2d/150l, SHA256
4dd85cebf0386e608733737459654c94b972a3883f5bc51ebe9329202383b9f1,
authenticated that leaf; its nonnegative unit-cost extension is NOT used.
P123's midpoint-clock alternative was rechecked: grid error<=2^(-b)/2,
U>=alpha implies U_b>=alpha/2, so log error<=2^(-b)/alpha<=Delta/2.
The tiny-grid abort implies U<alpha, already in the source budget. Delta's
dyadic choice is small enough; division by integer W>=1 and finite evaluation
use the other half. All randomness is finite; no continuous clock is sampled.

The primary's observed energy is bounded by N*ceil(log2(N!)). Expanded
binary exponents, not only compressed exponent encodings, are polynomial.
Multiplying a returned dyadic by M_ij or dividing by D^(2K) therefore has
polynomial bit size EVEN on bad-estimator branches. Fresh denominator
products involve at most K row weights, or m label weights; no history-wide
chain of conditional denominators is multiplied. The <=K^2 amplified calls,
their N-sized gadgets and precisions polynomial in K/epsilon remain polynomial.

For a positive integer weight total V, ell=ceil(log2 V) gives acceptance
V/2^ell>=1/2; V1 is deterministic. b capped blocks fail with probability
<=2^-b. At most2K+1 outer coins imply a total cap error<=epsilon/8 with
the stated b. A tiny Bernoulli success probability does not lower this
acceptance ratio: range rejection concerns its DENOMINATOR, not success.

Two wording cautions, not missing application arrows: categorical V must
be>0 (guaranteed by every actual call/fallback); K1's rational probabilities
can be evaluated exactly, but a non-dyadic law cannot be sampled EXACTLY
with bounded fair bits. Section5's cap/error must apply there too. The
normalized theorem is epsilon-approximate, as its opening explicitly states.

## 5. Raw mass, complete error and observation boundary

Contraction gives0<=Z<=1. The clipped independent relative estimate has
E|Z_hat-Z|<=delta_Z+rho_Z=epsilon/4. Couple its success Bernoulli with
Bernoulli(Z), then use FRESH conditional-sampler coins. No estimate/posterior
correlation or inverse-small-Z rejection is hidden. With delta=epsilon/(16K),
eta=epsilon/(8K^2), matching error<=epsilon/15+epsilon/8. Adding ALL outer
coin caps gives total TV<=epsilon/4+epsilon/15+epsilon/8+epsilon/8
=17epsilon/30<epsilon. Cap aborts map to the permitted coarse FAIL.
Do not condition on all coins accepting to claim an exact conditional law;
the bound is an unconditional prefix/abort coupling.

K0 returns the full vacuum exactly. For K>0, zero columns force certain
FAIL; nonzero columns give a positive Gram diagonal term even if rank deficient.
All successful sampled occupations total K, and all lower physical totals
are aggregated. This DOES NOT simulate their counts, resolved environment,
conditional quantum states, within-shot recovery, or observable runtimes.

For adaptive common histories, the uniform per-call guarantees plus fresh
known CF sources sum per-attempt TV errors. Polynomial histories/matrix
encodings and paid rebuilding/decoding are required, as source states.
Diagonal gauges change full-K amplitudes only by phases. For two certified
contractions at operator distance zeta, unnormalized K-particle vectors
differ by<=K*zeta; full-count plus aggregate-FAIL TV<=2K*zeta. No rare-event
normalization enters that accepted P104 error term. Positivity/gauge promises
cannot be replaced by entrywise absolute values of arbitrary complex matrices.

The proof supplies the alternative finite-bit realization needed by the
accepted P104 coarse-law reduction, CONDITIONAL ON the named external0/1
primitive being accepted. It does not retroactively prove P108's different
cooling sketch or create an exact sampler, practical speedup, full lossy-PNR
theorem, publication priority or positive optimizer result.

Only this review was written. No source/P104/P108/P110/contract/raw edits,
program/import/AST/test, scripted/numerical computation, RNG, graph/native/
runner/QPU, manuscript edit, delegation, checkout or push occurred.
