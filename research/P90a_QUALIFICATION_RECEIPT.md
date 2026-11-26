# P90a sealed tiny qualification receipt

26 November 2026. **PASS for the frozen tiny/scripted qualification only.**
ROOT executed one authorized qualification at clean producer
`82d7b63d35f2f0495df6ed9c0d86999b649c44ff`. This receipt adds documentation;
it does not change an input, raw record, threshold or authorization. No P90a
main, DEV graph, production role seed/RNG or K12 native sample has been run.

## Freeze, prior reviews and before-read seal

The producer freeze has seven implementation files totaling3,851 lines.
ROOT's full-source review and the separate174-line exact code review cover
that freeze. The latter is original commit
`e7ce34747d924c9e68b4818456593e491f73bd81`, SHA256
`6e1d3e6d2a492b05e14ea587bd1a3cd850c2ec92a2e6bc3ee75167585b227111`,
integrated by ROOT at3b9ddb0. The distinct one-qualification authorization is
ROOTe9e1150, reports/P90a_ROOT_QUALIFICATION_AUTHORIZATION.md, SHA256
`3e96b6eab1924022803e53e1f11cfb8aadb7c2fc968cdf95d4f65eb84d2954db`.

ROOT committed the four original raw files at
**`929f7521b7b9890467be06be9799762c2739410f` before interpreting them**.
That is this receipt's immediate parent. ROOT's later integrated raw copy
5ab76ae was made after interpretation; it is not the before-read seal.
The original producer commits, isolated fixture/contract contributions and
predata corrections remain reachable, without rewriting their evidence.

The exact source/test/contract bindings remain:

| Artifact | SHA256 |
|---|---|
| source | `95fa65c6c04a0d48bb29c5d38b4bb1cac1cfdc22170191ee49a280f2995098e1` |
| tests | `9fba751e5bc2970e77e63a1d45a751c4a3e788f64b2f718fb7b26d8fee6dc9ec` |
| literal spec | `87dda967c662b0507c364d216f2c1a937d6a83e8616b536b7a0330bd90be0e7f` |
| API | `8c153fc538dd8b789239e25f814126e2e37c9a422778bed1bbd45b60a9645ca5` |
| qualification contract | `16e8ee28db9a26215fb22a12df8dcb3941ac957bc2c76ce1606ee1e0d3bfdfd7` |
| main contract | `0ed33b3d86e25eaa2e946506c52dcc510c89b633eabb61d68da7ed4e2d58b707` |
| population inventory | `54e69aad02836d0e3f6c48de9b3cbbabd3f66117a20b9e3391ae92a0455b1e9f` |

All18 project input hashes in the v2 manifest are unchanged before/after.
The spec's18 critical external pins were separately inspected, including
actual interpreter and critical loaded native/Python identities. No external
absolute file was passed as an extra runner input. P43/P50 remain immutable.

## Actual command, bounds and completion

