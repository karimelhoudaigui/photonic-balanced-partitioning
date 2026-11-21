# Density and expected-collision certificate for classical replacement

Research derivation by the coordinator, 2026-11-21. A complete argument is
supplied below; fresh independent proof review and exact novelty checking are
PENDING. This is not a manuscript section or an advantage claim. Computational
checks cannot replace proof review. Prior spatial-Gram results N1/N2 are proved
and independently reviewed in `theory/near_collisionless_bound.md`.

## Setting and statement

Let V be an m-by-k complex matrix with orthonormal columns, k>=1. The bosonic
source has one photon in each of these k distinct input orbitals. Compare the
complete Fock output laws p_b and p_d, where p_d scatters the same photons
independently through the same occupied columns and forgets their labels.
All collision events are retained. Define

\[
q_{ia}=|V_{ia}|^2,\quad a_i=\sum_aq_{ia},\quad
M=\sum_i(a_i^2-\sum_aq_{ia}^2)
=\mathbb E_b\sum_i n_i(n_i-1)/2,
\quad \delta=\sum_i(a_i-\max_aq_{ia}).
\]

M is an expected number of unordered colliding pairs, not collision probability.
Let c be a positive lower bound on every nonzero a_i. Exactly zero rows can be
removed; small positive rows cannot be discarded. Put

\[
\rho(x)=2\sqrt x+x,\qquad
f(s)=\tfrac12\left(\frac{e^{-s}}{1-s}-1\right)\quad(0\le s<1).
\]

The supplied argument establishes

\[
\delta\le M/c,\qquad
\operatorname{TV}(p_b,p_d)\le
\begin{cases}\min(1,f(\rho(\delta))),&\rho(\delta)<1,\\1,&\text{otherwise.}\end{cases}
\]

Replacing delta by M/c gives a weaker bound. For fixed c>0 and M->0 this is
dimension-independent and linear to leading order:

\[
\operatorname{TV}(p_b,p_d)\le M/c+O((M/c)^{3/2}).
\]

The expansion describes the upper envelope; it is not an equivalence for every
circuit. The nontrivial branch requires delta < (sqrt(2)-1)^2, and the numeric
bound may reach one sooner. Failure of the sufficient test establishes no hardness.

There is a sharper observable-only refinement. When M<c^2/2, replace M/c by

\[
d_c(M)=\frac{c-\sqrt{c^2-2M}}2
=\frac{M}{c+\sqrt{c^2-2M}}.
\]

Then TV<=min(1,f(rho(d_c(M)))) on the convergent branch, giving
TV<=M/(2c)+O(M^(3/2)) at fixed c. The balanced example below makes this
leading constant sharp at c=1/2. No refinement is asserted without the
displayed small-M condition.

## Dominant-support argument

Assign each output row i to one maximizer g(i) of q_ia, resolving ties by a fixed
rule. Write S_g for the resulting partition, p_ga=sum_{i in S_g}q_ia and
C_ga=sqrt(p_ga). Columns of C have unit norm. Its diagonal squared is 1-l_a,
where l_a=sum_{i notin S_a}q_ia and sum_a l_a=delta.

Write C=D+E with D diagonal and E zero-diagonal. Then ||D||_op<=1 and
||E||_F^2=delta. For the spatial Gram matrix B_ab=sum_i sqrt(q_ia q_ib),
groupwise Cauchy gives the entrywise bound B_ab<=(C^T C)_ab. Both diagonals
are one. Therefore, with off(X) denoting its zero-diagonal part,

\[
\begin{aligned}
\sigma:=\|B-I\|_F
&\le\|\operatorname{off}(C^TC)\|_F\\
&\le\|DE\|_F+\|E^TD\|_F+\|\operatorname{off}(E^TE)\|_F\\
&\le2\sqrt\delta+\delta.
\end{aligned}
\]

The last term is at most ||E^TE||_F<=||E||_F^2. No dimension factor enters.
N1 gives TV<= (Per(B)-1)/2. The positive-cycle envelope in N2 gives
Per(B)-1<=exp(-sigma)/(1-sigma)-1 for sigma<1. This also follows by summing
the nonnegative formal-series coefficient bound there. Since f increases on
[0,1), the claimed support bound follows. N2's finite polynomial remains an
alternative when the infinite envelope does not converge.

