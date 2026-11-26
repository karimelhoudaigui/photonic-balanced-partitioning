# P99: weak fixed passive mixing admits a stronger distinguishable control

2026-11-26. **Shared ROOT candidate reconstructed and proved below in the
precise finite-temperature model stated here.** No counterexample was found
within that model. This is a static research derivation, not independent
review of another P99 document, a novelty claim or an executed experiment.
Parent: `9cad69d5a3e26978f1020da5562b782cd0c0d150`. P95 is not a dependency.

## Claim card and raw conventions

Let m=2K, 2<=K<=12, J=floor(K/2). Freeze one real symmetric H and one t for
the whole chain; neither may be current-state/history-dependent. H may
depend on the graph. Each attempt freshly prepares its stated CF source.
Assume |H_ai|>=b>0 for every a!=i, and lambda=||H||op. Put U(t)=exp(-itH).
The optical parameter family must admit both t and 2t. All matrix access,
compilation, source preparation, coins and scoring are paid resources.

The state space Omega consists of UNORIENTED bisections x=[S]={S,S^c}.
Each attempt independently chooses source S or S^c with probability1/2,
as a classical mixture, then injects one photon in each of its K modes.
Exactly K distinct observed outputs Y map to [Y]; every loss or collision
is a self-loop. Optional uniform vacuum-loss transmissivity is 0<eta<=1 AFTER U.
There is no conditioning on survival or CF success. K=1 has one class only.

For fixed K-subsets S,Y before loss, the raw unordered probabilities are

    p_B(Y|S;t)=|per U(t)[Y,S]|^2,
    p_D(Y|S;t)=per |U(t)[Y,S]|^2.

CF source/output factorials equal one; D sums the labeled assignments, with
no extra K! divisor. Its full count law is obtained by independent photon
outputs and aggregation. Both retain all invalid outcomes as paid attempts.
For y!=x the class proposal is exactly

    Q_X^eta(x,y;t)=eta^K/2 * sum_(A in x, B in y) p_X(B|A;t).       (1)

Uniform loss multiplies this whole CF-K event by eta^K, including every
routing order. Thus Q_X^eta=eta^K Q_X^1+(1-eta^K)I on classes. Source
orientation is essential to this quotient definition. Since U^T=U, each
raw p_X(B|A)=p_X(A|B), so Q_B and Q_D are symmetric stochastic kernels.

## Leading routing and the orientation factor

For two distinct classes choose Y in y so ell=|S\Y|=r<=K/2; r>=1.
Set A=Y\S, B=S\Y, and M=H[A,B], an r-by-r matrix. In the permanent,
each missing output requires one off-diagonal amplitude. Exactly r factors
of t are possible only when every common input stays fixed and the r moved
photons use a bijection B->A. Consequently the leading raw coefficients are

    |per M|^2 for B,       d(M)=per |M|^2 for D, at degree 2r.

Any route through a common mode, or nontrivial common-mode cycle, uses
additional powers. It cannot change this coefficient. For r! complex terms,
Cauchy gives |per M|^2<=r! d(M). Density gives d(M)>=r! b^(2r)>0.

If r<K/2, two of the four terms of (1) have distance r; the other two
have distance K-r>r. The two minimal matrices are M and M^T. Their equal
coefficients cancel the orientation factor1/2: d_xy=d(M), not d(M)/2.
If K is even and r=K/2, all four terms are minimal. There are two transpose
pairs, yielding d_xy=d(M_1)+d(M_2)>=2r!b^(2r). The B coefficient has the
same sum structure. In all cases, for the LOSSLESS class kernels,

    Q_B^1(x,y;t)=beta_xy t^(2r)+remainder,
    Q_D^1(x,y;t)=d_xy t^(2r)+remainder,
    0<=beta_xy<=r! d_xy,       d_xy>=r!b^(2r).                    (2)

Negative H entries can cancel beta_xy; they cannot cancel d_xy. For K=2
all distinct class pairs are midpoint pairs and have TWO leading terms.
For K=3, r=1 has only one effective term, including at maximal class distance.
The midpoint enhancement is not necessary for the uniform lower bound.

## A uniform Taylor remainder, without an exponential factor

For B, work on the symmetric K-particle space; for D, on the labeled tensor
space. The many-particle generator G=sum_i H_i has ||G||<=K lambda in both.
The source-orientation average is a density matrix rho. The class-output
indicator E is a projector, including all labeled assignments for D.
Write f(t)=Tr(E exp(-itG)rho exp(itG)). Its derivative of order n>=1 is
Tr(E L^n rho_t), L=-i[G,.]. The Hermitian matrix L^n rho_t has trace zero,
trace norm at most (2K lambda)^n. For any such A and 0<=E<=I,
|Tr(EA)|<=||A||_1/2, by its positive/negative parts of equal trace.

The real-time integral Taylor remainder after degree p therefore obeys

    |f(t)-Taylor_p f(t)| <= (2K lambda)^(p+1)|t|^(p+1)/(2(p+1)!). (3)

No series of absolute values or exp(2K lambda t) is needed: unitary evolution
preserves the derivative norm at every real intermediate time. The indicator
rank and the classical orientation mixture do not change this bound.
All coefficients below 2r vanish by the routing expansion above; at degree
2r they are (2). Higher routing orders are covered by (3), not discarded.

Put R_r=(2K lambda)^(2r+1)/(2(2r+1)!),
C_r=R_r(1+2^(2r+1)), and L_r=(4^r-r!)r!b^(2r). For r=1,...,6,
4^r>r!, so L_r>0. Equations (2)-(3) give

    Q_D^eta(x,y;2t)-Q_B^eta(x,y;t)
      >= eta^K t^(2r) [L_r-C_r t].                             (4)

