# R4 adaptive replacement: substantive checkpoint, not goal completion

Owner: coordinator; base03b92ea, 2026-11-22. Three requested independent agent
packages were quota blocked; this route's new proof is self-reviewed only.
Target: propagate an exact per-circuit density/TV condition through a classical
adaptive, fresh-input protocol at equal physical attempts, including training.

Result: `theory/phase3_adaptive_replacement.md` derives transcript TV at most
1-product_t(1-e_t), at most sum e_t, and a history-sensitive expectation bound.
The distinguishable replacement samples independent categorical outputs with
charged frame construction and preprocessing. Relative rare-event ratios,
coherent memory, exact-distribution oracles and equal accepted shots are excluded.

The decisive finite check is `experiments/P34_adaptive_replacement/run/`:
four exact rational policies with T1/2/3 or stopping on success, plus a two-step
control. All ten outcomes, including collisions, enter the histories. The
largest enumerated tree contains1058 histories, including zero-mass leaves.
All asserted inequalities pass exactly. T3 transcript TV is approximately
0.02900506, below the product bound0.16186482 and history-sensitive bound0.03149941.
The initial-zero-certificate control has positive transcript TV0.004981287:
checking only the first circuit is insufficient for an adaptive protocol.
No optimization signal, shots, hardware or population inference is claimed.

Source update superseding the proof note's pending extraction sentence:
the author-hosted second edition of Levin–Peres, with Wilmer contributions,
*Markov Chains and Mixing Times*, was downloaded from
https://pages.uoregon.edu/dlevin/MARKOV/mcmt2e.pdf on2026-11-22.
PDF SHA2569ef39f9467d9647ff3f5e8747b9ce24b7a90d13be2f8156fbd827b95b661a772.
Apple PDFKit extracted461 pages; text SHA256
92cae05daaa965e8f4551f99d7a7d880fb693c5bb1a5e9f662017ee0fdf800e0.
Both are retained only in the existing ignored `.local/references/` cache.
No fetched full text is committed.

Checked locator: §4.2, Proposition4.7, equation4.8, printed page50/PDF page66;
construction on printed pages51–52. The source identifies TV with the minimum
coupling mismatch probability and explicitly constructs a coupling attaining it.
Dictionary: source mu,nu become the two conditional complete Fock laws at the
same history; its maximal coupling is used successively before the first
mismatch. Finite outcome distributions meet its hypotheses. Authentication,
statement extraction and this local application were checked by the same
coordinator. Implication verdict: verified for the coupling leaf. The adaptive
photonic composition still awaits a fresh proof audit.

Overlap label: **formal corollary not stated** for the composed adaptive bound;
ordinary sequential coupling is known. No novelty is claimed for this route.
This result makes the density theorem operational and sharpens fair-baseline
accounting; it does not rescue the original optimization hypothesis.

Disposition: KEEP as a conditional classical-replacement consequence. Next:
fresh proof audit; then examine whether any proposed optimizer uniformly stays
inside its small TOTAL-error regime. A few visited circuits cannot establish
that hypothesis. The remaining genuine-benefit route remains OPEN.
