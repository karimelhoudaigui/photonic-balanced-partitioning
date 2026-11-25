# P75 small-case exact-hash independent review

Primary verdict: **proved as written for the internal small-case results
and their stated consequences**. The complex k=2 and k=4 bounds are sharp,
the proposed k=6 Frobenius extension is genuinely false, and none of the
three analyzed six-mode families refutes the probability conjecture.
The general k=6 inequality remains unproved by this artifact and this
audit. No correction to the scoped mathematical statements is requested.

## Exact artifact, exclusions and coverage

Reviewed ALL 179 lines of ROOT's
`research/P75_Gaussian_CF_overlap_route.md`, SHA256
`9015bc5e484c4a01696c04ea84a78906f8373a46d52f6339396a32185715fdfd`,
identified by ROOT as original `4248181` / root `cb2bf6c`.
This review is pinned to the file hash. It covers normalization,
compression, both complete proofs, equality constructions, the failed
six-mode norm lemma, safe families, the bunched-target caveat, conjecture
status and independent-color application.

The three source-citation records in section 6 were read as part of the
artifact but were NOT independently revalidated against primary texts
in this audit. Their numerical external fidelity values, bibliography and
claimed extraction provenance are not promoted to proved evidence here.
None is a premise of the reconstructed proofs. This is not a novelty
review or a declaration about every later research artifact.

Review date: 2026-11-25, worktree `.local/p66-dark-barrier`, starting at
`5586b13b84d4c0f5dc8d929d05a522d4ae818e13`. Only this review file is added.
No P75b/P75c output, code, test, numerical contract, other agent derivation
or review was opened. No imports, AST, RNG, numerical probability query,
test, backend, external source acquisition, physical sample, QPU or
manuscript action was used. All checks below are hand derivations from
the allowed source and definitions.

## 1. Exact class, pure-state normalization and complete event

The stated class is finite-mode, pure, zero-displacement Gaussian with
complex symmetric Z and ||Z||op<1. In Takagi coordinates, each mode has
pair exponential coefficients s^n sqrt((2n)!)/(2^n n!), with squared
unnormalized norm (1-|s|^2)^(-1/2). Multiplication gives the source's
amplitude factor det(I-ZZ^dagger)^(1/4).

This complex reduction need not assume Z real. One direct justification
uses the antilinear map T(v)=Z conjugate(v). Symmetry of Z gives
T^2=ZZ^dagger and <Tv,w>=<Tw,v>. On an eigenspace of T^2 with eigenvalue
s^2>0, T/s is an antilinear isometric involution. Its fixed vectors have
real mutual inner products and span the space over the complex numbers
by v=(v+Jv)/2+i(v-Jv)/(2i). Real Gram-Schmidt gives an orthonormal fixed
basis there; T vanishes on its zero eigenspace. Collecting those bases
gives Z=U diag(s_i) U^T. Thus the one-mode norm calculation applies to
the complete complex symmetric class, including diagonal pair terms.

For k distinct singly occupied output modes S and vacuum EVERYWHERE else,
the creation-exponential coefficient is haf(Z_SS). Pair ordering and the
exponential factorial cancel, while all target occupation factorials are
one. Squaring the normalized amplitude gives precisely

    q_Z(S)=sqrt(det(I-ZZ^dagger)) |haf(Z_SS)|^2.

The determinant exponent is one half for ONE source. It is not the
two-color determinant of P73. Odd k gives zero by total even parity;
k=0 is a vacuum probability at most one. Displacement, mixed states,
unobserved-output tracing, clicks and bunched occupations are correctly
excluded from this claim.

## 2. Vacuum-auxiliary compression is a raw-probability inequality

Write Z=[A B;B^T C] around S, and M=I-ZZ^dagger>0. Then
M_SS=I-AA^dagger-BB^dagger<=I-AA^dagger and M_aux<=I. The positive
Schur complement M_aux-M_aux,S M_SS^(-1) M_S,aux is no larger than
M_aux. Determinant monotonicity on positive matrices therefore gives

    det M <= det M_SS det M_aux <= det(I-AA^dagger).

