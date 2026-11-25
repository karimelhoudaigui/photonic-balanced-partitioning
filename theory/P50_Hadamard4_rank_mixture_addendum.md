# H4 top2 has a two-component exact classical sampler

2026-11-25. ROOT proposed the mixture below after reading the independent
checkpoint b710d215d1a6c3ebfa3bd6c3736e96e88565a947. This addendum checks it
independently and preserves that attribution. No code, numerical experiment,
P50 raw data, graph generation or hardware call was used. The earlier full
Fock/moment derivation remains unchanged.

## Verified identity and sampler

Use the earlier four-mode source H(exp(i phi)), four CF photons, top2 of
n-1 with UNIFORM ties, equivalently fresh iid continuous jitter0<beta<1/2.
No fixed-priority beta0 rule or finite tie bucket is silently substituted.
Let O={{0,2},{1,3}}, X the four cross pairs, and u=sin^2(phi). The previously
derived individual-pair probabilities are

    p(O pair)=1/6-u/24,
    p(X pair)=1/6+u/48.

Let U6 be uniform on ALL six pairs and UX uniform on X. Then EXACTLY

    p_top2 = (1-u/4) U6 + (u/4) UX.                                (1)

On an O pair the right side is(1-u/4)/6. On an X pair it is
(1-u/4)/6+u/16. These agree with both probabilities above and sum to1.
There is no remaining interference-dependent normalization or hidden oracle.

The sampler is: draw Bernoulli(lambda), lambda=u/4; if false draw a uniform
pair from four vertices, and if true draw one independent uniform vertex
from each of the TWO architecture-known opposite pairs. This produces the
FULL decoded-pair law and needs no permanent, Fock table, covariance or graph
optimization. It also reproduces the law on unoriented balanced partitions,
where each pair is identified with its complement.

The cost is O(1) random primitives/arithmetic once the pairing and lambda
are supplied. For the two endpoints phi0 and pi/2, lambda0 or1/4 is exact
using fair bits, with constant expected work for the uniform-six draw.
For arbitrary real phi, an O(1) probability-primitive statement is not a
bit-complexity theorem for computing transcendental coin probabilities;
any numerical implementation must state its parameter precision/error.

## A graph-weight check and stronger mean-only control

On an arbitrary weighted four-vertex graph write W_O for the sum of weights
on O and W_X for that on X, W=W_O+W_X. A uniform balanced pair separates
each edge with probability2/3, so

    E_U6[C]=2W/3.

Under UX each O edge is ALWAYS separated, while each X edge is separated
with probability1/2. Therefore

    E_UX[C]=W_O+W_X/2,
    E_top2[C]=2W/3+u(2W_O-W_X)/24.                                (2)

This checks the previous K2,2 and matching signs. The only knob in this
decoded law is a partial classical bias towards cross-pair diversification.
An optimum-blind rule comparing2W_O with W_X can choose U6 or UX, whichever
has the smaller expected cut. Its mean is <= the mean in(2) for EVERY phi.
This comparison needs only the six graph weights, not an optimum or fitting.
It is a MEAN statement, not stochastic dominance of both components or a
best-of-budget tail claim. More fundamentally, sampler(1) already reproduces
every decoded-pair event exactly at the supplied phi.

## Scope: no promotion to a global mechanism

This shortcut reproduces the DECODED law, not the raw full Fock law, its
moments, an internal quantum state or later use of unobserved counts. An
adaptive procedure that uses only these decoded subsets/cuts can replace
this conditional kernel with(1) at each known parameter/pairing. A procedure
using additional count information requires a stronger replacement.

b4 is already exactly B for this four-photon source. The earlier35-pattern
table is an independent constant-size full-count sampler. A direct sum of
independent four-mode blocks consequently has a classical full-count sampler
linear in the number of blocks; the mixture shortcut alone must not be
mistaken for a proof about a GLOBAL topK of all block counts. Neither result
extends automatically to a genuinely coupled tensor/global interferometer.

A larger Hadamard family must establish an effect beyond b4, continuous
phase, and cheap orbit/tensor/DP or mixture controls before it earns a pilot.
Fixed Q/P/covariance and a nonzero high-order moment alone are insufficient.
The missing implication is a globally useful decoded law with a justified
resource comparison, not another proof that H4 has an interference signal.
No scalable gain, novelty, P50 panel change or hardware conclusion follows.
