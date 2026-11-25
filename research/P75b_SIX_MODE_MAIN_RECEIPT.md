# P75b: sole six-mode search receipt and its material limitations

25-Nov-2026. **Observed status: NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH.**
This means no threshold violation among the1,033 logged numerical evaluations,
including one analytic baseline. It is NOT proof or strong numerical support
for the universal six-mode Gaussian cap, a new optimizing point, or a positive
balanced-partitioning/QPU result. The weak absolute-gradient stopping behavior
of three starts is a material limit, documented below without repair/rerun.

## Authorization, source and raw-first sealing

ROOT separately authorized exactly ONE main after its full source/contracts,
independent source-review and tiny-qualification review. The producer was
clean `00256fc2e4a69b9d80065af3dd5734518ac4d5ef`. All ten inputs and the five
source/card hashes were reconfirmed before launch; no new mathematical note
was read first and no import, canary, collection or extra test was run.

The command exactly matched the frozen main JSON:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P75b_gaussian_cf_six.py --output research/P75b_gaussian_cf_search/run_001/data

The installed bounded runner used the matching worktree root/main JSON,
exactly ten --input entries and all four declared result paths. Limits were
wall60s,CPU30s,max-threads1 and combined logs4MiB; no hard address-space or
CPU-affinity cap was requested. The single numerical slot was exclusive.

The ENTIRE raw directory, including manifest/logs/four data files, was sealed
BEFORE scientific interpretation and its commit was sent to ROOT first:

    4a5254ce3e19f1681f4c1e6fd852fcc979d5d409

No file in that raw directory was subsequently edited. The v2 validator
returned valid evidence/runcompleted against the matching producer tree.
Every one of the ten before/after input hashes agrees. All four declared
results exist and are regular; no missing/invalid result was reported.
The source remains SHA256
`b86f2c69d26a3cc53d914122fac2a04e005f61141e8a4f1de8f919fdc69c09bb`;
fixtures remain19e14762, helperfb3cf959, P73 model97392ff3, MD4e47b8fa and
JSON contracts d6ba600b/a9992db6. No card or program was modified.

## Actual coverage and optimizer reports

Raw lines comprise1,033 evaluation records and six start-termination records.
There are no evaluation-failure rows. The evaluation indices are contiguous
1 through1,033, every parameter vector has43 coordinates and both stored
real/imaginary matrices are6x6. All recorded physical flags are true.
These are checks of recorded fields, not independently recomputed probabilities.

| Start | Evaluations | Registered termination | Maximum observed q |
|---|---:|---|---:|
| Analytic three-pair baseline | 1 | Fixed single evaluation | 0.015625000000000003 |
| 7510001 | 300 | EVALUATION_BUDGET_EXHAUSTED | 0.00012950802252583623 |
| 7510002 | 44 | SciPy status0, iterations0 | 1.4399369388535882e-7 |
| 7510003 | 300 | EVALUATION_BUDGET_EXHAUSTED | 0.000050086982910386906 |
| 7510004 | 300 | EVALUATION_BUDGET_EXHAUSTED | 0.0011218979143342385 |
| 7510005 | 44 | SciPy status0, iterations0 | 3.9153009358259266e-13 |
| 7510006 | 44 | SciPy status0, iterations0 | 1.0504356478122841e-10 |

The counts reconstruct exactly1+300+44+300+300+44+44=1,033, below the frozen
maximum1,801. No start or seed was replaced. Expected hard budget stops are
not failures or retries; the three early returns are also retained exactly.
No unusual optimizer termination, unexpected exception or resource interruption
was reported. certificate.json and failure.json both contain JSON null.

The GLOBAL BEST is the predeclared analytic three-disjoint-pair baseline,
not a newly found point. Its tiny floating excess above exact1/64 is far
below the frozen1e-8 trigger margin and is not a counterexample. The largest
recorded optimizer value is0.0011218979143342385 from seed7510004, also below
the baseline. No float trigger occurred; exact certificate attempts=0.
No six-mode rational witness or exact6x6 physical certification was produced.

## Why this no-hit result is weak

