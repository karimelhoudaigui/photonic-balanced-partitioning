# P104 independent proof and source-applicability audit

Reviewer `/root/p66_dark_audit`, 2026-11-26; `proof-audit` / `literature-check`.
Primary verdict: **CONDITIONAL ON a polynomial finite-bit implementation of
the weighted matching/counting primitives**. The internal probability reduction
and stability bounds pass; the original card does not close the claimed binary
runtime/random-bit/output-length bridge. This is not a mathematical counterexample
to that stronger claim. Padding also needs the explicit output map stated below.

Exact target: `research/P104_GAUGE_POSITIVE_FAILURE_TRANSCRIPT.md`, all 138 lines,
ROOT commit `79913dcbc86640777aa6c5907804a03439e37999`, SHA256
`24577741cd5351c8becab25058791347aa78b82a5b3f57ce82424800a883cb47`.
I am not an author of this source. Later suggested bit-bridge work is not an
audited dependency here; ROOT's proposed rational-cooling sketch is not accepted
as proof by this review. Original source is left unchanged.

## Typed observation and dependency verdicts

Known fresh CF K-photon source, passive vacuum environment, supplied contraction
T=D_o A D_i with diagonal unitary phases and nonnegative rational A.
Observe a full occupation n of TOTAL K, INCLUDING collisions, or one aggregated
FAIL for all N<K. The policy may not inspect the actual partial-loss record.
The promise supplies the gauge/contraction certificate; finding or calibrating
one is not part of the sampling theorem and must be paid separately.

Dependency map: normalized CF no-loss vector -> phase cancellation / Gram Z;
nonnegative permanent estimator -> success gate -> conditional occupation sampler
-> coarse observation coupling -> common-decoder / adaptive transcript coupling.
Tensor telescoping -> unnormalized measurement stability -> additional 2K zeta.
Gram, normalization, success-mass restoration, error addition, stability and coarse
policy contraction passed. External probability-law applicability passed in the
sources' stated arithmetic setting; the finite-bit complexity upgrade remains
conditional. Raw partial-loss simulation and optimizer/time/novelty claims are out of scope.

## Exact primary leaves checked, with model caveat

