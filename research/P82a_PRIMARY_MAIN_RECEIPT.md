# P82a unique primary main: sealed recorded receipt

26 November 2026. **PROVISIONAL RECORDED STATUS: INCONCLUSIVE_FAST_ELIGIBILITY.**
The producer records `positive_accepted=false` and `failure.status=NO_FAILURE`.
This receipt reports sealed data and provenance; classification and numerical
consistency remain subject to ROOT's independently frozen recorded-data audit.
It is neither an accepted strict classical veto nor evidence of a B advantage.

ROOT separately authorized this one main after qualification. It ran from clean
commit `39b61bb9289cab7439ca15a4aa79d265b068f6f9`, with the source frozen at94f80b94
unchanged. Immediately after the runner returned, **before opening any data,
logs or manifest**, all eleven raw outputs were committed as
`561410b385c29d52231b5e0cbe9938fa813c1739`. Only the necessary runner
`completed` status was observed before that seal. No retry or further main ran.
The numerical slot was released at the raw seal; later work only read records,
summarized recorded fields and validated provenance.

## Command, limits and unchanged inputs

The exact child argv in the frozen main contract was used once:

```
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P82a_split_scatter_veto.py --spec research/P82a_execution_spec.json --output experiments/P82a_dev_veto/run_001/data
```

The installed Mathbox4.0.0 `computation-audit/scripts/run_experiment.py` v2 runner
used `--root /Users/karimelhoudaigui/Desktop/pasqal/.local/p65-independent-audit`,
`--contract research/P82a_split_scatter_execution_contract.json`, the exact
fifteen individual `--input` paths listed below, all eight individual contract
`--result` paths, and fresh `--output experiments/P82a_dev_veto/run_001`.
Caps were `--timeout 90 --max-cpu-seconds 60 --max-threads 1
--max-output-bytes 4194304`. The shell set `PYTHONDONTWRITEBYTECODE=1` and all six
OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS thread variables to1 before Python execution.

[The manifest](../experiments/P82a_dev_veto/run_001/manifest.json) records
`run.status=completed`, exit0, started at `2026-11-26T01:26:43.152264+00:00`, and
elapsed29.354166s. Post-seal parsing confirmed exact child-command and declared
result-array equality with the contract. All fifteen SHA256 values below were
identical before and after execution; repository dirty state at launch wasfalse.
No result was missing or invalid.

| Input path | SHA256 before = after |
|---|---|
| `AGENTS.md` | `6c4c409cdf9d05330bc46b9f607b7034e16bcaf51086b712a80d03ccd8e78e5a` |
| `research/P82_HARDWARE_COMPATIBLE_ESCAPE_DESIGN.md` | `c008f60143a1c4b0e81dcec1ba7a07c28d89244b10d4d69695070d27b0916723` |
| `research/P82a_DEV_VETO_CONTRACT.md` | `d5e994d970f278bb9c51fa8a806555dce4047e82c8342f676fe267b75dbe71b9` |
| `research/P82a_PREEXEC_CLOCK_ADDENDUM.md` | `1b548885d05fe6a42487c77b12ac00292ebd8bd379c4074e6ce3a49ceb93a8d4` |
| `research/P82a_split_scatter_veto.py` | `7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc` |
| `tests/test_p82a_split_scatter_veto.py` | `e70b74c2915632cf62677c80f40ebeea8e67c669116660096426101542794861` |
| `research/P82a_execution_spec.json` | `8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838` |
| `research/P82a_split_scatter_preflight_contract.json` | `209696de0b0170ff4099cdfd77b6acdaec3c4f78e04e86631047008c13517c0d` |
| `research/P82a_split_scatter_execution_contract.json` | `dca509b4fee65b652227fb395cfc982b4426a9c8ae0da05de75f825493cc5f20` |
| `research/P82a_IMPLEMENTATION_POPULATION.md` | `9080adee7e67189731cdbcbd297c0b419748337025135f85cf7406bee5c1a4ba` |
| `research/P43_global_gain_probe.py` | `b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777` |
| `research/P50_fast_from_scratch.py` | `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86` |
| `research/P50_FAST_FROM_RAW_API_CARD.md` | `3a73269e3a98f853a2a7d0695f77e9efa06f65ad0914daf932ea1715c162ad91` |
| `pyproject.toml` | `7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4` |
| `requirements-research-lock.txt` | `3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1` |

