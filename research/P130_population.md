# P130 fixed-few-loss exact qualification — CODE ONLY

2026-11-26. Source/schema text and manual counts only; no import, AST,
evaluation, test, RNG, native call or reference payload read in this task.
Earlier P114 work read P107 mean-coefficient rows; no P130 reference-law or
grid preview was used here. Matrices/population were supplied independently
of these outcomes. Freeze all three files, obtain full non-author plus ROOT
review, then require a DISTINCT ROOT-authorized binding before any execution.

## Fixed population, r0=2

ALL eleven nonnegative P96 catalog inputs are retained. H2 and S3 are excluded
solely because their INPUT matrices have signed entries; no output filter.
P107 uses three prescribed real nonnegative circulants, not an optimized grid.

| Case | m,K | Matrix | Full bins | Top bins | Sectors |
|---|---|---|---:|---:|---:|
| V0 |1,0|empty occupied columns|1|1|1|
| U1 |1,1|[1/2]|2|2|2|
| D3 |3,3|diag(1/4)|20|19|3|
| R3a |1,3|all1/4|4|3|3|
| R3b |1,3|all1/8|4|3|3|
| B4 |2,4|all1/4|15|12|3|
| D4 |4,4|diag(1/4)|70|65|3|
| Z4 |2,4|all0|15|12|3|
| R4 |1,4|all1/4|5|3|3|
| C3 |2,3|[[1/2,0,0],[0,1/2,0]]|10|9|3|
| X4 |1,4|all1/2|5|3|3|
| F0 |4,4|J4/4; P107 x=y=0|70|65|3|
| Fhalf |4,4|circulant first row(9,3,1,3)/16; x=y=1/2|70|65|3|
| F1 |4,4|I4; x=y=1|70|65|3|

Total14 cases,39 sectors,361 full reference bins,327 top-state comparisons,
14 coarseFAIL comparisons. Every zero and collision remains. X4's old
P96 degree-two surrogate is OUTSIDE its low-trace domain and has negative q;
that archived value is retained as legacy_P96_surrogate_q, never confused
with the DIFFERENT positive proposal q_P126. X4 is a valid contraction here.

## Independent exact computation and completion

No producer/helper module is imported. The permanent is an independently
written row/subset DP, size<=4; determinant is exact rational pivoted Gaussian
elimination, size<=6. Four algebra hands are empty, [[1,2],[3,4]], swap and
rank-one2; their literal permanent/determinant pairs are(1,1),(10,-2),(1,-1),(2,0).
They add no physical case. Every matrix/probability calculation uses Fraction.

For each case emit A,G,H and all H principal determinants before contraction
checks. For each sector construct the source subsets, lost complements and
L=per(H_lost), then ALL principal minors of L AND I-L, including empties.
The total1468 rows is4+8+4*36+8*164. The four K3 and eight K4 cases determine
these multiplicities; K0/K1 use their separate smaller domains.
Compute a_S, p=a^TLa/n!, q=sum a_S^2/n!, the rational Rayleigh ratio and
0<=p<=q, preserving signed L entries. All source-Gram binomial moments are
compared against full reference laws:59 moment rows. Sector sums validate
Q=sum per(G_S), binomial inversion and reference P_N, with Q<=binom(K,r).
All fourteen FAIL values include every lower sector, with no renormalization.

Nominal2328 records:1 provenance+4 hands+2 reference completion+361 reference
bins+14 case contexts+59 moments+39 sector contexts+1468 principal minors
+327 state comparisons+39 sector totals+14 FAIL. Final success requires every
counter and all14 cases; no early positive prefix is a pass. Comparison
mismatches are retained through the full population. Other exceptions preserve
the available raw prefix and remain INCONCLUSIVE_FIRST_FAILURE.

## Exact original references and authority

P96 original seal240c7e5518fbcd69d8f22bbe5e8ead3c1bbbc9c1; P107 original
seal99f2d98d93f13c7fc088218bfb06ff39af4c40e9. Each has six files:manifest.json,
stdout.txt,stderr.txt,data/records.jsonl,data/summary.json,data/failure.json,
under its existing research/P96_column_loss_main/run_001 or
research/P107_symbolic_filter_main/run_001. ROOT authenticated exact Git-blob
bytes; actual descriptors enter a separate binding, with no guessed hashes.
Manifest/stdout/stderr are only hashed. P96 parsing checks ALL167 raw-record
metadata and13 source/audit cases, then selects151 bins from the fixed11.
P107 checks9612 lines/25 grid-point metadata and reads ONLY the three fixed
grid B_probabilities lists,210 bins; no producer reevaluation or native replay.
Both original final states must be complete. Inputs/binding are rehashed
after computation. Unknown/native payload kinds and sign certificates are
not used as a qualification oracle.

Python3.11.15 -B, six thread settings1, one worker, CPU60/wall90, science4MiB,
combined final results64KiB, runner logs4MiB, zero retries/native/RNG/FPRAS.
Fresh exclusive data child research/P130_few_loss_main/run_001/data. ROOT
enforces fresh ENTIRE parent, wall/log bounds, manifest v2 closure, original
seals and raw sealing before interpretation. Missing finals cannot pass.
This is finite exact identity qualification, not execution of the P126
approximate sampler, FPRAS software, measured speed, optimizer or QPU validation.
