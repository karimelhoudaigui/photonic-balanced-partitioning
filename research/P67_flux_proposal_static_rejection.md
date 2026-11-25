# P67: nongauge degree flux does not supply a new leading optimization mechanism

25-Nov-2026. STATIC derivation; no scientific code, numerical matrix, import,
test, seed, graph draw or hardware call. Base
`eae1ddabb215c9dfda05ea9bdcc286a6698ba0ad`.
P41's chiral proxy and leading double-swap control, and P54's full-input weak
hop obstruction, were read before deriving this route. No P65 rerun is
proposed and no novelty claim is made.

**Route decision: REJECT the proposed weak/leading chiral explanation.**
The encoding is physically well defined, but it does not escape the P66
regular-family barrier. Transpose symmetrization exactly removes every odd-
time contribution. Its first coherent two-swap coefficient is already
covered by P41's classical sampler and a retimed distinguishable control.
Finite-angle many-swap transport remains unproved rather than refuted.

## 1. Prospective encoding and exact gauge checks

Let A be a fixed symmetric nonnegative weighted graph adjacency matrix with
zero diagonal. Put f_i=d_i/max_j d_j, taking f_i=0 if every degree is zero.
For i!=j set

    H_ij=(A_ij+lambda)*exp(i*theta_ij), lambda>=0,
    theta_ij=kappa*(f_i*f_j^2-f_j*f_i^2), kappa real,
    H_ii=0.

An optional positive scalar normalization does not change the arguments.
Antisymmetry of theta makes H Hermitian, and the formula is exactly graph-
covariant even at equal degrees. It contains no optimum, cost threshold or
optimal-state mask. Its oriented triangle phase is

    theta_ij+theta_jk+theta_ki
      =kappa*(f_i-f_j)*(f_j-f_k)*(f_k-f_i).

It can therefore be nongauge when three distinct features and the necessary
nonzero matrix entries exist. This is an algebraic possibility, not an
established benefit. A pure gradient theta_ij=alpha_i-alpha_j gives
H=G*H0*G^dagger and U=G*U0*G^dagger. Every fixed input/output Fock amplitude
then differs only by a phase, so ALL PNR probabilities remain unchanged.
If f takes at most two distinct values, the proposed antisymmetric phase is
also a gradient: set the two vertex potentials to reproduce its single
inter-class phase. Occupancy alone, being a two-level feature, cannot create
this flux. On every regular graph all theta vanish. In particular the
connected and disconnected P66 families are unchanged by this encoding.
The stronger exact-covariance obstruction is proved separately in
`research/P67_exact_covariance_symmetry_obstruction.md`.

## 2. What the transpose coin does and does not establish

For fixed H define the Cayley unitary

    U(t)=(I+i*t*H)*(I-i*t*H)^(-1).

It is generally not symmetric. Draw an independent fair classical coin and
apply either U(t) or U(t)^T. For collision-free subsets S,T the bosonic raw
proposal is

    Q_B(S,T)=(|per U[T,S]|^2+|per U[S,T]|^2)/2,

and the distinguishable raw proposal replaces squared permanents by
permanents of entrywise squared magnitudes. Each is symmetric in S,T.
Repair collisions to self-loops and use the ordinary Metropolis acceptance;
for fixed graph-only parameters this produces the usual Gibbs detailed
balance, with all physical attempts counted. The two circuit implementations,
coin, compilations and physical source costs would remain paid.

For Hermitian H,

    U(-t)=U(t)^dagger,
    U(t)^T=conjugate(U(-t)).

Complex conjugation changes no Fock output probability. Therefore the entire
raw Fock output law of the mixture is EXACTLY

    [p(t;H)+p(-t;H)]/2.

It is even in t. This removes every odd Taylor coefficient, including P41's
cubic chiral currents, not merely their total sum. It is also invariant under
H to conjugate(H), so reversing all flux signs does not provide a directional
optimization signal after this symmetrization. Cosine/other even flux
invariants can remain.

If H is recomputed from the current subset S, using U_S and U_S^T at S does
NOT generally make the global transition kernel symmetric: the reverse
proposal uses U_T, which need not equal U_S. The same issue occurs for
current-dependent parameter selection. A graph-cost acceptance alone then
has no Gibbs theorem without an additional exact reversibility argument or
Hastings ratio. Hard proposal probabilities cannot be assumed free.
The symmetry of the mixture applies at fixed H, not across unrelated H_S.

## 3. First coherent two-swap term and an explicit four-port formula

Fix occupied a,c and vacant b,d, with every other occupied output unchanged.
Write

    x=H_ba*H_dc,  y=H_bc*H_da,  R=|x|^2+|y|^2.

The Cayley expansion is U=I+2itH-2t^2H^2+O(t^3). At minimum order the two
moved photons supply the two new outputs, giving amplitude
-4t^2*(x+y). After transpose symmetrization, for this fixed finite graph,

    Q_B(S,T)=16t^4*|x+y|^2+O_H(t^6),
    Q_D(S,T)=16t^4*R+O_H(t^6),
    Q_B-Q_D=32t^4*Re(x*conjugate(y))+O_H(t^6).

