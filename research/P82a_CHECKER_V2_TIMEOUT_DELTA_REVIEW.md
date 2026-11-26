# P82a checker v2 timeout delta: static review

**Verdict: PASS_STATIC_DELTA; no blocking defect found in the reviewed change.**
This accepts the narrow representation correction for a future separately
authorized qualification. It is not a test PASS, execution authorization or
renewed full recorded-data audit.

Target: clean `.local/p66-dark-barrier` at
`a965e08dbbade4a6ea45d785b0b6fa37af3c8e3a`, compared with parent
`696b4006eb3bab287088b3ff8324691bbe8e5d86`. The complete six-file diff was read:
82 insertions/13 deletions, including all documentation and path changes.
Additional context read: `integer`, `number`, `same`, the helper's actual call
inside `verify_closure`, closure-to-`MainReplay` order, test imports, complete
spec/preflight/TEMPLATE, and the installed Mathbox v2 timeout parser/serialization.
No import/AST/test, RNG/role evaluation, native call or B raw inspection occurred.
The reviewer knows primary P82a outcomes from the producer role and makes no
claim of blindness to them. No other checker verdict was used as proof here.

## Exact reviewed file hashes

| Changed file, relative to reviewed tree | SHA256 |
|---|---|
| `research/P82a_independent_raw_audit.py` | `56a3bb2a686203a4e3752687f7e42170d65a5ccfe5987989fbff333fb39afcfd` |
| `tests/test_p82a_independent_raw_audit.py` | `38383d9e304e26dc3a1f01e7a8d47ab915ed8cc3d1ec3e600b69caa0909d92b4` |
| `research/P82a_independent_audit_spec.json` | `222e9cd9681eb893655dc08671ad794048dcd174a8896a5b3b9ce69745696499` |
| `research/P82a_independent_audit_preflight_contract.json` | `b32aab4db39ab45b0b3c9235dac2ec6bf1689fa9bb2ce1d684c58b240e82a785` |
| `research/P82a_independent_audit_main_TEMPLATE.json` | `14ddd37b03825146923dc7ef484da972a8238620fd5138be772c529de62563c6` |
| `research/P82a_INDEPENDENT_AUDIT_BINDING.md` | `931a66f706be8aada402b40c596e601c05e1039f8a2f3834790055806d521db5` |

## Representation correction and scientific invariance

The installed runner declares `--timeout` with argparse `type=float` and stores
`args.timeout` directly in `manifest.run.timeout_seconds`. Thus a normal wrapper
argument90 is serialized as90.0. The old `same(actual,90,...)` required exact
Python int type and rejected that representation before any `MainReplay` call.
This explains the stated metadata-type failure without using any B value.

The new `producer_limits_checked` first applies unchanged `number`: only exact
builtin int/float types, finite and nonnegative, are accepted and converted to
float. It then requires `same(wall,90.0,...)`, which is exact numeric equality.
There is no `near`, epsilon, clipping or interval expansion. String90.0, bool,
NaN/inf, negative values and any parsed finite value different from90 fail.
Equality concerns the parsed Python numeric value, not arbitrary decimal-text
precision beyond the unchanged JSON parser.

The log4194304, producer CPU60 and thread1 checks retain the original `same`
calls with integer expected values. Since `same` explicitly matches actual and
expected types for int/bool expectations, their floating equivalents and booleans
still fail. Global `same`, `number`, integer/cut/mask checks, residual3e-12,
zero clock tolerance, H-zero rule, replay, scores and decision logic are unchanged.
The helper is invoked exactly where the four old closure checks stood, before
the remaining producer-manifest commit/input/result checks and scientific replay.
Only the valid timeout representation is broadened; scientific predicates are not.

The one added fixture makes22 ordinary test functions: two accepted timeout
representations90.0/90; rejection of90.000001, NaN, string and bool; rejection of
floating log/CPU/thread caps. Each malformed dictionary is a deep copy, and
`deepcopy`, pytest and `AuditIssue` are already available. The valid base leaves
wall as int90 before testing the three other fields, so those failures reach
their intended strict-cap checks. No native or main-replay primitive is added.

## Closure, paths and retained failure

All eleven preflight input paths are unchanged, project-relative and tracked
regular files(mode100644); they include every one of the six modified files.
Qualification argv remains the same synthetic module, with `-B` and disabled
pytest cache, but its JUnit/result/output paths consistently move to fresh
`research/P82a_independent_audit_preflight/run_003`. The source count and spec/
contract counts agree at22. No test was collected to establish this count.

The main TEMPLATE changes only its output/result/runner paths to fresh
`research/P82a_independent_audit_main/run_002`; its binding remains unbound.
The actual dataset-binding file and both new run directories were absent at
review. The eleven-input qualification closure is distinct from the later
main closure, which must still be populated and authorized by ROOT.

Checker caps remain CPU30/WALL60/env1/log4MiB, logical256MiB plan, no hard RSS
claim and zero automatic retries. They must not be confused with the checked
producer caps CPU60/WALL90. The changed spec/MD accurately label this as a
post-seal administrative correction, not a new predata scientific freeze.
The historical failed-run account is ROOT-supplied context; its raw files were
not opened here. No historical output path is edited by the diff.

Strongest safe conclusion: the exact metadata-type mismatch is corrected while
the frozen scientific checker remains unchanged. Qualification003 is still
pending separate ROOT authorization; main002 remains a TEMPLATE, not an active
binding or automatic retry. Runtime behavior is unverified by this static report.
