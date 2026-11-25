# P52 qualification run_002: guards pass, durable API report fails

Verdict: **API qualification INCOMPLETE; no full replication authorization**.
The six administrative/analytic guards passed, but this run does not preserve
the numerical residuals or native API metadata needed for the requested review.

ROOT read the observation-only delta and authorized this single fresh attempt
on clean `fe61688851fece72053bb101a6ba283183d2c392`, with unchanged eleven
execution inputs, CPU20/wall30, thread environment1 and log4MiB. Source SHA256
`3242986191a797c25693195c9a3d8af4acc027ba5ad1a1c92bd71f4c49d10400`.
Historical run_001 and its administrative argv rejection remain unchanged.

Actual runner invocation is exactly that recorded in
`P52_naive_qualification_run_001_review.md`, substituting run_002 for run_001
in its output and both declared-result paths. The runner, pinned Python,
contract path, eleven --input arguments and all caps are unchanged. Child argv:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode qualify --output research/P52_naive_qualification/run_002/data
```

The child started `2026-11-25T08:37:22.890615+00:00`, exited1 after19.105268
runner wall seconds, and was not timed out. Preserved JUnit records six tests,
zero failures/errors/skips, time0.031s. Stdout also reports `6 passed in 0.03s`.
The EPERM/timeout optional-observation fixture passed. Actual Perceval import
occurred: stderr retains its persistent-data warnings and Matplotlib fallback
cache/font-cache warnings. No cache setting was changed prospectively or
retrospectively, and no second import/run was attempted.

Finalization failed in `write_json(...report...)` with
`TypeError: Object of type bool is not JSON serializable`. NumPy2's boolean
scalar has this type name. The helper's `residual <= ABS_TOL` comparison can
return `numpy.bool_` for NumPy-derived residuals; it was placed into a check
record without conversion to builtin bool. The report's checks list had been
constructed, hence the eleven-check routine had returned, but its comparisons,
residuals, docstrings and file metadata were never written. They are not
recoverable evidence from this run, so I do not report eleven PASS or claim
that native threading was qualified. The failure is my wrapper's JSON boundary
defect, not a demonstrated physical probability disagreement.

No source/vendor/backend change, retry, full25,740 production loop, primary
data rewrite, optimization or remote call followed. The exclusive slot was
released on inspection. Any future correction requires a separately frozen
delta, fresh directory and ROOT authorization. Cold Perceval/Matplotlib import
cost remains part of the capped execution; this run does not establish full-run
resource feasibility.

Durable files in `research/P52_naive_qualification/run_002/`:

| File | SHA256 |
|---|---|
| manifest.json | 05dc7303c02845a9570bdc16f2e0bbe28077a12d5aec0769a0007616363b2a85 |
| stdout.txt | c4975fe185b7504fe3a652776f5076b77ae85115764a68f517084de8afc2c238 |
| stderr.txt | 4e24859b7750416e9210a520b0a9bd0e396db58bbddba456fbd7e97d1519607f |
| data/guard_junit.xml | 7c2a826b665f823faedf920c87e240c0fe87855e150344b70785a6114c7420da |

The runner correctly marks report.json missing and status failed. All eleven
input hashes before/after agree. The following actual command returned exit0:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py research/P52_naive_qualification/run_002/manifest.json --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication
```

Output: `valid evidence record (run status: failed); mathematical interpretation
requires review`. This is closure/schema validation of failed evidence, not a
physics/API PASS. The input revision is fe61688; subsequent source amendments
must not be substituted for that historical closure.
