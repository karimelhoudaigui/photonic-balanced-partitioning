# Density floating semantics: coordinator self-review

Finite assertion verified; no interval certification. Exact theorem unchanged.
Source: density evaluator at77a8588; run source85b3414 with dirty new audit files.
The fresh reviewer requested on this continuation was usage-quota blocked.
This is a coordinator self-review, not a substitute for that independent pass.

The positive-sum fix removes the previously observed cancellation at angle
1e-10. It cannot make arbitrary complex128 evaluations rigorous upper bounds.
For a rational rotation t=2^-600, cos=(1-t²)/(1+t²), sin=2t/(1+t²), the exact
two-column frame is orthonormal. Pad its two active rows by two zero rows:
m4,k2, every positive row intensity is exactly one. Its complete bosonic and
distinguishable laws have TV=2cos²sin²>0 and M=4cos²sin².
When this physical rational frame is rounded to complex128, squaring the tiny
off-diagonal entries underflows. The evaluator returns zero estimates for M,
leakage and the refined TV bound. Its residual also rounds to zero. The exact
positive TV is retained as a rational numerator/denominator in raw.json.
Thus a zero floating residual does not certify an exact physical input, and
a zero returned estimate is not an outward-rounded upper bound. The returned
FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED label is necessary and appropriate.

Eight fixed scalar envelope values were additionally compared with 90-digit
Decimal evaluations at their exact binary floating inputs. These are roundoff
diagnostics, not a proof of an interval enclosure. The exact-series remainder
in the algorithm controls truncation, not floating arithmetic in every step.
The witness is outside the preregistered P33 grid scale; no material failure
of that finite grid or counterexample to the exact theorem follows.

Execution: `experiments/P33_density_float_review/run_002/manifest.json`, completed.
The first `run/manifest.json` is preserved as failed: missing PYTHONPATH, before
any mathematical assertion executed. The successful command adds PYTHONPATH=src
and uses the same bounded runner, source and exact witness. Reproduce with:

```sh
PYTHONPATH=src .venv/bin/python experiments/phase3_density_float_review.py \
  --output /tmp/density-float-review-new.json
```

The script refuses to overwrite its output. Zero physical shots; no manuscript
or QPU changes. A bit-rigorous certificate still requires an explicit input and
arithmetic error budget. No ad hoc epsilon is presented as that missing proof.
