# P53b fixed-point exact discriminator — implementation freeze

ROOT approved proposal commits a0a6881 and 1dbb3f9 for implementation only.
The single point x=1/4 (theta=pi/3) was chosen before evaluating it: it is a
simple rational point absent from P52's x=0,1/2,1 cells. P53's inconclusive
global Bernstein result remains unchanged. No new point has been evaluated,
native LP called, or test/import run at this source freeze.

Inputs are P53's sealed exact_source.json.gz (SHA256
2a593abba088327ccb8b54f5f14bab6f8edcf5fc42128de6c31f394bf454d7a0) and
exact_library.json.gz (SHA256
cb210de13928e365b8983c2a17b882623a346975b522293fd549b6980871963b).
Their hashes are checked BEFORE decoding. Canonical integer/Fraction pairs,
all 28 degree-six polynomials, exact incident identities, complete endpoint
labels, all 71 vertices and uniform vertex are checked. Neither target nor
library is ever rationalized from a float. The sole point is evaluated by
exact Horner arithmetic only in the separately authorized main.

The immutable P53 source supplies exactify_support, exact_q and serialization;
its SHA256 is aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692.
P52's immutable provider SHA256 is
56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242.
One primal call uses its existing convex_fit and support-only exactification:
support >1e-10 then all positive if distinct, 29 exact equations, first
nonzero pivots, free variables zero, nonnegativity and all equations exact.
A solved numerical NO_MATCH is allowed to propose a useful support.

Exactly one dual call follows, even if the primal succeeds. Variables are
wplus,wminus>=0 and free t; objective min w.b-t, inequalities t<=w.v_c for all
71 vertices, sum(wplus+wminus)<=1. The signed FLOAT subtraction wplus-wminus
is converted coordinatewise using Fraction.from_float; this is the only
frozen rationalization rule. If its exact L1 norm exceeds 1, divide by that
exact norm. Recompute t=min_c(w.v_c) and ALL 71 strict gaps w.v_c-w.b over Q.
Only a strictly positive rational minimum gap certifies separation.

HiGHS method highs-ds/options and native readback match qualified P52:
time_limit1s, threads1, parallelFalse/off, seed5201001, presolveTrue,
dual/primal feasibility tolerance1e-9. Only the exact expected public
forwarding warning is allowed. At most TWO native solves, with no retry,
alternative point, solver, degree, tolerance or raised cap. Main acceptance
requires solver status0 AND successTrue AND an exact witness. Timeout/failure
keeps a valid candidate separately but remains inconclusive. Exact primal
and dual simultaneously verified is an inconsistency: write evidence and
exit with failure, accepting neither.

Any dual witness yields a POSTHOC nonnegative graph by adding
c=max(0,-min w) to every edge. All target/library edge totals equal 16, so
every mean shifts by 16c and the gap is identical. Divide by the strictly
positive sum of shifted weights and verify the normalized gap again exactly.
This witness concerns ONLY the fixed ENDPOINT71 mean closure. It is neither
a DEV/held-out graph nor a comparison to continuously reoptimized b4,
efficient feasible search, full output laws, tails or optimization. There is
no C*, known partition, training, physical/MC sample, QPU or manuscript work.

Scientific outputs: certificate.json.gz (exact target, library, labels,
proposals and witnesses) plus summary.json. Gzip JSON contains canonical
Fraction pairs, no pickle. Bound inflated inputs at 16MiB each after hash
checks; actual sealed files total 2,664,500 expanded bytes. Output uncompressed
certificate and total scientific files are capped at 4MiB; summary <=64KiB.
Plan scientific arrays/data <64MiB, excluding Python/native-library baseline;
there is no claimed hard Darwin memory/affinity enforcement. Runner caps:
CPU20s/wall30s/native thread1/log4MiB. No outcome exists at this freeze.

Twenty qualification tests use only synthetic exact kernels and mock LPs:
canonical rationals/schema/hash/inflation; fixed-Horner toy identities;
binary versus decimal witness, rescaling, all-vertex/strict/shape checks;
exact shifted graph gap; known LP signs/flags/readback; invalid warnings and
timeout/failure gates; changed exact primal weights despite float NO_MATCH;
strict dual and retained inconclusive candidates; contradictory witnesses;
frozen spec, exclusive bounded gzip, missing/nonfinite proposals. Qualification
does NOT open the physical x=1/4 target or call native solvers. Root/physics
static review precedes an explicit exclusive qualification slot; a second
explicit main gate is required. Preserve every failure without automatic retry.
