# P63 independent recorded-data checker: code-only freeze

2026-11-25. Designed from the frozen producer's source/schema and prior audit
templates, without opening P63 raw data, summary, FAST output or main manifest.
The reviewer knew the synthetic qualification was reported as 46 PASS and
that the unique main was running. No main scientific outcome was supplied to
this checker during authoring. This is a recorded-data consistency audit,
not a new prospective quantum experiment or independent physical replication.

**CODE ONLY: no checker import, collection, fixture test, calculation, graph,
count draw, native calibration or audit execution occurred during authoring.**
ROOT must inspect and freeze these files, then bind sealed input paths/hashes
and separately authorize an exclusive bounded run. Nothing here authorizes a
retry, another primary run, changed scientific budget, paper edit or QPU call.

## Exact primary format and independent reconstruction

The supported producer is original commit
`8b20dca7bbe476a2eed75433b31e5ca582809484`, source SHA256
`7f60cb437a9936323851d926ca18f16c7899b16a8d5353c69df88cf21a03d5d6`.
The later primary run may have a different repository commit containing that
unchanged source. Its actual run commit is bound separately, never guessed.
No P43, P50, P63 or other production module is imported by this checker.
Dependencies are Python stdlib and pinned NumPy2.4.6 only.

The checker independently reconstructs U as tensor products and a full mixer
matrix, rather than the producer's entry loop. It checks every recorded U,
q, both Gram matrices, masses and the C6 input-cycle identity within absolute
3e-12. Exact Fraction arithmetic reconstructs every signed SPSA probe/update,
using one direction per pair and all four cuts per sign. Scalar integer edge
sums reconstruct every recorded actual cut. Ranking occurs on physical counts
and carried priorities before the fixed mode-to-vertex map.

Deterministic PCG64 recipe replay covers the weight MULTISET, physical
embedding, shared perturbation directions and each carried
priority. The full seven-arm prospective seed table is rebuilt from role names
without drawing an optional-model sample. This deterministic replay is the
only RNG use: no NetworkX graph or optical count is generated. The recorded
ER/RR topology and weight assignment to particular edges are not independently
reproduced; RR degree6 and weight range1..5 are checked. In particular the
producer sorts `graph.edges()`: NetworkX orientation/node-insertion order is
not serialized in the adjacency, so replacing that order with `i<j` would be
an unjustified audit convention. The B/FAST comparison uses the SAME archived
adjacency and exact scalar cuts regardless of that unverified generation step.

A completed primary requires two cases, 40 requested/completed B observations
per case, 16 completed batches, all exact losses/updates, final-theta-before-
fresh ordering, 16 fresh cuts per case, the equal normalized graph mean,
all-paid online minima, private cache keys and expected seed roles. B paid
WALL is rebuilt from recorded component clocks: context plus half compiler,
directions, setup less returned backend/diagnostics, postprocessing, means,
updates, final aggregation and half equal-graph aggregation. Factory prefix
and CPU-split-unknown receipts are checked. Timing tolerance is 1e-8 seconds.

For every FAST checkpoint, three-byte little-endian masks are unpacked without
the producer, padding/cardinality checked, scalar cuts recomputed, and best
cuts/time/work monotonicity checked. Recorded work counters and full81-delta
scans are reconciled. The LAST actual timestamp within the RECORDED CPU budget
determines the eligible result; later audit bests remain excluded. The recorded
budget must match the independently summed B-only WALL less adapter CPU within
the declared clock tolerance. Exact deadline comparisons then use that recorded
budget, avoiding a new rounding convention at an equality boundary.

Four separate FAST results must exist for a completed comparison. A same fixed
mode must match/beat B's all-paid minimum on BOTH graphs to reproduce a veto;
the checker never takes a free per-graph random/spectral portfolio. Favorable
survival additionally needs all stronger first-scan/no-early-guard flags. Every
primary and checker result must keep `positive_accepted=False`.

## Failure/partial semantics and bounded interpretation

First recorded batch failure must be followed by first failure, not another
scientific attempt. Failed primaries may contain fewer than 80 B events and
missing per-case files. A readable prefix is checked without forcing missing
events. Invalid/truncated gzip/JSON tails of an unsuccessful primary are marked
as incomplete, not repaired or resampled. A failed primary remains inconclusive
even if some completed files happen to contain a nominal veto. A runner kill
after summary creation can leave such a label in the file; the unsuccessful
manifest overrides it, without treating that label alone as corrupted data.

