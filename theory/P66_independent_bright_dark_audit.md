# P66 independent audit: a bright/dark occupation barrier

25-Nov-2026. Static mathematical review, worktree base
`3e708637639b8664d0f81bb8947ce05fed0e0a4c`.

**Primary verdict: correct only after a stated restriction.** The proposed
one-attempt and zero-temperature bounds follow under the kernel and starting
state hypotheses below. The finite-temperature sum is literal for a fixed
schedule, or deterministic lower bounds on an adaptive schedule. A fully
random history-dependent schedule requires expectations of conditional terms.
This is an explicit obstruction to one restricted proposal family, not an
optimization advantage, a result on arbitrary graphs, or a novelty claim.

The reviewer received the candidate statement and suggested projector/PGF
argument, but no other P66 author's file or verdict. Every load-bearing step
below was rederived. No Python, import, numerical experiment, test, external
source lookup, hardware call or manuscript edit was performed. The existing
P65 kernel note was read only for the collision-counting conventions.

## 1. Normalized claim card

Let L be an integer at least 2. Set N=4L and K=2L. A weighted undirected graph
has disjoint vertex sets A1,A2,B1,B2, each of cardinality L. Within each set all
edges have weight M>0. A perfect matching of weight h>0 joins A1 to A2 and
another joins B1 to B2. There are no other edges. Assume

    M(L-1)>Lh;  g=2M(L-1)-2Lh>0.

In particular, M=3,h=1 gives g=4L-6>0. Denote the two connected components
CA=A1 union A2 and CB=B1 union B2. Let A be the zero-diagonal adjacency
matrix, J the N by N all-ones matrix, and

    H=(A+lambda*(J-I))/D,  lambda>=0, D>0,
    U=(I+i*t*H)*(I-i*t*H)^(-1), t real.

The inverse exists. The conclusion also holds for any unitary preserving each
component's dark one-particle subspace, in particular unitary spectral
functions of these H and products of such unitaries. D,t,lambda may be chosen
adaptively before an attempt, conditional on arbitrary past classical data.
The component decomposition and the uniform bright modes remain fixed.

Each attempt starts by freshly preparing the normalized collision-free Fock
state with one photon at every vertex of the current balanced subset S.
The optical evolution is the stated ideal lossless unitary; all output
counts are measured. Collided outputs are paid self-loops; only a full
collision-free output defines a new feasible subset T. Optional independent
uniform loss after this unitary can only remove successful events, and is
also counted as a paid self-loop. Arbitrary internal loss or noise is outside
this statement. A collision-free proposal is accepted with

    min(1,exp(-beta*(C(T)-C(S)))), beta>=0,

where C is the ordinary weighted graph-cut cost. Zero temperature means
accepting every non-uphill proposal and rejecting every uphill proposal.
Accepted proposals determine
the next source. The initial source and incumbent are a member of

    B={A1 union B1,A1 union B2,A2 union B1,A2 union B2}.

No external restart, accepted uphill move at zero temperature, classical
candidate insertion, different decoder, retained coherent state between
attempts or different optical matrix class is included in this claim.

Define

    a_L=L!/(2L)^L,
    b_L=min(1, ((L+1)/2)*((L+1)/(2L))^L),
    p_L=min(1,2*a_L*b_L).

For any S in B, the raw probability of proposing either strictly better
balanced subset is at most p_L, uniformly in the admissible optical unitary.
At zero temperature this is also the conditional improvement hazard after
every unsuccessful history, so the probability of improvement within T
paid attempts is at most min(1,T*p_L). There is a stronger geometric survival
bound stated below. At finite temperatures beta_j, the first-exit argument
below yields the corresponding scoped bound.

## 2. Dependency graph

1. The clique balance argument isolates B and the two zero-cut targets, with
   gap g to every other balanced subset.
