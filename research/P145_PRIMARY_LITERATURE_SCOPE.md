# P145 — bounded primary-literature scope for photonic local-neighborhood search

Checked 26-Nov-2026 with the literature-check workflow. Scope: quantum proposals,
photonic graph completion, product-state triad phase and the cited 2026 PT paper.
**Disposition: the broad framework and physical triad effect are established;
the exact P145 raw-cut-utility/comparator bridge and its priority remain unverified.**
This is source authentication/extraction, not a new proof, optimizer result or novelty certificate.

Existing P65/P100/P132 literature records were consulted first. Two bounded search
strategies used exact titles/identifiers, then quantum-proposal/PT/local-group synonyms.
Only publisher/arXiv texts support the statements below. No large download, source
cache, code, import, AST, scientific computation, RNG, raw-data read, native or QPU call.
External payloads were browser-read, not retained; no external file SHA is asserted.

## S1 — quantum-generated proposals and the exact symmetry condition

David Layden et al., *Quantum-enhanced Markov chain Monte Carlo*,
[Nature 619, 282–287 (12-Jul-2023), DOI10.1038/s41586-023-06095-4](https://www.nature.com/articles/s41586-023-06095-4).
Exact extraction: [arXiv2203.12497v1, 23-Mar-2022](https://arxiv.org/html/2203.12497v1),
main Eqs.(2)–(7), proposal/acceptance section and Performance. Publisher metadata
was authenticated; the full Nature page hit an identity-provider redirect, so
journal/preprint byte identity or identical equation numbering is not claimed.

Prepare the current spin configuration, apply U, measure a proposal, then accept
classically. Eq.(3) contains the reverse/forward proposal ratio. Their symmetry
condition removes that ratio; a real symmetric Hamiltonian gives U=U^T.
Irreducibility/aperiodicity and the correct acceptance rule matter for convergence.
The reported iteration/scaling comparisons are empirical, not a general mixing
speedup theorem or a photonic/wall-time advantage. This verifies the generic
quantum-proposal arrow, not its transfer to a source/repair-dependent PLNS kernel.

## S2 — photonic graph encoding already includes classical-prefix completion

Rawad Mezher, Ana Filipa Carvalho and Shane Mansfield,
*Solving graph problems with single photons and linear optics*,
[PRA108,032405, 6-Sep-2023](https://journals.aps.org/pra/abstract/10.1103/PhysRevA.108.032405).
Extracted [arXiv2301.09594v2](https://arxiv.org/pdf/2301.09594v2), submitted revision
14-Aug-2023, PDF dated15-Aug-2023: §IV Eqs.(3)–(6), §V.C Th.1/Eqs.(12)–(17),
pp.2–4, with the corresponding graph simulation discussion.

A norm-scaled matrix is embedded in a passive 2n-mode unitary. The densest-subgraph
construction stacks J candidate adjacency blocks, uses 2kJ modes, and selects
specified output patterns. It also discusses fixing a prefix classically and
completing the remaining vertices optically. All k-subsets require J=binom(n,k);
a fixed-size residual can leave polynomial J. Thus hybrid completion is prior art.
Th.1 only gives a permanent UPPER BOUND increasing with edge count; the authors
explicitly distinguish it from actual permanent monotonicity. It supplies no
raw balanced-cut improvement guarantee, free preprocessing, all-attempt efficiency
or independently retuned-D dominance. The model/selected outcomes differ from PLNS.

## S3 — triad physics is established, not a useful graph-utility theorem

Adrian J. Menssen et al., *Distinguishability and Many-Particle Interference*,
[PRL118,153603, published10-Apr-2017](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.118.153603).
Extracted [arXiv1609.09804v1, 30-Sep-2016](https://arxiv.org/html/1609.09804v1),
Theory Eqs.(1)–(5), Appendix A Eq.(17)/tritter Eqs.(21)–(24), Appendix B.
Three independent photons with pure internal states have a collective product
J=<chi1|chi2><chi2|chi3><chi3|chi1>, beyond pair-overlap moduli; scattering laws
can differ while those moduli agree. Timing and polarization implement the experiment.

Dimensionality is essential: Appendix B does not license an arbitrary continuously
tunable phase at fixed pair moduli using polarization alone. The two-dimensional
Gram constraint fixes Re(J), hence cos(arg J) when J is nonzero; P142's conjugate signs can remain.
That last statement is the internal Gram dictionary, not a claimed new experiment.
No graph-cost decoder, accepted-improvement sign or classical-control separation
is established by this source. Observing a triad-sensitive count bin is insufficient.

## S4 — the cited PRR acceptance is genuine; its optimization chain is heuristic

Kate V. Marshall et al., exact accepted title
*Quantum-enhance Markov chain Monte Carlo for combinatorial optimization*,
[APS Accepted20-Nov-2026, DOI10.1103/th44-jfjh](https://journals.aps.org/prresearch/accepted/10.1103/th44-jfjh).
This is an accepted-paper record, not an asserted final volume/page citation.
Exact full-text extraction: [arXiv2602.06171v3, revised17-Nov-2026](https://arxiv.org/html/2602.06171v3),
§III.1–III.6, §IV–V, Appendices C,D,G; its arXiv title uses “Quantum-enhanced”.

The workflow combines classically pretrained warm-started circuits, many samples,
energy filtering, a Metropolis-style test and replica exchange. Appendix D explicitly
acknowledges asymmetric proposals and lack of guaranteed Boltzmann sampling;
§V describes a heuristic without a convergence guarantee. It must not inherit S1's
exact stationary-law theorem. Hardware MIS demonstrations reach117 variables,
but the tested instances are efficiently solved by CPLEX. §IV.4 notes overlapping
confidence intervals for a fitted scaling comparison; Appendix G distinguishes
whole-trial and best-observed times. None establishes a general or PLNS advantage.

## S5 — directly adjacent local quantum blocks with frozen-environment fields

Stuart Ferguson and Petros Wallden,
*Quantum-enhanced Markov chain Monte Carlo for systems larger than a quantum computer*,
[PRR7,013231, 3-Mar-2025](https://doi.org/10.1103/PhysRevResearch.7.013231).
Exact extraction: [arXiv2405.04247v2, 13-Jan-2025](https://arxiv.org/html/2405.04247v2),
§III.1 Algorithm3, §IV.1–IV.3, especially Eqs.(14)–(15)/Algorithm4, §V.
It updates selected spin groups with a smaller quantum processor while freezing
the remainder. The improved local method incorporates outside spins as effective
fields; a multiple-group variant sequentially updates environments. Numerical
thermalization/gap results are illustrative finite Ising studies, not a general
complexity, optimal block-selection or photonic-utility theorem.
This is a direct antecedent for local quantum blocks and boundary-field encoding.

## Dictionary, bounded overlap and remaining P145 obligations

| Proposed arrow | Disposition from the checked sources |
|---|---|
| Quantum proposal followed by a classical decision | Known after translation, S1; heuristic variant S4 |
| Small active block with the rest represented by fields | Known after translation, S5 |
| Classical prefix plus photonic graph completion | Partial/adjacent result only, S2; distinct encoding/resource model |
| Product-state triad phase beyond pairwise moduli | Known verbatim physical phenomenon, S3 |
| Positive raw three-photon balanced-cut utility versus reoptimized controls | Unverified by these sources |
| Novel PLNS composition or practical advantage | Unverified; neither absence nor a new label establishes it |

In project notation, a proposal Q is not yet the accepted/decoded transition P.
Stationary Boltzmann sampling, one-step raw utility I3, finite-horizon best cut,
and matched-resource optimization are different assertions. P65 already records
the proposal framework; its classical veto does not logically decide a changed PLNS.

P142's exact source `ee9bf009`,131l/SHA256
`8368acc5e02d67b25bd3e48a26c9d0d9f3b137f515bf426c1f88283dfdab492e`
separates the triad count contrast from its graph-weighted sum: degree-two means
agree at fixed transfer; clipping/invalid-hold effects need the complete raw ledger.
Cost-matched conjugation-closed spatial controls can already absorb its two source signs.
P143's103l/SHA256 `2c500892071978d87d8067e03c2a9a261371f3c0b3cf59a3c69f62a024824c99`
requires a finite common tag-blind instrument, analytic D probabilities and a
deterministic null to obtain its weak-window retuning obstruction. A changed
local controller must check these premises; the theorem is neither a blanket
PLNS rejection nor a positive escape certificate when a premise fails.

Any finite I3 claim still needs its OWN exact source, valid physical Gram family,
common decoder, all loss/collision/failed outcomes and scored preprocessing costs.
Include independently retuned D/proper groups, conjugate settings where admissible,
fixed-three-photon exact-law sampling and serious feasible local search with shared
graph information. These sources establish neither today's Lucy preparation/PNR
capabilities nor equal hardware latency. No computation or execution is authorized.
Coverage is bounded to the five primary papers/locators above, not all LNS or all
photonic optimization literature. Combined priority and the positive objective remain OPEN.
