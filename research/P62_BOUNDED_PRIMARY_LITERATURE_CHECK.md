# P62: bounded primary-source overlap check

Date checked: 2026-11-25. Base checkout:
`682d3573c47ffe4261ae4c018d2132af8e5d8a8e`.
Scope: attribution and overlap, using the literature-check skill. This is not a
new proof audit, an experiment, or publication novelty clearance.

**Verdict: known ingredients; exact P62 composition not established by the three
checked sources; novelty OPEN.** The overlap classification for P62 as a whole
is **partial or adjacent result only** for each source below. Failure to extract
P62 from these sources is not evidence that P62 is new. Its existing internal
proof certifications and this literature question are separate.

## Exact target and interpretation

Target: `theory/P62_random_embedding_local_control_obstruction.md` at
`aff6ceaa642752d72cbf6ab08251852bf22f1176`, SHA256
`138b8a79511ef127480cd23f4a8275e663039b644ab6068daf23a07d4559dd37`.
The copy in this checkout has the same SHA256. The independent reconstruction
`f301920` and focused audit `e312909` already certify the stated proof; this
report does not strengthen their scope.

The source question is the exact arrow: for every fixed finite weighted graph
G and feasible k, one independent uniform physical embedding Pi is drawn once;
the outside joint count law is fixed conditional on Pi and the entire history,
independent of Pi, G and controls; controls affect only s active output modes;
top-k ties are uniform. The best of T fresh classical uniform frontiers, each
scoring at most 2^s feasible active-subset/outside-prefix candidates, dominates
the decoded quantum best of T after averaging over Pi. Every classical score
is paid. The theorem permits adaptive control knowing G and Pi.

This is not a statement about matched wall time, equal score counts, a selected
fixed embedding, a Pi-dependent additional frontend, or a graph-informed
outside law. Neither uniform objective functions nor efficient simulation of
the outside quantum distribution is assumed.

## S1: Wolpert--Macready, original NFL theorem

