# P43 local-mean author-proof review, after independent reconstruction

Review date: 2026-11-24. Analytic only; no numerical/physical run, production
change, manuscript edit or QPU call. This receipt preserves the first source's
restriction verdict separately from the corrected source.

**Primary verdict on the final source SHA bae5da4f...: proved as written** for
the stated local-mean DP in its arithmetic/controlled-number model and the
additive estimator at the explicitly qualified scale. This is neither a
floating certificate nor an algorithm for globally optimizing or sampling
the complete occupation law. The earlier restrictions remain recorded below.

## Targets and independence boundary

The independent derivation was frozen BEFORE reading the encoding proof:
commit `fa6d1f77535dd1a297dab41a43f46684ea422e67`, file
`theory/P43_local_mean_independent_reconstruction.md`, SHA256
`93443ba701cfab14d3bef2f4387653c31f68fd9a1db0b6717bca9acfb388fda0`.
Its mathematical claims and source-scope counterexamples were sent to the
coordinator before that freeze. Subsequent author comparison does not change
that text or turn it into an audit of a source it had not yet read.

Author source path in another worktree:
`/Users/karimelhoudaigui/Desktop/pasqal/.local/p41-worktrees/encoding/theory/P42_encoding_local_L1_oracle.md`.

| Version actually inspected | Commit | Source SHA256 |
|---|---|---|
| Initial | `1eba68a0ba072ddcd0aa35a4736f65e32fd137dc` | `4b6bc6ee4bd5e9ae739264da37e0ebb3d6bb6a2b0fad7e16267738c14a3a638a` |
| Qualification correction | `c9cd90c7f9679914ff0b8235103d2020b65f5546` | `fc87dfe1ca034a121536abb6fa19bb115c2a96e0bfac786ff7514e1f1c525897` |
| Scale-qualified final | `1468f03af48157921561f24bde5dcefa6eea4144` | `bae5da4f08ea41499599e9eaf0c244584c82773c07a1195aa068e935d385ba44` |

The first two complete texts were read and their SHA256 values checked. Their
Git diff was inspected after the corrected version was read. For the final
version, the whole-file Git delta and the revised summary were read, with its
SHA256 checked; the delta changes only the scale qualification and correction
record. The DP and main formulas were unchanged through these revisions.
The companion source audit was also read, SHA256
`2adb832368d3ac78135281a93a4b8300a5a703776eb3cd430edeb9261518a882`,
at `research/P42_encoding_Monbroussou_L1_audit.md` in the encoding worktree.
Its own literature verdicts were not accepted as a substitute for the checks
listed below.

This reviewer's earlier noise/P40 authorship and P33/P37 reviews are disclosed.
None of that code/evidence is imported or rerun. P42 replication inputs and
raw remain unchanged. The author received the previously frozen reconstruction
and later this reviewer's scope objection, so the corrected proof is not an
author-blind second derivation. Independence refers to the earlier reconstruction
and the subsequent mathematical checks, not to an absence of communication.

## Claim card and dependency graph

Source: K perfectly indistinguishable photons in K distinct input modes;
selected-column isometry V, V*V=I_K; passive terminal interferometer; lossless;
no intermediate measurement/feedforward/nonlinearity. Output pairs are i<j.
The measured occupation has total K and keeps collisions. The target is the
UNCONDITIONAL mean of F_G, R_K and J_G in the source, not a conditional CF law.

The exact chain is:

1. Normalized Fock matrix element of D tensorpower K -> per(V*DV).
2. V*V=I and two observed modes -> identity plus two rank-one updates (L1).
3. Expansion by a COMMON active input subset -> coefficient identity (L3).
4. Equal left/right degrees -> three-index DP and its update (L5).
5. Shift of generating variables -> joint probabilities (L6).
6. Polynomial number of local cost terms -> exact mean (L7).

The additive chain is:

1. Fourier expansion of |d| on the cyclic group of size 2K+1 -> (L8)-(L9).
2. Phase return amplitude -> permanent of contraction Z_l.
3. Random-sign identity and norm bound -> unbiased X_l with |X_l|<=1.
4. Nonpositive nonzero Fourier coefficients -> bounded, unbiased local Y_ij.
5. Nonnegative pair weights -> bounded weighted estimator and Hoeffding (L10).

All these project implications were reconstructed directly below. External
sources provide attribution/context, not an unchecked load-bearing substitute.

## Obligation matrix

