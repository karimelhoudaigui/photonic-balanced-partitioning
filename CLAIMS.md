# Scientific claims registry

Current checkpoint: 2026-11-22. Allowed statuses: OPEN, PROVEN,
NUMERICALLY_SUPPORTED, HARDWARE_SUPPORTED, REJECTED. Proof does not imply novelty.
No claim is HARDWARE_SUPPORTED. Manuscript claims are frozen, not evidence.

| ID | Exact statement / scope | Status | Evidence and limits |
|---|---|---|---|
| CLAIM-001 | Passive lossless optics preserves total photon number. | PROVEN | Number-conserving mode transformation; known background, not contribution. |
| CLAIM-002 | CF output of k photons decodes to weight-k bits. | PROVEN | Definition of CF; known background, not contribution. |
| CLAIM-003 | Fixed photon number implies no collisions. | REJECTED | HOM and explicit double-occupation states; PHYSICS_VALIDATION.md. |
| CLAIM-004 | Every fixed-k interferometer has P_CF=1. | REJECTED | HOM gives zero; full Perceval cross-validation. |
| CLAIM-005 | Cardinality penalty always makes the final QUBO fully dense. | REJECTED | Each pair gets 2lambda, but graph coefficients can cancel it at lambda=w; test_penalty.py and PENALTY_BASELINE_AUDIT.md. Sparse-to-quadratic coupling growth is generic, not universal. |
| CLAIM-006 | Fixed-particle encoding has a demonstrated resource benefit over real optical penalty methods. | OPEN | P30 authentic static optical component validated; full ObliQ training/source selection/decoder remains incomplete; classical penalty reference is explicitly labelled. No cross-hardware gate/depth equivalence. |
| CLAIM-007 | Haar average P_CF=binom(m,k)/binom(m+k-1,k), for fixed normalized input independent of Haar U, lossless. | PROVEN | theory/proven_results.md T-Haar; known Arkhipov–Kuperberg result. |
| CLAIM-008 | For even m, k=m/2, the Haar mean is asymptotic to sqrt(3)*(16/27)^(m/2). | PROVEN | T-Scaling, self-contained Stirling derivation; not a bound for every U. |
| CLAIM-009 | E01 means agree with the known P_CF prediction within stated marginal intervals. | NUMERICALLY_SUPPORTED | 3250 Haar circuits, n4/6/8/10, fixed seeds and raw.csv. Not a theorem or simultaneous test. |
| CLAIM-010 | A universal Pareto tradeoff forbids (P_CF,P_opt_given_CF)=(1,1). | REJECTED | Known-target mode permutation attains (1,1); T-Pareto. Discovery is classical. |
| CLAIM-011 | With one photon per occupied input mode, P_CF=1 iff occupied-column output supports are disjoint; then independent distinguishable sampling is exact. | PROVEN | T-Pairs, collision moment proof and independent review; no ancillas, loss or non-Fock input. Novelty OPEN. |
| CLAIM-012 | Full-distribution TV(p,d) <= min(1,(Per(B)-1)/2), B_ab=sum_i abs(U_ia U_ib). | PROVEN | theory/near_collisionless_bound.md N1; independent review and E08 finite checks. TV=half L1; spatial B. Formal corollary of Deshpande et al. after normalization; research/phase3_density_novelty.md. |
| CLAIM-013 | TV <= min(1,H_k(S)/2), H_k(S)=sum_{r=2}^k (!r/r!)*S^(r/2), S=norm(B-I)_F^2. | PROVEN | N2 cycle/closed-walk coefficient bound; independently reconstructed. Known permanent/cycle machinery; research/phase3_density_novelty.md. |
| CLAIM-014 | S <= m*binom(k,2)*(1-P_CF); the induced TV bound is a fixed-size stability certificate. | PROVEN | N3 via Cauchy–Schwarz and pair moments. Not dimension-uniform or a hardness claim. |
| CLAIM-015 | Small collision probability alone implies TV to distinguishable statistics vanishes uniformly at balanced density. | REJECTED | N4: m=2k, k even, delta=2/(k+2)->0 and TV=1/2. Exact rational cases plus full Fock checks. |
| CLAIM-016 | The tested generic bosonic mesh supplies a computational benefit at equal ideal attempts. | REJECTED | E05b fixed family/seed grid: distinguishable final means higher and uniform feasible first discovery faster in aggregate. Rejection is scoped to this tested protocol, not a universal impossibility. |
| CLAIM-017 | Broad graph-population significance or asymptotic algorithm advantage is established. | OPEN | Two instances/family and shared seeds; pooled intervals descriptive only. |
| CLAIM-018 | New overlap certificate/counterexample is novel relative to all prior work. | OPEN | N1/N2 overlap is established; density composition and balanced obstruction attribution remain unresolved. Correctness alone supplies no novelty. |
| CLAIM-019 | Shallow success is invariant to vertex labels and all optima remain reachable. | REJECTED | E09 five of48 permuted n6 slots have structurally inaccessible optimal bisections at depth2. |
| CLAIM-020 | Physical success equals P_CF*P_opt_given_CF. | PROVEN | Conditional probability identity, with zero-CF support treated separately; not an independent objective or scientific novelty. |

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
| CLAIM-028 | A fully completed native seven-role Qwen scientific cycle has passed independent audit. | OPEN | Workflow subagent smoke passes; previous density cycles failed execution/replication. Typed-action cycle under validation. Agent Team lifecycle remains FAIL. |

CLAIM-025 depends on CLAIM-012/013 and the explicitly proved dominant-row and
density implications. It does not imply CLAIM-016 or hardware readiness.
