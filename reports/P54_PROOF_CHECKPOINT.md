# P54 proof checkpoint — 25 November 2026

ROOT proof4d6826d, independently reconstructed43b35f9 and focused review
91fb868 are integrated. Read the precise claim in
[the proof](../theory/P54_full_input_small_hop_obstruction.md) and its
[independent review](../research/P54_FOCUSED_INDEPENDENT_PROOF_REVIEW.md).

For a fixed finite weighted graph, real sqrt(weight) hopping, full CF input
and ideal number-resolving top-half uniform-tie decoding, the local expected
cut increases by4t² Var_uniform(C)/q, with a fixed-graph O(t⁴) remainder.
The distinguishable coefficient is half and can be retuned; a classical
rare-hop mixture reproduces the leading decoded law. The general weighted
adjacency A=w extension is false, as the separate exact N4 covariance
counterexample shows. ROOT manually rechecked its three rational cut pairs
and covariance -31/750; no executable experiment was needed for that proof.

Correctness status: **PROVED AS WRITTEN, same-team independent reconstruction**.
Novelty, scalable remainder, finite-strength behavior, equal total resources,
partial filling, threshold detection, other decoders and useful optimizer
advantage are not established. This does not complete the user's objective.

Conservative self-review under mathbox:proofread-math covered all77 lines of
ROOT's new proof and the nearby statement conventions. Routine edits: none.
Mathematical-token changes: none. Unresolved prose/notation issues: none
within that scope. Independent correctness is supplied by the separate
focused audit, not by proofreading. Git diff --check passed. The full822
regression tests passed for the unchanged executable source; no extra tests
were invented for a hand-derived asymptotic theorem. Manuscript untouched.
