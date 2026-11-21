# Threshold low-rank route: exact overlap and source audit

Checked: 2026-11-21. Base commit: `2996904f861a5db2a732e38dbc97bd6c91e5708b`.
Scope: `theory/phase3_threshold_lowrank.md`, no code or manuscript changes.
Reviewer: same author, **self-review**. Independent proof/implementation review
is not inferred from agreement with a cited paper.

**Finding:** polynomial evaluation of a fixed number of output-mode marginals
and the proposed factorial-weighted polynomial are established prior art.
Threshold-QUBO expectation evaluation is a direct application. Calling that
general mechanism a new dequantification theorem would misattribute it.
Whether the concrete ObliQ audit, bit-explicit implementation, or any broader
research package has publishable novelty remains **OPEN**; no such conclusion
is established by this search.

## Verified primary records

### A. Aaronson–Arkhipov / Gurvits

Scott Aaronson and Alex Arkhipov, *The Computational Complexity of Linear
Optics*, [arXiv:1011.3245v1](https://arxiv.org/html/1011.3245v1), 2010-11-14,
Appendix 12, Lemma 67 and Theorem 68; proof following Theorem 68.
The exact v1 PDF is 94 pages, SHA256
`44d4f6f833b4ae8d08cc3fac41c33a98706ec46ec81d07ded66bc4cb99d14828`.

The lemma states polynomial arithmetic computability of the permanent of
identity plus fixed-rank matrix. The theorem gives deterministic
\(N^{O(r)}\) evaluation of any specified occupation pattern on (r) output
modes. Its generating-function proof writes the relevant expectation as
\(\operatorname{per}((U^\dagger D U)[C,C])\). Setting diagonal entries of
(D) to zero on the selected outputs and one elsewhere gives our vacuum
formula directly. The appendix assumes the low-rank lemma without proof.

Translation: their (n=N), (k=r), their first (n) occupied input modes
are our arbitrary distinct set (C) after relabeling. Their generating
variables (|c_a|^2=0) mean vacuum projection, with (0^0=1).
Their matrix named (V) in the low-rank lemma is our (-V^\dagger V),
not our rectangular row submatrix (V).

Verdict: **verified** for exact qualitative computability and the vacuum
identity. Overlap: **known after translation of notation**; the QUBO linear
combination is a **formal corollary not stated**. Numbering is version-specific:
the later published appendix uses different labels, so do not cite Lemma 67
as if it were its published label.

### B. Ivanov–Gurvits: the exact proposed polynomial already appears

Dmitri A. Ivanov and Leonid Gurvits, *Complexity of full counting statistics
of free quantum particles in product states*, Phys. Rev. A **101**, 012303
(2020), DOI [10.1103/PhysRevA.101.012303](https://doi.org/10.1103/PhysRevA.101.012303).
Checked primary [arXiv:1904.06069v2](https://arxiv.org/html/1904.06069v2),
2020-02-21, eight-page published-version preprint, SHA256
`1fd11b7e700a8fb9e85af6b4b81970c8d59da24dca382d5c72a3c78d3c9a8616`.

§IV.A, equations (15)–(17), proves the auxiliary polynomial and extraction
by equal multi-degrees weighted with factorials. The stated operation bound
is (O(N^{2r+1})), using a coarse monomial count. §V.A explicitly includes
zero-occupancy projection through vanishing generating variables. §II.D
defines complexity as arithmetic operations; bit complexity and certified
finite-precision stability are not supplied there.

Translation: in their factorization of the rank-(r) update use
(u_j^{(a)}=-\overline{V_{aj}}\), (v_j^{(a)}=V_{aj}). Their formal variables
then give exactly the product in our equation (2), and their equation (17)
is our factorial-weighted diagonal extraction.

Verdict: **verified**. Overlap: the DP polynomial and extraction are
**known after translation of notation**, rather than merely a neighboring
idea. The equal-total-degree state count refines a loose published count by
an elementary observation; no claim that this refinement is new or optimal.

Source caution: printed equation (25) has a sign inconsistent with equation
(24): expanding (U_0^{-1}e^{i\Lambda}U_0) requires
(I+U_0^{-1}(e^{i\Lambda}-I)U_0). This discrepancy is present in the checked
PDF and HTML. The rank statement is unaffected, but the sign must not be
copied into a vacuum formula. Our proof uses the projector Gram matrix
directly, and cites equations (14)–(17), (24), with this caution.

### C. Oh–Lim: recent explicit restatement and mean-value context

Changhun Oh and Youngrong Lim, *Classical algorithms for measurement-adaptive
Gaussian circuits*, checked primary [arXiv:2509.00746v1](https://arxiv.org/html/2509.00746v1),
2025-08-31, 34-page PDF, SHA256
`9ece55d3456634907a735396b4d5060b1043c2f6820da3601437f5d0d8691314`.
This record uses v1 theorem/equation numbering, not the revised v2 or journal
version numbering. The abstract page separately lists PRX Quantum **7**,
010329 (2026); that journal text was not used to authenticate these labels.

§VI.B.1, equations (63),(64) and following paragraph, explicitly reviews the
same low-rank product/coefficient/factorial algorithm and (O(N^{2r+1}))
bound, crediting Ivanov–Gurvits. Lemma 2 recalls Gurvits's generating-function
algorithm. The paper extends the method and emphasizes distinctions between
sampling and mean-value tasks.

Verdict: **verified** for the restated algorithm; **partial or adjacent result
only** for its more general Gaussian/product-state framework, which our proof
does not need. The exact-generating-function/mean-value distinction itself
cannot be presented as a new conceptual discovery here.

### D. Roga–Takeoka: few-mode marginals in simulation applications

Wojciech Roga and Masahiro Takeoka, *Classical simulation of boson sampling
with sparse output*, Scientific Reports **10**, 14739 (2020),
[DOI 10.1038/s41598-020-71892-0](https://www.nature.com/articles/s41598-020-71892-0).
Primary version-of-record full text read through the web tool; no retained PDF
hash claimed. Its Theorem 1 repeats Gurvits's few-mode marginal algorithm,
then applies marginals to reconstruction under sparsity assumptions.

Verdict: **verified** for the repeated marginal theorem, **partial or adjacent
result only** for full-distribution reconstruction. Our QUBO expectation result
requires no sparse full output law. The paper is evidence that application-level
use of easy marginals in otherwise hard boson sampling is also established.

### E. Barvinok: discovery record, not a substitute low-rank-update proof

Alexander I. Barvinok, *Two Algorithmic Results for the Traveling Salesman
Problem*, Mathematics of Operations Research **21**(1), 65–84 (1996),
[DOI 10.1287/moor.21.1.65](https://pubsonline.informs.org/doi/10.1287/moor.21.1.65).
The primary abstract establishes fixed-rank permanent computability. Full
theorem text was not authenticated here. In any case (I_N-V^\dagger V)
usually has rank (N), so a theorem about the matrix's own low rank does not
directly prove our result. The relevant property is a fixed-rank **update to
identity**, authenticated by A/B above. Verdict for a direct Barvinok-only
application: **unverified**, with a known hypothesis mismatch if used without
an extra reduction. Overlap: **partial or adjacent result only**.

## Source acquisition and search limits

PDFs A/B/C were downloaded from their exact official arXiv version URLs into
`/tmp/pasqal_lowrank_*`, hashed with SHA256, and read after extraction using
pypdf 6.4.0. Primary HTML formulas and PDF text were cross-checked. Full
copyrighted source texts are not copied into this repository. No external
program was executed, and no credential or QPU endpoint was accessed.
The default network sandbox initially prevented the arXiv download; the
authorized read-only download then completed. This does not leave a source
verification gap for A/B/C.

Searches on 2026-11-21 included:

- `boson sampling marginal distribution fixed number output modes permanent low rank vacuum probability`;
- `permanent identity plus low rank matrix polynomial time rank fixed Barvinok`;
- `"permanent" "identity" "low-rank" "Gurvits" algorithm`;
- `"Classical simulation of boson sampling with sparse output" arxiv`;
- `Ivanov Gurvits Complexity full counting statistics free quantum particles product states 012303 arxiv`;
- `"threshold" "QUBO" "Gurvits"` and `"ObliQ" "classical" "marginal"`.

First pass: direct marginal/low-rank queries found A/D and older low-rank
permanent work. Second strategy, by the **same searcher**, followed the
backward references of C's equation (64), locating B's exact polynomial.
No independent searcher or exhaustive forward-citation survey is claimed.
No positive novelty inference is made from searches missing an ObliQ-specific
phrase. The core overlap is established by exact formulas, not by an empty
search or snippets.

## Internal proof and precision self-audit

Target: propositions L1/L2 and equations (1)–(13) of the companion note.
Primary self-review verdict: **proved as written**, under its distinct-input,
passive-unitary, unconditioned-measurement hypotheses and its explicit finite
input representation. This is not an independent audit certificate.

| Obligation | Result | Exact reason |
|---|---|---|
| Vacuum is a Gram permanent, not its squared modulus | passed | Project creation vectors, then take their norm; distinct inputs have input norm one. |
| (p!) diagonal weight and minus sign | passed | Match two label assignments with (p!) bijections and subset sign ((-1)^{|S|}). |
| Off-diagonal coefficient states retained | passed | DP (5) permits later transitions into the diagonal. |
| State count and rank-two exponent | passed | Stars-and-bars at equal total degree; exact sums in table. |
| Arithmetic vs bit complexity | passed after explicit representation | Common-denominator integer recurrence, numerator bound (10), rational coefficient sizes counted. |
| Arbitrary irrational data exact in finite bit time | not claimed | Classical entry approximation oracle/algorithm must be supplied. |
| Fixed float precision stable by polynomial op count | rejected | Cancellation possible; instead (11),(12) give sufficient certified dyadic precision. |
| Relative error near zero | not claimed | Identity and fully occupied-output cases can have exactly zero vacuum probabilities. |
| QUBO expectation and symmetric-Q factors | passed | (J_{ij}=2Q_{ij}); threshold inclusion–exclusion (8). |
| Full sampler, modal candidate, best sample, global conditioning | out of scope | None is determined by the first two threshold moments. |
| Repeated input occupancy covered by (1) | refuted | Two photons in one mode give ((1-q)^2), not (1-2q+2q^2). |
| Global optimization becomes polynomial | not claimed | Efficient objective evaluation does not solve nonconvex parameter minimization. |

The precision proof is constructive but conservative: (|V_{aj}|\le1),
approximation error at most one, coefficient \(\ell_1\)-norm product bounds,
and (p!\le N!) suffice. Its logarithmic precision cost is polynomial despite
a potentially very large absolute condition estimate. It neither assumes
that complex cancellations are benign nor promotes float64 cross-checks into
a bit-complexity theorem.

No load-bearing numerical computation or new numerical performance result is
reported here. Independent Perceval checks are the parent's separate task.
The appropriate research consequence is to include a classical ideal-objective
oracle baseline and distinguish it from modal/best-sample/conditioned tasks.
This route does not by itself meet a goal of an original publishable theorem.

Repository validation in this isolated worktree:
`PYTHONDONTWRITEBYTECODE=1 <main>/.venv/bin/python -m pytest tests/`:
**194 passed in 17.86s**, Python 3.11.15, pytest 8.4.2. Nine Perceval warnings
report its inaccessible default persistence folder and temporary-folder
fallback; no test failed. These existing tests guard repository compatibility,
not the universal mathematical claim in this note. New tests were not added
because this task changes only two research documents, and the parent owns
the independent implementation and numerical cross-checks.
