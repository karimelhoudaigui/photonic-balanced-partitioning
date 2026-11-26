# P82a code-only population and execution handoff

This is a prospective implementation handoff, not an execution receipt. No import,
AST/bytecode compilation, collection, test, graph generation, seed-hash evaluation,
native query, sample, calibration or DEV run was performed while authoring this
implementation. Execution requires a separately reviewed frozen revision and an
explicit ROOT slot. Qualification passing does not authorize main. The original
145-line design, 147-line card and 69-line clock addendum remain authoritative and
unchanged.

## Prospective qualification population

The qualification command is the exact `planned_command` in
`P82a_split_scatter_preflight_contract.json`. It selects exactly **27 explicit
pytest nodes**, without parameterization. No stochastic sampling or DEV setup
belongs in that population. Native observations total **183 deterministic Naive
amplitudes**:

- Three two-mode, two-photon HOM outputs: `(2,0)`, `(1,1)`, `(0,2)`.
- At each of three phases `0`, `pi/2`, `pi`, all six removed input pairs and all
  ten two-photon occupations of four receiving modes: 180 observations.

Every observation, including exact/tiny zeros and exception representations, is
recorded as a JUnit property before the native assertions. The native absolute
tolerance is `2e-12`, with relative tolerance zero. There is no native eight-photon
source or main-size matrix, no Clifford random draw, no PCG construction, no seed
hash evaluation, no graph generator, no DEV start and no RNG call. The hardcoded
K4/r2 witness must show the exact prequench mean difference
`mean(phi=0)-mean(phi=pi) = -8/225`. The eta-zero branch is analytic: it sets `J=H=0`
and preserves initial phases. Its combinatorial decoder null is independent of
floating Fourier residuals.

Tiny D-decoder/repair fixtures enumerate the finite ordered-draw law; controlled
hooks test the 96-attempt main schedule with mocked compilers, samplers, scorers
and scripted clocks. Those hooks verify control flow and preservation of raw
branches, not real K8 physics or elapsed-time performance. Immutable P43 factory
randomness is mocked whenever qualification exercises that factory boundary.
Portable tests use their executing interpreter. They may verify critical installed
Python source hashes and dependency versions and archive discovered native and
interpreter provenance; they must not require the workstation's absolute Python
path or its Darwin binary hash.

The exact item names, each prefixed by
`tests/test_p82a_split_scatter_veto.py::` in the JSON command, are:

- `test_qualification_executing_interpreter_and_installed_provenance`
- `test_profile_exact_probabilities_and_nonuniform_range`
- `test_eta_zero_is_analytic_graph_independent`
- `test_small_receiver_independent_unitarity_and_phase_update`
- `test_decoder_keeps_collisions_and_deterministic_extremes`
- `test_decoder_uniform_repair_and_d_law_exact`
- `test_decoder_preserves_port_and_vertex_count_mappings`
- `test_eta_zero_all_r_combinatorial_null`
- `test_exact_r2_mean_difference_independent_fraction`
- `test_flat_r2_uniform_loading_cancels_and_marginals_are_phase_blind`
- `test_decoder_rejects_malformed_counts_without_retry`
- `test_all_swap_candidates_match_independent_scalar_cuts`
- `test_packbits_little_round_trip_padding_and_balance_guards`
- `test_quench_returns_best_scored_and_couples_complements`
- `test_quench_best_is_not_last_and_cap_is_not_optimality`
- `test_duration_difference_has_unknown_endpoints_and_cpu`
- `test_duration_difference_rejects_inconsistent_reported_wall`
- `test_dual_clock_uses_last_timely_cached_record`
- `test_dual_clock_no_wall_timely_candidate_and_adapter_subtraction`
- `test_dual_clock_trace_guards`
- `test_conservative_call_boundary_binding_preserves_direct_and_rejects_late`
- `test_scientific_cap_retains_partial_stream_and_failure_reserve`
- `test_scripted_96_attempts_raw_counts_current_refresh_and_tier1_veto`
- `test_scripted_native_fallback_is_first_failure_with_partial_raw`
- `test_scripted_control_exception_overrides_any_partial_veto`
- `test_scripted_mixed_fast_winners_are_not_free_portfolio_veto`
- `test_native_183_deterministic_amplitudes_and_properties`

