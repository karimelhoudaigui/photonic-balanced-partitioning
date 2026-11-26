# P96 finite validation population — CODE ONLY

No import, AST, collection, test, exact computation, numerical allocation, RNG, native call, runner, QPU or paper edit was executed to author this package. Shell text reads/hashes/line counts and Git are metadata work. The prospective code and hand tables need ROOT and independent review before any execution. `computation-audit` is applied as a design workflow. A contract is not a result.

Original freeze `ac67650ceaa2bf7639ed72ef6fddb28a02067749` was never qualified. A predata review identified lost diagnostics on rejected nonfinite/native-thread/eigenvalue/Gram paths. This correction preserves observations before rejection and adds two pure diagnostic tests; it changes no matrix, physical population, tolerance or resource cap. The old commit remains evidence of the reviewed source.

The169-line mathematical source was read at `6f4e7fb90e284a8e358c55886ddd2032d45811f9`, SHA256 `b378ebd6bb0bb6f981e9fe395938e3a43aec7775f761b81cda7b394f6dc1e94e`, in the separate producer checkout. It is not copied into this code checkout. ROOT must bind its actual integrated bytes separately for main. The static source/tests/two contracts/this note remain unchanged after qualification. The P94/P95 notes remain frozen; P33/P37/E05b and all negatives are preserved.

Every T has observed rows and occupied-input columns. Entries below are exact rational amplitudes; K is the number of columns, m the number of rows. The source factory order is this table. Every signal occupation with total0..K is emitted, including all exact zeros, vacuum and collisions.

| ID | m,K | literal T | trace µ | planned signal bins | planned native full bins |
|---|---|---|---|---|---|
| V0 |1,0| `[[]]` |0|1|1|
| U1 |1,1| `[1/2]` |1/4|2|2|
| H2 |2,2| `[[1/4,1/4],[1/4,-1/4]]` |1/4|6|10|
| D3 |3,3| diagonal1/4 |3/16|20|NOT_PLANNED|
| R3a |1,3| all1/4 |3/16|4|20|
| R3b |1,3| all1/8 |3/64|4|NOT_PLANNED|
| S3 |2,3| `[[1/8,1/4,-1/8],[1/4,0,1/8]]` |11/64|10|NOT_PLANNED|
| B4 |2,4| all1/4 |1/2|15|126|
| D4 |4,4| diagonal1/4 |1/4|70|NOT_PLANNED|
| Z4 |2,4| all0 |0|15|NOT_PLANNED|
| R4 |1,4| all1/4 |1/4|5|NOT_PLANNED|
| C3 |2,3| `[[1/2,0,0],[0,1/2,0]]` |1/2|10|NOT_PLANNED|
| X4 |1,4| all1/2 |1 OUTSIDE|5|NOT_PLANNED|

Counts were derived by hand: signal bins are `binom(m+K,K)`, giving162 in-domain plus5 outside=167. A dilation has m+K output modes and full-K bins `binom(m+2K−1,K)`:1+2+10+20+126=159 in five cases. The corresponding native signal marginals have1+2+6+4+15=28 bins. K0 uses a1-mode identity dilation and vacuum input.

Exact reference: dictionary-polynomial permutation expansion of `per(I+Tᵀ(diag(z)−I)T)`, K≤4. The independent q construction uses `lambda_j=Σ_i Tji²` and `g2_jl=lambda_j lambda_l+(Σ_iTjiTli)²−2Σ_iTji²Tli²`; q0=1−µ+Σg2/2, q1=lambda−rowsum(g2), diagonal q2=g2jj/2, distinct q2=g2jl once. All first/factorial-second moments of P and q must match. No clipping or normalization adjustment is allowed.

Exact finite gates: q≥0/sum1; `TV(P,q)=Σ_(N≥3)P(n)(N−1)²`; this is bounded by `(2/3)E(N)_3≤24e3(c)≤4µ³`. R3a/R3b must attain the factor24 equality. X4 remains a PHYSICAL contraction: its rank-one squared norm equals trace1. Its q1=−1/2 is expected outside the trace≤1/2 hypothesis. Its exact P stays normalized/nonnegative; it receives neither a theorem PASS nor a theorem failure.

