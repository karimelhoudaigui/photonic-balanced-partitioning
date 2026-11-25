# P47: a cost-directed polar step, its scope and an exact stall

Analytic checkpoint, physics owner, 2026-11-25. Base worktree commit:
`a6d7a278654099ac970b2defb0e06c0896fd6a02`. This note changes no P46
definition, code, command, data or outcome. It contains a self-contained
derivation, not an independent third-party validation. No P47 numerical
calculation, implementation, sampling or QPU call was performed. The
prospective rule below is fixed before any P47 outcomes. Its performance
after a PIT/completion decoder is open.

## 1. Index convention and the graph proxy

Let the anchor be A={u_1,...,u_b}, its complement B={v_1,...,v_b}, and retain
the label ordering supplied to all controls before outcomes. For the
undirected weighted graph cut J and adjacency matrix A_graph, define the
INSIDE-by-OUTSIDE matrix

    D_ij = J(A-u_i+v_j)-J(A)
         = ell_(v_j)-ell_(u_i)+2(A_graph)_(u_i,v_j),
    ell = degree-2 A_graph 1_A.

This is the layout specified for encoding P46: W_ij has the same i,j
indices. There is NO additional transpose. In the hollow Hamiltonian
H=[[0,W],[W*,0]], the old u_i to new v_j transition is proportional to
conj(W_ij), so its intensity is indeed |W_ij|^2. A source that supplies a
vacant-by-occupied table must convert its layout once at that interface;
that alternative convention is not an instruction to alter P46.

Write Z=I-11*/b, R=ZDZ, sigma=||R||_op, and, if sigma>0, C=R/sigma. C is
REAL and ||C||_op=1. The reference F is the normalized complex Fourier
matrix, F_ij=exp(2 pi i (i-1)(j-1)/b)/sqrt(b). Define

    S_D(W)=sum_ij D_ij |W_ij|^2,
    s_C(W)=sum_ij C_ij |W_ij|^2.

For every unitary W, |W|^2 is doubly stochastic, hence

    S_D(W)=sigma s_C(W)+(1/b)sum_ij D_ij.                 (1)

Indeed D-R is a sum of a row field and a column field. Their contributions
are constant because both intensity marginals equal one. Thus centering
preserves the direction of this proxy. It does not turn the proxy into the
actual cut of a simultaneous multi-swap. All b^2 scored single swaps and
all matrix construction/norm/polar work belong to the shared classical
frontend and common incumbent.

## 2. Differential statement, including its factors

Use the real Frobenius metric <X,Y>=Re Tr(X*Y). For any real C, the ambient
gradient of s_C at F is 2G, where G=C odot F. The tangent projection is

    Pi_F(G)=G-F sym(F*G)=F skew(F*G),
    sym(B)=(B+B*)/2,  skew(B)=(B-B*)/2.                  (2)

Consider the AMBIENT step followed by the unique unitary polar factor,

    W_epsilon = polar(F-epsilon G).

For small epsilon, put B=F*G. Then

    F*W_epsilon
      =(I-epsilon B)[(I-epsilon B)*(I-epsilon B)]^(-1/2)
      =I-epsilon skew(B)+O(epsilon^2).

Consequently W'_0=-Pi_F(G), and orthogonality of the tangent projection
gives the exact first derivative

    (d/depsilon)s_C(W_epsilon)|_0 = -2||Pi_F(G)||_F^2,
    (d/depsilon)S_D(W_epsilon)|_0 = -2sigma||Pi_F(G)||_F^2. (3)

The derivative can vanish for a NONZERO graph signal C. A pure tangent
retraction polar(F-epsilon Pi_F(G)) has the same first derivative, but the
finite-step proof below is for polar(F-epsilon G), not for that substitute.

## 3. Finite descent and the prospective deterministic step

Let nu=||G||_op and c=max_ij |C_ij|. The new prospective rule is

    h=max(nu,c),
    epsilon_star=1/(4h) if h>0,
    W=polar(F-epsilon_star G) if h>0; W=F if h=0.        (4)

