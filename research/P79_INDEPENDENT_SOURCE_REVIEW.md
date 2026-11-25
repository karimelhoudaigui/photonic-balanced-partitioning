# P79 independent full static source review

Primary outcome: **audited, not executed**. No material mathematical or
protocol blocker was found in the exact frozen source identified below.
Its implementation matches the three declared finite checks on the six
registered cases. This is a static verdict, not a qualification result,
main-run authorization, observed PASS or finite-bit sampling certificate.

## 1. Revision, coverage and evidence boundary

Reviewed worktree: `.local/p79-even-loops`, clean commit
`602acc70d2ebf00d3b819c0966e3558b4f07b267`.
All five new files were read completely, 969 lines in total:

| File | Lines | SHA256 |
|---|---:|---|
| `research/P79_even_loop_validation.py` | 591 | `74cb27b1e969447ec0b7122d8b5c2fcb286d64c3ed6f2600473819b5a51836f8` |
| `tests/test_p79_even_loop_validation.py` | 158 | `4dbebf0e852422691a0bc905dcc5d85054e4f7274630c020dbc04ca67c791574` |
| `research/P79_FINITE_VALIDATION_CONTRACT.md` | 180 | `afedc7b4f79d0bf66ea213014fce6c787579e4c83619f958b01db57bcca6d4b8` |
| `research/P79_even_loop_preflight_contract.json` | 20 | `94390ad71047d7d01f241011f18a82bce31e5ffbf28d0db2b10b81896f51f7e3` |
| `research/P79_even_loop_execution_contract.json` | 20 | `d61df50313029e804f7ea7944f5755a1dfbf4095fdaa454a761534f95aa0e012` |

The pinned P66 loader's top-level structure, native_api/native_readback,
version/thread guards and calling convention were read as text; its hash is
`fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d`.
The P78 author bytes still have the previously audited hash
`118c88279e01bb13b81450b7f30c2cb55ad852e3a34cfcffbdc56c1c64df7c4a`.

The other three inputs in both contracts are unchanged identified files:

- `AGENTS.md`: `6c4c409cdf9d05330bc46b9f607b7034e16bcaf51086b712a80d03ccd8e78e5a`.
- `pyproject.toml`: `7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4`.
- `requirements-research-lock.txt`: `3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1`.

This review is written only in the reviewer's separate
`.local/p66-dark-barrier` worktree, starting at
`2c9810ece01584a8baae863d6d81047a3709d5e3`. No source/test/contract edits
were made. No source import, AST parsing, collection, test, RNG, graph,
scientific calculation, native backend or probability query was executed.
No P79 outputs or P75 outputs were read. No P80 finite-bit argument is a
premise. The P78 ideal-model proof and its prior exact-source review are
background mathematics, not empirical evidence from P79.

The computation-audit workflow was applied statically. Thus there is no
run manifest, observed hardware profile, qualified native interface or
executed result to validate in this report. Hashing and text/Git operations
are the only executed checks.

## 2. Target and exhaustive finite populations

P79 tests full raw PNR statistics of the specified undisplaced pure
Gaussian pair matrices, not a passive collision-free Fock optimizer or
an available squeezed source on a QPU. The six literals in source lines
64-89 match the card, with rational component radii/vectors and signed
squeeze values. G5 has two separately processed pair components; G6 has
the nonuniform vector (1,2,1). None is selected after observing outcomes.

The occupation generator at 92-100 visits every nonnegative integer
m-tuple at the chosen total exactly once. Its population counts follow
directly from binomial(m+k-1,k):

| Modes/cases | Exact totals 0/2/4/6 | Native outputs 2/4 | Even-input/output calls | Statistical bins |
|---|---:|---:|---:|---:|
| 1 / G1 | 4 | 2 | 2 | 5 |
| 2 / each of G2,G3 | 16 | 8 | 21 | 17 |
| 3 / each of G4,G6 | 50 | 21 | 108 | 51 |
| 4 / G5 | 130 | 45 | 390 | 131 |
| Total over six cases | 266 | 105 | 650 | 272 |

For native calls the formula is out2*m + out4*binomial(m+1,2), because
all-even input occupations are twice the weak compositions of total/2.
The code retains inputs with zero source coefficient. Statistical bins
add exactly one tail>6 to each exact population. Counts are asserted
before later phases or final PASS; early failure is not silently reported
as complete coverage.

## 3. Exact coefficient and physical-normalizer paths

Source lines 103-158 correctly implement the expanded-label hafnian,
including the empty value one and collided labels, and divide its square
by product n_i!. This is the appropriate unnormalized real-Gaussian
number coefficient. For two photons in one mode it gives Z_ii^2/2,
whereas two distinct modes give Z_ij^2. No CF restriction removes bunching.

