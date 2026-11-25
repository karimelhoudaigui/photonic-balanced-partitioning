# P65 B80/FAST implementation and execution boundary

25-Nov-2026. CODE ONLY, not imported, qualified or executed. Independent
design review18d344b is integrated asd8c72a9; its two pre-data clarifications
are recorded separately in `P65_PRE_DATA_AMENDMENT.md`. Frozen card/spec022962e
and proof43dd873 remain unchanged. ROOT must read the complete source/tests
and contract, then authorize a single synthetic numerical slot. Qualification
does not automatically authorize the main.

## Dependencies and frozen scientific interface

`P65_cayley_markov_stage.py` imports only these project modules:
`P43_global_gain_probe.py` (seed_for,cut,make_optical_sampler) and
`P50_fast_from_scratch.py` (raw-graph FAST). Their source remains immutable.
P43 transitively imports NumPy/SciPy/NetworkX; it imports Perceval only when
the local factory is called. No P63 source, C6 identity, N18 source or QPU
client is reused. Importing P65 constructs no RNG, graph, matrix or source.
Conventional thread variables are set1 before scientific imports.

The CLI hashes the exact spec bytes against022962e's SHA256
6993da4efe018c80b7fd9021451fad301dd665b1c86c4eac8adab2b1904eeee4.
It also compares the parsed argument to that pinned local spec. Unknown or
changed fields/bytes fail before output/graph creation. There are no CLI
arm, graph, seed, grid, retry or budget overrides. Internal injectable
factory/coin hooks are for synthetic qualification only; main uses P43.

Main constructs exactly the two registered weighted N20 graphs, canonical
sorted edge ordering, PCG64 weights and identity port mapping. Each B case
pays a raw graph copy and all eight private Cayley matrices. Weighted degree
is the exact integer row sum, with rational normalization before float64
conversion. Complex128 solves implement the fixed global matrix; there is
no exact-algebraic main or certified-probability claim. Gram/transpose/q
diagnostics use absolute3e-12,rtol0 and stop without repair on failure.
In ideal arithmetic, H's absolute row sums are at most1 and H is symmetric,
so the 2-norm condition number of I-itH is at most sqrt(1+t^2)<=sqrt(5)
on the frozen grid. This elementary conditioning estimate is not a bound on
all rounded photon probabilities or a calibration result.
lambda0 preserves disconnected components; no ER connectivity filter or
ergodicity claim is permitted. The positive-lambda background is retained
because it is in the PRE-DATA grid, not selected after viewing graphs.

All five arm/count/coin/start/FAST namespaces are enumerated as metadata
before graph generation, without RNG draws. Native count seeds are nonzero;
non-start streams are globally unique within this spec. Common starts are
one logical metadata entry referenced by multiple arms. Metadata integrity
hashing is not paid B optimization; actual B seed derivations/RNG/start work
are repeated inside B's paid algorithm boundary. Independent fresh starts
are sampled WITH REPLACEMENT, retaining any duplicate subsets unchanged.

## Trajectory and score invariants

Every attempt calls a NEW P43 factory with sorted CURRENT ten-port source.
Every request/source/coin seed is archived before sampling. The helper's
returned backend WALL is the only excluded part of factory setup; its earlier
RNG/source-validation prefix stays paid. CPU subdivision is unknown, recorded
as None. Both full factory CPU/WALL and returned WALL are retained.

Full integer counts must have shape20,total10,nonnegative entries and no
fallback. In this eta1 run a wrong total is first failure. A valid collision
is an ordinary paid self-loop with coin=None, no priority or subset repair.
Every CF outcome is scored and consumes a fresh coin, even at acceptance1
or T=S. Count/CF checks, beta/coin work, acceptance, current score, chain-best
and paid-best updates are all paid. Current cuts are actually recomputed
after EVERY attempt; no unperformed score is added to resource counters.

The one common training initial score is copied to eight paid resets. Exactly
two attempts per candidate produce an exact Fraction mean of POST-STEP CURRENT
cuts/W, including collisions/rejects. Selection uses minimum Fraction and
first lex candidate on ties; all unselected candidate scores remain paid-best
eligible. Final selection is recorded BEFORE fresh starts/counts.

Each of three fresh eight-step chains starts with ITS OWN freshly scored cut
and chain-best initialized to that value. Neither training/global best is
used as its state or chain-best. Main records three final chain-bests and
their exact mean, starts, gains, all current/raw proposal scores and their
correlation structure. Counters per case are initial4,current40,proposal=n_CF,
attempted40/completed40. No claim of24 iid observations is made.

Optional D/species/r2/r3 are metadata/design only, never executed by this
program. Re-sorted species groups are not called symmetric/Gibbs. Their
independent selections, five-chain replacement controls and all wider
user-acceptance gates remain required after any surviving first stage.

## Exclusive costs, FAST and failures

Paid B work includes graph validation/W, every H/solve/cache, own seeds/RNG,
source routing requests/copies, immutable pre-clock factory prefix, CF/count
guards, every actual score, acceptance/selection and final aggregates. Pure
matrix diagnostics, source simulation, native imports/setup, raw graph
generation and evidence IO are timed separately/excluded. Each graph pays
its private compilation; the equal-graph mean's small common aggregation
cost is split equally. Optional preparation or serialized evidence cannot
fund the B allowance. This favorable zero-optical-latency envelope is not
practical QPU timing or a full resource advantage claim.

