# P58 complete Naive replication: finite numerical and exact-arithmetic PASS

The single authorized full run **PASSes**. All255 nonempty input groups and
all157183 complex amplitudes were evaluated, without pruning, and agree
with the archived creation-polynomial amplitudes. The maximum absolute
amplitude error is1.8735013540549517e-16; independent matrix alignment error
is4.3297802811774664e-17. Every complete source mass passes its5e-10 guard.
All6435 hypergeometric tie scalars and127 independently convolved exact
means agree exactly with the pinned primary archive.

The signed full-B mean is-767/327680. The smallest two-species gap is exactly
**649/327680**, attained by the2+6 splits with smaller groups{0,3},{1,2},
{4,7},{5,6}. Their signed mean is-59/163840. The recomputed decision is
SAME_PHASE_ALL_BIPARTITIONS_SEPARATED. This is a fixed-circuit, fixed-angle,
fixed-observable finite result; arbitrary finer partitions remain untested.
No genuine-order8 witness or useful optimization advantage is concluded.

## Provenance and independent parts

ROOT statically reviewed the frozen source/card/contracts at db573dd and
reviewed the real qualification66d5dcf (six stdlib guards plus five tiny
API/math checks). ROOT then authorized one separate full run from clean
HEAD `66d5dcf2a986595ac9d1b7fe0615dbaf4f6465de`. Source SHA256 remained
`7fe721b9dd27bdb7923558fe4e3e62b799b18570ed524959a9676b9521bd3479`.
No source, backend, tolerance, phase, library version, cap or input changed.
The same-source qualification manifest/report gate passed before work.

All six full-run outputs were committed **before detailed scientific
analysis** in `a3ce1dcb5e7ff551ed5b9002f65e0b0aec12a50e`. The runner had
reported completed/exit0 and the actual v2 validator returned0 before that
seal. This receipt was written afterward from the immutable outputs. There
was no retry, alternate reference, favorable prefix, new draw or QPU call.

The reviewer knew ROOT's candidate result and had reviewed related source
physics before implementation. This is explicitly posthoc, not blind,
held-out, a new graph experiment or independent physical randomness.
Independence concerns the numerical source engine, matrix construction,
state iterator, tie formula and convolution indexing described below.

The independently built matrix uses scalar trig and crossed-bit Walsh
characters in the original port order. It is aligned to the archive within
5e-12, but the independent matrix, not the archived one, is used by the
backend. Each of255 source masks sets its own distinct-single-photon input
Fock state. Own multisets generate every output state for that photon total,
including collisions and reference zeros; there is no probability iterator
threshold, CF filter, fallback, phase fitting or normalization correction.

Local Perceval1.3.0 NaiveBackend.prob_amplitude calls
exqalibur1.4.2 permanent_cx, rather than the primary creation recurrence.
For archived unnormalized coefficient C_n=a+b*exp(i*pi/3), the independently
checked normalized amplitude is C_n*sqrt(prod n!)/(sqrt(8)^r). The source
factorials/occupation alignment, exact weight sum8^r and all complex
amplitudes are checked. Native values are retained even at reference zeros;
the full8-source group alone includes5053 such zeros, none pruned. All
native amplitudes and per-group diagnostics are saved in gzip JSONL after
an independent-matrix header.

This amplitude agreement is a double-precision corroboration at absolute
tolerance5e-10, not an interval proof or a relative-error guarantee. The
following arithmetic checks are exact, using integer archive weights only
AFTER their complete native amplitude corroboration. The source ring
coefficients are not independently reconstructed as exact algebraic values
by this permanent backend.

The second implementation computes ties from the fourth-largest count
threshold and boundary hypergeometric inclusions, not the primary's70
subset enumeration. Single/pair inclusions give each edge crossing average,
and every one of6435 scaled scalar values agrees exactly. Base16 occupation
keys, instead of base9, implement all127 unordered split convolutions via
masks1..127 and their complements. Every one of11083116 pairs is included;
no final output factorial is added between distinguishable species. Full-B,
all127 means/gaps, the minimum and the decision agree exactly. All exact
reconstructed ties and means, not only the minimum, are saved.

## Execution, resources and warnings

Start2026-11-25T14:22:07.439718+00:00; runner completed/exit0,
wall7.702003s. Child CPU6.689109s, wall7.374631250044331s. Python3.11.15,
NumPy2.4.6, Perceval1.3.0, exqalibur1.4.2, macOS26.2arm64. Native maximum
thread readbacks were0 before,1 after configuration,1 after work; all six
thread-environment settings were1. This is an official configured maximum,
not an OS scheduling measurement. The report hashes the backend, Unitary
source, initializer and compiled permanent-engine binary.

