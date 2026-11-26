# P142 — Product triad phase: raw-utility scope and obstructions

26-Nov-2026. Manual investigation, parent cc615f5d197eda7753c8a2993e6d79fed2f9dbc3.
FULL read P132 (247 lines)@ff2150e7, review (166)@eb53e96b, P103 (125)@f4f1e4c and
P105 (174)@aa534e6a. P103/P105 SHA256 respectively 8046fad38f0f592105f8b5c76ad3c3ce839c36b94ac60a351f639973c30818ae,
4cd966e0f3f2da603845e7143ab068de1b257cfcf43d8e266ec0da2cb58c5216.
Existing Menssen/P132 triad physics is prior context, not rediscovered novelty.
No code/import/AST, program/matrix evaluation, RNG, new graph, P141 data,
native/QPU, manuscript edit or new simulation allocation. Proofs below are manual.

## Physical source and one concrete optimum-blind spatial family

Use three distinct spatial CF inputs with PRODUCT internal states
chi1=H,chi2=(H+V)/sqrt2,chi3±=(H+exp(±i*phi)V)/sqrt2.
Their pair-overlap moduli agree and the oriented product is
J±=<chi1|chi2><chi2|chi3±><chi3±|chi1>=(1+exp(±i*phi))/4.
These are compatible physical Gram matrices, not independently assigned phases.

A concrete inherited compiler is the graph Cayley family, not a new ansatz:
on n=24 choose balanced current S, public-marked R subset S of size 3, S0=S\R,
and receivers B_pool=R plus three public outside vertices, disjoint from S0.
Let d_j=sum_(h outside S0,h!=j)w_jh-sum_(i in S0)w_ji. With transported
mark ranks, Omega_jh=sign(rank(h)-rank(j)), choose real gamma and
H_jj=d_j/nu,H_jh=(-w_jh+i*gamma*w_jh*Omega_jh)/nu for j!=h,
nu=max(1,max_j(|d_j|+(1+|gamma|)sum_(h!=j)w_jh)). Then H is Hermitian,
||H||<=1 and U_G(t,gamma)=(I+i*t*H)(I-i*t*H)^-1 is unitary for real finite t.
Input ports are R; all six output ports are receivers. No optimum/eigenstate
or favorable target is loaded. This is an illustrative spatial family only:
no graph, t/gamma grid, resource contract, computation or pilot is registered.

## Exact degree-two obstruction at a FIXED spatial transfer

For any common passive tag-independent signal transfer T, including vacuum
loss, put s_ab=|<chi_a|chi_b>|^2. Product CF inputs give

    E[n_j]=sum_a|T_ja|^2,
    E[n_j*n_l-delta_jl*n_j]
      =sum_(a!=b)[|T_ja|^2|T_lb|^2
                    +s_ab*T_ja*T_lb*conj(T_jb*T_la)]. (1)

These follow by normal ordering: two annihilations select only two distinct
input labels, so their exchange contains s_ab, never a three-cycle. Ordinary
n_j^2 equals its factorial second moment plus n_j. Thus EVERY polynomial of
total occupation degree<=2 has equal mean under chi+ and chi- at this T.
Changing T while changing phase is a different comparison, not an exception.

In particular define the occupation extension
f(n)=C(S0)+sum_j d_j*n_j-2sum_(j<l)w_jl*n_j*n_l,
g(n)=C(S)-f(n). On receiver-CF total-3 events V, f is the actual balanced
candidate cut. Else it is merely an algebraic extension. All invalid events
hold S; the optimum-blind accepted improvement is h=g_+*1_V. Writing
Delta E[q]=E_+[q]-E_-[q], equation(1) gives the EXACT ledger

    Delta E[h]=-Delta E[g*1_invalid]
                          +Delta E[(-g)_+*1_V].       (2)

The signed, unclipped CF improvement has only the first term. With neither
invalid sectors nor clipping of worse candidates, the triad sign cannot
change mean cut improvement. It cannot train an unconditional quadratic
energy objective through this phase. Equation(2) does NOT declare every raw
nonlinear utility effect artificial: weighted invalid-type redistribution or
the acceptance cutoff can matter, but every event/cost must remain paid.

## Stronger lossless check: the CF RATE is unchanged

Assume COMPLETE three-column isometry W, no discarded spatial outputs, and
all N=3 records. Let S_int be the source internal Gram. For triple occupation j,

    P(3_j)=per(S_int)*product_a |W_ja|^2,
    per(S_int)=1+sum_(a<b)s_ab+2Re(J).                 (3)

