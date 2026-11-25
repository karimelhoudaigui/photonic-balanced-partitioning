# P56 — visibility obstruction for the proposed flat Diță family

Static derivation only. No new matrix, graph, polynomial, sample or program
was evaluated. This elementary symmetry result has no novelty claim and
does not complete the optimization objective.

## Model and exact decoder

Index20 output modes by (a,i), a in Z5, i in{0,1,2,3}, and input modes by
(b,j). Let omega=exp(2*pi*i/5), H the unnormalized real Walsh4 matrix, and

    U_theta[(a,i),(b,j)] = omega^(a*b)*exp(i*theta[b,i])*H[i,j]/sqrt20.

The source is one identical photon in EACH input. Decode every output count
vector by selecting its10 largest counts, uniformly among threshold ties.
All collision patterns are accepted; the decoder reads no graph or optimum.
This is the P56 top10 decoder, not an assertion about every P55 decoder.
An alternative decoder is covered only if it is equivariant IN LAW under
the output permutations used below, with graph-independent randomness.

Summing j gives4*delta(i,i'), then summing b gives5*delta(a,a'), so U is
unitary for every theta; |U|^2=1/20. Adding alpha[b]+beta[i] to theta is an
input-column/output-row phase gauge. Its dimension is5+4-1=8, leaving12
continuous physical parameters. No eigenproblem or prepared partition appears.

## Visibility theorem (pointwise in theta)

Let T_c(a,i)=(a+c,i). Then

    U_theta[T_c(a,i),(b,j)] = omega^(c*b)*U_theta[(a,i),(b,j)].

This is a column phase. A fixed Fock input changes by a global phase, so
the ENTIRE count law is T_c-invariant for every theta, including theta
chosen from a graph. Equivariance of uniform top10 ties makes its feasible
output law mu_theta(S) invariant under T_c as well.

For an undirected weighted graph A define C_A(S)=sum_(u in S,v notin S)A_uv
and barA=(1/5)*sum_c T_c^T A T_c. Invariance and linearity imply

    f_A(theta) = E_mu_theta C_A(S)
               = E_mu_theta [(1/5)*sum_c C_A(T_c S)]
               = f_barA(theta).

IMPORTANT: this compares the SAME theta. It does NOT equate the pipelines
f_A(theta(A)) and f_barA(theta(barA)), whose chosen theta can differ. The
optimum over all theta depends only on barA. Encoding invisible residuals
can change the chosen phase, but creates no additional mean-cost channel.

Each unordered edge has a free C5 orbit: a nontrivial odd-order shift cannot
fix its two endpoints as an unordered pair. Thus there are190/5=38 edge
orbits and a152-dimensional kernel of this mean-cost projection.

## Lower bound and explicit nonnegative counterexample

Every invariant feasible law satisfies, for every graph-dependent theta,

    f_A(theta) >= L(A),
    L(A)=min_(|S|=10) (1/5)*sum_c C_A(T_c S).

Proof: the expected orbit-average cost is a convex combination of those
costs. A classical uniform draw from a minimizing orbit attains L(A) after
that orbit has ACTUALLY been found. Returning its best member is no worse
in mean. This does not give an uncharged classical optimization oracle.

For a concrete obstruction take e={(0,0),(0,1)}, with T_1 e disjoint, and

    A = J-I + delta*(E_e-E_(T_1 e)),       0<delta<=1.

E_e denotes a unit undirected edge. All weights are nonnegative and
barA=J-I. Every balanced cut of J-I has10*10=100 edges, so EVERY phase rule,
even an expensive rule, has f_A(theta(A))=100. Feasible partitions with
X_e-X_(T_1 e)=+1 and-1 both exist: assign the four endpoints accordingly
and fill the remaining places from16 other vertices. Their costs are
100+delta and100-delta. This is a mathematical counterexample, not an input
used to train a circuit or a favorable benchmark instance.

The bound concerns an all-shot MEAN. Best-of-many cost selection or
graph-dependent repair can break decoded C5 invariance; this theorem is not
a bound for those pipelines, other architectures, or all possible decoders.

## Exact classical search size, with costs still to be paid

For cost evaluation identify complements as well as C5 translates.
Burnside for C5 x complement, order10: identity fixes C(20,10)=184756;
each of four nontrivial shifts fixes C(4,2)=6 sets (unions of two complete
five-vertex color orbits). No complement-times-shift fixes a set: squaring
would force shift invariance, then S=S^c, impossible. Therefore

    number of cut-equivalence classes = (184756+4*6)/10 = 18478.

One may enumerate these representatives and minimize the exact integer
sum_c C_A(T_c S), dividing by5 only at the end. Precomputed orbit-crossing
features h[S,e] in{0,...,5} have18478*190=3,510,820 uint8 entries; masks
use73,912 bytes as uint32. Per graph the dot product has that many terms,
plus graph loading/aggregation and up to five original-cut evaluations.
Generation of representatives/features, validation and storage are costs,
not free gifts; amortization must be declared. No timing was measured and
this note does not call the enumeration a matched-budget efficient control.

## Continuation and the small-member trap

A fixed monomial output V only conjugates the permutation obstruction;
a V commuting with T preserves it. A generic V may break it, but failed
state-stabilizer equations alone do not prove the COUNT law breaks it.

A useful N20 candidate is V=direct_sum_i V_i, each V_i mixing the five a
within the SAME color. Then U' has (V_i F5)[a,b]*exp(i theta[b,i])*H[i,j]
entries/sqrt20: q'=|U'|^2 is independent of theta, though generally nonflat.
D's Poisson-multinomial law, each B marginal and count moments through
degree3 stay fixed in theta; P=I and mean counts1 survive. The low-moment
statement follows by expanding the full-single-input normal generating
function product_q(1+L_q(s)R_q(t)): cumulants1,-2,12 and P=I leave only q
in diagonal count derivatives of degree<=3. It still needs peer review.

For a real beamsplitter gamma between (0,0) and(1,0), write s=sin(2gamma).
Its first mixed row has q'_r,bj=[1+s*cos(2*pi*b/5)]/20, hence
sum q'_r^2=1/20+s^2/40 and Var_B(n_r)=19/10-s^2/20. An unmixed translated
row has variance19/10. For s!=0 this explicitly breaks C5 in the COUNT law
without adding a theta-dependent distinguishable or marginal channel.

However the requested TWO-block N8 analogue does NOT break C2 this way.
Take F2 real, theta[0,i]=0, theta[1,i]=phi_i, any within-color V_i in U2,
and X swapping a, Z=(-1)^a. Removing color-global phases lets V_i be SU2.
SU2 pseudoreality gives X V=Z V* Z X. Also

    X U_phi=U_phi Z_b,       Z U_phi=D_i(phi) U_(-phi) X_b.

Because H/F2 are real and D_i commutes with V,

    X V U_phi = Z D_i(phi) (V U_phi)* X_b Z_b.

Row phases, conjugation and input monomials preserve full-Fock number laws.
Thus the N8 law stays C2-invariant for ALL within-color U2 mixers, including
gamma=pi/8, even though V need not commute with X. It is not a valid
symmetry-broken surrogate for the odd five-block construction.

Mixing different colors, a generic second Diță layer, or using an odd small
member needs fresh analysis. Generic stacking may make q theta-dependent,
requiring a fully reoptimized D control. None of these statements proves a
nonzero coefficient of the actual feasible-cut mean or an optimization gain.
