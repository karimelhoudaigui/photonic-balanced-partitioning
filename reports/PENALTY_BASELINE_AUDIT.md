# Full-cube penalty baseline audit

**PASS: implemented classical full-cube penalty energy and sampling. OPEN: authentic optical ObliQ comparator.**

The previous `PenaltyObliq` sampled the fixed-k photonic distribution, dropped collisions, and evaluated a conditional energy that ignored lambda. It never explored the full binary cube. That implementation cannot support a penalty-vs-photon scientific claim.

The replacement is explicitly named `PenaltyProductBernoulli`, a classical independent-bit sampler over all `2**n` bitstrings with n real logits. The old class name is a warning-emitting compatibility alias; optical matrix arguments now raise a shape error. No ObliQ dynamics or circuit depth is inferred.

## Exact QUBO identity

`E(x) = sum_(i,j) w_ij*(x_i+x_j-2*x_i*x_j) + lambda*(sum_i x_i-k)**2`.

Upper-triangular convention: offset `lambda*k**2`, linear coefficient `degree_i + lambda*(1-2*k)`, pair coefficient `2*lambda-2*w_ij` (missing graph edges have w=0). Some graph couplings cancel exactly when lambda=w; the realized density must be measured.

Exhaustive path checks on n=4,6,8 and seven lambda values (2352 binary evaluations) have maximum direct-vs-QUBO residual `2.66e-15`. This validates the finite implementation; it is not evidence of an efficient quantum solver.

## Executed lambda diagnostics

The Gibbs table uses beta=1 and exact exponential enumeration. It is a diagnostic of the energy, not an efficient sampler, a variational result, or a physical optical circuit.

| n | lambda | Gibbs P_feasible | Gibbs P_success | All penalized minimizers feasible? | QUBO coupling density | Coefficient abs range |
|---:|---:|---:|---:|:---:|---:|---:|
| 4 | 0 | 0.216064 | 0.143735 | False | 0.500000 | 2.000000 |
| 4 | 0.1 | 0.259141 | 0.172391 | False | 1.000000 | 9.000000 |
| 4 | 0.5 | 0.425790 | 0.283253 | True | 1.000000 | 2.000000 |
| 4 | 1 | 0.587324 | 0.390712 | True | 0.500000 | 2.000000 |
| 4 | 2 | 0.801983 | 0.533512 | True | 1.000000 | 2.500000 |
| 4 | 4 | 0.967742 | 0.643781 | True | 1.000000 | 1.833333 |
| 4 | 10 | 0.999917 | 0.665186 | True | 1.000000 | 1.611111 |
| 6 | 0 | 0.183980 | 0.076819 | False | 0.333333 | 2.000000 |
| 6 | 0.1 | 0.243437 | 0.101644 | False | 1.000000 | 9.000000 |
| 6 | 0.5 | 0.428926 | 0.179093 | True | 1.000000 | 3.000000 |
| 6 | 1 | 0.585618 | 0.244518 | True | 0.666667 | 2.000000 |
| 6 | 2 | 0.799374 | 0.333769 | True | 1.000000 | 4.500000 |
| 6 | 4 | 0.967211 | 0.403848 | True | 1.000000 | 3.166667 |
| 6 | 10 | 0.999916 | 0.417503 | True | 1.000000 | 2.722222 |
| 8 | 0 | 0.162468 | 0.041055 | False | 0.250000 | 2.000000 |
| 8 | 0.1 | 0.232945 | 0.058865 | True | 1.000000 | 9.000000 |
| 8 | 0.5 | 0.424469 | 0.107263 | True | 1.000000 | 2.500000 |
| 8 | 1 | 0.582214 | 0.147125 | True | 0.750000 | 3.000000 |
| 8 | 2 | 0.797363 | 0.201493 | True | 1.000000 | 6.500000 |
| 8 | 4 | 0.966815 | 0.244313 | True | 1.000000 | 4.500000 |
| 8 | 10 | 0.999915 | 0.252678 | True | 1.000000 | 3.833333 |

## Executed shot-trained diagnostic

Paths n=4,6,8; seeds 101,102,103; lambda=.1,1,10; COBYLA with **maximum** 80 objective evaluations, each 256 full binary shots. Every infeasible output counts. Best noisy objective determines the retained logits. A disjoint 4096-shot evaluation uses seed+10000. Exact diagnostic probabilities are evaluated only after selection. Actual evaluations are recorded because COBYLA can converge early; these unequal realized costs are not an equal-budget comparison.

