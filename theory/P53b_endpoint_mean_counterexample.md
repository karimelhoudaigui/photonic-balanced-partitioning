# P53b: an exact counterexample to ENDPOINT71 mean replacement

25 November 2026. **Exact finite certificate, independently checked in separate
code within the same team. Not an optimization advantage or novelty claim.**

Use precisely the P52/P53 eight-mode unitary, eight distinct single-photon
inputs, ideal lossless count measurement and uniform-tie top4 decoder.
Write c_ij(theta) for the probability that its decoded balanced subset crosses
edge {i,j}. ENDPOINT71 consists of all35 complementary 4+4 distinguishability
groupings at each of theta=0 and pi/2, plus uniform70. Group photons interfere
within each four-photon species; the two species' count laws are convolved.

At the prospectively fixed point theta=pi/3, x=cos²(theta)=1/4, this bosonic
edge-mean vector lies OUTSIDE the convex hull of ENDPOINT71.

## Exact witness

In lexicographic edge coordinates, choose

    w_04=1/2, w_15=-1/2, all other w_ij=0.

All71 classical vectors v_c satisfy w.v_c=0, whereas the exact bosonic vector
b at x=1/4 satisfies

    w.b = -767/327680.

Thus EVERY convex combination of these71 controls has a larger value of this
linear functional by exactly767/327680. In fact the target is outside their
affine span, since the same equality holds for all71 generators.

A nonnegative weighted graph follows by adding1/2 to every edge: weights
are1/2 except a_04=1 and a_15=0. Every balanced4-of8 crossing kernel has
sum_(i<j) c_ij=16. Its expected cut therefore adds the common constant8:
all71 controls have mean8 and the bosonic mean is8-767/327680. Total graph
weight is14; the normalized mean gap is767/4587520. This graph is an explicitly
POSTHOC constructive witness, obtained from a separating functional, not a
held-out instance or a useful benchmark. Its structure is elementary, and
all70 feasible subsets at this size are readily enumerated classically.

## Evidence and independent checking

P53b sourcebb0ba2d followed ROOT/physics full static review and20 synthetic
tests PASS atfa3eb9a. ONE main on that clean qualification revision completed
2.072363s,13 unchanged inputs, exactly one primal and one dual proposal.
Both solvers returned status0/successTrue. The primal support did not certify
membership; the dual's signed vector was converted with the predeclared
binary Fraction rule, and every rational inequality was checked exactly.

Certificate SHA256:
`bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe`.
Source data2a593abb... and librarycb210de1... are the immutable exact P53
artifacts; no physical target/kernel was obtained by rounding a float.
Read research/P53b_fixed_point_main_receipt.md for the original command,
versions, limits, all outputs and scientific exclusions.

The separate98-line stdlib checker018641eb imports no production module.
It reconstructs b by a direct sum of powers rather than production Horner,
checks every one of71 kernels/all28 coordinates, signed-binary witness/L1,
all strict margins, nonnegative graph shift/normalization and solver gates.
Its unique bounded run reports PASS and the same exact gap. This was a
posthoc computational audit with the outcome known, not blind sampling or
an independent new reconstruction of the optical source. The physical
source polynomial/normalization have the separate P53 derivation reviews.

## Scope and next falsifier

This refutes extending P52's four observed mean matches to ALL continuous
phases using only ENDPOINT71. P53's failed global Bernstein search alone did
not prove this; the new point and strict rational certificate do.

It says nothing against b4 controls reoptimized over continuous phase,
arbitrary classical feasible search, full count/rank distributions, tails,
costs, loss, other sizes or hardware. The immediate P53c falsifier adds ALL35
b4 controls at the SAME pi/3, retaining the old witness/graph unchanged for
diagnosis. No such control is yet evaluated in this report. A new coherent
mean response is not the user's required reproducible optimizer advantage.
Paper/P33/P37/E05b remain unchanged; positive confirmation and QPU gates closed.

## Subsequent evidence — 25 November 2026

The preceding next-step paragraph describes the original checkpoint.
P53c has since evaluated all35 SAME-phase b4 controls and retained the strict
fixed witness. A separate complete permanent implementation verifies all70
four-photon source laws,35 convolved controls and the original106-control
gap; see research/P53c_INDEPENDENT_PERMANENT_RECEIPT.md. P53d's further
all-classical-phase extension is a primary candidate pending independent
checking. These developments change the restricted mean-hull scope, not the
posthoc graph, classical-search limitations or the still-open optimizer goal.
