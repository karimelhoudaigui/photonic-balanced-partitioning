# P65 independent recorded replay: code-only contract

2026-11-25. Source/fixtures authored before opening any P65 primary output.
At assignment, ROOT had not begun qualification and no P65 graph, count or
outcome existed. Only frozen format/source/spec/contract information is used.
No checker import, AST, test, seed evaluation, graph, matrix calculation,
draw or numerical audit was executed during authoring. The code is frozen
before any primary output may be opened by this reviewer.

Supported producer: original commit
`da4d41800819f35dd8ea299395435ca0bdb8157b`, source SHA256
`a115929779ea50ecd6987f8c63646e95bebc6cc739df3760e6ccbffba0961a4b`.
Spec bytes are pinned by SHA256
`6993da4efe018c80b7fd9021451fad301dd665b1c86c4eac8adab2b1904eeee4`.
The actual later producing run commit is supplied by a sealed binding, not
assumed equal to its source-freeze commit.

## Independent assertion and limits

The checker imports stdlib and NumPy only. It imports no P43/P50/P65 production
module and no prior checker. Reused scalar/hash/JSON patterns are local copies
from the author's P63 audit, with N20/K10 conventions independently replaced.
There is no P63 C6/SPSA/top-k decoder here.

For every case, all eight Cayley matrices are rebuilt by independent symmetric
eigendecomposition of H and its spectral Cayley factors, instead of the
producer's complex linear solve. Weighted row sums and rational scale are
recomputed from the archived adjacency. U/H/parameters/degrees/normalization,
both Gram matrices, transpose symmetry and q masses are checked with absolute
3e-12 tolerance. This is floating matrix consistency, not exact or interval
control of PNR probabilities. No permanent, full Fock law or sampling engine
is constructed.

Topology is NOT regenerated with NetworkX. The two registered case identities,
integer symmetric weights1..5, RR degree6 and the exact PCG64 weight assignment
on the producer's CANONICAL `min/max` sorted edge list are checked. The latter
differs from P63's unspecified RR edge orientation. All subsequent cuts use
the SAME archived adjacency for B and FAST.

All820 metadata roles are reconstructed, including intentional common-start
aliases, optional count/coin/replacement paths, unique/nonzero native count
seeds and FAST roles. Starts, coins and edge weights are deterministic PCG64
recipe replay only; no new DEV start is proposed to the primary experiment.
Repeated independently seeded starts are retained, never required distinct.

The state machine replays every recorded complete 20-count vector, requiring
total10. Each request's sorted ten-port source must equal the PREVIOUS current
state, with a new request/factory for each attempt. Valid collisions are paid
self-loops with no coin/proposal repair. Every CF outcome consumes the owned
coin even when acceptance is one or proposal equals source. Scalar cuts,
acceptance, post-step current, own chain-best and the all-paid incumbent are
reconstructed. Initial4/current40/proposal=n_CF actual calls are distinguished;
eight training resets do not invent eight initial scores.

Eight two-step training fitnesses use exact post-step CURRENT Fraction means.
Selection is minimum with first lexicographic tie, archived before the three
fresh chains. Every fresh chain resets to ITS OWN scored start and best, not
the training/global incumbent. Its eight steps produce one final chain-best;
the primary metric is the exact normalized mean of those THREE values per
case and then equal graph weight. Twenty-four fresh steps are not claimed iid.

The ordered paid ledger is independently assembled from raw/context meter
records, including labels and CPU fields. It has198 components at arm_complete
and199 after the global share in a complete case: preparation/compilation,
one training start, three fresh starts, eleven resets, forty beta preparations,
forty setup/post/prefix triples, eight fitness computations, selection, eleven
chain finalizations, arm finalization and global aggregation share. Factory
prefix is total factory WALL minus ONLY returned backend WALL; its CPU stays
None. Excluded matrix diagnostics/count generation/import/IO/other-arm costs
do not enlarge the B grant. Recorded sums use tolerance1e-8 seconds; this does
not authenticate true clocks, timing causality or practical hardware prices.

