# P59 small exact guards: observed qualification receipt

25-Nov-2026. **16 PASS; no full calibration executed.** ROOT authorized this
one qualification only, following complete source/caller and physics static
reviews. The numerical slot was explicitly released after manifest validation.
No automatic main, retry, parameter change, graph or QPU followed.

## Frozen provenance and observed run

Source revision: clean `5c8bfcdd97dfc07bae1f9d97fca51fe243c99dc6`.
Primary source SHA256
`f1d79ac3940b9c02826d0150dcea8470e2ccc9e5f995615b0ead9aa765de0374`;
test SHA256
`7f1da4d13df247082ee115b94232adadd898f2700de1d6efe781ba84a18433c6`;
spec SHA256
`2b0a0564ad4dfb747bae25441cc9ceaac0c8d6590232d31a765b867a6e3ef1e2`.

Interpreter: `/private/tmp/pbp-clean-venv-20261124/bin/python`, Python3.11.15,
pytest8.4.2. Child command:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q tests/test_p59_exact_fixed_response.py --junitxml=research/P59_exact_response_guards/run_001/junit.xml
```

The installed Mathbox v2 runner used the project worktree as root,
`research/P59_exact_fixed_response_guards_contract.json`, exactly its13
execution_artifacts as repeated inputs, fresh output
`research/P59_exact_response_guards/run_001`, and junit.xml as declared result.
Enforced CPU20s/wall30s/environment threads1/log4MiB. Logical64MiB was a planned
scientific-workspace estimate, not an RSS/affinity measurement or hard limit.

Observed UTC start2026-11-25T14:41:44.992287+00:00. Runner runtime0.433988s,
exit0, status`completed`, no missing/invalid results, all13 input hashes
unchanged. Pytest stdout: **16 passed in0.18s**. JUnit records16 tests,
zero failures/errors/skips, suite time0.047s. These clocks have distinct scopes;
they are not interchangeable. Stderr is empty. No cap was reached.

## Scope actually qualified

Ring arithmetic/conjugation; strict integer and decoder-domain rejection;
formal Gram/q/phase placement; two-mode/two-photon HOM with three Fock outcomes;
one independent720-term single-occupation permanent/Fock fixture; Fourier
orientation; all-ones/all-bunch uniform ties and the complete tie-count support;
the ten-class crossing Gram/inversion; known identity/HOM factorial moments;
exact marginal PGF; small occupation coverage and exact proof serialization.

Tests never called `calibrate`, `main`, or six-photon full-source multiplication.
The six-photon work was ONE occupation's720-permutation fixture. The full
source fixture had only TWO photons in TWO modes. The actual15 edge responses,
ten class responses, all462 probabilities and83 phase-invariance checks remain
uncomputed. A passed fixture does not decide their signs or scientific status.

## Immutable evidence and validation

All files below are in `research/P59_exact_response_guards/run_001/`:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| manifest.json |8874|`4192ca5217ad4248c91baa302c4c32686a0abcdaf0ada5714bf17a117840e800`|
| stdout.txt |245|`6715fae78e50c4dc26be4cd4daa6147c63ee0bf7f9ab035cc27c74f1b931266e`|
| stderr.txt |0|`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`|
| junit.xml |2193|`84ef6bf252468b75c555edfaf002bfe42e8ff484f5824b782040f2d89c80ba60`|

Evidence totals11312 bytes. Installed `validate_manifest.py` with this
manifest and `--root` pointing at the worktree returned exit0 and
`valid evidence record (run status: completed); mathematical interpretation
requires review`. This validates provenance and observed guard completion,
not the pending full scientific assertion. No independent physical replication,
graph-optimization benefit, classical separation or hardware claim is made.
