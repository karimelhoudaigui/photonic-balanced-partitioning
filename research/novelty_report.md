# Literature and novelty audit

Checked 2026-11-20 from base `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`.
**No novelty claim is authorized. PAPER_READY remains false.** This is a
bounded search, not a theorem of absence of prior work. Primary sources are
linked in `literature_matrix.csv`; no fetched paper text is copied into the repo.

## Decisive overlaps

1. Haar twirling and the exact CF counting ratio are **known after translation
   of notation**. Arkhipov–Kuperberg, [1106.0849v1](https://arxiv.org/html/1106.0849v1),
   Prop. 1, Cor. 2, and the formula following Theorem 3 explicitly establish
   the needed arrow. Published version pp. 2–4 checked too. The dense balanced
   asymptotic here is an elementary Stirling specialization, not evidence of novelty.
2. Hamming-weight-preserving minimum-bisection optimization is **known after
   translation of notation**. Hadfield et al., [1709.03489v2](https://arxiv.org/html/1709.03489v2),
   Appendix A.3.2, already specifies the feasible domain and ring XY mixer.
   This is a qubit method; its physical resource cost differs from passive bosons.
3. Variational photonic **minimum bisection with penalty QUBO and CVaR** is
   **partial or adjacent result only**, but especially close. Cazalis et al.,
   [2412.14783v1](https://arxiv.org/html/2412.14783v1), Example 1 and Sec. VI,
   use threshold-detected Gaussian input states, not the fixed-Fock input used
   here. The abstract page labels the submission 2024-12-19; the HTML body
   displays a 2026 date, so publication dating should use authenticated metadata,
   not that body date. No theorem from this source is needed by our proofs.
4. Training a photonic circuit while balancing target quality and postselection
   success is **partial or adjacent result only**. Chen–Zhang,
   [PRA 114, 022607 (2026)](https://doi.org/10.1103/93x9-y3y9), explicitly
   advertises this in its publisher abstract. Full method and exact loss were
   not extracted; do not claim our collision-aware objective is new based on
   this search.
5. Bosonic optimization plus classical bit flips is **partial or adjacent result
   only**. Makarovskiy et al., [2510.08274v1](https://arxiv.org/html/2510.08274v1),
   Sec. III.1, uses trainable bit flips to reach the full binary space with fewer
   photons. Its fixed photon input does not impose fixed output Hamming weight
   after its classical decoding.

## What survives mathematically

The direct collision witness, disjoint-support characterization, and
permutation counterexample in `theory/proven_results.md` are useful project
results. The moment machinery is standard: Martinez–Font-Segura,
[2602.09894v1](https://arxiv.org/html/2602.09894v1), Sec. 3.6 gives general
Fock-state moments. Their relationship to our exact support classification
has not been exhaustively traced. Assign **novelty OPEN**, not “apparently new.”
The Haar conditional-mean and covariance statements are formal symmetry
corollaries; they calibrate experiments and do not establish computational utility.

## Search scope and limitations

Databases: web scholarly discovery with primary arXiv, publisher and author
repository follow-through; one independent SciSpace index query. Queries covered
“bosonic birthday paradox”, “average collision free probability”, “ObliQ”,
“Bosonic Binary Solver”, “photonic minimum bisection”, “boson sampling graph
partitioning”, “variational boson sampling graph optimization”, “XY mixers
Dicke fixed Hamming weight”, “photonic postselection variational”, “collision-free
disjoint boson interferometer”, “zero collisions boson unitary”, “bunching
disjoint supports photons” and factorial moments. Search date horizon through
2026-11-20; primary language English. Second strategy: exact support/moment
search in SciSpace, which returned multiphoton distinguishability and suppression
law papers; no exact match was authenticated. BBS references were followed
backward to Brádler–Wallner and Banchi–Quesada–Arrazola. Comprehensive forward
citation chasing, thesis coverage, non-English sources and conference versions
remain incomplete. One agent performed both strategies.

ObliQ's publisher page was discoverable and its abstract authenticated, but
direct full text returned HTTP 403 and its Rice repository copy could not be
opened through the web reader. Therefore anchor construction, collision
decoding and the precise QUBO dynamics remain **unverified**, not absent.
An implementation merely named `PenaltyObliq` is not competitor validation.
Several additional records in the matrix were checked only at abstract level;
their detailed assumptions must be authenticated before reimplementation.

## GO / NO-GO interpretation

NO-GO for a paper based on number conservation, known Haar scaling, a generic
conditional CVaR objective, a universal Pareto obstruction, or oracle-trained
state preparation. GO for testing a narrower operational question: can
optimum-blind, collision-aware training improve total success at matched
training and physical-attempt budgets over reoptimized distinguishable and
strong classical feasible search? A positive small simulator result still
would not establish novelty, scaling, hardware support or quantum advantage.
