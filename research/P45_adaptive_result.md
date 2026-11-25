# P45-A — cavity completion: preserved negative development result

Decision: **REJECT this frozen mechanism at the tested budget.** All256 B
observations were completed to feasible balanced partitions, including194
collisional counts, but NONE improved the shared incumbent. D and all declared
stochastic classical field controls produced improvements. The larger positive
discovery objective remains OPEN; there is no universal obstruction or QPU gate.

## Contract, actual execution and provenance

Scientific contract/code/tests froze at
`c20193ba400dd00c00c150f28e0c6943ea7d3112`, base
`8f83f2bff321f658182a23aacf07d03b12c6633b`.
Four targeted reference tests passed in0.86s; their argv, source hashes, limits,
stdout/stderr and JUnit result are saved in `research/P45_adaptive_preflight/`,
committed BEFORE the pilot at `19a9902f6570592e7e7f7ca528da8014ea657408`.
The existing full suite was not rerun by this lane in its allocated slot.

The unique experiment is `experiments/P45_adaptive/run_001`. Its v2 manifest
records source19a9902, exact9-input closure, unchanged before/after hashes,
software versions, child argv, all6 declared data results, exit0 and `completed`.
The Mathbox manifest validator passed against this worktree. Actual enforced
limits: CPU60s, wall90s, numerical threads1, log-output cap32MiB. Planned arrays
were below256MiB; no unsupported macOS address-space/affinity limit is claimed.
The complete saved directory is about13MiB, below the32MiB planned new-data cap.
Observed run wall time17.36936s; inside-main CPU1.810534s. Cold imports and
bookkeeping are recorded setup work, not measured QPU time. No automatic rerun,
graph replacement, discarded seed, device access or manuscript edit occurred.

The actual child command, invoked through the bounded runner, was

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python research/P45_adaptive_probe.py \
  --contract research/P45_adaptive_contract.json \
  --output experiments/P45_adaptive/run_001
```

The manifest stores the exact command and hashes; `P45_adaptive_execution_contract.json`
lists all runner input paths and caps. A new experiment must use a NEW output
directory and a new explicit hypothesis; do not overwrite or silently repeat001.

## Credited classical front end and fixed optical source

| Graph | Initial source cut | After source best-swap | Public Cref BEFORE photons | Shared front-end score units |
|---|---:|---:|---:|---:|
| p45a16_er | 132 | 78 | 78 | 681 |
| p45a16_rr | 126 | 28 | 28 | 745 |
| p45a20_er | 191 | 100 | 96 | 1251 |
| p45a20_rr | 98 | 39 | 39 | 1151 |

The improvement100->96 on20ER was produced by the ZERO-FIELD classical
completion, before any photon sample. It is credited to EVERY method, never
to B. Original S0 remains the fixed optical source; Sref/Cref is a separate
public incumbent. Zero, pure-greedy and vacuum calls were all charged, as were
every marginal inspected in completion and every source best-swap candidate.

## All outcomes decoded; collisions are diagnostic here

Every primary model has256 proposals and13952 decoder score units (every
partial marginal plus final cut). The paired B permutation adds another13952
classical score units and ZERO additional physical samples; its discoveries
are separately reported. No method receives this second decoder for free in
a deployable-resource interpretation. B/D/b4 each represent2304 modeled source
photons. Actual device photons and QPU calls are ZERO.

| Model / field | Feasible decoded outputs | Improving outputs | Sum of gains against public Cref |
|---|---:|---:|---:|
| Full identical B | 256 | 0 | 0 |
| Independently selected D | 256 | 3 | 12 |
| Phase-multinomial mean-field | 256 | 11 | 52 |
| Exact-moment hybrid D + phase-intensity field | 256 | 8 | 22 |
| Gaussian with B covariance | 256 | 7 | 37 |
| Independent matching-variance noise | 256 | 14 | 73 |
| Species b4 | 256 | 1 | 2 |
| B values permuted before the SAME decoder | 256 | 16 | 74 |

Raw count diagnostics: B62 CF /194 collisional, D107/149, species b474/182,
phase-multinomial0/256. These are NOT acceptance counts: ALL were decoded and
scored. Hybrid uses continuous corrected fields with an underlying labelled
count; Gaussian/independent noise are continuous fields. Do not interpret their
fields as detector Fock states or invent CF probabilities for them.

The gain sums are repeated single-proposal improvements against a FIXED Cref,
used for declared training selection; they are not cumulative improvements of
a moving incumbent or a significance statistic. All B tuple sums are zero, so
its global selector returns identity. Other models select their settings from
their OWN data. Every tuning discovery, including nonselected tuples, remains
in the raw history and best-cost comparisons below.

## Best costs across ALL charged tuning discoveries

The first two graph families have identical values for both replicates. On
16ER every method retains78; on16RR every method retains28. These are known
feasible costs, not certified global optima.

| Graph/seed | B | D | Phase field | Moment hybrid | Gaussian | IID | b4 | Permuted B | Anneal | Spectral | Collective KL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| p45a20_er:0 | 96 | 96 | 96 | 94 | 96 | 94 | 96 | 94 | 94 | 96 | 94 |
| p45a20_er:1 | 96 | 96 | 94 | 94 | 94 | 94 | 96 | 94 | 94 | 96 | 94 |
| p45a20_rr:0 | 39 | 33 | 32 | 32 | 32 | 29 | 37 | 32 | 33 | 29 | 29 |
| p45a20_rr:1 | 39 | 35 | 32 | 37 | 29 | 29 | 39 | 29 | 29 | 29 | 29 |

Each of3 strong feasible-search controls receives1376 units per16-mode
graph/replicate and2112 per20-mode case, plus the same public front end. Each
therefore performs13952 scored feasible candidates over the full pilot. A
partial unbalanced marginal and a complete feasible cut have DIFFERENT CPU
costs; counts are one explicit comparison axis, not a matched hardware cost
theorem. All preprocessing and timings remain available for review.

## Separate scalar raw-data audit and limits

`research/P45_adaptive_raw_audit.py` independently implements scalar graph-cut
and marginal loops to reconstruct45292 raw rows without importing NumPy, the
production probe, or a physics simulator. Its output is
`research/P45_adaptive_audit_receipt.json`. It checks all manifest hashes,
source full-scan coverage/moves, all zero/vacuum decoder candidates, public
incumbents, every recorded stochastic completion choice/marginal/cut, paired
permutations, all classical raw cuts/anytime minima, candidate/score counts,
global settings and their agreement with summary. The audit exits0.

This is AUTHOR SELF-AUDIT using a separate implementation, not fresh-agent
physical replication or an independent optimizer study. The pre-run root
review and small-reference tests are separate evidence. No p-values, held-out
results, graph-relabel robustness, loss robustness or global novelty are claimed.

The decoded B zero-gain failure survives removal of CF rejection and is not
explained by all incumbents being unoptimizable: controls improve both20-mode
graphs. Permuting B field values improves some proposals, so the particular
graph alignment used here did not help this decoder at this budget. It does
not prove that every graph-aligned quantum field is worse, or determine a
general causal mechanism from this small development sample.

No unchanged grid/seed sweep, held-out search, hardware circuit, Laurent job
or manuscript integration is warranted by this result. Further work needs a
changed mechanism with a new falsifiable step. All known P33/P37/E05b and
P41-P44 evidence, historical raw data, and the manuscript remain preserved.
