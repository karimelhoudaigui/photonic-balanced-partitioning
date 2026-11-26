# P140 — A fixed-source count law with no passive static mirror

26-Nov-2026. ROOT asked the fixed-source question; P66 derived this example.
Parent 71b146479f8b76773481984746bc1a02bbc63657. Manual only; no population,
code, matrix program, RNG, native/QPU call or manuscript edit. P138 is unchanged.
Verdict: the assertion that EVERY such feedback count law has a static passive
mirror, even for one fixed CF source, is REFUTED. The example is not an optimizer
advantage: a proper group and a trivial classical graph-law mirror reproduce it.

## One-body invariant for the exact fixed source

Use six data modes (a,b,c,d,e,g) and protected flag modes (f1,f2).
The ONE fixed normalized source is |1a,1b,1c>, with every other input vacuum.
For any fixed passive eight-mode unitary W and fixed physical output port j,

    E_W[n_j]=sum_(i in {a,b,c})|W_ji|^2<=1.             (1)

This follows from <a_i^dagger a_h>=delta_ih on the three occupied inputs and
row normalization. Equivalently its one-body density is a rank-three projector.
Vacuum ancillas, passive contraction/loss, or an independent classical mixture
of static passive settings retain this upper bound. No optimum or tomography
is used. Output-dependent relabeling/conditioning is not part of a STATIC raw
physical-port count law; a bunched or nonvacuum-ancilla source is a different source.

## Explicit causal protocol and all 120 ideal outcomes

Let W0 first apply the real balanced Hadamard on a,b, then swap its b output
with the initially vacuum flag f1. The third photon in c is a spectator:

    W0|1a,1b,1c>=(|2a,1c;0f1>-|1c;2f1>)/sqrt(2).      (2)

Unused data/flag modes are vacuum. Measure the flags, then apply I on data
unless (f1,f2)=(2,0), when apply the data swap P_ac. The ONLY nonzero terminal
spatial-count probabilities, including measured flags, are

| data (a,b,c,d,e,g); flags (f1,f2) | Probability B |
| --- | ---: |
| (2,0,1,0,0,0);(0,0) |1/2|
| (1,0,0,0,0,0);(2,0) |1/2|

The remaining 118 occupations among binom(10,3)=120 have probability zero.
No outcome is discarded, no source restart/herald denominator is introduced,
and every attempt injects three photons. Hence

    E_feedback[n_a]=3/2>1.                             (3)

Equations (1)-(3) exclude EVERY possible fixed eight-mode passive W on this
SAME source, not merely the original prefix plus a branch-blind terminal mixer.
Even the data marginal already contradicts (1); full joint records also cannot
match. The conclusion is about this physical-port law, not retained quantum-state
distinguishability or several different input probes.

## An active complex prefix, without a false phase explanation

The example can meet the stronger complex-prefix request. Let omega=exp(2pi*i/3)
and C be DFT3 on data (a,c,d), identity on other data, with matrix
[[1,1,1],[1,omega,omega^2],[1,omega^2,omega]]/sqrt(3).
Set W=(C directsum I_flags)W0. Measure flags, then use V_f=C^dagger except
V_(2,0)=P_ac C^dagger. These two mixers are neither equal nor a conjugate pair.
The occupied-prefix rectangle at rows(a,c), inputs(a,c) is omega/18, nonreal;
thus the active prefix is not made real by row/column phase gauges.

Protected flag projectors commute with C/C^dagger, so this protocol has EXACTLY
the table above. The complex pre/post block cancels; complexity of the prefix
is not the claimed resource. The load-bearing change is measurement-conditioned
non-conjugate routing. P122's conjugate-only count-null has no such premise.
Deferred conditioning would require a photon-count-controlled operation, not
one passive one-particle matrix; (3) proves that distinction on the fixed source.

ROOT supplied a second, smaller check, independently rederived here: two CF
photons, real prefix rows (1,-1,0)/sqrt(2), (1,1,-2)/sqrt(6), (1,1,1)/sqrt(3),
with the last row a flag. Write data coordinates d,s. The flag-zero vector is
(s^dagger)^2/6-(d^dagger)^2/2, with norm squared 5/9 and mean n_d=1
unnormalized; flag-one is sqrt(2)*s^dagger/3, weight 2/9; flag-two has weight 2/9.
Swap d,s only on flag-one: mean n_d=11/9>1. The SAME D controller gives 7/9;
that number is not a globally retuned D bound. No additional input probe is used.

## Distinguishable/group controls and the graph-decoder bridge

For three mutually orthogonal tags, with the SAME protocol, probabilities are
1/4 on each table row plus 1/2 on (1,0,1,0,0,0);(1,0). Thus mean n_a=5/4,
which also rules out a static D implementation on the same CF source.
For an independently variable real a/b splitter reflectivity R, put q=R(1-R).
The B probabilities for flags 0,1,2 are (2q,1-4q,2q), giving mean 1+2q<=3/2.
D has (q,1-2q,q), giving mean 1+q<=5/4. This is a SAME-family
retuned-R concentration contrast, not comparison with arbitrary retuned D optics.
The proper species partition {a,b}|{c} reproduces the complete B law exactly:
only the HOM pair interferes after cancellation. There is no unique three-source
optimization mechanism here, nor a comparison to fully reoptimized controllers.

To use the requested common completion, associate the six data ports with six
receiver vertices of a balanced residual, remove three current vertices, and
freeze the other nine as S0. Keep all positive receiver supports, then greedily
fill to three distinct vertices using paid incremental cut scores and public ties.
Define the rule on all 120 records, including zero-probability ones; partial
helper cuts never become feasible incumbents. Only two completed candidates
occur here: Y2=GreedyComplete({a,c}) and Y1=GreedyComplete({a}).

For any raw utility h of the lifted feasible candidate, including holds,

    E_B h=(h(Y2)+h(Y1))/2,
    E_D h=3h(Y2)/4+h(Y1)/4,
    E_B h-E_D h=(h(Y1)-h(Y2))/4.                        (4)

That sign is graph dependent. A classical fair bit reproduces B's full record
distribution and calls the SAME greedy branch, with the SAME feature/score
work and no optical attempt. If both completed candidates were computed, their
best is fully credited. Thus a favorable graph sign in (4) cannot establish
photonic optimization advantage; the extra partial-count repair is not free.

The ideal hardware is eight addressed modes/three CF photons, two measured
protected flags, data storage and conditional swap/mixer, then terminal counts.
PNR/latency/source-preparation/calibration and a Lucy in-shot control API remain
uncertified. No hardware use or changed experiment is authorized here.
The useful result is the exact fixed-source nonstatic-count witness (3), with
its proper-group/classical optimization veto preserved. A further mechanism
must change that last missing implication, not relabel this witness as success.
