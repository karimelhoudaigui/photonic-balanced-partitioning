# P36 continuation: variational witnesses for the pinched trace distance

2026-11-22, coordinator derivation at5375202, exchanged with /root/physics.
This is a matrix reduction and a singular-boundary obstruction, not a proof
of TV<=delta. The variational ingredients are standard; no novelty claim.
No manuscript or hardware change. Numerical falsification of the stronger
pinched-state bound is a separate P38 task.

## Measurement and normalization

Let V be an m-by-k orthonormal occupied frame and partition output modes into
S_g, assigning each row to a largest squared column entry. Define effects
E_g=V^dagger P_(S_g)V on the k-dimensional input span, so E_g>=0 and
sum_g E_g=I. Both states below use the first-quantized tensor-product space:

    |s>=1/sqrt(n) sum_pi |pi(1),...,pi(k)>,
    rho_d=1/n sum_pi |pi><pi|,                  n=k!.

Apply V to each particle and pinch each factor by the P_(S_g). This preserves
internal degrees of freedom inside every region. The fine output occupation
measurement commutes with this pinching. Thus its TV is at most the trace
distance of these two pinched states; replacing fine outcomes by grouped
counts would give the wrong inequality direction.

For a sector t=(t_1,...,t_k), let a_pi be the unnormalized product vector
tensor_j P_(S_(t_j))v_(pi(j)). Its n-by-n Gram matrix is

    (G_t)_(pi,sigma)=product_j (E_(t_j))_(pi(j),sigma(j)).

Let K=J_n-I_n. The sector difference is T_t K T_t^dagger/n, with columns
of T_t equal to a_pi. Polar decomposition identifies its nonzero eigenvalues
with those of sqrt(G_t)K sqrt(G_t)/n. Since K has at most one positive
eigenvalue, so does this sector difference. Sum_t G_t=I_n and the traces of
the normalized differences sum to0. Therefore the exact pinched distance is

    D_pinched = (1/n) sum_t F(G_t),
    F(G)=Tr[(sqrt(G)K sqrt(G))_+].

This fixes both the factorial and the final factor1/2: the latter disappears
only after summing all sectors with zero total trace. Individual sector
trace norms cannot be replaced by their positive eigenvalue without that
trace bookkeeping. For k3 there are27 sectors and6-by-6 Gram matrices.

## Exact variational identity and usable upper witnesses

For any Hermitian K and PSD G,

    F(G)=max_(0<=X<=G) Tr(KX)
        =inf_(Z>=0, Z>=K) Tr(GZ).

Proof of the first equality: 0<=X<=G implies X vanishes on ker G. On the
support write X=sqrt(G)W sqrt(G), 0<=W<=I. Diagonalizing
H=sqrt(G)K sqrt(G), the maximum of Tr(HW) is Tr(H_+).

For every feasible dual Z, Tr(KX)<=Tr(ZX)<=Tr(ZG); hence each such Z gives
a rigorous upper bound. If G>0, choose Z=G^(-1/2)H_+G^(-1/2). It is PSD,
Z-K=G^(-1/2)H_-G^(-1/2)>=0 and its cost equals Tr(H_+). If G is singular,
apply this construction to G+epsilon I. The resulting Z_epsilon remains
feasible for K and has cost against G at most F(G+epsilon I). Continuity,
together with weak duality, yields equality of the infimum with F(G).
Attainment has not been claimed for singular G.

The primal also proves concavity in G: convex combinations of feasible X's
are feasible for the same combination of G's. It proves positive homogeneity
and Loewner monotonicity. This does **not** imply concavity in the common
effects E_g: G_t depends on them with total degree k.

For K=J_n-I_n, the constant witness Z=(n-1)J_n/n is feasible because
Z-K=I_n-J_n/n>=0. Using sum_t G_t=I_n gives

    D_pinched <=(n-1)/n.

At k3 this recovers5/6, a known universal symmetrized-versus-mixture bound.
It proves TV<=delta only in the already trivial regime delta>=5/6.

## A false minimum statement, retained explicitly

My initial message used `min` in the dual formula for every PSD G. That
attainment claim is false; the physics agent independently checked the same
restriction. Take n=2,K=[[0,1],[1,0]],G=diag(1,0). Then F(G)=0.
If feasible Z had cost0, PSD would force the first row of Z to vanish.
PSD of Z-K, whose first diagonal entry would also be0, would force its first
row to vanish too, contradicting the off-diagonal entry -1. Yet

    Z_epsilon=[[epsilon,1/2],[1/2,1/(4epsilon)]]

and Z_epsilon-K are PSD, with cost epsilon. Thus the infimum is0 and is
not attained. Divergent witness entries near disjoint supports are possible;
a bounded continuous dual ansatz must not be assumed without proof.

## Open mathematical obligation

For complex k3 the dominant-refinement cone has a useful exact reduction.
Fix g and consider C_g={E>=0:E_gg>=E_aa for every a}. Every such effect is
a sum of rank-one effects with the same dominant label. Here is a direct
finite-dimensional proof. Normalize a nonzero E to trace1. If rank r>=2,
the Hermitian operators on its support have real dimension r²>=4. Trace0
and the at most two active diagonal equalities impose at most three real
linear constraints. Choose a nonzero support perturbation H satisfying them.
For small positive/negative t, E+tH stays PSD and preserves all active
constraints; inactive inequalities remain strict. Extend t both ways to the
ends of its feasible interval. Trace1 makes this interval bounded. Each end
either loses rank or gains an active inequality. E is a convex combination
of the ends. Repeating terminates: along each branch rank only decreases
and the set of active equalities only grows. At rank1 each terminal effect
is rr^dagger with |r_g|²>=|r_a|².

Finally at most9 terminal effects are needed: trace-one Hermitian3 matrices
have affine dimension8, so any longer convex representation has an affine
dependence; shifting its weights along that dependence until one vanishes
reduces its length. Thus three effects E_g>=0 with sum I and diagonal
dominance each admit a physical rank-one refinement with at most27 rows.
The resulting frame has orthonormal columns. Any allowed maximizing label
may be fixed on ties; delta itself is tie independent. This reduction is
special to complex dimension3: at dimension4 rank2 has four parameters and
the active constraints can already prevent the perturbation argument.

This cone argument was proposed by the physics agent before its next quota
interruption and reconstructed here. It is not a returned independent proof
audit. For the sufficient pinching bound one may therefore study the compact
three-effect PSD domain directly, not assume that every larger column count
admits the same refinement argument.

For k3, find admissible witnesses Z_t (or another argument) with

    sum_t Tr(G_t Z_t)<=6 delta,
    delta=sum_g[Tr(E_g)-(E_g)_(g,g)].

Orthogonality supplies sum_g E_g=I, including zero off-diagonal sums. These
phase cancellations might eliminate troublesome terms after sectors are
summed. Entrywise absolute-value permanent bounds already fail and must not
be reused. A numerical violation of D_pinched<=delta refutes this stronger
route, not necessarily the measured TV conjecture. Even a proof of the
stronger bound would require exact source/novelty audit and would not imply
an optimization advantage.
