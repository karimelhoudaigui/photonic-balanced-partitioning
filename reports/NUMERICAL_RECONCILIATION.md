# Numerical reconciliation — 2026-11-24

**Decision: retain the validated ideal-simulation results and remove the blanket superiority claims introduced by cf49741/6154b46.** Reconstructing every E05b run confirms that the distinguishable control has a larger mean final success probability than the bosonic model at n=4,6,8. Every one of the 756 runs already encountered an optimum during training. The classical uniform feasible baseline discovers optima earlier on the reported retrospective first-hit metric. These archives establish neither quantum advantage nor a completed hardware experiment.

The canonical publication data are **only** `results/validated/recovery_2026-11-24/summary.json`, `benchmark.csv`, `campaigns.json` and `source_hashes.json`. The portable generator is `scripts/reconcile_experiments.py`. A preliminary successful capture is retained under `results/validated/_recovery_2026-11-24_preliminary/` with its executed script snapshot and relocation map; it is not a second publication source. The second reconciliation added complete raw-case metadata and row locators for alleged gains, without rerunning any historical experiment.

Scope: worktree `recovery-numeric-20261124`, base `6154b460e1c8b37cf2a7023fcbfff35d31a7220c`. Original experiments/results were accessed read-only through `--archive-root`. No old driver, optimizer, simulator campaign, QPU, paid model, installation or message submission was executed. No paper or shared registry was written. Mathbox computation-audit guided the contract, observed-input hashes and bounded provenance record.

## E05b: complete raw reconstruction

The data form exactly the declared grid: n=4,6,8; six families; two nominal graph-instance slots per family; three optimizer repeats; seven methods, with penalty lambdas 0.1,1,10 treated separately. There are **756 distinct run keys**, **90,720 objective batches**, 30,720 training draws and 4,096 heldout draws per run, and **26,320,896 total simulated draws**. All count vectors, evaluation indices, aggregate counts, selected parameters, losses, cumulative best-valid costs and heldout Wilson intervals pass reconstruction.

Each nominal n/method group has 36 runs. Its point estimate preserves the original nominal-grid weighting, rather than selecting a favorable graph, seed or penalty lambda.

| Method | n=4 final mean success | n=6 | n=8 |
|---|---:|---:|---:|
| Bosonic | 0.6523129783 | 0.2795490911 | 0.0678727604 |
| Distinguishable, independently trained | 0.7132846817 | 0.5366140370 | 0.1377071293 |
| Classical iid multinomial | 0.4206245980 | 0.1099581352 | 0.0259655922 |
| Product-Bernoulli penalty, lambda0.1 | 0.1990297521 | 0.0567189782 | 0.0165171810 |
| Product-Bernoulli penalty, lambda1 | 0.2027729022 | 0.0560989080 | 0.0162610498 |
| Product-Bernoulli penalty, lambda10 | 0.1988574864 | 0.0561352960 | 0.0166559725 |
| Uniform feasible classical | 0.5277777778 | 0.1750000000 | 0.0595238095 |

These are exact probabilities of the selected ideal simulated distribution, after finite-shot training; heldout sample rates and their per-run Wilson intervals are separate fields. Bosonic final probabilities exceed this particular product penalty control in this grid, but that does not imply superiority to serious classical search, distinguishable photons, or a genuine optical ObliQ implementation.

| n | Nominal graph slots per method | Unique labeled weighted graphs | Bosonic descriptive interval | Distinguishable descriptive interval |
|---:|---:|---:|---|---|
| 4 | 12 | 9 | [0.4637583,0.8038930] | [0.5900623,0.8348538] |
| 6 | 12 | 9 | [0.1783044,0.4225103] | [0.3888968,0.6464171] |
| 8 | 12 | 10 | [0.0331228,0.1070821] | [0.0753155,0.1972667] |

A graph cluster is the SHA256 of n and the sorted undirected weighted edge list, preserving exact encoded weights and vertex labels. Path/cycle duplicates and equal regular graphs are retained, but never counted as new independent graphs. Unique graphs by family are `(1,1,1,2,2,2)` at n=4 and n=6 and `(1,1,2,2,2,2)` at n=8, in path/cycle/regular/ER/weighted/planted order. All 36 nominal graph slots and their actual edges are in `summary.e05b.graphs`; none is filtered out.

