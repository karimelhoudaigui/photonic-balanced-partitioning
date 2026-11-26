# P116: measured catalytic cut interaction, its weak branch and its vetoes

26 November 2026; parent1b88942c37df8238890c5bca1b5cfb7e6341cd13.
**Manual research checkpoint; positive optimizer objective remains OPEN.**
No code/import/AST/test/RNG/graph generation/native call/run/QPU/manuscript
change occurred. This file alone is added. All derivations are hand algebra;
independent proof review and any novelty assessment remain pending.
P105 and P102 were read in full; accepted P84/P86/P87/P99/P109 contracts
are boundaries, not claims that every passive/measurement protocol fails.

The substantive move is an exact nonunitary graph-edge interaction induced
by two measured single-photon helpers, with a causal all-record feed-forward
extension. It is not a new name for a fixed passive sampling ansatz or an
NS/CNOT success probability. The primitive is adjacent to established
catalysis/entanglement filtering. A ROOT counter-continuation introduced the
one-qubit rail flip in section3; I independently checked its algebra and
derived the closed compiler and resource law. This is shared-proposal
research with self-review, not a blind independent discovery certificate.

## 1. Fully specified small encoding and graph compiler

Four vertex modes are `(a0,a1,b0,b1)`. Two data photons encode
`|xy>=a_x† b_y†|vac>`, x,y in{0,1}; thus exactly two vertices are selected.
This includes four of the six balanced subsets, not all balanced partitions.
The pairing/vertex marks must be chosen by a declared graph-independent
uniform permutation, or by a paid public coarsener shared with controls.
Two more known CF helper photons occupy c+,c−; two vacuum ports dA,dB
provide attenuator flags. Total: EIGHT modes, FOUR input photons, no hidden
polarization/copy modes. |00> preparation followed by two disjoint Hadamard
splitters prepares |++>; it prepares no known graph solution.

Given nonnegative graph weights, select a positive cross-pair edge e with
the public law w_e/sum(cross-pair weights); zero total means bypass. Rail
permutations put its endpoint occupations in the logical bits of interest.
For a fixed declared beta>0, set gamma=beta*w_e and rho=exp(−gamma).
The desired elementary cut filter is

    F_e(gamma)=exp[−gamma*(x XOR y)/2]
             =diag(1,sqrt(rho),sqrt(rho),1).                 (1)

The compiler in section3 gives every beam splitter/attenuator parameter from
gamma alone. Edge selection, exp/sqrt precision, pairing, all graph features
and scoring are paid; no C*, optimum mask or optimal partition is an input.
For general graphs this is one edge operation, not a proved global optimizer.
Edges within a rail pair are always cut in this encoding and are constants.

## 2. Normalized Fock derivation of the interaction

One catalyst mixes a signal b and a helper c by the REAL unitary

    B_R=[[r,t],[-t,r]], r=sqrt(R),t=sqrt(1−R), 0<R<1.

For input |n>_b|1>_c, expand `(r b†−t c†)^n(t b†+r c†)/sqrt(n!)`.
Projection onto exactly one c photon returns the normalized signal |n>
with amplitude

    k(n)=r^(n−1)[R−n(1−R)].                               (2)

The two terms are helper-stays and helper/data exchange, coherently added.
Output factorials are already included in this normalized Fock coefficient.
In particular k(0)=r, k(1)=2R−1, k(2)=r(3R−2), and
`k(0)k(2)−k(1)^2=−(1−R)^2`. A geometric independent one-mode attenuation
has zero such difference: this conditional operation is not one-particle
attenuation or a deterministic local phase.

Mix the two endpoint rails by the balanced real Hadamard splitter, catalyze
its + and − modes independently with c+,c−, and undo that splitter.
For |11>, HOM produces `( |20>−|02> )/sqrt(2)`; both terms acquire the
same factor k(0)k(2), and recombination returns |11>. For |10>/|01>, both
one-photon superposition components acquire k(0)k(1). Thus measuring helper
counts(1,1), without measuring the data, gives the EXACT code-preserving map

    G_R=diag(g0,g1,g1,g2),
    g0=R, g1=sqrt(R)(2R−1), g2=R(3R−2).                   (3)

All other helper outcomes are real outcomes, not zero-probability errors.
The nonfactorizable invariant `g0*g2−g1²=−R(1−R)²` is explicit. The result
uses indistinguishability with BOTH helpers; a D calculation must not reuse
this pure Kraus operator after merely changing a final permanent.
This conditional logical map escapes the no-ancilla deterministic-code
premises of P84/P86/P87. A deferred one-branch witness still IS a global
passive four-photon experiment. It does not escape every passive physical
model; section6's causal branch settings are the extra architecture. P99's
specific weak-chain premises and P109's admissible rescaling must be checked,
not declared applicable or inapplicable just from the word interaction.

