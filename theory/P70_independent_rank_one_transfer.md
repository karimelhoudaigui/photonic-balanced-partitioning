# P70 independent derivation: selected-clique rank-one transfer

25 November 2026. Static derivation at worktree base 0804f6c268a376026d8db8c9eb6911d63ee46048. The target is the coordinator's prospective P70 claim, supplied with a suggested rank-one conditioning argument. No P70 author file, author proof or separate review verdict was read. The proof-audit skill was applied; no import, numerical calculation, test, experiment, literature query or hardware call was executed.

**Primary verdict: proved as written**, with the model and quantifiers normalized below. There is a strict raw-shot bosonic separation from every allowed distinguishable common-unitary proposal for $L\ge3$. The same uniform whole-clique move has a stronger elementary classical implementation. Consequently this mechanism fails the full positive optimizer gate. Neither a general optical advantage nor novelty is established.

## 1. Claim card

Let $L\ge2$. Use four disjoint size-$L$ cliques $A_1,A_2,B_1,B_2$, with heavy weight $M$, matching weight $h>0$ between the two A cliques and between the two B cliques, and $M(L-1)>Lh$. Put $C_A=A_1\cup A_2$, $C_B=B_1\cup B_2$. Cross-block edges have weight $w=0$ or $0<w<h/L$ and, when present, form the complete bipartite graph. The concrete choices $M=3,h=1,w=0$ or $1/(2L)$ satisfy these conditions.

The source is a freshly prepared normalized collision-free Fock state on a bad whole-clique subset, initially $S=A_1\cup B_1$. It contains $K=2L$ photons, one per occupied input mode. A good target is either $C_A$ or $C_B$, with one photon in every target mode. All probabilities are unconditional raw measurement probabilities. Collisions, rejected outputs and unfavorable optical-matrix choices are paid attempts; there is no collision-free denominator.

For B, conditionally on every preceding history, choose one occupied clique $X$ uniformly from two and one vacant clique $Y$ uniformly from two, independently. The same selected one-particle unitary acts on all photons, which are perfectly indistinguishable; evolution is ideal, passive and lossless.

For D, the $2L$ photons are labeled independent particles localized at those same distinct source vertices. A controller may choose any common one-particle unitary $V$, including a separately optimized, graph-informed, source-informed or history-dependent one. Each realized $V$ before the shot must have cross-block rank at most one between $C_A,C_B$. Mixtures of such realized matrices are allowed. A restriction only on an averaged matrix, separate per-photon unitaries, correlated output assignments or a different source is outside this comparison.

Rows label outputs and columns inputs. Define

\[
\alpha_L=\frac{L!}{L^L},\qquad
p_B=\frac{\alpha_L^2}{2},\qquad
q_D=\min\left(1,\frac{2L!}{L^{2L}}\right).
\]

The claimed probabilities are $P_B(\mathrm{good})=p_B$ and $P_D(\mathrm{good}\mid S,V)\le q_D$ uniformly over the D class. The ratio against its optimized probability is at least $L!/4$, strictly greater than one for $L\ge3$.

## 2. Unitarity and cross rank

For a clique $X$, put $b_X=L^{-1/2}\sum_{x\in X}|x\rangle$ and $P_X=|b_X\rangle\langle b_X|$. Distinct cliques have orthogonal bright vectors. Define

\[
U_{XY}=I-P_X-P_Y+
i|b_X\rangle\langle b_Y|+
i|b_Y\rangle\langle b_X|.
\]

The bright span of $b_X,b_Y$ and its orthogonal complement form a reducing decomposition. On the bright span the matrix is $\left(\begin{smallmatrix}0&i\\i&0\end{smallmatrix}\right)$, whose adjoint times itself is the identity; on the complement it is the identity. Thus $U_{XY}$ is unitary and symmetric. It is a passive, photon-number-preserving optical transformation.

For opposite-block $X,Y$, each directed cross block is one outer product and has rank one. For same-block $X,Y$, both cross blocks vanish. No preservation of the old full-block dark sectors is asserted: selecting one clique bright mode can mix a P66 block-dark sector. This matrix class is larger than the original P66 Cayley/dark-preserving family.