| n | lambda | seed | evaluations | training shots | heldout feasible/4096 | heldout optimum/4096 | exact P_success | best valid cut |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 0.1 | 101 | 39 | 9984 | 1466 | 503 | 0.115018 | 1 |
| 4 | 0.1 | 102 | 46 | 11776 | 1900 | 1701 | 0.404094 | 1 |
| 4 | 0.1 | 103 | 40 | 10240 | 1529 | 550 | 0.133926 | 1 |
| 4 | 1 | 101 | 35 | 8960 | 1531 | 480 | 0.108491 | 1 |
| 4 | 1 | 102 | 49 | 12544 | 3808 | 3808 | 0.924558 | 1 |
| 4 | 1 | 103 | 47 | 12032 | 3982 | 3982 | 0.973982 | 1 |
| 4 | 10 | 101 | 34 | 8704 | 1531 | 480 | 0.108492 | 1 |
| 4 | 10 | 102 | 40 | 10240 | 1492 | 583 | 0.142955 | 1 |
| 4 | 10 | 103 | 47 | 12032 | 3954 | 0 | 0.000108705 | 2 |
| 6 | 0.1 | 101 | 60 | 15360 | 477 | 85 | 0.0224951 | 1 |
| 6 | 0.1 | 102 | 75 | 19200 | 3279 | 3235 | 0.787235 | 1 |
| 6 | 0.1 | 103 | 58 | 14848 | 1153 | 153 | 0.0370191 | 1 |
| 6 | 1 | 101 | 75 | 19200 | 3444 | 19 | 0.00309706 | 1 |
| 6 | 1 | 102 | 76 | 19456 | 2575 | 2448 | 0.608213 | 1 |
| 6 | 1 | 103 | 50 | 12800 | 1247 | 94 | 0.024725 | 1 |
| 6 | 10 | 101 | 78 | 19968 | 3944 | 0 | 2.55826e-05 | 4 |
| 6 | 10 | 102 | 71 | 18176 | 3363 | 1 | 0.000222585 | 1 |
| 6 | 10 | 103 | 60 | 15360 | 1607 | 223 | 0.0523926 | 1 |
| 8 | 0.1 | 101 | 68 | 17408 | 1116 | 31 | 0.00685402 | 1 |
| 8 | 0.1 | 102 | 80 | 20480 | 7 | 1 | 3.82197e-05 | 1 |
| 8 | 0.1 | 103 | 64 | 16384 | 979 | 26 | 0.0047432 | 1 |
| 8 | 1 | 101 | 69 | 17664 | 1171 | 32 | 0.00686349 | 1 |
| 8 | 1 | 102 | 74 | 18944 | 1243 | 14 | 0.00448198 | 1 |
| 8 | 1 | 103 | 80 | 20480 | 1889 | 3 | 0.00118551 | 1 |
| 8 | 10 | 101 | 78 | 19968 | 1255 | 33 | 0.0085718 | 1 |
| 8 | 10 | 102 | 74 | 18944 | 1157 | 9 | 0.00329984 | 1 |
| 8 | 10 | 103 | 75 | 19200 | 1239 | 10 | 0.00350849 | 1 |

Negative results: training is sensitive to lambda, seed, and SciPy implementation. Canonical Python 3.11 / SciPy 1.17.1 runs are tabulated above; all failed seeds and traces are retained. In the canonical run n=6, lambda=10, seed101 has 3944/4096 feasible outcomes but no optimum, best valid cut 4 versus optimum 1, and exact success only 2.558e-5. At n=4, lambda=10, seed103 has 3954/4096 feasible outcomes and no optimum. Feasibility and large penalty alone do not imply computational quality. The prior Python 3.9 / SciPy 1.13.1 run is preserved separately at `experiments/validation/objective_penalty_audit.python39.json`: n=8, lambda=.1, seed102 gave feasible mass .00176622, success 1.87054e-5, and only 7/4096 heldout shots feasible with no optimum. This version sensitivity prohibits treating individual favorable seeds as robust algorithmic evidence.

At a fixed beta, feasible Gibbs conditioning is lambda-independent because every feasible string has zero penalty; increasing lambda changes feasibility, not the relative Gibbs weights within the feasible sector. This simple energy fact must not be claimed as a new photonic mechanism.

## Reproduction, provenance, and API

```sh
PYTHONPATH=src .venv/bin/python experiments/validation/objective_penalty_audit.py
.venv/bin/python -m pytest tests/test_objectives.py tests/test_penalty.py -q
```

Run timestamp `2026-11-20T17:45:49.366759+00:00`, base Git `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508` with dirty state recorded. Raw JSON contains input SHA256 before/after, all logits and objective traces, heldout counts, Wilson intervals, platform, software versions, and runtime. Targeted tests: **24 passed** in Python 3.11.15 / NumPy 2.4.6 / SciPy 1.17.1. The previous Python 3.9 raw run is preserved and is not the canonical table.

Public API: `.bitstrings` (2**n by n), `.energies(edges)`, `.probabilities(logits)`, `.metrics(logits,edges,optimal_energy=None)`, `.qubo_coefficients(edges)`, `.sample(logits,num_shots,edges,seed)`, `.optimize(edges,num_iterations,seed,method,shots_per_evaluation)`. The `num_iterations` argument is the evaluation cap. Supported optimizers: COBYLA, Nelder-Mead, random. Finite logits are clipped to Bernoulli probabilities [1e-12,1-1e-12], retaining full support.

The authentic penalty optical comparator remains **OPEN**. `obliq_circuit_depth=None` is intentional. A fair eventual comparison must include all optimization/heldout shots, same graph instances, disjoint evaluations, and optical preparation resources. There is no present evidence supporting superiority over ObliQ.
