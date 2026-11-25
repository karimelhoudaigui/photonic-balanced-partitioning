# P69: a uniform low-rank transport obstruction with moving dark subspaces

25-Nov-2026. STATIC independent derivation from the coordinator's exact
candidate. File-only work in `.local/p66-dark-audit`; the unavailable Git
index is untouched. No numerical computation, scientific import, test,
random draw, external theorem lookup, graph generation or QPU call.

**Verdict: proved as written below.** The source/target bound holds for any
unitary with bounded cross-block rank, without graph covariance, fixed dark
subspaces, or unmarked histories. It is a raw-probability obstruction for
specified source/target configurations. Its optimization consequence needs
the separately proved P66 cost barrier and prescribed warmstart. It is not
an all-graphs impossibility, a positive optimizer or a novelty claim.

## 1. Exact finite statement

Let L>=2 be an integer, d=2L, N=2d=4L and K=2L. Fix two labeled vertex
blocks CA,CB, each of size d. A normalized CF source has one photon at each
of L distinct vertices SA in CA and L distinct vertices SB in CB. The two
good target Fock states have one photon at every vertex of CA, or one at
every vertex of CB. They are distinct full-count PNR events.

Let the complete ideal one-particle unitary, including all coherent
rerouting after source preparation, be

    U = [ A  C ],
        [ D  B ]

with d by d blocks, rows indexed by output CA,CB and columns by input
CA,CB. Suppose rank(C)<=r, where r is an integer, 0<=r<=d. The ranks of
C,D are equal by the proof below. For r>=1 define

    a_Lr=min(1, r(r+1)...(r+L-1)/L^L),

    b_Lr=1,                                      if r>=L,
    b_Lr=min(1, ((L+r)/(2r))^r*((L+r)/(2L))^L),   if 1<=r<L,

    p_Lr=min(1,2*a_Lr*b_Lr).

The raw probability of either good target is at most p_Lr. For r=0 it is
exactly zero. No conditioning on collision-freedom is included. The
proposal theorem starts with the specified ideal CF source; any physical preparation cost
or failure must be accounted for separately, and is not a free mechanism.
Output collisions, other targets and rejections retain their probability
mass and resource costs. The theorem itself is ideal and lossless; post-unitary independent uniform loss can
only remove these full-K-photon target events. General internal loss,
nonunitary filters, extra modes or intermediate measurements require a
separate model.

The result is uniform in U, SA,SB and all their labels. Before each attempt
U may be chosen from the complete marked history, including the current
subset and arbitrary random data, provided each realized NET unitary has
the stated cross-rank bound relative to these same two logical blocks.
Input/output relabeling cannot conceal a high-rank physical operation or
turn a differently decoded event into one of these targets.

## 2. Unitarity gives equal cross ranks and moving projector intertwiners

Put qC=rank(C), qD=rank(D). If x belongs to ker(D), then

    U(x,0)=(Ax,0).

Since U is unitary, A is an isometry on ker(D). This image is orthogonal
to range(C): the input (x,0) is orthogonal to every (0,y), hence their
outputs have inner product <Ax,Cy>=0. Therefore

    A ker(D) subset (range C)-perp,
    d-qD <= d-qC, hence qD>=qC.

Similarly B acts isometrically on ker(C) and maps it inside (range D)-perp,
giving qC>=qD. Thus qC=qD=q, and the dimension inclusions are equalities:

    A ker(D)=(range C)-perp,
    B ker(C)=(range D)-perp.

Define input dark subspaces

    DA_in=ker(D) inside input CA,
    DB_in=ker(C) inside input CB,

and output dark subspaces

    DA_out=(range C)-perp inside output CA,
    DB_out=(range D)-perp inside output CB.

Their orthogonal complements within their respective blocks are the input
and output bright spaces, each of dimension q. U maps each input dark
space ONTO its named output dark space. By unitarity, the remaining bright
sum maps onto the output bright sum. For the corresponding one-particle
dark projectors E, this is the INTERTWINING identity

    E_A_out U = U E_A_in,   E_B_out U = U E_B_in.

These are generally not commutators with a common projector. Confusing
input and output spaces would invalidate this extension of P66/P68.

On the K-photon Fock space set NA_in=dGamma(E_A_in), and analogously for
B and output. Passive second quantization gives

    NA_out Gamma(U)=Gamma(U) NA_in,
    NB_out Gamma(U)=Gamma(U) NB_in,

and the same intertwining for every spectral projection. All projectors
within one side commute because their dark mode spaces are orthogonal.
These input/output projectors may change on every attempt; no trajectory-
wide occupation conservation is assumed.

## 3. Elementary bosonic and Gaussian identities used below

The proof has no unverified Wick or Gamma-distribution leaf. Here are the
finite identities and their direct justifications.

