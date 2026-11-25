# P70: explicit rank-one bosonic transport, with decisive classical falsifiers

25-Nov-2026. STATIC derivation from the coordinator's candidate, after P69's
proof file was frozen. No numerical calculation, import, test, random draw,
source qualification, graph generation, QPU call or manuscript edit.
This file is written without retrying the worktree's unavailable Git index.

**Verdict: the restricted bosonic separation is proved; the positive
optimization gate FAILS.** For L>=3 the specified bosonic mixture exceeds
a proved upper bound for EVERY independently chosen common-interferometer
distinguishable-photon unitary of cross rank at most one. It nevertheless
loses to an elementary feasible classical proposal and to distinguishable
whole-clique permutations of higher cross rank. The rank restriction is
essential; this is not a quantum optimization advantage or a novelty claim.

## 1. Graph, source, target and optimum-blind rule

Use the P66 four-clique graph: A1,A2,B1,B2 have L vertices each, heavy
within-clique edges of weight M>0, matched edges of weight h>0 between
A1,A2 and B1,B2, with M(L-1)>Lh. There are either no edges between
CA=A1 union A2 and CB=B1 union B2, or all these edges have a common
weight 0<w<h/L. Take L>=3 for the strict comparison; L=2 is treated below.
There are N=4L modes and K=2L injected photons.

Start from S=A1 union B1, with one photon at every occupied vertex and
vacuum elsewhere. More generally the same rule applies to any of the four
bad whole-clique states. The two improving outputs are the full-CF subsets
CA,CB. The P66 cost proof shows every other feasible state is either another
bad whole-clique state of equal cost or an uphill partial-clique state.

Choose X uniformly from the two currently occupied whole cliques and Y
uniformly from the two vacant whole cliques, independently. Selection uses
only these graph cliques and the current subset. It does not inspect which
pair joins a good target, evaluate C*, select a known optimal partition,
use a target mask, or retain only cross-block choices. The four cliques can
be extracted from the maximal-weight-edge graph; this same graph access
is available to every comparator. Evaluation of success uses CA,CB only
after defining the rule.

For any clique Z let bZ be its normalized uniform one-particle mode. Apply

    U_XY=I-|bX><bX|-|bY><bY|
           +i|bX><bY|+i|bY><bX|.

It is identity on the common orthogonal complement and equals
[0 i; i 0] on span{bX,bY}; hence it is unitary. It exchanges the two bright
modes with phase i and leaves all their dark modes unchanged. If X,Y lie
in different CA/CB blocks, each optical cross block has rank one. If they
lie in the same block, the optical cross rank is zero. Every realization
therefore has cross rank at most one relative to these fixed blocks.

The rule is random and graph-covariant in LAW. Individual realized choices
can break automorphisms of (graph,current subset); pathwise exact covariance
is not assumed. The arbitrary-marked-history low-rank result P69 still
applies, and there is no conflict with it.

Measure complete output counts. A collision is a paid self-loop; a CF
output is scored with the graph cost. For zero-temperature search accept
all non-uphill outputs and reject uphill ones. Every attempt injects the
same K photons, including collisions, neutral outputs and rejections.
There is no repeat-until-CF normalization or free heralded preparation.

## 2. Exact bosonic transfer probability

Define a=L!/L^L. Consider a cross-block choice, for example X=B1,Y=A2.
The other occupied clique Z=A1 is completely unaffected. Reaching the good
output CA requires every photon originally in X to leave X and occupy Y
once each; the Z output stays its original CF state.

The source has overlap sqrt(a) with the normalized state containing L
photons in bX. To see the normalization explicitly,

    |L_bX>=(bX^dagger)^L|0>/sqrt(L!),
    <L_bX|1_X>=sqrt(L!)*L^(-L/2).

All other source components contain at least one dark-X photon. U_XY leaves
the dark-X subspace fixed, so those components cannot contribute to a target
with X vacuum. On the sole contributing bright component,

    Gamma(U_XY)|L_bX>=i^L|L_bY>.

