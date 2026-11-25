# P63 B + FAST stage-one source and caller contract

2026-11-25. CODE-ONLY freeze for ROOT review. Nothing in this document records
an executed test, graph, sample, calibration, benchmark or DEV outcome.
The normalized stage-one question and corrections are in
`P63_STAGE1_PRE_DATA_AMENDMENT.md`; original P63 card/theory remain archived.

## Exact object, source and randomness

`P63_spsa_fast_stage.py` imports only immutable `P43_global_gain_probe.py`
(including its scientific-library imports) and `P50_fast_from_scratch.py`
from this project. It does not import P48/P45 or any QPU client. P43's local
Perceval/Clifford2017 factory receives the complete square U, source ports
0..17, model bosonic and a separately frozen observation seed. Perceval is
created inside each required native batch. Main imports exqalibur and Perceval
in separate excluded meters before graphs, with maximum1 set after exqalibur
and read back again after Perceval import. Importing creates no circuit/source
or draw. The native factory remains unchanged and sees those warm imports.

`expected_spec()` is authoritative and must equal the complete supplied JSON;
unknown/changed values fail before an output directory or graph is created.
F3/F6 are compiled once from positive-exponent scalar Fourier entries. U is
filled by explicit `(a,i),(b,j)` indexing and then its ordered output rows
0,6 are mixed by the fixed rational matrix. The exact ten Fraction angles
convert to float only for sine/cosine circuit entries. There is no graph
feature, optimum mask, partition, reference solution or alternative mixer.

Graphs are N18 ER seed6301801,p6/17 and RR seed6301802,degree6. On sorted edges,
the P50 PCG64 convention assigns integer weights1..5 using
`seed_for(graph_seed,"weights")`. Supplied graph generation is metered but
excluded from B's allowance. Each algorithm pays its own raw-copy/validation.
Zero total weight is retained inconclusive, never replaced or divided by zero.

Seeds use SHA256 of slash-joined textual parts, first four bytes little-endian:

| Role | Frozen formula |
| --- | --- |
| physical embedding | seed_for(6318000,case_id) |
| direction, ONE per paired step | seed_for(6320000,case_id,arm,step) |
| batch master | seed_for(6330000,case_id,arm,stage,step,sign,trial) |
| observation stream | seed_for(master,"observation") |
| fresh priority permutation | seed_for(master,"priority",shot) |
| future continuous coefficients / multinomial | seed_for(master,role,shot), role coherent_coefficients/coherent_multinomial |
| future phase-average F6/tritter draw | seed_for(master,role,shot,copy), role F6_source/tritter |
| fixed FAST initialization/search | seed_for(6340000,case_id,mode) |

Trained-arm stage labels are `(training,step,plus/minus,0)` and
`(evaluation,3,final,trial0/1)`. Flat-control labels are
`(fixed_fresh,0,flat,trial0..4)`. Roots and all role formulas for all SEVEN
models are predeclared. `seed_namespaces()` performs metadata-only global
uniqueness checks; its serialized table is written before graph generation.
It creates no RNG, phase or count. Only the B streams are subsequently used.
All independent RNG construction explicitly uses PCG64, and native B batches
are separately reseeded by the immutable factory. No favorable embedding is
chosen; each physical-to-vertex permutation is retained for the whole case.

## Count, decoder, optimizer and evidence contract

Every native request is archived before its call; every completed complete
integer count is archived with its batch theta/seed, fresh physical-priority
order, selected physical ports, mapped graph vertices and exact actual cut.
Fresh uniform permutations implement exact uniform ties on integer counts,
without buckets, floating priorities, clipping, conditioning or a greedy repair.
Count conservation, C6 support and expected presence of a collision are guards.
No hidden count/phase redraw is permitted when any guard fails.

Diagnostics use absolute3e-12 guards for both Gram matrices, expected q, row
and column masses and the input-cycle matrix identity. Native Config maximum1
is set/read before the first factory and read again after work. Conventional
thread environment variables are1 before NumPy/SciPy imports. This is not an
OS thread-count/affinity measurement or hard Darwin RSS claim.

All24 training cuts per graph enter their respective four-shot means and
the all-paid incumbent. The update minimizes normalized cut with exact
Fraction arithmetic. Nothing selects a favorable iterate, sign or seed.
The final Theta3 is archived before2x8 fresh observations. Fresh per-graph
mean is `sum(cuts)/(16*total_weight)`; the global mean is the exact equal
average of the two normalized graph means. Paid best includes all40 attempts
per graph and is cached online inside the paid decoder/cut timer.

Raw JSONL gzip records include graph/circuit U/q/Gram/C6 setup, paired probes,
directions, complete counts/priorities/subsets/cuts, exact updates and losses,
frozen final theta, batch timing, and the first failure. Full U is saved once
per unique exact-theta network, maximum seven/case; evaluation reuses its
case-private final network. Per-case context and B summaries, four separate
FAST results, seed table, failure.json and summary.json are fresh exclusive
files. No existing file is overwritten. Fraction values serialize as exact
strings; arrays use integer/float lists and complex U has real/imag parts.

