# P75c independent prospective source review

**Outcome: audited, not executed. No material static blocker found.** The
exact rational-certificate implication remains valid; the new scalar loss,
cache and budgets implement the stated finite search. This is neither a
qualification PASS nor main authorization, a universal Gaussian theorem,
an optimizer result or evidence of improved convergence.

25 November 2026. Worktree `.local/p75c-code-review`, starting at
`137f4943af9c75ba93c1f20cab9890d64c33a7ff`. Applicable AGENTS.md and the
computation/proof-audit workflow govern this static review. Only this file
is written. The old `.local/p75-code-review` unavailable index and files are
untouched. ROOT supplied exact source identifiers and review questions;
the reviewer independently checked the source and B-to-C changes, without
authoring them. This is source review, not independent discovery or execution.

No imports, AST parsing, collection, tests, RNG, numerical probabilities,
optimizer, backend, circuit, manuscript or QPU action were performed.
No C output was inspected. The B main receipt was read solely as an explicitly
declared C input for prospective change/resource provenance, not reaudited
or treated as a C result.

## Exact source and inputs

All five new files,765 lines total, were read completely at the author's
clean `51deeed2ed1a5dad8f46652be7269fa40e1d1af9` in
`.local/p75-gaussian-cf`. SHA256 values were independently checked:

| File | SHA256 |
|---|---|
| `research/P75c_gaussian_cf_six.py`,456 lines | `ea9f8c6a071ab64678501c0f2091c878b4c75346735484a36681072611b6d9c8` |
| `tests/test_p75c_gaussian_cf_six.py`,134 lines | `9a3432cfa6c658d16f9e6646f5fdf2899fcbd147ac8aea7ec9eef8f1372e7a03` |
| `research/P75c_LOG_OBJECTIVE_CONTRACT.md`,135 lines | `9cee6fe59104d873fa553ea08b6eb1ff6898e0f1be69e6d60721351e9ea7c40b` |
| `research/P75c_gaussian_cf_preflight_contract.json`,20 lines | `f9a871cb76ea69ca4fa59dcf99404b832b3a636e800f8a073e61b010f0cd689c` |
| `research/P75c_gaussian_cf_execution_contract.json`,20 lines | `aac8c52309617d24f8577d0e4b244c2911558c4440bedb62ce079c49d6a31fdb` |

The B source is unchanged at
`b86f2c69d26a3cc53d914122fac2a04e005f61141e8a4f1de8f919fdc69c09bb`.
Its receipt has SHA256
`e88cdc7052c45c0c6a1ffb8586567a33dd46ae2e4fe7cce74bdf823b30f263ef`.
The exact-field helper remains
`fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d`.
The full B-to-C source and fixture text diffs were read. No change to the
physical probability, hafnian, rational field, LDL, rounding or certificate
criterion is hidden in the new objective.

Both cards list the SAME twelve execution_artifacts in the same order:
instructions, two package inputs, P73 model, P66 field, frozen B source and
receipt, and the five new C files. The runner must hash those exact inputs
before/after. The real Markdown path is `P75c_LOG_OBJECTIVE_CONTRACT.md`;
the cards use it consistently. This review's own report is separate from
the frozen experiment input list.

## Mathematical object and exact certificate

The six-mode pure, zero-displacement Gaussian CF111111 raw probability is

    q(Z)=sqrt(det(I-Z Z^dagger))*|haf(Z)|^2,
    Z=tanh(r)B/||B||, r in[0,3], B complex symmetric.

Its43 coordinates are42 bounded real/imaginary upper-triangle components
and one radius. B=0 maps to Z=0. No diagonal removal, phase clipping or
eigenvalue repair is introduced. The full Gaussian normalization includes
vacuum and every other photon/count outcome as failures; no CF denominator
appears. The domain restriction r<=3 is material and not exhaustive of
all strict contractions.

The recursive first-partner hafnian still contains5*3*1=15 perfect-matching
terms at dimension6. The shared three-pair baseline, evaluated once only
in main, has q=[s^2(1-s^2)]^3=1/64 at s=1/sqrt(2). It is not an optimizer
start or an optimum mask. No baseline calculation was executed for this review.

Only TRUE q>1/64+1e-8 triggers a certificate. The float margin means no-hit
does not even exclude a smaller exact violation within that margin. One
fixed nearest/ties-even rounding to denominator10^12 constructs rational
Z. Exact symmetry and Q=I-Z Z^dagger are checked over Q(i). Strictly positive
real unpivoted Hermitian LDL pivots, plus exact L D L^dagger reconstruction,
prove Q>0; their product is det(Q)>0. The exact hafnian gives

    q^2=det(Q)*(|haf(Z)|^2)^2.

Because q>=0, exact q^2>1/4096 certifies q>1/64 for that rounded physical
matrix, independently of floating convergence. Nonpositive pivots or a
failed rational inequality do not certify a counterexample. There is one
certificate attempt, no adaptive precision/rounding, retry or alternate point.
Real/nonnegative/zero-diagonal membership flags remain explicit: a generic
complex witness would not automatically refute P73's narrower graph family.

## New loss and truthful final probabilities

For q above its floor, ell(q)=-log(q) is decreasing and has derivative
-1/q. This addresses the absolute raw-q gradient scale that allowed B's
documented early stops near vacuum; it does not guarantee convergence or
remove flat/singular behavior in parameter space. At q<=1e-300 the loss
is a plateau, deliberately recorded as such.

