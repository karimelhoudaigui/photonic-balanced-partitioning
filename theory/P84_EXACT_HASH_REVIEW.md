# P84 exact-source audit of passive balanced-cut phase obstructions

**Primary verdict: proved as written.** Under the exact fixed-unitary,
lossless, no-ancilla dual-rail contract, a balanced cut admits its
all-basis diagonal phase at nonzero angles approaching zero if and only
if it is constant on the balanced slice. This is equivalent to additive
off-diagonal edge weights. The necessary single-angle lattice, genuine
periodic exceptions and the independent note's stronger parity-phase
classification also pass this review. No continuity of the physical
implementations is needed.

## 1. Frozen artifacts and provenance

The two complete sources audited are:

| Artifact | Original commit | Lines | SHA256 |
| --- | --- | ---: | --- |
| `theory/P84_PASSIVE_GRAPH_COST_PHASE_OBSTRUCTION.md` | `a47e27533da1ab37c36dc19f7177f5db2fe35630` | 303 | `cdb0892f3acaec911e732691bad96f33fea0595188dbb5ba21fb86a825b87786` |
| `research/P84_independent_cost_phase_obstruction.md` | `57068159d45b0881960bfa71804a30c826d345f9` | 275 | `e2098c9948272126612ab0d13c69898a9e0d112600c870b0984add57f5c26a76` |

All **578 source lines** were read. Committed-blob hashes and producer
worktree hashes match. The independent note was frozen before reading
the other P84 author. This audit, by a separate agent after reading
both sources and ROOT's contextual candidate, is an exact-source review,
not another blinded reconstruction or independent discovery.

The review uses the previously read `AGENTS.md`, `mathbox:proof-audit`
and mathematical self-proofreading instructions. It writes only this
file in the isolated `.local/p81-exact-review` worktree, branch
`research/p81-exact-review`. No scientific code/import, AST, test, RNG,
numerical graph or matrix calculation, backend, QPU or manuscript action
was performed. No P82/P85 output was inspected. Existing evidence and
author files are untouched.

## 2. Normalized statement and exact dependency

Let even `N>=4`, `K=N/2`. The physical system has `N` photons on `2N`
rails, one photon per logical qubit pair in each basis state `|S>`,
`|S|=K`. A graph has real symmetric off-diagonal weights `w_ij` and

    C(S)=sum_(i in S,j notin S) w_ij.

Each crossing undirected edge is counted once. Signed weights and
absent edges are allowed. Self-loops do not enter the cost.

For one fixed angle a single lossless passive mode unitary on these
same rails must satisfy

    Gamma_N(U_gamma)|S>
       = exp(i chi_gamma-i gamma C(S)) |S>

for **every** balanced `S` with one common `chi_gamma`. This condition
is stronger than preparing one vector or preserving one visited input.
Ancillas, losses, heralded branches, filters, input-dependent maps and
nonlinear operations are excluded. No graph optimum is an algorithmic
input; extrema used in the theorem are mathematical quantities only.

The one prior-project dependency is the exact P81 classification at
`0a51544a1a449c64b87cb48e82bf637583402278`, section 7, SHA256
`7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`,
with its separate reconstruction and this agent's exact-source review
`f915cf90a79429d09fd8de9854ab42b1e08b861c`, SHA256
`5abfd4c9e5fa86452b83fae995cbe754ddf35e39bc74b0007bc1033c1bcb64e0`.
That theorem was previously read completely and audited: exact
balanced feasibility for these `N>=4` inputs forces whole-pair
permutation, local monomial blocks and either no flips or global
complement. P84 uses precisely that exact refinement; it does not
substitute an empirical or visited-input leakage statement.

The new implication graph is internal:

    all-basis cost phase -> exact balanced feasibility -> P81
        -> logical identity forces physical pair action trivial
        -> multiplicative local-rail phase on subsets
    complement symmetry
        -> common phase square -> pointwise cost-difference lattice
        -> no nonconstant cost on an accumulating or open angle set
    constant balanced cut
        -> swap identities -> equal four-vertex matching sums
        -> explicit additive off-diagonal edge representation
        -> constant cut and a passive common-phase implementation

No external citation, numerical leaf or conjectural statement is needed.

## 3. Faithfulness of the restricted logical action, including N=4

