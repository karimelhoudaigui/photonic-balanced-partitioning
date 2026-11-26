# P100 independent lifted-chiral proof audit

Reviewer `/root/p66_dark_audit`, 2026-11-26; `proof-audit` workflow.
Primary verdict: **PROVED AS WRITTEN under the stated all-nonmoves-flip policy**.
Loss-induced sign-memory washout is POLICY-SPECIFIC, not an intrinsic no-go
for every lossy chiral policy. No optimization benefit is proved by these identities.

Exact source: `research/P100_LIFTED_CHIRAL_PHOTONIC_CARD.md`, all 203 lines,
commit `f7d3ba94506fa9b462612e062bf1b1b7bed16cb6`, SHA256
`45586c2b6f243f7edc814775fbfd4546e0e1219b66d2dd7b9480c5b4489b56c6`.
The author supplied this frozen identity before review. This is a non-author
independent reconstruction; neither parent nor author verdict is a proof leaf.

## Typed model and obligations

m=2K,K>=3, global fixed Hermitian H,t, fresh known CF K-photon sources,
vacuum elsewhere, and an independent uniform choice of S/S^c each attempt.
Only complete K-distinct CF outputs change the unoriented class x=[S].
Every other event, including same-class CF and rejection, flips sigma.
Accepted different-class moves keep sigma. Full counts are retained; no CF or
survival renormalization occurs. Both signs use the same finite graph cost,
finite alpha>=0 and Metropolis acceptance, independent of any optimum mask.
Uniform optional loss has fixed common 0<eta<=1 AFTER U_sigma=exp(-i sigma tH).

Dependency map: inverse-unitary reciprocity -> skew cost balance -> invariant Pi;
CF route expansion -> cubic coefficients/orientation -> antisymmetric Gamma;
triad cancellation -> polynomial classical null;
alternating failure renewal -> waiting/sign law -> fixed-state memory bound.
These obligations, compiler/gauge checks and weak-window connectivity pass.
Global optimizer, matched-cost, hardware, novelty, finite-time speed and adaptive
H claims are not established. All load-bearing proof leaves below are internal.

## Off-diagonal reciprocity and exact lifted stationarity

For CF sources/targets all factorials are one. B has probability |per U[Y,S]|^2;
D aggregates independent labeled assignments to per |U[Y,S]|^2. Since
U_-sigma=U_sigma^dagger, raw input/output reversal exchanges signs. Summing
the two source and two target representatives, with SOURCE factor1/2,
gives Q_-sigma(y,x)=Q_sigma(x,y) off the diagonal. No equality of filled
invalid-loop diagonals, row activities or same-sign reverse rates follows.

With pi proportional to exp(-alpha C), define R_sigma=Q_sigma a, y!=x,
a_sigma(x)=sum_(y!=x)R_sigma(x,y). Common cost acceptance gives
pi(y)R_sigma(y,x)=pi(x)R_-sigma(x,y).
Incoming moving mass under Pi(x,sigma)=pi(x)/2 is pi(x)a_-sigma(x)/2;
incoming flip mass from (x,-sigma) is pi(x)(1-a_-sigma(x))/2.
Their sum is Pi(x,sigma). This proves stationarity without a permanent ratio.
Flipping only selected nonmoves, arbitrary repair, adaptive H or changing
directional tuning cannot inherit this calculation without another balance proof.

For the displayed compiler, [W,D_z]_ab=W_ab(z_b-z_a) is real antisymmetric,
so i kappa[W,D_z] is Hermitian. W>=0 and nu>0 imply |H_ai|>=nu off diagonal.
The common nu diagonal is only a global phase; the off-diagonal floor remains.
Frozen transported marks preserve the stated relabeling convention; distinct
marks alone do not prove a useful sign or a nongauge effect on every graph.
For sufficiently small nonzero t, all one-swap rates are positive to order t^2,
and finite alpha preserves their positivity. Their class graph is connected;
flips have positive probability because nonmoves approach one. A flip gives a
2-cycle and within-sign one-swap triangles give a 3-cycle for K>=3, hence
irreducibility/aperiodicity in some weak window. No useful explicit rate follows.
For diagonal or revival U, spatial trapping and nonunique invariant laws remain
possible; the stationarity proof alone never excludes them.

