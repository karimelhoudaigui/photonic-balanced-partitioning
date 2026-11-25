# P68 independent review: joint graph/current-subset covariance

Primary verdict: **proved as written**, for the ideal, raw-attempt,
collision-inclusive update model stated in the source and the P66
Metropolis convention. The covariance must hold for every realized
deterministic map, not merely for its distribution. The bound is vacuous
at L=2. It is an upper bound on success for specified warm starts, not an
optimization advantage, a statement about generic starts, or a lower bound
for unrestricted graph algorithms.

## Exact target and review provenance

Audited artifact:

- `research/P68_current_covariance_rank_two_audit.md` in ROOT's worktree;
- freeze commit `1f12a8a5f6850e40c30b21a1afd51bf5e5156b49`;
- SHA256 `0c587b01c3a37bac5b0ff94fb03546d451babb69695a35ff1d702af8e78f264b`.

Review authored on 2026-11-25 in `research/p66-dark-barrier`, starting from
`2bcf84b82781cdf2bf8379e61fa5e9071aa25bbc`. Only this review file is added.
The source author's verdict was visible, so this is not a blind review.
The symmetry action, Fock overlaps, moment identity and trajectory argument
were reconstructed independently below. The reviewer's earlier P66 proof
is background, not independent corroboration of that earlier proof. The
separate peer P66 proof and P67 proof/counterexample were not read for this
review; their conclusions are not used as unproved leaves here.

Skills applied: `mathbox:proof-audit` and final self-review with
`mathbox:proofread-math`. There are no load-bearing computations or external
theorem citations. No scientific imports, tests, numerical computation,
graph generation, seeds/draws, backend experiment or QPU call was performed.

## Normalized claim and dependency graph

Let L>=2 be an integer. Four cliques A1,A2,B1,B2 have size L and internal
edge weight M>0. The two pairs A1,A2 and B1,B2 are each joined by a perfect
matching of weight h>0, with M(L-1)>Lh. Set CA=A1 union A2 and
CB=B1 union B2. Cross-block edges are absent or all have the same weight
0<w<h/L. A feasible subset has size K=2L. The start belongs to

    B = { Ai union Bj : i,j in {1,2} }.

For every permutation matrix P the allowed deterministic maps satisfy

    U(P A P^T, P S) = P U(A,S) P^T,

and are unitary on the 4L vertex modes. Every attempt freshly prepares
the normalized Fock state with one photon per current selected vertex.
Full PNR is measured. A collision consumes an attempt and leaves the
current subset unchanged; there is no conditioning, retry, repair or
external candidate insertion. Non-uphill collision-free moves are
accepted; an uphill move of cost increase Delta is accepted with
probability exp(-beta Delta), as in P66. This is the acceptance convention
used by the finite-temperature statement.

Write

    g = 2M(L-1)-2Lh > 0,
    a = L!/L^L,
    b = min(1, (L+2)^2/16 * ((L+2)/(2L))^L),
    p = min(1, 2ab).

The claim is a uniform probability bound p for proposing either of the
two improving whole-block targets from any S in B. It implies the stated
zero-temperature tail, waiting-time and photon bounds and the separate
finite-temperature first-exit bound. The distinguishable-particle claim
is a separate upper bound min(1,2L^(-L)), not a comparison of two engines.

The complete implication chain is:

    graph cut decomposition -> only two targets; uphill gap g
    exact joint covariance -> commutation with stabilizers of (A,S)
    stabilizer averages -> common block-dark projectors
    normalized source and target Fock states -> two projection norms
    two support identities + unitarity -> direct bound p
    conditional hazard + acceptance rule -> trajectory conclusions.

Each leaf is an internal argument, an explicit model convention, or the
unitarity/covariance hypothesis. No numerical surrogate or assumption of
Gibbs stationarity is required.

## Reconstructed critical implications

### 1. The graph gap remains the right first-exit gap

If a clique has x selected vertices, its contribution is Mx(L-x).
A partial clique contributes at least M(L-1), and exactly one partial
clique is impossible when all occupancies sum to 2L. Thus every feasible
subset outside the six unions of two whole cliques has within-clique cut
at least 2M(L-1).

With no cross-block edges, four states in B have cost 2Lh and the two
targets CA,CB have cost zero. In the connected case put x=|S intersect CA|.
Its cross-block cut is

    w[x^2+(2L-x)^2] >= 2wL^2.

Bad and good costs are respectively 2Lh+2wL^2 and 4wL^2. The latter is
smaller precisely because w<h/L. Every partial-clique state has cost at
least the bad cost plus g. This proves the graph leaf directly, without
depending on the peer P66 proof. In source section 1, “every other balanced
subset” is understood as outside B and the two targets: other members of
B have equal cost, as the later chain argument explicitly uses.

