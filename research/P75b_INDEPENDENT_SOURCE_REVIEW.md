# P75b independent prospective source and certificate review

**Mathematical verdict: proved as written for the exact certificate
implication below. Computation outcome: audited, not executed.** No material
static blocker was found in the proposed bounded search. Qualification,
observed resource use and the main remain pending separate ROOT decisions;
this report authorizes none of them. It does not prove the conjectured
universal Gaussian bound.

Review date: 25 November 2026. Worktree `.local/p75-code-review`, starting
at `8e330e54c872da4ce8e923c8e8ab7599918b9db5`. The applicable AGENTS.md,
computation-audit checklist/runner and proof-audit obligations were read.
Only this report is written. The review uses source text, Git metadata,
SHA256 checks and hand algebra. No source import, AST parse, collection,
test, RNG evaluation, matrix/probability calculation, optimization,
native backend, graph draw, output inspection or QPU call was performed.

## Exact frozen artifacts and independence

All five prospective files were read completely in the author's clean
`.local/p75-gaussian-cf` worktree at
`5b2b52d3c12523f413f694fa250a40a8bf894747`. The independently recomputed
SHA256 values are:

| Artifact | SHA256 |
|---|---|
| `research/P75b_gaussian_cf_six.py`,419 lines | `b86f2c69d26a3cc53d914122fac2a04e005f61141e8a4f1de8f919fdc69c09bb` |
| `tests/test_p75b_gaussian_cf_six.py`,107 lines | `19e14762858c02e39448a48a17ba3ea74ce44af36cabf4a08a74b72e9893b40b` |
| `research/P75b_GAUSSIAN_CF_SIX_CONTRACT.md`,146 lines | `4e47b8fab3ad46fdc958e2a5f77bd5c3dfc0a1992d88fa74dfc2077cc975d188` |
| `research/P75b_gaussian_cf_preflight_contract.json` | `d6ba600b78aa0544e8159ea16dbc51e4b8d31108a08a0942bd4a59d7925b19fc` |
| `research/P75b_gaussian_cf_execution_contract.json` | `a9992db697c46689ed524bebbf4203fed5dafb88428589cf5bd7ac59320bed9f` |

The reused field source `research/P66_exact_finite_check.py` matches
`fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d`.
Its complete exact C class and import/entrypoint boundary were read. P75b
hashes that helper before loading C; it never calls `native_api()` or a P66
population. This is evolved development source, not a claim to regenerate
the archived P66 v1 grid.

The reviewer did not author these files and uses a separate worktree.
ROOT supplied the proposed claim, exact source identifiers and review
questions. The author's contract and intended outcomes were visible.
This is independent static reconstruction of the implemented implications,
not blind discovery, independent execution or physical replication. No
scientific outputs were consulted.

## Claim card and dependency graph

The numerical search examines complex symmetric six-by-six matrices
Z=tanh(r) B/||B||, B drawn/optimized in the specified bounded coordinates,
0<=r<=3; B=0 maps to Z=0. For the pure zero-displacement Gaussian source,
the exact all-ones raw probability is

    q(Z)=sqrt(det(I-Z Z^dagger))*|haf(Z)|^2.

No successful-shot denominator is present. Vacuum, other photon totals and
all other outcomes remain outside this one event's probability. The source
must be normalized and strictly contractive. This is a mathematical active
Gaussian model, not a claimed available hardware source.

The assertion to be searched is a violation of the UNPROVED cap q<=1/64.
Six local L-BFGS-B starts do not exhaust this continuous domain; r<=3 also
excludes a neighborhood of the contraction boundary. No-hit supports only
the registered local-search statement, never that cap or a graph optimizer.

The dependency chain is:

    symmetric bounded coordinates -> strict floating contraction diagnostics
    normalized Gaussian CF coefficient -> numerical q and threshold screen
    recursive matching sum -> six-mode hafnian
    one fixed rounding -> rational symmetric Z in Q(i)
    exact Hermitian LDL/reconstruction -> Q positive definite and det(Q)>0
    exact hafnian -> exact q^2=det(Q)(|haf Z|^2)^2
    exact q^2>1/4096 -> physical rounded counterexample q>1/64.

The exact certificate implication is the proved component. Its premise is
the recorded rational matrix and positive LDL pivots, not the optimizer's
score or convergence status. The numerical population has not been run.

## Normalization and independently reconstructed small cases

