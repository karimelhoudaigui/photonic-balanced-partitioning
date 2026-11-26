# P99 independent weak-passive/control proof audit

Reviewer `/root/p66_dark_audit`, 2026-11-26, parent `afefa4cb8074e8681b5f7eed17532b67a828f216`.
Primary verdict: **PROVED AS WRITTEN in the precise stated model**.
The optional lazification sentence uses the conventional half-lazy transform;
arbitrary nonzero holding alone would not guarantee nonnegative spectrum.
No optimizer advantage, equal-cost domination or actual warm-start result follows.

Exact source: `research/P99_WEAK_PASSIVE_REOPTIMIZED_D_CARD.md`, all 198 lines,
commit `a8e80a10d5ae9e1f54e371c613240276a79b40f4`, SHA256
`8543039fc6346a8beb6f8fcb626863067c13b3e43a5e8f47dd03b168bf8e8bb1`.
This is a non-author independent reconstruction of the frozen shared candidate;
the source/parent verdict is not used in place of a proof below.

## Claim card and dependencies

2<=K<=12, m=2K, fixed GLOBAL dense REAL symmetric H, |H_ai|>=b>0 off diagonal,
lambda=||H||op; both t and 2t are admissible in the same family.
Fresh known CF input each raw attempt; source S or its complement is chosen
independently with probability1/2, a classical mixture. Output classes are
unoriented bisections; every collision/loss is a self-loop. Optional loss has
one common uniform 0<eta<=1. The Metropolis graph cost is complement invariant
and finite, alpha>=0 is finite/fixed, and both chains use the same acceptance.
Target A is nonempty and proper, used in ANALYSIS, not a policy/optimum mask.

Dependency graph: normalized CF/labeled routing -> class orientation average
and reciprocal proposals -> leading coefficient inequality + uniform Taylor
remainder -> explicit strict window -> irreducibility/common reversible target
-> Dirichlet/Rayleigh order -> killed inverse order -> pi-outside hitting mean.
Obligations routing / orientation / remainder / threshold / eta / irreducibility /
reversibility / Rayleigh / killed mean **passed**. Finite precision, cost matching,
hardware/novelty, all-start hitting/mixing and annealing claims **not established**.
All load-bearing leaves below are internal finite algebra/calculus, not numerics.

## Full raw law, orientation factors and reciprocity

For CF input/output, each factorial is one. B's transition amplitude is per U[Y,S];
D independently sends K labeled particles and sums K! feasible assignments,
giving per |U[Y,S]|^2, with no extra divisor. Output events Y and Y^c are
disjoint. Averaging TWO source states gives exactly eta^K/2 times the FOUR
input/output-orientation probabilities, not an average over four source choices.
Invalid outcomes complete the row to a stochastic self-loop; no CF normalization.
H^T=H implies U^T=U, so each raw probability is reciprocal. The full four-term
sum is invariant on exchanging classes. This proves symmetry of Q, including
its row-completing diagonal. Without the fresh orientation mixture this inference
is generally false; a concrete counter to that weakening is given below.

Choose S,Y at class distance r=min(|S\Y|,K-|S\Y|), 1<=r<=floor(K/2).
Partition modes into C=S intersect Y, B=S\Y, A=Y\S, D=S^c intersect Y^c.
A new output needs an off-diagonal amplitude -it H_ai+O(t^2).
At exactly r such factors, every shared input remains on its own output;
the moved block contributes (-it)^r per H[A,B]. Distinguishable paths instead
add squared products, giving d(M)=per |M|^2 at probability order 2r.
For r<K/2, the minimal blocks are H[A,B] and its transpose; the other pair
has distance K-r>r. Hence the factor1/2 cancels these two equal coefficients.
At the even-K midpoint all four are minimal: two transpose pairs give a sum
of TWO block coefficients, for both B and D. No cross term joins these blocks
because the source orientations are a mixture and the target outcomes disjoint.

