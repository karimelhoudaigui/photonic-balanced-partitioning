# P95: what dissipative photonic filtering contributes at small strength

26 November 2026. **Static mathematical result, self-review only.** The B−D first derivative vanishes; its quadratic coefficient is a sum of explicit two-source exchange stencils, including all losses. A convex mixture of group2 experiments at the SAME channel need not reproduce that sum. Cubic magnetic flux can enter a pair-propagation term as well as a genuine three-source exchange cycle. No favorable graph-optimization sign or total-resource advantage is proved.

## 1. Model, observation and evidence contract

Base `b2b15069acbfd4257996f78fd0609258142df41d`, branch `research/p94-mechanism-design-reuse`; only this new file is written. P94 is frozen. No code/import/AST, test, RNG, matrix or probability execution, native call, graph generation, QPU, manuscript, delegation or push occurred. All derivations and examples are by hand. `research-program` and `proof-audit` workflows apply; no independent review is claimed.

Let L be an m×m Hermitian positive-semidefinite matrix, β≥0, and `T_β=exp(−βL/2)`. The channel is passive with vacuum environments. The known input has one photon in each of K DISTINCT modes A, K≤m. B photons are identical; D photons have mutually orthogonal product internal labels and experience the SAME spatial channel. A grouped control partitions these labels into mutually distinguishable species, identical within a species. No ancillary nonvacuum state, herald renormalization, gain or dark-count replacement is included.

The observed record is `(n,ℓ)`, where n is the COMPLETE signal PNR vector and `ℓ=K−Σ_a n_a` is the total number lost. Vacuum and every collision/loss record remain. This does **not** specify which environmental mode or time recorded a loss. Resolved dump/time records require an explicit physical dilation/unravelling; T alone does not determine them. Here “all losses” means no discarded attempts, with their total recorded.

Fix any bounded real f(n,ℓ), independent of β, used identically for B/D/groups. It may be a graph-cut cost after a fixed balanced decoder, or the indicator of improving a known paid incumbent; it may not use C*, an optimal mask or a known optimal partition. A common randomized decoder is covered by averaging f over its independent coins. Evaluating that average or a capped quench is not a free oracle. Bounds below use `R_f=sup f−inf f`.

Local attribution: read P62's124-line `research/P94_BOUNDED_PARITY_ORACLE_PRIOR_ART.md` at `e3b1e6e2a0eeb41727559d5931c93b8a4924cbf1`, SHA256 `bf52c6cb6b84bbc2f08cddba818aca48ef0cda840b7c509519cdf95c0dbd0367`. Its authenticated Seron–Novo–Arkhipov–Cerf2212.09643v2 and Aaronson–Hance1212.0025v2 extraction establishes prior counting-characteristic/permanent and additive-estimator ingredients. This note uses an internal expansion, not a novelty claim for those identities or the filter architecture; no fresh external source verification was performed.

## 2. Exact raw generating functions and the vanishing first derivative

Use commuting formal variables z_a for signal counts and v for lost number. Let Z=diag(z_a), restrict matrix rows/columns to A, and put

    M(β)=T_β[Z−vI]T_β+vI,
    G_B(z,v;β)=per(M(β)[A,A]),
    G_D(z,v;β)=product_(i∈A) M_ii(β).                 (1)

To derive (1), dilate the occupied input columns as `[T_β[:,A];E_A]`, with `E_A†E_A=I_A−(T_β²)[A,A]`. The signal/loss counting operator has one-particle action diag(Z,vI_environment). Its CF Fock matrix element is the permanent of the compressed matrix; independent labels instead factor its diagonal entries. A specified species grouping gives the product of the corresponding principal-block permanents. No complete-count probability is conditioned on survival.

Write `z_B=product_(i∈B)z_i`, with `z_empty=1`. At β0 the restricted M is diagonal with entries z_i. Define

    h_ij=v−(z_i+z_j)/2,
    a_ij=L_ij h_ij,
    g_ij,a=(z_i+z_j+2z_a−4v)/8,
    b_ij=Σ_(a=1..m) L_ia L_aj g_ij,a.

