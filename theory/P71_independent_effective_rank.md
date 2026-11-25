# P71: effective cross rank and a complete-law error bound

Primary verdict: **proved as written** for the normalized statement below.
A unitary admits a nearby unitary with truncated cross rank, including at
zero and unit singular values. The complete K-photon PNR laws differ in
total variation by at most K times that one-particle operator-norm error.
Only an additive robustness bound follows; a polynomially small singular
tail does not by itself imply an exponential success obstruction.

Independent static derivation of ROOT's P71 candidate, 2026-11-25, branch
`research/p66-dark-barrier`, starting checkpoint
`69ad2ceae881571186db311d7914252d34449e99`. No other P71 proof or verdict
was read. Only this new file is written. The CS construction, its endpoint
completion, norm calculation, tensor telescoping and trace-distance step
are proved below rather than cited as unverified leaves. No scientific
import, test, numerical calculation, graph generation, seed/draw, backend,
external-source lookup or QPU call was performed. There is no novelty claim.

## 1. Statement and exact P69 dependency

Let L>=2 be an integer, d=2L and K=2L. The physical one-particle space
is HA direct-sum HB, with each labeled vertex block of dimension d.
Let the complete one-particle unitary from the prepared source to detection
be U, written

    U = [ A B ],       C: input HA -> output HB,
        [ C D ]        B: input HB -> output HA.

Let 1>=s1>=...>=sd>=0 be the singular values of C, including zeros.
Section 2 also proves these are the singular values of B. For every integer
0<=r<d there exists a unitary V on the same blocks with cross rank at most
r such that

    ||U-V||op = delta(s_{r+1}),
    delta(s) = sqrt(2-2sqrt(1-s^2)) <= sqrt(2)*s,    0<=s<=1.

For r=d take V=U and define its tail error to be zero. No singular value
s_{d+1} needs to be evaluated.

Prepare the same normalized source x with one photon at each of L distinct
vertex modes in HA and L distinct modes in HB. Let P_U,P_V be their
complete normalized K-photon PNR laws in the same vertex output basis,
including all collisions. Then

    TV(P_U,P_V) <= min(1,K||U-V||op).

The two raw target events are the normalized CF states with one photon
in every vertex mode of exactly one block. The exact P69 input is the
uniform-over-allowed-matrices bound p_Lr for those two events, as proved
in `theory/P69_independent_low_rank_transport.md`, commit
`e5477a74d5282bb752e759780046826b63196520`, SHA256
`fb4f7f828bcba0ad644971ba8851c219599dc73a20d45071d7f63bddc3a2b620`.
For clarity its constants are

    a_Lr = min(1,r(r+1)...(r+L-1)/L^L),         r>=1,
    b_Lr = 1,                                  r>=L,
           ((L+r)/(2r))^r*((L+r)/(2L))^L,       1<=r<L,
    p_Lr = min(1,2 a_Lr b_Lr),                  r>=1,
    p_L0 = 0.

For 1<=r<L the displayed b is already below one. P69 applies to every
unitary of the indicated cross rank, not only a graph-derived ansatz.
It therefore applies to the mathematical comparator V even if that V
cannot be implemented by a proposed compiler or controller family.
Consequently

    P_U(two targets)
       <= min(1,p_Lr+K delta(s_{r+1}))
       <= min(1,p_Lr+sqrt(2) K s_{r+1}),         0<=r<d.

For r=d the same comparison has zero tail error and reduces to P69 with
r=d. This case supplies no nontrivial rank obstruction.

## 2. Constructing the cosine/sine channels, endpoints included

By unitarity A^dagger A+C^dagger C=I. Thus C^dagger C is Hermitian
positive semidefinite and has eigenvalues in [0,1]. Choose an orthonormal
input HA eigenbasis v_i with eigenvalues s_i^2, in the order above, and
put c_i=sqrt(1-s_i^2). The finite-dimensional Hermitian diagonalization
used here follows by maximizing its real quadratic form on the unit
sphere, obtaining an eigenvector, and iterating on the invariant
orthogonal complement.