Uncertainty uses 2,000 deterministic graph-cluster bootstrap replicates. For cluster g, keep every associated optimizer repeat together, with sum t_g and record count n_g. Resample G whole graph clusters and compute `sum(t_g)/sum(n_g)`. Repeating optimizer seeds cannot increase G. Thus the original nominal mean is retained while intervals respect duplicate graph clusters. These are **descriptive percentile intervals**, not validated population 95% confidence intervals: graph families are fixed, only two nominal instances were generated per family, and generator seeds are reused across families. They are marginal, not simultaneous. No broad significance claim follows from whether an interval crosses zero.

### Discovery and reciprocal metrics

All 756 runs find an optimum in their training counts, before the heldout stream. The best-found metric is reconstructed directly from every nonzero sampled feasible category. Counts identify the **first winning batch**, not the order of individual draws inside it. The archived first-shot index is checked to lie in that earliest winning batch and to remain unchanged afterward. It is not independently reconstructed from aggregate counts; per-shot sequences were not retained. `benchmark.csv` keeps both `first_training_success_batch` and that explicit validation limit.

| Method | Archived median first attempt n4 | n6 | n8 |
|---|---:|---:|---:|
| Bosonic | 2 | 15.5 | 89 |
| Distinguishable | 2 | 11 | 27 |
| Multinomial | 2 | 6 | 43 |
| Each penalty lambda | 7 | 7.5 | 38 |
| Uniform feasible | 1 | 4 | 17.5 |

These are retrospective diagnostics using C*, not an oracle-free stopping rule or measured wall-clock time. Training does not stop after finding an optimum. The post-training expectation `1/p_success` answers a different question. At n=8, averaging per-run reciprocals gives about 806.014 bosonic,59.614 distinguishable and23.576 uniform draws, whereas reciprocals of the pooled means give14.733,7.262,16.8. Neither quantity replaces the cost of training/discovery, nor can one be substituted for the other.

### Anti-oracle and budget audit

The pinned historical E05b driver is `experiments/run_equal_budget.py`, captured at `af0978455258bb44ef51d328e9ac977546eb2331`. Its training value is fixed before retrospective hits are computed. Photonic/iid loss uses observed conditional cut plus `2*(1-observed feasible rate)`; zero-feasible batches use the declared fixed fallback. The penalty uses sampled full binary QUBO costs. Every stored loss agrees with independent cost/count reconstruction. Parameters minimize the observed loss, without selecting on the success diagnostic. Fixed-budget completion and fallback proposals do not depend on C*. The heldout RNG has its separate declared seed stream.

An exact optimum is nevertheless enumerated during simulation setup and used for retrospective success labels; that reference calculation must not be portrayed as free practical optimization. Cost tables, probability enumeration, circuit construction, parameter dimension, setup time and scoring work are additional resources. The recorded 34,816 score lookups are logical draw-index lookups, not a measured count of independent black-box graph oracle evaluations. Collisions consume draws; conditioning does not remove them from the budget. Physical emission/detection losses are omitted.

The graph optimized is also the graph evaluated. Heldout means independent draws from the selected circuit, not unseen test graphs. Each lambda consumes its own full training allocation. Pooling a winning lambda without charging its search, calling product Bernoulli genuine optical ObliQ, equating equal draw counts with equal classical time, or claiming generalization would be unsupported.

## Haar table reconstructed from raw.csv

There are 3,250 Haar circuits: 1,000 each at n=4,6,8 and250 at n=10. Circuit seeds are unique within each size. The intervals below are Student-t intervals across independent generated Haar circuits, not hardware-shot intervals.

| n | k | Circuits | Mean P_CF | Circuit interval | Known exact ensemble expectation |
|---:|---:|---:|---:|---|---|
| 4 | 2 | 1000 | 0.5984963892 | [0.5893478142,0.6076449643] | 6/10 |
| 6 | 3 | 1000 | 0.3584474515 | [0.3540705371,0.3628243660] | 20/56 |
| 8 | 4 | 1000 | 0.2121182708 | [0.2101532420,0.2140832996] | 70/330 |
| 10 | 5 | 250 | 0.1258819853 | [0.1239403218,0.1278236489] | 252/2002 |

