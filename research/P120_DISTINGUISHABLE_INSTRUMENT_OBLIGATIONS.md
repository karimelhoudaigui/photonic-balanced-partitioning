# P120: distinguishable controls for photon-catalysis instruments

2026-11-26. MANUAL prospective obligations, before P116 author-source access.
Read the full P74 resource-screen source, P76 weak-filter source, both ROOT
accepted checkpoints, and P105 neighboring-mechanism/source portfolio.
This note assumes no P116 implementation, herald yield or positive result.
It introduces no scientific run, source installation or hardware claim.

## 1. State space and the appropriate D model

Two dual-rail data photons encode TWO qubits. Add two single-photon helpers;
the complete modeled injection costs four photons before loss. Count all
data rails, helper ports and vacuum/loss ports in the physical circuit.
A graph encoding and feasible decoder are separate obligations; two data
qubits must not silently become four logical vertex qubits.

The fully distinguishable control gives all four injected photons mutually
orthogonal conserved internal tags d1,d2,h1,h2. Every optical element acts
identically on tags. PNR detection reports spatial occupations, ignoring
tags. Ignoring a tag sums orthogonal probabilities; it does NOT coherently
erase distinguishability. State preparation, spatial/internal dimensions
and the actual means of producing equivalent tags must be documented.

For a product source in four known occupied ports and a FIXED passive
network, fold coherent local qubit preparation/mixers into that full network.
D can then be computed by labeled routing/occupation sums, equivalently an
intensity permanent with output factorials at terminal detection. Different
paths of EACH individual photon still interfere. Replacing every beam
splitter by a classical intensity transition would wrongly remove that
single-photon coherence. An entangled initial data source instead needs its
explicit labeled density operator and paid preparation, not this product rule.

## 2. Minimal exact catalysis discriminator

Fix the real beam splitter on active data mode a and helper mode b:

    U_R=[[t,r],[r,-t]], t=sqrt(R), r=sqrt(1-R), 0<=R<=1.

For identical photons in input |1,1>, the one-in-each amplitude is
r^2-t^2=1-2R. Hence the B coincidence probability is (2R-1)^2.
With orthogonal tags d,h the accepted output instead has two assignments:

    -R |d>_data |h>_herald,
    (1-R) |h>_data |d>_herald.

They are orthogonal. The unresolved PNR coincidence probability is
R^2+(1-R)^2. At R=1/2, B is ZERO and D is 1/2. The remaining events
are bunched/failure outcomes, not deleted probability. This is a local HOM
interference witness, not an optimizer advantage or a four-photon mechanism.

The counterexample also exposes why a scalar D filter is inadequate. Let
logical |0> put data tag d in a spectator rail, |1> in active rail a, and
inject helper h. Conditional on one helper count, tracing only the measured
helper/tag gives two accepted Kraus branches, up to irrelevant branch phases:

    A_h: |0,d> -> t|0,d>,  |1,d> -> R|1,d>,
    A_d: |0,d> -> 0,       |1,d> -> (1-R)|1,h>.

The corresponding B accepted logical operator is diag(t,2R-1), up to
one global phase. Its amplitudes must not be reused as D's logical map.
Even choosing diag(sqrt(R),sqrt(R^2+(1-R)^2)) for D is incorrect: it
matches the two basis success probabilities but invents coherence.
At R=1/2, both D basis states succeed with probability 1/2. Nevertheless,
on input |+>, after tag tracing its normalized logical density matrix has
diagonals 1/2 and off-diagonal 1/(2sqrt(2)). A subsequent Hadamard gives
Pr(+ before H)=Pr(0 after H)=(1+1/sqrt(2))/2, whereas the invented scalar
identity filter predicts one. This manual test concerns the isolated gadget;
global composition must retain the actual tag/branch structure.

## 3. Complete instrument, protected flags and code leakage

P116 must supply the full source and physical network, with every herald
occupation h=(h1,h2), every retained data occupation and every loss branch.
Construct each B/D CP instrument on its actual retained Fock/tag space:
project the measured spatial counts, sum unresolved detected tag assignments
incoherently, and trace only discarded degrees of freedom. All outcome
traces, including vacuum and preparation failure, must sum to one per
declared source attempt. A sole successful bosonic Kraus matrix is not D.

Even helper counts (1,1) do not generally certify one photon in each data
rail pair. Prove the accepted code-invariance/leakage statement in BOTH
arms, or retain wrong-code outcomes for the common final decoder. Bosonic
destructive cancellation of leakage need not survive fully orthogonal tags.
Preserve loss, wrong photon number, bunching, helper replacement and all
noncode amplitudes/probabilities. Graph balance is another constraint beyond
the dual-rail code. The same fixed invalid-event holding/repair rule is paid
for B and D; no favorable conditional or valid-only denominator is allowed.

P74/P76 show why final data projection cannot replace intermediate code
monitoring: leakage can leave and later reenter the code. Consequently do
not multiply isolated projected logical matrices unless composability is
proved. Distinct protected helper records may instead be measured at the
end when ALL later operations act trivially on those helper degrees of
freedom; the projectors then commute. Reusing/remixing helper modes invalidates
that shortcut. A final success table is not a nondestructive monitor.

Complete FAILURE maps are required if later operations/recovery depend on
them. The positive-filter classical-prefix identity in P76 does not supply
arbitrary failure-dependent dynamics from success diagonals. Conversely,
diagonal-only accepted bias without recombination needs P76's exact latent
classical rejection/prefix control, with every rejected attempt charged.

## 4. Optimization and common resources

Independently optimize D over the SAME physically allowed reflectivities R,
filters, attenuations, rail phases, coherent mixers and preparation choices.
Supply exactly the same graph features, compiler information and fixed
decoder. Sharing only B's fitted settings demonstrates an interference
contrast, not a positive optimization result. D may prefer a high-transmission
or identity catalyst setting if that setting belongs to the allowed family.
Unavoidable external loss is common physics, not a free optimizable gain.

Use the full physical tag-aware network for this optimization; replacing
permanents inside an already conditioned two-qubit effective gate does not
define a correct D control. Group-2/3 species profiles must also include
possible data/helper groupings and be independently optimized; a local
data-helper HOM effect alone cannot separate B from a group-2 control.
Include exact tiny feasible/classical search with the same features and
paid scores/preprocessing. No C*, optimal mask or known-solution preparation
may enter training. Relabeling, fresh seeds and held-out tests remain later
gates; this analytic note passes none of them.

Count all attempted source preparations, four modeled input photons per
actual prepared injection, helpers launched before failures, loss/rejection,
parameter training, scores and mesh/setup work. Early-abort savings require
real measured flags and on-demand resources; a static deferred-herald circuit
cannot claim them. Variable preparation costs need an actual common ledger.
Extra detector/source loss must be included in both complete instruments;
one/two helper photons cannot be distinguished by assuming threshold=PNR.
Authenticated raw-attempt/preparation counts and actual detector capabilities
are necessary before transferring these formulas to Lucy; none is assumed.

Disposition: these are falsifiable control/instrument requirements and two
manual counterexamples to incorrect D models, not a negative universal
theorem or a promised useful catalysis mechanism. Frozen P113/P114/P115 are
unchanged; no imports/AST/tests/scripts/RNG/native/QPU/paper operation ran.
