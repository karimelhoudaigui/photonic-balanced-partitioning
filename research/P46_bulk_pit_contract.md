# P46: bulk transfer and standardized marginal geometry — DEV veto

Owner encoding, 2026-11-25. This preregistration fixes one experiment before
opening its outcomes. It is a new mechanism discriminator, not a positive
optimization result, novelty claim, held-out test or hardware gate. The paper
and all historical evidence, including negative P45, remain unchanged.

## Question, hypothesis and physical architecture

Does a graph-programmed, extensive bosonic transfer kernel produce useful
correlations for balanced partitioning after every scalar count marginal is
standardized, relative to independently selected distinguishable photons,
bounded species, a matched transfer/phase control and strong feasible search?
The hypothesis concerns the joint law passed to a nonlinear decoder; a change
in collision rate, covariance, photon transport or mean cut does not establish
it. Earlier P45-A motivation reported B aligned gain0, B permuted gain74,
IID gain73, Gaussian gain37; these are development observations, not a causal
PIT test or independently replicated evidence.

There are K source single photons in K anchor modes and K empty modes.
For fixed p in{1/4,1/2}, zeta in{0,1/4}, define

    H = [[0,W],[W*,0]], U = sqrt(1-p) I - i sqrt(p) H,
    Delta[i_inside,j_outside] = ell[j]-ell[i]+2 A[i,j],
    J = I-11*/K, R=J Delta J, F[i,j]=exp(2pi i i j/K)/sqrt(K),
    W = polar(F+i zeta R/||R||op), or F if ||R||op<=1e-12.

The block order is the declared inside order followed by the outside order.
**Delta uses inside rows and outside columns**, the transpose of the convention
in the independent physics note. Consequently old-to-new transfer is W*;
the code, PIT and conditional phase all use that same orientation. This is a
defined graph map, with no optimization by orientation after outcomes.
The physical number transferred is exactly Binomial(K,p), including zero
and all K. The polar input has singular value at least1-zeta. The numerical
implementation is complex128/float64, checked for unitary residual3e-12;
it is not an exact rational implementation or certified rounding proof.
All graph features are optimum-blind. R=0, weak response and awkward graph
orders are retained. Recorded stable rank, ||W-F||F^2, I4 and quartets are
diagnostics only. No graph is selected by these values.

## Common frontend and information budget

Four NEW development graphs, n24/28, weighted ER(p=.35)/RR(degree4), have
exact seeds/families in the JSON spec. Integer weights1..9 use immutable P43
generation. A shared random initial partition receives up to8 full strict
best-swap scans; the cap is not called a local-minimum certificate unless a
complete no-improvement scan occurs. Every evaluated cut is retained.
Fixed role-separated random orders inside/outside, vertex tie priority and
species assignment precede outcomes. All K^2 actual swap cuts from final S0
are scored, logged and credited, including any improvement. The physical
source remains S0, without secretly rerunning the frontend after a discovery.

Every network, one-mode PMF, phase calibration and matrix decomposition is
computed in the common frontend and available to classical methods. It is
charged ONCE there, not charged again to each model's online time. Common
decoder-only discoveries are shared: zero field with q=ceil(K/2), pure greedy
q=0, plus the fixed all-zero-count midpoint PIT for each discrete model,
network and lambda. Every inspected cut marginal and final cut is charged.
The reference Cref is the minimum of ALL cuts actually scored in this
frontend, not merely C(S0). No optimal value, optimal masks, optimal partition
or exact solver is used. The saved context includes every adjacency, Delta,
network, numerical PMF, phase histogram, seed and resource ledger.

The greedy decoder is immutable P45-A complete(a,u-.5,K,lambda,priority,q),
q=ceil(K/2), lambda in{0,1}. It first seeds the q highest fields, then greedily
adds vertices using exact cut marginals plus its declared field bias.
This q differs from the q=K illustrative case in the physics note and is
shared without alteration by all six primary models. One proposal costs94
score units at n24 or127 at n28 (each inspected marginal plus the final cut).
It always returns a feasible K-subset. Completion can fill unclicked modes;
the click-contained P44 no-go does not apply. No postselection or resampling
of optical observations occurs. Raw collisions and all outcomes are kept.

## Six primary controls, randomization and PIT qualification

For B, D and independently assigned species chunks of at most4 photons,
the true theoretical unconditional one-mode generating functions are

    B: sum_r r! e_r(|U[i,source]|^2)(z-1)^r;
    D: sum_r    e_r(|U[i,source]|^2)(z-1)^r;
    b4: convolution of the per-species B PMFs.

Coefficients use80-digit Decimal arithmetic applied to numerical one-particle
probabilities, then float output with explicit checks/minimal rounding clip.
This avoids an unqualified float inversion; it is still numerical PMF
evaluation, not exact arithmetic/interval certification. Old-mode tables are
replaced by the exact specified Bernoulli(1-p) PMF for all count controls.
The absolute coefficient bound for new modes at p<=1/2 is favorable; it is
not a relative guarantee for tiny tails. Preflight compares independent
small-Fock permanent enumeration and labeled-particle enumeration.

Each count vector uses u_i=F_i(n_i-1)+xi_i PMF_i(n_i), with independently
seeded uniform jitters per mode and shot, independent from physical/field
sampling. With true PMFs the marginals are exactly uniform; the production
numerical tables give that statement only up to their unbounded numerical
error. This is the randomized/checkerboard convention for discrete copulas.
It need not match bivariate laws, preserve raw covariance or ensure uniform
top-q seeds except under IID. Gaussian_Bcov uses the exact stated raw B
covariance then Phi(raw/std), using the ACTUAL factor variance sum_j factor_ij^2
after clipping tiny negative eigensystem roundoff, with independent uniform
jitter at exactly zero variance. Target variance and covariance residuals are
saved separately. It does not match the photonic PIT bivariate copula. IID uses
independent exact uniform fields. Beating either alone is insufficient.

