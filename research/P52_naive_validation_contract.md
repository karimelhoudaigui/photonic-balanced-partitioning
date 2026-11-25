# P52 independent Naive replication: preregistration

Implementation authority: ROOT `a78f91af0a789f7660f3fdac218adf4197513713`,
`research/P52_NAIVE_VALIDATION_CARD.md`. Earlier API/source-read proposal:
`8d73dcd96b7ad17df08578ae9956de063426e5bd`. This contract precedes every
scientific import and qualification/run of this validator. No primary P52
implementation is imported. Author proofs and primary source were previously
read for the disclosed static review; the present independence is of the
amplitude evaluation and occupation enumeration, not author blindness.

## Frozen inputs and scope

The six byte-identical reference files under
`experiments/P52_collective_phase/run_001/` come from data commit
`762877a65125e5411e10906ccdb7f64ff280d840`, copied by `git archive | tar -x`.
Their individual SHA256 values are in `P52_naive_replication.py`; the reference
manifest SHA256 is
`d580e0c0473a763257d6e8fecb3be5a7e27b0596d573c6af49b4bb738d7fe1b7`.
The primary script recorded there is
`56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242`.
No ancestry assumption is imposed on a later cherry-picked checkout.

All four phases 0, pi/4, pi/2, 3pi/4, all 6435 occupations of eight modes
and eight indistinguishable photons injected in distinct inputs are retained.
No lost sector is relevant here: this is the eta=1 primary experiment. All
collisions and numerical zeros remain. No mask, conditional renormalization,
probability iterator, threshold, optimizer, random draw, graph or remote
processor is used.

Independent slot-multiset enumeration is aligned to reference occupations by
complete tuple-set equality and a dictionary, not ordering assumptions. A
scalar bit-parity construction independently specifies
`U[4q+j,4b+a]=W[j,a] exp(i b j theta) (-1)^(qb)/sqrt(2)`.
It must match the archived matrix to 5e-12 absolute error, and its unitarity
residual must be at most 5e-12, before a phase's permanent calls. The backend
then receives that archived matrix unchanged. Perceval preserves this supplied
matrix; complex amplitudes are compared directly, with no global or
state-dependent phase fit. This tests engines on identical numerical inputs.

Perceval 1.3.0 `NaiveBackend.prob_amplitude(FockState(n))` constructs the
repeated-row/input-column submatrix, calls exqalibur `permanent_cx`, and divides
by the square root of the input/output occupation factorial product. This is
an independent engine from the primary creation recurrence. It is float64
agreement, not an interval certificate or a verification of the native
permanent implementation's internals.

## Qualification first

After this source/contract/test/input commit, ROOT reviews and grants the tiny
qualification slot. The single bounded child `--mode qualify` runs eight
administrative/analytic pytest guards (third-party plugin autoload disabled),
then eleven checks: HOM CF zero, HOM bunching factorial, a complex 2x2
orientation/amplitude pair at phi=.37, one identity-eight CF amplitude,
vacuum, one known native complex 2x2 permanent, four independent scalar-unitary
residuals. The sixth guard mocks denied/timed-out ps and unavailable platform
metadata without executing ps. The seventh checks JSON roundtrip of builtin
records produced from simulated foreign float/bool-like scalars, without
NumPy. The eighth mocks the official native maximum setter/readback, strict
JSON and a changed post-work maximum, without importing exqalibur. No
production U8 permanent is computed during qualification.

Qualification writes actual Python/package versions, implementation/binary
hashes, `permanent_cx` docstring/signature where available, thread-named exports,
six thread environment values and `ps -M` snapshots before import, after import
and after work. No native thread keyword is guessed. These samples cannot
establish a one-worker native permanent call; absent an exposed documented
control run_003 remained `NATIVE_THREADS_UNVERIFIED`. The actual Config doc
then revealed the official static `compute_max_thread_count` interface. For
run_004 and future full validation, after imports but before any backend or
permanent, the validator records its previous integer value, assigns1 and
requires readback1. It reads back1 again after work before any PASS status.
The requested value/interface/documentation are recorded; no precision or
ptype override is applied. This configures the documented native maximum,
without independently measuring native internals or OS scheduling. An
OSError/TimeoutExpired observing ps produces unavailable/type/errno/error
metadata at all three call sites, and optional platform metadata tolerates
OSError. These observations never infer one native worker. ROOT must
review this actual limitation and approve any full run separately; an API PASS
does not itself authorize production.

Qualification command, inside the Mathbox v2 bounded runner:

```
/private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode qualify --output research/P52_naive_qualification/run_004/data
```

## Full finite check, separately authorized

Only after the actual qualification/metadata review may ROOT authorize the
single full command:

