# Exact density-success scope receipt

Completed bounded check at density-certificate base `75e5831`; no circuit/graph sweep, training, random sampling, or QPU. The underlying 75e density theorem is inherited, not independently certified by this receipt. All ten Fock outcomes for each of seven fixed cases are retained as exact fractions.

## Checked conclusions

- Raw TV and expected bosonic collision pairs both equal M. Raw optimum probabilities are M and M/2, with acceptance 1-M and 1-M/2.
- Conditional TV is exactly M/[(1-M)(2-M)]. The bound with max(P(CF),Q(CF)) holds exactly, and is attained at the fully mixed endpoint (conditional TV=2/3).
- At the zero-angle endpoint both success probabilities are zero; no numerical success ratio or finite waiting time is assigned.
- A separate HOM control rejects conditioning on zero bosonic CF mass, despite positive distinguishable CF mass.
- A classical control using the supplied two mode groups has success one for this deliberately aligned path example. Its sampling function has no optimum/graph input. This is a structural counterexample to overclaiming, not an algorithm benchmark.

| fixed example | M=raw TV (rounded) | raw success ratio | conditional TV (rounded) | density envelope epsilon (floating diagnostic) |
|---|---:|---:|---:|---:|
| Pythagorean_t_1_over_8 | 0.11384072 | 2 | 0.0681094665 | 1 |
| Pythagorean_t_1_over_32 | 0.00776686487 | 2 | 0.00392908898 | 0.00994471322 |
| Pythagorean_t_1_over_128 | 0.000488102471 | 2 | 0.00024423002 | 0.000515103661 |
| Pythagorean_t_1_over_512 | 3.05168796e-05 | 2 | 1.52591383e-05 | 3.09170924e-05 |
| Pythagorean_t_1_over_2048 | 1.9073459e-06 | 2 | 9.53675681e-07 | 1.91351878e-06 |
| zero_angle | 0 | undefined (both zero) | 0 | 0 |
| fully_mixed_endpoint_rational_frame | 0.5 | 2 | 0.666666667 | 1 |

The floating exp/sqrt envelope column is not interval arithmetic. The exact rational probabilities, not that numerical column, establish the rare-event counterexample. Occupation first means stay exactly 1/2 in every mode; this does not mean that all nonlinear objective expectations are unchanged.

For positive M, physical raw first-hit attempts are 1/M for bosons and 2/M for the independent reference. Their ratio persists while both costs diverge. Absolute TV guarantees relative inverse-probability control only when the reference event probability exceeds epsilon by a controlled margin.

## Provenance and commands

Recorder status `completed`, exit 0; start `2026-11-21T20:45:24.233639+00:00`. Its v2 manifest records actual commands, Python version and before/after input hashes. The validator returned `valid evidence record (run status: completed)`.

```sh
../../../.venv/bin/python -B experiments/P33_density_success_scope/check_exact.py \
  --output /private/tmp/pasqal-density-success-reproduction-new.json
../../../.venv/bin/python -B /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  experiments/P33_density_success_scope/run/manifest.json --root .
```

The check uses only the Python standard library and refuses to overwrite an output file. Receipt paths/times can change on replay; exact mathematical fractions should agree. No source module, shared status, manuscript or QPU gate was changed.

Raw SHA256: `9c58d9780a7552203f0103f9057ee7e915457e2d4eb11baf7a94c8f880ef19da`.
Theorem-note SHA256: `76d4ac6ac3869d47df49427a3fd5a6c17418cb4fd3e1175893192a19e93b3b13`.
Exact-check SHA256: `8e8b58d89f6afb172c9bd89c90ee8c16165e4a8fe3ce3455c6b3422a70c1b3f1`.

Regression at the same isolated base: `PYTHONPATH=src ../../../.venv/bin/python -B -m pytest tests/ -q -p no:cacheprovider` completed with **201 passed, 9 local Perceval cache warnings**, in 20.44s. No production source or existing tests were changed.
