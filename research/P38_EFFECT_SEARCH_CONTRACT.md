# P38b: search the compact three-effect domain

Base d1661b5. The36-frame discriminator and its direct-state audit completed
without refutation. The changed next step uses the proved complex-k3 cone
reduction: optimize over three Hermitian PSD3x3 effects E_g with sum I and
E_g,gg>=E_g,aa, rather than sampling another frame grid. A positive result
would refute only the stronger pinched-state lemma, not measured TV<=delta.

Four sequential SLSQP cells: target delta1/5,3/5; seeds20261210,20261211.
E1,E2 have18 real coordinates; E3=I-E1-E2. PSD, dominant diagonals and
target-delta equality are explicit constraints. Begin from the strictly
feasible diagonal model with small seeded complex off-diagonals. Max25
iterations per cell,4000 objective calls globally,120s wall,1thread,retries0.
All objective calls including infeasible trials and solver failures retained.
No global-optimality claim from solver success or absence of a counterexample.

Compute D_pinched from27 Gram matrices of order6. Any near-feasible trial
with D-delta>1e-8 is a numerical candidate. For each cell's largest excess,
rationalize E1,E2 exactly and form exact E3=I-E1-E2. Mix toward the strict
diagonal model, testing eps=2^-30,...,1, until every exact principal minor and
dominance difference is nonnegative. Preserve the repair and actual delta.
Exact Rayleigh lower witnesses certify a stronger-lemma counterexample only
when their rational sum/6 is strictly greater than exact delta. A repaired
candidate failing this test is inconclusive, not a counterexample.

One rational embedded two-photon control exercises the effects-based witness
code before search. Physical realizability is an existence consequence of the
cone lemma; no explicit optical implementation, Fock simulation, Perceval call,
shot, optimizer training or hardware execution is claimed by this matrix search.
