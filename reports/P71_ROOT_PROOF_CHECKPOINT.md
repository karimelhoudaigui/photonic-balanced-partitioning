# P71 accepted: approximate optical cross-rank obstruction

25 November 2026. ROOT read the complete301-line author proof,348-line
before-reading independent derivation and285-line exact-source review,
and accepts the statement under its explicit source, target and history
hypotheses. CLAIM-042 remains OPEN; this is not a positive optimizer result.

Author `research/P71_approximate_cross_rank_transport.md`, commitb2f84ccb,
SHA256 `c320f925b53f68738931da93ef28bb0a2f84f887988404153f974dae8b6cfe03`.
Independent `theory/P71_independent_effective_rank.md`, original5a1ff71/
root8b8783c, SHA256
`33ccc65cf779f76cbb57da787522267dbc0379d8e96555f6ca50ac0569256dc8`.
Exact review `theory/P71_AUTHOR_EXACT_HASH_REVIEW.md`, originalcd59bcf/
root6ada954, SHA256
`7a626452c8d6e7cfbaa000bb37fc3f77a736cd5d5c880b011f650af68e7da992`.
ROOT supplied the candidate/route; the review independently reconstructs
the mathematics, not its discovery. All statements are static, not runs.

## Accepted implication

For a passive unitary U split into two equal blocks, its CS singular values
s_i are those of its cross block. Truncating all but r CS rotations gives
a UNITARY V with cross rank<=r and exact operator distance

    ||U-V|| = sqrt(2-2sqrt(1-s_(r+1)^2)) <= sqrt(2)s_(r+1).

The proof constructs complete endpoint/degenerate CS bases, including
singular values0 and1. It does not discard part of a matrix and pretend
the result is unitary. In a fixed K-photon sector, tensor telescoping and
pure-state trace distance give PNR total variation<=K||U-V||. ROOT checked
the factor: no additional one-half belongs in this upper bound.

For the P69 L/L CF source, K=2L, and either full-block CF target,

    P_U(good) <= min(1, p(L,r)+sqrt(2)K*s_(r+1)),

with r=0 treated by p(L,0)=0. The source/target hypotheses of P69 remain
essential. No arbitrary-source or decoder claim follows.

For adaptive controllers the safe first-exit bound conditions on the actual
history and adds expected per-step errors (and, when used, thermal exits).
A full transcript-TV coupling needs the SAME classical update kernel and
record schema driven by counts. Actual differing U/V matrix tags or backend
timing records can distinguish transcripts with TV1 and are excluded.
The review checks measurable CS selection and the correct survival indicators.

A polynomial singular tail supports only the corresponding additive error
bound; it does not imply exponential suppression on an arbitrary horizon.
Exponential conclusions need sufficiently small tails and the stated
horizon. No measured device tail, hardware cost or novelty is established.
