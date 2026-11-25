# Scientific claims registry

Current checkpoint: 2026-11-25. Allowed statuses: OPEN, PROVEN,
NUMERICALLY_SUPPORTED, HARDWARE_SUPPORTED, REJECTED. Proof does not imply novelty.
No claim is HARDWARE_SUPPORTED. The user-authorized rebuilt manuscript reports the evidence below; manuscript wording alone is not evidence. Submission readiness and full-composition novelty remain open; see reports/PUBLICATION_READINESS.md.

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-001 | Passive lossless optics preserves total photon number. | PROVEN | Number-conserving mode transformation; known background, not contribution. |
| CLAIM-002 | CF output of k photons decodes to weight-k bits. | PROVEN | Definition of CF; known background, not contribution. |
| CLAIM-003 | Fixed photon number implies no collisions. | REJECTED | HOM and explicit double-occupation states; PHYSICS_VALIDATION.md. |
| CLAIM-004 | Every fixed-k interferometer has P_CF=1. | REJECTED | HOM gives zero; full Perceval cross-validation. |
| CLAIM-005 | Cardinality penalty always makes the final QUBO fully dense. | REJECTED | Each pair gets 2lambda, but graph coefficients can cancel it at lambda=w; test_penalty.py and PENALTY_BASELINE_AUDIT.md. Sparse-to-quadratic coupling growth is generic, not universal. |
| CLAIM-006 | Fixed-particle encoding has a demonstrated resource benefit over real optical penalty methods. | OPEN | P30 authentic static optical component validated; full ObliQ training/source selection/decoder remains incomplete; classical penalty reference is explicitly labelled. No cross-hardware gate/depth equivalence. |
| CLAIM-007 | Haar average P_CF=binom(m,k)/binom(m+k-1,k), for a fixed normalized state in the indistinguishable k-photon Fock space, independent of Haar U, lossless. | PROVEN | theory/proven_results.md T-Haar; known Arkhipov–Kuperberg result. |
| CLAIM-008 | For even m, k=m/2, the Haar mean is asymptotic to sqrt(3)*(16/27)^(m/2). | PROVEN | T-Scaling, self-contained Stirling derivation; not a bound for every U. |
| CLAIM-009 | E01 means agree with the known P_CF prediction within stated marginal intervals. | NUMERICALLY_SUPPORTED | 3250 Haar circuits, n4/6/8/10, fixed seeds and raw.csv. Not a theorem or simultaneous test. |
| CLAIM-010 | A universal Pareto tradeoff forbids (P_CF,P_opt_given_CF)=(1,1). | REJECTED | Known-target mode permutation attains (1,1); T-Pareto. Discovery is classical. |
| CLAIM-011 | With one photon per occupied input mode, P_CF=1 iff occupied-column output supports are disjoint; then independent distinguishable sampling is exact. | PROVEN | T-Pairs, collision moment proof and independent review; no ancillas, loss or non-Fock input. Novelty OPEN. |
| CLAIM-012 | Full-distribution TV(p,d) <= min(1,(Per(B)-1)/2), B_ab=sum_i abs(U_ia U_ib). | PROVEN | theory/near_collisionless_bound.md N1; independent review and E08 finite checks. TV=half L1; spatial B. Formal corollary of Deshpande et al. after normalization; research/phase3_density_novelty.md. |
| CLAIM-013 | TV <= min(1,H_k(S)/2), H_k(S)=sum_{r=2}^k (!r/r!)*S^(r/2), S=norm(B-I)_F^2. | PROVEN | N2 cycle/closed-walk coefficient bound; independently reconstructed. Known permanent/cycle machinery; research/phase3_density_novelty.md. |
| CLAIM-014 | S <= m*binom(k,2)*(1-P_CF); the induced TV bound is a fixed-size stability certificate. | PROVEN | N3 via Cauchy–Schwarz and pair moments. Not dimension-uniform or a hardness claim. |
| CLAIM-015 | Small collision probability alone implies TV to distinguishable statistics vanishes uniformly at balanced density. | REJECTED | N4: m=2k, k even, delta=2/(k+2)->0 and TV=1/2. Exact rational cases plus full Fock checks. |
| CLAIM-016 | The tested generic bosonic mesh supplies a computational benefit at equal ideal attempts. | REJECTED | E05b fixed family/seed grid: distinguishable final means higher at n4/6/8; retrospective first-hit diagnostics favor uniform feasible sampling, but within-batch shot order is not independently reconstructible. Rejection is scoped to this tested protocol, not a universal impossibility. |
| CLAIM-017 | Broad graph-population significance or asymptotic algorithm advantage is established. | OPEN | Two nominal instances/family with shared seeds; only9/9/10 unique labeled graphs at n4/6/8. Graph-cluster intervals are descriptive only. |
| CLAIM-018 | New overlap certificate/counterexample is novel relative to all prior work. | OPEN | N1/N2 overlap is established; density composition and balanced obstruction attribution remain unresolved. Correctness alone supplies no novelty. |
| CLAIM-019 | Shallow success is invariant to vertex labels and all optima remain reachable. | REJECTED | E09 five of48 permuted n6 slots have structurally inaccessible optimal bisections at depth2. |
| CLAIM-020 | In the ideal fixed-k direct encoding, success equals P_CF*P_opt_given_CF; with loss use the full-k valid event F. | PROVEN | Conditional probability identity, with zero-CF support treated separately; not an independent objective or scientific novelty. |

