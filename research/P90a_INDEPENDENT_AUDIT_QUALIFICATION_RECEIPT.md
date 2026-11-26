# P90a independent auditor — qualification receipt

26 November 2026. **Recorded tiny/synthetic qualification: 29 PASS.**
This receipt reads the uniquely executed qualification after its raw seal.
It adds no execution, validator, replay or physics observation and does not
authorize the producer main or recorded audit. No B outcome was accessed.

## Original execution and seal

Checker source/tests/spec/contracts/binding freeze:
944f9bc7fadea36ff17373b29ca2c5369ccb5267, clean at execution.
Original raw seal BEFORE interpretation:
f6f3c8b7961e527259557278e64536e10ee74801, direct child of that freeze.
This new receipt is a separate child commit, not a rewrite of the raw seal.
ROOT executed exactly one qualification; the receipt writer did not run it.

Raw directory: research/P90a_independent_audit_preflight/run_001/.
Manifest schema 2, claim P90a-INDEPENDENT-RECORDED-AUDITOR-TINY-QUALIFICATION.
Started 2026-11-26T03:30:07.789282+00:00; completed, exit 0;
runner wall 0.504861 seconds. No missing or invalid result was recorded.
Stdout reports 29 passed in 0.11s; JUnit records 29 tests, failures 0,
errors 0, skipped 0 and suite time 0.108s. All 29 stored names match the
unparameterized frozen module inventory. No warning appears in stdout;
stderr is empty. ROOT independently reports the official v2 validator PASS.
No validator was rerun for this receipt.

## Command, population and resources

The observed argv matches the frozen preflight command, using persistent
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python with -B and a literal
stdlib -c launcher. Before loading pytest, that launcher sets soft/hard
RLIMIT_FSIZE to 524288 and fixes sys.argv to the complete test module:
pytest -q -p no:cacheprovider -o junit_family=legacy,
tests/test_p90a_independent_raw_audit.py,
--junitxml=research/P90a_independent_audit_preflight/run_001/junit.xml.
There is no outcome filter, parameter generator, retry or alternate seed.

Runner output parent is the fresh run_001 directory above. JUnit is its
strict-child result; manifest.json/stdout.txt/stderr.txt remain runner-owned.
The child has CPU 30s/WALL 60.0s, max_threads=1 and log cap 4194304 bytes.
The fixed inherited contract specifies bytecode/cache suppression, disabled
third-party plugin autoload, empty pytest overrides and six thread variables=1.
The runner records Python 3.11.15, pytest 8.4.2 and macOS arm64.
No native optical backend belongs to this qualification. The 512KiB JUnit
limit is per file, not an aggregate temporary-file or RSS guarantee.
The 256MiB logical plan is not an observed/enforced memory bound; the
manifest has memory_bytes=null. No actual CPU total is inferred from its cap.
The observed 6074-byte JUnit fits the declared 524288-byte limit.

The 29 tests exercise a hardcoded weighted n4 adjacency, strict scalar cuts,
canonical masks, all tiny swap positions and duplicate/first-min credits;
Taylor40 against scalar/complex-Hermitian 2x2 closed forms and malformed
normalizers/transport; full-count/repair lineage including a scripted
six-port collision fill; typed factory unknown CPU, disjoint paid scope,
unclipped call gaps and every retained dual-clock trace row. Scripted cases
check reset/current/Q/compiler/global credit, full photon accounting,
partial-prefix/failure precedence, strict four-control panel, path/parser
guards and preseal authorization rejection.

These are tiny/scripted checks: no production role hash or PCG constructor,
DEV graph generator, real K12 compiler, NumPy/SciPy numerical dependency,
P43/P50 import/call, optimizer replay or native probability/sample was used.
The complete tiny case has one chain/attempt and 18 scored candidates;
it is not an execution or replication of the 96-attempt main population.

## Actual nine-input closure

The manifest records exactly these nine local inputs, once each, in the
contract order. Every recorded before/after pair is identical. The clean
execution revision and unchanged input closure preserve the predata code.

