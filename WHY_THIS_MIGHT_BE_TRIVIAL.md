# Adversarial science review

Reviewed 2026-11-20 from checkpoint
`847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`.
This is a same-agent self-review of the theory route, not an independent
certificate or a review of experimental outputs not yet supplied.

| Required attack | Finding | Consequence |
|---|---|---|
| Is this only fixed Hamming weight? | Number conservation plus CF decoding is elementary. | No contribution claim. |
| Already known in QAOA? | Hadfield et al. App. A.3.2 explicitly gives XY-mixer Minimum Bisection; Dicke-state comparisons are established. | Do not claim constraint-preserving optimization itself is new. |
| Already known in boson sampling? | Haar twirling and exact CF ratio are in Arkhipov–Kuperberg. | Haar experiment is validation, not discovery of the law. |
| Can a classical method do the same? | Direct feasible sampling avoids rejection; disjoint-column circuits have an exact independent categorical sampler. | Compare their charged classical search costs. |
| If optimum known, can U prepare it trivially? | Yes: a mode permutation yields success one. | Direct success optimization with known `C*` is an oracle diagnostic, not an optimum-blind solver. |
| Does postselection erase benefit? | Haar mean success is uniform balanced success times d/D. | Count every physical attempt; conditional metrics alone are inadequate. |
| Is classical optimization doing the work? | It can directly prepare any selected bisection; graph-informed anchors may already solve these small graphs. | Evaluate anchor alone and equal-evaluation classical search. |
| Is multiphoton interference useful? | Exactly collisionless circuits with distinct input modes have disjoint column supports and no nontrivial interference in output probabilities. | Perfect collision suppression alone is insufficient; compare reoptimized distinguishable circuits. |
| Can a classical sampler reproduce outputs? | Yes exactly at P_CF=1; every experiment in the proposed tiny range can also be simulated exactly. | No quantum advantage inference from small-n enrichment. |
| Does gain survive equal shots? | Not yet determined by theory or naming a baseline. | Include training attempts, failed CF events and final holdout sampling. |
| Is there a universal Pareto tradeoff? | No: (1,1) is attainable for any nonempty known target set. | Only restricted ansatz/budget/entropy frontiers are meaningful. |
| Are we counting waiting time correctly? | 1/E[p] and E[1/p] differ; zero observed successes gives an unbounded upper waiting-time confidence limit. | Separate ensemble averages, fixed-circuit waiting time and observed binomial intervals. |
| Is lower CVaR a solver-quality certificate? | Once the optimal conditional mass exceeds alpha, lower CVaR can saturate while physical success remains low. | Track physical success separately; no robustness claim from CVaR alone. |
| Is a class named PenaltyObliq a competitor? | No. Authentic full-support penalty dynamics and decoding must be extracted from a primary source. | A repaired classical penalty reference does not close the photonic competitor gate. |

The known Haar law, the permutation counterexample, and the exact collisionless
classification survive these logical attacks under their stated hypotheses.
They establish useful constraints and negative results. Their novelty remains
unestablished. A publishable optimization benefit remains OPEN.