The required strong conditional_phase control samples independent Bernoulli(p)
transferred input set T, preserves old counts exactly1-1_T and, conditional
on T, uses four-root random phases followed by a |T|-photon multinomial in
the new block. It preserves old patterns, total photons and transfer sectors.
Zero transferred photons means old all1/new all0, not physical eta=0 vacuum.
For EACH network its GLOBAL UNCONDITIONAL one-mode law (averaging T) is
calibrated by4096 separate classical draws, never a T-conditional CDF or a
production-batch empirical rank. All histograms are saved. Old-mode PMFs
are analytic; only new-mode PMFs are estimated. Calibration and production
have distinct namespaces. No global phase-multinomial model is used; the
more structured conditional control replaced it before outcomes.

For d=K+1 categories, a union of one-sided Hoeffding bounds over2^d subsets
gives Pr(TV(p,p_hat)>epsilon)<=2^d exp(-2 M epsilon^2). The saved per-mode
TV radius uses this expression, separately from the saved DKW CDF radius.
Per-mode failure .05/(16*14) provides an at-most.05 union bound across all
new-mode calibration histograms; no independence across modes is assumed.
The exact one-mode uniformity error under an estimated PIT is TV(p,p_hat).
No joint-copula error is certified, and this calibration tolerance remains
a limitation that could matter to any apparent B/phase difference.

## Finite population, tuning and costs

For each of4 graphs,2 trial seeds,4 network settings,2 decoder lambdas and4
draws give64 proposals per model/graph, **256 per model** total. All six
models see the same candidate settings and equal decoded-proposal and graph
score budgets. Each independently selects the largest pooled DEVELOPMENT
gain max(0,Cref-C), with fixed setting-index tie break; no held-out claim is
made about that selected setting. If every gain is zero selection is null.
This is a veto pilot, not enough samples for acceptance or tail estimation.
Selection for Gaussian/IID may contain duplicate network laws; they retain
the same exploration effort rather than using saved effort for hidden tuning.
B,D,b4 are physically sampled via unchanged P43 serial Clifford2017/local
exqalibur helper; there is no full-Fock enumeration or remote processor in
the pilot. D law itself is sampled by independent categorical particles.

Independent strong baselines anneal, spectral_swap, KL_collective and
block_matching each receive32*94=3008 or32*127=4064 actual cut queries per
graph/trial. Matching starts from S0 and alternates Bernoulli.25/.5 removed
inside subsets; a rectangular Hungarian assignment on SHARED Delta chooses
distinct outside vertices, then the REAL simultaneous cut is scored once.
Empty and all-transferred subsets are retained. It is not claimed that summed
single-swap deltas equal a collective move cost. All solve time is charged.
Other baselines start at common best Cref. Their already known initial cuts
are not counted again. No graph-query-free search discoveries are hidden.
Every score is logged; partial matching/spectral calculations are allowed to
use the same graph/matrix data as the photonic arm. No classical optimum oracle.

Report separately total shared preprocessing, physical simulated attempts,
injected photons K per B/D/b4 attempt, classical field samples, phase
calibration draws, partial-marginal scores and final-cut scores, setup,
sampling/PIT, decoder, total observed online wall and all baseline queries.
Phase calibration uses65536 classical raw draws across16 networks, zero QPU
shots; every graph's four4096-draw histograms are shared setup costs.
Each classical prefix is also compared with each model's actually observed
online wall time AND score cap, using per-query elapsed timestamps. These
are offline observed timings, not predictions of hardware latency or a fair
future QPU throughput comparison. No total-runtime advantage can be inferred
from a single noisy timing. Report each baseline separately; choosing their
best after outcomes would require its own shared tuning/resource account.
Loss eta1 is exploratory. Any subsequent hardware gate MUST account for
source preparation, loss, detections and physical attempts without using PIT
to relabel a classical decoder improvement as an optical optimization benefit.

## Outcomes, freeze and bounded execution

All code/spec/contracts/tests must be committed before the first scientific
execution. Root reviews the frozen commit; the independent reviewer receives
the same SHA. The sole numerical slot is required even for targeted tests.
Then run the declared preflight and, only if it passes, one unique bounded
pilot. No automatic retry, graph substitution, outcome-based filter or file
overwrite. Planned arrays<=256MiB, one numerical thread,60CPU/90wall seconds,
new outputs32MiB. The runner enforces CPU/wall/log caps; array budget is a
declared design bound, not a Darwin RLIMIT_AS promise. Failure/timeout is
resource or implementation inconclusive and every partial artifact is retained.

Possible decisions: REJECT this family/budget if strong controls reproduce or
beat it; FOLLOW-UP only if a mechanism-specific signal survives all listed
comparisons; INCONCLUSIVE for resource/calibration/implementation limitations.
**No positive result, held-out validation, novelty, quantum advantage or QPU
readiness can be accepted by this pilot.** Any interesting result requires
fresh graph/seed/relabeling, separately optimized controls, calibration checks,
independent replication and full total-cost auditing before a hardware gate.

Sources: immutable P45-A source from c20193b and19a9902; unchanged P43 sampler.
Independent physics note a6d7a278654099ac970b2defb0e06c0896fd6a02,
SHA2563e84a34cf9a788f7346d3c1d5531bd4bb303fb1c9d092494418fb06af845b998;
independent adaptive reconstruction ed5b1e5 preceded reading that derivation.
These are internal proof reviews, not external priority evidence. Novelty of
the combined optimization mechanism remains OPEN.