| Input | SHA256 before = after |
|---|---|
| AGENTS.md | 6c4c409cdf9d05330bc46b9f607b7034e16bcaf51086b712a80d03ccd8e78e5a |
| pyproject.toml | 7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4 |
| requirements-research-lock.txt | 3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1 |
| research/P90a_independent_raw_audit.py | 609959307bbddfb08ac70b71e714e81df962c2c0d615b56aed20a970cf46a62a |
| tests/test_p90a_independent_raw_audit.py | dcc2a352a004885fa12fd5740552ba103f4f6bb9f3ead76491bdacefab1a0cfd |
| research/P90a_independent_audit_spec.json | a80869d6a9638280c62130c85f367e99d6f0b30e407e8c4cd837d3a4cd5f6de2 |
| research/P90a_independent_audit_preflight_contract.json | 5896474eb0802b3a0ce5859d00d4a68712bbfec6c137c132c7e275ff86b64601 |
| research/P90a_independent_audit_main_TEMPLATE.json | ae2ccdb3dfc080c6308be7b6f76681fda449b3ddef46c94f99f5d0e0f00abb66 |
| research/P90a_INDEPENDENT_AUDIT_BINDING.md | bd639cb6f33448ca52530d60eacaa6d13839cc928bcf05d77ca69641c33f1bbc |

No absent primary file, external absolute runner input or B artifact was
introduced into this qualification. Primary source/qualification commit 82d7b63
and prospective primary main commit b2f9af31 remain separate pins in the
unchanged checker; neither is this checker's execution commit 944f9bc7.

## Raw artifacts and preserved reader failure

Paths below are relative to the raw qualification directory.

| Artifact | Bytes | SHA256 |
|---|---:|---|
| manifest.json | 7592 | d8f3e69ad2543dfcb6a7083fde2acdf4e45cdd0060e15d675d6607f890b38a21 |
| stdout.txt | 246 | 7fccf899f0db45921389a0d322e1bfc157c92a02965c7e92e3d17c6427ded6be |
| stderr.txt | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| junit.xml | 6074 | ec8b5a9152d038c0bb3086e0b8a50df94ff09de07f57c63c09fef2d62812e713 |

Total raw bytes 13912. These file hashes/byte counts were read independently
for this receipt; the files themselves were not edited or copied.

ROOT inspection artifact:
reports/P90a_integration_validation/checker_recorded_qualification_inspection.json,
SHA256: faea5ea9e2ba8c78a10d572ff9c318bc4c39167700c4c586f0acd1ba7bad371e.
It records PASS, the original seal/execution commits, 29 actual items,
nine checked input hashes, runner runtime and 6074-byte JUnit under the
project .venv Python 3.11.15 reader.

The earlier postseal metadata-reading failure is separately preserved at
reports/P90a_integration_validation/checker_metadata_reader_failure.json,
SHA256: 59543437baa0bb70851dc5c1046e6d1c986cee59eaa757ac50bb0e697c98bdd2.
System Homebrew Python 3.14.6 could not import pyexpat because its linked
libexpat lacked _XML_SetAllocTrackerActivationThreshold. The affected step
was ElementTree.parse of the already sealed JUnit. ROOT then read that
same XML using the frozen project .venv Python 3.11.15. The failure record
states scientific_inputs_changed=false, raw_outputs_changed=false, no
inspection output from the failed attempt, one qualification launch,
zero qualification reruns and no system installation/configuration change.
This reader failure is not a failed qualification or a second test attempt.

## Scope

The finite result qualifies these 29 synthetic items and their frozen
recording/provenance only. It establishes neither a Born law/global TV
bound nor an interval certificate, optimizer benefit, authentic clock
timing, full-resource comparison, physical replication or quantum advantage.
The main TEMPLATE remains a separate gate: ROOT review/authorization and
later opaque postseal dataset binding are still required. No future B path
was probed and no later B outcome was read while preparing this receipt.

Only text/metadata/hash reads and this new receipt/Git commit were performed.
Source/tests/spec/contracts/raw remain unchanged. No import, test, validation,
seed/RNG/replay/native/main/experiment/push/paper/QPU action was performed
for the receipt. Failed and negative evidence remain preserved.
