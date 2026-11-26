# P104: positive transfer matrices and coarse failure transcripts

2026-11-26, ROOT; base31f5630 plus P102 mission continuation.
**Candidate corollary/derivation; independent proof review pending.**
External sampling/counting ingredients are established. No novelty, practical
runtime win or universal optimizer obstruction is asserted. No computation ran.

## Model and claim

Fresh known CF K-photon source, vacuum environment, passive channel with
occupied-column contraction T in C^(m x K). Each attempt's observation is
either FULL signal occupation n with |n|=K (collisions INCLUDED), or one
symbol FAIL aggregating ALL lower-total outcomes. Further classical decoding,
loss self-loop or lifted-sign flip may depend only on that observation,
known source/history and fresh classical coins. Raw partial-loss counts
are NOT available to that downstream policy in this theorem.

Suppose diagonal phase matrices D_o,D_i and a NONNEGATIVE RATIONAL matrix A
are explicitly supplied, with T=D_o A D_i and A^T A<=I. Given rational
epsilon in(0,1), this observation law has a randomized classical epsilon-TV
sampler with polynomial cost in dimensions, rational-input bits and1/epsilon,
using the external primitives below. No trace-transmission bound is required.
If m<=K, append known zero output rows to obtain m'>K, then remove them.
K=0 is deterministic vacuum; a zero input column gives deterministic FAIL.

This excludes an exponential sampling separation for this logical observation
model, not a measured polynomial/constant-factor hardware benefit. Source/
compiler/matrix arithmetic, sampling and all classical decoding remain paid.

## Mathematical reduction

Let Gamma_K(T) be T^tensor K restricted to the symmetric K-particle space,
and let |S> be the normalized known CF input. The unnormalized no-loss vector
is psi=Gamma_K(T)|S>. Its full-K number amplitudes are per(T_n)/sqrt(n!).
The output/input phases have unit modulus; hence

    w(n)=|per(T_n)|^2/n! = per(A_n)^2/n!,
    Z=sum_(|n|=K) w(n)=||psi||^2=per(A^T A), 0<=Z<=1.       (1)

The Gram identity follows directly by commuting the K linear annihilators
through their creators; all K! contractions occur once. It also follows
from summing the symmetric-tensor norm. Since ||Gamma_K(T)||<=1, Z<=1.
For nonzero columns, diagonal Gram entries are positive and the identity
permutation shows Z>0. C=A^T A is rational/nonnegative with polynomial-size
encoding. The physical observation is FAIL with probability1-Z and otherwise
the normalized full-K law mu_A(n)=w(n)/Z. Normalizing it alone would erase
the preparation cost; the construction below explicitly retains Z.

Use the external permanent FPRAS on C to return a rational estimate Zhat,
with relative error at most delta except on probability rho. Its published
exp(+-accuracy) convention permits accuracy=delta/2 for0<delta<1; median
amplification uses O(log(1/rho)) trials. Clamp its
output to[0,1]. On the good event, |Zhat-Z|<=delta Z<=delta; on the bad event
the error is at most1. Thus E|Zhat-Z|<=delta+rho. Generate a Bernoulli(Zhat).
On failure return FAIL; on success independently draw nu_A using the external
fixed-K nonnegative-matrix sampler with TV(nu_A,mu_A)<=epsilon_s.
Coupling Bernoulli outcomes first and conditional occupations second gives

    TV(P_observation,P_classical)<=delta+rho+epsilon_s.        (2)

Choose each term epsilon/4. A rational Bernoulli can use a block of fair bits
and rejection against its denominator; acceptance is at least1/2. Cap this
at B=ceil(log2(4/epsilon)) blocks and retain an explicit computational-failure
flag (or output FAIL); added TV<=2^-B. All random-bit/output lengths and
FPRAS repetitions are polynomial. This construction is an existence proof,
not an executable implementation of either large matching algorithm.

