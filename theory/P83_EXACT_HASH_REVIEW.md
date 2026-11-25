# P83 exact-source audit: gauge invariance and frustrated count laws

**Primary verdict: proved as written.** The diagonal-congruence gauge
criterion, its all-even-closed-walk equivalent, complete raw PNR
invariance, and the explicit signed four-cycle exclusion of a positive
compound-Poisson count representation pass this audit. The raw cumulant
and two-photon-per-color qualifications also pass. No optimizer advantage,
classical hardness or device implementation follows from these results.

## 1. Exact source, review mode and instructions

The complete frozen source read was
`theory/P83_GAUGE_AND_FRUSTRATION_BOUNDARY.md`, **338 lines**, commit
`d1749a1778f1107c3887f76b0c58cb715c4b94ec`, SHA256
`ec6a88bc87e236ca3f9ab38cccc2a447c3bb1a1b6f38e675a5b8a5dae7da9b06`.
The producer worktree file and the committed blob were both checked
against that hash. No source edit is requested or made.

This audit is written in the isolated `.local/p81-exact-review`
worktree, branch `research/p81-exact-review`. It applies the already-read
`AGENTS.md`, `mathbox:proof-audit` and mathematical self-proofreading
instructions. Only this new audit is changed. It is an independent-agent
exact-source audit **after** reading the source and its verdict; ROOT
supplied the gauge and signed-cycle candidate before the author derived
them. This is neither blinded reconstruction nor independent discovery.
Agreement between agents is not substituted for the algebra below.

No P82 data or output was inspected. No scientific code/import, AST,
test, RNG, matrix numerics, native backend, QPU or manuscript operation
was performed. Existing experiment records and author files are untouched.

## 2. Claim card and dependency graph

The object is a symmetric complex pair matrix `Z` of a pure undisplaced
pair-exponential source. Physical normalizability is assumed where PNR
probabilities are discussed, with `||Z||op<1`. The gauge question is
whether `Z=D B D` for a diagonal unitary `D` and real entrywise
nonnegative `B`. Zeros impose no phase constraint; nonzero diagonal
entries are support loops. The factorization, if it exists, forces
`B=|Z|` entrywise.

The exact logical dependencies are:

    diagonal unitary congruence
       -> identical singular norms and Gaussian normalization
       -> diagonal number-basis phase action
       -> identical complete raw PNR law at every photon total
    support phase equations theta_i+theta_j=phi_ij
       -> tree propagation with root parity
       -> consistent residual edge constraints
       <-> zero alternating phase for every closed even walk
    explicit real signed four-cycle
       -> Z^2=2t^2 I and a physical normalized source
       -> hafnian cancellation at 1111
       -> negative 1111 coefficient of log PGF
       -> no positive compound-Poisson count representation
    complete-event pair-exponential coefficients
       -> gauge-invariant raw four-mode cumulant formula
       -> no conditional phase effect for two CF photons per color

The tree construction, determinant identity, hafnian phase rule and both
coefficient calculations are internal algebra. The compound-Poisson
definition, analytic power-series conventions and elementary matrix
identities are stated explicitly. No empirical output, external theorem
or novelty assertion is load-bearing. P78/P80 are used only to identify
which previously audited sampler applies after the exact gauge reduction;
their separate resource premises are retained.

## 3. Gauge invariance, including collisions and vacuum

If `Z=D B D`, then

    Z Z^dagger = D B^2 D^dagger,
    det(I-Z Z^dagger) = det(I-B^2),
    ||Z||op = ||B||op.

This is congruence by `D` on both sides, rather than similarity by `D`
and `D^dagger`. For the repeated-label matrix belonging to occupation
`n`, every matching uses each label occurrence once. Thus

    haf(Z_n) = product_i d_i^(n_i) * haf(B_n).

The rule includes a physical diagonal entry appearing between repeated
label occurrences; no diagonal support term is silently omitted. It
preserves all normalized count probabilities, not merely collision-free
or fixed-number accepted probabilities. Vacuum is unchanged as well.
Equivalently the creation-operator phase rotation is diagonal in the
measured Fock basis. A common graph decoder cannot change this equality.

The norm argument is legitimate for this gauge class without a missing
general-complex Takagi theorem: real symmetric `B` can be orthogonally
diagonalized, its one-mode pair norms normalized, and the result carried
through the diagonal phase unitary. Negative real eigenvalues cause no
problem for the norm series. P78 then applies to `B`; the rational P80
variant requires `B` rational as separately stated. No arbitrary-phase
recognition complexity or finite-bit phase arithmetic is declared free.

## 4. Necessary and sufficient support criterion

All phase equalities below live in `R/(2*pi*Z)`. In each connected
nonzero-support component choose a root and a spanning tree of non-loop
edges. The tree recurrence gives exactly

    theta_v=alpha_v+sigma_v theta_r,
    sigma_v=(-1)^(tree depth),
    alpha_v=phi_(parent,v)-alpha_parent.

