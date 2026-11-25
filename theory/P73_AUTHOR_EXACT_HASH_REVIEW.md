# P73 exact-hash independent author-proof review

Primary verdict: **proved as written** for the source's scoped analytic
claims and controls. Its REJECT/KEEP/FOLLOW-UP disposition is supported by
those claims, with no implication that all Gaussian optimizers fail.
No mathematical correction to this frozen source is requested.

## Exact artifact and independence

Reviewed the entire 378-line artifact
`.local/p66-dark-audit/research/P73_complementary_pair_source_route.md`,
SHA256
`97392ff30ae1b25ad1399c8f08bbea064a16f13b86b62c21cc99bf484d1d33a0`.
It was frozen as an uncommitted file in the author's worktree; this review
is pinned to those exact bytes, not an invented source commit. A later
byte-identical copy has the same mathematical review provenance.

Before reading it, the reviewer froze an independent 398-line derivation,
`theory/P73_independent_complementary_pairs.md`, commit
`a527e90b806538d4bf3c935ef60d28a0d9213502`, SHA256
`6f1947c64b8da9b37d52a92a46334d55db6c724c8e11da6687c383deed171df3`.
That hash was checked unchanged. The present review is not blind: the
author's stated disposition was visible, but it is not a proof premise.
The explicit uncut-edge mixture, which was not in the independent file,
was reconstructed from its sampling rule below.

Review date: 2026-11-25. Worktree: `.local/p66-dark-barrier`, starting at
the independent P73 checkpoint. Only this new review is written. No author
source, prior proof, raw data or executable file is changed. The proof-audit
and mathematical-proofreading workflows were applied; the two cited primary
editions were checked directly as a bounded source verification. No science
code, import, probability computation, graph draw, random sample, test,
backend experiment or QPU call was run. Browser/text reads are not physical
or numerical evidence.

## Claim and dependency checks

The model explicitly assumes even k>=2, N=2k, real symmetric nonnegative
zero-diagonal A, W=J-I+epsilon A, and Z=lambda W with lambda>0 and
||Z||<1. Two independent zero-displacement Gaussian colors occupy 2N
resolved mode degrees of freedom. Acceptance fixes red CF subset S of
size k and blue CF complement Sc. All other source cycles are failures;
the colors make S and Sc distinct records. The source changes P69's input
assumptions and does not borrow its CF-input transport conclusions.

The implication chain is

    diagonal squeezed-mode series -> normalized Gaussian pair source
    CF exponential coefficient -> raw two-color hafnian probability
    matching expansion -> shared weak tilt and centered coherence term
    explicit edge mixture -> feasible classical first-order control
    complete-background spectrum -> acceptance and signal-photon ceilings
    passive number conservation/pair congruence -> preparation boundaries.

The route's primary literature is supplementary attribution for the
Gaussian ingredient and graph-sampling context; all P73-specific
normalization, perturbation and cost implications are internally derived.

## Normalization, first order and the coherence term

For one diagonal pair parameter z, the unnormalized coefficients are
z^m sqrt((2m)!)/(2^m m!). Their squared norm is (1-z^2)^(-1/2).
For real symmetric Z, passive diagonalization therefore yields normalization
det(I-Z^2)^(1/4). A CF k-set coefficient is haf(Z_S), with exponential
order and pair-orientation factorials cancelling. Each color contributes
a square-root determinant to its probability and lambda^k to its k-photon
event. Their independent product is exactly

    q_epsilon(S)=det(I-lambda^2 W^2) lambda^(2k)
                         haf(W_S)^2 haf(W_Sc)^2.

There is neither a missing square root nor an extra determinant. Real
entries justify squares; the source correctly reserves modulus squares
for a complex extension. Odd k would give zero acceptance, and the stated
even-k restriction is used throughout. The detector event must retain
both vertex and color labels.

Let H=(k-1)!! and E_T the induced total A weight. Uniform perfect matching
edge probability is 1/(k-1), so d log haf(W_T)/d epsilon at zero is
E_T/(k-1). Since E_S+E_Sc=W_A-C_A(S), the log spatial weight has derivative
2(W_A-C_A)/(k-1). Normalizing against the uniform balanced law gives the
centered coefficient and expected-cut derivative printed in section 4.
The incoherent matching weight has edge factors (1+epsilon A_e)^2;
its linear log coefficient is identical. The min-cut derivative is thus
not a leading-order interference discriminator.

For a uniform matching M on T, write X_T=sum_{e in M}A_e, V_T=Var X_T,
and Q_T=sum_{e in T}A_e^2. Expanding the matching products gives

    log haf(W_T)^2
      =2log H+2epsilon E X_T
             +epsilon^2(V_T-Q_T/(k-1))+O(epsilon^3),
    log haf((W elementwise-squared)_T)
      =log H+2epsilon E X_T
             +epsilon^2(2V_T-Q_T/(k-1))+O(epsilon^3).

