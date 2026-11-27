# P146 — cost interactions and local resource repair, with the algorithm gap exposed

27 November 2026, Europe/Paris. Base `fbefdb4d15120cb550178a83014d59141022939a`.
**The original optimization objective remains OPEN. No positive optimizer,
held-out replication, novelty clearance or QPU result is claimed.** The paper
is unchanged. This phase changes physical assumptions rather than retuning P145.

## What the three competing routes establish

**A — A real cost interaction, conditional resource preparation.** A persistent
quantum register coherently emits fresh photon mediators. Their measurement
induces CZ or a correctable local repeat. An additional non-Clifford memory
ancilla and two CZs induce `exp(±i theta Z_uZ_v)` with both outcomes usable
through a finite dyadic correction ladder. These are known physical ingredients;
the [primary-source review](P146_A_WEIGHTED_RECYCLE_PRIOR_ART.md) documents their
antecedents. Turning the analyzer phase alone does NOT supply a continuously
tunable reversible gate: it produces a nonunitary parity filter.

The substantive derived result is conditional local recovery of an OFFLINE
known weighted graph resource. Upon loss or timeout, measure the still-present
ancilla and both endpoint memories in Z, remove known rotations on their
neighbors, reset the deleted sites, and preserve the correctly built induced
graph. This avoids discarding every previously completed edge on every loss.
It requires ideal coherent memories, their emission interface, PNR/loss flags,
readout/reset and local corrections. Each is a paid, currently unverified Lucy
capability. Losing an unavailable memory or repairing unknown algorithmic data
is outside the result.

For a simple target resource graph with g edges and maximum degree Delta,
cap each native gate at R attempts. With per-photon survival eta, put

    tau=eta^2, p=tau/2,
    r_R=tau/(2-tau)*(1-p^R), c_R=(1-p^R)/(1-p), a=r_R^2, q=a/2,
    S_m=sum_(k=1..m-1)q^k+2q^m,
    C_m=c_R*(1+r_R)*sum_(j=0..m-1)q^j.

Here theta=pi/2^(m+1) and the specified compiler uses TWO native CZs even at
the terminal stage. For actual edge precisions use S_min and C_max. If

    delta=S_min-2(Delta-1)*(1-S_min)>0,

conditional drift gives expected macros at most g/delta and expected emitted
GATE photons at most `2*C_max*g/delta`. Initial states, ancilla rotations,
readout/reset, other photons, storage errors/time and compilation are additional
costs. The proof uses conditional expected work, not independence of success
and cost. A global macro cap gives a recorded timeout outcome; it is never
postselected away. Full [derivation](P146_A_INTERACTION_ROUTE.md) and
[non-author mathematical audit](P146_A_INDEPENDENT_AUDIT.md) are available.
This expected-work theorem is not proved by the finite calculations alone.
Its exact combined priority remains unassessed; no new gate framework is claimed.

**B — Collisions can contribute useful utility, but the proposed decoder loses
to direct classical crossover.** The balanced parent-majority tritter has
`J_B=10/9`, `J_D=26/27`, each fixed pair `22/27`, `I3=16/27` on its declared
hand graph. Collisions contribute `4/9`, escaping a CF-only utility premise.
Direct majority, or an allowed distinguishable monomial route, gives gain2.
This refutes an optimizer interpretation. Single-bit-mutant libraries cannot
escape a one-bit local minimum at ANY photon count. These are analytical
results, not another executed graph campaign. Preserve the
[derivation and negative result](P146_B_DECODING_ROUTE.md).

**C — Digital computation changes the model but does not make an algorithm.**
Known logical cost gates and cardinality-preserving mixers require complete
gate/failure instruments and all helpers. Public Lucy specifications distinguish
12 data qubits from24 modes; actual service access to the memory/retry primitive
is not authenticated. A separate [Lucy bridge](P146_LUCY_INTERACTION_BRIDGE.md)
identifies official evidence, the local Knill heralded alternative and seven
capability questions for Laurent. No account query, contact or job was performed.

## The first physical falsifier was actually executed

The [card](P146_EXPERIMENT_CARD.md), source and execution contract were frozen
before execution. Independent code review found two failure-diagnostic gaps;
both were corrected before the FIRST calculation, without changing any physics,
population or predicate. Final source SHA256:
`6653116e8aa39b7bde7db8c7bf1642ba3b8777bd07808713a7c34b91c93ee567`.
The [review](P146_INSTRUMENT_SOURCE_REVIEW.md) distinguishes implementation
review from independent authorship of the underlying mathematics.

