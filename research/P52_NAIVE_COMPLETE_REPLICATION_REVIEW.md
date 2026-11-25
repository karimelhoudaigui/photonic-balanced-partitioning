# P52 complete finite amplitude/probability replication

Verdict: **FINITE_FLOAT64_AGREEMENT, all4 phases and all6435 occupations**.
The uniquely authorized25,740 Perceval Naive permanent calls completed.
Maximum absolute complex-amplitude error9.812001025258123e-17 and maximum
absolute probability error9.540979117872439e-18 are below the predeclared5e-10
tolerance. No output, collision, numerical zero or phase cell was filtered.

This addendum supersedes historical P52 draft/proposal statements that the
complete Naive physical-probability check was PENDING. Those historical
records and primary raw data are preserved. It does not revise P52's negative
mean-kernel outcome or turn the replication into a held-out optimizer test.

## Independence and finite interpretation

Primary reference data are the immutable six files from
`762877a65125e5411e10906ccdb7f64ff280d840`. The primary amplitude engine is a
creation-operator dynamic program; the replica uses Perceval1.3.0
`NaiveBackend.prob_amplitude`, which forms the repeated-row submatrix, calls
exqalibur's complex permanent and divides by occupation-factorial square
roots. No primary project module/function is imported by the replica. The
independent multiset enumeration checks complete occupation-set equality and
aligns vectors by count tuples rather than array indices.

The circuit is reconstructed separately by a scalar bit-parity/phase formula.
That matrix is checked against the archived U before each phase. The actual
Naive backend receives the archived numerical U **after this check**, so the
amplitude engines compare identical matrix inputs. This is deliberately a
finite engine replication with independently checked matrix conventions, not
an independent new draw of a circuit. Amplitudes are compared directly with
no global/state-dependent phase alignment. No probability renormalization is
performed; all four laws' numerical masses are retained.

I had previously audited the primary code and knew ROOT's reported negative
mean outcome before writing this replication. Thus the independence is of
engine/enumeration/matrix reconstruction, not author blindness, a preregistered
prediction of P52 or external third-party review. Source/contract/cases were
frozen before imports. Two earlier wrapper failures and the two distinct
successful API qualifications are preserved, not silently replaced. ROOT read
the complete run004 receipt before authorizing this full production run.

## Complete results

| Phase | Permanent calls | Max amplitude error | Max probability error | Half-L1 numerical residual |
|---|---:|---:|---:|---:|
| 0 | 6435 | 5.551115123125783e-17 | 9.540979117872439e-18 | 2.8734745702654885e-16 |
| pi/4 | 6435 | 9.812001025258123e-17 | 7.15573433840433e-18 | 2.9053907717180305e-16 |
| pi/2 | 6435 | 8.439797369737068e-17 | 9.540979117872439e-18 | 2.7668839441830073e-16 |
| 3pi/4 | 6435 | 7.253204108099275e-17 | 6.071532165918825e-18 | 2.798562976410318e-16 |

The report calls half-L1 `TV_numerical`; these are floating residuals between
the stored unrenormalized arrays, not rigorous interval bounds on mathematical
TV. Naive masses range from0.9999999999999983 to0.9999999999999987; every mass
passes the unchanged absolute5e-10 gate. Largest matrix discrepancy is
2.7755575615628914e-17, unitary residual1.1102230246251565e-16, below5e-12.
Worst count tuples and reference masses remain in the report rather than
being selected away. Each of the four NPZ files stores complete independent
amplitudes/probabilities and aligned primary vectors, plus both matrices;
`occupations.npy` supplies their complete common tuple indexing.

This supports the ideal finite physical source/phase/factorial normalization
used by the primary creation DP at these four circuits. It does not re-audit
the primary decoder, phase Monte Carlo confidence, LP/statistics, tails or
full-law classical replacement; nor does it prove a universal simulator,
optimization gain, scalable speedup, novelty, hardware feasibility or loss
calibration. The negative P52 classical mean matches remain negative.

## Actual bounded execution and provenance