## 3. Important correction: a phase-free branch has h tending to one

First, the apparent resource veto: without a logical X, making even-parity
amplitudes equal by local diagonal contractions gives attractive magnitudes
only when `(3−sqrt(2))/7<R<(3+sqrt(2))/7`. The maximum common even amplitude
is `min(R,R*(2−3R))<=1/3`, hence its scalar success prefactor is<=1/9.
Indeed local diagonal factors leave `|g1|²/|g0*g2|` invariant, and balance
requires H<=min(|g0|,|g2|); solving the attractive-ratio inequality gives
that interval, with the maximum at R=1/3. This is a scoped gate bound.
Where all four entries are nonzero, its phase invariant is pi, retaining
a CZ byproduct up to local Zs.
At R=1/2 this balanced map is `(1/4)diag(1,0,0,−1)`, the known parity-filter
profile; it is not a new gate. This veto DOES NOT cover local X conjugation.

Now choose 2/3<R<1, where all entries in(3) are positive. Conjugate G_R by
X on B (a physical swap of b0,b1). It becomes diag(g1,g0,g2,g1).
Put s=3R−2 and apply local no-loss attenuator amplitudes

    L_A=diag(sqrt(s),1), L_B=diag(1,sqrt(s)).

Each uses one vacuum port; 0<s<1, so no noiseless amplification is assumed.
Direct multiplication gives

    K_e=(L_A⊗L_B) X_B G_R X_B
       =H diag(1,sqrt(rho),sqrt(rho),1),
    H=sqrt(R)(2R−1)sqrt(3R−2),
    rho=R(3R−2)/(2R−1)^2 <1,
    h:=H²=R(2R−1)^2(3R−2).                              (4)

For any FINITE gamma>0 the exact graph-to-hardware compiler is

    z=sqrt(1−exp(−gamma)), R=(1+z)/(1+2z),
    h(gamma)=exp(−gamma)/(1+2sqrt(1−exp(−gamma)))^4.       (5)

Here R is strictly between2/3 and1; (4) equals sqrt(h)*F_e with NO CZ
correction. This refutes a global extension of the earlier<=1/9 veto.
For an arbitrary normalized code state psi the ACTUAL herald probability is
`h*<psi|exp(−gamma*Pi_e)|psi>`, between h*rho and h, not h itself.
With |++> it is h(1+rho)/2. Its accepted state has concurrence
`(1−rho)/(1+rho)>0`: the interaction preserves quantum coherence,
although entanglement or conditional cut bias alone is no optimizer benefit.

These formulas concern IDEAL helper(1,1), attenuator flags(0,0), known
four-photon CF preparation and the code. Arbitrary intermediate count states,
source impurity, missed heralds or threshold clicks do not obey(4) by fiat.

## 4. Strength versus raw resource: h→1 is not a free weak-time limit

Put epsilon=1−R. From(4),

    rho=1−epsilon²/(1−2epsilon)²,
    gamma=epsilon²+O(epsilon³),
    h=1−8epsilon+O(epsilon²),
    log h(gamma)=−8sqrt(gamma)+O(gamma).                  (6)

Consequently dividing a FIXED positive edge strength Gamma into n separate
equal gates gives
`log[h(Gamma/n)^n]=−8sqrt(n*Gamma)+O(Gamma) -> −infinity`.
For this same commuting edge the full accepted map is exactly
`h(Gamma/n)^(n/2) exp(−Gamma*Pi_e/2)`, so its actual success also tends0.
This is a proved cost obstruction to THAT refinement procedure, not to
every weak measurement, gate compiler, recovery scheme or quantum trajectory.
Finite gates and noncommuting layers remain different unresolved regimes.

Fresh detection consumes both helper photons. With L data qubits and g
such gates, a spatially unrolled layout uses L+2g input photons and2L+4g
modes; a serial layout can reuse ports, but not the detected helper photons.
Thus L=2,g=1 fits4photons/8modes; L=2,g=2 already requires6TOTAL photons.
Using unmeasured helpers twice is not a product of the Kraus maps: failure
paths can return before final detection. Reuse requires a new full model.
If helpers are protected and measured only at the end, deferred EXACT PNR
conditioning does equal successive herald conditioning; that is not real-time
feed-forward or a recovery mechanism. All failed attempts still count.

