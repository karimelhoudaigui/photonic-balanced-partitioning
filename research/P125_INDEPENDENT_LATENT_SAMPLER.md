# P125: independent constructive positive-transfer latent sampler

2026-11-26. MANUAL derivation from the CF Fock probability, without reading
P123's moving source or another author's algorithm/outcomes. One file only;
no imports/AST, scripted algebra, numerical experiment, RNG, native/QPU call
or paper edit. Priority is unassessed; no novelty or optimizer gain is claimed.
The probability identity below is unconditional mathematics. Efficient
Turing implementation from a permanent FPRAS remains explicitly CONDITIONAL
on primitive guarantees and primary authentication not supplied by this note.

## 1. Physical probability and normalization

Let A be an m-by-K nonnegative rational matrix with A^T A<=I. The source
contains one photon in each of K distinct input ports, vacuum elsewhere.
Only full-K SIGNAL occupations n, including collisions, or one aggregate
FAIL are observed. On full-K, define n!=product_j n_j! and let A_n repeat
row j exactly n_j times. Expanding the signal creation-operator product

    product_(i=1..K) [sum_(j=1..m) A_(j,i) b_j^dagger] |vac>

gives the normalized Fock amplitude per(A_n)/sqrt(n!). Indeed the ordered
output assignments with multiset n sum to per(A_n)/n!, while their creation
monomial has norm sqrt(n!). Thus w(n)=per(A_n)^2/n!, with no CF-output
restriction. Its total mass is Z=per(G), where G=A^T A. To check this
directly, expand the Gram permanent into K independent row sums; grouping
the ordered output assignments by their multiset gives the same sum w(n).
Equivalently, taking the norm of the displayed bosonic product pairs each
input column once with every other ordering, producing per(G).

The contraction assumption makes Z<=1: the symmetric K-particle lift of A
has norm at most ||A||^K<=1 on a normalized CF state. It supplies a physical
full-K/FAIL law, with FAIL mass 1-Z. The conditional identity below itself
only needs A>=0 and Z>0, not contraction. Physical certification and optical
compilation of a claimed A are separate paid inputs, not oracle gifts.

## 2. Exact construction using one weighted-matching draw

The allowed matching primitive for a square nonnegative matrix G samples
a permutation sigma with probability product_i G_(i,sigma(i))/per(G).
For Z>0 perform these operations, with no rejection on the physical yield:

1. Draw sigma from that weighted-perfect-matching law on the K source labels.
2. Independently for each i, draw a SIGNAL mode J_i with rational weights
   A_(j,i) A_(j,sigma(i)), normalized by G_(i,sigma(i)).
3. Return the occupation n_j=#{i:J_i=j}; retain every collision.

An ideal sampled matching has every used G entry positive, so these
categorical probabilities are well-defined and sum to one. The joint law is

    P(sigma,J)=Z^(-1) product_i A_(J_i,i) A_(J_i,sigma(i)).

For fixed ordered J, summing sigma yields
Z^(-1) per(A_J) product_i A_(J_i,i). For all J having occupation n,
per(A_J)=per(A_n), and

    sum_(J:count(J)=n) product_i A_(J_i,i)=per(A_n)/n!.

Each distinct assignment appears n! times in the repeated-row permanent;
this is the complete output-factorial accounting. Consequently the returned
probability is exactly per(A_n)^2/(n! Z), as required. The latent sigma and
J are classical sampling auxiliaries, not physically observed photon paths,
an effective quantum-state description or distinguishable-photon labels.
Only elementary arithmetic, ONE supplied matching sample and K rational
categorical choices are used after constructing G in O(mK^2) arithmetic.

## 3. Zeros, dimensions and bunching

For K=0 the empty permanent is one, sigma is empty, the occupation is vacuum
and Z=1: no matching or random choice is needed. This includes m=0.
For K>0 a zero column of A forces Z=0 and every full-K w(n)=0; return FAIL
with certainty and do not define a conditional success law. Conversely if
all columns are nonzero, every G_ii>0 and the identity matching has positive
weight, so Z>0. Thus this special Gram family has an exact elementary
zero-Z test. For m=0,K>0 all columns are zero.

m<K and rank-deficient G cause no problem: the output is bosonic, not a
subset of m distinct modes, and no determinant/inverse is used. In the
full-bunch case m=1 with row (a1,...,aK), all ai>0, per(A_n)=K! product ai,
w(K)=Z=K! product ai^2. Matching permutations are uniform and all J_i=1;
the conditional output is deterministically n=(K). This also verifies the
single n!=K! divisor. For K=1 the construction reduces to probabilities
A_(j,1)^2/sum_j A_(j,1)^2, with the unique matching.

ROOT suggested the following additional hand check after this derivation:
m=1,K=2,A=[1/2,1/2]. Then G has every entry 1/4, Z=1/8, per(A_n)=1/2,
and w((2))=(1/2)^2/2!=1/8; FAIL has mass 7/8. Identity and swapped
matchings each have probability 1/2, and both mode choices are deterministic,
so the conditional output is (2) with probability one. No padding is needed.

To make an APPROXIMATE matching sampler total, define an arbitrary fixed
occupation n_star=(K,0,...,0) if it emits a zero-weight matching containing
some G_(i,sigma(i))=0. Ideal probability of this branch is zero; Z>0 ensures
m>=1. Do not condition/retry until a positive-weight matching appears.
This total extension is crucial for a direct TV contraction argument.

## 4. Error reduction and a conditional FPRAS implementation

