# P52 run_003: API qualification passes; native threads unverified

Exact verdict: **API_QUALIFICATION_PASS_NATIVE_THREADS_UNVERIFIED**.
Seven guards and eleven small analytic/API checks passed with a durable report.
This does not authorize or execute the full25,740 probability replication.
Runs001/002 and the first administrative argument rejection remain unchanged.

ROOT reviewed the JSON/cache correction and authorized this one exclusive-slot
qualification on clean `7745bf361ea92379aa00b45f4e87daad31f4cb9f`. Source SHA256
`a68f969ff3b943c5d2d3bd475652a260caf446469aa913cd4c476b347fa4be52`.
The runner invocation is the actual command recorded in the run_001 receipt,
with run_003 substituted in its output and both declared-result paths; the
same eleven --input paths, pinned Python, CPU20/wall30/thread-env1/log4MiB
arguments were used. Child argv:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode qualify --output research/P52_naive_qualification/run_003/data
```

Actual start `2026-11-25T08:45:50.266006+00:00`, runner status completed, exit0,
runner wall18.162023s. JUnit/stdout report seven guards PASS in0.03s, no errors,
failures or skips. The eleven report comparisons are:

| Check | Absolute error |
|---|---:|
| HOM collision-free amplitude zero | 0 |
| HOM bunched amplitude/output factorial | 1.1102230246251565e-16 |
| Complex2x2 orientation at phi=.37 | 1.1102230246251565e-16 |
| Complex2x2 collision-free permanent | 1.6711069443220838e-16 |
| Identity8 single CF amplitude | 0 |
| Vacuum amplitude | 0 |
| Native known complex2x2 permanent | 0 |
| Independent U8 unitary residual, each of four phases | 1.1102230246251565e-16 |

The largest recorded residual1.6711069443220838e-16 is below the predeclared
5e-10 absolute threshold. These are finite float64 checks, not intervals.
No production-family U8 permanent, sampling draw, primary probability loading,
optimization or hardware call occurred.

The report records actual imported versions: Python3.11.15, NumPy2.4.6,
Perceval-Quandela1.3.0, exqalibur1.4.2, pytest8.4.2. Actual source/binary SHA256:

| Artifact | SHA256 |
|---|---|
| Perceval `_naive.py` | aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d |
| Perceval `unitary_components.py` | 2f4bacd1d3d5c919b32eaaf28d1881a5f49be608ffca4be2ee53886a149786df |
| exqalibur compiled extension | b4687bc81b37cb447eb0c9c4fa89523da7feed8584a31ca74798ac3bcee06749 |
| exqalibur package initializer | 6a6ac3b31ef4ebc06ef95c2fa0aed19516e9c72bbe4e59b05aea1f2055686690 |

Native API observation matters: `inspect.signature` is unavailable for this
pybind builtin, but its actual docstring gives `permanent_cx(M, ptype='')` and
names Glynn/Ryser algorithm choices. It also explicitly points to
`exqalibur.Config` for allowed CPU thread control. No Config setting was
discovered/applied by the frozen source. The report's empty list of exports
whose names contain "thread" does **not** show absence of a Config-based
setting. All three ps observations are unavailable with EPERM. All six
conventional numerical thread environment variables were1, but that does not
establish the native permanent worker count. ROOT was notified of the newly
observed Config documentation before any full-run approval; it requires
inspection/qualification rather than an invented argument or vendor patch.

The child reports CPU1.442988s, wall17.818172959s and Darwin peakRSS166264832B.
CPU is the child's Python-process measurement, not aggregate descendant CPU.
The runner enforces per-process CPU and wall limits, not unsupported Darwin
affinity. Process RSS includes imported packages and is distinct from the
individual numerical-array cap64MiB. No cold/warm speed comparison is made.
The newly created persistent MPLCONFIGDIR is exactly the declared worktree
`.local/mplconfig`; report records preexisting=false. Stderr retains fontconfig
and Perceval fallback-folder warnings. No cache outcome was used to adjust a
cap, algorithm or parameter.

Durable artifacts under `research/P52_naive_qualification/run_003/`:

| File | SHA256 |
|---|---|
| manifest.json | 81b83e7b4896022bdfba667dce5a2238f12d37b37f4d108bee080356d2959116 |
| stdout.txt | 2d1e39e91dd08afd18d3884d732d772bfdd3bf16730279e81e6cd6a06b9e5dfb |
| stderr.txt | dd65094b41d527e777b6c4728c984494495743689a154eacc5573936bd5102cb |
| data/report.json | 66d4a2a16fc154f35e1b3d53631a6b20ae01e450d0e0d9af8454fc56b5feaf58 |
| data/guard_junit.xml | 3417ecbf044e483c661eaac33073c7d45b60828c00db0c452afadd0b08c26301 |

All eleven runner input SHA256-before/after pairs agree; the application's six
reference hashes agree too. Actual validation command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py research/P52_naive_qualification/run_003/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication
```

It returned0: valid evidence record, status completed. This checks provenance
closure/schema and does not independently establish the math beyond the
specific checks above. The exclusive slot was released after completion and
reading the report. No full run, native Config modification, new calculation,
retry, physical advantage or novelty conclusion followed.
