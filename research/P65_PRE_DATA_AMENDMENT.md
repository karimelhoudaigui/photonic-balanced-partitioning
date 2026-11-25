# P65 pre-data clarifications, before code qualification

25-Nov-2026. ROOT adjudications following the independent P65 physics/card
review, before any source import, test, graph, seed evaluation or photon draw.
Frozen proofs43dd873 and design card/spec022962e remain byte-identical.
This separate additive clarification belongs in both qualification/main input
closures. Nothing below reports execution or alters the registered panel,
candidates, objectives, attempt budgets or adverse gates.

1. Fresh chains are independent draws WITH REPLACEMENT from their declared
   uniform feasible-start streams. Distinct means distinct chain/stream IDs,
   not necessarily distinct subsets. If two or all initial subsets coincide,
   retain them. No uniqueness assertion, resampling, rejection, reseeding or
   favorable start selection is allowed. The intentional arm-independent
   start aliases remain the same across all arms.
2. degree_A(i) means the EXACT WEIGHTED row sum sum_j A[i,j]. It is not the
   number of nonzero neighbors or NetworkX's unweighted degree. The Cayley
   scale is max(1,max_i sum_j A[i,j]+lambda*(N-1)). Small synthetic weighted
   nonregular fixtures must distinguish these interpretations independently.

The existing card already states that freshly re-sorted species4/4/2 groups
do not imply a symmetric aggregated kernel. That arm is an optimization
heuristic control, not an exact Gibbs sampler; B/D's fixed-parameter ideal
symmetry does not transfer to it by name. No optional arm runs in stage1.

The analytical K2,2 mixing gadget is not the adjacency of its deliberately
constructed graph-cost barrier; it cannot validate the chosen graph encoding.
For lambda0, the graph-derived Cayley unitary is block diagonal across graph
components and conserves each component's photon total. Positive lambda's
global background may couple components, without proving ergodicity. Retain
every registered ER case, including a disconnected realization; no filtering
or new graph is allowed. Smaller component-block fixtures are qualification
only and do not change the frozen parameter grid.

Implementation explicitly recomputes forty post-step current cuts per case,
including collisions and rejects. The common training-start cut is scored
once and its exact cached value copied on eight paid resets; three fresh
starts each have their own actual initial-cut call. Thus there are four
initial calls, forty current calls and one proposal call for every CF attempt.
Copies do not become fictitious scores. Fresh chain-best begins at ITS OWN
start cut; it never inherits training or global paid best.

No threshold-oracle route is used by this passive Cayley pilot. That separate
nonlinear route remains deferred; none of its hypothetical benefits enters
the B cost allowance or this algorithm's claim.
