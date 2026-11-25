# P75 Gaussian collision-free overlap route

25 November 2026. Static proof/counterexample checkpoint, worktree base 8df6dd87e338cc06a6844e2508142351f418b03a. Only this note is written. No scientific import, AST parse, numerical evaluation, optimization, test, random draw, physical sampling, backend or QPU operation was executed. No other P75 agent's mathematical proof or verdict was read. A source-only delegate authenticated one paper; no mathematical P75 derivation was delegated or received.

**Global conjecture status: incomplete, with the first missing case at $k=6$.** The universal proposed bound is proved here for $k=2$ and $k=4$, with arbitrary complex symmetric pair matrices, arbitrary diagonals and any number of auxiliary modes required to be vacuum at output. It is sharp. The analogous Frobenius-norm lemma at $k=6$ is false, but its counterexample does not violate the proposed probability bound. No physical counterexample to the global conjecture has been established here. Bounded literature search without a match is not proof or novelty evidence.

## 1. Exact class and normalization

The candidate concerns a finite number $m$ of modes in a pure, zero-displacement Gaussian state. Its pair matrix is $Z=Z^T\in\mathbb C^{m\times m}$ with $\|Z\|_{\rm op}<1$. Write

\[
|\psi_Z\rangle=\det(I-ZZ^\dagger)^{1/4}
\exp\!\left(\frac12\sum_{ij}Z_{ij}a_i^\dagger a_j^\dagger\right)|0\rangle.
\]

Takagi factorization reduces normalization to independent one-mode pair exponentials. For a one-mode pair parameter $s$ the squared unnormalized norm is

\[
\sum_{n\ge0}\frac{(2n)!}{4^n(n!)^2}|s|^{2n}
=(1-|s|^2)^{-1/2}.
\]

Multiplication over modes gives the displayed determinant factor. Thus the state is physically normalized at finite squeezing.

For a specified set $S$ of $k$ distinct modes, the event is **one photon in every mode of $S$ and vacuum in every other mode**. Expanding the creation exponential gives one product per perfect matching, so

\[
q_Z(S)=\sqrt{\det(I-ZZ^\dagger)}\,|\operatorname{haf}(Z_{SS})|^2.
\]

All Fock occupation factorials are one. This is one Gaussian state's unconditional complete-count probability, not the product of two colored source probabilities, a threshold-click probability or a conditional CF law.

The conjecture is $q_Z(S)\le2^{-k}$ for even $k$. Odd $k$ has probability zero by total parity. $k=0$ is the vacuum event, bounded by one. Mixed Gaussian states, displacement, tracing out unobserved modes or bunched target occupations are not silently included.

## 2. Vacuum auxiliaries cannot increase this probability

Partition $Z=\left(\begin{smallmatrix}A&B\\B^T&C\end{smallmatrix}\right)$ according to $S$ and its complement, and put $M=I-ZZ^\dagger>0$. Then

\[
M_{SS}=I-AA^\dagger-BB^\dagger\preceq I-AA^\dagger,\qquad
0<M_{S^cS^c}\preceq I.
\]

The Schur complement is positive and no larger than $M_{S^cS^c}$. Consequently

\[
\det M
=\det M_{SS}\det(M_{S^cS^c}-M_{S^cS}M_{SS}^{-1}M_{SS^c})
\le\det M_{SS}\det M_{S^cS^c}
\le\det(I-AA^\dagger).
\]

Determinant monotonicity here follows by conjugating two ordered positive matrices with the inverse square root of the larger one; all resulting eigenvalues are at most one. The empty auxiliary block has determinant one. Also $\|A\|<1$ by compression.

The hafnian is unchanged, so $q_Z(S)\le q_A(\{1,\ldots,k\})$. Equivalently, projection of all auxiliary modes onto vacuum gives an unnormalized Gaussian state with pair matrix $A$; its vacuum-herald probability is at most one. No division by that probability is performed. It suffices to prove the conjecture on exactly $k$ modes; uncoupled vacuum auxiliaries preserve equality.

## 3. Sharp theorem for $k=2$

Let $A=\left(\begin{smallmatrix}a&c\\c&b\end{smallmatrix}\right)$ and $x=|c|^2<1$. The two positive diagonal entries of $I-AA^\dagger$ are $1-x-|a|^2$ and $1-x-|b|^2$. Its determinant is their product minus a nonnegative squared off-diagonal magnitude, hence

\[
\det(I-AA^\dagger)\le(1-x)^2,\qquad
q_A=x\sqrt{\det(I-AA^\dagger)}
\le x(1-x)\le\frac14.
\]

Equality occurs at $a=b=0$, $|c|^2=1/2$. This is a normalized two-mode squeezed vacuum with raw probability $1/4$ of the specified $|1,1\rangle$ outcome. Section 2 proves the same bound with any vacuum auxiliaries.