Dependencies: CLAIM-007 -> CLAIM-008/009; pair moment T-Pairs -> CLAIM-011/014;
CLAIM-012 -> CLAIM-013 -> CLAIM-014; explicit orthogonal columns + spectators
prove the rejection in CLAIM-015 independently of finite sampling.

Review provenance: theorem files retain hypotheses and exact audited SHA256 in
reports/THEORY_AUDIT.md and reports/NEAR_COLLISIONLESS_INDEPENDENT_REVIEW.md.
All raw run provenance and output checks: reports/RESULTS_AUDIT.json.


## Phase3 claim additions — 2026-11-22

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-021 | The authenticated static ObliQ kernel reproduces archive unitaries and full Fock probabilities in the tested finite ideal cases. | NUMERICALLY_SUPPORTED | P30, c3b83ef; archive hash and independent controls. Not complete optimizer reproduction. |
| CLAIM-022 | Fixed-input/fixed-order normalized static optical penalties wash out graph-dependent state differences at the stated O(lambda^-1/2) or O(lambda^-1) rates. | PROVEN | theory/phase3_penalty_washout.md; independent review6fcfc94. Not an optimization lower bound; graph-dependent decoder and source changes are excluded. |
| CLAIM-023 | Maximizing Haar feasible probability per attempt always also minimizes photon cost under loss and finite budgets. | REJECTED | P32 exact rational counterexamples; retain source and detector assumptions. |
| CLAIM-024 | For nonnegative graph weights and mu>=0, occupation quadratic mean cost is no smaller for bosons than distinguishable photons at the same occupied frame. | PROVEN | theory/phase3_occupation_dominance.md; explicit nonnegative gap and finite Perceval validation98e4ecc. Coordinator proposal with component reconstruction; not an author-blind proof audit. No tail/success dominance. |
| CLAIM-025 | With distinct singly occupied inputs and every positive row intensity at least c>0, expected collision pairs M bound full-law TV by the stated density envelope, with refined leading M/(2c) at fixed c. | PROVEN | Exact theorem75e5831, fresh independent review4420e17. Sharp balanced family. Novelty OPEN. Floating API77a8588 is not interval certified. |
| CLAIM-026 | A vanishing absolute-TV certificate implies every rare-event relative success ratio tends to one. | REJECTED | theory/phase3_density_success_scope.md; exact ratio-two family and divergent waiting times,385293e. |
| CLAIM-027 | Fixed-rank threshold objective polynomial evaluation is a new algorithmic contribution. | REJECTED | theory/phase3_threshold_lowrank.md; AA1011.3245 and Ivanov–Gurvits1904.06069 already give the relevant polynomial method. |
| CLAIM-028 | A native seven-role workflow completed execution/replication and passed the independent finite-data audit. | NUMERICALLY_SUPPORTED | b8b04ac, nine completed contexts, four real typed actions and three exact handoffs; 300 grid cases,12 extra physical crosschecks. Model reasoning remains unreliable and rejected. Separate Agent Team lifecycle FAIL. |