2. Graph regularity implies preservation of two separate dark subspaces.
3. Passive second quantization preserves their photon occupation numbers.
4. The source and target have different exact sector support constraints.
5. Bosonic factorial moments bound the target bright-mode tail.
6. A two-support projection and Cauchy--Schwarz bound the target amplitude.
7. Conditional hazards and a first-exit argument extend the bound to a chain.

All seven leaves are proved internally below. The exponential envelope uses
only an integral inequality for log factorial, also shown below. There are
no unchecked numerical or external-theorem inputs to the finite bounds.

## 3. Cost landscape and its boundary cases

A balanced subset that is a union of whole cliques consists of two of the
four cliques. Of the six choices, CA and CB have cost zero. Each of the four
members of B cuts both matchings, hence has cost C0=2Lh.

Every other balanced subset contains at least two partial cliques: with only
one partial clique of size x, where 1<=x<=L-1, its cardinality would be
x plus a multiple of L and could not equal 2L. A partial clique contributes
M*x*(L-x)>=M(L-1) to the cut. Thus every non-whole-clique subset costs at
least 2M(L-1)=C0+g. Matching edges have nonnegative weights and cannot
invalidate this lower bound.

This proves both that CA,CB are the only strictly better subsets than a
member of B and that every other possible exit from B is uphill by at least
g. The requirement h>0 ensures the asserted two-component interpretation.
The case L=1 is excluded: its positive-gap assumption is impossible.

## 4. One-particle invariant subspaces and photon numbers

Put d=2L. Let bA and bB be the normalized uniform vectors on CA and CB.
Within each component the graph is regular of weighted degree
r=M(L-1)+h. Since A is real symmetric, it preserves bA and its orthogonal
complement DA inside CA; it likewise preserves bB and DB inside CB.

The all-ones matrix annihilates DA and DB. The identity preserves them.
Consequently H and U preserve DA and DB separately. Their common orthogonal
complement is span{bA,bB}; it too is invariant. This is an orthogonal reducing
decomposition, not merely an invariant subspace assertion for a nonnormal
operator. For Cayley U, Hermiticity of H establishes unitarity and makes the
inverse well defined. For the broader class, unitarity and preservation of
the two dark subspaces are explicit hypotheses.

Let N_DA and N_DB be the second-quantized number operators for these two
one-particle subspaces. In a mode basis adapted to the orthogonal direct
sum, the passive Fock lift Gamma(U) acts separately on each block. Therefore
it commutes with both number operators and every joint spectral projector.
No assumption of independent indistinguishable photons is used here.

## 5. Source and target sector weights

Consider S=A1 union B1; the other members of B have the same argument. The
source has exactly L photons in each component, so N_DA<=L on its entire
support. Within CB, the probability that all L photons occupy the uniform
bright mode bB is

    a_L=|<L_bB | 1_B1>|^2=L!/d^L.

Indeed, expansion of (bB^dagger)^L/sqrt(L!) gives overlap
sqrt(L!)*d^(-L/2) with the normalized collision-free state on any L distinct
component modes. Thus the source weight in the joint projector

    Pi=1[N_DA<=L]*1[N_DB=0]

is exactly a_L.

For target |1_CA>, N_DB=0 exactly. Its weight in Pi equals the probability
that its occupation n of mode bA is at least L, because it has d=2L photons
in CA and N_DA=d-n. This is a genuinely bosonic occupation distribution;
it must not be replaced by a binomial law.

In the collision-free state containing one photon in all d component modes,
expansion of bA^m shows

    E[(n)_m]=(m!)^2*binom(d,m)/d^m=m!*(d)_m/d^m,
    0<=m<=d.

Here (x)_m is the falling factorial. Each m-element set of annihilated
occupied modes produces an orthogonal residual Fock state with coefficient
m!*d^(-m/2). This proves the equality including normalization. Hence for
0<=s<1,

    E[(1+s)^n]=sum_{m=0}^d (d)_m*(s/d)^m
               <=sum_{m=0}^infinity s^m=1/(1-s).

