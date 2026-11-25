# P66 CI portability correction: independent code and provenance review

25-Nov-2026. **Verdict: PASS static scope, conditional on separate post-fix
verification.** No source blocker, skipped physics assertion or weakened
scientific CLI guard was identified. This is a review of a portability fix,
not an experiment rerun or a receipt that tests/CI have passed.

## Exact reviewed version

Commit `b272df1980e8e040692e4f0e4e397b15898d18cb`. The complete commit patch
and all three changed files were read, as were the unchanged strict guard
and CLI boundary in their current source context.

| File | SHA256 |
|---|---|
| `research/P66_exact_finite_check.py` | `fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d` |
| `tests/test_p66_cli_portability.py` | `445ab66ae5601759e93bd2f995646396efe753f66565410eec33847c976d3667` |
| `reports/P66_CI_PORTABILITY_FIX.md` | `8ad04505098c9f44cf50f095ec9ab58bed4ad753ef5a1485225da228bed5e88f` |

The original native HOM fixture is byte-identical, SHA256
`76025610183aa7d90843ce6e9446d55a49fbb251b8117397516fc09d0bdb2f1f`.
The reviewer read no post-fix process output, test report, CI log, scientific
result or experiment manifest. No import, AST, test, backend query, simulation,
new route, Git mutation or raw-data edit was performed. Only this review
file was written in the separate broken-index worktree.

## Source change and guarded boundary

The sole behavioral source change removes the call to
`persistent_interpreter()` at the start of `native_api()` and adds a comment.
All rational arithmetic, graphs, probability formulas, matrix grids, point
selection, tolerances, native calls, output limits and scientific assertions
are unchanged. Four exact numerical-package version checks, native-thread
assignment/readbacks and observed interpreter provenance remain in the loader.

The supported scientific CLI still calls `persistent_interpreter()` in
`main()` at line523, before `run(output)` at line524. That unchanged guard
checks the resolved contracted interpreter path, actual virtual-environment
prefix and Python3.11.15. It executes before Ledger/output creation, the
exact population and native queries. No exception suppression or fallback
path was introduced. The mathematical source and CLI resource contract are
therefore not relaxed by making the helper portable.

The portable helper intentionally no longer enforces the scientific Python
path/prefix/version profile. Its package versions and actual interpreter
path/hash are observed instead. Directly importing/calling helpers or `run()`
is not the supported guarded CLI and is not a new authorization to launch
a scientific population outside a versioned contract.

## New tests exercise the intended distinction

The first test changes only infrastructure inputs: temporary ROOT, a false
contracted interpreter path and argv. It installs a fail-if-called `run` spy.
The output is inside the temporary ROOT, so the test reaches the interpreter
guard rather than merely failing path validation. It expects the guard's
RuntimeError and verifies that output was not created. This meaningfully
checks rejection before execution/output creation.

The second changes the contracted experiment path while invoking the REAL
loader/backend/point functions. It builds an actual rational 2x2 orthogonal
splitter with coefficients 3/5,4/5,-4/5,3/5, and checks the real CF two-photon
probability 49/625. This expected value is the square of
(3/5)^2-(4/5)^2=-7/25. No native amplitude, permanent or backend is mocked.
Native readback one and actual interpreter identity are asserted.

The frozen five-point HOM fixture is untouched. There is no skip marker,
conditional bypass, replacement expected physics, loosened tolerance or
workflow/version change in this commit. The new pytest.approx bound is an
ordinary real-probability test; it does not claim an interval certificate or
a new scientific point-grid validation.

## Two provenance/documentation qualifications

1. The reviewed report's phrase that no CI test is monkeypatched is broader
   than the code: the TWO NEW tests correctly monkeypatch infrastructure
   constants/argv and a fail-if-called execution spy. The precise statement
   is that the frozen HOM fixture and native PHYSICS are not mocked/skipped.
   This review supplies that clarification; any report correction should be
   made only after the running input-hashed receipt is sealed.
2. The unchanged loaded-module filter at source line277 only captures paths
   containing `/pasqal/.venv/`. A Linux CI installation outside that path can
   therefore produce an EMPTY loaded-module hash dictionary. The portable
   helper still verifies the four package versions, native configuration and
   actual interpreter path/hash, but this does NOT authenticate CI package-
   file closure. Rehashing an empty captured set is vacuous. No such stronger
   CI provenance claim should be made, and the current correction does not
   itself make that filter portable.

These limitations do not block a real pinned-package HOM unit test or weaken
the unchanged Mac experiment CLI. They delimit what its CI provenance proves;
they must not be promoted into a new scientific receipt or complete software
supply-chain validation.

## Historical experiment provenance remains separate

The producer branch still has tip4925feb, with the recorded chain

    88a0573 source -> dcb3aba qualification -> a5ea2b9 reviewed/qualified
      -> daf728d raw main -> 4925feb receipt.

Read-only checks of the frozen producer tree confirm its source remains
SHA256 `4eb143aae8255636e70732c6ab8971fa71df62f15e98daa6e370fc02d247978f`.
Its original fixture76025610 and both execution/preflight contracts retain
the previously reviewed hashes db6c81db/b390ef54. The fix commit changes
only its three listed development files; it changes no historical raw file,
manifest, scientific contract or frozen fixture. This review did not reopen
those raw outputs or independently revalidate their manifests.

Historical v2 manifests must be checked against that matching producer input
tree, such as `.local/p66-finite-check` at4925feb, or a clean checkout/worktree
of the producer revision. The current source is intentionally fb3cf959 rather
than4eb143aa. A current-root source hash mismatch is not a new scientific run
or a reason to rewrite the historical record. A previous pre-fix root check
remains a dated observation of that then-matching input tree.

Any future use of the evolved loader in a scientific qualification/main
requires a new source freeze, contract/input hashes and fresh evidence.
This portability patch does not automatically repeat the 32-point grid,
DEV optimization, held-out testing, or QPU execution.

## Verification status and acceptance conditions

The original CI failure and 1152-pass/1-fail count are ROOT's documented
observation in the reviewed report, linked to
https://github.com/karimelhoudaigui/photonic-balanced-partitioning/actions/runs/45707404987/job/139532781028.
The old loader's Mac profile call is consistent with that stated Linux
failure before HOM assertions; this reviewer did not read its CI log.
No post-fix pass count or CI success is inferred from source inspection.

Accept the correction after the separate full existing-test receipt and CI
check actually pass on this version, with unchanged relevant inputs and
observed native checks. Preserve the original failure, this narrow fix and
its post-fix verification separately. No old science-grid rerun is needed
merely to repair a portable unit-test loader. The positive optimization goal,
QPU readiness and manuscript state receive no new scientific support from
this infrastructure correction.