CLAIM-025 depends on CLAIM-012/013 and the explicitly proved dominant-row and
density implications. It does not imply CLAIM-016 or hardware readiness.

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-029 | Fresh-input classical adaptive protocols with conditional TV bounds and uniform majorants e_t in [0,1] admit the stated absolute transcript/success replacement bound. | PROVEN | Corrected proofb3b0219 passed independent review3c43eda; original missing-range defect retained. Exact coordinator and1640-transcript independent checks. Standard coupling, no novelty or rare-event ratio claim. |

2026-11-22 attribution refinement: research/phase3_density_crossfield_novelty.md
identifies the density row inequalities with known Bayes-error/quadratic-impurity
relations. No standalone novelty is claimed for those ingredients. Complete
photonic composition attribution remains OPEN.


## Latest bounded results — 2026-11-22

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-030 | For two occupied orthonormal input columns, full-law TV<=delta-delta²/2, sharp for every delta in [0,1]. | PROVEN | theory/phase3_linear_leakage_attempt.md,224327c: complete Cauchy/N1 derivation and exact sharp family. Physics proposal reconstructed by coordinator, no author-blind audit or novelty claim. |
| CLAIM-031 | The same-frame full-law TV<=min(1,delta) for every photon count. | OPEN | 256 fixed circuits and17856 targeted calls found no refutation; k2 proved, k>=3 unresolved. Positive-permanent shortcut explicitly false. Reports/P36 files retain all data and limits. |
| CLAIM-032 | The known rank1/2 marginal DP implementation reproduces the original threshold-QUBO mean on the fixed validation inputs. | NUMERICALLY_SUPPORTED | c6c1807: six exactly rational physical circuits match explicit Fock arithmetic exactly;12 Perceval comparisons, max energy error7.11e-15. No novel algorithm, full sampler or finite-shot training equivalence. |
| CLAIM-033 | For even m>=8,k=m/2,k<=N<=m and 0<eta<1 uniform independent loss, Haar-mean source maxima lie in {m-1,m} per attempt and {m-3,m-2,m-1,m} per photon, with ordered unique transitions. | PROVEN | Exact proof1d65279 passed fresh independent reconstruction7729b91. Exact1610-value/36-bracket check plus separate Polya check; reviewer has independent m8 polynomial checks. Known-law resource corollary, no novelty or graph-quality claim. |
| CLAIM-034 | P37 critical scaled losses tend to1 for attempt efficiency and1,2,3 for successive photon-efficiency transitions as even m grows. | PROVEN | Same proof independently reviewed7729b91: fixed-lambda, fixed-deficit moment/tail expansion and root sandwich. Values through m128 are finite checks only. Not fixed-loss or fixed-device complexity. |
| CLAIM-035 | Fine occupation TV is bounded by the stated internal-state-preserving pinched distance; its sector variational formula uses an infimum. Complex k3 dominant effects admit rank-one refinements with at most27 rows. | PROVEN | theory/phase3_pinching_dual.md,197af80, coordinator reconstruction/self-review, not blind audit. Source channel structure known. Boundary nonattainment handled separately in phase3_pinching_dual_boundary.md. |
| CLAIM-036 | For every physical three-column frame, D_pinched<=delta on the dominant partition. | OPEN | P38:36 circuits and explicit-state audit pass;10790 matrix queries have no certified refutation but no converged solver. Finite tests are not proof. Stronger than CLAIM-031. |
| CLAIM-037 | The exact k2 curve delta-delta²/2 also bounds every k3 pinched-state distance. | REJECTED | Post-hoc auxiliary hypothesis, not original P36. P39 explicit d19/25,e3/25 physical frame gives exact D_pinched>24493/50000>288/625, two rational arguments plus Perceval check. No refutation of the corresponding measured-TV statement. |

P20 archives and their independent review are integrated5dbdbc3/a4d4745.
They reject only the tested fixed-size proposal construction: selected kernels
have zero interference and match the product control. They are fixed-anchor
IID probes, not executed adaptive optimizers or equal-total-resource proofs.


## Recovery disposition — 2026-11-24

