# P56/P57 ROOT analytical checkpoint

These are scoped analytical results, not completed positive optimization
research. No graph, simulation, physical shot or QPU call was performed by
this review. ROOT read all primary notes, independently reconstructed the
critical identities below, and reconciled the separate reviewer correction.
No external novelty claim is accepted.

## P56 symmetry and its actual escape conditions

Exact primary7fee87b/root9e61035: all206 lines of the visibility theorem and
continuation card were read. The count law is invariant under simultaneous
C5 translation because the row permutation is a column phase of U. Uniform
top10 ties transfer that invariance to the feasible law. ROOT verifies
f_A(theta)=f_barA(theta) at the SAME theta, not equality of encoded pipelines,
and the lower bound by the minimum orbit-average cut.

The190 edges have free size-five orbits; the projected dimension is38 and
kernel dimension152. The nonnegative J-I plus opposite translated-edge
perturbations has invariant mean100 although feasible costs differ. Burnside
gives(184756+4*6)/10=18478 cut orbits; their explicit enumeration costs stay
paid. None is an all-tail, adaptive-selection or universal equal-cost bound.

For the proposed within-color N20 output mixer, ROOT derives directly
q=[1+s*cos(2*pi*b/5)]/20 on one mixed row and sum(q^2)=1/20+s^2/40.
Thus its count variance changes while q is phase independent; a generic
fixed output unitary would not suffice. Physics5f9ae00/root2a16402 provides
the independently derived full-square q-only formula for ALL factorial
moments through three, without needing flatness. ROOT reconstructs its
identity/transposition/three-cycle terms and confirms their multiplicities.

The N8 within-color U2 surrogate fails. For SU2 matrix[[a,b],[-b*,a*]],
direct multiplication verifies X V=Z V* Z X. The two stated source-matrix
identities then give the antiunitary full-count C2 symmetry. This excludes
that proposed escape, not odd members or mixing across colors. P59 therefore
examines a different odd member; no mean derivative has yet been computed.

## P57 cycle mechanism and complete classical replacement

Primary5432b7d/rootd8a3935 and independent same-team nonblind audit36d3ad1
were read in full. ROOT reconstructs the two interfering route words,
full-cell sector mass2^(1-L), event(2+2cosPhi)/4^L, proper-species phase
blindness, quadratic-cut parity cancellation and the explicit strict49-swap
barrier. The improvement PROBABILITY is1/256 versus5/256, as in the primary.

Two corrections are explicit in Git. First the MPS amplitude convention
uses incoming phase z_j^p for C:j->j+1; ROOT corrected the primary after
the independent review and checked the phase assignment directly. Second
ROOT caught the reviewer's C(4)=2 arithmetic error before accepting it:
C(4)=3, improvement gains2/5, K=-5, accepted-gain function
(15-5cosPhi)/512, difference5/256. Separate correction6c1600f/rootff774d7
preserves the old erroneous review in history. Event probabilities and route
rejection never changed. This is why reviewer agreement alone is insufficient.

The corrected review gives a complete direct classical sampler: fair route
bits, local vacuum/single/HOM sampling off the constant-route branch, and
conditional parity law(1+sigma*cosPhi)/2^L on that branch. ROOT verifies its
normalization and each complete outcome probability. At0/pi it uses only
O(L) fair bits/work. General phases require specified cosine precision;
TV error is at most2^(-L) times its absolute error. Actual classical and
decoder costs still need measurement for a finite runtime comparison.

Independent retiming/permutation also trivially solves the particular graph.
The new physical response is therefore not an optimizer advantage. Three
matchings on a wider routing graph are only a static continuation with a
missing accepted-gain coefficient, not a hardness claim or approved pilot.

Self proofreading of the extracted P53d theorem and these equation-heavy
notes checked constants, hypotheses, normalization, scope and provenance.
Paper/P33/P37/E05b remain intact; the user's positive target remains OPEN.