First failure stops the experiment without retry, keeps raw completed shots
and the failing payload, and returns INCONCLUSIVE_FIRST_FAILURE. A hard runner
kill can leave partial raw files without a closed gzip footer or final summary;
the v2 manifest's resource status is then authoritative and inconclusive.
Missing declared outputs are evidence of incompleteness, never permission to
replace a case. The output directory has a1MiB reserve for failure records.

## Timing, guards and outcomes

The B-only grant sums paid raw preparation, half of the shared graph-blind
compiler, each required phase/cache/RNG/source-request setup, postprocessing,
means, updates and online incumbent. Nested diagnostics are excluded. For
factory/setup accounting, only the immutable helper's returned backend WALL
is excluded; its earlier RNG/validation prefix stays paid. Total factory
CPU/WALL is retained separately. Internal optical/classical CPU fields are
None rather than a guessed difference; count-generation CPU/WALL is separate.
Per-graph final/equal-graph mean aggregation is paid, with common costs split
equally over the two planned cases. Evidence IO and imports do not fund FAST.

Each fixed random/spectral FAST call gets the FULL independently measured
B-only per-case WALL, minus actual adapter CPU, converted to its CPU budget.
The solver receives only the original raw graph, own seed, mode, budget and
fixed10k proposal guard. It receives no B mapping, circuit, subset or incumbent.
Its cached online prefix must have an actual finite eligible checkpoint time
within budget. A late overall best is never credited. A timely initialization
can veto; complete first scan and no early guard are required for survival.

One SAME fixed mode matching/beating B's all-paid best on BOTH graphs yields
DEV_REJECTED_FIXED_FAST. A mixed random/spectral best-of portfolio does not.
Otherwise unavailable eligibility yields INCONCLUSIVE_FAST_ELIGIBILITY;
complete eligible survival yields STAGE1_OPTIONAL_CONTROLS_REQUIRED. Every
status has positive_accepted=False. The six optional arms are explicitly unrun;
their means and paid-best comparisons do not exist at this stage. No later
hyperparameter, seed, graph or scope change is allowed from favorable raw data.

Planned arrays are small: fourteen18x18 complex U matrices and q diagnostics,
two integer graphs, exact rational trajectories, eighty count vectors, seed
metadata and four FAST traces capped at10k checkpoints/call. Each checkpoint
has two times, cut/work integers, a three-byte membership mask and a stage;
no full Fock occupation table or phase-average table is allocated. A
conservative logical estimate, including Python/JSON transient headroom, is
below128MiB, within256MiB planned logical workspace. Library/native resident
images and platform RSS are not certified by that estimate. The emitted
traces are projected below24MiB including their duplicate summary rendering;
the scientific-output cap is32MiB. Actual output size is checked between
batches/calls. A surprise cap is retained inconclusive and never raised.

Runtime is NOT established by this projection. The historical P55 timing is
only plausibility context; dense N18 and cold imports remain uncertain. The
exclusive bounded runner must enforce CPU60/wall90, envthreads1 and32MiB logs;
the child also checks the prospective32MiB scientific output. Darwin logical
workspace is planned, not a promised hard address-space/affinity limit. No
extra native18 warmup, canary, qualification draw or calibration is allowed.

## Frozen execution closure and future commands

The two JSON contracts list exact project-relative execution artifacts,
software pins and declared outputs. Use those complete lists as the bounded
runner's repeated --input arguments; no transitive project helper is omitted.
The installed computation-audit runner emits a version2 manifest, input
hashes before/after and actual result hashes. These JSON files are contracts,
not fabricated observed manifests. ROOT must inspect the whole closure and
commit before separately authorizing the following child argv:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest -q tests/test_p63_spsa_fast_stage.py --junitxml=research/P63_spsa_fast_stage_preflight/run_001/junit.xml
```

Qualification has46 prospectively authored items, not yet collected. It uses
deterministic18-mode matrix identities with ZERO native18 draws, a hardcoded
four-vertex graph, exact tie/permanent/SPSA fixtures, mocked timers/FAST/wrappers,
and a real TWO-photon/two-mode HOM source only. An additional hardcoded18-mode
one-edge adjacency uses mocked circuit, physics, factory, counts and priorities.
Mocked B80 integration is not a physical18-photon test. No DEV graph is generated.
Qualification success does not automatically start main or independently
validate a physical18-photon sampler. After a new explicit ROOT decision only:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P63_spsa_fast_stage.py --spec research/P63_spsa_fast_stage_spec.json --output experiments/P63_spsa_fast_stage/run_001/data
```

Use separate new runner parents for qualification and main; the main child
creates its new data directory. Both have zero failed retries. No file here
authorizes a manuscript, external message, hardware preparation or QPU call.
