# P53 exact source/certificate/caller review at a8f93a0

25-Nov-2026. **Verdict: conditional on bounded qualification/execution and the
saved exact certificate verification. PASS STATIC: no blocking source issue
found in the audited implementation.** This does not establish that a continuous
certificate exists or that the run succeeds. No import, test, integer DP, LP,
NPZ read, graph, stochastic sample or hardware call was executed by this reviewer.

Audited exact commit `a8f93a0187e9ea99e3663d66d6c8b2477028e835`:
`research/P53_exact_continuous_phase.py` (414 lines), SHA256
`aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692`;
all179 lines of `tests/test_p53_exact_phase.py` (17 planned cases),
`research/P53_exact_phase_spec.json`, contract MD and both execution/preflight
JSON contracts. ROOT87abe69 and API/derivationef476a4 were previously read in
full; the separate card audit is `research/P53_encoding_card_audit.md`.
The requested additional support-only mock is pending as a TEST-ONLY delta.

## Claim and dependency status

For the specified U8/full8-CF/eta1/uniform-tie-top4 family, success means an
EXACT convex replacement of the28 expected edge crossings for every real
theta over the FIXED71 controls (all35 b4 splits at0/pi2 plus uniform70).
It does not mean equality of the70 full ranked probabilities, tails, adaptive
history, runtime/source/loss costs, arbitrary N, novelty or optimizer advantage.

The source constructs the physical integer wave independently of P52 numerical
outputs, derives all exact probability/rank/edge coefficients and rational
control kernels, transforms the physical curve to Bernstein, asks an unchanged
qualified numerical LP ONLY for supports, then checks rational feasibility and
an independent power-basis identity. No dependency cycles or floating source/
target reconstruction were found. All physical-source leaves are exact internal
constructions; the existence/computational-verification leaves remain pending.

## Source and library arithmetic

- `walsh_factor` implements the four quartics, six pair terms with coefficient
  -2 and the +8 product. `_pair_power` carries the correct bottom-layer signs;
  phases2j,j+k,3 in z reproduce F(A)F_z(B). Each factor asserts90 terms.
- `wave_coefficients` multiplies those factors, fills ALL6435 compositions with
  seven integer entries including zero arrays, bounds phase degree0..6 and
  checks the source assignment L1 bound. Filtering EXACT zero intermediate
  coefficients drops arithmetic only, not physical output states.
- `probability_cosine` uses prod(n_i!) times squared/autocorrelated ordinary
  coefficients, doubles every nonconstant cosine coefficient and retains
  denominator8^8. It checks the full exact normalization polynomial, not just
  a few angles. No division by an output factorial or normalized monomial
  coefficient was substituted. Coefficient signs need not be positive;
  physical nonnegativity follows from the squared-amplitude construction.
- `tie_scaled_rows` uses counts strictly above the fourth threshold and every
  needed tied combination with weight420/binomial multiplicity. It keeps the
  uniform11111111 event and checks exact row mass. `rank_and_crossing` checks
  the exact source rank normalization and every incident sum4 polynomial.
- `_gaussian_columns(0/1)` denotes physical endpoints0/pi2, not P52 cell0/pi4.
  Its row sign and i^(row mod4) phase match U[out,input]. The4-photon ordinary
  coefficient is Gaussian-integer; `gaussian_group_law` multiplies its squared
  modulus by the output factorial and checks numerator sum8^4.
- `classical_library` enumerates all70 groups, then all35 unordered splits per
  endpoint with0 in the first group. The330x330 compact map adds counts, and
  convolution multiplies PROBABILITIES, with no final-output factorial. Every
  full law has6435 entries, nonnegative integer numerators summing8^8. Exact
  zeros may skip multiplication; no favorable support/graph filtering occurs.
  Uniform70 is appended with denominator-compatible entries. All71 vertex
  mass/incident/total identities are checked.

Python integers/Fractions carry the proof arithmetic throughout. The only
integer casts act on internally generated integer counts/coefficients. No
NumPy fixed-width arithmetic, floating rationalization, NPZ or cached P52
law enters these proof constructions.

## Polynomial transformations and exact support verification

`cosine_to_power` uses T0=1,T1=2x-1 and recurrence
T_(h+1)=(4x-2)T_h-T_(h-1), correctly mapping cos(2h theta) for
x=(1+cos2theta)/2. The probability/edge scale is divided exactly ONCE by
KERNEL_DEN. The power-to-Bernstein binomial ratios and direct signed-binomial
Bernstein-to-power expansion have the correct orientations.