## 3. Fock amplitude, permanent and uniform mixture

Let $Z$ be the other occupied clique. The source is $X\cup Z$, and complete replacement gives $T=Y\cup Z$. Every mode of $Z$ is fixed, with no coupling to $X\cup Y$. The source-to-target submatrix is

\[
U_{XY}[Y\cup Z,X\cup Z]
=\begin{pmatrix}(i/L)J_L&0\\0&I_L\end{pmatrix}.
\]

Every source and target occupation is zero or one, so both Fock occupation-factorial products equal one. Expanding the product of transformed creation operators sums one product of matrix entries for each input-to-output bijection, which is the permanent. The normalized amplitude is therefore

\[
\langle1_{Y\cup Z}|\Gamma(U_{XY})|1_{X\cup Z}\rangle
=\operatorname{perm}((i/L)J_L)\operatorname{perm}(I_L)
=i^L\frac{L!}{L^L}.
\]

There is no extra $K!$ or $L!$ denominator. The raw complete-replacement probability is $\alpha_L^2$.

An independent normalization check uses the normalized bright state $(b_X^\dagger)^L|0\rangle/\sqrt{L!}$. Its overlap with $|1_X\rangle$ is $\sqrt{L!}\,L^{-L/2}=\sqrt{\alpha_L}$. Only this all-bright source sector can empty $X$, because the $X$ dark modes are fixed. Its transfer to the all-bright $Y$ state has phase $i^L$; overlap with $|1_Y\rangle$ supplies another $\sqrt{\alpha_L}$. The product amplitude is $i^L\alpha_L$, agreeing with the permanent.

Of the four equally paid $(X,Y)$ choices, exactly two are cross-block choices and their complete replacements are good. In either such choice, the untouched occupied clique $Z$ rules out the other good target. The two same-block choices preserve $L$ photons in each large block and cannot produce a good target. Therefore

\[
P_B(\mathrm{good})=\frac24\alpha_L^2
=\frac12\left(\frac{L!}{L^L}\right)^2.
\]

All collided outcomes and unsuccessful optical choices remain included in the attempt count. Conditioning on a cross-block choice would incorrectly remove the factor $1/2$.

## 4. Arbitrary independently optimized D

Fix any admissible common $V$ and consider target $C_A$. Write its cross block from $C_B$ as $C$. If $C=0$, this target has zero probability. Otherwise rank one and the contraction property of a unitary block give

\[
C=\sigma u v^\dagger,\quad
\|u\|=\|v\|=1,\quad 0<\sigma\le1.
\]

For input $j\in B_1$, the probability of landing anywhere in $C_A$ is $\sigma^2|v_j|^2$. Independence gives, for the event $E$ that all $L$ B-origin photons cross,

\[
P(E)=\sigma^{2L}\prod_{j\in B_1}|v_j|^2
\le\left(\frac{\sum_{j\in B_1}|v_j|^2}{L}\right)^L
\le L^{-L}.
\]

Zero factors already imply zero target probability. Otherwise, conditional on $E$, the B-origin landing modes are independent with the same distribution $p_i=|u_i|^2$ on $C_A$. Their column-dependent phases and weights cancel in conditioning.

For each size-$L$ subset $Y\subset C_A$, let $r_Y$ be the probability that the A-origin photons occupy exactly $Y$ without a collision. These events are disjoint, so $\sum_Yr_Y\le1$. They do not condition away A-origin infeasibility. The two labeled groups are independent given $V$, and conditioning on $E$ does not change the A-origin probabilities.

For the target to be fully occupied without collision, the B-origin photons must fill $X=C_A\setminus Y$, each mode once. The conditional probability is

\[
L!\prod_{i\in X}p_i
\le L!\left(\frac{\sum_{i\in X}p_i}{L}\right)^L
\le\frac{L!}{L^L}.
\]

Consequently, without any CF postselection,

