# P52 documented native maximum1: prospective run_004

ROOT authorized implementation after the read-only Config receipt1f6ec5d and
completion of the P53 static review49e2e01. This checkpoint freezes code only:
no exqalibur/NumPy/Perceval import, Config assignment, test, permanent or new
numerical execution occurred in preparing it.

The official static interface was observed, not guessed:
`exqalibur.Config.compute_max_thread_count`. New helper
`configure_native_threads` records its integer value before configuration,
assigns1, and requires integer readback1 through `native_thread_readback`.
The interface, requested value, actual before/after and class documentation
are report data. Main invokes it after local imports, before any backend
construction or permanent call. The same readback is required after all work
before a completion/PASS status is assigned; a mismatch leaves INCOMPLETE and
exit1. It changes no precision setting or permanent `ptype` argument.

The documented default permanent method may change with this resource setting
(Glynn at1/2 allowed threads, Ryser otherwise). Thus run_003's successful
eleven checks with unverified native threads are preserved but do not qualify
the new path. Fresh run_004 prospectively runs **eight guards plus the same
eleven numeric checks** under the new maximum, after ROOT source review/slot.
The eighth guard uses a fake static Config class, tests before/after integer
readbacks and strict builtin JSON, and rejects a simulated post-work change
to2. It invokes no real native API. No extra production-family permanent is
added to qualification.

The hardcoded NOT_ESTABLISHED label is replaced by a documented-configuration
label. Successful qualification would report
`API_QUALIFICATION_PASS_NATIVE_MAXIMUM_1`. This is an API configuration and
readback result, **not** an OS thread observation or independent audit of
native enforcement. ps remains optional/EPERM-tolerant. Six environment
limits1 and CPU20/wall30/out4MiB remain unchanged. The cache resource setting,
six historical reference byte pins, matrices, four phases, source, factorial
normalization, amplitudes/probabilities, tolerance and backend are unchanged.
Full25,740 remains separately unauthorized.

Only the prospective run_004 path/count/native resource notes were changed
in contracts; input closure is still the same eleven paths. Historical
run001/002 failures, pre-launch argv rejection and run003 conditional API PASS
are intact, with their original input revisions retained in Git.

Exact amended bytes:

| File | SHA256 |
|---|---|
| research/P52_naive_replication.py | 2d590822218df9300457923d6fc9f619d15666eae522b96b91aafebd88b5a55e |
| tests/test_p52_naive_replication.py | c9cfed60bd07213bb909f4e5078f7842d1b5d2461fe14f8e1caa44f425e8eb87 |
| research/P52_naive_qualification_contract.json | e182fd651e51f42de22b5fd9b69ef8a59b9cc11ebc889ac9bf434bd241b47f6a |
| research/P52_naive_full_contract.json | f7c073faf567abfc589c609d1b70aa1715f9e230516c4e4b4d63579f89b6ae0a |
| research/P52_naive_validation_contract.md | 9c31883c595f980962ccc4396a7007da21a8d51c810833baec2b027f902bfc27 |

`git diff --check` passed. No test outcome or performance prediction is made.
Awaiting ROOT delta review and explicit fresh qualification slot, followed by
actual receipt review before any independent full probability replication.