Degree12 controls are recomputed exactly from the original power polynomial,
rather than calling `elevate_bernstein` in main. This is equivalent to elevation;
the independent elevation helper and monomial6/12 fixtures check that identity.
It is not a new family, fitted interpolation or extra degree.

`rational_rref_solution` copies the augmented exact system, chooses the first
nonzero row per ascending column, eliminates above/below, checks inconsistent
zero rows, and sets all free variables0. That is a deterministic sufficient
candidate, not a complete nonnegative-feasibility solver. `exactify_support`
uses only the declared >1e-10 support and one distinct all-positive fallback.
It uses29 equations in the declared order and checks every original coordinate,
nonnegativity and sum1 after solving. No rounded floating values become free
variables or target/kernel entries. Failure remains unresolved, not outside-hull.

`verify_polynomial_certificate` rechecks each convex vector and all28 control
equations, then expands the mixtures by DIRECT Bernstein-to-power binomials
and compares every coefficient with the ORIGINAL physical power polynomial,
including degree12 trailing zeros. This is stronger than sampling a grid and
uses a distinct algorithm from the forward Bernstein transform.

## Caller, numerical support and conservative gates

Only `P52_collective_phase_probe.convex_fit` is reused. Its exact qualified
SHA56a71f... is checked before main; its full source is an execution artifact,
along with the transitive P43 import. No floating creation/decoder result is
called. Library/target Fractions are copied into float lists only for the LP.
All evidence/proof equalities are reconstructed from the untouched exact data.

`fit_degree` requires `solver_fit_solved` AND exact rational verification for
EVERY control point, followed by the independent power identity. A timed-out/
failed proposal may retain a valid candidate and even an exact identity, but
the run's certified flag stays false. Degree6 runs7 calls; only if it fails
does degree12 run13, with a20-record hard guard. No alternative solver/cap,
degree, random restart or automatic subdivision was found.

ROOT clarified an important support-only reading during this review: a solved
status0 LP is allowed to propose a support even if its own residual is labelled
NO_VERIFIED_TOLERANCE_MATCH. RREF can change the weights on that support and
produce an exact certificate. For example library[0,1], target1/3 and numerical
proposal[.5,.5] yield exact weights[2/3,1/3]. This is mathematically valid and
matches the card: it is the EXACT certificate, not the old float residual,
that proves membership. Only true solver limit/failure blocks the run gate.
ROOT requested one additional mock of this case before qualification; program
behavior already matches the intended rule. No primary edit was made here.

## Evidence/qualification obligations

The audited17 cases cover independent four/eight-column integer products and
odd-power cancellation, source factorial/normalization/quartic witness, all
ties, endpoint Gaussian controls/library, exact Chebyshev/Bernstein/elevation,
internal-face failure, exact RREF/support fallback/corruption and solved/failed
driver mocks. They are prepared, NOT executed by this audit. The extra mock
must update the test/contract count to18 before the one authorized preflight.

Source/spec/MD/contracts list12 main and13 preflight inputs, including the
unchanged LP provider and transitive P43/metadata/lock. No proof data file from
P52 is an input. CLI freezes the spec by exact dictionary comparison, uses a
fresh output directory, saves source/library/failed attempts/certificate before
the scoped summary, and encodes Fractions as integer numerator/denominator
pairs without pickle. Runtime/memory/output projections are plausible for the
explicit finite bounds but remain projections; actual caps/manifest and before/
after hashes are required. Output overflow is checked after writing and must
remain a preserved failed/inconclusive run, never silently retried.

The cheapest next step is the requested test-only delta plus the already
planned bounded qualification, then independent ROOT/physics review and the
explicit main gate. No numerical source table or certificate currently exists
in this review. No statement of achieved continuous closure is supported yet.

Provenance: adversarial shared-context code review under mathbox:proof-audit
and static computation-audit checks. I authored P52 numerical code and a
related polynomial candidate, not this P53 factorization implementation.
The F/Fock/certificate implications were reconstructed from their definitions;
external/blinded independence is not claimed. No code, tests or data owned by
the implementer were edited. Scope reviewed: all414 source lines, all17
prepared test cases, spec, MD and both JSON contracts at the exact revision.
