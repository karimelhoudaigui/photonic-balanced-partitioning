# P101: finite magnetic filtering with a balanced decoder of every event

26 November 2026. **THEORY ONLY; no positive optimization signal is established.** One explicit8-mode/4-photon construction is specified. Its finite-strength point b1 is UNKNOWN against reoptimized D, but the proposed cooling explanation fails an analytic counterexample and the4-vertex optimization claim is defeated by a three-candidate classical frontier. No pilot is registered. These are scoped obstructions; other finite/intermediate-strength mechanisms remain open.

Base `b4efbe5e9944b66ef3126192889c5e9db400ce0c`, isolated `research/p94-mechanism-design-reuse`; only this card is written. All algebra below is manual and self-reviewed, not independently audited. No scientific import, AST, symbolic/numerical evaluation, RNG, test, simulation, runner, native/API/job, paper edit, push or delegation occurred. P94/P95/P96/P98 and old negatives remain frozen. Read P95, P96/P98, P70/P92/P93 scope records, P102/P103 and both Lucy compatibility documents. Standard bright-mode and Fock-lift machinery is inherited; no novelty is claimed for it or the construction.

## 1. What graph structure is encoded?

Let G have4 vertices, real symmetric weights0≤w_ij≤1, no self-loops. A partition contains TWO vertices; the physical source will contain FOUR photons. Define complement weights a_ij=1−w_ij. Fix an exogenous public vertex priority π, carried with graph relabelings. For π(i)<π(j) set θ_ij=4π/3 and θ_ji=−θ_ij. Define the PSD magnetic Laplacian by

    x†Lx=Σ_(i<j)a_ij |x_i−exp(iθ_ij)x_j|²,
    λ₀=min eig(L), Λ=max(1,max eig(L)−λ₀), H=(L−λ₀I)/Λ,
    T_b=exp(−bH/2), b≥0.                                  (1)

The concrete prospective point is b1; varying b below is analysis, not an authorized tuning sweep. λ₀ subtraction is part of the PAID compiler and defines an ideal contraction with norm1; it does not undo additional physical attenuation. Degenerate ground spaces cause no ambiguity in(1).

For every real balanced spin vector x∈{±1}⁴, with two plus spins,

    x†Lx=3Σ_(i<j)a_ij−8+2 C_G(x).                         (2)

Proof: cos θ=−1/2, so the quadratic form is3Σa−2C_complement; every balanced cut has4 possible cross edges, hence C_complement=4−C_G. This is an explicit graph-cut/spectral-relaxation bridge. It is not a many-particle cost-phase oracle: the optical input is a CF Fock state, not a superposition of these real spin test vectors. No C*, optimum mask or known partition enters(1).

## 2. Why might B help, and what exactly is decoded?

Inject `|1,1,1,1,0,0,0,0>` into a passive8-mode dilation

    E_b=sqrt(I−T_b²), U_b=[[T_b,E_b],[E_b,−T_b]].           (3)

H is Hermitian and commutes with E_b, so U_b is unitary. There are4 signal and4 vacuum/dump modes. Suppressing large single-particle Rayleigh energies could concentrate multiphoton amplitudes, and bosonic exchange changes the joint counts. Equation(2) alone supplies NO sign for the decoded cut; complex eigenvector phases may be lost upon detection.

Scientific record: the4 signal counts n and total missing count ℓ=4−|n|, with0≤|n|≤4. Retain any available native dump data separately, but the decoder and policy here do NOT use resolved dump occupations. The rank-one replacement below concerns (n,ℓ), not a sampler of the full resolved8-port joint record.

**PNR decoder D_P:** draw a fresh independent uniform permutation of the4 vertices, rank by decreasing n_i and then this tie priority, and return the first2. Every vacuum, loss, collision and all-four-click record gives a balanced partition. At n0 it is uniform among all6 subsets; there is no repeat-until-detection or CF normalization. Raw multiplicities are retained even though only their ranking enters the score.

