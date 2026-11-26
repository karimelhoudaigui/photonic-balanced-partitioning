# P145 float engine — independent prequalification source review

Final STATIC verdict: ACCEPT corrected freeze 7ba7142f below, within the
finite floating-engine scope. The original static blocker remains preserved.

26-Nov-2026. Non-author STATIC review, parent 6c5a63b2f0f70fe18774c7ebe7f0e4b75091ae99.
FULL 183+114=297 lines read at 1f1b0500e0d6e676f8ec24dec278210b64ec8b80:
research/P145_collective_lns_probe.py, SHA256
6af77fadb703120130545779abba5c87618c1331c657e55dab66a95cb75c42bb;
tests/test_p145_collective_lns.py, SHA256
d9bcf827788adde4ed2d5d91785d271026ae095690b54f0dc4746e56bae193cb.
Both hashes independently checked. No import/AST/collection/test, scientific
program, matrix/graph/RNG/native/QPU execution or raw-result reading occurred.

**BLOCKER before qualification: the native test can silently accept NaN.**
ROOT and author notified before any launch; first freeze must stay preserved.
No other material mathematical blocker found in these two files' stated scope.
This does not review the separate ROOT driver/population/resource authority.

## Critical failure and smallest required correction

The Naive test converts reference amplitudes to complex without checking
finite real/imaginary components. It appends prob_error/amp_error then tests
only max(errors)<tolerance. If the first row is finite and a later reference
is NaN, its derived NaN errors can be ignored by max: comparisons of NaN
against the finite running maximum are false. Both final inequalities can
therefore pass despite an invalid native point. json.dumps also permits
nonstandard NaN by default; its presence is not an assertion failure.
This is an adversarial source counterexample, not an observed backend failure.

Correct in a NEW predata revision: preserve the available return/point
diagnostics, then explicitly reject nonfinite amplitude components AND errors.
Serialize failure diagnostics without replacing a numerical invalid value by
a valid zero, and without losing prior/available raw points in finally.
An administrative wrapper may additionally reject skips/nonfinite properties,
but must not describe the old native test itself as safe. No silent retry.

## Reconstructed physical law and mathematical scope

The subset-DP permanent assigns each square matrix row one unused column;
its empty case is1 and it is guarded at size<=3. Each identical-species
occupation uses |per U[n,source]|^2/product_j n_j!, CF input divisor1.
Different orthogonal species convolve NUMBER distributions, with no extra
total-output factorial. This realizes B, all three one-pair profiles and D.

Uniform eta is explicitly INPUT-MODE attenuation, common to all modes/tags.
Tracing independent vacuum input-loss ports gives each surviving source
subset weight eta^l(1-eta)^(K-l); enumerating all subsets supplies its binomial
multiplicity. This is physically correct for this uniform channel, which
commutes with a common passive unitary. It is NOT the general lossy-T
independent-survival prescription refuted by P127.
Canonicalizing restricted tags preserves which survivors interfere.
All occupations N<=3 remain: 1+6+21+56=84, including zero-probability sectors
at eta1. The code checks raw normalization and never rescales by CF/survival.

direct_three_cycle explicitly sums both label three-cycles across all six
assignment paths with the repeated-output factorial. Lower N sectors are
zero in the five-arm difference; full N3 terms acquire eta^3. The direct
law is compared against B-pair12-pair13-pair23+2D at the SAME U, then against
the weighted raw utility. Signed components/near-zero status are retained;
this is FLOAT verification, not an exact sign or interval certificate.
Independent per-arm grid maxima preserve first ties and export no I3-of-maxima.

The mirror takes an already evaluated raw law to 20 CF probabilities plus
the SUM of all collision/loss mass. It queries no graph gain/cut and does
not condition away FAIL. It is a kernel, not a measured sampling-throughput
claim. The underlying permanent-square formula concerns fully identical B;
D/groups need their separate species evaluator, as the implementation does.
For the analytical adaptive mirror, errors must bound kernels at EACH common
history and the transcript is indexed by calls, not matched wall-clock time.

P33 diagnostics use M=2*sum_(row,a<b)q_a*q_b, minimum strictly positive mean
occupancy, the stable expm1/log1p envelope, and the refined branch M<c^2/2.
They neither drop small positive intensities nor declare interval bounds.
The same-U diagnostic is not independently retuned performance; no calibrated
hardware certificate follows from the approximate-unitarity tolerance.

## Coverage and remaining execution gates

Eight prospective tests cover vacuum/HOM factorials, all profiles' uniform
loss sectors, the known tritter 1/3 vs2/9 vs1/9, signed CF I3=4/9 with ZERO
current-cut gain, eta^3 cancellation, own-arm ties, feature exponential,
tiny-positive-density treatment and raw mirror FAIL. None has run here.
The DFT6 native test specifies all56 total-three occupations, comparing B
probabilities and NORMALIZED amplitudes using sqrt(occupation factorial).
It covers B only, not native verification of every distinguishable profile.
Perceval absence deliberately SKIPS: qualification must require eight passes,
zero skips, all56 native points, pinned versions and thread readback1.
ROOT must set startup env/caps and inspect sealed JUnit/log outputs separately.
The library imports no science at module load; NumPy is imported only by a
nonzero-t feature call. Graph boundary fields, strict-local-minimum/block
selection, score accounting and crediting the complete supplied gain table
remain driver obligations. Source alone authorizes no DEV or QPU experiment.
Await the corrected freeze/full delta review before any static acceptance
of native qualification; keep this first failure finding independently dated.

## Separate corrective freeze, before any qualification

Initial 92-line review frozen at c47b0df; its blocker was STATIC, not an
executed test/backend failure. FULL 119 corrective test lines and COMPLETE
diff read at 7ba7142f06534f001c9549608268644bf25b283b, parent 1f1b0500.
Test SHA256 585c8ebb58a07eeed6c479ed89ed85596e17f3c495d0af9b87c697ec686397bb.
Core 183 lines/hash are unchanged, so corrected closure is 302 lines.

The correction imports isfinite, records model/native amplitude components
and both errors, and computes an explicit finite flag for ALL these scalars.
It appends the point BEFORE asserting that flag; nonfinite diagnostics become
repr strings instead of invented numerical values. finally serializes with
allow_nan=False. An additional all-finite condition precedes the final maxima.
Thus a later NaN cannot be ignored and accepted by max; its offending point
and completed prefix remain available for the ordinary finite-guard failure.
No physics formula, tolerances, populations, source/tag definition or native
fixture changed. The original source/test freeze remains in Git.

STATIC ACCEPT of this correction; NO execution or runtime PASS by this reviewer.
Qualification still requires ONE separately authorized bounded run, eight
passes/zero skips, 56 finite native points, exact pins and thread observations.
Interpretation follows raw sealing; no DEV/main/rerun authority is inherited.
