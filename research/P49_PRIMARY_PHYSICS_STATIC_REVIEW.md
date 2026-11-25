# P49 primary source: exact-freeze static physics review

2026-11-25. **Verdict: no blocking physics defect found in the frozen
implementation; suitable for the declared targeted preflight, conditional on
that qualification.** This is not a test result, numerical sampler certificate,
performance result or positive acceptance. No import, test, DEV graph generation,
sampling or numerical calculation was performed in this review.

Target encoding commit `927448ab1e3434e83c93f436cbfa9681284dc5f2`, parent
`e2cb96edd1af4ed187743a551f39ff59e2fe0b6b`. The encoding worktree was clean at
the target commit on the closing read. The authoritative card is ROOT commit
`dc85fa5b49b095de3ba39c37f35d0cada70b47dd`, file SHA256
`1278f53b2ba9512c189a6bc3098db0233153b22c72edaceba679694b76755b61`.
The earlier card's generic HOM phase error was corrected before this target;
it is not silently treated as correct.

I did not author this primary code or its tests. I previously supplied P49
physics derivations, identified the card's HOM phase issue, reviewed the
inherited P48 helper and FAST, and authored earlier noise/P40 components.
This is independent of the implementation author within the same team/model,
not a fresh external validation of those reused components. The separate
caller/resource reviewer retains independent responsibility for its review.

## Physics and implementation checks

- Source lines49–62 implement the declared G under U[output,input], and
  R=G_even@G_odd (odd acts first). Creation operators give the normalized pair
  state cos(2theta)|11>+sin(2theta)(-exp(i phi)|20>+
  exp(-i phi)|02>)/sqrt(2). The tests check both complex amplitudes and
  rho[20,02]=-exp(2i phi)/2 at phi=.37, as well as 0/pi2. This detects a
  conjugated generic phase that probability-only HOM tests miss. Overlapping
  layers are not described as independent pairs.
- For V=ER, VV*=EE* and mu_i=sum_a|V_ia|^2 are invariant; q_ia=|V_ia|^2
  generally changes. Source lines254–280 build a fresh network and ALL
  marginal tables for each of the four V, rather than caching by P or mu.
  Source orthogonality, vacuum completion and rotation residuals are checked;
  projector/mu differences are recorded. Fixed ports0..r-1 contain one photon
  each and the complement is vacuum. Neither the anchor nor Cref constructs V.
- The inherited covariance diag(mu)+|P|^2-2qq^T is the CF bosonic covariance,
  including its diagonal. Its Gaussian factor/mask is recomputed after mixing.
  Exact empty or one-hot-one rows are masked, while mu=1 spread rows remain
  fluctuating. Source tests explicitly exercise a deterministic row becoming
  fluctuating after R. Effective variance is used for Gaussian CDF evaluation;
  variance-zero rows receive independent jitter. Residuals/row repairs remain
  floating diagnostics, not interval certification or a rigorous error budget.
- Inherited one-mode shifted-PGF coefficients are h!e_h(q_i) for B and e_h(q_i)
  for D; b4 convolves the corresponding bosonic group laws. The count sampler
  and tables use the SAME contiguous input-port groups of at most4. This is a
  genuine orthogonal-species control, not a global convex B/D mixture. Its
  grouping is architecture dependent and is not a proof that all collective
  interference is classically explained.
- Sphere uses a unit vector uniform on the complex source sphere followed by
  Multinomial(r,|Vz|^2). Right-unitary invariance makes its joint count law,
  marginals and randomized PIT invariant under R, so only Fourier/E are tuned.
  IID has no V parameter. D, phase, b4 and Gaussian are not generally invariant.
  Column phases AFTER V are CF-state nulls; a gauge BEFORE a fixed R can alter
  the state. The inherited carried-priority eigenvector pivot gauge is fixed
  before mixing, with occupied/internal and boundary gaps guarded. Relabeling
  carries marks and priority; a finite covariance fixture is provided.
- The local optical helper returns every full count vector, including
  collisions; no CF retry, threshold-only replacement, success conditioning,
  herald or loss-subset selection appears on this path. eta is fixed to1.
  PIT uses each model's own marginal and independent per-mode jitter before
  the common feasible decoder. This pilot therefore says nothing about an
  uncalibrated lossy device, detector feasibility or hardware latency.