Their two-side unnormalized difference contains the common baseline
2log H. After conditional normalization it is exactly the centered
negative variance expression in source section 6. The author has retained
the centering that would be indispensable in a normalized-law comparison.
The expected-cut difference is the stated covariance term; its sign is
not universally favorable.

For k>=4, edge inclusion probability 1/(k-1) and disjoint-edge pair
probability 1/[(k-1)(k-3)] give

    V_T=Q_T/(k-1)
          +(E_T^2+Q_T-sum_i(d_i^T)^2)/[(k-1)(k-3)]
          -E_T^2/(k-1)^2.

The incident-pair subtraction and factor two match the independent
derivation. This is O(k^2) arithmetic for an induced subset, not a free
full sampler. With k=2 there is one matching and the squared hafnian
equals the hafnian of squared entries at every strength; the author
correctly states exact equality of the two conditional laws there.
All Taylor statements are for fixed A,k. No uniform growing-size
remainder estimate is assumed.

## Explicit feasible uncut-edge sampler

This additional control is valid. Under the uniform balanced law g0,
an edge is uncut with probability

    u=2*k(k-1)/[2k(2k-1)]=(k-1)/(2k-1).

For W_A>0 choose an edge e with probability A_e/W_A. Conditional on this
edge being uncut, the two branches (both endpoints selected or both
excluded) have the same number of balanced subsets:
binom(2k-2,k-2)=binom(2k-2,k). Choosing the branch with probability one
half and the remaining subset uniformly therefore realizes exactly
g0 conditioned on the uncut event, without rejection.

Mix this edge-conditioned draw with g0, using
a=2epsilon W_A/(2k-1). Its exact density relative to g0 is

    (1-a)+a/(W_A u) sum_e A_e 1[e uncut]
      =1-a+a(W_A-C_A(S))/(W_A u)
      =1-2epsilon[C_A(S)-E_0 C_A]/(k-1).

The last equality uses E_0 C_A=W_A(1-u). This is precisely the source's
entire first-order B law as an EXACT classical affine mixture. It is
nonnegative under the stated 0<=a<=1 condition. For W_A=0 the fallback
is g0 and all cut weights vanish. Edge reading/setup, choices, subset
generation and scoring remain paid polynomial operations; no optimum,
partition mask, hafnian evaluation or optical successful-shot conditioning
is used. No claim is made for this mixture outside its parameter range.

The latent matching construction is correct too: a full perfect matching
on N vertices has k edges; coloring k/2 of them red yields k red vertices.
For fixed S, the respecting weighted matchings factor into the two induced
matching sums f_M(S). The number of possible edge colorings is the same
for every full matching, so the S marginal is proportional to f_M.
Sampling the weighted matching itself remains a real cost. Rejection from
uniform full matchings can define an exact finite-instance sampler with
a valid envelope, but the source correctly supplies no general favorable
acceptance rate or polynomial exact-sampling claim.

## Raw background acceptance and photon accounting

At epsilon=0 the spectrum is N-1 once and -1 with multiplicity N-1.
Every induced hafnian is H. Summing the oriented color records gives the
printed exact Pacc0, with binom(2k,k), H^4, lambda^(2k) and determinant
factors (1-lambda^2(N-1)^2)(1-lambda^2)^(N-1). There is no factor one
half from quotienting complements.

Factorial integral bounds give H<=k(k/e)^(k/2). Dropping determinant
factors and using the physical lambda cap yields

    Pacc0<=k^4 exp(-2k)[2k/(2k-1)]^(2k).

The stronger intermediate exp(4/3) factor in the author file is valid:
log(1+x)<=x and 2k/(2k-1)<=4/3 for k>=2. Its looser e^2 ceiling
agrees with the independent result. Probability caps at one are needed
only as stated; no optimum over lambda or all-epsilon claim is inferred.

Differentiating the normalized single-mode series gives mean photons
z^2/(1-z^2), so both colors give
nbar=2 Tr[lambda^2 W^2(I-lambda^2 W^2)^(-1)]. At the background,
dropping the positive denominator corrections gives the stronger lower
bound used by the author,

    nbar>=2lambda^2 Tr(W0^2)=2lambda^2 N(N-1).

Consequently

    Pacc0/nbar
       <=[(N-1)/(2N)] binom(N,k) H^4/(N-1)^N
       <=(e^2/2)k^4 exp(-2k).

The coefficient (N-1)/(2N) is correct. This inequality is uniform for
0<lambda<1/(N-1), excludes the vacuum zero-over-zero endpoint, and is
only a favorable signal-photon accounting bound at epsilon=0. It does
not certify pump, preparation, wall time or other source families.
For iid repetition until acceptance, expected photons nbar/Pacc follows
by summing each attempt's emission conditional on reaching that attempt;
it does not assume within-attempt independence of emission and success.

