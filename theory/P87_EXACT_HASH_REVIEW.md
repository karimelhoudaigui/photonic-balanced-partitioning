# P87 exact-source audit of sharp first-order passive oracle error

**Primary verdict: proved as written.** For fixed even `N>=4` and a
fixed real complement-symmetric balanced cost of range R, the optimized
common-phase all-basis vector error satisfies

    lim_(gamma->0,gamma!=0) delta_*(gamma)/|gamma| = R/2.

Identity optics has the same first-order coefficient. The analogous
optimized common-phase operator error, from the balanced code subspace
into the full N-photon space, has that limit too. The explicit finite
bound is correct, including its large-error branch. The constants can
grow factorially with N; no practical or dimension-uniform accuracy
threshold is inferred.

## 1. Exact source and review provenance

The complete ROOT source audited is
`theory/P87_FIRST_ORDER_PASSIVE_COST_PHASE.md`, **168 lines**, original
commit `643686079fb50c16f7d23b0a7f7b7214f0a4516c`, SHA256
`f4934640c71362f76c179d57435974d0c6959c0ea18b867c87d84a943bdac3cc`.
The committed blob and producer/root file hashes match.

The complete standalone argument in sections 1-8 was written before
reading or contacting the separate P87 reconstruction. A later peer
comparison, if appended, is identified separately. This is exact-source
review after ROOT's candidate and argument were read, not a blinded
derivation, independent discovery or novelty certification. The reviewer
previously audited the relevant P81 and P86 proofs.

The review applies the already-read `AGENTS.md`, `mathbox:proof-audit`
and mathematical self-proofreading instructions. Only this new audit is
written in the isolated `.local/p81-exact-review` worktree. No source
correction, scientific code/import, AST, test, RNG, matrix numerics,
backend, QPU or manuscript action occurs. No P82/P85 drafts or outputs
are inspected. Existing evidence and author files are untouched.

## 2. Typed contract and dependencies

`N` photons occupy `2N` dual-rail modes, one photon per input pair.
The basis consists of every logical balanced `|S>`, `|S|=N/2`. `U` is
a single lossless passive unitary on these same modes, with no ancillary
modes/photons, heralds, loss, intermediate filters or discarded outputs.
The real cost C is fixed and satisfies `C(S)=C(S^c)`; an undirected
weighted graph cut is one instance.

The metric is the maximum normalized state-vector error over all these
basis inputs, minimized over **one common** phase chi. The minimum is
attained by compactness of the phase circle and continuity of a finite
maximum. `delta_*(gamma)` is its infimum over every physical `U in U(2N)`.
No continuity, generator bound or coherent compilation family in gamma
is assumed. The infimum need not be assigned a regular optimizer for
the proof to work.

The physical stability input is quantitative P81, with

    C_N=4N(N-1)^2/(N-2),
    ||U-V||_F <= sqrt(C_N epsilon).

The exact author source is `0a51544a1a449c64b87cb48e82bf637583402278`,
SHA256 `7fe0b14f6412201bedbb3bd5af21d16fcb7d9724d6903f52dd7996efce9b068f`,
previously read in full and reviewed by this agent. P86's small-error
pair-permutation argument is repeated in P87 and checked below; no
additional conjectural theorem is needed.

The new proof graph is:

    all-basis delta -> raw uniform-balanced epsilon<=delta^2
       -> P81 pair-block V and N-photon comparison
       -> small delta forces V's pair permutation identity
       -> local off-diagonal entries O(delta)
       -> original U's entire physical off-diagonal mass O(delta)
    CF input-to-same-CF-output amplitude is a principal permanent
       -> every nonidentity term contains >=2 off-diagonal entries
       -> diagonal amplitude differs from diagonal product by O(delta^2)
       -> complementary diagonal products independent of S
       -> target phase invariant to 2delta+2Edelta^2
       -> uniform finite lower bound -> infimum and sharp lower limit
    identity with midpoint common phase
       -> matching upper limit for columns and restricted operator norm

No numerical computation, external literature, graph optimum oracle or
unchecked regularity assumption is a leaf in this graph.