The entire R=0 branch also returns F. No graph class, zero branch or stall
is dropped, and no alternative reference is selected after outcomes. For
flat F, h=0 iff C=0. Rule (4) is deterministic given the graph and the
predeclared ordering. It uses neither optima nor optical outcomes.

For any epsilon>0 with epsilon nu<=1/4, Weyl's elementary singular-value
inequality yields

    sigma_min(F-epsilon G)>=1-epsilon nu>=3/4.            (5)

Thus the polar factor is unique. In particular (4) obeys (5) and
epsilon_star c<=1/4. Put Y=polar(F-epsilon G), E=Y-F. The polar factor is a
global nearest unitary in Frobenius norm: for an SVD M=L Sigma V*, maximizing
Re Tr(Y*M) over unitary Y gives Tr(Sigma), attained by LV*. Comparing its
distance to M=F-epsilon G with the competitor F gives

    ||E||_F^2+2epsilon<G,E><=0.                           (6)

The cost is a quadratic polynomial, so its change is exactly

    s_C(Y)-s_C(F)
       =2<G,E>+sum_ij C_ij |E_ij|^2
       <=-(1/epsilon-c)||E||_F^2.                       (7)

At (4), 1/epsilon_star-c=4h-c>=3h, hence

    S_D(Y)-S_D(F)<=-sigma(4h-c)||Y-F||_F^2<=0.            (8)

These are exact real-arithmetic statements. They do not require a small-step
Taylor remainder estimate or a line search. Strict decrease holds if Y!=F.
Under epsilon nu<1, Y=F is equivalent to Pi_F(G)=0: if F*G is Hermitian,
I-epsilon F*G is positive definite and its polar factor is I; conversely
polar(F-epsilon G)=F implies F*(F-epsilon G) is positive Hermitian.

For comparison only, ||G||_op<=1 for the normalized C above, and c<=1.
The fixed epsilon=1/4 therefore satisfies (5) and
s_C(Y)-s_C(F)<=-3||Y-F||_F^2. It is retained as a lemma, not proposed as an
additional pilot. To verify the norm bound without a Schur-product
assumption, the isometry V_diag e_i=e_i tensor e_i gives

    C odot F = V_diag*(C tensor F)V_diag,
    ||C odot F||_op<=||C||_op||F||_op=1.                 (9)

Flatness additionally gives ||G||_F=||C||_F/sqrt(b)<=1. By (6) and
Cauchy-Schwarz,

    ||Y-F||_F<=2epsilon||G||_F.                          (10)

The fixed quarter-step thus changes F by at most 1/2 in Frobenius norm,
independent of b. The adaptive rule removes this particular O(1) upper
bound: h may shrink with b. It does NOT give a lower bound on graph response,
nor guarantee extensive response or extensive improvement.

For completeness it retains a density safeguard. If V=F*Y, write
I-epsilon F*G=VK with K>0. For an eigenvector Vx=exp(i theta)x,
x*(I-epsilon F*G)x=exp(i theta)x*Kx lies in the radius-1/4 disk about 1.
Therefore

    ||Y-F||_op<=sqrt(2-2sqrt(1-1/16))=:kappa,
    |Y_ij|<=1/sqrt(b)+kappa,  kappa approximately 0.252. (11)

This prevents convergence to a monomial permutation as b grows. It does
not prove a favorable cost distribution or a computational obstruction.

## 4. A realizable strict-local-minimum graph where the step is zero

The following exact example prevents replacing nonincrease by a claim of
strict descent for every nonzero centered signal, even at an improvable
strict 1-swap minimum. It must remain in any future coverage.

Take b=4, old vertices 0,1,2,3, new vertices 4,5,6,7, in that order. Let
v=(1,-1,1,-1). Set every intra-old and intra-new edge weight to 17/16, and
set the old i to new j edge weight to 1+v_i v_j/8. All weights are positive;
the graph is undirected without loops. The anchor is the old block.

