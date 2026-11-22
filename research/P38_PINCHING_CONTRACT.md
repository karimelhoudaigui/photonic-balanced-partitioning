# P38: falsify a stronger, phase-aware pinching bound

Base5375202,2026-11-22. The objectives reviewer planned this discriminator but
hit quota before creating code or running it. Astra takes over; do not claim
agent execution. No manuscript, noise, model service, paid inference or QPU.

Question: for physical orthonormal three-column frames, does the trace distance
after dominant-group pinching exceed delta? This is a stronger sufficient
lemma than the measured full-law TV<=delta conjecture. Its failure alone
does not refute that measured conjecture. Its validity is not inferred from
a finite sample. Root derivation: theory/phase3_pinching_dual.md.

Population:36 exactly Gaussian-rational frames, m3/6/9, seeds20261201..03,
rational strengths1/40,1/5,1/2,1. Start from disjoint nonflat column supports
(identity, pairs3/5:4/5, triples1/3:2/3:2/3), then apply every output-row pair
once in a seeded order with rational complex Givens rotations. No frame is
rejected or selected for its result; all deltas and laws retained. Distinct
construction from physics' interrupted15-frame diagnostic, not a rerun.

Check exact orthonormality and delta. Compute27 sector Gram matrices of order6
with complex128 eigensolvers, both trace-norm and positive-eigenvalue forms,
all fine Fock probabilities by explicit six-path routing, and D_fine<=D_pinched.
Six fixed new Perceval checks: each m at seed20261201 and strengths1/5,1/2.
Identity and sharp k2 controls check normalization and factorials.

Any D_pinched>delta+1e-9 is only a numeric candidate. For each candidate use
rationalized Rayleigh vectors and exact sector Grams to compute a rigorous
lower bound sum_s max(0,y†GKGy/(y†Gy))/6. Only an exact lower bound above
exact delta certifies a counterexample to the stronger lemma. Retain all
candidates, inconclusive witnesses and raw complex/rational frames.

One conventional CPU thread,120-second wall cap. No large Fock laws: at most
165 occupations. Full measured laws include all collisions. Zero physical
shots, no optimizer, no novelty or graph-advantage claim. Preserve partial
progress if the cap or a check fails; no overwrite of prior records.
