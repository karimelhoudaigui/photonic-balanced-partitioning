# P69 exact-hash independent review of the author's proof

Primary verdict: **proved as written**, under the source's explicit ideal
unitary, source, target, fixed-block and raw-attempt hypotheses. No
mathematical gap was found in the finite bound, its stated asymptotic and
chain consequences, the Cayley corollary, or the symbolic counterexample
to extending the Hamiltonian-rank claim to the exponential.

## Artifact and independent provenance

Reviewed source: `research/P69_low_rank_transport_obstruction.md`, current
SHA256
`37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`.
The author freeze is preserved at `f7f802f`; the current source includes
the single clarification in commit
`48321304296b9492d41294a5a8c96562550f8ffc`.
That exact diff was read: states outside the four bad states and the two
targets are uphill, while other bad states have equal cost. It changes
no formula, constant or physical model.

This review follows the reviewer's independently derived and committed
`theory/P69_independent_low_rank_transport.md`, commit
`e5477a74d5282bb752e759780046826b63196520`, SHA256
`fb4f7f828bcba0ad644971ba8851c219599dc73a20d45071d7f63bddc3a2b620`.
That 428-line artifact was frozen before reading the author's P69 proof
and is unchanged. The present comparison was not blind: the source's own
verdict was visible, but it is not a premise of this review. ROOT's prior
reading and rederivation are likewise not substituted for an obligation.
The separate peer P66 proof was not needed or consulted; the graph barrier
and optical bounds can be reconstructed from definitions.

Review date: 2026-11-25. Worktree: `.local/p66-dark-barrier`, starting at
the independent proof checkpoint above. Only this new review file is
written. Skills: `mathbox:proof-audit` and final mathematical proofreading
with `mathbox:proofread-math`. There is no external theorem or computation
leaf requiring citation or execution.

## Normalized claim and dependencies

The source uses blocks of size d=2L, L>=2, and the notation

    U = [ A C ],     rank C = rank D = q <= r <= 2L,
        [ D B ]

with input blocks as columns and output blocks as rows. A normalized
source occupies L distinct vertex modes in each block with one photon per
mode. The targets occupy all 2L modes of exactly one block. Every coherent
operation from this prepared source to detection belongs to the NET U.
The rank is relative to the same physical input/output blocks used by the
source and decoder.

For r>=1 the claimed bound is p=min(1,2ab), with

    a=min(1,r(r+1)...(r+L-1)/L^L),
    b=1 for r>=L,
    b=min(1,((L+r)/(2r))^r*((L+r)/(2L))^L) for 1<=r<L.

For r=0 the probability is zero. The dependency chain is

    unitarity -> equal actual ranks and IN/OUT dark intertwiners
    normalized CF Fock states -> Gram permanents
    scalar Gaussian integrals -> pairing and rising-factorial moments
    source AM-GM + target PGF -> two projection-norm bounds
    two support identities + unitarity -> target probability bound
    uniform conditional hazard + P66 cost gap -> chain bounds.

The depth, asymptotic and Cayley conclusions are separate consequences.
The exponential-Hamiltonian example is a separate counterexample to an
overextension, rather than a counterexample to the finite optical theorem.

## Critical implication checks

### Moving projectors and actual rank q versus upper bound r

If x is in ker D, U(x,0)=(Ax,0). Unitarity makes this map isometric and
orthogonal to every image U(0,y); hence A ker D is contained in
(range C)^perp. Their dimensions give rank D>=rank C. The identical
argument for B ker C gives the reverse inequality. Equality of dimensions
then upgrades both inclusions to equalities. This proves the source's
actual rank q and its stated input/output dark spaces without assuming
fixed dark vectors.

U maps each input dark subspace onto its named output dark subspace.
Since it is unitary, their orthogonal projectors intertwine; they need not
commute with U as a single projector. The Fock number operators and their
spectral projectors inherit that intertwining. Input and output bright
spaces each have dimension q. Replacing q by the larger integer r is
safe in the rising factorial and in (1-s)^(-q)<=(1-s)^(-r), 0<=s<1.
The q=0 case is handled separately, including when the stated upper bound
r is positive. The theorem does not identify r with an actual dimension
unless the cross rank attains that bound.

### CF factorials, Gaussian pairing and source AM-GM

For m distinct singly occupied modes, symmetrized-tensor expansion or
creation/annihilation commutation gives the permanent as the CF matrix
element of Gamma(M). The factorial normalization is m! with m equal to
the photon count in that matrix element: m=L for the source block and
m=2L for the full-block target. It cancels in both cases; no L! or (2L)!
survives in the displayed permanent identities.

The complex Gaussian density exp(-|g|^2)/pi gives zero mixed moments for
unequal holomorphic/antiholomorphic powers, and moment a! for equal powers
a, directly by angular integration and the radial factorial integral.
For independent coordinates, matching multiplicities counts the allowed
pairings with exactly those factorials. This verifies the author's Wick
identity without importing it as an external result. The multinomial
sum for q coordinates gives

    E||g||^(2L) = L! * binom(L+q-1,q-1)
                = q(q+1)...(q+L-1),       q>=1.