For L>=2, s=(L-1)/(L+1) lies strictly between zero and one. Markov's
inequality gives

    Pr(n>=L)<=1/((1-s)*(1+s)^L)
              =((L+1)/2)*((L+1)/(2L))^L.

Taking the minimum with one establishes the advertised b_L. The factorial
moments at m=0 and m=1 give 1 and 1, respectively, checking the probability
normalization and mean bright occupation without any independence assumption.

## 6. The projection step: a necessary logical qualification

Commutation of Pi with Gamma(U) ALONE would not allow an arbitrary amplitude
to be bounded by the product of its source and target Pi weights. There could
be a contribution from Pi's orthogonal complement. The missing support facts
are available in this problem and must be stated.

Let P=1[N_DA<=L] and Q=1[N_DB=0], so Pi=PQ. The source satisfies P|s>=|s>
and the target satisfies Q|t>=|t>. P,Q commute with each other and Gamma(U).
It follows that

    <t|Gamma(U)|s>=<t|Q*Gamma(U)*P|s>
                    =<Pi*t|Gamma(U)|Pi*s>.

Therefore Cauchy--Schwarz and unitarity give

    |<1_CA|Gamma(U)|1_S>|^2
        <=||Pi*1_CA||^2*||Pi*1_S||^2<=b_L*a_L.

Swapping CA and CB gives the same bound for the other good target. Their
Fock outcomes are distinct, so their raw probabilities add and the total
is at most p_L. This counts all collided outcomes as failures/self-loops;
there is no division by a collision-free probability.

## 7. Adaptive histories, finite temperatures and actual scope

At zero temperature, until improvement the accepted state stays inside B:
all other non-good feasible states are strictly uphill. Every unsuccessful
history therefore has the same upper improvement hazard p_L, even when the
controller chooses different admissible t,lambda or an internal random
mixture on every attempt. Conditional probabilities and induction imply

    Pr(tau>T)>=(1-p_L)^T,
    Pr(tau<=T)<=1-(1-p_L)^T<=min(1,T*p_L),
    E[tau]>=1/p_L.

The expectation is interpreted as infinity if improvement has positive
probability of never occurring. For a run that continues attempting until
improvement, every attempt injects K photons under the stated source
convention, so expected injected photons are at least K/p_L. For capped or
voluntarily stopped runs, only the finite-budget success bound is asserted;
assigning tau=infinity after stopping does not mean infinitely many photons
were actually injected. No simulator wall-time or measured hardware-time
comparison is inferred.

At finite beta_j>=0, while the current state remains in B, the chance of an
accepted non-good exit is at most exp(-beta_j*g), since each such proposal
is uphill by at least g and the total proposal mass is at most one. A good
proposal has probability at most p_L. Improvement by attempt T requires an
exit from B by then, hence for a deterministic schedule

    Pr(improvement by T)<=min(1,T*p_L+sum_{j=1}^T exp(-beta_j*g)).

The same formula holds with beta_j replaced by deterministic lower bounds
on a history-dependent schedule. For an arbitrary random beta_j selected
before the shot, one safe version is

    Pr(improvement by T)
      <=min(1,T*p_L+sum_j E[1[no previous exit]*exp(-beta_j*g)]).

The expectation is over the controller and history, with terms zero when
that attempt is not executed. Replacing a random beta_j inside this formula
by its mean is unjustified. In particular beta=0 makes the finite-temperature
bound vacuous. A schedule scaling as 1/L can also leave beta*g of constant
order: this argument does not prove exponential trapping for P65's actual
annealing schedule or its tested ER/RR graphs.

Arbitrary state-dependent parameter selection may fail detailed balance as
noted in P65, but detailed balance is NOT used in the hazard proof. The
occupation-sector preservation at every history is the relevant condition.

## 8. A self-contained exponential envelope and exact boundary checks

No asymptotic theorem is needed for the exact constants. For L>=2,

    log(L!)<=integral_1^L log(x) dx+log(L)
             =L*log(L)-L+1+log(L),

