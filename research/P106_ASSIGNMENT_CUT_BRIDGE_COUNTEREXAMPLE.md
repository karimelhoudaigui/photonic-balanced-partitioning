# P106: a transport/permanent proposal and its failed cut-quality bridge

2026-11-26, ROOT, P102 mission; parentf4f1e4c. Manual derivation only.
**Candidate counterexample awaiting independent review; no optimizer run.**
This is a new local transport proposal checked before a pilot, not a positive
benchmark on a selected graph. It does not refute every graph compiler.

## The proposed connection and six mechanism questions

1. Encode cross-boundary graph weights w_ai in a two-source transfer
   T_ai=gamma exp(-lambda w_ai), with gamma chosen to make a contraction.
   Outputs select a balanced two-for-two exchange from a fixed incumbent.
   Row/source fields may also encode the corresponding single-flip costs.
2. B adds coherent matching routes. Unlike D, its exchange cross term includes
   ALL four edges of a2-by-2 cross block, suggesting a useful boundary penalty.
3. D has the same intensities but lacks that cross term; it must independently
   retune lambda, contraction/field parameters and source selection. A same-T
   B/D contrast alone cannot establish a search benefit.
4. Public graph, feasible incumbent, removal pair, all single-flip fields and
   matrix normalization are supplied CLASSICALLY and paid. No C*, optimum
   partition or optimal mask is used in constructing the candidate.
5. Four receiving modes/two source photons admit a six-mode passive dilation
   with two environment modes. Known loss/collisions are failures/self-loops,
   not free postselection. This mathematical dimension is not a verified
   Lucy endpoint or a compiled device bundle. Full inputs/outputs remain paid.
6. A counterexample where larger raw B probability selects a worse exchange
   at equal source/row fields falsifies the claimed universal cost bridge.
   A classical exact local frontier/Gibbs control is mandatory in any sequel.

## The attractive cross term and the unwanted terms

For one receiving pair let X=w_11+w_22 and Y=w_12+w_21. All inputs/outputs
are CF, so occupation factorials are one. With no additional fields,

    p_B/gamma^4=(exp(-lambda X)+exp(-lambda Y))^2,
    p_D/gamma^4=exp(-2lambda X)+exp(-2lambda Y),
    (p_B-p_D)/gamma^4=2exp(-lambda(X+Y)).                  (1)

The interference term IS a Gibbs-like weight for the total cross block.
But it is not an independently accessible positive sample stream: actual
samples retain the two distinguishable route weights as well. Equivalently
p_B/gamma^4=4exp(-lambda(X+Y)) cosh^2(lambda(X-Y)/2).
Imbalance between matching costs can overwhelm the desired total-cost factor.
Subtracting observed D counts would estimate a signed statistic, not produce
free samples from the cross term; its shots/variance and sign must be charged.

For a pure phase map T_ai=gamma exp(i lambda w_ai), the corresponding weight
is4gamma^4 cos^2(lambda(X-Y)/2). It completely loses X+Y. Uniform shifts
of all block weights are a phase gauge but change their total boundary sum.
This also invalidates the automatic total-cost argument for the phase-only map.

## Exact graph counterexample, with equal single-flip fields

Use eight vertices r1,r2,a1,a2,y1,y2,y3,y4. Current balanced side
S={r1,r2,a1,a2}; its complement is all four y vertices. Freeze removal
R={r1,r2}. Edges absent below have weight0. Positive weights are

    w(r1,y2)=w(r2,y1)=3,
    w(r1,y3)=w(r1,y4)=w(r2,y3)=w(r2,y4)=1,
    w(a1,y3)=w(a1,y4)=1.

Candidate Y_A={y1,y2} has cross block [[0,3],[3,0]], X_A=0,Y_Acost=6.
Candidate Y_B={y3,y4} has cross block [[1,1],[1,1]], X_B=Y_Bcost=2.
The naming Y_Acost/Y_Bcost denotes a matching sum, not a partition optimum.
No internal R or internal receiving-pair edge is present.

For spins s_i=+1 on S and -1 otherwise, set h_i=sum_j w_ij s_i s_j.
The four receiving vertices ALL have h_y=-3; both removed vertices have
h_r=-5. Thus source/row factors depending on these local fields agree
between the two candidates and do not cure the following ordering.
For flipping F=R union Y, an exact edge count gives

    Delta C=sum_(i in F) h_i-2sum_({i,j} subset F) w_ij s_i s_j.

Here sum h=-16; internal selected R/Y weights vanish and cross selected
edges have opposite spins. Consequently

    Delta C_A=-16+2*6=-4,
    Delta C_B=-16+2*4=-8.                                  (2)

The B exchange is better, without needing the graph's global C*.
Yet for lambda=1 the raw photon weights are

    p_B(Y_A)/gamma^4=(1+exp(-6))^2 >1,
    p_B(Y_B)/gamma^4=4exp(-4) <1,                           (3)

where exp(4)>1+4>4 certifies the strict inequality. D also ranks them
incorrectly:1+exp(-12)>2exp(-4). B's relative interference enrichment
favors Y_B more than D does (its B/D ratio is2), but still fails to reverse
the physical raw ordering. This illustrates why a real interference effect
does not by itself provide the desired optimization mechanism.

To realize both receiving pairs in the SAME contraction, stack their two
blocks into a4-by-2 matrix F_ai=exp(-w_ai) and take gamma=1/3. Every entry
is<=1, so ||gamma F||op<=sqrt(8)/3<1. This is one common physical transfer,
not separately normalized/fitted circuits for each candidate. A standard
passive dilation exists; no explicit native circuit was generated or run.
Other receiving pairs, losses and collisions still exist and cannot be
deleted from any future data. The counterexample needs no claim about
their distribution: a universal monotone-rank assertion is already false.

## Classical control, scope and continuation

The exact balanced two-for-two gain depends on single-flip fields, TWO
internal-pair weights and ALL four cross weights. A matched classical local
frontier can compute all six receiving pairs here, paying six candidate
scores and shared setup, and returns their best. After at least six attempts
on THIS FIXED proposal pool, no best-of-samples method can exceed that local
quality. This is not an arbitrary outer-trajectory or wall-time theorem.

The positive transfer also falls inside P104's candidate all-K-or-FAIL
classical replacement (after certified rational approximation if needed).
That addresses sampling complexity separately from the sign failure above.
Any future phase/multilayer construction must encode missing internal-pair
and full-boundary information without pre-solving/scoring candidates for free,
and must beat independently reoptimized D and the complete paid frontier.
Neither a global contraction scale nor Sinkhorn balancing supplies that proof.

Disposition: REJECT automatic cut-quality enrichment for this local positive
or phase-only assignment construction. KEEP the algebraic exchange statistic
as a physics relation only; no numerical optimizer pilot is justified yet.
Arbitrary nonlocal encodings, retained partial-loss decoding and large coupled
residual policies remain OPEN, not exhausted by this explicit graph.
All derivations are internal from normalized Fock amplitudes and the cut
definition; P103 supplies adjacent assignment/matching sources. No novelty
claim or experiment/held-out/seed/QPU/manuscript action follows.
