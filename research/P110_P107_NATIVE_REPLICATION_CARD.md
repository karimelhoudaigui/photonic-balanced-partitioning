# P110: independent native replication of one finite P107 filter law

26 November 2026. **DESIGN ONLY; NOT EXECUTED; no implementation authorized
by this card.** One fixed algebraic-extension point, no graph optimization.
The source/schema freeze precedes code; sealed P107 inputs precede raw reading.
The computation-audit workflow is reused. No scientific import, AST, evaluation,
test, RNG, native call, raw-data read, runner, QPU, manuscript edit or push occurs.

## Finite assertion and scope

For x=1/2,y=1/4, independently construct the P101 passive filter dilation;
query deterministic Perceval Naive amplitudes for EVERY four-photon output;
sum their probabilities over dump occupations; compare EVERY signal bin with
independently evaluated exact P107 polynomials. Agreement is finite evidence
conditional on the pinned native stack and stated tolerance, not a proof of
all x,y, the physical b1 curve, optimization benefit or hardware capability.
This point is NOT on y=x^(2+sqrt(3)); it supplies no b1 sign or cooling result.

Theory input: P101 research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md,113 lines,
commit69e4a6fe434a677acfc5a7e616471990b16db86b, SHA256
65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c.
Its equations(3),(6) were read; our independent review remains unchanged.
P96 source0eabdadc70c2b7085c40b22183320e8655d00e1d was read as an API/
failure-recording pattern only; no P96 production import or matrix reuse.

## Independent construction and complete population

Indices j,r=0,1,2,3. Define F_jr=(-i)^(jr)/2 using the literal four-cycle
1,-i,-1,i, not trigonometric phase evaluation. Set

    d=(1,1/2,1/8,1/4), e=(0,sqrt(3)/2,sqrt(63)/8,sqrt(15)/4),
    T_jk=sum_r F_jr d_r conjugate(F_kr),
    E_jk=sum_r F_jr e_r conjugate(F_kr), U=[[T,E],[E,-T]].

Use scalar stdlib loops and explicit complex arithmetic; no eigensolver,
exponential, fitting, gauge search, graph loading or production matrix helper.
T can also be retained as exact Gaussian rationals before float conversion;
the only algebraic-to-float square roots are the displayed e. NumPy is used
only for the matrix interoperability needed by Perceval, not a reference law.
Rows are output ports, columns input ports. Ports0..3 are signal,4..7 dump.
Input is exactly |1,1,1,1,0,0,0,0>; no source randomness or loss conditioning.

Archive d,e,F,T,E,U before checking their values. Check finiteness,
Hermiticity of T,E, T^2+E^2=I, TE=ET, and full U†U=UU†=I.
Archive observed complex Gram/residual entries before rejecting them.
Naive uses this fixed8-mode unitary and that fixed normalized CF input.
Its returned Fock amplitude already includes output occupation factorials;
never multiply/divide its probability by another bunching factor.

Enumerate lexicographically ALL n in Z_>=0^8 with sum n=4: C(11,4)=330.
No threshold, probability cutoff, favorable-bin selection or native fallback.
Each occupation gets one amplitude query, at most330 calls, no duplicate retry.
Preserve native zeros, tiny positives, collision/loss outputs and amplitude phase.
Sum |amplitude|^2 by the first four occupations. ALL signal tuples s with
sum s<=4 must appear: sum_(r=0..4)C(r+3,3)=70, including vacuum and zeros.
Missing count ell=4-sum s is a total, not a resolved-dump reference prediction.
Archive the330-to70 index grouping and all aggregate values, not just maxima.

## Reference binding and comparison

P107 is an OPAQUE future input until ROOT seals its six raw files and supplies
their explicit paths, original seal commit, Git blob identities and SHA256s.
Do not open those raw contents while authoring/freezing this implementation.
The final frozen source/spec define the actual coefficient schema; no record
layout, producer SHA, active binding or command is guessed in this card.
After that source/schema freeze, write independent scalar Fraction evaluation
at(1/2,1/4), without importing P107 or copying its coefficient/matrix generator.
The evaluator must reject duplicate/missing occupations or powers, malformed
exact denominators/components and an unexpected complete reference population.
All explicit zero and negative polynomial coefficients remain evidence;
only the evaluated physical B probabilities must be real, nonnegative and sum1.
The B_moment/D columns, if present, are not substituted for the designated B law.