ONE bounded run started on `4064e17`, clean, at
2026-11-26T23:57:14.559372UTC =27-Nov00:57:14.559372Europe/Paris.
It completed in18.665072s, exit0; raw seal **`d8caa93` precedes interpretation**.
The [v2 manifest](P146_full_instrument/run_001/manifest.json) validates against
all eight current input hashes. [Raw records](P146_full_instrument/run_001/data/records.json)
contain all nine8-mode dilations,324 B and576 label-resolved D branches, plus
432 native amplitudes. Failure is null; all38 declared check records exist.

The exact Q(i) branch table retains collisions, vacuum, zeros and environment
labels. Distinguishable Kraus maps factor; all2025 coarse-state PPT principal
minors are nonnegative. A normalized B cross branch has PT determinant-1/16,
an entanglement RESOURCE witness rather than an optimization score. The known
weighted purge passes all832 fixture/environment/Z cases, and its non-diagonal
negative control remains. Eighteen capped resource identities and all44 dyadic
terminating histories pass. Those identities do not simulate a complete
adaptive graph-generation trajectory or a full graph optimizer.

Local Perceval Naive independently evaluates432 finite optical amplitudes,
including the loss-environment outputs, at z=i. Maximum absolute discrepancy
is `5.551115123125783e-17`; the largest dyadic identity error is
`1.1102230246251565e-16`, both below the declared1e-12 tolerance. This checks
the passive optical part of the assumed emitter instrument, not a real memory
interface or an independent optimization/hardware replication.

The declared degree3, m4, R8 cases illustrate the scope of the bound:

| eta, model survival probability | delta | Gate-photon expectation upper bound per target edge |
| --- | ---: | ---: |
|1|0.927317364|15.9894103|
|(399/401)^2 =0.990049813|0.273293880|49.4609987|
|(112/113)^2 =0.982379200|-0.152076608|No positive-drift certificate|

All18 cases, including negative deltas, remain in the raw checks. At eta1,
R4,m4 already has delta=-0.0398556104: a small retry cap can destroy this
SUFFICIENT certificate without any optical loss. Negative drift does not prove
the actual repair algorithm inefficient. None of these eta values is measured
on Lucy; the photon bounds exclude the additional costs listed above.

## Strong classical and algorithmic falsification

A group of TWO identical photons per native batch reproduces the entire B
instrument even with entangled retained memories. It is now a quantum resource,
not a cheap classical null; no old group-control criterion is silently passed.
Fully distinguishable photons with local emissions give separable instruments.
That resource distinction does not establish computational superiority.

More decisively, one weighted ZZ layer followed by local RX has an explicit
classical cut-MEAN formula costing O(g_cost*(Delta_interaction+1)) supplied-angle
arithmetic operations. It remains polynomial even for dense interactions.
This is not a full-law sampler, finite-bit implementation or tail/quench theorem.
The [formula and bridge analysis](P146_ALGORITHM_BRIDGE_VETO.md), independently
[reconstructed here](P146_ALGORITHM_BRIDGE_REVIEW.md), prevent treating a
single-layer mean improvement as the desired discovery.

After noncommuting data mixing, deleting one site already breaks the invariant
on two qubits. Adding an unused third endpoint yields the corresponding
counterexample to the macro's two-endpoint purge, as the independent review
specifies. Multiple alternating layers cannot inherit that recovery rule.
Known MBQC can move computation to measurements on an offline prepared resource,
but the whole graph, measurement/feed-forward pattern, byproducts, precision,
computation-time losses and total physical costs must be instantiated. Neither
generic QAOA nor an appeal to universality is a new mechanism or that contract.
Pair coding additionally searches only one vertex per public pair. Paid paired-
Ising search and unrestricted bisection retain those features/preparation credits.

**Next scientific obligation:** a complete optimum-blind noncommuting algorithm
with a useful sign beyond these controls, not another parameter scan. No such
surviving optimizer is established here. Therefore no DEV training campaign,
held-out graphs, Laurent execution packet, QPU call or manuscript revision is
opened by this phase. This is a concrete enabling resource result and a precise
remaining gap, not fulfillment of the original objective.

## Integration and preservation

ONE existing-suite run on clean `512071d` completed in32.261137s, pytest30.90s:
1569PASS,0 failures/errors/skips,6 Perceval temporary-storage warnings. Raw
seal `cb5353e` precedes interpretation; its [v2 manifest](P146_regression/run_001/manifest.json)
validates all224 inputs. This suite does not rerun the P146 scientific calculation.
The archive check passes all602 historical files; publication check passes7
generated outputs. P33/P37/E05b and every earlier raw/negative remain unchanged.
No changes relative to the base occur in src/, theory/, tests/, experiments/,
results/, .qwen/ or paper/. Main remains `27443954fb7491a293399f0417d05185009f5c9a`.
PDF SHA256 remains
`271946c9043d26c0e00a964591e9a47541d5816c399e7a52a62032630650243f`.
No model/agent infrastructure success is confused with optimizer success.
