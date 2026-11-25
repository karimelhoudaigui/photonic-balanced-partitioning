# P68 independent audit: current-subset covariance still leaves a dark barrier

25-Nov-2026. STATIC independent derivation from the coordinator's proposed
claim, following P67's frozen source files. Base committed ancestor
`eae1ddabb215c9dfda05ea9bdcc286a6698ba0ad`; exact P67 files are separately
hashed because the worktree index became unavailable while staging them.
No other author's P68 proof or verdict was read. No scientific code, import,
test, numerical matrix, graph draw, external source or QPU call was used.

**Verdict: proved as written below.** Exact deterministic covariance in BOTH
the graph and current feasible subset still enforces occupation invariants
on this particular graph/source family. The invariant bright space has rank
two per block, rather than P66/P67's rank one. The resulting asymptotic
obstruction is weaker but remains exponential. It is vacuous at the smallest
allowed L=2, and it excludes neither arbitrary random symmetry breaking nor
controllers carrying individually marked past outcomes.

## 1. Claim and admissible controller

Use the P66 family: four size-L cliques A1,A2,B1,B2, L>=2, heavy weight M>0,
matching weight h>0 inside each pair A1,A2 and B1,B2, and

    M(L-1)>Lh,  g=2M(L-1)-2Lh>0.

Between blocks CA=A1 union A2 and CB=B1 union B2 there are either no edges,
or all edges have a common weight 0<w<h/L. Start from any member of

    B={A1 union B1,A1 union B2,A2 union B1,A2 union B2}.

Prepare one photon in every current selected vertex, measure the whole ideal
unitary output, count every collision as a paid self-loop, and update only
by a collision-free Metropolis proposal. Zero temperature accepts every
non-uphill move and rejects every uphill move. The incumbent initially has
the current cost; no external candidate, restart or different decoder is
inserted. The two whole-block targets G={CA,CB} are the only strict
improvements from B. Every balanced subset outside B union G is uphill
from B by at least g, as proved in the independent P66 audit. The other
members of B have equal cost.

Let U(A,S) be an arbitrary deterministic one-particle unitary satisfying
EXACT JOINT permutation covariance

    U(P*A*P^T,P*S)=P*U(A,S)*P^T

for every vertex permutation P. The vertex subset is part of the argument;
there is no additional individual marking or ordered list of graph vertices.
A controller can also select among U_theta functions, provided each realized
function separately has this property. The theorem allows changing theta
with history because each allowed current matrix obeys the same invariants.
A general history-dependent function U(A,S,marked_history) is a larger class
and is not covered merely because its full input/output LAW is covariant.

Define

    a'_L=L!/L^L,
    b'_L=min(1,((L+2)^2/16)*((L+2)/(2L))^L),
    p'_L=min(1,2*a'_L*b'_L).

