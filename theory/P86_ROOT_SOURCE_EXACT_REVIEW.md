# P86 exact audit of ROOT's approximate passive cost-phase theorem

**Primary verdict: proved as written.** The specified common-phase,
all-balanced-basis state-vector error obeys

    delta(U,gamma) >= |sin(gamma*(C(S)-C(T)))|/(2 b_N),
    b_N=1+N sqrt[4N(N-1)^2/(N-2)],

for every balanced pair `S,T` under the fixed lossless, passive,
no-ancilla dual-rail contract. The small-angle consequence, boundary
cases and one-way restricted-operator-norm interpretation also pass.
This is a representability statement, not an optimizer lower bound.

## 1. Source and exact audit provenance

The complete ROOT source audited is
`theory/P86_APPROXIMATE_PASSIVE_COST_PHASE.md`, **171 lines**, frozen at
`daf49c64feb070f82412b8c3f59a63d8eb4f742d`, SHA256
`a8074fd204b5294d455601a1e44751b1cc6656e0f565b4e10ddefe100564a932`.
The committed blob and source file have this hash.

Sections 1-8 of this audit were fully reconstructed and written from
ROOT's source before reading or contacting the separate P86 author.
The later comparison section, if present, is explicitly distinguished.
This is exact-source review after reading ROOT's proof and candidate,
not a blinded derivation or independent discovery. The reviewer also
audited the named P81 dependency earlier, before P86 existed.

The audit follows the already-read `AGENTS.md`, `mathbox:proof-audit`
and mathematical self-proofreading instructions. Only this file is
written in the isolated `.local/p81-exact-review` worktree. No scientific
code/import, AST, test, RNG, matrix numerics, backend, QPU or manuscript
action occurs. No P82/P85 output is inspected. No author source changes.

## 2. Normalized claim and dependency graph

Let `N>=4` be even. There are `N` photons on `2N` physical rails, one
photon per input pair in each balanced code basis state. Logical ones
number `N/2`, not the photon number. `U` is one fixed lossless passive
unitary on these same modes, with no ancillary modes/photons, losses,
heralded branch, filtering or discarded outputs. `C(S)` is a real
complement-symmetric cost on every balanced subset. A weighted graph
cut is an instance, but no quadratic-cost identity is needed here.

The error is the maximum normalized vector error over **all** balanced
basis states, minimized over **one common** phase chi. An independent
phase for each basis vector would erase the cost oracle. For fixed U
the maximum is over finitely many continuous functions of chi on the
compact circle, so a minimizing phase exists. No continuity of U across
angles is assumed or used.

The exact named P81 dependency is the quantitative theorem, not merely
its exact monomial classification: for the uniform incoherent balanced
calibration source, raw code leakage epsilon supplies a block-permutation
unitary V with

    ||U-V||_F <= sqrt(C_N epsilon),
    ||Gamma_N(U)-Gamma_N(V)||op <= N sqrt(C_N epsilon),
    C_N=4N(N-1)^2/(N-2).