## Full Gaussian state versus a residual pair

The preparation arguments have distinct correct scopes. Any nonzero
squeezing coefficient has nonzero amplitudes in arbitrarily high even
number sectors. Passive changes of basis cannot eliminate that unbounded
total-number support. Finite-m Fock input, vacuum ancillas, passive optics
and photon-count heralding leave at most m photons, even after mixing
outcomes. They cannot prepare the exact full nonzero Gaussian state.

For a pure two-photon state, the symmetric pair coefficient transforms
as M to U M U^T. Two distinct CF photons give rank two. Vacuum padding
and passive processing cannot yield a generic rank-N pair matrix from
that resource. W0 is full rank and stays so locally, but the source
properly allows exceptional parameter values with smaller actual rank.

For m CF photons with m-2 detected, expanding the surviving two factors
gives M_res=V C V^T, with the m retained input-column projections as
columns of V. Thus rank M_res<=m. Passive conditional feedforward
preserves the branch rank. Forgetting branches does not turn a mixture
into a higher-rank pure pair: if the mixture is pure, every nonzero pure
component must be the same ray. This confirms the necessary m>=N pair
condition without claiming sufficiency or a herald probability.

The rank argument is not a universal lower bound for an arbitrary fixed
many-photon hafnian encoding. A changed fixed-number or truncated source
needs its own normalization, approximation and preparation success budget.
The Gaussian determinant cannot be imported unchanged. The author keeps
these boundaries separate and makes no claim that squeezing or color-
resolved Gaussian preparation is available on the project hardware.

## Bounded verification of the two primary citations

The official version metadata and full texts were read on 2026-11-25,
including versioned PDFs; no PDF bytes or extracted source text were
retained. These are ingredient checks, not a broader novelty search.

- Hamilton et al., *Gaussian Boson Sampling*,
  [arXiv:1612.01199v2](https://arxiv.org/abs/1612.01199v2), revised
  20 April 2017. [Primary text](https://arxiv.org/html/1612.01199v2),
  equations (10)–(11), gives B=T diag(tanh r_j)T^T and the pure squeezed
  CF hafnian-squared probability with its Gaussian normalization.
  The source's mapping B=Z and internally derived two-color prefactor
  are compatible. This is a verified known ingredient, not a citation
  proving the complementary acceptance/control construction or advantage.
- Arrazola and Bromley, *Using Gaussian Boson Sampling to Find Dense
  Subgraphs*, [arXiv:1803.10730v2](https://arxiv.org/abs/1803.10730v2),
  revised 30 July 2018. [Primary text](https://arxiv.org/html/1803.10730v2),
  equations (1)–(2) and their graph-encoding discussion, supports the
  cited fixed-size CF hafnian-weighted graph-sampling context. P73 uses
  that proportionality, not a paper's global prefactor as a substitute
  for its own lambda homogeneity or raw normalization. No runtime,
  postselection, comparator-cost or independent-replication conclusion
  is transferred from that paper to P73.

The locators and revision dates in the source match the primary records.
The Gaussian law and graph-sampling motivation are established adjacent
ingredients. No originality result for the complementary variant follows
from two citations or from this audit.

## Closure

| Obligation | Review result |
|---|---|
| Exact 378-line source and independent 398-line pre-read freeze | Passed |
| Gaussian determinant, lambda degree, parity and 2N color resolution | Passed |
| Weak min-cut derivative and matching control | Passed at fixed instance size |
| Normalized second-order centering, variance formula and k=2 | Passed |
| Explicit uncut-edge feasible mixture | Passed with 0<=a<=1 and zero-weight fallback |
| Background Pacc and uniform-lambda per-photon ceilings | Passed in their stated background scope |
| Finite-Fock Gaussian impossibility and separate pair-rank necessity | Passed; no sufficiency/rate claim |
| Two primary ingredient citations | Verified, without novelty or advantage transfer |
| Full sampler efficiency, finite-strength benefit and preparation bridge | Open, not established |

No remaining mathematical gap was identified in the source's actual
analytic statements. The strongest safe disposition is the one stated:
the leading-order advantage claim and free-source shortcut fail; the law,
controls and scoped preparation obstructions remain useful; materially
different or finite-strength mechanisms remain open under explicit raw
budgets and strong baselines. This audit authorizes no experiment or code.

Text reads, exact hashes, primary-source inspection and hand derivations
support this review. Git whitespace checks accompany its commit. Final
mathematical proofreading covered normalization exponents, color counts,
mixture coefficients, variance centering, photon denominators and the
distinction between pair rank and full Gaussian support. No scientific
execution was performed and the pre-read independent proof is unchanged.
