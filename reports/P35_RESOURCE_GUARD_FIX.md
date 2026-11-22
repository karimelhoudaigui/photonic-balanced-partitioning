# P35 resource-limit repair

The separate component review56a34d0 found that NaN limits disabled both DP
guards. Old-source exact results remain valid: the archived calls used finite
integer defaults and an outer time-limited runner. The mathematical recurrence
and all190 independently checked marginals were correct.

The repair adds one shared validation function before frame conversion and
before constructor work. Both public entry points now require Integral values
(excluding bool), max_states>=1 and max_transitions>=0. NaN, infinities,
fractional/float values, strings and None fail with ValueError. This is an
intentional tightening of invalid configuration handling; valid integer calls
use the same DP, factorial extraction and counters.

Validation after repair:23 focused tests pass in2.00s, including16 new invalid
limit cases checked at both entry points. The whole repository passes287
tests in18.74s with six existing Perceval cache-permission warnings. No data,
scientific assertion or paper changed in this repair.

The reviewer packet and old source remain immutable. Validate their manifests
at their pinned revision/worktree `.qwen/worktrees/p35-baseline-review`, not
against the repaired module. A current-input hash mismatch is expected across
these two source versions; do not rewrite historical manifests to hide it.
The original review report explicitly excludes the later fix from its verdict.
