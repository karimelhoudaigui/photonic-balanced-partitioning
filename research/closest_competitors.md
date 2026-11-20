# Closest competitors and comparison obligations

Checked 2026-11-20. See `literature_matrix.csv` for extraction depth.

| Competitor | Verified overlap | Material distinction / fair comparison needed |
|---|---|---|
| Cazalis et al., [GBS for binary optimization, 2412.14783v1](https://arxiv.org/html/2412.14783v1) | Minimum bisection, penalty QUBO, variational photonic ansatz, CVaR and optimum sampling metric | Squeezed inputs and threshold clicks; compare full physical attempts and tune penalty under an equal budget. It is not the same distribution as fixed-Fock passive sampling. |
| Ranjan et al., [ObliQ, DOI 10.1145/3771573](https://doi.org/10.1145/3771573) | Problem-customized static anchor plus variational photonic circuit; real hardware claimed in primary abstract | Full algorithm extraction pending. A generic fixed-k Haar search or classical penalty model is not an implementation of ObliQ. |
| Makarovskiy et al., [BBS, 2510.08274v1](https://arxiv.org/html/2510.08274v1) | Fixed-Fock photonic sampling, trainable circuit, classical bit flips, cost-evaluation benchmarking, hardware experiments | Bit-flip parameters change output Hamming weight and reach full binary space. Charge their updates and samples. Reimplement with the documented decoding before claiming head-to-head results. |
| Brádler–Wallner, [2112.09766v1](https://arxiv.org/html/2112.09766v1) | Variational shallow bosonic solver and parity decoding for binary optimization | Parity decoding is different from CF-only acceptance. Its input-pattern/run coverage must be reproduced. |
| Hadfield et al., [1709.03489v2](https://arxiv.org/html/1709.03489v2), App. A.3.2 | Minimum bisection with an XY mixer preserving feasible Hamming weight | No bosonic bunching, but qubit gate depths and cost layers have different hardware costs. Encoding novelty is unavailable. |
| Cook et al., [1910.13483v2](https://arxiv.org/html/1910.13483v2) | Dicke vs feasible-state starts, ring/complete XY mixers, fixed-cardinality graph optimization | Maximum k-cover, not bisection. Useful constrained optimization benchmark and initialization warning. |
| Chen–Zhang, [PRA 114, 022607](https://doi.org/10.1103/93x9-y3y9) | Interferometer optimization with fidelity and postselection success | Generative task rather than minimum bisection; only abstract authenticated. The quality/acceptance tradeoff is already a literature topic. |
| Direct classical feasible sampler and swap local search | Exact cardinality, no rejected samples, transparent cost-evaluation count | Must run on the same graph instances and seeds. Evaluate initialization before any photonic layer; otherwise classical discovery may supply all the gain. |
| Reoptimized distinguishable photons | Same single-particle mesh and number of photons, no collective interference | Two comparisons required: fixed U statistics ablation and independent equal-budget reoptimization. Neither alone settles the other question. |

Clifford–Clifford's [classical boson-sampling algorithm](https://arxiv.org/abs/2005.04214)
also prevents treating simulation difficulty of a naive permanent enumerator as
algorithmic advantage. Their exact complexity hypotheses need checking before
extrapolation; our tiny instances are fully classically simulable regardless.