| Obligation | Result |
|---|---|
| (L1) conjugations and source normalization | Passed: a_alpha=conj(V_i,alpha), so aa* has the required matrix entries. |
| (L3)-(L4) combinatorial factors | Passed: r!s! for GF coefficients, (r!s!)^2 for raw falling-factorial moments. |
| (L5) all four transitions and boundary indices | Passed: each u/v choice increments exactly the stated indices; decreasing total degree or two tables avoids reuse. |
| DP state/operation counts | Passed: sum_(d<=K)(d+1)^2=O(K^3) states; K updates and inversion give O(K^4) arithmetic per pair. |
| Normalization/occupation domains | Passed: constant coefficient1; probabilities obtained by G(z-1,w-1); n_i+n_j<=K. |
| Exact bit complexity | Passed for explicitly bounded rational real/imaginary entries and rational graph data; algebraic/arbitrary-real qualifications are required and stated. |
| Float64 certification | Not established or claimed: alternating inversion can cancel; source explicitly warns. |
| Fourier coefficients, signs and total weight | Passed by cyclic second differences and Fourier inversion at d=0. |
| Gurvits/Glynn identity, compression norm and local draw cost | Passed by direct expansion, AM-GM and rank-two matrix-vector multiplication. |
| Weighted sampler, initial source | Failed without restriction on v_ij; exact counterexample retained below. |
| Weighted sampler, corrected source | Passed under the newly explicit v_ij>=0, A>0, K>=1, with vacuum/A=0 branches. |
| Claim that additive estimator is polynomial time | Final version explicitly restricts it to normalized J/(AK), or polynomial A for absolute accuracy; controlled scalar/sampling precision remains necessary. Exact DP has a different bit-complexity guarantee. |
| Full sampler, global optimum or final-best-cost domination | Out of scope; explicitly not inferred by the source. |

## Combinatorics, bounds and manual checks

For (L3), expand per(I+A) as the sum of principal-submatrix permanents over
input subsets T. Fix counts r,s in the two rank-one colors. The product in
(L2) chooses the SAME T for left and right assignments; each matching of those
color classes admits exactly r!s! permutations. The coefficient is therefore
r!s! d_(r,s,r,s), with no residual enumeration of binom(K,r+s) subsets.
The update in (L5) stores total degree d, u1-degree r, v1-degree p; its cross
terms increment (r,p) by (1,0) and (0,1) with the stated complex coefficients.
This checks the proposed aggregate algorithm rather than bounding only the
rank of an individual summand.

Manual factor test: balanced identical two-photon input gives
M(x,y)=1+x+y+(x^2+y^2)/2. Thus d_(2,0,2,0)=1/4 and the raw second falling
moment is (2!)^2/4=1, whereas the GF coefficient is2!/4=1/2. The author's
explicit convention (L3)/(L4) passes. Vacuum gives the constant1 polynomial;
one photon can be outside the observed two modes, so its (0,0) probability
must remain1-|V_i,1|^2-|V_j,1|^2. Those are algebraic checks, not runs.

Rational bit bounds do not follow merely from counting scalar operations.
A common denominator may be cleared per input-column factor. The product
denominator has O(KB) bits; the exponentially many expanded terms add only
O(K) magnitude bits, not exponentially many bits. Factorials add O(K log K).
The compact DP thus retains polynomial bit lengths. Arbitrary compact angle
circuits or arbitrary algebraic encodings need a separate representation
contract; the source explicitly preserves that limitation.

For precision, the earlier reconstruction also gives the diagnostic bound:
if every GF coefficient has absolute error at most epsilon, the probability
error after exact inversion is at most
epsilon*binom(K+2,a+b+2). This can grow exponentially with K; it is not an
assertion that every case attains that condition number. No machine-precision
validation or interval certificate was performed here.

## Fourier/Gurvits portion: analytically verified

Let L=2K+1, K>=1. For the cyclic function h(d)=|d|, its discrete second
difference is2 at0 and-1 at the two endpoints. Its l-th Fourier coefficient
is multiplied by -2(1-cos(theta_l)), giving exactly (L9). All nonzero
coefficients are nonpositive. The coefficient sum is h(0)=0, so their
negative mass is c0 and total absolute Fourier weight is2c0<K+1.

Expanding X_l over maps from rows to columns, averaging its Rademacher signs
kills every term unless each column is selected an odd number of times.
There are K selections and K columns, hence each must be selected exactly
once. The surviving terms are precisely per(Z_l), with no extra sign or
normalization factor. The passive phase compression satisfies ||Z_l||<=1.
Therefore

    |X_l| <= (||Z_l sigma||^2/K)^(K/2) <=1.

Using the negative Fourier weights and taking the real part gives the correct
real mean of |n_i-n_j|, not |per(Z_l)|^2. Thus Y_ij is unbiased and belongs
to[0,2c0]. This estimates a phase amplitude and is NOT a photon-law sample.
Identity plus two rank-one updates permits Z_l sigma and X_l in O(K)
arithmetic given the relevant two rows. Preprocessing, Fourier/pair sampling,
input precision and circuit construction are additional charged work.

For nonnegative v_ij and A>0, drawing the pair with probability v_ij/A yields
an estimator of sum v_ij E|n_i-n_j| in[0,2Ac0]. Subtracting the stated constant
does not change its range length. A sufficient Hoeffding count is

    T >= (2 A^2 c0^2/delta^2) log(2/zeta),

up to integer rounding, for delta>0 and0<zeta<1. This establishes the order
in (L10). Polynomial draw count requires A/delta polynomial in the input
size. Nonnegativity alone does NOT bound numerical magnitudes of binary-encoded
weights. The exact DP remains polynomial-bit for large rational weights, but
this particular sampling bound is polynomial in their VALUE scale. Finite
precision approximation of the categorical weights and matrix entries adds
bias/error and needs an allocated error budget for a certified implementation.
For the normalized target J/(AK), put delta=AK*epsilon: the draw bound becomes
O(epsilon^-2 log(1/zeta)); each draw still costs O(K) scalar arithmetic, in
addition to preprocessing. For unnormalized inverse-polynomial delta it is
polynomial when A is polynomially bounded. These are the two alternatives
explicitly stated by the final revision, rather than a bit-complexity claim
polynomial in log A for arbitrary absolute accuracy.