so a_L<=e*L*(2e)^(-L). Also (1+1/L)^L<=e gives
b_L<=e*(L+1)*2^(-L-1). Thus

    p_L<=2*a_L*b_L<=e^2*L*(L+1)*(4e)^(-L).

This explicitly proves exponential smallness, with no unverified Stirling
leaf. The proposed sharper polynomial prefactor of order L^(3/2) is
compatible with the standard Stirling asymptotic, but is unnecessary here
and is not a dependency of this self-contained proof.

At L=2, a_L=1/8, b_L=27/32 and p_L=27/128. At L=3, a_L=1/36,
b_L=16/27 and p_L=8/243. These are symbolic hand checks, not simulated
transition probabilities; the inequalities need not be tight. For M=3,h=1,
g=4L-6 is positive at the smallest allowed L=2.

## 9. Distinguishable control and the classical falsifier

The same one-particle invariant decomposition gives an additional, independent
bound for distinguishable photons. The block from CB to CA of U is

    U_CA,CB=z*|bA><bB|, |z|<=1.

For any individual input vertex in CB, its probability of landing anywhere
in CA is |z|^2/d<=1/d. With L independently propagated labeled photons in
CB, a target with all K photons in CA requires all L to cross. Thus its
probability, even before imposing collision-freedom or constraints on the
other photons, is at most d^(-L). The two good targets give at most
min(1,2*(2L)^(-L)), uniformly over independently selected admissible optical
parameters. This is another upper bound, not a B-versus-D ordering: comparing
two upper bounds cannot establish either interference benefit or disadvantage.

The graph's connected components each have K vertices. Finding them by a
standard graph traversal immediately supplies a balanced zero cut, in
O(N+|E|) graph operations. Here |E|=4*binom(L,2)+2L=2L^2, so this is
polynomial in L. This intentionally obvious classical falsifier is part of
the construction. No experiment or matched measured CPU result is claimed.
An algorithm allowed to insert that classical solution into its incumbent
has already left the restricted optical-only update rule of this theorem.

## 10. Obligation matrix and remaining boundary

| Obligation | Outcome | Exact limitation |
|---|---|---|
| Balanced cost gap | Passed | Nonnegative stated weights, L>=2, strict gap assumption |
| Separate dark subspaces | Passed | Uniform component modes and regular components |
| Lift to occupation invariants | Passed | Passive unitary Fock evolution |
| Source sector weight | Passed | CF source with L distinct occupied modes per component |
| Target bright tail | Passed | Full-component CF target, bosonic factorial moments |
| Amplitude projection | Passed with explicit support facts | Commutation alone is insufficient |
| Adaptive zero-temperature chain | Passed | Accepted source updates only; no restarts or extra candidates |
| Fixed-schedule finite-temperature sum | Passed | First-exit upper bound, may be vacuous |
| Literal random-beta sum | Requires restriction | Use deterministic lower bounds or conditional expectations |
| Exponential envelope | Passed | Self-contained L^2 prefactor; sharp Stirling prefactor unused |
| Independently reoptimized D obstruction | Passed in same unitary class | No ordering inferred against B |
| Generic graph or generic passive-optics obstruction | Out of scope | Arbitrary U can violate the dark invariants |
| Random initialization or actual P65 DEV obstruction | Out of scope | Start and graph family here are explicit |
| Optimization advantage, QPU result, novelty | Not addressed | None follows from this proof |

An arbitrary passive permutation swapping B1 and A2 sends the chosen source
A1 union B1 to CA with probability one, illustrating why the unitary-class
restriction cannot be dropped. That permutation does not preserve the
specified dark subspaces and encodes graph information outside this Cayley
family. Likewise, retained collided Fock states and a different decoder
alter the source/target support facts and need a fresh argument.

The strongest safe conclusion is a low-temperature, shared-warmstart
obstruction for this regular-component graph family, explaining why the
uniform all-to-all optical background does not remove its dark-sector
barrier. The global positive-result objective remains open.

