# Separate records in this directory

The root `check.py`, `manifest.json`, `receipt.json` and `summary.json` are the
historical independent-review packet froma576ef (main integration9e8bd82), source
77a8588. Its empty declared-results field fails v2 validation; it is preserved
without repair or relabeling. Do not rerun that historical helper in this
directory: its fixed paths would overwrite its receipts. Reproduce only in a
fresh isolated checkout and retain new outputs separately.

`run/` and `run_002/` are the coordinator's different rational-underflow
experiment. The first failed before calculation because PYTHONPATH was absent;
the second completed with a valid v2 record. Its script refuses overwriting.
The coordinator report is `reports/PHASE3_DENSITY_FLOAT_SELF_REVIEW.md`;
the independent report is `reports/PHASE3_DENSITY_FLOAT_REVIEW.md`.

Neither record turns ordinary floating estimates into interval certificates.