The runner started at2026-11-26T03:06:00.517140Z, recorded completed/exit0,
and reported29.103454 seconds elapsed. Pytest reported283 passed,6 warnings
in28.34 seconds; JUnit records283 tests, errors0, failures0, skipped0,
and time28.330 seconds. These are elapsed/test durations, not measured total CPU.
The recorded child argv equals the frozen qualification contract exactly:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -c "import resource,runpy,sys;resource.setrlimit(resource.RLIMIT_FSIZE,(33554432,33554432));sys.argv=['pytest','-q','-p','no:cacheprovider','-o','junit_family=legacy','tests/test_p90a_source_bound_nonflat_veto.py','--junitxml=research/P90a_dev_veto_preflight/run_001/junit.xml'];runpy.run_module('pytest',run_name='__main__')"
```

The installed Mathbox v2 runner bound exactly18 repeated project inputs,
the one strict-child JUnit result and fresh parent
research/P90a_dev_veto_preflight/run_001. Its recorded caps are CPU60 seconds
per process, WALL90.0 seconds, combined log4MiB and max_threads1. There is
one worker, no retry, no affinity cap and no hard RSS/address-space claim.
The256MiB total/64MiB control quantities remain logical workspace plans.

The literal stdlib child launcher sets hard and soft RLIMIT_FSIZE32MiB
before importing pytest. This bounds the single declared JUnit file; it is
not an aggregate temporary-file cap. Production EvidenceWriter's1MiB final
reserve and4MiB single-JSON limit were exercised with synthetic sink fixtures;
neither limit is claimed for XML or as guaranteed free disk/native memory.
Explicit-B and inherited PYTHONDONTWRITEBYTECODE1 suppress bytecode writes;
pytest cache/plugin autoload and inherited extra selection options were disabled.

The six configured thread environment variables were recorded as1 before
configuration, after configuration, after each native point and at teardown.
The first native configuration readback was0 before setting it, then1 after
configuration and subsequent imports/observations/final checks. The initial0
is retained, not relabeled as1. All actual amplitude queries followed the
setting to1. Environment variables/readbacks do not certify all native behavior.

Versions are Python3.11.15, NumPy2.4.6, SciPy1.17.1, Perceval1.3.0,
Exqalibur1.4.2 and pytest8.4.2; NetworkX3.6.1 is recorded in the manifest.
No DEV graph generator was called. The actual interpreter resolves to the
pinned Python3.11.15 binary; native/source identities are preserved in XML.

## Tiny physical evidence and scripted evidence

The283 items match the complete frozen order:254 parameterized native items
and29 other items from30 test functions. Each native item records its observed
amplitude/probability, exact expectation, zero or exception representation,
provenance and readbacks before assertions. The native population is exactly
3 HOM +60 flat F4 r2 +191 nonempty H2-direct-sum-I2 points, at most4 receiver
modes/4 photons. Vacuum is analytic and makes no native query.

ROOT's independent inspector uses Gaussian-integer subset DP, distinct from
the fixtures' explicit-permutation Fraction-pair permanent oracle. Its source
was frozen at a60ee7c and tightened before data at5a0de0d, SHA256
`1b8e522a905bc99357d67ae49cda74f4b6a5cd3f28d94988c0f0ff70384826d0`.
It reports PASS for all254 amplitudes/probabilities, all283 item names,
18 unchanged project inputs,18 external pins, exact caps/paths and Git blob
seals. It checked exact six-key environment dictionaries and native readbacks1,
including the suite-level teardown property. ROOT also reports the official
Mathbox v2 validate_manifest check passed against the producer; this receipt
does not rerun that validator or the independent inspector.

There are181 zero reference probabilities and181 literal native zero
probabilities. Maximum absolute amplitude/probability errors are respectively
1.1102230246251565e-16 and2.220446049250313e-16, within the fixed abs2e-12/rel0.
No point was discarded for being zero, tiny, bunched or unfavorable.
The ROOT inspection JSON is reports/P90a_integration_validation/
recorded_qualification_inspection.json, SHA256
`b7f0278a8304afb8aa99a9139f27590a30b3e6a68d9598af8838ec774624fdb7`.
These independent numerical checks were performed by ROOT on sealed records;
the author of this receipt performed document/metadata reads only.

Exact tests retain all16 toy R, all occupations and uniform repairs, including
R013 and analytic vacuum. Their raw B-minus-D mean is-5/192; B and the toy
group2 full law agree, so its group2 advantage gate fails. The flat null is
fixed-R inclusion and uniform-R mean cancellation, not joint(R,Y) equality
or equality of quenched histories. A separate tiny2x2 compiler comparison
checks the fixed H/exponential convention against an analytic reference.

The complete96-attempt workflow, its1152 source-photon accounting units and
four control calls are SCRIPTED: graph, scorer, compiler, sampler, RNG/seed
and clocks are mocks. Additional error/resource/fallback fixtures are also
scripted. They test control flow, preclock arrays/best credit, typed ledgers,
dual-clock witnesses and retained failure prefixes. They are not measured B
attempts or production FAST/P43 calls. No real K12 matrix, stochastic native
sample, production role digest, PCG construction or optimizer replay occurred.

## Warnings, administrative scope and raw files

Stdout preserves six Perceval persistent_data.py warnings: three inability
notices for the default Application Support directory and three notices using
the existing system temporary directory. They are not test failures or native
sampler fallback observations. Stderr is empty; no warning was suppressed.

ROOT confirms one exact runner launch, no prelaunch rejection and no rerun:
the first qualification completed successfully. Two subsequent administrative
metadata-formatting reads raised KeyError('bytes'); ROOT replaced that lookup
with stat().st_size. They wrote no data and did not affect qualification or
validation. Earlier Git sandbox/slot issues were authoring administration;
the old P82 wrapper/type failures are not P90a qualification failures.

| Original sealed file | Bytes | SHA256 |
|---|---:|---|
| junit.xml | 1530960 | `933f2cb1485bab72643f74b1f4fed1879e696f370054e52ff5440977b60f84be` |
| manifest.json | 13733 | `dc914575db7e5a0f7baf380d31c68c5576f4f04bf30bc2733cecc696aea93189` |
| stdout.txt | 1744 | `06b2981cfce74e05a4b33605ed2be28fc9d371b44a2f328a555d8b8d5bbcf791` |
| stderr.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

These four files total1,546,437 bytes, including runner metadata/logs;
the scientific result itself is the1,530,960-byte XML. No raw byte changed.

This passes a bounded implementation qualification. It does not qualify the
K12 Clifford law, full Born/TV accuracy, a beneficial graph kernel, matched
total CPU/optical resources, actual clock authenticity, hardware/PNR/loss
capability, novelty or quantum/optimizer advantage. Main and its predata
independent recorded checker require their own reviews/authorization. All
prospective production D/species/DPP/heldout/replication controls remain NOT_RUN. No main,
retry, canary, push/CI, paid endpoint, paper or QPU action follows this receipt.
`positive_accepted` remains false and the positive research goal remains OPEN.
