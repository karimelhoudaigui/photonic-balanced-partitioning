# Direct cost phases and collective balanced mixing: pre-code checkpoint

2026-11-25, physics route after the reported negative P49. No P49 raw data
were used in these derivations, and no simulation, import, graph generation,
hardware call or manuscript change was performed. This route changes the
interaction: a genuine two-qubit cost phase followed by coherent transitions
between balanced partitions. It is not another passive spectral-source angle.

**Result:** a coherent ideal mechanism has a calculable favorable sign, but
its first-order proposal has an inexpensive exact classical counterpart.
A Grover-mixer variant also has a required polynomial classical sampling
control. Neither result proves equal-cost classical domination. Finite
collective mixing remains open, together with its photonic resource gate;
there is currently no justified new numerical pilot or hardware claim.

## 1. A specific ideal mechanism and its sign

Let n=2k, X={S subset [n]: |S|=k}, M=binom(n,k), and C(S) be the actual
weighted cut. No optimum, prepared partition or incumbent enters the state.
Start with |u>=M^(-1/2) sum_S |S>. Let A be the adjacency of the Johnson
graph: T~S exchanges one included vertex and one excluded vertex. Its degree
is d=k^2. Write B=A/d, so ||B||op=1, and apply

    |psi(beta,gamma)> = exp(+i beta B) exp(-i gamma C) |u>.

The opposite sign of the mixer reverses the following response. A direct
derivative at beta=0, with gamma arbitrary, gives

    p_S(0)=1/M,
    p'_S(0)= 2/(M d) sum_(T~S) sin(gamma [C(T)-C(S)]).                 (1)

Indeed the derivative amplitude is i sum_T A_ST exp(-i gamma C(T))/(d sqrt M).
Taking its interference with exp(-i gamma C(S))/sqrt M gives (1), including
its sign. Thus a partition with more expensive neighbors can be enhanced
without knowing an optimum. This is a proposal mechanism, not a guarantee
of useful deep-valley discovery or better best-of-budget performance.

If gamma>0 and all swap differences obey |gamma Delta|<=pi, the derivative
of the true mean cut is nonpositive:

    d E[C]/d beta at0
      = -1/(M d) sum_(S,T ordered neighbors) Delta_ST sin(gamma Delta_ST).

The normalization is by ordered neighbors. The inequality is strict if one
edge has Delta sin(gamma Delta)>0. Larger phases can reverse contributions;
one may not extrapolate the favorable small-phase sign to arbitrary angles.

## 2. An exact classical control for this first-order law

For |beta|<=1/2, define p_lin(S)=1/M+beta p'_S(0). It is a normalized
nonnegative probability law. Here is an EXACT sampler for it:

1. Draw S uniformly from X and one uniformly random swap neighbor T.
2. Compute Delta=C(T)-C(S), using the actual graph.
3. Accept S with probability
   (1+2 beta sin(gamma Delta))/(1+2|beta|); otherwise repeat.

Reversal (S,T)<->(T,S) cancels the total sine. The mean acceptance is exactly
1/(1+2|beta|), hence at most2 attempts on average, with one swap delta each.
This does not evaluate all k^2 swaps. Each uniform proposal and delta is
paid; a delta can be computed from the two incident neighborhoods. Every
partition actually scored can also be retained by this classical arm.

There is a dimension-independent approximation guarantee for this specified
normalization:

    TV(p_quantum(beta,gamma), p_lin) <= beta^2.                       (2)

To prove it, set rho0=exp(-i gamma C)|u><u|exp(+i gamma C). For
rho(beta)=exp(i beta B)rho0 exp(-i beta B), the second derivative has trace
norm at most4, since ||[B,[B,rho]]||1<=4||B||op^2||rho||1=4.
Taylor's integral remainder has trace norm <=2 beta^2. Measurement contracts
trace distance, giving (2); the affine measured state is exactly p_lin.
The affine density operator itself need not be positive; only the explicitly
constructed measured law is required to be positive here.

Consequently the favorable sign alone is already explained classically. At
q fixed trials, the product-TV bound is at most q beta^2 (clipped to1).
This is an approximation/control, not exact replacement of a finite-beta
circuit, nor a claim that the control beats FAST under equal CPU. For an
unscaled mixer A/c, the relevant perturbative parameter is beta*d/c; (2)
must use its square. A more extensive Hamiltonian cannot be declared weak
by changing notation or discarded on this unit-normalized bound.

## 3. A second control: rank-one Grover mixing

