# Density certificate: second source review across matrix geometry

Checked 2026-11-22, approximately 02:13 UTC. This is a bounded attribution
review using the `mathbox:literature-check` workflow. It is not a manuscript,
an independent proof certificate, or a global novelty determination. The
reviewer had read the coordinator's Rioul inventory and the first photonic
source audit; this is an alternative search strategy by the same literature
agent, not a blind fresh-reviewer check.

Isolated branch: `research/phase3-density-second-review`; base commit
`e201f1c337cb780225bdcdd0a806cfd7d20d2fe2`. The only changed tracked file is
this report. Target `theory/phase3_density_certificate.md` has SHA256
`7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c`.
The first audit and coordinator inventory are, respectively,
`research/phase3_density_novelty.md` and
`research/phase3_density_crossfield_novelty.md`. Neither proof nor inventory
was edited.

## Finding

The dominant-support construction has a direct antecedent in optimization
over the **nonnegative Stiefel manifold**. Jiang, Meng, Wen and Chen already
keep a maximum entry in each row, zero the others and normalize columns.
Their proof also bounds the resulting distance using discarded squared mass.
The spatial Gram estimate then follows from an elementary perturbation of
that same rounded matrix. Neither the construction nor the matrix-norm step
should carry a standalone originality claim.

The Rioul row-impurity attribution is confirmed, with an important difference
between conditional-probability weights and physical pair-moment weights.
A quantum-state-discrimination result provides another verified Gram bound,
but its translation introduces a factor in the photon count.

The complete density-to-full-Fock-law envelope, with its specified constants
and sharp leading coefficient, remains **unattributed in this bounded
review**. That is not a positive novelty finding. Its strongest defensible
presentation is an explicit certificate assembled from established ideas,
with the exact application and sharp constant still requiring attribution
review. The result establishes no optimization benefit by itself.

## Exact statement being compared

Let the occupied optical frame be an m-by-k complex matrix V with orthonormal
columns, one photon in each of k distinct inputs. Set q_ia=|V_ia|²,
a_i=sum_a q_ia, delta=sum_i(a_i-max_a q_ia), and
M=sum_i(a_i²-sum_a q_ia²). Here M is the bosonic expected number of unordered
colliding pairs, not the probability of any collision. Compare the full
unconditioned bosonic occupation law p_b with the independent-particle law
p_d after forgetting labels. Keep collisions.

For the spatial magnitude Gram B_ab=sum_i sqrt(q_ia q_ib), the target is

    sigma = ||B-I||_F <= rho(delta),       rho(x)=2sqrt(x)+x,
    TV(p_b,p_d) <= min(1,f(rho(delta))),
    f(s)=(exp(-s)/(1-s)-1)/2,             rho(delta)<1.

Every positive a_i must be at least c>0. The observable substitution is
delta<=M/c, refined for M<c²/2 to

    delta <= d_c(M)=(c-sqrt(c²-2M))/2.

It yields the upper envelope M/(2c)+O(M^(3/2)) at fixed c. The coefficient is
attained asymptotically by the target's m=4, k=2 family with c=1/2. Average
density k/m is not this intensity floor. Neither internal distinguishability,
a few-output marginal nor collision-free conditioning is the target domain.

## Source J: the rounded nonnegative frame is known

