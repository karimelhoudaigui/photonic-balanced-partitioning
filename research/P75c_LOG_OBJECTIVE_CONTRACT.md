# P75c prospective six-mode log-objective continuation

25-Nov-2026. **CODE ONLY — NOT EXECUTED.** No import, AST, collection, test,
RNG, objective, baseline, optimizer or certificate was evaluated during
preparation. ROOT must read/freeze these FIVE NEW files, authorize a separate
tiny qualification and independently consider a single main. The current
ROOT numerical slot is not used by this code-only work.

## Why this is a new registered experiment

P75b remains immutable: producer00256fc2, raw4a5254ce, main receipt4eb9e9cf,
sourceb86f2c69 and record hash7b6dfa4a. It recorded1,033 evaluations with
no counterexample. Three starts terminated at iteration0 after44 evaluations
on the absolute projected-gradient criterion; their initial raw probabilities
were tiny. The best was only the analytic three-pair baseline. That result
is weak and is NOT a proof, and it is not being relabeled or repaired.

This new continuation changes the specific failed numerical step:

    old objective=-true_q,
    NEW objective=-log(max(true_q,1e-300)).

The physical model, raw probability, comparison threshold and exact witness
are unchanged. All P75b files/results/statuses remain untouched. Six FRESH
seeds7511001..7511006 replace none of the old starts; they define a separate
experiment. Each now has a strict1,200 computed-objective limit, including
finite gradients, plus one shared analytic baseline, at most7,201 total.
Maxiter50,maxls20,gtol1e-5,eps1e-8,ftol2.220446049250313e-9 remain fixed;
maxfun is prospectively1,200. All SciPy statuses/first-failure rules remain
as in the frozen P75b source, including stopping on unexpected status.

The resource change was made BEFORE any C execution: P75b observed1.227817s
runner elapsed,0.79351s body CPU and3,272,101 record bytes for1,033 values,
roughly3,168bytes/value. This motivates, without guaranteeing, the fixed C
record31MiB/scientific32MiB caps for7,201 values plus extra loss fields. Logs
remain4MiB, combined36MiB, logical workspace128MiB, CPU30s,wall60s, thread1,
zero failed retries. No C canary or calibration was run to choose these caps.

## Unchanged mathematical target and raw source

Z is a complex symmetric six-mode contraction, constructed from42 bounded
real/imaginary upper-triangle coordinates B and one radius r in[0,3]:
Z=tanh(r)*B/||B||op, with B0 mapped to Z0. Its exact pure zero-displacement
Gaussian CF111111 probability is

    true_q=sqrt(det(I-ZZdagger))*|haf(Z)|^2.

The conjecture true_q<=1/64 remains UNPROVED here. This is not balanced-graph
optimizer training or a novelty claim. The physical family includes complex
diagonals; a generic witness does not automatically refute P73's narrower
loopless real nonnegative graph class. Every vacuum/other-count outcome stays
outside the raw target event without CF renormalization. No Perceval/QPU.

Main start generation remains a fresh Generator(PCG64(seed)):42 uniform[-1,1]
coordinates, then radius uniform[0,3]. No seed is evaluated before main.
The one analytic three-disjoint-TMSV pair baseline q=1/64 is evaluated once,
checked at abs1e-12 and is NOT an optimizer start. It uses the same six-mode
baseline definition as P75b and supplies no graph optimum/mask.

## Loss accounting and final-result correctness

Every streamed evaluation retains the TRUE floating q, physical flags,
parameters43, both6x6 matrix parts and diagnostics. It additionally records
optimizer_loss=-log(max(q,1e-300)) and whether q<=the floor. Best-observed
comparisons and the float trigger always use true_q, never the log loss.
The floor prevents log0; it does not turn a floor value into a counterexample.

Most importantly final_probability is NEVER -result.fun: that field is now
an actual-q lookup from previously evaluated parameters. A per-start cache
retains at most1,200 parameter tuples plus q/loss/index metadata, then clears
before the next seed. It stores no trajectory of matrices. If returned x
has no exact tuple match, final_probability=null with an explicit status;
no extra probability evaluation is performed. final_optimizer_loss is stored
separately. This lookup also preserves a true below-floor q rather than
inventing1e-300.

The inverse-loss helper is diagnostic only. Away from its floor boundary it
reconstructs an approximate exp(-loss). At the boundary it returns no q and
NO certified probability upper bound, because a binary64 log loses information
and may round neighboring values together. The main does not use that inverse
for its reported true probability or certificate.

## Unchanged physical and exact-certificate conditions

No clipping, sign change, eigenvalue/symmetry repair or favorable point
replacement is introduced. Numerical invariants remain symmetric stored Z,
strict contraction, positive Q eigenvalues, Hermitian residual<=1e-12,
positive real determinant with imag residual<=1e-12. All calls are counted
before numerical work; expected BudgetStop refuses a further evaluation.

Only true_q>1/64+1e-8 stops optimization for ONE fixed-denominator10^12
nearest/ties-even rational rounding. The frozen P66.C helperfb3cf959 is
used only as an exact field, never native_api. Exact Hermitian LDL pivots/
leading minors and reconstruction certify Q>0; the15-term hafnian gives

    q_squared=det(Q)*(|haf(Z)|^2)^2 >1/4096.

Only that exact physical witness is COUNTEREXAMPLE_CERTIFIED. Failed/absent
certification is inconclusive, with no precision increase, second rounding,
extra start or retry. Full exact rational data and narrow-class flags are
retained. No hit is NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH, never PROOF.
Unexpected first failure stops/cancels remaining work; hard limits can leave
only a failure prefix/runner manifest. No missing row is zero.

## Tiny qualification, input closure and commands

ELEVEN fixture functions contain only literal dimensions<=2, scalar log/floor
checks and infrastructure checks. They preserve all nine B fixtures and add
hand-derived q144/625 to log(625/144), nonfloor inverse, floor behavior and
invalid inverse-domain checks. They do NOT construct a six-mode matrix,
analytic baseline, RNG, source-population or optimizer. The tiny numeric
observation is retained in JUnit. Helpers are portable; scientific CLI remains
strict on persistent Python3.11.15/actual venv path and thread environment.

The twelve project inputs include instructions/packages/model, frozen P66
field, original P75b source and main receipt for change/resource provenance,
and the five NEW files. Both JSON lists are identical. Source cloning did
not modify the old source/fixtures/cards/data. Package versions remain
NumPy2.4.6,SciPy1.17.1,pytest8.4.2. Observed init-file/interpreter hashes do
not authenticate all BLAS/OS libraries; logical memory is not hard RSS/affinity.

Prospective child argv, not authorization:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -x -q -p no:cacheprovider tests/test_p75c_gaussian_cf_six.py --junitxml=research/P75c_gaussian_cf_preflight/run_001/junit.xml

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P75c_gaussian_cf_six.py --output research/P75c_gaussian_cf_search/run_001/data

Use installed computation-audit run_experiment.py with the matching root and
JSON, every execution_artifacts entry repeated as --input and all declared
results as --result. Fresh run_001 only; --timeout60 --max-cpu-seconds30
--max-threads1 --max-output-bytes4194304. No hard-AS/affinity claim. Seal raw
outputs before interpretation; validate the v2 record against its producer
tree. Qualification/main require separate ROOT decisions, and an analytic
resolution may cancel main before execution. No advantage or device claim
follows from improved objective scaling alone.