For each block, |per M|^2<=r! per |M|^2 by Cauchy on its r! route amplitudes.
Density ensures every squared product >=b^(2r), so d(M)>=r! b^(2r).
Summing midpoint blocks preserves beta_xy<=r! d_xy and strengthens the lower
bound to 2r!b^(2r); using only r!b^(2r) is conservative. K=2 is entirely this
midpoint case; K=3's maximal distance is r=1 with only one effective block.
Signs/cancellations may make beta_xy=0 but cannot cancel d_xy. Diagonal phases
and common-mode rerouting enter higher orders, not the leading coefficient.

## Uniform remainder, threshold and B connectivity

On symmetric K-particle space, or the labeled tensor space, G=sum_i H_i has
||G||<=K lambda. Source orientation gives a normalized density matrix rho.
The class-output effect E is a projector; for D it includes all labeled
assignments, but its operator norm stays one, independent of that rank.
For n>=1, L^n rho_u with L=-i[G,.] is Hermitian and trace zero, and
||L^n rho_u||_1<=(2K lambda)^n. A trace-zero Hermitian X has equal positive
and negative trace, hence |Tr(EX)|<=||X||_1/2 for every 0<=E<=I.
The integral Taylor remainder after degree p is consequently bounded by
(2K lambda)^(p+1)|t|^(p+1)/(2(p+1)!), uniformly over all classes and real times.
There is no exponential factor, orientation factor or labeled-assignment count
to multiply this bound. Reality also makes these probabilities even in t;
the stated order-(2r+1) remainder remains valid without using that improvement.

Put R_r=(2K lambda)^(2r+1)/(2(2r+1)!), C_r=R_r(1+2^(2r+1)).
Subtract the two Taylor statements at 2t and t. Their leading difference is
(4^r d_xy-beta_xy)t^(2r), and their worst combined remainder is C_r t^(2r+1).
For r=1..6, 4^r>r!, so define L_r=(4^r-r!)r!b^(2r)>0 and
t0=min_(1<=r<=floor(K/2)) L_r/C_r>0.
This gives Q_D^eta(x,y;2t)-Q_B^eta(x,y;t)
 >=eta^K t^(2r)(L_r-C_r t)>0 for every x!=y, 0<t<t0.
lambda>0 follows from b>0; an upper norm certificate only shrinks the window.
t=0 is identity, and t=t0 has only a non-strict certified inequality.
This is a sufficient window, not a maximal or experimentally accessible one.

For class one-swap neighbors B has beta>=b^2, also at K=2. Since
t0<=L_1/C_1=b^2/(3R_1), their probability is at least
t^2(b^2-R_1 t)>0 inside the window. Any oriented K-subset reaches any other
by exchanging missing/excess elements; its complement quotient is connected.
B is therefore irreducible; D has all distinct-class transitions positive.
Finite Metropolis acceptance preserves these positive edges. K=1 has one class
and no nonempty proper hitting target, so is correctly excluded.

## Uniform loss and common finite-temperature chain

All K photons must survive to produce a complete CF target. Uniform attenuation
after U gives precisely eta^K for every routing term; a lost collision cannot
reenter a complete K-photon CF event. Hence Q^eta=(1-eta^K)I+eta^K Q^1,
and the SAME relation holds after the common rejection/acceptance step.
The off-diagonal difference factors eta^K, so it cancels from t0. eta=0 would
destroy strictness/irreducibility and is excluded; unequal/mode-dependent loss
or survival-conditioned normalization is not covered by this factorization.

