# P69: an independent low-rank transport bound

Primary verdict: **proved as written** for the normalized claim in section 1,
with its specified passive unitary, collision-free input and targets,
and pathwise bound on the cross-block rank. The projectors at input and
output need not be the same. No covariance, graph automorphism or common
invariant subspace across attempts is required.

This is an independent derivation of ROOT's P69 candidate, authored on
2026-11-25 in `research/p66-dark-barrier`. Starting checkpoint:
`30361da172f7005f617629db7316ae5a2d9c6bbf`. No peer P69 proof or verdict
was read. Only this new file is written for P69. All probabilistic identities
needed below are proved internally. There was no scientific import, test,
numerical computation, graph generation, seed/draw, backend call, external
source or QPU call. There is no novelty assertion.

## 1. Exact claim

Let L>=2 be an integer. Split the one-particle space into two orthogonal
vertex blocks HA and HB of dimension 2L each. Let U be any unitary on
HA direct-sum HB, written with output blocks as rows and input blocks as
columns:

    U = [ A  B ],       B: input HB -> output HA,
        [ C  D ]        C: input HA -> output HB.

Let r be an integer with 0<=r<=2L such that rank B and rank C are at most r.
Their actual ranks are equal, as proved in section 2. The normalized
source x has one photon in each of L distinct vertex modes of HA and
L distinct vertex modes of HB. The two normalized target Fock states are

    yA = one photon in every vertex mode of HA, vacuum in HB,
    yB = vacuum in HA, one photon in every vertex mode of HB.

All photon probabilities refer to the complete, normalized 2L-photon
output of the passive Fock lift Gamma(U). There is no collision-free
conditioning. For r>=1 set

    a(L,r) = min(1, r(r+1)...(r+L-1)/L^L),

    b(L,r) = 1,                                      if r>=L,
             ((L+r)/(2r))^r * ((L+r)/(2L))^L,         if 1<=r<L,

    p(L,r) = min(1, 2 a(L,r) b(L,r)).

Then

    P_U(x -> {yA,yB}) <= p(L,r).

For r=0 this probability is exactly zero; define p(L,0)=0 separately.
The formula for b is never evaluated at r=0. A larger rank upper bound
than 2L can simply be replaced by 2L. These are upper bounds, not claims
that their values are attainable or equal to an optimized probability.

## 2. Different dark spaces at input and output

Define the input dark spaces

    DA_in = ker C inside input HA,
    DB_in = ker B inside input HB.

Unitarity gives

    A^dagger A + C^dagger C = I,
    A A^dagger + B B^dagger = I,
    B^dagger A + D^dagger C = 0,
    C A^dagger + D B^dagger = 0.

For v in ker C, Av is in ker B^dagger and A^dagger Av=v. Conversely,
for w in ker B^dagger, A^dagger w is in ker C and AA^dagger w=w.
Consequently A is an isometric bijection

    ker C -> ker B^dagger,

with inverse A^dagger. Its domain and codomain have dimensions
2L-rank C and 2L-rank B, respectively. Thus rank B=rank C=:k<=r.
The analogous statement holds for D. Define output dark spaces

    DA_out = ker B^dagger = (range B)^perp inside output HA,
    DB_out = ker C^dagger = (range C)^perp inside output HB.

U maps DA_in onto DA_out and DB_in onto DB_out. Let P_DA_in and so on
be the embedded orthogonal projectors on the full one-particle space.
Because U is unitary, mapping these subspaces onto one another also maps
their orthogonal complements onto one another. Therefore

    U P_DA_in = P_DA_out U,
    U P_DB_in = P_DB_out U.

The complementary bright subspace within each block has dimension k, at
both input and output. In general its orientation changes under U. No
identity between an input dark projector and an output dark projector is
asserted, and no conservation relative to a single fixed projector is used.