There is one native item with 183 observations, one portable provenance item and
25 pure/scripted items. Three scripted panels each exercise the 96-attempt schedule; a separate
first-failure panel requests two attempts and preserves one completed outcome.
These panels use fake physical hooks and clocks, not DEV data or sampling.

## Main finite population and stopping meanings

The main is two fixed unplanted n=16/K=8 anchors: ER seed 8201601 with edge probability
0.4, and degree 4 RR seed 8201602. NetworkX 3.6.1 generates topology without a
connectivity or quality filter. Min/max edge pairs are lexicographically sorted;
the frozen private PCG weight role supplies integer weights 1 through 5. Root seed
82026001 and the exact literal role recipe in the spec are not evaluated before
execution. There are three resets with 16 attempts per anchor: 48 per graph,
96 B attempts total and 768 modeled injected source photons. The conditional
receiver sampler handles every realized r from 0 through 8. The r=0 branch has no
native call but retains its paid attempt and eight modeled source photons.
Counts, collisions, zeros, repairs and repeated starts are retained.

The graph/mark compiler precedes the split draw. It uses rho=1, eta=1/2, two phase
sweeps and the fixed loading profile. Q canonicalizes global complements, returns
the BEST SCORED candidate including its input, and credits every evaluated
candidate. Its proposal cap is one complete scan of 64 neighbors; warmstart permits two
scans. No optimal mask, optimum cut, C*, heldout or earlier DEV data is an input.

Tier1 is four complete immutable FAST calls in fixed mode-major order:
random/ER, random/RR, spectral/ER, spectral/RR. Each fixed mode owns the **entire**
per-case B grant, rather than a share or a best-of-mode portfolio. A fixed same
mode must be a valid strict winner on both anchors. A completed FAST veto skips
Tier2 and reoptimized D/species work with `NOT_RUN`/null fields. Without that veto,
Tier2 contains the four frozen custom modes, each with its own complete per-case
grant. The predeclared work guard is 10000 per control call; it is not retuned.

No status accepts a positive claim. Complete surviving output only requests the
separate reoptimized D/species stage. A first exception, timeout, resource/output
failure or missing population is inconclusive, even when a partial prefix looks
favorable. There is no failed retry, seed replacement, fallback sampler or hidden
calibration. All 96 B attempts and all four normal Tier1 calls are necessary for
an accepted fixed-FAST negative conclusion.

## Clocks and witness interpretation

`G_case` is a favorable zero-optics B paid-classical WALL proxy. Disjoint directly
observed paid spans and explicitly derived factory overhead compose it. The
observed factory outer WALL minus helper-reported setup WALL is a
`DURATION_DIFF` prefix-plus-return residual; its endpoints and allocated CPU are
unknown/null. The observed outer CPU remains a separate observation. Returned
setup WALL must lie between zero and observed outer WALL: failure is preserved,
with no clipping. r0 records `NOT_CALLED`, never invented factory timestamps.

A direct control result tests BOTH adapter_CPU+checkpoint_CPU<=G and
adapter_WALL+checkpoint_WALL<=G. The binding witness uses the additional
conservative call-boundary correction below. Immutable P50's complete snapshot and packed mask
exist before its checkpoint clock. Selection uses the latest qualifying
chronological checkpoint; no cost-based favorable sorting, late-best mask/cut
reconstruction or CPU-only returned flag can upgrade it. Custom controls cache
their mask and cut online before both clocks. This is an archived timely RAM
prefix witness, not a hard-return guarantee. Separate real simulation/import/
native/setup/sample clocks are retained and never called physical QPU time.

### Conservative call-boundary binding supplement

This prospective supplement to the unchanged 69-line clock addendum is binding
before any execution. Archive the observed outer call total, directly observed
adapter duration and helper-reported compute duration on EACH CPU and WALL clock.
Define `Delta_C = outer_total_C - direct_adapter_C - reported_compute_C` and the
analogous `Delta_W`. Every operand and difference must be finite and nonnegative;
negative differences cause first failure, with no clipping. Each derived record
references its observed/reported operands. Its interval endpoints are
UNKNOWN/null: the difference includes entry, return and any postfix overhead,
and is not an observed prefix interval. Its CPU value is a duration difference,
not a newly observed CPU interval. This is separate from B's factory duration
difference, whose allocated CPU remains unknown.

