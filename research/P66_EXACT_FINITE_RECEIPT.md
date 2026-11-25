# P66 exact finite diagnostic: executed receipt

25 November 2026. **PASS_FINITE_ASSERTION** for the prospectively fixed
finite grid, with a numerical point reference conditional on its declared
tolerance. This supports implementation conventions of P66; it does not
replace the universal proof or establish an optimization advantage.

## Source, review and qualification

Original source freeze `88a0573907b503fe2b624d13920430353d27e779`:

- source526 lines, SHA256
  `4eb143aae8255636e70732c6ab8971fa71df62f15e98daa6e370fc02d247978f`;
- nine fixtures138 lines, SHA256
  `76025610183aa7d90843ce6e9446d55a49fbb251b8117397516fc09d0bdb2f1f`.

ROOT read the complete source/fixtures/MD/both JSONs, including final
pre-data native-archive changes. A second agent independently reviewed the
same complete files and installed primary NaiveBackend source without
opening any qualification/main output. Its conditional review SHA256 is
`440afb11f181e1b3a28ab0d8e6869e125a4425d1bf2435b003d42fe3c6bc12b3`,
preserved byte-identically in `P66_FINITE_CHECKER_SOURCE_REVIEW.md`.

One qualification at clean88a0573, raw **dcb3aba**:9PASS, pytest27.86s,
runner28.553662s. The five two-mode/two-photon native HOM probabilities are
archived in JUnit before assertions (observed0,0.5000000000000002,
0.5000000000000002,0.2500000000000001,0.5000000000000002). No random sample,
main-family graph, K4/K6 query or hidden calibration was run in qualification.
Native thread readback1,10 project inputs unchanged, v2 manifest valid.
The retained JUnit compatibility warning did not remove its two properties.

Qualification JUnit527874 bytes/logs1768 bytes fit the frozen28MiB/4MiB
plans. The JUnit writer has no in-process scientific-byte abort guard;
this was checked from the actual receipt before main and recorded in
`reports/P66_pre_main_review_receipt.json`. Main's scientific guards are
implemented separately. No source, scope, tolerance or cap changed.

## Unique main execution

The independent source review and pre-main receipt were sealed at clean
**`a5ea2b9c9232834e9d999ec02912c9ef190ced85`** before launch:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P66_exact_finite_check.py --output research/P66_exact_finite_main/run_001/data
```

Installed bounded runner: CPU60s, wall90s, environment/native thread1,
logs4MiB/scientific28MiB, logical256MiB plan, one worker, zero failed retries.
No hard Darwin RSS/affinity limit is claimed. Runner completed/exit0 in
**33.850853s**. Body WALL33.499643875s/CPU8.987306s are supplemental timers,
not a matched optimizer resource budget. All10 project inputs unchanged,
all three declared data files present, v2 manifest validates with `--root .`.
Raw outputs were sealed at **daf728d** before ROOT interpreted them.

All **4902 assertions** passed; these include supplemental input/module-hash
checks and must not be counted as4902 physical samples. Actual population:

| Fixed population | Completed |
|---|---:|
| Exact rational Cayley matrices |32|
| Exact raw CF bosonic probabilities |256|
| Exact raw CF distinguishable probabilities |256|
| Two-target unions (each with B/D values) |128|
| Every balanced cut on the four deterministic graph fixtures |1988|
| Complete one-bright-mode source/target PGF pairs, L2..8 |7|
| Predetermined native bosonic probability references |32|

Matrices use L2/3, M3/h1, disconnected or uniform-cross connected weights,
t=(0,1/4,1,2) and lambda=(0,1/4), in the literal contract order.
Every source/target pair is retained, with **112 exact B zeros and112 exact
D zeros**. No CF probability or full multimode law was computed, and no
postselection denominator was applied. Dark commutation, both inverse
identities, exact unitarity/symmetry and uniform rank-at-most-one cross
blocks passed. Source/target Fock factorials are one in the main; collided
normalization is separately covered by qualification.

The 32 native Naive points use only t1/lambda1/4. All are positive; none
falls in the contract's tiny-positive category. Maximum observed absolute
error **2.439454888092385e-19**, maximum relative error **7.088974891359269e-15**.
Sixteen tolerance tests are relative-dominated and sixteen absolute-dominated.
Agreement uses exactly1e-12+1e-7*max(p_native,float(p_exact)); observed relative
errors are descriptive, not an interval or global relative-accuracy
certificate. No native D points, random counts or complete PNR comparison
is claimed. Actual package versions and loaded-module paths/hashes are
archived and rehashed; OS libraries/lazy unobserved files remain outside
that supplemental provenance.

Scientific output960409 bytes/logs2445 bytes fit the original budget.
All original cache/cold-import warnings are retained. Failure file is null.
ROOT's separate read-only recorded-output inspection verifies the exact
Cartesian coverage, all serialized scalar cuts and both models' union sums;
it does not recompute permanents or claim independent physical sampling.
Receipt: `reports/P66_full_validation/recorded_inspection.json`.

## Regression, interpretation and hashes

All existing tests at rawdaf728d: **1153PASS**, six retained cache warnings,
pytest43.15s/total44.247098458s, environment/native thread1 before/after.
Command/logs: `reports/P66_full_validation/`. The main grid was not rerun
by that regression. Integration must preserve identical executable inputs
and validate current manifests; no automatic wider sweep is implied.

Main manifest SHA256:
`2e9474d6d3642cc36566f5259bb9561baed08d1a0c615c50787bd8651f6157ee`.
Exact/native records SHA256:
`976b7a4d2915857d60fddf96ff55b2390bc9fbdea5432eb9e87fdd30f66540c6`.
Summary SHA256:
`189d8e8a14a4290403073b9f6da162f69d5deba21ceb663b3667b046eefb98c6`.

**Accepted finite assertion:** these fixed exact graph/matrix/PNR/moment
conventions pass, with the stated tolerance-conditional native reference.
**Excluded:** generic graph distribution, complete output law, optimized
B/D comparison, relative-tail/global-TV guarantee, actual hardware runtime,
novelty or a positive optimizer. Optimizer steps0, native random draws0,
QPU calls0. The universal P66/P68/P69 claims rest on their independently
audited proofs; the user's positive discovery goal remains OPEN.