The unsupported cf49741/6154b46 superiority and ready flags are withdrawn. Current accepted claims are the exact P33 density-qualified absolute-TV certificate (known ingredients, complete originality OPEN), P37 criterion-dependent Haar-loss source theorem, and the restricted negative E05b benchmark. Per-state/graph constants and source domains are corrected in the rebuilt manuscript. Current evidence: reports/SCIENTIFIC_INTEGRITY_AUDIT.md, NUMERICAL_RECONCILIATION.md and PUBLICATION_THESIS.md.

A new optimum-blind training API rejects optimal-mask objectives; old oracle diagnostics remain archived. New noise code is a bounded theoretical pure-internal-state/loss simulator, not a hardware calibration. The local pilot works; actual backend compatibility/authorization remain false. PDF/tests do not change novelty or advantage status.

## P41/P42 discovery restart — 2026-11-24

These are research results, not manuscript additions. Audited hashes, commits,
commands and data: reports/P42_DISCOVERY_CHECKPOINT.md. Proof does not imply novelty.

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-038 | For disjoint one-photon output groups and a fixed passive frame, an efficient classical random-wave feasible law pointwise dominates the unconditioned grouped probabilities. | PROVEN | P41_encoding_grouped_domination.md and independent reconstruction/audit. Known phase-twirl/Glynn ingredients; no automatic adaptive-history or equal-realized-score-budget extension. |
| CLAIM-039 | Fresh distinct identical-photon inputs, uniform internal-blind loss and complete direct-support readout obey the P42 per-string cap; L*binom(2k,k)*b<=1 with L=ceil(nQ/nC) implies uniform feasible search stochastically dominates adaptive best newly measured cost. | PROVEN | Frozen525e254; independent exact-hash adaptive/physics verdicts. No Haar assumption; eta<=1/5 suffices at equal counts. Source, loss, frontend and guaranteed cost hypotheses essential. No measured QPU efficiency. |
| CLAIM-040 | The general fixed-Fock/unknown-internal-state support bound is the sum of the largest projector-rank number of loss block traces, with ordered surjection ranks for arbitrary internals. | PROVEN | P42_general_fock_loss_extension.md, independent ordered partial-trace reconstruction in P42_replication_report.md.42 configurations/168 laws check a finite implementation; no superposition/herald/nonuniform-loss claim. |
| CLAIM-041 | The complete P42 adaptive optimization obstruction is globally new. | OPEN | Known loss/spectral/first-hit ingredients identified. Bounded source comparison does not establish absence from prior literature. |
| CLAIM-042 | A new optimum-blind interference optimizer passes independent D, strong feasible classical controls, fresh seeds, labels, held-out graphs and full costs. | OPEN | No such result yet. P41 is diagnostic; P42 is an obstruction. Positive replication/QPU gate remain closed. |

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-043 | Unconditional L1 occupation means for identical CF inputs admit polynomial arithmetic two-mode marginal evaluation; the exact/additive variants obey the stated representation/scale contracts. | PROVEN | P42_encoding_local_L1_oracle.md, corrected SHAbae5da4f; independent P43_LOCAL_AUTHOR_PROOF_REVIEW.md. Known marginal/Gurvits methods. No full sampler, conditioned-tail solver or optimizer guarantee. |
| CLAIM-044 | For identical CF source inputs through passive vacuum-loss T, any fixed k-mode all-click event is bounded by ||T[:,A]||^(2k), and click-contained decoders inherit the cap; the P42 guaranteed-budget criterion yields adaptive best-cost domination. | PROVEN | Rootb87e677, exact-hash independent P44_AUTHOR_PROOF_REVIEW.md and frozen reconstruction2d15012.190 small dilation cases support finite consistency. No Haar/uniform loss assumption; no actual hardware norm/cost value or universal ideal no-go. |
| CLAIM-045 | Arbitrary internal states at fixed CF spatial inputs under common T obey the conservative k!*||T[:,A]||^(2k) moment cap. | PROVEN | Independent routing/purification Cauchy derivations in the P44 proof/review; product and correlated small cases retained. Does not give the identical dimension-uniform eta<=1/4 criterion, and excludes internal-dependent loss. |
| CLAIM-046 | The tested P43 global-gain finite-angle echo supplies useful optimization benefit at its frozen budgets. | REJECTED |896 B attempts,zero improvements,373 CF/523 collisions; all4 graphs retained; classical anneal/spectral improve both20-mode anchors. Full raw reconstruction agrees. This rejects one family/budget, not every optical algorithm. |
| CLAIM-047 | The complete P44 adaptive balanced-search application is globally novel. | OPEN | Known Cauchy–Binet/norm/thermal ingredients explicitly attributed. Exact source-directed comparison is bounded, not exhaustive novelty certification. |

