# P143 — Independent finite-instrument weak-obstruction review

26-Nov-2026. Non-author manual audit, parent ee9bf009ec8d1d237cafd581f203c50b16b6e156.
FULL 103 lines read at 82682862a334c2efa0b5442dba14c2bd1afff195,
research/P143_FINITE_INSTRUMENT_WEAK_OBSTRUCTION.md, SHA256
2c500892071978d87d8067e03c2a9a261371f3c0b3cf59a3c69f62a024824c99.
No draft/raw/P141 data, import/AST, program/matrix evaluation, RNG, test,
native/QPU, source overwrite or manuscript work was used.

**ACCEPT under the stated common-spatial-effect and analytic-null premises.**
The ideal destructive passive/count/feedback reduction is reconstructible.
This is not a verdict adopted from the author, nor a certificate that any
device bearing the same controller/API satisfies those premises.

## Input order and physically common effects

For K photons in DISTINCT source modes, the K! ordered spatial permutations
are orthogonal, even though the full space/internal state is bosonic.
Their projector P has rank N=K!. Tracing any normalized allowed internal
state leaves a positive trace-one spatial density supported on P, so
rho_J<=P. Fully orthogonal tags give mutually orthogonal permuted internal
tensors; the reduced spatial mixture is exactly rho_D=P/N. Thus
rho_J<=N*rho_D, uniformly even if the internal state depends on kappa.
The symmetric pure B state attains eigenvalue one: the uniform factor cannot
simply be omitted. rho_D is NOT a symmetric-spatial Fock state.

A common positive effect gives Tr(E_z rho_J)<=N*Tr(E_z rho_D). Equivalently
apply the SAME CP branch to the order inequality and trace. Completeness
normalizes both raw laws. This step is elementary operator order, with no
postselection denominator or probability analyticity needed for rho_J.

I reconstructed the destructive-detector model on a FIXED labelled K-particle
space enlarged with private spatial sinks. Gates act as U^tensorK and the
identity on tags. A number projector counts particles in its ports without
resolving mathematical particle labels. On each measured branch, swap those
ports into fresh vacuum sink modes; future gates act only on active modes.
Previously measured photons never return or interact. Reused detector ports
receive fresh vacuum. Tracing protected photons/internal states at the end
then reproduces ideal destructive statistics and their effects on survivors.
Count-dependent future gates still give linear CP maps on UNNORMALIZED
branches. With finitely many gates/modes/records, the initial effects are
common spatial effects. No Markov assumption on the reduced surviving
spatial state, coherent erasure of tags, or physical QND memory is invoked.

This construction assumes the detector/router is genuinely tag-blind; it is
not proved by omitting its tag record. A one-photon H/V router already sends
the SAME spatial density to different ports depending on internal state,
contradicting a common spatial effect. Tag-sensitive detection/efficiency or
feedback is therefore excluded. Coarsened detection needs its actual CP
instrument, not an unproved choice of coherent threshold-state update.

Every initially prepared helper/reservoir CF photon belongs to K, and D
must tag ALL of them orthogonally. Distinguishing only data photons leaves
a different rho_D. Conditional fresh preparation, uncharged reservoirs,
bunched/unknown ancillas or pre-heralded states need a separate full reduction.
If a fixed initial bank is used to purify such a protocol, its photons are
really charged; the mathematical dilation is not a free resource equivalence.

## Analytic probabilities, zero germs and the smaller factor

For the finite fixed raw alphabet, q_D(z;0)=delta_z,z0 and p_J<=N*q_D force
every admitted internal family to share that deterministic endpoint. Any
nonzero off-null real-analytic probability has a finite integer valuation
nu>=1, with positive leading coefficient by one-sided physical nonnegativity.
The extension at negative kappa need not be positive; nu need NOT be even.
Thus q_D(z;c*kappa)/q_D(z;kappa) tends to c^nu>N for integer c=N+1.
The strict local comparison to p_J is uniform over all internal families,
because their only input is the same factor N. Identically zero D germs
force zero J probabilities on their neighborhoods. Including their radii
and rho/c in the finite minimum gives one positive common window. There is
no uniform/effectively computed lower bound, or claim about an infinite alphabet.

For finitely many analytic Kraus maps A_z,l on that SAME enlarged space,

    q_D(z;kappa)=N^-1*sum_l ||A_z,l(kappa)P||_HS^2.

At an off-null endpoint every summand vanishes separately. A nonzero analytic
A_z,l P has positive integer order, so its squared norm has even valuation;
the finite positive sum cannot cancel its leading coefficient. Therefore
nu>=2 is even and c=ceil(sqrt(N+1)) suffices. Products of finite analytic
optical gates and fixed count projectors/record prescriptions provide these
Kraus maps in the ideal sink model. This is stronger than probability
analyticity: q=kappa is a legitimate one-sided analytic probability but
needs a sqrt(kappa)-type amplitude at zero, not an analytic Kraus amplitude.

## What the result does and does not establish

For common bounded h>=0 with h(z0)=0, the off-null ordering gives the stated
raw mean-utility domination, strictly if a reachable germ has positive h.
A classical decoder must be identical across arms AND retuned strengths,
and its induced h must vanish at z0. Known-solution null preparation and
rare normalized success sectors do not supply an exception. K=1 has identical
same-setting spatial laws; its retuning benefit is ordinary control tuning.

The D family must actually allow c*kappa. No same-strength static mirror is
proved, and P140's nonstatic witness is not contradicted without checking its
D-null/record premises. The factor/window alone does not implement D tags,
an efficient sampler, or an inexpensive feedback controller. Synthesis,
precision, source/helper preparation, detector latency, classical work and
wall time are unmatched. The factorial factor may be very large after helpers.
This is a nonuniform local probability/utility obstruction for a FIXED finite
physical model, not an all-strength/adaptive optimizer or practical-cost no-go.
Only this review was written; original source and frozen P141 are unchanged.
