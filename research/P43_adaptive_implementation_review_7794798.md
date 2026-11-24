# P43 implementation review — frozen 7794798

Verdict: **AUDITED, NOT EXECUTED — STATIC ALIGNMENT PASS, WITH SCOPE LIMITS**.
No blocking physics, optimum leakage, postselection normalization, or population
selection defect was found in the frozen implementation. This permits the
specified exploratory veto if root's preflight passes and an external bounded
runner enforces the resource contract. It is not a test-pass receipt, sampler
distribution validation, independent experiment, or accepted positive result.

## Reviewed objects and reviewer scope

Author revision: `77947983a71904d4bb0c625ee9b25f361772c9ee`.
Files were read from that exact Git revision, not from mutable uncommitted code.
Git blob identifiers:

| Path | Blob |
|---|---|
| research/P43_global_gain_probe.py | d78d0b6be925075f2a5d694fea774443b5b584df |
| research/P43_execution_spec.json | eccea48be6f70110945980f8ab0bbd6c04586fec |
| research/P43_execution_contract.json | 0c2cc594c4fbdbb66a4fd2b3dd7419efc31c7eea |
| tests/test_p43_global_gain_probe.py | 369b9ad6f8013aef0f73eb92c90164026c066c5a |

The adaptive lane wrote the scientific card at `1811ad7` and the symmetry
derivation at `088bcc8`; root wrote the implementation. This is a design-author
review of a separately authored implementation with shared project context,
not independent scientific replication or a blinded reviewer. Mathbox's
computation-audit checklist was used. No sampler, pilot, graph generation,
test suite, or numerical experiment was run by this reviewer.

## Alignment checked from code

1. **Population and source.** Four graph constructors and seeds match the frozen
   ER p=.35 / RR degree4, weights1..9 population. There is no score-dependent
   filtering, connectivity filter, optimal-state helper, exact solver, or input
   optimum. Each graph gets ONE common anchor, not one per model/replicate.
   Every full scan examines and records all k^2 one-swap candidate scores; at
   most8 complete scans are allowed. Strict improvement and lexicographic ties
   are implemented. A last-scan improvement is correctly NOT certified locally
   optimal. The anchor remains fixed during all subsequent tuning/probes.
2. **Physical echo.** The same-side mask implements H_intra, its complement
   H_cross; separate spectral norms and centered linear gradient match the card.
   Row multiplication by exp(-i alpha ell) is the intended diagonal phase.
   W.conj().T @ D_phase @ W has the correct reversed/sign-changed echo, not a
   mistaken repeated forward circuit. No nonlinear optical cost gate is claimed.
3. **Photonic law.** B sends k distinct occupied input modes through a local
   Clifford2017Backend; no remote Processor/client is imported. `sample()` is
   called serially and counts from all modes are retained. D independently
   routes each labelled input through |U[:,source]|^2. b4 samples disjoint input
   photon groups with the same U, then adds all occupations; collisions between
   species are retained. No full exponential Fock distribution is constructed.
4. **Global payoff.** Every optical attempt is retained. CF is checked on full
   k-photon occupations; all collisions have gain zero and consume an attempt.
   The scalar gain is exactly max(0,C0-cut) on CF, without a division by P_CF,
   optimum mask, favorable postselection, or C*. Using integer edge weights and
   small integer sums makes the graph scores exactly representable in float64.
5. **Phase-field law.** The alphabet is the specified four roots. The suffix DP
   table satisfies e_r(i)=e_r(i+1)+w_i e_(r-1)(i+1), so choosing i with
   w_i e_(r-1)(i+1)/e_r(i) gives the product-weight k-subset law by conditioning.
   Dividing every weight by their total does not change that law. Degeneracy
   uses one charged uniform-feasible fallback; it does not repeatedly redraw
   phases until a convenient support is obtained. The generic nonuniform law
   has not been tested numerically in this review.
6. **Selection.** Every tuple receives 14 shots in every one of8 graph/replicate
   cases. Summing those equal-size batch means is equivalent to ranking pooled
   raw means. Each model selects its own tuple; np.argmax chooses the first
   lexicographic tie and all-zero totals select analytic identity. All scores,
   including nonwinning tuples, remain in the raw file for best-so-far analysis.
   Downstream summaries must actually include those tuning discoveries.
