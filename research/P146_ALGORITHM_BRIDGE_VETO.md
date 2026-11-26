# P146 — veto of an automatic resource-to-optimizer bridge

27-Nov-2026; non-author focused hand reconstruction, ROOT named the audit
questions; not a blind review. No program/import, numerical experiment or job.
Read FULL P146-A311 at ROOT commit `6cf60d2b3fc2b18139f7dc1cf5877690c645aa77`,
SHA256 `d93789b588292f09b52aa3c99ef8d176e4da4e94cbd6cc96a8310c5439a9caef`,
and the separate weighted-recycling supplement137, SHA256
`6aa2d01aab3b4dea99fa309bb35aedcfa15f08347fa7092bba17a57236cfa87f`.
This does not re-audit every native-instrument/drift step of A.

**Primary verdict: incomplete, with the smallest missing implication being
a complete all-branch algorithm compilation after resource preparation.**
A explicitly leaves useful noncommuting dynamics OPEN; its offline guarantee
is not refuted. Directly reusing that purge invariant between alternating
layers fails. A known MBQC compilation can instead provide a conditional
logical bridge, but no such executable resource/measurement contract is supplied.

## One layer: explicit classical mean control, without a sampler claim

Let `U=exp(i sum_(a<b) theta_ab Z_a Z_b)`, input `|+>^n`, and apply
`R=product_a exp(-i beta_a X_a)` before Z readout. Assume known local Z
byproducts were undone, with no additional fields. Put `c_a=cos(2 beta_a)`,
`s_a=sin(2 beta_a)`, symmetric theta with zero diagonal, and

    P_b^a=product_(k!=a,b) cos(2 theta_bk),
    Q_±^(ab)=product_(k!=a,b) cos(2(theta_ak ± theta_bk)).

Independent Pauli expansion gives the exact completed-resource identity

    E[Z_a Z_b] = -sin(2 theta_ab)*(c_a s_b P_b^a+s_a c_b P_a^b)
                +(s_a s_b/2)*(Q_-^(ab)-Q_+^(ab)).                 (1)

`R† Z R=c Z+s Y`; direct-edge conjugation gives
`U† Z_aY_b U` expectation `-sin(2 theta_ab)P_b^a`. The direct edge
commutes with `Y_aY_b`; summing the other independent uniform Z eigenvalues
gives `(Q_- - Q_+)/2`. These facts reconstruct both terms of (1).
For one isolated edge and common beta it reduces to
`-sin(4 beta)sin(2 theta_ab)`, agreeing with the earlier two-bit witness.

For paired cost `C0-sum J_ab Z_aZ_b`, (1) computes its mean by products of
trigonometric scalars: O(g*(Delta+1)) arithmetic operations for g cost pairs
and interaction degree Delta. This even stays polynomial for dense graphs.
Angles, certified precision, compilation and parameter search remain paid;
no free exact-real oracle or implemented finite-bit algorithm is asserted.
This is a hand-derived identity, not an external-priority claim. It does NOT
sample the full count law or establish best-of-T, clipped-improvement, quench
or barrier-crossing dominance. Timeout/failure and timing records remain extra.
At fixed layer depth and bounded degree the finite backward light-cone mean
control also remains available; this is not an all-depth simulation theorem.

## Smallest purge failure after a noncommuting gate

Take `e^(i theta Z1Z2)|++>`, apply `RX1(beta)=e^(-i beta X1)`, then
measure/delete qubit1 in Z, outcome z=±1. The NORMALIZED remaining state is

    [cos(beta)e^(i z theta Z2)-i sin(beta)e^(-i z theta Z2)]|+>.

Both z outcomes have probability1/2, but conditional populations are
`Pr(Z2=+1|z)=[1-z sin(2 beta)sin(2 theta)]/2`. At
`theta=beta=pi/4`, the remainder is `|1>` for z=+1 and `|0>` for z=-1.
An induced one-vertex weighted resource is `|+>` up to known Z rotations;
such rotations cannot correct these unequal populations. Thus the exact
known-induced-resource certificate is lost already on two qubits. This
does not rule out special circuits, error correction or paid global reprepare.

In particular, preparing one cost layer offline does not justify purging
algorithmic data when a later cost gate fails after RX. Treating all arbitrary
data losses as full-run abort reintroduces A's stated survival penalty for
that implementation. It is not a universal penalty on all MBQC architectures.

## A logically valid alternative is known MBQC, with a larger contract

Freeze the entire optimum-blind circuit first, e.g. public J, paid beta/gamma
and `product_l [RX(beta_l) exp(i gamma_l sum J_ab Z_aZ_b)]|+>^n`.
For `Rz(phi)=exp(-i phi Z/2)`, exact gate identities give

    exp(i theta ZaZb)=CNOT_ab [I tensor Rz(-2theta)] CNOT_ab,
    RX(beta)=H Rz(2beta) H,    CNOT=(I tensor H)CZ(I tensor H).

A minimal local MBQC transfer identity is explicit: attach fresh `|+>`,
apply CZ, and measure the old wire in
`(|0>+(-1)^s e^(i alpha)|1>)/sqrt2`. Its Kraus map onto the new wire is
`e^(-i alpha/2) X^s H Rz(-alpha)/sqrt2`. ALL outcomes are usable with
known byproducts; later measurement angles/outcome interpretation must adapt.
CZ-linked wires supply the standard entangling gate patterns. Merely copying
the problem's weighted cost graph into time slices is not that compilation.

This is the established circuit-to-cluster mechanism: Raussendorf–Browne–Briegel,
[quant-ph/0301052v2](https://arxiv.org/pdf/quant-ph/0301052v2), 14-Jan-2003,
PRA68,022312, §§II.B (gate patterns), II.D (composition), II.H (resources).
Its ideal cluster universality and resource scaling are known; the located
patterns/statements were checked, not the entire37-page proof re-audited.
The weighted/non-Clifford variant and dyadic correction are also known from
the Kissinger–van de Wetering source pinned in the supplement.

One may build the COMPLETE known cluster/resource offline, using local reuse
only during that preparation, and then execute its prescribed measurements.
The unknown logical data flow through it by teleportation rather than being
reset to |+> after a failed computational measurement. Once computation begins,
loss needs a separately proved fault/erasure strategy or a charged abort;
offline preparation's linear expectation alone does not bound this cost.
Clifford resource preparation plus non-Clifford adaptive measurements already
suffices in principle; weighted edges are not a new universality framework.

## Decisive remaining gate

Supply the whole resource graph, preparation/reset invariant, measurement
bases/order/feed-forward, all byproducts, precision and EVERY computation-time
loss/timeout branch, with memory/mode/photon/depth/cost bounds. The n paired
data bits are not the total physical resource size. Lucy compatibility is a
separate unverified interface question. P146 presently establishes only a
conditional resource-construction result, not useful optimizer performance.
Paid paired-Ising and unrestricted bisection search, local-mean evaluation,
exact small-channel/state simulation and tensor/stabilizer-rank controls remain
mandatory; D/species must use the same physical instrument with independent
retuning. Group2 already reproduces A's per-microattempt optical instrument.
No generic QAOA/MBQC discovery, practical advantage or positive goal closure.