Anand, Chen, Cryan, Freifeld, Goldberg, Guo and Zhang,
[Simulating Gaussian boson sampling on graphs in polynomial time, arXiv v3](https://arxiv.org/html/2511.16558v3),
6-Nov-2026, Theorem1.3, Section3, Eq(5). The normalized occupation weights are
per(A_n)^2/n! for nonnegative rectangular A, with K<m. The matching construction
uses polynomially many row copies and rational edge weights when A is rational.
This verifies the distribution/normalization translation, not an explicit
random-bit implementation; its stated runtime does not specify input-bit costs.

Jerrum, Sinclair and Vigoda,
[A Polynomial-Time Approximation Algorithm for the Permanent of a Matrix with Nonnegative Entries](https://www.math.cmu.edu/users/af1p/Teaching/MCC17/Papers/approxpermanent.pdf),
JACM51(4),671–697, July2004: authenticated 27-page published scan, Theorem1.1
p673, Section2.1 p674, Section5 pp690–693 and Section7 p694. It provides the
nonnegative permanent FPRAS, exponential relative-error convention and median
confidence amplification. The arbitrary-weight discussion distinguishes
positive-weight dynamic-range dependence from a unit-arithmetic strongly
polynomial variant. DOI access failed; the published scan was checked instead.

The bridge gap is specific: polynomially many real operations and polynomial
log(weight ratio) do not alone bound rational intermediate/output lengths or
finite-bit transition simulation. JSV's displayed cooling uses exp(-1/2);
the original P104 does not specify its finite-precision replacement, accumulated
transition error or internal coin caps. The same missing implementation bridge
affects the matching calls in the occupation sampler. No inspected result proves
the card's blanket finite-bit sentence merely by quoting its real-cost bound.

## Gram identity, contraction and success probability — passed

Gamma_K(T) is the restriction of T tensor K to symmetric tensors. Its norm is
at most ||T||^K<=1. Applied to the normalized distinct-mode input it gives the
unnormalized no-loss vector psi. Its coefficient on occupation n is
per(T_n)/sqrt(product_j n_j!), with every input factorial equal to one.
In each permanent, output phases contribute product_j(D_o,jj)^n_j and the
input phases contribute product_i D_i,ii, regardless of the routing permutation.
They have modulus one, proving w(n)=per(A_n)^2/n!.
Commuting annihilators through creators gives
sum_(|n|=K) w(n)=||psi||^2=per(T^dagger T)=per(A^T A)=Z<=1.
The input phases cancel in the Gram permanent as well. Positivity is physical
and algebraic: C=A^T A is entrywise nonnegative, and for nonzero columns its
diagonal product is a strictly positive permanent term. Hence Z>0 in that case.
C's entries are rational with polynomial encoding size under rational arithmetic.

K=0 is deterministic observed vacuum, not FAIL. If K>0 and one column is zero,
no full-K event is possible and the COARSE observation is certainly FAIL;
the remaining physical photons may still have a nontrivial partial-loss law.
Rank-deficient nonzero columns do not force Z=0 because collisions are included.
K=1 reduces to a rational intensity/categorical calculation; no many-photon issue arises.

## Conditional sampler composition and fair bits — passed as an interface reduction

Let the counting primitive return a finite rational estimate, with exponential
accuracy parameter delta/2 and failure probability rho. On its good event,
Zhat/Z is between exp(-delta/2) and exp(delta/2); since 0<delta<1,
exp(delta/2)-1<=delta, yielding |Zhat-Z|<=delta Z. Clipping to [0,1] cannot
increase error from the true Z in that interval. Therefore E|Zhat-Z|<=delta+rho.
Couple Bernoulli(Z) and Bernoulli(Zhat) using one uniform coin. Their mismatch
probability is E|Zhat-Z|. On joint success, independently couple the fixed-K
occupation laws with error epsilon_s. This proves TV<=delta+rho+epsilon_s;
it never waits for physical success or divides the runtime/error by Z.

For rational Zhat=a/b, draw a uniform integer below b by rejection from
ceil(log2 b) fair bits. Each block succeeds with probability at least1/2;
b=1 is deterministic. A B-block cap has failure probability <=2^-B.
Without a cap the coin has finite expected but unbounded worst-case length;
with the cap it uses at most B ceil(log2 b) bits. Neither statement bounds the primitives.
Map that computational failure to FAIL, or use an extended alphabet with zero
physical flag mass and charge the same error. Taking delta=rho=epsilon_s=epsilon/4
and B=ceil(log2(4/epsilon)) gives total error<=epsilon. This argument bounds
the FINAL Bernoulli coin once b has polynomial bits; it does not establish bit
costs of the two external primitives or cap all their internal random choices.

Padding clarification: append zero rows until m'>K. Exact target occupations
have zero counts there. An approximate sampler specified only by TV may still
put small mass on a padded coordinate. Map ANY such output to FAIL; otherwise
remove the zero coordinates. This preserves the intended alphabet and cannot
increase TV. Alternatively prove the implementation always outputs valid
matchings excluding zero-weight edges. Blind removal alone is insufficient as
an interface rule because it could emit an illegal N<K occupation instead of FAIL.

## Unconditional approximate-gauge stability — passed

For contractions T,T0, telescoping their K-fold tensor powers gives
||Gamma_K(T)-Gamma_K(T0)||<=K||T-T0||<=K zeta.
Let psi,psi0 be the two unnormalized no-loss vectors; each has norm<=1.
By factorization of squared moduli and Cauchy-Schwarz,
d=sum_n ||psi_n|^2-|psi0_n|^2|
 <=(||psi||+||psi0||)||psi-psi0||<=2K zeta.
The FAIL mass difference is |Z-Z0|<=d, so the COARSE-law TV is
(d+|Z-Z0|)/2<=d. Adding the simulator error proves exactly 2K zeta+epsilon.
There is no 1/Z amplification because full-attempt masses, not normalized
conditional states, are compared. K=0 has zero difference. The contractions and
operator-norm certificate are supplied assumptions, not inferred efficiencies.

## Nulls, finite-bit boundary and permitted continuation

For an ordinary nonnegative undirected Laplacian L, qI-L is nonnegative when
q>=max degree, and exp(-beta L/2)=exp(-q beta/2) exp(beta(qI-L)/2) is nonnegative.
PSD L makes it a contraction. This does not turn generally irrational heat
entries into rational inputs: a paid contractive approximation/certified zeta is
still required. No finite-angle impossibility for magnetic filters follows.
Nonnegative orthonormal columns have disjoint supports; in a square isometry
each occupies one different row with entry one, giving a permutation.
For K>=1, A_jr=1/sqrt(mK) instead has C=J/K, so Z=K!/K^K and
mu_A(n)=K!/(m^K n!), the uniform multinomial law. This algebraic rank-one
diagnostic is separate from the rational-input complexity statement.

Lower-total counts are excluded for a reason: their loss Gram is I-T^dagger T,
which can have negative off-diagonal entries. Positivity of signal A neither
gives a nonnegative full dilation nor an independent survivor-subset mixture.
The current proof does not simulate those records and does not prove them hard.
Any common decoder, including lifted updates using only full-K/FAIL, contracts TV.
Adaptive use needs the promise and fresh primitive guarantees at each COMMON
history; reusing a fitted random estimate needs its own conditional failure budget.
First-mismatch coupling gives the sum of per-attempt errors, capped at one.
Polynomial transcript cost additionally needs polynomial history/matrix sizes,
attempt count, primitive bit cost and charged rebuilding/decoding. Rare conditioning,
hidden optical memory and wall-clock transcripts do not inherit this bound.

Strongest safe result now: the full-raw-success-mass composition is mathematically
valid for this coarse observation, given the stated approximate primitives;
binary polynomial cost is CONDITIONAL until their precision/output/random-bit
bridge is supplied. The next proof obligation is exactly that bridge, not a new
numerical pilot. ROOT's queued addendum has not been opened or accepted here.
No global novelty search was done. Read-only cache lookup found no local source
cache; primary browser texts were used without PDF retention or invented paper
hashes. During this audit there was no raw-data access, code/import/AST, numerical
execution, RNG/test/runner/native/QPU call, push, checkout or manuscript change.
