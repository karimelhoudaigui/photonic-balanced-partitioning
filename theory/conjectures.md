# Open conjectures and falsified directions

Checkpoint: `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`; reviewed 2026-11-20.
These notes contain no unverified theorem.

| ID | Statement or question | Status | Discriminator / evidence |
|---|---|---|---|
| C-01 | A universal tradeoff prevents `P_CF=1` and `P_opt|CF=1` simultaneously. | REJECTED | A permutation prepares any known target bisection; T-Pareto. |
| C-02 | The Haar CF expectation is a new contribution. | REJECTED | Arkhipov–Kuperberg 1106.0849v1 already gives it; T-Haar. |
| C-03 | Beating Haar CF decay is itself a nontrivial algorithmic contribution. | REJECTED | Identity/permutations have CF probability one at all sizes. |
| C-04 | Untrained Haar gives mean conditional enrichment on optimal cuts. | REJECTED | T-Haar-Metrics gives exactly the uniform feasible fraction. |
| C-05 | Exactly collisionless circuits can use collective bosonic interference to change the output probabilities for distinct-mode single-photon inputs. | REJECTED | T-Pairs gives disjoint supports and classical product sampling. |
| C-06 | A restricted shallow mesh can enrich success per attempt beyond Haar at a fixed training budget without access to `C*`. | OPEN | Compare conditional energy/CVaR plus collision penalty with paired seeds, random balanced and classical swap search; charge training and initialization. |
| C-07 | Such enrichment requires indistinguishability. | OPEN | Reoptimize distinguishable circuits under the same budget, and evaluate the same fixed circuits under both statistics. |
| C-08 | Near-zero collision probability implies a practically useful approximation by a disjoint-support sampler with a dimension-controlled error bound. | OPEN | Prove a quantitative stability statement; T-Pairs controls pair overlap but alone is insufficient. |
| C-09 | A useful concentration/collision bound holds after requiring a nondegenerate complement-symmetric target distribution. | OPEN | T-Pareto removes unrestricted version; exact two-support obstruction in T-Pareto suggests a narrower question. Quantitative bound unproved. |
| C-10 | Optimized fixed-particle training beats an authentic penalty photonic algorithm at equal total physical attempts and equal classical evaluation cost. | OPEN | Needs an authenticated implementation and matched resource accounting; a classical Bernoulli/Gibbs penalty baseline alone cannot settle it. |

Stop rule: a result appearing only when the optimum is supplied, collision
failures are discarded from the budget, favorable graphs are selected, or
initialization performs the classical combinatorial search does not establish
the claimed optimization benefit. Preserve such outcomes as negative results.