Compression also gives ||A||op<1. The hafnian has not changed, proving
q_Z(S)<=q_A(all k modes). This includes a zero-dimensional auxiliary
block with determinant one. The monotonicity step is justified by
conjugating ordered positive matrices by the inverse square root of
the larger one; the resulting eigenvalues do not exceed one.

Equivalently, the all-vacuum auxiliary projection leaves a pure Gaussian
with pair matrix A, multiplied by a herald amplitude of magnitude at most
one. Keeping that raw factor is essential. The proof does not replace
the complete event by a conditional click or trace over arbitrary
auxiliary counts. Uncoupled vacuum auxiliaries preserve the equality
examples below.

## 3. Sharp k=2 and k=4 bounds, including complex diagonals

For k=2, write A=[a c;c b], x=|c|^2<1. The determinant of I-AA^dagger
is the product of its positive diagonals minus the nonnegative squared
off-diagonal magnitude. Its diagonal product is at most (1-x)^2. Hence

    q_A=x sqrt(det(I-AA^dagger))<=x(1-x)<=1/4.

This calculation is valid for arbitrary complex a,b,c. Choosing a=b=0
and |c|^2=1/2 attains 1/4 with a physical finite two-mode squeezed state.

For k=4, put T=Tr(AA^dagger) and x=T/4 in [0,1). The three matching
terms in its hafnian obey

    |haf A|<=1/2 sum_{i<j}|a_ij|^2<=T/4=x.

Each product is bounded by half the sum of its two squared magnitudes.
The six off-diagonal entries are counted twice in the Frobenius norm;
the additional diagonal squares are nonnegative. The coefficient 1/4
is therefore correct, including nonzero complex diagonal entries.

For the four singular values, AM-GM gives

    sqrt(det(I-AA^dagger))
       =[product_i(1-s_i^2)]^(1/2)<=(1-T/4)^2=(1-x)^2.

Thus q_A<=x^2(1-x)^2<=1/16. Compression proves the same bound for any
larger pure source with all remaining modes tested at vacuum. No real,
zero-diagonal, phase-aligned or numerical assumption has entered.

Two disjoint two-mode squeezed pairs with pair magnitudes 1/sqrt(2)
attain 1/16: each specified |1,1> pair event has probability 1/4.
Their singular values are below one. More generally k/2 such pairs attain
2^(-k) for every even k. For k>=6 this is only an achievable construction,
not a universal upper bound.

## 4. Six modes: a failed norm lemma, not a probability falsifier

For A=t(J6-I6), 0<t<1/5, the singular norm is 5t<1. There are
5*3*1=15 perfect matchings, so haf A=15t^3, whereas T=30t^2.
The proposed Frobenius envelope is 5sqrt(5)t^3, which is smaller since
3>sqrt(5). This is a physical analytic refutation of that norm lemma.

The normalized target probability, however, is

    q_A=225t^6 sqrt((1-25t^2)(1-t^2)^5)
        <=225/5^6=9/625<1/64,

where the last comparison is 576<625. It cannot refute the desired
probability bound. Strict finite squeezing, determinant normalization
and distinction between the norm lemma and the final probability claim
are all retained by the source.

The two additional families are safe exactly as stated:

- Rank one A=s u u^T, ||u||=1: the hafnian is
  15s^3 product_i u_i. AM-GM gives product_i|u_i|^2<=6^(-6).
  The determinant square root is sqrt(1-|s|^2)<=1 and |s|<1, so
  q_A<=225/6^6=25/5184<1/64. Arbitrary complex phases and diagonals
  in this family do not change that conclusion.
- Isotropic bipartite A=s[0 V;V^T 0], V unitary of size three:
  AA^dagger=|s|^2 I6, haf A=s^3 perm V. The permanent is a normalized
  three-photon CF transition amplitude of a passive unitary, bounded
  by one by unitarity and Cauchy-Schwarz. Thus
  q_A=[y(1-y)]^3 |perm V|^2<=1/64, y=|s|^2. A permutation V and
  y=1/2 attain equality.

