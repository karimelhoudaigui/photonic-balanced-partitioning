# P43 independent raw-data reconstruction — run_001

Decision: **REJECT the tested phase-gradient-echo family at the frozen pilot
budget: NO_SIGNAL_AT_PILOT_BUDGET.** This rejects its progression under the
P43 card. It is neither a universal photonic obstruction nor a statistical
advantage claim, and does not close the larger discovery program.

The adaptive lane independently reconstructed9952 JSONL rows using stdlib-only
code, without importing the photonic implementation, regenerating a graph,
sampling photons, running an optimizer, or computing a unitary. Author code was
previously reviewed; this is independent reconstruction of the EXISTING finite
data, not independent experiment execution. The lane shares overall context
and authored the P43 scientific card.

## Exact provenance and reproduction

- Run: `experiments/P43_global_gain/run_001` in the parent repository.
- Frozen run revision: `c062f2fcf48a83f301742900e53a8e8759a29d3e`.
- Production code is the reviewed1db2038 implementation.
- Raw SHA256: `17a6fb9097807220b38ccf499967f61d020cd413d78fc43713bcfb8037ba41e9`.
- Development-prefix SHA256:
  `6bdba10c217eab5f6bc6d46abedce6ee316f6e2c512d9860a2db00794de842b3`.
- Audit code: `research/P43_adaptive_raw_audit.py`.
- Full per-case/per-tuple numeric receipt:
  `research/P43_adaptive_raw_audit_receipt.json`, including its auditor code hash.

Reproduce this aggregation, choosing a NEW output filename:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python research/P43_adaptive_raw_audit.py \
  --root /Users/karimelhoudaigui/Desktop/pasqal \
  --run /Users/karimelhoudaigui/Desktop/pasqal/experiments/P43_global_gain/run_001 \
  --output /private/tmp/P43_adaptive_raw_audit_reproduced.json