There is one L! contribution for each weak composition of L, counted by
placing q-1 separators among L+q-1 positions. The q=0 positive moment
is zero. Thus no rank offset, complex-versus-real Gaussian factor of two,
or missing source factorial is present.

For an arbitrary rank-q projector P=VV^dagger, restrict the isometry V
to the L occupied rows, T=V[SB,:]. The source projection probability is
per(P[SB,SB])=E product_i |(Tg)_i|^2. Since T^dagger T<=I, pointwise
AM-GM gives

    product_i |(Tg)_i|^2 <= (||Tg||^2/L)^L
                            <= (||g||^2/L)^L.

Taking expectations gives the claimed rising-factorial source bound;
the probability cap at one is valid. This check needs no flat projector
diagonal or favorable selected vertices.

### Target PGF, Chernoff optimizer and two-support insertion

For the full-CF target, Gamma(I+sP)=(1+s)^(N_P). Its expectation is
per(I+sP), not a distinguishable-particle moment. Expanding identity
factors fixes every complementary index of the permutation, giving

    per(I+sP)=sum_I s^|I| per(P[I,I])
            =E product_i (1+s|(Vg)_i|^2).

The empty permanent is one. Since V is an isometry on all target-block
rows, the last expression is at most E exp(s||g||^2)=(1-s)^(-q).
This establishes the target tail bound with all normalization factors.
For 1<=r<L, the logarithmic derivative of its Chernoff envelope is
r/(1-s)-L/(1+s), with positive second derivative and minimizer
s=(L-r)/(L+r). For r=L the minimum is the boundary s=0; for r>L the
trivial cap one is used. No expression dividing by r is applied at r=0.

For target CA, the source has at most L photons in its input CA dark
space; the target has zero photons in its output CB dark space.
Inserting those two support projections and intertwining them gives

    <t|Gamma(U)|s> = <Pi_out t|Gamma(U)|Pi_in s>.

The source norm squared is the all-bright CB probability bounded by a;
the target norm squared is the probability of at least L output CA
bright photons bounded by b. Cauchy-Schwarz gives ab. The second target
uses the exchanged projections, and its orthogonal event probability
adds. A common projector or conserved occupation across attempts is never
needed. If actual q=0, block photon totals cannot change and neither
target is reachable.

## Asymptotics, adaptive histories and physical scope

The author's growing-rank estimate is valid. Monotonicity of log gives

    sum_{j=0}^{L-1}log(r+j) <= integral_r^(r+L) log x dx,
    log a <= min(0,L[h(alpha)-1]),
    alpha=r/L,   h(alpha)=(1+alpha)log(1+alpha)-alpha log alpha.

The target formula equals exp(-L I(alpha)) for 0<alpha<1, with
I(alpha)=(1+alpha)log 2-h(alpha). Its derivative is
log(2alpha/(1+alpha))<0 and I(1)=0. It follows that r<=alpha0 L,
0<alpha0<1, yields the stated uniform exponential target bound.
For positive r=o(L), h(alpha)->0 and I(alpha)->log 2; the source and
target factors give p<=exp(-L log(2e)+o(L)). Rank-zero subsequences
have p=0 and obey this upper bound trivially.

For fixed integer r and L>r, the exact finite envelope in source section
8 is checked by multiplying

    a <= e L exp(-L) (L+r-1)^(r-1)/(r-1)!,
    b <= e^r (L+r)^r 2^(-L)/(2r)^r.

The factor two for the targets gives precisely the coefficient printed
there. It agrees with the looser polynomial envelope in the prior
independent proof. None of these expressions asserts attainability.

The P66 cut decomposition supplies the graph gap independently: at least
two partial cliques contribute 2M(L-1); in the connected case the cross
cut is at least 2wL^2, while the bad cost is 2Lh+2wL^2. Thus only the two
whole-block targets improve, other bad states tie, and outside those six
states the increase is at least g=2M(L-1)-2Lh. The current clarification
states exactly this classification.

Before a zero-temperature improvement, each accepted current source has
L distinct occupied modes per block. Conditional on any past and random
markings used to choose U before the draw, the same raw bound applies
if the NET cross rank is at most r. No covariance or independence between
attempts is used. The tail lower bound (1-p)^T, and hence expected attempts
at least 1/p, follow. Expected injected photons at least K/p requires an
execution continuing until success, as the author explicitly states.
Actual capped or aborted runs receive the finite-budget success bound.

For finite temperature, the first accepted exit from the bad set is either
a direct target or an uphill move of increase at least g. The stated
Metropolis rule exp(-beta_j Delta) gives the thermal term. For adaptive
random beta_j chosen before the draw, the indicator-weighted expectation
in the source is required and correct. A different Hastings acceptance
rule is not silently covered. No conclusion of Gibbs stationarity, actual
P65 thermal trapping or typical uniform initialization follows.