Seeds7510002,7510005,7510006 returned after44 finite-difference evaluations
with ZERO L-BFGS-B iterations, reporting
`CONVERGENCE: NORM OF PROJECTED GRADIENT <= PGTOL`.
Their initial radii were respectively0.19100601398572903,
0.022019773000368947 and0.0894096517367916. Their tiny raw probabilities
and the frozen absolute gtol1e-5 allow early local stopping near vacuum.
The recorded message is an optimizer local criterion, not a global optimum
certificate or an independently verified gradient/error bound.

The other three seeds each used the full300-evaluation allowance. In43
parameters this is a very small local-search budget, and no global coverage
or broad attraction-basin exploration is established. The analytic baseline
was deliberately not an optimizer seed. The finite source family also has
radius restricted to[0,3]. Local convergence/no-hit must not be promoted
into universal support for q<=1/64.

No objective rescaling, tolerance change, altered seed, extra evaluation,
rounding, larger budget or rerun was performed in response to these data.
A future scaling study would be a distinct prospective experiment with its
own authorization/freeze and would preserve these failed/limited starts.

## Recorded floating diagnostics and exact-certificate status

The largest recorded optical singular value is0.9930719897147728 and the
smallest recorded Q eigenvalue is0.013808023243941578. Every saved evaluation
passes its stored symmetry, strict-contraction, Q-positivity/Hermitian-residual
and determinant checks. These are the predeclared binary64 diagnostics, not
interval certification or independent recalculation of every q.

The source's exact rational branch was never entered: no value exceeded
1/64+1e-8. There was no rounding attempt, precision adjustment or failed
certificate to suppress. The tiny qualification's exact two-mode LDL checks
remain separate from this numerical six-mode search. No implication about
P73's narrower real/nonnegative loopless class follows from a no-hit search
of generic complex matrices.

## Actual runtime, environment and raw bytes

Runner start:2026-11-25T22:37:11.373704UTC. Its elapsed time is1.227817s,
exit0/statuscompleted. Supplemental child-body wall time is1.0402827500001877s
and body CPU time0.79351s. These different timing boundaries are retained;
they are not a hardware-time or graph-optimizer cost comparison.

Python3.11.15, NumPy2.4.6 and SciPy1.17.1 were observed. The resolved Python
binary/hash and NumPy/SciPy init-file hashes are in summary.json. OMP,
OPENBLAS,MKL,VECLIB and NUMEXPR thread variables are all recorded as1. These
settings do not measure actual native thread activity or authenticate every
BLAS/OS library. Logical128MiB is a plan; RSS/affinity were not enforced.

| Raw file | Bytes |
|---|---:|
| data/evaluations.jsonl | 3,272,101 |
| data/summary.json | 5,228 |
| data/certificate.json | 5 |
| data/failure.json | 5 |
| stdout.txt | 0 |
| stderr.txt | 0 |
| manifest.json, runner-owned | 9,738 |

Child scientific files total3,277,339bytes, below8MiB; records are below7MiB,
logs below4MiB and combined child/log bytes below12MiB. The runner-owned
manifest is retained separately. No warning/error log was dropped.

SHA256 identifiers:

- manifest: `6d568ba54a35c3be2392c7943a8549982fd1bfa637f3f6785476bf45a95434a8`;
- evaluations: `7b6dfa4ae4bec57bf68ca3c4751a708b5e34f4ed3a3ce16687fccd6b8248e781`;
- summary: `237f0602bade4c27e95ee5d95e0b59b7097f2c061eaa78598896ff009eade735`.

## Scope and handoff

After raw sealing, only matching-tree manifest validation and stdlib parsing
of the existing JSON/JSONL were used. This computed record counts, shapes,
observed extrema and bytes; it did not invoke any new objective, matrix
probability, RNG, solver or independent native calculation. No full test
suite was run and no extra qualification followed. Perceval_calls=0,
QPU_calls=0 and optimizer_advantage_claimed=false in the source summary.

The numerical slot is FREE. ROOT has separately reported reading the main
summary and validating its matching v2 record, and highlighted the same
zero-iteration limitation. Further full tests or a differently scaled search
remain separate decisions. This receipt closes only the registered P75b
attempt, with its negative/limited evidence preserved. The six-mode universal
bound and the user's positive optimization objective remain OPEN.