### 2. Stabilizer, fixed spaces, and the invariant actually obtained

Choose labels so that the A matching pairs vertex r in A1 with vertex r
in A2. For each sigma in S_L, apply sigma simultaneously to the r labels
in both A cliques and do nothing on CB. All weighted edges are preserved,
including constant cross-block edges, and every S in B is preserved.
This is a subgroup of the stabilizer of (A,S). Its two orbits in CA are
A1 and A2, each transitive, including when L=2.

Let b_Ai=L^(-1/2) sum_{v in Ai}|v>. The fixed vectors in CA are exactly

    BA = span{b_A1,b_A2}.

The subgroup average on the full one-particle space is the orthogonal
projector R_A=P_BA direct-sum I_CB: an invariant vector is constant on
each orbit, and finite-group averaging projects orthogonally onto those
vectors. Exact joint covariance implies that U(A,S) commutes with each
group element, hence with

    P_DA = I-R_A.

Repeating with B matching pairs proves commutation with P_DB, where
DB is the orthogonal complement of span{b_B1,b_B2} inside CB.
These subspaces and projectors do not depend on which Ai,Bj form S.

Only DA and DB as whole block subspaces are asserted invariant. Inside
DA, the two copies of the nontrivial S_L representation may mix: dark
photons can move between A1 and A2. The proof never requires conservation
of either clique's separate dark occupation. Likewise for DB. The Fock
lift Gamma(U) commutes with N_DA=dGamma(P_DA) and N_DB=dGamma(P_DB).
These are per-proposal invariants; PNR and source repreparation do not
conserve them along the measured classical trajectory.

### 3. Source normalization and target moment factorization

For S=Ai union Bj, the source has L photons in CA, so N_DA<=L on its
support. In CB its photons occupy Bj, and its other clique is vacuum.
Projection to N_DB=0 replaces each occupied creation operator by
b_Bj^dagger/sqrt(L). The projected CB vector is

    (b_Bj^dagger)^L/L^(L/2) |0>
       = sqrt(L!)/L^(L/2) |L photons in b_Bj>.

Thus its squared norm is exactly a=L!/L^L. No input factorial is missing:
the original occupied vertex modes each have occupation one. The second
CB bright mode is empty in the input, so rank two does not introduce an
extra factor two into a.

For target |1_CA>, the two full-clique Fock factors are a tensor product.
Let ni be the occupation of b_Ai. Since these number operators act on
separate factors, their joint spectral distribution factorizes. For a
single size-L clique, applying b^m to the full collision-free state gives
one orthogonal hole-set vector for each m-element subset, with coefficient
m!/L^(m/2). Hence, for 0<=m<=L,

    E[(ni)_m] = (m!)^2 binom(L,m)/L^m,
    E[(1+s)^ni] = sum_{m=0}^L (L)_m (s/L)^m <= 1/(1-s),
    0<=s<1.

The finite binomial expansion divides the factorial moment by m!, which
leaves exactly (L)_m in the PGF. This is not an independent-photon model.
Multiplying the two PGFs yields

    P(n1+n2>=L) <= [(1-s)^2(1+s)^L]^(-1).

The derivative of the logarithm of this last expression is
2/(1-s)-L/(1+s), with positive second derivative. For L>2 its minimum
is at s=(L-2)/(L+2), giving the stated b. At L=2 the minimum is the
boundary s=0 and b=1. Then a=1/2 and p=1: the statement is valid and
vacuous, not a nontrivial finite-L obstruction at that boundary.

### 4. The two-support identity closes the amplitude argument

For source x=|1_S> and target y=|1_CA>, put

    Q=1_{N_DA<=L},   R=1_{N_DB=0},   Pi=QR.

The source satisfies Qx=x, the target satisfies Ry=y, and both projections
commute with Gamma(U). Moving R from the target to the source and Q from
the source to the target proves

    <y|Gamma(U)|x> = <Pi y|Gamma(U)|Pi x>.

Its squared modulus is at most ||Pi y||^2 ||Pi x||^2 <= ab.
This uses the separate support statements, not just commutation of Pi.
Exchange A,B for target CB; the two output Fock events are orthogonal,
so their probabilities sum to at most 2ab and at most one. This proves p.

### 5. History, waiting time, photons, temperature and loss

Let tau be the first strictly improving raw attempt, with tau=infinity
if none occurs. Before success at zero temperature the accepted current
is still in B. Condition on the complete past and on any controller choice
made before the next fresh proposal. Each realized selected map obeys the
same projector commutations, so its conditional success probability is at
most p. It follows by induction, without independent successes, that

    P(tau>T) >= (1-p)^T,
    P(tau<=T) <= min(1,Tp),
    E[tau] = sum_{T>=0} P(tau>T) >= 1/p.

