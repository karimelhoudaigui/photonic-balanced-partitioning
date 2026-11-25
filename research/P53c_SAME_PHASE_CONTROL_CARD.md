# P53c — same-phase four-body falsification (STATIC proposal only)

ROOT requested this after inspecting P53b's endpoint-library separator.
P53b remains intact: x=1/4, theta=pi/3, the same full-eight-photon source,
uniform-tie top4 decoder and posthoc graph. No new control, kernel, LP or
sample has been evaluated for this card. No implementation/run is authorized
by the card itself. This is a post-result falsification, not a blinded test.

**Question.** Does adding ALL 35 complementary 4+4 species groupings at the
SAME theta=pi/3 explain the fixed quantum mean? Retain every original
ENDPOINT71 vertex and append all 35, giving 106 labeled vertices, including
duplicates. No group, output occupation or unfavorable result is filtered.
Membership would explain this single mean vector with finite four-body
controls; it would not prove a full-law identity or a theorem for all theta.

## Independent algebra check

Let xi=exp(i*pi/3). The exact ring is Z[xi]/(xi^2-xi+1). Represent a+b*xi by
the INTEGER pair (a,b). Direct substitution gives

    (a,b)*(c,d) = (a*c-b*d, a*d+b*c+b*d),
    conjugate(a,b) = (a+b,-b),
    norm(a,b) = a*a+a*b+b*b = (a+b/2)^2+3*b*b/4.

Hence the norm is nonnegative and zero only at (0,0). The six powers are
(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1), returning to (1,0). These identities
were reconstructed algebraically, not inferred from floating complex values.

Use the original column geometry, not a newly chosen interferometer:

    U[i,a] = s[i,a]*xi^((i mod 4)*1[a>=4])/sqrt(8),
    s[i,a] = Walsh[i mod 4,a mod 4]*(-1)^1[i>=4 and a>=4].

The root-of-unity norm1 and the Walsh/block cancellation prove the same
unitarity. For each group G of four DISTINCT input ports, multiply its four
linear creation forms over the ring, retaining all 330 occupations n of four
photons in eight modes. If C[G,n] is the unnormalized coefficient, then

    P_G(n) = prod_i(n_i!)*norm(C[G,n]) / 8^4.

The normalized Fock amplitude has factor sqrt(prod n!)/8^2. In particular,
the output factorial MULTIPLIES the coefficient norm, and the probability
denominator is 8^4. Exact sums must equal 8^4 before any control is used.
Compute all 70 input-group laws once; the complementary species pairs are
the 35 groups containing port0, paired with their complements.

For two distinct species groups G and Gc the observed TOTAL count law is

    P_G|Gc(n) = sum_(u+v=n) P_G(u)*P_Gc(v).

This is a convolution of probabilities: NO extra final-output factorial or
interference between species is introduced. Keep all 6435 occupations,
including exact zeros, and assert mass 8^8. The unchanged uniform top4 tie
pushforward uses integer weights with denominator420. Every new edge mean
therefore has denominator dividing 420*8^8, incident sums4 and total16.

## Proposed finite procedure, subject to ROOT arbitration

1. Pin P53's original exact source/library and P53b's certificate by SHA256.
   Reconstruct the SAME exact x=1/4 target and verify equality to the saved
   P53b target. Keep the original 71 kernels unchanged. Read exact Fraction
   fields canonically; floating proposal fields never supply physical data.
2. Construct the 70 ring-valued four-photon laws and all 35 probability
   convolutions, then exact tie pushforwards. Archive all laws/labels and
   normalization/incident checks, without changing source or decoder.
3. Evaluate the SAVED P53b signed dual and normalized nonnegative graph on
   the new controls over Q, with no LP. Report every margin and its minimum.
   The P53b graph remains fixed. A new control beating that graph's mean is
   a falsifier of extending that graph claim to the expanded library.
4. At this SAME target, permit at most ONE primal and ONE dual provider call
   over ALL 106 vertices. Reuse unchanged qualified HiGHS options/readback,
   native1s/thread1, seed5201001. Primal support-only exactification and dual
   signed-binary Fraction.from_float/L1 rescaling/all-106 strict checks are
   unchanged. Retain raw proposals, strict rational margins and failed gates.
   No additional point, solver, threshold, grouping, LP or retry.
5. Require status0/successTrue AND an exact witness. Both exact witnesses
   simultaneously verified is inconsistency/failure. A new dual, if any,
   is a separating FUNCTIONAL for the fixed106 mean hull, not a replacement
   graph benchmark; do not switch the P53b graph to rescue optimization.

Outcomes: exact membership certifies only the point's mean replacement;
strict exact separation certifies only nonmembership in this expanded fixed
library; otherwise INCONCLUSIVE. Failure of the old dual does not itself
prove membership. Membership here cannot imply all-phase classicalization;
separation here cannot exclude continuously reoptimized b4 or strong
classical feasible search. N=8 remains classically trivial for graph search.
No C*, optimum mask, known partition or optimizer training appears anywhere.

## Prospective implementation, qualification and limits

Only after ROOT approval: new P53c source/tests/spec/contracts, frozen before
imports. Reuse immutable exactification/native-check/dual helpers; do not edit
P53/P53b or old artifacts. Qualify ring arithmetic against an independent
Q+Q*sqrt(-3) representation, selected four-photon coefficients against direct
source-assignment/permutation enumeration, Fock denominators, probability
convolution with known small fixtures, exact tie means and mocked gates.
No full106 fit or evaluation of the real B target in qualification.

Planned bounds: 70*330 group outputs; at most 35*330^2=3,811,500 integer
convolution pairs, plus bounded tie aggregation; at most two native1s fits
and two bounded29x106 exact systems. Use Python integers/Fractions, never
int64 proof overflow or rounded kernels. Archive new occupation/group laws,
all106 labels/means, fixed-old-witness diagnostics and proposed certificates.
Propose CPU20s/wall30s/thread1/log4MiB/scientific4MiB/planned64MiB scientific
arrays, no hard Darwin memory promise. A projected cap failure remains a
preserved failure, not permission to raise caps. Static review, one exclusive
qualification, then a distinct explicit main gate are all required.

No new graph/sample/QPU/manuscript action or accepted optimizer positive
follows from any P53c outcome. This task tests whether the apparent endpoint
separator merely omitted same-phase four-body controls.