Every paid component is retained in the arm/result `paid_components` ledger
and the matching raw event: preparation, compilation, training/fresh starts,
chain resets, each beta, attempt setup/postprocessing/factory prefix, candidate
fitness, selection, chain finalization, arm finalization and global aggregation
share. Their WALL sum reconstructs B_classical_wall. Beta/start/fitness/final
meter records are explicitly archived rather than inferred from a residual.
The per-attempt factory prefix has cpu_seconds=None; no CPU split is invented.
Ledger/evidence recording is outside those algorithm meters and does not fund
FAST. Synthetic controlled-clock tests must independently reconcile the raw
meters, component counts and sum before main can be approved.

Four independent P50 calls receive the original raw graph and own seed/mode.
Each budget is max(0,B-only case WALL minus actual adapter CPU), with10k
proposal work guard. Trace storage is additionally guarded at20002 checkpoints
per call, a conservative metadata/memory cap, not additional proposal work.
For the immutable helper, every checkpoint except the one anneal_setup follows
at least one new work unit, so10k work implies at most10001 checkpoints. The
20002 guard is deliberately looser than that static bound. Numeric trace
arrays use at most35 bytes/checkpoint (two float64 times, int64 cut/work and
three-byte membership mask atN20), plus stage labels/Python objects/export
overhead. Only one full FAST result is kept while its file is written; case
summaries retain compact eligibility fields, not duplicated trace arrays.
JSON overhead is bounded by the separate32MiB output guard/reserve, without
claiming a strict Python-object/RSS bound from numeric-array bytes.
Only cached eligible prefix snapshots count. A timely initialization can
veto; surviving comparisons need first timely full scan and no early guard.
Only one SAME mode no worse than B on BOTH cases rejects. No free portfolio,
late winner, B incumbent, source state or feature is passed to FAST.

Any first failure takes precedence over a partial veto and stops without
retry. Nonfinite payloads are retained as explicit tagged diagnostic strings,
not converted to numerical evidence. Fresh exclusive files prevent overwrite.
All completed raw events and the failing payload remain in raw.jsonl.gz;
failure.json/summary.json record incompleteness. A hard runner kill may leave
partial gzip/missing result files: the v2 resource status is authoritative,
never a positive/negative scientific gate. Source performs size guards with
a1MiB failure reserve; final summary duplication is checked before writing.

Stage1 statuses are DEV_REJECTED_FIXED_FAST,
INCONCLUSIVE_FAST_ELIGIBILITY,INCONCLUSIVE_FIRST_FAILURE, or
STAGE1_OPTIONAL_CONTROLS_REQUIRED. Every status has positive_accepted=False.
No code automatically chains another run, new graph, retry or optional arm.

## Prospective qualification and commands

Only SMALL synthetic matrix/kernel/weighted/relabel fixtures and mocked
20-count/ten-source trajectories are allowed in qualification. The only true
native source is a two-photon HOM fixture in FOUR modes, at most eight draws,
seed6599001, official native maximum1 configured/read before and after. No
ten-photon canary, N20 compilation/calibration, DEV graph or DEV start draw.
All namespace hashes are metadata only; mocked starts can intentionally all
coincide. The tests independently check weighted normalization, source refresh,
coins on every CF branch, collision self-loops, score counts, fresh/global
best separation, exact selection, prefix accounting, FAST deadlines and
exclusive first-failure evidence. Passing these is implementation qualification,
not independent physical/optimizer replication.

Use the pinned persistent interpreter
`/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python`.
The runner is
`/Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py`.
Both contracts' execution_artifacts must EXACTLY match these repeated inputs:

```text
AGENTS.md
research/P65_cayley_markov_stage.py
research/P65_cayley_markov_dev_spec.json
research/P65_CAYLEY_MARKOV_DEV_CARD.md
research/P65_PRE_DATA_AMENDMENT.md
research/P65_CARD_INDEPENDENT_PHYSICS_REVIEW.md
research/P65_cayley_markov_stage_contract.md
research/P65_cayley_markov_stage_preflight_contract.json
research/P65_cayley_markov_stage_execution_contract.json
theory/P65_collision_counted_photonic_markov_kernel.md
research/P43_global_gain_probe.py
research/P50_fast_from_scratch.py
research/P50_FAST_FROM_RAW_API_CARD.md
research/P50_fast_from_scratch_contract.json
pyproject.toml
requirements-research-lock.txt
tests/test_p65_cayley_markov_stage.py
```

For qualification, pass --root "$PWD", --contract
research/P65_cayley_markov_stage_preflight_contract.json, one --input per
listed path, --output research/P65_cayley_markov_stage_preflight/run_001,
--result research/P65_cayley_markov_stage_preflight/run_001/junit.xml,
`--timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1`,
followed by -- and the EXACT argv in that JSON's planned_command.
No hard --max-memory-bytes or affinity flag is requested on Darwin; logical
256MiB is a prospective workspace plan, not an RSS enforcement claim.

For main, ROOT must first inspect the actual separately sealed qualification
and approve a new single-worker slot. The execution JSON gives the full argv,
the fresh experiment output and all12 --result paths. Use the same17 --input
paths and CPU60/wall90/thread1/log32MiB limits. Scientific files are manually
bounded32MiB separately from runner logs. Validate each actual v2 manifest
with the installed validate_manifest.py MANIFEST --root .; a valid scaffold
or completed process does not certify the scientific assertion.

Source/cache work is small (sixteen20x20 U matrices, no Fock table), but
Perceval/native allocations and import latency are external costs recorded
under their proper scopes. One numerical worker and zero failed retries.
The source/contract freeze is not proof that execution fits these caps.

No paper, old data, C*, held-out graph, QPU credential/call, Laurent message,
or positive research conclusion is produced by installing this program.
