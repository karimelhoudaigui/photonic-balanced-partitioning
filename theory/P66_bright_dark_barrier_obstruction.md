# P66: a bright/dark obstruction for a specified warm-start proposal kernel

Status: independent static derivation, frozen before comparison with the peer
proof. This is a theorem about an engineered graph family and a restricted
proposal mechanism. It is not a claim about all graph encodings, the registered
P65 graphs or annealing schedule, quantum advantage, or novelty.

Provenance: authored in `research/p66-dark-barrier`, based on
`3e708637639b8664d0f81bb8947ce05fed0e0a4c`, on 2026-11-25. The initial
candidate supplied by ROOT was the disconnected four-clique construction,
the sector weights below, and the proposed trajectory bounds. The connected
rank-one extension and exact-equivariance extension were then supplied as
separate candidates. Each is derived below. The graph barrier also received
an independent focused derivation by the author's graph-lemma child. The
separate ROOT peer proof has not been read for this freeze. No scientific
Python, import, test, graph generation, random draw, numerical experiment,
or QPU call was used.

## 1. Graph and chain conventions

Let L be an integer at least 2. There are N=4L vertex modes and K=2L
indistinguishable photons. Four disjoint sets A1,A2,B1,B2 each contain L
vertices. Every pair within one of these sets has edge weight M>0. A1,A2
are joined by a perfect matching of L edges of weight h>0; B1,B2 have an
identical matching. Initially there are no other edges. Write

    CA = A1 union A2,       CB = B1 union B2,
    M(L-1) > Lh,           g = 2M(L-1) - 2Lh > 0.

Cuts are sums of weights of edges with exactly one endpoint in an oriented
subset S of size 2L. A subset and its complement are distinct Fock outputs;
we do not quotient them into one partition. Define

    B = { Ai union Bj : i,j in {1,2} },
    G = { CA, CB },         C_bad = 2Lh.

The starting subset is any member of B; in particular A1 union B1 is allowed.
Its optical input is the normalized Fock state |1_S>: one photon at every
vertex of S and vacuum elsewhere. A proposal applies a passive one-particle
unitary U and measures the complete 2L-photon PNR output. A collision is a
self-loop and consumes one raw attempt. A collision-free output is decoded
as its occupied vertex subset, without changing labels or repairing it.
The source for the next attempt is freshly prepared from the current subset.

For the zero-temperature chain, all non-increasing collision-free proposals
are accepted and increasing proposals are rejected. At finite inverse
temperature beta>=0, an increase Delta is accepted with probability
exp(-beta Delta), using a fresh uniform acceptance coin independent of the
proposal, conditionally on the history. No collision-free conditioning,
retry-until-success, or discarded failed attempt is permitted.

The controller may use the entire past, including the current state, to
select an allowed U before the next fresh source is measured. It may also
randomly choose among allowed U's, provided every selected realization has
the invariance property proved below. A deterministic raw-attempt horizon T
is used; an earlier adaptive stop may be padded by self-loops.

## 2. The graph barrier

For any balanced subset S, let x_C=|S intersect C| for each of the four
size-L cliques. Its within-clique cut is

    M sum_C x_C(L-x_C).

If 0<x_C<L, that clique contributes at least M(L-1). Exactly one partial
clique is impossible: all other clique occupancies would be multiples of L,
whereas the sum of all four occupancies is 2L. Consequently every subset
which is not a union of two whole cliques has at least two partial cliques,
and its cut is at least 2M(L-1). Matching contributions are nonnegative.

There are exactly six unions of two whole cliques. The two members of G
have cut zero; the four members of B cut both matchings and have cut 2Lh.
Therefore every other balanced subset has cut at least C_bad+g. In
particular, the only strict improvements from B are the two members of G.
The lower bound g need not be attained. The hypotheses h>0 and g>0 matter:
with h=0 the alleged bad whole-clique states would already be optimal.
The example M=3,h=1 gives g=4L-6>0 for every L>=2.

## 3. One-particle and Fock invariants

Let b_A and b_B denote the unit vectors uniform on CA and CB, respectively:

    b_A = (2L)^(-1/2) sum_{v in CA} |v>,
    b_B = (2L)^(-1/2) sum_{v in CB} |v>.

Let D_A be the subspace supported on CA and orthogonal to b_A; define D_B
similarly. Write P_A,P_B for their orthogonal one-particle projectors.
Each block of the graph is regular with degree d0=M(L-1)+h. Its real
symmetric adjacency preserves its uniform vector and its orthogonal
complement. Thus the full adjacency A preserves D_A and D_B separately.