Only a completed, fully bound producer with both complete B cases, all four
verified FAST calls, all 12 expected data files, no primary failure and no
checker discrepancy can yield `complete_comparison_verified=True` and accepted
recorded fixed-FAST veto modes. Otherwise these accepted modes are empty.

Checker outcomes are `PASS_RECORDED_CONSISTENCY`,
`PARTIAL_CONSISTENCY_INCONCLUSIVE`, or `FAIL_RECORDED_CONSISTENCY` (which includes
malformed/inconsistent or unchecked evidence). A PASS authenticates recorded
relations within the stated range, not a probability distribution, real clock,
online timing causality, each unrecorded FAST proposal, significance, held-out
performance, optimizer superiority, novelty or hardware runtime.

Limits are CPU20s/wall30s, one worker/thread, logs4MiB and new report4MiB,
planned logical workspace64MiB. Input data plus primary manifest are bounded at
32MiB; decompressed raw text at8MiB, one raw line at1MiB; FAST checkpoints at
10k/call and40k total; at most32 short failure examples. No full Fock law,
permanent table, new graph or physical sampler is constructed. The checker
holds the primary summary and one separate FAST payload at a time, with small
raw state. Logical workspace excludes installed library resident images and
is not a Darwin hard-RSS guarantee. External bounded-runner status remains
authoritative for time/resource/output failure. First failed run is retained;
no automatic retry or post-data enlargement is allowed.

## Binding after checker freeze

The checker REFUSES to open scientific inputs without a separate binding JSON.
ROOT creates `research/P63_independent_raw_audit_input_binding.json` AFTER
freezing this checker and sealing the primary. It has this schema; angle-bracket
values below are placeholders, not observed hashes or permission to run:

```json
{
  "schema_version": 1,
  "primary_source_commit": "8b20dca7bbe476a2eed75433b31e5ca582809484",
  "primary_source_sha256": "7f60cb437a9936323851d926ca18f16c7899b16a8d5353c69df88cf21a03d5d6",
  "checker_source_sha256": "<SHA256 of this frozen checker>",
  "producer_commit": "<actual commit in the sealed main v2 manifest>",
  "producer_manifest": "experiments/P63_spsa_fast_stage/run_001/manifest.json",
  "data_directory": "experiments/P63_spsa_fast_stage/run_001/data",
  "artifacts": [
    {"path": "<primary manifest path>", "sha256": "<actual SHA256>"},
    {"path": "<each EXISTING primary data file path>", "sha256": "<actual SHA256>"}
  ]
}
```

Every existing regular data file must be bound, including partial/failure
files; paths are project relative, unsymlinked and limited to the producer's
declared whitelist. At most12 data files plus the primary manifest are allowed.
All bound hashes are checked BEFORE parsing any scientific content and AFTER
the audit. The main v2 manifest's 18-artifact closure, known source/test/helper/
contract hashes, before/after equality and result hashes are reconciled. This
does not replace the standard installed manifest validator or full ROOT review.
No command from an evidence record is executed.

The committed JSON execution contract is an UNBOUND scaffold. ROOT must make
a new bound contract copy after sealing, append the binding, primary manifest
and every existing data path to its exact `execution_artifacts`, and use that
same full list as the runner's repeated `--input` arguments. Bind the committed
checker, this MD, scaffold, bound contract, tests and dependency/instruction
files as well. Do not alter this checker, seeds, tolerances or resource caps
while binding. Runtime manifests are produced only by an authorized run; none
is fabricated by this code-only task.

## Commands, separately authorized

Synthetic fixtures (eight authored functions, not collected):

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest -q tests/test_p63_independent_raw_audit.py --junitxml=research/P63_independent_raw_audit_preflight/run_001/junit.xml
```

The small tests check scalar cuts, little-endian masks/padding, rank-before-
mapping, a hand-calculable Fraction SPSA step, deterministic matrix identities,
same-mode veto and missing/early-eligibility gates. They open no P63 result and
sample no native source. Their passing would not execute the main audit.

Recorded-data audit, only after frozen checker + sealed binding + ROOT review:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P63_independent_raw_audit.py --root . --binding research/P63_independent_raw_audit_input_binding.json --output research/P63_independent_raw_audit/run_001/data/audit.json
```

Use a NEW bounded-runner parent for each separately authorized command, v2
manifest, CPU20/wall30/thread1/log4MiB/scientific4MiB/logical64MiB. The report
uses exclusive file creation and never writes to primary input paths. No raw
data are read by the act of committing these sources/contracts.