Any COMMON randomized classical decoder contracts TV. For adaptive policies
the above supplied hypotheses must hold at EVERY common observation history;
hybrid coupling bounds the T_attempt joint-transcript TV by the sum of the
per-attempt errors. History lengths/matrix rebuilding/decoding must be
polynomial and charged for a polynomial transcript-cost conclusion. Rare
conditioning, exponentially long trajectories or a hidden optical memory
do not follow from this argument.

## Approximate positive representatives: unconditional stability

If T and supplied T0=D_o A D_i are contractions and ||T-T0||op<=zeta, tensor
telescoping gives ||Gamma_K(T)-Gamma_K(T0)||op<=K zeta. Both no-loss vectors
have norm<=1. Therefore the l1 distance of their unnormalized full-K count
laws is at most (||psi||+||psi0||)||psi-psi0||<=2K zeta. Adding the FAIL
weight changes total variation by at most that same l1 distance. Consequently

    TV(P_observation(T),P_classical(T0))<=2K zeta+epsilon.     (3)

This is an ABSOLUTE full-attempt bound, without a 1/Z factor. The matrix
norm/contraction/gauge certificate is an input assumption, not inferred from
public efficiencies. It does not certify the raw partial-loss count law.

## Falsifiers, nulls and transfer limits

- Exact real heat filters of a nonnegative undirected graph, exp(-beta L/2),
  are entrywise nonnegative contractions: L>=0 and uniformization writes
  the exponential as a positive sum of powers of qI-L>=0, q>=max degree.
  Applying the finite-bit statement additionally needs a supplied rational
  contractive approximation and certified zeta, with its construction paid.
  It must not be represented as a finite-angle impossibility for magnetic
  filters, whose irreducible complex phases can violate the assumption.
- A positive Sinkhorn/transport intensity table is not automatically an
  interferometer. Nonnegative orthonormal columns have disjoint supports,
  since each nonnegative pairwise inner product must vanish. For a square
  lossless device this forces a permutation. Ancilla contraction or genuine
  nongauge phases change the physical model and must be accounted for.
- For A_jr=1/sqrt(mK), Z=K!/K^K and the conditional occupation law is exactly
  multinomial(K;1/m,...,1/m). This real algebraic rank-one diagnostic is
  separate from the rational-input theorem. Bunching/preparation yield is
  not an optimization mechanism; all failed preparations remain charged.
- Retaining lower-total counts breaks THIS reduction. Their Gram formula
  involves I-T^dagger T, with possibly negative off-diagonal entries even
  when T>=0. Nonnegative signal entries do not prove a positive full dilation
  or an independent survival-subset mixture. This does not assert that full
  raw sampling is hard, only that (1)-(2) do not simulate those observations.

## Authenticated external leaves and exact application

Anand, Chen, Cryan, Freifeld, Goldberg, Guo, Zhang,
*Simulating Gaussian boson sampling on graphs in polynomial time*,
[arXiv2511.16558v3,6-Nov-2026](https://arxiv.org/html/2511.16558v3),
Theorem1.3/Section3, equation(5); author PDF marked accepted Quantum3-Nov-2026.
It supplies the normalized nonnegative rectangular fixed-K occupation sampler.
The version, theorem and matching-reduction proof were read; its use for
mu_A is VERIFIED. It does not supply our aggregated failure probability.

Jerrum, Sinclair, Vigoda, JACM51(4),671–697(2004),
[DOI10.1145/1008731.1008738](https://doi.org/10.1145/1008731.1008738),
Theorem1.1 and Sections5,7 (nonnegative extension), published27-page scan.
It supplies a permanent FPRAS; application to rational nonnegative C is
VERIFIED. Confidence amplification and the coupling above are spelled out
rather than importing an exact counting oracle. No runtime benchmark follows.

Browser primary texts are authenticated/extracted, not retained/hash-cached
locally. External overlap: **formal corollary not stated** for this coarse
failure-transcript composition, subject to independent internal review;
no global priority search or first-result attribution was completed.
The sharp boundary is an explicit positive/gauge-positive transfer AND
aggregated failures. P101's all-output decoder remains a distinct open route.
CLAIM-042 OPEN. No held-out graph, optimizer, manuscript, hardware bundle
or QPU run is authorized by this theorem card.