For a vector v in either dark subspace, its total coordinate sum vanishes,
so Jv=0 and (J-I)v=-v. Hence for every scalar D>0 and lambda>=0,

    H = (A + lambda(J-I))/D

commutes with P_A and P_B. H is real symmetric. For every real t its Cayley
unitary

    U = (I + itH)(I - itH)^(-1)

exists, is unitary, and commutes with both projectors. The same holds for
U=f(H) whenever f is a scalar spectral function of modulus one on the
spectrum. This is the precise meaning of a spectral unitary here.
An arbitrary unitary satisfying only [U,H]=0 is not enough: it can exchange
equal-eigenvalue dark eigenvectors of the two identical blocks. Nor may one
choose an arbitrary basis-dependent action inside a degenerate eigenspace
and call it a scalar spectral function.

On the fixed-2L-photon Fock space, let Gamma(U) be the induced passive
unitary and let

    N_A = dGamma(P_A),      N_B = dGamma(P_B).

They count photons in orthogonal dark mode subspaces. Their definitions
are independent of the basis chosen inside those subspaces. The one-body
commutations imply that Gamma(U) commutes with N_A,N_B and with all their
spectral projections. In particular define

    Q_A = 1_{N_A <= L},     Q_B = 1_{N_B = 0},
    Pi = Q_A Q_B.

This is conservation during an individual passive proposal. PNR
measurement and subsequent input repreparation do not conserve these
numbers along a classical trajectory; the trajectory argument will instead
apply a uniform bound afresh at every bad current state.

## 4. Exact source sector weight

Fix S=Ai union Bj. Its CA factor has L photons, so Q_A|1_S>=|1_S>.
Projecting its CB factor to zero dark photons replaces every creation
operator at a vertex of Bj by b_B^dagger/sqrt(2L). This leaves

    (b_B^dagger)^L/(2L)^(L/2) |0>
      = sqrt(L!)/(2L)^(L/2) |L photons in b_B>.

All distinct occupied input modes originally have occupation one, so the
original input has norm one and no additional input factorial is present.
The other block factor keeps norm one. Therefore, exactly,

    ||Pi |1_S>||^2 = a_L = L!/(2L)^L.

This holds for each of the four bad sources.

## 5. Target factorial moments and a tail bound

For the target |1_CA>, there are 2L photons in CA and none in CB. Its
Pi weight is the probability that at least L photons occupy the bright
mode b_A, because on this target N_A+n_b=2L and N_B=0. We bound this
bright occupation n_b without assuming independence of photons.

Let n=2L, b=n^(-1/2) sum_{v in CA} a_v, and let (z)_m denote a falling
factorial. For 0<=m<=n, applying b^m to |1_CA> gives

    b^m |1_CA>
      = m! / n^(m/2) sum_{I subset CA, |I|=m} |1_{CA minus I}>.

Each unordered hole set has m! ordered annihilation sequences. Different
hole sets are orthonormal. Taking squared norms proves the exact identity

    E[(n_b)_m] = (m!)^2 binom(n,m)/n^m,

and moments above n vanish. For 0<=s<1, the finite binomial expansion gives

    E[(1+s)^n_b]
      = sum_{m=0}^n E[(n_b)_m] s^m/m!
      = sum_{m=0}^n (n)_m (s/n)^m
      <= sum_{m=0}^n s^m <= 1/(1-s).

The m! in the expansion cancels exactly one of the two m!'s in the
factorial moment; omitting this cancellation changes the law. Markov's
inequality now yields

    P(n_b >= L) <= 1 / [(1-s)(1+s)^L].

The choice s=(L-1)/(L+1), in (0,1), minimizes this displayed upper bound:
the derivative of its logarithm is 1/(1-s)-L/(1+s), with positive second
derivative. Define

    b_L = min(1, (L+1)/2 * ((L+1)/(2L))^L).

We have proved ||Pi |1_CA>||^2<=b_L. This is a bound on a normalized
Fock-state projection, not a phase average or a distinguishable-photon
approximation. By exchanging A,B, the analogous bound holds for |1_CB>.

## 6. A two-sided sector bound for direct improvement

Let x=|1_S> and y=|1_CA>. The support facts Q_A x=x and Q_B y=y, and
commutation with Gamma(U), give the exact identity

    <y|Gamma(U)|x> = <Pi y|Gamma(U)|Pi x>.

