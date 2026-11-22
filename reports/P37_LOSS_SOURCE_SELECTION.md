# P37 checkpoint: exact source choices under uniform loss

The finite source phase diagram is derived in
`theory/phase3_loss_source_selection.md`. All112 prescribed cells and1610
source probabilities pass exact arithmetic checks;36 critical thresholds
have rational sign brackets of width2^-40. This is a resource calculation
for a known Haar-averaged law, not evidence of graph-optimization benefit.

## Mathematical result and review status

For even m>=8,k=m/2, distinct single inputs k<=N<=m and independent uniform
survival 0<eta<1, the per-attempt optimum is among N=m-1,m, with a unique
transition. Per-injected-photon efficiency has exactly four possible optima,
N=m-3,m-2,m-1,m, with three strictly ordered transitions. The argument uses
the exact lossless ratios, binomial coupling/size bias, a one-crossing signed
polynomial, and a probability-ratio comparison. Endpoint eta=1 has the known
per-attempt tie N=m-2,m-1; eta=0 has zero success.

The proof also derives the critical-loss limits m(1-eta)->1 for the attempt
transition and ->1,2,3 for the successive photon-cost transitions. Its error
expansion holds for eta=1-lambda/m, fixed lambda and fixed source deficit;
no fixed-loss rate theorem follows from that expansion.

After the initial Astra self-review, reviewer /root/physics independently
reconstructed the argument without reading the coordinator verdict or numeric
probe. Verdict: **proved as written**, commit94b5099 integrated7729b91; exact
target SHA and separate m8 rational/symbolic checks are in
reports/P37_INDEPENDENT_PROOF_REVIEW.md. That manifest validates. The author's
separate arithmetic verifier remains self-review. Neither review supplies a
novelty or optimization-benefit certificate.

## Executed validation

Protocol/code/proof frozen1d65279, run retainedd402374:

- m8,10,12,16,24,32,48,64; six fixed efficiencies and eight eta=1-lambda/m
  values at every m. Every source N=k,...,m retained:1610 exact probabilities.
- Survivor-mixture and generating-coefficient positive sums agree exactly.
  Both efficiency criteria are maximized over the entire allowed source set.
- Four thresholds at each of those sizes and m128:36 sign brackets,40 exact
  bisections each. Raw polynomial coefficients and endpoint differences remain.
- Separate review reconstructs the Haar click law through a normalized Polya
  urn and the loss mixture through de Casteljau affine averaging. It checks
  every stored probability, cost, maximizer and trace entry, then recalculates
  all root signs by recurrent binomial weights. All checks pass exactly.

Internal runtimes on the measured M2/8GiB host: primary0.397s, review0.478s.
These are small analytic sums, **zero full Fock simulations and zero physical
shots**, including at64/128 modes. The run cap was120s, one conventional
numerical-library thread. No model/service/download was needed.

| m | Attempt transition: scaled loss | Photon transitions: scaled losses |
|---|---:|---|
| 8 | 0.864823 | 0.258803,1.382611,2.248439 |
| 32 | 0.968222 | 0.815162,1.821713,2.766438 |
| 64 | 0.984248 | 0.907009,1.908619,2.879185 |
| 128 | 0.992156 | 0.953327,1.953726,2.938557 |

Rounded display values above do not drive any decision. The exact brackets
are in `experiments/P37_loss_source/run/data/raw.json`; review summaries are
under `experiments/P37_loss_source/review/data/`. Both v2 manifests are completed
and validated against their pinned sources. The large differences at m8
also warn against treating limiting thresholds as finite-size answers.
The standalone figure is `experiments/P37_loss_source/figures_final/loss_source_phase.pdf`
(PNG also provided), with its raw/script hashes in the render receipt.

For example at m64, eta=.99 chooses N63 per attempt and N61 per photon;
eta=.9 or .5 chooses N64 for both. This comparison says nothing about
whether the accepted graph partition is good. The ensemble's accepted subset
is uniform; classical stars-and-bars/loss sampling reproduces that marginal.

## Reproduction and non-claims

Recorded argv and input/output hashes are in the manifests. Direct regeneration
commands, using fresh destinations to protect raw data, are:

```sh
.venv/bin/python experiments/phase3_loss_source_probe.py --output /tmp/p37-fresh-primary
.venv/bin/python experiments/check_loss_source.py --raw experiments/P37_loss_source/run/data/raw.json --output /tmp/p37-fresh-review
.venv/bin/python scripts/plot_loss_source.py --raw experiments/P37_loss_source/run/data/raw.json --output /tmp/p37-fresh-figures
```

The first two fail if their destination exists. For archival evidence use
the installed computation-audit v2 runner and the corresponding contracts,
as done for the recorded runs. The figure receipt hashes its script/raw input.

The known-law source is Bouland et al.,
[2312.00286v2, Lemma1/Eq6](https://arxiv.org/html/2312.00286v2#S4), already
authenticated in P32. The elementary corollary's novelty remains unassessed:
a bounded search is not a novelty certificate. No full noisy optimizer,
finite-budget allocation optimum, fixed-device waiting cost, real source
heralding/latency model or classical cost comparison is established here.
Bounded source inventory: research/P37_SOURCES_AND_SCOPE.md. Newly discovered
2026 loss-simulation preprints are marked as incompletely audited adjacent
sources, not silently adopted as theorem dependencies.

Decision: **SUPPORTED** for the exact finite assertions; KEEP as a resource
audit. The general optimization objective is still OPEN. PAPER_READY=FALSE,
QPU_GATE=CLOSED. Manuscript untouched; no hardware request.
