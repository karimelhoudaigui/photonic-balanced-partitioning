# P35 post-fix resource-guard addendum

**Verdict: PASS for the resource-validation repair in `b5d2888f8b7f8cac32e3b5f2cc23ba0d3aa7a547`.** The previously demonstrated NaN bypass is closed at both public entry points. The DP recurrence, extraction and threshold/QUBO arithmetic are unchanged by this patch. This is a separate API/code review, not a rerun of the P35 scientific experiment.

Reviewed production SHA256: `99a827e8057d8dde30b673deec9cbdc89d41e9fbcfd17d05ec16ad0065163f05`. This differs from the pre-fix SHA256 `3a780d09389d80fe5156a86a062c56210378d0ee64ed97d0f1faa994faa5b515` reviewed in commit `6258cd567ff70f922b9547f78ee2e23c82f81dc4`. The pre-fix report, scripts, counterexample and manifests are unchanged. The present receipt does not replace their source hash.

The same reviewer proposed the original P35 API and reviewed the coordinator's implementation, so the independence limits in the earlier report still apply. This follow-up checks the coordinator's repair, not code written by this reviewer.

## Diff and logic

I read `git show b5d2888 -- src/photonic_balanced_partitioning/photonic/threshold_marginals.py tests/test_threshold_marginals.py` from the isolated review branch. The new `_resource_limit` first rejects booleans and objects outside `numbers.Integral`, then rejects integers below the minimum, and finally normalizes accepted integral objects with `int(value)`. The type checks short-circuit before comparing inappropriate objects. NaN, infinity, floats, Fractions, strings and None therefore cannot slip through comparisons with a numeric cap.

Both `vacuum_probability` and `ThresholdMarginals.__init__` invoke this helper for both limits **before consuming the supplied rows/frame**. The minimum is one for `max_states` and zero for `max_transitions`. The integer defaults are unchanged. The internal state/transition guards remain in place; accepting a nonnegative transition cap does not promise that a particular nontrivial calculation can finish within it.

The patch adds 16 parametrized existing-test cases covering two limits and eight invalid values, with both entry points exercised inside each case. No other production arithmetic was modified. Root reported 23 targeted tests and 287 full-suite tests passing; this addendum does not count those as independently rerun tests.

## Separate executed check

`experiments/P35_postfix_review/check_resource_fix.py` loaded the production module directly from the principal checkout's absolute path. Before loading it, the checker required its SHA256 to equal the module blob at the exact fix commit. The same hash was observed after checking. The receipt records that path, commit, command, timestamp, Python version and before/after hashes.

**50 rejection checks passed:** eleven invalid values for each limit at both entry points, plus lower-bound violations. The invalid values include NaN, both infinities, integer-valued float1.0, fractional and integer-valued Fractions, string, None, both booleans and complex1. Each call supplied a sentinel iterable that raises if touched; the intended ValueError occurred first and identified the relevant limit.

Compatibility checks passed for default and explicit builtin-integer caps, an IntEnum integral value, the allowed zero transition limit on trivial cases, and exact answers `5/8` and `[1,0]` on the existing tiny fixtures. Smaller finite caps still raise the expected RuntimeError. Constructor defaults and explicit sufficient integer caps both preserve the deterministic single-photon result. There were no pytest, full-suite, Perceval or scientific-campaign reruns, no generated physical circuits and no hardware shots.

The successful check took approximately 0.030 s with a ten-second CPU cap. Its custom operational receipt is `experiments/P35_postfix_review/receipt.json`; this is explicitly separate from the v2 scientific manifests and makes no new scientific validation claim.

One reviewer-fixture failure is preserved in `attempt1_failure.json` and `check_resource_fix_attempt1.py`: the first compatibility check set `max_states=1` for an occupied unary row, whose constant and degree-one coefficients require two transient states. The expected state-budget RuntimeError exposed that overly tight test fixture. Changing that fixture to two states yielded the successful check; no production change was involved. The first attempt's exact start timestamp was not retained and is not reconstructed.

The repaired guard now matches the finite-integral-limit restriction of the original review. This closes its identified API validation defect. All original mathematical domain, exact-input, bit-cost, finite-range and non-advantage limitations remain applicable.