Indeed one may insert Q_B from the target and move it to the source, and
insert Q_A from the source and move it to the target. Merely asserting
[Pi,Gamma(U)]=0 without these support facts would not justify this identity.
Unitarity and Cauchy-Schwarz therefore give

    P_U(S -> CA) <= ||Pi y||^2 ||Pi x||^2 <= a_L b_L.

For CB use the exchanged projector 1_{N_A=0,N_B<=L}. The two targets are
orthogonal PNR events, so for every S in B and every allowed U,

    P_U(S -> G) <= r_L,     r_L = 2 a_L b_L.

No independence of the two sector weights or the two target events is
claimed. Collisions and all other outcomes remain in the normalization.

## 7. History-adaptive trajectory bounds

Let F_{j-1} be all information before the j-th proposal, including the
current state and the selected unitary and inverse temperature if these
are randomized before the proposal. Let tau be the first accepted exit
from B. On {tau>=j}, the current source is one of the four sources already
bounded. Conditional on this information, direct improvement has
probability at most r_L, uniformly in the controller's choice.

At zero temperature every accepted exit from B is a strict improvement
into G: the graph lemma excludes any other equal or lower-cost states.
A conditional union bound, without independence between attempts, proves

    P(strict improvement by raw attempt T) <= min(1, T r_L).

This includes an improvement found by scoring a proposal: a lower-cost
collision-free proposal is accepted with probability one. It does not
include an external classical routine injecting a different current source
or reporting a separately found solution as an optical improvement.

At finite temperature, every accepted non-target exit from B increases
the cost by at least g. The probability of such an exit at step j,
conditional on F_{j-1} and tau>=j, is at most exp(-beta_j g); the total
probability of proposing those states is at most one. Every improvement
requires an exit, even if an uphill exit happens first and all later
behavior is unrestricted. Thus, for a deterministic schedule beta_j>=0,

    P(strict improvement by T)
      <= min(1, T r_L + sum_{j=1}^T exp(-beta_j g)).

If beta_j is itself selected from the random history, the unconditional
statement must instead use

    min(1, T r_L
           + sum_{j=1}^T E[1_{tau>=j} exp(-beta_j g)]).

One may drop the indicator for a weaker bound, or replace beta_j by a
deterministic almost-sure lower bound. A history-random right-hand side
cannot be treated as an unconditional numerical bound without this
expectation. Arbitrary adaptive t,lambda,D are allowed because the same
invariance and r_L apply to every realized choice. The argument does not
require the resulting adaptive chain to have a Gibbs stationary law.

## 8. Constants and exponential rate

All constants above are explicit. In particular a_L<=2^(-L) and b_L<=1,
so r_L<=2^(1-L)<=1/2. An elementary integral bound gives

    L log L - L + 1 <= log(L!)
      <= L log L - L + 1 + log L.

Also (1+1/L)^L<=e, whence

    b_L <= e(L+1) / 2^(L+1),
    r_L <= e^2 L(L+1) (4e)^(-L).

For all sufficiently large L, the uncapped expression defining b_L is
less than one and at least (L+1)/2^(L+1). The lower integral bound on L!
then gives

    r_L >= e(L+1) (4e)^(-L).

Consequently log r_L=-L log(4e)+O(log L). For every polynomial raw-attempt
horizon the zero-temperature upper bound tends to zero. Constant success
under this restricted warm-start mechanism requires an exponential number
of attempts in this sense; this is not a lower bound for solving the graph
optimization problem by arbitrary classical or quantum methods.

## 9. Separate connected extension

Add all edges between CA and CB with a common weight w satisfying

    0 < w < h/L.

The graph is connected and weighted regular. For a balanced subset with
x=|S intersect CA|, the cross-block cut is exactly

    w[x^2+(2L-x)^2] = 2w[(x-L)^2+L^2] >= 2wL^2.

For the four bad whole-clique states x=L, whereas the two component-shaped
targets have x=0 or 2L. Hence

    C_bad(w)  = 2Lh + 2wL^2,
    C_good(w) = 4wL^2 < C_bad(w).

Every partial-clique state has cut at least

    2M(L-1) + 2wL^2 = C_bad(w)+g.