When c_i>0 define the output HA vector a_i=A v_i/c_i. For every pair
with positive c_i,c_j,

    <a_i,a_j> = <v_i,(I-C^dagger C)v_j>/(c_i c_j) = delta_ij.

Complete these vectors to an orthonormal basis of output HA by choosing
the missing a_i at precisely the indices c_i=0 (s_i=1). Their values
are unconstrained by the vanished A v_i. Likewise, when s_i>0 define
b_i=C v_i/s_i in output HB. These form an orthonormal family; complete
it to an orthonormal output HB basis by assigning the missing b_i at
indices s_i=0. These completions are always possible: the numbers of
missing vectors equal the respective codimensions of the two families.

For every index, including both endpoints,

    U(v_i,0) = alpha_i := (c_i a_i,s_i b_i).

Define z_i=(-s_i a_i,c_i b_i). The orthonormal a and b bases give

    <alpha_i,alpha_j>=delta_ij,
    <z_i,z_j>=delta_ij,
    <alpha_i,z_j>=0.

The d vectors z_i are therefore an orthonormal basis of the complement
of U(input HA). Since U is onto, U^dagger z_i lies in input HB and
these d vectors give an orthonormal basis there. Identify them as w_i,
so

    U(0,w_i)=z_i.

At s_i=0 the two images are (a_i,0) and (0,b_i). At s_i=1 they are
(0,b_i) and (-a_i,0). Thus no division by zero or omitted endpoint
subspace is hidden in this construction.

Let P_A,P_B send the standard coordinate bases to v_i,w_i, and Q_A,Q_B
send them to a_i,b_i. All are unitary maps inside their own blocks. With
S=diag(s_i) and C0=diag(c_i), the preceding image identities prove

    U=(Q_A direct-sum Q_B) R (P_A direct-sum P_B)^dagger,
    R=[ C0 -S ],
      [ S  C0 ].

After grouping the two coordinates with the same i, R is the direct sum
of real two-dimensional rotations

    R_i=[ c_i -s_i ],     c_i^2+s_i^2=1, c_i,s_i>=0.
        [ s_i  c_i ]

In particular B=-Q_A S P_B^dagger and C=Q_B S P_A^dagger have exactly
the same singular values, with no rank-equality assumption needed first.
The decomposition is constructed, not invoked as a CS theorem leaf.

## 3. Truncation and the operator-norm error

For i<=r retain R_i. For i>r replace R_i by I_2. Let R^(r) be this
unitary direct sum and define

    V=(Q_A direct-sum Q_B) R^(r) (P_A direct-sum P_B)^dagger.

Its two cross blocks contain only the retained s_i, hence have rank at
most r. Multiplication on either side by the same local basis unitaries
preserves the norm of U-V. On a discarded channel,

    (R_i-I)^dagger(R_i-I)=2I-R_i-R_i^dagger=2(1-c_i)I.

Therefore the norm of that channel error is sqrt(2-2c_i). The norm
of a direct sum is the maximum channel norm, so sorting the s_i gives
exactly delta(s_{r+1}). For s>0 rationalizing the square root gives

    delta(s)^2 = 2s^2/(1+sqrt(1-s^2)) <= 2s^2.

At s=0 both sides vanish. The formula includes delta(1)=sqrt(2).
If the singular tail is exactly zero the construction gives V=U, even
if the discarded null-space bases were not uniquely determined. At r=0,
V is block diagonal; at r=d there is no discarded channel. The construction
supplies existence and the stated exact norm for this comparator.

## 4. From one-particle error to the complete bosonic law

On the K-fold tensor space, a telescoping identity is

    U^(tensor K)-V^(tensor K)
      =sum_{j=1}^K U^(tensor(j-1)) tensor (U-V)
                           tensor V^(tensor(K-j)).

Each other tensor factor has norm one. The triangle inequality gives

    ||U^(tensor K)-V^(tensor K)||op <= K||U-V||op.

Passive K-boson propagation is the restriction of those tensor powers
to the symmetric tensor subspace. Restriction cannot increase the norm,
so with psi=Gamma_K(U)x and phi=Gamma_K(V)x,

    ||psi-phi||2 <= K||U-V||op.

