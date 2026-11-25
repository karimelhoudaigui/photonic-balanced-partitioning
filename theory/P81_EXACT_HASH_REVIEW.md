# P81 exact-source proof audit

**Primary verdict: proved as written.** For even `N>=4`, a fixed lossless
passive unitary on `2N` dual-rail modes whose raw code leakage is epsilon
on the entire uniform incoherent balanced basis ensemble is within

    ||U-V||_F^2 <= 4*N*(N-1)^2*epsilon/(N-2)

of a whole-pair permutation with independent local two-mode unitaries.
The full N-photon PNR laws differ by at most

    min(1, 2*N*(N-1)*sqrt[N*epsilon/(N-2)]).

The exact balanced-feasibility refinement, the N=2 exception, and the
qualified measured/reset adaptive corollary also pass this audit. These
are source- and architecture-restricted statements, with absolute error
and no matched-cost optimization conclusion.

## 1. Exact artifacts and review provenance

The following complete files were read, not excerpts or summaries:

| Artifact | Frozen commit | Lines | SHA256 |
| --- | --- | ---: | --- |
| `theory/P81_dual_rail_balanced_average_stability.md` | `0a51544a1a449c64b87cb48e82bf637583402278` | 358 | `7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f` |
| `research/P81_independent_dual_rail_stability.md` | `13ce8144b49ec91e916e9ca3f7b178c3490547bf` | 178 | `b9261878a61760ab68a44c2519c2a76712f13673d73c21eee92eafac4b2f4fb0` |

Both the committed blobs and their producer worktree files have the
listed hashes. This review was performed in the separate worktree
`.local/p81-exact-review`, branch `research/p81-exact-review`, starting at
`514a421`. Only this audit is written; neither author file is changed.

This is an independent-agent audit of exact sources after reading their
arguments and verdicts. ROOT's candidate formulas and the contextual
summary were also available. It is not a blinded reconstruction, an
independent discovery, or an external referee certification. The two
author notes separately record their own before-other-author-reading
reconstructions. Shared model/context errors remain possible; agreement
is not itself the mathematical evidence.

Applicable instructions were read from `AGENTS.md` and the
`mathbox:proof-audit` skill, including its relevant general-logic,
representation and source obligations. There is no `.mathbox/` ledger
in this review worktree. No narrower `AGENTS.md` was found under `theory/`
or `research/`. The old results, manuscript, QPU access, raw experiment
files and scientific source code are untouched.

## 2. Normalized claim card

* `N` is even and at least four; there are `N` photons and `2N` physical
  modes. The logical Hamming weight is `K=N/2`, not the photon number.
* A code basis state occupies one selected rail of each input pair.
  The calibration state is the uniform diagonal mixture of **all**
  `binom(N,N/2)` balanced basis states. No coherent Dicke state, visited
  subset or conditional source replaces it.
* `U` is one fixed complex unitary on the same `2N` modes, acting
  passively. There are no ancillary modes, losses, heralds, intermediate
  filters or discarded output records in the theorem's channel.
* If `n_a` is the total output occupancy of rail pair `a`, epsilon is
  the raw probability of `exists a: n_a!=1`. This is pair-code leakage;
  it includes two photons in different rails of one pair, even without
  a same-mode collision.
* The target `V` is a physical unitary with one unitary `2x2` block in
  each block row and each block column. It is constructed from `U`, not
  chosen from a known optimum partition.
* The operator-norm and TV conclusion holds for every common input
  density matrix in the N-photon sector. Efficient classical sampling
  at `V` is asserted only for known code basis inputs or an efficiently
  sampled classical mixture, with local probability access accounted
  for. It is not asserted for arbitrary entangled inputs.
* The additional monomial/global-complement classification uses exact
  code preservation **and** exact balanced-output preservation. Approximate
  code leakage alone does not prove proximity to that smaller class.

## 3. Dependency graph and leaf status

    passive U + one photon per input pair
        -> ordered nonnegative bosonic factorial-pair kernel
        -> exact all-code moment identity
        -> doubly stochastic block-intensity matrix B
    full balanced incoherent source + N>=4
        -> positive two-bit weights
        -> all-code moment <= c_N * balanced moment
    total photon number N + raw code failure epsilon
        -> balanced moment <= N(N-1)epsilon
    B doubly stochastic
        -> positive-support matching -> finite decomposition
        -> weighted assignment >= ||B||_F^2
        -> off-block mass delta <= 2 F_all
    local contraction blocks + unitary polar completions
        -> physical block-permutation V
        -> ||U-V||_F^2 <= 2 delta <= 4 F_all
    N-fold tensor telescoping + trace-distance contraction
        -> full raw PNR TV bound for every common N-photon input
    epsilon=0 + additional exact balanced feasibility
        -> local Bernoulli variances zero -> monomial local blocks
        -> flip set empty or all qubits
    pointwise certified reset protocols + common classical controller
        -> measurable V selection + first-divergence coupling
        -> sum of conditional absolute TV bounds