For a residual edge `uv`, substituting this expression yields
`(sigma_u+sigma_v)theta_r=tau_uv`, with
`tau_uv=phi_uv-alpha_u-alpha_v`. Opposite tree parities therefore require
`tau_uv=0`; equal parities require the same value
`2 theta_r=sigma_u tau_uv` for every such edge. A loop is precisely the
equal-parity case with `u=v`, so its diagonal phase is fully included.
If there is a residual half-phase condition, its two roots in the circle
both exist; otherwise the root phase is free. This proves both directions
without ignoring a parity or a square-root ambiguity.

The closed-walk version is also exact. If a walk has edge phases
`phi_j`, its alternating sum telescopes to zero for even length and to
`2 theta_start` for odd length. Conversely the fundamental rooted walk
through a residual edge has alternating phase `sigma_u tau_uv`. Its
length is even for opposite parities and odd for equal parities. Two
odd rooted walks concatenate to an even walk, and their alternating
sums subtract. Requiring zero for **every** even closed walk therefore
forces precisely the residual conditions above, hence constructs `D`.

Repeated vertices, repeated edges and loops cannot be removed from this
criterion. A backtrack of length two gives zero identically, but
concatenated odd cycles can carry an essential even-walk obstruction.
Disconnected components are independent. An isolated zero mode is free;
a singleton loop has one removable half phase. Trees are gaugeable.
Connected bipartite loop-free support has one continuous root freedom.
Compatible nonbipartite support has two root choices differing by a
common sign; an isolated odd cycle is always compatible.

## 5. Falsification checks for tempting weaker criteria

For triangles `1231` and `1451` sharing only vertex 1, take all phases
zero except `phi_51=pi`. The first triangle gives `2 theta_1=0`, the
second gives `2 theta_1=pi`. No simple even cycle exists, but their
length-six concatenation is a frustrated even closed walk. Thus the
strong walk criterion is necessary; simple-even-cycle checking would
be false. Scaling the finite symmetric matrix sufficiently small keeps
this counterexample physical without changing its phase constraints.

For two vertices with a loop at each, elimination of the root gives
`phi_11+phi_22-2 phi_12=0`. A positive scalar multiple of
`[[1,i],[i,1]]` violates it. Its product with its adjoint is twice the
squared scalar times the identity, so it can also be physical. The
source's statement that the loops demand real signs uses that positive
scalar convention; any common scalar phase can first be absorbed by
the already-proved global diagonal congruence. No conclusion depends
on treating a genuinely complex scalar as a positive number.

A triangle of negative real edges is gaugeable by `D=i I`, illustrating
why ordinary directed flux or real signed-graph switching is a different
problem. On a loopless four-cycle the only residual invariant is
`Phi=phi_12+phi_34-phi_14-phi_23`. Components on at most three loopless
vertices are trees or a triangle, so four vertices are indeed minimal
in that restricted support class. The two-loop example shows why this
minimality must not be stated for arbitrary support with diagonals.

## 6. Physical signed cycle and independent coefficient checks

For the source's matrix `Z=t A`, each row of `A` has squared norm two,
and the two length-two paths joining either opposite pair cancel.
Adjacent-vertex entries of `A^2` vanish by bipartiteness. Therefore

    Z^2=2t^2 I_4,
    ||Z||op=sqrt(2)t < 1  for 0<t<1/sqrt(2),
    p_0=sqrt(det(I-Z^2))=(1-2t^2)^2 > 0.

The two nonzero perfect-matching products are `t^2` and `-t^2`.
Consequently `haf(Z)=0` and the raw 1111 probability is exactly zero
throughout that physical interval. The magnitude matrix has norm `2t`.
On `0<t<1/2` both sources are physical and their hafnians differ; on
the rest of the signed source's physical interval the magnitude source
is not a strict contraction. Neither part can be a hidden phase gauge.

For real symmetric signed `Z`, the ordinary PGF domain is `0<=z_i<=1`;
one may also use the analytic polydisc `|z_i|<=1` near zero. In that
domain

    ||sqrt(D_z) Z sqrt(D_z)||op
       <= (max_i |z_i|) ||Z||op < 1.

This is the domain of the source's contraction/convergence sentence.
No assertion for unrestricted `z` is needed or justified. The analytic
germ around zero already suffices for the log-coefficient argument.
On the real PGF domain the weighted pair-state norm and the determinant
identity give

    log G(z)=sum_(l>=1)
       [Tr((D_z Z)^(2l))-Tr(Z^(2l))]/(2l).

For the squarefree degree-four monomial only the length-four term can
contribute. Its four roots and two orientations each have product
`-t^4`, so the coefficient is `-8t^4/4=-2t^4`.

