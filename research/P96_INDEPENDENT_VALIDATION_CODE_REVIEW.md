# P96 exact-freeze validation code review

26 November 2026. **CORRECT ONLY within the declared finite real-rational
mathematical scope; NOT READY for execution under the full failure-diagnostic
promises until E1 below is repaired.** No nominal mathematical/selection error
was found. The evidence-preservation defect cannot create a false PASS, but
can discard values required to explain an unsuccessful native/guard call.
No qualification, import or experiment was run for this review.

## Exact target and complete coverage

Target clean at reading: ac67650ceaa2bf7639ed72ef6fddb28a02067749,
parent f145aca1, .local/p81-exact-review, research/p94-mechanism-design-reuse.
All five committed artifacts,550 lines, were read completely:

| File under research/ unless shown otherwise | Lines | SHA256 |
|---|---:|---|
| P96_column_loss_validation.py |346|`3a9e92668bd573b8397a457eaa46923246c2d26a4a83685362a764f477291fe0`|
| tests/test_p96_column_loss_validation.py |100|`148770d282d3365677d3748c5e250f8f96531051726aab23d633edf09e32c3b8`|
| P96_column_loss_validation_contract.json |37|`2eb61afd03906e6eb022134680c973620a09b15e691196c8e8948150316d1845`|
| P96_column_loss_validation_preflight_contract.json |24|`1aaa6119f65c565d8404b45f035aca912307df51f8f67099d88158902fd179b7`|
| P96_VALIDATION_POPULATION.md |43|`efce85ea663c22a05fc9065e1d50e3cffed67a5e1632354921510ceeb6e008e2`|

An initial filename lookup used two wrong long names and read no source;
the actual names above were then resolved. An oversized combined display
was truncated; complete bounded rereads supplied tests and both contracts/
population before this coverage claim. No missing range was inferred.

The169-line mathematical proof was reconstructed by this reviewer before
the code task, source6f4e7fb90e284a8e358c55886ddd2032d45811f9, SHA256
b378ebd6bb0bb6f981e9fe395938e3a43aec7775f761b81cda7b394f6dc1e94e.
The separate157-line P96_INDEPENDENT_SURROGATE_REVIEW.md was read in full,
SHA256 a64783dee2b4903b475a8b1ea554640b4c320d9da81cf854871f219725e29d7f.
Its general complex-T theorem does not enlarge this code's real-T population.
No P95 proof, outcome or unrelated route is a dependency here.

## Mathematical reference and normalization

The polynomial reference builds each entry of I-T^tT+T^t diag(z)T exactly,
then takes its permanent by permutation/dictionary multiplication. The
constant loss Gram term, signed off-diagonal entries and all coherent
permutation cancellations are retained. Only exact intermediate zeros are
removed; the final law is initialized with EVERY occupation of total0..K,
so structural zeros remain visible. Positivity and mass1 are exact gates.

This reference uses the unconditioned PGF from the proof, with CF input
normalization one. It is not an amplitude permanent whose square/factorial
would need to be applied afterward. The full observed/environment Fock
normalization is instead independently exercised by the native marginal test.
No CF rejection, fixed-survivor denominator or accidental input factorial
appears. K0 gives the empty permanent1 and the unique vacuum occupation.

The q construction separately evaluates lambda and the real specialization
of g2=lambda_j lambda_l+|(TT^dagger)_jl|^2-2 sum_i p_ji p_li. Diagonal
pair masses divide by2; distinct pairs occur once. For K<2 impossible
zero-mass categories may be omitted harmlessly. All q support lies inside
the enumerated P support, so the exact TV sum omits no q-only configuration.
First/factorial-second moments of both laws, q nonnegativity/normalization,
TV=weighted tail and the full2/3,24e3,4mu^3 chain are checked as Fractions.

The12 valid fixtures obey the certified trace domain. X4 has physical
trace/norm1, exact positive P and q(singleton)=-1/2; it is explicitly
EXPECTED_OUTSIDE_DOMAIN with theorem_applied=false, not a failed theorem or
a normalized negative sampler. Both sharp K3 cases require TV=24e3.
No output clipping, tolerance or floating arithmetic enters the exact audit.

## Noncircular fixtures and complete populations

The nine pure tests use independent hardcoded hand tables rather than merely
calling audit and asserting its status. Manual comparison with the PGF/proof
confirms the vacuum/unary, signed HOM and nonorthogonal K2, two K3 rank-one,
X4 and boundary K4 total-count tables. The HOM zero coincidence and bunch
weights test the collision factor; the signed nonorthogonal case tests
cross-column terms. K3 tables test the exact24 coefficient, while K4's
nonzero fourth sector prevents confusing TV with just four times P(N=3).
The final pure test binds the literal shape/order/iterator population.