For every current S in B the raw good-target probability is at most p'_L,
independently of the permitted optical matrix or global scalar parameters.
At zero temperature this gives the conditional improvement hazard bound
and thus Pr(improvement within T attempts)<=min(1,T*p'_L).

## 2. Stabilizer groups: why the bright rank is two

Fix for clarity S=A1 union B1. Within CA, simultaneously permute the labels
of the L matching pairs in A1 and A2. Every such permutation is a graph
automorphism AND preserves S. It acts as identity on CB. This subgroup GA0
is a copy of S_L. A separate subgroup GB0 does the same in CB. All are valid
also for the complete uniform cross-block extension.

The pair swaps used in P67 to exchange A1 and A2 no longer preserve S, so
they cannot be included. The fixed subspace of GA0 on CA is now

    BA=span{bA1,bA2},

where each bAi is uniform and normalized on its own size-L clique. To see
this exactly, the simultaneous S_L action is transitive within each clique
and does not move vertices between the cliques. Its fixed vectors are
constant separately on each clique. This includes L=2. Let DA=BA-perp
inside CA; define BB and DB analogously.

Every automorphism preserving S commutes with U(A,S) by exact joint
covariance. Averaging GA0 gives the orthogonal projector

    R_A=projector_BA direct-sum I_CB.

The elementary group-average proof from P67 applies, so U commutes with
I-R_A, the projector onto DA. It likewise commutes with the DB projector.
Thus U preserves these two dark subspaces separately. It may mix the two
standard-representation copies INSIDE a block; this is why claiming separate
invariance of each individual clique's dark subspace would be too strong.
Only the total block dark photon number is used in the proof.

The subspaces DA and DB defined this way are the SAME for all four members
of B. Each source has the same matching-pair stabilizers, so the statement
holds at every unsuccessful zero-temperature history, even when the current
bad whole-clique subset changes.

## 3. Source sector weight

Let N_DA,N_DB be the photon-number operators for these two dark subspaces.
Their projectors commute with the passive Fock lift Gamma(U). The source
has exactly L photons inside CA and L inside CB, so N_DA<=L on its support.
In CB the source is the full collision-free state on B1 and vacuum on B2.
Its bright support consists only of bB1, not bB2. Projection onto N_DB=0
therefore requires all L photons to lie in the single uniform B1 mode.
Expansion of its normalized L-photon occupation gives probability

    a'_L=L!/L^L.

The second bright mode does not double this probability: its source
occupation is exactly zero. This is a bosonic Fock overlap, not the
probability of L independent particles choosing a mode.

## 4. Target bright tail and the L=2 boundary

For the target containing one photon at every vertex of CA, let n1,n2 be
the occupations of bA1,bA2. It has no CB photons, hence N_DB=0 exactly,
and its total CA dark occupation is 2L-n1-n2. The event N_DA<=L is
therefore n1+n2>=L.

The target Fock vector factorizes over the two cliques. Since the bright
operators act on separate clique mode sets, their occupation distributions
factorize too; this is a tensor-product statement, not an assumption of
independent photons within either clique. For each full size-L CF clique,
the factorial-moment expansion gives

    E[(1+s)^ni]=sum_{m=0}^L (L)_m*(s/L)^m<=1/(1-s),
    0<=s<1.

The proof is identical to the explicit annihilation-operator derivation
in the P66 audit, with d=L. Multiplication yields

    E[(1+s)^(n1+n2)]<=1/(1-s)^2.

Markov's inequality now gives

    Pr(n1+n2>=L)<=1/((1-s)^2*(1+s)^L).

For L>2 choose s=(L-2)/(L+2), which lies in (0,1), obtaining b'_L.
For L=2 the same expression uses s=0 and merely yields b'_2=1.
Also a'_2=1/2, so p'_2=1: the probability bound is valid but vacuous there.
The theorem must not be described as a useful numerical obstruction at all
finite L>=2. It is an asymptotic statement with an explicit small-L boundary.

## 5. Two-support projection and chain consequence

For target CA put P=1[N_DA<=L], Q=1[N_DB=0]. The source satisfies P|s>=|s>
and the target Q|t>=|t>. Their product Pi=PQ commutes with Gamma(U).
Consequently

    <t|Gamma(U)|s>=<Pi*t|Gamma(U)|Pi*s>,
    |<t|Gamma(U)|s>|^2<=a'_L*b'_L.

The target CB has the same bound after exchanging the blocks. Summing these
two distinct raw CF output events gives p'_L. Commutation alone would not
justify the projection without the separate source/target support facts.

At zero temperature the accepted source stays inside B until improvement.
Therefore the same conditional bound holds after every unsuccessful history:

    Pr(tau>T)>=(1-p'_L)^T,
    Pr(tau<=T)<=min(1,T*p'_L),
    E[tau]>=1/p'_L.

Expected injected photons are at least K/p'_L only for an execution that
continues attempting until success; capped or aborted runs have only the
finite-budget success statement. Any optional independent uniform loss after
the ideal unitary removes successful events and cannot weaken these upper
probability bounds. General internal noise is outside the model.

For deterministic beta_j>=0 the same first-exit argument gives

    Pr(improvement by T)
       <=min(1,T*p'_L+sum_{j=1}^T exp(-beta_j*g)).

For an adaptive random schedule use deterministic lower bounds or the
conditional-expectation version recorded in the P66 audit. At beta=0 the
bound is vacuous. If beta scales as 1/L while g scales as L, this does not
establish exponential thermal trapping. No conclusion about the actual P65
schedule or its ER/RR graph panel follows.

## 6. Explicit asymptotic envelope and independently optimized D

The elementary integral bound log(L!)<=L*log(L)-L+1+log(L) gives

    a'_L<=e*L*e^(-L).

Since (1+2/L)^L<=e^2,

    b'_L<=e^2*(L+2)^2*2^(-L)/16,
    p'_L<=e^3*L*(L+2)^2*(2e)^(-L)/8.

Thus the bound decays exponentially, with a self-contained polynomial
prefactor. No Stirling theorem or numerical asymptotic fit is needed.

For independently propagated distinguishable photons, the cross-block part
of U acts only between the rank-two bright spaces. An individual input
vertex of B1 has squared bright projection 1/L, and no component of its dark
projection can leave CB. Its total crossing probability is therefore at
most 1/L. All L photons originally in CB must cross to reach target CA,
so the probability of that target is at most L^(-L). Summing the two good
targets gives min(1,2*L^(-L)), uniformly over independently reoptimized
allowed optical matrices. This is a separate upper bound, not a comparison
of B with D and not an interference advantage.

## 7. Scope and next scientific choice

| Obligation | Audit result |
|---|---|
| Stabilizer action and fixed-space dimension | Passed: rank two per block |
| Preservation of each clique's separate dark space | Not claimed; generally false |
| Common block dark occupations across bad sources | Passed |
| Source projection | Passed: only occupied clique bright mode contributes |
| Target PGF factorization | Passed: separate clique tensor factors |
| Tail and smallest L | Passed; L=2 is vacuous |
| Adaptive global-parameter controller | Passed within the pathwise matrix class |
| Full history with individually marked outcomes | Outside scope |
| Random covariance only in law | Outside scope; P67 supplies a counterexample |
| Actual positive optimizer/QPU result/novelty | Not established |

The classical graph-structure certificate from P66/P67 still solves these
families in polynomial graph work. The obstruction is therefore scientifically
useful only with its shared-warmstart, exact-covariance and optical-update
restrictions visible. It does not supersede the user's requested positive
result. A candidate escaping it must actually change one of those assumptions,
for example by paid random individual markings, retained collided states or
a different physical interaction. Relabeling covariance in law alone is not
evidence of benefit; all classical feasible controls still apply.
