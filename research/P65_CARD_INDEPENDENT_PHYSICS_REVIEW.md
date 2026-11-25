# P65 independent static card review

2026-11-25. **Primary verdict: conditional on the two accepted pre-data
clarifications below.** With those conventions, the card/spec define a
coherent B80 + fixed-FAST finite DEV falsifier. No remaining material source,
Metropolis, score-budget, selection or information-leak defect was found in
this design scope. This is not an implementation or execution qualification.

Audited commit: `022962e69c76e37c573d5ed9bf71f1b6414338b6`.
The complete208-line card and177-line spec were read, with the source/kernel
definitions in the frozen P65 proof and immutable P43/P50/P55 caller context.

| Artifact | SHA256 |
| --- | --- |
| `research/P65_CAYLEY_MARKOV_DEV_CARD.md` | `dbb74c1943c47d9446d0c89245b73fc24c6275e750982ac77c71972386c2a773` |
| `research/P65_cayley_markov_dev_spec.json` | `6993da4efe018c80b7fd9021451fad301dd665b1c86c4eac8adab2b1904eeee4` |
| `theory/P65_collision_counted_photonic_markov_kernel.md` | `3ffb2be9e19b6d9acb49b6d376a7cbe1fc294940a24ee50313b840b3bf522271` |

## Required clarifications accepted before any data

1. Card line90 says distinct common start subsets. Independent uniform
   draws from distinct streams can produce the SAME subset. The frozen
   permutation recipe does not guarantee unequal values. ROOT accepted:
   distinct identifies streams/chains; repeated subsets are retained without
   uniqueness checks, rejection, reseeding or replacement. An enforced
   distinct-subset rule would change both the probability law and work.
2. Define `degree_A(i)=sum_j A_ij`, the exact WEIGHTED row sum in the Cayley
   normalization at card line31/spec line28. An unweighted NetworkX degree
   would produce different effective angles despite passing unitarity and
   symmetry checks. ROOT accepted an explicit prospective amendment and a
   smaller weighted nonregular qualification fixture.

ROOT instructed the implementation author to record both in a new pre-data
amendment, preserving this card/spec and the proof byte-identically. That
future amendment/source was not reviewed here. No start seed or realized
subset was evaluated to motivate either clarification.

## Obligation matrix and decisive reasoning

| Obligation | Static finding |
| --- | --- |
| Current partial-fill source | Passed: TEN photons in sorted CURRENT S, not one photon in every N20 mode; a new P43 factory on every attempt, with no obsolete-source closure reuse |
| Global Cayley family | Passed: H is real symmetric; I-itH is invertible and the two factors commute, giving unitary symmetric U and graph-label covariance; no selected partition enters H |
| B/D proposal symmetry | Passed for a fixed candidate in the ideal model: unconditional CF probabilities are respectively modulus-squared permanent and permanent of q; transposition exchanges S,T |
| Collisions / wrong total | Passed: every collision is a paid raw self-loop; eta1 wrong-total/fallback is first failure, not loss postselection or a new detector law |
| Acceptance | Passed: fresh independent coin for EVERY CF result, including T=S/probability1; collided attempts retain current S and record unused coin seed |
| Annealing interpretation | Passed as a finite optimization schedule: beta_j is state-independent and the selected U stays fixed; no single equilibrium/convergence claim follows for the changing-beta trajectory |
| Training | Passed: eight reset two-step candidates, same uniform training start, all post-step CURRENT cuts in exact Fraction fitness, first listed candidate breaks ties; all scored losing candidates retained |
| Fresh statistic | Passed: three new eight-step chains, final chain-best INCLUDING each initial cut, and exact mean over three chain-bests; these are not24 iid observations |
| Score budget | Passed: four actual initial scores per optical case/arm, forty actual post-step current scores, plus one proposal score for each CF outcome; reset copies do not invent score calls |
| Paid incumbent | Passed: all actual initial/training/fresh scores, including unselected candidates; current/chain-best/incumbent do not silently replace the current source state |
| Common starts / namespaces | Conditional on clarification1 and the later metadata guard: deliberate aliases only for common starts; counts, coins, arms/candidates/steps, r-controls and FAST have distinct declared roles |
| Selected parameter versus RNG | Passed: fresh stream uses literal selected, not the chosen parameter index; selection cannot search later fresh streams |
| Optional D | Passed: independently selected eight-candidate trajectory and own preprocessing/streams; no copied B optimum or inherited uncharged matrix |
| Sorted species | Passed as a heuristic: source-dependent4/4/2 grouping can break reverse-state symmetry, so no automatic Gibbs law is asserted |
| r2/r3 | Passed: independent uniform remove/add choices on occupied/complement sets, five fresh eight-step chains and no fake training; their five-chain estimator/cost differs explicitly from B's three-chain estimator |
| FAST gate | Passed: both fixed modes separately on both raw graphs, no B start/incumbent/features, same-mode two-graph veto, eligible online prefix only; timely initialization can refute, first scan/no early cap required for survival |
| B-only grant | Passed as the stated favorable envelope: actual B graph/circuit/start/request/seed/score/selection work paid; optional work, graph generation, diagnostics, simulator calls and evidence IO do not enlarge its grant |
| Factory prefix | Passed: only returned backend WALL excluded; RNG/source validation before the helper clock stays paid; total factory CPU/WALL retained, internal CPU split unknown |
| Outcome / hardware scope | Passed: no stage-one status accepts a positive; optional controls need separate review and the broader held-out/full-resource/replication gates remain open |

For B and D, retaining unconditional collision mass on the diagonal avoids
the state-dependent CF-normalization bias. At each FIXED beta, the symmetric
proposal with Metropolis acceptance has the intended Gibbs distribution as
a stationary law. Uniqueness, convergence, irreducibility and aperiodicity
require additional hypotheses; this review does not infer them from the card
or from a finite annealing/chain-best statistic.

The four initial-score calls are one training start plus three fresh starts.
The eight training resets copy the one exact training-start score and pay
copy/validation work. Every attempt then pays the required current-cut call,
even for collision or rejection. Thus the complete optical budget remains
forty attempts/factories per graph, eighty attempts/eight hundred modeled
photons overall. Optional work cannot fund the four FAST allowances.

## Remaining source-freeze obligations and provenance

The actual source must still qualify integer/count/overflow guards, exact
candidate-order tie handling, current-state resets, every-attempt factory
ownership, independent/unused coin roles, weighted normalization, repeated
start retention, all-shot statistics, nested-clock prefix accounting and FAST
timestamp/cap eligibility on SMALLER fixtures. Global seed uniqueness/nonzero
native seeds are prospective checks, not results of this static review. No
N20 canary, full70-state diagnostic, optimum or graph draw is required here.

This report records an independent same-team static review with shared broad
task context. An isolated subagent separately checked costs and namespaces
and identified the same two implementation conventions. That agreement is
review provenance, not experimental evidence or blind external replication.
proof-audit/computation-audit methods and changed-report mathematical
proofreading were applied. Only read-only text/git/hash inspection and this
report write/commit occurred: no import, Python/AST, pytest, numerical
calculation, seed evaluation, graph or draw. Existing tests remain a later
authorized worker's gate before merge.

Only this report is written in `.local/p65-card-review`, branch
`research/p65-card-review`. No N18, P63, author card/spec/proof, old raw data,
manuscript or credentials were changed. ROOT retains exact-source review,
qualification and execution authorization. No accepted positive or QPU step
follows from the conditional static pass.