## 4. Sharp theorem for $k=4$

Now let $A$ be any complex symmetric $4\times4$ contraction, with arbitrary diagonal. Set

\[
T=\operatorname{Tr}(AA^\dagger)=\sum_{i=1}^4s_i^2<4,\qquad x=T/4,
\]

where $s_i$ are its singular values. The exact hafnian and elementary triangle/arithmetic--geometric mean inequalities give

\[
\begin{aligned}
|\operatorname{haf}A|
&=|a_{12}a_{34}+a_{13}a_{24}+a_{14}a_{23}|\\
&\le\frac12\sum_{i<j}|a_{ij}|^2
\le\frac14\|A\|_F^2=x.
\end{aligned}
\]

The factor $1/4$ is correct: the six unique off-diagonal entries are counted twice in $\|A\|_F^2$, while its diagonal terms are nonnegative. Independently,

\[
\sqrt{\det(I-AA^\dagger)}
=\left(\prod_{i=1}^4(1-s_i^2)\right)^{1/2}
\le(1-T/4)^2=(1-x)^2.
\]

Thus, for the full complex class,

\[
\boxed{q_A\le x^2(1-x)^2\le1/16.}
\]

Together with section 2 this proves the $k=4$ bound for arbitrary $m\ge4$, including all complex phases, nonzero diagonal entries and entanglement with vacuum-tested auxiliaries. No numerical search is needed to settle that class.

For every even $k$, disjoint two-mode squeezed pairs with off-diagonal pair parameter $1/\sqrt2$ attain $2^{-k}$ on the all-single-photon event. Each pair has probability $1/4$, and its singular values are strictly below one. In particular this supplies equality for the proved $k=2,4$ cases. It is a lower construction for the general conjecture, not a general upper proof.

## 5. A failed $k=6$ extension, preserved explicitly

The tempting analogue

\[
|\operatorname{haf}A|\stackrel{?}{\le}
(\operatorname{Tr}(AA^\dagger)/6)^{3/2}
\]

is false. For $A=t(J_6-I_6)$, $0<t<1/5$, the eigenvalues are $5t,-t,\ldots,-t$, so the matrix is a physical real nonnegative zero-diagonal contraction. But

\[
\operatorname{haf}A=15t^3,\quad
\operatorname{Tr}(AA^\dagger)=30t^2,\quad
(30t^2/6)^{3/2}=5\sqrt5\,t^3<15t^3.
\]

The strict inequality follows by squaring $3>\sqrt5$. Therefore the short Frobenius proof cannot be reused unchanged for six photons.

This is **not** a counterexample to the desired raw probability inequality. For the very same family,

\[
q_A=225t^6\sqrt{(1-25t^2)(1-t^2)^5}
\le\frac{225}{5^6}=\frac9{625}<\frac1{64},
\]

where $9\cdot64<625$. The determinant normalization must not be discarded when interpreting a candidate matrix.

Two further six-mode families also fail to falsify the probability bound analytically:

- Rank one, $A=suu^T$, $\|u\|=1$, $|s|<1$: $\operatorname{haf}A=15s^3\prod_i u_i$ and $\prod_i|u_i|^2\le6^{-6}$, so $q_A\le225/6^6=25/5184<1/64$.
- Isotropic bipartite, $A=s\left(\begin{smallmatrix}0&V\\V^T&0\end{smallmatrix}\right)$ with unitary $V$ of size three: $q_A=|s|^6(1-|s|^2)^3|\operatorname{perm}V|^2\le1/64$. Here $|\operatorname{perm}V|\le1$ is the normalized three-photon CF transition-amplitude bound for a passive unitary; the scalar factor is $[y(1-y)]^3\le4^{-3}$. Permutation $V$ and $|s|^2=1/2$ attain equality.

These are nonexhaustive families. They do not settle a general complex six-mode pair matrix.

The CF condition is essential: a two-mode squeezed vacuum at $|s|^2=2/3$ has raw probability $(1-|s|^2)|s|^4=4/27>1/16$ for the bunched four-photon pattern $(2,2)$. That event is outside the conjecture and is not counted as its refutation.

## 6. Bounded primary literature check

Exactly three primary publications were authenticated, checked on 25 November 2026. Discovery used Gaussian-fidelity/Fock-overlap queries and a separate hafnian-norm/extrema strategy. No worldwide novelty or completeness claim is made.