On Fock space, let N_DA_in=dGamma(P_DA_in), and define the other three
number operators similarly. Transforming creation operators under the
passive U proves

    Gamma(U) N_DA_in = N_DA_out Gamma(U),
    Gamma(U) N_DB_in = N_DB_out Gamma(U).

Their spectral projections obey the same intertwining identities. The
A and B number projections commute on each side because the underlying
subspaces are orthogonal.

## 3. Elementary permanent and complex-Gaussian identities

Three finite-dimensional facts used in both norm estimates are recorded
with proofs to avoid an unverified Wick or factorial-moment dependency.

First, for vectors v1,...,vm, the squared norm of

    a^dagger(v1)...a^dagger(vm)|0>

is per G, where G_ij=<vi,vj>. Commuting the first annihilator across the
m creation operators pairs it with each of them once. Iterating gives
exactly the m! permutation terms of the permanent. There is no division
by m! for a source with distinct, singly occupied input vertex modes.

Second, let g1,...,gk be independent standard circular complex Gaussians,
with one-coordinate density pi^(-1) exp(-|g|^2), and let z=Tg. Direct
polar integration gives

    E[g^a conjugate(g)^b] = 0 if a!=b, and a! if a=b.

The angular integral gives the first assertion. For a=b, the substitution
t=|g|^2 gives integral_0^infinity t^a exp(-t) dt=a!, by repeated
integration by parts. Expand the product of m coordinates of z and
m conjugate coordinates. A term survives precisely when each Gaussian
index occurs equally often on both sides. If index j occurs nj times,
its expectation is nj!. Summing bijections between the occurrences on
the two sides counts exactly those factors. It follows that

    E[product_{i=1}^m |z_i|^2] = per(T T^dagger).

This also holds for singular covariance matrices; T need not be square
or injective. The same argument gives principal-subset versions by
selecting any m rows of T.

Third, R=sum_{j=1}^k |gj|^2 has

    E[exp(sR)] = (1-s)^(-k),       0<=s<1,
    E[R^L] = k(k+1)...(k+L-1).

The first formula is a product of integrals of exp(-(1-s)t) on [0,infinity).
Differentiating it L times at zero gives the second. Differentiation is
justified by domination in a fixed interval s<1, or by integrating the
nonnegative power series there. For k=0, R=0 and its positive moments
are zero.

## 4. Source projection bound

Let Q be any rank-k orthogonal projector on a 2L-dimensional vertex block,
and let the source in that block occupy L distinct vertex modes S.
Projection of all those photons onto the bright subspace range Q produces
the vector with creation factors a^dagger(Q e_i), i in S. Its squared
norm is therefore per Q[S], the permanent of the principal Gram matrix.

Write Q=W W^dagger with W having k orthonormal columns, and let T be the
submatrix consisting of its L selected rows. Then Q[S]=T T^dagger and
T^dagger T<=I_k. By the Gaussian identity and the arithmetic-geometric
mean inequality applied to L nonnegative numbers,

    per Q[S] = E[product_{i=1}^L |(Tg)_i|^2]
       <= E[(||Tg||^2/L)^L]
       <= E[(||g||^2/L)^L]
        = k(k+1)...(k+L-1)/L^L.

It is also a squared norm after an orthogonal projection of a normalized
state, hence at most one. Increasing k to r only increases the last
positive product. Thus the desired source norm is bounded by a(L,r).
This works for every orientation of the bright space and every choice
of L distinct source modes; no flatness of its diagonal is assumed.

## 5. Target bright-tail bound

Let Q be a rank-k bright projector in a block containing the full
collision-free target |1^n>, where n=2L. Let N_Q count its bright photons.
For s>=0, the one-body operator I+sQ has eigenvalue 1+s on range Q and
one on its complement. Its Fock lift on the n-photon space is consequently
(1+s)^(N_Q). By the permanent overlap identity,

    E_target[(1+s)^(N_Q)] = per(I+sQ)
       = sum_{I subset {1,...,n}} s^|I| per Q[I].

