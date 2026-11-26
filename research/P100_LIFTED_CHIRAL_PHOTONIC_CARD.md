# P100: a lifted chiral passive proposal, with explicit classical and loss vetoes

2026-11-26; parent `49a7b0c5c3161b34b2f723ed52900daffd9ebda6`.
**Stationarity and the cubic term are derived below; no optimizer benefit
is proved.** The claim that a real floor is necessary for nongauge chirality
is refuted below and preserved as such. This reconstructs ROOT's candidate,
not an unseen author's proof. Independent review and attribution are pending;
lifting itself is an established MCMC framework, not presumed new here.

## Source, compiler and actual lifted update

Use m=2K, K>=3, known fresh CF K-photon inputs, vacuum elsewhere and a fixed
global Hermitian H with U_sigma=exp(-i sigma tH), sigma in {+1,-1}.
Freeze H,t and finite alpha>=0 for a chain. Its state is (x,sigma), where
x=[S]={S,S^c}; graph cost C(S)=C(S^c) is finite and minimized. Every attempt
classically chooses source S or S^c uniformly, then observes the FULL counts.
Only exactly K distinct outputs Y produce the class y=[Y]. Every other
count is invalid; no survival/CF conditioning or discarded shot is allowed.

One optimum-blind family is H_G=W+nu J+i kappa[W,D_z], with W the public
real symmetric nonnegative graph-weight matrix, W_ii=0, J all ones,
D_z=diag(z), nu>0 and real kappa. Public distinct continuous vertex marks
are chosen independently of graph/warm start, frozen once, and transported
with graph relabelings. This is Hermitian;
the nu diagonal contributes only an irrelevant common phase. All graph,
matrix, source, phase-programming and training costs are paid. No C*, optimum
mask or known solution enters the source/compiler. Actual calibrated matrix
access, inverse-circuit synthesis and hardware availability are not assumed.

For X=B or D, set p_B(Y|S;U)=|per U[Y,S]|^2 and
p_D(Y|S;U)=per |U[Y,S]|^2. These are raw CF probabilities, factorials one.
The oriented-source average gives off-diagonal proposals

    Q_sigma(x,y)=1/2 sum_(A in x, B in y) p_X(B|A;U_sigma), y!=x.

All remaining probability is a self-loop in this proposal notation. Since
U_-sigma=U_sigma^dagger, OFF-DIAGONAL reciprocity holds exactly:
Q_-sigma(y,x)=Q_sigma(x,y). No identity of the invalid-loop diagonals is
needed or assumed. Use a(x,y)=min(1,exp[-alpha(C(y)-C(x))]). Accept y!=x
with that probability and KEEP sigma. EVERY nonmove FLIPS sigma, including
invalid counts, Metropolis rejection and CF output in the same class.
No permanent ratio is evaluated in that acceptance rule.

## Exact invariant law and its limits

Put pi(x)=exp(-alpha C(x))/Z, R_sigma(x,y)=Q_sigma(x,y)a(x,y), y!=x,
and a_sigma(x)=sum_(y!=x)R_sigma(x,y)<=1. The lifted transitions are
(x,sigma)->(y,sigma) with R_sigma(x,y), and
(x,sigma)->(x,-sigma) with 1-a_sigma(x).
Metropolis cost balance and reciprocity imply

    pi(y)R_sigma(y,x)=pi(x)R_-sigma(x,y).

Under Pi(x,sigma)=pi(x)/2, incoming moving mass to (x,sigma) is
pi(x)a_-sigma(x)/2; incoming flipping mass is
pi(x)(1-a_-sigma(x))/2. Their sum is Pi(x,sigma), proving stationarity.
Ordinary forward-only Metropolis lacks this proof for nonsymmetric Q; it
would generally require a proposal ratio or another global-balance argument.
State-dependent H, directional tuning or arbitrary repair is not covered.

Stationarity alone proves neither irreducibility nor mixing. For nu>0,
nonnegative W and sufficiently small nonzero t, all one-swap moves have
positive leading probabilities. Their graph is connected; nonmove flips
also have positive probability. For K>=3 it contains within-sign triangles,
so this weak window is irreducible/aperiodic. No explicit useful window or
mixing rate is supplied here; an exactly diagonal/revival U can instead trap x.
At Pi the one-step spatial projection averages R_+ and R_- and is reversible.
Any lifted gain would concern temporal persistence, not a different stationary
graph-quality law or a universally favorable instantaneous cost drift.

