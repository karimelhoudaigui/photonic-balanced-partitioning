# P48-B static physics/code review at the second pre-execution freeze

2026-11-25. Target code commit
`4a199f85a0a6f015c31ad96b83d8a66c73702659`, parent
`e87035a853c84a4e8f33d5c928458a6452a0fa2e` (unexecuted first snapshot).
Primary script: `research/P48_spectral_pit_probe.py`, SHA256
`98b7d2d6b7623e935af728bd0d114636b752b9e1c8301ab6c7cfb6e8e609661c`.
Authoritative root card:
`bfdff40926ad395a14f64260513b6ef21a1257f5`,
`research/P48_SPECTRAL_BASIS_CLAIM_CARD.md`, SHA256
`9e0a5c7d46cc1fb2f61eaec81f3508ef729ccc88a7317c4981bb6f5eec53fb4f`.

Primary verdict: **incomplete, with one precise pre-run numerical-control
obligation**: Gaussian normalization at a structurally deterministic
OCCUPIED output row is not protected by the empty-row mask or existing
fixtures. This is a statically demonstrated permitted-error amplification,
NOT an observed NumPy failure or an observed problem on a DEV graph.
The remaining source/physical, comparison, accounting and preflight-isolation
checks below passed static review. No other blocking mismatch was found.
An independent exact-hash addendum is needed for the announced correction.

No P48 Python import, test, graph generation, sampling, numerical spectrum,
MILP, helper run or QPU call was performed by this review. The reviewer
authored the earlier P48-A twirl/PMF analysis and P48-B card critique; this
is implementation review independent of the encoder author, not a new
third-party validation of those self-authored mathematical arguments.

## Frozen closure inspected

The script, spec, contract MD, two runner contracts and integration tests
were read completely; the first-to-second-freeze diff was inspected. The
imported coherent helper and its exact finite test file were read. P43/P45
helper bodies had already been inspected in the P47 static review; their
hashes are unchanged. They supply the local sampler, integer graph cuts,
common anchor, classical searches and feasible completion. Software versions
in the contracts are declarations here, not a newly measured runtime.

| File | SHA256 at inspected freeze |
|---|---|
| research/P48_spectral_pit_spec.json | 7e1881ce23fe1690bafae4c8b7ee8a339da99ed670b727b816448ba0e77763e8 |
| research/P48_spectral_pit_contract.md | 9079179878d8ca5aa102c1e097dcfe61a3e5cd8d7e5471af4b240986d363b8a2 |
| research/P48_spectral_pit_preflight_contract.json | a6695a4df3bd285aa1ebca8e98f1d29e26d475e8dd94a994ebf867cb99dfc4a4 |
| research/P48_spectral_pit_execution_contract.json | a6c0c94cca8a59facbe287ab5c36f936918b262d62ec2c1df96c38c24ba0446b |
| tests/test_p48_spectral_pit.py | e53f178f0428be800c1abe06b5a9c3c02c43a18dd4e7884df34f6a2a98e518f3 |
| research/P48_coherent_marginals.py | a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac |
| tests/test_p48_coherent_marginals.py | 43fb78402527c607124ec58a44017bae53b1520c14296021e52910e95a14ff0c |
| research/P43_global_gain_probe.py | b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777 |
| research/P45_adaptive_probe.py | bb00ca61e45794ecea2333e0aa1864edfaec43128c1efa98dd8384c3d6889f92 |

The runner lists 11 main execution artifacts and 12 preflight artifacts,
including the helper/test and dependency lock files. Full runner closure
and installation/version measurement remain execution checks, not a static
manifest or a claim of tests already run. The helper's earlier 26-pass
qualification is reported by the supplied contract; it was not rerun here.

## Passed static obligations

**Spectral source and gauge.** Script lines52-86 implement the marked real
combinatorial Laplacian, its opnorm normalization and ascending eigensystem.
The first r columns are used without Haar rotation. Guarded gaps[:r]
include r-1 internal occupied gaps plus the occupied/vacuum boundary;
all N-1 gaps/residuals are recorded. Vacuum-complement degeneracy is not
mistaken for a change of the occupied state. The r+1th eigenvector used
only for a classical rounding follows the declared numerical convention;
if the vacuum complement is degenerate that extra rounding is not itself
a uniquely invariant spectral object, but its actually scored discoveries
are shared and do not alter the source. Column pivots fix only phases;
real signed top/bottom roundings are both retained. Marks, Fourier order
and priority have carried-label conventions.

**Ports and completion.** Lines89-133 build the two N-by-r frames and
U=[V,null_space(V*)]. The FIRST r source columns remain V. Every physical
model occupies ports0,...,r-1, while species groups permute those SOURCE
ports, not graph vertices. The graph anchor is constructed only for common
classical candidates and matching; it never enters V or selects a new
optical source. Vacuum-column choices do not change the occupied state.
All N outputs/counts are retained; no CF retry, hidden herald or loss
filter appears. The formulas mu=sum q, P=VV*,
Cov_B=diag(mu)+|P|^2-2qq^T are the correct CF-source identities.

**Subunit rows and coherent PMFs.** Lines136-217 represent numerical q
exactly as Fractions. A genuinely subunit row is unchanged. Only an excess
sum above1 of at most3e-12 is removed from the largest entry, with raw/used
mass and L1 correction recorded. The same repaired q goes to all five
discrete-model tables; no input row is scaled to1. The original sampler
uses the numerical V/U, so that tiny repair is explicitly an approximation,
not an equality or interval certificate. B coefficients h!e_h(q), D e_h(q),
species convolution, fixed-phase polynomial coefficients and the sphere
positive mixture have the correct factorials and row mass mu<=1.

