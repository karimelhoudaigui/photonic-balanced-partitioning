# P146-A — Independent interaction/resource audit

27-Nov-2026, P66. Primary verdict: **proved as written within the explicitly
ideal memory, loss, readout and preparation model**. No algebraic blocker was
found for the native instrument, weighted gadget, purge invariant or drift
bound. This verdict does NOT establish an optimizer or a Lucy implementation.

FULL311-line target: c0b950c079e3146fc5128da7b72f4fb1c6d5c4d3,
research/P146_A_INTERACTION_ROUTE.md, SHA256
d93789b588292f09b52aa3c99ef8d176e4da4e94cbd6cc96a8310c5439a9caef.
Independent non-author reconstruction; ROOT/P94 verdicts are not evidence.
Only this report is written on the isolated P146-B branch. No import/AST,
program, numerical evaluation, graph/RNG/test, scientific raw or native/QPU
access. Original sources, P145 evidence and manuscript remain unchanged.

## 1. Instrument: complete branches and the phase-knob obstruction

The displayed U(z) is unitary for |z|=1. Its two source-column pairs have
U_(j,a_x)=(-1)^(t_j*x)/2, U_(j,b_y)=b_j*(-1)^(t_j*y)/2 as stated.
For j!=k, expanding the two creation operators gives
K_xy=U_(j,a_x)U_(k,b_y)+U_(k,a_x)U_(j,b_y). For jj it gives
sqrt2*U_(j,a_x)U_(j,b_y); this is the output factorial, not tag averaging.
The four bunch operators, two zeros and four cross operators follow exactly.
Their effects sum to I. Cross effects are(I+Re(v)Z_AZ_B)/8, bunch effects I/8.

Only z=+/-i gives state-independent nonzero cross success. At z=i the normalized
cross map is a known local S/S-dagger correction times CZ; each raw successful
record has probability1/8, total1/2. The other four nonzero records have
probability1/8 and local recovery. Coarse four-branch operators have amplitude
1/2, hence probability1/4 each. No missing factor of two was found.
For other unit-circle v, ((1+v)/(1-v))^2 is negative real, so the nonlocal
phase invariant stays pi while singular values change. At v=+/-1 rank drops.
Thus the claimed continuously tunable locally reversible shortcut is refuted;
the formal two-filter inverse is only a separately paid postselected sequence.

Uniform loss can be commuted through U using an environment unitary. In the
environment basis labeling lost SOURCE rails, surviving A/lost B gives
sqrt(eta(1-eta))*M_(A,r) tensor |y><y|, and vice versa. Losing both gives
(1-eta)|xy><xy|. The two-photon branches are eta*K. Summing effects yields
eta^2 I,2eta(1-eta)I,(1-eta)^2 I for detected totals2,1,0. The alphabet has
10+4+1=15 records, including both identically zero two-count events. A one-count
port has FOUR unresolved Kraus operators, not a recoverable scalar operator.
These conclusions assume 0<=eta<=1, independent uniform photon loss, no dark
counts and unchanged/readable stationary memories; photon loss alone is not
a benign-repeat flag. Threshold detection cannot supply the asserted branch
discrimination at eta<1 without another verified loss interface.

## 2. Weighted phase and all stopping/work factors

Ancilla amplitudes c=cos(theta),s=sin(theta), followed by two completed CZs,
give c|0>I+s|1>Z_uZ_v. Y projection is(cI-/+isZ_uZ_v)/sqrt2, so both effects
are I/2 even on entangled input. The induced phases are exp(-/+i theta Z_uZ_v),
with invariant -/+4theta. For theta=pi/2^(m+1), after k wrong signs the phase
is -(2^k-1)theta; at stage m the correction iZ_uZ_v supplies +pi/2. Therefore
the maximum is m gadgets, including m=1, rather than an infinite sign walk.
The m=1 gadget is Clifford; non-Clifford resources are required in general,
not by that endpoint alone. Their actual preparation/precision cost is extra.

Put tau=eta^2, b0=tau/2. Summing native repeat probabilities gives
r=(tau/2)/(1-b0), c_native=1/(1-b0). Stage completion needs two native
successes, hence a=r^2; wrong-sign continuation has probability q=a/2.
Summing reach probabilities proves S_m=sum_(k=1..m-1)q^k+2q^m and reached
gadget count=sum_(j=0..m-1)q^j. Within each reached gadget the first native
gate is paid always and the second only with probability r, giving
C_m=c_native*(1+r)*sum q^j. This is unconditional work, not work conditional
on eventual success; no independence between final success and cost is needed.

For a native cap R, sums stop at R: r_R=r(1-b0^R), c_R=c_native(1-b0^R).
Treat timeout as a purged macro failure, substitute a_R=r_R^2, and retain
every failed/partial record. Bounds2*m_max*R*t_max native attempts and twice
as many flying photons are valid deterministic limits. At eta=1 a fixed small
R can STILL make the drift nonpositive; the uncapped high-efficiency window
must not be imported without recomputing delta_R. Ancilla/memory/readout/reset
and idle-time/phase-precision resources are not included in those photon totals.

