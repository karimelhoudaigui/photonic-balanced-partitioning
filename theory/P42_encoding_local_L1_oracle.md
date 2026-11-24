# P42 — a classical oracle for the proposed L1 occupation mean

Date: 2026-11-24. New analytic file; sealed P41/P42 files and the manuscript
are unchanged. No new program or experiment has been executed. This proof
was reconstructed while checking Monbroussou et al., arXiv:2607.24728v1;
it is a formal application of established marginal/low-rank methods, not
a claim of a new simulation theorem. Independent review is required.

## 1. Model and exact consequence

Write K for the project's photon count k, to distinguish it from a monomial
degree or an irrep index. Unless treating the trivial vacuum branch below,
assume 1<=K<=m. Let V be the m-by-K occupied-input column matrix
of a passive interferometer, V*V=I_K. The source is one perfectly identical
photon in each of K distinct spatial inputs. There is no loss, intermediate
measurement, feedforward or nonlinear optical gate in this model.

For a terminal occupation n, define

    F_G(n)=sum_(i<j) w_ij |n_i-n_j|,
    R_K(n)=sum_(i<j) |n_i-n_j|-K(m-K),
    J_G(n)=F_G(n)+lambda R_K(n).

The intended project domain has w_ij>=0 and lambda>=0, with absent edges
having w_ij=0. The exact marginal DP and linear combination also work for
signed coefficients; the weighted probability sampler in Section 5 has
the explicit nonnegativity restrictions stated there. If K=0, the only
occupation is vacuum, F_G=R_0=J_G=0, and no Fourier sampling is necessary.
The graph, lambda and an arbitrary circuit V
are supplied classically; no optimal cost, optimal masks or optimal partition
is needed. The proposed certificate choice lambda=(C0+epsilon)/(2(K-1))
is included when K>=2 and C0 is a scored feasible incumbent. Its construction
and scoring costs remain charged.

**Consequence.** The expectations of F_G, R_K and J_G can be computed using
a polynomial number of arithmetic operations by evaluating two-mode
marginals. There is an explicit O(m^2 K^4) arithmetic upper bound below,
with O(K^3) temporary coefficient memory per pair. Exact BIT computation
additionally requires controlled rational/algebraic input representations;
an ordinary floating-point output is not an exact certificate. Alternatively,
a simple bounded random-sign estimator gives inverse-polynomial additive
accuracy in polynomial time without constructing the entire Fock law.

Neither conclusion minimizes the graph cost, reproduces the full joint
occupation law, computes a conditioned CF tail, or proves a measured
wall-time comparison against a QPU.

## 2. A two-mode generating polynomial

For output modes i,j define column vectors

    a_alpha=conj(V_i,alpha),    b_alpha=conj(V_j,alpha).

The orientation is important: A_i=aa* has entry
conj(V_i,alpha)V_i,beta. The joint probability generating polynomial is

    G_ij(z,w)=E[z^(n_i)w^(n_j)]
       =per[I_K+(z-1)aa*+(w-1)bb*].                     (L1)

To see this, insert the diagonal one-particle matrix D with entries z at i,
w at j and 1 elsewhere between the output bra and ket. Contracting the K
creation/annihilation pairs gives per(V*DV). Since V*V=I_K, this is(L1).
Equivalently it is the Fock return amplitude of the phase circuit for |z|=|w|=1,
extended to all z,w by the polynomial identity. Define the factorial-basis
polynomial

    M_ij(x,y)=G_ij(1+x,1+y).

Its coefficients are binomial moments E[binom(n_i,r)binom(n_j,s)], not raw
factorial moments. This distinction determines the factorials below.

## 3. Explicit finite-rank coefficient algorithm

Introduce four formal variables u1,u2,v1,v2 and form

    H(u1,u2,v1,v2)
      =prod_(alpha=1..K) [1+
          (conj(V_i,alpha)u1+conj(V_j,alpha)u2)
          (V_i,alpha v1+V_j,alpha v2)].                   (L2)

Let d_(r,s,p,q) be its coefficient of u1^r u2^s v1^p v2^q. Then

    M_ij(x,y)=sum_(r+s<=K) r!s! d_(r,s,r,s) x^r y^s.     (L3)

In particular the RAW factorial moment is

    E[(n_i)_r (n_j)_s]=(r!s!)^2 d_(r,s,r,s),              (L4)

where (n)_r=n(n-1)...(n-r+1). Equations(L3) and(L4) must not be conflated.

Proof of(L3): expand

    per(I+A)=sum_(T subset[K]) per(A[T,T]).

