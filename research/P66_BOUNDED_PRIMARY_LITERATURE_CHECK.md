# P66 bounded primary literature check

Date checked: 2026-11-25. Report prepared before reading any P66 author proof. Base: `58c95e0270c4b0a28c0982a9e9a622219239dbce`, branch `research/p65-independent-audit`. This is a bounded attribution and applicability check, not a correctness certificate or a novelty certificate. The `mathbox:literature-check` workflow was applied.

## Question and conclusion

The supplied inquiry concerns two regular blocks of size $2L$, uniform rank-one interblock coupling, and a passive bosonic unitary preserving each block's dark occupations. A collision-free input has $L$ photons in each block; success puts all $2L$ photons in one block. The proposed estimate is

\[
p_{\mathrm{good}}\leq 2a_Lb_L,\qquad
a_L=\frac{L!}{(2L)^L},\qquad
b_L=\frac{L+1}{2}\left(\frac{L+1}{2L}\right)^L,
\]

with exponential scale polynomial times $(4e)^{-L}$. The inquiry also specifies a connected weighted construction using four heavy cliques, a matching and weak complete bipartite edges, a strict bad local warm start, and a classical comparator examining six clique unions. These are project statements supplied for comparison; none is verified here.

**Conclusion: partial or adjacent result only.** The three checked papers establish relevant symmetry selection rules, finite bosonic counting moments, and a scoped quantum-proposal MCMC obstruction. They do not supply the complete P66 implication or its stated graph/comparator construction. Priority and novelty remain **OPEN**. Failure to locate the composition in this small search is not evidence of global novelty.

## Authenticated primary sources and exact applicability

### S1 — photonic symmetry selection rules

