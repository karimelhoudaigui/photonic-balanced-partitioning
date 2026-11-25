# P66 prospective exact finite diagnostic

Status: **CODE ONLY — NOT EXECUTED**. Source and contract must be frozen and read in full by ROOT before one separately authorized qualification, then one separately authorized main in an exclusive numerical slot. No import, AST parse, collection, test, scientific calculation, backend query or data inspection was performed while preparing these files. The computation-audit skill was applied.

This checks finite implementation conventions of the proof in theory/P66_independent_bright_dark_audit.md, including its connected extension. That proof and research/P67_exact_covariance_symmetry_obstruction.md were read completely. The computation does not prove the universal theorem, the P67 general covariance extension, novelty, or any positive optimization result.

## Frozen assertion and coverage

Use $L=2,3$, $N=4L$, $K=2L$, heavy clique weight $M=3$ and matching weight $h=1$. Vertices, in order, are $A_1,A_2,B_1,B_2$, each with $L$ vertices. Match equal offsets between $A_1,A_2$ and between $B_1,B_2$. The two families have cross-block weight $w=0$ or $w=1/(2L)$. The latter connects every vertex of $C_A=A_1\cup A_2$ to every vertex of $C_B=B_1\cup B_2$.

All adjacency and matrix entries remain exact in $\mathbb Q(i)$. For every family and $L$, form

\[
D=\max_i\sum_j A_{ij}+\lambda(N-1),\qquad
H=(A+\lambda(J-I))/D,\qquad
U=(I+itH)(I-itH)^{-1}.
\]

Use precisely $t=(0,1/4,1,2)$ and $\lambda=(0,1/4)$, in that order: **32 matrices**. Gauss--Jordan inversion has first-nonzero pivoting, maximum dimension 12; it uses no floating approximation, Sympy, NumPy, production helper or special graph spectral formula. Check both inverse identities, $U^\dagger U=I$, symmetry, commutation with both block dark projectors, and uniform cross blocks of rank **at most** one (zero coupling at $t=0$ is allowed). Weighted normalization is checked against the explicit regular degree.

For every matrix, keep all four bad sources $A_a\cup B_b$, $a,b\in\{1,2\}$, and both targets $C_A,C_B$, without symmetry reduction: **256 bosonic points**, **256 distinguishable points** and **128 two-target unions**. Rows are output modes and columns input modes. A Gray-code Ryser implementation computes each exact complex permanent for $K\leq6$; its modulus squared is the raw bosonic collision-free probability. The same routine over the exact entrywise squared moduli computes the distinguishable probability. Every main source and target has occupations zero or one, so both Fock factorial products are one. A separate generic normalized-Fock helper is exercised only by tiny collided fixtures.

The exact point and union assertions are

\[
a_L=\frac{L!}{(2L)^L},\quad
b_L=\min\!\left(1,\frac{L+1}{2}\left(\frac{L+1}{2L}\right)^L\right),\quad
P_B(T\mid S)\le a_Lb_L,\quad
\sum_{T=C_A,C_B}P_B(T\mid S)\le\min(1,2a_Lb_L),
\]

and $P_D(T\mid S)\le(2L)^{-L}$, with union at most $\min(1,2(2L)^{-L})$. All collisions remain outside these raw target events: there is no collision-free postselection denominator and no inferred B-versus-D ordering.

Enumerate **every** balanced subset, including complements, for both families: $2(\binom84+\binom{12}6)=1\,988$ exact scalar costs. The two good unions must cost $4wL^2$, four bad unions $2L+2wL^2$, and every partial-clique subset at least the latter plus $g=6(L-1)-2L>0$. These checks do not sample or search for favorable graphs.

For each $L=2,\ldots,8$, expand the complete one-bright-mode PGFs of a full $d=2L$ target and an $L$-occupied source:

\[
F_{d,k}(z)=\sum_{m=0}^{k}\frac{(k)_m}{d^m}(z-1)^m.
\]

Archive both rational coefficient vectors. Check nonnegativity, mass one, target mean one, target tail $\Pr(n\ge L)\le b_L$, and source all-bright mass $L!/(2L)^L$. This finite single-mode law is not a complete multimode PNR enumeration or an assumed exact thermal law.

## Separate numerical point reference

Only $t=1,\lambda=1/4$, both $L$ values and both graph families, are sent to local NaiveBackend.prob_amplitude: all eight source/target combinations per case, **32 predetermined points**. No random seed, sample, Processor, remote operation or full output law is used. The exact rational matrix is converted entrywise to binary64 complex; Perceval 1.3.0 / Exqalibur 1.4.2 computes the independent native permanent amplitude, including both Fock factorials.