**Threshold decoder D_T:** use h_i=1_(n_i>0). If at least2 vertices click, choose a uniform2-subset of the click set. With1 click, include it and choose1 uniformly from its complement. With0 clicks, choose a uniform2-subset of all vertices. This uses no inferred photon multiplicities. Both variants score the actual accessible cut C_G and may credit the best previously SCORED candidate; neither trains on an optimum. There is no adaptive optical training in this card.

Preparation failure is a separate recorded flag with a uniform balanced fallback, no automatic retry; its source/time/photon costs remain charged. The optical model requires a verified4-CF preparation on its success branch. Unknown input preparation is not silently treated as that state. Physical empty attempts must be recorded to use the unconditional predictions.

For B, the complete signal PGF is `per(M)`, `M=I+T_b†(diag z−I)T_b`; D gives product_i M_ii and a fixed species grouping gives the product of its principal-block permanents. This identifies the exchange terms. It does not prove that their sign improves a cut or that these groupings can all be realized on today's Lucy allocation.

## 3. What separation from reoptimized D is actually justified?

**Counterexample, fixed before any simulation:** take π=(1,2,3,4), w13=w24=1 and w12=w23=w34=w14=1/2. The graph is connected. Its three unoriented balanced cuts have costs2,3,3; the cost2 partition follows directly from scoring the three candidates, not from a training oracle. Its complement is a uniform weighted4-cycle with flux2π/3. Its L spectrum is

    {1−sqrt(3)/2, 1/2, 3/2, 1+sqrt(3)/2}; Λ=sqrt(3).

The spectrum follows by gauging the cycle to equal edge phaseπ/6 and applying its four Fourier vectors. The ground is simple with |v_i|²=1/4; the normalized gap is Δ=(sqrt(3)−1)/(2sqrt(3)).

Here P95's WHOLE-ATTEMPT quadratic stencil gives

    E_B C(D_P)−E_D C(D_P)=b²/12+O(b³),
    E_B C(D_T)−E_D C(D_T)=b²/9 +O(b³).                    (4)

Independent check: write C_ij for the cost of {i,j}, equal to its complement's cost. Under D_P the pair stencil is `(2C_ij−C_ik−C_il)/4`; under D_T it is the same numerator/3. This follows by averaging the six P95 records: base, two single losses, double loss, and two bunches. Multiply by |H_ij|²=a_ij²/Λ² and sum the four cycle edges to obtain(4). No output is discarded.

The inherited P95 remainder, K=4, ||H||op=1 and cut range1 give absolute error≤(8b)³/6. The PNR difference is at least `b²(1−1024b)/12`; the threshold difference is at least `b²(1−768b)/9`. Thus both are rigorously POSITIVE for0<b<1/1024: B is WORSE than the SAME-T D control on this example. Reoptimized D cannot rescue an asserted B advantage already absent against an allowed D member. This does not determine the b1 sign, and does not prove finite-b domination on all graphs.

Multiplicity can matter differently under the detectors. Counts `(2,1,1,0)` and `(1,2,1,0)` give probability1/2 versus0 of the cost2 cut under D_P; their threshold records coincide and D_T gives1/3 for both. A PNR-only mechanism may therefore disappear under thresholding; one cannot transfer its prediction by relabeling a click as one photon.

**Finite strong-filter obstruction.** For ANY fixed G whose H has a simple ground projector P=vv† and gap Δ>0, write t_r=exp(−bλ_r(H)/2). The canonical occupied-column isometries V_b=[T_b;E_b] and V_∞=[P;I−P] commute spectrally, giving exactly

    ||V_b−V_∞||op²=max_(r>0){t_r²+(sqrt(1−t_r²)−1)²}
      =max_(r>0){2−2sqrt(1−t_r²)}≤2 exp(−bΔ).

The inherited K-particle tensor telescoping bound and measurement contraction therefore imply

    TV(P_b^B(n,ℓ),P_∞^B(n,ℓ))≤ε_b=min(1,4sqrt(2)exp(−bΔ/2)). (5)

