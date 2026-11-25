# P48: graph-filtered occupied subspace — prospective claim card

25-Nov-2026, root/Astra. This is a new DEV mechanism after P47, not an accepted
positive, a revision of its data, or a QPU plan. No P48 code/outcome exists at
this freeze. P47 B gained22 versus D0, but a single fixed annealing control
equalled or beat its best cuts on all four graphs. That veto remains.

## Changed physical bottleneck and falsifiable hypothesis

In the full hollow architecture the newly occupied block has projection
Gram pI. Its unconditional second occupation moments lose all quartet phases.
This does not prove a no-go for PIT/completion, but it motivates a different
occupied subspace rather than another polar-routing step. Encode the graph
through a heat-filtered rectangular isometry spanning ALL vertex output modes.
Its projection Gram is generally nondiagonal on those vertices. The hypothesis
is that the resulting bosonic copula, after marginal PIT and the same charged
completion, can improve graph cuts beyond independently selected D, Gaussian,
classical coherent-field and feasible-search controls. This is open. A Gram
diagnostic, changed variance or positive B-versus-D pilot alone cannot pass.

## Prospective construction (no optimum or anchor in the optical map)

For integer weighted adjacency A on N=2K vertices let L=diag(A1)-A. Set
Lhat=L/||L||op when nonzero, otherwise zero. Set r=K source photons. Draw ONE
role-seeded complex Gaussian frame Z of shape N-by-r, entries with independent
standard real/imaginary parts divided by sqrt(2). Use that SAME Z for
tau in {0,4}. Define

    Y_tau=exp(-tau Lhat) Z,
    V_tau=Y_tau (Y_tau* Y_tau)^(-1/2) = rectangular polar(Y_tau).

V*V=I_r. Numerically use thin SVD Y=U Sigma R* and V=UR*. Record singular
values, residual and Gram for every graph/temperature; do not reject graphs
or replace frames to improve outcomes. Build a full N-mode unitary with
FIRST r columns exactly V and any verified orthonormal vacuum completion.
Input is |1,...,1,0,...,0>, r fixed source ports. Output modes are the N graph
vertices. The input port labels do not encode a partition or a known solution.
There is no retained old anchor block, transfer filter or discarded collision.

Tau0 is the graph-blind random-subspace ablation. Tau4 is graph-guided. This
is established heat filtering and polar linear algebra, not a novel theorem.
Under full-column-rank Z, smin(Y)>=exp(-tau)smin(Z) and
cond(Y)<=exp(tau)cond(Z). A row permutation Pi with Z carried to Pi Z gives
V -> Pi V. Fresh Z is row-isotropic in law. Eigenvalue degeneracy creates no
truncated-eigenspace convention. Near-rank-deficiency is an explicit numerical
failure retained as inconclusive, never a reason to redraw a favorable frame.

The graph and all preprocessing are given to every control. A common anchor,
single swaps, direct spectral rounding, deterministic zero/greedy decoders and
every scored counterfactual vacuum-PIT discovery are credited to Cref first.
The optical isometry is independent of that anchor; its construction is charged.
Direct spectral rounding uses the already computed Laplacian eigenvectors:
score top-K and bottom-K sets of each of the first r nonconstant eigenvectors
(available vectors only), without evaluating an optimum or selecting a graph.

## Physical invariants and strong explanatory nulls

Let q_ia=|V_ia|^2, mu_i=sum_a q_ia, P=VV*. For CF input photons:

    E n=mu,
    Cov_B=diag(mu)+|P|^2-2 q q^T,
    Cov_D=diag(mu)-q q^T.

The usual PSD-Laplacian obstruction for raw quadratic occupation energy still
applies. The claim being tested requires a nonlinear feasible decoder. It is
not established by lowering an unconstrained occupation energy.