## Cubic factors reconstructed from Fock routes

Fix S, i in S, a outside S, R=S\{i}, h=H_ai. Put
T_iaj=Im(H_ia H_aj H_ji). In the CF permanent the identity-on-spectators route
has U_ai product_(j in R)U_jj. At amplitude order t^2 the only additional
assignments are i->j and j->a for one occupied spectator j. Therefore
A_B=-it h-t^2 B+O(t^3),
B=(H^2)_ai/2+h sum_(j in R)H_jj+sum_(j in R)H_aj H_ji.
The probability cross term is +2t^3 Im(conj(h)B), checking the sign for -itH.
Diagonal H_jj are real. Distinguishable exchange assignments cost probability
order t^4; their direct route has cubic coefficient Im(H_ia(H^2)_ai).
Thus p_D=t^2|h|^2+t^3 sum_(j!=i,a)T_iaj+O(t^4), and
p_B-p_D=2t^3 sum_(j in R)T_iaj+O(t^4), exactly (1).
No three occupied sources are required for this exchange correction.

The complementary minimal route removes a and inserts i, with T_aij=-T_iaj
and spectators S^c\{a}. The other two orientation routes have distance K-1>=2,
so enter probability at order >=4. Their source average cancels D's cubic
coefficient and leaves B-D coefficient
Gamma_xy=sum_(j!=i,a) s_j T_iaj, s_j=+1 on S and -1 otherwise.
Complementing the representative negates both s and the directed triad, hence
leaves Gamma invariant. Reversing the move keeps spectator spins and negates
the triad, so Gamma_yx=-Gamma_xy. Inverse-sign reciprocity and analyticity give
Q_B^+(x,y)-Q_B^+(y,x)=2t^3 Gamma_xy+O(t^5).
Only the odd Taylor terms survive subtraction; the O(t^4) terms cancel.
D's cubic current vanishes, but its higher-order current is not proved zero.
K=2 has additional minimal midpoint routings and is expressly outside this formula.

## Classical cubic-current null and exact gauge counterexample

Sum Gamma over the K^2 distinct one-swap neighbors (no complement duplicates
when K>=3). For occupied j, pair the term (i,a,j) with (j,a,i); their triads
are conjugate. For empty j, pair (i,a,j) with (i,j,a); their triads are conjugate
and their spin signs agree. Both pairs cancel, proving sum_y Gamma_xy=0.

v_xy=|H_ai|^2 is symmetric. Hence Q_cl^sigma=delta^2 v+sigma delta^3 Gamma
on one-swap edges, zero on other distinct classes, has inverse-sign reciprocity.
If |delta Gamma|<=v, it is nonnegative; divergence zero makes its row sum
delta^2 sum_y v. Fill the diagonal when that sum<=1. The displayed bounds
|Gamma|<=(2K-2)h_max^3 and sum v<=K^2 h_max^2 give the claimed sufficient
0<=delta<=min(h_min^2/[(2K-2)h_max^3],1/[K h_max]). h_min>=nu>0 makes it usable.
Its lifted Metropolis kernel has the SAME invariant Pi by the proof above.
At admissible delta=t it matches the entire COARSE class/sign proposal through
degree three, including filled nonmoves; it does not simulate the full invalid
PNR record law. Computing all coefficients from paid public H costs O(K^3).
This null and independently optimized complex-H D/groups must not be omitted.

At nu=0, unit triangle weights and marks (0,1,2) give
(1+i kappa)^2(1-2i kappa)=1+3kappa^2+2i kappa^3.
For real nonzero kappa this loop product is nonreal and gauge invariant,
so no vertex-diagonal phase conjugation can make all hoppings real. This
validly refutes the preserved claim that a real floor is necessary for chirality.
The phase is a gradient only at first order. Heterogeneous floor/edge ratios
can expose linear-kappa flux; equal ratios cancel that linear contribution.
Constant marks give zero commutator. Exact H=D_phi W D_phi^dagger gives
U=D_phi exp(-itW)D_phi^dagger, whose Fock amplitudes acquire only input/output
phases, leaving all count probabilities unchanged. Imaginary entries alone are
therefore not a physics witness. Reflecting kappa conjugates H and exchanges
the inverse-time probability kernels; it supplies no universal graph-cost sign.

