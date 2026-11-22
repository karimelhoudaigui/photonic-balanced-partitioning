# P36b: bounded phase-sensitive search found no counterexample

Completed from frozen protocol3f7f7b3. General TV<=delta for k>=3 remains OPEN.
No absence of a counterexample, solver flag or observed maximum proves it.

Eight searches used two seeds and two target leakages in each family: a
three-angle/one-phase three-mode unitary, and a general six-by-three frame
obtained by QR around disjoint pairs. Differential evolution used1464 calls
per three-mode cell; Nelder-Mead used3000 per six-mode cell. Every one of the
17856 calls is retained with parameters, leakage, full-law TV, penalized score
and numerical residuals. The experiment's externally enforced limit was120
seconds/one thread; it completed without exhausting that limit. Physical shots0.

The score kept the leakage near0.25 or0.75 while separately recording the
largest unpenalized excess. No excess exceeded the1e-8 falsifier. The largest
observed excess was -5.928e-7 at small leakage; this is not a uniform margin.
Score winners had leakage approximately0.238–0.710 in the three-mode family
and0.237–0.720 in the six-mode family. Solver iteration/evaluation caps are
retained explicitly; this is not global-optimization certification.

The audit `experiments/check_linear_leakage_search.py` reads every trace row,
rechecks scores, normalization/orthogonality bounds, cell counts and stored
winners. All16 stored winners (excess and penalized score) were reconstructed
and compared with Perceval, maximum probability error8.882e-16. This is a
post-run physical audit, not an independent precommitment or fresh-agent proof
review. Its valid v2 manifest is in `experiments/P36_adversarial/review/`;
the search manifest and complete trace are in `experiments/P36_adversarial/run/`.

The targeted search changes the discriminator beyond the earlier random grid:
it attacks phase-sensitive nongeneric frames rather than infer a theorem from
random examples. It nevertheless leaves the same missing implication: control
of occupation measurements retaining cancellations lost by the positive Gram
majorant, or an analytic k>=3 counterexample. The two-photon exact bound and
the counterexample to the permanent shortcut remain the proven partial results.
Do not repeat this unchanged search until a different construction or method
addresses that bottleneck. No graph algorithm, manuscript or QPU gate is advanced.