Bo Jiang, Xiang Meng, Zaiwen Wen, Xiaojun Chen, *An exact penalty approach
for optimization with nonnegative orthogonality constraints*,
[arXiv:1907.12424v2](https://arxiv.org/abs/1907.12424v2), 2020-12-31,
32-page primary PDF. Introduction (1.6), §3.1, **Procedure 3.1 and Lemma
3.2**, pp. 9–10, equation (3.4), are the checked locators.

For nonnegative unit-column matrices X, their procedure retains one maximum
per row, with deterministic tie breaking, then normalizes columns; a fallback
handles empty columns. Nonnegative orthonormal columns have disjoint
supports. With their auxiliary matrix T satisfying ||T||_F=1 and
omega=min_ab(TT^T)_ab>0, their q=2 estimate is

    dist(X,S_+) <= ||X^R-X||_F
                   <= sqrt(2k/omega)*sqrt(||XT||_F²-1).

The proof's small-residual case bounds squared rounding distance by twice
discarded squared mass. Authentication, extraction and applicability to the
magnitude matrix X_ia=sqrt(q_ia) are **verified**. The construction is **known
after translation of notation**. Their theorem bounds distance by a Gram
residual, with dimension-dependent constants; it does not assert photonic
TV or the density-floor envelope.

Version warning: the later [author-hosted copy](https://www.polyu.edu.hk/ama/staff/xjchen/S-6.pdf)
uses Procedure 1/Lemma 3.1. Those are discovery locators, not the numbering
of the version pinned here. The source's auxiliary matrix, denoted V there,
is our T and is not the complex optical frame V.

### Explicit comparison, derived here rather than quoted from J

Use X=|V|, and let Y be its row-max truncation **before** normalization.
Write Z=X-Y. Then Y has disjoint column supports,

    ||Z||_F²=delta,     Y^T Y is diagonal,     ||Y||_op<=1.

The retained squared column masses are 1-l_a and sum_a l_a=delta. If
delta<1, each column is nonempty and the source's fallback is unnecessary.
Restoring the original phases on the retained entries gives exactly the
target proof's disjoint-support complex frame after normalization.

Moreover B=X^T X exactly. Hence the target Gram bridge has the direct form

    off(B)=off(Y^T Z+Z^T Y+Z^T Z),
    ||B-I||_F <= 2||Y||_op ||Z||_F+||Z||_F²
                <= 2sqrt(delta)+delta.

This derivation needs no grouped matrix C and no normalization of Y. It is
ordinary Gram perturbation applied to the already-known truncation; it is
**not asserted to be a verbatim theorem in J**. Its application verdict is
verified as this explicit elementary translation. Treating the isolated
bound as a substantial new geometric principle would be poorly supported.

## Source C: backward attribution independently confirmed

Xiaojun Chen, Yifan He, Zaikun Zhang, *Tight Error Bounds for the
Sign-Constrained Stiefel Manifold*,
[arXiv:2210.05164v7](https://arxiv.org/abs/2210.05164v7), 2024-05-19,
33-page primary PDF. **Lemma 7, equation (22), and Remark 2**, p. 11,
explicitly identify their row-max truncation with J's Procedure 3.1 and its
discarded-mass estimate with J's Lemma 3.2. **Theorem 5**, p. 13, gives

    dist(X,S_+) <= 5 r^(3/4)
        (||X_-||_F^(1/2)+||X^T X-I||_F^(1/2)).

Here X is any real n-by-r matrix and X_- is its negative part. Thus for our
nonnegative X=|V| this is a distance estimate in terms of sigma^(1/2), with
an r-dependent factor. It does not invert to the desired upper bound on
sigma or imply a bosonic-law bound. **Verdict:** verified geometric overlap,
**partial or adjacent result only** for the complete target. Numbering from
earlier versions or the original v1 title is not substituted for v7.

## Source R: the coordinator's row-impurity attribution is verified

Olivier Rioul, *The Interplay between Error, Total Variation, Alpha-Entropy
and Guessing: Fano and Pinsker Direct and Reverse Inequalities*, Entropy
25(7), 978, published 2023-06-25, DOI
[10.3390/e25070978](https://www.mdpi.com/1099-4300/25/7/978).
Checked the 31-page published author PDF: equations (3), (5), (22), (23),
and Example 16, equations **(75), (76)**, p. 20.

These identify R2=1-sum_a t_a² and Pe=1-max_a t_a; (75) gives the sharp
unconditional region, whose Pe<=1/2 lower branch is 2Pe(1-Pe). Equation
(76) gives conditional R2>=Pe. **Verdict:** verified, **known after
translation of notation** for the row quantities. Rioul also points to
earlier error/entropy work; this review does not claim Rioul's priority.

### Weight translation and remaining elementary aggregation

Take the input label uniformly in [k] and Pr(A=a,I=i)=q_ia/k. For a_i>0,
the label posterior is t_a=q_ia/a_i. Put e_i=1-max t_a and
g_i=1-sum t_a². Then

    delta/k = MAP label error,
    delta=sum_i a_i e_i,              M=sum_i a_i² g_i.

The ordinary conditional impurity averages with weights a_i/k, not a_i².
Thus M is not k times a conditional impurity. The intensity floor supplies
the missing comparison:

    M >= c sum_i a_i g_i >= c delta.

The elementary weaker row inequality g_i>=2e_i(1-e_i) holds also beyond
the first sharp branch: bound the squared off-maximum masses by e_i².
Together with the floor this yields

    M >= 2c delta-2sum_i(a_i e_i)² >= 2c delta-2delta².

The coarse bound and M<c²/2 select the small quadratic root. This is a
**formal corollary not stated**, not a new row inequality. Jensen alone
cannot supply the asserted quadratic conditional bound: e(1-e) is concave.

## Source M: a different Gram/classification route loses a dimension factor

Ashley Montanaro, *A lower bound on the probability of error in quantum
state discrimination*, [arXiv:0711.2012v2](https://arxiv.org/abs/0711.2012v2),
2008-03-11, four-page primary PDF, **Theorem 1**, p. 1. For any measurement,

    P_error >= sum_(a>b) p_a p_b F(rho_a,rho_b),

with squared fidelity F. Authentication and extraction are verified. Apply
it to unit vectors u_a=sum_i sqrt(q_ia)|i>, priors 1/k, and the measurement
that reads i then guesses its dominant label. Its error is delta/k and
F(u_a,u_b)=B_ab². Therefore

    delta/k >= sigma²/(2k²),           sigma² <= 2k delta.

This application is **verified**, a **formal corollary not stated**.
Although the source theorem uses no explicit dimension factor, equal-prior
normalization introduces k here. It does not recover the target's uniform
sigma<=2sqrt(delta)+delta. Nor are these positive-amplitude states the
orthogonal complex optical columns themselves. The PDF has an anomalous
body date in 2019; the identifier, arXiv revision stamp and bytes are pinned
to v2, not silently replaced with later v3.

## Complete-chain attribution and smallest unresolved item

| Arrow or component | Attribution after this review | Limit |
|---|---|---|
| Posterior row impurity and classification error | known after translation of notation, R | Physical moment has different row weights. |
| Floor-weight comparison and small-root inversion | formal corollary not stated of standard row inequalities | Requires all positive rows and the explicit small-M branch. |
| Max-row truncation, disjoint supports, normalization | known after translation of notation, J; confirmed by C | Cannot be sold as a new frame construction. |
| Delta-to-spatial-Gram bound | elementary Gram perturbation of J's truncation, derived explicitly above | Not located as a verbatim source theorem; that does not make it a research novelty. |
| Gram-to-full-law routing/permanent bound N1 | formal corollary not stated, Deshpande et al., as checked in the first audit | Occupation factorials and orientation require the project's proof. |
| Cycle/Frobenius envelope N2 | formal corollary not stated of MacMahon, as checked in the first audit | Infinite envelope requires sigma<1. |
| Complete minimum-positive-intensity full-law envelope and sharp coefficient | Exact attribution unresolved | No positive originality or publication-readiness conclusion. |

N1/N2 source checks are inherited from the pinned first audit, not freshly
repeated here. Its exact Deshpande version is arXiv:1703.05332v3, supplement
(S12)–(S16); the classical identity is Etingof–Pak's author copy, Theorem 1.
This review adds no theorem of those sources and does not hide their stated
locality conditions or the first audit's printed-normalization cautions.

The smallest still-unattributed candidate is the **explicit uniform
photonic composition** for this source/comparator/domain, with the
observable-only small-root substitution and the sharp M/(2c) leading
coefficient. The construction, statistical inequalities, perturbation
norms, independent-particle comparator, coupling and cycle majorant are
established ingredients. The two-photon sharpness mechanism is elementary
interference, not a newly identified phenomenon. Even the complete
composition might be regarded as a routine application of these ingredients;
this review cannot settle that editorial or originality question.

## Search coverage, authentication and reproducibility

The alternative strategy searched nonnegative orthogonality, row-max
rounding, Stiefel error bounds, Gram/Bayes error, Hellinger affinities and
spatial-support classical approximation. Web-index queries included:

- `"nonnegative orthogonality" "rounding" "Gram"`;
- `"nonnegative orthogonality" "rounding" Jiang Meng`;
- `"Hellinger" "Gram" "Bayes error" Frobenius`;
- `"Gram matrix" "Frobenius" "probability of error" Montanaro`;
- `"boson sampling" "spatial overlap" distinguishable bound`;
- `"boson sampling" "disjoint" classical simulation`;
- `"boson" "minimum" "intensity" distinguishable approximation`.

Primary-source restrictions were used for the focused follow-up queries.
The J-to-C citation chain was checked in the actual text. Rioul was checked
against the existing authorized local copy and publisher metadata rather
than inferred from the coordinator's summary. Other discovery candidates
and generic search hits do not support an absence claim. Coverage is
English-language, web/arXiv/publisher/author sources through 2026-11-22;
comprehensive citation indices and non-English literature were not covered.
No statistical sampling or numerical experiment was performed in this review.

Exact PDF bytes checked, with pypdf text extraction:

| Source/version | PDF SHA256 | Checked primary artifact |
|---|---|---|
| J, 1907.12424v2 | `ffaeb0e03cbd39b41271bc395463de399613e39e39a26b5e58aa3d758871f0db` | [arXiv PDF](https://arxiv.org/pdf/1907.12424v2) |
| C, 2210.05164v7 | `c29d66e98ee42ac82e67e0afe2f79fe1ac7dd2995932fac2a74a70e7d85dd1d8` | [arXiv PDF](https://arxiv.org/pdf/2210.05164v7) |
| R, published 2023 author copy | `57c700e2acbf48044d049f7458ad468e70e4aceaceaf0e1bb764728ca1683b4f` | [Author PDF](https://perso.telecom-paristech.fr/rioul/publis/202306rioul.pdf) |
| M, 0711.2012v2 | `9c6293e994e90ff69553281928779888b4e471ae9c55b8310fd64449cbe44f57` | [arXiv PDF](https://arxiv.org/pdf/0711.2012v2) |

R retains the project's existing ignored `.local/references/rioul_2023`
cache; the other downloads were read from temporary files. No full source
text, credentials or shared scientific state was added to Git. Hashes
identify bytes, not mathematical verification. This document-only review
does not run numerical tests or claim that prior passing tests certify
these attributions. Unresolved attribution remains **OPEN**.