All seven primary arms have the same decoder and independently selected
tau/lambda settings: B, D, species groups of at most4, Gaussian_Bcov, IID
uniform, fixed-amplitude continuous-phase multinomial, spherical-coherent
multinomial. The last two are essential classical bunching controls:

- Phase: z_a=exp(i theta_a)/sqrt(r), theta independent uniform; draw
  Multinomial(r, |Vz|^2). Use continuous phases or r+1 roots, NOT four roots.
- Sphere: z=g/||g|| for iid circular complex Gaussian g; draw
  Multinomial(r, |Vz|^2). This is a positive classical mixture; all norm/cost
  checks remain explicit. No vacuum component or preparation probability is
  silently postselected.

Their one-mode PGF coefficients in powers of (s-1) are

    c_h^phase=(r)_fall_h h! / r^h * [t^h] prod_a sum_m q_ia^m t^m/(m!)^2,
    c_h^sphere=(r)_fall_h mu_i^h / (r)_rise_h,
    c_0=1.

Mean equals mu_i. The phase formula must keep sum_a q_ia=mu_i<=1; the P47
unit-row conditional oracle must NOT normalize this to1. A NEW helper with
explicit subunit row convention, Decimal80 and recorded tiny corrections is
required. Sphere can instead use a nonnegative mixture: for r>=2,
L0~BetaBinomial(r,1,r-1), then n_i|L0~Binomial(L0,mu_i). Handle r1 and vacuum
separately. Test these against independent finite phase enumeration and exact
integrals/moments before any DEV graph outcome. Gaussian PIT divides by its
actual factor variance after clipping. Every PIT has independent per-mode
jitter, zero-mass branch and explicit arithmetic tolerance. Exact marginal
identities do not certify the joint copula or rare tails numerically.

## Frozen prospective DEV population and costs

Four NEW graphs, not held-out confirmation:

| N | r=K | Family | Seed |
|---|---|---|---|
|26|13|weighted ER p=.35|4802601|
|26|13|weighted RR degree4|4802602|
|34|17|weighted ER p=.35|4803401|
|34|17|weighted RR degree4|4803402|

Integer weights1..9 and generation convention inherit the immutable P43
helper; no graph replacement. Frame/priority/species/production/baseline seed
namespaces must be fixed in a spec before execution. Grid tau0/4 and decoder
lambda0/1 has four settings. Two trial seeds0/1, eight proposals per setting
per trial per graph:256 proposals per primary arm. Source photons per optical
arm3840, with all raw counts retained. No known optimum, optimum mask, held-out
graph or QPU access. Same completion target K=N/2 and initial q=ceil(K/2).

Retain anneal, spectral+swap, collective KL and shared-Delta block matching,
each independently given3200/5536 informative cut-score units per graph/trial
as in P47. Add direct heat-subspace rounding with feasible swap improvement:
sample spherical fields from each tau, round top-K |Vz|^2, score and refine,
with the same score ceiling. Its extra own trials are not pooled for free.
Keep actual measured time prefixes and preprocessing ledger separately;
informative score units are not an exact count of every repeated cut() call
and do not equate simulator time to QPU latency. No total-cost/hardware
advantage can be asserted from this development veto.

One worker/thread, CPU60/wall90/output32MiB, planned arrays<=256MiB. Commit
code/spec/contracts/tests before the first preflight; obtain independent static
review. Main runs only after preflight PASS. Keep all failures and partial
outputs, no automatic retry. Strong fixture checks: V/unitary normalization,
all-count Fock/labeled/species marginals, covariance, nonunit row phase/sphere
PMFs, row permutation with carried Z, zero graph, source port convention,
PIT and full informative resource accounting. No paper edits.

Decision: REJECT frozen mechanism/budget when strong controls explain it;
FOLLOW-UP only for a mechanism-specific signal meriting frozen fresh-seed,
relabeling and then held-out tests; INCONCLUSIVE for computation/precision
ambiguity. No positive gate is accepted by these four DEV graphs alone.