The target CF state on Y has overlap sqrt(a) with |L_bY>. Thus the full
normalized K-photon target amplitude is i^L*a, and its raw probability is

    p_B(good target | cross choice)=a^2=(L!)^2/L^(2L).

No physical projection onto the bright component was performed or declared
free: both small overlaps are already paid in this raw probability. There
are no cancelling contributions from other dark sectors because those
sectors have no support on the required X-vacuum target.

A direct permanent derivation checks the same normalization. The relevant
full K by K submatrix splits into an identity on Z and the L by L matrix
i*J_L/L from X to Y. Hence its permanent is i^L*L!/L^L. Both input and
target are CF, so every Fock factorial is one.

Of the four equally likely choices, B1 to A2 and A1 to B2 are cross-block
and each permits exactly one good target. The other two choices preserve
component/block photon totals and cannot reach either good target. Therefore

    p_B,mixture=(1/2)*a^2=(L!)^2/(2*L^(2L)).

Other outcomes include collisions AND partial CF subsets; they are not
silently identified with one another or discarded. Their total probability
is one minus the displayed good-target probability by unitarity. No claim
that all failures are collisions is made.

## 3. A sharper universal distinguishable rank-one upper bound

The comparison is against ANY independently chosen unitary U of cross rank
at most one, with arbitrary within-block matrices, graph/current/label data
and any classical parameter-selection computation. It is not restricted to
U_XY, the same optical moduli, the same chosen pair, or the same parameters.
Every labeled photon propagates independently through the SAME one-particle
unitary, and the source and raw CF decoder remain those in section 1.
Label-controlled different interferometers, added modes or a different
classical decoder are separate resource/model classes.

Write U=[A C;D B] in CA/CB blocks. If C=0 then target CA is impossible.
Otherwise rank-one singular-value factorization gives

    C=sigma*u*v^dagger, ||u||=||v||=1, 0<sigma<=1.

For a photon at an occupied input j in CB, crossing into CA has probability
sigma^2*|v_j|^2. All L CB photons must cross to reach target CA. Independence
and AM--GM give

    P(all CB photons cross)
       =sigma^(2L)*product_{j in SB}|v_j|^2<=L^(-L).

Conditional on crossing, every such photon has the SAME output distribution
p_i=|u_i|^2, independently of its input label. If a crossing probability is
zero, the target probability was already zero and no conditioning is needed.

Independently, consider the L photons initially in CA. Reaching target CA
requires all of them to end in CA at L DISTINCT vertices, forming some
L-element set Y0. If they cross out or collide, the full-CF target fails.
For each eligible Y0, the CB photons must fill the complementary L-element
set X0=CA minus Y0 exactly once each. Conditional on all CB photons crossing,

    P(CB photons fill X0)=L!*product_{i in X0}p_i
                          <=L!*(sum_{i in X0}p_i/L)^L
                          <=L!/L^L.

The possible Y0 events depend only on the CA photons and are independent
of the CB photon outcomes. Their unconditioned total probability is at most
one. Summing over them therefore proves

    p_D(target CA)<=L!/L^(2L).

Unitarity makes rank(D)=rank(C), as established by the two isometric
inclusions in P69. Exchanging CA,CB proves the same bound for the other
target. The two events are disjoint, so for EVERY such D matrix,

    p_D(either good target)<=min(1,2*(L!)/L^(2L)).

The bound also holds for arbitrary randomized mixtures or history-dependent
choices whose every realized NET matrix has cross rank at most one. The
proof has not restricted a D optimizer to the bosonic parameters, and even
supplying D with favorable graph knowledge cannot violate this bound.

## 4. Strict restricted separation, and its smallest boundary

For L>=3, L!>4. Comparing the exact B mixture probability with the universal
D upper bound yields

    p_B,mixture / [2*(L!)/L^(2L)] = L!/4 >1.

Thus this raw event has a strict interference-dependent separation against
ALL common-interferometer D models in the specified cross-rank-one class.
Both use the same CF source and K=2L injected photons per raw attempt. This
is a per-attempt/per-injected-photon event comparison; it is NOT a matched
TOTAL-resource optimizer claim, a hardware-time measurement or an unrestricted
D comparison.