Independently propagated distinguishable photons have crossing
probabilities with sum at most Tr(C^dagger C)<=q<=r over the occupied
vertices. AM-GM bounds their independent product by (r/L)^L; no individual
probability bound r/L is needed. The separate min(1,2(r/L)^L) estimate
therefore survives independent reoptimization and establishes no ordering
between bosonic and distinguishable performance.

The raw model includes collisions and full photon counts. Physical source
filters, ancillas, changed decoding, intermediate measurement and internal
noise are excluded. Post-unitary independent uniform loss only removes
full-K-photon targets without conditioning. All coherent rerouting must
be included in U relative to the same blocks; relabeling alone cannot
remove its physical cross rank.

## Composition, Schur sign and the exponential counterexample

For the same block partition, the cross block of a product is a sum of
two products, so its rank is at most the sum of the two cross ranks.
The coherent-layer consequence follows by induction. A parallel layer
with many cross couplers can have extensive rank, as the source notes;
this is not a generic circuit-depth theorem.

For H=[X Z;Z^dagger Y], set E=I-itX. In I-itH the off-diagonal blocks
are -itZ and -itZ^dagger. Thus the Schur complement is

    S=I-itY - (-itZ^dagger) E^(-1) (-itZ)
      =I-itY + t^2 Z^dagger E^(-1) Z.

The plus sign is correct. Hermiticity and real t make E and I-itH
invertible, and block elimination makes S invertible. The off-diagonal
inverse block is +it E^(-1) Z S^(-1). Therefore the Cayley cross block
is 2it E^(-1) Z S^(-1), preserving the rank of Z for t!=0 and vanishing
at t=0. Within-block corrections do not affect this rank conclusion.

The exponential example was checked symbolically by hand, without a
program. Take real diagonal X=diag(x1,x2), Y=diag(y1,y2), and Z=J2,
the two-by-two all-ones matrix. The cross blocks of H,H^2,H^3 are

    Z,
    XZ+ZY,
    X^2 Z+XZY+ZY^2+ZZ^dagger Z.

Here ZZ^dagger Z=4J2, so the author's entry expansion is exact through
order t^3:

    C_ij(t)=it-t^2(xi+yj)/2
                -it^3(xi^2+xi*yj+yj^2+4)/6+O(t^4).

Put delta=(x1-x2)(y1-y2). The determinant's order-t^2 terms cancel
because its leading matrix is rank one. The order-t^3 coefficient is
zero because the alternating sum of xi+yj vanishes. At order t^4 the
two contributions are

    (it) times the alternating cubic coefficients:  +delta/6,
    determinant of the quadratic coefficients:      -delta/4.

Explicitly, the latter is
[(x1+y1)(x2+y2)-(x1+y2)(x2+y1)]/4=-delta/4.
The former uses the alternating sum of xi^2+xi*yj+yj^2+4, which is delta,
and i*(-i)=+1. Hence

    det C(t) = -delta*t^4/12+O(t^5).

This checks the requested negative sign and the remainder order: an
O(t^4) entry is multiplied by an O(t) entry in a determinant term.
For delta!=0 the analytic determinant is nonzero for sufficiently small
nonzero real t, so rank C(t)=2 although rank Z=1. Local uncoupled
spectators embed the example in blocks of dimension 2L with L>=2 without
changing those ranks. It correctly refutes the generic exponential
Hamiltonian-rank extension while leaving the resolvent/Cayley proof intact.

## Obligations, remaining gap and validation

| Obligation | Result |
|---|---|
| Exact current source hash and clarification diff | Passed |
| Equal actual ranks, q<=r, moving IN/OUT projectors | Passed |
| CF factorial normalization and Gaussian Wick identity | Passed by direct reconstruction |
| Source contraction/AM-GM and target permanent PGF | Passed |
| Chernoff cases r=0, r=L and r>L | Passed |
| Two-support identity with different projectors | Passed |
| Marked histories, finite beta and expected photons | Passed under stated source/update conditions |
| Fixed-rank and r=o(L) envelopes; fixed-fraction rate | Passed with printed constants |
| Separate D bound | Passed as an upper bound only |
| Product rank and Schur sign | Passed for fixed blocks and real t |
| exp(itH) expansion and determinant sign | Passed by hand; valid counterexample |
| Generic source/decoder/noise or all-graphs claims | Not claimed and outside scope |
| Positive optimizer, runtime advantage and novelty | Not established |

There is no remaining mathematical gap in the normalized source claim.
No correction to its current formulas or hypotheses is requested. The
strongest safe conclusion remains a uniform ideal low-rank transport
bound with a restricted warm-start optimization corollary on the explicit
easy classical family. A finite computation could check implementation
conventions later; none is needed to complete this proof audit or
authorized by it.

Validation consisted of text reads, exact SHA256 checks, reading the
clarification diff, and the independent hand derivations recorded here.
Git whitespace checks accompany this report's commit. No imports, tests,
scientific computations, seeds/draws, experiments or QPU calls were run.
Final mathematical proofreading covered the whole review, particularly
block names, q/r distinctions, factorials, expectation quantifiers,
Schur signs and the order-t^4 determinant. The 428-line independent proof
and all original source artifacts remain unchanged.