Separately, write the constant-normalized series as
`G/p_0=1+F_2+F_4+...`. Here `F_2` is `t^2` times the sum of the four
edge monomials. The squarefree coefficient in `F_4` is zero. Its
coefficient in `F_2^2` is `4t^4`, from the two disjoint edge matchings
and both product orders. Hence the coefficient in
`log(G/p_0)=F_2+F_4-F_2^2/2+...` is again `-2t^4`. The constant
`log p_0` has no effect. No conditioning or count rejection occurred.

## 7. Exact compound-Poisson exclusion and its limits

For nonzero nonnegative integer count jumps `k` with rates `nu_k>=0`,
a compound-Poisson law has

    G_CP(z)=exp(sum_k nu_k (z^k-1)).

Positive vacuum mass requires finite total rate, with
`sum nu_k=-log p_0`. A deterministic nonzero count drift would make
vacuum impossible. Thus the analytic logarithm with real constant
`log p_0` has coefficient `nu_k>=0` at every nonzero monomial. The
negative 1111 coefficient is a direct contradiction. The argument
excludes arbitrary nonnegative count-vector jumps, not just a proposed
closed-walk implementation.

It does not exclude a different positive latent-variable construction,
rejection, sequential sampling or any other classical algorithm. Nor
does the gauge iff criterion characterize all laws that happen to be
compound Poisson: it characterizes the specific congruence to `|Z|`.
The four-mode example has fixed dimension and elementary pairing
cancellation, with no computational-hardness or novelty implication.

## 8. Raw statistic, phase dependence and graph-objective scope

The complete-event formulas on four distinct modes give

    p_(ij)/p_0=|Z_ij|^2,
    p_1111/p_0=|M_1+M_2+M_3|^2,
    M_1=Z_12 Z_34, M_2=Z_13 Z_24, M_3=Z_14 Z_23.

Every unlisted mode is vacuum. The squarefree log coefficient subtracts
the three pair-probability products divided by `p_0^2`, leaving exactly

    2 Re(M_1 conj(M_2)+M_1 conj(M_3)+M_2 conj(M_3)).

All three `M_j` acquire the same phase under `D Z D`; the statistic is
gauge invariant. On the four-cycle this is `2|M_1 M_3| cos(Phi)`, so
the signed source gives `-2t^4`. With a repeated 22 occupation the
hafnian is `Z_11 Z_22+2 Z_12^2`, providing the analogous loop invariant.
These are coefficient identities, not vacuum-conditioned probabilities.

Four photons are the first pair-exponential order containing competing
matching monomials. Raw vacuum and raw two-photon probabilities can
already depend on source phase through their common normalization;
there is no broader raw phase-blindness claim. At two CF photons per
independent color, each relevant hafnian has just one edge. Conditional
complementary-subset weights therefore depend only on the squared
edge magnitudes. Raw normalization and acceptance can still change.

No graph optimum is required to specify these motifs, but a negative
raw coincidence cumulant is not a lower decoded cut cost. The source
correctly retains full-source vacuum, all raw pulses, acceptance,
preparation and uncertainty costs. Marginalized count events, a rare
vacuum denominator, another source architecture or a hardware edge-phase
capability would require separate justification. None is inferred here.

## 9. Obligation matrix and remaining implication

| Obligation | Status | Decisive evidence |
| --- | --- | --- |
| Congruence rather than similarity | passed | Edge phase sums and `Z Z^dagger=D B^2 D^dagger` |
| Collisions and raw normalization | passed | Repeated-label phase factor and unchanged vacuum |
| Support iff, including zero/loop/odd cases | passed | Tree residual equations and two-root compatibility |
| All-even-walk equivalence | passed | Fundamental walks and subtraction of odd walk phases |
| Simple-even-cycle shortcut falsified | passed | Bowtie's two incompatible root half phases |
| Signed-cycle physicality | passed | `Z^2=2t^2 I`, strict interval and vacuum determinant |
| Hafnian and log coefficient | passed | Exact cancellation; separate trace and series counts |
| PGF convergence domain | passed | Standard unit polydisc; no unrestricted-variable claim |
| Positive compound-Poisson exclusion | passed | Nonnegative log coefficients forced by finite rate |
| Raw cumulant and two-photon qualification | passed | Complete events and single-edge hafnians |
| Arbitrary classical hardness/optimizer gain | out of scope | Not implied or claimed |
| Hardware preparation, statistics, novelty | out of scope | No evidence or authorization supplied |

There is no remaining internal gap and no author change is required.
The strongest safe result is an exact reduction of the gauge class to
the existing nonnegative-source controls, together with a physical
counterexample to their unrestricted positive compound-Poisson
extension. The next scientific obligation remains a physically paid,
optimum-blind mechanism with favorable cost-relevant raw statistics and
independently optimized controls. This audit does not supply it.

Checks used only complete file reads, commit metadata, committed-blob
and worktree `shasum -a 256`, line counts and document/Git operations.
The complete audit was self-proofread for notation, coefficient factors,
scope and prose after its mathematical review. No mathematical token
in the author source was changed. No computation-based scientific
verification or existing test suite was run for this static document.
