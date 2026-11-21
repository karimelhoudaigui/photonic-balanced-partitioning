# Occupation objective: exact moments and same-frame bosonic mean dominance

Base: `2996904f861a5db2a732e38dbc97bd6c91e5708b`.
Scope: ideal lossless passive optics, one photon in each of k distinct input
modes, m>=k>=0. V is the m-by-k occupied-column frame, V*V=I_k.
The root proposed the dominance identity; this component audit independently
reconstructed its coefficients and finite references after seeing that proposal.
This is not an author-blind independent proof certificate. **Novelty OPEN; the
low-order correlation inputs are known.** No optimization or hardware claim.

## Definitions and moments

For real nonnegative weighted edges w_ij and mu>=0 let

    H(n) = sum_edges w_ij (n_i-n_j)^2 + mu M(n),
    M(n) = sum_i n_i(n_i-1)/2.

Use P=V V*, q_ia=|V_ia|^2, a_i=sum_a q_ia,
b_i=sum_a q_ia^2, C_ij=sum_a q_ia q_ja. The distinguishable reference independently
scatters one labelled particle from every occupied input column and then forgets
its label. It is not an iid multinomial with the columns averaged together.

Both models have E[n_i]=a_i. Direct normal ordering on the single-occupation
Fock input, or expansion of independent labelled categorical variables, gives

| moment | indistinguishable bosons | distinguishable particles |
|---|---|---|
| E[n_i^2] | a_i+2(a_i^2-b_i) | a_i+(a_i^2-b_i) |
| E[n_i n_j], i!=j | a_i a_j+|P_ij|^2-2 C_ij | a_i a_j-C_ij |
| E[M] | sum_i(a_i^2-b_i) | (1/2)sum_i(a_i^2-b_i) |

For the bosonic factorial diagonal moment, the two annihilation orders and two
matching creation orders give 4 sum_(a<b) q_ia q_ib=2(a_i^2-b_i).
For i!=j, the direct routing terms give a_i a_j-C_ij and the exchange terms give
|P_ij|^2-C_ij. These derive the stated normalization and factors without Fock
probability renormalization. Distinguishable moments follow from excluding the
same labelled photon from two simultaneous detections.

Each mean H is quartic in entries of V (with quadratic mean terms). It can be
evaluated on edges in O((m+|E|)k) arithmetic, after an O(mk^2) orthonormality
check, without enumerating Fock states or computing a permanent. An exact scalar
objective being cheap does not make its nonconvex minimization easy.

V is a frame, not just its column-space projector: a right rotation V R can
change b_i,C_ij and the Fock state even though V R R* V*=P. For example identity
versus a two-mode HOM rotation have identical occupied-column projectors but
different collision moments. Stiefel coordinates must retain this information.

## Ground-state proposition and assumptions

Fix total occupation sum_i n_i=k with 0<=k<=m. In the collision-free sector,
H equals the ordinary cut C_G(x). Let W=sum_edges w_ij. Every collision has
M(n)>=1, and every graph term is nonnegative, so H(n)>=mu for such a state.
Every collision-free cut has cost <=W. Thus if **mu>W**, all full-Fock ground
states are collision-free and the ground energy equals the cardinality-k cut
optimum (minimum bisection when m=2k).

No C* is needed to compute H or its expectation. A permutation routing to a
known optimal k-subset attains that ground energy in both statistics. Therefore
both variational families have the same global minimum C*, although finding
that routing remains the combinatorial problem.

The sufficient penalty can be sharpened to mu>C_G(S0) for any known feasible
k-subset S0, since C*<=C_G(S0). Constructing/scoring such a bound is classical
preprocessing to be charged; this observation supplies no quantum improvement.

The weight hypothesis matters. With m=4,k=2, one edge of weight -1 and mu=1,
mu>W=-1 holds, but collision (2,0,0,0) has H=-3 while the best CF cut is -1.
The implemented component rejects negative weights. Omitting the collision
penalty also fails in general: a triangle plus an isolated fourth mode has
best balanced cut 2, but occupation (0,0,0,2) has graph cost 0.

## Dominance proposition