The corresponding path optimum-success means are0.205198471,0.034878205,0.005888123,0.000976685. P_CF is not optimum-success probability. Haar ensemble decay does not constrain an individual trained circuit or prove solver speedup. There is no empirical n=12 Haar point in E01; a clearly labeled theoretical value is a different kind of evidence.

## Campaign census and provenance limits

`campaigns.json` inventories **50 manifests**, including reviews/continuations rather than pretending they are 50 independent experiments. It records status, resource limits, counts/summary metadata, raw metadata, output hashes, source status and relocation resolution. There are43 completed captures with verified output hashes, two completed captures with a source-snapshot gap, three preserved failed captures and two excluded root P33 records. Of270 distinct recorded input pins,197 match the Git blob at their recorded commit,70 match an available pinned snapshot only, and three remain unresolved. The failed captures are E06, the first P33 float-review attempt and the first P36 linear-grid attempt.

A current source change does not invalidate a historical capture if its historical Git blob matches the pin. Dirty/untracked source captures are identified separately. The unresolved pins are the earlier P34 theory note at03b92ea7, the interrupted P36 analytic check atde77a140, and pyproject.toml in the excluded root P33 capture at77a85882. The corrected P34 continuation remains a separate capture. The P36 interruption is preserved evidence of an attempt, not a successful universal theorem.

Copied archives are resolved by pinned content hashes, including supervised P33 captures whose original path labels name the root directory. They are not silently compared to a different newer root file. **Root `results/P33_density_primary` and `P33_density_replication` remain excluded**: later Git addition of raw/summary files does not supply the missing original declared result hashes. Only the preserved supervised primary/replication captures have their own usable result provenance; their scientific acceptance still says pending proof/novelty review.

The following census describes recorded finite assertions. Except for E05b arithmetic and Haar reaggregation, it is a metadata/output-integrity audit, not a new proof or rerun of each scientific assertion.

| Campaign | Retained amount/status | Interpretation limit |
|---|---|---|
| E01 | 3250 Haar circuits | Ensemble calibration, not optimized performance |
| E02 | 648 runs, all success-oracle training | State-preparation diagnostic; no blind solver evidence |
| E03 | 324 runs, n4 only;108 oracle-objective runs | No n8 objective-comparison evidence |
| E04 | 288 oracle runs, n4/6 | Exact objective-call budgets, not hardware superiority |
| E05 | 756 older runs | Superseded equal-cost protocol: early stopping and analytic uniform control |
| E05b | 756 runs, all reconstructed | Equal ideal draws; costs/limitations above |
| E06/E06b | Original failure;120 Haar +4 disjoint controls after correction | Preserve failure and corrected capture separately |
| E07 | 432 spectral-hybrid runs;216 oracle objectives | Classical anchor cost/quality must be charged |
| E08 | 240 interpolation cases +9 counterexample cases | Finite TV checks and rational controls, not novelty certification |
| E09 | 240 oracle label-control runs | Reachability/label diagnostic, not optimization advantage |
| P20 | Initial1152 and continuation1920 test blocks;64 synthetic attempts/method/block | Selected product kernels; fixed-anchor tests, no executed adaptive optimizer |
| P21 | 2880 runs;345600 scored search partitions;61056 reference evaluations | Serious optimum-blind classical controls; query budget differs from photon draws |
| P30 | 10 coincidence +48 convergence cases | Static optical component and source convention checks, not VQC optimization |
| P31 | 972 unitary +36 full-Fock +36 limiting-gap cases | Bounded washout checks and preserved counterexample |
| P32 | 19 lossless maxima and50 operational cells plus exact controls | Criteria-specific Haar/loss calculation; no optimization advantage |
| P33 | Supervised primary/replication:150 full +36 certificate-only +7 sharpness +6 dilute cases each | Root copies excluded; proof/novelty acceptance remains separate |
| P34 | Exact three-step adaptive controls and independent review | Conditional transcript bounds, not measured search superiority |
| P35 | 12 marginal circuits, six exact physical;190 independent marginal comparisons | Known ideal-objective baseline, distinct-input scope |
| P36 | 256-case grid;17856 adversarial evaluations; failures/analytic attempt preserved | No certified general linear-bound refutation; no proof from absence |
| P37 | 112 cells,1610 probability crosschecks,36 transition brackets | Exact finite loss/source calculations; no hardware loss measurements |
| P38 physical | 36 circuits,5 controls,6 Perceval checks | No certified linear pinched-bound counterexample in this finite population |
| P38 effect relaxation | 2076 initial +8714 refinement calls;four cells;zero solver-success flags | PSD-effect search is a relaxation; not automatically a physical row-region population |
| P39 | Exact rational witness,9 modes/3 photons;165 Fock outcomes | Refutes the curved pinched envelope, not the linear TV conjecture |

