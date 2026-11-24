# Portable reproduction of the frozen P40 calculation

P40 is a known-model, four-mode/two-photon calibration prediction check. A
reproduction does not create a new physical calibration, optimization campaign,
quantum-advantage result or hardware measurement. The mathematical population
and predictions remain exactly those in the original advance contract.

## Historical driver limitation, preserved

The original `experiments/scripts/validate_sharpness_pilot.py` deliberately
requires its one historical output path, rejects an existing directory, checks
ancestry of contract commit `efd1718a6a8b8e8ffac1ad84360566bf4346648a`, and
requires that exact contract Git-log commit. After cherry-picking into an
integration branch, identical source bytes need not have that ancestry or the
same last-modifying commit. The archived driver therefore is not a portable
rerun entry point. This is a reproducibility limitation of that entry point,
not a failure of the archived numerical comparison.

The executed driver, original contract and every original result file remain
byte-identical and keep their existing publication pins. No historical guard
is patched, mocked, removed or bypassed. The new entry point is a separately
implemented replay that does not import or invoke the historical driver. It
authenticates that driver's bytes and the old data before reading them.

## New replay command

From a checkout containing the pinned source/archive and project dependencies:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/pasqal-mpl-noise PYTHONDONTWRITEBYTECODE=1 /path/to/python scripts/replay_sharpness_pilot.py --output results/validated/a_fresh_P40_replay
```

`--output` is required. Use a fresh sibling directory for each authorized
reproduction; an existing output is rejected before physics. Destinations
inside historical P40 data, protected project source/history directories, or
an existing campaign below a results directory are rejected. Existing
results/ and results/validated/ containers may hold a new sibling. A fresh
out-of-tree output is supported; its manifest records the common evidence
root needed to resolve input/output paths. Symlinks are resolved before the
destination checks.

The script resolves its source checkout from its own file, uses that checkout's
noise package, and records the actual invocation directory, worktree, branch,
Git commit and source hashes. Git ancestry and historical Git-log identity
are not requirements. The original contract SHA256 is
`30dbbdae5aa2d0c89eb936f7700e5808cde49f215c5118011f10f8fd2e70c4a2`;
the executed historical driver SHA256 is
`2e9dba7c14beafd37901dc1917f59a7354a84dbfa0d45ccdfee09adb4d0c01d0`.
Those and all four old result-file hashes must match before use.

The new execution reconstructs five Rx/PERM/split circuits, calculates five
local Perceval SLOS ideal laws and exactly 45 noise-module Gram/loss laws at
the registered parameters. The x=0 cells supply their distinguishable
controls. It compares every new all-sector law to the original archived law,
checks normalization, circuit unitarity, the original predictions and the
ideal SLOS references at 1e-10. No sampling, fitting or source selection occurs.
Limits are CPU 60 seconds, wall 90 seconds and one BLAS/OpenMP thread.

New files are raw.jsonl, circuits.json, summary.json and manifest.json. They
are explicitly marked **P40_REPLAY**. A completed match is reported as
`REPLAY_MATCH`; it is not the original run or its chronology. The manifest
records the real current context and before/after hashes, including original
data hashes. It never relabels a cherry-picked checkout as the historical
contract execution. Float64 results remain non-interval-certified estimates.

For the repository reproduction recorded here, the actual output argument was
`results/validated/P40_replay_2026-11-24/` in the isolated recovery physics
worktree. This directory is a new record and must not be overwritten. The two
tests read the saved replay and check its complete-law agreement with the
archive; destination-rejection tests do not launch another optical run.

This removes the portable-entry-point obstruction while preserving the
original evidence. It does not settle real-device loss/internal overlap,
PNR availability, source/attempt calibration or QPU suitability. None of those
quantities was measured, and no remote processor is used.

## Actual replay receipt

The single optical replay returned `REPLAY_MATCH`: 45 matching cells, five
circuits, CPU 1.009944 seconds and wall 2.297685916 seconds. Maximum differences
were 0 for archived full noise laws, 4.163336342344337e-17 for SLOS versus the
archived ideal laws, and 9.71445146547012e-17 for the scalar predictions.
Normalization error was at most 2.220446049250313e-16 and unitarity error at
most 1.1102230246251565e-16. These are observed floating-point residuals.

The actual command, executed once from the isolated worktree, was:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/pasqal-mpl-noise PYTHONDONTWRITEBYTECODE=1 /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python scripts/replay_sharpness_pilot.py --output results/validated/P40_replay_2026-11-24/
```

The manifest truthfully records parent commit
`ab119952c06160d2ecf433e405257d2f21e1542c`, branch
`recovery/physics-20261124`, the absolute worktree and `dirty: true`: this
new replay source and its evidence had not yet been committed. Its executed
source identity is the SHA256 below; a later delivery commit does not replace
that actual run context. The historical six pinned files have identical
before/after hashes.

| New artifact | SHA256 |
|---|---|
| `scripts/replay_sharpness_pilot.py` | `d62123881ef77c29424fd0401a3c6f10c103d61578868d4f7a3cd622563d2496` |
| `raw.jsonl` | `e0936677c3d3f94ad94534bac322825119298106a2a57e1b02a45414bd33db41` |
| `circuits.json` | `2ce9c3a6bf954a10e568ed25e5c95741a92a8afc65b6c3192115f7464563bbc6` |
| `summary.json` | `db36a1e6debe33f6b1cd4a5eda6e20cb8fca9ae0fde3978257e18cc720fa0ee8` |
| `manifest.json` | `9576580108a6e97c796112b0765b7009eb36c3a53ba3592a525ed47a47881a2c` |

The Mathbox computation-audit `validate_manifest.py` accepted this manifest
with `--root .`. `pytest tests/test_sharpness_replay.py -q` passed both tests;
these read the saved evidence and exercise rejected destinations without
another optical replay.

The complete test suite materialized in this sparse worktree also passed:
332 tests in 2.81 seconds, with six Perceval local-storage fallback warnings.
It was run with the same four thread limits, `MPLCONFIGDIR` and bytecode
settings as above, plus `PYTHONPATH=src`, through this bounded Python command:

```sh
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -c 'import resource,subprocess,sys; resource.setrlimit(resource.RLIMIT_CPU,(30,30)); p=subprocess.run([sys.executable,"-m","pytest","tests/","-q"],capture_output=True,text=True); print(p.stdout[-3000:]); print(p.stderr[-1000:]); raise SystemExit(p.returncode)'
```

This suite result covers this worktree's available tests; integration of
other branches and their additional tests remains a separate check.