## Research continuation P45–P55 — manuscript unchanged

The following entries record new research evidence, not new statements in the
published/delivered manuscript. CLAIM-042 remains OPEN. No positive held-out
optimizer replication or hardware claim has been accepted.

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-048 | The frozen P45–P50 DEV pipelines supply the requested optimization benefit at their tested budgets. | REJECTED | Per-route raw data/manifests and research/P45_LIVE_STATE.md. In P50 each independently budgeted raw classical mode beats paid B on all4 graphs; a separate raw consistency audit is not blind physical replication. Rejection is scoped to tested families/cost contracts. |
| CLAIM-049 | A passive unitary preserving the whole r-photon collision-free subspace, 2<=r<=N, is monomial; the stated continuous nonconstant balanced-cut phase shortcut is unavailable in that model. | PROVEN | theory/P50_passive_hard_core_cost_phase_obstruction.md and separate reconstruction/review. Fixed-input, r1, dualrail, heralding and isolated integer-phase exceptions are explicit; not a general optimizer no-go. |
| CLAIM-050 | For a square flat unitary with one photon in every input, all joint factorial moments through total order3 are phase invariant. | PROVEN | theory/P51_Hadamard_low_order_invariance.md and ROOT reconstruction. Truncated columns and B-versus-D comparisons are different questions; novelty not established. |
| CLAIM-051 | Equal factorial moments through b at fixed total r imply identical <=b survivor sectors under common uniform loss and TV<=Pr[Binom(r,eta)>b]. | PROVEN | theory/P51_uniform_loss_matched_moment_lemma.md and ROOT reconstruction. Exact eta^r scaling requires b=r-1. Nonuniform loss/random source totals excluded. |
| CLAIM-052 | The specified H4 top2 phase response has an exact constant-size classical mixture. | PROVEN | theory/P50_Hadamard4_ranked_cut_checkpoint.md and rank_mixture_addendum.md. Physical phase sensitivity alone is not an optimization advantage or arbitrary-N replacement. |
| CLAIM-053 | P52's four fixed circuits show a low-moment-invariant cut-mean response, numerically replaced by mixtures of regrouped b4 kernels/uniform70. | NUMERICALLY_SUPPORTED | Primary762877a, all4 mean fits verified; independent Perceval25,740-amplitude engine replication agrees. research/P52_collective_phase_result.md and P52_NAIVE_COMPLETE_REPLICATION_REVIEW.md. No full-law, continuous-phase, total-cost or optimizer conclusion. |
| CLAIM-054 | Every continuous phase of the P52 family admits the fixed ENDPOINT71 convex mean replacement. | OPEN | P53's exact source/library construction passes18 targeted tests; degree6/12 sufficient certificate search is INCONCLUSIVE. Failed Bernstein controls prove neither curve nonmembership nor a quantum advantage. P53b single-point question is separately prospective. |
| CLAIM-055 | For a fixed finite graph, full-CF input, real sqrt(weight) hopping and raw-count top-half ties, the bosonic leading cut drift is +4t² Var(C)/q with O_G(t⁴) remainder. | PROVEN | Root4d6826d, independently frozen43b35f9 and focused91fb868 review; reports/P54_PROOF_CHECKPOINT.md. Weak effect has a classical rare-hop replacement and retuned D control. Weighted A=w, finite strength, other inputs/decoders and equal-cost dominance excluded. |
| CLAIM-056 | The proposed neutral-count decoder yields a useful finite-coherence optimizer advantage over independently retuned D and strong classical controls. | OPEN | research/P55_NEUTRAL_DEFECT_DECODER_CARD.md is a prospective definition/DP proof with a known classical weak-order explanation. Prototype qualification and any finite pilot remain separate gates. No positive or hardware compatibility inferred. |
