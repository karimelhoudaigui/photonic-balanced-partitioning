# P75b prospective six-mode pure-Gaussian CF falsifier

25-Nov-2026. **CODE ONLY, NOT EXECUTED.** No import, AST parse, collection,
test, matrix evaluation, RNG evaluation, optimizer, native amplitude query
or main experiment was performed during authoring. ROOT must read and freeze
all five files, authorize one qualification, inspect it, then separately
consider one bounded main. A prior analytic resolution may cancel it instead.
This is conjecture falsification, not a graph optimizer or QPU preparation.

## Pre-execution change history: four-mode search cancelled

The originally proposed P75a four-mode search was never written/frozen or
executed. A static proof resolved its bound first. For symmetric complex
4x4 contraction Z, put S=Tr(ZZ-dagger), x=S/4<1. Its three-term hafnian has
absolute value at most one half the sum of its six off-diagonal squared
moduli, hence at most S/4=x. AM--GM on four singular values gives
sqrt(det(I-ZZ-dagger))<=(1-x)^2. Therefore its all-ones CF probability is
at most x^2*(1-x)^2<=1/16, including complex diagonals. This cancelled the
four-mode main PRE_EXECUTION; it is not a negative measurement or failed retry.

ROOT prospectively changed the first unresolved target to SIX modes.
No data existed when parameter dimension changed from21 to43, the analytic
baseline changed to1/64 and the scientific-byte cap changed from4 to8MiB.
The same six seed integers and300-evaluation/start bound are predeclared
for this new experiment. None has been evaluated. All other caps below
were also fixed before qualification/main.

## Exact mathematical question and parameterization

For a pure zero-displacement Gaussian state on SIX modes with complex
symmetric contraction Z, the raw probability of the exact pattern111111
(vacuum elsewhere, here there are no extra modes) is

    q(Z)=sqrt(det(I-ZZ-dagger))*|haf(Z)|^2.

The conjectured universal bound q<=1/64 is UNPROVED here. The experiment
tries to find a counterexample, not infer a theorem from local optimization.
Use complex symmetric B with21 upper-triangle complex entries, represented
by42 real coordinates in[-1,1], in lexicographic (i,j), i<=j order, real then
imaginary. The43rd parameter is radius r in[0,3]. Let alpha=tanh(r) and
Z=alpha*B/||B||op, or Z=0 when B=0. No diagonal removal, sign/phase clipping,
symmetrization or eigenvalue repair is allowed. Every evaluation checks
exact stored symmetry, norm<1, positive Q eigenvalues, Hermitian residual
<=1e-12 and determinant imaginary residual<=1e-12 with positive real part.
Q=I-ZZ-dagger. Failed physical checks stop the whole main with retained prefix.
These are floating diagnostics, not exact physical certification.

The six fixed starts use NumPy Generator(PCG64(seed)), seeds7510001 through
7510006. Each draws42 uniform[-1,1] coordinates, then one uniform[0,3] radius.
L-BFGS-B minimizes -q, with maxiter50,maxfun300,maxls20,
ftol2.220446049250313e-9,gtol1e-5,eps1e-8 and those fixed box bounds.
All finite-difference objective evaluations count against a STRICT300/start
counter checked BEFORE any additional evaluation. Its BudgetStop is expected
termination, not a retry. SciPy status0 or1 is recorded as a normal return;
any other status is an unexpected first failure. No seeds or starts are
replaced, and no optimizer/cap/tolerance retuning is permitted.

There is exactly ONE extra evaluation of a predeclared analytic three-TMSV-
pair baseline: B has off-diagonal ones at(0,1),(2,3),(4,5), all else zero;
r=atanh(1/sqrt2). Its q=1/64 is checked with absolute1e-12. It is not used
as an optimization start or solution mask. Total main evaluations are at
most1+6*300=1801, including finite-gradient calls. Every completed evaluation
streams parameters43, Z real/imag36+36, q, physical flags and diagnostics;
unexpected failed evaluations retain parameters/available Z, null q and error.
All six registered start reports remain, even after explicit cancellation.

## One exact certificate attempt after a floating violation

