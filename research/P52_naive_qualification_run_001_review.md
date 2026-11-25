# P52 Naive API qualification: failed before scientific imports

Verdict: **qualification NOT EXECUTED to completion; no API/physics PASS**.
This is an infrastructure observation, not a disagreement with primary P52
probabilities. No full probability replication has been authorized or run.

Source and all eleven inputs were clean at
`d96009fe3174ca1350bcebecdf2d499ded7f475b`. ROOT reviewed this exact source and
authorized only the tiny qualification in the exclusive numerical slot.
Source SHA256:
`ca46ea81afa171cfd528e9ca61ee48e50bcd9bc99edd80b54e58097a46de4de4`.

The first runner invocation was rejected before creating a directory or
starting a child: I incorrectly supplied project-relative result names as
`data/report.json` and `data/guard_junit.xml`. Runner exit2 said:
`declared result must be inside the fresh output directory: data/report.json`.
`ls -ld research/P52_naive_qualification/run_001` then confirmed that the
directory did not exist. This administrative argument error was disclosed to
ROOT immediately. Only the two result arguments were corrected to their full
project-relative paths. No calculation had occurred and no source, input,
parameter, cap or numerical method was changed.

The actual child started once at `2026-11-25T08:31:23.178899+00:00`; runner wall
time0.092146s, exit1, status`failed`. It reached the byte-hash checks and fresh
directory creation, then raised `PermissionError: [Errno 1] Operation not
permitted: 'ps'` in `thread_snapshot_before_import`. The sandbox forbids this
local process observation. The source placed the first observation before its
try/finally block, so no application report was produced. This is my wrapper's
robustness defect. Five guard tests and eleven numerical checks were not
reached; neither NumPy nor Perceval was imported, and no permanent was called.
No retry, vendor patch, source amendment or cap increase followed. The slot
was released immediately after inspection of the preserved stderr.

Executed runner command (working directory the isolated worktree):

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P52_naive_qualification_contract.json --output research/P52_naive_qualification/run_001 --input research/P52_naive_replication.py --input tests/test_p52_naive_replication.py --input research/P52_naive_validation_contract.md --input research/P52_naive_qualification_contract.json --input research/P52_naive_full_contract.json --input experiments/P52_collective_phase/run_001/manifest.json --input experiments/P52_collective_phase/run_001/data/geometry.npz --input experiments/P52_collective_phase/run_001/data/theta_0.npz --input experiments/P52_collective_phase/run_001/data/theta_1.npz --input experiments/P52_collective_phase/run_001/data/theta_2.npz --input experiments/P52_collective_phase/run_001/data/theta_3.npz --result research/P52_naive_qualification/run_001/data/report.json --result research/P52_naive_qualification/run_001/data/guard_junit.xml --timeout 30 --max-output-bytes 4194304 --max-cpu-seconds 20 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode qualify --output research/P52_naive_qualification/run_001/data
```

Durable outputs, unchanged:

| File in `research/P52_naive_qualification/run_001/` | SHA256 |
|---|---|
| manifest.json | c3cd30053b0426fbc14dbf4234bb4ac40c2deaf51bd08b26f307054698c0425b |
| stdout.txt (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| stderr.txt | efdeb800f4b6038e593ae8c66b65e60970aa453c6ebc2327afaf7c8d28f72272 |

The Mathbox v2 validator was actually run:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py research/P52_naive_qualification/run_001/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication
```

It returned exit0: `valid evidence record (run status: failed); mathematical
interpretation requires review`. This validates the failed record's schema and
hash closure, not the mathematical checks. All eleven SHA256-before/after
pairs agree. Both declared scientific report/JUnit files are correctly listed
as missing. The environment software versions in the manifest are contract
declarations plus the actual runner Python version, not an observed successful
Perceval import. Native thread signature/behavior is still unqualified.

Any future attempt requires a separately frozen observation-only robustness
correction, a fresh output directory and ROOT authorization. Historical
`run_001`, the original source and all primary raw probabilities remain intact.