The CF source is normalized in this identification; there is no extra
K! or sqrt(K!) multiplying this estimate. Both output vectors have norm
one and include the entire collision-allowed K-photon space.

For completeness, the pure-state trace distance is

    Dtr=1/2 || |psi><psi|-|phi><phi| ||1
       =sqrt(1-|<psi,phi>|^2).

To derive it, restrict the difference of the two rank-one projectors
to the span of psi,phi. It has trace zero and squared nonzero eigenvalues
1-|<psi,phi>|^2, hence opposite eigenvalues of those magnitudes; the
coincident-line case gives zero by the same formula. Put c=<psi,phi>.
Then

    ||psi-phi||2^2-(1-|c|^2)=|1-c|^2>=0,

so Dtr<=||psi-phi||2, without an additional factor two.

For any PNR event E, the corresponding measurement projector satisfies
0<=E<=I. For the Hermitian trace-zero density difference Delta, its
positive and negative parts each have trace Dtr. Thus
|Tr(E Delta)|<=Dtr. The complete PNR law has finitely many outcomes,
all occupations summing to K, and

    TV(P_U,P_V)=1/2 sum_n |P_U(n)-P_V(n)|
              =max_event |P_U(event)-P_V(event)|.

It follows that TV<=Dtr<=K||U-V||op, also bounded by one. This proves
the claimed K coefficient with the standard half-sum convention for TV.

An independent Euclidean check gives the same coefficient: for PNR
amplitude vectors alpha,beta, apply Cauchy-Schwarz to
sum_n ||alpha_n|-|beta_n||(|alpha_n|+|beta_n|)/2. The second factor is
at most two and the first is at most ||alpha-beta||2. This confirms the
normalization of the measurement and trace-distance step.

The input, measurement basis and event must agree for U and V. A shared
fixed classical processing rule cannot increase TV, but it does not extend
P69's target bound to an arbitrary decoder. In particular CF conditioning
can amplify an error by its normalization, and decoding collisions into
the good subsets changes the event to which P69 applies. Here collisions
are retained raw and become self-loops for the specified optimizer.

## 5. Conditional histories and finite-temperature first exit

Use the original or connected P66 four-clique graph with M,h>0,
M(L-1)>Lh, and cross weight w=0 or 0<w<h/L. The four bad whole-clique
subsets select L vertices in each fixed block; the two whole-block
targets are the only strict improvements. Every subset outside those
six has cut at least C_bad+g, where g=2M(L-1)-2Lh>0.
The graph fact follows because at least two cliques are partial, each
contributing M(L-1); connected cross cut is at least 2wL^2, while the
bad cut is 2Lh+2wL^2 and good cut is 4wL^2. Other bad states tie.

Fix a common rank cutoff r<d. Before attempt j, the controller can use
any past, marks and fresh classical randomness to choose the NET U_j.
Condition on those choices before drawing its optical output. Let

    eta_j=s_{r+1}(U_j),
    kappa_j=min(1,p_Lr+K delta(eta_j)).

For every still-bad current state the conditional raw target probability
is at most kappa_j. Different attempts can have completely different
channel bases and comparator unitaries. They need not share projectors,
covariance, ansatz parameters or randomness. The new optical source is
always the stated CF state of the accepted current subset.

At zero temperature accept every non-uphill CF proposal and reject
uphill proposals. The current state remains bad until success. For a
fixed deterministic horizon T and tau the first improvement, conditioning
and summing first-success events give

    P(tau<=T) <= min(1,sum_{j=1}^T E[1_{tau>=j} kappa_j])
       <= min(1,T p_Lr
                 +K sum_{j=1}^T E[1_{tau>=j} delta(eta_j)])
       <= min(1,T p_Lr
                 +sqrt(2) K sum_{j=1}^T E[1_{tau>=j} eta_j]).

If controller randomization is not included in the conditioning history,
its conditional expectation must be taken as well. A random eta_j is not
an unconditional numerical right-hand side. No independence between
attempts is assumed. If deterministic bounds eta_j<=epsilon_j<=1 hold
almost surely before every draw, the simpler bound is

    P(tau<=T) <= min(1,T p_Lr+sqrt(2) K sum_j epsilon_j).