Single swaps have the same B/D leading coefficient 4t^2*|H_ba|^2.
No size-uniform remainder or all-angle ordering is asserted here.

Let r_ij=|H_ij|. The two-swap interference term is

    Re(x*conjugate(y))
      =r_ba*r_dc*r_bc*r_da*cos(Phi),
    Phi=theta_ba+theta_dc-theta_bc-theta_da
       =kappa*(f_a-f_c)*(f_b-f_d)*(f_a+f_c-f_b-f_d).

This is a generic four-port minor formula, without asserting that arbitrary
chosen features and magnitudes are simultaneously realizable by a four-
vertex degree encoding. In a graph with only these four vertices,
f_a+f_c-f_b-f_d=2*(A_ac-A_bd)/d_max, so additional degeneracies can force
Phi=0. A four-port comparison is a normalization/transport fixture; if it
is the entire N4/K2 partitioning graph, the double swap is complementation
and has exactly the same cut cost. It is not an optimization example.

At equal crossing magnitudes r, the formula reduces to

    Q_B=32r^4t^4*(1+cos(Phi))+O_H(t^6),
    Q_D=32r^4t^4+O_H(t^6).

The B/D leading ratio ranges from zero to two. Since all r are nonnegative,
kappa=0 already maximizes EVERY leading bosonic double-swap weight at the
same magnitudes: |x+y|^2<=2R, with the fully constructive real case at the
maximal phase alignment. Changing flux can selectively suppress routes,
but cannot increase a leading two-swap raw mass above its zero-flux value.
Suppressing unwanted routes could change later basins; that is a finite-time
many-step question and is not a proved advantage.

## 4. Independent retiming and the existing classical falsifier

For every two-swap output, |x+y|^2<=2R. A distinguishable model retimed to

    t_D=2^(1/4)*t_B

therefore weakly dominates ALL these leading t^4 coefficients simultaneously.
Its leading single-swap rate is also larger by sqrt(2). This concerns only
leading coefficients at fixed H; higher terms, collisions and actual circuit
costs forbid interpreting it as a finite-angle or measured-resource theorem.
It nevertheless rules out a claimed irreducible factor-two mechanism.
Independent D optimization may choose still other parameters.

A stronger score-free classical proposal directly reproduces the coherent
coefficient, following the P41 construction. Let

    Z=sum_{i occupied,j vacant}|H_ji|^2.

For Z>0, draw two crossing entries independently with weights |H_ji|^2/Z.
Reject repeated inputs or outputs. A fixed unordered pair of inputs/outputs
appears with probability 2R/Z^2. Accept it with |x+y|^2/(2R), defining zero
acceptance when R=0. This lies in [0,1]. Its final probability is exactly
|x+y|^2/Z^2 for that double-swap outcome. Multiplying the entire procedure by
a gating probability 16t^4Z^2 reproduces 16t^4|x+y|^2 whenever this gate is
at most one. The other probability is an explicit self-loop. If Z=0 hold.
A sufficient gate condition is |t|*||H||<=1/(2sqrt(K)), since
Z<=K*||H||^2.

This uses two categorical draws and four complex entries after crossing-
weight preprocessing, with no graph-cut calls or large permanent. Its setup,
sampling and eventual candidate score remain paid. Fixed r=3 analogues can
also use tiny permanents; none is a classical polynomial sampler for an
extensive number of moved photons. A meaningful optical claim would have
to beat these controls after complete resource accounting, not just show a
nonzero fourth-order interference term.

## 5. Relation to P41 and P54, and route disposition

P41 already supplies a classical proxy for leading chiral single swaps and
for coherent double swaps. The present even-time Cayley version changes
coefficients, not that obstruction. P54 instead concerns full filling and
top-K decoding; this current-subset CF kernel avoids P54's exact setup, but
its leading single swaps are the ordinary classical rates. Merely changing
complex phases does not create a new leading optimizer.

A current-dependent single-flip-cost feature from P41 also degenerates on
the P66 bad whole-clique starts. For occupied vertices,
(1-2x_i)*(d_i-2(Ax)_i)=M(L-1)-h; the same equality holds for vacant vertices.
The uniform cross-block weight cancels out. Thus that particular attempted
replacement feature is constant too, before any concern about reversibility.

**Executed analytical checks:** gauge invariance, triangle and four-cycle
flux identities, exact transpose/time-reversal identity, leading two-swap
B/D coefficients, retimed-D coefficient comparison, classical pair-sampling
normalization and P66 feature degeneration. These are symbolic derivations;
no favorable graph or seed was selected.

**Rejected:** a new weak-angle chiral advantage from this degree encoding;
a P65 grid resweep under a new name; a claim that a transpose coin alone
repairs a state-dependent optical proposal.

**Open but unestablished:** finite-angle extensive rearrangements with an
explicit mechanism beyond these controls. No bound or experiment presently
supports that continuation, and the exact-covariance theorem still excludes
the P66 family. A substantive next route must change the source, retained
measurement state, graph cost interaction or pathwise symmetry hypothesis.
Preparing two-color graph-correlated pair sources is one different operation,
but requires its own raw-success law and hardware/resource justification;
its conditional cut drift alone would not satisfy the research objective.
No squeezed source, free heralding or native Lucy capability is assumed.