The full child ran on clean
`d7f49f5a1077a4fcd1bce821da941744ad67b1a7`, after run004 was committed.
Source SHA256 `2d590822218df9300457923d6fc9f619d15666eae522b96b91aafebd88b5a55e`
and all eleven execution inputs were unchanged. CPU20/wall30/log4MiB limits
and six numerical environment variables1 were unchanged. Official native
`Config.compute_max_thread_count` read0 before assignment,1 after assignment
and1 after work; ps observations remain unavailable, with no OS scheduling
claim. Actual versions: Python3.11.15, NumPy2.4.6, Perceval1.3.0, exqalibur1.4.2.
Native binary hash is the same as qualification:
`b4687bc81b37cb447eb0c9c4fa89523da7feed8584a31ca74798ac3bcee06749`.

Actual runner command (isolated worktree working directory):

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P52_naive_full_contract.json --output experiments/P52_naive_validation/run_001 --input research/P52_naive_replication.py --input tests/test_p52_naive_replication.py --input research/P52_naive_validation_contract.md --input research/P52_naive_qualification_contract.json --input research/P52_naive_full_contract.json --input experiments/P52_collective_phase/run_001/manifest.json --input experiments/P52_collective_phase/run_001/data/geometry.npz --input experiments/P52_collective_phase/run_001/data/theta_0.npz --input experiments/P52_collective_phase/run_001/data/theta_1.npz --input experiments/P52_collective_phase/run_001/data/theta_2.npz --input experiments/P52_collective_phase/run_001/data/theta_3.npz --result experiments/P52_naive_validation/run_001/data/report.json --result experiments/P52_naive_validation/run_001/data/progress.json --result experiments/P52_naive_validation/run_001/data/occupations.npy --result experiments/P52_naive_validation/run_001/data/replica_theta_0.npz --result experiments/P52_naive_validation/run_001/data/replica_theta_1.npz --result experiments/P52_naive_validation/run_001/data/replica_theta_2.npz --result experiments/P52_naive_validation/run_001/data/replica_theta_3.npz --timeout 30 --max-output-bytes 4194304 --max-cpu-seconds 20 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode full --output experiments/P52_naive_validation/run_001/data
```

Start2026-11-25T11:51:26.340337+00:00, runner completed/exit0, runner
wall2.872489s. Child reports CPU1.841588s, wall2.59547725s and
DarwinRSS170737664B. Process CPU/RSS are not aggregate descendant CPU or a
hard address-space limit. Cache was preexisting; no cold/warm resource claim
or outcome-driven cap/model/algorithm adjustment is made. All ten generated
files including logs/manifest total1,378,987bytes (`wc -c` actually checked),
below4MiB. The exclusive numerical slot was released immediately on outcome
inspection. There was no retry or additional numerical work.

## Sealed output hashes

All files below `experiments/P52_naive_validation/run_001/`:

| File | SHA256 |
|---|---|
| manifest.json | 356d7f487b0a09b8250084c9f1202b73570cb63199b024ea704603f6053dc8e7 |
| data/report.json | c9aab39b0b992c5c9f82851d0ee2dd6dfbc825b268d951c9b18c9256395af8f4 |
| data/progress.json | 3adab32fdd96add3d046403b25057a9c1b29d0a103f2aeea865ba2a6e244a76f |
| data/occupations.npy | 0416e283b63e6823b89f6c012e66d06b1f7006aa6e835ac4716f91bd1654b7dc |
| data/replica_theta_0.npz | e2dcda88321127e750e654b0a6979f5c277b6f4f5ae3e17976a0c2143e691302 |
| data/replica_theta_1.npz | 1ac88429954b6ef028d28c19f5aa360148f0f8dd7dd05de05ed3089a5071cb1d |
| data/replica_theta_2.npz | b03ce0747788f9ae02ebc11e476234954da130be9cead790e55ec0bf22daf3c4 |
| data/replica_theta_3.npz | f613395c0e930d8d85d8581d4ccfb46d0f7f25b068a6989e41b5a5e245be7719 |
| stdout.txt | 25cdaadacbfd9c8df9089f979925d410faa1c13ef689c4c25e240a733e9434d6 |
| stderr.txt | f6b8d749925516cd93ff94e5a2a2dbbfa298d03e6f7e97babf6434cda66b3025 |

Actual Mathbox v2 validation returned0, status completed:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P52_naive_validation/run_001/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication
```

The eleven runner input hashes match before/after, as do all six application
reference pins. No historical primary raw or shared source was rewritten.
The schema/closure validation and finite float agreement are separate from
an exact mathematical proof; P53's exact algebraic source audit is separate.
