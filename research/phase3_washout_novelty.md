# Phase 3 adversarial novelty audit: penalty-normalized optical anchors

**Verdict: the broad novelty claim is refuted; the exact architecture-specific claim remains OPEN.** Large penalties suppressing the effective objective after hardware rescaling is explicitly documented in earlier primary literature. The copy-discrimination bound and strict-gap ranking/argmin stability are standard mathematical tools. No checked source states the complete ObliQ-specific limit with the same hypotheses and the `R=1` versus `R>=2` exponents, but an unsuccessful exact-match search does not establish originality. Much of that specialization follows directly from the authenticated angle formula by elementary calculus and a finite-product perturbation bound.

The defensible candidate is a quantitatively delimited failure mechanism of a particular static optical encoding, with operational consequences still requiring task evidence. It is not a new principle about penalty methods, quantum measurement, or the complete ObliQ algorithm. This audit authorizes no manuscript or QPU work.

Checked 2026-11-21. Isolated worktree: `.qwen/worktrees/phase3-literature`; base commit `1680234067000c0f4d8121fe328176fb2edc8c16`. Only this report is written. No simulation, original external program, optimizer, hardware experiment, or QPU call was executed for this literature task.

## Exact target under review

The claim being compared to prior work is narrower than "penalties are bad". For fixed even mode count `m`, a fixed noncomplete nonnegative weighted graph, `k=m/2`, and the symmetric convention `x.T Q_lambda x`, sufficiently large `lambda` gives

\[
(Q_\lambda)_{ii}=d_i-(m-1)\lambda,\qquad
(Q_\lambda)_{ij}=\lambda-w_{ij},
\]

and global entrywise min–max normalization gives

\[
(A_\lambda)_{ij}=1-\frac{w_{ij}}{m\lambda-d_{\min}}\quad(i\ne j).
\]

Feed those normalized off-diagonal values into the **authenticated static archive kernel**, fixing the pair order and repetition number `R`:

\[
g_R(a)=\tfrac12\arccos\sqrt{1-a/R^2},\qquad
G(\beta)=\cos(\beta/2)I+i\sin(\beta/2)X.
\]

The candidate is convergence to the same ordered circuit with all off-diagonal couplings equal to one, `U_lambda -> U_infty`, which does not depend on the graph. Proposed upper rates are `O(lambda^-1/2)` at `R=1` and `O(lambda^-1)` for fixed `R>=2`. A fixed common `N`-photon input, independent of the graph and penalty, gives an output-vector distance at most `e_lambda=N ||U_lambda-U_infty||`. For `T` independently prepared copies, a common channel and any final measurement, the candidate consequence is `TV <= sqrt(T) e_lambda` and a necessary cost `T=Omega(lambda^(2 alpha)/N^2)` to obtain a fixed positive discrimination distance when `||U_lambda-U_infty||=O(lambda^-alpha)`.

The rates are upper bounds, not asymptotic equalities; the shot cost is a necessary bound for the specified discrimination experiment, not a hardness bound for graph optimization with a classically known graph. Fixed `m,R,graph` and their constants cannot silently become a uniform joint scaling result in `m,N,lambda`. The paper-corrected doubled API angle is a separate variant.

A further candidate is stability of marginal-ranked prefixes or a modal pattern under strict limiting gaps. That is a conditional decoder result, not an automatic consequence of the raw-state convergence.

Local target/specification inputs read from the research checkout:

- `theory/phase2_candidates.md`, SHA256 `b10a2c03c1c3239f80c8306c6e42607f210675e5e3b34c4bf3371fda3cb36888`.
- `research/optical_penalty_spec.md`, SHA256 `d00db87b4d27633106c447c5657a860cfbb263482fd2da7ebef1e980f854e4cf`.

Their internal proof status is separate from this source-overlap audit.

## Claim-by-claim overlap assessment

