# P51/P52: bounded primary-source attribution check

2026-11-25, literature-check workflow. Question: which parts of the permanent
PGF, single-mode phase invariance, complex-Hadamard family and four-particle
phase response are already explicit, and which checked source establishes
the EXACT full-input, arbitrary-Hadamard, joint-order<=3 statement?

**Result:** the PGF, single-mode invariance, H4 family and examples of genuine
four-particle interference are known. The three checked papers do not establish
our exact P51 third-order theorem or P52 ranked-mean/control-hull implication
under the same hypotheses. This is a limited extraction result, NOT evidence
of novelty. P51 correctness and any novelty assessment are separate tasks.

## Correa Anguita et al.: PGF and one-mode invariance

- Experimental validation of boson sampling using detector binning,
  [arXiv:2502.05093v1](https://arxiv.org/abs/2502.05093v1),7-Feb-2025.
  DOI10.1088/2058-9565/adecbc identifies the published paper; extraction here
  is from the versioned arXiv primary text.
- [Appendix A](https://arxiv.org/html/2502.05093v1), Eqs27/31, writes
  the virtual matrix U†Lambda U and its occupied-input permanent with the
  distinguishability matrix. Fully identical CF photons give our permanent
  characteristic/PGF formula after choosing single-mode bins and variables.
- [Appendix F](https://arxiv.org/html/2502.05093v1), text before Eq42,
  explicitly explains why a one-mode photon-number distribution depends only
  on the row magnitudes. Thus our identical one-mode laws for fixed Q are
  known after notation translation. Generic multi-mode phase sensitivity does
  not establish or refute the extra full-input Hadamard cancellations.
- Source formula/argument extracted; not a full-paper proof audit. The sign
  printed in Eq44 is NOT used for any implication here. No exact arbitrary-
  Hadamard joint-third-order theorem was extracted. Overlap: known after
  translation for PGF/one-mode claims; partial/adjacent for P51/P52 as a whole.

## Jones et al.: the H4 family and an internal four-cycle phase

- Interfering distinguishable photons,
  [arXiv:2001.08125v1](https://arxiv.org/abs/2001.08125v1),22-Jan-2020;
  published as Multiparticle Interference of Pairwise Distinguishable Photons,
  [PRL125,123603](https://doi.org/10.1103/PhysRevLett.125.123603).
- [Main Eq3 and supplement Sec2/Eq6](https://arxiv.org/html/2001.08125v1)
  give a flat four-mode quitter with spatial phase chi. Its matrix is
  symmetric and our H4 equals P U_quit P, P exchanging zero-based indices1,2.
  The matrix FAMILY is therefore known after relabeling.
- Main Eq4/supplement Eq10 describes four-photon coincidence with a special
  internal overlap ring: opposite internal pairs are orthogonal, adjacent
  overlaps remain nonzero, and their collective phase affects interference.
  One must NOT set all overlaps to1 in that reduced formula: the omitted
  exchange terms used the orthogonality premise. Supplement Eq8 uses only
  TWO injected photons and is not a counterexample to P51's full-input result.
- Matrix/formula/hypotheses checked, not experimental data or the full proof.
  Overlap: known family; partial/adjacent collective mechanism. No P52 decoder
  or all-identical arbitrary-Hadamard theorem is supplied by this extraction.

## Faleo et al.: high-order phase with lower-order correlators unchanged

- Entanglement-induced collective many-body interference,
  [arXiv:2310.08630v3](https://arxiv.org/abs/2310.08630v3),30-Jun-2024;
  [published DOI10.1126/sciadv.adp9030](https://doi.org/10.1126/sciadv.adp9030).
- [Theory SecI, Eqs1/3/5 and AppA Eq18](https://arxiv.org/html/2310.08630v3)
  derive a four-point correlator proportional to cos² of half a collective
  phase, while lower-point correlators do not depend on those phases. Their
  source includes an internally entangled pair and controlled polarizations;
  their spatial network is parallel beam splitters. This is NOT P52's
  unentangled identical full-CF source through a general flat unitary.
- AppB Eqs19–24 distinguishes threshold coincidences from factorial/number
  correlators: a lower click-fold count may contain higher-order contributions.
  This supports the need to keep PNR moments and threshold events separate,
  not a transfer of their numerical fringe to our ranked decoder.
- Exact primary locations/hypotheses extracted; full proof/experiment not
  independently audited. Overlap: partial/adjacent known four-body mechanism;
  inapplicable as a proof of P51 or the P52 top4/control-hull arrow.

## Authentication, coverage and limits

Exact arXiv version histories and HTML headers were checked against the
abstract pages; the stable primary texts above, not search snippets, supplied
the equations. No full copyrighted source text is copied here. A read-only
stdlib literature-cache lookup found no project cache, and an alternate
reference-name search found no matching retained source. No PDF was downloaded
or retained; there is NO local source SHA256 to report or invent. No cache,
ignore rule, shared ledger or manuscript was initialized/modified.

The bounded search used a general web index plus primary arXiv/publisher
pages. Queries covered complex Hadamard/multiphoton/third-order correlations,
four-photon collective phases, moments/permanents, and the detector-binning
title. A second synonym pass searched explicit third-order/moment terms.
One-hop references exposed Laing et al., PRL108260505(2012), and the Quantum8,
1479 binning paper, but their complete primary texts were NOT verified here.
No comprehensive forward-citation, older combinatorics or classification
search was performed. No "apparently new" label is justified by this scope.

No project/scientific module was imported or numerical work performed.
Only the read-only stdlib cache helper, metadata/file search and browser
source reads were used. Implementation review has priority when P52 freezes.