Thus exactly the same two targets improve on B, and the lower uphill gap
g is unchanged. The cross-block adjacency has rank one and annihilates
each D_A,D_B vector because its coordinate sum in that block is zero.
All invariance, sector, and trajectory proofs above carry over unchanged.
The projectors still refer to the fixed blocks CA,CB, which are no longer
connected components of the full graph.

At the concrete choice w=h/(2L), the target cost is 2Lh and the bad cost
is 3Lh. In particular the good cost is not zero. If M,h are positive
integers, scaling every edge weight by 2L produces integer edge weights
2LM,2Lh,h. It scales all cuts and g by 2L; any fixed-temperature statement
must transform beta accordingly. A normalized beta proportional to N/W,
where W is total edge weight, compensates this global scaling.

These graphs remain elementary classical instances. The assumptions give
M>h>w. Edges of maximal weight identify the four heavy cliques. Evaluate
the six balanced unions of two such cliques and select a minimum. The
graph lemma proves this returns an optimum. This uses O(V^2+E) arithmetic
from a matrix or an edge-list representation, with no optimum oracle and
no optical samples. The connected family removes disconnectedness, not
the availability of this elementary classical solution.

## 10. Separate exact graph-only equivariance corollary

There is a broader sufficient condition on the one-particle unitary than
being a scalar function of H. Suppose a deterministic graph-only map
assigns a unitary U(G) on the vertex modes and satisfies the exact identity

    U(P G P^T) = P U(G) P^T

for every permutation matrix P. Every automorphism of the fixed graph
then commutes with U(G).

Inside CA, simultaneous permutations of the L matched pairs, together
with exchanging A1,A2, form a transitive automorphism subgroup acting
identically on CB. Denote it by G_A. There is an independent transitive
subgroup G_B supported on CB. These subgroups exist for both the original
graph and the connected constant-cross-weight extension. The average of
the permutation matrices of G_A is

    R_A = |b_A><b_A| + I_CB.

To see this, the average fixes the vectors constant on each group orbit;
there is one orbit on CA and a singleton orbit for each vertex in CB.
An average over a finite permutation group is the orthogonal projector
onto this fixed-vector space. Thus I-R_A=P_A. Commutation of U with every
group element implies commutation with R_A and P_A. The same proves
commutation with P_B. Equivalently, the cross-block operator has the form

    U_AB = z |b_A><b_B|:

invariance under G_A forces its range into the CA bright line, and under
G_B forces its input functional onto the CB bright line. The diagonal
blocks preserve bright and dark subspaces. This proves the same Fock
sector and trajectory bounds for every such exact graph-only equivariant
unitary, without assuming that it is a spectral function of adjacency.

A history controller may select among maps each having this property;
every realized selected map still preserves the same projectors. This
does not cover covariance only in distribution, independently randomized
symmetry-breaking marks whose realizations do not commute with the
automorphisms, maps equivariant jointly in (G,current subset), or arbitrary
extra sources/modes/nonunitary preprocessing. A finite collection of
relabeling checks is not proof of this exact functional identity.

## 11. Scope relative to P65 and remaining routes

The obstruction starts inside B. Most uniform balanced starts are partial
clique states and are outside the hypothesis. One can apply the same
argument after a stopping time at which a chain enters B, but this says
nothing by itself about the likelihood of doing so or the quality of
earlier proposals. No claim about typical uniform starts follows.

For completeness the total graph weight, including the connected case,
is

    W = 2L[M(L-1)+h+2Lw],       w=0 in the original graph,
    N/W = 2/[M(L-1)+h+2Lw].

For fixed positive M,h, w=0 or 0<w<h/L, and a fixed step index j, the
P65-shaped schedule beta_j=(N/W)2^(j/2) is of order 1/L, whereas g is of
order L. Their product need not grow, and the thermal escape term need
not vanish. The finite-temperature inequality can therefore be vacuous
for that schedule. This is not a no-go theorem for actual P65 annealing,
its registered ER/RR graph cases, or its finite resource budgets. For a
polynomial horizon T=L^p, a sufficient condition for the displayed thermal
term to vanish would be beta_min*g >= (p+delta) log L with delta>0;
no assertion that the actual schedule has this property is made.

Current-dependent encodings, symmetry breaking, different sources,
additional modes, postselection and a different decoder can invalidate
the premises. Studying them would require a new model and proof; no
execution or implementation is authorized here. All probability bounds
above are ideal, normalized, collision-inclusive statements. No wall-time,
physical sampler speed, global optimization advantage, or novelty result
is inferred from them.
