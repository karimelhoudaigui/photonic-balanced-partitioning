# P78 bounded primary literature check

26 November 2026. **Disposition: established loop-soup ingredients; a verified loop-side translation; adjacent photonic algorithms with different targets. No novelty certification.** The optical identification and the explicit cost theorem remain project claims to audit, not theorems quoted verbatim from these publications.

## Target and bounded protocol

All 183 lines of research/P78_nonnegative_Gaussian_even_loop_sampler.md were read at commit d42b4b3f37a28329a9d7f6d9b80cd03edea4c5bc, SHA-256

    118c88279e01bb13b81450b7f30c2cb55ad852e3a34cfcffbdc56c1c64df7c4a

The target is the complete raw PNR law for finite real symmetric entrywise nonnegative $Z$, $\|Z\|<1$, including diagonal entries, vacuum, collisions and unbounded photon number. The separate proposed work bound is expected proposed transitions at most $m\bar n$, with exact Perron data and ideal random primitives.

Exactly three publications were investigated. Official versioned arXiv abstracts, HTML and PDF text were used; the Springer catalog authenticated the book edition only. Sections and equation numbers below refer to the named preprints, not an assumed identical journal or book pagination. No secondary account supplies a mathematical implication.

The project-root literature-record directory was absent on a read-only identifier lookup. The Python cache helper was not invoked under the no-import/no-execution instruction. No PDF or full extracted text was retained; consequently there is no retained-source SHA. Le Jan HTML and PDF screenshot rendering were unavailable; its official PDF text was extracted. All quotations are avoided. Only this report is written; no ledger or manuscript is updated.

## S1 — Oh, Fefferman, Jiang and Quesada