1. O. Hahn, R. Takagi, G. Ferrini and H. Yamasaki, *Classical simulation and quantum resource theory of non-Gaussian optics*, Quantum 9, 1881 (13 October 2025), DOI 10.22331/q-2025-10-13-1881. Exact text: [arXiv:2404.07115v5](https://arxiv.org/html/2404.07115v5), 25 February 2026; the [publisher](https://quantum-journal.org/papers/q-2025-10-13-1881/) records the update. Section 6.1 before (119) expressly treats $1/4$ for $|1,1\rangle$ as a numerical lower bound without proved optimality. Appendix H, (327)–(335), optimizes a pure Gaussian family allowing displacement; the found candidate has zero displacement. This supports nonmultiplicativity in the broader Gaussian class, not an all-$k$ upper bound. The Chalmers PDF initially discovered is older v4. Implication for the conjecture: **unverified**; overlap: **partial or adjacent result only**.

2. U. Chabaud, G. Roeland, M. Walschaers, F. Grosshans, V. Parigi, D. Markham and N. Treps, *Erratum: Certification of Non-Gaussian States with Operational Measurements*, PRX Quantum 6, 010902, published 25 March 2025, [DOI and primary PDF](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.6.010902). The one-page erratum changes the earlier numerical value 0.342 to 0.25 in F13/F21 and the figure. Its corrected equation (1) states the two-mode $|1,1\rangle$ supremum for the stellar-rank-zero class; the caption permits displaced Gaussian factors. This correction is important numerical provenance, not a proof of the present arbitrary-even-$k$ zero-displacement inequality. No analytic optimality proof is supplied in the erratum itself. The original paper was not additionally authenticated in this bounded three-publication check. Implication for the global conjecture: **unverified**; overlap: **partial or adjacent result only**.

3. Youngrong Lim and Changhun Oh, *Approximating outcome probabilities of linear optical circuits*, npj Quantum Information 9, 124 (16 December 2023), DOI 10.1038/s41534-023-00791-9. Exact primary text read: [arXiv:2211.07184v2](https://arxiv.org/html/2211.07184v2), revised 17 December 2023; [version metadata](https://arxiv.org/abs/2211.07184v2). Section IV.3.1 gives the all-single-photon pure-squeezed hafnian probability and Theorem 1's additive-error estimator. Appendix C.2 concerns structured squeezed-thermal block matrices under its classicality restrictions; Table 2 leaves the general $|\operatorname{haf}R|^2$ upper-bound entry unspecified. Neither that estimator nor the structured mixed-state bounds establish the desired determinant-weighted pure-state extremum. Implication for the probability formula: **verified after notation translation**; implication for the conjectured universal upper bound: **unverified**; overlap: **partial or adjacent result only**.

The project-local alternate cache was queried by the stable source identifiers and had no matching retained record. Only this report may be retained, so no PDF, copied primary full text or new cache record was written and no retained-source SHA-256 is claimed. Source versions and formula locators above identify the checked texts. No external extremal-fidelity assertion is used as a premise of the $k=2,4$ proofs.

## 7. Exact consequence for the P73 model and remaining obligation

The source/count definitions in P73 sections 1–2 specify two independent colored Gaussian sources, with one color occupying a prescribed $k$-subset and the other its complement, vacuum in the other modes, $N=2k$. Their raw probabilities multiply; each individual source carries a square-root determinant, while identical sources yield one determinant after multiplication.

For $k=2$ or $4$, even allowing different independently optimized complex pair matrices for the colors, the proved bounds give

\[
q(S)\le(2^{-k})^2=2^{-N}.
\]

Thus the finite-strength window is closed for the independent-color cases $N=4$ and $N=8$, for every physical finite source strength and encoding. The fresh uniform oriented balanced proposal has point mass $1/\binom{N}{N/2}>2^{-N}$, so every specified feasible outcome and every set of such outcomes has at least as much mass per classical feasible proposal as per raw Gaussian pulse. All Gaussian failed outcomes remain paid; this is not a claim about the conditional law or matched wall time.

For odd $k$, independent zero-displacement colors cannot emit the required odd photon number, as P73 already states. For general even $k\ge6$, the proposed all-$N$ conclusion is still open in this route.

A joint Gaussian source on all color modes is a different case: its accepted pattern has $N$ distinct single photons, so it requires the **one-source theorem at $k=N$**. The $k=4$ result covers a joint total-four-photon source, not a joint total-eight-photon source. It must not be squared to cover the latter.

The first missing implication is now precise: prove, or refute by a physical normalized complex symmetric contraction $B$ of size six,

\[
\sqrt{\det(I-BB^\dagger)}\,|\operatorname{haf}B|^2\le1/64.
\]

A strict counterexample would require positive definite $I-BB^\dagger$ and exact or certified strict violation, equivalently $\det(I-BB^\dagger)|\operatorname{haf}B|^4>1/4096$. A complex counterexample would refute the broad conjecture but would not automatically refute P73's real nonnegative zero-diagonal subclass.

No falsifier code or numerical contract is written here: the full $k=4$ class is already settled by proof. Any later six-mode scientific execution needs a separate prospective contract and authorization; a bounded search without finding a violation would not settle the inequality. The global conjecture and positive optimizer objective remain open.
