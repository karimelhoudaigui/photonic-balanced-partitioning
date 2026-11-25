# P49: actual feasible-mean training fails the declared hybrid control gate

2026-11-25. **REJECT the tested P49 hybrid pipeline on these four DEV graphs.**
Training a coherently mixed spectral source on the actual feasible-cut mean
does not produce a positive result against the strong controls. This is not
a universal obstruction to source mixing, lean B-only implementations or all
passive photonic optimization. No retrospective budget change, extra P49 run,
held-out claim, manuscript edit or QPU validation follows from this result.

## Frozen question, review and real execution

ROOT card dc85fa5 (initial7b791bf) fixes four bases, all-shot mean training,
independent model selection and fresh evaluation. Physics f898028 independently
reviews the source/gauge/HOM convention; the complex phi=.37 fixture fixes
coherence, not merely HOM probabilities. No graph/seed/policy was adjusted
after outcomes. Source927448a is preserved. The cost-only correction3d6a1f2,
identified BEFORE any P49 execution, separates necessary classical RNG/hash
setup from the optical simulation backend and charges it to FAST as well.
The scientific family, RNG streams, objective and allocations did not change.

Independent FAST source0bc492e has SHA256
`018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff`.
Its15-test qualification and prelaunch schema refusal/contract correction are
preserved; no FAST algorithm/test was rewritten by this implementation.
Combined targeted preflight: **42 PASS**,15.79s,14 unchanged inputs, validated
v2 manifest, committed **32615d1**. This is not by itself a full-suite claim.

The ONE main ran on CLEAN32615d1, source SHA256
`384057373739a90bbe6ec0f37726324b222ceeed2609bec57ae0dfebd700b7f5`.
Runner v2 **completed**, exit0, **24.299721s** wall; script CPU **9.583834s**,
wall **23.4010135s**. Enforced CPU60/wall90/thread1/log32MiB; no hard memory
or affinity promise. Directory **24,727,892 bytes**, below32MiB, with13 unchanged
inputs and all10 declared results present/regular. No truncation, retry or cap
increase. All4 graphs passed numerical guards, every arm completed128 paid
training+128 fresh evaluation proposals. No held-out graph, optimum/mask or
physical QPU call was used. The primary manifest validated against inputs.

Primary data: `experiments/P49_trained_source/run_001/data/`.
Raw SHA256:
`f890601b3237e329df883fddee8f8ca4a81ec9055d2539332ecfc11a736b6f26`.
Summary SHA256:
`61c96a19778294367c56c228c7c4a39da48a1bd8f525fc94381c1a0ace5e7103`.
All10 results and the separate read-only audit contract/source were committed
**9074386** before that audit. Actual argv, versions, seeds, limits and hashes
are in the primary manifest. Reproduction requires a NEW output directory.

## Selection really uses the feasible mean, then fresh shots

For each policy the selection objective is the exact Fraction mean of EVERY
cut/graph-total-weight, equally weighted across all4 graphs. Better and worse
shots remain in the loss. Cref, gain and success labels do not enter selection.
Global policy selection is frozen before any fresh evaluation shot; there is
no post-evaluation reoptimization. Source bases never load a training partition.

| Arm | Selected policy | Training normalized mean | Fresh evaluation normalized mean |
|---|---|---:|---:|
| B | E R(pi/4,0),lambda0 |0.319189889|0.327830358|
| D | Fourier,lambda1 |0.309947181|0.332946568|
| b4 contiguous ports | E R(pi/4,0),lambda1 |0.329272868|0.330770389|
| Gaussian_Bcov | E R(pi/4,0),lambda1 |0.316458473|0.329071878|
| Continuous phase | E,lambda1 |0.314394575|0.327847685|
| Spherical coherent | E,lambda1 |0.318050808|0.324040899|
| IID | lambda1, no source basis |0.332473978|0.333183434|

Exact fractions and all losing policy cells are retained. B's fresh mean is
better than D's, almost equal to continuous phase and worse than the spherical
control's. These are finite DEV observations, not a significance claim or an
independently replicated ranking. The drift from selected training means to
fresh means remains visible; no favorable policy/graph is substituted.

The nonredundant allocations were applied: eight policies x4 draws/graph for
B,D,b4,Gaussian,phase; four x8 for sphere; two x16 for IID. Each has32 training
draws/graph, then16+16 evaluation draws under two FRESH seeds at the fixed policy.
All128+128 costs count. Cref was frozen for every graph before the first train
shot. Training discoveries remain private paid incumbents, never gifts to
other models or changes to the optical family.

## Incumbents and actual photon-shot minima

Each cell below is **training incumbent / fresh-evaluation incumbent / total
paid deployment incumbent**, always initialized with the shared Cref.

| Arm | N26 ER4902601, Cref180 | N26 RR4902602, Cref56 | N34 ER4903401, Cref366 | N34 RR4903402, Cref72 |
|---|---|---|---|---|
| B |173/173/173|54/56/54|366/365/365|72/72/72|
| D |179/179/179|56/56/56|366/366/366|72/72/72|
| b4 |180/169/169|56/49/49|366/365/365|72/72/72|
| Gaussian |180/180/180|55/56/55|366/366/366|72/68/68|
| Continuous phase |173/158/158|56/49/49|363/366/363|72/71/71|
| Sphere |180/174/174|54/55/54|366/366/366|72/72/72|
| IID |158/180/158|56/56/56|366/366/366|72/72/72|

An incumbent initialized with Cref is not necessarily a photon-generated
partition. Actual B-shot minima distinguish that point:

| Graph | Cref | Raw B training minimum | Raw B fresh minimum | Paid B deployment | FAST admissible best |
|---|---:|---:|---:|---:|---:|
| N26 ER |180|173|173|173|158|
| N26 RR |56|54|57|54|49|
| N34 ER |366|366|365|365|359|
| N34 RR |72|76|73|72|63|

