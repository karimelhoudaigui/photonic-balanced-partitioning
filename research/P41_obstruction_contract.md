# P41/R3 first discriminator: L1 escape and convex-order falsification

Base f09c7ec82b2fe23395116e21bd56614f3739107c. Exploratory analytic route,
not a positive optimization benchmark. Author p41_obstruction.

Target: independently expand the complete two-photon laws and test the exact
identity E_B H_L1-E_D H_L1=z*(mu I-2A)z, with no rejected sector hidden.
Check the connected Walsh path witness epsilon1/4,mu1, strict gap-3/16,
feasible minimum and all collisional values. Preserve its relation to existing
Walsh data; do not relabel it a new quantum algorithm or independent dataset.

Finite domain fixed before execution: all64 unweighted simple graphs on4
labelled vertices; mu in {0,1,3}; two rational orthogonal frames (Walsh and
three-mode rational Householder embedded in4). One additional connected
weighted witness epsilon1/4,mu1. No random seeds or optimizer.

Independence: direct two-particle routing/permanent formulas use Fraction;
the spectral difference is computed separately. For each graph test the
complete-multipartite equivalence by an exact induced triple criterion and
a rational quadratic-form LDL check, rather than floating eigenvalues.
All10 Fock occupations remain, including exact zeros. Costs use only A,mu.

Caps:10CPU seconds,30wall seconds, one thread, small JSON (<1MiB), and a fresh
output directory. Numerical slot must be granted by root before execution.
Commit code and this contract first. Save actual command, code/input hashes,
git commit/dirty state, versions, outcomes and all assertion failures.

Success means this finite assertion and implementation survive exact checks;
it does not prove the analytic theorem or novelty. Any mismatch falsifies the
implementation/statement pending diagnosis, and its run is preserved.