This derivation uses commuting spectral projectors, not an unverified generic square-root Hölder estimate. It fails to give a rank-one surrogate when the ground is degenerate, and slow gaps make it uninformative at moderate b. Common PNR/threshold decoders contract(5); a cost of range R changes by≤Rε_b. It is a bounded strong-filter statement, not a whole-finite-b no-go.

The limit signal law has an explicit classical description inherited from bright-mode/factorial-moment identities. With c_i=|v_i|², first draw N from

    E z^N=Σ_(d=0..4)d!e_d(c)(z−1)^d,

then draw the4 signal occupations as a multinomial of N with cell weights |v_j|². Loss totals, vacuum and bunches remain. Elementary coefficients and this count table take O(K²) arithmetic; loading/obtaining v, precision and draws are paid. No resolved-dump sampler or physical small-species realization is asserted.

On the counterexample |v_j|²=1/4, the limit raw signal law is permutation invariant, so BOTH decoders return a uniform balanced subset. Its mean cost is8/3, while the three-candidate classical frontier gives2. Ground-state phase information that made(2) attractive has been erased by PNR. Equation(5) quantifies approach to that classical limit even though the ideal occupied-column trace tends to1, outside the low-trace regime.

## 4. What classical information and costs must be shared?

Every control receives G, π, complement weights, L, its spectral data, the intended T/U and both decoders. Their acquisition, eigensolver, matrix exponential/root, mesh compilation/calibration, source attempts, all injected photons, all losses/rejects, switching and every decoded score/tie draw are paid. Classical spectral rounding and intensity routing receive the SAME features. A partition found classically during compilation is credited immediately to the classical arm, never counted as an optical discovery.

Mandatory controls: independently reoptimized D; all group2/3 species profiles with independently trained settings and matched total costs; spectral/diffusion and intensity-only proposals; the rank-one limit when(5) is useful; a finite4-photon classical reference with paid precision; and exhaustive feasible search. There are only3 unoriented bisections on4 vertices. After3 paid cut evaluations, exhaustive search returns their minimum deterministically, so no optical best-cost statistic can strictly beat it under a budget that permits those evaluations. This is a candidate-count obstruction, not a measured-clock theorem. Here the claimed practical optimization advantage has no remaining task beyond that frontier.

The fixed-b rule uses no fitted optimum. If a future rule learns b/phases, all training samples and classical updates are paid and D/groups optimize independently. Source/phase/tie priorities are carried under relabeling; new marks/seeds cannot be selected after results. These controls prevent both one-body graph preprocessing and known-solution preparation from masquerading as useful multiphoton optimization.

