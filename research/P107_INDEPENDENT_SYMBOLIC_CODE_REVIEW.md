# P107 independent symbolic-code review

2026-11-26. Non-author STATIC review only; prospective engine, no result.
Frozen package: `6d9c16cde14ff25d51593c75607c712dcd7e9326`.
FULL text read, all 456 lines, with Git-blob SHA256 independently checked:

| File in research/ | Lines | SHA256 |
|---|---:|---|
| P107_symbolic_filter_validation.py | 389 | 4e0973ebfe8a250dbf012719087dcb0b7390932acd3ddab4e7055b3808cb2bbc |
| P107_SYMBOLIC_FILTER_POPULATION.md | 38 | 051d24038066d7cac3ef34f6f835703793c0d7e93b085cf20fa03d99ac14636b |
| P107_symbolic_filter_contract_TEMPLATE.json | 29 | d150e2042c5f8a02b09baab4da8426fd92348eb66525a2d7bf1a90ddb734e8ed |

Reference: all 113 lines of P101 at `69e4a6fe434a677acfc5a7e616471990b16db86b`,
SHA256 `65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c`.
Review parent: `90965893a38e06799333951f101a57a982504eb1`.

**STATIC PASS: no blocking defect found in the frozen finite calculation.**
This is not execution qualification, a sign result, independent numerical
replication, a runtime assertion or permission to run. ROOT's separate bound
authorization and runner remain necessary. No author retest is requested.

## 1. Fourier, Gaussian arithmetic and raw PGF

PHASES represents (-i)^r; family() therefore builds N_jk=sum_r
(-i)^((j-k)r)(1,x,xy,y)_r, exactly T=N/4=F diag(1,x,xy,y) F^dagger.
For example N_01=(1-xy)+i(x-y), agreeing with P101. Input/output gauge
conjugation does not alter the fixed-CF-input counting law or either decoder.
For real x,y, N is Hermitian and swapping x,y conjugates N. The checks
test both identities and later test realness/x-y symmetry for every raw
occupation coefficient. On the unit square all four eigenamplitudes lie
in [0,1], so this target really is a passive vacuum contraction.

laws() builds each occupied-column PGF entry as
16 delta_ij+sum_a (z_a-1)conj(N_ai)N_aj. Permanent for B and product of
diagonal entries for D have common denominator 16^4=65536. All signal
totals 0..4, including vacuum, losses and collisions, are extracted. There
is no survival denominator or conditional normalization. Each coordinate
degree is <=8 and total signal degree <=4; guards precede any larger
polynomial product. Permanent matrices never exceed size four.
Integer Gaussian addition, multiplication and conjugation are correct;
zero removal is algebraic cancellation, not selection of favorable outputs.

## 2. Independent factorial-moment representation and literal fixtures

For a signal multi-index r of total d, the second path forms
sum_(source subsets S,|S|=d) |per N_(rows repeated r,S)|^2 / product_j r_j!,
then multiplies by 16^(4-d) for the common denominator. This is the
coefficient of t^r in P_B(1+t), not the unnormalized falling moment.
There is no missing d! or additional input factorial for the CF source.
Repeated output rows make the integer division exact; the source asserts
that divisibility. Multivariate binomial inversion uses the correct
(-1)^(|r|-|n|) product_j binom(r_j,n_j). Degree zero/empty permanents work.
All 5670 dense B coefficients are compared, including zeros and negatives.

The two paths share Gaussian/permutation primitives, as disclosed. They
are independent mathematical representations, not independent libraries.
D has the direct independent-particle PGF plus literal fixture/endpoint
checks; a second independent symbolic D implementation is not claimed.
The five fixture tables reconstruct correctly by hand: vacuum, unary,
identity, the signed 3-4-5 rotation and the lossy rank-one two-source map.
The rotation probabilities include the required bunching factorial; the
rank-one fixture retains its zero B single-survival events. Their complete
state counts are 1+2+6+6+6=21, including all zero occupations.

## 3. Decoding, exact costs and target endpoints

cut() has the P101 graph weights: opposite edges 1, cycle edges 1/2;
balanced cut costs are 2 or 3. PNR averages all 24 independent priority
permutations after sorting by decreasing count. Threshold averages the
specified click-pair subsets, single-click completions or six vacuum pairs.
Thus every signal record is decoded, with no inferred number from clicks.
The four hand means 8/3,8/3; 8/3,8/3; 5/2,8/3; 3,8/3 check correctly.
Each of 70 occupations gets both exact expected costs, followed by all
81 coefficients of each B/D/difference mean. These are expected decoder
scores, not 24 physically evaluated partitions at the price of one query.

