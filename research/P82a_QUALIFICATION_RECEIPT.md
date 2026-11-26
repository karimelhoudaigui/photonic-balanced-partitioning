# P82a unique deterministic qualification receipt

26 November 2026. **QUALIFICATION PASS; MAIN NOT RUN OR AUTHORIZED BY THIS RECEIPT.**
The single authorized qualification ran on clean commit
`94f80b94f75317524c202ce9ef5bf932d78ddc5e`. Its four raw files were committed as
`8e6ba06645954a0113b8d473eaf4648c7dbf4221` immediately after the runner returned,
before reading JUnit, logs or manifest contents. Only the runner's necessary
`completed` status was observed before that seal. No retry occurred. The numerical
slot was released after the raw commit; subsequent work read sealed records and
validated provenance only.

## Execution and binding

The exact `planned_command` from
[the preflight contract](P82a_split_scatter_preflight_contract.json) ran once
through the installed Mathbox4.0.0 `computation-audit/scripts/run_experiment.py`
v2 runner, with all fifteen contract `execution_artifacts` supplied as individual
`--input` arguments, the declared JUnit `--result`, and the fresh output directory
`research/P82a_dev_veto_preflight/run_001`. No `-x` or fail-fast option was added.
Post-seal parsing confirmed exact command equality and exact ordered equality
between the 27 JUnit node names and the 27 literal contract nodes.

The wrapper used `--timeout 90 --max-cpu-seconds 60 --max-threads 1
--max-output-bytes 4194304`. Its environment set `PYTHONDONTWRITEBYTECODE=1` and
OMP/OPENBLAS/MKL/VECLIB/NUMEXPR/BLIS thread variables to1 before child execution.
The persistent interpreter was
`/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python`. No core-affinity or
address-space limit was requested: manifest `memory_bytes` and `max_cores` are
null. The 256MiB logical workspace plan is not a measured or enforced RSS claim.

[The v2 manifest](P82a_dev_veto_preflight/run_001/manifest.json) records:

- Started at `2026-11-26T01:11:23.553679+00:00`; clean source commit94f80b94.
- `run.status=completed`, exit0, runner elapsed29.445581s.
- All15 input SHA256 values identical before and after; no missing/invalid result.
- All three runner checks true: unchanged inputs, successful bounded process,
  declared regular result present.
- Python3.11.15, NumPy2.4.6, SciPy1.17.1, NetworkX3.6.1,
  Perceval1.3.0, exqalibur1.4.2, pytest8.4.2; macOS26.2 arm64.

The installed validator was run **after the raw seal**, using
`validate_manifest.py research/P82a_dev_veto_preflight/run_001/manifest.json
--root /Users/karimelhoudaigui/Desktop/pasqal/.local/p65-independent-audit`.
It exited0 and reported `valid evidence record (run status: completed)`.
CPU60 is the enforced per-process limit; actual CPU consumption was not reported.
Runner elapsed time, pytest elapsed time and JUnit suite time have different
boundaries and are retained separately rather than equated.

Relevant unchanged execution inputs:

| Input | SHA256 |
|---|---|
| Source | `7e1a0d037f5fe0a6af036c1b2a92e765981c93e8d473535984e6f07ea7acfbbc` |
| Fixtures | `e70b74c2915632cf62677c80f40ebeea8e67c669116660096426101542794861` |
| Literal spec | `8598bd4220d1caadb20aed68601e92b4bba85db787bfe71b83efb6376151c838` |
| Preflight contract | `209696de0b0170ff4099cdfd77b6acdaec3c4f78e04e86631047008c13517c0d` |
| Main contract | `dca509b4fee65b652227fb395cfc982b4426a9c8ae0da05de75f825493cc5f20` |
| Population/binding MD | `9080adee7e67189731cdbcbd297c0b419748337025135f85cf7406bee5c1a4ba` |

The complete fifteen-input hashes, including immutable design/card/addendum,
P43/P50/API card, AGENTS and dependency files, are in the sealed manifest.

## Actual qualification population

[JUnit](P82a_dev_veto_preflight/run_001/junit.xml) contains27 tests, zero failures,
zero errors and zero skips, in the contracted order. Its suite time is28.308s;
[stdout](P82a_dev_veto_preflight/run_001/stdout.txt) reports
`27 passed, 8 warnings in 28.46s`. Each following exact suffix has prefix
`tests/test_p82a_split_scatter_veto.py::` and passed:

| # | Node suffix |
|---|---|
| 1 | `test_qualification_executing_interpreter_and_installed_provenance` |
| 2 | `test_profile_exact_probabilities_and_nonuniform_range` |
| 3 | `test_eta_zero_is_analytic_graph_independent` |
| 4 | `test_small_receiver_independent_unitarity_and_phase_update` |
| 5 | `test_decoder_keeps_collisions_and_deterministic_extremes` |
| 6 | `test_decoder_uniform_repair_and_d_law_exact` |
| 7 | `test_decoder_preserves_port_and_vertex_count_mappings` |
| 8 | `test_eta_zero_all_r_combinatorial_null` |
| 9 | `test_exact_r2_mean_difference_independent_fraction` |
| 10 | `test_flat_r2_uniform_loading_cancels_and_marginals_are_phase_blind` |
| 11 | `test_decoder_rejects_malformed_counts_without_retry` |
| 12 | `test_all_swap_candidates_match_independent_scalar_cuts` |
| 13 | `test_packbits_little_round_trip_padding_and_balance_guards` |
| 14 | `test_quench_returns_best_scored_and_couples_complements` |
| 15 | `test_quench_best_is_not_last_and_cap_is_not_optimality` |
| 16 | `test_duration_difference_has_unknown_endpoints_and_cpu` |
| 17 | `test_duration_difference_rejects_inconsistent_reported_wall` |
| 18 | `test_dual_clock_uses_last_timely_cached_record` |
| 19 | `test_dual_clock_no_wall_timely_candidate_and_adapter_subtraction` |
| 20 | `test_dual_clock_trace_guards` |
| 21 | `test_conservative_call_boundary_binding_preserves_direct_and_rejects_late` |
| 22 | `test_scientific_cap_retains_partial_stream_and_failure_reserve` |
| 23 | `test_scripted_96_attempts_raw_counts_current_refresh_and_tier1_veto` |
| 24 | `test_scripted_native_fallback_is_first_failure_with_partial_raw` |
| 25 | `test_scripted_control_exception_overrides_any_partial_veto` |
| 26 | `test_scripted_mixed_fast_winners_are_not_free_portfolio_veto` |
| 27 | `test_native_183_deterministic_amplitudes_and_properties` |