For a uniform epsilon this is min(1,T[p_Lr+sqrt(2)K epsilon]). An
earlier adapted stop can be padded with self-loops. External candidate
injection or restart at another input is not the specified trajectory.

At finite inverse temperature beta_j>=0, accept an uphill CF move of
increase Delta with probability exp(-beta_j Delta), using a fresh
independent acceptance coin. Let sigma be the first accepted exit from
the bad set. Before that exit, direct targets have hazard at most
kappa_j and any other accepted exit has hazard at most exp(-beta_j g).
Every improvement requires such an exit, regardless of later behavior.
If beta_j and eta_j are history-random but chosen before the draw,

    P(improvement by T)
      <=min(1,sum_j E[1_{sigma>=j}(kappa_j+exp(-beta_j g))]).

With deterministic beta_j and deterministic tail bounds epsilon_j,
this implies

    P(improvement by T)
      <=min(1,T p_Lr+sqrt(2)K sum_j epsilon_j+sum_j exp(-beta_j g)).

Deterministic almost-sure lower bounds on random beta_j give a weaker
bound of the same form. A bare random thermal sum requires expectation,
not substitution as a scalar bound. No stationarity or detailed-balance
claim for general history-dependent proposals is needed.

## 6. What a small effective tail does and does not imply

This is additive continuity of the complete law, not a multiplicative
approximation to exponentially small target probabilities. Suppose the
exact-rank term p_Lr is exponentially small and T=O(L^p), K=2L.
A deterministic tail bound epsilon_L=O(L^(-c)) contributes only the
polynomial estimate

    T K epsilon_L = O(L^(p+1-c)).

For c>p+1 this suffices for a vanishing error term, without establishing
an exponentially small upper bound. For smaller c the displayed error
bound need not even vanish. Polynomial smallness alone therefore does
not guarantee an exponential obstruction by this argument. To obtain
one from this continuity estimate requires an exponentially small bound
on the additive sum T K epsilon_L, or another stronger argument. This is
a limitation of the bound; it does not assert that exponentially small
tails are necessary for the actual success probability to be small.

Finite-temperature terms must also be controlled separately. In particular
the P65-shaped beta of order 1/L with g of order L does not automatically
give exponential thermal trapping. A measured numerical spectrum or a
typical tail is not, without further evidence, an almost-sure conditional
bound for every adaptive history. No such empirical claim is made here.

## 7. Dependency and scope audit

| Obligation | Result |
|---|---|
| Complete CS construction | Proved by explicit input/output bases |
| Missing vectors at s=0 and s=1 | Completed; both endpoint images checked |
| Equality of cross singular-value multisets | Follows from the constructed diagonal cross blocks |
| Rank-r unitary comparator and exact delta norm | Proved by coherent channel truncation |
| sqrt(2) singular-tail estimate | Proved by rationalizing delta squared |
| Fixed-K passive lift and telescoping | Proved with coefficient K |
| Trace, Euclidean and TV conventions | Proved with half-trace/half-sum definitions; no lost factor two |
| CF target bound for the comparator | Exact P69 dependency pinned above |
| History-random tails and beta | Expectations retained before unconditional claims |
| r=0 and r=d | Separate correct constructions and conclusions |
| Polynomial versus exponential robustness | Only additive bound asserted |
| Physical filters, changed sources or decoded events | Outside hypotheses |
| Implementability or cost of the mathematical V | Not assumed and not claimed |
| Generic starts, all graphs, optimizer advantage, novelty | Not established |

The physical unitary is always the whole NET U relative to the same two
blocks used by the source and detector labels. Additional physical modes,
nonunitary preparation filters, heralding or intermediate measurements
are not silently represented by a unitary submatrix. V is a comparison
device in the proof and carries no hardware or compiler claim. This
restricted ideal-model robustness result supplies no positive optimizer,
runtime separation, manuscript authorization or QPU authorization.

Final mathematical proofreading covered the whole file: channel ordering,
endpoint completions, conjugations, norm constants, Fock normalization,
TV conventions, rank cases and conditional expectations. Only text and
Git integrity checks accompany this freeze; no scientific execution was
performed.