For a one-particle linear operator M, not necessarily unitary, its symmetric
tensor lift Gamma(M) has diagonal CF matrix element

    <1_I|Gamma(M)|1_I>=per(M[I,I]).

Expand the normalized symmetrized tensor for the distinct occupied modes;
each permutation contributes one product of matrix entries and the L!
normalization cancels the repeated input ordering. If M=P is an orthogonal
projector, Gamma(P) is the projector onto states in which EVERY photon is
in range(P), so this matrix element is a projection probability.

For a standard complex Gaussian g with density exp(-|g|^2)/pi, polar
integration gives

    E[g^a conjugate(g)^b]=0 if a!=b,
    E[|g|^(2a)]=a!.

The first identity is the angular integral; for the second, x=|g|^2 has
density exp(-x) on x>=0, and integration by parts evaluates its a-th moment.
For independent coordinates g_j the moments multiply. Expanding products
then proves the pairing identity

    E[product_i g_(u_i) product_j conjugate(g_(v_j))]
       =sum_{sigma in S_m} product_i 1[u_i=v_(sigma(i))].

If the coordinate multiplicities differ, both sides vanish. If they agree,
both equal the product of the multiplicity factorials, which counts the
allowed pairings. For z=Vg, expansion of its linear forms now gives

    E[product_{i in I}|z_i|^2]=per(P[I,I]),  P=V V^dagger.

This is the required complex Gaussian permanent identity, with its proof.
It is a mathematical representation for these moments, not a classical
sampler for the full optical law.

For r independent standard complex Gaussian coordinates, multinomial
expansion also gives, exactly,

    E[||g||^(2L)]
      =sum_{n_1+...+n_r=L} L!/(product n_j!)*product n_j!
      =L!*binom(L+r-1,r-1)=r(r+1)...(r+L-1).

For 0<=s<1, the one-coordinate exponential integral gives
E exp(s|g_j|^2)=1/(1-s); independence therefore gives

    E exp(s||g||^2)=(1-s)^(-r).

All moments and normalizations needed in the bounds are now established.

## 4. Uniform source all-bright projection bound

Let P be any rank-q orthogonal bright projector inside CB, q<=r. Write
P=V V^dagger with V an isometry from q dimensions into the d CB modes.
The projection of the L-photon CF source on SB onto all-bright occupation
has probability

    per(P[SB,SB])=E[product_{i in SB}|z_i|^2], z=V[SB,:]g.

The row-restricted isometry is a contraction. The arithmetic-geometric mean
inequality and the preceding exact Gaussian moment yield

    per(P[SB,SB])
       <=E[(||z||^2/L)^L]
       <=E[||g||^(2L)]/L^L
       =q(q+1)...(q+L-1)/L^L
       <=r(r+1)...(r+L-1)/L^L.

If q=0 the projection is zero. Capping the probability at one proves a_Lr.
The same bound applies to any L distinct occupied vertices inside CA.
Neither a flat bright mode nor favorable labels were assumed.

## 5. Uniform full-CF target bright-number tail

For the target |1_CA>, let P be its output CA bright projector, rank q<=r,
and n=dGamma(P). Its PGF is

    E_target[(1+s)^n]
       =<1_CA|Gamma(I+sP)|1_CA>
       =per(I+sP)
       =sum_{I subset CA} s^|I| per(P[I,I]).

The first equality follows by diagonalizing the orthogonal projector: its
bright eigenvalues in I+sP are 1+s and dark eigenvalues are one. The last
equality follows by expanding each permanent factor: identity factors fix
the complementary indices, leaving the permanent on I. It includes the
empty set with permanent one. Thus there is no missing factorial or Fock
normalization in the PGF.

Use the proved Gaussian identity for z=Vg, with P=V V^dagger and V an
isometry. For 0<=s<1,

    E_target[(1+s)^n]
       =E[product_{i in CA}(1+s|z_i|^2)]
       <=E exp(s||z||^2)
       =E exp(s||g||^2)
       =(1-s)^(-q)<=(1-s)^(-r).

Consequently

    Pr_target(n>=L)<=(1-s)^(-r)*(1+s)^(-L).

If r>=L, take the trivial bound one. If 1<=r<L, the logarithm of the
right-hand side is strictly convex, with derivative
r/(1-s)-L/(1+s). Its minimizing s=(L-r)/(L+r) lies in (0,1). Substitution
proves b_Lr. This is a bosonic occupation-tail argument; independent-particle
binomial approximations would be incorrect.

## 6. Two supports and different input/output projectors

For the target in CA define

    X_in=1[NA_in<=L],   Y_in=1[NB_in=0],   Pi_in=X_in Y_in,
    X_out=1[NA_out<=L], Y_out=1[NB_out=0], Pi_out=X_out Y_out.