The cheapest future finite check is exact small-L matrix/permanent validation
of the sector probabilities and raw CF transition bounds, with a frozen
prospective input/command/output contract before execution. Such a check
would validate implementation conventions, not replace this universal proof.
No test suite was run in this static-only review; executable integration
checks remain the coordinator's responsibility.

## 11. Separately audited connected weighted extension

After the core derivation, the coordinator requested a connected extension.
No other author's extension proof or verdict was supplied. Retain the same
four size-L cliques, M,h and matchings, but add every edge between CA and CB
with weight

    0<w<h/L.

Here CA,CB denote the two original blocks, not connected components of the
new graph. Every vertex has the same weighted degree
M(L-1)+h+2Lw. On the one-particle subspace orthogonal to the uniform vector
inside either block, its complete bipartite cross adjacency is zero.
Consequently the old dark subspaces remain separate reducing subspaces of
the new adjacency matrix, of H and of its Cayley transform. Adding lambda*J
also preserves them. Every sector, Fock moment and projection bound from
sections 4--7 survives with these block interpretations. The graph is now
connected; the proof does not rely on graph disconnection itself.

For a balanced subset S put x=|S intersect CA|. It contains 2L-x vertices of
CB, so its cross-block cut contribution is exactly

    w*(x^2+(2L-x)^2)=2wL^2+2w*(x-L)^2>=2wL^2.

For the two whole-block targets CA,CB, this contribution is 4wL^2 and the
internal cut is zero. For the four bad whole-clique subsets, it is 2wL^2,
and the internal matching cut is 2Lh. Thus

    C_good=4wL^2,
    C_bad=2Lh+2wL^2,
    C_bad-C_good=2L*(h-Lw)>0.

A subset containing partial cliques has at least two of them by balance,
so its heavy cut is at least 2M(L-1). Its matching cut is nonnegative and
its cross cut at least 2wL^2. Its total cost is therefore at least

    2M(L-1)+2wL^2=C_bad+g.

Hence these same two whole-block targets are the only strict improvements
from B, and the uphill gap remains exactly the previously proved LOWER
BOUND g=2M(L-1)-2Lh. The actual minimum uphill difference may be larger.
The raw improvement probability <=p_L and all the scoped first-exit bounds
therefore apply without changing a_L or b_L. In this extension the good
cuts have positive cost; referring to them as zero cuts would be false.

The concrete choice w=h/(2L) gives C_good=2Lh and C_bad=3Lh. With M=3,h=1,
scaling every edge weight by 2L gives integer heavy, matching and cross
weights 6L,2L,1. The resulting gap is multiplied by 2L. Cost scaling requires
the reciprocal beta scaling if one wants to preserve a particular thermal
transition law; no such law equivalence is needed for the cost certificate
or zero-temperature obstruction.

The ordinary connected-component baseline from section 9 no longer finds
a balanced solution. A comparably explicit classical control still does:
M>h>w follows from the hypotheses. The graph consisting only of edges of
largest weight M is exactly four disjoint K_L cliques. Extract these four
cliques, evaluate the six unions of two, and keep a minimum-cost union.
This requires a graph read, a traversal of the largest-weight-edge graph
and six graph-cut passes: O(N+|E|) operations for an edge-list input, or
O(N^2+|E|) when reading a dense matrix. Here the new graph has |E|=6L^2.
The cost-gap proof certifies that the minimum among these six is a global
minimum, because all partial-clique subsets cost strictly more than every
bad whole-clique subset, which in turn costs more than a good union.
No known optimum is used as a training mask; this is a disclosed classical
solver of the explicitly constructed family.

**Extension audit outcome: passed under the written hypotheses.** This
extension removes literal graph disconnection while retaining a low-rank
inter-block optical coupling, a shared bad warmstart and an elementary
classical certificate. It still does not establish an obstruction for
arbitrary connected graphs, arbitrary graph-dependent interferometers,
fresh random starts, or the actual P65 DEV panel.