```
/private/tmp/pbp-clean-venv-20261124/bin/python research/P52_naive_replication.py --mode full --output experiments/P52_naive_validation/run_001/data
```

Exactly 25,740 `prob_amplitude` calls, one per phase/state, with no pruning,
fallback, retry or cap extension. Amplitude and probability absolute errors
must each be <=5e-10. Every probability sum must differ from one by <=5e-10.
There is no relative-error claim near zero. Failure, cap exhaustion or partial
coverage remains incomplete/disagreement; phase-by-phase complete arrays and
progress are retained. No decision is made from a favorable prefix.

Outputs are independent occupations plus four complete amplitude/probability
vectors, the aligned reference vectors and matrices, phase maxima, worst
occupations, masses, numerical L1/TV residuals, source/software/input hashes
and actual resources. There is no rescaling of laws. Hashes of inputs before
and after must agree. Existing output destinations or descendants of the
historical reference are refused before scientific imports.

Both modes use Mathbox v2 `run_experiment.py` (SHA256
`06b28f46a55327414ebbc202cd4434b22d6b3a2390979ac7ad65f2eae1a2284a`),
CPU20 seconds / wall30 seconds / six numerical thread limits1 / one sequential
worker / output4MiB; no unsupported Darwin affinity or 64MiB address-space
claim. Planned simultaneously live numerical arrays are <4MiB and every
individual array <64MiB; package process RSS is recorded separately. A native
thread-control limitation is not concealed by these environment settings.
Qualification includes pytest in the same capped process. Runner inputs are
the exact eleven files listed in each JSON execution contract (source, tests,
this MD, both contracts and six reference files); the runner hashes them
before and after. There is no undeclared project import.

Before imports, an explicit `MPLCONFIGDIR` is preserved; otherwise the validator
creates and uses the persistent writable worktree path
`ROOT/.local/mplconfig` (here
`/Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication/.local/mplconfig`).
The actual path, whether set by the validator and whether preexisting are
recorded. This cache/configuration setting changes no mathematics or vendor
code and supplies no warm/cold performance claim; the same CPU/wall caps
include initialization. Cache contents are not scientific inputs.

Runner results: qualification `data/report.json` and `data/guard_junit.xml`;
full `data/report.json`, `data/progress.json`, `data/occupations.npy` and four
`data/replica_theta_i.npz`. Runner manifest/stdout/stderr are separate and
included in the complete receipt. No new method choice follows observed data.

This validates only finite ideal probabilities. It does not validate the
primary MC confidence/LP result, full-law classical replacement, performance,
optimization, heldout generalization, novelty or QPU feasibility. Parent
reports that the primary four mean kernels have classical matches; that
negative result is preserved, not reclassified by a physics replication.

## Observation-only correction after failed qualification

`run_001` and its administrative-argument rejection are preserved in
`research/P52_naive_qualification_run_001_review.md` at commit51712a5. The one
actual child failed on sandbox-denied ps before pytest, NumPy or Perceval, so
the original five guards and eleven checks were not executed. ROOT authorized
only the observation robustness correction, a mock fixture and this prospective
path/count update. No backend, vendor, scientific field/formula, threshold,
reference byte, resource cap or production path changes. `run_002` is fresh and
requires a new source review/slot; this correction does not authorize a retry.
The original source/contracts remain recoverable at d96009f and the unchanged
failure record is validated against that historical input revision.

## JSON-only correction after failed run_002

`run_002` is preserved with receipt50991ab: six guards passed, but report
serialization failed on a NumPy boolean scalar; the eleven check results/API
metadata were not durable and are not reported PASS. ROOT authorized a pure
stdlib `check_record` boundary that converts values to builtin complex-derived
float coordinates, float residual and bool indicator, plus the seventh mock
guard and the prospective run_003 path. Scalar fields elsewhere already use
builtin primitives. Matrix/backend/vendor/source/phase/reference values and
tolerances are unchanged. ROOT separately authorized the optional persistent
Matplotlib cache setting above. Full production remains pending actual
qualification/API-thread review. No corrected qualification is automatically
run by this amendment.

## Official native maximum amendment before run_004

Run_003 at68b8c83 preserves its actual7guards/11checks PASS conditional on
unverified native threads. A separate authorized read-only Config metadata
process (preregistered7286e9e, sealed1f6ec5d) documented the official static
property; no setter ran in that probe. ROOT authorized this prospective setter,
two readbacks and eighth mock guard. The actual maximum before/after and Config
doc are saved in new reports. The permanent doc says its default may choose
Glynn for1/2 threads, Ryser otherwise; the same eleven checks must therefore
qualify this newly configured native path. No invented permanent keyword,
vendor patch, floating precision, physical formula/reference or cap changes.
Fresh run_004 requires source review/slot before execution. Full25,740 remains
pending its actual qualification and separate approval.
