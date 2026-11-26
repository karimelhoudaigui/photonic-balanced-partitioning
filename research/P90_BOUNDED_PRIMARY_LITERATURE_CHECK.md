# P90: three-source primary literature and overlap check

**Disposition: broad prior overlap is verified; P90-specific priority
and positive performance remain unverified.** Neither Fock-state
variational optimization nor graph-dependent `exp(-iHt)` is a new
architecture claim. The precise source-binding/repair combination still
requires investigation; this bounded search does not certify novelty.

Target: `research/P90_SOURCE_AWARE_NONFLAT_DESIGN.md`, original commit
`c52afab21bd4a1d4645f359619e510f118cb944b`, SHA256
`b3c0b04c486f3368a0cbbc7e2030d8225d015f182cbfb00e0a9b63e0a0b2f173`.
Checked client date: **2026-11-25**. Producer commit dates remain unchanged.

## 1. Scope, acquisition and provenance

The `literature-check` skill and its source-cache/source-record rules
were read. A read-only filesystem/identifier check found no project
`.research-cache/literature/records` directory. The existing
`research/literature_matrix.csv` already records the first two sources;
they are not new discoveries. No Python cache helper, installer or
scientific import was run. No cache was created, and no fetched paper
or full text was retained in Git. Retained-source SHA256: **NONE**;
extraction status: **selected online text available, not locally retained**.

Exactly three publications were prioritized and authenticated below.
Searches used general web discovery, then official versioned arXiv
abstract/HTML/PDF pages. Secondary search hits supplied no evidence.
The existing P85 2020 nonnegative-GBS attribution record remains intact;
it is not repeated as a discovery or counted as a new source here.

The same agent performed broad and author/citation-directed passes,
not an independent second literature review. No pilot outcomes, actual
seeds, generated graphs or numerical/native computations were inspected.
Only this report is written; paper, QPU and the frozen pilot are untouched.

## 2. Three authenticated records and exact extraction

### S1: Fock variational optimization with classical occupation mapping