\[
P_D(C_A\mid S,V)
=P(E)\sum_Yr_Y\,L!\prod_{i\in C_A\setminus Y}p_i
\le\frac{L!}{L^{2L}}.
\]

The same argument applies to $C_B$. A rank restriction on one directed cross block of a square partitioned unitary also restricts the reverse block: for $V=\left(\begin{smallmatrix}A&C\\B&D\end{smallmatrix}\right)$, unitarity gives $CC^\dagger=I-AA^\dagger$ and $B^\dagger B=I-A^\dagger A$. The two right sides have equal rank since $AA^\dagger,A^\dagger A$ have the same singular-value spectrum. Thus $\operatorname{rank}C=\operatorname{rank}B$.

The good targets are disjoint, so their probabilities add to at most $q_D$. Conditioning on the controller's realized matrix and then averaging proves the same bound for arbitrary mixtures and adaptive choices within this class. The argument assumes neither $V=U_{XY}$ nor uniform singular vectors nor identical A-origin output distributions.

The per-target constant is attainable: fix one cross-block bright swap and leave the other occupied clique untouched. Each labeled assignment of the transferred photons to the vacant clique has probability $L^{-2L}$; the $L!$ assignments are disjoint. The raw good probability is $L!/L^{2L}$. Attainability of the union upper bound is neither needed nor asserted.

## 5. Strict range and boundary

For $L\ge2$, $L!\le L^L$ and $2/L^L<1$, so $q_D=2L!/L^{2L}$ and

\[
\frac{p_B}{q_D}=\frac{L!}{4}.
\]

The optimized D probability is positive, by the fixed bright-swap witness, and at most $q_D$. Thus $p_B/\sup_VP_D(\mathrm{good})\ge L!/4$. Since $3!>4$ and factorials increase thereafter, the separation is strict for $L\ge3$.

At $L=2$, $\alpha_2=1/2$, $p_B=1/8$ and $q_D=1/4$. More decisively, the fixed cross-block D bright swap has raw probability $2!/2^4=1/8$, matching the uniform B mixture. The uniform B mixture therefore cannot strictly beat optimized D at this boundary; the D optimum could be larger than this witness. The loose union upper bound must not be treated as an achieved optimum. $L=1$ is outside the positive-gap graph hypotheses.

## 6. Zero-temperature chain and photon cost

The cost landscape supplies closure of the source class. A good whole-clique union has cost $4wL^2$ and a bad one has cost $2Lh+2wL^2$, with positive difference $2L(h-Lw)$. Every other balanced subset has at least two partial cliques: one partial clique would leave its cardinality nonzero modulo $L$. A partial clique containing $z$ selected vertices contributes $Mz(L-z)\ge M(L-1)$, so the heavy-edge cut is at least $2M(L-1)$. With $x$ selected vertices in $C_A$, its cross-block cut is $w[x^2+(2L-x)^2]\ge2wL^2$; matching cost is nonnegative. It therefore exceeds a bad union by at least

\[
g=2M(L-1)-2Lh>0.
\]

In particular the only strictly better balanced subsets are the two good targets.

For $U_{XY}$ the untouched $Z$ stays fully occupied. Any CF output consists of $Z$ plus $L$ distinct modes in $X\cup Y$. A partial selection in both cliques is strictly uphill and is rejected at zero temperature. Complete replacement is either a good cross-block move or an equal-cost same-block move; staying at $X$ is also unsuccessful. Collisions are self-loops. Under acceptance of every non-uphill feasible output, every unsuccessful history leaves the source in the four-element bad class.

With fresh conditional uniform choices and fresh Fock preparation, the improvement hazard is exactly $p_B$ after every such history. For the first improvement time $\tau_B$ in paid attempts,

\[
P(\tau_B>T)=(1-p_B)^T,\qquad
E[\tau_B]=p_B^{-1}=\frac{2}{\alpha_L^2}.
\]

Every attempt injects all $2L$ source photons, including those in $Z$. Therefore

