# P37 bounded source comparison — 2026-11-22

Target: theory/phase3_loss_source_selection.md at1d65279. This note separates
authenticated input, internal corollary and newly discovered adjacent work.
No global novelty finding is made. The full literature-check workflow and
earlier cached P32 input are used; new loss preprints below are discovery
records, not fully audited theorem dependencies.

## Authenticated input

Bouland et al., *Complexity-theoretic foundations of BosonSampling with a linear
number of modes*, [arXiv:2312.00286v2](https://arxiv.org/html/2312.00286v2),
19 March2025, §4 Lemma1/Eq6. HTML locators and formula were rechecked.
Their n,c are our survivor count l,target k. Uniform weak compositions give
the exact occupied-mode law. The loss mixture/coefficient formula was audited
in P32. No originality is claimed for this law, threshold decoding, source
conservation, or stars-and-bars sampling. The two/four candidate reduction,
ordered loss transitions and fixed-lambda boundary expansion are internal
derivations from that law; attribution remains unresolved.

## New adjacent sources: read status matters

Armando Angrisani and Hela Mhiri,
[*Polynomial-time classical simulation of boson and fermion sampling under thermal loss*](https://arxiv.org/abs/2611.08444v1),
arXiv:2611.08444v1,5 November2026,83 pages. Metadata, abstract and selected
HTML passages were read; the full theorem/proof chain was not audited.
The authors state efficient Haar-typical simulation at fixed nonzero loss,
including saturated inputs, and stronger near-full-input conclusions. Treat
these as source claims pending exact hypothesis/error/runtime verification.
Do not substitute them for a proved worst-case statement about trained U.

Youngrong Lim,
[*Boson sampling is fragile to loss*](https://arxiv.org/abs/2611.01434v1),
arXiv:2611.01434v1,1 November2026,9+30 pages. Metadata/abstract read;
no full-proof audit. The stated result concerns full-output approximate
classical sampling under fixed uniform loss with Haar-averaged error,
including distinct single inputs and additional vacuum modes. This is
adjacent to the project, not an authenticated prerequisite or a universal
optimization no-go theorem. Its abstract reports an earlier21 October
Zenodo version; event dates and arXiv dates are distinct.

P37's boundary regime eta=1-lambda/m loses O(1) photons; fixed nonzero loss
instead loses Theta(m) at N near m. These regimes must not be identified.
Neither efficient sampling of the Haar-averaged marginal nor an average-case
simulation guarantee automatically simulates a graph-trained/adaptively
selected circuit under the project's desired relative success metric.

## Bounded search and unresolved comparison

Queries executed22 November: `boson sampling threshold detectors loss optimal
photon number occupied modes Haar clicks`; `"boson" "threshold" "photon number"
"optimal" "Haar"`; `"binomial" "Bernstein" "sign changes" "unique root"`.
These surfaced adjacent threshold/loss/sampling work, not an authenticated
matching source-selection theorem. That absence proves no novelty. Generic
Bernstein variation-diminishing ideas are established mathematics; the proof
is deliberately elementary and self-contained instead of claiming a new
root-counting method. No full external source text is committed.

Remaining obligations: audit the exact new loss theorem relevant to any
proposed QPU regime; search photon-source allocation/click-resource literature
with exact quantities; independently review P37. Keep manuscript and QPU closed.
