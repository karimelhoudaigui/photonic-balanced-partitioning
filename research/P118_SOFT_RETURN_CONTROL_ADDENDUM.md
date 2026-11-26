# P118 continuation: a weak-soft-return control, not a global walk no-go

26 November 2026. **MANUAL DERIVATION; soft-return route remains OPEN.**
This is separate from the strict note1111db217354a9c9183dfbd62ae49185753b4152,
research/P118_NONRETURN_WALK_ROUTE.md154l, SHA256
ceb0a6523ff7f31742887394b6e166fa5ee78535ded56ccb238265973212d21a.
ROOT proposed the bound; its derivation and the necessary loss restriction
are checked below. No numerical/symbolic execution or experiment is implied.

## Fixed model and a nearby monomial step

Keep C4's eight directed-arc modes and a fixed lossless vertex-local walk
U=S (directsum_v C_v), with S the arc shift and each C_v a2x2 unitary.
Allow both diagonal amplitudes to have modulus<=epsilon,0<=epsilon<1.
Thus this is a CHANGED coin class, not a strict no-return walk. Let L>=0
be an integer number of identical coherent steps, and use a known CF input
of K in{2,3,4} photons. There is no entangled/coherent superposition source.

Write C_v=[[a,b],[c,d]]. Row/column normalization gives

    |a|=|d|=r_v<=epsilon, |b|=|c|=sqrt(1-r_v^2)>0.

Take M_v=[[0,b/|b|],[c/|c|,0]], a unitary monomial with zero diagonal.
The diagonal part of C_v-M_v has norm r_v; its off-diagonal part has norm
1-sqrt(1-r_v^2). By the triangle inequality and monotonicity in r_v,

    ||C_v-M_v||op<=delta,
    delta=epsilon+1-sqrt(1-epsilon^2).                    (1)

This constructs one close monomial; no exact closest-distance formula is
claimed. Its phase normalization is defined because epsilon<1. For epsilon=0,
M_v=C_v and delta=0. Direct sums and the unitary shift preserve this bound:
U_0=S (directsum_v M_v) is monomial and ||U-U_0||op<=delta.

Telescoping L powers of unitary operators gives

    ||U^L-U_0^L||op<=L delta.                            (2)

For L=0 both operators are I. The unoptimized bound can exceed2 and then
is loose; the final probability/TV bounds are capped. Phases, graph features,
compilation and input orientation must be shared/paid for the control.

## Bosonic concentration near a known CF output

Let A be the occupied input modes. U_0^L sends them to a known distinct
set p_L(A), hence its normalized K-boson output is exp(i theta)|n_0>,
where n_0 is a known CF occupation. The K-particle tensor telescoping bound,
restricted to the symmetric subspace, gives

    ||Gamma_K(U^L)|A>-exp(i theta)|n_0>||<=K L delta.

Project onto the orthogonal complement of |n_0>. The reference vector
vanishes there, so the complete lossless PNR law satisfies

    P_B(n!=n_0)<=min(1,K^2 L^2 delta^2).                  (3)

This is a NUMBER-MEASUREMENT concentration bound. It does not bound the
full output quantum-state trace distance quadratically; coherent observables
can distinguish amplitudes at first order. No output patterns are discarded.

## Distinguishable control and raw-law comparison

For each independently prepared distinguishable input particle at i,
equation(2) bounds its one-particle vector difference from the corresponding
phase times |p_L(i)> by L delta. Therefore its probability of landing
outside that designated mode is at most L^2 delta^2. If no particle misses,
the observed occupation is n_0. Union bound gives

    P_D(n!=n_0)<=min(1,K L^2 delta^2).                    (4)

Some incorrectly labelled destinations could still yield n_0; treating every
label error as a count error only enlarges this bound. Detection never needs
to recover the labels. For any count law P, TV(P,pointmass_n0)=P(n!=n0).
Triangle inequality with the SAME reference consequently proves

    TV(P_B,P_D)<=tau=min(1,K(K+1)L^2 delta^2).            (5)

Here D uses the same U; an independently optimized D family contains this
member. This is not a guarantee for all reparametrized D coins, and not a
matched-cost optimum statement. A bounded count-score of range R differs
in mean by at most R*tau, and any raw count event differs by at most tau.

## Exactly which loss/decoder operations preserve the quadratic bound?

A common CLASSICAL stochastic kernel Kappa on the already specified count
alphabet contracts total variation. Thus(5) holds after portwise independent
thinning (including uniform loss), thresholding, common randomized balanced
repair, or any other common count-level decoder. The reference may then
become a nontrivial distribution Kappa(pointmass_n0), but it is the SAME
for B and D. No loss outcome or source photon is dropped from the ledger.

This is NOT a claim for an arbitrary subsequent coherent mode-mixing or
correlated-loss optical channel. Equal count laws hide different quantum/
internal-label states: a later balanced beamsplitter already creates the HOM
contrast from a two-mode CF input even when the preceding walk is monomial.
Contraction of measured count laws cannot be invoked through that operation.
The count-kernel restriction was raised independently and accepted by ROOT.

The bound is unconditional on the raw attempt. Rare herald/CF conditioning
can amplify differences; no postselected-TV or normalized-success guarantee
is inherited. Unknown preparation error, filtering and device loss are not
silently supplied by the ideal CF or common-kernel hypotheses.

## What this changes, and the remaining scientific gap

Since delta=epsilon+epsilon^2/(1+sqrt(1-epsilon^2)), small epsilon gives
delta of order epsilon. For fixed K, L*epsilon tending to0 forces tau to0:
a shallow walk with small return amplitude has no large single-attempt B/D
count advantage. At L of order1/epsilon, the bound may be order1/vacuous.
It proves no impossibility in that deeper regime, nor a beneficial signal.

That is the next OPEN regime: a concrete nonmonomial soft coin, graph-only
compiler and all-output statistic must still survive independently optimized
D and classical-memory/intensity/pair controls. Nothing here supplies that
useful graph-cost/hazard bridge or a new experimental population. L is circuit
depth, not measured time; every attempt still pays K injected photons plus
all L steps, preparation, classical memory/decoding and scoring. Deeper-device
loss/phase capabilities and total cost remain unknown. No DEV/run is authorized.

Only this addendum was written. No import/AST, scripted calculation, native,
test, simulation, RNG, graph draw, runner/QPU, manuscript edit, push or change
to the frozen strict note, P110 code/contracts or raw data occurred.