Expanding both matrix exponentials gives `M_ij=δ_ij z_i+β a_ij+β² b_ij+O(β³)`. In particular `a_ii=L_ii(v−z_i)`. Every nonidentity permutation moves at least two indices, so

    G_B−G_D=O(β²),
    d/dβ E_B f|_0=d/dβ E_D f|_0
      =Σ_(i∈A)L_ii[f(n⁰−e_i,1)−f(n⁰,0)],          (2)

where `n⁰=1_A`. Thus the first-order PNR law contains only one-loss events and their normalization decrement; the corresponding coefficients use only L_ii. Individual environmental channels need not obey the last “diagonal only” statement before summing them.

## 3. Quadratic exchange stencil, with no omitted loss branch

Only a transposition contributes to the B−D coefficient at order2:

    P₂(z,v)=Σ_(i<j∈A)|L_ij|² h_ij² z_(A\{i,j}).

Consequently `E_B f−E_D f=β² Σ_(i<j∈A)|L_ij|² H_ij[f]+O(β³)`, where

    H_ij[f]= f(n⁰−e_i−e_j,2)
             −f(n⁰−e_i,1)−f(n⁰−e_j,1)
             +f(n⁰+e_i−e_j,0)/4
             +f(n⁰+e_j−e_i,0)/4+f(n⁰,0)/2.        (3)

Each stencil sums to zero. Its positive mass is2 and negative mass2. Different pairs have disjoint two-loss and directed-bunch states; their only other shared states are the unchanged positive atom and one-loss negative atoms. Therefore the RAW-law TV separation has leading coefficient

    TV(P_B,P_D)=2β² Σ_(i<j∈A)|L_ij|²+O(β³).

This is a local distinguishability statement, not useful optimization or measured cost. There is no fixed favorable sign: f=1_{ℓ=2} gives H_ij=1, while f=1−1_{ℓ=2} gives H_ij=−1. Both are bounded nonnegative statistics. A graph/decoder-specific sign must be derived rather than inferred from bosonic bunching.

Holding the diagonal and off-diagonal magnitudes of L fixed, (3) is magnetic-phase blind. It is a two-source exchange contribution, including correlated double loss and one-loss deficits; describing it solely as a collision-only HOM probability would omit essential branches.

**Group2 mixture counterexample.** At the SAME L,β, a fixed grouping retains the quadratic term for pair ij only when i,j share a species. With groups≤2 these pairs form a matching. A convex mixture of groupings gives coefficients p_ij with `Σ_(j≠i)p_ij≤1`; it cannot in general set every p_ij to1.

Take K=m=3, A all modes, and the ordinary triangle Laplacian `L=3I−J`, which is PSD with diagonal2 and off-diagonal−1. For f=1_{ℓ=2}, full B−D is `3β²+O(β³)`. Every grouping≤2 contains at most one pair, so any β-independent convex mixture at this channel has coefficient≤1 instead of3. β-dependent mixtures still cannot exceed1 at leading order. This disproves the unqualified convex-mixture claim, not the existence of a classical replacement, independent reoptimization, or a different time/resource comparison. A signed sum of pair effects is not a normalized sampler.

## 4. Exact cubic coefficient and what magnetic flux means

Define `[P]_f` by replacing each monomial `z^n v^ℓ` in a homogeneous degree-K polynomial P with f(n,ℓ), preserving its coefficient. This is a finite signed linear functional, not a sampling procedure. The complete cubic coefficient of G_B−G_D is

    P₃=Σ_(i<j∈A) 2 h_ij Re(L_ji b_ij) z_(A\{i,j})
       +Σ_(i<j∈A)|L_ij|² h_ij²
          Σ_(k∈A\{i,j}) L_kk(v−z_k) z_(A\{i,j,k})
       +Σ_(i<j<k∈A)2 Re(L_ij L_jk L_ki)
          h_ij h_jk h_ki z_(A\{i,j,k}).             (4)

