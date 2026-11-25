# P47 quarantined post-hoc headroom: one bounded float64 MILP run

2026-11-25. Outcome: **conditional on floating point solver bounds**, with
three solver-optimal cases and one resource-limited unresolved case. This
is evaluation of FOUR ALREADY CLOSED P47 graphs, not training or a new
optical mechanism. No P48 input was opened and no new partition/assignment/
mask/hash of a partition was exported. The P48-B card had already been
frozen at e30f75ced16e61fbb69ebe2f6d9509f90a7aa4ae before this diagnostic.
These post-hoc scalar outcomes must not select its families or settings.

The complete preparation was committed at
`b394a0d4e801887b85ec08d1756102e30b45e4b8` BEFORE coordinator permission
and the sole run. Code SHA256:
`4d72248d224da423097f85829618e90d61f0cc0bcb05d7cca6da9cbc47542680`.
The preregistered model/protocol is unchanged. Only run_001 was executed;
there was no retry, expanded time limit or substitute graph.

## Observed scalar results

| Closed case | Frozen Cref | B best | Classical best / all-method best | HiGHS dual bound estimate | Solver incumbent | Status |
|---|---:|---:|---:|---:|---:|---|
| n26 ER4702601 |154|146|146|146|146|0, declares optimal |
| n26 RR4702602 |37|35|35|34.99999999999995|35|0, declares optimal |
| n34 ER4703401 |359|359|351|297|351|1, native 5s limit |
| n34 RR4703402 |66|66|49|48.99999999999994|49|0, declares optimal |

Solver statuses and bounds are FLOAT64 estimates, not exact or interval
certificates; tiny nonintegral dual values are kept in raw. We do not round
them into an exact proof. Each solver incumbent's binary/balance/x0
conditions and direct INTEGER cut scalar were checked in memory. Only
that scalar survives; the assignment was deleted without serialization.

The observed best/classical costs coincide with the solver's primal/dual
values to numerical tolerance on three cases. This is evidence of possible
benchmark saturation there, not a new exact optimum theorem. On n34 ER,
the best known scalar351 and dual estimate297 leave the question unresolved;
54 is a gap to an estimated LOWER BOUND, not a measured distance from optimum.
The recorded relative solver gap is .15384615384615385. The native-call
elapsed wall time is 5.00543s including wrapper overhead; the configured
native HiGHS limit remains5s. This time-limited case is fully retained.

Independently of trusting a solver lower bound, P47 already recorded a
feasible classical cut351 on n34 ER and49 on n34 RR, versus B359 and66.
Those finite feasible comparisons leave at least8 and17 units respectively
below B's observed result. The diagnostic does not explain away all
non-improvement as saturation. Conversely, B reaching the same value as
classical searches on the N26 cases does not prove an optical advantage.
The previous eight-path comparison with anneal remains unchanged.

## Actual execution, resources and provenance

The Mathbox v2 runner started at2026-11-25T04:44:29.345240Z on the CLEAN
preregistration commit, reported status completed/exit0 and6.353376s wall.
Measured after the script environment guard:5.630822s process CPU,
5.701847s wall. Global limits were CPU25s/wall40s/thread1/log1MiB; no hard
macOS affinity/memory limit is claimed. Nine exact execution artifacts
were hashed unchanged before/after; the six copied P47 archives retain
their original hashes. Numerical versions observed at runtime were
Python3.11.15, NumPy2.4.6 and SciPy1.17.1.

The bundled native HiGHS options object read back threads1/parallel off.
Every model supplied threads1, boolean parallel=False (converted to native
off by the pinned wrapper) and fixed random_seed47047. The public SciPy
warning about unrecognized forwarded option names is preserved in each
JSON row; there were no native-wrapper ignored-option warnings, which
were configured as errors. Sparse CSC indices and indptr are recorded
int32 in all four solves. stderr is empty; the captured forwarding warning
belongs in JSON, not stderr. No optimum vector or raw OptimizeResult is
printed, and disp is false.

Actual child argv, also recorded by the runner manifest:

    /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P47_headroom_quarantine/solve.py --output experiments/P47_headroom_quarantine/run_001/data --execute-posthoc-p47-only

It was launched by the installed Mathbox computation-audit
scripts/run_experiment.py with root equal to this isolated replication
worktree, contract experiments/P47_headroom_quarantine/contract.json,
the EXACT nine execution_artifacts repeated as --input, output
experiments/P47_headroom_quarantine/run_001, two --result paths
data/records.jsonl and data/summary.json under that run directory,
--timeout40 --max-output-bytes1048576 --max-cpu-seconds25 --max-threads1.
No environment/command was copied from an untrusted prior manifest.

The subsequent actual validation command was:

    /private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P47_headroom_quarantine/run_001/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication

It exited0: “valid evidence record (run status: completed); mathematical
interpretation requires review”. This records provenance, not exact
optimality. No new sampling, QPU, credentials, training oracle or held-out
evaluation was performed. No original P47 source/raw was modified.

Result hashes are recorded in the run manifest; this report is separate
from immutable data/records.jsonl, data/summary.json and runner logs.
No statement here changes a paper or upgrades P47's exploratory status.