The phase-oracle condition sends every balanced basis vector exactly
to itself up to phase, so P81 applies. Let `tau` send input qubit `i`
to output qubit `tau(i)`, and let `sigma` be the common flip bit.
The deterministic logical output satisfies

    y_(tau(i)) = x_i xor sigma.

If `sigma=0` and `tau(i)!=i`, a size-K set containing `i` but excluding
`tau(i)` has `x_i=1`, `x_(tau(i))=0`; it cannot be fixed. Therefore
the no-complement action is faithful and `tau` is identity.

If `sigma=1`, a fixed point of `tau` already contradicts `x_i=1-x_i`.
For a nonfixed `i`, choose a balanced set containing both `i` and
`tau(i)`. It exists since `K>=2` and contradicts the required opposite
bits. This also works at N=4, where `K=2` and those two labels themselves
form the balanced set. Thus no globally complemented permutation can
fix every input. Local rail phases cannot hide this deterministic-label
contradiction by interference.

Hence the physical unitary is rail-diagonal. Its N-photon basis phase is

    product_i alpha_(i,0)
       * product_(i in S) [alpha_(i,1)/alpha_(i,0)].

Bosonic creation operators commute, so there is no permutation sign
or an extra factor K. Absorbing the allowed common phase gives exactly

    f_gamma(S)=exp(-i gamma C(S)) = B * product_(i in S) z_i,

with all factors of unit modulus. This is a phase identity in the
circle, not an unjustified equality of real-valued logarithms.

## 4. Complement product, angle lattices and the exact quantifiers

Undirected cuts satisfy `C(S)=C(S^c)`. Multiplying the local expression
for the two complementary subsets gives

    f_gamma(S)^2 = B^2 * product_i z_i,

which is independent of `S`. Consequently, for every balanced pair,

    exp[-2i gamma(C(S)-C(T))]=1,
    gamma(C(S)-C(T)) belongs to pi*Z.

The common optical phase cancels. No branch of an argument, derivative,
or consistent compiler across angles is selected. If one difference
`D!=0` exists, every implementable angle lies in the discrete lattice
`(pi/D)Z`. This excludes every nonempty open interval and every sequence
of nonzero implementable angles tending to zero, even when each physical
unitary is chosen discontinuously and independently.

In particular, for balanced range `R>0`, a necessary condition is
`gamma R in pi Z`. The punctured interval `0<|gamma|<pi/R` contains no
implementable angle. The endpoints are not excluded. This lattice
condition alone is not sufficient at an isolated angle.

If the cost is constant `c`, the passive optical unitary
`exp(-i gamma c/N) I_(2N)` has N-photon action `exp(-i gamma c)`;
equivalently identity optics with a suitable allowed common phase works.
This proves the full equivalence of constant cost, every-angle
implementation and nonzero accumulating-angle implementation.

## 5. Exact constant-cut graph characterization

Set `d_i=sum_(j!=i) w_ij`. Comparing the cuts of `T union {i}` and
`T union {j}`, where `|T|=K-1` excludes both labels, gives

    d_i-d_j = 2 sum_(k in T)(w_ik-w_jk).

For four distinct `i,j,k,l`, choose `T0` of size `K-2` outside all
four labels. The inequalities `0<=K-2<=N-4` hold for every even `N>=4`.
Comparing `T0 union {k}` and `T0 union {l}` yields

    w_ik+w_jl = w_il+w_jk.

Relabeling supplies equality of all three opposite-pair sums. At N=4
`T0` is empty, so this is an actual covered case, not a large-N limit.

Using vertices 1,2,3, define the three parameters from their edge sums,
for example `a_1=(w_12+w_13-w_23)/2`, and define
`a_r=w_1r-a_1` for `r>=4`. The four-label identities on `1,2,3,r`
give all edges from `r` to the first three labels. Those on `1,2,r,s`
give the remaining edges. Thus every off-diagonal weight is
`w_ij=a_i+a_j`. At N=4 there is no pair `r,s>=4`, and the preceding
step already covers all six weights.

Conversely, additive weights give

    C(S)=(N-K)sum_(i in S) a_i + K sum_(j notin S) a_j
         = K sum_i a_i.