For the unnormalized pair exponential, the coefficient of one creation
operator in every occupied mode sums one product per perfect matching.
Pair orientations cancel the quadratic factor1/2, and exponential ordering
cancels its factorial. The CF amplitude is therefore haf(Z). The Bargmann
norm integral is a real positive Gaussian integral: completing its real
quadratic form, or unitary diagonalization of a symmetric pair matrix,
gives norm squared det(I-Z Z^dagger)^(-1/2). The normalized amplitude
prefactor is its inverse square root, so the raw probability has the
SQUARE-ROOT determinant shown above. P73's determinant for TWO independent
colors must not replace it.

The recursion in lines77–87 chooses the partner j of vertex0, then recurses
on the remaining vertices. Every matching has one unique such j. Six
vertices give5*3*1=15 distinct terms, four give3, two give1 and the empty
hafnian is1. Diagonal entries do not enter this CF coefficient, but remain
in Q and the state normalization.

For Z=[[0,s],[s,0]], q=(1-s^2)s^2. At s=3/5 this is144/625;
det(Q)=256/625 and q^2=20736/390625. The proposed tiny fixtures contain
those independent hand-computable values. For the three disjoint pairs
with s=1/sqrt(2), six-mode haf(Z)=s^3 and
q=(1-s^2)^3 s^6=(1/4)^3=1/64. This derives the baseline without executing
it. It is three two-mode pairs on six modes, not six pairs.

The complex Hermitian LDL fixture [[1,i],[-i,2]] has pivots1,1,
lower entry -i and determinant1. This checks the conjugation direction;
the main code uses lower[j,k]*conj(lower[i,k]) in elimination and
lower[i,k]*d[k]*conj(lower[j,k]) in reconstruction, as required.

## Exact rational witness

`rounded_witness` rounds the REAL and IMAGINARY binary-float components
once to denominator10^12. Fraction.from_float preserves the binary input
exactly; round(Fraction) implements nearest integer with ties to even.
The two copied symmetric entries have identical floats and hence identical
roundings. No adaptive precision, alternative point or second rounding
is attempted.

`exact_witness` independently checks exact symmetry, constructs every Q
entry as delta_ij-sum_k Z_ik conjugate(Z_jk), and calls unpivoted Hermitian
LDL in dimension at most6. It verifies Hermitian equality before division.
Every pivot must be real and strictly positive. A nonpositive pivot returns
nonphysical; it is not repaired. For positive pivots the full reconstruction
L D L^dagger=Q is verified entrywise. Thus Q is positive definite and
||Z||<1, and its determinant is exactly the product of those pivots.
All leading-minor products and pivots are returned, with Q and Z. L itself
is not serialized but is exactly reconstructible from Q; the contract asks
for pivots/minors and the reconstruction check, not an archived L matrix.

The hafnian uses the same recursively defined matching polynomial over
the exact Fraction-pair field. The field's addition, multiplication,
conjugation, norm squared and division preserve Q(i), without a binary64
coercion. Let d=det(Q)>0 and h=|haf(Z)|^2>=0. Then q^2=d*h^2. Since q
is nonnegative, d*h^2>1/4096 is equivalent to q>1/64. This validates
certification of the ROUNDED matrix even if a floating candidate were
inaccurate. A failed PD or rational inequality cannot certify a hit.

Exact diagonal-zero, real, nonnegative and strictly positive off-diagonal
membership flags are recorded separately. A generic complex/diagonal
counterexample would not establish a counterexample in P73's real,
nonnegative, zero-diagonal graph family. Nor would either result demonstrate
any balanced-partitioning advantage.

## Population, limits and failure paths

The coordinates are21 upper-triangle complex entries plus one radius,
43 real parameters. The loops use real/imaginary order for each i<=j.
The NumPy start draws use a fresh Generator(PCG64(seed)) for each of the
six declared seeds7510001–7510006:42 uniform[-1,1] coordinates, then one
radius uniform[0,3]. The fixed baseline is evaluated once separately and
is not an optimization start.

SciPy's maxfun may be soft during finite differencing, so the independent
Counter guard is necessary. It reserves before decoding or objective
evaluation and raises BudgetStop before any301st evaluation in a start.
All finite-difference calls use that wrapper. Thus at most1+6*300=1801
objective attempts occur. A failed physical evaluation is charged and its
parameters, available matrix, diagnostics and null q are retained.
BudgetStop is a planned termination, not a retry. SciPy statuses0/1 are
ordinary returns; other statuses abort the remaining population.