The permanent expansion chooses Q entries on I and identity entries
outside I; the latter force the permutation to fix every outside index.
The empty principal permanent is one. With Q=W W^dagger and z=Wg,
the Gaussian identities give the exact representation

    per(I+sQ) = E[product_{i=1}^n (1+s|z_i|^2)].

Using 1+sx<=exp(sx), W^dagger W=I_k, and 0<=s<1,

    E_target[(1+s)^(N_Q)]
       <= E[exp(s sum_i |z_i|^2)]
        = E[exp(s ||g||^2)] = (1-s)^(-k).

This argument uses bosonic amplitudes and a Gaussian auxiliary integral.
It does not replace the photons by independent particles, phase-average
the optical law, or suppose that occupations in the target are sampled
from a multinomial distribution.

Since k<=r, Markov's inequality now gives

    P_target(N_Q>=L) <= (1-s)^(-r)(1+s)^(-L).

For 1<=r<L the logarithmic derivative is r/(1-s)-L/(1+s), with
positive second derivative. Its minimum over 0<=s<1 occurs at
s=(L-r)/(L+r), and the value is exactly b(L,r) in section 1.
If r>=L the minimum of this relaxed bound is its value one at s=0;
we use b=1. These cases cover r=L without a false interior minimizer.

## 6. Input/output support identity and the probability bound

For target yA define

    Q_in  = 1_{N_DA_in<=L},     R_in  = 1_{N_DB_in=0},
    Q_out = 1_{N_DA_out<=L},    R_out = 1_{N_DB_out=0},
    Pi_in=Q_in R_in,           Pi_out=Q_out R_out.

The source x has L photons in input HA, so Q_in x=x. The target yA has
vacuum in output HB, so R_out yA=yA. All paired projections intertwine
under Gamma(U). Inserting those two support identities first, then using
the intertwinings, yields

    <yA|Gamma(U)|x> = <Pi_out yA|Gamma(U)|Pi_in x>.

For example, inserting R_out at the target and moving it right gives
<yA|Gamma(U) R_in|x>; Q_in can then be inserted at the source and moved
left. Unitarity gives the Cauchy-Schwarz bound by the product of squared
projection norms.

The source Pi_in norm is the probability that all L input HB photons
are in its input bright space, bounded by a(L,r) in section 4; its
Q_in constraint was automatic. The target Pi_out norm is the probability
that N_DA_out<=L. All 2L target photons are in output HA, so that event
is exactly N_brightA_out>=L, bounded by b(L,r) in section 5. Therefore

    |<yA|Gamma(U)|x>|^2 <= a(L,r)b(L,r).

Swap A,B for yB, and sum the two distinct orthogonal PNR events. This
proves p(L,r). For k=0, U is block diagonal and preserves the number of
photons in each block. A source with L in each block cannot reach either
target with all 2L in one block, proving the separate r=0 assertion.

## 7. Conditional chain bounds on the P66 cost landscape

For application to the P66 four-clique family, retain M,h>0,
M(L-1)>Lh, and either absent cross edges or complete cross edges of common
weight 0<w<h/L. Start at one of Ai union Bj. Only the two full-block
targets improve on these four bad subsets, and every other subset outside
those six has cost at least C_bad+g, with g=2M(L-1)-2Lh>0.

For clarity, this graph fact is independent of optics: a partial clique
contributes at least M(L-1), and exactly one partial clique is impossible
at total occupancy 2L. Cross-block cut in the connected case is
w[x^2+(2L-x)^2]>=2wL^2, with x=|S intersect CA|. The bad cost is
2Lh+2wL^2, and the target cost 4wL^2 is smaller under w<h/L.

Suppose every realized proposed U, conditional on the full history and
all controller choices made before its fresh draw, has cross rank at most
the same r. There is no requirement that its singular subspaces, random
markings or coefficients be shared across attempts. Classical state-based
selection or filtering of candidate matrices is allowed subject to this
pathwise rank condition. This does not authorize nonunitary filtering or
heralding of the physical input state, which would change the source
assumptions. The physical source, labels and complete PNR decoder remain
the ones in section 1.