After sealing, the installed `validate_manifest.py` was invoked on this manifest
with `--root` equal to the worktree. It exited0 with
`valid evidence record (run status: completed)`. This checks recorded provenance,
not the independent scientific interpretation or authenticity of physical clocks.

## Recorded B population and cuts

Both fixed unplanted anchors completed three resets times sixteen attempts:
**96 requests, 96 outcomes, 768 modeled full-source photons**. Root seed82026001,
the ER8201601/RR8201602 recipes, weights, rho1/eta1/2, phases, two compiler sweeps,
warmstart/Q caps and all control settings stayed frozen. Recorded graph edge
counts/total weights are ER50/155 and RR32/91. No optimum or exhaustive optimum
certificate was computed or consulted.

| Recorded quantity | ER8201601 | RR8201602 |
|---|---:|---:|
| Requests / outcomes | 48 / 48 | 48 / 48 |
| Full-source photons | 384 | 384 |
| Conditional receiver photons | 187 | 189 |
| All-paid best cut | 46 | 22 |
| All-paid best little-endian mask | `eb03` | `a13d` |
| Actually recorded scored candidates | 3507 | 3507 |
| Raw proposal mean cut | `979/12` | `45` |
| Q-best mean cut | `251/4` | `121/4` |
| Raw mean / total edge weight | `979/1860` | `45/91` |
| Q mean / total edge weight | `251/620` | `121/364` |
| Strictly accepted Q endpoints | 4 | 4 |
| Raw proposals strictly cheaper than current | 0 | 1 |
| Q strictly improves raw proposal | 48 | 48 |
| Bunched attempts requiring RNG repair | 33 | 31 |
| Backend fallback flags | 0 | 0 |

The complete r0 through r8 histograms, retaining zero bins, are:

| r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ER | 0 | 2 | 4 | 14 | 11 | 12 | 4 | 1 | 0 |
| RR | 0 | 2 | 9 | 5 | 16 | 10 | 2 | 4 | 0 |

Thus r0/r8 did not occur in this one draw; they were not discarded or redrawn.
Every receiving vector has eight entries, every restored full count vector has
sixteen entries summing to8, and all observed receiving vectors retain zero
components. All96 nonzero-r requests have a recorded new factory and one serial
native observation; 64 of the96 observations are bunched and repaired.
Conditional simulation of376 receiver photons does not reduce the768 modeled
full-source photons.

Own-chain warmstart-to-final-best cuts are ER `58→49`, `52→46`, `54→46` and RR
`28→22`, `23→23`, `33→22`; these are recorded chain values, not optimum gaps.
Both first discoveries of the all-paid best are **classical Q-neighbor scores**:
ER score1522 at chain1/step3, batch1494/index28, removes2/adds7; RR score670 at
chain0/step8, batch650/index20, removes9/adds8. Indices are zero-based. They must
not be credited as raw optical discoveries. The 7014 paid scored candidates
include all warmstart and Q neighbors, with repeated evaluations retained.
The largest recorded compiler guard error per case is
`2.2226252407574303e-16` / `2.2296817627811213e-16`, against the frozen3e-12 guard;
this is not a many-photon TV or physical sampling certificate.

## Grants and disjoint/derived timing records

Each case has104 directly observed paid spans plus48 paid factory differences,
and48 unpaid `REPORTED_DURATION` factory operands. Their recorded WALL sums give
the grant, without adding reported setup again:

