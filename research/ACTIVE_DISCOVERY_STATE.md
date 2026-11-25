# Active discovery state — P41 to P44

Current25-Nov continuation: [P45_LIVE_STATE.md](P45_LIVE_STATE.md).
The user's newest target requires a POSITIVE result; the P44 scoped theorem
below is not a stopping criterion. Two genuinely changed P45 pilots have run
and remain negative against strong controls. P46 is a new unexecuted
hollow-transfer/copula mechanism, not an unchanged larger sweep. The preserved
24-Nov checkpoint follows; paper and QPU gates remain closed.

Date:24-Nov-2026. Original validated release:2744395. Integration branch:
research/p41-discovery. This is the live entry point; historical contracts,
proofs, raw files and receipts retain their original status at their source.

**Positive optimum-blind optimizer: OPEN. Scoped mathematical obstruction:
PROVED. QPU_GATE:CLOSED. Manuscript:unchanged.**

The user permits either a genuine interference-dependent optimization result
or a substantial obstruction for the current approach class. P44 supplies the
latter in an explicitly bounded transmission/cost regime; it does not settle
all ideal optical algorithms. The general discovery target remains open outside
that regime. Complete-composition novelty is an independent unresolved question.

## Current strongest result

For one photon per occupied spatial input, fully identical photons and a passive
vacuum-environment transmission T, set eta0>=||T[:,occupied]||_op^2. For every
specified k-set S of detector modes,

    Pr(all S modes click) <= E product_(i in S)n_i <= eta0^k.

The proof includes collisions, every lost-photon sector, nonuniform attenuation
and arbitrary graph/prior-history-dependent passive controllers. It covers any
single-candidate decoder whose chosen vertices all actually clicked, even if
additional modes clicked or external outputs were not observed. Filling
unclicked vertices classically is outside this implication. No postselection
renormalization, quantum memory, false clicks or same-attempt heralded control
is included. See [the complete P44 proof](../theory/P44_nonuniform_loss_moment_obstruction.md).

For m=2k let D=binom(2k,k), nQ be a guaranteed optical-attempt upper bound,
nC>0 a guaranteed classical-draw lower bound, and L=ceil(nQ/nC). If

    L D eta0^k <=1,

uniform feasible search stochastically dominates the best newly measured cut,
including arbitrary allowed adaptation. A shared classical incumbent and all
additional classical discoveries/costs must receive their proper credit. Equal
proposal counts satisfy the criterion for every k when eta0<=1/4. These are
physical proposal counts, not a claim that scoring, photons and wall time are
interchangeable. Guaranteed costs and score ceilings must instantiate nQ/nC.

Unknown internal states require the separate conservative k!*eta0^k bound,
assuming the same T acts on all internal degrees. A retained physical DFT6
counterexample forbids blindly reusing eta0^k. The eta0 required here is a
SPECTRAL transmission upper bound; a public mean or maximum single-column
transmission is insufficient. No value has been inferred for Lucy.

Root proof b87e677 has SHA256
5407871a6afe5f6d7eb478792c88b73c964918bd593dbd19ef6d56e82204730b.
Physics reconstructed it BEFORE reading the author argument, frozen2d15012;
the subsequent [exact-hash review](P44_AUTHOR_PROOF_REVIEW.md) says proved as
written. Encoding separately checked the permanent/thermal ingredients and
their [primary-source attribution](P44_encoding_sources.md). These ingredients
are established; their composed optimization application is not certified
globally novel by a bounded search. A separate frozen numerical dilation run
has completed:190 configurations and1240 support checks pass the declared
1e-10 tolerance; maximum residual1.333e-15. It includes nonuniform loss, vacuum,
all environment occupations, complex product internals and correlated internal
fixtures. [Its manifest](../experiments/P44_replication/run_001/manifest.json)
pins the4-file closure at source0687912. These finite float checks support
implementation consistency; the general theorem rests on the audited proof.
The [full execution receipt](P44_replication_report.md) records the actual
command, normalization/complex-phase checks, resource observations and hashes.

## Route ledger

| Route | Evidence and disposition | Changed bottleneck before any further run |
|---|---|---|
| P41 weak-angle chiral proposal |72 declared cells; classical positive proxy reproduces the leading interference current. No optimizer advantage. General proxy proof still lacks a fresh complete exact-hash audit. |Finite-angle effects or a different global observable, with the proxy as a control. Do not repeat the same pilot.|
| P41 grouped feasible encoding |Classical random-wave grouped domination independently proved;1260 Fock outcomes and Perceval comparisons. Core phase-twirl ingredients known. |A genuinely changed decoder/encoding; do not assume all-CF normalization or divergent adaptive-history domination.|
| P41/P43 local L1 mean |Connected counterexample breaks the old quadratic ordering, but the unconditional local L1 mean has a known polynomial marginal oracle. Corrected exact/additive proof independently reviewed, with representation/scale caveats. |A global/tail observable or changed physical operations; a lower mean alone is insufficient.|
| P43 finite-angle graph echo |New global-incumbent-gain pilot:896 B attempts,373 CF,523 collisions,zero improvements. D/phase-field/b4 also zero. Strong classical controls improve both20-mode graph anchors. Full raw reconstruction agrees. |REJECT at this family/budget. No unchanged sweep, held-out fishing, positive replication or hardware circuit.|
| P42 uniform-loss spectrum |Exact cap and general block-trace variant independently proved and numerically checked by two different representations. |P44 removes uniform loss for CF sources; original P42 tables/PNR/source-specific refinements remain valid.|
| P44 general passive-loss moment |Root proof independently reconstructed and reviewed; source attribution explicit. Stronger direct-click adaptive cost obstruction. |Calibrated spectral/cost assumptions are needed for a device verdict. Arbitrary completion/high-transmission/richer-resource approaches are not ruled out.|

The negative P43 screen is [fully documented](P43_global_gain_result.md), including
its8 predeclared settings, four unique graphs, fixed charged anchors, separately
selected controls, score budgets and actual samples. All-zero selection cancels
the128 possible optical relabel draws, so optical fresh-seed/covariance checks
are N/A, not passed probes. The5 classical controls did run their probes. No
held-out graph, C*, optimum mask or known optimal partition entered training.

## Verified checkpoint and continuation rules

529 existing/new tests passed before the P43 run, including a generic3-photon
Clifford2017-vs-independent-Fock sampling check. P43 completed under real
CPU60/wall90/thread1 limits and its manifest validates. The602 historical
scientific files and the entire paper/ snapshot remain unchanged. P33/P37/E05b
retain their validated evidence and limitations. Original worker Git refs must
be preserved together with integration commits, because manifests cite the
pre-run source revisions, not their cherry-picked copies.
The [final verification receipt](../reports/P44_validation/verification.json)
confirms archive/publication/manifest integrity and that production, tests and
P43 implementation are unchanged since the full529-test run. New P44 code has
its separately frozen, completed validation; no unrecorded physics rerun occurs.

No new paper, new hardware preparation, message to Laurent or QPU job is
authorized by these negative/model results. Under the newest user gate a
positive optimizer requires frozen held-out tests, independently reoptimized D,
strong feasible controls, fresh seeds/labels, independent physical replication
and full resource accounting before the hardware stage.

Future research may examine high-transmission global mechanisms or a changed
decoder that uses partial detections with credited classical completion. That
is an OPEN route, not a positive algorithm or a hardware capability claim.
Nonlinear/heralded proposals need a genuine physical/resource specification;
terminal sample postprocessing does not implement nonlinear quantum dynamics.
Do not close the unrestricted discovery target merely by renaming these scoped
theorems as a universal no-go.