Its cut is 16. Every one-swap delta is

    D_ij=3/8+v_i v_j/4 in {1/8,5/8}.

Thus the anchor is a STRICT one-swap local minimum. The balanced candidate
{0,2,4,6}, obtainable by two swaps, has cut

    8(17/16)+8(7/8)=31/2<16.

Since Zv=v, centering gives R=vv*/4, sigma=1, C=R. Let D_v=diag(v), and
let P_2 be cyclic translation by two indices. For the above Fourier F,

    G=D_v F D_v/4,  F*D_v F=P_2,
    F*G=P_2 D_v/4.

P_2 commutes with D_v, so F*G is Hermitian with eigenvalues in {+1/4,-1/4}.
Also nu=c=1/4, so (4) chooses epsilon_star=1. The eigenvalues of
I-F*G are 3/4 and 5/4; it is positive definite. Hence

    polar(F-G)=F,  Pi_F(G)=0,  C!=0.                      (12)

The fixed quarter-step also remains at F. This is an analytic witness, not
a sampled failure or a claim that every reference ordering stalls. No
outcome-driven relabeling, reference replacement or witness exclusion is
permitted by this note. It refutes strict direction for every improvable
anchor, not (7), and not the possibility of useful copula effects elsewhere.

## 5. What the guaranteed direction does and does not buy

Since |W|^2 is doubly stochastic and permutations themselves are unitary,

    min_(unitary W) S_D(W)=min_(permutation pi) sum_i D_(i,pi(i)). (13)

This follows directly from the linear assignment relaxation/Birkhoff
decomposition. Polynomial classical assignment therefore already solves
this proxy globally (dense Hungarian arithmetic O(b^3)). The polar map is
a known classical constrained-gradient construction, not an optical
advantage. Its intensity direction and one-particle effects are shared by
bosons and distinguishable particles. Independent or matching proposals,
spectral/nonlocal controls and the common frontend receive the same D and
preprocessing budget. Finding a better scored classical move is credited
to that frontend.

Moreover S_D sums SINGLE-swap costs: the actual cut change of a block
contains interactions among its changes. In particular moving the entire
old block to its complement leaves an undirected balanced cut unchanged,
regardless of a favorable assignment proxy. Neither (3) nor (8) implies
better raw improvement probability, collision-free yield, final cut,
PIT copula, search efficiency or hardware performance. A future P47 test,
after P46, would need the same loss/collision-aware decoder, B/D/internal
species, phase and matched classical nonlocal controls, all tuning and
preprocessing charged. No such experiment is executed or claimed here.

## 6. Attribution, provenance and checks actually performed

Projection/polar retractions and tangent projection are established tools.
Primary context inspected: Absil and Malick, *Projection-like Retractions
on Matrix Manifolds*, SIAM J. Optim. 22(1), 135-158 (2012), DOI
[10.1137/100802529](https://doi.org/10.1137/100802529), author-hosted
[published PDF](https://sites.uclouvain.be/absil/2010-038_retractions/80252.pdf),
section 3.1 and Lemma 4 (printed p. 140). The author's
[record and errata](https://sites.uclouvain.be/absil/2010.038) were also
inspected. That real Euclidean-manifold source is context, not an assertion
that it supplies our complex graph constants or the witness. Equations
(1)-(13) were derived directly here. No novelty claim follows from this
bounded source check.

Actual local checks were reading AGENTS.md and the immutable P46 note,
checking branch/base/clean status, manual algebra including the explicit
graph cut and polar stall, and Git whitespace/scope plus file-hash checks
at commit. No Python, physical simulator, test suite, P46 CLI or raw data
was run/read for this P47 note. The changes are mathematical documentation
only; no claim of test execution is made. The separate blind claim card
permits an adversarial review without importing this owner's verdict.
