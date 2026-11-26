# P96 pre-execution diagnostic correction: exact-source addendum

26 November 2026. **E1 FIXED; the nominal finite assertion is preserved.**
Outcome: audited, not executed. No remaining execution blocker was found in
this delta. This closes the diagnostic restriction of the original review;
it supplies neither qualification results nor authorization to run main.

## Exact target and coverage

Corrected freeze: `0eabdadc70c2b7085c40b22183320e8655d00e1d`, parent
`ac67650ceaa2bf7639ed72ef6fddb28a02067749`, clean when inspected in
`.local/p81-exact-review`, branch `research/p94-mechanism-design-reuse`.
The complete five-file diff (+76/-18) was read, together with the relevant
unchanged Evidence, setup, native-call, exception/finalization and binding
context. This is a delta review, not a second claim to reread every line of
the new 608-line package. The original full 550-line review remains
`45d73ccfc013cf07f13cc602e95b1f626b58d44a`, report SHA256
`3bd85b48ae620e00c34f0c750113383f77cebe4a001ca86524ecf883e070441c`.
The original source and review are preserved, including their NOT READY verdict.

| File under research/ unless shown otherwise | Lines | SHA256 |
|---|---:|---|
| P96_column_loss_validation.py |366|`ee3592ef608b0b7ad19ba81babcdc369bf4da50e319f3f00baf868074d83c223`|
| tests/test_p96_column_loss_validation.py |134|`a5b7d94dcf9b202fc30309e57e63227700a1c65c5964140e4334535560a45c1a`|
| P96_column_loss_validation_contract.json |37|`a1d17209cc1c032b35f92cf0d93773fe735f0a567d9d901aa26a1240c3becb7d`|
| P96_column_loss_validation_preflight_contract.json |24|`d8fcba7e1794416ceda6b0e7bf1885f5d914a867143b233ad873669611dba629`|
| P96_VALIDATION_POPULATION.md |47|`1642dda4dec65926d35aa84131655a4f9b9e31e86f607563d7ff694d715697d5`|

## Resolution of the failure paths

Source143-152 recursively turns builtin float NaN/Inf into explicit
`nonfinite_float_repr` objects. It keeps finite floats and exact Fraction
strings unchanged. Evidence still uses `allow_nan=False`; the diagnostic
objects are never substituted into mathematical calculations as numbers.
The affected array observations use `.tolist()` and native amplitudes are
converted to builtin complex components, so this cleaning covers those rows.

For each recorded native attempt, source240-246 clears the last-return and
probability repr fields, stores `repr(raw_amplitude)` immediately after the
backend returns, then performs complex conversion. Thus conversion failure
or the post-call `threads()` failure in finally248 retains that return in
failure.prefix. The state does not falsely reconstruct an unavailable
probability if conversion or probability arithmetic itself raises.

If conversion/probability evaluation succeeds, native_raw251-253 is emitted
before the explicit finite-component/probability guard254-255. A nonfinite
observation is therefore diagnostic raw evidence followed by first failure;
it cannot enter the marginal sums or produce a finite-validation PASS.
The returned-call counter advances before conversion now; on a failing path
it counts a backend return, not a successfully validated observation.

Source176-182 forms the full native/six-environment snapshot before asserting.
Its AssertionError carries that snapshot, retained by the main exception repr
and traceback. A post-call drift may still prevent native_raw, but the return
repr and the offending readback both survive. This resolves the finally loss
explicitly identified in the original review, without pretending the call passed.

Root operands211 are emitted before finiteness/eigendecomposition, returned
spectra/eigenvectors214-215 before positivity checks, and U/both Grams/all
residuals224-225 before unitarity rejection. A failing eigensolver has no
invented returned spectrum; its operand and exception remain available.
Both residuals and U now have explicit finite gates. No eigenvalue clipping
or tolerance relaxation was introduced. Ordinary IO/output-cap failure can
still leave a partial prefix; this is not an atomic-storage guarantee.

## Fixtures, invariance and limits

Two unparameterized pure fixtures are added, giving eleven rather than nine.
One tests recursive diagnostics plus strict records/summary/failure JSON in
pytest temporary files; `parse_constant` rejects bare NaN/Infinity. The other
uses a fake Config and monkeypatched environment, checking the exact observed
dictionary in the thread exception. Neither imports/calls a native backend.
They are synthetic diagnostics, not physical samples or an executed full
mock of native_case. Their source plus the static call-order inspection
supports E1 closure; no test PASS is asserted before execution.

The nine original hand-table/population tests are unchanged. The exact PGF,
Fraction/convolution reference, q masses, TV identity and bounds, matrices,
case order and expected outside-domain X4 are unchanged. The physical plan
remains 12 valid plus one invalid-domain physical case, 167 exact signal bins,
159 exhaustive native occupations and 28 unconditional signal marginals.
Input/output orientation, collision factorials, abs1e-11/rel0 tolerances,
eight static paths, external pins, commands, fresh paths and caps are unchanged.
Qualification remains CPU30/WALL60 with its 512KiB JUnit FSIZE; main remains
CPU60/WALL90/log4MiB, scientific8MiB/reserve128KiB, one worker, zero retries.
The contracts/population honestly record the predata correction and eleven
pure items. They do not convert the old unqualified freeze into a failed run.

The exact-audit pre-emission limitation described in the old review remains:
an internal exact assertion may preserve case/T and traceback rather than
every derived table. That disclosed limit does not invalidate the finite
assertion or require instrumentation of every intermediate for E1 closure.
The future actual binding/proof/qualification/auth inputs still need ROOT
review before a separately authorized main. General complex-T correctness,
finite-bit sampling, physical calibration, novelty, matched costs and an
optimization advantage are not supplied by this diagnostic correction.

Only this addendum was written. No import, AST, collection, test, scientific
execution, RNG, native call, runner, validator, delegation, checkout, push,
paper or QPU action occurred; the reviewed package and old proof/review were
not edited by this reviewer.