A FloatCandidate propagates through the inner finally, updating the
current report's evaluation count, then stops the optimization and attempts
one certificate. Remaining starts are explicitly canceled in summary.
All six start records remain. Certificate exceptions are distinguished
from an uncertified candidate. Normal completion reconciles the global
counter against the baseline and per-start counts. Partial failures do
not silently fill omitted evaluations with zero.

Records stream to an exclusive new binary file and are flushed each time;
only compact best metadata and one current/candidate matrix are retained.
Seven MiB bounds evaluation records, and eight MiB bounds those records
plus summary/certificate/failure files. Encoding rejects NaN. A byte-cap
exception or failed final serialization can leave only a prefix; it must
be interpreted with the bounded runner's actual status and logs, not as
a no-counterexample result. Existing directories/files are never reused.

The contracts separately request CPU30s, wall60s, one worker, conventional
thread variables1, log4MiB and zero failed retries. The runner must actually
receive those flags and the ten identical execution_artifacts paths.
It enforces wall/log and supported per-process CPU caps; the script enforces
scientific bytes and reserves. The128MiB logical workspace is a PLAN,
not a Darwin hard RSS/address-space/native-import cap or CPU affinity proof.
Environment thread settings alone do not prove actual native thread counts.

CLI checks the contracted resolved interpreter, prefix, Python3.11.15 and
all five thread variables before `run` creates output. Library helpers
remain portable for tests. The NumPy/SciPy versions are checked before
scientific loading. Actual interpreter hash and package init-file hashes
are recorded; this is not complete authentication of every native library.

## Qualification coverage and residual risks

All nine test functions were read. They use literal dimensions at most2,
no RNG, six-mode baseline or search, and test real/complex hand cases,
domain rejection, PD boundaries, exact serialization, counter/exclusive
prefix behavior and rejected CLI execution before output. The monkeypatch
in the last test concerns the infrastructure guard, not a physical law.
Observed tiny q diagnostics would be archived in JUnit.

The fixtures do NOT exercise the recursive branching for dimensions4/6,
the full optimizer, FloatCandidate propagation, main summary serialization
or an actual six-mode certificate. The hafnian branching and control-flow
checks here are static hand reconstruction. Adding a fixed proved n4
recursion fixture is an optional prospective improvement requiring a new
contract because this one explicitly limits qualification to n<=2. It is
not reported as a test already passed or a material blocker after the
complete recursion audit. A claimed certified hit should receive a second
independent rational reconstruction from its serialized Z before acceptance.

The coverage is a bounded, possibly truncated local countersearch. It has
no global optimum guarantee, contraction-boundary coverage, interval
certificate of a floating maximum, physical sampling or quantum advantage
interpretation. A prior analytic theorem may make the entire unexecuted
main unnecessary. Its cancellation would be a mathematical resolution,
not measured negative data.

## Obligation matrix and safe next step

| Obligation | Static review |
|---|---|
| All five exact frozen files and reused field hash | Passed by full text/hash reads |
| Single-source determinant exponent and CF hafnian | Passed by coefficient/norm derivation |
| Fifteen-term haf6 recursion and tiny hand values | Passed analytically; not executed |
| One fixed rounding and exact physical q-squared witness | Certificate implication proved |
| Counter, finite gradients, seeds and max1801 attempts | Passed by call-path inspection |
| Failed-prefix, first-hit and explicit canceled starts | Passed subject to runner/serialization status |
| Scientific bytes versus external CPU/wall/log caps | Separated; actual enforcement remains unobserved |
| Nine tiny fixtures and planned commands | Reviewed, not collected or run |
| Main, finite result, package runtime and manifests | Pending, no evidence invented |
| Universal bound, P73 graph subclass, optimizer/QPU/novelty | Not established |

No remaining material static gap was found in the stated prospective
finite assertion or the exact certificate implication. The cheapest next
check, if no analytic resolution supersedes it, is the separately authorized
tiny qualification with exact input hashes and actual JUnit bytes/status
inspected. Only ROOT can subsequently consider one bounded main. A zero
runner exit would still need result interpretation; no-hit is never a proof.

Whitespace/Git integrity checks accompany this report's freeze. The source,
fixtures and contracts remain unchanged. No execution is authorized or
claimed by this independent review.
