# P94: three changed mechanisms, with their strongest countercontrols

26 November 2026. **No positive optimization result is established.** This is a static portfolio and a hand-derived obstruction for one candidate class, not another parameter sweep. The most concrete new route below changes the decoder and objective, but its proposed expressivity advantage fails a two-photon-group counterconstruction. Its possible computational search advantage remains open.

## Contract and provenance

Owner: P94 mechanism-design child; isolated base `eca20b5031089786a35ba31a7c9ddc1a2238a34d`, branch `research/p94-mechanism-design-reuse`. ROOT metadata was read at `027653e2c36030549df2c7536404e6c611da12f2`. Only this file is written. No import, AST, test, RNG, graph/matrix/probability execution, native call, model download, QPU call or manuscript edit occurred. No new raw B file was opened.

The supervisor supplied a **provisional, independently unaudited** P90a main summary: B111/28 versus each FAST104/27, 96 attempts,1152 modeled photons,29478 scored candidates; both B best discoveries are classical `compiler_M`. This rejects no larger class. ROOT's read STATUS/CLAIMS still describe the earlier pre-main checkpoint; these historical records were not edited here. P33/P37/E05b and all negatives are preserved.

Read inputs: AGENTS; CLAIMS/STATUS/NEGATIVE_RESULTS; P44/P62/P69/P81/P84/P91/P93 source statements; P82/P90 design and P90 bounded primary-literature record; recorded scopes P70–P80/P83/P85–P87/P89. The `research-program` skill governs route selection; `proof-audit` was applied as **self-review**, not an independent audit. No novelty is certified. Passive Fock cost training and parity decoding already have authenticated prior overlap with Brádler–Wallner, arXiv2112.09766v1, recorded in `research/P90_BOUNDED_PRIMARY_LITERATURE_CHECK.md`; only that local authenticated extraction was used, not a fresh full-paper verification.

Acceptance still requires optimum-blind learning, independently reoptimized D and groups≤3, strong feasible classical search, shared paid features, full costs, fresh seeds/relabeling, unopened held-outs and independent replication. A fixed-circuit B/D contrast, one permanent zero, or preparation of a classically found partition cannot satisfy that contract.

## A. Balanced Walsh-code decoding: an actual different objective

**Mechanism.** Use K≤12 distinct occupied inputs, m≤24 output modes and a passive U; record every count, including collisions. Pair the graph's N=2L vertices as `(j,+),(j,−)`. Fix public binary masks `q_j in F_2^m`, without an optimal partition. Pairing/masks are graph-blind marks or explicitly paid shared graph features. Define

    p_a=n_a mod2,  χ_q(p)=(-1)^(q·p),
    s_(j,+)=χ_(q_j)(p),  s_(j,−)=−χ_(q_j)(p).

Every record produces exactly L positive spins, even with missing photons or vacuum. Balance is classical decoding, not physical occupation of all graph vertices. This is neither top-K nor P90's uniform collision fill. A large graph can be represented, but only inside the disclosed paired/code family; classical controls may search outside it. Vacuum returns a fixed classical partition that must also be credited to every control.

For an edge `e={(j,σ),(l,τ)}`, with σ,τ=±1,

    C_e(p)=w_e[1−στ χ_(q_j xor q_l)(p)]/2.

Thus the EXACT decoded cut is a Walsh polynomial `C_G(p)=Σ_r b_r χ_r(p)`, obtained by aggregating all edges, including within-pair edges. There is no C*, optimal-state mask or selected target in this identity. Changing the masks after seeing scores is training and must be paid, recorded and exposed to controls.

**Exact quantum channel, including losses.** Let T be the accessible passive-vacuum transmission, A the K occupied distinct inputs, and Q_r the diagonal projector onto the output modes selected by mask r. Then

    F_B(r)=E[χ_r(p)]=per(I_K−2 T_A† Q_r T_A),
    F_D(r)=product_(i in A) [1−2(T_A† Q_r T_A)_ii].       (A1)

Proof by hand: dilate T_A to orthonormal columns `V=[T_A;E_A]`, so `V†V=I_K`. The parity operator is the passive lift of `Z=diag(I−2Q_r,I_environment)`. The diagonal CF Fock matrix element of its lift is `per(V†ZV)` by expanding the K creation operators and their K! contractions. Each input occupation is one; there is no extra K! denominator. This gives (A1). Independently labeled particles factor into the diagonal entries. A specified partition of inputs into indistinguishable species gives the product of the corresponding principal-block permanents. This is not a formula for arbitrary internally entangled sources.