[Quantum-inspired classical algorithm for graph problems by Gaussian boson sampling, arXiv:2302.00536v2](https://arxiv.org/abs/2302.00536v2), 23 April 2023; associated journal reference [PRX Quantum 5, 020341 (2024)](https://doi.org/10.1103/PRXQuantum.5.020341). Checked: [official HTML](https://arxiv.org/html/2302.00536v2), §II Eq. (1), §III pp. 3–4 Eqs. (3)–(11), §V pp. 7–8 Eqs. (15)–(20), and §VI Eq. (21).

Their constructive pair sampler yields a single hafnian weight, whereas the optical weight is its square. Section V normalizes within a fixed photon-number sector; its hypothetical distribution separations concern that particular classical control. Diagonal augmentation preserves distinct-vertex hafnians, not an arbitrary full repeated-occupation law. Section VI also gives the independent-pair Poisson law, again with a single hafnian. **Verified mismatch; partial or adjacent result only.** Neither pair construction is P78's exact full-PNR squared-hafnian law. The source identifies relevant classical controls, not a general nonnegative-GBS impossibility or matched-wall-time theorem.

## S2 — Zhang et al.

[Efficient Classical Sampling from Gaussian Boson Sampling Distributions on Unweighted Graphs, arXiv:2505.02445v2](https://arxiv.org/abs/2505.02445v2), 17 September 2025; associated [Nature Communications DOI](https://doi.org/10.1038/s41467-025-64442-7). Checked: [official PDF](https://arxiv.org/pdf/2505.02445v2), §II.A–C pp. 2–7; Supplementary Note 3B–E pp. 24–30; Note 4 pp. 30–32; cross-checked against [official HTML §II.1–3](https://arxiv.org/html/2505.02445v2).

Algorithm 2 has vertex-set stationary mass $\eta^{|S|}\operatorname{haf}(A_S)^2$; no repeated occupations. Theorems 4–5 state TV-error sampling bounds
$\widetilde O(m^2n^{15+2\xi}\log^2\epsilon^{-1})$ and
$\widetilde O(n^{20+2\xi}\log^3\epsilon^{-1})$:
constant missing-degree cap $\xi$, respectively $\delta_1\ge n-\xi,\delta_2\ge m-\xi$ or $\delta\ge2n-1-\xi$.
Main-text $\lambda>1/4$ conflicts with Supplementary Theorems S5/S6 requiring $\lambda>1/2$ and $\lambda>1/\sqrt6$; no weaker threshold is certified here. Note 3E exhibits exponential mixing, Eq. (S64), outside density guarantees. Note 4, Lemma S11/Eq. (S5), gives weighted stationarity with rescaled positive edge weights and a weighted inner sampler, not general weighted rapid mixing.

Notation caution: PDF Eqs. (8)–(9) print $c^{2|S|}$ despite $B=c\Delta$; hafnian homogeneity gives $c^{|S|}$ for vertex cardinality. Use independent fugacity $\eta$; do not copy that raw normalization. **Partial or adjacent result only:** collision-free conditional family at stationarity, not P78's full raw law; finite MCMC is approximate.

## S3 — Le Jan: authenticated ingredients and dictionary

Yves Le Jan, [Markov paths, loops and fields, arXiv:0808.2303v4](https://arxiv.org/abs/0808.2303v4), latest authenticated revision 10 September 2010. [Springer](https://link.springer.com/book/10.1007/978-3-642-21216-1) confirms 2011, LNM 2026; its body was not substituted for the [v4 PDF](https://arxiv.org/pdf/0808.2303v4).

Checked: finite transient reversible chain §1.2; rooted discrete-loop mass $\prod Q/k$, Eqs. (2.4)–(2.5), p. 21; Poisson functional Eq. (4.1), p. 43; continuous occupation determinant, Corollary 1, p. 44; discrete zeta determinant and Perron-normalized transition, §2.7 pp. 32–33; $h$-transform, Remark 10, p. 66. These are established results; jump counts are not continuous holding times.

**Project translation, not quoted theorem:** set
\[
K=\begin{pmatrix}0&Z\\Z&0\end{pmatrix},\quad
\widetilde D=\operatorname{diag}(D,D),\quad\alpha=\tfrac12.
\]
Here $D=\operatorname{diag}(z_i)$. On each nonzero component choose positive Perron vector $v$, $Kv=rv$, and $V=\operatorname{diag}(v)$. Then $Q=V^{-1}KV$ has row sum $r<1$ and preserves cyclic products. Source conductances are $v_uK_{uv}v_v$, holding weights $v_u^2$, killing $(1-r)v_u^2$; zero blocks contribute vacuum. The doubled $K$ has zero diagonal even with diagonal $Z$.

The loop PGF becomes
\[
\left[\frac{\det(I-K)}{\det(I-\widetilde D K)}\right]^{1/2}
=\left[\frac{\det(I-Z^2)}{\det(I-(DZ)^2)}\right]^{1/2}.
\]
Each projected even rooted walk has two lifts; $2\alpha=1$, retaining its $1/(2\ell)$ weight. No orbit divisor is added. **Verified; formal corollary not stated optically.**

## Application disposition and remaining boundaries

| P78 arrow | Bounded source conclusion |
|---|---|
| Positive even-loop representation | The loop side is a Le Jan corollary under the displayed dictionary; it should be attributed accordingly. |
| Optical full-PNR PGF equals that loop PGF | The equality is the project's optical-to-probability bridge. This literature check identifies its exact external loop law; it does not replace the independent P78 proof audit. |
| Perron change of measure | Known after translation of notation. P78's particular Poisson/logarithmic-length rejection construction is an explicit project specialization. |
| Expected proposed transitions $\le m\bar n$ | No such photon-number cost statement was extracted from these sources. Attribution of that bound as an existing theorem remains unverified; it requires its own derivation. |
| Efficient CF-conditioned sampler | Does not follow from a raw sampler. Rare-event rejection and all failures remain paid. |
| Finite-bit or matched physical cost | Not supplied by ideal exact-real primitives or a stationary-distribution identity. Perron preprocessing, precision/TV control and actual resource ledgers remain separate. |

The full-count object cannot be replaced by a normalized distribution over subsets, by an IPS pair law, or by a continuous occupation-time field. P78's restriction is on the fixed output pair matrix; nonnegative graph input alone does not guarantee that restriction after an arbitrary later interferometer.

This was an attribution/overlap check of the three named publications, with one official book-catalog query and targeted section extraction. No broader citation graph, forward-citation survey, alternative-language search or independent second literature pass was performed. A failed exact-phrase query supplies no novelty evidence. The loop ingredients are established; publication priority for the optical specialization or cost formulation is **unresolved within this bounded check**, with no “apparently new” designation.

The candidate remains unmodified. No scientific code, import, AST, test, RNG, numerical probability, backend or QPU call was used; no P75 experimental output or other P78 derivation/verdict was read. This report supplies source comparison, not a positive optimizer result or experiment authorization.
