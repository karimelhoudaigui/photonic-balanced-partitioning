# P122: conjugate feedback can have exactly a static terminal count law

26-Nov-2026. Manual post-freeze falsifier for P116's SPECIFIC controller.
Target source fbe08686fe69dd3de14384013fdc0da98e8da541,
research/P116_MEASUREMENT_INTERACTION_ROUTE.md315l, fully read at ROOT.
This is a new analytic claim for non-author review, not an executed test.
The source is preserved unchanged. No numerical or symbolic program is run.

## General finite passive-count lemma

Let W be a REAL passive one-particle unitary on data and flag modes.
Inject a fixed normalized Fock state; in the distinguishable arm all
occupied input particles instead have mutually orthogonal internal tags.
Photon counting ignores tags. Partition output ports into flags and data.
Measure the flags f, then apply a data unitary V_f chosen from EXACTLY
{V,conjugate(V)}, with an arbitrary deterministic choice for every f.
Flag modes are protected and not mixed or reused. Finally count all data.

Then the COMPLETE joint flag/data terminal count law equals that of the
single static passive circuit

    U=(V directsum I_flags) W,                          (1)

for B and independently for D. No normalization on selected flags is used.
This holds before any common classical count decoder or scoring operation.
It does not assert equality of the retained quantum instruments.

Proof: for a specified joint occupation(f,n), the causal probability is
the probability obtained from

    U_f=(V_f directsum I_flags) W.                       (2)

Indeed the projector onto flag f commutes with the later data-only unitary,
and the already observed flag is not subsequently remixed. This identity
applies branchwise; it is not a general license to replace feed-forward by
one unitary without checking its probabilities.

If V_f=V, equation(2) is U. If V_f=conjugate(V), reality of W and the flag
identity gives U_f=conjugate(U). The repeated-row/input-column matrix is
therefore either M or conjugate(M), at the SAME port labels. For B,

    per(conjugate(M))=conjugate(per(M)),
    p_B=|per(M)|^2/(product output! product input!),

so the normalized Fock probability is identical. For the fully tagged D
arm, each labeled assignment probability is a product of |M_ij|^2.
All those intensities and their unlabelled occupation sum are also identical.
For CF input the latter is per(|M|^2)/product output!; no extra factorial
or coherent erasure of tags is introduced. Thus every joint outcome agrees.
Summing any events, conditioning on an event of nonzero common probability,
or applying a common classical decoder preserves this equality. There is
no approximation, grid range, small-angle assumption or discarded flag.

## Application to the exact P116 controller

The prescribed W_e is real: source Hadamards, rail permutations/X swaps,
real balanced endpoint splitter and its inverse, real B_R catalysts, and
real passive attenuator dilations. Its graph compiler uses real gamma/R/
attenuation values. No additional complex prefix phase is specified.
The product mixer on the data rails satisfies

    M_theta=exp(-i theta X) tensor exp(-i theta X),
    M_(-theta)=conjugate(M_theta).                       (3)

Under the intended physical reading, the one-particle data matrix V_theta
has two disjoint2x2 blocks with
cos(theta) on the diagonal and -i sin(theta) off diagonal. This also defines
the mixer on ALL retained Fock sectors, not only the dual-rail code.

Typing caveat: P116 uses the same M symbol for a logical tensor-product
matrix and a one-particle matrix. They are not the same operator. Precisely,
V_theta=exp(-i theta X) directsum exp(-i theta X), and its second
quantization restricts to the stated logical M_theta on the code. The
ambiguous frozen source must not be executed as if this distinction were
resolved. Under a literal numerical reading that inserts the4x4 logical
tensor matrix as a one-particle matrix, one gets a DIFFERENT device; its
negative-angle matrix is still its conjugate, so the count-null lemma holds
there too. This proof does not silently repair P116's full instrument.

P116 chooses theta on f=(1,1,0,0) and -theta on every other flag. Equations
(1)--(3) therefore prove that its all-record adaptive count law is EXACTLY
the static terminal law with +theta on EVERY flag, for B and for D.
Partial data number, bunching, wrong-code and vacuum branches are included.
The graph's top-two-count/tie decoder cannot reveal a difference that is
absent from each count probability. Independent parameter reoptimization
does not change the identity at any common parameter setting.

This rejects THIS sign-switch controller as a distinct count-level adaptive
mechanism. A different retained quantum state may remain in each branch;
later non-conjugate coherent operations could detect it, but those operations
are not part of the frozen P116 controller. No claim that every measurement
instrument is passive/static or every feedback policy is useless follows.

## What is preserved and what remains genuinely open

The catalytic Kraus interaction, phase-free weak gate, h(gamma) resource
law and one-edge accepted-record veto in P116 are separate claims. This
lemma neither changes them nor proves that failure records cannot help.
Retaining failures may change a success-only statistic; it simply gives
the SAME law as a static all-record circuit for this particular controller.
B and D can still differ on that static circuit. No optimizer advantage,
whole-law classical hardness or equal-wall-time conclusion is inferred.

To escape this symmetry one must change a premise, for example choose
branch-dependent mixer magnitudes instead of conjugate signs, introduce a
genuinely complex prefix, add further non-conjugate stages, or use a different
source/instrument. Each is a new prospectively specified route, not a patch
to the frozen claim. None guarantees useful graph-cost bias, survival of
independently optimized D/classical controls, scalable resource costs or
real Lucy capability. P116's four/six-candidate classical frontier remains
mandatory. Preserve failed controller and evidence; CLAIM-042 remains OPEN.
