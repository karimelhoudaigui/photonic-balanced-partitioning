# P85: bounded primary-source comparison for nonnegative Gaussian sampling

26 November 2026. **Disposition: substantial prior overlap; exact guarantees
must remain separated; publication priority is OPEN.** The broad idea of
classical simulation in the nonnegative-GBS class is already present in the
[2020 primary source](https://arxiv.org/html/1908.08068v3) and is not our new contribution.
A general covariance-sign implication is refuted below by a physical thermal
counterexample, while a separate internal proof preserves our pure subclass.
Neither fact establishes novelty or a positive graph-optimization advantage.

This is a scoped ADDENDUM to
`research/P78_BOUNDED_PRIMARY_LITERATURE_CHECK.md`, not a replacement or erasure
of that earlier three-source record. Only this P85 file is written. P84,
P79/P80 sources, experimental outputs, shared state and paper remain untouched.

## 1. Query, acquisition and independent-provenance contract

ROOT supplied two primary identifiers, the suspected inverse-sign step and
the candidate thermal matrix. The algebra and source implications below were
reconstructed here, but this is not a blind search, independent discovery or
external referee certification. Exactly FOUR adaptive web rounds inspected
only these TWO publications, through official arXiv abstract/HTML/PDF pages.
No wider database search, citation survey, third paper or forward search was
performed; no negative search is evidence of priority.

The literature-check skill and its cache/source-record instructions were read.
A read-only identifier/cache lookup found no project literature-record cache
directory or existing record for either identifier. Under the STATIC no-import
instruction, no Python cache helper or installer was invoked, no cache was
initialized, and no PDF/full text was retained or added to Git. Retained-source
SHA256: NONE; extraction status: available online, not locally retained.
Versioned URLs and the authentication observations below are the durable
locators. Mathematical verification is separate from source availability.

No scientific code/import, AST, test, RNG, numerical matrix, probability
query, native backend, QPU call or other agent contact occurred. All displayed
counterexamples and checks are exact hand algebra. P82 outputs were not read.
Source summaries are paraphrases; no passages are quoted.

## 2. Authenticated sources and bounded extraction

S1. Nicolás Quesada and Juan Miguel Arrazola,
[Exact simulation of Gaussian Boson Sampling in polynomial space and exponential time](https://arxiv.org/abs/1908.08068v3),
arXiv:1908.08068v3, revision16-Nov-2020. The abstract record identifies
Phys. Rev. Research2,023005(2020),
[DOI](https://doi.org/10.1103/PhysRevResearch.2.023005).
Equation locators here refer to the authenticated
[v3 HTML](https://arxiv.org/html/1908.08068v3), not assumed journal pagination:
II.1(1)–(4), II.2(20)–(23), II.4.4(32)–(33), III.1(34), Appendix A(35)–(50),
and the detector-cutoff identity Appendix B(51). II.4.4 and Appendix A were
read completely. They propose sequential approximate sampling using hafnian
determinant estimates. The pure kernel includes our source; the abstract
already claims polynomial approximate sampling. The estimator sample count
and stated subexponential error do not establish P80's uniform finite-bit
TV contract. Appendix B's separate cutoff analysis is not ignored.

S2. Alexey Uvarov and Dmitry Vinichenko,
[On randomized estimators of the Hafnian of a nonnegative matrix](https://arxiv.org/abs/2312.10143v2),
arXiv:2312.10143v2, revised6-Mar-2024, first submitted15-Dec-2023.
Checked [HTML](https://arxiv.org/html/2312.10143v2) II propositions1–2,
II.1(7)–(9), II.2 in full, and IV's concluding sampling comparison;
[PDF](https://arxiv.org/pdf/2312.10143v2) authenticates11pages and printed
date7-Mar-2024. The HTML's rendered dateline24-Aug-2026 conflicts with that
version metadata; we retain the arXiv/PDF version, not a supposed2026 revision.
Their determinant estimators are unbiased but can have exponential relative
variance. Particular component/bridge preprocessing helps some examples;
this is not a hardness theorem for all samplers. Their empirical low-order
correlations are not a TV certificate.

Authentication, extraction and mathematical application are distinct checks.
In particular an authenticated broad claim is not automatically a verified
uniform algorithmic guarantee.

## 3. Exact notation translation: same complete raw pure-state law

The following is our algebraic application of S1's displayed conventions,
not a quoted additional theorem. To avoid a symbol collision, use Z for
OUR m-by-m pair matrix and J_sig for the paper's uncertainty-signature matrix.
Their pure-state B is exactly our Z, with Z real symmetric, entrywise
nonnegative and ||Z||op<1. In their doubled ordering put

    A=diag(Z,Z),  X=[[0,I],[I,0]],  K=X A=[[0,Z],[Z,0]],
    Q=(I-K)^(-1),  Sigma=Q-I/2.

For a repeated occupation n, the doubled matrix is
A_n=diag(Z_n,Z_n). Perfect matchings factor over its blocks, so

    haf(A_n)=haf(Z_n)^2,
    det(Q)^(-1/2)=sqrt(det(I-Z^2)),
    p(n)=sqrt(det(I-Z^2))*haf(Z_n)^2/product_i n_i!.

This is the project's FULL PNR source, including vacuum, collisions and
arbitrary total counts, not merely a normalized collision-free subset law.
Rational Z in P80 is a restricted input encoding of this same physical
class. There is no interpretation in which renaming B as Z removes overlap.
Implication label: **verified** for this target-distribution identification;
overlap label: **known after translation of notation**.

## 4. General inverse-sign claim: a fully physical counterexample

The suspect implication is entrywise nonnegative SPD Q -> Q^(-1) is an
M-matrix, used between S1's(37) and(38). Here is an independent exact test
that includes the quantum covariance requirement, not just arbitrary SPD.

Define the real symmetric occupation-correlation matrix

    N=[[1,3/5,1/10],
       [3/5,1,3/5],
       [1/10,3/5,1]].

Its leading principal minors are

    1, 16/25, det(N)=171/500,

so N is strictly positive definite. Diagonalize it by a real orthogonal
mode transformation and prepare independent thermal states with its positive
eigenvalues as mean occupations. Transforming their modes back gives a
valid zero-mean gauge-invariant Gaussian state with correlation N and zero
anomalous moment. Thus, in the doubled complex ordering,

    Sigma=diag(N+I/2,N+I/2),
    J_sig=diag(I,-I),
    Sigma+J_sig/2=diag(N+I,N)>0.

Sigma and Q=Sigma+I/2=diag(I+N,I+N) are entrywise nonnegative. This state
satisfies the required physical uncertainty condition, even though it is
mixed and thermal. Nothing here assumes squeezed-source hardware access.

Let H=I+N. Exact three-by-three cofactor algebra gives

    det(H)=1653/250,
    (H^(-1))_13=[(3/5)^2-2*(1/10)]/det(H)
               =(4/25)/(1653/250)=40/1653>0.

For C=I-H^(-1), therefore C_13=-40/1653. The actual doubled hafnian kernel
is

    A=X(I-Q^(-1))=[[0,C],[C,0]],

and A_(1,6)=-40/1653<0. An M-matrix must have nonpositive offdiagonals;
Q^(-1) does not. Physicality, SPD and entrywise nonnegative covariance
therefore do NOT justify that general sign implication. Spectral bounds
on an inverse do not fix its offdiagonal entry signs.

Implication label: **inapplicable as a general proof step; refuted by this
physical example**. This conclusion targets that implication, not all of
S1, and is not a novelty argument. The example is outside the pure encoded
subclass used by P78/P80, whose marginal signs are proved next.

## 5. Pure nonnegative sources retain nonnegative marginal kernels

For OUR class use K from section3. It is symmetric, entrywise nonnegative,
||K||op=||Z||op<1, and Q=(I-K)^(-1). Partition doubled coordinates into
retained R and eliminated T, with R containing both copies of each retained
physical mode. The inverse covariance is M=I-K. Block elimination gives

    (Q_RR)^(-1)=M_RR-M_RT*(M_TT)^(-1)*M_TR.

Because K_TT is a symmetric principal compression of K, its norm is below
one. Its Neumann inverse (I-K_TT)^(-1)=sum_(j>=0)K_TT^j is entrywise
nonnegative. Substitution yields the exact entrywise identity

    I_R-(Q_RR)^(-1)
       =K_RR+K_RT*(I_T-K_TT)^(-1)*K_TR >=0.

For T empty the second term is zero. The reduced X_R is a permutation
matrix, hence A_R=X_R[I_R-(Q_RR)^(-1)] is entrywise nonnegative too.
This proves the required closure directly; it does not rely on the false
converse inverse-sign assertion from section4 or an unchecked M-matrix
citation. Joint prefix probabilities use these Gaussian marginals; no
Gaussianity after photon-number conditioning is assumed.

Consequently the general counterexample does NOT remove S1's overlap with
our pure targets, nor create priority for our source subclass. The correct
implication here is **verified by the internal block identity**. It remains
separate from an efficient accurate hafnian estimate or end-to-end sampler.

## 6. Why an unbiased determinant is not a uniform sampling guarantee

The following simple calculation is our own hand check for the unmodified
Godsil-Gutman determinant average. It illustrates an estimator limitation,
not a lower bound on all algorithms or on raw sampling.

For one four-cycle with unit edges, take independent Rademacher edge
variables. Its skew determinant is (a+b)^2 with a,b independent uniform
signs. It is4 with probability1/2 and0 otherwise; its mean is2. For k
independent disjoint four-cycles, the determinant D is4^k with probability
2^(-k) and0 otherwise. Thus

    E D=2^k,  E D^2=8^k,
    Var(D)/(E D)^2=2^k-1.

An average of M such draws is zero unless at least one nonzero draw
appears. Its chance of even being positive is at most M*2^(-k). Achieving
success probability2/3 for relative error strictly below one therefore
requires M>=(2/3)*2^k for this plain estimator. This is a direct probability
lower bound, not an invalid inference from variance alone. Factoring the
known components changes the algorithm and fixes this particular example.

Rescale the four-cycle adjacency by any fixed rational c with0<c<1/2:
Z=c*A_cycleunion is a legitimate nonnegative pure contraction. Homogeneity
scales determinant samples and their mean by the same factor, preserving
the zero-hit and relative-variance obstruction. Duplicating Z in the full
kernel simply duplicates the blocks. Yet a different raw sampler, such as
the internally derived loop construction, is not constrained to estimate
these rare probabilities. Thus no estimator failure is misreported as
hardness or quantum advantage for this source family.

## 7. P78/P80 scope comparison and attribution decision

The local P80 finite-bit route read for this comparison is
`research/P80_finite_precision_loop_sampling_route.md`, SHA256
`5fa9ce9441691b639a8208b536172fa67ba6972edb01ea7bb45990eb0050b10b`;
the rational killed-walk derivation is
`theory/P80_independent_rational_loop_sampler.md`, SHA256
`fcc0150467adda7b509018d2ec440e52e7e40e053b0fe8124aae384a930d5b02`.
Those are project proofs, not conclusions imported from the two papers.

P78's stated mathematical construction is exact in its ideal primitive
model, with explicit positive loops and expected proposed transitions
<=m*meanphotons. P80's rational version and separate finite-bit bridge
specify rational input encoding, finite random bits, bounded work, overflow
flags and a full raw TV budget polynomial in m,B,meanphotons,1/epsilon.
They do not claim practical speed, exact bounded-bit sampling, cheap rare
conditioning or a positive optimizer. Their validity depends on their own
reviewed proofs; this source check does not replace those audits.

The missing implication from a noisy point-probability estimator to that
contract is substantial: uniform error control must cover all conditional
prefixes, normalization, unbounded tails, estimator failures, precision and
total random-bit/work costs. A detector-cutoff identity covers one error
source only. No source assertion, finite estimator budget or low-order
correlation agreement supplies all these obligations automatically.

| Comparison arrow | Checked disposition |
| --- | --- |
| Pure physical target identification | Verified; known after notation translation |
| Broad claim of approximate efficient nonnegative-GBS sampling as our new contribution | Reject that attribution; prior primary claim exists |
| General nonnegative-covariance sign argument | Refuted for physical thermal covariance; section4 |
| Our pure-source marginal sign closure | Verified internally; section5, so prior overlap survives |
| Determinant-estimator accuracy -> P80's uniform TV/bit-cost contract | Not verified; explicit additional bounds required |
| The two estimator families as a lower bound on all raw samplers | Inapplicable |
| Exact loop mechanism / photon-cost / finite-bit guarantee priority | OPEN; partial or adjacent result only in this bounded comparison |

This two-paper check is insufficient for an apparently-new designation.
The earlier literature record also found established loop-soup ingredients;
neither source omission nor a refuted broad auxiliary claim restores a
global novelty argument. Preserve all prior claims/results with calibrated
attribution rather than claiming a first general dequantization theorem.
The positive interference-dependent optimizer objective remains OPEN.

## 8. Handoff and unresolved obligations

Source authentication and target-notation translation are complete within
the explicitly named versions. The physical counterexample and pure closure
are internal exact derivations requiring their own independent review if
used as load-bearing claims. A broader priority comparison and any proposed
publication wording are NOT completed or authorized here. No P78/P80/P84
source, status file, manuscript or experiment was modified; no runtime or
numerical result is asserted. Only this report and its isolated Git freeze
accompany the four bounded primary web rounds.
