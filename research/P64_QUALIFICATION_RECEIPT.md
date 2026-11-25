# P64: the corrected synthetic qualification completed

ROOT read the complete source, tests and contracts atbff4a48 and both
pre-data corrections e151573/677348b. Independent static reviewc59baf9
reconstructed the Fock/coherent-suffix argument and checked the correction
from raw Born recursion to the explicitly normalized categorical kernel.
Neither correction followed an execution or observed P64 result.

One qualification ran on CLEAN original677348b through the frozen v2 runner
command:22PASS, pytest0.54s, runner0.793044s, exit0. All8 inputs were unchanged
and all6 declared outputs present. Manifest validation with the current
worktree passed. CPU60/wall90/environment threads1/log32MiB; logical256MiB
is a plan, not a hard Darwin RSS limit. No graph or N18 random draw occurred.
The12-draw reproducibility fixture used N6 only, twice with its fixed seed.

The complete exact F6 source table has462 occupations, denominator46656,
and **68 nonzero weights**. The earlier proof's bound S<=80 remains valid;
this finite table strengthens its compatible-width bound to S^2=4624 for
this source. Actual per-M widths and sampler throughput were not measured.
All exact zeros and weights remain archived; no admissibility filter or
floating threshold was used to count the support.

The normalized rounded candidate kernel agrees with the separate dense
six-mode/Ryser reference at all462 outcomes for each predeclared phase:

| Phase | Maximum absolute probability error | Half-L1 residual |
| --- | ---: | ---: |
| 0 | 1.214306433183765e-16 | 8.682799217032277e-16 |
| pi/6 | 1.1796119636642288e-16 | 8.439175600742995e-16 |
| pi/3 | 1.1796119636642288e-16 | 8.092823828610710e-16 |
| -0.4 | 1.1796119636642288e-16 | 8.300219845745927e-16 |

The four complete candidate/reference tables, norms, phase float/hex values,
JUnit and exact source table were sealed as4ee15ab BEFORE interpretation,
under research/P64_qualification/run_001/. Source SHA256 at execution:
af2b016b9ce5dd71919a8745d21c7e7f363a1588a089f697770a29d5b9353543.

The source and tritter coefficient operations are exact integers. Conditional
amplitudes, phases, masses, normalized CDFs and finite-bit PRNG quantiles
remain approximate. This finite N6 check is not a global N18 TV certificate,
blind replication, full N18 law enumeration, optimizer test, measured complete
sampler cost or asymptotic efficiency proof. The ideal-arithmetic complete
law construction and this finite implementation evidence are separate claims.

The existing full regression plus these tests then passed1020 items; the
actual receipt/logs are in reports/P64_qualification_validation/. No DEV
rescue sweep or optional P63 comparison was run. A separately frozen sparse
N18 permanent cross-check may address physical implementation accuracy at
specified points; no execution is implied here. Positive optimizer OPEN;
paper/main and all protected historical files remain preserved, QPU closed.