The exact Fraction fixture passed the **unconditioned r2-sector contribution**
`mean(phi=0)-mean(phi=pi)=-8/225`, consistent with the frozen design's convention;
it is not a mean renormalized by the probability of r2. The uniform-loading and
eta0 nulls, repaired D law, scalar swap/canonical quench checks and typed duration
links passed in their specified tiny/scripted domains. Main-size workflow hooks
used literal mock compiler/sampler/scorers and clocks, including all-r branches,
partial first failures, each custom policy, work guards and late cheaper caches.
Their PASS does not validate real DEV timing or an eight-photon trajectory.

## Native observations, zeros and provenance

The native JUnit properties report planned=attempted=actual=**183** deterministic
Naive amplitude queries: three HOM outputs and180 K4/r2 points. Each of three
phase IDs has60 observations; the180 `(phase, removed pair, occupation)` tuples
are distinct. Native errors are an empty list. Every observation and its amplitude
representation is present in the properties, recorded before assertions.

- HOM probabilities, in `(2,0),(1,1),(0,2)` order, are
  `0.4999999999999998, 0.0, 0.4999999999999998`.
- Across183 records there are65 exact-zero expected probabilities and65 observed
  probabilities equal to zero. No expected zero was replaced by an omitted row
  or a positive tiny value.
- The largest absolute recorded-probability residual from its stored exact
  Fraction reference is `2.220446049250313e-16`; the predeclared tolerance was
  absolute2e-12, relative0. No tolerance was changed.

All six environment thread values were recorded as1 before native setup,
after configuration and after the queries. The native Config readback was0
before configuration, then1 after setting it,1 after importing Perceval and1
after the queries. The initial0 is an unconfigured readback, not a measurement
of active threads; the registered native queries followed configuration to1.

The provenance property has no errors. Its five Perceval Python source SHA256
checks all match the frozen pins; Perceval1.3.0 and exqalibur1.4.2 match. It records
the actual native extension at the persistent environment path with SHA256
`b4687bc81b37cb447eb0c9c4fa89523da7feed8584a31ca74798ac3bcee06749`, and the executing
interpreter resolving to
`/opt/homebrew/Cellar/python@3.11/3.11.15/Frameworks/Python.framework/Versions/3.11/bin/python3.11`
with SHA256 `831807be3d255aae0708810462ce0cde2467235f7daaa86e93d0ddc58b1a4101`.
Both actual binary identities match the literal workstation pins. Qualification
was portable and did not impose the Mac path/binary guard. It did not exercise
main CLI's complete ten-external-artifact enforcement; the v2 runner binds the
fifteen project files, not those external paths.

Eight warnings are preserved, with no source edit or rerun:

- Two pytest warnings say `record_property` is incompatible with xunit2, one for
  provenance and one for the native item. The properties were nevertheless
  present and successfully parsed from the sealed JUnit file.
- Three Perceval warnings report inability to read/write its default persistent
  user folder; three report use of the existing temporary folder. No backend
  fallback or count retry was used: these warnings concern storage setup.

## Sealed outputs and limits

| Raw file | Bytes | SHA256 |
|---|---:|---|
| `junit.xml` | 70044 | `b46f164eb7b2b668e474c781157d6bd393011dc9d6e30a003779d6384901ad64` |
| `manifest.json` | 13216 | `1c068598e1327bc3d4988b8be9f90b3ab878e6802048f0edccb447a08d831b0b` |
| `stdout.txt` | 2243 | `038be61c64033bbd551a8e660d808d62e3feb26286243e9d95aaffd8198f8529` |
| `stderr.txt` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Total raw output is85503 bytes, uncompressed. Combined logs are2243 bytes,
below4MiB; JUnit and all raw files are below32MiB. The 1MiB final reserve and
logical256MiB plan remain prospective main policy; qualification tested the
writer's reserve behavior on its registered tiny fixture and did not measure RSS.
No output was replaced, compressed, discarded or repaired.

This result qualifies only the registered finite fixtures under the recorded
floating tolerance/library versions and scripted paths. It generated no DEV
graph, no real PCG role stream or seed digest, no stochastic Clifford sample,
no actual P43 factory/P50 optimizer call, no real K8 matrix or eight-photon
native source. P43/P50 were hash-bound inputs; the workflow boundaries were
mocked. No QPU, optimizer outcome, heldout, fair total-resource conclusion,
quantum advantage or novelty conclusion follows. **MAIN remains a separate
ROOT decision after raw/receipt inspection and the independently frozen checker.**
