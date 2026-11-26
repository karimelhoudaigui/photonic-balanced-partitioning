# P82a checker qualification run_003: separate receipt

Outcome: **22 synthetic tests passed**, with zero failures/errors/skips.
No warning was reported in stdout/stderr or the inspected JUnit. This
is a new receipt for the administrative v2 checker, not a replacement
for the unchanged137-line run_002 receipt. It does not authorize binding
or execution of audit main run_002, and no P82a B data was opened here.

## Authorization, correction and order of evidence

ROOT separately authorized one qualification on clean commit
a965e08dbbade4a6ea45d785b0b6fa37af3c8e3a after exact-diff review.
That revision changes only producer timeout representation, plus its
synthetic regression and corresponding version/binding metadata: a
finite numeric EXACT90 seconds may be int90 or float90.0. It adds no
epsilon. Cuts/masks and CPU/thread/log caps retain strict integer checks.
No scientific bound, tolerance, control or decision rule was retuned.

The earlier f595 audit source encountered the already sealed main001
administrative failure at manifest/wall-cap on90.0, before MainReplay.
Only that failure/provenance was previously authorized to be inspected;
no B scientific field, graph, count, cut or producer record was read.
The v2 correction is explicitly post-seal administrative, not falsely
described as a new predata scientific freeze.

Run_003 was invoked exactly once. Before inspecting its JUnit or logs,
the four raw files were committed at
b3260916043361327dfddb668f6456aa5634bf86. Before that commit, only the
runner's completed/exit0 status was observed. ROOT was notified and the
numerical slot released. Raw inspection and v2 validation followed;
this separate new receipt was then written. No source/spec/test update
was made during or after this qualification.

## Exact invocation and actual observations

The recorded child command is:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_p82a_independent_raw_audit.py --junitxml=research/P82a_independent_audit_preflight/run_003/junit.xml

The installed Mathbox4.0.0 computation-audit runner used that same
persistent interpreter with -B, all11 separate inputs from the frozen
contract, one declared JUnit, and output parent
research/P82a_independent_audit_preflight/run_003. Requested flags were
timeout60s, CPU30s, threads1 and combined logs4194304 bytes. The explicit
invocation set OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS variables to1 and
PYTHONDONTWRITEBYTECODE=1. No cache or automatic retry was used.

| Field | Observed value |
|---|---|
| Producer commit / dirty | a965e08dbbade4a6ea45d785b0b6fa37af3c8e3a / false |
| Runner start | 2026-11-26T01:57:34.450084+00:00 |
| Runner status / exit | completed / 0 |
| Runner runtime_seconds | 0.684385 |
| Pytest stdout | 22 passed in 0.25s |
| JUnit totals | tests22, failures0, errors0, skipped0 |
| JUnit suite time | 0.082s |
| JUnit timestamp | 2026-11-26T02:57:34.692835+01:00 |
| stderr | Empty, 0 bytes |
| Missing / invalid declared results | Empty / empty |
| Warnings | None reported in the three inspected result/log artifacts |

The22 names match the frozen unparameterized test functions: the original
21 synthetic fixtures plus
test_runner_timeout_exact_numeric_90_preserves_other_strict_caps.
The latter passed exact90 and90.0 and rejected the prescribed different,
NaN/string/bool values and floats for the other integer caps. These
checks did not invoke main roles, PCG, DEV reconstruction, native
queries, P50/Clifford replay or production data.

The manifest records runner Python3.11.15, contracted Python3.11.15 and
pytest8.4.2, on macOS-26.2-arm64-arm-64bit. These are its software fields,
not authentication of every installed dependency. The thread limit is
conventional environment control; CPU30 is per process. No measured hard
RSS, affinity or aggregate descendant bound is claimed. Logical256MiB
remains a plan. The three timing boundaries above are distinct descriptive
fields, not an optimization or hardware-throughput benchmark.

## All11 frozen inputs

The manifest records each SHA256 identically before and after. The
installed v2 validator also checked current file hashes against those
records after raw seal.

