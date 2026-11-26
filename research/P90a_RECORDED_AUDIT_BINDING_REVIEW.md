# P90a recorded-audit binding: independent metadata-only review

Reviewer: `/root/p66_dark_audit`. Date: 2026-11-26.
Verdict: **NO MATERIAL METADATA BLOCKER; execution remains NOT AUTHORIZED.**
This review concerns the pending binding below, not the scientific B result.

## Exact reviewed objects

- Builder freeze: `4397224d9a99c45943ea6d49bff0ac599a6a264e`.
  `reports/P90a_integration_validation/prepare_recorded_audit.py`, all 99 lines;
  SHA256 `aea4474ea0803c56477b48d7bf6a442fb2e0ffee8b649d3515eca4f0ab20dd4e`.
- Prepared metadata: `027653e2c36030549df2c7536404e6c611da12f2`.
  `research/P90a_independent_audit_execution_contract.json`, all 169 lines;
  SHA256 `c6b31ea10f2a0375058e7fe86097ad8b070fd3e50d4c279065c823f03ee52f69`.
- `research/P90a_independent_audit_dataset_binding.json`, all 382 lines;
  pending SHA256 `f5ddda5b4df2ed3a8d887a9c40df24385d90ed8e002892515270ac50e7425b1b`.
- Unchanged checker SHA256:
  `609959307bbddfb08ac70b71e714e81df962c2c0d615b56aed20a970cf46a62a`.
  Tests `dcc2a352a004885fa12fd5740552ba103f4f6bb9f3ead76491bdacefab1a0cfd`;
  spec `a80869d6a9638280c62130c85f367e99d6f0b30e407e8c4cd837d3a4cd5f6de2`.
  The earlier full source review remains the scientific-code authority;
  no checker or producer source was edited or executed for this review.

## Closure, paths and bytes

Independently reconstructed the builder's ordered, deduplicated union of the
25 TEMPLATE inputs, all three manifests and their inputs/outputs, 16 added
provenance/review/builder paths, the execution contract and the binding.
It equals the final **62 unique execution paths**, with no addition or omission.
The binding has **61 unique descriptors**, each `name == path`, with exactly
`name/path/sha256/bytes`; they cover every execution input except the binding.
The contract itself is described. The binding has no circular self-hash;
the future runner must hash its actual authorized bytes as the 62nd input.

All 62 current files were independently SHA256-hashed and stat'ed.
Every descriptor SHA and byte count matched, with zero mismatches.
Every path is project-relative and contains neither empty, dot nor parent
components. All 62 are regular files; all 12 distinct ancestor paths are
directories, so no listed file or intermediate ancestor is a symlink.
The eight opaque primary data files total **3,667,492 bytes**, below 32 MiB.
No primary data value, graph, B record, control record, summary, failure value,
scientific receipt or recorded-inspection payload was opened or interpreted.
Those objects were checked solely through hashes, sizes and Git blob hashes.

## Frozen producer, qualifications and raw seal

Read the three complete manifests as metadata and checked their commands,
declared paths, repository state, input hashes before/after, output hashes/kinds,
completed status, zero exit status, all three passing runner checks, and empty
missing/invalid-result lists against the frozen contracts and descriptor table.

- Primary main: clean commit `b2f9af31af86c83d8aef8841891c4d37832c69e5`;
  exactly 18 inputs, 8 declared results and 2 logs.
- Primary qualification: clean source freeze
  `82d7b63d35f2f0495df6ed9c0d86999b649c44ff`; the same exact 18 inputs.
  JUnit metadata only: 283 testcase tags; suite tests=283 and
  failures=errors=skipped=0. Its 1,530,960 bytes fit its 32 MiB file cap.
- Checker qualification: clean freeze
  `944f9bc7fadea36ff17373b29ca2c5369ccb5267`; exactly 9 inputs.
  JUnit metadata only: 29 testcase tags; suite tests=29 and
  failures=errors=skipped=0. Its 6,074 bytes fit its 512 KiB file cap.

No testcase payload/property or native amplitude was inspected. Qualification
counts/closures were checked, not rerun; their scientific receipts stayed opaque.
Both archived qualification commands contain `-B` and set their literal
soft/hard RLIMIT_FSIZE before pytest. Log sizes are 2,445 bytes for main,
1,744 for primary qualification and 246 for checker qualification, each <4 MiB.

Independently compared **59 Git blobs** against current descriptor hashes:
18 primary inputs at source freeze, the same 18 at execution commit, 9 checker
qualification inputs at its freeze, 11 original raw-seal files, the builder at
its freeze and the two prepared metadata files at theirs. All 59 matched.
The 11 raw files are the manifest, both logs and all eight results at
`d3962d5b846a9905d061d8eb28cf2d0876b0ba00`; none was decoded.
Primary manifest SHA256:
`a8b459fb9e214c1d0e06053376c54e06bf99d00f889baad60bdb57172667a9d6`.
This verifies byte identity with the original seal; it does not independently
attest the producer's clocks, physical probabilities or scientific conclusions.

## TEMPLATE delta, fresh output and resource binding

A complete structural comparison found exactly three top-level differences:
the pending contract state, expanded execution_artifacts, and added original
raw-seal commit. Command, algorithms, tolerances, scientific population, limits,
environment, software pins, results and all other fields are unchanged.
Inherited TEMPLATE prose is not execution authority; explicit guards govern.

The planned command uses the persistent Python with `-B`, the unchanged checker,
the stated binding, and `research/P90a_independent_audit_main/run_001/data`.
Runner output is its `run_001` parent; both declared JSON results are strict
children under `data/`, distinct from manifest/log names and every input.
Neither output is an input or an ancestor/descendant of an input.
The enclosing `P90a_independent_audit_main`, runner parent, data directory and
both results are absent, including dangling symlinks. Existing `research/`
is a regular directory. These are observations at review time, not a reservation.

The unchanged contract requires CPU 30 s, wall 60 s, one thread/worker,
4 MiB combined runner logs, 512 KiB checker output, 32 MiB sealed raw input,
4 MiB single-object/line cap and zero failed retries. Six thread environment
variables are 1; bytecode is disabled. Logical 256 MiB is a plan; memory/affinity
hard limits remain null. Runner log caps do not substitute for scientific-output
guards. This review launches neither the bounded runner nor a validator.

## Authorization and limits

Observed binding: `SEALED_POST_B_PENDING_ROOT_AUTHORIZATION`,
`b_raw_sealed=true`, **`audit_authorized=false`**. It cannot pass the checker's
required `SEALED_POST_B_RAW_AUTHORIZED` plus true authorization flag.
Only a separate ROOT authorization may change those two fields, leaving the
contract, all 61 descriptors and checker unchanged. That transition creates a
new binding SHA, which the actual future runner must capture before/after;
the pending SHA above must never be described as the authorized binding SHA.

No import, AST parse, collection, scientific calculation, production role/seed
evaluation, RNG, test, native call, replay, optimizer or CI job was performed.
No paper/QPU action occurred. A successful future replay could validate recorded
arithmetic and protocol consistency only; it would establish no new sample,
Born-law certificate, independent physical replication, matched-resource
advantage, novelty, hardware readiness or positive research gate.