The source stores the true floating q, separate optimizer_loss and floor
flag in every successful evaluation record. `best_observed` and the float
certificate trigger compare q, never loss or exp(-loss). Thus scalar
rescaling cannot itself manufacture a physical gain or certified hit.

The per-start `current_points` dictionary keys the EXACT tuple of parameters
already used for a recorded evaluation. Its values contain actual q, loss,
global evaluation index and floor status, not matrices. It is cleared before
each seed and has at most1,200 distinct points in a start. Repeated identical
tuples may replace prior metadata with another actual observation. The
single baseline's cache entry is used before the first clear.

On a normal SciPy return, final_probability is looked up by the returned
parameter tuple. A miss is null with NO_MATCHING_EVALUATED_POINT; a match
records its real global evaluation index. There is no extra probability
call and no use of -result.fun as a probability. final_optimizer_loss stays
separate. A true below-floor q remains that q in the lookup. Tuple equality
does not supply a global or local optimum certificate.

The inverse-loss helper is NOT used by main. Off its floor boundary it
returns an approximate exp(-loss), with no certified upper bound. At the
rounded floor boundary it returns no probability and no upper bound;
neighboring true values can share a binary64 log. Invalid/nonfinite domains
are rejected. That ambiguity is correctly kept out of reported true q and
exact certification.

## Population, resources and first failures

Six FRESH seeds7511001–7511006 each use a new Generator(PCG64(seed)), drawing
42 uniform[-1,1] coordinates and then one radius uniform[0,3]. They do not
replace B starts or alter B evidence. L-BFGS-B options are explicitly fixed,
including maxiter50,maxfun1200,maxls20,gtol1e-5,eps1e-8 and the stated ftol.
Counter.reserve runs before numerical decoding/evaluation, charging finite
gradients and refusing a1,201st computed value. With baseline1, total computed
objective attempts are at most7,201. A denied BudgetStop call does no further
scientific evaluation and is planned termination, not a retry.

The inherited finally updates the current start count even when a float
candidate propagates outward. Its record retains true q and matrix; one
certificate follows and every remaining start is explicitly canceled.
Statuses0/1 are ordinary optimizer returns, other statuses a first failure.
Normal completion reconstructs the total count. Physical invariant failures,
unexpected errors and incomplete work are not silently filled with zeros.

Records stream/flush, with a31MiB record cap; summary/certificate/failure
files share a32MiB child-science cap. Only cache metadata, one current matrix
and at most one witness are retained. NaN serialization and byte interruptions
can leave only a prefix; the actual runner status/logs then control the
interpretation, not a missing or stale summary. Exclusive creation prevents
reuse of earlier result directories or files.

The separate wall60s, per-process CPU30s, log4MiB, one worker and conventional
thread variables1 need the actual runner flags; the script's JSON is not
enforcement. Science+logs give the declared36MiB boundary. Logical128MiB
is a workspace PLAN, not a Darwin RSS/native-import/address-space or affinity
cap. Environment variables do not prove actual native thread activity.

The increase to1,200/start and31/32MiB was frozen prospectively for C,
using B receipt's1,033 records,3,272,101 record bytes,0.79351 body CPU seconds
and1.227817 runner seconds as rationale. These observations motivate but
do not guarantee C resource use. No C canary, search, import or calibration
was consulted. C is a different registered experiment, not a retelling or
repair of the B result.

CLI path/prefix/Python3.11.15 and thread checks precede output/population;
helpers remain portable. Exact NumPy/SciPy versions are checked before
scientific loading. The recorded interpreter and package init-file hashes
are useful observations, not complete BLAS/OS supply-chain authentication.
P66 native_api and historical grids are never called.

## Qualification coverage and remaining checks

All eleven fixture functions were read. They preserve the nine B hand cases
and add log(625/144) for q=144/625, nonfloor approximate inversion, the
zero/below-floor ambiguity and invalid-domain rejection. They construct
only literal n<=2 matrices and scalar tests, no six-mode matrix/baseline,
RNG or optimizer. The CLI monkeypatch concerns infrastructure, not physics.
The proposed tiny JUnit observation is not already observed evidence.

The fixtures do not run the full minimize/cache/report path, finite-difference
termination or a six-mode certificate. Those paths were checked statically
here. No extra fixture is requested merely to mirror the source. An actual
certified hit should still receive an independently coded rational witness
reconstruction before acceptance. A no-hit main would establish only its
registered finite observation, even if all optimizer returns report success.

| Obligation | Static result |
|---|---|
| Complete five-file/hash and B-to-C change review | Passed |
| Physical q,15-term hafnian and exact PD/q-squared implication | Passed; no execution |
| Loss floor, inverse ambiguity and true-q trigger/best fields | Passed |
| Actual-point cache and no unbudgeted final evaluation | Passed |
| Seeds, strict counts, first failures/cancellation and byte boundaries | Passed as prospective source logic |
| Eleven tiny fixtures and identical twelve-file input closure | Reviewed, not collected or run |
| Actual C qualification, limits, manifests and main outcomes | Pending |
| Universal cap, new optimizing point, graph benefit, hardware or novelty | Not established |

No material static gap remains in the stated prospective finite assertion.
If the route is not resolved analytically first, ROOT may separately decide
on one tiny qualification, inspect its real status/JUnit/input hashes, then
separately consider one bounded main. This report authorizes neither.
Git/text integrity checks accompany its freeze; all author and B evidence
remain untouched.