\[
E[\text{injected photons until improvement}]
=2L\,E[\tau_B]=\frac{4L}{\alpha_L^2}.
\]

For stopping on success with a cap of $T$ attempts, actual expected photons are $2L[1-(1-p_B)^T]/p_B$. A stopped run is not charged an infinite continuation. No simulator, compilation or wall-time equivalence follows.

A D chain with the same bad start, collision self-loops, feasible-only updates and rejection of uphill moves also stays in this source class before success. Its conditional raw improvement hazard is at most $q_D$, even when each common matrix is independently optimized against history. Thus $P(\tau_D\le T)\le1-(1-q_D)^T$ and, for continued attempts, $E[\tau_D]\ge1/q_D$. For $L\ge3$, the B success probability exceeds this D upper envelope; the ratio of the D expected-attempt lower bound to the B expectation is $L!/4$. External restarts, extra candidate insertion, uphill acceptance or changed sources require a different argument.

## 7. Optimum-blind classical and unrestricted-D controls

Since $M>h>w$, the heavy-edge graph is exactly four disjoint size-$L$ cliques; identifying them uses only the input graph. Given the two occupied cliques, choose the same uniform occupied $X$ and vacant $Y$ and form

\[
S'=(S\setminus X)\cup Y.
\]

The result is always balanced and CF. The procedure does not identify good choices before selecting, query an optimum, use an optimum mask, or require the analytic block names $C_A,C_B$. Ordinary graph-cut evaluation suffices for zero-temperature acceptance. Among the four choices, two improve and two have equal cost. Hence

\[
p_{\rm classical}=\frac12,\qquad E[\tau_{\rm classical}]=2,\qquad
\frac{p_{\rm classical}}{p_B}
=\frac{E[\tau_B]}{E[\tau_{\rm classical}]}
=\alpha_L^{-2}.
\]

Heavy-clique identification and applying/evaluating the move have polynomial graph cost. The photonic construction already uses those same clique identities. This is an explicit comparator, not a measured runtime experiment, and it prevents a positive optimizer conclusion.

Unrestricted common-unitary D realizes this same move by a mode permutation exchanging $X,Y$ through any fixed bijection and fixing the other modes. Every labeled photon lands deterministically at its prescribed distinct output. The uniform mixture again has raw good probability $1/2$. For a cross-block choice the cross block has rank $L$, outside the rank-one restriction when $L\ge2$. No indistinguishability benefit is required for this implementation.

## 8. Obligations and remaining scope

| Obligation | Outcome | Exact scope |
|---|---|---|
| Unitarity and cross rank at most one | Passed | Each realized selected-clique matrix |
| Normalized Fock/permanent amplitude | Passed | Ideal indistinguishable CF source/target; no CF denominator |
| Two-of-four uniform mixture | Passed | All optical choices and collisions paid |
| Independently optimized D bound | Passed | Product labeled source and common realized rank-one unitary |
| Strict $L\ge3$ and $L=2$ boundary | Passed | No strict B superiority at $L=2$ |
| Chain closure and exact B hazard | Passed | Fresh conditional uniform choices and non-uphill feasible updates |
| Photon accounting | Passed | All $2L$ photons per attempt |
| Classical move and unrestricted-D permutation | Passed | Both have raw probability $1/2$ |
| Positive optimizer gate | Failed | Explicit stronger optimum-blind classical comparator |
| General advantage, measured runtime, QPU, novelty | Not addressed | None is established |

All load-bearing leaves are finite linear algebra, normalized Fock/permanent identities, independence in the specified labeled model, arithmetic--geometric mean and conditional probabilities, with their uses shown above. No external source or computational evidence is needed here. No shared ledger or research status was changed.

There is no remaining gap in the normalized restricted statement. The exact D union supremum is not identified and is unnecessary for the strict $L\ge3$ result. The strongest safe statement is a restricted bosonic transfer effect with an explicitly stronger optimum-blind classical control. Any later finite check would validate conventions only; it would neither repair the failed optimizer gate nor establish novelty. Such execution was not authorized or performed in this review.
