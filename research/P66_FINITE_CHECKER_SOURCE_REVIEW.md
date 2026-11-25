# P66 finite checker: independent exact-source static review

25-Nov-2026. **Primary verdict: PASS conditional (audited, not executed).**
No material static blocker was found in the exact source, fixtures and
contracts below. The finite assertion is implemented consistently with the
stated mathematics. This verdict requires a separately verified successful
qualification and one complete bounded main run before any finite-result
claim. It is neither a run receipt nor evidence that those processes passed.

## 1. Exact target and independence

Frozen author revision: `88a0573907b503fe2b624d13920430353d27e779`, worktree
`.local/p66-finite-check`.

| File | SHA256 | Read coverage |
|---|---|---|
| `research/P66_exact_finite_check.py` | `4eb143aae8255636e70732c6ab8971fa71df62f15e98daa6e370fc02d247978f` | All 526 lines |
| `tests/test_p66_exact_finite_check.py` | `76025610183aa7d90843ce6e9446d55a49fbb251b8117397516fc09d0bdb2f1f` | All 138 lines |
| `research/P66_EXACT_FINITE_CHECK_CONTRACT.md` | `7fa64f384a919522e4b55d7881d4419594665c9d5aeba5b217bce5423c1d7293` | Entire contract |
| `research/P66_exact_finite_preflight_contract.json` | `b390ef541f477742d8c0ab76b3d6ccb637aee46173219736382d42161fd29ba1` | Entire JSON |
| `research/P66_exact_finite_execution_contract.json` | `db6c81db428c3df3f9859c484bf6a4ab8c3303603cd2fb9876a3df7fa9aefa90` | Entire JSON |

Both proof-definition input hashes match the reviewer's previously frozen
and fully read derivations: P66 independent proof
`7cb9a101155df7b1e9c5c7a219c3877e74b6246195952356801d86cb6cb973a9`
and P67 covariance proof
`63f891ca6b03790024bbade59d275e8f115dfccc1fa17c9632aa7ca878c25cf8`.
AGENTS.md, package definition and pinned research lock were also read.
The five code/contract hashes were rechecked after the full source reads.

This review read no qualification stdout, stderr, JUnit, manifest, main
output or scientific result. No Python import, AST, collection, test,
source execution, matrix construction, native call, RNG or metadata query
was performed by the reviewer. Filesystem hashing and text reads only.
Only this review file was written in the separate broken-index worktree;
checker bytes and Git metadata were untouched.

## 2. Mathematical contract and actual finite population

The universal P66 theorem remains a separate proof. This checker addresses
only its finite implementation conventions for L=2,3, N=4L,K=2L, clique
weight 3, matching weight 1, and w=0 or 1/(2L). Its matrix grid has
four t values and two lambda values in the frozen order. No graph, source,
phase or native point is selected using observed success.

The source loops implement exactly:

- 2 L values times 2 families times 4 t values times 2 lambda values:
  32 matrices;
- every matrix times 4 bad sources times 2 targets: 256 B points and
  256 D points, with 128 two-target unions;
- all balanced subsets, including complements, in each family:
  2*(binom(8,4)+binom(12,6))=1,988 costs;
- L=2 through 8: seven COMPLETE one-bright-mode target/source PGF pairs;
- t=1,lambda=1/4 only, both sizes/families, all eight combinations each:
  32 frozen native B probabilities.

No multimode PNR law, collision-free probability, optimizer, sampler,
held-out panel, generic-covariant-unitary population or QPU is computed.
Raw target probabilities are not divided by a collision-free probability.
The D exact point law is checked algebraically; the separate native point
reference is bosonic only.

## 3. Arithmetic, graph and physics obligations