## Cubic Fock derivation: pair exchange, not a three-source effect

First take sigma=+, lossless. Let i in S, a not in S,
Y=S\{i} union {a}, R=S\{i}, h=H_ai, and
T_iaj=Im(H_ia H_aj H_ji). All H_jj are real. The bosonic amplitude through
second order, obtained by expanding every permanent routing, is

    A_B=-it h-t^2[(H^2)_ai/2+h sum_(j in R)H_jj
                                  +sum_(j in R)H_aj H_ji]+O(t^3).

The extra summands are the exchange i->j->a involving ONE occupied spectator.
Distinguishable two-hop assignments contribute only at probability order t^4.
Direct propagation gives

    p_D(Y|S)=t^2|h|^2+t^3 sum_(j!=i,a)T_iaj+O(t^4),
    p_B(Y|S)-p_D(Y|S)=2t^3 sum_(j in R)T_iaj+O(t^4).             (1)

Diagonal spectator phases have zero imaginary contribution in the cross term;
this checks the sign for U_+=exp(-itH). For K>=3 the other two class routings
have distance K-1>=2, so they enter only at order t^4 or later. The complementary
minimal routing moves a->i, with T_aij=-T_iaj and complementary spectators.
For s_j=+1 on S and -1 off S, define

    Gamma_xy=sum_(j!=i,a) s_j T_iaj.

The factor1/2 from orientation then gives

    Q_B^+(x,y)-Q_D^+(x,y)=t^3 Gamma_xy+O(t^4),
    Q_D^+(x,y)=t^2|H_ai|^2+O(t^4).

Gamma is unchanged if the representative S is complemented, and
Gamma_yx=-Gamma_xy. Time reversal therefore yields the bosonic current
Q_B^+(x,y)-Q_B^+(y,x)=2t^3 Gamma_xy+O(t^5); D's cubic current is zero.
This is two-photon exchange interference. D may have higher-order chiral
terms; it must not be declared reversible or restricted to real H in controls.
K=2 has four minimal midpoint routings, so (1)'s class formula is not asserted.

## The lowest-order signal already has a polynomial classical mirror

Sum Gamma over all one-swap neighbors of x. Terms with two occupied vertices
cancel when those vertices are exchanged; terms with two empty vertices
cancel when those are exchanged. Triangle reversal negates T in both cases.
Thus sum_y Gamma_xy=0. Together with antisymmetry, this is a divergence-free
circulation for the uniform class measure, with no universal graph-cost sign.

An exact classical null at sufficiently small delta is

    Q_cl^sigma(x,y)=delta^2 v_xy+sigma delta^3 Gamma_xy,
    v_xy=|H_ai|^2, for one-swap y; zero for other distinct y.

Choose delta so |delta Gamma_xy|<=v_xy and
delta^2 sum_y v_xy<=1, and fill the diagonal. It is positive stochastic and
has the same off-diagonal inverse-sign reciprocity. The lift above therefore
preserves Pi exactly. For nu>0, let h_min,h_max be the minimum/maximum
off-diagonal moduli. A sufficient explicit global choice is
delta<=min{h_min^2/[(2K-2)h_max^3],1/(K h_max)}: |Gamma|<=(2K-2)h_max^3
and sum_y v_xy<=K^2 h_max^2. Since h_min>=nu, no optimum inspection is needed. Computing
all one-swap coefficients costs O(K^3) arithmetic from public H, not Fock sampling.
At delta=t when admissible, this reproduces the ENTIRE coarse bosonic proposal
through degree3; moves at distance>=2 start at degree4. This null must be paid
and independently optimized. The cubic witness alone cannot show advantage.

## Failed gauge subclaim and usable compiler nulls

For nu=0, H_ab=W_ab[1+i kappa(z_b-z_a)]. Its phase is a gradient only
TO FIRST ORDER in kappa. On a triangle with W_ab=1 and marks (0,1,2),

    H_12 H_23 H_31=(1+i kappa)^2(1-2i kappa)
                    =1+3kappa^2+2i kappa^3.