| Timing quantity, seconds | ER | RR |
|---|---:|---:|
| B grant G, paid WALL sum | 0.14144878596925992 | 0.13791904402751243 |
| Direct observed paid CPU sum | 0.13930699999999963 | 0.13660700000000014 |
| Derived factory WALL paid in G | 0.0013288709851622116 | 0.001157750994025264 |
| Unpaid helper-reported factory setup WALL | 0.007782417014823295 | 0.004846125000767643 |
| Observed factory outer CPU | 0.008257000000001291 | 0.005987000000001075 |
| Observed factory outer WALL | 0.009111287999985507 | 0.006003875994792907 |
| Excluded serial sample CPU | 0.0021370000000007217 | 0.00164000000000053 |
| Excluded serial sample WALL | 0.00229349600704154 | 0.0016463370011479128 |

Factory differences retain null CPU/endpoints and references to identified outer
and helper-reported operands. No total paid B CPU is inferred from G or allocated
to the unknown factory residual. The full ledger has402 observed spans,
96 reported factory durations and96 duration differences. It includes separately
timed synthetic input generation. These are producer records pending independent
replay; this receipt did not reconstruct a new observed clock from scalar costs.

The excluded import/configuration span is2.360325 CPU /28.2938599170011 WALL s.
The source whole-run snapshot before final evidence writing records2.976764 CPU /
28.93848316599906 WALL s. Completed serialization/I/O before the final evidence
snapshot is0.2075850000000301 CPU /0.2234160750558658 WALL s; final summary/failure
writing is outside that snapshot. These are different scopes from runner elapsed
time. No local-backend/import time is called QPU wall time, and the favorable
zero-optics G grant is not a matched total-resource measurement.

## Four fixed FAST calls and the recorded stop

All four registered calls returned normally in fixed mode-major order. Each got
its own whole case grant and CPU budget `max(0,G-direct_adapter_CPU)`; grants were
not divided among modes. The final archived witness uses adapter+conservative
entry/return difference+checkpoint on BOTH clocks. The following are the
producer's selected chronological cached witnesses, including that correction:

| Mode / case | CPU budget s | Checkpoint / cut / mask | Corrected CPU s | Corrected WALL s | Work |
|---|---:|---|---:|---:|---:|
| RANDOM / ER | 0.14143378596926004 | 225 / 46 / `eb03` | 0.01669400000000021 | 0.01880200000232435 | 10000 |
| RANDOM / RR | 0.13790704402751253 | 228 / 22 / `5ec2` | 0.016970999999999847 | 0.016976165996311465 | 9963 |
| SPECTRAL / ER | 0.14143478596925974 | 227 / 46 / `14fc` | 0.01864200000000027 | 0.02138804199785227 | 9962 |
| SPECTRAL / RR | 0.13790704402751253 | 228 / 22 / `a13d` | 0.017175999999999636 | 0.017187834000651492 | 9963 |

The four traces contain226,229,228,229 checkpoints respectively, all912 recorded
as dual-timely; each first complete scan is dual-timely. P50's four helper-reported
compute operands have identified `REPORTED_DURATION` records in their headers,
with source hash, null interval endpoints and the typed reference from the
conservative difference. Direct-adapter CPU values are15,12,14,12 microseconds;
the corresponding derived CPU additions are40,44,36,33 microseconds. Their WALL
additions are `3.675099651445635e-05`, `4.0499999158782884e-05`,
`3.220899816369638e-05`, `3.2084000849863514e-05` seconds. No negative difference
was clipped and no late best was reconstructed as an earlier witness.

Every fixed mode's selected cut **ties** B's46/22. No same fixed mode is a strict
winner on both anchors, so the strict negative-veto condition is absent. Every
call also reaches its predeclared work guard before spending its allowance:
RANDOM/ER stops at `max_proposals`; the other three stop at
`proposal_guard_before_full_scan`. All four have `early_guard=true` and
survivor `eligible=false`. Consequently the frozen producer policy records
**INCONCLUSIVE_FAST_ELIGIBILITY**. This is not an accepted surviving positive
panel or a reason to enlarge the10000 guard after seeing the result.