7. **Probe chronology and labels.** A selection file with raw-prefix, code and
   spec hashes is written before any probe outcome. A single fixed permutation
   is applied to each preselected graph. Inverse permutation maps the SAME
   anchor and photon/species identities to new labels; it does not reoptimize
   the source. Replicates2/3 use the fresh seed namespace430200. Matrix covariance
   is checked at1e-11, stricter than the design tolerance1e-10. These remain
   relabels of development graphs, not independent held-out graph units.
8. **Caps.** Complete tuning uses 4*2*8*14=896 attempts per sampled model;
   probes use at most2*2*32=128, giving at most1024. An identity selection skips
   its probe attempts rather than spending the remainder on new settings.
   Each of5 classical methods receives112 candidate scores in each tuning case
   and32 in each probe case. Common anchor scores are separately recorded.

## Disclosures, limitations and follow-up obligations

- **b4 assignment clarification.** The original scientific card mentioned a
  fixed partition per graph/replicate; the execution code/spec fix one seeded
  source order per GRAPH and reuse it for both replicates. This is a visible
  pre-outcome closure, not a selected species partition. It provides fewer
  independent species assignments and cannot support a claim robust across
  all such assignments. Its identities are transported correctly under labels.
- **Baseline strength.** The spectral method scores spectral/noisy proposals
  but accepts them only when no worse than the current anchor. It does not
  descend from a worse spectral starting point into another basin. Calling it
  a fully tested strong multistart spectral optimizer would overstate the code.
  The short annealer and pair-exchange search are likewise specified bounded
  heuristics, not independently tuned best classical optimizers. These are
  acceptable generous optical veto controls because no pilot positive is
  accepted; any apparent positive must face stronger costed baseline tuning.
- **Costs are incomplete by algorithm.** Matrix setup/compilation and sampling
  times, score counts, and the common anchor are recorded. Selection, repeated
  covariance matrices, bookkeeping and some repeated known-anchor `cut` calls
  are not separately assigned to model ledgers. Global CPU includes them, but
  row timings are not the full runtime of a deployable algorithm. Extra calls
  on the already known source reveal no new candidate, yet do use CPU. This
  blocks any total-resource/hardware advantage interpretation, already excluded
  by the contract. Simulation time must not be called measured device time.
- **Validation scope.** Current sampler tests cover HOM, deterministic seeding
  and identity/species conservation. They do not compare a generic complex
  multi-photon network against an independently implemented probability law,
  nor validate the generic weighted-subset frequencies. Local installed
  Perceval1.3.0 source was read: Clifford2017Backend directly delegates unitary,
  input and serial samples to exqalibur; random_seed seeds exqalibur. Its C++
  sampler correctness was not independently established here. A nontrivial
  small-network permanent/Fock reference is a useful preflight extension and
  necessary before trusting a positive optical mechanism. Passing HOM alone
  does not establish a generic many-body law.
- **Resources are external obligations.** The script itself does not enforce
  CPU/wall/output caps or one-thread environment variables. Metadata alone is
  not enforcement. Root must use its bounded runner and retain partial output
  on resource failure; such a failure is INCONCLUSIVE, never a negative result.
- **Provenance boundary.** The selection file is an automatic serialized freeze
  with hashes, not a separate intermediate Git commit. The program does not
  inspect probe outcomes before making that selection. There is no scientific
  need for an intervention on these development relabel probes; do not describe
  this as an independently reviewed held-out validation boundary.
- **Frozen inputs only.** The graph builder hardcodes p=.35 and degree4 rather
  than reading those numeric spec fields. These equal this exact frozen spec;
  a future changed spec alone would not change the actual generator. Any later
  variant needs an explicit new frozen implementation and contract.

No listed issue changes the analytical clipped-payoff identity or supplies a
counterexample to the echo's physical model. No result from this audit warrants
a scientific positive, QPU run, paper modification, or main-program closure.
