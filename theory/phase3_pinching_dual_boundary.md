# Boundary obstruction to a finite dual-witness proof

2026-11-22, self-review of theory/phase3_pinching_dual.md at197af80.
The variational identity with an infimum remains correct. Its final request
for finite witnesses costing at most k!*delta needs a boundary restriction.

At delta=0 all occupied-column supports are disjoint. Every nonzero pinching
sector contains exactly one permutation assignment, so its Gram matrix is
G=|pi><pi|. The pinched states agree directly and D_pinched=0.

However for K=J-I, k!>=2, every finite feasible dual Z>=0,Z>=K has
Z_(pi,pi)>0. If that entry were0, positivity of Z would make its pi row0.
The pi diagonal of Z-K is also0, so positivity would force its pi row0,
contradicting its off-diagonal entries -1. Thus every such sector has a
strictly positive finite dual cost. Summing finite costs cannot prove an
exact upper bound of0. The infimum is0 but is not attained.

This refutes the all-delta **finite-witness subgoal**, not the pinching
conjecture or its dual identity. A valid continuation must handle delta=0
directly and seek witnesses/limits for delta>0, or prove bounds with vanishing
excess before taking a limit. A bounded continuous dual ansatz at disjoint
supports is unjustified. Other singular sectors can also require care.

The argument is exact elementary PSD algebra, not inferred from a failed
optimizer or finite experiment. It supplies no novelty or optimization claim.