## All-failure-flip renewal and its exact uniform-loss cost

At fixed x start with incoming sign sigma. Write q=eta^K, a=a_sigma(x),
b=a_-sigma(x), A=a+b, D=A-qab. R_sigma here is LOSSLESS. All-K survival
multiplies moves by q; every other result flips. This is qL_1+(1-q)F_flip,
not ordinary lazy slowing. If A=0 no move ever occurs. For A>0,q>0,
D>=A(1-q/2)>0. A pair of failures has probability (1-qa)(1-qb).
Summing its geometric series gives
J_q(y,sigma)=R_sigma(x,y)/D,
J_q(y,-sigma)=(1-qa)R_-sigma(x,y)/D.
The masses sum to [a+(1-qa)b]/D=1. First-step equations
E_sigma=1+(1-qa)E_-sigma and E_-sigma=1+(1-qb)E_sigma yield
E_sigma=(2-qa)/(qD)>=1/q;
the last inequality follows from 2-qa-D=(1-a)+(1-b)(1-qa)>=0.
Every attempt, not only an accepted jump, costs K injected photons.

As q decreases, J_q tends to J_0(y,tau)=R_tau(x,y)/A independently of incoming
sign. The sigma component's excess mass and opposite component's deficit are
both qa^2b/[A(A-qab)], proving the exact TV formula, including a=0 or b=0.
Using ab/A^2<=1/4, a<=1 and ab/A<=1/2 gives TV<=q/(4-2q).
In the dense weak window a,b=O(t^2), this is more specifically O(qt^2).
No global trajectory/mixing or optimizer domination follows from this one-jump
fixed-x memory bound without accumulation and resource arguments.

## Fixed-state, stationary, jump-time and policy qualifications

At Pi, sigma conditional on x is uniform. The ONE-STEP spatial off-diagonal rates
are q(R_++R_-)/2, completed by holds, a reversible pi-kernel. This does not make
the spatial projection a Markov process conditional on an entire observed history.
The limiting fixed-x J_0 spatial kernel is (R_++R_-)/A, reversible with weight
pi(x)A(x), on positive-activity states. A=0 states have no jump distribution.
This jump-biased weight is distinct from attempt-time pi. For finite q and a
fixed incoming sign, J_q's spatial kernel is generally NOT that J_0 formula.
Invariant Pi was proved directly for all q; no favorable stationary quality or
uniform instantaneous cost-drift sign follows. Gains, if any, concern dynamics.

ROOT-suggested counter-continuation, rederived here, to an INTRINSIC loss no-go
(not to P100 as stated): with
true PNR, retain sigma on N<K; only N=K nonmoves flip, as in lossless L_1.
Uniform loss then gives exactly L_tilde_q=(1-q)I+qL_1. Pi stays invariant;
accepted-jump sign memory equals the lossless skeleton, while raw waiting means
and photon cost inflate by 1/q. This follows by deleting independent loss holds,
not by discarding their cost. D and the classical null inherit the same option.
Thus changing the policy can avoid THIS washout, not the eta^K waiting penalty
or the strong comparisons. Threshold clicks generally cannot distinguish loss
from a full-photon collision; actual PNR/Lucy capability is not certified here.

Balanced repair of every raw count, nonuniform loss, adaptive compilers and hidden
source state require new reciprocity/balance arguments. P99's form-order proof
does not automatically apply: more within-sign moves reduce cross-sign flips,
so full lifted off-diagonal dominance is absent. Escaping that premise is not
a positive result. No trained C*, known solution, free conditional branch or
unpaid classical feature is supplied by this card. No code/import/AST, numerical
calculation, RNG/native/test/runner/QPU call, raw-data read, push, manuscript edit
or delegation occurred; P98 is unchanged and P104 remains unread. Remaining
gaps are independently replicated, fully costed optimization and attribution.