No B shot reached72 on the last graph:72 is the retained CLASSICAL frontend
incumbent. Paid training partitions may legitimately be retained, but their
full experimental spending remains charged and none becomes a prepared input.

## Strong classical controls and the precise cost veto

Each legacy control independently used its full6400/11072 informative-score
campaign budget per N26/N34 graph, split into two seeded half-budget runs.
These counts remain diagnostics, not CPU-equivalent prices.

| Graph | Paid B | Anneal | Spectral+swap | KL | Block matching | Coherent rounding |
|---|---:|---:|---:|---:|---:|---:|
| N26 ER |173|158|158|158|180|180|
| N26 RR |54|49|54|49|56|56|
| N34 ER |365|359|359|359|366|366|
| N34 RR |72|68|63|72|72|72|

One fixed annealing control already improves the paid B incumbent on every
graph at the declared informative ceiling. No free portfolio is needed.

FAST also strictly beats paid B on all4 graphs under its PREDECLARED envelope:

| Graph | Full granted CPU seconds | Admissible FAST best | Evaluated proposals | Stop |
|---|---:|---:|---:|---|
| N26 ER |0.139166801|158|136109|CPU deadline|
| N26 RR |0.131974850|49|132774|CPU deadline|
| N34 ER |0.286483924|359|394695|CPU deadline|
| N34 RR |0.274868350|63|335369|CPU deadline|

Only **best_cut/best_subset from the completed deadline-admissible prefix**
are used. No late overall-completed improvement is credited. No early proposal
cap or wall safeguard occurred; max100,000,000 was solely a guardrail. FAST
gets CPU seconds from B's measured classical WALL: shared bracketed compute,
classical constructor setup (total minus make_optical_sampler), per-shot
PIT/decoder/fitness and a quarter of global B selection. Backend/cold import,
optical count generation and raw/context/trace JSON contribute ZERO allowance.
This convention explicitly gives optical setup/sampling zero latency.

The independent scope review **d61b8c63ca9ff680960c374fff9ca72efb03c05e**,
preserved locally in `research/P49_review_cost_veto_scope.md`, is essential:
the expensive common searches/Cref, comparator PMFs/Gaussian factorization
and some numerical diagnostics are NOT all dependencies of a lean B-only
policy. The full shared-wall grant therefore measures THIS research hybrid
pipeline, not a lower bound on every possible B-only implementation. FAST
also starts from the shared Cref, which was computed and supplied free.
Removing frontend work would remove that gift too. No smaller retrospective
budget or new initialization is applied to rescue or strengthen the verdict.

That review checks first strictly better completed FAST checkpoints at
0.723,0.709,2.674,1.630ms solver CPU, using balanced masks and reconstructed
cuts. These are descriptive observed prefixes from Cref, not from-scratch
certificates, new registered budgets, timing confidence intervals or hardware
latency bounds. Thus the honest conclusion is: **the declared P49 hybrid
campaign fails its cost/control gate even under zero optical latency.** It
does not prove impossibility of every source-mode mixing or optimized lean
implementation. A distinct candidate needs a NEW prospective cost closure,
paid initialization, confirmation/replication and hardware gates.

## Physical validity, resources and data reconstruction

Every source rotation preserves P/mu numerically while changing q-dependent
laws; all four bases recalculate PMFs, covariance, factor and deterministic
mask. b4 input groups remain contiguous. Production phase coefficients are
continuous; sphere/IID do not tune redundant circuit labels. Minimum guarded
spectral gaps were0.00943966483,0.00829756688,0.00470935852,0.00512257189.
Independent unitary residuals were<=2.23e-15. No row-mass repair was needed on
actual contexts. None of these valid physical invariants demonstrates a gain.

B,D,b4 each used3840 injected SIMULATED photons (1920/stage), zero physical
QPU shots. Collision-containing samples were B255,D251,b4=255,phase256,sphere255,
all retained. Primary informative cost is64 decoded proposals/graph,100/173
units each. Setup/count generation and classical setup/PIT/decoder/selection
wall+CPU are saved separately. Setup subcomponents are not added twice. The
experimental and selected-policy evaluation/setup ledgers remain separate;
selected setup bounds are not minimal optimized or physical QPU prices.

The ONE additional computation was a separately frozen, bounded, stdlib-only
READ-ONLY consistency audit, not new sampling. Its v2 manifest completed and
validated with14 unchanged inputs; all10 primary hashes matched before/after.
Internal wall **3.559903s**. Evidence:
`research/P49_trained_source_raw_audit/run_001/manifest.json` and
`research/P49_trained_source_raw_audit/run_001/data/receipt.json`.
It independently checked:

- ALL184,326 raw feasible cuts (93,595 distinct cached subsets),1792 primary
  decoders and168 common decoders;
- 1280 count-PIT/256 Gaussian-PIT fields,528 direct preparation candidates,
  128 signed roundings and174,720 legacy queries;
- ALL-shot/equal-graph Fraction losses, canonical selections, complete model
  grids, fresh namespaces/fixed evaluation policies and private paid incumbents;
- classical setup/FAST allowance and every one of14,207 FAST clock/cut/mask
  checkpoints, including prefix eligibility and uncredited late results;
- source-port/first-column equality, independent E R product, marked eigen
  residuals, unitaries/projectors/covariances, subunit PMFs and saved repairs.

This verifies consistency of implemented finite evidence, not independent
distribution replication, a statistical positive, an interval theorem or an
optimized hardware cost. All raw data remain unchanged. P49 is archived as
a failed declared hybrid pipeline, with its limited B>D mean contrast retained
and fully explained as insufficient for the program's positive gate.