No sign restriction was used. Uniqueness for `N>=3` follows since
`b_i+b_j=0` on each pair of a triangle forces every `b_i=0`. Writing
`W=sum_(i<j) w_ij`, the additive class has

    W=(N-1)sum_i a_i,
    d_i=(N-2)a_i+sum_j a_j,
    a_i=[d_i-W/(N-1)]/(N-2),
    C_bal=K W/(N-1).

These are graph-only recovery/certificate formulas, not formulas that
make an arbitrary graph additive. Nonnegative edge weights require
`a_i+a_j>=0`; they do not require every `a_i>=0`. Self-loop weights are
irrelevant. A nonuniform unit-weight star gives a valid constant-cut
example with `a_center=1` and all other coefficients zero.

## 6. Independent note's stronger isolated-angle iff

This additional claim is proved in the second source and was checked
separately from the lattice necessity. Since every `f_gamma(S)^2` is
the same, exchanging `i` and `j` in a balanced set implies
`(z_i/z_j)^2=1`. Such exchanges exist for every pair of distinct labels.
Thus `z_i=z eta_i` for signs `eta_i`, and

    f_gamma(S)=c product_(i in S) eta_i.

Complement symmetry requires `product_i eta_i=1`, equivalently an even
number of negative signs. Conversely this parity phase is implemented
by local rail phases and is complement symmetric. Therefore an isolated
angle is implementable **iff** its phase values on the balanced slice
equal a common phase times parity on an even-cardinality vertex set.
This concerns phase values, not real affinity of the cost. The common
phase and the sign representation need not be unique.

For integer weights, including signed integers,

    C(S)=sum_(i in S) d_i-2 sum_(i<j, i,j in S) w_ij

implies `exp(-i*pi*C(S))=product_(i in S)(-1)^d_i`.
The odd-degree vertex set has even cardinality because
`sum_i d_i=2W` is even. The N=4 graph consisting only of edge 12
has balanced costs 0 and 1 yet admits this local phase at pi. Thus
isolated-angle exceptions are genuine and compatible with the stronger
criterion. They do not supply a continuously tunable nonlocal oracle.

## 7. Obligation matrix and limits

| Obligation | Status | Decisive check |
| --- | --- | --- |
| Exact P81 hypotheses and source hashes | passed | Same photons/modes; all-basis exact balanced feasibility |
| Faithful pair action at N=4 | passed | Contain/exclude labels; global complement contradicted |
| Bosonic and global-phase conventions | passed | Product of N rail entries; common phase absorbed once |
| Modular lattice, no U-continuity premise | passed | Complementary product and discrete-angle argument |
| Open interval and small-angle scope | passed | Range pair gives necessary `gamma R in pi Z` |
| Constant cut iff additive graph weights | passed | Swaps, four-label identities and explicit construction |
| N=4, signed weights, degree formulas | passed | Empty `T0`, no positivity used, sums checked |
| Isolated-angle parity iff | passed | Pairwise sign ratios and complement sign product |
| Periodic integer-weight examples | passed | Degree parity on every code string |
| Approximate or arbitrary optimizer obstruction | out of scope | Not established by this exact theorem |
| Novelty, hardware, equal-resource advantage | out of scope | No such evidence or claim |

No internal gap remains; no author correction or restriction beyond
the stated contract is needed. The result obstructs a specified exact
all-basis cost-phase representation. It does not obstruct every passive
optimization mechanism, a prepared state, an ancilla-assisted map, an
approximate oracle, a measured/reset hybrid or an unrelated encoding.
At angle zero identity works for any graph; at N=2 balanced cut values
are automatically constant, but P81's physical classification is not
silently extended there. True cost extrema are used only for analysis,
not training or preparing an optimum.

The cheapest next step for this result is ROOT's exact-source review
and provenance integration. A quantitative approximate statement needs
its own proof and metric. This audit does not authorize an experiment,
manuscript revision or QPU call, and does not close the positive optimizer
objective.

Evidence commands were complete file/instruction reads, commit metadata,
`shasum -a 256` for worktree and committed blobs, line counts and isolated
Git/document operations. The complete new audit was self-proofread for
coefficients, signs, quantifiers, notation and prose. No mathematical
token in an author source changed. No scientific computation or existing
test suite was run for this static document-only audit.