Four certified injected photons cost4 per injection. For a successful ideal
gate, photons per accepted code event are at least4/h, plus preparation
failures, discarded runs, source/coupling, measurement and latency costs.
Under the ADDITIONAL model of independent uniform detector efficiency eta,
a VALID four-detected-photon event gains eta^4; no mean throughput number is
a norm/efficiency certificate. Unequal/path-dependent loss or missed flags
requires its own instrument, not a substituted scalar. These resource laws
do not silently apply to the all-record policy of section6.

## 5. Exact falsifiers: diagonal sampling and a one-edge noncommuting mixer

One diagonal cost layer on uniform |+>^L gives raw successful basis probability
`2^(−L)*(product h_e)*exp(−sum gamma_e Pi_e(x))<=2^(−L)`.
Uniform feasible proposals therefore pointwise dominate its successes when
failures hold the incumbent. Classical weighted rejection also reproduces
the normalized diagonal law. This is the existing diagonal-only veto, not
a claimed new result. Noncommuting coherent dynamics must do further work.

The natural smallest proposed extension ALSO has a direct falsifier.
After K_e on |++>, apply `M_theta=exp(−i theta X)⊗exp(−i theta X)`.
Its raw accepted basis probabilities are

    p00=p11=h/4*[cos²(2theta)+rho*sin²(2theta)],
    p01=p10=h/4*[rho*cos²(2theta)+sin²(2theta)].            (7)

Each is<=h/4<=1/4 for EVERY gamma,theta. A D control can bypass the
catalytic modules, route its same two helpers directly to their detectors,
and use disjoint single-photon Hadamards to obtain all four code states
with probability1/4. It uses no optimum. Equal source/nominal photon budget
and common valid-four-detection attenuation preserve this pointwise order.
Every improved-cost event and fixed-incumbent best-of-independent-attempts
is then dominated when other records hold. This does not order arbitrary
changing-incumbent trajectories or measured wall clocks.

Equivalently, the conditional cut probability is
`[1−((1−rho)/(1+rho))*cos(4theta)]/2`; its minimum is theta=0.
One edge plus the standard equal X mixer supplies no further conditional
mincut mechanism. This is not a no-go for other mixers, several edges,
coherent multi-round dynamics or useful recovery of the failure branches.

A separate encoding counterexample is connected: put weightM on a0-a1 and
b0-b1, weightdelta>0 on all four cross edges, with M>delta. The excluded
partition{a0,a1}|{b0,b1} costs4delta; every one-per-pair code partition costs
2M+2delta>4delta. A valid accepted-code search cannot find that optimum.
Under the uniform law on three unordered pairings, this bad pairing has
probability1/3 and must be retained. Selecting a favorable pairing after
computing the optimum is forbidden. Arbitrary failure decoding can
leave the code, so this particular support obstruction does not cover it.

## 6. Concrete all-record feed-forward continuation and six mission answers

There is a genuine changed architecture to analyze, not an assumed remedy.
Measure all four flags f=(c+,c−,dA,dB), retaining every count pattern. Let
W_e be the explicit passive sequence: two data Hadamards; declared rail
relabeling; X_B; balanced endpoint splitter; two B_R catalysts; inverse
endpoint splitter; X_B; local attenuators above; undo rail relabeling.
All unused modes carry identity. After those flags are detected, apply
M_(theta_f) to the remaining data, where theta_f=theta for f=(1,1,0,0)
and theta_f=−theta otherwise. This is a causal, fully specified branch law.
Different branches use different noncommuting settings; no static common
one-particle-unitary premise may be silently imposed on this instrument.

For each full raw occupation(f,n) of total4, set
`U_f=(M_(theta_f)⊕I_flags) W_e`. Its lossless B probability is the squared
4×4 repeated-row permanent divided by `f!*n!`; D replaces it with the
permanent of squared moduli. The input factorials are one. This formula
is valid branchwise because M_f acts after the measured flag and on disjoint
remaining modes. Sum over ALL flags/data; no herald normalization. Every
final n is decoded into its two largest vertex counts with uniform priority
ties, including vacuum, one-photon, bunched and wrong-code branches.
Score the actual full graph cut and retain best-so-far by the declared rule.
Real loss introduces additional raw records and may alter the controller;
it must be modeled before any scientific run, not repaired afterward.

1. **Graph structure?** Paired balanced vertices, sampled weighted cross
   edge and its exact cost filter; a paid residual/coarsener is necessary
   beyond four vertices. The pairing restriction is an explicit limitation.
2. **Why B?** Coherent helper/data exchange creates(2)–(4); accepted data
   can be entangled. Useful interference must survive noncommuting stages
   and all failure records; equations(6)–(7) already veto simple claims.
