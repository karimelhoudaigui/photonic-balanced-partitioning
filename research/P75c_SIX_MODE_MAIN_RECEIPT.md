# P75c: sole six-mode log-objective main receipt

Run dated 25-Nov-2026. **NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH.** The sole
authorized main recorded 7,145 raw probability evaluations. Its global best
was only the supplied analytic three-pair baseline, not a newly discovered
point. This bounded local search proves neither the six-mode Gaussian cap
nor an optimization advantage. All P75b evidence and P75c source/cards remain
unchanged; no new search or retuning is authorized by this receipt.

## Authorization, producer and raw-first archive

The source/cards were frozen at `51deeed2ed1a5dad8f46652be7269fa40e1d1af9`.
ROOT reported its full read of all 765 new lines, the B-to-C diff and the
199-line independent review at `e490d2261fdfc3ee7957bda4169c4b438d322c6d`
(review SHA256 `327bc5d360c2c2cb31c6b94e78737b3a3e3b81566264d9207b0c59e23786d381`).
The eleven-item tiny qualification was separately authorized, executed once
and archived at `f343302e92a4e7be273d09dc8219a73b858e9ac0`. Its receipt is
`research/P75c_TINY_QUALIFICATION_RECEIPT.md`, commit
`f02e4713b7cba68bce67e449dcf1a1a518665b1f`, SHA256
`bd9fb4f2a9548ee5158e66d65f532049512b53f935e9a13fb94df0c3b947df35`.

ROOT independently read that entire receipt, the full qualification manifest,
all eleven JUnit items/property and checked matching-tree v2 validity before
SEPARATELY authorizing ONE main. This records decision provenance; tests or
review approval do not prove the mathematical conjecture.

The main producer was clean commit
`f02e4713b7cba68bce67e449dcf1a1a518665b1f`. All twelve execution-artifact
hashes were reconfirmed immediately before the only launch. There was no
canary, preceding new import, scientific case, full suite or RNG draw. The
numerical slot was exclusive to this main.

All seven files of `research/P75c_gaussian_cf_search/run_001/` were committed
BEFORE reading or interpreting the raw manifest, summary or evaluation rows:

    f082dd60f187676393be88d66e3f93d56ddee79d

The raw commit was sent to ROOT first. No source modification, second main,
retry, cap increase, fresh seed, precision increase or additional witness
attempt followed. The installed v2 validator returned valid evidence with
status completed against the matching producer tree. All twelve input hashes
are unchanged before/after; all four declared scientific results exist and
are regular. The child exit was 0, with no missing/invalid result.

## Recorded command and actual search population

The exact child argv matched the frozen execution JSON:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P75c_gaussian_cf_six.py --output research/P75c_gaussian_cf_search/run_001/data

The installed bounded runner used the twelve declared inputs, four declared
results, CPU 30 seconds, wall 60 seconds, thread environment 1 and log cap
4 MiB. The objective was `-log(max(true_q,1e-300))`; every row separately
retains its TRUE raw q. Source/threshold/model/certificate rules remained
exactly those qualified before launch.

There are 7,145 evaluation rows and six start-termination rows, with no
evaluation-failure row. The observed count is

    1 baseline + 1,144 + 1,200 + 1,200 + 1,200 + 1,200 + 1,200 = 7,145,

below the predeclared maximum 7,201. The complete fixed population is:

| Source / seed | Evaluations | Maximum recorded true q | Termination |
| --- | ---: | ---: | --- |
| analytic three-pair baseline | 1 | 0.015625000000000003 | baseline check |
| 7511001 | 1,144 | 0.007980239745852524 | SciPy returned status 0 |
| 7511002 | 1,200 | 0.007979202431270293 | hard evaluation budget |
| 7511003 | 1,200 | 0.010493384705812264 | hard evaluation budget |
| 7511004 | 1,200 | 0.00798017969369894 | hard evaluation budget |
| 7511005 | 1,200 | 0.010402460032593014 | hard evaluation budget |
| 7511006 | 1,200 | 0.007980239407246669 | hard evaluation budget |

The baseline is known analytically as 1/64. Its floating residual above that
value is far below the registered 1e-8 trigger margin and is not a violation.
The best point arising from an optimizer start was seed 7511003, below that
baseline. No row crossed `1/64+1e-8`; certificate_attempts is 0. Both
certificate.json and failure.json contain the literal JSON null. No exact
witness calculation or certification was needed or performed.

