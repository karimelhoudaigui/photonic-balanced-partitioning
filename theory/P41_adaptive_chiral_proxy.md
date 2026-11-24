# P41/R1 — a positive classical proxy for the leading chiral search current

Base: f09c7ec82b2fe23395116e21bd56614f3739107c. Author: p41_adaptive.
Status: derived argument awaiting independent proof audit. Novelty unclaimed.
This is a local obstruction to a short-time mechanism, not to all passive
interferometers or graph optimization. No empirical optimization gain is claimed.

## Proposed mechanism and exact domain

Let H=H* be an m-by-m single-particle Hamiltonian, h=||H||_op, and let
S be a k-subset of occupied inputs, 1<=k<m. Rows are outputs, columns inputs.
Inject one photon per input in S and apply U(t)=exp(-itH), with ideal lossless
number-resolving measurement. On a collision, retain the current partition S;
otherwise use the measured k-subset. Call this repaired proposal kernel B_t.
Every optical shot, including a collision/hold, is charged. No conditioning
or multiplication of an accepted probability is performed.

One graph-dependent option uses the single-flip cost features
f_i=(1-2x_i)(sum_j A_ij-2(Ax)_i) and
H_ij=A_ij exp(i phi sign(f_i-f_j)), H_ii=0, followed by norm scaling.
These features are obtained from the graph and current feasible partition;
they do not require C*, an optimum mask or an optimal partition. Relabeling
vertices covariantly relabels H, even at tied features. The phases generally
have nonzero triangle flux, unlike the pure gauge exp(i phi(f_i-f_j)).

The attractive hypothesis is that chiral exchange currents direct proposals
toward better swaps without sacrificing feasibility at leading nontrivial
order. The construction below gives the serious classical countercontrol:
it reproduces those currents without a bosonic permanent or optical rejection.

## Cubic exchange identity

For a in S, b outside S, put T=S\{a} union {b}. Direct expansion of the
permanent amplitude gives

    A_B(S->T) = -it H_ba - t^2 Q_ba + O(t^3),
    Q_ba = (H^2)_ba/2 + H_ba sum_(i in S\{a}) H_ii
                             + sum_(i in S\{a}) H_bi H_ia.

The last sum comes from routing photon a to occupied output i while photon i
goes to b. The preceding diagonal sum is real times H_ba. For labelled
distinguishable particles, all other routings have probability O(t^4), so

    P_B(T)-P_D(T)
      = 2t^3 Im[conjugate(H_ba) sum_(i in S\{a}) H_bi H_ia] + O(t^4). (1)

This is a physical feasible-output identity, not a conditional CF statement.
For each unordered occupied pair {a,i} and vacant b, its contribution to
the a->b current is the negative of its i->b contribution. Summing (1) over
all single swaps therefore cancels at cubic order. A real H has zero cubic
current. Complex conjugation of H or t->-t reverses its sign.

An elementary hand control uses k=2, m=4, S={0,1}, H_01=H_12=1,
H_20=i, Hermitian conjugates, and all other entries zero. The two exchange
coefficients toward b=2 are respectively -2 and +2. This control is not a
large-scale mechanism; the planned probe also couples all k=4 and k=5 photons.

## Positive proxy and finite bound

Write the cross block A0=H_(Sbar,S) and

    B0=(H^2)_(Sbar,S)/2 + H_(Sbar,S) H_(S,S).
    q_ab=t^2 |(A0)_ba-it(B0)_ba|^2.

Sample swap a->b with probability q_ab, and otherwise hold at S. Each q_ab
is nonnegative, and the second term added by including i=a in B0 is a real
multiple of H_ba. Hence q_ab agrees with the bosonic single-swap probability
through order t^3. It contains an explicitly nonnegative fourth-order term.

The norm estimates

    ||A0||_F <= sqrt(k) h,
    ||B0||_F <= (3/2) sqrt(k) h^2

follow by taking the k columns of H^2 and by submultiplicativity for
H_(Sbar,S)H_(S,S). Consequently

    sum_ab q_ab <= k (|t|h)^2 (1+(3/2)|t|h)^2 <= 49/64 < 1

whenever |t|h<=1/(2sqrt(k)). This is a valid feasible classical sampler Q_t
throughout that range, with no sign truncation or postselected normalization.

Let K=dGamma(H) on the k-particle bosonic sector. Since K is a restriction
of a sum of k copies of H, ||K||<=kh. Expand the density matrix evolution
through degree3 in the commutator superoperator. Its trace-norm remainder is
at most exp(2k|t|h)(2k|t|h)^4/24. Measurement and collision-to-S repair
contract trace norm, including on a Hermitian signed Taylor remainder.

A collision-free output differing by at least two swaps has amplitude
O(t^2) and no probability Taylor coefficient below degree4. The repaired
third-degree probability vector therefore has support only S and its single
swaps. Its single-swap entries are exactly the quadratic+cubic terms above,
and its S entry is one minus their sum. Q_t differs from this signed Taylor
vector only by t^4 |(B0)_ba|^2 on each swap and the opposite total at S.
Using the triangle inequality gives the explicit uniform bound

    TV(B_t,Q_t) <= epsilon(k,h,t),
    epsilon = exp(2k|t|h)(2k|t|h)^4/48
                                      + (9/4)k(|t|h)^4.                 (2)

The effective probability bound is min(1,epsilon). Bound (2) can be loose,
and is nonvacuous only in its actual parameter regime; report constants in
numerical checks. This proof does not use an independently optimized D model:
it constructs a stronger classical feasible surrogate of the bosonic kernel.

## Adaptive search and resource interpretation

For any fixed collision-repair and accept/reject rule based on graph costs,
applying the same stochastic rule to B_t and Q_t cannot increase TV. The
graph, current partition, H and t may depend on a classical history, provided
the comparison uses the same rule conditionally at every matching history.
If step j has a uniform epsilon_j bound, sequential coupling gives transcript
TV <= 1-product_j(1-min(1,epsilon_j)). This is the established coupling
principle already scoped in P34, not a new coupling theorem. Bounded terminal
costs then differ by at most their range times this TV bound.

Computing the needed cross block H^2 costs O(m^2 k) dense arithmetic;
the additional occupied block product costs O(mk^2), with O(mk) proposal
weights. Sampling thereafter needs no Fock enumeration and no permanent.
This computation, graph processing and scoring must still be charged. The
statement is an arithmetic upper bound, not a proved wall-time or hardware
dominance theorem for every architecture. It does not apply at finite angles
outside the validity/accuracy regime or to coherent quantum memory.

Thus a leading cubic chiral signal alone cannot establish irreducible
photonic optimization benefit: Q_t reproduces it at fourth-order absolute
error with feasible proposals. A remaining candidate must demonstrate an
advantage beyond this countercontrol, for example through finite-angle or
genuinely many-swap effects that this approximation does not capture.

## Source scope

Chiral transport itself is established. Zimboras et al., *Quantum Transport
Enhancement by Time-Reversal Symmetry Breaking*, arXiv:1208.4049v2
(1 Aug2013), Sec.RESULTS Eqs.(1)-(2), develops complex Hermitian graph hopping
and directional triangle transport. [Primary PDF](https://arxiv.org/pdf/1208.4049v2).
It is an adjacent single-excitation result; it does not establish the repaired
many-boson kernel (2). Taylor/trace-norm ingredients here are elementary.
No exhaustive attribution search or claim of original classical simulation
complexity is made. The route must undergo independent audit before acceptance.