| Input | SHA256 before = after |
|---|---|
| AGENTS.md | 6c4c409cdf9d05330bc46b9f607b7034e16bcaf51086b712a80d03ccd8e78e5a |
| pyproject.toml | 7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4 |
| requirements-research-lock.txt | 3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1 |
| research/P82a_independent_raw_audit.py | 56a3bb2a686203a4e3752687f7e42170d65a5ccfe5987989fbff333fb39afcfd |
| tests/test_p82a_independent_raw_audit.py | 38383d9e304e26dc3a1f01e7a8d47ab915ed8cc3d1ec3e600b69caa0909d92b4 |
| research/P82a_independent_audit_spec.json | 222e9cd9681eb893655dc08671ad794048dcd174a8896a5b3b9ce69745696499 |
| research/P82a_independent_audit_preflight_contract.json | b32aab4db39ab45b0b3c9235dac2ec6bf1689fa9bb2ce1d684c58b240e82a785 |
| research/P82a_independent_audit_main_TEMPLATE.json | 14ddd37b03825146923dc7ef484da972a8238620fd5138be772c529de62563c6 |
| research/P82a_INDEPENDENT_AUDIT_BINDING.md | 931a66f706be8aada402b40c596e601c05e1039f8a2f3834790055806d521db5 |
| research/P82a_INDEPENDENT_RAW_AUDIT_PLAN.md | b3b8d4e83acaf4ac6430bc8967be021e41520fe25c70cf9c3a2a2ca10eaa4119 |
| research/P82_ZERO_LOADING_INDEPENDENT_NULL.md | bc5943faa105dd76a41645376b52cc62f69fcf6d7e40fc303e57b48437885c4a |

The sole declared scientific result is the JUnit below the fresh runner
output parent. There is no P82a B artifact in this qualification closure.

## Raw bytes and v2 status

All four files are in
research/P82a_independent_audit_preflight/run_003/.

| File | Bytes | SHA256 |
|---|---:|---|
| manifest.json | 7268 | 943411e77a1e30984ad889442748e85b91bed672b62f11ad548da9c0dae72869 |
| stdout.txt | 246 | 00e458a9726046e89f804230113f5ceef97266d2b7fd2fa44b18d010d28237e1 |
| stderr.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| junit.xml | 3316 | 91b0f3986d9f018f57ebfa6cf3045d8cf834b37048824a114ad46d8ac9b50cc4 |
| Total | 10830 | Four immutable raw artifacts |

After the raw commit, installed validate_manifest.py was invoked on
this run_003 manifest with --root pointing to the isolated worktree.
It returned exit0, valid evidence record, run status completed, with
mathematical interpretation explicitly reserved. No test rerun occurred
for this validation or receipt.

## Preservation and remaining boundary

The run_001 prelaunch archive remains2268 bytes with SHA256
7370eaf805e6e5eacfc242ca8763ddb808d24f27e8108147bcbd4baa4332aa61.
The earlier137-line run_002 qualification receipt is unchanged, SHA256
9b84802de97e766c13a39cd83eda21151cb437cbad06d5cb2a58d873291cd0aa;
its raw75a4697 and receipt696b400 remain historical. They are not
overwritten or presented as validation of the corrected v2 source.

ROOT reports preserving the failed v1 audit main001 raw at b4aa0f3 on
research/p82a-audit-v1-evidence. That archive was not opened or revalidated
here. Historical manifests must be checked against their own matching
input revision, not the newer v2 working copy. The administrative failure
and its original f595 source remain evidence, not removed negatives.

This PASS qualifies the22 synthetic fixtures only. It does not guarantee
the recorded-data main will complete or establish Born law, TV, physical
replication, basin performance or advantage. No new raw dataset binding
was assembled, no P82a B data/manifest/log opened and no audit main
run_002 executed. ROOT inspection and a separate authorization remain
necessary. The positive optimizer objective is OPEN.