For A=xaa*+ybb*, assign a label in{1,2} to the chosen row and column of
each entry. A label count (r,s) on the rows can be matched to the columns
only when the column label count is also (r,s). There are r!s! permutations
matching those labels. The product in(L2) aggregates the COMMON chosen
subset T and both assignments. Taking its diagonal coefficients and
multiplying by r!s! therefore gives precisely(L3). This accounts for all
subsets at once; it does not enumerate binom(K,r+s) surviving terms.

Each factor in(L2) has only five terms. Moreover every coefficient satisfies
r+s=p+q=d<=K. Thus it suffices to store (d,r,p), with s=d-r and q=d-p.
After processing a source mode alpha, the update is

    h'_d,r,p = h_d,r,p
       + |V_i,alpha|^2 h_(d-1,r-1,p-1)
       + conj(V_i,alpha)V_j,alpha h_(d-1,r-1,p)
       + conj(V_j,alpha)V_i,alpha h_(d-1,r,p-1)
       + |V_j,alpha|^2 h_(d-1,r,p).                      (L5)

Invalid indices are zero, h_0,0,0 starts at 1, and updates use an old/new
table or decreasing d. There are sum_(d=0..K)(d+1)^2=O(K^3) entries and K
updates, hence O(K^4) arithmetic. A naive four-dimensional grid instead
gives the still-correct upper bounds O(K^4) memory and O(K^5) operations.

Write B_rs=r!s!h_(r+s,r,r). Joint probabilities follow by binomial inversion:

    P(n_i=a,n_j=b)
      =sum_(r>=a,s>=b,r+s<=K)
         (-1)^(r+s-a-b) binom(r,a)binom(s,b) B_rs.        (L6)

There are O(K^2) output coefficients and O(K^2) terms per coefficient, so
O(K^4) remains an upper bound. Then

    E|n_i-n_j|=sum_(a+b<=K) |a-b| P(n_i=a,n_j=b).         (L7)

Sum(L7) over edges and all pairs as required. At most O(m^2) marginals are
needed; the subtraction lambda K(m-K) is a known constant. This proves
the consequence stated in Section 1 for the actual distinct-input source.

## 4. Precision and resource contract

For exact rational real/imaginary V entries with input bit lengths bounded
by B, all factors in(L2), factorials and binomial coefficients have controlled
polynomial bit lengths: products contribute O(KB), factorials O(K log K),
and the sums add only polynomially many such terms. Exact rational arithmetic
therefore gives a polynomial bit algorithm for rational graph data as well.
A comparable algebraic-number statement needs specified extension degrees
and operations; it is not automatic for arbitrary algebraic encodings.

A matrix supplied by arbitrary floating-point angles or matrix exponentials
does not have an exact rational unitary representation just because its
entries are stored as doubles. One may use controlled approximation or
interval arithmetic at specified input precision. The alternating inversion
in(L6) can catastrophically cancel in machine precision. A double-precision
implementation needs numerical validation before any result is called a
certificate; the symbolic polynomial bound alone does not provide one.

The exponent in the exact bound depends on the number of observed modes.
For a fixed number d, the analogous coefficient table has K^{O(d)} size.
It is polynomial for d=2; calling it polynomial uniformly as d grows with K
would be incorrect. A degree-K interpolation of the absolute value is not
a constant-degree observable, even though its two-mode locality is fixed.

## 5. An explicit additive estimator using phase shifts

The known random-sign permanent identity also gives an alternative that
avoids high-degree moment inversion. In this section K>=1; the K=0 case
is the deterministic vacuum branch of Section 1. Let L=2K+1 and theta_l=2pi l/L. The
function h(d)=|d| on integers -K,...,K has discrete Fourier coefficients

    c_l=(1/L) sum_(d=-K..K) |d| exp(-i theta_l d),
    |n_i-n_j|=sum_(l=0..L-1)c_l exp(i theta_l(n_i-n_j)).   (L8)

Here c0=K(K+1)/(2K+1). For l!=0, the cyclic second difference of h is +2 at
0 and -1 at K and -K. Hence

    c_l=-(1-cos(K theta_l))/[L(1-cos theta_l)] <= 0,
    sum_l |c_l|=2c0=2K(K+1)/(2K+1)<K+1.                 (L9)

The coefficient sum, not merely the number of terms, controls additive
error. Both are polynomial here. For each phase put

    Z_l=I_K+(exp(i theta_l)-1)aa*+(exp(-i theta_l)-1)bb*.

This is the occupied-input compression of U*D_l U and has operator norm at
most 1. For iid signs sigma_alpha in{-1,+1}, the established estimator

    X_l(sigma)=(prod_alpha sigma_alpha)
                    prod_alpha (Z_l sigma)_alpha