## Controls, qualification and interpretation

The source family, four graph seeds, model order, policies and lambdas are
fixed. All four contexts and scored preparation candidates are completed and
shared before the first training sample; failures do not select a successful
subpopulation. Training selects by exact Fraction ALL-shot feasible-cut mean,
normalized per graph and averaged equally over graphs. Cref/gains/optima never
enter selection. Model-specific paid training incumbents do not refresh Cref
or the physical input. Fresh role-separated evaluation uses the selected
policy without reselection. These remain the same DEV graphs, not held-out.

The seven arms each receive128 training and128 fresh evaluation proposals;
the optical count is3840 simulated photons per arm. Sphere/IID avoid redundant
R tuning. Five legacy searches are separate paid controls, not a free portfolio.
FAST receives int64 input and inverse-order rank-per-vertex, the free common
incumbent, and CPU time granted from measured B classical WALL with optical
setup/count latency set to0. The caller uses deadline-eligible best_cut, not
overall_completed_best, and makes early cap/wall cases inconclusive. Timing
envelope details also receive the separate caller audit; no hardware break-even
claim follows from static inspection or one future timing run.

The42 planned preflight cases comprise27 primary fixtures and15 FAST cases.
I read all primary fixtures and previously reviewed FAST's15 fixtures; none
was run by me here. The two contracts close13 main artifacts and14 preflight
artifacts (the latter adds its own contract). Their CPU60/wall90/thread1 and
output32MiB limits are prospective runner obligations; arrays256MiB are a
projection, not a Darwin hard-memory guarantee. No automatic retry, survivor
positive or accepted positive is authorized. Require the actual preflight,
runner closure, all residual/failure outputs and independent caller review
before any main execution decision.

P/mu invariance, pair NOON preparation, a smaller raw quadratic proxy, B>D,
or an improvement on these four DEV graphs cannot establish advantage.
The frozen objective is decoded feasible mean; the previously derived raw
quadratic B/D common argmin does not settle that objective or its tails.

## Exact artifact closure

SHA256 values read directly from the target worktree:

| Artifact | SHA256 |
|---|---|
| research/P49_trained_source_probe.py | cdb0c72d935707965b0c3e28432a72812dc522fbc40e04fa842ac8ea8dbb8a93 |
| research/P49_trained_source_spec.json | 275bb9bcae40e0f4d7ba7ee8945c40435b617c89134f83e8e598ab7437387a42 |
| research/P49_trained_source_contract.md | df2f2bcaca44da25ad4966c863e299f49297794a588cbbd0c93ea1a9ee863a5d |
| research/P49_trained_source_execution_contract.json | 28f534d0ae5125d40fc62a42c5caf12bd76ca49859471a5ccb19d8d96d2f5a6f |
| research/P49_trained_source_preflight_contract.json | e6ee8cdd7dcbdc35fbcdd9004207a64d61c26ef3f3d3da39a9c10176875e0dd3 |
| tests/test_p49_trained_source.py | 0d97a6adaee9d7b4013a24fc0573a5fd3c3193dc12163aec3f73a4abd89e14c3 |
| research/P49_fast_classical.py | 018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff |
| tests/test_p49_fast_classical.py | 50bb0c50234934260ccd88cf065dd9752b959a7f447f81fda1a63c132f437621 |
| research/P48_spectral_pit_probe.py | b123bec4f67feb8ffc2255e0a56bc1181748a80bb716fe92328954a6f4d538ca |
| research/P48_coherent_marginals.py | a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac |
| research/P43_global_gain_probe.py | b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777 |
| research/P45_adaptive_probe.py | bb00ca61e45794ecea2333e0aa1864edfaec43128c1efa98dd8384c3d6889f92 |
| pyproject.toml | 7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4 |
| requirements-research-lock.txt | 3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1 |

Actual review commands were read-only git-show/diff/stat/rev-parse/status,
rg, complete sed/numbered source and test reads, cat of spec/contracts/card,
and shasum -a256. Algebra was reconstructed directly as above. No encoding
file, raw archive, paper or shared registry was changed. This new receipt
alone is written and committed in the isolated replication worktree.