Thus define the explicit, conservative positive threshold

    t_0=min_(1<=r<=J) L_r/C_r.

For EVERY distinct x,y, 0<t<t_0 and admissible 2t imply STRICT off-diagonal
proposal dominance. At t=0 both chains are identity; at t=t_0 the bound
alone is non-strict. Uniform eta^K cancels from t_0 exactly. Using only a
CPTP contraction remainder without that factor would give a valid weaker
eta-dependent threshold, but is unnecessary for this CF-K self-loop decoder.
A certified upper bound on lambda may replace its exact norm conservatively.

The window also makes B irreducible: one-swap class neighbors have leading
coefficient at least b^2 and remainder at most R_1 t^3. Since
t_0<=3b^2/(9R_1)=b^2/(3R_1), their probabilities are positive. The quotient
of the connected one-swap bisection graph is connected. D has all distinct
class transitions positive. No numerical estimate of the window is asserted.

## Common Metropolis target and spectral consequence

Take any finite complement-invariant graph cost C(x), finite alpha>=0,
and pi(x)=exp(-alpha C(x))/Z>0. Both chains use the SAME acceptance
a(x,y)=min(1,exp[-alpha(C(y)-C(x))]); rejected attempts stay put.
Finite alpha and a nonempty proper target below are explicit restrictions:
no zero-temperature singular limit is imported. No C*, optimum mask or
optimal-state information is needed to build the control U(2t).

For x!=y, P_X(x,y)=Q_X(x,y)a(x,y). Symmetry of Q gives
pi(x)P_X(x,y)=min(pi(x),pi(y))Q_X(x,y), hence detailed balance.
With P_B using t and P_D using 2t, (4) implies for every real f

    E_D(f)=1/2 sum_xy pi(x)P_D(x,y)(f(x)-f(y))^2 >= E_B(f).

Therefore the Rayleigh variational gap
gap(P)=inf_(Var_pi f>0) E_P(f)/Var_pi f satisfies gap(P_D)>=gap(P_B).
This is 1-lambda_2, not 1-max|lambda_i|. It does not order absolute-eigenvalue
mixing bounds without laziness, or total variation from every starting state.
Common lazification retains the form order and makes the spectrum nonnegative;
even then no pointwise finite-time mixing dominance is established here.
Common uniform loss gives P_X^eta=(1-eta^K)I+eta^K P_X^1. Hence these
Rayleigh gaps scale by eta^K, while killed mean hitting times below scale
by eta^(-K). Equal loss does not change their ordering or the weak window.

## Mean hitting time: precisely the stationary-outside initialization

Fix nonempty proper A subset Omega and B=A^c. Let L_X=I-P_X[B,B], acting
in the weighted inner product <f,g>_pi=sum_(x in B) pi(x)f(x)g(x).
Extending f by zero on A identifies <f,L_X f>_pi with E_X(f), so
L_D>=L_B. Irreducibility and pi>0 make both killed operators positive
definite: zero energy would force a constant extension, hence f=0.

For a positive definite L, completing the square proves

    <v,L^(-1)v>_pi=sup_f [2<v,f>_pi-<f,Lf>_pi].

Let tau_A=inf{n>=0:X_n in A}, and h_X(x)=E_x tau_A for chain X.
Thus inverse order holds on quadratic forms. From every state a finite path
to A has positive probability. Finitely many states give a uniform positive
chance to hit within boundedly many steps, hence a geometric block tail.
First-step equations therefore give finite h_X=L_X^(-1)1_B. Consequently

    E_(pi(.|B)) tau_A^D = <1_B,L_D^(-1)1_B>_pi/pi(B)
                       <= <1_B,L_B^(-1)1_B>_pi/pi(B).

The same inequality holds for unconditioned stationary initialization with
tau_A=0 on A, without dividing by pi(B). It does NOT order h_X(x) for every
fixed x, the distribution of tau_A, warm-start best-of-T curves or annealing.
The target set can be any analytically specified quality event; the algorithm
does not need to know or recognize an optimal mask to define its proposal.

## Falsification checks and optimizer interpretation

The potentially missing orientation half is resolved explicitly in (2).
Cauchy is sharp for a constant-sign equal-entry moved block, so the r!
factor is real, not a loose assumption of distinguishability. In contrast,
the coherent cancellation case only strengthens D's leading advantage.
K=2, odd maximal distance, midpoint ties, eta=1, t=0, and collision/loss
retention are covered separately above. No additional routing is assumed
absent: the unitary-sector derivative bound controls its full contribution.

This supplies an optimum-blind REOPTIMIZED D control for every frozen
admissible (H,t) in the explicit weak window. It uses the same K source
photons per raw attempt and the same loss; it does not match physical
evolution duration, circuit compilation, simulation CPU or graph-query costs.
Independent photon draws for D, formation of U(2t), orientation, all setup,
source operations and any evaluated candidate still have to be charged.
The stationary-outside hitting theorem is not a replacement for testing
an optimizer from its actual warm start under a fixed paid budget.

Dense nonzero couplings, global fixed H, unconditioned self-loops, common
cost/acceptance and admitted 2t are load-bearing. Sparse routing, adaptive H,
herald-normalized proposals, independently changed decoders, zero temperature
or time-dependent schedules require other arguments; this note claims no
advantage or hardness there. Small b can make t_0 impractically tiny, and
hardware precision may exclude the entire window. No device claim follows.
All proof leaves above are internal finite combinatorics, unitary calculus
and variational identities; no external theorem or numerical result is used.
This single note changes no earlier source/proof/data. No code/import/AST,
scientific execution, RNG, graph/native/test/runner/QPU/paper/push/checkout
or delegation occurred. Positive optimization target and novelty remain OPEN.
