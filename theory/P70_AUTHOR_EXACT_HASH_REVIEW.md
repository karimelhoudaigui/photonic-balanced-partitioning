# P70 exact-hash author review

25 November 2026. **Primary verdict: proved as written.** This verdict covers the restricted raw-event separation, the zero-temperature repetition statement and the explicit failure of the positive optimizer gate, under the hypotheses below. No load-bearing correction is required.

## Exact source and reading coverage

- Author file: research/P70_rank_one_bosonic_transfer_and_classical_falsifier.md.
- Author commit: 55b208d08d961e03c15723055e29edea54f184d3.
- SHA-256 of the complete Git blob: c6a8a9bb5485c91b4c0800728444036626a44d70770c3b45e68e5daaf1a9e53e.
- Coverage: **all 260 raw lines, 1–260**, including every display, scope statement and final disposition.
- The author file was first read only after my independent derivation had been frozen at commit 17c3f5c644a55f6780c5d42d9c6740405dbe1219. That 194-line file, theory/P70_independent_rank_one_transfer.md, retains SHA-256 1770f84e02f58a9ac0e05ffdbce538b38662da48254d9659ebbfb0cbdc8631db.

The author source was obtained directly from the named commit; its blob hash matches the requested hash. The prior derivation was unchanged after this comparison. Independence here means derivation before reading the author proof; both reviewers received the coordinator's candidate and suggested conditional-fill route. It is not a claim of an unrelated search strategy or formal verification.

The proof-audit skill was applied, followed by proofread-math in review-only mode for the author source and self-review mode for this report. Only this review file was written. No science import, calculation, test, data audit, native query, experiment or new research route was executed.

## Checked implication chain

| Author lines | Obligation | Finding |
|---|---|---|
| 18–38 | Family, warm start and optimum-blind pair rule | Passed |
| 40–50 | Unitarity and realized cross rank | Passed |
| 65–101 | Normalized Fock amplitude, permanent and two-of-four mixture | Passed |
| 110–160 | Arbitrarily optimized common-unitary D bound | Passed |
| 164–190 | Strict range, same-circuit ratio and $L=2$ boundary | Passed |
| 194–219 | Same-pair classical control, zero-temperature hazards and paid photons | Passed |
| 224–232 | Higher-rank common-unitary D countercontrol | Passed |
| 169–174, 234–260 | Interpretation and absence of a total-resource advantage claim | Passed |

The dependency chain is: bright-swap unitarity → exact permanent → exact B probability; rank-one factorization → crossing bound → conditional distinct fill → uniform D bound; cost barrier → closure of the bad-state class → conditional hazards; feasible classical replacement and higher-rank permutation → rejection of the optimizer claim.

## Quantitative comparison with the prior derivation

The author's $a$ equals the prior proof's $\alpha_L=L!/L^L$, not the differently normalized full-block constant used in the earlier P66 argument.

On the two selected bright modes, $U_{XY}$ is $\left(\begin{smallmatrix}0&i\\i&0\end{smallmatrix}\right)$; every orthogonal mode is fixed. This establishes unitarity. Opposite-block choices have one outer product in each directed cross block; same-block choices have zero cross rank.

The untouched occupied clique contributes an identity factor. The nontrivial transfer block is $iJ_L/L$, hence the normalized CF amplitude is $i^L L!/L^L$. Both occupation-factorial products are one. The two bright overlaps each have amplitude $\sqrt{a}$; no physical projection or free preparation is used. Exactly two of the four uniform choices can reach a good target, giving

\[
p_B=\frac12a^2=\frac{(L!)^2}{2L^{2L}}.
\]

For arbitrary allowed D, a zero cross block already makes target CA impossible. Otherwise $C=\sigma uv^\dagger$, with unit singular vectors and $0<\sigma\le1$. All $L$ CB-origin photons must land in CA; their net crossing probability is at most $L^{-L}$. If any source crossing probability is zero, the target again has probability zero. Otherwise conditioning is legitimate and their landing modes are iid with probabilities $|u_i|^2$. For any distinct CA-origin occupied set, the CB-origin photons must fill its size-$L$ complement, with conditional probability at most $L!/L^L$. The CA-origin sets have disjoint, **unconditioned** probabilities summing to at most one. Multiplying and summing therefore gives

\[
P_D(C_A)\le\frac{L!}{L^{2L}},\qquad
P_D(C_A\text{ or }C_B)\le\min\left(1,\frac{2L!}{L^{2L}}\right).
\]

No A-origin collision or escape probability is divided out. This argument permits arbitrary within-block matrices and independent D optimization, not just the B parameters. Conditioning on each realized matrix extends it to mixtures and marked adaptive histories.

The reverse-cross-rank equality used at lines 151–152 was also checked independently: if the CA diagonal block is $A$, then $CC^\dagger=I-AA^\dagger$ and the reverse block satisfies $D^\dagger D=I-A^\dagger A$. These have equal rank. The P69 statement and its section-2 isometric-inclusion proof were read at the same author commit to check this cross-reference. No new verdict on the rest of P69 is asserted; P70 needs no further P69 theorem to establish its displayed D bound.