## Preserved initial restriction verdict and corrected version

Initial SHA `4b6bc6ee4bd5e9ae739264da37e0ebb3d6bb6a2b0fad7e16267738c14a3a638a`:
**correct only after a stated restriction** for the combined oracle claim.
The exact DP is valid, but its weighted probability sampler omitted
v_ij>=0 and a K=0 branch. In particular, m=4, K=2, w_01=6, other w=0,
lambda=-1 gives A=sum(w_ij+lambda)=0 while

    J(1,1,0,0)=0,
    J(1,0,1,0)=6.

Thus unrestricted A=0 does not imply constancy. Both occupations are valid
CF outputs attainable by a source-mode permutation. This is a quantifier
counterexample, not an optimization discovery. It does not refute (L1)-(L7).

Corrected SHA `fc87dfe1ca034a121536abb6fa19bb115c2a96e0bfac786ff7514e1f1c525897`:
the exact DP and the FORMULAS/range/sample-count bound of the additive oracle
are **proved as written**. The source now explicitly restricts the weighted
sampler to nonnegative v, treats A=0 under that condition, and excludes vacuum
from Fourier sampling while returning its deterministic zero cost separately.
The earlier counterexample and source hash remain in its correction history.
The shorthand polynomial-time additive phrase in Section1 must be read with
(L10)'s polynomial-scale and representation qualification above; without that
qualification its general binary-input runtime interpretation is not proved.
This review does not silently drop that remaining interpretation condition.

Final SHA `bae5da4f08ea41499599e9eaf0c244584c82773c07a1195aa068e935d385ba44`:
**proved as written** for the normalized/local-mean arithmetic statement and
its explicitly controlled rational bit interpretation. Section1 now states
J/(AK), AK>0, or polynomially bounded A for the unnormalized additive guarantee,
and distinguishes value A/delta from log A. The mathematical expectation,
sample-count and DP statements have no remaining missing combinatorial factor
or domain condition within those declared models. K=0 and A=0 use the existing
explicit deterministic branches. This final verdict does not rewrite either
previous verdict and does not certify a finite-precision implementation.

## Primary-source checks and limits of this audit

- [Aaronson--Arkhipov author PDF](https://www.scottaaronson.com/papers/optics.pdf),
  Appendix12, Lemma68 and Theorem69, printed pages97--98: the fixed-output-mode
  marginal statement and identity-plus-low-rank reduction were inspected.
  Lemma68 is expressly assumed there with proof deferred; that PDF alone is
  not a self-contained proof of the low-rank lemma. The explicit two-mode DP
  audited above avoids that missing leaf for this application. The author's
  PDF is unversioned and was not assumed byte-identical to an arXiv revision.
- [Aaronson--Hance author PDF](https://www.scottaaronson.com/papers/gurvalg.pdf),
  Section2, equations(20)--(27), Proposition1: the Glynn expectation identity
  and operator-norm bound were checked in the primary text, as well as
  independently derived above. This establishes the needed complex-matrix
  Gurvits-estimator arrow; the original Gurvits2005 paper was not itself
  retrieved or audited. The broader generalization in that paper is not used.
- [Monbroussou et al., arXiv:2607.24728v1](https://arxiv.org/pdf/2607.24728v1),
  Technique5 and AppendixC (C1), Proposition10, Technique7: the relevant source
  passages were inspected. For distinct inputs and degree d, (C1) retains
  binom(K,d) subsets. A bound on each permanent's rank alone does not sum them
  efficiently. The companion's caution is justified; it is not a refutation
  of the marginal statement. No whole-paper or all-techniques audit is claimed.

These are primary-source passages checked online on2026-11-24. No new PDF cache
was written, and the companion's local PDF/text hashes were not independently
reauthenticated. Lim--Oh's full theorem, all Monbroussou simulation/concentration
arguments, and a global novelty comparison are outside this review. The
project derivation is self-contained in the physical model stated above.

## Remaining obligations and checks actually performed

There is no unresolved combinatorial factor in the two-mode DP or the ideal
nonnegative Fourier/Gurvits estimator. An actual implementation still needs
its own precision/sampling-error contract and validation. Arbitrary internal
states, repeated spatial inputs, loss channels, nonlinear layers, full-law
sampling, global optimization, and measured QPU/classical cost comparisons
remain outside these particular formulas. The source's proposed global
improvement target is an uncovered target, not a proven hard or useful one.

Actual checks: read both author source versions and the companion; SHA256
verification; author Git diff; direct symbolic reasoning above; online primary
source extraction; Git status/whitespace checks for this new receipt. No
numerical script, test suite or physical calculation was run. The frozen
independent reconstruction and all P42 code, inputs, logs and raw are preserved.