Consequently `E C_G=Σ_r b_r F_B(r)` is a deterministic small-permanent objective. With d distinct nonzero graph characters, a direct subset expansion costs `O(d[mK²+K2^K])` arithmetic operations, plus graph/mask/mesh setup; finite-bit error and derivatives need separate treatment. At K12, `2^K=4096`. This is a required classical mean/gradient or objective-search competitor, not proof that its runtime beats a QPU. It does not itself return the best sampled cut or solve the nonconvex circuit-training problem.

**Stronger additive-mean control, supplied by the supervisor and verified by hand.** Write `A_r=I_K−2T_A†Q_rT_A`. Since `0≤T_A†Q_rT_A≤I_K`, A_r is a Hermitian contraction. For independent Rademacher signs x_j=±1 and K≥1 define

    Z_r(x)=(product_j x_j) product_i (A_r x)_i.

Expanding the K factors, a monomial survives sign averaging only when each index occurs an odd number of times. There are exactly K occurrences on K indices, so each occurs once. Hence `E Z_r=per(A_r)`. Also

    |Z_r|≤(||A_r x||²/K)^(K/2)≤(||x||²/K)^(K/2)=1.

Thus `Re Z_r` is a signed bounded estimator of F_B(r), with `Pr(|sample_mean−F_B|>ε)≤2exp(−nε²/2)`. Each sample costs `O(K²)` arithmetic plus K random bits, after PAID construction of A_r. Estimating d characters simultaneously to additive ε with failure≤δ costs `O(dK² ε^(-2) log(2d/δ))` arithmetic plus setup. The same sign vector may serve all characters: correlation between them does not invalidate a union bound. Finite precision and arithmetic/random-bit costs remain explicit obligations. No priority claim for this identity/estimator is made.

Alternatively estimate `b_0+Σ_(r≠0)b_r Re Z_r(x)` directly. Its centered absolute range is at most `B=Σ_(r≠0)|b_r|`; Hoeffding gives additive-error cost proportional to `B²/ε_absolute²`. For nonnegative weights, `B≤Σ_e w_e/2` by the edge expansion. Consequently bounded relative-to-total-weight mean accuracy needs no exponential-in-K permanent calculation in this arithmetic model. Fresh estimator bits or justified adaptive concentration are needed during training; reusing one fitted random table is not automatically valid.

This is **not a sampler of feasible partitions**, a positive-probability model, a relative-error rare-event estimator, or a best-of-run/quantile guarantee. Signed estimates cannot be credited as discovered cut candidates. No measured wall-time ordering or classical optimizer convergence follows. It nevertheless removes mean-only “hard permanent” rhetoric from this decoder family even beyond K12.

**A tempting witness, and its falsification.** Take K=m=4, all four inputs occupied, and a real Hadamard/2 mesh. Observe one output parity. Its compressed reflection is `I_4−J_4/2`, so

    F_B=Σ_(j=0..4) binom(4,j) j!(-1/2)^j=1/2.

At that SAME row, species partitions2+2,3+1,2+1+1 and1+1+1+1 give respectively1/4,1/8,1/8 and1/16. Even independently reoptimized D on four fully occupied modes has `F_D≤1/16`: the row probabilities q_i sum to1; if any q_i>1/2 the product is nonpositive, otherwise AM–GM on `1−2q_i` gives the bound. This statement does not cover extra vacuum modes or changed source resources.

Nevertheless a reoptimized HOM pair with row probabilities `(1/2,1/2,0,0)` makes that output occupation always even. Its two-photon group gives F=1 and beats the witness. A one-character objective is therefore **REJECTED as an advantage witness**, despite beating reoptimized D in the restricted four-mode comparison. The full-B family can use the same HOM construction; larger coherent groups are unnecessary here.

**Stronger hand-derived obstruction: parity support needs at most two-photon groups.**

Claim A2. In the ideal lossless m≥K passive model with known CF input, every parity vector with `|p|≤K` and `|p|≡K mod2` is produced deterministically by a circuit with interfering groups of size at most two. Therefore every full-B parity law belongs to the convex hull of such deterministic group≤2 parity laws.

Proof: route |p| photons individually to precisely the odd-designated output modes. The remaining `K−|p|` photons come in pairs. Give each pair a disjoint balanced two-mode HOM block, using output modes outside the designated odd set. Each block outputs `(2,0)` or `(0,2)`, both with even parity. Exactly K output modes suffice. A source/output permutation and disjoint splitters implement this from the fixed CF input. Conversely any K-photon count vector has exactly the two displayed parity constraints. Mixing these deterministic constructions with weights equal to a desired parity law proves the convex-hull statement.

The input pairs/species and circuit may be reoptimized independently of the original B mesh. The statement is not restricted to a shared intensity profile. It assumes independently permitted input grouping and ideal HOM; a restricted fixed-species device requires its own control specification.