At x=y=1 only (1,1,1,1) remains. At x=y=0, T=J/4 and the B total-survival
law is (15/32,1/4,3/16,0,3/32), followed by multinomial(N;1/4).
D has Binomial(4,1/4) survival followed by the same multinomial. Both
endpoint formulas and their output factorials agree with the independent
manual bright-mode reconstruction; the source plans all 140 rows, including
the N=3 zero. No full eight-port native enumeration is performed or claimed.

## 4. Bernstein conversion, fixed coverage and scientific status

For x=a+w u, the coefficient of u^r in x^k is binom(k,r)a^(k-r)w^r;
degree-eight elevation uses u^r=sum_i binom(i,r)/binom(8,r) B_i^8(u).
The implemented transform is exactly their composition, with a tensor
product in y. No degree-eight truncation after a triangular substitution
occurs: conversion is directly on square boxes in x,y. Constant, linear
and x^8 y^8 hand tables correctly fix degree elevation and tensor indices.
The nine local reconstruction nodes are supplementary checks; correctness
of the conversion rests on this exact formula, not on nine samples alone.

Each decoder processes EVERY box at levels 0,1,2: 1+4+16=21. All 81
coefficients and each box's nine exact reconstruction comparisons are kept.
A whole level covers the unit square; nonnegative coefficients on every
box of that level certify nonnegative B-minus-D mean there. Positive
partial coverage is not accepted. A negative coefficient alone is not a
negative-value proof, and failure of all registered levels is INCONCLUSIVE.

All 25 grid pairs retain both complete 70-bin laws and both mean pairs.
Grid positivity/normalization and mean-vs-direct-decoder sums are checked
exactly. Negative grid differences are retained and do not stop later
registered work. COUNTEREXAMPLE_TO_SQUARE_ONLY does not decide the curve
y=x^(2+sqrt(3)); NONNEGATIVE_ON_WHOLE_SQUARE covers that curve and triangle.
ENGINE_PASS is separate from these statuses; a contradictory full-level
certificate plus negative grid observation correctly fails the engine.
No parameter reoptimization, graph selection or claimed advantage occurs.

## 5. Counts, prefix preservation and execution boundary

I independently counted 78 registered tasks and 9612 nominal record rows:
1 provenance +21 fixtures +4 decoder hands +3 Bernstein hands +1 matrix
+5670 coefficients +1 normalization +140 decoder costs +162 mean
coefficients +140 endpoints +25 grids +3402 Bernstein coefficients +42 boxes.
The plan comparison, dense row counts and completed/attempted registry
prevent accepting an early successful prefix as the full experiment.
The target matrix is emitted before its structural assertions; observed
coefficients, endpoint/grid values and box coefficients precede rejecting
checks. Signed/imaginary diagnostics and actual mismatches are preserved.
Exceptions mark the failed task and NOT_RUN suffix; science certificates
become NOT_ACCEPTED_ENGINE_FAILURE. Hard interruptions can lack finals and
must remain inconclusive, never inferred as an engine or science pass.

The passive TEMPLATE is rejected by authorize(). A separate ROOT_AUTHORIZED
binding must provide actual descriptors for all eight static inputs, exact
source/P101 hashes and the binding as a self-input without selfhash.
Descriptor paths are canonical relative regular files, with symlink checks,
unique names and exact execution-artifact closure. Inputs are not imported.
The source fixes its output location and demands a fresh exclusive data
child; input checks also exclude a symlinked research directory, and the
output checks exclude symlinked experiment/parent directories.

Python 3.11.15 and all six thread settings equal one are checked. Only
stdlib modules are imported, with no RNG, native library, old producer,
worker pool or dynamic source import. CPU 60s and per-file FSIZE 4MiB are
hard/soft limits; science aggregate is 4MiB with a 64KiB final reserve.
Wall 90s, separate 4MiB runner logs, fresh ENTIRE run parent, active v2
manifest/command validation, exit/file completeness and raw-directory seal
are OUTER RUNNER obligations, not additional guarantees of main(). ROOT
must establish them before executing these bytes and interpreting output.

No runtime feasibility, sign, uniform-flux extension, first-hitting,
best-of-T, total-cost comparison, held-out replication, novelty, QPU or
manuscript conclusion follows from this static review. Frozen P101/P96
remain untouched. Only text reads, manual algebra, hashes and Git metadata
were used; no import/AST/test/symbolic/numerical/native execution occurred.