For every bin, compare the observed signal marginal against the exact rational
B value converted once for reporting. Use the fixed rule
abs(observed-reference)<=2e-12+1e-10*abs(reference), with no clipping,
renormalization, adaptive tolerance, repaired native zeros or discarded bins.
Use the same absolute-plus-relative rule against the identity for matrix
entries and against1 for total native probability and total marginal mass.
All70 comparisons and both masses must pass; archive each observed/reference/
error/tolerance and the exact rational reference before asserting completion.
This does not independently certify each complex amplitude; a330-amplitude
permanent oracle is intentionally outside this bounded replication.

## Provenance, resource and failure policy

Before numerical/native imports, set OMP_NUM_THREADS, OPENBLAS_NUM_THREADS,
MKL_NUM_THREADS, VECLIB_MAXIMUM_THREADS, NUMEXPR_NUM_THREADS and BLIS_NUM_THREADS
to1 and record their dictionary; explicitly set xq native configuration1.
Pin Python/interpreter, Perceval, Exqalibur, NumPy, relevant installed source
and extension files by actual version/path/hash in the future frozen contract.
Require persistent project Python for main; portable pure fixtures use their
executing interpreter. Launch with -B and PYTHONDONTWRITEBYTECODE=1.
Do not guess installed pins or install dependencies.
Record actual xq configuration and environment before/after each native call
and at final readback. These observations do not claim OS-thread enforcement.
Any unexpected configuration is a preserved first failure, not an automatic fix.

Before conversion or a finally/guard can throw, retain the returned amplitude
repr, its occupation/index, attempted-call counter and raw thread observations.
Emit strict-JSON diagnostic representations of NaN/Inf or exceptions before
the finite guard; nonfinite values cannot become a passing scientific number.
The same record-before-rejection rule applies to matrices, spectra/configuration,
versions and construction failure context. Never let a post-call thread failure
erase an already returned amplitude; store null for unobserved fields, not0.
Stop on the FIRST failure, preserve its prefix, leave later queries NOT_RUN,
and retain warnings/stdout/stderr. A partial population cannot be called PASS.

Prospective caps, not calibrated: one worker, CPU60s, wall90s, numerical/native
thread1; at most330 amplitude calls, RNG0, retry0. Runner combined logs4MiB.
Set RLIMIT_FSIZE8MiB before numerical imports; additionally enforce a combined
8MiB uncompressed scientific-output budget with64KiB reserved for final failure/
summary records. FSIZE alone is per-file, not that combined-byte enforcement.
Stream records and check bytes before writing; no compression or hidden copies.
Only the active contract may authorize a fresh output parent
experiments/P110_native_filter_main/run_001, with every declared result below it.
No measured runtime, RSS/bit-complexity claim or optical resource equivalence.

The future v2 contract must close over this card, P101, frozen P107 source/spec,
the six ROOT-sealed reference files plus their provenance manifest if separate,
new source/tests/spec/contracts, binding, AGENTS, dependency lock/project files,
and actual external pins. A TEMPLATE is not an active authorization or evidence.
Freeze code, exact argv, closure and any tiny pure/mocked qualification population
before imports/tests; ROOT and independent review precede separate run authority.
There is no extra native HOM/canary population silently added to330.

## Outcomes and current blocking condition

Complete330/70, invariant checks and all comparisons passing may yield
FINITE_NATIVE_REPLICATION_PASS, positive_accepted=false. A finite discrepancy
is retained for diagnosis of reference/construction/native/model conventions;
it is not by itself a universal theorem counterexample. Resource exhaustion,
missing observations/pins or first failure yield INCONCLUSIVE_FIRST_FAILURE.
Raw output must be committed before interpretation; receipt is a separate commit.
Currently BLOCKED BEFORE CODE by the unfrozen P107 source/schema. The later
ROOT raw binding gates raw reading/execution, not code authoring. No active
command, execution evidence or hardware bundle exists.
