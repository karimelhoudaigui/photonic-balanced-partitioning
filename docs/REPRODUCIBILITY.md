# Reproducibility

Use Python3.11 and the exact extras in pyproject.toml. The root requirements-research-lock.txt additionally pins the previous research environment; install the project extras afterwards to include the publication PDF checker. No Qwen CLI is a Python dependency.

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-research-lock.txt
.venv/bin/python -m pip install -e '.[all]'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m pytest tests/ -q
.venv/bin/python scripts/build_publication.py --check
```

The tested suite includes independent graph enumeration, anti-oracle losses, permanents, normalization, HOM/collisions, Perceval comparisons, internal-state phases/loss sectors, historical-data reconstruction, bundle integrity and offline job/result handling. Perceval may warn about a sandboxed persistent cache; it falls back locally and no device account is required.

## Regenerate evidence and paper

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python scripts/reconcile_experiments.py \
  --archive-root . --output /tmp/pbp-reconciliation-new
.venv/bin/python scripts/build_publication.py
.venv/bin/python scripts/build_publication.py --check
tectonic --untrusted --keep-logs paper/main.tex
.venv/bin/python scripts/verify_manuscript.py --receipt /tmp/pbp-build-check-new.json
```

Choose a fresh reconciliation destination. This parses archived records; it does not relaunch756 optimization runs. A new run's timing/provenance fields can differ even when its scientific aggregates agree. Tables and figures are generated from the accepted source and analytic definitions. The manifest pins input/output/generator hashes; --check rejects stale or changed outputs. PDF metadata for generated figures is fixed.

Tectonic0.16.9 is an external build tool, installed locally using Homebrew. Its first build downloads fonts and TeX packages; subsequent cached builds need no device/network access. The build checker reads the final PDF/log, citation/input inventory and source hashes. It detects undefined references and significant layout failures; it is not a scientific referee.

## Reproduce offline circuit preparation

```sh
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
 .venv/bin/python qpu/offline_pilot_20261124_v1/reproduce.py \
 --output /tmp/pbp-offline-pilot-new
```

This creates eight immutable stage/analysis bundles, three fixed circuits and two synthetic count examples. Source/config/graph/unitary/reference hashes and known/unknown attempt semantics are preserved. All network sockets/DNS are denied by the CLI. A fresh supervisor reproduction is retained in results/validated/offline_pilot_2026-11-24_supervisor/. It is not hardware data.

Historical manifests are checked against pinned Git blobs or archived source snapshots. Later edits of pyproject/status do not change historical evidence. The numerical census identifies unresolved source pins, prior failures and excluded unattributed copies. Do not rerun old fixed-output drivers in place. make clean removes only explicitly named LaTeX auxiliaries, never results or the compiled PDF.

## CI and reviews

The local workflow .github/workflows/research.yml runs pinned tests, data-generation integrity checks and a TeX/PDF check without QPU access. CI configuration is supplied; a remote CI run is not claimed unless its actual result is linked.

Reviewer artifacts under reports/manuscript_review_2026-11-24/ pin the manuscript snapshot, disclose scopes and prior involvement, preserve raw findings and record their dispositions. Reviews are distinct from tests, proof, literature novelty and actual hardware calibration.


## Validated recovery release — 24 November 2026

The release was installed in a NEW isolated Python3.11.15 venv: all37 locked dependencies match and pip check passes. The integrated release suite returns **484 PASS**, with six Perceval persistent-cache fallback warnings. Command/stdout/stderr and before/after source hashes are retained in reports/recovery_2026-11-24/release_clean_pytest_receipt.json and adjacent text files.

P40's original driver is an immutable historical entry point with fixed-path/ancestry guards. Use [the separate portable replay](P40_REPRODUCTION.md) to recompute its45 cells/five SLOS circuits into a fresh output; do not edit or bypass the original guard. The supervisor replay in a clean venv on scientific-recovery-publication also returns REPLAY_MATCH with zero archived-law difference.

The original isolated worker commits are preserved in reports/recovery_2026-11-24/isolated-worker-history.bundle. It has a6154b46 base prerequisite and three original branch refs. In a full checkout containing that base, `git bundle verify reports/recovery_2026-11-24/isolated-worker-history.bundle` checks the bundle without contacting a remote. This preserves original pre-execution contract/source identifiers across later cherry-picks. A shallow checkout may need the base history first.

Remote CI is configured but was not triggered here. Local YAML syntax, full tests, archive/data checks, compilation and PDF verification ran successfully; this does not claim a tested Linux CI execution.

## Subsequent Lucy/TGCC delivery

The [separate delivery receipt](../reports/LUCY_TGCC_DELIVERY.md) records505
passing tests after adding21 mock-transport tests. The scientific paper and
historical raw evidence remain byte-identical. [Lucy/TGCC instructions](LUCY_TGCC.md)
distinguish offline planning, a read-only live-spec query and an explicitly
authorized single QPU acquisition. These remote operations were not run here.
The CI now fetches full history; archived worker refs still require the
preserved bundle when inspecting their original commits.

The [actual GitHub Linux run for c8b6161](https://github.com/karimelhoudaigui/photonic-balanced-partitioning/actions/runs/45400833067)
now passes pinned installation, the suite, archive checks and TeX/PDF compilation.
Its [status snapshot](../reports/lucy_tgcc_2026-11-24/github_ci_c8b6161.json) is
preserved. The older recovery description above records the state before that
first remote run. The source archive and Laurent packet are indexed in
[deliverables/README.md](../deliverables/README.md); the extracted packet passed
its46 selected tests with the previously installed pinned environment.
