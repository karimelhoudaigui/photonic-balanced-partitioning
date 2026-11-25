# P53 implementation interface and fixed exactification policy

25-Nov-2026. Prospective implementation after ROOT87abe69; no execution yet.
Branch `research/p53-exact-phase`. New source will be
`research/P53_exact_continuous_phase.py`, tests `tests/test_p53_exact_phase.py`.
All proof inputs are constructed from integer Walsh signs and the exact card,
not P52 numerical arrays. Sealed P52 data will NOT be an execution input.

Pure APIs (names fixed here; detailed representation documented in source):

- `wave_coefficients()` : all6435 occupation tuples ->7 INTEGER z coefficients.
- `probability_cosine(wave)` : exact integer numerators, common denominator8^8.
- `tie_scaled_rows(counts)` : subset-mask/weight pairs with denominator420.
- `rank_and_crossing(cosine)` : exact70/28 polynomial coefficients, denominatorD.
- `classical_library()` : all35 splits at each of theta0/pi2 plus uniform,
  exact71-by-28 rational matrix, exact source/convolution normalization checks.
- `cosine_to_power(coefficients)`, `power_to_bernstein(power, degree)` and
  `bernstein_to_power(controls)` : exact Python integer/Fraction transforms.
- `rational_rref_solution(matrix, target)` : deterministic exact elimination.
- `exactify_support(library, target, used_float_weights)` : bounded attempts.
- `verify_polynomial_certificate(power, controls, exact_weights, library)` :
  all equalities/signs/normalization and reconstructed power identities EXACT.

The ONLY floating proof-search dependency is immutable qualified
`P52_collective_phase_probe.convex_fit`, used unchanged to PROPOSE supports.
No P52 floating creation/decoding output is called/read. The main source/closure
will include that module and its seed-helper imports. No solver replacement.

Support exactification is frozen BEFORE main:

1. Use ascending vertex indices with used_weight>1e-10 as primary support.
2. If exactification fails, one fallback support uses ALL used_weight>0.
   This consumes no new LP. Preserve both supports/attempts and failures.
3. Build29 exact equations: normalization row first, then lexicographic28 edges.
   Columns follow ascending support indices. RREF uses the first nonzero row
   at/after the pivot row, columns ascending, with exact zero tests only.
4. If inconsistent, fail. If underdetermined, set all free variables EXACTLY0;
   no rounded floating free values or tolerance solve. Then require every
   weight>=0, sum1 and every original rational equation EXACTLY. Otherwise
   mark support unresolved, not nonmembership. No extra subset search/pivots.

One LP per degree6 control (7 calls), then ONLY if degree6 does not fully
certify, one per degree12 control (13 additional). Maximum20 fits, each1s,
native threads1; no other degree/cap/retry/solver. A failed/timed-out solver
keeps any exact candidate separately but remains inconclusive at the run gate,
as specified by ROOT. A solved LP is still NOT a proof without the verifier.

Save all6435 exact source coefficients/probability polynomials, all70 fixed b4
probability laws and normalized mean kernels, all attempted LP/support/exact
linear checks, all rational control weights and polynomial reconstruction.
Use JSON/GZIP with integer numerators/denominators, not object-array pickle.
Estimated symbolic sizes:<=8100 source products,70*330² bounded integer control
convolution updates,20 systems of at most29x71; full source/control probabilities
are finite constant-size tables. Python big integers/Fractions downstream.

Code/spec/contracts/tests will freeze before any import/test; root, encoding
and physics reviews plus explicit exclusive slot precede qualification/main.
No graph, C*, MC draw, new quantum sample, article edit or hardware operation.
Only a scoped exact continuous edge-MEAN replacement could be certified.