The Re operation conjugates matrix coefficients, not the real formal variables. The three lines arise respectively from β×β² corrections to a transposition, one first-order diagonal spectator on that transposition, and the two orientations of a three-cycle. No diagonal-only permanent term survives subtraction of G_D. Thus the exact Taylor statement is

    E_B f−E_D f=β²[P₂]_f+β³[P₃]_f+remainder.        (5)

The last line of (4) is genuine THREE-source exchange. It requires those three source indices to share a species; a group3 control is necessary when testing a proposed benefit from this term. It does not follow that one convex mixture of group3 experiments reproduces ALL overlapping pair/triple coefficients simultaneously.

But the FIRST line also contains gauge-invariant `Re(L_ji L_ia L_aj)`. A third mode a can be EMPTY initially. Therefore a flux-dependent cubic correction can already occur with TWO occupied photons through a two-step one-particle propagation path. That effect remains inside a two-photon-group experiment; magnetic flux by itself does not certify a third-photon contribution. On a magnetic Laplacian the triangle product is a signed product of weights times cos(cycle flux), so reversing the flux does not produce an odd-in-flux gain here.

If the off-diagonal support of L is triangle-free, these cubic loop factors reduce to diagonal/magnitude terms and no nontrivial cycle flux appears through order3. This does not exclude longer-loop effects at higher order or finite β. It assumes fixed matrix magnitudes; changing a compiler's magnitudes/diagonals with its phase settings introduces a separate classical feature.

## 5. A hard remainder for arbitrary bounded raw decoders

Let `λ=||L||op`. The channel family is a pure-loss semigroup: composing two vacuum attenuations multiplies their T matrices and leaves a vacuum environment, so their β parameters add. In the eigenmode basis an infinitesimal step has no-loss Kraus operator `I−dβ R_op/2+O(dβ²)` and one-loss Kraus operators `sqrt(dβ)J_α+O(dβ^(3/2))`, with `J_α=sqrt(λ_α)c_α`; two-loss probability is O(dβ²). This derives the following generator on the finite space with at most K photons:

    R_op=Σ_α J_α†J_α=dΓ(L)≤Kλ I,
    ℒ(X)=Σ_α J_α X J_α†−{R_op,X}/2,
    ||ℒ(X)||_1≤2Kλ ||X||_1  for Hermitian X.

For the jump part, apply its positive map to the Jordan positive/negative parts of X and use R_op≤KλI. The anticommutator contributes at most Kλ||X||_1 by the operator/trace-norm product inequality. The semigroup is CPTP and contracts the trace norm of Hermitian operators. The same bound holds with independent internal labels or species, since the one-particle loss matrix is L⊗I_internal.

The integral Taylor remainder after degree p applied to a normalized state is at most `(2Kλβ)^(p+1)/(p+1)!` in trace norm; no exponential prefactor is needed because the remaining semigroup is contractive. Center f at the midpoint of its range and add the B and D bounds. In particular

    |ΔE f−β²[P₂]_f|≤R_f(2Kλβ)^3/6,
    |ΔE f−β²[P₂]_f−β³[P₃]_f|≤R_f(2Kλβ)^4/24.       (6)

These bounds are conservative, valid for β≥0, and concern signal PNR plus TOTAL lost count. They are not a relative-error claim about a rare subevent or a certificate for a particular hardware loss/dilation. β0, L0 and K0 are immediate zero-difference endpoints; K1 has no permutation cycle and B=D exactly at every β.

## 6. Research decision and the missing optimization implication

For a fixed balanced graph decoder, (3) is an optimum-blind, falsifiable prediction of the leading B−D mean or known-incumbent improvement hazard. However, evaluating it exposes at most `1+K+3 binom(K,2)` distinct raw records: the unchanged record, K single losses, pair double losses and directed bunches. Every associated feasible decoded partition can be placed in a classical paid frontier; decoded duplicates may be removed with their actual costs recorded.

