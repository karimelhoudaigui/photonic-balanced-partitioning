# P121: a catalytic-strength instantiation of the P74 proposal screen

26 November 2026. Manual derivation from ROOT's proposed threshold, using
the exact phase-free P116 gate and P74's existing product/uniform screen.
This is shared-proposal research with self-review, not an independent review
of P116 or a novelty claim. No code, import, AST, numerical evaluation,
test, RNG, graph generation, native call, runner, QPU or manuscript action.
Only this file is added; the original P116 source remains unchanged.

## Exact inputs and scope

P116 source: `research/P116_MEASUREMENT_INTERACTION_ROUTE.md`,315 lines,
commit `fbe08686fe69dd3de14384013fdc0da98e8da541`, SHA256
`27679d1a076d5e5a48844c11b6a0243e0b9f9570bbcc59de883f093c4c921db9`.
Its exact filter is the mathematical input; its independent review remains
separate. P74 `research/P74_heralded_graph_cost_resource_screen.md`, sections
4–7, was read in full context; SHA256
`0b4b4bbca399ab8c80d4b5f152b7eff1f3c8b50c344e3a2d2ab8ba5966cea12b`.
That record already supplies the general
no-recovery product bound and uniform-proposal interpretation. This note
instantiates those statements for a strength-dependent filter profile;
it does not rediscover the P74 screen or its fixed-CZ application.

Fix L logical bits, each one photon in a pair of vertex rails. The fixed
paired code has D=2^L states and selects L out of2L UNIT vertices. Equal-mass
paired blocks also qualify if their balance is certified. This is a subset
of the full bisection space, not D=binom(2L,L). Complementary logical states
can describe the same unoriented partition; treating both identically in
the two samplers preserves every inequality below.

Each required accepted gate, on this valid logical code, has Kraus operator

    K_e=sqrt(h(gamma_e))*exp(−gamma_e*Pi_e/2),
    h(gamma)=exp(−gamma)/(1+2sqrt(1−exp(−gamma)))^4,        (1)

where Pi_e is the cut projector and gamma_e>0. Thus
`||K_e||op<=sqrt(h(gamma_e))`, including entangled input registers.
The actual accepted probability is h times an expectation, not h itself.
The bound holds for arbitrary unitary mixers ON THE LOGICAL CODE between
these gates. A physical passive mesh leaking out of that code needs a new
full-Fock bound: its projected logical matrix cannot be composed by fiat.
Arbitrary logical mixers are granted for this upper bound, not declared
native or free; their physical synthesis/resources must also be paid.

## The sufficient threshold theorem

Assume L>=5 and that the STIPULATED compiler actually requires at least
g>=L−1 accepted catalytic heralds on every completed attempt, each with

    gamma_e >= gamma0 := log(64/63).                       (2)

An uncorrected failure holds the common incumbent. No other failure branch
is returned as a candidate. Every accepted pattern is counted in the gate's
total conditional success cap; an unbounded collection of equivalent heralds
cannot be represented by only one K_e. Preparations/readout are contractions
or trace-nonincreasing physical stages, without conditioning away their cost.

Then for every logical output state y, its unconditional SUCCESSFUL proposal
mass satisfies

    q_B(y) <= (13/32)^g <= 2^(−L).                        (3)

Consequently uniform logical sampling pointwise dominates these successful
proposals even with arbitrary coherent mixers between the accepted gates.
Nothing here asserts pointwise order of the full repaired Markov kernel.

Proof of the new profile substitution. Write rho=exp(−gamma). Under(2),
rho<=63/64 and sqrt(1−rho)>=1/8, so directly from(1)

    h(gamma) <= (63/64)/(5/4)^4 = 252/625 < 13/32.         (4)

The last comparison is exact:252*32=8064<8125=13*625. For any fixed
all-accepted circuit, submultiplicativity of operator norms gives
`trace(sigma_success)<=product_e h(gamma_e)<=(13/32)^g`.
This is independent of the input state and interleaved code-unitary choices;
each diagonal output mass is at most the total mass. Equivalently one can
apply P74's conditional tower bound with this cap. No independence of the
gate-success events is assumed. Adaptive choices obey the same bound when
every conditional accepted cap and the minimum required gate count hold.