3. **Reoptimized D?** Independently optimize R, bypass, source mesh, edge/
   pairing law, local filters, every allowed theta_f, decoder and schedule.
   Make ALL four input photons distinguishable in the model, including
   helpers; account for internal labels and experimental overlap costs.
   D is a label-unresolved mixture, not the B pure Kraus map. Include groups
   of2/3, bypass controls and an explicit classical full-Fock mirror.
4. **Classical information?** The full graph, weights/precision, pairing,
   boundary data, decoder and feed-forward transcript are common and paid.
   Four code states can be scored directly; all six balanced subsets can
   be scored if decoding leaves the code. This is the FIRST baseline gate.
   It is a constant-block frontier, not an optimum oracle in training.
5. **Hardware?** One edge uses4photons/8modes, four intermediate flag
   measurements and data delay/conditional mixers. True helper1/1 needs
   PNR or an explicitly different resolved instrument. Threshold final
   fourfold coincidences can qualify a known-four-photon witness, but do
   not certify an intermediate herald while the data remain unmeasured.
   All source/helper/detector/delay failures and calibration are paid.
6. **Falsifier?** Reject if the paid four/six-state frontier, reoptimized D
   or the classical full-Fock mirror matches the raw improvement process.
   Reject a positive claim based only on entanglement or conditional bias.
   No outcome/label/seed selection or free best-of-portfolio is allowed.

The all-record policy escapes the success-only bound(7) as a logical matter;
whether its extra branches help is UNKNOWN. Its tiny instance has330 full
8-mode four-photon outcomes; each branch has a permanent with only24 terms.
This supplies a mandatory concrete classical mirror, not a hardness claim
or an unmeasured same-wall-time result. A four/six-state exact frontier is
still stronger for one fixed graph block once its actual cost is charged.
Keeping several interacting coherent bits with several successful/recovered
measurements is the first unresolved optimizer bridge; the current4-photon
budget cannot hide its new helpers in an input-state preparation convention.

## 7. Primary attribution and device boundary

The literature-check workflow used bounded English mechanism/title queries
and exact primary passages, checked26-Nov-2026. The local literature record
directory is absent; no Python cache helper, download or cache write was
executed locally. Retained external artifact SHA: NONE. No novelty inference follows.

S1. Lvovsky/Mlynek, [quant-ph/0202164v1](https://arxiv.org/html/quant-ph/0202164v1),
27-Feb-2002, Theory equations2–5 and introduction: conditional interference
with a single-photon helper is established catalysis. The paper also models
threshold clicks and source vacuum admixture. Its experiment is not an ideal
PNR certification. Our exact Fock algebra above is derived here, not a claim
that this source proves a graph optimizer or our entire tunable architecture.

S2. Okamoto et al., [0905.0074v1](https://arxiv.org/html/0905.0074v1),1-May-2009,
equation1/Figure2 and experimental paragraph: the two-helper parity-filter
profile is prior work; its reported verification used four threshold-detector
coincidences. That source distinguishes a true helper herald from output
postselection. Overlap: known after basis translation at the fixed parity
point; the priority of any tunable-strength parametrization is unassessed.

S3. Official [Perceval v1.3 feed-forward notebook](https://perceval.quandela.net/docs/v1.3/notebooks/Quantum_teleportation_feed_forward.html),
sectionsII–III, demonstrates simulated measured-control configurators. This
verifies a software modeling route, not native Lucy feed-forward/PNR access.
S4. Quandela's [October2025 technical whitepaper](https://www.quandela.com/wp-content/uploads/2025/10/202510-Quantum-HPC-Quandela-Whitepaper.pdf),
Road to Utility/Access and Software Stack, PDFpp7–8/12, places PNR and
feed-forward among additional modules and distinguishes their simulation.
That dated roadmap neither certifies nor disproves our account's present
capabilities. No remote discovery/login/QPU call or contact was performed.

## 8. Disposition and exact next uncertain implication

KEEP the exact catalytic gate, the phase-free h(gamma) branch and the scoped
refinement bound as mathematics pending non-author review. REJECT the claimed
optimizer rescue by a diagonal layer or one edge plus the equal X mixer.
DEFER the all-record multi-edge coherent route: its paid classical frontier,
reoptimized controls, scalable helper/photon accounting and certified hardware
bridge are unresolved. It is not exhausted by the rejected one-edge model.
The next meaningful pre-run check is an exact multi-edge/coherent cost
statistic exceeding the explicitly paid classical/D controls, not another
HOM/entanglement demonstration or favorable small-graph mean. No scientific
execution or QPU preparation is authorized by this card. P33/P37/E05b and
all prior failures remain preserved; the user objective is not achieved.
