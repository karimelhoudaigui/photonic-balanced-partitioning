# Density certificate: bounded novelty and exact-source audit

Checked 2026-11-21. Scope: literature and hypothesis comparison only; the
coordinator's proof was not edited. This document is not an independent proof
certificate, a full survey, or a manuscript section.

Exact target read from main commit
`75e5831a34b7bbf82ae21bb88894a2c12d4a6d47`:
`theory/phase3_density_certificate.md`, SHA256
`7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c`.
Earlier N1/N2 proof read at the same revision:
`theory/near_collisionless_bound.md`, SHA256
`30dc286d6a112c98a2be6c08d1a7223daad0ddb91eba6355966bbc31748ebbd3`.
The isolated worktree's parent is `97274b6a35a0c9849bacfb92212bce7b16e74247`;
the newer main proof is an explicitly external read-only input to this audit.

## Verdict and exact novelty boundary

**N1 overlaps Deshpande et al. (2018):** the compact permanent certificate is
a **formal corollary not stated**, rather than a new interference principle.

**N2 is a formal corollary of a classical identity:** its nonnegative cycle
majorant follows from MacMahon's Master Theorem, followed by a Schatten/Frobenius
norm estimate. A particular convenient scalar formula does not establish a
novel combinatorial method.

The output-intensity/dominant-assignment bridge, its composition with N1/N2,
the small-(M) refinement, and its balanced sharpness example were **not
authenticated as exact results in the checked corpus**. That is an unresolved
attribution question, not proof of originality. No “apparently new” label or
publication-readiness conclusion is assigned. Novelty remains **OPEN**.

## Target and notation dictionary

The target fixes an $m\times k$ orthonormal occupied-column matrix (V), one
photon in each distinct input, and compares full unconditioned Fock laws
(p_b,p_d) for identical bosons versus independent labeled particles with
labels forgotten. Output collisions are retained. With (q_{ia}=|V_{ia}|^2),

\[
a_i=\sum_aq_{ia},\quad
M=\sum_i\left(a_i^2-\sum_aq_{ia}^2\right),\quad
\delta=\sum_i(a_i-\max_aq_{ia}),\quad
B_{ab}=\sum_i\sqrt{q_{ia}q_{ib}}.
\]

Here (M) is the **expected number of colliding unordered pairs**, not the
probability of at least one collision. The lower bound (c>0) applies to
**every positive output intensity** (a_i); zero rows can be removed, but small
positive rows cannot be ignored. The average density (k/m) does not supply
this lower bound. Spatial (B) is a Gram matrix of magnitudes of spatial
orbitals, not a Gram matrix of photons' internal states.

The targeted composition is

\[
\sigma=\|B-I\|_F\le2\sqrt\delta+\delta=:\rho(\delta),\qquad
\operatorname{TV}(p_b,p_d)\le\min(1,f(\rho(\delta))),
\quad f(s)=\tfrac12\left(\frac{e^{-s}}{1-s}-1\right),
\]

on the branch $\rho(\delta)<1$. The observable replacement is
$\delta\le M/c$, improved, when (M<c^2/2), to

\[
\delta\le d_c(M)=\frac{c-\sqrt{c^2-2M}}2.
\]

The resulting leading upper envelope is (M/(2c)+O(M^{3/2})) at fixed (c).
These exact hypotheses are what a source would have to reproduce or imply.
A theorem about loss, small internal indistinguishability, a Haar average,
constant observable locality, or dilute lattice evolution is not that statement.

## Primary source 1: Deshpande et al. (priority comparison)