**What A2 does not prove:** computing the mixture weights can be as hard as computing/sampling B; no efficient universal replacement or same-cost optimizer dominance follows. Fixed hardware loss can destroy deterministic parity preparation, so A2 is not automatically a theorem about a prescribed lossy T. The result rejects a parity-*expressivity* explanation and a small witness, not every computational benefit of parity-based search.

**Exact latent countercontrol.** For lossless even K, p lies in the even-parity hyperplane. Rewrite all graph characters on m−1 independent bits, aggregate their coefficients and perform a Walsh transform. This obtains ALL code cut costs in `O(|E|m+(m−1)2^(m−1))` arithmetic work and `O(2^(m−1))` storage. Restrict to `|p|≤K` if demanding the same photon parity support. With loss, use all m bits or restrict to reachable weights; allowing the full code is also a legitimate stronger classical feasible control.

For m24, the lossless table has `2^23=8388608` entries; one8-byte table is64MiB. This memory count is arithmetic, not a benchmark or a finite-bit guarantee. At integer-weight input an exact rational/integer transform is possible with paid bit sizes. For fixed m this is a finite classical search independent of the number of graph vertices after aggregation. No scalable advantage in N follows merely from the large graph label count.

The resulting minimum pathwise dominates RAW code candidates if fully enumerated and paid. It does **not** automatically dominate the endpoints of applying a nonlinear quench to every candidate: those additional descents must all be paid, or their stronger claim withheld. A timed classical sampler for the same passive law is another compulsory finite-K control.

**Disposition A:** KEEP the explicit loss-parity identity, bounded additive-mean control and A2 for independent mathematical audit. REJECT parity support/one-character separation and hard-mean rhetoric as mechanisms of advantage. Multi-character best-candidate search dynamics remain OPEN, but no new optimization pilot is justified solely by this construction. The masks/decoder and estimator are not certified novel.

## B. Coarse-grained collective moves on graphs larger than the device

**Mechanism.** Build a paid hierarchy or balanced pairs of vertex blocks using graph features, then let optical outcomes select correlated whole-block flips. With12 logical binary decisions, a single proposal can move many vertices and escape a one-swap basin. This changes the search space, rather than the P90 split angle or its normalization. Every encoded decision must preserve block cardinality, or use a disclosed paid repair.

**Decisive countercontrol.** If the decoder depends on only12 binary choices, there are at most `2^12=4096` candidates. Contract graph edges to an explicit quadratic block objective; exhaustive enumeration or branch-and-bound uses exactly the same features. If it instead selects12 of24 supervertices, enumerate `binom(24,12)=2704156` oriented choices, or1352078 complementary cut classes when the decoder has that symmetry. The larger underlying graph does not enlarge this latent domain.

All setup, block discovery, contractions, candidate decoding, scores and descents are paid. Pure repeated scoring of the original graph is an unnecessarily weak classical baseline when edge contraction is available. Multiple refreshed hierarchies, learned embeddings or histories change the domain and must be given equally to adaptive classical controls; a theorem for one frozen code does not cover them for free.

Falsifiable prediction: a putative photonic gain caused only by discovering a favorable block union disappears once the same paid latent frontier is exhausted. Before nonlinear descent, this is an exact pathwise statement, not a population conjecture. Whether exhaustion fits the measured budget is a separate timed question.

**Disposition B:** REJECT graph-size amplification alone as the proposed innovation. It relocates a low-dimensional classical problem and can manufacture an apparent gain against deliberately local baselines. A nontrivial remaining proposal would need an explicit expensive growing latent search that the physical count law solves more cheaply, not a known favorable block prepared optically. No such implication is supplied here.

## C. Frustrated dissipative filtering rather than unitary graph evolution

**Mechanism.** Use a graph-dependent passive contraction, not another `exp(-iH)` mesh. For graph edges choose publicly specified antisymmetric phases `φ_uv=−φ_vu` and define a positive magnetic Laplacian by

    x†L_φ x=Σ_({u,v}) w_uv |x_u−exp(iφ_uv)x_v|²,
    T_β=exp(−β L_φ/2),  β≥0,  w_uv≥0.

Cycle flux nonzero modulo2π cannot be removed by vertex-diagonal gauge conjugation of L_φ; at β0 the channel is nevertheless identity. The hypothesis is that competing coherent path families followed by dissipation could create useful collective proposal correlations beyond one-body routing. There is **no proved favorable relation between this filter and balanced minimum cuts**. A spectral partition, classical diffusion, identical-feature perturb-and-optimize search, D with independent β/phases, small groups and exact passive simulation are required controls. Saying “imaginary-time cooling” does not supply that missing relation.