Christoph Dittel, Gabriel Dufour, Mattia Walschaers, Gregor Weihs, Andreas Buchleitner and Robert Keil, *Totally Destructive Interference for Permutation-Symmetric Many-Particle States*, **arXiv:1801.07019v2**, revised **18 June 2018**; *Physical Review A* **97**, 062116 (2018), DOI `10.1103/PhysRevA.97.062116`. [Version metadata](https://arxiv.org/abs/1801.07019v2); [primary text](https://arxiv.org/html/1801.07019v2).

Section II.2, equations (10)–(13), assumes a permutation-invariant input occupation and constructs scattering matrices from the permutation's eigenvectors, with diagonal input/output phases. Section II.4.1, equation (19), proves that an indistinguishable-boson output vanishes when the product of its assigned permutation eigenvalues differs from one. This is a sufficient suppression condition. Their $U_{jk}$ runs from input $j$ to output $k$; transpose it for the convention $U_{\mathrm{out},\mathrm{in}}$. Their particle/mode counts must also be distinguished from P66's $L$.

**Extraction verified; direct P66 application conditional.** Graph-automorphism commutation is a different hypothesis from this eigenbasis construction; P66's chosen collision-free input need not have the required permutation invariance. This paper does not establish the proposed nonzero tail bound or optimization construction. Overlap: **partial or adjacent result only**.

### S2 — finite bosonic bin-counting moments

Malaquias Correa Anguita, Anita Camillini, Sara Marzban, Marco Robbio, Benoit Seron, Leonardo Novo and Jelmer J. Renema, *Experimental validation of boson sampling using detector binning*, **arXiv:2502.05093v1**, **7 February 2025**. [Version metadata](https://arxiv.org/abs/2502.05093v1); [primary text](https://arxiv.org/html/2502.05093v1).

Appendices A–B, equations (27)–(34), treat distinct occupied input modes in lossless linear optics. For a bin, set $H_{ij}=\sum_{k\in\mathrm{bin}}U_{ki}^{*}U_{kj}$, restricted to occupied inputs, and let $X$ be the distinguishability Gram matrix. The coefficient of $(e^{iy}-1)^a$ in the count characteristic function is the sum of principal $a$-mode permanents of $H\odot X$. For ideal bosons $X_{ij}=1$. Appendix F explains the single-output-mode dependence on row magnitudes.

**Extraction verified; moment translation conditional on the chosen bright-mode basis.** This supplies finite-input factorial-moment machinery, not an exact thermal law. It does not state $b_L$, the proposed product bound, dark conservation, or a graph escape theorem. Haar-averaged results elsewhere in the paper cannot substitute for a fixed-unitary bound. Overlap: **partial or adjacent result only**.

### S3 — a scoped quantum-proposal MCMC no-go

Alev Orfi and Dries Sels, *Bounding speedup of quantum-enhanced Markov chain Monte Carlo*, **arXiv:2403.03087v1**, **5 March 2024**. [Version metadata](https://arxiv.org/abs/2403.03087v1); [primary text](https://arxiv.org/html/2403.03087v1).

For $2^N$ spin configurations with unknown marked-state energy $H_c=-\alpha N|k\rangle\langle k|$, equations (13)–(16) bound the reversible Metropolis–Hastings gap by

\[
\delta\leq\left((2^N-1)^{-1}+e^{-N\beta\alpha}\right)
\sum_{x\ne k}Q(k|x)A(k|x).
\]

Measured unitary or unital-channel proposals have the sum at most one. At fixed $\beta\alpha>\log 2$, this precludes better gap scaling than uniform classical proposals. The argument before (16) calls measured-unitary proposals symmetric; that is false for arbitrary unitaries. Double stochasticity and $A\leq1$ suffice for the displayed capacity bound, without that assertion.

**Extraction verified; direct P66 application inapplicable without another argument.** This is an unstructured marked-state Gibbs mixing obstruction, not a theorem about structured graph optimization from a specified warm start. Its conclusion explicitly leaves structured problems open. Overlap: **partial or adjacent result only**.

## Project-side bridges still requiring proof

These comparisons are deductions about the inquiry's hypotheses, not statements attributed to the papers.

1. **Dark-sector conservation.** Rank-one uniform cross coupling alone must be combined with within-block preservation of the uniform vector and its orthogonal complement. The resulting one-particle invariant subspaces then need their stated passive Fock-space lift. S1's output cancellation law is not a substitute for this conservation argument.
2. **The quantitative tail.** S2 identifies an appropriate finite-input counting language. A derivation must still identify the relevant input projection, normalize it, derive the bright-occupation estimate and combine them to obtain exactly $2a_Lb_L$. No independence of those events or exact thermal distribution has been supplied by a citation here.
3. **The optimization separation.** The graph's regularity, connectivity, strict local warm-start claim, characterization of success and cost of the six-union comparator remain project obligations. Neither a suppression identity nor a global Gibbs mixing gap directly establishes finite-shot optimization failure under a specified cost model.
4. **Adaptive and cost scope.** A repeated-attempt conclusion requires a valid conditional bound for each allowed history and encoding, together with explicit shot and classical costs. A fixed-kernel statement does not automatically cover current-dependent encodings or changing proposals.

## Stronger exact-covariance extension: hypothesis dictionary

The proposed extension uses a deterministic, graph-only one-particle rule with exact relabel covariance,

\[
U(PGP^T)=P\,U(G)\,P^T.
\]

For $P\in\operatorname{Aut}(G)$, this gives $PU(G)=U(G)P$. If each block has a transitive automorphism subgroup acting independently and fixing every other block, averaging that subgroup gives the block projector $P_b=|u_b\rangle\langle u_b|$, with $u_b$ uniform and normalized. Commutation forces every cross block to satisfy

\[
U_{ab}=P_aU_{ab}P_b\quad(a\ne b),
\]

so its rank is at most one, and the within-block dark complements are invariant. This is the elementary group-averaging/commutant ingredient, not a priority claim. No representation-theory source was authenticated in this three-paper check; no citation is being offered as verification of the whole extension.

The assumptions must remain exact. Covariance **in law** does not imply that every realized matrix commutes with the automorphisms. A rule $U(G,S)$ depending on the current state is constrained by the joint stabilizer of $(G,S)$, which can be smaller than $\operatorname{Aut}(G)$. Simultaneous transitivity in several blocks is weaker than independently acting transitive subgroups: a matching can intertwine simultaneous actions while retaining higher-rank cross coupling. Whether the particular connected graph construction has the needed independent subgroups has not been checked. Even if this structural bridge holds, the quantitative probability and optimization bounds still require separate proof.

## Search boundary, authentication and retention

The bounded search used a general web index for discovery, then exact-version arXiv metadata and primary full text for extraction. Six queries were used:

- `bosonic suppression laws arbitrary unitary symmetry eigenmodes Dittel Dufour 2018 arxiv dark states`
- `quantum enhanced Markov chain Monte Carlo no advantage no go mixing time 2025 2026 arxiv`
- `boson bunching probability all photons subset modes bright dark collective mode occupation moment bound`
- `Dittel Dufour symmetry suppression laws 2018 arxiv many particle interference eigenvalue`
- `Shchesnovich generalized bunching probability subset modes permanent 2016 arxiv`
- `"Bounding speedup of quantum-enhanced Markov chain Monte Carlo" theorem unital bottleneck`

Only the three primary versions above were authenticated and extracted. Related suppression, generalized bunching and quench papers found through discovery were not used as theorem evidence. Coverage is English photonic permutation symmetry, bin-count moments and quantum-proposal MCMC bottlenecks, checked on 2026-11-25; it is not an exhaustive search across representation theory, optical dark modes, probability tails or all citation descendants. There was no independent second literature reviewer. No “apparently new” label is claimed.

The established alternate project cache was queried by identifiers and authors; no matching retained record was found there. No new PDF, source text or cache record was retained because this task authorizes only this report file. Accordingly there is **no retained-source SHA-256** to report. Exact arXiv versions and formula locators above pin the consulted sources; arXiv version history, rather than an HTML rendering date, supplies revision dates. No `.mathbox` evidence or research-state status was written. No P66 proof, graph data, scientific code, test, simulation, native backend or QPU was opened or run.

The verified source results are attributable ingredients. The proposed P66 composition, its stronger covariance formulation, and any publication-level novelty claim remain **OPEN** under this bounded check.