Symmetry of Q gives pi(x)P(x,y)=min(pi(x),pi(y))Q(x,y) for x!=y,
pi proportional to exp(-alpha C). This proves common detailed balance and
pi>0 for finite alpha, including alpha=0. The acceptance uses only cost
differences, not Z, C*, an optimum mask or a known solution. alpha=infinity
may remove edges; no such limiting chain is part of the proof.
The off-diagonal order implies E_D(f)>=E_B(f) for every real f by summing
pi(x)P(x,y)(f(x)-f(y))^2/2. Thus inf E/Var gives the claimed order of
1-lambda_2, NOT by itself an order of 1-max|lambda_i| or total-variation curves.
Standard common half-lazification (I+P)/2 preserves order and makes eigenvalues
nonnegative (reversible stochastic spectra lie in [-1,1] by Jensen contraction);
arbitrary small holding need not do so. Even nonnegative spectra
do not establish the source's expressly excluded pointwise mixing comparison.

## Killed inverse and precisely which hitting mean is ordered

Let B=A^c, nonempty, and extend functions on B by zero on A. Then
<f,(I-P[B,B])f>_pi=E_P(f_extended). Irreducibility and pi>0 force every
zero-energy extension to be constant globally, hence zero because A is nonempty.
Both killed operators L_X are positive definite, and L_D>=L_B in this space.
Completing the square gives <v,L^-1 v>=sup_f(2<v,f>-<f,Lf>).
Therefore L_D^-1<=L_B^-1 as QUADRATIC FORMS, not as entrywise matrices.
Finite-state irreducibility supplies paths to A of uniformly bounded length
and uniformly positive probability; a geometric block-tail bound makes hitting
means finite even without an aperiodicity argument. First-step recursion gives
h_X=L_X^-1 1_B. Taking v=1_B and dividing by pi(B) proves exactly the
pi(.|B)-initialized mean-hitting inequality. Starting from pi gives the same
inequality without division, since tau_A=0 on A.
Also L_X^eta=eta^K L_X^1, so inverse hitting means scale eta^(-K);
Rayleigh forms/gaps scale eta^K. No graph target must be recognized by the
proposal; choosing A for analysis does not provide a trained solution oracle.

## Adversarial checks of essential restrictions

Orientation counter: take K=2,H=vv^T,v=(1,2,3,4)/sqrt(30), which is real and
dense. Let z=exp(-it)-1, u=v_2^2,w=v_3^2,d=v_1^2 v_4^2, x=[12],y=[13].
With fixed representatives (no source coin), the two quotient probabilities
differ by p(24|12)-p(13|34). The relevant B amplitudes are
z v_1 v_4(1+2zu) and z v_1 v_4(1+2zw), respectively. Their squared-modulus
difference is 2d(u-w)(2(u+w)-1)|z|^4, nonzero for arbitrarily small nonzero t.
This refutes removing the orientation condition, not P99's averaged kernel.

All-start hitting counter to a stronger form-order inference: use a symmetric
three-state chain with edge probabilities p13=1/2,p23=1/4 and p12=c, diagonal
filled by row sums, target {3}, uniform pi. Increasing c from0 to1/4 is strict
off-diagonal/form domination. Yet h1 rises from2 to12/5, while h2 falls from4
to16/5; the pi-outside mean falls from3 to14/5. This abstract counter is not
asserted realizable by the optical family; it demonstrates why inverse FORM
order alone cannot yield the excluded every-start conclusion.

Dense nonzero couplings, global fixed H/t, both admitted times, fresh orientation,
fresh CF source, identical loss/decoder/acceptance and finite alpha are load-bearing.
Structural zeros remove the uniform coefficient lower bound; adaptive H,
annealing, heralded normalization and independently changed decoders need new
proofs. A frozen-chain theorem does not compare best-of-T warm-start policies.
The D control is optimum blind from the supplied H,t, but duration doubles;
compilation, independent draws, source operations and graph-query counts are
not matched by this argument. Tiny b can make the window impractical.
No full scientific-goal, novelty or QPU gate follows. P98's three code files
and theory are unchanged. No imports/AST, code or numerical execution, RNG,
native/test/runner call, raw-data access, push, checkout, delegation, paper or
QPU action occurred. Remaining application gaps are those paid-resource and
actual-policy comparisons, not the finite fixed-chain inequalities audited here.