FAST uses three-byte masks with FOUR padding bits and ten selected vertices;
every archived best mask gets an independent scalar cut. Times/work and best
cuts must be monotone, full scans consume100 deltas, and counters reconcile.
The last recorded checkpoint no later than the RECORDED CPU budget is eligible;
late audit bests are excluded. The recorded budget must equal B-only WALL minus
actual recorded adapter CPU within1e-8. Timely initialization can veto; survival
needs timely first scan and no early guard. A same FIXED mode must match/beat B
on BOTH graphs; no free per-graph mode portfolio is used. The helper's10k work
and producer's20002 stored-checkpoint guard are kept distinct. Actual unrecorded
FAST proposals/deltas/RNG trajectory and online-time authenticity are unverified.

Only a successful v2 producer with all80 completed/requested B attempts,
80 factories, all four FAST calls, no failure, all12 data files and unchanged
bound inputs can yield `complete_comparison_verified=True` and accepted recorded
fixed-mode veto modes. Every positive_accepted remains False. First-failure or
resource-limited primaries stay inconclusive; readable prefixes are audited
without forcing80. Incomplete JSON/gzip tails are reported, not repaired.
Complete-case ledgers are fully reconciled; partial failed-attempt finalizer
ledgers are retained but not certified as complete by this checker.

## Freeze, binding and provenance

ROOT must inspect and freeze the checker/fixtures/contracts before this
reviewer opens any primary output. Then ROOT seals the primary and creates
`research/P65_independent_raw_audit_input_binding.json`, schema1:

```json
{
  "schema_version": 1,
  "primary_source_commit": "da4d41800819f35dd8ea299395435ca0bdb8157b",
  "primary_source_sha256": "a115929779ea50ecd6987f8c63646e95bebc6cc739df3760e6ccbffba0961a4b",
  "checker_source_sha256": "<frozen checker actual SHA256>",
  "producer_commit": "<actual commit from sealed primary v2 manifest>",
  "producer_manifest": "experiments/P65_cayley_markov_stage/run_001/manifest.json",
  "data_directory": "experiments/P65_cayley_markov_stage/run_001/data",
  "artifacts": [
    {"path": "<primary manifest>", "sha256": "<actual hash>"},
    {"path": "<EACH existing primary data file>", "sha256": "<actual hash>"}
  ]
}
```

Placeholders are not observed evidence. At most12 declared data files plus
manifest are permitted. All existing data files, including failed partials,
must be listed. All paths must be relative regular unsymlinked project files.
Hashes are checked before parsing scientific content and again afterward.
The producer's v2 result hashes and exact17-input closure, unchanged before/
after hashes and known source/spec/helper hashes are reconciled. Standard
v2 manifest validation and ROOT provenance review remain separate requirements.

The committed execution JSON is UNBOUND and cannot authorize an audit.
ROOT creates a NEW bound contract copy, adding itself, binding, primary
manifest and every existing data file to execution_artifacts and the runner's
matching repeated --input list. Retain checker/MD/scaffold/tests/instructions/
dependency inputs. Binding may supply actual paths/hashes only, without
changing checker, tolerances, scientific scope or caps after seeing results.

## Separately authorized commands and caps

Nine deterministic fixture functions are authored, not collected or run.
They use small hardcoded weighted graphs, generic small transition counts,
two/four-mode spectral identities, packed masks, exact fitness ties and gate
logic; one test evaluates only metadata hashes for820 roles. No primary output,
native backend, true20-mode sample or DEV graph is opened by fixtures.

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest -q tests/test_p65_independent_raw_audit.py --junitxml=research/P65_independent_raw_audit_preflight/run_001/junit.xml
```

Only after frozen source, sealed binding and ROOT's separate audit authorization:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P65_independent_raw_audit.py --root . --binding research/P65_independent_raw_audit_input_binding.json --output research/P65_independent_raw_audit/run_001/data/audit.json
```

Separate NEW v2 bounded-runner parents: CPU20/wall30/thread1/log4MiB,
scientific4MiB, planned logical64MiB, one numerical worker, zero failed
retries. Inputs<=32MiB, decompressed raw<=8MiB, raw line<=1MiB characters,
at most32 short discrepancy examples. Summary and one separate FAST payload
are held at a time; no full state kernel/Fock table is allocated. Logical
workspace is a plan excluding library resident images, not a Darwin hard-RSS
claim. Resource/output failures remain inconclusive with original evidence
retained. No retry, additional primary draw, cap expansion, optional arm,
paper edit or QPU action is authorized by this code-only artifact.