The cut factor is correct: xor=(I-Z_uZ_v)/2 implies target exp(+i gamma*w ZZ/2)
up to a scalar. For actual paired physical vertices, the logical edge weight
is SIGNED J_uv=sum_(sigma,tau) sigma*tau*w_((u,sigma),(v,tau)); then the angle
is gamma*J_uv/2, with within-pair edges constant. It is not automatically the
original positive w. This translation and signed dyadic decomposition must
be instantiated before any optimizer; the note does not supply arbitrary-real
angle compilation for free. Reversing the requested sign preserves the ideal
probability/work argument. Vanishing logical edges need no gate.

## 3. Why the weighted purge works, and where it stops

All DATA operations during resource preparation are diagonal. Every primitive
loss Kraus is diagonal/projective on the macro ancilla and u,v only. Condition
on the subsequent measured Z values z_a,z_u,z_v of these STILL PRESENT memories.
Any incomplete ancilla-endpoint or uv phase becomes a scalar. Each previously
built incident exp(i theta_uw Z_uZ_w) becomes the KNOWN rotation
exp(i theta_uw z_u Z_w). Removing those rotations leaves exactly the induced
weighted graph resource on surviving sites. For each unresolved environment
label the remaining vector differs only by a scalar, so mixing those labels
does not dephase surviving sites after that conditioning and correction.

This uses the KNOWN |+> product resource amplitudes and accessible Z readout.
It is not true for a lost, unavailable memory qubit: an unobserved Z label can
leave unknown rotations on neighbors. It is not recovery of an unknown input,
nor valid after an untracked noncommuting DATA mixer. Ancilla preparation/Y
measurement are allowed because the ancilla is also purged; noncommuting data
evolution during this invariant is not. Successful resource preparation alone
leaves computational-basis probabilities uniform until a later mixer/readout.

For a missing target edge uv in a SIMPLE graph, deleting both endpoints loses
at most(deg u-1)+(deg v-1)<=2(Delta-1) correct edges. Resetting those vertices
to |+> and marking their incident edges missing preserves the induction.
For b=2(Delta-1), conditional drift is at least(S_e)-b(1-S_e)>=delta.
Stopping increments at completion and telescoping up to t gives
delta*E[min(t,T)]<=E[W_(t wedge T)]-W0<=g-W0. Monotone convergence gives
E T<=(g-W0)/delta. Predictable per-macro conditional work<=C_* similarly gives
E total_work<=C_* E T, even when expensive paths correlate with failures.
Markov then gives the stated timeout bound. These are ideal expected-work
bounds, not accepted-only averages or equal-wall/device measurements.

Algebraically S_m=a/(2-a)+q^m*(1-a)/(1-a/2)>=a/(2-a), so
a>2b/(1+2b) suffices. For Delta=1, b=0 and any S_*>0 suffices; eta=0 gives S=0
and no positive-drift conclusion. Finite fixed R and actual angle/resource
errors must be tested against the NEW premise, not discarded on failure.

## 4. Controls, source applicability and exact remaining gap

Fully D outcomes resolve into a mixture of product memory Kraus operators;
the bunch term has no bosonic sqrt2. With only the stipulated local memory
operations this cannot entangle product memories. Conversely a group of TWO
identical photons on every microattempt reproduces the entire B instrument
and its adaptive retained-memory process. Thus the original proper-group
superiority requirement is NOT met; calling that group2 control quantum does
not remove the requirement. Clifford-only variants have the usual stabilizer
control. A bounded-degree one-ZZ-layer/local-Rx mean has bounded backward cones,
so its O(g*2^O(Delta)) local contraction is a valid CUT-MEAN control, not a
global sample/tail theorem. These points prevent an optimizer-positive reading.

Primary checks27-Nov-2026: [Lim--Beige--Kwek v4](https://arxiv.org/pdf/quant-ph/0408043v4),
20-Apr-2005, PDFpp2-3 Eqs2-15/Fig2, verifies memory encoding and four corrected
branches; [Wein et al. v2](https://arxiv.org/pdf/2412.08611v2),19-Dec-2025,
II.A.4 and AppendixH/Fig10, verifies the adjacent hybrid-memory/erasure/pruning
context. These passages do not prove this weighted drift or certify Lucy.
No source artifact retained, SHA:NONE. KLM/Clifford source leaves were not
newly authenticated in this bounded review; no new theorem is imported from
them into the internal Kraus/purge/drift derivation. Novelty remains unassessed.

P145's fresh fixed-CF measured kernel and CF-only hold hypotheses omit the
growing coherent memory/emission resource here. P121's all-gates/no-recovery
product premise is likewise changed; the local-pruning proof shows why.
This escapes those particular assumptions, NOT their original conclusions.
The missing scientific implication is useful noncommuting graph optimization
against group2 and strongest classical controls at full cost. The missing
engineering interface is coherent stationary memories plus emission, PNR,
readout/reset/correction and calibrated lifetime; a24-mode passive Lucy unitary
does not supply it. No new computation or hardware experiment is authorized.