Kamil Brádler and Hugo Wallner, *Certain properties and applications of
shallow bosonic circuits*, **arXiv:2112.09766v1, 17-Dec-2021**.
[Version record](https://arxiv.org/abs/2112.09766v1),
[exact HTML](https://arxiv.org/html/2112.09766v1),
[PDF](https://arxiv.org/pdf/2112.09766v1).

Locators inspected: sections **2.1–2.3, Algorithm 1, equations (1)–(4)**;
selected 2.5/2.7/2.8 passages. It proposes a single-photon-input passive
interferometer, classical parity decoding of occupation records and
cost-based training. Collisions contribute through that decoding.
The selected algorithm is not P90's exact-size uniform-fill decoder.

Authentication, method extraction and this limited translation are
verified. **Overlap: known after translation of notation** for the
Fock-ansatz/classical-cost loop; **partial or adjacent result only**
for P90's balanced repair. No source gradient rule, parity-surjectivity
theorem or optimization advantage theorem is imported. The 34-page PDF
was opened only in selected passages, not fully read. Its arXiv stamp
is v1; a later HTML rendering date is not a new research revision.

### S2: trainable classical decoding and all-training candidate credit

Alexander Makarovskiy, Mateusz Slysz, Łukasz Grodzki, Dawid Siera,
Thorin Farnsworth, William R. Clements, Piotr Rydlichowski and
Krzysztof Kurowski, *A Binary Optimisation Algorithm for Near-Term
Photonic Quantum Processors*, **arXiv:2510.08274v1, 9-Oct-2025**.
[Version record](https://arxiv.org/abs/2510.08274v1),
[exact HTML](https://arxiv.org/html/2510.08274v1),
[PDF](https://arxiv.org/pdf/2510.08274v1).

Locators: **III.1, Algorithm 1, III.1.1, VI–VII, Appendix B** in selected
HTML passages. BBS uses thresholded Fock samples, trainable probabilistic
bit flips and circuit training; all scored training candidates count
towards its incumbent. These facts establish prior hybrid-decoder
optimization, not fixed Hamming-weight repair. Section VI explicitly
uses function-evaluation comparisons rather than wall-clock accounting.

**Overlap: partial or adjacent result only** for P90's exact algorithm;
**known after translation of notation** for training plus classical
postprocessing and candidate credit. The method extraction is verified;
P90 superiority is unverified. Only selected portions of the 14-page
PDF/HTML were read. No experimental table or gradient theorem was
independently reproduced; no result transfers to a matched-total-cost claim.

### S3: graph-Hamiltonian optical walks and particle-dependent dynamics

Yizhi Wang, Yingwen Liu, Junwei Zhan and colleagues, *Large-scale
full-programmable quantum walk and its applications*,
**arXiv:2208.13186v1, 28-Aug-2022**.
[Version record](https://arxiv.org/abs/2208.13186v1),
[exact HTML](https://arxiv.org/html/2208.13186v1).

Locators: main-text **equation (1)** and the adjoining graph-model and
two-photon implementation paragraphs, HTML lines 35–44; **Fig.1**.
They define graph CTQW evolution by `exp(-iHt)` and distinguish
multi-particle bosonic, fermionic and distinguishable evolutions.
The described implementation uses two optical single-particle copies.

The model/architecture overlap is **known after translation of notation**.
It is **partial or adjacent result only** for P90's optimization task:
the inspected material is graph-walk dynamics, not its split/repair
basin kernel. The PDF fetch failed with a cache miss; no PDF or
supplementary completeness is claimed. Selected HTML is the evidence.
Graph hitting/mixing comparisons do not verify strong optimization
baselines, large-photon advantage or a Quandela hardware capability.

## 3. Exact P90 translation: known ingredients versus open combination

| P90 component | Checked implication | Overlap classification |
| --- | --- | --- |
| Fock inputs, programmable passive mesh, cost-feedback training | Verified broad framework, S1/S2 | known after translation of notation |
| Graph-dependent `exp(-iH)` | Verified model, S3 equation (1) | known after translation of notation |
| `W_ai=V[tau(a),sigma(i)]` as physical basis transport | Row/column basis relabeling is an algebraic consequence, not a separate new optical resource | formal corollary not stated |
| H built from current full-graph swap deltas | This exact initializer was not extracted from the three checked algorithms; priority is unverified | partial or adjacent result only |
| Split Fock kernel plus exact-size uniform collision fill | Neither parity nor free bit flips is that decoder; exact overlap remains unverified | partial or adjacent result only |
| Nonflat r2 repaired inclusion/cost identities | Internal two-photon algebra; no external attribution or novelty verification supplied | partial or adjacent result only |

The last rows mean **unverified priority**, not “apparently new.” Absence
from selected text does not establish absence from the papers or the
literature. The P90 formula is compatible with standard exchange
physics; specificity of notation or decoder is insufficient novelty.

The fixed-low-photon veto needs no external hardness theorem: for
bounded r, enumerate receiver occupations and small permanents, then
apply the same repair. This is polynomial in mode count at fixed r
under ideal arithmetic. Independent bounded-size species groups also
give a necessary positive classical control. These are internal control
constructions, not a verified approximation theorem for all bosonic
laws. P90's two-mode-block witness is exactly covered by its two-photon
group null and cannot establish computational advantage.

## 4. Search record, blind spots and remaining obligation

Discovery query families included: `photonic quantum walk graph partitioning
optimization boson sampling variational`; `bosonic quantum walks combinatorial
optimization unitary graph encoding collisions`; `boson sampling optimization
Fock variational graph`; and `Brádler Wallner variational Fock`.
The second strategy used the local literature matrix and BBS's backward
reference to Brádler–Wallner. Only the three authenticated primary sources
support this report. No comprehensive forward-citation, patent, non-English,
decoder-specific or late-2026 survey was completed. Some combined tool
outputs were truncated; targeted rereads supplied the specific locators
above. No full-PDF claim is based on a truncated response.

Safe disposition: retain P90 as a prospective mechanism whose broad
framework has clear prior art. Before any novelty claim, compare the
precise label-bound kernel, initializer and repair identities with a
separate targeted source pass. Before any positive claim, independently
reoptimized D, exact small-group/repair controls and strong feasible
search must still be beaten under full resource accounting, held-outs
and replication. This literature check proves none of those outcomes
and authorizes no experiment or manuscript revision.
