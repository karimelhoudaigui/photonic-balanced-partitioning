# P63 stage one: independent adversarial static source review

2026-11-25. **Verdict: static source/caller check passed within the frozen
stage-one contract; no material defect found that reverses its nominal verdict
or enlarges its B-only grant. Execution qualification remains pending.** This
is not an executed test, sampler validation, physical replication, positive
result, runtime estimate or authorization to run.

The review was performed in a separate same-team subagent/worktree, with shared
parent context. Preliminary reading preceded the source freeze; the final
freeze and its final changes were then checked. No author source, test,
contract, dependency, graph or scientific result was edited.

## Exact reviewed object

Reviewed original commit: `8b20dca7bbe476a2eed75433b31e5ca582809484`.
Its worktree `.local/p63-physics-review` was clean when checked. Exact hashes:

| Artifact | SHA256 |
| --- | --- |
| `research/P63_spsa_fast_stage.py`, 651 lines | `7f60cb437a9936323851d926ca18f16c7899b16a8d5353c69df88cf21a03d5d6` |
| `tests/test_p63_spsa_fast_stage.py`, 648 lines | `1bf5baac5740e75a37096dd841c10d4b5486691811259062bd15a569f7d2bd9b` |
| `research/P63_spsa_fast_stage_spec.json` | `5eea4f4c46789effa5102f6f1d5f71bb9de6d2c8b050c3cb3920bef2a67877dd` |
| `research/P63_spsa_fast_stage_contract.md` | `74262584762abda98b6e9e627b332817b2fa8aa11c210e75b9f65dd2737604e3` |
| `research/P63_spsa_fast_stage_preflight_contract.json` | `9fa288deeb562e31516fac0b8d2f1ba331c25c9dad448dbe44a2f80f0683dea6` |
| `research/P63_spsa_fast_stage_execution_contract.json` | `5232bf44880b092cce603b242391882b0ec3a63f0c0577fd2dde98697d343482` |
| `research/P63_STAGE1_PRE_DATA_AMENDMENT.md` | `08214cc0c05760359ffc637318fac60f7deb1cf683675e637008c1f63b1e53b4` |
| Immutable `research/P43_global_gain_probe.py` | `b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777` |
| Immutable `research/P50_fast_from_scratch.py` | `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86` |

The complete source and tests were read, together with the spec, both JSON
contracts, amendment, caller contract, P63 architecture/theory and earlier
static physics review. P43's actual cut/factory and P50's actual validation,
initialization, descent, checkpoint, guard and export paths were read. The
P50 API card, P55 pre-data timing clarification, repository AGENTS and pinned
dependency files supplied the corresponding interface requirements.

## Checks and decisive evidence

| Obligation | Static finding |
| --- | --- |
| Optical matrix convention | `circuit()` uses positive Fourier entries, rows `(a,i)` and columns `(b,j)`, phases indexed `(b,i)`, followed by the ordered output-row mixer on ports 0,6. This implements the amended ten-phase family; it is not an input-row/mapping transposition. |
| q, locality and C6 | The two mixed rows use phases fixed at color zero; the other rows retain the prescribed magnitudes. The column-cycle diagnostic uses the same positive Fourier sign. With full input `1^18`, its input cycle has eigenvalue one, so allowed outcomes satisfy the declared color-weighted residue. Collision-free `1^18` has the incompatible residue. The collision requirement is therefore a diagnostic consequence, with no retry or accepted-count conditioning. |
| Native full-count source | P43 receives the entire 18x18 U and distinct source ports 0..17, model `bosonic`, and the observation seed. Its local Clifford backend sets occupation one on every input and returns all output counts. No remote processor, CF-only factory or species fallback is invoked. |
| Decoder and mapping | `rank_counts()` ranks physical ports by descending integer counts and fresh permutation rank, takes nine, then maps through the retained physical-to-vertex permutation. Sorting the returned set does not change its cut. `base.cut()` sums the actual selected-to-unselected edges once. |
| SPSA | Each step constructs one ten-coordinate direction, then both signed probes from that same direction. All four cuts/sign enter exact normalized Fraction means. The update subtracts the signed finite-difference gradient; no minimum, incumbent clipping, best-iterate selection or sign-dependent direction enters it. |
| Budget and final freeze | Three paired four-shot steps contribute 24 training requests per case; two final-theta batches contribute 16 fresh requests. The final theta is emitted before those fresh batches. The online paid best sees both training and fresh cuts. Only B executes in stage one; seven-arm seed metadata is not seven executed models. |
| Seed ownership | Graph weights, embedding, directions, observations and carried priorities use separate declared role formulas. Batch seeds differ by sign and trial. Metadata registers all later arm roles before graph generation and rejects a collision without searching a replacement. No DEV graph was generated to check this table here. |
| Network cache | The exact Fraction key is private to each case. Six signed training networks plus a final network are the maximum possible distinct keys, checked before construction. Repeated final batches reuse U but construct independently seeded observation factories. |
| B classical grant | Paid blocks cover graph copy/validation, mapping, half the shared graph-blind Fourier compiler, own circuit/cache/RNG/source-request setup, priorities/decoder/cuts/incumbent, all updates and actual means. Equal-graph mean aggregation is split equally. Supplied graph generation, imports, simulator/count work, diagnostics and evidence IO are excluded as prospectively declared. Optional arms supply no time. |
| Factory prefix and nested clocks | P43 constructs its NumPy RNG and validates source ports BEFORE its internal backend clock. The caller subtracts only the RETURNED backend WALL and the nested diagnostic WALL from its total setup WALL. It does not subtract the whole factory. Final source lines 368--369 also require finite nonnegative backend WALL no greater than the independently measured factory WALL, within the frozen tolerance. Total factory CPU is retained; unavailable internal CPU splits stay `None`. |
| Adapter and raw FAST input | Each random/spectral call receives only the original raw graph, its own seed/mode, the fixed 10k guard and `max(0,B_classical_WALL-adapter_CPU)`. The adapter seed preparation is timed. No B incumbent, mapping, optical matrix, priority, spectral feature or other-arm cost is passed. |
| Online timing eligibility | P50 prepares the best subset and packed snapshot before its checkpoint clock. Only a timestamp within its CPU allowance enters the eligible snapshot; later completed work remains audit-only. The caller checks a finite in-budget timestamp and online-cache flag. A timely initialization can veto; survival additionally requires the timely first scan and no early guard. |
| Same fixed mode on both cases | `classify_stage1()` requires two distinct cases and both modes. It checks one same mode against B's all-paid best on BOTH graphs, rather than selecting the better mode separately on each graph. Veto precedes the stronger survival-eligibility condition. Every outcome keeps `positive_accepted=False`. |