The source has only L photons in input CA, so X_in|s>=|s>. The target has
no output CB photons, so Y_out|t>=|t>. Intertwining from section 2 then
permits insertion and transport of BOTH projections:

    <t|Gamma(U)|s>
      =<t|Y_out Gamma(U) X_in|s>
      =<Pi_out t|Gamma(U)|Pi_in s>.

The source Pi_in norm squared is its probability that all L CB photons
are in the input bright subspace, at most a_Lr. The target Pi_out norm
squared is its probability that at least L of its total 2L CA photons are
in the output bright subspace, at most b_Lr. Cauchy--Schwarz and unitarity
give the target probability <=a_Lr*b_Lr. Exchange CA,CB to get the same
bound for the other target; the two distinct event probabilities add.
For r=0, component photon totals are preserved and neither target is
reachable from the L/L source. This proves the exact finite statement.

## 7. Marked adaptive histories and optimization scope

Apply the bound to the P66 original or connected four-clique family, whose
four bad whole-clique states have L distinct occupied vertices per block.
The only better feasible states are the two full-block targets, while all
other states cost at least C_bad+g, g=2M(L-1)-2Lh>0.

If every realized unitary has cross rank at most r, the bound is uniform
after every still-bad history, including arbitrary marked outcomes, labels,
current-state dependence and noncovariant circuit choices. A fresh CF source
is prepared from the current state; collisions remain paid self-loops.
At zero temperature the accepted state stays bad until improvement, so

    Pr(improvement by T)<=min(1,T*p_Lr).

No independence between attempts or constancy of the dark projectors is
used. A deterministic finite-temperature schedule gives

    Pr(improvement by T)
      <=min(1,T*p_Lr+sum_j exp(-beta_j*g)).

For adaptive random beta, replace the thermal sum by
sum_j E[1[no earlier accepted exit]*exp(-beta_j*g)], or use deterministic
almost-sure lower bounds on beta. Capped executions receive finite-budget
success bounds only. In an execution continued until success, the uniform
hazard bound implies expected attempts at least 1/p_Lr and expected injected
photons at least K/p_Lr. A separately computed classical solution or an
external restart is outside this optical-update statement.

These graphs have an elementary classical certificate. The theorem does
not show that balanced partitioning itself is difficult, or that these
warmstarts are typical under a uniform feasible initialization. The actual
P65 anneal may escape thermally; no new claim about its tested graph panel
or measured budgets follows.

## 8. Exponential regimes, including growing rank

For 1<=r<L put alpha=r/L. Direct logarithms of the uncapped target bound
show

    b_Lr=exp(-L*I(alpha)),
    I(alpha)=(1+alpha)log(2)-(1+alpha)log(1+alpha)+alpha log(alpha).

Here I(1)=0 and I'(alpha)=log(2alpha/(1+alpha))<0 on (0,1), so I>0 there.
In particular the expression is already below one. For any fixed
0<alpha0<1, all r<=alpha0*L give a target bound at most
exp(-L*I(alpha0)), without needing a nontrivial source bound.

A uniform source estimate follows from monotonicity of log:

    log(product_{j=0}^{L-1}(r+j))
       <=integral_r^(r+L) log(x) dx,
    log(a_Lr)<=min(0,L*[h(alpha)-1]),
    h(alpha)=(1+alpha)log(1+alpha)-alpha log(alpha).

Thus when r=o(L), h(alpha)->0 and I(alpha)->log(2), giving

    p_Lr<=exp(-L*log(2e)+o(L)).

This uses only integral inequalities, not Stirling or a numerical fit.
For fixed integer r>=1 an explicit finite envelope follows from
L!<=e*L*(L/e)^L and (1+r/L)^L<=e^r:

    p_Lr<= [2*e^(r+1)/((r-1)!*(2r)^r)]
            *L*(L+r-1)^(r-1)*(L+r)^r*(2e)^(-L),  L>r.

The bound may be loose or vacuous at small L; r>=L has b_Lr=1 and no
exponential conclusion is asserted by this formula. It is a sufficient
obstruction, not a tight characterization or an achievable rate.

## 9. Distinguishable control: a separate upper bound

For a labeled photon starting at input vertex j in CB, crossing probability
is q_j=(C^dagger C)_jj. Unitarity makes every singular value of C at most
one, so sum_{j in SB}q_j<=Tr(C^dagger C)<=r. Independence of the L labeled
photons and AM--GM imply

    Pr(all L CB photons cross)<=product_{j in SB}q_j<=(r/L)^L.