The exact determinant algorithm performs row swaps and Schur updates;
the stale entries below a past pivot are never used as a later Schur
entry. Its sign and pivot product are consistent. Exact leading principal
minors of Q=I-Z^2 certify positive definiteness for the symmetric inputs,
and hence the strict contraction domain. The raw prefactor is
sqrt(det Q), not det Q or a sector normalizer. Equality to product(1-s_j^2)
is checked independently from the literal signed spectrum.

The polynomial path at 161-194 constructs DZ with the departure variable
z_i on each matrix row. Its trace at lengths 2,4,6 is divided by that
length. Polynomial convolution then adds L, L^2/2!, L^3/3! through degree
six; terms of greater order cannot contribute because L has minimum
degree two. It shares no expanded-hafnian computation. No root/reversal
quotient, trace multiplicity or factorial is missing.

Each point, including zero, is emitted with both exact rational
coefficients and its binary64 raw q before the equality assertion.
The future finite equality would be exact in those coefficients; the
square-root prefactor and reported physical q remain floating values.

## 4. Independent passive-sector amplitude reconstruction

The literal decompositions at 241-273 match U diag(s) U^T=Z: H2 uses
the two signed eigenvalues for G2/G3; H2 direct sum H2 matches G5;
the first DFT3 column gives J3/6 in G4; G6's columns are mutually
orthonormal and its first column is (1,2,1)/sqrt(6). Both unitarity
orders and pair reconstruction are checked at residual<=1e-12.
Signed s is intentional; this is not a claim that signed values are
the conventional nonnegative Takagi singular values.

For an even single-mode input n=2j, expansion of the pair exponential
gives s^j*sqrt((2j)!)/(2^j*j!). The product formula at 276-280 is therefore
correct, including negative signs and s=0,n=0. At 394-420 the native
amplitudes for every source are weighted coherently, summed as complex
numbers, and only then squared and multiplied by sqrt(det Q). Summing
probabilities or dropping negative/zero terms would be wrong; neither
occurs. Raw terms, sums, zero labels, errors and tolerance branches are
archived before the point-level assertion.

P79 uses pcvl.Matrix(u) directly, so the complex DFT entries do not pass
through P66's rational-C coercion helper. The only loaded project helper
is the hash-checked frozen P66 file. Its native_api verifies pinned
package versions, sets exqalibur's actual compute_max_thread_count to
one and reads it back before/after loading Perceval. P79 additionally
reads it before the factory and around every prob_amplitude call.
The portable helper does not weaken the contracted main CLI profile.
Actual compatibility and residuals remain unobserved until an authorized
run; static inspection does not certify a third-party native binary.

The mixed bound is exactly 1e-12+1e-7*max(|q|,|reference|), with the
absolute/relative dominant branch retained. This validates specified
point probabilities at tolerance if executed, not relative accuracy
for all small probabilities, all photon sectors or global TV distance.

## 5. Perron tables and full raw loop sampling

At 197-238, rational rows must sum exactly to one before an integer CDF
is built. Partition, positive r/v, support connectivity and absent
cross-block edges are checked. The row-sum identity enforces Zv=rv on
each component. For nonnegative connected symmetric input, a positive
such vector supplies the correct top radius. All registered components
satisfy the required algebraic identities; G6 produces the nonuniform
row probabilities (1/6,4/6,1/6). No floating repair or global-vector
division across G5's components is used.

The integer selector draws from [0,denominator), chooses the first
strictly larger CDF endpoint and thus skips any zero-probability entries
without reweighting. Its guarded denominator fits the requested integer
generator range. The root at 433 is uniform over the component modes,
independently of the Perron stationary weights.

The population is Poisson(-m_c/2*log1p(-r_c^2)), and the half-length
uses logseries(r_c^2). The loop visits the departure before each of its
2l transitions, excludes the duplicate terminal vertex, and adds visits
only on a return. All proposals and transitions, including rejected
paths, are counted. Component results add; G5 consumes successive
variates from its one registered case stream. No sector/CF filter is
inserted. All complete records, including vacuum and tail observations,
are emitted before count-domain assertions and histogram accumulation.

The implementation intentionally uses floating Poisson/log-series
parameters. It is not an exact Turing sampler, even though Z,P and their
CDFs are rational. A fixed PCG64 stream is a reproducibility convention,
not a proof of ideal iid randomness. No result should replace these
limitations by the ideal P78 theorem. Also component_tables is a helper
for the specified nonzero components, not a claimed general treatment
of every zero-matrix instance in P78.

## 6. Statistical family, reference tail and stopping