Eleven pure qualification functions retain the original nine hand-table/population tests and add strict JSON failure diagnostics plus thread drift from a FAKE object. Hand tables: vacuum, unary, H2, signed nonorthogonal K2, R3a, R3b, X4 and B4 totals. For R3a, P=(1709,297,39,3)/2048, q=(107/128,9/64,3/128), TV=3/512. For R3b, P=(125117,5769,183,3)/131072, TV=3/32768. H2 has vacuum49/64, each unary7/64, each bunch1/128 and coincidence0. B4 total-count P=(331,124,42,12,3)/512 and TV75/512. X4 P=(15/32,1/4,3/16,0,3/32), with negative q retained. These are hand calculations to be checked, not reported execution.

All13 exact cases complete before native setup. Native U has blocks `[[T,sqrt(I_m−TTᵀ)],[sqrt(I_K−TᵀT),−Tᵀ]]`; inject one photon in each of FIRST K columns, not first m. Roots use NumPy symmetric eigendecomposition, with no clipping. Both UᵀU and UUᵀ residuals must be≤1e−11. Native Naive evaluates exactly159 complete output amplitudes; every attempted state, amplitude, squared probability, thread readback and zero is kept. Sum environments independently for each of28 signal bins and compare to exact P with absolute tolerance1e−11, relative tolerance0; total native mass must also be1 within that tolerance.

Failure diagnostics are JSON strict: nonfinite floats become objects `{"nonfinite_float_repr":"nan/inf/-inf"}` and cannot satisfy the explicit finite guards. Native raw records precede finite rejection; the raw backend-return repr is saved before complex conversion/finally so post-call thread failure still preserves it in failure.prefix. Thread-drift exceptions include actual native/environment observations. Root operands, spectra/eigenvectors and U/both Grams/residuals are emitted before positivity/unitarity rejection. Synthetic Evidence files from the new pure test use pytest temporary directories; their durable observations are recorded in JUnit and are not physical samples.

Main CPU60/wall90, one worker, six environment thread variables1, actual exqalibur config1 before NumPy/Perceval/native computation and before/after every call. The unavoidable first exqalibur import occurs only after environment configuration and FSIZE; its initial config value is recorded before setting1. Actual installed versions, interpreter hash, eight pre-import external pins and loaded critical-module hashes are retained. No claim of authenticating every transitive dependency, RSS limit or hardware calibration.

Main explicitly sets hard/soft RLIMIT_FSIZE8MiB and CPU60 before scientific imports; the outer bounded runner supplies wall90/log4MiB. The three scientific result files collectively stay≤8MiB, with128KiB final-report reserve. This does not bound arbitrary library caches. Output is exactly `research/P96_column_loss_main/run_001/data`, newly created below a fresh runner parent; no resume/overwrite/automatic retry. Source errors preserve prefix and failure metadata; raw directory including manifest/logs must be committed BEFORE outcomes are read.

Qualification has its own pure-Python command, CPU30/wall60 and hard/soft FSIZE512KiB before importing pytest, disabled third-party plugin autoload, legacy JUnit with rational observations, and no native calls. It does not inherit main's8MiB cap. Its sole result is `research/P96_column_loss_preflight/run_001/junit.xml`; the8 relative static inputs are identical in both prospective contracts. The actual theory/native artifacts are not missing qualification files.

The separate future `research/P96_column_loss_main_binding.json` is NOT created by this package. It must declare SEALED_ROOT_AUTHORIZED, pin this frozen static contract and all8 qualified static inputs, include itself/the actual proof/qualification/auth evidence as real relative input files, and bind the actual proof hash. It can also serve as the bounded runner's active v2 contract with exactly that enlarged execution_artifacts list; scientific CLI still reads the unchanged static contract. This avoids modifying a qualification-pinned contract or creating a self-hash cycle. ROOT decides authorization only after qualification raw seal, inspection and separate receipt.

Prospective commands are arrays in the two contracts; do not run them until the respective explicit ROOT authorization. Passing this finite population would validate exact construction/factorials/positivity and selected native marginals, not an optimizer, global theorem proof, finite-bit random sampler, matched quantum speed, novelty or a QPU gate. The positive scientific objective remains OPEN.