Reaching target CA requires this crossing event, even before its CF and
other-photon constraints. The opposite target has the same bound. Hence
their total distinguishable probability is at most min(1,2*(r/L)^L), with
zero when r=0. This is uniform over independently chosen allowed optical
matrices and parameters. Comparing this upper bound to the bosonic upper
bound establishes no ordering, no interference benefit and no advantage.

## 10. Circuit composition and the Cayley-specific corollary

For two optical matrices using the SAME block decomposition,

    (UV)_CA,CB=U_AA V_CA,CB+U_CA,CB V_BB.

Subadditivity of rank gives rank((UV)_CA,CB)<=rank(V_CA,CB)+rank(U_CA,CB).
Iterating bounds the net cross rank by the sum of layer cross ranks, capped
at d. Block-local unitaries have cross rank zero and do not increase this
sum. If the total number of rank-one cross-transport layers is o(L), with
all other layers block-local, the resulting raw improvement probability
on the specified barrier is exponentially small by section 8.
This is not a generic circuit-depth lower bound: a single parallel layer
can contain many independent cross couplers and have extensive rank.

Now let H=[X Z; Z^dagger Y] be ANY Hermitian block matrix, with
rank(Z)<=r; no regularity or fixed dark eigenvectors are assumed. For real t,

    U=(I+itH)(I-itH)^(-1)=2*(I-itH)^(-1)-I.

The principal block E=I-itX is invertible because X is Hermitian. The full
matrix I-itH is also invertible. Its Schur complement

    S=I-itY+t^2*Z^dagger*E^(-1)*Z

is invertible: block elimination has determinant det(E)*det(S), and both
the full matrix and E are nonsingular. The off-diagonal inverse block is
it*E^(-1)*Z*S^(-1), giving

    U_CA,CB=2it*E^(-1)*Z*S^(-1),
    rank(U_CA,CB)<=rank(Z)<=r.

This proves the low-rank bound for a SINGLE Cayley transform, even with
arbitrary current/history-dependent within-block Hamiltonians. At t!=0,
the displayed invertible factors in fact preserve rank exactly. Products
of different Cayley transforms obey the sum-of-ranks composition bound,
not necessarily the rank of one Hamiltonian cross block.

For the P66 connected family, uniform cross-block adjacency plus a uniform
lambda*J background has rank one. Arbitrary within-block graph corrections
or diagonal current-dependent potentials in H do not change that fact.
A single Cayley transform therefore remains in the r=1 class even when
all previous fixed-dark and exact-covariance arguments no longer apply.
This is a structural obstruction, not a new optimizer.

The same Hamiltonian-rank claim must NOT be extended to exp(itH) without a
new proof. For example take two-dimensional local diagonal blocks
X=diag(x1,x2), Y=diag(y1,y2), with Z the two by two all-ones rank-one matrix.
The cross block C(t) of exp(itH) has the symbolic expansion

    C_ij(t)=it-t^2*(xi+yj)/2
              -it^3*(xi^2+xi*yj+yj^2+4)/6+O(t^4),
    det C(t)=-t^4*(x1-x2)*(y1-y2)/12+O(t^5).

For unequal local diagonal entries this is nonzero at sufficiently small
nonzero t, so the optical cross rank is two although rank(Z)=1. This is
an analytic scope counterexample, not a simulated graph. Extra local
spectators embed it into larger blocks if desired. The resolvent structure
of Cayley, not low Hamiltonian coupling rank alone, supplied section 10's
rank-preservation statement.

## 11. Audit obligations and exact remaining boundary

| Obligation | Result |
|---|---|
| Equal optical cross ranks | Passed by two isometric dimension inclusions |
| Input/output dark spaces | Passed; different projectors, intertwined by U |
| Bosonic projection permanent | Passed by symmetric-tensor expansion |
| Complex Gaussian pairing | Proved from scalar polar moments |
| Rising-factorial moment | Proved by multinomial expansion and weak compositions |
| Full-CF target PGF | Exact permanent/subset expansion, with factorials accounted for |
| Chernoff optimizer | Passed for 1<=r<L; r=0 and r>=L handled separately |
| History-dependent unitary choice | Passed under a realized NET optical-rank bound |
| Fixed/growing rank exponential claims | Passed with explicit scope and finite envelopes |
| D control | Separate valid upper bound; no B/D ordering |
| Product and Cayley corollaries | Passed for the same fixed block decomposition |
| Generic exponential-Hamiltonian rank corollary | Refuted by the symbolic two-mode-block example |
| Arbitrary decoder, new source, extra modes, nonunitary gates | Outside scope |
| Positive optimizer, held-out replication, QPU result, novelty | Not established |

The cheapest future validation would independently implement small exact
unitaries/projectors and compare the full-CF amplitudes with the stated
bounds under a prospective frozen computation contract. Such a finite check
would support implementation conventions rather than prove this theorem.
No such execution was performed or implied by this static checkpoint.