| Claim or inference | Closest checked primary evidence | Overlap classification | Application verdict |
|---|---|---|---|
| A large penalty plus global hardware scaling makes objective differences hard to resolve | Künnemann–Phillipson 2023, Sec. 4; Doucet et al. 2026, Secs. V.1 and VI | **known after translation of notation** | **Verified** as an earlier explicit mechanism. A broad originality claim fails. |
| Balanced graph partitioning is encoded by a quadratic cardinality penalty plus cut energy | Lucas 2014, Sec. 2.2 | **known after translation of notation** | **Verified** for the standard construction; expanding to the stated weighted Q matrix is elementary. |
| The exact min–max formula above for this balanced penalty matrix | Standard penalty expansion plus the original archive's normalization | **formal corollary not stated** | The external ingredients are authenticated. Correctness of the project's algebra remains an internal proof obligation, not a theorem imported from an unrelated paper. |
| The authenticated ordered BS anchor converges to a graph-independent circuit with the endpoint-dependent rates | ObliQ Sec. 4.1 and exact archive `circ_init.py`; the scalar map is explicit | **formal corollary not stated** | No exact prior full theorem was authenticated. The endpoint exponents are a direct specialization of the map's square-root endpoint versus smooth interior, rather than an independently new perturbation principle. Novelty of the complete architecture-specific package remains OPEN. |
| Small vector distance implies `TV <= sqrt(T) e_lambda` for independent copies | Fuchs–van de Graaf 1998 v2, Thm. 1 Eq. (46); Watrous 2018, Prop. 3.16 and Thms. 3.27/3.33; Audenaert et al. 2006 v1, Secs. II and IV | **formal corollary not stated** | **Verified** under the common-input, independent-copy and common-channel assumptions. This is an application of established state-discrimination machinery. |
| A positive gap preserves a finite ranking, modal choice or finite-set minimizer under sufficiently small uniform perturbation | Elementary gap argument; adjacent quantitative QUBO rounding result in Mücke–Gerlach–Piatkowski 2023, Sec. 2.3 | **formal corollary not stated** | **Conditional** on the actual relevant gaps. The cited QUBO energy gap is not an optical marginal gap. |
| A good finite-shot penalty can be selected with a guaranteed feasible/low-energy probability | Alessandroni et al. 2026 v2, Def. 1, Thms. 3 and 14 | **partial or adjacent result only** | **Inapplicable** to the optical anchor without establishing the required Gibbs law. It is substantial prior work on penalty selection and finite sampling, not an ObliQ theorem. |
| The complete hybrid ObliQ optimizer, its graph-aware decoder or all penalty-based photonic methods must fail at this rate | None of the checked sources, and not implied by the static theorem | **partial or adjacent result only** | **Unverified** and overbroad. Graph-dependent source selection, retuning and classical processing remain separate information channels. |

"Formal corollary not stated" identifies a routine mathematical implication of checked ingredients; it does not assert that the whole project result was published verbatim. The table deliberately does not assign an "apparently new" label to a theorem just because no match was found.

## Strongest prior work and exact hypothesis comparisons

### 1. Direct earlier statement of normalization-induced objective suppression