For each occupied input pair a<b define z_i^(ab)=V_ia conjugate(V_ib).
The two models have the same mean vector. Their raw second-moment/covariance
difference is

    Delta = Cov_b(n)-Cov_d(n)
          = 2 sum_(a<b) Re[z^(ab) z^(ab)*].

Proof: on the diagonal,
Delta_ii=a_i^2-b_i=2 sum_(a<b)|z_i^(ab)|^2. Off diagonal, expanding |P_ij|^2
and removing its a=b terms gives
Delta_ij=|P_ij|^2-C_ij=2 sum_(a<b) Re[z_i^(ab) conjugate(z_j^(ab))].
For every real vector c,

    c^T Delta c = 2 sum_(a<b) |sum_i c_i z_i^(ab)|^2 >= 0.

Hence Delta is positive semidefinite as a real covariance matrix. Orthogonality
of occupied columns gives sum_i z_i^(ab)=0, consistent with Delta*1=0 and fixed
total particle number. The vacuum and one-photon cases have empty pair sums.

Applying the identity to every edge difference and to M gives the exact formula

    E_b[H]-E_d[H]
      = 2 sum_(a<b) sum_edges w_ij |z_i^(ab)-z_j^(ab)|^2
        + mu sum_(a<b) sum_i |z_i^(ab)|^2
      >= 0.

For **mu>0**, equality holds exactly when every z_i^(ab)=0, equivalently the
occupied columns have pairwise disjoint output supports. Then the complete
bosonic distribution equals the independent-particle distribution. If mu=0,
equality only requires every z^(ab) to be constant on each positive-weight
connected component. On a connected graph its sum is zero, forcing disjoint
supports again. On a disconnected graph equality need not eliminate overlap.

More generally, any real positive-semidefinite quadratic form n^T A n plus any
linear term has a no-smaller bosonic mean for the same V. This is a quadratic
expectation statement, not a general multivariate convex-order assertion.

## Exact non-implication for physical success

Take m=4,k=2, the path edges (0,1),(1,2),(2,3), all of weight one, and mu=4>W=3.
Use the normalized Walsh matrix

    U = (1/2) [[1, 1, 1, 1],
               [1, 1,-1,-1],
               [1,-1, 1,-1],
               [1,-1,-1, 1]],

with photons in its first two columns. Its full output classes are:

| outcomes | count | bosonic probability per outcome | distinguishable probability per outcome |
|---|---:|---:|---:|
| double occupancy in one mode | 4 | 1/8 | 1/16 |
| CF pairs 01 and 23 | 2 | 1/4 | 1/8 |
| the other CF pairs | 4 | 0 | 1/8 |

The unique optimal bisection up to complement is 01|23, with C*=1. Consequently

    E_b[H]=11/2 > E_d[H]=4,
    P_success,b=1/2 > P_success,d=1/4,
    P_CF,b=1/2 < P_CF,d=3/4.

The mean dominance therefore cannot be promoted to dominance of optimum
probability, low-energy tails, or conditional CF cost. Nor does it compare two
independently trained optimizers, their discovery budgets, or their wall times.
This explicit exception is retained alongside the negative mean result.

## Prior work and disposition

Walschaers et al., *Statistical benchmark for BosonSampling*, New J. Phys. 18
032001 (2016), [published Eq. (3) and Appendix A](https://epub.uni-regensburg.de/33650/1/2016-NewJPhys-Walschaers-et-al.pdf),
already derives bosonic/distinguishable output correlations and their efficient
classical computation. Their U uses input-first indices; transpose to our
output-first V. Martinez–Font-Segura,
[arXiv:2602.09894v1, Sec. 3.6, Eqs. (39)–(41)](https://arxiv.org/html/2602.09894v1),
also gives general factorial and cross moments. These exact primary sources
were inspected. The displayed PSD/Laplacian specialization is derived here,
without claiming it is absent from earlier work. No exhaustive novelty search.

**Decision:** keep the component as an exact classical objective and a negative
mechanism audit. Stop the proposed justification that bosonic interference
lowers this convex occupation mean relative to distinguishable photons at the
same frame. The mathematical optimum encoding survives, but that does not
justify large training or quantum sampling as an improvement. Any tail-based
continuation needs a new explicit discriminator; it is not established here.
