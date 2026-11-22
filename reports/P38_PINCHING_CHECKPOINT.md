# P38: phase-preserving upper bound, still an open general inequality

The new route preserves three-cycle phases before measurement. Dominant-region
pinching retains quantum degrees of freedom inside each region; fine occupation
TV is at most that pinched trace distance. Grouping the classical outcomes
alone would give the opposite, unhelpful comparison. The derivation is in
theory/phase3_pinching_dual.md, frozen197af80.

The pinched distance depends on27 Gram matrices of order6. A matrix variational
identity supplies exact upper witnesses; its dual is an **infimum**, not always
an attained minimum. A two-dimensional exact example proves nonattainment.
For complex three-column frames, a support-perturbation argument also reduces
the sufficient lemma to three PSD3-by-3 effects with dominant diagonals and
sum I. Every such triple admits a dominant rank-one refinement with at most27
rows. This does not generalize by the same argument to four columns.

These are structural reductions, not a proof of the desired linear bound.
Standard Naimark/least-disturbing structure is already in primary literature.
The exact coefficient-one pinched inequality, and the weaker measured-TV
conjecture, both remain OPEN. The source draft distinguishes these quantities
in research/P36_PRODUCT_MEASUREMENT_SOURCES.md. Its old enlarged-domain caveat
is superseded only for complex k3 by the new cone proof, as its prefix records.

## Actual executions and coverage

The reviewer planned a new finite falsification experiment, then hit quota
before code/execution. Astra implemented and ran it from frozen197af80.
All36 Gaussian-rational physical frames are retained: m3/6/9, seeds20261201..03,
strengths1/40,1/5,1/2,1, nonflat disjoint starts and all row-pair complex rational
Givens rotations. Exact frame orthogonality and delta pass. Twenty-one cases
have delta<5/6, the nontrivial range; the other15 are not silently discarded.
Full Fock laws have at most165 occupations and retain every collision.

Two identity and three sharp k2 controls pass. Six newly executed Perceval
comparisons have maximum probability error1.11e-16. No numeric candidate for
D_pinched>delta was found; largest excess is -7.37258e-6. This is finite
evidence, not a universal proof or a uniform margin. Primary runtime0.501s,
zero physical shots. Raw data/trace: experiments/P38_pinching_probe/run/.

A separate Astra implementation reconstructs the states in the ordered-particle
tensor basis and diagonalizes each actual density-matrix block, without Gram
square roots. It checks all36 pinched distances and reaggregates every ordered
probability into occupations. Max pinching discrepancy9.50e-14; max probability
discrepancy2.23e-16; max trace residual1.71e-16. Runtime16.876s. All stored
Perceval laws and the entire progress trace agree. This is a distinct code path
by the same author, not independent-agent review or interval certification.

The exact Rayleigh certificate code, untriggered on the36 cases, is exercised
on the three sharp controls: its rational lower bound equals the known rational
distance exactly in all three. No counterexample certificate is being claimed.
Both primary and review v2 manifests validate, status completed, under120s and
one conventional numerical-library thread. Perceval/cache warnings are retained.

## Interrupted work and next discriminator

The physics agent left complete exact formulas for two connected k3 families,
an exact signed cycle decomposition and15 bounded diagnostics. The real files
are preserved with original hashes under experiments/P36_interrupted_phase_attempt/
and research/P36_PHASE_ANALYTIC_INTERRUPTED.md. Its original computation manifest
validates in its worker. The mathematical continuation and literature draft
had no final return/commit after quota; they are explicitly labeled as such.
Do not rerun their fixed-output scripts in place.

Decision: KEEP the reduction and finite checks; INCONCLUSIVE on the universal
linear inequality. A changed next step is constrained optimization over the
compact three-effect domain or a phase-aware analytic witness, not another
unchanged measured-TV grid. The constant dual witness only recovers5/6;
it does not solve delta<5/6. A refutation of the stronger pinched bound alone
would not refute the actual measured-TV conjecture. No graph advantage,
novelty, manuscript readiness or QPU gate follows.