The expectation is an extended expectation and may be infinite. Exactly
K=2L source photons are injected per attempt, so the expected injected
photons are at least K/p for an execution continuing until success.
Capped or aborted runs do not inherit that lower bound on their actual
photon expenditure. They retain the finite-budget success bound.

At finite beta, stop the argument at the first accepted exit from B.
The conditional probability of a direct target is at most p. Every other
accepted exit increases cost by at least g, so the Metropolis acceptance
contributes at most exp(-beta_j g). This proves the stated deterministic
schedule bound. If beta_j is history-random and selected before the draw,
the unconditional version is

    min(1, Tp + sum_j E[1_{no accepted exit before j} exp(-beta_j g)]).

Deterministic almost-sure lower bounds on beta_j give a weaker numerical
bound. No random right-hand side may be substituted without expectation.
At beta=0, or beta of order 1/L with g of order L, a useful exponential
thermal obstruction need not follow. No Gibbs or detailed-balance claim
is supplied for a general current-dependent U. In particular a different
Hastings rule with an extra proposal-ratio factor is not the stated
acceptance convention and would need a new first-exit analysis.

Independent uniform loss after the ideal U can only delete a successful
K-photon target event. With no survival conditioning or repair it cannot
increase the raw success bound. General internal noise is not covered.

### 6. Explicit envelope and the separate distinguishable bound

The elementary integral bound on log(L!) gives a<=e L exp(-L).
The inequality (1+2/L)^L<=e^2 gives

    b <= e^2 (L+2)^2 2^(-L)/16,
    p <= e^3 L(L+2)^2 (2e)^(-L)/8.

All caps are in the safe direction; this envelope proves asymptotic
exponential decay without asserting that p is the actual optimized
success probability.

For a vertex v in the selected CB clique, its projection onto BB has
squared norm 1/L, and the rest lies in DB. Invariance of DB prevents
that rest from reaching CA. Therefore an independently propagated
distinguishable photon at v crosses to CA with probability at most 1/L.
All L CB photons must cross for the CA target, so independence of those
distinguishable trials bounds this event by L^(-L), even before imposing
the target's collision-free pattern. The CB event is bounded identically.
The result min(1,2L^(-L)) is uniform over separately optimized allowed
matrices. It neither orders B and D performance nor certifies an
interference advantage. It requires the distinguishable product-source
model and the same pathwise matrix class; conditioning on CF is excluded.

## Obligation matrix, gaps and validation

| Obligation | Result |
|---|---|
| Weighted graph gap, connected target cost and h,w boundaries | Passed by direct cut decomposition |
| Joint covariance and stabilizer action | Passed; simultaneous pair permutations preserve every bad S |
| Fixed spaces and common projectors across four sources | Passed; rank two bright space per block |
| Separate clique-dark conservation | Not assumed; would be too strong |
| Source factorial and empty second bright mode | Passed |
| Target tensor factorization, exact factorial moments and PGF | Passed |
| Chernoff minimizer and smallest allowed L | Passed; L=2 is vacuous |
| Two-sided support insertion and summed target bound | Passed |
| Predictable adaptive choice among individually covariant maps | Passed |
| Tail, extended expectation and photon counting | Passed with the stated run-until-success scope |
| Finite-beta first exit and random-schedule expectation | Passed under the declared Metropolis acceptance |
| Loss after U | Passed without conditioning; internal noise outside scope |
| Separately optimized independent distinguishable particles | Passed as an upper bound only |
| P67's referenced counterexample and literature novelty | Not addressed; unnecessary for these implications |
| Random covariance in law, marked-history maps, generic starts | Outside the theorem's hypotheses |

There is no remaining mathematical gap in the normalized claim above.
The only local prose clarification identified is the meaning of “every
other balanced subset” in source section 1: it excludes the other equal-cost
bad states as well as the two targets. No source change is made by this
review. The strongest safe conclusion is the explicit ideal-model bound
with its warm-start and pathwise covariance restrictions. No execution is
needed to establish it, and no numerical test can replace those universal
hypotheses.

Validation: exact source SHA checked with `shasum -a 256`; source freeze
metadata read with `git show --stat --oneline 1f12a8a`. Text-only diff and
whitespace checks accompany this review's commit. No test suite or scientific
command was run, as expressly required. Final mathematical proofreading
covered all of this review: coefficients, factorials, L=2 boundary,
projector names, conditional events, and probability versus expectation
quantifiers. No mathematical token in the audited source was changed.