Keep `G_case` unchanged. The helper CPU budget remains
`max(0, G_case - direct_adapter_CPU)`. Preserve the direct dual-clock result and
its raw cache. For the final binding witness, however, require BOTH
`direct_adapter_CPU + Delta_C + checkpoint_CPU <= G_case` and
`direct_adapter_WALL + Delta_W + checkpoint_WALL <= G_case`. Choose the latest
chronological cached checkpoint satisfying those two fixed inequalities. This
conservative use of entry-plus-return overhead cannot promote a late best or
reconstruct its mask/cut. The archived direct result remains diagnostic and
cannot override the binding eligibility test. This is still a cached RAM-prefix
claim, not a hard-return or equal-QPU-time guarantee.

## Runner v2 binding and command population

Both JSONs are prospective `run_experiment.py` contracts; the runner creates the
schema-version2 manifest. The exact 15-element `execution_artifacts` array in
each JSON is the required repeated `--input` population. It includes both
contracts, this handoff, design/card/addendum, source/tests/spec, immutable P43/P50
and API card, AGENTS, pyproject and the research dependency lock. No execution
input is an output, absolute path or symlink. At launch, the runner hashes those
project files before and after; the frozen commit, argv and results are recorded
in its manifest.

The installed critical backend files, native extension, two distribution metadata
files, virtual-environment metadata and resolved physical interpreter are outside
the isolated worktree. Their concrete absolute paths and SHA256 pins are the ten
`external_artifacts` records. **The runner does not bind these external records.**
Main CLI independently checks its literal external pins before scientific imports,
enforces the persistent interpreter and records actual provenance. The frozen
execution command uses
`/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python`; it resolves through the
recorded virtual-environment links to the pinned Python3.11.15 physical binary.
This workstation path guard belongs only to CLI/main, not portable fixtures.

Run the installed Mathbox v2 runner from the isolated worktree only after the
separate authorization, with the selected JSON as `--contract`, every listed
project file as an individual `--input`, the declared result path(s) as individual
`--result`, the matching `runner_output_directory` as `--output`, and the exact
`planned_command` argv after `--`. Mandatory runner flags are `--timeout 90`,
`--max-output-bytes 4194304`, `--max-cpu-seconds 60`, `--max-threads 1`. The runner
script is the installed Mathbox4.0.0
`skills/computation-audit/scripts/run_experiment.py`. No wrapper may silently
substitute a different command, input population, output directory or cap.

Qualification declares one JUnit file at
`research/P82a_dev_veto_preflight/run_001/junit.xml`. Main declares exactly eight
scientific files under `experiments/P82a_dev_veto/run_001/data`: `metadata.json`,
`graphs.json`, `B_ER.jsonl`, `B_RR.jsonl`, `paid_ledger.jsonl`, `controls.jsonl`,
`summary.json`, `failure.json`. Fresh runner output directories must not already
exist. Successful `failure.json` records no failure, rather than omitting the file;
early failures retain partial context and unexecuted values remain null/NOT_RUN.
Runner-owned stdout/stderr/manifest files are additional provenance, not one of
the eight scientific results.

## Resources and interpretation

Both prospective slots have CPU 60 s, WALL 90 s, environment/native thread 1, one
worker, zero failed retries, runner stdout+stderr 4 MiB and scientific 32 MiB
**uncompressed**, with 1 MiB reserved for failure/summary context. The logical
workspace plan is 256 MiB; this is not a measured or enforced RSS guarantee. Native
thread configuration and environment values are checked and archived. Output
records stream within the fixed cap; compression cannot make excess scientific
bytes eligible. These values are prospective and were not timing-calibrated.

The runner's POSIX CPU limit is per process; no descendant-aggregate, CPU affinity
or hard RSS promise is made. First-failure/resource status takes precedence over
a nominal scientific status. A successful runner manifest still establishes only
execution/provenance, requiring result inspection and the separate raw audit.
No implementation qualification or DEV outcome proves quantum advantage, fair
total-resource superiority, physical counts, novelty or hardware performance.