**Primary-source transfer checked26-Nov-2026:** Anand et al., [arXiv2511.16558v3](https://arxiv.org/abs/2511.16558v3),6-Nov-2026; [author PDF](https://homepages.inf.ed.ac.uk/hguo/papers/BS-simulation.pdf), Theorem1.3/Section3, printed pp3,5–7. The normalized fixed-n occupation law for entrywise nonnegative real A is classically approximable in polynomial time when n<m; collisions remain. Square A is handled by a zero-row CLASSICAL padding, with no optical mode added. VERIFIED transfer only to the all-four-survival conditional law for gauge-nonnegative T. This is not a measured runtime claim. Selected primary passages were checked; retained source SHA256:NONE. P103 was consulted; no new cache or novelty survey was created.

That theorem does NOT by itself sample this card's partial-loss branches: the environment Gram `I−T†T` can have negative off-diagonal entries even for T≥0. The all-output decoder does not replace those outcomes by an all-K failure flag. No full lossy-PNR transfer is claimed. Real positive heat/gauge-positive filters are mandatory known-law nulls; complex phase alone does not establish hardness.

For the explicit counterexample use indices j,r=0,1,2,3 and the EXACT Fourier convention `F_jr=exp(−iπjr/2)/2`. Let `D_jj=exp[i j(π/6−4π/3)]`; then `D†L D` has phaseπ/6 on each forward cycle edge, and

    D†T_b D = F diag(1,x,xy,y) F†,
    x=exp[−b(sqrt(3)−1)/(4sqrt(3))],
    y=exp[−b(sqrt(3)+1)/(4sqrt(3))].                     (6)

Gauge phases do not change the CF-input PNR law or either decoder. A forward neighboring entry in(6) is `[(1−xy)+i(x−y)]/4`. For finite b>0,0<y<x<1 and `(1−xy)−(x−y)=(1−x)(1+y)>0`; its argument is strictly between0 andπ/4. The oriented four-cycle product is therefore nonreal. Positive diagonal entries force any input/output phases making T entrywise nonnegative to reduce to diagonal conjugation, contradicting that invariant. Thus this finite counterexample is genuinely outside the positive-matrix null, yet still fails the optimization rationale. The limit becomes gauge-positive; the full lossy signal sampler there was proved separately above.

## 5. What hardware and loss regime are actually needed?

The circuit model requires8 passive modes,4 distinct single-photon inputs,4 vacuum inputs and final detection only; no within-shot feed-forward, Kerr gate, squeezing or arbitrary nonvacuum ancilla is assumed. Arbitrary U8 synthesis and the requested input/detector/mode capabilities are NOT established for Lucy by this card. Existing [Lucy/TGCC](../docs/LUCY_TGCC.md) and [compatibility](../docs/QPU_COMPATIBILITY.md) explicitly leave actual PNR, routing, filtering and physical-attempt denominators unverified. A modeled Perceval feature is not hardware support. No account or specs query was made.

For ideal(1) with all4 input columns, `µ_b=Tr(T_b†T_b)=Tr exp(−bH)>1` at finite b, so the P96 µ≤1/2 guarantee and P98 µ<1/2 geometric regime do not apply. This is a mathematical property of the ideal filter, not a device certificate. Any physical trial claiming to escape them must supply an ACTUAL certified lower bound on its occupied-column trace above1/2 and a model-error budget; nominal normalization and public mean efficiency do not supply that. If actual columns put µ≤1/2, use the P96/P98 classical controls. Being outside their useful regime remains insufficient for advantage, as(5) and the3-cut frontier show.

If only threshold detection is established, use D_T and its own prediction(4); do not infer N or ℓ from click number. Preserve all native ports/flags available, including dump data; their use for adaptive decisions would require a new model beyond the marginal replacement in(5). If the API reports only nonempty/filtered shots, physical empty attempts cannot be reconstructed from these counts. Without authenticated preparation/emission counts and filtering information, raw useful yield and per-injected-photon advantage remain undefined. Hardware acquisition is blocked until those facts AND the scientific gates are satisfied.

## 6. Specific falsifiers, decision and the next bounded question

Falsifiers are explicit: disagreement with the signed stencil(4) within its remainder budget; failure of the simple-ground continuity prediction(5) after declared model/detector errors; loss of a proposed effect under D_T; reproduction by reoptimized D/groups or a paid classical feature/frontier; or apparent gain disappearing when all attempted preparations/empty events are counted. A changed physical model is audited as such, not accepted as a breakthrough from a failed ideal prediction.

**Decision:** REJECT this4-vertex construction as an optimization-advantage pilot; KEEP the graph-energy bridge, detector distinction and scoped endpoint/continuity counterarguments for independent proof review. b1's same-family B/D sign is UNKNOWN; no promising probability, held-out benefit or novelty is invented. The weak negative interval, simple-ground limit and3-query obstruction do not refute every larger graph/decoder or all finite magnetic filters. No numerical run, hardware bundle or manuscript update follows from this card.

If another analytical step is useful, the concrete next question is the FULL finite-b sign on this fixed connected example: derive the rational bivariate mean-difference polynomial in x,y from the four-photon PGF, restricted to the physical curve `y=x^(2+sqrt(3))`. A nonnegative polynomial on the larger triangle0≤y≤x≤1 would suffice; a negative point OFF that curve would not refute the finite-b claim. A negative mean difference on the curve would justify only a physical-mechanism follow-up, while the3-cut classical optimization obstruction remains. This is a bounded symbolic question, not another optimizer sweep or a promise of success.