The pair contractions, balanced probabilities, matching/decomposition,
polar inequality and constants are proved internally. Elementary
finite-dimensional linear algebra (spectral decomposition, orthonormal
completion, tensor norm identities) and the usual trace-distance/TV
conventions are the remaining mathematical conventions used explicitly.
No literature result, cited numerical computation, empirical estimate or
unchecked novelty premise is load-bearing. There is no circular leaf
from the conclusion back to the input assumptions.

## 4. Obligation matrix

| Obligation | Status | Decisive check |
| --- | --- | --- |
| Physical modes, photon number and source typed | passed | `N` photons, `2N` rails, diagonal balanced calibration |
| Bosonic exchange kernel and ordering | passed | Two contractions per ordered pair, no same-photon term |
| Factor six in all-code identity | passed | `(Tr I_2)^2 + Tr I_2^2 = 4+2` |
| Balanced-to-all comparison | passed | Minimum pair-pattern weight `(N-2)/(4(N-1))>0` |
| Raw leakage controls factorial moment | passed | Total occupancy fixed at `N`; failure indicator retained |
| Weighted assignment | passed | Support-capacity contradiction and finite support deletion |
| Polar completion, including singular blocks | passed | Complete zero-singular subspaces; no inverse at zero |
| Final Frobenius constant | passed | Four times `F_all`, not four times the balanced moment |
| Full-sector lifting and TV convention | passed | N telescoping terms and trace distance without extra two |
| Classical sampler scope | passed | Conditional product law; arbitrary mixtures may correlate |
| Exact balanced-feasibility classification | passed | Variance zero; all fixed-size subsets force all/no flips |
| N=2 counterexample | passed | Partial rail swap fixes balanced inputs but leaks 00/11 |
| Measurable adaptive comparison | passed | Per-history counterfactual premise and common reset source |
| Empirical leakage confidence, finite-bit implementation | out of scope | No experiment or algorithmic accuracy contract supplied |
| Novelty, equal CPU cost, optimizer advantage, QPU | out of scope | None is asserted or inferred |

## 5. Reconstructed decisive algebra

Fix output pair `a`, and let `u_(b,sigma)` be the two-component projected
column of `U` from input rail `(b,sigma)`. Put `R_ab=U_ab U_ab^dagger`,
`t_ab=Tr R_ab`, `B_ab=t_ab/2`. For two distinct occupied input modes,

    q(u,v)=||u||^2 ||v||^2 + |u^dagger v|^2 >= 0.

The normally ordered `n_a(n_a-1)` has both direct and exchanged input
contractions. Thus its expectation is the sum of `q` over **ordered**
distinct input pairs. Summing the two rail labels independently gives
`t_ab t_ac+Tr(R_ab R_ac)`. In the all-code mixture the rail-pair weight is
`1/4`, so `sum_b R_ab=I_2` yields

    F_(a,all)=[6-sum_b(t_ab^2+Tr(R_ab^2))]/4.

Since `0<=R_ab<=I_2`, the sum of traces of squared blocks obeys
`sum_b Tr(R_ab^2)<=2`. Consequently

    F_(a,all) >= 1-sum_b B_ab^2.

The balanced two-bit probabilities for distinct positions are exactly
`(N-2)/(4(N-1))` for equal bits and `N/(4(N-1))` for unequal bits.
Nonnegativity of **each** kernel is what permits coefficientwise
comparison; a potentially signed interference sum is not being bounded
by discarding its signs. Summing over output pairs gives

    F_all <= (N-1)/(N-2) F_bal
          <= N*(N-1)^2*epsilon/(N-2).

The second step uses, record by record,

    sum_a n_a(n_a-1) <= N*(N-1)*1_{code failure}.

There is no assertion that fixed photon number implies code feasibility.

For doubly stochastic `B`, its internally derived convex permutation
decomposition makes the average selected weight equal to `sum_ab B_ab^2`.
One selected permutation therefore has at least that weight. The
off-block mass and selected-block polar errors then satisfy

    delta = 2[N-sum_a B_(a,pi(a))]
          <= 2[N-sum_ab B_ab^2] <= 2 F_all,
    sum_a ||U_(a,pi(a))-Q_a||_F^2
          <= sum_a [2-||U_(a,pi(a))||_F^2] = delta.

The selected and nonselected entries are disjoint. The complete unitary
distance is at most `2 delta`, proving exactly the announced constant.
The polar scalar inequality `(1-s)^2<=1-s^2` is valid on the entire
closed interval `[0,1]`, including a zero block.

On the symmetric N-fold tensor sector the passive map is the restriction
of `U^(tensor N)`. The N-term telescoping identity gives operator error
at most `N||U-V||op`. For normalized pure outputs with inner product `z`,

    1-|z|^2 <= 2-2 Re(z)

