# P118 independent strict nonreturn-walk review

2026-11-26. Non-author MANUAL proof review; no calculation was executed.
Source FULL read: `research/P118_NONRETURN_WALK_ROUTE.md`, 154 lines,
commit `1111db217354a9c9183dfbd62ae49185753b4152`.
SHA256 `ceb0a6523ff7f31742887394b6e166fa5ee78535ded56ccb238265973212d21a`.
Separate soft source FULL read: `P118_SOFT_RETURN_CONTROL_ADDENDUM.md`,
122 lines, commit `a43e5ef266929fad34180c535720e6929c485a7d`, SHA256
`b27a9dc3903fecb3bfa8f44f6a7bca02d74d33b2c8787b6f86e97c20dbe5f39c`.
Review parent: `196c585febbf4a104ce17d40e51719b27e3ca3d7`.

**PROVED AS WRITTEN within the explicitly defined strict arc-memory class.**
The cycle table, monomial obstruction, 12-mode lower bound and sharpness
construction all check. This is equality of ideal raw counting laws and
coupled classical transcripts, stronger than a mean identity. It is not a
theorem about arbitrary small passive circuits or every no-return policy.
**SOFT ADDENDUM: proved under its count-measurement/common-classical-kernel
hypotheses; it is not a quadratic quantum trace-distance or arbitrary-loss bound.**

## Architecture and hand table

The auxiliary C4 has four undirected edges, hence EIGHT distinct directed
arc modes, including empty modes. |u,v> really records previous/current
vertices. A zero diagonal in the neighbor-indexed coin forbids returning
to u; it is not merely the absence of a self-loop on a vertex-mode walk.
The specified two-neighbor rule sends |u,v> to |v,other(v,u)> with a phase.
There is a unique predecessor of every outgoing arc, so it is a permutation
with unit-modulus weights, hence unitary. W>=0 makes its compiler denominator
1+W positive, and the graph phase needs no optimum or feasible-state mask.

For initial S={0,1}, incoming + at 0 is |3,0>, incoming - is |1,0>;
at 1 they are |0,1> and |2,1>. Applying the rule directly gives

| Memory | Outgoing current vertices | Pair class |
|---|---|---|
| ++ | 1,2 | {0,3} |
| +- | 1,0 | {0,1} |
| -+ | 3,2 | {0,1} |
| -- | 3,0 | {0,3} |

Each occurs with probability 1/4 under the declared independent memory
coins. Thus the two listed classes have mass 1/2 and the opposite class
{0,2} has mass zero, for arbitrary task-graph weights. No arc or vertex
bunch occurs in this particular adjacent-source table. Other sources can
share a CURRENT vertex while occupying distinct arc modes; the total decoder
explicitly retains these events. Neither case depends on compiled phases.

## Structural obstruction and sharpness

Assumptions matter: the auxiliary graph is simple, undirected and loopless;
the complete mode space is its 2E directed arcs; EVERY incoming basis arc
has a lossless vertex-local scattering coin with zero return diagonal.
Degree one is impossible because its 1-by-1 unitary would have nonzero
diagonal. Degree two forces a swap with phases. For degree three, any two
different rows share at most one potentially nonzero column, since the two
diagonal entries are zero. Orthogonality forces that single product to
vanish. Every column therefore has at most one nonzero entry. Unitarity
requires exactly one in every row and column, of modulus one: monomial.

A nonmonomial coin consequently requires degree at least four. Its four
distinct neighbors must each have degree at least two because degree-one
coins are forbidden. Their degrees plus the hub give a degree sum at least
4+4*2=12, hence E>=6 and m=2E>=12. Other vertices/components only increase
the count; isolated vertices supply no optical arc modes. This proves the
claim for every m<=10, not only the example at eight modes.

The figure-eight graph of two triangles sharing a hub has exactly six
edges, hub degree four and all four other degrees two. At the hub,
[[0_2,H_2],[H_2,0_2]] with H_2=[[1,1],[1,-1]]/sqrt(2) has orthonormal
rows, zero diagonal and two nonzero entries per row. Outer vertices use
swaps. Thus twelve is genuinely sharp for admitting a nonmonomial local
coin. It is NOT a demonstration of useful interference or graph optimization.

## Full-law equality and adaptation

The arc shift is a permutation, and products of monomial matrices remain
monomial on the counted common mode space. Thus U|a>=exp(i theta_a)|p(a)>.
For a fixed known CF input, the many-photon output has deterministically
the pushed-forward occupation p_*n. Normalized Fock phases cannot change
that probability. D's labeled photons deterministically take the SAME
output modes, so B/D/classical mode occupations agree exactly. Vertex
aggregation, stochastic tie decoding, repair and best-recorded scoring
preserve equality when their rules/coins are shared.