A finite contraction is physically implementable in principle: diagonalize its singular values, couple each attenuated bright mode to a vacuum dump splitter, and undo the singular-vector bases. Full dilation, mesh synthesis and all dumps must be accounted for. A general24-signal-mode contraction can require24 additional vacuum modes; it is not automatically a24-mode Lucy circuit. Reserving dumps inside24 modes reduces signal modes or the independently attenuated rank. No availability of tunable loss, dump detectors or calibration is established here.

Classical decoding must be fixed for EVERY raw signal/loss record. A failed filter cannot be renormalized away or rerun without cost. A success-flag branch receives P74's applicable resource screen; a click-contained branch receives P44's applicable cap. If a certified occupied-input norm `||T_A||²≤η<1` applies, P91's normalized low-survivor replacement still bounds any common decoded statistic, so a nonlinear decoder cannot amplify its absolute-TV error into a free signal.

For the displayed unshifted filter, `||T_β||²=exp(−β λ_min(L_φ))`; its normalized contrast depends on the spectral gaps. Subtracting λ_min I would define a DIFFERENT physically allowed contraction with norm1. Thus spectral suppression is not an unavoidable theorem about every realization of this idea: the shifted compiler must be specified and separately charged. A public mean transmission is not a certificate of either norm.

The first useful discriminator is mathematical: find a concrete graph-blind decoder and graph-to-filter rule for which an unconditional many-photon improvement statistic has a sign or structural prediction that is NOT already a paid spectral/diffusion feature. A derivative depending only on a fixed-small-photon marginal fails that discriminator. Complex phases alone, or loss-conditioned dense-subgraph enrichment, do not pass it. No such witness is presently derived here.

**Disposition C:** DEFER, not exhausted. This genuinely changes the physical channel, but currently lacks the optimization implication and a24-mode resource-respecting specification. It is not ready for a DEV run, a hardware freeze or a novelty claim. A bare graph heat kernel with no decoder/cost prediction is not a complete algorithm.

## Obstruction map and concrete continuation

P44 assumes click-contained decoding and a certified spectral loss cap; A escapes click containment through classical coding, not through free physical feasibility. P62's fixed outside-law/top-K hypothesis is absent, but its paid-frontier lesson remains. P69–P72 bound specific transport events/ranks, not arbitrary coded output costs. P73–P80's nonnegative Gaussian-source samplers do not automatically sample a Fock source. P81/P84/P86/P87 obstruct all-basis dual-rail preservation/cost phases; none of these routes assumes such an oracle. P83's nongauge phase witness is not hardness or optimizer advantage. P89/P90 source-coupling observations and P93's rank-two initializer surrogate are preserved; no residual-size assumption is made here.

**Next concrete question Q94:** Is Claim A2 correct with the stated CF source, independently chosen species grouping, full parity support and m≥K, and do its lossless Walsh-frontier consequence and the additive-mean control survive exact source-level audit? An independent hand reconstruction is warranted before promoting them. The proof obligations are the HOM parity output, the K-mode resource count, the convex-hull-versus-efficient-mixture distinction, the even-parity coordinate reduction, the sign-averaging/AM–GM argument and the mean-versus-best-candidate/quench scope. This is a bounded obstruction audit, not a new optimizer experiment.

After that audit, A's unresolved continuation is a fully costed *search-dynamics* mechanism that beats exact Walsh/permanent controls; C's is an explicit decoder/filter with a nontrivial unconditional optimization prediction and a mode/loss budget. B's frozen-latent construction is closed as an expressivity escape, while adaptively changing code families remain outside that closure. No route is silently declared globally impossible. None currently earns another positive DEV claim.

Self-review verdict: **A1/A2, the bounded additive-mean control and the finite latent bounds are proved as written by hand, pending independent review; the optimization advantage remains incomplete.** Boundary checks: K0 vacuum gives permanent(empty)=1 and only p0, so bypass the estimator's K denominator; K1 has no pair; odd K uses the odd parity hyperplane; m=K still has enough HOM output modes; extra loss changes the support/preparation theorem and is treated only by A1 and its estimator. The four-photon same-mesh witness is explicitly falsified by a reoptimized group2 circuit.

The meaningful remaining obstruction is computational: physically distinguishable high-order probabilities must lead an optimum-blind policy to better graph solutions sooner than classical feasible search with the SAME information, while paying code/feature discovery, circuit training, sources, all raw attempts/photons, compilation/calibration, loss, decoding, score evaluations and any descent. Neither a new decoder nor a quantum-looking distribution proves that implication. Paper, held-out-positive and QPU gates remain closed.