because their difference is `|1-z|^2>=0`. This verifies the trace-distance
bound directly, including a possibly loose global phase. Mixed inputs
and complete PNR measurement preserve the claimed upper bound by
convexity and measurement contraction. TV uses the factor `1/2` in the
L1 convention, so there is no missing factor two.

## 6. Boundary, ordering and falsification checks

The all-code moment normalization can be checked by hand on
`U=H_2 tensor I_2`. At either output pair its two projected blocks have
`R=I_2/2`. Equal input rail labels give factorial moment `1`, unequal
labels give `1/2`; the all-code average is `3/4`, matching the factor-six
formula. This checks the ordered-pair normalization without numerical
evaluation or an experiment.

At epsilon zero the derived distance is zero, so `U=V` exactly. If every
balanced basis input also has deterministic balanced output weight,
the conditionally independent local bits have variance sum
`sum_a p_a(1-p_a)=0`. Every input rail is used by some balanced input,
so every local unitary column must be deterministic and the block is
monomial. A fixed proper nonempty flip set cannot have the same
intersection size with every `N/2`-subset: exchanging one location in it
with one outside changes that intersection by one. Empty and full flip
sets both work, the latter because `K=N/2`. This does not imply arbitrary
many-body basis phases.

For N=2, the mode permutation exchanging `a_1` and `b_0` fixes balanced
01 and 10 as bosonic Fock states. It maps 00 to both rails of pair `a`
and 11 to both rails of pair `b`, so it is not a whole-pair block
permutation. The missing equal-bit patterns are exactly the zero weights
at `N=2`; this is a genuine exception, not merely a proof singularity.

The visited-input restriction is also substantive at larger N. With
N=4 and input 1100, swapping the occupied rails `1_1` and `3_0` fixes
that Fock input but is not a whole-pair permutation. Zero leakage on
this one visited input cannot imply the stated conclusion. Coherent
balanced preparation instead adds input off-diagonal terms; neither
author applies the nonnegative-mixture comparison to that source.

## 7. Adaptive and sampling qualifications

For a fixed code basis input under `V`, photons occupy distinct output
pairs. Local Bernoulli choices are independent, and there are no
overlapping inter-pair paths on which distinguishability can matter.
For a diagonal input mixture, independence holds **given** its sampled
basis label; the unconditional law can be correlated. This equality
with a distinguishable law is at `V`, not an equality claim at `U`.

The first author additionally supplies a measured/reset adaptive
corollary. Each realized `U`, at each common history and shared random
mark, needs its own entire uniform-balanced-average leakage premise.
The actual common source can then use the full-sector norm bound. No
differing hidden coherent memory is permitted. Lexicographic selection
among finitely many maximum-weight assignments is measurable. Local
polar choices can be made continuous on the full-rank stratum and
piecewise continuous on fixed rank-one pivot strata, with a fixed
choice at rank zero. Thus the conditional `V` kernel is well-defined.

When prefixes agree, maximal coupling of the finite raw count laws has
mismatch probability at most `eta_h`. The first-divergence probability
at each step is bounded by `E[1_{common prefix} eta_h]`, which is at most
the expectation under the true U-history marginal. Summing gives the
stated `min(1,sum_j E_U eta_h)` transcript bound. Common classical
decoders and stopping rules within the same shot cap contract it.
This argument neither substitutes visited-input leakage nor makes
postselection, coherent multishot dynamics or unequal resource budgets
free. The second note does not assert this extra adaptive corollary;
it states the fixed-map scope conservatively.

## 8. Disposition, commands and remaining work

There is no remaining internal gap in the claims audited here. No
author correction or changed hypothesis is required. Keep the bound,
exact rigidity and explicit exception at their present scopes. Its
Frobenius coefficient grows as order `N^2`, and its TV coefficient as
order `N^2*sqrt(epsilon)`; this does not furnish a dimension-independent
or automatically useful empirical certificate.

The only commands used for evidence were file/instruction reads,
`git show --format=fuller --stat` for the two producer commits,
`git show COMMIT:PATH | shasum -a 256`, worktree-file `shasum -a 256`,
`wc -l`, instruction/ledger path searches and isolated Git operations.
All 536 author lines were read. No P79 outputs were inspected. No
scientific import, AST, test, RNG, probability calculation by code,
matrix computation, native backend, QPU or manuscript operation occurred.
Existing tests were not run for this static document-only audit; ROOT's
integration checks remain separate.

The cheapest next step for this result is ROOT's exact-source review
and provenance integration. Estimating epsilon, extending the theorem
to another architecture, validating finite-bit sampling, or asserting
novelty would require separate evidence. This review supplies no
positive optimization result and no permission to release a QPU circuit.

Self-proofreading covered this complete new audit after its mathematical
review. Routine edits: one clarification of prose about `Tr(R_ab^2)`.
Mathematical-token changes to author sources: none. Unresolved issues:
none within the audited scope. Validation: source hashes and line counts
checked; document whitespace checked with `git diff --check`.
