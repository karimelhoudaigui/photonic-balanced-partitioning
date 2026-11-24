# P41/R3 — exact cost classification for two photons and an L1 escape

Base: `f09c7ec82b2fe23395116e21bd56614f3739107c`.
Author: independent obstruction lane. Status: analytic derivation, self-audited;
fresh proof review and finite validation pending. This does **not** establish an
optimization advantage or close the unrestricted P41 target. No QPU result.

## 1. Domain and the exact difference formula

Let V=(u,v) be any complex m-by-2 frame with orthonormal columns, m>=2.
Inject one ideal indistinguishable photon in each occupied input; D routes
the two labelled particles independently through |u_i|^2, |v_i|^2. For i<j,

    p_B(e_i+e_j)-p_D(e_i+e_j) = 2 Re(z_i conjugate(z_j)),
    p_B(2e_i)-p_D(2e_i) = |z_i|^2,
    z_i = u_i conjugate(v_i),  sum_i z_i=0.

These follow by expanding |u_i v_j+u_j v_i|^2 and the repeated-output
normalization |sqrt(2)u_i v_i|^2. All collisional outcomes are retained.

For any real cost f on the complete two-photon occupation space define the
real symmetric matrix K_f by (K_f)_ij=f(e_i+e_j), including
(K_f)_ii=f(2e_i). Then exactly

    E_B f-E_D f = z* K_f z.                                  (1)

There is no postselection or small-angle approximation in (1).

**Theorem (complete same-frame criterion at two photons).**
E_B f>=E_D f for every orthonormal two-column frame V if and only if K_f is
positive semidefinite on 1-perp. Necessity is substantive: for any nonzero
complex h with sum h_i=0, put L=sum_i|h_i| and

    u_i=sqrt(|h_i|/L),
    v_i=conjugate(h_i)/sqrt(L |h_i|) if h_i!=0, otherwise0.

Both columns have norm1 and u*v=sum conjugate(h_i)/L=0; their z is h/L.
Thus every zero-sum direction is physically realizable. Sufficiency follows
from (1). A negative eigen-direction may be chosen real because K_f is real.
The frame extends to a passive unitary; the criterion does not charge finding
or implementing it and is not a computational speedup theorem.

## 2. Penalized absolute-occupation graph cut

Let A be a real symmetric nonnegative adjacency with zero diagonal and

    F_G(n)=sum_(i<j) A_ij |n_i-n_j|,
    M(n)=sum_i n_i(n_i-1)/2,
    H_G,mu(n)=F_G(n)+mu M(n),  mu>=0.

On binary occupations F_G equals ordinary graph cut. For two photons,

    F_G(2e_i)=2d_i,
    F_G(e_i+e_j)=d_i+d_j-2A_ij,
    K_H=d1*+1d* -2A +mu I.

The two degree terms vanish on 1-perp, so

    E_B H-E_D H = z*(mu I-2A)z.                              (2)

Write lambda_perp(A) for the maximum of h*Ah over zero-sum unit h.
The exact no-gain condition is mu>=2lambda_perp(A); strict mean lowering is
physically possible if and only if mu<2lambda_perp(A).
This concerns the same V and complete physical law, not independently trained
models, best-so-far discovery or total resource cost.

For any known feasible pair S0 with cut B, **mu>B** suffices to make every
ground state of H collision-free: every collision has H>=mu>B, while the
feasible state S0 has H=B. This uses no C* but scoring S0 is charged classical
work. Consequently a proper ground-state encoding and a strict same-frame
L1 mean improvement can coexist when B<mu<2lambda_perp(A). The generic
mu>sum_edges A_ij may be too large and must not be silently substituted.

## 3. Explicit connected balanced witness; convex-order proposal refuted

Use m=4,k=2 and the rational Walsh frame consisting of the first two columns
of

    U=(1/2)[[1, 1, 1, 1], [1, 1,-1,-1],
            [1,-1, 1,-1], [1,-1,-1, 1]].

Set A_01=A_23=1, A_12=epsilon, all other weights0, with0<epsilon<1.
The graph is connected. Here z=(1,1,-1,-1)/4, ||z||^2=1/4 and

    E_B H-E_D H = -1/2+epsilon/4+mu/4.

The feasible pair {0,1} has cut epsilon. Therefore any

    epsilon<mu<2-epsilon

gives a proper collision-penalized ground-state encoding and a smaller bosonic
mean. In particular epsilon=1/4, mu=1 gives difference -3/16. Since F_G and
M on nonnegative occupations are convex (M is quadratic plus a linear term),
this refutes the proposed extension of the earlier PSD quadratic theorem to
**all convex occupation costs**. The L1 cost agrees with the cut on every
feasible occupation; the effect is not the old unnormalized CF-energy bug.

For epsilon=0,mu=0 the means are E_B F=1 and E_D F=3/2. The equality of
single-particle means and PSD covariance increase do not imply convex order.
This is not a new optical probability table: its law is the already retained
Walsh example, with a newly considered convex L1 observable.

## 4. Exact graph-class consequence, mu=0

For a simple unweighted graph, E_B F_G>=E_D F_G for all two-photon frames
holds **if and only if G is complete multipartite**, including the empty
graph viewed as one part.

If the parts are C_l, A=11* -sum_l 1_C_l 1_C_l*, so for sum z_i=0,
z*Az=-sum_l|sum_(i in C_l)z_i|^2<=0. Conversely, a graph that is not
complete multipartite has three vertices i,j,l inducing just the edge ij:
nonadjacency-with-equality fails transitivity. The zero-sum vector with
h_i=h_j=1 and h_l=-2 has h*Ah=2>0, giving strict lowering by (2).
This elementary graph classification is not asserted novel; it is a project
consequence of the two-photon optical difference. It does not apply unchanged
to k=m/2 with k>2 or to interacting deterministic spectators.

## 5. What this does and does not open

The earlier convex quadratic occupation route is genuinely too narrow to
exclude this changed L1 objective. A graph-dependent witness can be constructed
from an eigen-direction of the compressed adjacency P A P, P=I-11*/m.
Its classical preprocessing and all information it reveals must be charged.
For k=2, exact sampling is efficient and balanced partitioning has only m=4;
there is no algorithmic or hardware gate from this example.

To scale the mechanism, test genuinely many-body L1-based search on held-out
graphs with a non-oracular penalty. Disjoint fixed-size modules are a rejected
shortcut: a classical correlated sampler can enumerate their tiny local laws,
and can remove physical rejection rather than paying for bosonic collisions.
Any new multi-photon route must compare to this control as well as reoptimized D.

## 6. Source scope

The full two-photon formulas and covariance inputs are established optical
identities; see the existing source audit in theory/phase3_occupation_dominance.md.
The equivalence (1), the L1 specialization and the graph-class consequence are
derived above without external theorem dependencies. Novelty is **unresolved**:
a bounded web search on24-Nov-2026 did not find a matching optical L1 criterion,
but absence of a phrase match is no evidence of global novelty. Searches also
found adjacent Schoenberg/graph-distance literature; its distance matrices are
not this raw adjacency matrix, so those results are not substituted here.