## 3. Small-error structure and constants

Write `delta=delta(U,gamma)`, choose a minimizing common chi, and put
`f_S=exp(i chi-i gamma C(S))`. Each target lies in the code, so
orthogonal projection onto its complement bounds each raw leakage
probability by `delta^2`. The full uniform incoherent balanced average
therefore has `epsilon<=delta^2`, exactly the P81 premise.

With

    s=sqrt(C_N), b=1+N s, delta0=1/(2b),

P81 supplies a physical pair-permutation/local-block V with

    ||U-V||_F <= s delta,
    ||Gamma_N(V)|S>-f_S|S>|| <= b delta = e.

The second inequality uses N-fold tensor telescoping between two
physical passive unitaries, not an invalid conversion of target column
errors into operator norm. The tensor factor is N photons.

For `delta<delta0`, normalization gives every V diagonal overlap
modulus at least `1-e^2/2>7/8`. A nonidentity output-to-input pair match
`pi(a)=b!=a` would give balanced 00 and 01 patterns in the same output
row, forcing both `|Q_a[0,0]|` and `|Q_a[0,1]|` above `7/8`. Their
squared moduli would sum above one. Both patterns exist at N=4 as
well: the 00 input uses the two remaining logical one-rails. Thus pi
is identity. This repeats the valid P86 argument without requiring
the local Q_a already be monomial.

The V diagonal amplitude now is `product_a Q_a[x_a,x_a]`. Each factor
has modulus at most one; a product of modulus at least `1-e^2/2`
therefore forces every selected factor to have at least that modulus.
Every input rail is selected by some balanced string, so every local
diagonal entry meets the same bound. Row unitarity then gives

    |Q_a[0,1]|^2, |Q_a[1,0]|^2
       <= 1-(1-e^2/2)^2 <= e^2.

There are exactly `2N` such physical off-diagonal entries in V. The
operation `off` deleting a matrix's main diagonal is contractive in
Frobenius norm. Consequently

    tau=||off(U)||_F
       <= ||U-V||_F+||off(V)||_F
       <= s delta+sqrt(2N)e = d delta,
    d=s+sqrt(2N)b.

This controls physical mode off-diagonals, not merely inter-pair
blocks. No diagonal optical phase has been fixed or declared small.
The distinction is essential for the permanent argument.

## 4. Principal permanent and its quadratic remainder

Let `I(S)` be the N distinct occupied physical rails of a code basis
input. For the overlap with that same normalized Fock state,

    A_S=per(U[I(S),I(S)]),
    B_S=product_(i in I(S)) U_ii.

The permanent is the full bosonic amplitude. All occupation factorials
are one; there is no collision-free postselection in defining this
particular matrix element, and other output probabilities remain part
of the original column error.

The identity permutation term is exactly B_S. Every other permutation
moves at least two labels, hence contains at least two **physical**
off-diagonal entries. Choose two of them and bound each by tau; every
remaining actual entry, including any further off-diagonal one, has
modulus at most one by unitarity. Thus each term is at most `tau^2`,
and summing the `N!-1` terms yields

    |A_S-B_S| <= (N!-1)tau^2 <= E delta^2,
    E=(N!-1)d^2 > 0.

This argument does **not** require `tau<=1`. Replacing a product of
three or more off-diagonal entries by a power of tau and then assuming
that power is at most tau squared would be invalid without that
restriction; the source correctly retains the remaining entrywise
unitary bounds instead.

Both `|A_S|<=1` and `|B_S|<=1`: the former is an N-photon unitary
amplitude and the latter a product of unitary entries. I(S) and I(S^c)
partition all `2N` rails, so

    B_S B_(S^c)=product_(i=1..2N) U_ii = L,
    |A_S A_(S^c)-L| <= 2E delta^2.

The latter follows by replacing the two factors one at a time, with
the unchanged factors bounded by one. No division by a potentially
zero diagonal entry or amplitude is used.

## 5. Target phase, finite bound and branch inversion

