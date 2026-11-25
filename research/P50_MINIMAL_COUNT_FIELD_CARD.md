# P50 proposal — direct count fields, prospective only

25-Nov-2026. Short design for review, **no code/run authorized by this card**.
No graph, seed population, simulation or held-out panel has been generated.
P49's unchanged negative hybrid result and its scoped cost audit remain valid.

## Candidate and physical nulls

For an explicit weighted graph on N50 or100 vertices, K=N/2, keep respectively
r13 or17 photons; do not identify fixed photon number with feasible occupancy.
Use the P49 carried-gauge spectral E and R in {I,R(pi/4,0),R(pi/4,pi/2)};
retain graph-blind Fourier as an encoding control. V has orthonormal columns.
All arms observe ALL occupations, including collisions, with no postselection.
Let Q=|V|², mu=Q*1, dmax=max weighted degree. Define

    H = I-alpha*L/dmax, alpha in {0,1}; H=I if dmax=0,
    y = H*(n-mu) + beta*zeta, beta in {0,.1},
    zeta_i iid Uniform[-1,1], independent of the observation,
    S = top K entries of y; score the actual balanced cut C(S).

No Cref, anchor, Delta, CDF, PIT, greedy completion or other-model PMF enters
this policy. Training minimizes the exact all-shot normalized feasible-cut
mean, equally per graph, separately for every model. It never uses C*, masks,
success labels, previous incumbents or evaluated outcomes. A paid best sampled
partition may be retained without affecting the source or later proposals.

H is symmetric, nonnegative and doubly stochastic at alpha1; sum(n-mu)=0.
Thus every arm's centered field has mean0, not a graph-energy certificate.
For alpha=beta=0 and interior0<mu_i<1, ALL clicked modes belong to S because
their centered values are positive and empty-mode values negative. Remaining
vertices are filled by smallest mu; multiplicities then do not change S.
This inclusion is **support(n) subset S**, the REVERSE of P44's condition
S subset support(n). For r<K, P44 does not cover this completion.
With bounded jitter, support retention persists whenever
1-(max(mu)-min(mu))>2*beta; Fourier mu constant always satisfies it here.
Alpha1 can change that ordering; neither branch guarantees useful interference.
Quantized/tolerant ties must be fixed before execution, with carried priorities,
and tested on uniform mu so floating-point ties cannot encode a hidden rule.

## Controls and what a signal would have to survive

- D: independent categorical outputs Q[:,a], one per source photon; b4:
  fixed contiguous source-port blocks, same circuit, independently trained.
- Phase: z_a=exp(i phi_a)/sqrt(r), independent continuous phases, then
  Multinomial(r,|Vz|²). Sphere: z uniform unit complex sphere, same multinomial.
  Both have mean mu; sphere is invariant under right-unitary R, so remove
  redundant rotations from its grid rather than wasting its budget.
- Gaussian: g~N(0,Sigma_B), y=H*g+beta*zeta, where
  Sigma_B=diag(mu)+|VV*|²-2*Q*Q.T. Use the ACTUAL factor covariance and handle
  zero variance; no clipping of significant PSD errors. Independent noise:
  y_i=sqrt([H*Sigma_B*H.T]_ii)*g_i+beta*zeta_i, independent standard normals.
  This latter arm matches FINAL one-mode variances, not joint correlations.
- Static preparation null: n=0 gives -H*mu+beta*zeta; also test mean counts
  n=mu (pure jitter/ties). Their costs include their own graph/mean preparation.
  An advantage explained by these nulls is preparation/rounding, not photons.
- Strong classical controls start FROM THE RAW GRAPH, with paid random balanced
  initialization or paid spectral rounding. Include vectorized best-pair
  descent FIRST, then incremental annealing/multistarts/perturbations; no free
  Cref. Do not rely only on FASTv1's initial8N anneal steps under tiny budgets.

r1, monomial V, post-source column phases, conjugation, uniform-mu ties and
carried relabeling are required physics/decoder nulls. Gaussian reproducing a
B effect would explain it by classical second moments; B>D alone is insufficient.

## Cost and smallest useful discriminator

Meter B's OWN graph/basis/marks/gauge/rotation/required circuit preparation,
mu, H, jitter setup, topK, cut scores, training and selection. No covariance,
other-arm calibration, rounding discovery or diagnostics may inflate its FAST
allowance. Keep simulator setup/count generation separate; real programming,
photons/losses/detection/latency remain unmeasured, not established zero-cost.
Every control pays its own preprocessing, tuning and search; serialization
stays outside timed loops. CPU-from-wall and any ideal zero-optical-latency
envelope must remain explicit and are not a hardware advantage.

A bounded DEV veto can keep four cases (two graph families at each size),
32 training+32 fresh evaluation draws/case/arm: four bases x alpha/beta gives
16 settings x2 training draws, sphere8x4. Other redundant controls get their
own nonredundant grid/effort. Independent model selection precedes every eval.
No graph selection by score; ALL cases/seeds/caps to be frozen in a separate
execution contract. Use only serial local Clifford2017 samples at fixed r,
never full Fock enumeration; larger N still increases sampling, preparation
and scoring work, so a resource projection/preflight is required first.

This design tests whether cheap graph diffusion plus balanced ranking exposes
a high-order count benefit that survives ALL controls and efficient total-cost
search. It promises no positive or novelty. A DEV signal licenses only review
and a new prospective confirmation; held-out/program-alpha, independent physical
replication and hardware gates remain mandatory before any accepted claim.