The cubic polynomial similarly exposes only O(K²m+K³) raw-record terms before deduplication. Coefficients and every actual decoder/score/quench invocation must be charged; an averaged stochastic decoder is not one free scored candidate. Classical evaluation of a favorable mean coefficient is not itself a discovered partition, but the materialized deterministic frontier candidates are. Applying a quench to only the minimum raw-cost candidate does not establish dominance over all quenched endpoints.

**Sharper discriminator for the collision/loss-self-loop policy.** Suppose all collisions/losses return the known incumbent, and a complete CF record n⁰ returns that same incumbent. Then f equals f₀=f(n⁰,0) on those records. Equation(3) vanishes. In (4), every genuine three-occupied-source cycle and every spectator term also evaluates to zero after centering f. Only a pair-propagation term through an initially empty mode a can change the result. With `δf_(i→a)=f(n⁰−e_i+e_a,0)−f₀`,

    ΔE f=−β³/4 Σ_(i<j∈A, a∉A) Re(L_ji L_ia L_aj)
                    [δf_(i→a)+δf_(j→a)]+O(β⁴).     (7)

Thus this cubic magnetic effect explores only the paid physical-one-replacement CF frontier. In direct vertex-occupation graph encoding (m=2K), these are graph ONE-SWAPS; an arbitrary decoder can instead map them to larger graph moves. With strictly improving acceptance and no improving decoded member of this frontier, all these δf vanish for accepted cost or improvement indicator, so B−D has no improvement signal through order3. This statement excludes a quench that can turn a nonimproving one-swap into a better basin: such a quench changes δf and must be evaluated and paid.

More generally a complete CF target `A'=(A\R)∪Y`, with R⊂A, Y⊂Aᶜ and |R|=|Y|=r, has leading raw probabilities

    P_B(A')=β^(2r)/4^r |per(L[Y,R])|²+O(β^(2r+1)),
    P_D(A')=β^(2r)/4^r per(|L[Y,R]|²)+O(β^(2r+1)).   (8)

Proof: each of the r new output rows requires an off-diagonal T entry, so every amplitude routing has at least r powers of β. At exactly r powers, every shared output must be its own diagonal input; the remaining r sources/rows give the displayed permanent, with `T_ai=−βL_ai/2+O(β²)`. CF input/output factorials are1. Squaring gives (8); independently labeled routes add without cross terms. If that permanent vanishes the leading coefficient is simply zero, not a claimed success. No survival-conditioned denominator is introduced.

In direct vertex-occupation encoding, from a strict one-swap local minimum without basin-changing quench, the first possible accepted improvement therefore has order at leastβ⁴, from two-replacement targets; this is still a two-source exchange channel, not irreducible large-photon interference. Fixed-r physical CF frontiers have `binom(K,r)binom(m−K,r)` candidates and are mandatory whenever their actual work fits. Extending r or finite β is an open, separately costed question rather than an implication of the small-strength expansion.

Therefore a positive quadratic sign, or even a cubic flux coefficient, is **not sufficient justification for a new optimization pilot**. A candidate mechanism must beat this paid frontier and independently reoptimized D/groups/strong feasible search, or derive a nonperturbative collective advantage outside these finite-order predictions. No equal-wall-time domination follows when the full frontier does not fit the actual allowance. No theorem here rejects all finite-β filters.

**Disposition:** KEEP (1)–(8), the group2-mixture counterexample and the two-source flux caveat for independent reconstruction. REJECT “zero first derivative means no interference,” “all quadratic effects are one convex group2 mixture,” and “flux implies genuine large-photon optimization.” The filter route stays OPEN at the finite-strength, total-cost search step; a concrete favorable graph-to-filter/decoder relation has not been found. P33/P37/E05b and all negative results remain preserved. No paper or hardware gate opens.