Replacing B by |u><u| gives another precisely specified classical control.
For p rounds with real cost phases and arbitrary known angles, write the
amplitude as f_j(C(S))/sqrt M, f0=1. Exactly,

    f_j(c)=exp(-i gamma_j c) f_(j-1)(c)+(exp(-i beta_j)-1) alpha_j,
    alpha_j=E_(S uniform)[exp(-i gamma_j C(S)) f_(j-1)(C(S))].

Normalization implies |alpha_j|<=1, hence |f_p(c)|<=2p+1. If the alpha_j
are available, uniform rejection with acceptance |f_p(C(S))|^2/(2p+1)^2
samples the full output law, with mean (2p+1)^2 proposals. That is a necessary
counter-control, NOT a proof of domination of p quantum oracle calls.

The coefficients need not be assumed exactly available: sequential fresh
Monte Carlo can approximate each mean to tau=epsilon/(2p). In the true
uniform L2 space the exact update is unitary, so errors accumulate by at
most2tau per round, rather than multiplying exponentially. On the successful
estimation event, ||f_tilde-f||2<=epsilon, the approximate norm stays within
epsilon of1 and its supremum is O(p). Bounded-mean concentration therefore
uses polynomially many cost/phase evaluations in p,1/epsilon,log(1/failure).
Rejection from the resulting squared amplitude has an explicit polynomial
envelope and O(epsilon) TV error after normalization. This assumes costs and
phases can themselves be evaluated to the needed accuracy in polynomial
time. It says nothing about exact probabilities, exponentially small tail
relative error, or a superior constant/total-resource performance.

The (2p+1)^2/M point-probability envelope is already stated in Xie et al.,
arXiv:2405.03173v2 (24-May-2024), Sec2 Eqs3–7 and Theorem1 Eq10:
[primary text](https://arxiv.org/html/2405.03173v2#S3.SS1).
Their full proof and performance regressions were not independently audited
here. We use only the independently derived non-strict bound above, including
p=0. No novelty claim is attached to this known mixer or to this checkpoint.

## 4. The photonic obligation cannot be hidden

The ideal state |u> is a balanced Dicke superposition; an ordinary CF input
through a passive interferometer does not provide it for free. In dual rail,
one photon per vertex encodes a qubit and the weight-k subspace represents X.
This already uses n=2k data photons, rather than P49's k, before any ancillas.
Preparation, ancillas, all failed preparations and measurement must be paid.
The cost is C=sum_(i<j) w_ij(1-Z_i Z_j)/2, so its nontrivial phase requires
logical two-qubit ZZ gates. The ideal Johnson adjacency is the restriction
of sum_(i<j)(sigma_i^+ sigma_j^-+sigma_i^- sigma_j^+). Its implementation is
a logical XY evolution, not free hopping of indistinguishable photons.

With vertex occupation modes, passive hopping leaves the hard-core subspace
and creates collisions. A final collision filter is not exact Johnson
evolution at finite time. Repeated hard-core projections would require a
specified nondestructive operation and all its cost; none is assumed.

LOQC with single photons, passive optics, detectors and detector feedback is
conceptually established by Knill–Laflamme–Milburn,
[quant-ph/0006088v1](https://arxiv.org/abs/quant-ph/0006088v1) (20-Jun-2000).
That source's existence result is not a gate specification or a capability
claim for an available Quandela processor. No device calibration is inferred.
In a naive abort-on-failure circuit with state-independent conditional success
p_g at each of G gates, success is p_g^G; photons/attempt divided by this
success must be charged. A sequence of commuting edge phases already needs
O(|E|) specified interactions; compiling the noncommuting mixer and preparing
the input adds costs. Feedforward/resource-state schemes can change this
scaling, but their actual ancilla, delay, loss and detection resources must
replace the naive model explicitly, not be assumed free.

## 5. Decision and precise remaining question

Keep this as a DISTINCT deferred interaction route, not a new accepted
pilot. Its first-order improvement has the exact sine-swap control, while
the rank-one variant has the rejection control. Before any code, the useful
remaining question is whether a finite-depth, finite-strength local
cost-phase/XY architecture provides a useful full output law beyond those
controls, annealing/FAST and tensor-network or bounded-width simulation,
after actual source/oracle/mixer/heralding costs. Small independent gates or
components alone are not enough; growing interaction width must contribute.

A future claim would need the same total-budget classical controls, no free
success conditioning, and an effect not explained by the perturbative TV
remainder. Phase/sphere/D controls are still appropriate if an optical
compilation exists, but merely breaking their P49 passive-source law is not
the success criterion. The missing implication is a finite-resource gain,
not a missing favorable sign. No such implication is proved or asserted.