For the SAME bright-swap circuit and same uniform pair choice, the D target
submatrix has every squared entry 1/L^2. Its permanent gives

    p_D,mixture,samecircuit=(1/2)*(L!)/L^(2L),
    p_B,mixture / p_D,mixture,samecircuit = L!.

The factor L! is the coherent sum over the L! matchings, already reduced by
the raw source/target bottleneck. The universal independently reoptimized
bound allows D a factor four relative to this same-circuit mixture.

At L=2 the B mixture has probability 1/8, while the universal D bound is
1/4, so this argument certifies NO strict separation. A rank-one D bright-
swap aimed always at one cross pair has raw target probability 1/8 and
already matches the B mixture. The strict result is stated only for L>=3.
These are symbolic identities, not numerical test or experiment results.

## 5. Decisive classical and unrestricted-D falsifiers

A classical feasible proposal chooses EXACTLY the same X,Y uniformly and
sets

    T=(S minus X) union Y.

It always moves the whole clique and is always a balanced feasible subset.
Two of the four choices are good, so its raw success probability is 1/2.
The other two are neutral bad whole-clique states. It uses no C*, optimal
mask, known target selection or postselection. Its graph/clique extraction,
choice, subset update and score are paid classical operations of polynomial
cost. This is the appropriate immediate feasible countercontrol.

It exceeds the optical B success probability by the factor

    (1/2)/p_B,mixture=1/a^2.

For fixed-horizon zero-temperature repetitions, current states remain in B
until success, and fresh uniform pair choices give constant success hazards:

    P_B(success by T)=1-(1-a^2/2)^T,
    P_classical(success by T)=1-(1/2)^T.

The expected attempts, when continued until success, are 2/a^2 and 2,
respectively. The optical process additionally consumes 2L photons per
attempt, including its many failures. No simulator time measurements are
needed to see that this specific mechanism fails its feasible-search gate.
A still stronger classical routine can inspect the matched clique structure
and output a certified optimum directly; this is already known for this
engineered family.

Even the distinguishable model escapes the separation if the rank restriction
is removed. For the same uniformly selected X,Y, use a passive PERMUTATION
exchanging all L individual mode pairs of X and Y, leaving the other cliques
fixed. This maps the CF source to T deterministically, without collisions.
Its cross rank is L on cross choices and zero on same-block choices. Its
mixture success probability is also 1/2, with the same photon number and no
selection of a known good pair. Thus rank-one reoptimization is a genuine
architectural restriction; it cannot stand in for unrestricted strong D
control or an end-to-end QPU advantage.

## 6. Interpretation and scientific disposition

This example isolates a bosonic contribution rather than merely reporting
a same-unitary discrepancy: collective transport through a single shared
bright channel has a factorial enhancement that survives independent D
reoptimization WITHIN that channel-rank class. The source was a known bad
CF configuration; the good output was not prepared as input. Both bunching
and unbunching suppress its absolute physical probability.

The contribution is nevertheless a poor optimization mechanism. The bright
bottleneck is unnecessary for the classical whole-clique move or a higher-
rank optical permutation. The four-clique graph is explicitly engineered
and classically transparent. No held-out instance result, broad algorithmic
advantage, novelty, source feasibility on Lucy, calibrated optical depth,
loss tolerance or actual QPU performance is established.

The construction is passive-unitary mathematics; no squeezed source or
additional nonlinear resource is assumed. Implementing the uniform-mode
transforms, phase swap, source routing and detection on actual hardware
would incur real compilation, calibration, source, loss and readout costs.
This static note authorizes none of those calls and makes no readiness claim.

**Decision: KEEP as a fully scoped analytical mechanism/countercontrol
fixture; REJECT as a positive photonic optimization result.** The global
research objective remains open. A finite independent implementation check,
if useful, must first receive its own prospective input/command/output
contract; none was run for this proof-only checkpoint.