The transcript claim follows by induction for shared classical controllers:
equal current records and coupled fresh coins choose the same next source,
monomial step and paid preparation; their next records agree again. It
requires that every stage remain in the stated class and every register,
memory/flag/mode used be counted. An independent D search family already
contains this copying control; reproducing its law needs no optimizer oracle.
No independence of different attempted optical steps is needed for this
conditional equality. Costs of graph loading, compiler, reset/memory, decoder
and every score remain real, so equality of ideal counts is not a measured
wall-time or total-cost benchmark. The three-cut classical frontier remains
an additional paid comparison for the four-vertex task graph.

## Exact limits of the conclusion

Simple-graph, vertex-local, lossless and strict-for-all-input hypotheses are
essential. Parallel edges, loops, nonlocal coins, extra coherent registers,
nonvacuum helpers or altered sources require a new analysis. The soft-return
concentration below changes the strict class and leaves a deeper regime open.
A zero-diagonal four-mode unitary on vertices does not satisfy the claimed
edge-memory encoding merely by having zero diagonal. Unverified source,
detector/loss or routing effects cannot silently inherit the ideal input law;
they need their actual common record/fallback model and raw denominators.
The internal finite proof does not rely on an external quantum-walk mixing
theorem or transfer a classical mixing rate into cut-quality improvement.
Accept rejection of THIS strict small-mode route before a pilot; retain
all broader routes as unevaluated. No source/experiment/graph-seed/QPU/paper
or code change occurred. Only this review was written, with manual algebra,
text/hash/Git inspection and no imports/AST/tests/RNG/native/scripted run.

## Separate soft-return audit: which quadratic statement is valid

This addendum concerns the eight-mode C4 with LOSSLESS 2-by-2 local coins,
known CF K in {2,3,4}, one fixed U and an integer L>=0 coherent depth.
It does not automatically cover degree-three soft coins on other graphs.
For a coin [[a,b],[c,d]], row/column normalization gives |a|=|d|=r<=epsilon,
|b|=|c|=sqrt(1-r^2)>0. The normalized off-diagonal swap M is unitary;
the diagonal difference has norm r and the off-diagonal difference norm
1-sqrt(1-r^2). Thus ||C-M||<=delta=epsilon+1-sqrt(1-epsilon^2), with
the stated monotonicity, direct-sum and shift bounds. Epsilon<1 is essential
to normalize phases. At epsilon=0 M=C; at L=0 both powers are I.

Unitary telescoping gives ||U^L-U0^L||<=Ldelta. Symmetric tensor telescoping
then bounds the B state-vector difference from its OWN monomial CF reference
exp(i theta)|n0> by KLdelta. Projecting off |n0> before squaring proves
P_B(n!=n0)<=min(1,K^2L^2delta^2). Each labeled D particle has off-designated-
mode probability <=L^2delta^2. Union bound gives P_D(n!=n0)<=min(1,KL^2delta^2);
some label errors can cancel in counts, which only weakens this bound.
With TV defined as half L1, distance to a point mass is its off-point mass.
Triangle inequality therefore gives exactly tau=min(1,K(K+1)L^2delta^2),
without an extra factor two. Mean differences of a range-R score are <=Rtau.
The D control is the SAME U, not an assumed optimized or physically supplied U0.

The quadratic claim is about NUMBER COUNTS ONLY. For example the pure
state cos(t)|n0>+sin(t)|n1> has count distance sin^2(t) from |n0>, but
quantum trace distance |sin(t)|. Its coherent off-diagonal terms are first
order. Thus projecting onto the count complement cannot justify a quadratic
trace-norm estimate or arbitrary subsequent quantum-channel contraction.

A genuine common classical kernel on the final count alphabet contracts TV.
Terminal tag-independent independent port loss has the binomial thinning
kernel product_j binom(n_j,m_j)eta_j^m_j(1-eta_j)^(n_j-m_j), so it qualifies;
thresholding and total common randomized repair also qualify. An arbitrary
physical loss/mixer interleaved with coherent evolution need not be this
kernel. Neither common hardware wording nor a common efficiency proves it.

An explicit scope counterexample: start from CF |1,1> with a monomial walk,
so the preceding B/D count TV is zero. A later balanced beam splitter gives
B probabilities (1/2,0,1/2) versus D (1/4,1/2,1/4) on (20,11,02), TV=1/2.
The added coherent mixer cannot be treated as a common stochastic map of
the preceding count law. The source addendum correctly excludes this case.

Rare conditioning is another distinct operation: the count laws
(1-p)delta0+p delta1 and (1-p)delta0+p delta2 have raw TV=p, but conditioning
both on {1,2} gives TV=1. Common TOTAL repair is allowed; normalizing a rare
accepted/CF subset afterward is not covered by tau. No failures become free.

Finally delta=epsilon+epsilon^2/(1+sqrt(1-epsilon^2)) is O(epsilon).
For fixed K and L epsilon->0, tau->0, with all raw events retained. At
L of order 1/epsilon the bound can be finite or vacuous and supplies neither
an impossibility nor a useful signal. That deeper soft-return regime remains
OPEN pending an actual graph-dependent statistic and strong controls. L is
depth, not wall time; preparation, K photons and all L operations remain paid.
Accept this separate scoped concentration theorem. No calculation, code,
experimental population, device capability or optimizer result is supplied.