The fixture factory is fixed before execution, with no RNG/filter/search.
It has162 valid signal bins plus five X4 bins:167 total, including zeros.
Only V0,U1,H2,R3a,B4 receive native calls. Their exhaustive full-sector
populations are1,2,10,20,126, totaling159; their unconditional signal
marginals have1,2,6,4,15 bins, totaling28. The exact13-case audit precedes
all native setup. This is neither an exhaustive theorem proof nor an
independent replication merely because two formulas occur in one program.

## Halmos/native conventions and numerical guards

For each selected real rectangular T, U=[[T,sqrt(I_m-TT^t)],
[sqrt(I_K-T^tT),-T^t]] has m+K rows/columns. Its first K INPUT columns
and first m OUTPUT rows contain the intended T; input is [1]*K+[0]*m.
Rectangular R3a/B4 make confusing these two partitions observable.
K0 explicitly uses the one-mode identity with vacuum input.

Symmetric eigendecomposition supplies both square roots with no negative-
eigenvalue clipping. Both U^tU and UU^t are tested at absolute1e-11.
The five selected operands are away from the zero-eigenvalue boundary;
the singular physical X4 is exact-only. This is not a timing prediction.
Native Naive evaluates every full-K occupation, never sample()/a stochastic
backend. Environment occupations are summed by the first-m signal tuple;
all28 marginals and total mass are tested at absolute1e-11, relative0.
There is no repeated numerical run, cutoff or favorable-outcome selection.

## E1: failure observations can be discarded before serialization

Source228–235 obtains an amplitude, then emits amplitude/probability using
json.dumps(...,allow_nan=False). A returned NaN/Inf, or overflow in the
probability, can raise before native_raw is written. The previous native_attempt
preserves the case/full occupation, but neither amplitude repr nor the actual
nonfinite probability is retained in state/failure. Hence the promise that
every returned observation is preserved, including unsuccessful ones, is unmet.

Likewise threads() at173–178 asserts before returning its observed dictionary.
An environment/native drift can leave last_native_after=null with only a
generic assertion message, losing the actual offending readback. The finally
call at231 can also raise after prob_amplitude has returned, before native_raw
is emitted; neither that raw return nor the converted amplitude is retained
in failure state. Conversion itself can fail before storing a return repr.
Reset and preserve the raw return per point before conversion/finally guards.
Finally,
native_case206–218 checks eigenvalues/unitarity before native_setup: a failed
root/Gram guard loses its computed operand/eigenvalues/U/residual values.
These defects do not weaken acceptance: those paths stop inconclusively.
They weaken the prospective failure evidence and must be repaired before
claiming that evidence contract. ROOT acknowledged E1 before this report
was frozen and requested a separate pre-execution author correction.

The exact audit also runs its gates before emitting its returned p/q table;
an internal exact failure retains case/T/start and traceback rather than a
complete failing table. This limits diagnosis, without permitting a false
finite PASS. Pure test record properties precede their external hand-table
assertions, but cannot recover values if audit itself has already raised.
A future corrected source/tests/population must be reviewed at its new hash;
no prospective correction or added test has been read/approved here.

## Execution, bindings and limits

Import is stdlib-only; the persistent Mac interpreter/version guard is inside
main, so pure fixtures do not impose that path on the executing interpreter.
The pure launcher uses-I -B, literal nine-node module selection, disabled
plugin autoload/cache, legacy JUnit and FSIZE512KiB BEFORE pytest. Its own
runner budget is CPU30/WALL60/log4MiB; no optical import belongs there.

Main sets FSIZE8MiB and CPU60 before scientific imports. Six environment
variables are set before exqalibur; native config1 precedes NumPy/Perceval
work. Versions, eight external preimport hashes, actual critical loaded
identities and interpreter hash are checked. Main has WALL90 via the outer
runner, log4MiB, one worker and zero retries. Evidence reserves128KiB within
its aggregate three-file8MiB sink; FSIZE alone is per-file, not aggregate
cache/RSS enforcement. Physical IO failure may leave an incomplete prefix.

The two contracts share exactly eight existing static paths. The proof is
honestly contextual at this freeze, not a guessed missing preflight input.
Main requires a separate real binding with the eight qualified static hashes,
its own path, actual proof/hash and ROOT-selected qualification/auth evidence.
The binding is hashed as an input, without requiring a circular self-hash.
Its exact input list/command/caps and theory source still need ROOT review.
The fixed data child is below the fresh runner parent, with no resume/overwrite;
raw records/logs/manifest must be sealed before inspection and receipted later.

Only text reads, file/Git metadata and this isolated report were used. No
import/AST/bytecode/collection/test, scientific execution, RNG, graph,
native API, runner/validator, checkout, delegation, push, QPU or paper action
occurred. Source/proof/tests/contracts/raws remain unchanged by this reviewer.
Even a corrected finite PASS would not establish a full Born law, complex-T
coverage, finite-bit sampler, matched hardware cost, novelty or positive goal.