Count collisions as self-loops. Update only from collision-free proposals,
with no external restarts or candidate injection. At zero temperature
accept all non-uphill moves and reject every uphill move. Before first
improvement the source remains one of the four bad subsets, each with
L distinct occupied modes per block. The conditional improvement hazard
is at most p=p(L,r) after every such history, even though Pi_in and
Pi_out vary between attempts. Hence

    P(first improvement by T raw attempts) <= min(1,Tp),
    P(first improvement after T) >= (1-p)^T.

For a run continuing until success, the extended expectation of attempts
is at least 1/p and of injected photons is at least 2L/p. For p=0 these
are infinite. Actual capped or aborted runs have only the finite-budget
success bound; no expenditure lower bound is inferred for them.

At finite temperature use the P66 acceptance rule exp(-beta_j Delta)
for an uphill collision-free proposal. Stop at the first accepted exit
from the bad set. Direct targets have hazard at most p and any other
accepted exit pays an increase of at least g. For deterministic beta_j>=0,

    P(improvement by T) <= min(1, Tp + sum_{j=1}^T exp(-beta_j g)).

For history-random beta_j selected before the proposal, replace the sum
by sum_j E[1_{no earlier accepted exit} exp(-beta_j g)], or use
deterministic almost-sure lower bounds on beta_j. A random expression
cannot serve as an unconditional numerical bound without this expectation.
After an uphill exit no bound on later behavior is needed. No claim of
Gibbs stationarity or general Metropolis-Hastings acceptance is used.

The cost landscape, warm start and update rule are essential. These are
not conclusions about typical uniform starts, generic graphs or the actual
P65 temperature schedule. Counting discarded collision-free retries as
free proposals, changing the decoder, retaining collided inputs, physical
postselection, ancillas or additional sources change the model.

## 8. Separate distinguishable-particle bound

For independent distinguishable photons in the same singly occupied
source, let qi=||B e_i||^2 for the L input HB vertices. The contraction
B has rank k and singular values at most one, so

    sum_{i in selected HB} qi <= trace(B^dagger B) <= k <= r.

All those L photons must cross to output HA for target yA. Independence
and AM-GM therefore bound this target probability by

    product_i qi <= (r/L)^L.

This does not assert an individual bound qi<=r/L, which is generally
false. Ignoring the other L photons and the final collision-free pattern
only weakens the estimate. Swapping blocks and summing gives

    P_distinguishable({yA,yB}) <= min(1,2(r/L)^L),

with zero at r=0. This is uniform over separately reoptimized allowed
matrices. It is a separate upper bound and gives no ordering or separation
between the attainable bosonic and distinguishable success probabilities.

## 9. Fixed-rank and coherent-depth consequences

For fixed integer r>=1 and L>r, elementary factorial integral bounds give

    L! <= e L (L/e)^L,
    r(r+1)...(r+L-1) = (L+r-1)!/(r-1)!,
    a(L,r) <= e r^(r-1) L^r exp(-L)/(r-1)!.

The last estimate uses (L+r-1)!<=L!(L+r-1)^(r-1) and
L+r-1<=rL. Also (1+r/L)^L<=e^r and L+r<=2L imply

    b(L,r) <= e^r L^r 2^(-L)/r^r,
    p(L,r) <= [2e^(r+1)/r!] L^(2r) (2e)^(-L).

Thus the stated bound decays exponentially for fixed r, with an explicit
polynomial prefactor. No Stirling formula or numerical fit is needed.

More generally, fix 0<alpha<1 and suppose r<=alpha L. In the target
Chernoff bound choose s=(1-alpha)/(1+alpha). Then

    b(L,r) <= exp(-L I(alpha)),
    I(alpha) = (1+alpha)log 2 + alpha log alpha
                 - (1+alpha)log(1+alpha) > 0,
    p(L,r) <= min(1,2 exp(-L I(alpha))).

