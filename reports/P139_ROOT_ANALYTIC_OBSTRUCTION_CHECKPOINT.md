# P139 ROOT checkpoint — a local obstruction without a dense-entry floor

26-Nov-2026. ROOT read all119 source lines35d84e49,76 addendum lines58c333d4,
96 non-author review lines79765362 and74 addendum-review linesf7c9b7c5.
Original source hashes are recorded in the reviews; immutable original
commits remain the provenance. ROOT proposed the valuation argument, the
author reconstructed it, and a non-author separately reconstructed the
original BEFORE opening the addendum. This is independent mathematical
review by agents, not external publication review or optimizer replication.
No new computation, graph draw, RNG, native/QPU call or paper edit was used.

## Accepted theorem

Fix finite K>=2 and a finite receiver pool. Let the occupied signal transfer
T_x be real analytic near zero, a physical contraction for small x>=0, and
T_0=E inject the known current K-set R. The CF-source input and common
CF/otherwise-hold-R decoder are fixed. Let c=ceil(sqrt(K!+1)). There exists
a positive window kappa0, depending on this fixed curve and pool, such that
for every receiver-CF target Y!=R and 0<kappa<kappa0,

    p_D(Y;c*kappa)>=p_B(Y;kappa).

The inequality is strict whenever Y's D probability germ is nonzero; if the
germ is identically zero, both laws vanish on its included neighborhood.
The comparator family must physically admit c*kappa. For K2/3/4, c=2/3/5.
No explicit computable or dimension-uniform window is obtained here. P137
remains stronger where its dense-floor assumptions give c=ceil(sqrt(K)) and
an explicit window. P139 covers every FIXED sparse P138 reflection as well.

The proof uses two independently checked facts. First, Cauchy gives
p_B(Y;x)<=K!*p_D(Y;x). Second, the positive sum of squared analytic path
amplitudes has leading term a_Y*x^(2v_Y), with a_Y>0 and integer v_Y>=1.
Unlike the bosonic sum, this leading D term cannot cancel. Its retuned ratio
tends to c^(2v_Y)>K!. Continuity and a minimum over FINITELY many targets,
including zero-germ neighborhoods and the physical domain/c, finish the
proof. ROOT independently checked the stated eta enclosure, sparse exact
hand and C-infinity oscillatory counterexample. Smoothness alone is weaker
than the analytic hypothesis; the prescribed stretch can fail without it.

## Full-count and internal-state extension

Under the ADDITIONAL hypothesis of a FULL analytic occupied isometry with
distinct monomial occupied columns at zero, the same theorem covers every
spatial PNR pattern except the deterministic pattern n0. This includes
collisions and dump ports. The physical internal permutation kernel may
depend arbitrarily on kappa: its normalized modulus bound gives
p_J(n;x)<=K!*p_D(n;x), with the SAME occupation divisor n! in both arms.
Thus one common local window dominates all admitted physical J families.
A classical repair/count kernel is allowed if identical across BOTH arms
AND strengths, with nonnegative induced utility and h(n0)=0.

The FULL analytic assumption is not automatic from signal analyticity.
T_x=(1-x)E would require dump Gram(2x-x^2)I, impossible for an analytic dump
block vanishing at zero. P133/P138 instead supply an explicit rational full
block; P138 separately has the required monomial incumbent endpoint. Actual
loss already present at zero needs a proven common-kernel/h(n0)=0 bridge;
it is not removed by this theorem or by a mean-transmission estimate.

## Research decision

ACCEPT CLAIM-139-ANALYTIC and its separately scoped full-count extension as
PROVEN. Nonnegative raw improvement utilities inherit the pointwise order;
known-incumbent preparation is never credited as progress. All modeled
attempts inject K photons. This excludes a weak-limit interference benefit
over admitted retuned D in this class; it does not say interference is absent.

Finite strength, nonanalytic/adaptively changing curves, parameter-dependent
decoders, growing-dimension uniformity, measured total costs, calibrated
hardware and global optimizer performance remain outside the result.
Analytic local dominance is not an efficient-sampling theorem or a universal
photonic no-go. Exact combined priority is UNVERIFIED; elementary ingredients
are not advertised as new identities. P141 will test finite strength under
a separate prospective contract. CLAIM-042 remains OPEN; paper/main/QPU
stay frozen, with every earlier positive physical contrast and failure kept.