- **Bibliography/version:** David H. Wolpert and William G. Macready,
  *No Free Lunch Theorems for Optimization*, IEEE Transactions on Evolutionary
  Computation 1(1), 67--82, April 1997; printed revision 30-Dec-1996.
  [DOI 10.1109/4235.585893](https://doi.org/10.1109/4235.585893).
- **Authentication:** the original published primary paper was read in this
  [academic PDF copy](https://www.cs.ubc.ca/~hutter/earg/papers07/00585893.pdf).
  Its printed header supplies title/authors/journal/pages/revision;
  the [authors' IBM institutional record](https://research.ibm.com/publications/no-free-lunch-theorems-for-optimization)
  confirms title/authors/DOI. IBM says December; the journal says April.
  Publisher/NASA author access failed. This is a published-paper mirror.
- **Result extracted:** Secs II/III, Theorem 1, p69, with stochastic extension
  in Sec III.B, p71. For finite X,Y, any algorithms a1,a2 and a fixed observed
  value sequence d, the sums over all f:X->Y of P(d|f,m,a1) and P(d|f,m,a2)
  agree. Uniform-all-functions average performance agrees. The model
  counts distinct oracle evaluations and excludes wall-clock measures.
  Short exact excerpt: “For any pair of algorithms”.
- **Dictionary:** X would be the feasible k-vertex sets; f would be C_G;
  m counts distinct oracle calls, unlike P62's T frontier trials.
- **Application verdict:** **inapplicable** as a direct proof of P62. Fixing G
  and randomizing its vertex-to-mode map does not uniformly randomize all
  objective functions on k-subsets. Budgets also differ.
  **Overlap:** partial or adjacent result only.

## S2: Rowe--Vose, finite-group algorithm symmetrization

- **Bibliography/version:** Jonathan E. Rowe and Michael D. Vose,
  *Unbiased Black Box Search Algorithms*, GECCO'11 proceedings,
  pp2035--2041, 12--16 July 2011. The
  [official conference-proceedings PDF](https://groups.csail.mit.edu/EVO-DesignOpt/gecco2011Proceedings/proceedings/p2035.pdf)
  supplies the title, author affiliations and conference header.
- **Result extracted:** finite X,Y; nonrepeating black-box traces; a problem
  class F subset Y^X; G(F) is the group of search-space permutations preserving
  F. Definition 3 averages conjugate algorithms over G(F). Theorems 3--6,
  p2037, give invariance/equal average performance;
  Theorem 6 adds a worst-case comparison for monotone performance.
  Theorems 7--8, p2038, identify uniform random search when G(F)=X!.
  Short exact excerpt: “has the same expected average performance”.
- **Dictionary:** a vertex permutation induces a permutation of feasible
  k-subsets, a subgroup of all permutations of that search space; the orbit
  of C_G is a possible F. The group-average algorithm is adjacent to averaging
  Pi; P62's frontier envelope is additional.
- **Application verdict:** **verified** for the source's finite-group
  averaging statement under its own model; **inapplicable** as a standalone
  proof of P62. Vertex-permutation symmetry need not give G(F)=X!, and
  P62 allows revisits, graph access and unequal per-trial score counts.
  The extracted results do not supply its local-control frontier or the
  fixed-Pi best-of-T comparison. **Overlap:** partial or adjacent result only.

## S3: Oh--Fefferman--Jiang--Quesada, classical GBS graph baseline

- **Bibliography/version:** Changhun Oh, Bill Fefferman, Liang Jiang and
  Nicolás Quesada, *Quantum-inspired classical algorithm for graph problems
  by Gaussian boson sampling*,
  [arXiv:2302.00536v2](https://arxiv.org/abs/2302.00536v2), 23-Apr-2023,
  associated published DOI
  [10.1103/PRXQuantum.5.020341](https://doi.org/10.1103/PRXQuantum.5.020341).
  Extraction uses v2. Version history, PDF header and
  [versioned primary HTML](https://arxiv.org/html/2302.00536v2) agree.
- **Result extracted:** Sec II, Eqs1--2, encodes a graph's symmetric matrix
  through interferometer and squeezing parameters. Sec III, Eqs3--11,
  constructs a classical sampler for nonnegative symmetric matrices using
  mixtures of independent photon pairs; collision-free fixed-size outcomes
  have hafnian rather than squared-hafnian weights. Sec IV compares graph
  heuristics empirically; Sec V discusses possible separations, rather than
  proving universal domination. Short exact excerpt:
  “we require the matrix A to be nonnegative”.
- **Dictionary:** source A is an adjacency matrix, whereas P62's A is the
  active physical-mode set. Source M is P62's N; source N in pair sampling
  counts pairs. The graph determines global optical/sampling parameters.
- **Application verdict:** **inapplicable** as a proof of P62: its graph-aware
  circuit and collision-free sector differ from P62's graph-independent
  outside law and top-k decoder retaining collisions. It supplies a concrete
  prior classical graph-sampling baseline, not P62's frontier construction
  or fixed-embedding guarantee. **Overlap:** partial or adjacent result only.

## What is elementary, and what this check leaves open

The following are project-side comparisons and elementary deductions, not
additional results attributed to the three papers:

| P62 ingredient | Bounded attribution outcome |
| --- | --- |
| Every top-k result is an active subset plus an outside prefix | Direct order-statistic containment; no novelty claimed |
| A uniform Pi sends any fixed ordered physical partition to a uniform vertex ordering | Elementary finite-group averaging; S2 is adjacent general symmetrization literature |
| With Pi fixed, iid outside contexts have T-fold failure f_Pi(c)^T | Conditional product law; actual adaptive decoded costs need not be iid |
| E[f_Pi(c)^T] >= (E f_Pi(c))^T | Elementary Jensen inequality for x^T on [0,1]; no new exchangeability theorem or de Finetti representation is needed |
| Fresh classical frontiers have failure (E f_Pi(c))^T | Independent restart product; refreshing the classical roles must be explicit |
| Entire chain with at most 2^s paid candidates and the top-k decoder | Exact composition not extracted from S1--S3; global prior-art status OPEN |

The shared-latent-embedding issue is therefore handled by an elementary mixture
of conditionally iid failures. It must not be silently replaced by independent
unconditional quantum shots. This report authenticated no dedicated restart
paper or general exchangeability result; the bounded three-source allocation
was used on NFL, finite-group symmetrization and photonic graph optimization.
Calling the composition elementary does not establish that it was previously
published, nor does a missing exact citation establish novelty.

## Search record and coverage

General web-index discovery on 2026-11-25 used these four initial queries:

1. `Wolpert Macready 1997 No Free Lunch Theorems for Optimization pdf author theorem 1`
2. `random restart latent variable Jensen failure probability fixed random environment independent restarts symmetrization theorem`
3. `Gaussian boson sampling graph optimization random embedding local control output modes no advantage theorem`
4. `permutation invariant random search fixed objective random labeling symmetrization no free lunch theorem`

Three adaptive access/authentication queries followed:

5. `"No Free Lunch Theorems for Optimization" "wolpert" pdf site:santafe.edu`
6. `"No Free Lunch Theorems for Optimization" site:nasa.gov pdf`
7. `"No Free Lunch Theorems for Optimization" pdf Wolpert Macready 1997`

Only the three primary papers above support overlap judgments. Secondary
summaries, snippets, abstracts and search results were discovery aids, not
theorem evidence. A direct read of versioned arXiv, official proceedings and
the published NFL primary text formed the extraction pass. S2's bibliography
exposes earlier focused-NFL references; S3's introduction exposes graph-encoding
and dense-subgraph predecessors. Those additional papers were not authenticated
or extracted here. No comprehensive backward/forward citation traversal,
separate bibliographic index, non-English search, or independent second
reviewer was used. The later access queries were by the same searcher and
are not an independent novelty search. The date horizon is index availability
on the date checked, not certified coverage of all literature through that date.
No “apparently new” label is justified.

## Retention and checks

The initial read-only NFL DOI lookup found no existing project cache.
PDFs and pypdf-extracted text were retained under this isolated checkout's
ignored `.research-cache/literature/`, following the explicit source-cache task.
The tracked root ignore rule was added. No source full text is tracked.

| Source/version | Retained PDF SHA256 | Extraction |
| --- | --- | --- |
| S1 published April1997/revised30-Dec1996 | `7bf3552a29bcbdfa60e70156a7ab6072174586fb596ae29fb4b1509cff0b6266` | Text available; mathematical glyphs partly missing, so Theorem1's displayed equality was also visually checked from PDF p69 |
| S2 GECCO2011 proceedings | `a17c6e752614b365fa47b765a31a3a6cad0e5c47cb9e760d1cd456950e39ae79` | Text available; browser primary extraction cross-checked |
| S3 arXiv2302.00536v2 | `1a11dd95a2259152ab831b7fd0b74329a0a1bc5253b8818c12928341acd10829` | Text available; versioned primary HTML cross-checked |

Checks performed: source metadata/version authentication, bounded extraction
at the listed locations, notation/hypothesis translation, and applicability
comparison. These are not full-paper proof audits. The cache helper verified
all three records and hashes with no issues, effective Git exclusion and a
root repository ignore rule. Cached extraction establishes availability, not
mathematical correctness; another clone need not have these ignored files.

No research-state source evidence was recorded: none of the three sources
proves the complete P62 arrow, and no ledger update was requested. No paper,
scientific code, experiment, graph, source state, raw result, credential or QPU
was changed or executed. Only document/source extraction and integrity checks
were performed. Existing pytest tests were not run in this literature-only
subtask; integration remains subject to the repository's existing-test rule.
The positive optimizer objective remains OPEN.
