# P82a independent checker qualification: run_002 receipt

Outcome: **21 synthetic tests passed**, zero failures/errors/skips. One
separately authorized qualification child was executed on the corrected
binding. This receipt does not authorize dataset binding or audit main.
All P82a B datasets, manifests and logs remain unopened by this reviewer.

## Order and preserved first rejection

Code-only source freeze: 34c9513072d385373805215dba6679ffb5686ab9.
The original run_001 command was rejected before child launch because
JUnit lay outside the runner output directory. Its raw rejection remains
unchanged at ebee1a041d8a9c564fb8c9a012ea7753045f2026, file
research/P82a_independent_audit_preflight/run_001/prelaunch_rejection.json,
2268 bytes, SHA256
7370eaf805e6e5eacfc242ca8763ddb808d24f27e8108147bcbd4baa4332aa61.
No tests, JUnit or v2 manifest were produced by run_001.

ROOT separately authorized only the three-file binding correction at
a7e423b28f75f9a5a87068be667c8bf6f1eadd96, then explicitly authorized the
fresh run_002. The source, tests, specification and numerical rules were
unchanged. This was not an automatic retry.

Run_002's FOUR raw files were committed immediately at
75a4697fcc442e0a4308cbff40fa08a316d43766 BEFORE reading the JUnit/logs or
interpreting their result. Only the runner's completed status/exit0 was
observed before that raw commit. The numerical slot was then released
and ROOT notified. Result inspection, v2 validation and this separate
receipt followed. No source or raw artifact is edited by the receipt.

## Exact execution and observed result

The v2 manifest records clean producer commit
a7e423b28f75f9a5a87068be667c8bf6f1eadd96, dirty=false, and the exact
planned child argv from the corrected qualification contract:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_p82a_independent_raw_audit.py --junitxml=research/P82a_independent_audit_preflight/run_002/junit.xml

The installed Mathbox4.0.0 computation-audit runner used the same
persistent interpreter with -B, eleven individual --input arguments,
the single declared JUnit result, and fresh output directory
research/P82a_independent_audit_preflight/run_002. Flags were
--timeout60, --max-cpu-seconds30, --max-threads1,
--max-output-bytes4194304. The invocation explicitly set
OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS thread variables to1 and
PYTHONDONTWRITEBYTECODE=1. There was no cache, native backend, graph
reconstruction, main-role hashing, PCG, solver replay or DEV read in
the selected qualification population.

Observed fields, kept as distinct timing boundaries:

| Record | Observation |
|---|---|
| Runner start | 2026-11-26T01:37:07.063102+00:00 |
| Runner v2 status / exit | completed / 0 |
| Runner runtime_seconds | 0.610468 |
| Pytest stdout | 21 passed in 0.24s |
| JUnit population | 21 tests, failures0, errors0, skipped0 |
| JUnit suite time | 0.077s |
| JUnit timestamp | 2026-11-26T02:37:07.318851+01:00 |
| stderr | 0 bytes |
| Warnings | None reported in stdout/stderr or the inspected JUnit |
| Missing / invalid declared results | Empty / empty |

The JUnit names match the frozen21 unparameterized synthetic functions
from the one declared test file. They cover independent integer cuts/
canonical masks, every toy swap and Q-best, exact F4 features, actual
rounded tiny-H and analytic-zero semantics, collision repair/no-RNG
extremes, typed duration references, conservative dual-clock prefixes,
cached-best lineage, same-fixed-mode witnesses, malformed input guards
and the postseal boundary. No main or native experiment is hidden in
this passing population.

The manifest lists runner Python3.11.15, contracted Python3.11.15 and
pytest8.4.2, platform macOS-26.2-arm64-arm-64bit. This is recorded
software/provenance, not authentication of every installed dependency.
The thread cap is conventional environment control. CPU30s is a
per-process POSIX cap; no aggregate descendant, affinity or hard RSS
claim is supplied. Logical256MiB remains a plan. These qualification
timings do not forecast the main or establish a throughput advantage.

## Eleven unchanged execution inputs

For every row the manifest's before and after SHA256 are identical;
the installed v2 validator also checked them against the current root.

| Input | SHA256 before = after |
|---|---|
| AGENTS.md | 6c4c409cdf9d05330bc46b9f607b7034e16bcaf51086b712a80d03ccd8e78e5a |
| pyproject.toml | 7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4 |
| requirements-research-lock.txt | 3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1 |
| research/P82a_independent_raw_audit.py | f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529 |
| tests/test_p82a_independent_raw_audit.py | 7dc3dfabbe78d9e515098d6eb91cc0446cbe588ed92e0ab103c2fce4b59b84c6 |
| research/P82a_independent_audit_spec.json | 6fd8c3639aa8bc2c4db407b15d3124d4289a585e507992ab6f07a45be9db8fc9 |
| research/P82a_independent_audit_preflight_contract.json | 99d5a8bbd5678342c1316a1a87a2b804b939b5673a1a00e66e7e6309c94e8ecc |
| research/P82a_independent_audit_main_TEMPLATE.json | c11b0c803e4d4f50697b8f6bbb51c8d8360466d659356bd6adac8b84c202ff6a |
| research/P82a_INDEPENDENT_AUDIT_BINDING.md | 301d5722b232c9f276471f33f12446de206faf382622b88bde6dcde168f5538b |
| research/P82a_INDEPENDENT_RAW_AUDIT_PLAN.md | b3b8d4e83acaf4ac6430bc8967be021e41520fe25c70cf9c3a2a2ca10eaa4119 |
| research/P82_ZERO_LOADING_INDEPENDENT_NULL.md | bc5943faa105dd76a41645376b52cc62f69fcf6d7e40fc303e57b48437885c4a |

The input population is exactly the corrected contract's11 paths; the
only declared scientific result is the JUnit child of run_002. The raw
manifest additionally hashes its two logs. No B path is in this closure.

## Sealed bytes and validation

All paths below are inside
research/P82a_independent_audit_preflight/run_002/.

| File | Bytes | SHA256 |
|---|---:|---|
| manifest.json | 7449 | 2a82001fac46844f9a352c4d6c753a23106d6ced448eaac3ed3775332b31315b |
| stdout.txt | 246 | 9ac228254367b631450efb7312ccc2c4446081c73a5e896b615e9793ef4ef704 |
| stderr.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| junit.xml | 3169 | 949d725c03db5eb8f0abd00ff25b8dd38827192bf0f27f6c03fc3dc83bc3ba00 |
| Total | 10864 | Four separate immutable raw files |

After raw seal, the installed computation-audit/scripts/validate_manifest.py
was run with the manifest path and --root pointing to this isolated
worktree. It returned exit0 and reported a valid evidence record with
run status completed, while reserving mathematical interpretation.
No tests were rerun for validation or receipt preparation.

## What this qualifies

This is finite synthetic qualification of the recorded-data checker,
not an audit of P82a B records and not an end-to-end Born-law, TV or
physical replication certificate. It does not infer basin performance
from96 adaptive draws or claim the main will pass. The accepted
source-bound compiler timing/IO limitations and non-replayed custom
policy scope remain unchanged.

Main TEMPLATE remains unbound. No opaque dataset binding, producer/B
manifest or log access, graph reconstruction or audit main is authorized
or performed. ROOT must inspect this receipt and separately commission
that next action if appropriate. The earlier prelaunch rejection is
retained, and the user's positive optimizer objective remains OPEN.