Tier2 is an empty executed panel with reason `FAST eligibility incomplete`.
RECIPIENT_FRONTIER, PHASE_HYPERPLANE, CONTINUED_DESCENT and MULTISWAP each have
two explicit `NOT_RUN` entries and null outcomes. Reoptimized D/species are
`NOT_RUN`; no fresh seed/relabel/heldout, extra optical attempt, follow-on control,
calibration or rerun was launched. The control stream has four headers,
912 checkpoints and four results. No favorable best-of-mode portfolio is credited.

## Runtime provenance, warnings and sealed output hashes

The metadata records all ten external path/pin checks matching before scientific
imports: five Perceval Python files, native extension, two package METADATA files,
virtual-environment metadata and the physical interpreter. The main persistent
interpreter guard ran. Actual versions are Python3.11.15, NumPy2.4.6,
SciPy1.17.1, NetworkX3.6.1, Perceval1.3.0, exqalibur1.4.2 and pytest8.4.2,
on macOS26.2 arm64. The complete actual paths and SHA values are in metadata;
external pins are checked by CLI and are not runner `--input` bindings.

Initial and final archived native Config readbacks are1; all six recorded
environment thread values are1. The frozen per-case native checks returned
without exception. The pregraph metadata table contains502 potential PCG-role
seeds and96 potential native seeds; this includes roles for controls later not
run and must not be read as an actual Generator/call count. Source seeds and
marks for all96 attempts are retained in the raw records.

`stdout.txt` is empty. All2445 stderr bytes are preserved: three pairs of Perceval
default-storage/temporary-folder warnings; a Matplotlib default-cache permission
notice and temporary-cache fallback; a Fontconfig no-writable-cache diagnostic;
and the font-cache-build notice. No path, cap, source or cache setting was changed
to suppress them, and no retry occurred. They did not produce an exception:
the failure file explicitly records `NO_FAILURE` and runner exit is0.

All paths below are within `experiments/P82a_dev_veto/run_001/`:

| Raw path | Bytes | SHA256 |
|---|---:|---|
| `data/B_ER.jsonl` | 951714 | `a3bd4357ed2509dd201f6e3bba628d85b96f0839285ca32b9a98b2dcda987a2f` |
| `data/B_RR.jsonl` | 952509 | `2798618a796db8571a8377ac0f027b74af8d715f107810e31228c90de749a9cf` |
| `data/controls.jsonl` | 251320 | `b0b9d448e4cab86454a137a61b63a4326d936b0c332e56a70edfa884161bc611` |
| `data/failure.json` | 24 | `b24b6f7f3627ec4fec61d369b7ad9a35c8918c6da5f7f9390fd97cd5ed29a643` |
| `data/graphs.json` | 1322 | `28e64b8684c7c85ed2005fae6870ca017785f74f0b732dc6c91d8a1dd7626e8d` |
| `data/metadata.json` | 73503 | `759937f271bdc2e8f6816a738fdf7d5981d7d200d31dc4f426c0bc6aba50e35b` |
| `data/paid_ledger.jsonl` | 204561 | `a887e9629194198300c2d0ed66ba678bd1e95053eef1efcf3a5f1fd4d6921044` |
| `data/summary.json` | 90989 | `79e917c92b31b026c818f836d313dbb7c526e805a6cb718a73b1a3f6cede9a8c` |
| `manifest.json` | 13686 | `2fe4cc045e74eb3983c210c2ee7476d466b5963ffe9f9fee73cf0400268d9e4e` |
| `stderr.txt` | 2445 | `69c9d26f8c323c387de2072b75c0600baa427e0c7e9dac04c40b4da56b5945c0` |
| `stdout.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The eight scientific files total2525942 bytes, uncompressed, below32MiB and its
1MiB final reserve policy; all eleven raw files total2542073 bytes. Combined logs
are2445 bytes, below4MiB. No RSS measurement or hard RSS promise follows from the
256MiB logical plan; runner address-space and core-affinity fields are null.

This is one seeded floating local-backend DEV record, not physical count/clock
authentication, a certified sampling-TV error, an optimum certificate, a generic
graph conclusion, matched total-resource advantage, novelty, or a positive
optimizer result. **The independent recorded-data audit is still pending for
this receipt; no further execution is authorized or started here.**
