# P50 minimal count field: independent static physics-card review

2026-11-25. No implementation, import, numerical calculation, graph generation,
test, raw outcome or hardware call is evidence for this review. I reconstructed
the identities below from the CF source state and read the complete cards.
I previously reviewed/authored related P49 physics notes and reviewed its
helpers; this is same-team independent review of ROOT's new design, not an
external replication or review of P50 code that does not yet exist here.

**Verdict:** the prospective physical model is coherent. The execution card's
corrections resolve the factor/mask and monomial/conjugation ambiguities.
The abstract inclusion lemma needs a stronger margin for the declared bucket
decoder. No physical advantage, favorable diffusion theorem or numerical
qualification follows. Implementation and finite preflight remain separate.

## Exact versions read

| File/version | SHA256 |
|---|---|
| P50_MINIMAL_COUNT_FIELD_CARD.md at7b188e726f42bbc512acd779bd1f57ea3e52318a | 2e856b07b68a6ec3af2f4a29897cde9ff115969f9156cf5aab79ee35c65f6235 |
| P50_EXECUTION_CARD.md atf9689d29953c808cbfbe6daee05062f85c90dd9d | 698651eae6efca891c2d49efa6bc79518960d821439cc9001d7d9994cf9ce3bd |
| P50_EXECUTION_CARD.md at79d3550c1527ea59f1cbd4bc98b51fabe003e17d | fe246e6192319299a58f108ddf64e7d61a55d0e6c1d01476fe2fd717f49e92ac |
| P50_EXECUTION_CARD.md atded2cfb086fe791a9dfac1176d610ed880a33c7d | dd35ce543d1edfce0aabf5e30517ad9e1590eb13ee4a5731733c38a0dde5b919 |

These hashes were computed from git-show bytes, not inferred from filenames.
The79d3550 version fixes ties and acknowledges Fourier static duplicates;
ded2cfb adds the tenth product-marginal arm and the quantized inclusion margin.
This review does not incorporate later changes by implication.

## Covariance and final variance control

For orthonormal columns V, the normalized state is
prod_a(sum_i V_ia a_i^dagger)|0>. Write Q_ia=|V_ia|^2, P=VV*, mu=Q1.
Expanding the normally ordered pair moment gives, including i=j,

    E[:n_i n_j:] = mu_i mu_j + |P_ij|^2 - 2 sum_a Q_ia Q_ja.
    Cov_B = diag(mu)+|P|^2-2QQ^T.

Consequently E[n]=mu, sum n=r, sum mu=r and Cov_B 1=0. For D the covariance
is diag(mu)-QQ^T. Continuous uniform phases and uniform complex-sphere
coefficients both satisfy E[zz*]=I/r, hence their multinomial counts also
have mean mu and total r. A covariance match does not match a discrete law.

If the implemented Gaussian factor is the REAL matrix F, its actual
covariance is FF^T, including every recorded numerical repair/mask. The
Gaussian final field must use HFg, while the independent final-variance
control uses independent normals with variances

    v_i = sum_a (HF)_ia^2.

These definitions exactly match FINAL variances for the actual factor, not
for a separately repaired nominal matrix. Significant PSD failures must be
inconclusive, not silently clipped. Apply the structural deterministic mask
to F BEFORE H. A zero-variance input row can receive fluctuations from its
neighbors; masking it again after H would be wrong. The f9689d2 card fixes
both points. Jitter must be independent of counts/Gaussian draws and fresh
per observation. Covariance/factor/PMF work belonging only to controls must
not enter B's resource allowance.

## H, ranking, inclusion and nulls

For dmax>0 and alpha0/1, H is symmetric nonnegative doubly stochastic.
The declared dmax=0 branch must use H=I, without division.
Its eigenvalues lie in[-1,1], so it is an L2 contraction. It need not be PSD
or damp the bipartite alternating mode: alpha1 can retain eigenvalue-1.
It preserves the sum of a centered physical count vector, but this alone
does not imply anything favorable about the balanced ranked cut.

For alpha=beta=0, exact topK retains every clicked mode if 0<mu_i<1 and
r<K: clicked scores are positive, empty scores negative, and their number
is at most r. Remaining modes are the smallest-mu empty modes, with fixed
ties; multiplicities above zero do not affect that partition. With bounded
jitter an exact-ranking sufficient margin is

    g=1-(mu_max-mu_min)-2 beta >0.