The comparison uses an **exact achieved B probability** and a uniform D upper bound, rather than comparing two upper bounds. Their ratio is $L!/4>1$ for $L\ge3$. For the same circuit and pair mixture, D instead has probability $L!/(2L^{2L})$, giving the stated ratio $L!$. The factor-four allowance for the universal D upper bound is correct; it is not asserted to be attained.

At $L=2$, B has probability $1/8$. A fixed cross-pair rank-one D bright swap also has probability $1/8$, so the author's refusal to claim strict superiority over optimized D at this boundary is necessary and correct. The D union optimum is not identified.

## Cost barrier, chain closure and countercontrols

The cost dependency agrees with the prior independent derivation. In the connected or disconnected family,

\[
C_{\rm good}=4wL^2,\quad C_{\rm bad}=2Lh+2wL^2,\quad
C_{\rm bad}-C_{\rm good}=2L(h-Lw)>0.
\]

Every other balanced subset has at least two partial cliques and costs at least $C_{\rm bad}+2M(L-1)-2Lh>C_{\rm bad}$. Thus partial CF outputs are rejected at zero temperature. Collisions self-loop; complete same-block replacements are neutral. Every unsuccessful history leaves a bad whole-clique source, so fresh conditional uniform pair choices give the displayed B and classical hazards. Continued B repetitions have expected attempts $2/a^2$ and expected injected photons $2L(2/a^2)=4L/a^2$. All $2L$ photons, including the untouched clique's photons, are charged on every attempt.

The classical replacement $(S\setminus X)\cup Y$ is always balanced and feasible. It uses exactly the same four uniform choices; two are good and two neutral. Its probability $1/2$ is obtained without inspecting whether a chosen pair is good, using an optimum mask or selecting a known solution. Its graph extraction, update and score remain paid classical operations. The separate stronger direct-optimum routine mentioned later receives only classical solver credit; its known solution is not credited as a photonic proposal.

The unrestricted D countercontrol is one common mode permutation exchanging the selected cliques. It maps the entire CF source to the classical candidate deterministically. Its opposite-block cross rank is $L$, and its uniform-mixture success probability is $1/2$. It is a valid countercontrol outside the rank-one class, not label-dependent different interferometers disguised as a common one.

These facts prove the stated rejection of this mechanism as a positive optimizer result. They do not supply a measured wall-time comparison or a theorem about all possible hardware cost models. The author's explicit exclusions of total-resource, general-graph, hardware, loss, source-readiness and novelty claims are appropriate.

## Necessary proof restrictions

The verdict retains the author's actual model:

- Strict B-versus-all-D separation is for $L\ge3$, with the stated $L=2$ exception.
- Each attempt starts from the specified fresh CF source with $L$ photons in each fixed logical block; the targets are complete full-block CF occupations.
- B is ideal passive lossless indistinguishable evolution. D is a labeled product source with independent propagation through a **common realized net unitary** of cross rank at most one. Bounds on a generator, individual layers or the averaged matrix do not replace this condition.
- Added modes, label-controlled different interferometers, correlated output assignments, changed decoders, retained collided Fock states, external restarts, extra candidate insertion or uphill acceptance change the model.
- The chain formulas use zero-temperature non-uphill acceptance, collision self-loops and fresh conditional uniform choices. Finite-temperature or arbitrary initialization claims are absent.
- The equality of optical photon counts supports the raw-event comparison only. Classical computation, optical compilation, source, detection and other costs have not been equated or measured.

The covariance-in-law sentence at lines 52–55 is consistent when graph and current subset are relabeled jointly. No pathwise exact covariance is needed. The realized net rank and source/target hypotheses match P69's statement, so its scope does not conflict with this particular achievable event.

## Mathematical proofreading, review-only

One nonblocking referent clarification is warranted at lines 176–177: “target submatrix” there means the **nontrivial $L\times L$ transfer block**. The complete $K\times K$ target submatrix also contains the untouched identity block and zero cross blocks, as lines 92–95 already specify. The formula following the sentence is correct because the identity permanent is one. This requires no change of coefficient, normalization, theorem hypothesis or proof argument.

At line 129, $S_B$ is naturally $S\cap C_B$; defining that notation explicitly would remove an implicit local abbreviation. Neither point is a load-bearing mathematical defect. No other objective notation, sign, factorial, index, range or display inconsistency was found.

Proofread scope: all 260 author lines and this report. Routine edits to author: none. Mathematical-token changes to author: none. Validation: static reading and metadata hash verification only; no build or test was run because this was an expressly static review. The exact-hash source and the independent 194-line derivation remain unchanged.

The restricted separation and the classical veto are supported. The positive optimization objective remains open, and this review adds no numerical or publication-novelty evidence.