| Component | Exact source locator | Independent static check |
|---|---|---|
| Q(i) field | Lines 28--87 | Fraction-pair addition, multiplication, conjugation, norm and division formulas are correct; zero divisor is rejected |
| Matrix order/adjoint | Lines 90--103 | Rows/columns and conjugation implement ordered products and adjoints |
| Gauss--Jordan | Lines 106--124 | Exact first-nonzero pivoting, row normalization and elimination; inverse dimension guard 1..12; both inverse identities later checked |
| Gray-code Ryser | Lines 127--146 | Every nonempty subset visited once; one changed column; update direction and sign (-1)^(n-cardinality) correct; empty n permanent is one |
| Normalized Fock helper | Lines 149--159 | Repeated output rows/input columns; BOTH occupation factorial products divide the squared permanent; invalid occupations/total counts rejected |
| Literal graph | Lines 162--179 | Heavy clique branches, complete cross-block branch and fixed-offset within-pair matching are mutually consistent; cross branch prevents accidental extra matching |
| Scalar cut | Lines 182--185 | Each undirected crossing edge is counted once from its selected endpoint |
| Source/target order | Lines 188--192 | Tuples are sorted; all four bad and two good subsets are distinct; membership matches combinations' tuples |
| Cayley construction | Lines 195--206 | Weighted normalization, J-I off-diagonals, plus times inverse-minus, and exact rational entries agree with contract |
| Dark projector | Lines 209--212 | Embedded I-J/d on the full CA/CB block, not on an individual clique |
| PGF | Lines 215--227 | Correct (occupied)_m/modes^m coefficient of (z-1)^m; no extra/missing factorial |
| B/D bounds | Lines 230--233 | P66 point/union constants and separate uniform-bright D bound match the proof |
| Exact record encoding | Lines 236--255 | Rational strings and complex pairs retain exact values; finite JSON required |

The Cayley normalization omits a max-with-one because the frozen weighted
degrees are already strictly above one; it is exactly the stated prospective
D, and the theorem permits every positive D. This is not a change to P65's
registered objective or parameters.

The nine fixtures cover actual independent or hand-checkable invariants.
The four-mode direct permutation sum supplies an algorithmically distinct
permanent reference. The rational two-mode splitter has the stated normalized
CF-input and bunched-input probabilities; their masses sum to one. The
explicit inverse fixture requires a pivot exchange and its stated inverse
is correct. The two small cuts, projector, d=2 PGFs and complex-field
expected values were checked analytically. No fixture calls the main graph
factory or its population iterator.

## 4. Main coverage, rank and bound checks

Lines 346--437 preserve the entire frozen domain. The landscape enumeration
has no filter. Exact weighted degree, good/bad costs and the positive gap
are checked before every family grid. Partial-clique costs use the correct
lower bound rather than an equality that might fail.

Each matrix checks both inverse identities, U-dagger U=I, symmetry,
commutation with BOTH block dark projectors and uniformity of BOTH cross
blocks. Rank is recorded as zero/one from a representative entry only
because the corresponding all-entry uniformity assertion is also required.
Rank-zero t=0 and disconnected lambda=0 cases are retained. A failed
uniformity assertion stops the run; its earlier row is only a failure prefix,
not a validated rank certificate.

Every B point uses |per(U[target,source])|^2 and every D point
per(|U[target,source]|^2). All main occupations are CF, so their input/output
factorials are one. Bounds and nonnegativity are asserted per point and
then on each two-target sum. The separate D bound follows from the rank-one
UNIFORM cross block: each of the L source photons in the other component
crosses with probability at most 1/(2L). This is not a B/D ordering.

The PGF stage retains both complete rational vectors and checks their
nonnegativity, masses, target mean, tail and source highest coefficient.
Target mean one is correct; no source mean-one assertion is made. The
seven PGF pairs are one-mode laws only. Their calculation reuses the derived
factorial-moment formula, so it cannot independently prove that formula or
the universal theorem.

## 5. Native reference and tolerance boundary

Lines 258--315 and 440--477 use local NaiveBackend point amplitudes only.
To confirm the API semantics without importing it, the installed primary
source was read directly:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/lib/python3.11/site-packages/perceval/backends/_naive.py
    SHA256 aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d