Abhinav Deshpande, Bill Fefferman, Minh C. Tran, Michael Foss-Feig, Alexey V.
Gorshkov, *Dynamical phase transitions in sampling complexity*, PRL **121**,
030501 (2018), DOI [10.1103/PhysRevLett.121.030501](https://doi.org/10.1103/PhysRevLett.121.030501).
Checked [arXiv:1703.05332v3](https://arxiv.org/html/1703.05332v3), 2018-08-05,
12-page PDF including supplement; SHA256
`7493ed821279c9a344b2f3a3783ca5a0468bf649705c85cdb5a87bbe20df7ece`.

Theorem 1.A/Lemma 3 assume separated single-boson inputs, local lattice
dynamics, $m=c_1n^\beta$, $\beta>1$, and $t\le0.9L/v$. The comparator
is independent particles. Supplement (S12)–(S16) uses interference pairs,
relative permutations and ordered routings; factoring gives N1 after
consistent normalization. Their continuation uses maximum overlap row sums
and localization, not (M,c).

Printed (S13) drops an occupation factorial and reverses indices without an
explicit adjoint; (S19)/(S20) differ by two. Our factorial proof must therefore
accompany the attribution. **Verdict:** verified methodological overlap; N1
is a **formal corollary not stated**. Direct arbitrary-frame/density
application of their locality theorem is **inapplicable** without a bridge.

## Primary source 2: 2607.24728 (priority comparison)

Léo Monbroussou, Hugo Thomas, Hela Mhiri, Zoë Holmes, Elham Kashefi,
*Classical simulation and model concentration in passive linear optics*,
[arXiv:2607.24728v1](https://arxiv.org/html/2607.24728v1), 2026-07-27.
Checked 43-page primary PDF, SHA256
`4c7d63d1f9c22da4124025bc0d8648143d179f195629a2cc71ad9d49ae4961e9`.

§IV, Simulation Techniques 1–5, and Appendix C concern classical evaluation
or approximation of **observable expectations**, through irrep compression,
additive amplitude estimation, and direct monomial expansion. Technique 2 is
a Haar-average surrogate; Techniques 1 and 5 give exact restricted regimes.
The paper explicitly separates average-case and worst-case guarantees.
Its collision-free input discussion concerns input occupation/resource
profiles, rather than our measured output (M).

**Application verdict:** **partial or adjacent result only**. Computing low
moments such as (a_i,M) is consistent with its simulable observable regimes.
That does not supply total-variation closeness of the complete output law to
the particular independent-particle law. No theorem giving the target
$\delta$, minimum-positive-intensity (c), or sharp (M/(2c)) envelope was
authenticated in its simulation discussion or appendices. This is a bounded
comparison, not a global absence claim. The paper is important context for
the separate, already-known low-rank objective-oracle route.

## Primary source 3: MacMahon and the cycle majorant

Pavel Etingof and Igor Pak, *An algebraic extension of the MacMahon Master
Theorem*, [author PDF](https://www.math.ucla.edu/~pak/papers/et6.pdf), Theorem 1,
page 2, equations (1),(2). Title/authors and eight-page form match the sole
version [arXiv:math/0608005v1](https://arxiv.org/abs/math/0608005), 2006-07-31.
The actual author-copy bytes checked have SHA256
`251f91076a08084eeee828cc728126fabb5f790bd9c85368c7ca6ee8d3f1ce83`;
byte identity with the arXiv PDF is not claimed.

The classical theorem expresses repeated-multi-index coefficients as the
series $1/\det(I-TA)$, with formal diagonal variables (T). Specializing to
nonnegative (A), squarefree coefficients give principal permanents.
Dropping all nonsquarefree coefficients produces a nonnegative coefficient
majorant. **Application verdict:** verified, **formal corollary not stated**
for the target cycle/Frobenius envelope, not a new master theorem.

The explicit bridge, derived here for comparison, is

\[
\operatorname{per}(I+zA)
\preceq\det(I-zA)^{-1}
=\exp\left(\sum_{\ell\ge2}\frac{\operatorname{tr}(A^\ell)}\ell z^\ell\right)
\preceq\frac{e^{-\sigma z}}{1-\sigma z},
\quad\sigma=\|A\|_F,
\]

for real symmetric nonnegative zero-diagonal (A). The last step uses
$0\le\operatorname{tr}(A^\ell)\le\sigma^\ell$. At (z=1) the infinite
envelope requires $\sigma<1$; finite coefficient truncation needs no such
convergence assumption. This is the classical explanation of N2's ingredients.
It does not derive the new target's $\sigma$-versus-$\delta$ bridge.

## Primary source 4: density is already an established parameter

Valery Shchesnovich, *Distinguishing noisy boson sampling from classical
simulations*, Quantum **5**, 423 (2021),
[DOI 10.22331/q-2021-03-29-423](https://quantum-journal.org/papers/q-2021-03-29-423/).
Checked revised primary [arXiv:1905.11458v9](https://arxiv.org/abs/1905.11458v9),
2022-03-07, 25-page PDF, SHA256
`7a545fea87ac9117fb70def582d71937126c339cf07ecb386736189d7de77529`.
This is a later revision than the publisher's v7; version interchangeability
is not assumed.

The introduction and §2 define density as photon count divided by mode count,
and study distinguishing noisy outputs from approximations retaining limited
interference order. Explicit noise assumptions are introduced, including
uniform internal distinguishability and uniform loss for particular formulas.
**Application verdict:** **partial or adjacent result only**. That global
density is not $\min_{a_i>0}a_i$, nor does its role prove our uniform
small-(M) upper bound. It prevents framing “density matters for classical
approximation” as a new conceptual observation.

## Separating the remaining elementary bridges from an originality claim

The following is an algebraic interpretation for finding prior art, not an
external theorem attribution. Choose an input label uniformly from ([k]),
then sample its output using the column-stochastic channel (q). The output
law is (a_i/k), its posterior label law is (t_{a|i}=q_{ia}/a_i), and

\[
\delta/k=\sum_i(a_i/k)(1-\max_a t_{a|i}),\qquad
M=\sum_i a_i^2(1-\sum_a t_{a|i}^2).
\]

Thus normalized dominant-assignment loss is a Bayes classification error and
the collision moment is a weighted quadratic/Gini impurity. Their elementary
row inequalities should not be called new quantum principles. The refined
inversion additionally combines a global small-(M) branch condition with
$M\ge2c\delta-2\delta^2$. The frame partition and groupwise Cauchy–Schwarz
then link this to a Frobenius spatial-overlap quantity.

The exact composition and balanced leading-constant sharpness remain the
plausible attribution targets. No checked source above proves all of these
arrows as one theorem. Conversely, no extensive information-theory survey
of Bayes-error/Gini/Hellinger matrix inequalities was completed. That is an
explicit blind spot, not evidence that the frame inequality is novel.

## Scope-sensitive comparison and non-claims

| Item | Overlap / attribution status | What remains distinct or missing |
|---|---|---|
| Independent-particle comparator and routing triangle | formal corollary not stated in Deshpande notation | Preserve factorials and full Fock domain. |
| Positive cycle / inverse determinant majorant | formal corollary not stated of MacMahon | Frobenius specialization is elementary. |
| Small spatial support overlap suppresses interference | partial or adjacent result only in lattice localization work | General arbitrary-frame constants are not their stated locality theorem. |
| Efficient fixed-degree moment evaluation | known after translation of notation | A moment algorithm is not a full-law TV theorem. |
| Density affects simulation/error analysis | partial or adjacent result only | Global (k/m) differs from minimum positive row intensity. |
| $\sigma\le2\sqrt\delta+\delta$, $\delta\le d_c(M)$, composed sharp envelope | exact overlap unresolved | Do not label newly proved research solely because search missed an exact phrase. |

For the target's (m=4,k=2) balanced example, (a_i=1/2) and
$M=\operatorname{TV}=\delta(1-\delta/2)$, so the leading envelope
(M/(2c)=M) is internally consistent at (c=1/2). This is a sharpness family
of elementary two-photon mixing, not a hardness construction or a novel
Hong–Ou–Mandel phenomenon. This audit did not recompute its full Fock law.

The target's dilute/spectator obstruction has $c\to0$. It therefore remains
essential: replacing (c) by average density, dropping tiny positive rows,
or replacing expected pairs (M) by collision probability can invalidate the
intended interpretation. Relative success on rare events, graph-dependent
postprocessing, reoptimization, noise identification and QPU benefit are not
established by this literature check.

## Search protocol, provenance, and remaining work

Two strategies, by the **same searcher**, were used: exact/synonym searches
for spatial overlap, dominant assignment, low collisions, flat occupancy,
distinguishable approximation and full-output TV; then backward/contextual
checks of the requested 2018 and 2026 papers and the classical determinant
identity. Representative exact query strings included:

- `boson sampling spatial overlap disjoint supports collisions distinguishable total variation bound`;
- `boson sampling classical distinguishable approximation near permutation unitary collisions bound`;
- `boson sampling spatially separated wavefunctions leakage distinguishable particles total variation bound`;
- `"permanent" "Frobenius norm" "identity matrix"`;
- `"permanent" "MacMahon" "determinant" "upper bound"`;
- `"boson sampling" "collision" "minimum" "intensity"`;
- `"boson sampling" "overlap matrix" "classical approximation"`;
- `Gini impurity Bayes error inequality` and `"Bhattacharyya" "Gram matrix" "error probability"`.

Search horizon: material discoverable through 2026-11-21, English-language
physics/combinatorics sources; no exhaustive forward-citation graph, complete
older classification literature, private databases or blind second reviewer.
Discovery snippets were not used as theorem evidence. Primary PDFs were
downloaded to `/tmp/pasqal_density_*`; pypdf 6.4.0 extracted text, with the
read equations checked against primary HTML where available. Source hashes
identify the exact inspected bytes. Full copyrighted texts are not tracked.

A temporary ENOSPC error prevented one extracted-text file write; the PDFs
had downloaded and hashed successfully, and their relevant pages were then
read in memory. No project file was removed. This did not leave any of the
four primary records above dependent on an unread search snippet.

No mathematical proof file, code, benchmark, manuscript, raw experiment,
QPU program, or main-workspace state was changed. This document adds a
literature record only. The 194-test pass recorded for its parent commit
`97274b6...` is not promoted into evidence of this mathematical or novelty
claim; no repeated repository test run is needed for this single prose file.

Next checks with the highest information value: an independent search focused
on the frame/assignment inequality and Bayesian-channel formulations; then
compare the exact sharp envelope against older spatial-localization bounds.
If those establish the same result, reclassify the composition accordingly.
Until then, use **candidate certificate with established ingredients and
unresolved novelty**, with proof review and experimental validation reported
separately.