For the ACTUAL bucket decoder, g>0 is insufficient when opposite sides of
the ranking boundary merge in one bucket. A sufficient mathematical condition
is g>h, h=1e-12, with an additional allowance for bounded numerical error.
Fourier has constant mu=r/N and g=1 or.8, safely above h. The result is
support(n) subset S; P44's S subset support(n) obstruction does not cover it.

The79d3550 rule sets t=y-max(y), then ranks by floor(t/h+.5) and carried
priority. It is common-offset invariant in exact arithmetic, and a field
of range<h/2 lies in bucket0. Fixed boundaries still have rounding-sensitive
cases. Fixtures must cover both sides of a boundary, exactly uniform fields,
near-uniform fields and carried relabeling. No fixed tolerance guarantees
all recomputed floating spectra are exactly covariant at every boundary;
no nontransitive pairwise near-equality comparator should replace this rule.

Required physical distinctions for fixtures:

- r1: B,D,b4,phase and sphere are the SAME categorical law. Gaussian controls
  are not categorical. A product-of-B-marginals control, if added separately,
  is also not this physical one-photon law.
- Monomial V: B,D,b4 counts are deterministic, Cov_B=0, and their centered
  fields are pure jitter/ties. Phase/sphere at r>=2 remain stochastic; they
  must not be forced to satisfy this deterministic null.
- Column phases AFTER V and conjugation leave the named physical count LAWS
  invariant. Same-seed pathwise equality of backend samples is not implied.
  Phase/sphere pathwise fixtures need carried/conjugated coefficient vectors.
- Relabel A,V,marks,priority,counts and jitter consistently. Then H,mu and
  exact fields transform covariantly, and the ranked subset/cut follows.
  The spectral gauge is fixed BEFORE R; an arbitrary pre-R gauge is not a null.

For static n=0 the field is -Hmu+beta*zeta, not a mean-zero photon field.
For n=mu it is pure jitter/ties. With beta>0 fresh iid continuous jitter gives
uniform balanced subsets; beta0 with a fixed priority repeats one partition.
Fourier static fields are a constant plus jitter for BOTH alpha choices,
so they duplicate these laws. The card explicitly retains their predeclared
allocation; they are not separate discoveries. Static E need not be uniform
and can expose graph-dependent preparation/rounding bias without photons.

## A precise analytic veto of a diffusion interpretation

Take the simple unweighted graph K_(k,k), N=2k. This is an analytic witness,
not an added/selected DEV graph. Then dmax=k and at alpha1, H=A/k. For any
zero-sum field z, let t=sum_(left) z. Exactly,

    (Hz)_left=-t/k,    (Hz)_right=t/k.

If t!=0, beta0 topK returns ONE ENTIRE SIDE. Its cut is k^2, the maximum;
the minimum balanced cut is ceil(k^2/2), since choosing a left and k-a right
vertices gives a^2+(k-a)^2 crossing edges.

For the Fourier source with odd r (including13 or17), mu=r/N and
t=n_left-r/2 is a half-integer, hence NEVER zero for any count outcome.
Thus every B/D/b4/phase/sphere shot in this branch returns the maximal cut,
irrespective of interference. The inter-side score gap is at least1/k,
so the1e-12 tie bucket does not rescue this witness at the proposed sizes.
This refutes a universal claim that alpha1 diffusion followed by ranking
improves min-bisection. The cards promise no such theorem, and this is NOT
a refutation of the fixed ER/RR panel, alpha0 branch or the broader goal.

## Scope and next gate

Removing PIT means B>Gaussian can reflect discrete marginal shape as well as
joint higher-order correlations. The separately documented product-marginal
classical control tests that explanation and was prospectively adopted in
ded2cfb; it is not retroactively inserted into the earlier card hashes.
Its probabilities are the ordinary z coefficients AFTER the shifted PGF
transform, not the h!e_h shifted coefficients themselves. Source ports, r versus K,
all occupations, eta1, no herald/postselection and independent model training
must remain explicit. Loss calibration or a device feasibility conclusion
cannot be inferred. The next obligation is exact-source implementation review
and targeted qualification under the independently frozen execution closure,
not a favorable interpretation of these identities.

Actual commands: read-only git-show/stat, git-rev-parse and shasum on cards;
no model import or numerical run. This new review alone is authored in the
isolated replication worktree; ROOT cards/code/raw/paper are untouched.