It constructs rows from output occupations and columns from input occupations,
calls xq.permanent_cx, and divides by the square root of BOTH Fock factorial
products. This agrees with the checker. No remote backend, Processor or
sample operation is invoked. Its native permanent is distinct from the
new exact Python Gray-code routine, although agreement is still numerical.

The 32 native cases are selected by frozen t/lambda comparisons while all
source/target rows are retained. There is no success-based filtering or
replacement. Their full exact probabilities and native complex amplitudes
are recorded. The comparison is exactly

    absolute_error <= 1e-12 + 1e-7*max(native_probability,float(exact_probability)).

The relative error uses that same maximum scale and is zero when both
values vanish. Exact zeros, floating zeros and tiny positive values remain
explicitly labeled. Absolute-dominated acceptance certifies no relative
accuracy; a native zero can pass for a sufficiently small exact positive.
This limitation is correctly stated in both contracts and the source.
There is no interval-error certificate, full-law comparison or global TV
bound.

The native qualification contains five fixed two-mode HOM probabilities,
including bunched input and output normalization. Observations and provenance
are emitted to JUnit before the tolerance assertions; a later query exception
retains earlier completed observations. An import failure before metadata
exists instead remains an ordinary failed qualification, never a pass.

## 6. Provenance, limits and failure prefixes

The source verifies the persistent interpreter's resolved path, actual virtual-
environment prefix and Python 3.11.15. It dynamically checks exact versions
of NumPy, SciPy, Perceval and Exqalibur. Pytest and all additional research
dependencies are pinned in the project/lock; this loader does not dynamically
assert every installed package version or authenticate all OS libraries.

Exqalibur is imported before Perceval. Config.compute_max_thread_count is
set to one and read before/after Perceval import, around every point, and at
the end. The bounded runner must also supply its conventional numerical
thread environment limit. Loaded module paths/hashes and the interpreter
path/hash are observed; the captured module files are rehashed after all
queries. Files lazily loaded after that snapshot, OS libraries and install
provenance are outside this supplementary closure, as the contract admits.
The ten declared project inputs contain both JSON contracts, source, fixtures,
proof conventions and pinned package files.

The planned runner arguments impose wall90, per-process CPU60 and combined
logs4MiB with one intended worker/thread setting. There is no claimed hard
Darwin RSS or unsupported affinity cap. Logical256MiB is a workspace plan.
Main's stream guard caps records at27MiB and the three scientific files at
28MiB, making main's combined log/scientific plan32MiB. Qualification's
JUnit writer has no separate in-process28MiB abort guard: ROOT must verify
its actual declared-output size from its receipt against that plan. This
is a post-execution receipt check, not an amendment of source or caps.
The main guard and the runner's log cap are actual different controls.

Fresh output directories and exclusive files prevent overwrite. Records are
flushed before assertions. First failure retains context and traceback with
nonzero exit and no permitted retry. Hard resource/launch/filesystem failures
may prevent a summary; the existing prefix and runner status then remain
the evidence. They cannot be interpreted as missing zero-probability rows.
The exact expected-count gate precedes PASS_FINITE_ASSERTION. The source
explicitly sets universal_proof_certified=false and identifies its native
comparison as tolerance conditional.

## 7. Conditions for accepting a finite result

1. ROOT independently verifies that qualification actually passed its nine
   fixtures, that the complete native observations are present, and that
   observed outputs fit the declared budget. This review has not read them.
2. The main uses these exact frozen hashes and argv in an exclusive bounded
   slot, with no cap, tolerance, scope, point or retry changes after launch.
3. The v2 manifest is valid, inputs are unchanged, execution completed, all
   declared outputs exist, and the complete counters match the contract.
4. ROOT inspects raw rows/failures and calibrates conclusions to the finite
   grid and mixed-tolerance limitations. Full existing tests remain required
   before merging executable changes.

Under those conditions the implementation supports its finite diagnostic.
No static correction or main-blocking source defect is identified. Passing
would strengthen confidence in these conventions; it would not turn the
negative optimizer state into a positive scientific result or authorize QPU
execution, a paper revision or a claim of novelty.