Both sides have the same s_ab and ReJ, so every P(3_j) agrees. Also
E binom(n_j,2)=sum_(l!=j)P(2_j,1_l)+3P(3_j) agrees by(1), hence
sum_(l!=j)Delta P(2_j,1_l)=0 for EACH doubled port. If
A_coll=sum_j binom(n_j,2), P3=sum_j P(3_j), then

    P_CF=1-E[A_coll]+2P3.                             (4)

This proves equal TOTAL collision-free probability for opposite triad phases,
although its allocation among individual feasible Y may change. Any useful
CF contrast in this complete lossless setting is not a survival/CF-rate gain.
For a truncated signal transfer with loss/dump modes excluded, Nsignal need
not be 3; equation(4) is NOT automatically a receiver-sector identity.

## The exact utility bridge still has no guaranteed useful sign

Use complete three-photon output records of an isometry W, including vacuum
loss outputs if present; h is zero outside the receiver-valid sector. Put
A_sigma=product_j W_(o_j,sigma(j)), with output factorial n!,
c=(123), and Z_n=(1/n!)*sum_sigma A_sigma*conj(A_(c^-1 composed sigma)).
Identity/transposition terms agree; the oriented three-cycles give

    p_+(n)-p_-(n)=-4Im(J+)*Im(Z_n),
    Delta E[h]=-4Im(J+)*Im(sum_n h(n)*Z_n).             (5)

This is an exact RAW graph bridge with the current-cut threshold, no C*.
Its sign is UNKNOWN for the graph compiler above. A phase-sensitive bin is
not the weighted sum; the known P132 hand bin is not reused as an optimizer.
For a gauge-real FULL W every Z_n is real and the full contrast vanishes. For a
uniform complete graph all balanced candidates have the same cut, h=0,
so even a nonzero physical contrast supplies no graph benefit.

There is a second obstruction to a sign-only resource claim. Conjugating the
spatial amplitudes and ALL product internal states preserves each real
count probability. Hence p_-(n;W)=p_+(n;conj(W)). If the admissible spatial
family is conjugation-closed with identical allowed costs and common decoder,
adding the chi± knob does not enlarge its law/utility set: fixed chi+ plus
W or conj(W) already realizes both signs. For the displayed Cayley family,
conj(U(t,gamma))=U(-t,-gamma). A conjugate-paired average also has zero sign
contrast. Hardware cost symmetry is an assumption, not inferred from this.
This does NOT prove triad sources equivalent to D or proper pair controls.

## Six obligations and disposition

| Obligation | Answer or missing implication |
|---|---|
| Graph encoding | Current R, full-graph boundary fields, public marks and finite U above; exact lifted balanced cut, no C*/mask. |
| Why interference | Only three-cycle weighted term(5) changes at fixed pair moduli; moments(1) and rate(4) constrain it. A favorable useful sign is unproved. |
| Retuned controls | D chooses its OWN spatial parameters; all three 2+1 partitions, fully identical source and partial-pair endpoints retune independently. Include conjugates, exact-law mirror and strong feasible search, not a same-T handicap. |
| Paid classical work | Share fields, selection, inverse/mesh, overlaps/phases, past scores and all 20 residual candidates if evaluated. Two sign probes plus proposal cost 9 injected photons; all scored probes are credited. |
| Lucy applicability | Three photons/six spatial modes with two color copies cost 12 orthogonal modes; product source couplers plus U directsum U and classical color forgetting simulate the internal states. Orthogonal D needs 3 labels: 18 copy modes or another certified resource. Source prep, addressing, PNR/attempt visibility, calibration and Lucy API are UNVERIFIED; in-shot feedback is not required here. |
| Falsifier | Reject quadratic-objective phase gain, unequal lossless CF rates, a claimed sign resource already absorbed by conjugates, or a utility win reproduced by independently tuned groups/classical search. |

Color forgetting is a classical trace, not coherent erasure or entangled-source
resource. The enlarged network is STATIC; fixed-three-photon exact-law sampling
is a mandatory costed control, and the 20-state pool is already tractable.
This note proves scope restrictions and an exact bridge, not a positive
optimization result, novelty clearance or global no-go. No useful-sign theorem
surviving the controls was found; no new numerical pilot is justified by this
analysis alone. A later card needs an additional falsifiable cost mechanism.
Only this note was written. All validated/negative results and paper stay intact.
