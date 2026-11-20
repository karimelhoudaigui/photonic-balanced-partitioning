# Objective validation

Status: PASS for ideal exact-distribution implementation and tested regression cases. This is not a scientific performance gate.

Run: `2026-11-20T17:45:49.366759+00:00`; base Git `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`, dirty working tree. Raw evidence: `experiments/validation/objective_penalty_audit.json`. Input hashes before/after agree.

## Definitions and corrected bugs

- Conditional energy is `sum_CF p*C / P_CF`; zero collision-free mass returns infinity. The unnormalized sum remains a diagnostic and is never the minimization target.
- Physical success is `sum_CF,opt p`, factored as `P_CF * P_opt_given_CF`. The optimum is obtained by exact enumeration for diagnostics; using it in training supplies an explicit classical optimum oracle.
- Collision-aware energy is `E_CF + mu*(1-P_CF)`; the log barrier is `E_CF - gamma*log(P_CF+epsilon)`. The negative sign discourages rejection.
- CVaR is the mean of the **lowest** alpha probability mass after conditioning on CF; it respects unequal weights and splits the probability atom at the quantile. Empty/no-CF samples return infinity.
- CollisionAwareSolver now computes actual collisions, preserves collision shots, passes seed by keyword, and uses the full Fock basis. CVaR sampling indexes the filtered valid samples, avoiding partition/energy mismatches.
- Fixed-circuit independent binomial Wilson intervals are inverted to give uncertainty on `1/P_success`; zero observed successes gives an infinite upper bound. This is not a training-seed uncertainty interval.

## Executed falsification cases

| CF / optimal masses | E_CF | Unnormalized CF energy | P_success | Expected attempts | CVaR_0.5 |
|---|---:|---:|---:|---:|---:|
| [0.5, 0.5, 0.0] | 2 | 2 | 0.5 | 2 | 1 |
| [0.05, 0.05, 0.9] | 2 | 0.2 | 0.05 | 20 | 1 |
| [0.01, 0.0, 0.99] | 1 | 0.01 | 0.01 | 100 | 1 |
| [0.9, 0.0, 0.1] | 1 | 0.9 | 0.9 | 1.11111 | 1 |

The leakage pair reduces the bad unnormalized objective by ten times while making physical success ten times worse. Conditional energy is unchanged, while the collision-aware and barrier objectives worsen. The final pair has identical conditional energy and conditional CVaR but expected attempts 100 versus 1.11111: neither conditional objective guarantees usable physical success. CVaR alone is therefore not a hardware success metric.

An independent weighted quantile regression uses energies `[1,4,9]`, weights `[.2,.5,.3]`, alpha=.5. The exact lower-tail value is `(1*.2 + 4*.3)/.5 = 2.8`; alpha=1 gives 4.9.

## Reproduction and limits

```sh
PYTHONPATH=src .venv/bin/python experiments/validation/objective_penalty_audit.py
.venv/bin/python -m pytest tests/test_objectives.py tests/test_penalty.py -q
```

Observed targeted result: **24 passed** in the project environment (Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1). A prior system-Python run also passed; its differing penalty-training outputs are preserved at `experiments/validation/objective_penalty_audit.python39.json`.

The revised Haar helper optimizers report exact-distribution objective calls and zero physical shots. This is simulation mode, not a finite-shot hardware optimization. Their per-iteration distribution is computed once and reused for energy diagnostics.

Gate limitations: losses, detector models, source impurities, optimization enrichment, and comparisons with authentic ObliQ remain separate obligations. No QPU was accessed.
