# P38c: resume the specifically capped effect searches

P38b completed2076 calls and no certified refutation, but all four solvers
stopped at the25-iteration limit. This follow-up changes that bottleneck:
warm-start each same cell from its recorded best near-feasible parameters,
allow120 iterations, and reduce finite-difference step from2e-6 to1e-7.
No new seed/cell or favorable result is selected; all four are retained and
their previous cost stays charged. Global cap12000 calls,120s,1thread.

The physical domain and strong-lemma distinction are unchanged. Preserve
every objective call, constraint residual and final solver status. Independently
of any positive numeric excess, repair and rationally validate each cell's
best point using the frozen exact PSD/dominance/Rayleigh routine. A rigorous
refutation still requires exact lower>exact actual delta, not solver success.
No global proof, new circuit, Perceval call, physical shot or QPU inference.
