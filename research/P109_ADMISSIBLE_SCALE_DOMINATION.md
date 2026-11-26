# P109: an admissible transmission-scale obstruction

26-Nov-2026, ROOT; continuation of P106, base1ad816b.
**Candidate theorem; independent review pending.** The permanent Cauchy
bound is elementary/established; priority of this application is unassessed.
This is not a theorem that unavoidable hardware loss can be removed.

## Contract and exact statement

Fresh known CF K-photon input, K>=1, passive vacuum channel, same signal
modes and full-attempt denominator. A control family supplies BOTH nominal
contractions T_B and T_D=c T_B, with c>0 and c^(2K)>=K!; their realizability
within the admissible hardware/control family is an explicit assumption.
For example, c=(K!)^(1/(2K)) is mathematically allowed if
||T_B||op<=1/c and the family really admits that amplitude rescaling.
Merely reporting a low measured transmission does not grant this control.

An optional COMMON fixed scalar external attenuation multiplies both
transfers; it is not rescaled, inverted or made free. Include all attempted
source preparations, their failures and K photons per modeled injection.
The mathematical source remains ideal known CF on the common preparation
success branch; unverified source correlations are outside the model.

Let V be any declared set of full-K output occupations (e.g. all CF states).
On n in V apply a COMMON randomized classical balanced decoder. All other
outcomes, including lower-total loss, map to the same fixed incumbent/failure
state. Then the distinguishable D control's raw probability of every n in V
is at least the indistinguishable B probability. The same holds for every
decoded event excluding that common incumbent/failure atom.

For any fixed feasible incumbent with cost C0, score a decoded candidate if
present and retain min(C0,C_candidate). D has no larger expected retained
cost and stochastically dominates B's one-attempt improvement distribution.
For T_attempt independent repetitions from that SAME source/incumbent/fixed
circuit, the identical order holds for best-of-T_attempt quality. No C* is
required by the sampler or controller; analytical thresholds are not training
oracles. This is not a changing-state/adaptive/annealing trajectory theorem.

## Proof, retaining factorials and failures

For full-K occupation n, let n!=product_j n_j!, and let M be the K-by-K
matrix with repeated output rows of T_B. CF input factorials are one.
Writing z_sigma=product_i M_i,sigma(i), Cauchy gives

    |per M|^2=|sum_sigma z_sigma|^2
       <=K! sum_sigma |z_sigma|^2=K! per |M|^2.

Therefore p_B(n;T_B)<=K! p_D(n;T_B). This includes collisions and every
zero; its K! coefficient is not a success-normalized ratio or a graph claim.
Scaling amplitudes by c scales every full-K D probability by c^(2K), hence

    p_D(n;cT_B)=c^(2K)p_D(n;T_B)>=p_B(n;T_B).             (1)

The total D success mass cannot exceed1 because its supplied transfer is
a contraction. No lower-sector probability is asserted ordered individually;
only their common aggregated failure/hold is used. Multiplying both physical
transfers by a fixed sqrt(eta) contributes the same eta^K and preserves(1).

For any common decoder event E, sum(1) over n in V with the nonnegative
conditional decoder weight Pr(E|n). For improvement threshold d>0, choose
E={C_candidate<=C0-d}; then raw D event probability is at least B. At
d<=0 the retained-cost CDF is completed by its incumbent atom. Integrating
these tail inequalities gives the expected retained-cost order. With fresh
independent trials, probability of never reaching any such E is(1-p(E))^T,
which is smaller for D, proving the fixed best-of-T order.

No probability ratio, permanent, optimum or known-solution preparation is
needed to implement the rescaled control once its admissible transfer is
provided. Computing that transfer, its mesh and decoder costs remains paid.

## P106 concrete exact veto, including its positive same-T effect

P106 has K2, gamma_B=1/3 and F with receiving rows
(1,q),(q,1),(p,p),(p,p), p=exp(-1),q=exp(-3).
Thus ||F||op²=(1+q)²+4p². The choice gamma_D=2/3 is a contraction:
exp(1)>2 and exp(3)>16 imply

    ||gamma_D F||² <(4/9)[(17/16)²+1]=545/576<1.

It is in the SAME transfer family with the SAME lambda1, known graph/source
and decoder, changing only gamma. Every full-K D probability increases by16;
the K2 Cauchy factor is2. Hence D_new(n)>=8 B_old(n) for each CF receiving
pair. All six possible pair gains are NEGATIVE: -4, four copies of-6, and-8.
Invalid outputs hold. Its expected improvement magnitude is consequently
at least8 times B's, regardless of the positive same-T B-minus-D gain.
This explicit change uses no global optimum or optimal-state mask.

The same-scale raw B mean improvement is a real interference effect; P106's
absolute rank reversal does not refute that effect. Rather, the legal D
rescaling and complete paid six-pair frontier defeat an advantage assertion
for that proposed operating point. Independent reconstruction is pending.
The B arm could also retune its scale; this example does not reject that
entire family or prove domination at its saturated optimum.

## Limits, falsification and next decision

This sufficient obstruction fails if the scaled transfer is inadmissible,
the source is changed, conditional normalization is substituted, different
hardware attenuation applies, or retained lower-total records inform useful
decoding. Failure of its hypotheses proves no advantage. In particular P101
nominal filters have spectral norm1 and do NOT admit c>1 by this argument.
Known scalar loss alone cannot be inverted to create that missing margin.

Only the fixed attempt/photon/source/mode comparison is ordered. Real source
timing, different meshes, calibration, preprocessing/decoding, wall time and
finite precision require separate accounting. This is not a matched total-
cost result or an independent optimizer benchmark. Threshold hardware can
use V=K distinct clicks with all other records held; full-K collisional
decoding generally needs number discrimination and verified denominators.

Disposition: keep a falsifiable control obligation for attenuated proposals;
do not claim a no-go for saturated, all-output, nonlinear or adaptive methods.
No numerical run, native/QPU call, manuscript edit or novelty claim. CLAIM-042 OPEN.