Only if q>1/64+1e-8, stop all optimization immediately and round every Z
real/imaginary entry ONCE to the fixed denominator10^12. The rule is exact
nearest rational to the binary float with ties to even; precision never
expands. Check exact symmetry. Form Q exactly over Q(i), using the frozen
P66.C field class ONLY (helper SHAfb3cf959...). No Perceval/native_api call.

Unpivoted Hermitian LDL elimination for dimension at most6 archives every
exact pivot and product-leading-minor, and verifies L D L-dagger=Q. Strictly
positive real pivots prove Q positive definite, hence a strict contraction;
no zero/negative pivot is silently repaired. The determinant is their exact
product. A recursive first-vertex matching sum has15 terms for haf6. Archive
rounded Z,Q, pivots/minors, determinant,hafnian and

    q_squared=det(Q)*(|haf(Z)|^2)^2.

Only a physical exact witness with q_squared>1/4096 yields
COUNTEREXAMPLE_CERTIFIED. Both probabilities are nonnegative, so squaring
is legitimate. This certifies the rounded matrix, not an interval estimate
of the floating optimum. A candidate without that exact witness remains
INCONCLUSIVE_FLOAT_CANDIDATE. Unexpected certificate exceptions are preserved
as INCONCLUSIVE_FIRST_FAILURE. There is one certificate attempt, no rerun,
precision increase, second rounding or favorable point replacement.

Record exact diagonal-zero/real/nonnegative/strict-positive-off-diagonal
membership flags. A generic complex/diagonal counterexample does NOT by
itself refute P73's loopless real nonnegative graph family or establish any
balanced-partitioning benefit. Broad/narrow claims must be kept separate.

## Outcomes and resource boundary

COUNTEREXAMPLE_CERTIFIED or NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH return
zero; the latter means ONLY no threshold violation in the registered local
search. It is never PROOF or quantum advantage. A certified hit cancels
remaining starts explicitly. An uncertified float hit or unexpected first
failure returns nonzero, preserves the full prefix/reason and cancels the
remaining registered work. Hard timeout/resource/byte interruption can
prevent summary creation; the bounded runner's status/prefix is then the
evidence. No missing evaluation is a zero and no failed retry is authorized.

One process only: CPU30s,wall60s, environment threads1, logs4MiB,
scientific files8MiB (records7MiB), combined12MiB, logical workspace128MiB,
zero failed retries. The logical plan is NOT an enforced Darwin RSS/native
import cap or CPU-affinity claim. Stream records; retain only a current
matrix, optimizer state, compact best metadata and at most one exact witness.
Native arithmetic is NumPy2.4.6/SciPy1.17.1, not Perceval or a sampling model.

CLI is pinned to persistent Python3.11.15, resolved interpreter/venv path
and explicit thread environment. Helpers remain portable for unit tests.
Record versions, actual interpreter/hash, NumPy/SciPy init-file hashes and
thread variables. These are observed files/version pins, not a complete
native/OS supply-chain certificate. All ten project input artifacts are
listed identically in both JSON contracts and hashed before/after by the
v2 runner. Original P66 field producer source is a versioned input, not a
claim to rerun any P66 grid or mutate its old evidence.

## Tiny qualification and exact commands

Nine fixtures use only modes<=2, no six-mode matrix/baseline/search/seed/RNG.
They cover zero/symmetric contraction mapping and domain rejection; the
known two-mode cross3/5 probability144/625; exact complex LDL/determinant;
exact physical witness algebra; PD-boundary/asymmetry rejection; fixed
rounding/serialization; strict budget/exclusive prefix; and CLI rejection
before any population/output. The observed tiny numeric diagnostics are
written to JUnit. They establish no six-mode result.

From this worktree, the prospective child argv are

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -x -q -p no:cacheprovider tests/test_p75b_gaussian_cf_six.py --junitxml=research/P75b_gaussian_cf_preflight/run_001/junit.xml

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P75b_gaussian_cf_six.py --output research/P75b_gaussian_cf_search/run_001/data

ROOT uses the installed computation-audit run_experiment.py, exclusive fresh
run_001 directories, every execution_artifacts path as --input and all
result paths as --result; limits --timeout60 --max-cpu-seconds30
--max-threads1 --max-output-bytes4194304. These argv are not authorization.
Validate the resulting v2 manifest against the matching producer tree;
inspect actual status and outputs before interpretation. A new analytic
proof may cancel the unexecuted main without generating numerical evidence.
