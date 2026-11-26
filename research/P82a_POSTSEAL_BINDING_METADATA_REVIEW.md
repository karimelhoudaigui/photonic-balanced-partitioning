# P82a postseal input binding: independent metadata review

26 November 2026. **Verdict: metadata binding accepted; no material blocker
found. The checker guard is still closed.** No scientific output value was
decoded and no checker, test, import, AST, role hash, RNG or backend was run.

## Exact prepared artifacts

Reviewed PRIMARY ROOT freeze:
`dead3ed4d1a520b95a32402c02823b0f1b46b2b6`.
The complete builder (95 lines) and both JSON artifacts (125+292 lines)
were read, separately from their underlying scientific payloads.

| Artifact | SHA-256 |
|---|---|
| `research/P82a_independent_audit_execution_contract.json` | `0c652771bbd423a8b4e1c4cc462411d0e917dd2e9573521cee5f53c86e8bd4f5` |
| `research/P82a_independent_audit_dataset_binding.json` | `da0be8f573a51a0016825bdbede0296b19decc923fc3ed26f67c16ef1864d845` |
| `reports/P82a_integration_validation/prepare_audit_binding.py` | `ff58f44a35b3db724a5b5222af4df5d43be7ee1796c13e61de712a4ede931bde` |

The checker source/test/spec hashes remain the previously reviewed
`f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529`,
`7dc3dfabbe78d9e515098d6eb91cc0446cbe588ed92e0ab103c2fce4b59b84c6`,
and `6fd8c3639aa8bc2c4db407b15d3124d4289a585e507992ab6f07a45be9db8fc9`.
Their behavior and physics are outside this metadata-only review.

## Closure, provenance and opaque checks

The final contract contains 46 unique relative input paths. Its set is
exactly the 45 unique binding artifact paths plus the binding itself.
There are 45 unique aliases. The binding includes the final contract's
hash and does not attempt a recursive hash of itself. The eventual v2
runner must hash both files as ordinary separate inputs.

All 45 artifact hashes and byte sizes were independently checked against
the actual ROOT files. Each was a regular file; all 11 distinct directory
components checked were directories, with no symlink component. No path
is absolute, contains traversal, or is inside the future audit output.

The primary manifest alias resolves to
`experiments/P82a_dev_veto/run_001/manifest.json`, SHA-256
`2fe4cc045e74eb3983c210c2ee7476d466b5963ffe9f9fee73cf0400268d9e4e`.
Its recorded execution commit is
`39b61bb9289cab7439ca15a4aa79d265b068f6f9`, clean. The reviewed source
freeze stays `94f80b94`, with source/spec pins `7e1a0d03`/`8598bd42`.
All 15 primary and 11 qualification manifest inputs have identical before/
after hashes, agree with the binding and match the actual files. Every
declared manifest output hash also agrees with its opaque local artifact.

The eight required scientific aliases occur exactly once and resolve to
the corresponding basenames under the declared dataset directory. Their
total is 2,525,942 bytes, below 33,554,432. Their contents were read only by
byte-hashing utilities, never parsed or exposed as cuts, graphs, seeds,
phases, counts, decisions or scientific observations. Primary manifest
inspection was limited to provenance, caps, input/output hashes and run
integrity. It supplies no optimizer conclusion in this review.

The qualification receipt records 21 passing synthetic tests and identifies
its raw seal; its v2 manifest records completed/exit0, unchanged inputs,
CPU30/WALL60/environment-thread cap1 and valid result inventory. Receipt,
manifest, logs and JUnit hashes are bound. No qualification was rerun, and
no independent JUnit or scientific interpretation is claimed here.

## Output, resources and authorization boundary

The final contract preserves the TEMPLATE's assertion, numeric rules,
software, planned child argv, resource bounds and declared results. Only
the prepared state, opaque input description/closure and resource note
differ. The runner output parent `research/P82a_independent_audit_main/run_001`
was absent at inspection. Both `data/audit_*.json` results are strict
children, not reserved files or inputs; the child creates its data directory.

The limits remain CPU30/WALL60, one worker/environment threads1, no native
backend or optimizer replay, raw32MiB/output512KiB/log4MiB, logical256MiB
PLAN and zero retries. No hard RSS or actual audit-runtime claim follows.

Current binding state is `SEALED_POST_B_RAW_REVIEW_PENDING`, `b_raw_sealed`
true and `audit_authorized` false. The reviewed source rejects this before
replay. ROOT's stated later transition may change only binding_state to
`SEALED_POST_B_RAW_AUTHORIZED` and audit_authorized to true. This changes
the binding's own hash, which must be frozen/captured in the actual runner
input; it does not change the 45 record hashes or the final contract.
This review does not itself make that transition or authorize execution.

Only read-only metadata parsing/comparison, file statistics/byte hashes,
text reads and isolated review/Git operations were used. PRIMARY ROOT,
the builder, checker and all sealed science bytes remain unchanged by this
review. No B value, paper change, QPU action or positive result is inferred.