Compare probabilities using exactly

    abs(p_native - float(p_exact)) <= 1e-12 + 1e-7*max(p_native,float(p_exact)).

Archive the exact probability, native complex amplitude and probability, both errors, tolerance and whether its absolute or relative term dominates. Archive every zero, tiny positive and other positive point; none is filtered or replaced. Absolute-dominated agreement certifies no relative precision. This reference is numerical and tolerance conditional, not an interval proof or independent physical experiment.

The persistent interpreter is /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python, Python 3.11.15. The loader checks actual virtual-environment prefix, interpreter path and pinned NumPy/SciPy/Perceval/Exqalibur versions, imports Exqalibur first, sets and reads Config.compute_max_thread_count=1, then imports Perceval and reads it again. Each point and the end read back one native thread. Loaded module file paths/hashes and interpreter path/hash are archived before queries; these observed module files are rehashed after queries. This supplements the runner's project-file closure; it does not authenticate all OS libraries, install provenance or unloaded package files.

## Qualification boundary

The nine fixture functions contain only explicit matrices of dimension at most four, exact field/inverse/product/permanent tests, a permutation-sum reference for a fixed 4-by-4 matrix, both normalized Fock factorials on a rational 2-by-2 splitter, the $d=2$ bright PGF, a four-mode scalar cut/dark projector, serialization/exclusive-output checks, and five fixed native two-mode/two-photon HOM probabilities. The native inputs are $(1,1)$ and $(2,0)$; the five queries and numerical observations are retained in JUnit properties. No fixture invokes the P66 family generator, population iterator, $K=4/6$ probability, main matrix grid, graph draw or random draw. A qualification PASS authorizes no main automatically.

## Resources, outputs and failure interpretation

For each authorized process: **CPU 60 s, wall 90 s, one worker, environment and native thread count one, logs 4 MiB, scientific files 28 MiB, combined 32 MiB, logical workspace plan 256 MiB, zero failed retries**. The logical plan is not a hard Darwin RSS cap or a claim that native imports occupy less than 256 MiB. Fixed loops and dimensions bound logical arrays; records stream to disk. No cost calibration, canary, scope reduction, cap increase or replacement point is permitted after starting.

Use bytecode-disabled Python and disable pytest's cache provider. Output directories must be fresh. Main creates exactly records.jsonl, failure.json, summary.json; rows are flushed as they are emitted. Main stops on the first exception, retains its context/traceback and prefix, and returns nonzero with INCONCLUSIVE_FIRST_FAILURE. Hard timeout/resource/output termination may prevent summary creation; the bounded runner's failed manifest and existing prefix remain the evidence. No missing row is a zero. Only the complete expected coverage can yield PASS_FINITE_ASSERTION. A failing invariant is a diagnostic discrepancy requiring interpretation, not automatically a theorem counterexample.

The bounded runner records complete child time, inputs before/after and output hashes. Main's body and per-query timers are supplemental and do not establish a matched optimizer budget. No QPU, DEV panel, optimizer, physical random count, random initialization, seed search, heldout data or paper/shared-state change occurs.

## Input closure and prospective commands

Both JSON contracts list the same complete project input closure: instructions, proof definitions, this source and its fixtures, this contract and both JSON contracts, package definition and pinned research lock. There are no production helper imports. External installed numerical dependencies are specified by pinned versions and observed native loaded-file hashes as described above; that observation is not a stronger software supply-chain certificate.

From /Users/karimelhoudaigui/Desktop/pasqal/.local/p66-finite-check, the child argv are:

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B -m pytest -x -q -p no:cacheprovider tests/test_p66_exact_finite_check.py --junitxml=research/P66_exact_finite_preflight/run_001/junit.xml

    /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B research/P66_exact_finite_check.py --output research/P66_exact_finite_main/run_001/data

These are **not launch authorization**. For the future authorized command, invoke the installed computation-audit scripts/run_experiment.py with this worktree as --root, the appropriate JSON as --contract, every execution_artifacts entry repeated as --input, all prospective result paths repeated as --result, a fresh corresponding run_001 as --output, --timeout 90 --max-output-bytes 4194304 --max-cpu-seconds 60 --max-threads 1, then -- and the exact child argv above. No hard address-space limit or unsupported CPU-affinity enforcement is asserted. Validate the resulting v2 manifest against this root after execution. Execution remains ROOT's responsibility after full static review and an exclusive slot.