The original oracle column error gives `|A_S-f_S|<=delta`.
Complement symmetry gives `f_(S^c)=f_S`. Combining the two replacements
with the preceding product estimate gives

    |f_S^2-L| <= 2delta+2E delta^2.

Subtracting the relations for S and T and using the exact phase chord
identity gives

    2|sin(gamma(C(S)-C(T)))| <= 4delta+4E delta^2.

The common chi cancels. For `t=|sin(gamma(C(S)-C(T)))|` the positive
quadratic root is exactly

    q(t)=[sqrt(1+2E t)-1]/(2E)
        =t/[1+sqrt(1+2E t)].

Thus the small-error branch `delta<delta0` gives `delta>=q(t)`.
In the complementary branch `delta>=delta0`, delta already dominates
`min(delta0,q(t))`. The equality boundary is included in this second
branch. Therefore for **every** physical U,

    delta(U,gamma) >= min(delta0,q(t)).

The rationalized root also verifies `q(0)=0` and `q(t)/t->1/2` at zero.
No numerical evaluation, optimizer selection or limiting differentiation
of U enters this bound.

## 6. Infima and sharp first-order limit

The finite lower bound is independent of U and hence survives its
infimum. Select a true range pair for analysis, giving
`t=|sin(gamma R)|`. With fixed N and C, both E and delta0 are fixed,
and for R>0, `q(t)` is eventually smaller than the positive delta0.
Since `t/|gamma|->R` and `q(t)/t->1/2`,

    liminf delta_*(gamma)/|gamma| >= R/2.

This argument works for arbitrary, even discontinuous or independently
optimized physical choices at every angle. No existence or regularity
of an optimizer needs to be assumed.

For the matching upper bound take actual identity optics and fit the
common reference chi to `gamma*(max C+min C)/2`. Every target phase
deviation then has absolute size at most `|gamma|R/2`; at sufficiently
small gamma, distance is monotone on that centered arc and is maximal
at the endpoints. The error for this one reference choice is exactly
`2sin(|gamma|R/4)`. Minimization can only decrease it. Consequently

    delta_*(gamma) <= delta(I,gamma) <= 2sin(|gamma|R/4),

giving limsup at most R/2 and the asserted two-sided limit. Identity's
own error is squeezed to the same first-order coefficient. This does
not require proving finite-angle optimality of the midpoint reference
among all phase choices, much less finite-angle optimality of identity.
For R=0 a common phase makes identity's error exactly zero, covering
the remaining case directly.

## 7. Operator metric and calibrated scope

The restricted operator maps the balanced code span **into the full
N-photon space**; it is not the compressed matrix obtained by discarding
leakage. At each common chi its norm dominates each normalized column
error. Infima over chi and U preserve the lower bound by delta_*.
For identity the restricted difference is diagonal on the balanced
basis and its norm equals the maximum diagonal-entry distance, exactly
the centered upper bound above. The identical squeeze proves R/2 for
the optimized operator metric. No converse dimension-free column-to-
operator estimate is inferred for general U.

The range and midpoint are analysis quantities and a fitted unobservable
phase reference. Identity optics uses no optimum partition, optimal mask,
training information, C* evaluation or graph-dependent device setting.
N and C must remain fixed; factorial E prevents a dimension-uniform or
practical error-threshold interpretation. Periodic parity aliases can
make sine bounds vanish at isolated angles. The theorem does not rule
them out or assert that identity is optimal at such angles.

Per-basis PNR, fidelity or trace distance to an individual target ray
cannot observe a cost phase and receive no such bound. The result
requires a common relative-phase oracle on all balanced basis states.
It is not a statement about one prepared state, selected inputs, general
sampling optimizers, alternative encodings or source resources. Ancillas,
heralding, nonlinearity, loss and filtering change the model. There is
no cumulative algorithm-error bound from merely summing these one-step
errors, and no matched-resource optimizer advantage is established.

## 8. Standalone audit verdict and obligations