Decimal80 coefficient inversion/corrections are saved. The helper tolerance
1e-60 and B/D tolerance1e-12 are checks, not proved forward-error bounds.
The helper correctly handles r0, r1, mu0 and mu1, including the fact that
mu1 with several nonzero q is NOT a deterministic B/sphere occupation.
Production coherent count and rounding generators both use CONTINUOUS
phases; r+1 roots occur only in finite polynomial count fixtures. Sphere
uses circular complex Gaussian coefficients normalized to unit norm.
Both use Multinomial(r,|Vz|^2), conserving r counts with tiny norm repairs
recorded. Their own unconditional PIT tables and separate jitters are used.
Gaussian uses the actual factor variance, with the zero-variance qualification
in the next section; IID fields are independent uniforms.

**Preparation discoveries and comparison budgets.** The amendment adds
top/bottom mu and every column q, for EACH encoder, plus a rectangular
N-by-r assignment minimizing -log(max(q,1e-300)). It selects r distinct
output rows, one for each source column. Metadata correctly disclaims
optimization of the permanent/summed D support probability. Row priority
controls ties; floor counts/cost/time are retained. These candidates and
the signed low-eigenvector roundings are scored and credited before Cref,
alongside the anchor, K^2 swaps, zero/greedy and vacuum-mid-PIT discoveries.
No discovered subset is loaded into V. Outer common timers include sorting,
matrix construction, marginal tables and all preparation work.

All seven arms share the encoder/lambda grid, decoder, seed priority and
100/173 informative units per proposal. Four settings*eight draws*two
trials*four graphs give 256 proposals/arm and 3840 simulated photons per
physical arm, if the whole population completes. Five baseline methods
each get their own 3200/5536 units per graph/trial; their portfolio is not
free. The new coherent-rounding baseline uses both frames and both
continuous phase/sphere laws, then at most two fully charged swap scans.
Joint timing/score prefixes and all tuning cells remain archived. Counts
are informative evaluations, not every repeated cut() invocation or a
hardware throughput metric. Shared spectral/guide information and classical
discoveries cannot be presented as optical gains.

**Failure and population handling.** Known gap/PMF/network numerical failures
save context/marks/reason and make that entire graph inconclusive rather
than redrawing it. A partial successful population is labeled incomplete;
positive acceptance remains false. Unexpected exceptions/resource limits
may stop a run and leave partial files/logs; they must remain failures,
not be converted into a successful subset. No run/retry was made here.

## Remaining pre-run obligation: deterministic nonempty Gaussian rows

Lines120-123 mask only mu==0. A CF source row q=(1,0,...) instead has
mu1 and n_i=1 DETERMINISTICALLY; its target covariance row/diagonal are0.
The all-zero-graph fixture has an entirely zero covariance, so it does
not test such a row mixed with nontrivial stochastic covariance.

Here is a permitted-error analysis, not a measured NumPy counterexample.
In a two-coordinate covariance sector diag(0,sigma^2), rotate the zero and
positive eigenvectors by a small angle epsilon. The resulting positive
factor column is sigma(epsilon,sqrt(1-epsilon^2)) up to higher orders.
The covariance/eigen residual is O(epsilon sigma^2), small enough to pass
absolute checks for arbitrarily small epsilon. Yet effective variance on
the deterministic first row is epsilon^2 sigma^2>0. Lines281-285 then
standardize its raw value by epsilon sigma, producing the SAME order-one
normal variable as the second row instead of independent jitter. Thus
small absolute residuals do not control the normalized copula near zero
variance. Exact algebraic sparsity may happen to be preserved by a given
LAPACK call, but this code/fixture set supplies no universal guarantee.

The minimal requested correction is to mask exactly structurally
deterministic0/1 CF rows, record their indices and preserve an independently
jittered Gaussian field there. Do not mask all mu1 rows: a spread mu1 row
has positive B variance. A mixed deterministic/stochastic/empty fixture,
with injected tiny admissible eigenfactor leakage, can verify the defense
without opening DEV graphs. Any near-unit tolerance beyond exact one-hot
structure must be predeclared and its covariance change recorded.
This obligation blocks a static green light on the OLD hash; it does not
assert an observed DEV bug or invalidate the other passed checks.

## Preflight isolation, provenance and limits

The planned 50 cases are 24 integration fixtures plus26 helper fixtures.
They were READ, not run. Integration uses a fixed6-mode graph,10-mode
species4+1 fixture, exact source/vacuum examples and permutations. The two
N26/34 decoder tests use ZERO arrays, not the frozen DEV graph generators.
The retention test monkeypatches make_graph to a six-mode zero graph and
forces a declared degenerate-mark fixture. No test loads the DEV spec or
calls main; imports do not generate a DEV graph. The local Clifford test
is a smoke acceptance/count-conservation check, not a statistical sampler
certificate. No model/graph outcome can be accepted by those fixtures.

Actual checks were read-only cat/nl/sed/rg, git-show/diff and SHA256 reads
on the exact cards, source/tests/helper/contracts; algebraic reconstruction
and the symbolic leakage example above. No external proof/source novelty
check, P48 numerical computation, pytest or graph generation occurred.
This review file alone is written in the isolated replication branch.
The next cheapest check is exact-source review of the minimal correction,
then the coordinator-authorized targeted preflight at its new closure.