For P39, delta=18/25 and the curved envelope is288/625=0.4608. The exact rational Rayleigh lower bound exceeds that curved value; displayed pinched distance is0.4901082883 and fine TV0.2651530737, both below delta0.72. Calling this a refutation of linear `TV<=delta` or `D_pinched<=delta` would change the claim being tested.

## Unsupported checkpoint values and trace locators

The valid Haar means in cf49741 survive reconciliation. The performance narrative does not:

- The n6/path value0.982 matches rounding of **one** E02 oracle run: `runs.jsonl` line235, instance1, seed20862120, selected evaluation119, probability0.9818491204585299. It is not a mean or an E05b result. The six E02 oracle path runs average0.8835615746.
- The claimed n8/path0.537 has no matching selected E02 path run at the stated three-decimal precision. Their six-run mean is0.2699443076; the nearest selected value is0.5326972539. It remains unsupported as reported.
- n10/path0.112 and n12/path0.034, their penalty ratios and bosonic ratio4.81 at n12 are outside the recorded E02/E05b domains. No supporting extension campaign was identified.
- The reported “E05b200 evaluations,1.1x–10x superiority” contradicts the actual120-call protocol and omits the stronger distinguishable/uniform/classical controls. Ratios to a weak penalty model are not general encoder or solver advantage.
- The n8/path objective table is outside E03's n4 domain. Selecting the best probability-to-optimum objective uses C* and cannot establish an implementable optimum-blind objective's superiority.
- Claimed coverage/ready-for-QPU conclusions, empirical n12 scaling and hardware-like numbers do not follow from these ideal archives. Zero hardware attempts are recorded here.

`summary.unsupported_claims` records the numerical dispositions and available raw row locators. A rounded value match identifies a possible trace source, not proof of how the unsupported report was generated. No invented numbers are substituted for missing data.

## Schema, commands and checks

`summary.json` schema1 contains `haar.groups`, `e05b.groups`, `e05b.graphs`, paired boson-minus-distinguishable descriptive effects, raw campaign profiles, `unsupported_claims`, and explicit publication-policy booleans. E05b groups use `(n,model,lambda_value)`; `final_p_success_mean` is the nominal point estimate, `instance_interval` is descriptive and `unique_graphs` is its cluster count. `benchmark.csv` has one row per run, including both attempts and objective-call budgets, frozen-model exact/heldout metrics, earliest winning batch, archived first hit, best-valid cost and audit flags. `campaigns.json` is the finite campaign/provenance census. `source_hashes.json` records historical source-pin resolution and all311 observed historical input files' unchanged before/after hashes.

Portable data generation from the repository containing this script, with a fresh output directory:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 \
  /path/to/.venv/bin/python -B scripts/reconcile_experiments.py \
  --archive-root /path/to/original/repository \
  --output results/validated/new_reconciliation
```

The actual bounded command, start time, versions, resource limits, local input hashes and output hashes are in the canonical `manifest.json`. The runner pins the local script/contract/pyproject; the script separately verifies the external archive files and historical Git blobs and records their indexed hashes. No claim that the runner independently inferred that external dependency closure is made. The final reconciliation took about13.27s; the preliminary pass15.69s. Each used one conventional numerical thread,180s wall cap and120s CPU cap. Neither pass reran a historical experiment.

Targeted verification used the root venv, this worktree's src on PYTHONPATH and `pytest tests/test_reconciled_evidence.py -q -p no:cacheprovider`: **9 passed**. Tests reject corrupted counts, C*-style loss substitution, wrong selected parameters and changed first-hit history; ensure optimizer duplicates do not create new graph clusters; accept historical source pins despite changed current code; and verify relocated archives by hash. An initial fixture demanded exact binary-float equality after duplicate summation and failed by2.8e-17; its source, output and receipt are preserved separately. Replacing that assertion with an absolute1e-15 comparison fixes the test without changing reconciliation mathematics or data. No full-suite repetition was performed here.