Neither family exhausts general complex symmetric six-mode contractions.
In particular the isotropic result is not a proof for every bipartite
matrix with unequal singular values. No numerical search or evidence
from any other P75 artifact is used to extend these scopes.

The bunched-pattern warning also passes: a two-mode squeezed state has
probability (1-y)y^2 for |2,2>. At y=2/3 this is 4/27>1/16. It is
a four-photon event on TWO occupied modes, not the k=4 CF event on four
distinct modes with unit occupations. It is outside the conjecture.

## 5. Exact independent-color consequences and the joint-source boundary

For P73, N=2k and each color occupies k distinct specified modes while
its other modes are vacuum. For k=2 or 4, each pure zero-displacement
source contributes at most 2^(-k), even with arbitrarily optimized complex
pair matrices and all physical finite strengths. Conditional independence
of the two colors given their chosen source parameters then gives

    q(S)<=2^(-2k)=2^(-N).

Identical red/blue matrices are unnecessary. Uniform oriented balanced
proposals have mass 1/binom(N,N/2)>2^(-N) at each feasible S. Therefore
the raw pointwise and eventwise proposal comparison closes that model's
finite-strength window at N=4 and N=8. Failed pulses, vacuum and all
wrong counts remain paid. This does not compare their conditional laws,
matched CPU, photons or wall time. Additional preparation heralding can
only reduce the raw candidate mass if failure supplies no candidate.

The factorization must not be applied to a quantum-correlated joint
Gaussian source. Its accepted colored pattern has N distinct occupied
modes in one larger source and needs the one-source theorem at k=N.
The proved k=4 result therefore covers a joint total-four-photon event;
it does not cover a joint total-eight-photon event by squaring itself.
That distinction in the source is correct. Odd k independent colors
have zero accepted probability by their individual parity.

The first missing universal case remains the full complex six-mode
inequality in the reviewed route. Squaring its proposed q<=1/64 bound
gives the equivalent falsifier threshold

    det(I-BB^dagger) |haf B|^4 > 1/4096,

only for a physical contraction with I-BB^dagger positive definite.
A strict certified complex violation would address that broad conjecture;
it would not automatically refute P73's real nonnegative zero-diagonal
source subclass or establish an optimization benefit. This audit supplies
neither such a violation nor an all-six-mode upper proof.

## Closure

| Obligation | Result |
|---|---|
| Exact 179-line source hash and full text read | Passed |
| Pure zero-displacement complex Gaussian normalization | Reconstructed |
| Complete CF event and square-root determinant | Passed |
| Vacuum-auxiliary Schur compression | Passed without herald renormalization |
| Sharp complex k=2 and k=4 bounds, arbitrary diagonals | Passed analytically |
| Finite TMSV equality examples | Passed; not an all-k upper proof |
| Physical k=6 Frobenius counterexample | Passed; not a probability counterexample |
| Rank-one and isotropic bipartite six-mode families | Passed within those nonexhaustive families |
| Bunched target and joint-source boundary | Passed |
| Independent-color N=4/N=8 all-strength raw screen | Passed under the stated source/count model |
| General complex k=6 | Incomplete in this artifact and audit |
| Three external citation/fidelity records | Not revalidated; no numerical claim used as proof |

No load-bearing gap was found in the internally proved small-case
statements. Their strongest safe scope is the stated pure, undisplaced,
complete-count class and its independent-color raw-proposal consequence.
There is no authorization or need here for a four-mode numerical search,
and no six-mode numerical result is admitted by this review.

Only text reads, exact hashing and hand proofs support this review.
Git whitespace checks accompany its commit. Final mathematical
proofreading covered determinant exponents, complex conjugations,
Frobenius factors, equality parameters, six-mode physicality and the
independence versus joint-source distinction. No original artifact,
scientific code, data or other agent work was changed.