Hendrik Künnemann and Frank Phillipson, *Finding Debt Cycles: QUBO Formulations for the Maximum Weighted Cycle Problem Solved Using Quantum Annealing*, **Mathematics 11(12), 2741 (2023)**, published 2023-06-16, [DOI 10.3390/math11122741](https://doi.org/10.3390/math11122741), Sec. 4, paragraphs on penalty selection and D-Wave autoscale.

The full primary article explicitly explains that large penalties reduce the relative objective weight; autoscaling into a fixed coefficient range can make the objective disappear after rounding. It also distinguishes too-small penalties allowing infeasible solutions. This is a published implementation discussion, not a theorem about photonic unitaries or independent-copy shot complexity. Its annealer/rounding hypotheses do not yield the exact ObliQ lossless limit, but they decisively rule out presenting the generic dilution mechanism as a discovery of this project. [Primary full text](https://www.mdpi.com/2227-7390/11/12/2741).

### 2. An explicit recent global-rescaling/energy-scale account

Emery Doucet et al., *Thermodynamic significance of QUBO encoding on quantum annealers*, [arXiv:2601.04402v1](https://arxiv.org/html/2601.04402v1), dated 2026-01-07. Relevant locations: Sec. V.1, discussion comparing Figures 4–6, and Sec. VI. The checked version discusses stronger global rescaling under larger penalties, the reduced physical objective scale relative to thermal fluctuations and control errors, and resulting degradation. It studies job-shop encodings on D-Wave and thermodynamic quantities.

This is not the same mathematical result: an ideal passive optical static kernel has no annealing temperature or ground-state preparation law. The source supplies a close established physical motivation and vocabulary. Its exact-state dynamics, observables and constants cannot be substituted for the project's BS construction.

### 3. Substantial 2026 penalty-selection and finite-sampling theory

Edoardo Alessandroni et al., *Scalable Determination of Penalization Weights for Constrained Optimizations on Approximate Solvers*, [arXiv:2604.02416v2](https://arxiv.org/html/2604.02416v2), dated **2026-10-20**; v1 is dated 2026-04-02 and has different theorem numbering and author list.

Definition 1 requires probability at least `eta` of a feasible state below energy threshold `E_f`. Theorem 3 assumes a **Gibbs sampler at inverse temperature beta**, infinite preliminary samples, zero margins and the full penalty cutoff; when its algorithm returns a penalty, the guarantee holds. Appendix B, Theorem 14 gives the finite-sample confidence version with `E_f` and bin width chosen independently of samples. Those assumptions and the conditional "if the algorithm returns" clause matter. This is an adjacent theorem about choosing penalties, not an optical min–max/unitary convergence theorem.

A Gibbs conditional law on feasible states, at fixed inverse temperature and without global rescaling, is independent of a penalty which vanishes there. Consequently, no claim that arbitrarily increasing a penalty inherently destroys the feasible objective ranking is justified without specifying normalization, precision, effective temperature or the actual non-Gibbs optical encoding.

### 4. Formal dynamic-range and gap-robustness work

Sascha Mücke, Thore Gerlach and Nico Piatkowski, *Optimum-Preserving QUBO Parameter Compression*, [arXiv:2307.02195v1](https://arxiv.org/html/2307.02195v1), dated 2023-07-05. The later publication is [Quantum Machine Intelligence, DOI 10.1007/s42484-024-00219-3](https://doi.org/10.1007/s42484-024-00219-3); theorem references here are to **v1**.

Sec. 2.1 defines optimum inclusion; Sec. 2.2 defines dynamic range; Sec. 2.3 models rounding as a bounded energy perturbation. Definition 5 defines the lowest distinct energy gap, and Theorem 1 states a sufficient scaling for optimum-preserving rounding in the authors' upper-triangular Q convention. The source's particular constant is not needed or transplanted here. This establishes that using a nonzero optimization gap to protect a minimizer is existing machinery. It does not establish marginal-order stability of a photon distribution: that needs the project's separate probability-gap assumptions and normalization dictionary.

### 5. The basic bisection penalty is established

Andrew Lucas, *Ising formulations of many NP problems*, **Frontiers in Physics 2, 5 (2014)**, [DOI 10.3389/fphy.2014.00005](https://doi.org/10.3389/fphy.2014.00005), Sec. 2.2, treats even-size balanced graph partitioning with a quadratic balance penalty plus edge-cut cost and discusses adequate penalty strength. Its spins satisfy `s_i in {-1,+1}`; the project uses `x_i in {0,1}`. Expanding that standard encoding, with weighted edges, gives the project's Q matrix. The exact min–max denominator belongs to its subsequent optical translation, not a new constrained-optimization encoding.

### 6. Independent-copy discrimination and channel monotonicity are standard

Christopher Fuchs and Jeroen van de Graaf, *Cryptographic Distinguishability Measures for Quantum Mechanical States*, [arXiv:quant-ph/9712042v2](https://arxiv.org/html/quant-ph/9712042v2), revised **1998-04-03**, Sec. 4.2 and Thm. 1, Eq. (46), identify measured distinguishability with halved trace distance and bound it using the unsquared fidelity/Bhattacharyya quantity. John Watrous's [2018 author draft of *The Theory of Quantum Information*](https://cs.uwaterloo.ca/~watrous/TQI/TQI.pdf), Prop. 3.16 Eq. (3.90), Thm. 3.27 Eq. (3.173), and Thm. 3.33 Eqs. (3.204)–(3.205), respectively gives tensor multiplicativity, common-channel fidelity monotonicity and the same distance inequalities. The exact implications and conventions were checked; no claim of a new discrimination inequality is supportable.

K. M. R. Audenaert et al., *The Quantum Chernoff Bound*, [arXiv:quant-ph/0610027v1](https://arxiv.org/html/quant-ph/0610027v1), submitted **2006-10-04**, published **PRL 98, 160501 (2007)**, Sec. II Eqs. (1)–(2), characterizes the independent-copy asymptotic error exponent; Sec. IV gives the pure-state fidelity specialization. The arXiv abstract/version record, rather than the HTML renderer's regenerated internal title date, fixes the version. This is an additional source showing that fidelity controls copy cost; the simpler finite-copy inequality already suffices for P2-B.

## What the exact ObliQ sources do and do not say

Aditya Ranjan, Daniel Silver, Tirthak Patel, Bhargav Chickmagalurnanjun and Devesh Tiwari, *ObliQ: Solving Quadratic Unconstrained Binary Optimization Problems on Real Photonic Quantum Machines*, **PACM MACS 9(3), Article 58 (2025)**, [DOI 10.1145/3771573](https://doi.org/10.1145/3771573). Relevant primary text: Sec. 4.1, especially journal pages 58:8–58:9; Sec. 4.2 for the graph-aware decoder; Sec. 5 for its fixed graph-coloring penalty experiment. The [Rice author-repository PDF](https://repository.rice.edu/server/api/core/bitstreams/0c308cfa-0cac-4b03-ba49-9effdba0799b/content) has SHA256 `61f3fb1f26a9553845b75d0fc7b6e973c28d30cc06c1c7e730c108a3d7a2da86`.

The paper specifies a constant/zero-diagonal QUBO class, normalized couplings, kernel layering, and classical solution mapping. The [versioned Zenodo artifact 17343439](https://zenodo.org/records/17343439), `ObliQ.zip`, SHA256 `8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948`, fixes the executable global entrywise normalization and `a/R^2` angle map. It pins Perceval 0.11.0; the inspected [legacy BS source](https://raw.githubusercontent.com/Quandela/Perceval/v0.11.0/perceval/components/unitary_components.py) fixes the Rx half-angle convention.

No penalty-to-infinity optical limit or the proposed exponents were found in these checked relevant sections. That absence is a bounded content observation. It does not establish that no predecessor, later reproduction, unpublished note or equivalent general theorem contains the result.

## Adversarial assessment of the architecture-specific part

The strongest attempted reduction of the novelty claim is structural:

1. The min–max limit is obtained by expanding an already standard QUBO and identifying its maximum and minimum coefficients.
2. In the explicit archive map, at `R=1` the limiting argument is the square-root/arccos endpoint; at fixed `R>=2` it lies away from that singular endpoint. The half-power versus first-power response is ordinary scalar regularity.
3. A finite product of unitary gates inherits a sum of per-gate perturbation bounds. Fixing the sequence, routing and repetitions makes this a standard telescoping estimate.
4. Restricting `U^(tensor N)` to the symmetric subspace introduces the usual at-most-linear `N` norm factor.
5. State fidelity, tensorization and a common channel produce the conventional copy-discrimination bound.

Thus even a correct exact theorem requires explanation of why this particular operational failure mode matters. Combining familiar lemmas around an explicit implementation can yield a useful technical result, but the derivation alone is weak evidence of a nontrivial original contribution. Constants, hypotheses, relevant operating ranges and an actual effect on the graph task are the plausible distinctive content. Generic claims of quantum or penalty-method impossibility are not.

The `R=1` exponent must also be interpreted carefully: an upper bound `O(lambda^-1/2)` does not imply a matching lower bound, and gate cancellation, state symmetries or measurement coarse-graining may give a faster observed rate. Likewise the common graph-independent limiting **unitary** does not imply a graph-independent state if the input preparation itself depends on the graph.

## Shot-cost dictionary and exclusions

Use `F=|<psi_lambda|psi_infty>|^2` for squared fidelity. The original Fuchs–van de Graaf quantity and Watrous's `F` use its square root; confusing these conventions changes powers. If vector distance is at most `e_lambda`, then `F>=1-e_lambda^2`. For independent copies, fidelity is `F^T`; hence

\[
\operatorname{TV}({\rm measured\ copies})
\le \sqrt{1-F^T}\le\sqrt{T}\,e_\lambda.
\]

The common channel may include a fixed physical loss/readout process, but hypothesis-dependent processing does not follow from this argument. A fixed target distinction `c>0` requires `T>=c^2/e_lambda^2`, and substituting the proven architecture-specific upper bound gives the proposed necessary powers. This finite-copy derivation is a standard application of the cited results. It does not prove tightness, optimal sample complexity for a particular detector, a lower bound on optimization when the graph is already supplied, or a barrier to graph-aware classical proposals. Adaptive selection of different circuits or graph-dependent hybrid inputs is outside the identical-copy experiment.

No new numerical values or experiments are inferred from these inequalities in this report.

## Prefix stability: ordinary gap mathematics with a genuine scope hazard

If `TV(p_lambda,p_infty)<=epsilon`, each click marginal and each individual output probability changes by at most `epsilon`. A strictly ordered pair of limiting marginals separated by more than `2epsilon` retains its order. A uniquely most probable pattern with a gap exceeding `2epsilon` remains modal. The same elementary statement for finitely many scores preserves an argmin whenever its objective gap exceeds twice the uniform score perturbation. These are conditional finite-ranking/argmin continuity arguments, not a new photonic mechanism. The adjacent QUBO rounding theorem above concerns **energy** gaps; it cannot be cited as an optical **probability** gap theorem.

A gap must actually be established. The theory workstream supplied the admissible four-mode matching order

`[(0,1),(2,3),(0,2),(1,3),(0,3),(1,2)]`.

At equal limiting angles, the three matching generators commute, giving `U_infty=exp(i R beta (J-I)/2)`. With the permutation-invariant input `(1,1,1,1)`, all limiting click marginals are equal. This algebraic example makes a universal strictly-positive marginal-gap assumption false. It is reported as a project scope objection, not as a previously published novelty result or a new simulation performed here. A strict-gap prefix theorem can remain correct while being inapplicable to an important symmetric limit.

Without a gap, arbitrarily small probability perturbations can change a ranking. Exact-probability prefix order can therefore still depend on the graph even while full-output TV goes to zero. Finite-shot resolution, deterministic tie rules and graph-aware scoring must be treated explicitly. A graph-aware decoder still has the supplied graph and can obtain all its useful information classically; raw-state closeness alone does not bound that full hybrid algorithm's performance.

## Adjacent photonic sources and unverified leads

- Łukasz Grodzki, Mateusz Slysz and Grzegorz Waligóra, *Solving the Portfolio Optimization Problem on a Photonic Quantum Computer*, **Entropy 28(7), 717 (2026)**, published 2026-06-23, [DOI 10.3390/e28070717](https://doi.org/10.3390/e28070717). Sec. 2.3.2 explicitly compares classical and BBS methods using objective-evaluation budgets rather than iteration counts; its optical/bit-flip variational construction is not the static min–max ObliQ anchor. This is **partial or adjacent result only**, not an exact washout theorem.
- The [MerLin reproduced-papers repository](https://github.com/merlinquantum/reproduced_papers) advertises an ObliQ reproduction with an ancilla extension for nonconstant diagonals and BBS classical-source ablations. Its top-level README was read as a primary statement of that software project's scope. The ObliQ subdirectory fetch was blocked and no immutable commit/source-level washout theorem was authenticated. Its reported benchmark conclusions are not adopted as verified evidence here.
- Verma–Lewis, *Penalty and partitioning techniques to improve performance of QUBO solvers*, [DOI 10.1016/j.disopt.2020.100594](https://doi.org/10.1016/j.disopt.2020.100594), **Discrete Optimization 44, 100594 (2022)**, with online-first records from 2020: discovered through primary abstracts and citation chains; full publisher access returned 403. Exact theorem details remain **unverified** in this pass.
- Jiajie Liu and Alberto Moraglio, *Penalty Sensitivity in Quantum Optimisation Across Computational Paradigms: A Benchmark Study*, [DOI 10.1145/3795101.3814661](https://doi.org/10.1145/3795101.3814661), **GECCO Companion 2026, pp. 1631–1634**: independent-index discovery flags a balanced-Max-Cut benchmark close to the task; ACM full text returned 403. The full abstract was retrieved through the scholarly index and describes simulated gate-based, annealing and classical comparisons, but that is not primary full-text authentication. Its exact architecture and conclusions remain **unverified**, and the close task overlap cannot yet be dismissed.
- Hoeffding's 1963 bounded-sum paper was located through its [primary DOI](https://doi.org/10.1080/01621459.1963.10500830). The institutional PDF endpoint returned a bot block and another PDF lacked extractable text. No exact theorem-number-dependent implication is based on that inaccessible text here.

These access gaps are unresolved source questions, not evidence in favor of originality.

## Search protocol, authentication and coverage limits

Two discovery strategies were actually executed:

1. Exact/synonym web searches with primary full-text follow-through and backward citation tracing: QUBO penalty magnitude, global rescaling, min–max normalization, objective suppression, finite precision, optical/photonic penalties, static anchors, square-root angle response and measurement/sample cost.
2. A separate SciSpace scholarly-index query: `photonic QUBO penalty normalization graph information washout ObliQ static anchor sampling complexity`. It retrieved ObliQ, adjacent photonic solvers, penalty-weight theory and the 2026 balanced-Max-Cut penalty-sensitivity lead. Index summaries and inconsistent bibliographic dates were used only for discovery; primary versions control the report.

Representative exact web queries included:

- `"ObliQ" "normalization" "coefficient"`
- `QUBO penalty coefficient normalization dynamic range objective suppression quantum annealing precision penalty weights`
- `"quadratic penalty" "normalization" "original objective" quantum annealing augmented Lagrangian`
- `"photonic" "QUBO" "penalty" "dynamic range"`
- `"ObliQ" "washout" OR "precision" OR "large penalty"`
- `"QUBO" "normalized" "shot complexity" penalty`
- `"Scalable determination of penalization weights" arxiv`

Exact-source verification then checked the strongest candidates' own versions, section/theorem labels, conventions and hypotheses. The project-local literature cache was queried read-only and was absent. Existing authenticated ObliQ PDF/archive/legacy-BS files were reused from `/private/tmp`; no additional source-cache files or tracked copies of fetched full texts were created. New web-read sources have stable primary URLs/version labels above, but no locally retained content hash is claimed for them.

Scope: English-language material discoverable through the web/arXiv, publisher and author/institutional sites, original software deposits and SciSpace, through **2026-11-21**. Backward references were followed for generic penalty and state-discrimination machinery. There was no complete Scopus/Web of Science/MathSciNet or Google Scholar citation census, no exhaustive forward-citation graph, no private/unpublished-source access, and no complete software-repository history review. The same reviewer performed both search strategies. This is a bounded adversarial audit, not a theorem of global priority.

## Decision for the research program

Reject novelty wording centered on generic penalty dilution, inverse-square independent-copy discrimination, or "a positive gap stabilizes a ranking." Preserve those facts with correct attribution. Keep the **exact static-architecture specialization** as an OPEN candidate, with all current hypotheses, and keep any numerical/task evidence separate from that candidate's originality.

The remaining discriminators are substantive rather than cosmetic: authenticate the blocked closely related task study; compare the literal archive to the explicitly corrected/control encodings; establish whether the exact asymptotic mechanism affects useful bisection output at penalties and sample budgets that matter; and determine what survives a graph-aware decoder and strong feasible classical search. A merely correct limit plus standard inequalities does not by itself satisfy the requested nontrivial scientific-result gate.