| Obligation | Status | Decisive check |
| --- | --- | --- |
| Physical setting, common phase and minimizer | passed | Same P81 model; finite maximum on compact circle |
| Uniform raw leakage consequence | passed | Orthogonal target-code projection on every basis input |
| P81 constants and N-photon lift | passed | `s=sqrt(C_N)`, `b=1+Ns`, no column shortcut |
| Small-error identity pair permutation | passed | Two entries of one row exceed 7/8, including N=4 |
| Local and original physical off-diagonal mass | passed | All rails occur; 2N local off entries and contractive deletion |
| Principal permanent and factorial conventions | passed | N distinct input/output rails; normalized CF basis |
| Quadratic remainder without tau<=1 | passed | Two moved factors; every other actual entry bounded by one |
| Complementary product and four-error constants | passed | Full 2N diagonal product; no divisions |
| Quadratic root and both delta branches | passed | Exact positive root, then minimum with delta0 |
| Infimum and fixed-dimension limit | passed | Uniform-in-U bound; fixed E and delta0 |
| Identity and restricted-operator upper bounds | passed | Centered diagonal norm and one-way column domination |
| Finite-angle identity optimality, optimizer, hardware, novelty | out of scope | Not implied or claimed |

No internal gap or author correction is needed. This is a sharp
fixed-dimension first-order obstruction for the stated passive coherent
oracle task. It does not close the user's positive graph-optimization
objective or authorize an experiment, manuscript revision or QPU call.

This complete standalone argument was written before reading the
separately frozen independent P87 proof. Any subsequent comparison
must retain that distinction rather than label this source audit blind.

## 9. Comparison after the standalone argument was complete

Only after sections 1-8 were fully written and their hash reported to
ROOT did this reviewer read the independent source:

* `research/P87_independent_first_order_optimality.md`;
* original commit `17ba1d4568621870cf18d6766d79e6714654b5ac`;
* **308 lines**, SHA256
  `c23638c0345a0c5c1fdcc35d59228367303cebec3d58a830a9b3a7d894b132cb`.

Both its committed blob and producer worktree file match that hash.
The standalone 290-line audit before this comparison had SHA256
`7f4b1ccf1349a0daff9a16787141b34a9ae13510cbee17ebf5df81f7d5c2744f`,
recorded in tool output and reported before the peer read. This append
does not change its derivation or verdict. No direct contact with the
peer author occurred.

All 308 peer lines were read, giving **476 complete source lines**
audited across ROOT's candidate and this reconstruction. The peer's
before-ROOT-source derivation starts from ROOT's supplied route and
constants. This later exact-source audit is not itself blinded or an
independent discovery; shared candidate assumptions remain explicit.

Every critical implication agrees after reconstruction: all-input raw
leakage; P81's exact N-photon constants; the N=4 row-norm contradiction;
control of both local diagonal columns; physical rather than block
off-diagonal mass; exact principal permanent with unit factorials;
two moved factors without requiring tau at most one; complementary
sets partitioning all 2N rails; the `4delta+4Edelta^2` phase chord;
both delta branches and rationalized positive root; and the fixed-N
infimum/limit squeeze with identity's centered-arc upper bound.

The peer explicitly gives the sufficient upper-bound domain
`|gamma|R<=2*pi`, consistent with ROOT's and section 6's sufficiently
small-angle condition. It also gives a useful excluded-premise example:
a nonconstant additive vertex cost admits exact local phases but
generally fails complement symmetry. Thus omitting that hypothesis
would falsify the conclusion. This boundary adds no hypothesis or
repair to either audited source. The restricted-operator definition
also matches the full N-photon codomain used in section 7.

**Comparison verdict: proved as written.** No discrepancy, additional
premise, author correction or computational verification is required.
The theorem and its evidence still do not establish finite-angle
identity optimality, an optimizer advantage or hardware readiness.

Evidence operations were complete file reads, committed-blob/worktree
`shasum -a 256`, line counts, commit metadata and isolated document/Git
operations. The complete new audit was self-proofread for constants,
signs, quantifiers, notation and prose. Author mathematical-token
changes: none. No scientific import, AST, test, RNG, numerical probability
or matrix evaluation, backend, QPU, manuscript or P82/P85 draft/output
operation occurred. Existing tests are not run for this static document.
