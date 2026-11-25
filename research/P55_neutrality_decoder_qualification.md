# P55 exact neutral-count decoder: bounded qualification

Status: **29 PASS**, one authorized run, no retry, no graph or physical sampler.
This qualifies the finite combinatorial decoder, not a photonic optimization
advantage. The broader research and hardware gates remain open.

Source freeze: `4812e881a3aee34443f0f6d2811d170a61827639`, clean at launch.
Primary module: `research/P55_neutrality_decoder.py`, 96 lines,
SHA256 `59d157f19e20f628e7955abb8c52defc9260f9d77ee36eb055a53e9adef70762`.
Root statically reviewed source/tests/contract before authorizing this run;
the independent analytic reconstruction is identified by `72c9bb99` in the
supervisor's integration receipts. That review is separate from this execution.

## Actual command and bounds

The unchanged six-input contract is
`research/P55_neutrality_decoder_preflight_contract.json`. The Mathbox runner
received exactly its `execution_artifacts`, recorded before/after hashes, and
created the fresh directory `research/P55_neutrality_decoder_preflight/run_001`.
It ran the exact child command recorded in the manifest:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q tests/test_p55_neutrality_decoder.py --junitxml=research/P55_neutrality_decoder_preflight/run_001/junit.xml
```

Runner bounds: CPU20 seconds, wall30 seconds, one conventional numerical
thread, combined logs4 MiB. Logical memory was prospectively budgeted128 MiB;
no hard Darwin address-space/affinity cap or measured peak-memory claim is made.
The CPU cap is enforced but actual CPU usage is not recorded by this runner.
No optical backend, graph generation, phase draw or production RNG was used.

## Observed result and coverage

- Runner: `completed`, exit0, elapsed0.553372 seconds, UTC start
  `2026-11-25T12:22:33.853002+00:00`.
- Pytest stdout: **29 passed in0.31 s**. JUnit records29 tests, zero failures,
  zero errors, zero skipped, aggregate test-body time0.100 s. These clocks
  measure different execution envelopes.
- All six input SHA256 values are unchanged; all three declared log/result
  files are regular and present. Stderr is empty. No failure or retry occurred.
- Exhaustive synthetic tests cover every count composition for N2/4/6 and
  total M0..N (1000 vectors), with every admissible minimizer rank compared to
  independent brute-force balanced subsets. Each route also checks exactly
  one mock `randbelow(ways)` call. These are internal routes within three
  parametrized pytest items, not thousands of separate pytest cases.
- Additional fixtures cover vacuum, one photon, all bunching, all-one counts,
  same-side doublon/hole decoding, odd total without exact neutrality, M>N,
  complement/relabeling law equality, arbitrary-size integers above64 bits,
  and invalid input/rank/resource refusals. Largest actually allocated DP
  fixture is N70/M0,2556 cells. No maximal-domain stress test is claimed.

The installed `validate_manifest.py` accepted the schema-v2 evidence record
against the isolated project root after completion. Inspecting the JUnit and
hashes afterward used only standard-library metadata reads, not another test,
simulation, decoder enumeration or physical experiment.

## Immutable evidence

All evidence is below `research/P55_neutrality_decoder_preflight/run_001/`:

| File | Bytes | SHA256 |
| --- | ---: | --- |
| `manifest.json` | 7578 | `f20b9c5e1a4f8bf84739680b358816224efe209d5733d7a0f3554d6d5a68905a` |
| `junit.xml` | 4670 | `aa1ac464ae86b8404b5b174f7ec40bb4a8cc01985c03e0403ac7f4f8eb7acbb4` |
| `stdout.txt` | 252 | `5267259f63cf198e0ace2e4dbdbb617328a84e416005b15ac35292d613fcfe27` |
| `stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The mock-rank bijection supports uniform sampling when the external integer
oracle is uniform; this is not an assessment of a real RNG's statistical
quality or runtime. Any later experiment must pay the integer DP, validation,
random-bit generation and cut-scoring work and retain out-of-domain failures.
No hardware-compatible label, QPU call or manuscript change follows this PASS.
The exclusive numerical worker was explicitly released after completion.