The direct algebra above checks implementation conventions against the frozen
internal theory. It supplies no new N18 decoded-response or distributional
simulation claim. The old architecture card's ambiguous direction wording and
optional execution order are resolved by the later explicit stage-one amendment,
spec, source and caller contract.

## Resources, failures and the final freeze changes

The 10,000 limit is per FAST call, with four calls. In immutable P50, work
counts initialization, scan deltas, anneal deltas and restart/perturbation work.
At N18 a full scan consumes 81 work units. Every checkpoint consumes positive
guarded work except the single anneal-setup checkpoint, which follows a full
initial scan; this gives slack for the stated checkpoint bound. The caller
rejects an unexpectedly longer trace. This is a trace/work guard, never a
claim that its work units equal B shots or wall time. An early guard may still
leave a valid negative prefix but cannot certify favorable survival.

The final native import path was checked explicitly: exqalibur is imported in
its own excluded meter; documented maximum threads is set/read to one; Perceval
is imported in another excluded meter; maximum one is read back again before
the compiler and graph loop. It is read after work as well. Environment thread
variables are set before scientific imports. These are configuration/readback
checks, not OS affinity or actual thread-count measurements.

Output directories/files use exclusive creation. Each shot request is emitted
before the native call; invalid completed counts stop the trajectory. The
exception path retains completed evidence and requests no replacement. Its
partial failure record lists completed cases/modes/counts without duplicating
all stored FAST traces. The final change also serializes/sizes the full summary
before writing a successful final status: if the duplicate rendering would
consume the reserved MiB, it writes an inconclusive compact summary instead,
leaving raw and per-call evidence. The earlier unguarded final-summary concern
does not apply to the reviewed hash.

The child checks output size between batches/calls and CPU/wall consumption
relative to the scientific-import clock. Hard process limits, closed-manifest
status and declared-output enforcement remain obligations of the separately
authorized bounded runner. Library calls, final serialization and OS failures
are not interruptible/persistable at every instruction by this module. A hard
kill may leave partial gzip/missing final outputs; the contract already treats
that as inconclusive without retry. The logical 256MiB workspace and projected
output size are prospective bounds, not measured peak memory, an OS RSS limit,
or a completed-run observation. No native Fock table is allocated by this
Python source. The native library's actual allocation is not certified here.

## Closure and qualification boundary

Both JSON `execution_artifacts` lists contain the stage-one source/spec/tests,
all amended contracts, architecture/theory/review, immutable P43/P50 helpers,
P50 interface/contract, P55 timing amendment, AGENTS and dependency pins. Static
project imports introduce no further helper. No `conftest.py`, `sitecustomize.py`
or `usercustomize.py` was found in the project file search. This does not audit
every third-party package or pytest plugin.

The actual interpreter path in BOTH planned argv lists is the existing
`/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python`, not a nonexistent
worktree-local environment. Read-only symlink inspection finds `python3.11`
under Homebrew; `pyvenv.cfg` declares Python3.11.15 and the persistent root
environment. Imports resolve the worktree's source: direct execution places
the script's `research` directory on Python's module search path, while the
test fixture explicitly inserts that directory. The lock lists the declared NumPy/SciPy/NetworkX/Perceval/exqalibur/
pytest versions. Installed-package versions were not imported or independently
qualified by this review.

The qualification suite was inspected statically, not collected or executed.
Its native fixture uses only two photons/two modes and eight HOM requests;
18-mode matrix fixtures are deterministic. Its toy four-vertex cuts and mocked
18-mode one-edge counts/trajectories do not generate either DEV graph or sample
the 18-photon source. They exercise signed probes, full training means, carried
ties, case-private caches, factory-prefix accounting, first invalid count,
timely/late FAST snapshots, adapter CPU and fixed-mode logic. The suite does
not execute `execute()` end to end; static control-flow review covers its final
import/output changes, and any later run must still have the full runner/input
closure. The declared 46 pytest items remain prospective, not a reported PASS.

No Python/project/scientific module was executed or imported in this review;
no pytest collection, graph/RNG construction, phase/count draw, calibration,
benchmark or QPU call occurred. Shell reads, Git metadata and file hashing were
the only inspection tools. Only this review file was added in the reviewer's
own worktree. No independent numerical replication, merge-test completion,
useful optimizer result, novelty clearance or QPU authorization follows.