Each complete case has exactly 20,000 unselected raw records. Every
occupation at totals 0/2/4/6 and one tail>6 receives an interval, including
zero-reference/zero-observed bins. Odd totals would fail a domain guard;
they are not treated as another discarded optical class. The tail
reference is 1-fsum(finite raw q), explicitly checked in [0,1] and never
clipped or renormalized.

The formulas at 289-299 are the two-sided marginal Clopper-Pearson
beta-quantile bounds, with exact endpoint limits for counts zero and N.
The per-bin error is .01/272. Bonferroni supplies the declared nominal
1% family exclusion rate under ideal iid sampling without independence
between bins. Predeclared first-exclusion stopping cannot inflate that
union bound: observing only a prefix does not add exclusion events.
The code labels an exclusion STATISTICAL_DISCREPANCY, including its
possible family false-alarm interpretation, rather than a disproved
unbounded theorem.

Both q and beta quantiles are floating. Expanding coverage by 1e-12 is
an explicit numerical allowance, not a certified reference interval or
a proof of quantile error. The nominal statistical statement is not an
end-to-end finite-bit guarantee. Descriptive photon/step means are
emitted before interval decisions; no mean confidence interval is
invented. The source mean sum s^2/(1-s^2), component transition mean
sum m_c*r_c^2/(1-r_c^2), and P78 bound use emitted/raw quantities.

## 7. Order, prefix integrity and resources

The run function has strict global order: all 266 exact points, then all
105 native points/650 calls, then stochastic cases in fixed G1..G6 order
on seeds 7910001..7910006. No RNG is constructed before the first two
phases complete. A later case is not drawn after the first failed case
statistics. completed_draws/completed_bins and per-phase states expose
the exact visited prefix and all later NOT_RUN entries.

StepBudget reserves before each transition and is shared across all
cases, with fixed maximum 5,000,000. A cap does not truncate a path into
a valid output or replace an interrupted draw by vacuum. Complete
previous records are flushed; summary/failure retain the last context,
including partial visits and work counters. That context is not a full
RNG-state checkpoint or full partial path, and no resume is promised.
The complete-draw totals must reconstruct budget increments on every
completed case; the global counter also retains interrupted work.

Records are exclusive, incrementally written and flushed, with a 30MiB
cap. Summary/failure add to a 32MiB scientific cap. CPU60/wall90, log4MiB
and hence combined36MiB depend on the contracted external runner; the
source does not self-enforce CPU/wall deadlines. Logical256MiB is honestly
a plan, not an RSS/address-space or affinity guarantee. Output support
and random work remain unbounded until an inconclusive resource stop.
External interruption can leave only a prefix or missing results, as the
card states. An actual v2 receipt must be checked before interpretation.

Internal summary timers stop before final hash/summary serialization;
they are descriptive script fields, not the external runner's complete
resource measurement or a hardware timing claim. No caught failure,
step/record resource stop or statistical exclusion in the three scientific
phases reaches FINITE_VALIDATION_PASSED. Final serialization failures can
leave incomplete artifacts, potentially including an already-written
summary; its status string alone is insufficient. Successful child exit,
all declared results and the matching validated receipt are required.
A partial run still requires sealing and inconclusive interpretation.

## 8. Tiny qualification, closure and final disposition

The test source contains exactly 12 literal functions, with no cases()
or production draw invocation. Direct expanded hafnians and direct/native
photon fixtures stop at two photons; scalar trace checks reach degree
six on at most two physical modes. The two native HOM points use source
(1,1), targets (1,1)/(2,0), references 0/.5 and readback one. CP boundary,
row/Perron rejection, serialization/exclusive prefix and CLI-before-factory
guards are covered prospectively. No seed or main case is evaluated by
qualification. These tests have not been collected or run in this audit.

Both v2 JSON files bind the same ten input paths: three instruction/
dependency files, P78 author, frozen P66 loader and the five P79 files.
The exact main child command, separate pytest/JUnit child command, seeds,
results and bounds are mutually consistent. The strict main CLI checks
the persistent Python3.11.15 venv and all five numerical environment
keys before output creation/case construction. Actual wrapper inputs,
result declarations and before/after hashes remain future run evidence.
No installation, network dependency, QPU call or credential is introduced.

There is no material pre-execution source correction requested. This
verdict covers only the frozen implementation and finite assertion; it
does not assert any of its expected equalities or statistics passed in
the environment. ROOT must separately decide qualification and main.
P79 PASS, if later validly observed, would remain finite validation of
this raw-count model and not prove an unbounded law, global TV bound,
novelty, photon-source availability or an optimizer advantage.

Final hand review checked coefficient normalizations, signed coherence,
all populations and retained zeros, root/visit conventions, CP endpoints,
early exits, seed order, native API calls, hashes, byte/resource scopes
and serialization. No extra mirror tests or execution were requested.