has E X_l=per Z_l and |X_l|<=1. The latter follows from AM-GM on squared
absolute row values and ||Z_l sigma||^2<=K. Because Z_l is identity plus two
rank-one updates, each draw costs O(K) arithmetic when the two rows are
available. This is an additive amplitude estimator, not a draw from the
physical photon output law.

Since the negative Fourier coefficients sum to -c0, sample l!=0 with mass
(-c_l)/c0 and independently draw sigma. Then

    Y_ij=c0[1-Re X_l(sigma)]

is a NONNEGATIVE unbiased estimator of E|n_i-n_j| in[0,2c0]. For the weighted
mean of J, assume v_ij=w_ij+lambda>=0 for every pair, as guaranteed by the
project domain w_ij>=0, lambda>=0. Let A=sum_(i<j)v_ij. When A>0, draw a pair with mass
v_ij/A, use A Y_ij, and finally subtract lambda K(m-K). Its mean is E J and
its pre-subtraction range is[0,2Ac0]. Hoeffding therefore gives additive
error delta with failure probability zeta after

    O((A K/delta)^2 log(1/zeta))                           (L10)

draws, plus preprocessing and matrix construction. Under these
NONNEGATIVITY hypotheses, A=0 forces every v_ij=0, so J is the known
constant -lambda K(m-K) and needs no draw. For signed coefficients,
sum v_ij=0 does NOT imply a constant objective. The exact DP still applies
to that case; the probability sampler just described does not. No exact
optimal partition is used.

The dependence on delta is additive, and weights/lambda rescalings change
A correspondingly. Multiplicative error for a tiny value or precision
relative to a tiny variation is not promised at constant cost. This oracle
also has no theorem comparing its actual variance with physical shot noise;
a practical timing/variance comparison would need a fresh controlled study.

## 6. What survives this obstruction

A nontrivial bosonic/distinguishable gap in E J is physically possible and
can be worth diagnosing. It does not make that mean expensive to compute
classically, or prove a graph-search benefit. A classical optimizer can use
the same supplied mean oracle; global minimization may still be difficult.
The source paper's expectation-value results do not provide a full joint
sampler or feasible-search dominance outside their separate hypotheses.

One precise remaining target is

    p_improve(V;G,S0)
      =Pr_V[ n is CF AND C_G(supp n)<C_G(S0) ],            (L11)

with every non-CF event counted as failure per attempt. S0 is a scored
classical incumbent, fixed before evaluating a batch; no C* or optimal mask
appears. This is a global indicator, not a sum of two-mode functions. Its
conditional-state projector may have exponentially many outcomes. The local
DP does not evaluate it. That is a gap in this oracle argument, not a proof
that(L11) is classically hard, new, trainable or advantageous. The source's
phase expansion also needs controlled total Fourier weight; no such bound
has been proved for(L11). The existing low-loss P42 uniform domination
still applies wherever its assumptions and resource criterion hold.

A change of optical physics rather than readout is another distinct route:
interleave graph-dependent nonlinear occupation phases exp(-i gamma J_G(n))
with passive mixers. The graph and scored incumbent specify the phase
without optimal labels. Such a layer is not a one-particle passive matrix;
merely postprocessing samples with that phase does NOT implement it. True
nonlinear interactions or measurement-induced operations with ancillas,
heralding and feedforward require a physical resource/compilation contract.
No availability on the current QPU, preparation success rate, classical
hardness, feasibility advantage or novelty is established here. A single
larger passive network followed only by terminal detection remains inside
the model above and does not implement this proposed escape.

## Sources and status

The exact two-mode approach is a formal corollary of established fixed-mode
marginal methods; Aaronson–Arkhipov's author PDF, Appendix 12, Theorem 69
and Lemma 68 give the corresponding n^{O(d)} framework. The low-rank DP above
is written out so that the present implication does not rely on an omitted
summation argument. The additive construction applies the known random-sign
identity and passive phase expectation reduction. Its source comparison is
recorded in research/P42_encoding_Monbroussou_L1_audit.md. No novelty claim,
finite calculation or accepted independent proof review is recorded here.

### Qualification correction after physics review

The previous file SHA-256
`4b6bc6ee4bd5e9ae739264da37e0ebb3d6bb6a2b0fad7e16267738c14a3a638a`
omitted the weighted sampler's nonnegativity hypothesis and the K=0 branch.
The physics reviewer supplied m=4,K=2,w_01=6, other weights zero, lambda=-1:
sum_(i<j)(w_ij+lambda)=0, yet J(1,1,0,0)=0 and J(1,0,1,0)=6. That exact
counterexample invalidates the unrestricted A=0 wording, not the marginal
DP. The current explicit domain and separate vacuum branch correct it. The
earlier source version remains in Git history; no numerical run was used.
