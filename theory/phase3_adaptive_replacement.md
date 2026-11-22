# Adaptive fresh-input replacement at equal attempts

Coordinator derivation, base03b92ea, 2026-11-22. Self-reviewed; fresh independent
review remains deferred by agent quota. This is a standard sequential coupling
consequence applied to the density criterion, not a new coupling theorem, an
optimization advantage, or a manuscript section.

## Contract

Fix a graph and a classical randomized policy with at most T physical attempts,
including training. Its internal state and random bits may be included in the
history. At each history h, it constructs a passive lossless interferometer
with occupied orthonormal frame V_t(h), prepares fresh distinct singly occupied
input photons, measures the complete occupation, and updates classically.
The reference runs the identical policy, replacing each bosonic measurement by
independent scattering through the same occupied columns. No quantum memory,
coherent feedback, entangled cross-attempt inputs, free exact-distribution
oracle, or outcome-dependent shot accounting is allowed in this contract.
Classical stopping and decoding are allowed. Pad stopped histories by an
absorbing symbol up to T; both kernels agree at an absorbed history.

Let b_t(.|h),d_t(.|h) be the conditional outcome laws at the SAME history.
Assume TV(b_t(.|h),d_t(.|h))<=epsilon_t(h), for every eligible history, with
0<=epsilon_t(h)<=1. A sampled collection of visited circuits does not prove
this uniform hypothesis. If deterministic bounds e_t dominate these epsilons,
the complete transcript laws satisfy

    TV(B_1:T,D_1:T) <= 1-product_(t=1)^T(1-e_t) <= sum_t e_t.

The bounds include the policy's classical actions, state and final output,
because shared postprocessing cannot increase TV. Every success event A,
including discovery before budget exhaustion, therefore satisfies

    |Pr_B(A)-Pr_D(A)| <= 1-product_t(1-e_t).

No relative ratio, accepted-shot comparison or unbounded waiting-time bound
follows. A useful approximate replacement requires the TOTAL error budget to
be small, not merely a small one-attempt number.

## Proof, including adaptive histories

Couple policy randomness identically while histories agree. At a common history
h, maximally couple b_t and d_t: match their shared probability mass, of total
1-TV(b_t,d_t), and route the disjoint remainder separately. This construction
is a proof device; the reference simulator need not compute this coupling.
After the first mismatch, use arbitrary couplings preserving both marginals.
Before mismatch, histories, chosen frames, stop decisions and actions coincide.
Conditional on no earlier mismatch, failure to match at t has probability at
most e_t. Induction gives probability of no mismatch at least product_t(1-e_t).
For any coupling and event A, |Pr(X in A)-Pr(Y in A)|<=Pr(X!=Y), since equal
samples have identical membership. Taking the event supremum proves the first
inequality. The second follows by the union bound or induction. Identical
postprocessing is immediate from the same event argument. Absorbing padding
ensures stopped histories introduce no new mismatch. This proof does not assume
the frames are fixed in advance or independent of earlier outcomes.

A history-sensitive variant follows from the same construction:

    TV(B_1:T,D_1:T) <= min(1,sum_t E_B[epsilon_t(H_(t-1))]).

Indeed the probability of first mismatch at t is bounded by the expectation of
epsilon_t on the coupling's equal-prefix subprobability measure. That measure
is dominated by the B-prefix marginal. This is a mathematical upper bound;
estimating its expectations reliably is a separate task. Do not substitute
arbitrary empirical averages from a few trajectories.

## Photonic dictionary and classical cost

For each exact frame, use the density theorem's sufficient bound

    epsilon_t(h) = min(1, f(2sqrt(delta_t(h))+delta_t(h))),

on its domain, otherwise1, where delta is dominant-row leakage. The observable
coarse surrogate delta<=M/c is also valid when c lower-bounds EVERY positive
row intensity. In the refined branch M<c²/2, use
delta<=[c-sqrt(c²-2M)]/2. These are exact mathematical bounds; the current
complex128 implementation is explicitly not a rigorous numerical enclosure.
Experimental estimates of M or c require a separate confidence/error budget.

With fixed c and uniformly small M, epsilon<=M/(2c)+O((M/c)^(3/2)), with the
constant understood in this fixed-c regime. A dimension-free coarse sufficient
condition for a sequence of T-attempt protocols is

    T * sup_(t,h) M_t(h)/c_t(h) -> 0.

It ensures the coarse density envelope tends to zero after composition even
if c varies. Do not use the sharper leading coefficient uniformly while c also
vanishes without controlling the refined-branch conditions and remainders.

Given V, the distinguishable sampler draws one categorical output per occupied
column and sums occupations. A naive exact-real-arithmetic draw takes O(mk)
per attempt; finite numerical samplers need their own approximation budget.
Alias preparation is O(mk), followed by O(k) draws if that V is reused. Changes
of V require their preprocessing to be charged. Building the circuit/frame,
policy optimization, graph scoring, certificate calculation and output storage
are additional classical costs, not free oracle operations. M,c,delta require
O(mk) arithmetic from a given frame; the optional Gram diagnostic is O(mk²).
This establishes a same-policy classical replacement under the stated small
total-error hypothesis. It does not make arbitrary circuit optimization easy,
nor cover optimizers granted exact all-outcome expectation queries for free.

## Falsifiers and exclusions

A cheap exact discriminator enumerates three-step adaptive histories of the
balanced four-mode rational-rotation family, retaining all ten Fock outcomes.
The next strength depends on whether the preceding outcome collided. Check
full transcript TV against both bounds, without Monte Carlo intervals.
A separate two-step control starts with a disjoint-support frame (epsilon=0)
then switches to a mixing frame: its positive transcript TV rejects any attempt
to use only the initial circuit's certificate for the whole adaptive policy.
This finite enumeration checks interpretation, not the general proof.

The coupling inequality and maximal-coupling construction are standard; a
primary reference is Levin–Peres, *Markov Chains and Mixing Times*, second
edition, author-hosted PDF https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf.
Exact proposition extraction is pending; the argument above is self-contained
and does not treat an unextracted citation as a proof dependency.
