# P53b frozen source: physics / rational-dual / caller review

Verdict: **STATIC PASS for the declared synthetic qualification**, with no
load-bearing normalization, dual-sign or caller blocker found. No physical
x=1/4 target was read/evaluated, no source imported, and no test, LP, sample or
executable witness computation was run. Membership/separation remain unknown
to this review. The planned main still requires its separate authorization.

Exact audited commit `bb0ba2d6d08c31d096b79fac58886f113d24f8f3`; files read
completely from immutable git objects:

| File | SHA256 |
|---|---|
| research/P53b_fixed_point_discriminator.py | 66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908 |
| tests/test_p53b_fixed_point.py | ff5ff9b1723644e6f7838178f10321e5184fb74aaa540faa6b5521a2ddcf9c90 |
| research/P53b_fixed_point_contract.md | 2f8120b8dc97edcc2d700e7200b0917e8cd5369fe206c375d09cad4554855053 |
| research/P53b_fixed_point_execution_contract.json | a7483fe07e1e7b93d793bad4b3d27fda19cdd182270046d807ccf6591ba971f1 |
| research/P53b_fixed_point_preflight_contract.json | ae227fc5bbaf88c4fc10a393fdd04df70a4bd4071a3e0d6b97d6565535ca98c1 |

I also read the complete spec. My pre-source card review was frozen5faebcd.
I did not write this implementation/tests. I had previously audited the exact
P53 physical source and P52 numerical engine, within the same team; those
dependencies are reused with disclosure, not promoted into a new blind or
external source verification. No primary raw target coordinates were inspected
to reach this static verdict.

## Physics/data normalization

The caller pins P53 exact source/library gzip bytes before decoding, and pins
the exact provider aedbc561... and LP provider56a71f04.... Those are the same
physical-source/exactification and qualified LP conventions reviewed earlier.
The source mean powers are already rational normalized coordinates; the
loader does **not** divide them again by420*8^8. Library integer numerators
are divided by that denominator once. No float/NaN numeric JSON is admitted,
and rational pairs require Python integers, positive denominator and gcd1.

All28 polynomials must have seven coefficients. At degree0 their total is16
and every incident-row sum4; at higher degrees both totals are0. Library
schema requires all71 labels, all35 complementary splits at each fixed
endpoint and uniform70; all28 entries are bounded exact integer numerators.
Each library vector must have total16, incident rows4, with uniform vertex
exactly4/7 in every coordinate. These are correct balanced4-in8 invariants.
Both target and library use lexicographic unordered edge labels.

The sole target is exact Horner evaluation at Fraction1/4 from the power
polynomial, not a Bernstein control point or a rounded physical kernel.
`fixed_target` rejects floats through exact_q and verifies bounds0..1 and
balanced totals. No x parameter/search appears in this interface, and the
spec validator fixes the point, library, calls, witness rule and resource
limits. It applies to lossless full8-CF with uniform top4 ties only, retaining
the original physical decoder/source normalization rather than introducing
collision filtering.

## LP signs and exact proof boundary

The dual variables are(wplus,wminus,t), with objective(b,-b,-1), constraints
(-V,V,1)<=0 and(sum56,0)<=1, nonnegative split variables and free t. Therefore
it minimizes w·b-t subject to t<=w·v_c and||w||1<=1, the intended separation
orientation for a smaller optical mean cost. All71 vertices enter the LP.

The signed **floating subtraction** wplus-wminus is frozen before conversion;
each finite coordinate is mapped with Fraction.from_float, not decimal
rounding/limit_denominator. Any overflowed/nonfinite signed difference is
unavailable. The exact L1 is scaled only if greater1; a zero proposal is safe
and yields no strict gap. The verifier recomputes min_c w·v_c and every
w·v_c-w·b over Fractions, demanding a positive exact minimum. LP t/fun and
residual tolerances never become proof values.

Primal supports reuse the frozen exactification: nonnegative rational weights,
sum1 and every equation must verify, regardless of whether float weights were
initially a tolerance match. A failed support or free-zero RREF is explicitly
inconclusive, not a nonmembership result. Both provider calls occur once even
if the first arm succeeds; no alternative x/support optimizer is introduced.

Solver status0 AND successTrue gates the winning arm separately from exact
witness validity. Timeouts/failures retain any available exact candidate but
do not promote it into an accepted solved arm. Both exact witnesses cause
inconsistency regardless of solver status; main writes evidence and exits
with failure, accepting neither. A strict dual and primal membership at the
same exact inputs would be algebraically contradictory, so this is the
correct defensive priority.

## Nonnegative graph and interpretation

The graph converter independently requires exact total16 for the target and
every control. Adding max(0,-minw) to all28 edges shifts **both** means by the
same16c. It verifies all positive margins, preservation of the exact minimum
gap, and the normalized gap after dividing by the positive total weight.
Strict separation forbids an all-zero shifted graph. The graph edge ordering
is explicitly exported. It is a rational nonnegative graph witness for the
fixed ENDPOINT71 closure, not C*, a prepared optimal partition or a benchmark.

An emitted graph candidate remains labelled posthoc even if a solver gate
is inconclusive, and no graph is silently accepted in a contradictory case.
The target/source/classical library here cannot establish a claim against
continuously reoptimized b4, phase/sphere/Gauss, arbitrary feasible classical
search, tails, full laws, generic sizes, loss or hardware. All70 feasible cuts
remain trivially enumerable at N8. A mean-only strict witness is neither a
held-out optimizer result nor the user's achieved positive goal.

## Caller/resources and fixtures

Imports/JSON parsing are before the internal point-and-LP timer, but the named
summary fields explicitly measure only point/LP work; the external runner
caps the whole child. It must pin the13 main inputs (14 for qualification)
and record hashes/actual outcome. Providers are hash-checked; gzip decoding
is bounded16MiB each (trusted sealed inputs, not arbitrary generated arrays).
Source projection distinguishes scientific data64MiB from package RSS; it
does not assert hard Darwin address-space/affinity enforcement. Each native
LP uses the known single-thread readback/options and1s time limit, with the
frozen highs-ds method/seed/tolerances. Only the established SciPy-forwarding
warning is accepted. No retry/cap/point/solver choice follows an outcome.

Scientific output is exclusive canonical rational gzip JSON plus summary;
both uncompressed witness and total scientific bytes are bounded4MiB. Partial
failure must remain a failure rather than an unproduced successful result.
The exact graph/source bits are not reconstructed from numerical output.

All20 fixtures were read, not executed: exact schema/types/hashes/inflation;
synthetic Horner and balanced-coordinate checks; binary-vs-decimal duals,
rescaling/strict/all-vertex/shape cases; graph shift and normalized gap; mocked
LP signs/flags/forwarding/native mismatch; status/timeouts/retained candidates;
changed exact primal weights; contradiction override; fixed spec/exclusive
gzip and nonfinite proposals. They use synthetic kernels and mocked optimizers,
not the physical point or real native solves. A targeted PASS is still an
execution obligation, and any emitted exact witness will require a separate
post-run verification. No primary source, test, raw, proof or paper was changed.
