# P53c independent complete four-photon permanent replication

ROOT requested this after the primary candidate was sealed61a4683. Outcome
and claimed minimum were disclosed before implementation, so this is posthoc,
not blind/held-out. It independently reconstructs every NEW control probability
and the fixed old functional, not the eight-photon source or ugly new LP dual.
No code/import/selftest/control/LP has run for this implementation checkpoint.

Inputs are only the original P53b certificate (bd987439...; target/old71/fixed
weights already checked independently atcc4c73b) and P53c certificate
`408140f0a1a3865e374256d2a1e797961adcf6742cd8b1d234c2c7b4b2cbc065`.
The latter was copied byte-identically from61a4683 with git archive, without
decompression/evaluation. Both old and new raw remain immutable. Canonical
Fraction proof fields are read without converting physical values from float.
No production helper, NumPy, SciPy, Perceval or optimizer is imported.

## Independent probability algorithm and complete population

Use basis(1,i*sqrt3) with unnormalized matrix-entry numerators over2. The four
right-block phases have pairs(2,0),(1,1),(-1,1),(-2,0), with an independent
Walsh bit-parity sign and lower-right block sign. Matrix entries represent
the original U8(theta=pi/3) multiplied bysqrt8. Integer-pair multiplication is
(a,b)*(c,d)=(ac-3bd,ad+bc), different from production's xi-basis rule.
Exact numerator Gram32I checks unitary normalization before probabilities.

For EVERY one of70 input groups and EVERY one of330 output multisets, compute
the4x4 permanent by all24 LABELLED source permutations, retaining repeated
output rows. If its numerator pair is(A,B), the unnormalized permanent equals
(A+B*i*sqrt3)/16. The four-photon probability numerator for denominator8^4 is

    (A²+3B²) / (256 * prod n!).

Require exact integer division, positivity and mass4096. This is the PERMANENT
formula dividing output factorial, distinct from the creation-coefficient
formula multiplying it. Optional coefficient comparison uses
per_num=(8 f(2a+b),8 f b), f=prod n!, for archived C=a+b*xi; the archived values
never supply the independent probabilities. Synthetic guards at the known
Walsh subblock require bunch numerator24,2+2 numerator16 and CF numerator64.

Enumerate counts by combinations-with-replacement of output slots, separately
from production compositions. Align data by count tuples. Convolve independent
group probabilities for ALL35 complementary splits; map total occupations by
base9 integer encoding (no digit carry, since each total occupation<=8),
not production's tuple-add map. Keep ALL6435 outputs, exact zeros and all35
labels, checking mass8^8 and equality with every archived occupation value.

Rebuild the TOP4 uniform-tie functional independently by enumerating all70
balanced subsets for each occupation and retaining those with MAXIMUM photon
sum (not P55's neutrality decoder). For delta=X04-X15, define integer
alpha_n=420*sum_(maximizers)delta/number_of_maximizers. Then the fixed
w=(X04-X15)/2 mean of a law with integer numerators p_n/8^8 is
sum p_n*alpha_n/(840*8^8). Guards include all-one alpha0 and the directed
0-doubled/4-empty pattern alpha168. This avoids production tie/rank helpers.

Read and verify the original saved w and normalized graph unchanged. Compare
all35 independently computed functional means against raw crossing numerators,
expanded mean vectors and saved fixed-graph diagnostics. Compute every margin,
not a selected grouping. Old71 strict margins are rechecked from the trusted
old certificate. Strictness on all106 proves this finite mean separation via
the OLD w, regardless of a new LP; no new binary LP witness is checked or used.
If strictness fails, report that negative outcome rather than assert a proof.

## Freeze, resources, outputs and interpretation

The complete source/card/execution JSON and two immutable certificates form
five runner inputs. ROOT must review the freeze and grant the single exclusive
run before imports/guards/reconstruction. CPU20/wall30/threadenv1/log4MiB,
scientific output4MiB; planned scientific tables<64MiB, no hard Darwin memory
claim. All data are Python integers/Fractions; no native solver, random draw,
graph optimization, calibration or hardware. Never retry/change phase/group/
cap after an error. There are23100 permanent evaluations /554400 terms, plus
35*330² bounded integer convolution pairs and6435*70 finite tie candidates.

Archive independent matrix numerators,70 complete group laws/permanents,
35 complete convolution laws, both count indexings, all tie-functional weights,
35 functional means/margins and a compact report. No exponentially larger
eight-photon direct permanent sweep is proposed. Check all output/input hashes
and a v2 manifest after execution, preserve failure/partial logs and release
the slot. The three toy permanent calls add72 terms to the554400 production
terms; all count toward the same CPU/wall cap. The result concerns one N8
ideal same-angle mean hull only; it is
not a global classical impossibility/optimization/tail/loss/resource/novelty
or hardware result. P55 remains a separate prospective pilot.