Observed Darwin peak RSS was212975616bytes, exceeding the134217728-byte
planned LOGICAL workspace; that projection was not an enforced process-RSS
cap. Interpreter/library/JSON overhead is included in the observed number.
No claim that the process stayed below128MiB, hard RSS bound, affinity or
hardware latency follows. CPU60/wall90/output16MiB caps were unchanged and
not reached. All six output files total2089165bytes.

The declared persistent MPLCONFIGDIR remained unchanged. Stderr preserves
Perceval's default persistent-data access warnings and temporary-folder
fallback. No vendor or cache patch, warm-up, repeated run, credential read
or remote processor was introduced. These are execution observations,
not evidence of a calibrated provider runtime or PNR capability.

Actual runner invocation:

```sh
'/private/tmp/pbp-clean-venv-20261124/bin/python' '/Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py' '--root' '/Users/karimelhoudaigui/Desktop/pasqal/.local/p58-naive-replication' '--contract' 'research/P58_naive_full_contract.json' '--output' 'experiments/P58_naive_replication/run_001' '--input' 'research/P58_naive_replication.py' '--input' 'research/P58_NAIVE_REPLICATION_CARD.md' '--input' 'research/P58_naive_full_contract.json' '--input' 'experiments/P58_same_phase_species/run_001/manifest.json' '--input' 'experiments/P58_same_phase_species/run_001/data/source_laws.json.gz' '--input' 'experiments/P58_same_phase_species/run_001/data/tie_scalars.json.gz' '--input' 'experiments/P58_same_phase_species/run_001/data/summary.json' '--input' 'research/P58_naive_qualification/run_001/manifest.json' '--input' 'research/P58_naive_qualification/run_001/data/report.json' '--input' 'pyproject.toml' '--input' 'requirements-research-lock.txt' '--result' 'experiments/P58_naive_replication/run_001/data/native_amplitudes.jsonl.gz' '--result' 'experiments/P58_naive_replication/run_001/data/independent_ties_and_means.json' '--result' 'experiments/P58_naive_replication/run_001/data/report.json' '--timeout' '90' '--max-output-bytes' '16777216' '--max-cpu-seconds' '60' '--max-threads' '1' '--' '/private/tmp/pbp-clean-venv-20261124/bin/python' 'research/P58_naive_replication.py' '--mode' 'full' '--output' 'experiments/P58_naive_replication/run_001/data'
```

Actual v2 validator invocation (exit0):

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P58_naive_replication/run_001/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p58-naive-replication
```

All eleven declared input SHA256 pairs match before/after. Reference source
laws0efca069..., ties52bb7247..., summary7f82c318... and manifestf03c242c...
remain byte-identical. Qualification artifacts remain unchanged as well.
The numerical worker was explicitly released immediately after the raw seal,
before detailed analysis or this receipt; no additional numerical job ran.

Files under experiments/P58_naive_replication/run_001:

| File | SHA256 |
| --- | --- |
| manifest.json | f319aaf27aaf8c6d1d9152add8cb14f07af95723775d76551502c12f527cf522 |
| data/native_amplitudes.jsonl.gz | 1c3a2f113629ce7cddc4670b6089b4a1691ae30f39e266fbf5ba36a50b4017d4 |
| data/independent_ties_and_means.json | db25a5716798b51c3d2ce2a2d24e2e6731d1d0a2f90b7023017124e6dbec744c |
| data/report.json | 37d5476994571d45a20f3447426ba36cc2a77617c014f34250f2f0db886c886b |
| stdout.txt | 2e226db1e1f9f7a5b92d047b1321e4149f54942d5e1e07468f34687f4060a7ca |
| stderr.txt | f6b8d749925516cd93ff94e5a2a2dbbfa298d03e6f7e97babf6434cda66b3025 |

The prospective 'full pending' qualification receipt is superseded only
for execution status by this completed full-run addendum; historical pinned
cards/contracts are not rewritten. No raw primary, graph, witness or angle
changed. The validated assertion remains finite numerical source-engine
corroboration plus exact tie/convolution arithmetic. It does not establish
arbitrary finer-species convexity, continuous-phase optimality, global or
population performance, novelty, matched total-cost advantage, unknown-optimum
discovery, hardware feasibility or a genuine eight-photon witness.

