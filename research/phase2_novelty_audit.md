# Phase 2: bounded novelty and competitor audit

Base checkpoint: `99f82e367ef079e4d52f763d615476698727b739`.
Date checked: 2026-11-20. Owner: literature/theory agent. No manuscript edits,
competitor executions, QPU calls or novelty certification occurred.

## Current verdict

An original publishable result has **not** been established by this search.
The spatial-overlap certificate remains mathematically useful but its novelty
is OPEN. Its triangle/permanent mechanism is close to established interference
bounds. The exact Haar click-count law is already explicit in prior work.
The strongest next optimization question concerns photon-budget-aware encoding
choice and whether large penalty coefficients erase graph information from
the *authenticated* ObliQ anchor. Candidate proofs and falsifiable protocols
are in `theory/phase2_candidates.md`.

## Exact claims versus checked primary sources

| Project claim | Primary source and locator checked | Overlap classification | Safe interpretation |
|---|---|---|---|
| Haar-averaged Fock distribution is uniform on occupations | Arkhipov–Kuperberg, [1106.0849v1](https://arxiv.org/html/1106.0849v1), Prop. 1/Cor. 2; previous cycle authenticated | known after translation of notation | No new Haar twirl claim. |
| Haar probability of exactly c occupied modes is `binom(m,c)binom(N-1,c-1)/binom(m+N-1,N)` | Bouland et al., [2312.00286v2](https://arxiv.org/html/2312.00286v2), Sec. 4, Lemma 1 and Eq. (6), version 2025-03-19 | known verbatim | The count is already a theorem, including a direct stars-and-bars proof. |
| Dense click statistics concentrate near their mean | Same source, Sec. 4, discussion after Lemma 1 and Lemma 2 | known after translation of notation | A polynomial central-window probability alone is not a new photonic optimization theorem. |
| TV bound by permanent minus one of an overlap Gram matrix | Tichy, [1410.7687v3](https://arxiv.org/html/1410.7687v3), Sec. IV.2 Eq. (55), IV.4; 2015-02-18 | partial or adjacent result only | Its Gram matrix describes internal photon states; our B describes absolute spatial columns. Its L1 convention lacks our factor 1/2. No exact substitution was established. |
| Derangement coefficients express a permanent with uniform off-diagonal overlaps | Rodari et al., [PRX Quantum 6, 020340](https://journals.aps.org/prxquantum/pdf/10.1103/PRXQuantum.6.020340), Appendix D, Eqs. (D1)–(D3), published 2025 | partial or adjacent result only | Uniform internal distinguishability, not our arbitrary spatial B or its Frobenius envelope. Derangements in interference bounds are established machinery. |
| Occupation-list conversion to ordered outputs | Clifford–Clifford, [author manuscript](https://research-information.bris.ac.uk/files/142614302/Raphael_Clifford_The_Classical_Complexity_of_Boson_Sampling.pdf), Sec. 3, “Expanding the sample space” | known after translation of notation | The factorial conversion in our N1 proof is standard, although the resulting B bound was not found verbatim. |
| An exactly collisionless distinct-input sampler has disjoint supports | Direct project proof; general Fock factorial moments overlap Martinez–Font-Segura [2602.09894v1](https://arxiv.org/html/2602.09894v1), Sec. 3.6 Eq. (39) | formal corollary not stated | Standard moment expansion implies the characterization; no novelty certification. |
| Low collision probability alone does not uniformly suppress interference | Dilute boson-sampling literature already separates rare collisions from useful interference; project supplies an elementary explicit balanced spectator family | partial or adjacent result only | The general phenomenon is familiar; the particular balanced construction has no authenticated exact match in this bounded search. |
| Penalty-normalized anchor loses graph contrast for large lambda | Original ObliQ algorithm authenticated below; direct candidate derivation in phase2_candidates | no overlap classification assigned yet: OPEN | An implementation-specific mechanism may be a useful negative result, but generic penalty/precision tradeoffs are already known. |

The combinatorial lemma applies for all allowed integer m,N,c. The same
paper's complexity hardness theorem has additional mode-density and
conjectural hypotheses. Do not import a hardness conclusion into the `N=m`
threshold-bisection setting just because the click-count lemma applies.

## Major correction to the earlier competitor access gap

ObliQ's full primary paper and original software were acquired this cycle.
The prior report's full-text access limitation is superseded by the source
records in `research/optical_penalty_spec.md`; the earlier record is preserved.
The Rice PDF authenticates the paper's constant/zero-diagonal class and links
the Zenodo artifact. The archive confirms threshold decoding, `N=m` static
input, variable hybrid input and graph-aware classical prefix decoding.
It also exposes a paper/API beamsplitter-angle mismatch. Reproducing the
literal code and implementing the paper's intended two-mode identity are
different variants and must be named accordingly.

The original artifact is stronger evidence than the subsequently found
[MerLin reproduction repository](https://github.com/merlinquantum/reproduced_papers),
which advertises an extension to nonconstant diagonal matrices using an
ancilla mode. That repository was used only as a discovery pointer; its
extension and results were not audited and cannot authenticate our baseline.

## Searches performed and coverage limits

Two strategies were used: exact/synonym web discovery with primary-source
follow-through, and a SciSpace query spelling out the matrix
`B_ab=sum_i abs(U_ia U_ib)` and the requested TV/collision connection.
Queries included spatial overlap, absolute overlap, Bhattacharyya coefficient,
Gram matrix, exchange interference, disjoint support, collision probability,
Frobenius bound, derangements and MacMahon/cycle enumeration. Both strategies
returned Tichy and related internal-distinguishability work; no exact spatial
B certificate was authenticated. The cycle argument is elementary
permutation enumeration and may be a formal consequence of older permanent
inequalities. A failed exact-match search is not evidence of novelty.

For the new optical question, searches covered ObliQ penalty normalization,
photonic QUBO coefficient normalization, graph-information washout, photon
number/Hamming weight, cardinality and threshold optimization, and Haar
click distributions with loss. They identified the exact prior click-count
law, but no authenticated paper explicitly deriving the proposed
minimum-bisection penalty-anchor limit. Generic annealing literature already
warns that strong penalty terms reduce the relative scale of objective
coefficients; our candidate needs an exact optical theorem plus operational
evidence to add more than that standard observation.

Scope: English-language sources indexed through 2026-11-20; arXiv,
publisher sites, author repositories, original software deposits and one
SciSpace index. Citation chasing and prior permanent inequalities remain
incomplete. The same agent performed both discovery strategies. No global
novelty statement or “apparently new” label is authorized.

## Research-quality gates retained

An optical parameterization theorem is not an optimization improvement.
The decisive tests must evaluate bisection quality and success per attempt,
including classical prefix search, photons, loss and training cost. A QPU
study is justified only after a locked simulation prediction distinguishes
encodings or a failure mechanism at realistic operating parameters.
Confirming known click combinatorics or interference alone is insufficient.