Put q=13/32. Since `13^4=28561<32768=32^3`, we have q^4<1/32.
Also q<1/2. Therefore for L>=5,g>=L−1,

    q^g <= q^(L−1)=q^4*q^(L−5)
         <=2^(−5)*2^(−(L−5))=2^(−L).                   (5)

Preparation or final-feasibility failures can only reduce successful mass.
This proves(3). A positive observation for arbitrary finite-strength gates
would not contradict it unless every hypothesis above were established.

## What pointwise domination means, and what it does not

For any set A of paired-code candidates, summing(3) gives
`q_B(A)<=|A|/2^L`. Uniform independent bits produce that candidate mass
without a cost oracle or known optimum; scoring remains paid. With a common
incumbent and retain-the-better scoring, P74 transfers this order to the
one-attempt best-recorded-cost CDF, using cost sublevel sets below the
incumbent. Failures are paid holds. Above its cost both CDFs equal1.

On this SAME FIXED paired code, if the cap holds conditionally after every
history, P74's induction bounds T-attempt hits of a fixed sublevel A by
`1−(1−|A|/2^L)^T`, attained by iid uniform candidates. This is a raw-attempt
count statement, not a wall-clock or CPU/photon equivalence. Changing the
pairing changes A's intersection with the code; no fixed-hit-rate formula
is asserted for arbitrary histories that change the candidate universe.

An admissible D bypass can generate the identical uniform code law by
disjoint single-photon Hadamards. All helper photons may be routed straight
to separate detectors if an equal nominal photon/source budget is required.
Extra internal distinguishability is unnecessary for this block-diagonal
law. A common independent preparation/readout success factor multiplies
both sides; arbitrary unequal/path-dependent loss does not. No actual
hardware capability or matched-runtime measurement is supplied here.

The counted catalytic layout pays at least L data photons plus2g fresh
helpers, and2L+4g modes when spatially unrolled, before any extra mixer or
preparation resources. L=5,g=4 already means at least13
injected photons/26 modes in that layout, outside the4-photon/8-mode witness.
Serial early abort can save later helpers only when truly not injected;
it does not remove the attempt-count bound. The actual source, ancilla,
flag, delay, graph compilation, decoder and scoring costs remain in a full
ledger, just as required by P74. Uniform's classical costs also remain paid.

## Exact open boundaries and disposition

The condition g>=L−1 is a COMPILER PREMISE, not a lower bound proved from
graph connectedness. Gates can cancel, be omitted, compiled jointly or have
zero effective angles; paired encoding can make some graph edges constant.
The theorem does not forbid such changes and cannot charge missing gates.

Weak gamma_e<gamma0 remains outside this uniform-cap substitution; indeed
h(gamma)->1 as gamma->0. P116's refinement tradeoff still applies to its
specific repeated weak-gate construction, not every weak-interaction scheme.
L<=4 with only g>=L−1 is not covered by(5); other sufficient product bounds
may hold but are not presumed. The2-bit one-edge X-mixer veto is P116's
separate result, not an application of this L>=5 theorem.

All-record decoding/recovery, repeat-until-success, multiplexing several
accepted corrected outcomes, changed sources, coherent ancillary reuse and
jointly compiled gates require their TOTAL instrument cap and full resource
accounting. An individual pattern's h cannot bound their sum. These are
open architecture changes, not counterexamples satisfying this contract.

KEEP(3) as a scoped negative screen pending independent review. It rejects
a raw-attempt optimization benefit in this no-recovery strength/gate-count
regime; it does not reject all measurement-induced optimization. Passing
outside the screen
would not establish a positive result, matched total cost, novelty or QPU
readiness. P116 and all earlier negative results remain preserved. No new
experiment is authorized; the user's positive optimization target is OPEN.