Only seed 7511001 actually returned a SciPy result: status 0, success true,
24 iterations, nfev 1,144, message
`CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`. The remaining five
statuses mean evaluation budget exhausted, not convergence. Their iteration
counts were not recorded and must not be invented. A global-coverage or
convergence theorem does not follow from the one local return either.

## Actual-q lookup and recorded physical diagnostics

The returned seed 7511001 result reports:

- final_optimizer_loss = 4.830786824631888;
- final_probability = 0.007980239745851797;
- final_probability_source = LOOKUP_ACTUAL_EVALUATION;
- final_global_evaluation = 1102; final_probability_floor_applied = false.

Inspection of the already recorded row 1102 confirmed exact equality of its
43 parameters, true q, optimizer loss and floor flag with those final fields.
The probability was not obtained from `-result.fun`, an inverse log or an
extra objective evaluation. The last finite-gradient row has a slightly
different q and is not misreported as the returned point.

Streaming metadata inspection of all 7,145 saved evaluations checked
contiguous global/local indices, 43 parameters, two 6x6 matrix parts,
registered parameter bounds, finite recorded q/loss, five stored physical
flags true, floor-flag consistency with recorded q and no threshold crossing.
All six saved termination records exactly match the summary records. This
inspection did not independently recompute Z, hafnians, eigenvalues,
probabilities, optimizer steps or RNG draws.

Maximum stored singular value was 0.9950547536867309; minimum stored Q
eigenvalue was 0.009866037165439318. These are extrema of recorded diagnostics,
not independent recalculations. Seed 7511006 has 43 rows marked at the
probability floor and minimum recorded q 0; all other groups have no floor
row. This observation does not assert that every floor row equals exactly
zero. Present zero/floor values remain explicit data, not missing outcomes.

The loss floor reached 690.7755278982137 in that seed. The scalar floor can
remove local information, so its presence is retained as a limitation. No
unregistered rescaling or recovery was attempted after viewing it.

## Resource and provenance observations

Runner start: 2026-11-25T22:56:27.450984UTC. Runner elapsed: 2.99137 seconds.
The source separately recorded body wall 2.7859197910001967 seconds and body
CPU 2.529067 seconds. These are distinct scopes, not interchangeable timings.
All stayed below the fixed wall/CPU caps. The source reports the pinned
Python 3.11.15, NumPy 2.4.6 and SciPy 1.17.1, with all five conventional
thread variables recorded as "1". The actual resolved interpreter and
interpreter/NumPy/SciPy init-file hashes remain in the immutable summary.
Actual native thread activity and all BLAS/OS library bytes were not audited.

Observed output sizes are:

| Artifact | Bytes |
| --- | ---: |
| evaluations.jsonl | 22,690,428 |
| summary.json | 3,414 |
| certificate.json | 5 |
| failure.json | 5 |
| stdout.txt / stderr.txt | 0 / 0 |
| manifest.json | 10,434 |

Scientific results total 22,693,852 bytes, below 32 MiB; evaluation records
are below 31 MiB. Logs are below 4 MiB and results plus logs below 36 MiB.
The complete archive including its runner-owned manifest is 22,704,286 bytes.
Logical 128 MiB was a plan; no hard RSS/address-space or affinity limit was
requested or inferred. CPU enforcement is per process; conventional thread
limits are not proof that a native library used only one thread.

Manifest SHA256:
`dec521c8e51c567d3cf7372cf4b7a87a209816ab71c1e0e12b59e36518f26c4e`.
Records SHA256:
`2bb135922c0c51c3a1f6080d24f9d24d5490d9f9ee4788dbdf6dd14c6e82171c`.
Summary SHA256:
`a4a228f8737e26e01b713f7ab393730c66ac611ce6e569ba6f66cc7d842237ce`.
Both null JSON files have SHA256
`38e0b9de817f645c4bec37c0d4a3e58baecccb040f5718dc069a72c7385a0bed`.

## Scope of the outcome

C addresses a specific numerical scaling weakness observed in B but uses
fresh seeds and a larger prospective budget. Their different trajectories
cannot be attributed solely to the objective transformation. No systematic
coverage of all complex symmetric contractions has been established; even
a successful local return cannot support such coverage. The conjecture
remains analytically unresolved by these data. No counterexample in this
registered search is not strong numerical evidence for a universal theorem.

This is not graph optimizer training or a balanced-partitioning benchmark.
It supplies no advantage against classical search/distinguishable controls,
no held-out replication, no QPU readiness and no permission to revise the
manuscript. No Perceval/native_api/QPU call occurred. P75b's original limited
result remains intact. The numerical slot is FREE; further research requires
a fresh justified question and ROOT's separate decision, not an automatic
continuation or repeated search.