```

The script exited0 in0.34 wall seconds. It checked every manifest-declared
output hash and every input hash against the frozen Git revision and the
manifest's before/after hashes. Manifest status is `completed`, exit0, no
missing/invalid declared results. The repository dirty flag is TRUE, but all
listed load-bearing inputs match their committed blobs and remained unchanged.
This is declared, not silently converted into a clean-tree claim.

## Raw optical totals: tuning only

| Model | Attempts | CF scores | Collisions | Improving draws | Total gain |
|---|---:|---:|---:|---:|---:|
| Bosonic B | 896 | 373 | 523 | 0 | 0 |
| Independently tuned D | 896 | 531 | 365 | 0 | 0 |
| Phase-field feasible | 896 | 896 | 0 | 0 | 0 |
| Species b4 | 896 | 463 | 433 | 0 | 0 |

Each optical tuple received14 shots in each of8 graph/seed cases. The independent
reconstruction recomputed every raw CF cost by an edge-crossing loop on saved
adjacencies and checked every gain against max(0,C0-cut); collisions contributed
zero, with no conditioning or hidden retry. All4*8 pooled tuple gains are zero.
All four independently selected global settings are therefore IDENTITY, matching
`selection.json` and `summary.json`. Both predeclared gamma-zero duplicate-law
pairs (indices0/4 and2/6) are fully present; their finite draws are not treated
as evidence of additional mechanisms or independent graph units.

Each B/D/b4 tuning total represents8064 modeled injected photons. Actual device
photons and QPU calls are ZERO. A phase-field draw is a classical subset sample,
not an injected-photon resource. No hardware resource comparison is inferred.

## Common classical front end reconstructed from raw complete scans

The initial source is recovered from the removed vertices in the first full
scan. The audit independently checks every one-swap score/delta, complete k^2
pair coverage, strict best-move/lexicographic ties, and subsequent source updates.
The saved summaries and contexts match the reconstructed final anchors.

| Graph | Initial cut | Fixed source cut C0 | Scores including initial | Certified one-swap minimum |
|---|---:|---:|---:|---|
| dev16_er | 93 | 52 | 193 | yes |
| dev16_rr | 77 | 29 | 257 | yes |
| dev20_er | 201 | 156 | 301 | yes |
| dev20_rr | 123 | 45 | 501 | yes |

These1252 score evaluations across4 graphs are common charged CLASSICAL work.
Their improvements are not attributed to optics. Certification is only against
one-swap neighbors, never a claim of global optimality.

## Best costs including all tuning discoveries, by graph and fresh seed

Every table entry includes the already known source, and is the minimum across
ALL tuples/attempts for that model, not just the selected setting. B, D,
phase-field and b4 all retain C0 in every case, so a single column records them.
Each feasible control receives112 scores per development graph/seed case.

| Graph/seed | C0 = each of B/D/field/b4 | Uniform | Two-swap | Swap descent | Anneal | Spectral + descent |
|---|---:|---:|---:|---:|---:|---:|
| dev16_er:0 | 52 | 52 | 52 | 52 | 52 | 52 |
| dev16_er:1 | 52 | 52 | 52 | 52 | 52 | 52 |
| dev16_rr:0 | 29 | 29 | 29 | 29 | 29 | 29 |
| dev16_rr:1 | 29 | 29 | 29 | 29 | 29 | 29 |
| dev20_er:0 | 156 | 156 | 155 | 156 | 135 | 135 |
| dev20_er:1 | 156 | 152 | 145 | 156 | 135 | 135 |
| dev20_rr:0 | 45 | 45 | 45 | 45 | 45 | 37 |
| dev20_rr:1 | 45 | 45 | 45 | 45 | 37 | 37 |

Thus lack of optical improvement is not explained by all four anchors being
unimprovable: the classical controls find lower costs on BOTH20-mode graphs.
This statement does not use or determine C*.

## Relabel/fresh-seed stage: distinguish skipped optics from passed probes

The automatic selection boundary's raw-prefix hash was independently verified
before the first raw fresh-relabel row. Code/spec hashes also match frozen
inputs. For all four sampled models, identity selection legitimately cancels
the128 potential optical probe draws. Sixteen summary rows are analytic
identity placeholders, not samples. Consequently numerical optical relabel
covariance and optical fresh-seed behavior were **NOT EXERCISED** in run_001;
they must be reported N/A, not PASS. The architecture's prior analytical/code
checks are separate evidence.

All5 classical controls still receive32 scores on each of the4 probe cases.
The permutation in each context is a bijection, and recomputing scores on the
permuted saved adjacency matches every raw probe candidate. All raw seeds match
the independent SHA256 seed derivation. Recorded seed sets are disjoint:
296 development seeds and20 fresh classical-probe seeds, with no overlap.

| Probe | Analytic identity cost | Uniform | Two-swap | Swap descent | Anneal | Spectral + descent |
|---|---:|---:|---:|---:|---:|---:|
| dev16_er:probe2 | 52 | 52 | 52 | 52 | 52 | 52 |
| dev16_er:probe3 | 52 | 52 | 52 | 52 | 52 | 52 |
| dev20_rr:probe2 | 45 | 45 | 45 | 45 | 45 | 40 |
| dev20_rr:probe3 | 45 | 45 | 45 | 45 | 45 | 40 |

Each classical method has896 development plus128 probe scores. There are still
only4 unique development graphs, not8 or12. No held-out graph was opened.

## Interpretation and limits

The bounded runner records17.533394 wall seconds, CPU limit60, wall limit90,
and thread cap1. The script reports1.474721 CPU seconds measured inside main;
that excludes imports executed before main. These are simulation observations,
not QPU latency. Their exact resource interpretation remains as in the runner.
All checked summary counters, chosen tuples, anchor ledgers and best costs
match the raw reconstruction. Raw files and the manuscript were not modified.

The predeclared all-zero decision applies. Do not open held-out graphs, rerun
the same unchanged grid at a favorable seed, freeze a hardware circuit, or
revise the paper as if a positive mechanism had appeared. Any next attempt must
change the mechanism or supply a new explicit obstruction and preregistration.
P43 is a preserved negative for this finite-angle echo at k8/k10 and this
budget; passive optics, other decoders, adaptivity and other finite-angle
architectures remain outside the logical conclusion.