Finally sum_a q_ia^2 <= (max_a q_ia)*a_i, so
a_i^2-sum_aq_ia^2 >= a_i(a_i-max_aq_ia). For nonzero rows divide by a_i>=c
and sum. This proves delta<=M/c. The Taylor expansion
f(2sqrt(delta)+delta)=delta+O(delta^(3/2)) gives the stated leading bound.

For the refinement put d_i=a_i-max_a q_ia. The off-maximum squared sum is at
most d_i^2. Therefore A_i=a_i^2-sum_aq_ia^2>=2d_i(a_i-d_i), so
M>=2c delta-2sum_i d_i^2>=2c delta-2delta^2. The preceding global bound
delta<=M/c and M<c^2/2 ensure delta<c/2, where 2delta(c-delta) is increasing.
Inverting the quadratic yields delta<=d_c(M). The Taylor expansion follows.

## Independent weaker construction

When delta<1, every retained column mass 1-l_a is positive. Restrict v_a to
S_a and normalize it to w_a. The w_a have disjoint supports. A moment argument
in an orthonormal basis extending these w_a bounds the bosonic probability of
leaving occupation (1,...,1,0,...) by 2delta. Indeed diagonal retained masses
are 1-l_a and total off-diagonal column mass is delta. For an occupied row its
expected squared number deviation is at most l_a+3r_off,a; outside rows it is
at most 3a_i. The sum is at most 4delta. Every different fixed-number occupation
has squared distance at least two. Pure-state fidelity and trace distance then
give TV(p_b(V),p_b(W))<=sqrt(2delta).

For distinguishable photons, coupling each categorical draw to its restriction
on S_a gives TV(p_d(V),p_d(W))<=1-prod_a(1-l_a)<=delta. Disjoint supports imply
p_b(W)=p_d(W). Thus TV<=min(1,sqrt(2delta)+delta), a weaker independent check.
The moment argument uses orthonormal occupied columns, so every transformed row
intensity is <=1. It would not apply to arbitrary nonorthogonal frames.

## Sharp leading support constant in a balanced example

Take m=4,k=2. Let w_1=(1,1,0,0)/sqrt2 and w_2=(0,0,1,1)/sqrt2. Mix these two
occupied columns by the real rotation with cosine c_theta and sine s_theta.
Every output mean a_i remains exactly 1/2 and neither photon is deterministic.
For 0<=theta<pi/4,

\[
\delta=2s_\theta^2,\quad
M=\operatorname{TV}(p_b,p_d)=2c_\theta^2s_\theta^2
=\delta(1-\delta/2).
\]

To see the TV identity, first count photons in the two disjoint mode groups.
Their bosonic probabilities are (2c^2s^2,(c^2-s^2)^2,2c^2s^2), versus
(c^2s^2,c^4+s^4,c^2s^2) for distinguishable particles. Splitting each group
uniformly into its two physical modes gives identical conditional laws for
both statistics. Thus the leading coefficient one in the delta envelope cannot
be uniformly reduced. This is an elementary, classically simulable sharpness
example, not an advantage or many-body hardness construction.

## Scope and falsifiers

The known balanced dilute/spectator example has M=2/(k+2), c=2/(k+2), delta=1
and TV=1/2. Its density degrades, so it does not contradict this statement.
Low collision probability alone is still insufficient. The certificate is about
absolute output-law or success-probability error for the same interferometer;
relative rare-event gains, reoptimized controls, input impurities and automatic
hardware certification do not follow. Identical output stochastic channels can
only decrease TV, but no noise campaign has been performed here.

P33 tests global connected perturbations, exact-flat-density fixed-projector
frames, the sharpness family, and the dilute obstruction. Full distributions are
restricted to m<=12; larger-frame certificate calculations are explicitly not
full-distribution checks. No source or graph seed is selected for a favorable
result. A single bound violation beyond tolerance would reject the computational
implementation or the asserted implication. Novelty remains OPEN.