Indeed I(1)=0 and I'(alpha)=log(2alpha/(1+alpha))<0 for 0<alpha<1.
This argument does not need the source bound to be nontrivial in that
regime. It is an upper bound for ranks below a fixed fraction of L,
not an assertion at alpha=1.

For two coherently composed one-particle unitaries V,W with the same
fixed block partition,

    (VW)_AB = V_AA W_AB + V_AB W_BB,
    rank((VW)_AB) <= rank(W_AB)+rank(V_AB).

Induction bounds the cross rank of d coherent layers by the sum of their
cross ranks. In particular rank-one layers with d<=alpha L obey the last
exponential bound for their composite proposal. There can be arbitrary
unitary operations within each block. Intermediate measurement, input
repreparation, or nonunitary filtering is not a coherent unitary product
and is not covered by this depth inference.

## 10. Cayley transform preserves the cross-rank bound

Let H be any Hermitian operator on the same two blocks, and let t be real.
Its Cayley unitary is

    U=(I+itH)(I-itH)^(-1) = 2(I-itH)^(-1)-I.

For t=0 its cross rank is zero. Otherwise put V=I-itH with diagonal
blocks E=I-itH_AA, F=I-itH_BB and off-diagonal blocks
X=-itH_AB, Y=-itH_BA. Both V and E are invertible because their
Hermitian generators have real eigenvalues. The Schur complement
S=F-Y E^(-1)X is invertible: a vector in its kernel would produce a
vector in the kernel of V after choosing its A part as -E^(-1)X times
its B part. Solving the same block equations gives

    (V^(-1))_AB = -E^(-1) X S^(-1).

Consequently rank U_AB<=rank H_AB. The other cross rank is equal by
unitarity (and H's two cross ranks agree by adjunction). Thus every
single Cayley proposal whose Hermitian cross coupling has rank at most r
obeys the theorem, without any graph covariance requirement. A bound on
the coupling rank alone is not asserted here for arbitrary other spectral
functions of H or general continuous-time evolution.

## 11. Dependency and scope audit

| Obligation | Result |
|---|---|
| Equality of the two cross ranks | Passed by inverse isometries A and A^dagger |
| Input/output dark spaces and count projectors | Passed; intertwined rather than identified |
| Source permanent normalization | Passed for distinct singly occupied input modes |
| Wick identity and gamma moments | Proved internally from one-coordinate integrals |
| Source rank-contraction bound | Passed; all orientations and selected vertex sets |
| Target permanent PGF and exponential moment | Passed; normalized bosonic target |
| Chernoff optimum, r=0, r=L, r>L | Passed with the stated separate cases |
| Two-support amplitude identity | Passed with input/output projections on their own sides |
| Adaptive matrices and varying/random singular subspaces | Passed if every realized rank is bounded before each fresh draw |
| Expected photons | Only for runs continuing until success |
| Finite temperature | Conditional first-exit bound under the stated acceptance rule |
| Distinguishable control | Separate upper bound; requires independent particle propagation |
| Coherent depth and Cayley rank transfer | Passed on the same fixed physical partition |
| Ancillas, changed sources, physical filters, CF conditioning | Outside this theorem |
| All-graphs no-go, positive optimizer, actual P65 schedule, novelty | Not established |

The graph family remains easy for a classical routine that identifies the
four heavy cliques and evaluates six unions. The theorem is therefore a
restricted transport obstruction on engineered shared-warm-start instances.
It is not a hardness result for the optimization problem, does not show
which upper bound is attained, and does not imply that increasing rank
produces a useful optimizer.

Final self-review covered all formulas, input/output block conventions,
rank cases, factorial normalization, conditional quantifiers and units of
attempts versus photons. Only text integrity and Git whitespace checks
are applicable to this proof-only freeze. No scientific execution was
performed or authorized by this file.