Its author source is `0a51544a1a449c64b87cb48e82bf637583402278`, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`,
previously audited in full by this reviewer at
`f915cf90a79429d09fd8de9854ab42b1e08b861c`. The physical modes, photons,
source averaging and no-ancilla premises match P86 exactly.

The remaining implication graph is internal:

    minimizing common-phase column errors <= delta
       -> orthogonal code-leak probabilities <= delta^2
       -> P81 V with operator error <= N sqrt(C_N) delta
       -> V-column errors <= e=b_N delta
    e>=1/2 -> desired sine bound is trivial
    e<1/2 -> each diagonal V amplitude has modulus >7/8
       -> nonidentity pair permutation contradicts one local row norm
       -> identity pair permutation, without monomializing local blocks
       -> complementary diagonal amplitude products constant
       -> target phase squares within 4e -> sine bound

No external literature, empirical estimate, numerical experiment,
spectral conjecture, optimum oracle or continuity input is load-bearing.

## 3. Leakage and the only operator-norm lifting used

Choose one minimizing chi and put
`f_S=exp(i chi-i gamma C(S))`. Each target `f_S|S>` lies inside the
dual-rail code. Orthogonal projection onto the code complement is
contractive and annihilates this target. Hence every raw leakage
probability is at most delta squared, and their uniform incoherent
average satisfies `epsilon<=delta^2`.

This is an algebraic counterfactual calibration consequence of the
all-basis error; the mixture need not be physically prepared. It does
not infer leakage from a visited subset, from mean fidelity, from
postselected data or from a coherent source's count interference.

Applying P81 with this epsilon and its tensor-telescoping estimate gives

    ||Gamma_N(U)-Gamma_N(V)||op <= N sqrt(C_N) delta.

The triangle inequality on each normalized code column then yields

    ||Gamma_N(V)|S>-f_S|S>|| <= b_N delta = e.

There is no inference from a maximum column error to the same-sized
operator error. The operator bound comes instead from P81's one-particle
matrix estimate. Thus no square root of the balanced-subspace dimension
is suppressed.

## 4. Small-error branch forces identity pair permutation

If `e>=1/2`, then `delta>=1/(2 b_N)` already dominates every claimed
right-hand side. This includes the equality boundary. Suppose `e<1/2`.

Write `A_S=<S|Gamma_N(V)|S>`. Both vectors in the preceding column norm
are normalized, so

    2-2 Re(conj(f_S) A_S) <= e^2,
    |A_S| >= 1-e^2/2 > 7/8.

For V's output-pair-to-input-pair permutation pi and local blocks Q_a,

    A_S=product_a Q_a[x_a,x_(pi(a))].

There is exactly one photon routed to each output pair. The overlap
therefore has this product form without an extra factorial or a
fermionic sign, even when the local blocks are not monomial.

If `pi(a)=b!=a`, there is a balanced input S0 with `x_a=x_b=0`, since
`N-2>=N/2`. There is also a balanced input S1 with `x_a=0,x_b=1`.
These choices exist at N=4: the first occupies both remaining one-rails,
and the second occupies b and one other one-rail. All other product
factors have modulus at most one, forcing

    |Q_a[0,0]|>7/8,   |Q_a[0,1]|>7/8.

The sum of their squared moduli would exceed `2*(7/8)^2=49/32>1`,
contradicting the same row's unit norm. Thus pi is identity. No exact
code or balanced preservation for the original U is inferred, and no
exact diagonality of the local Q_a is required.

## 5. Complement products and constants

With identity pi, the amplitudes are diagonal-entry products, so

    A_S A_(S^c)=product_a Q_a[0,0] Q_a[1,1] = L

is independent of the balanced S. This remains true for nonmonomial
blocks; asserting exact local diagonal form would be unnecessary and
unjustified here. From the column norm, `|A_S-f_S|<=e`.
Complement symmetry gives `f_(S^c)=f_S`; `|A_S|<=1` by unitarity.
Consequently

    |L-f_S^2|
       <= |A_S| |A_(S^c)-f_S| + |f_S| |A_S-f_S|
       <= 2e.

Comparing S and T gives

    |f_S^2-f_T^2| <= 4e,
    |f_S^2-f_T^2| = 2|sin(gamma(C(S)-C(T)))|.

The common chi cancels exactly. Therefore
`delta>=|sin(gamma(C(S)-C(T)))|/(2 b_N)`, completing the small-error
branch and matching the already handled large-error branch. There is
no phase logarithm or derivative of the physical unitary in this step.

## 6. Small-angle and boundary checks

For actual balanced range `R>0`, use a maximizing and minimizing pair
in the universal inequality. On `|gamma|R<=pi/2`, the elementary chord
bound `sin x>=2x/pi` on `[0,pi/2]` gives precisely

    delta >= |gamma|R/(pi b_N).

For fixed N and a fixed nonconstant cost, this excludes `delta=o(|gamma|)`
for every family of implementing unitaries, even a discontinuous one.
In fact the same sine inequality before its chord relaxation also gives
`liminf delta/|gamma| >= R/(2 b_N)` as nonzero gamma tends to zero.
The latter is a direct additional consequence, not needed for ROOT's
stated weaker finite-interval bound.

If delta is zero, every cost difference lies on the P84 necessary
single-angle lattice. At integer-weight pi phases that sine bound can
vanish, as it should. If the cost is constant, identity with a common
phase has delta zero. These are consistency checks of an absolute
error bound, not a claim that its converse characterizes isolated angles.

Identity optics also gives `delta<=|gamma|R/2` after choosing the common
phase from the midpoint of the cost range. Thus a nonzero error floor
independent of gamma is not claimed, and first-order small-angle
approximation remains possible. The constants are loose and depend on
N: `C_N` is of order `N^2`, and `b_N` is of order `N^2`.
No uniform-in-growing-N fixed-error conclusion is established.

## 7. Operator norm, observability and scope

Let `P_bal` project onto the balanced code span and let
`D_gamma|S>=exp(-i gamma C(S))|S>` on that span, regarded as a map into
the full N-photon space. Products with `P_bal` extend it by zero.
For each common chi the restricted-subspace operator norm dominates
every normalized basis-column error. Taking the minima therefore gives

    min_chi ||Gamma_N(U)P_bal-e^(i chi)D_gamma P_bal||op
       >= delta(U,gamma).

The lower bound transfers in this one direction. Its converse does not
follow: coherent superpositions can accumulate column errors. P86 does
not use such a converse in its proof.

The metric is phase-sensitive with a common reference. Measuring a
basis input in PNR or checking only its fidelity cannot observe its
oracle phase; identity passes those phase-insensitive tests. That is
not coherent oracle validation. A selected or visited input family,
ancillary sources, loss, monitored outcomes, filters, other encodings
and general optical optimizers change the premises. None is shown
impossible, available or free by this proof.

The use of the true range is theorem interpretation only. No training,
encoding or calibration procedure queries C*, an optimal-state mask or
known optimal partitions. N=2 lies outside P81; its balanced graph cut
is constant anyway, and no classification at N=2 is imported here.

## 8. Audit obligations and disposition before peer comparison

| Obligation | Status | Decisive check |
| --- | --- | --- |
| Exact common-phase metric and minimum | passed | Compact circle and finite continuous maximum |
| Raw leakage from column error | passed | Orthogonal projection, then full uniform average |
| P81 constant and mode/source assumptions | passed | Exact `C_N`; N photons, 2N rails, same U |
| Operator lifting versus columns | passed | P81 tensor norm only; no reverse column inference |
| Large-error branch and threshold | passed | `e>=1/2` dominates sine numerator at most one |
| N=4 nonidentity-permutation contradiction | passed | Both 00 and 01 patterns exist for one row |
| Local nonmonomial blocks allowed | passed | Complement amplitude product uses diagonal entries only |
| Four-e and two-sine factors | passed | Two product errors and one phase-chord identity |
| Fixed-N small-angle scaling and identity upper bound | passed | Sine limit and midpoint common phase |
| Optimizer, hardware or novelty implication | out of scope | No such evidence or conclusion |

No internal gap or author correction is needed. The strongest safe
statement is a first-order lower bound for this all-basis passive
cost-phase representation problem, with the stated resource and source
restrictions. It does not settle the positive optimizer objective,
describe a practical gate-error threshold or authorize QPU work.

This complete source-audit argument was written before any read of the
separately frozen P86 reconstruction. The subsequent peer comparison,
if appended, must not be described as before-source independence of
this audit.

## 9. Comparison with the separately frozen reconstruction

Only after the entire source-audit argument above had been written did
this reviewer read the complete independent reconstruction:

* `research/P86_independent_approximate_cost_phase.md`;
* original commit `36ff60481e259438fd9d4cf58ef6953109572384`;
* **256 lines**, SHA256
  `cf156f61e2c47864c024cc471d6e1fc873aec18158ba5a4c70898d456eb8342a`.

Both its committed blob and producer worktree file have that hash.
The previously written 245-line standalone audit, before the peer read,
had SHA256 `3a5022f9f932b960f1ab24a6d4716aa1eb9b45ce26a89b1a6fb45907834fb920`,
recorded in the tool output and reported to ROOT. The later edits add
this comparison and make the already-used `P_bal`/`D_gamma` notation
explicit; they do not change the standalone reasoning or its verdict.

All 256 peer lines were read, for **427 audited source lines** in total.
The peer records its own before-ROOT-file-reading reconstruction from
ROOT's supplied candidate route and constants. This audit is not
retroactively reclassified as before-source reconstruction. No direct
contact with the peer author occurred before finishing the standalone
argument or during this comparison.

The two arguments agree at every load-bearing step: attained common
phase; raw epsilon bound; exact P81 constant; N-photon telescoping;
the `e>=1/2` branch; balanced 00/01 witnesses at N=4; local row norm;
complementary products without requiring monomial blocks or division
by their entries; and `2|sin|<=4e`. The peer's stronger fixed-N
`liminf delta/|gamma|>=R/(2 b_N)` statement agrees with the consequence
already derived in section 6 before reading it. Its stronger-metric
interpretation also correctly gives only `Eop>=delta`.

The peer additionally makes clear that the full collection of pairwise
sine bounds can be stronger than the range bound at isolated angles
where the latter vanishes. This follows directly from ROOT's universal
pairwise statement and is not a contradiction or a repaired gap. Both
notes explicitly preserve phase-sensitive observability, zero-cost-range
and periodic-angle exceptions, and the limits of optimizer inference.

**Comparison verdict: proved as written.** No additional premise,
author correction, numerical verification or source mutation is needed.

Evidence operations were only full file reads, committed-blob and
worktree `shasum -a 256`, line counts, commit metadata and isolated
document/Git operations. No scientific import, AST, test, RNG, numerical
matrix/probability evaluation, backend, QPU, P82/P85 data or manuscript
action occurred. The complete audit was self-proofread for coefficients,
scope, notation and prose; mathematical changes to author sources: none.
Existing tests are not run for this static document-only review.