Use TV=half L1. If the supplied matching distribution has TV error <=eta,
the exact categorical/count kernel above gives conditional occupation error
<=eta, by data processing, including the zero-weight fallback. If each of
the K mode choices instead has uniform conditional TV error <=xi, coupling
adds at most K xi. There is no factor 1/Z in this conditional reduction.

For completeness, an INDEPENDENT conditional implementation of the matching
primitive can self-reduce a permanent FPRAS. In a current row i, choose column
j with weights G_ij per(G with row i/column j removed), and then recurse.
The empty minor has permanent one. Suppose each queried minor estimate is
a nonnegative rational with relative error <=r<1 except probability beta,
uniformly for each queried input, using fresh randomness. Zero permanents
must be returned as zero on that guarantee, or a separately certified
support/zero test must precede such a query. These are primitive premises.
Normalize the rational estimated weights categorically. Writing estimated
weights as w_j(1+e_j), |e_j|<=r, gives
hat_p_j-p_j=p_j(e_j-E_p e)/(1+E_p e), hence categorical TV<=r/(1-r).
Individual zero weights receive probability zero. If ALL estimated row
weights vanish, use a fixed permutation completion/fallback, not an unbounded
retry; on a legal positive parent this requires a bad estimate event.
At most N=K(K+1)/2 minor queries and K row choices give

    matching TV error <=min(1, K r/(1-r)+N beta).

The bound holds with adaptive minors: the fresh per-query guarantee applies
conditioned on the past, and row-kernel coupling sums the local errors.
It does not condition the sampler on the global event that every estimate
was good. For target eta in (0,1), r=eta/(4K), beta=eta/(4N) suffice for
K>=1, since the displayed bound is at most eta/3+eta/4<eta. Approximate
row categorical choices would add their own K-times error separately.

All of this is an ORACLE REDUCTION, not primary verification of JSV or a
certified software implementation. Polynomial BIT runtime additionally
requires uniform polynomial runtime/output bit length for the FPRAS on
nonnegative rational minors, its zero-input behavior and amplification
guarantee. Those assumptions remain for independent P124/P123 verification.
The Gram sums have polynomial rational bit length: clearing denominators
across m products increases bits at most linearly in m and input bit size.
Minor entries remain subsets of G; sequential path probabilities need not
be multiplied explicitly. No inverse-small-Z or Gram-rank conditioning is
needed in this reduction. Large polynomial constants are not measured speed.

Exact rational categorical choices admit a Las Vegas fair-bit construction:
clear denominators to integer weights, draw a uniform b-bit integer with
2^(b-1)<W<=2^b, reject integers >=W, and locate the cumulative weight.
Acceptance exceeds 1/2 (or equals one); expected trials are below two.
This is an EXPECTED-time assertion, not a bounded worst-case exact draw.
After s trials, a fixed fallback adds at most 2^(-s) TV; all finite-cutoff
failure/error and computational cost must be charged. Non-dyadic rationals
must not be silently sampled exactly with a fixed number of fair bits.

## 5. Raw FAIL law, rare success and observation scope

The matching sampler alone gives a CONDITIONAL law; it does not supply a
free exact normalizer. With exact Z, a rational Bernoulli(Z) followed on
success by the construction yields the exact physical raw full-K/FAIL law.
For example A->cA rescales Z by c^(2K) but leaves BOTH latent conditional
steps unchanged. Arbitrarily rare survival therefore cannot be inferred
from a normalized matching distribution alone.
Alternatively let a separate count primitive estimate Z relatively within
r_Z with failure probability beta_Z, and set p=clip(estimate,0,1). Clipping
does not increase error from the true Z in [0,1]; it is not a proof that an
unverified estimate is accurate. With conditional occupation error eta_Q,
coupling the Bernoulli branches gives the full-law bound, on a good estimate,

    TV(raw approximate,raw true)<=|p-Z|+min(p,Z)eta_Q
                               <=Z(r_Z+eta_Q).

Fresh primitive randomness or an equivalent uniform conditional guarantee
justifies that combination; the estimator bad-event probability adds
beta_Z. Rational-Bernoulli truncation adds its own TV error. With only an
additive normalizer error alpha, replace the first term by alpha instead;
small absolute raw TV alone does not guarantee conditional precision at
rare Z. Neither version treats optical discarded attempts as free successes.

For T draws sharing a precomputed normalizer, compilation/estimation costs
remain paid and the common estimator bad event is not T independent events.
A conservative joint-transcript bound is beta_Z+T times the good-event
per-draw bound, with fresh draws and uniform conditional guarantees. Rare Z
does not force 1/Z physical postselection in the CLASSICAL conditional
algorithm, but says nothing by itself about matched classical runtime costs.

The identity also applies to transfers gauge-equivalent to A: independent
input/output diagonal phases change every fixed full-K Fock amplitude only
by an occupation/input phase, preserving w and Z. Arbitrary signed/complex
transfers are excluded: their product expansion is not a positive latent
measure. Taking entrywise moduli is not a valid extension.
FAIL here aggregates ALL lower-signal-total records. This does not sample
their individual counts, resolved environment records or conditional states;
I-A^T A can have negative off-diagonal entries. A controller using such
records, another coherent optical operation or adaptive recovery needs a
new instrument theorem. Common classical postprocessing of the declared
full-K/FAIL record is legitimate; a new observation alphabet is not free.

Disposition: exact constructive count-law identity and explicit conditional
approximation reduction. This note does not authenticate a polynomial-time
primary source or establish practical runtime, optimizer advantage, hardware
support or a universal photonic no-go. Actual source/preparation errors need
their own channel/flag model. All source attempts, K photons, FAIL events,
normalizer/Gram work, precision, training and scoring remain paid.