The nonreal gauge-invariant product refutes the claim that nu is necessary
for nongauge chirality. A floor can expose order-kappa flux on heterogeneous
edge weights; equal weights still cancel that linear term. If z is constant
(e.g. degree marks on a regular graph), [W,D_z]=0 and there is no chirality.
An EXACT phase conjugation D_phi W D_phi^dagger is another null: its photon
probabilities equal those of real W, unlike the linear commutator ansatz.
Reflected kappa exchanges the time-reversed probability kernels; it supplies
no universal favorable sign for the same graph cost. Gauge nulls, not merely
nonzero imaginary matrix entries, are mandatory physics checks.

## Uniform loss: exact waiting law and disappearance of incoming-sign memory

Let q=eta^K for fixed common uniform transmissivity 0<eta<=1 after U_sigma. Only all-K
survival can yield a move, so moving R_sigma is multiplied by q EXACTLY;
every failure still flips. Keep lossless R_sigma,a_sigma in the formulas below.
At a fixed x, write a=a_sigma(x), b=a_-sigma(x), A=a+b and D=A-qab.
If A=0 there is no accepted spatial move. Otherwise the next accepted move,
starting at (x,sigma), has the joint destination/sign law

    J_q(y,sigma)=R_sigma(x,y)/D,
    J_q(y,-sigma)=(1-qa)R_-sigma(x,y)/D,
    E attempts_until_move=(2-qa)/(qD) >=1/q.                    (2)

These follow by summing alternate-failure pairs with factor (1-qa)(1-qb).
All those attempts and K input photons per attempt are paid. As q decreases,
J_q approaches J_0(y,tau)=R_tau(x,y)/A, independent of the incoming sign.
Direct subtraction gives TV(J_q,J_0)=q a^2 b/[A(A-qab)]
<=q/(4-2q), using a,b<=1 and ab/A^2<=1/4. Its spatial projection is
(R_++R_-)/(a_++a_-), reversible with weight pi(x)(a_++a_-).
The attempt-time holding restores pi, not that jump-biased measure. Thus
directional persistence washes out as eta^K->0, while waiting costs diverge.
This is a model limit, not a certified device efficiency or a wall-time result.
Even without loss, the dense weak window has a,b=O(t^2), so the exact TV
formula above gives incoming-sign memory O(qt^2). Frequent same-class flips
already suppress persistence there; retaining sigma on moves alone does not
guarantee a useful directed excursion.

## Cheapest meaningful falsification, before any DEV authorization

Prospective algebraic qualification must check (1), its opposite-time sign,
orientation/complement equivalence, sum Gamma=0, exact gauge/real nulls and
lifted balance on a tiny full-state example, retaining zeros and invalid counts.
It must also check the failure-pair calculation (2). No such computation is
authorized or reported here. A cubic nonzero witness verifies physics only.

Before attributing any optimizer signal, compare independently reoptimized
D with complex compiler/time controls, groups of two and three indistinguishable
photons, and the classical triad-current lift. Expose all compiler features;
pay setup, source/phase changes, sampling, every scored candidate and any quench.
Use common feasible warm starts, fresh unplanted graphs/relabels and transported
marks, no C*/known-solution preparation or free portfolio. Exact Fock simulation
is not optical latency; both its cost and a favorable-zero-optics veto must be
disclosed. A later prospective contract/review must freeze parameters and budgets.

Generic collision/loss repair need not preserve inverse-sign reciprocity; a
balanced all-output decoder requires a separate proof and cannot be silently
substituted. Nonuniform directional loss, adaptive H and source uncertainty
also require new arguments. P99's reversible comparison does not directly apply
to this lift: even a D control with more within-sign moves has fewer flips,
so it does not dominate all lifted off-diagonals. That is an escape from the
proof's premise, not evidence of improvement or a positive optimization gate.
Only this note changed. No code/import/AST/scientific execution/RNG/graph/native/
test/runner/QPU/paper/push/checkout/delegation occurred. Positive goal remains OPEN.
