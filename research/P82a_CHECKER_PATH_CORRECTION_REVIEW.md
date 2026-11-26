# P82a checker: independent path-correction delta review

26 November 2026. **Verdict: corrected path binding accepted statically;
no material blocker found for a separately authorized run_002 qualification.**
No import, AST, validator/test execution, RNG, graph or backend was used.
No B result, manifest or log was opened. Main remains separately gated.

The reviewed clean producer freeze is
`a7e423b28f75f9a5a87068be667c8bf6f1eadd96`, `.local/p66-dark-barrier`.
The complete three-file correction from the previously reviewed `34c95130`
was read: 30 insertions/4 deletions, including the prelaunch corrigendum.

| Changed file | SHA-256 |
|---|---|
| `research/P82a_independent_audit_preflight_contract.json` | `99d5a8bbd5678342c1316a1a87a2b804b939b5673a1a00e66e7e6309c94e8ecc` |
| `research/P82a_independent_audit_main_TEMPLATE.json` | `c11b0c803e4d4f50697b8f6bbb51c8d8360466d659356bd6adac8b84c202ff6a` |
| `research/P82a_INDEPENDENT_AUDIT_BINDING.md` | `301d5722b232c9f276471f33f12446de206faf382622b88bde6dcde168f5538b` |

Unchanged checker/source/test/spec hashes were reconfirmed as
`f595fcaea18dee10b7c89982c2ef700cadca417ec8b2ff63557e95b0e9ba9529`,
`7dc3dfabbe78d9e515098d6eb91cc0446cbe588ed92e0ab103c2fce4b59b84c6`,
and `6fd8c3639aa8bc2c4db407b15d3124d4289a585e507992ab6f07a45be9db8fc9`.

## Decisive installed-runner checks

The installed `computation-audit/scripts/run_experiment.py` was read as text
at lines 170–207 and 225–253, including reserved-file names at line 39.
Its v2 launch requires each declared result to be a strict descendant of a
fresh runner output directory, not a reserved runner file or an input.
Those checks precede output-directory creation and the child launch.

The old `/run_001/runner` output with sibling `/run_001/junit.xml` violated
that rule. My earlier source review did not catch this launch constraint;
the frozen historical review is preserved and this document corrects it.
The producer's corrigendum preserves the rejection as prelaunch evidence,
not as a failed or passed test. No historical archive byte or timing was
independently re-evaluated in this delta review.

Qualification now uses output
`research/P82a_independent_audit_preflight/run_002` and the exact child
`run_002/junit.xml` in both planned argv and declared results. `junit.xml`
does not collide with manifest.json/stdout.txt/stderr.txt. Main's TEMPLATE
similarly uses its `run_001` parent; both unchanged `data/*.json` results
are strict children, and the checker still creates only its fresh data child.
Neither corrected output directory existed at the static filesystem check.

The same 11 unique qualification input paths were compared with the contract
and confirmed tracked/local. No result is an input or lies above/outside its
output directory. Relative paths contain no traversal or reserved collision.
The schema-version-2 structure and all fields other than these path strings
are unchanged. These are static contract checks; the validator was not run.

## Unchanged boundary and disposition

The patch changes no checker behavior, assertion, fixed tolerance, seed,
21-item synthetic population, CPU30/WALL60/environment1/log4MiB limit or
zero-retry policy. No test child ran as part of this correction/review.
Run_001 rejection remains preserved; run_002 requires a distinct authorization
and fresh raw receipt. Main still needs qualification review plus its own
opaque sealed-input binding and authorization. No B-data access or parameter
change is implied. This separate review closes only the prelaunch path defect.
