# Independent float64 review of density estimates

**Outcome:** implementation and finite assertion checked in the stated range,
conditional on the high-precision numerical reference; not interval-certified.
The positive-sum correction removes the earlier theta=1e-10 cancellation.
`FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED` correctly describes the remaining
outputs. Explicit counterexamples to interpreting them as rigorous numerical
upper bounds remain, and are preserved below. The exact density theorem is
not refuted or re-proved by this audit.

Reviewed revision: `77a858821710192791b8f23a0b15218e2223f13a`.
Source: `src/photonic_balanced_partitioning/photonic/density_certificate.py`,
SHA256 `6705d826b72dbf3883d0a4e123af191b41c22ab478878dce6a23395596f5d461`.
Reviewer `/root/physics` did not author this correction. Its production source
was read-only in isolated sparse worktree `phase3-density-float-review`.

## Formula and semantics checks

The new pair expression is `2 sum_(i,a<b) q_ia q_ib`, evaluated with suffix
sums; it equals the exact M without subtracting nearly equal row moments.
The leakage is the sum of all entries except one maximizing column per row,
which equals exact delta even at ties. Unary inputs give empty pair sums and
zero leakage. These changes remove the identified cancellation mechanism, but
ordinary rounding and underflow still affect nonnegative sums and products.

For small sigma the recurrence used is correct: with a_n=!n/n!, a_0=1,
a_1=0, one has a_n=((n-1)a_(n-1)+a_(n-2))/n. Summing degrees2 through12
and adding sigma^13/(1-sigma) majorizes the omitted positive tail in **exact
arithmetic**, since 0<=a_n<=1. The factor one half is correct. This is not a
proof of outward rounding for the implemented floating recurrence, powers,
sum or tail. For 0.1<=sigma<1 the log1p/expm1 formula avoids the earlier
small-sigma cancellation; sigma>=1 returns the trivial one. Invalid negative
or nonfinite sigma is rejected. No error enclosure is returned.

Every tested density result carries the explicit non-interval semantics field
and an orthonormality residual. This is an honest qualification. The older
docstring terms "bounds" / "certificate" and `non_claim` prose do not override
that field: stripping the qualifier would produce an unsupported numerical
claim. The input tolerance admits approximately orthonormal floating matrices;
it is not exact projection onto the physical Stiefel manifold.

## Bounded independent numerical checks

No production sampler or density function was used to define the reference
physical laws. Scalar f(sigma) was independently evaluated at 800 decimal
digits using mpmath; two-photon physical TV was derived as
2 cos(theta)^2 sin(theta)^2 for the four-mode rotation family. The exact binary64
theta was converted to high precision before evaluating this ideal normalized
family. The supplied floating frame approximates that family, so differences
also include frame construction error. The scalar comparisons isolate the
envelope function independently of frame error.

The deterministic grid contains 588 unique scalar inputs: logarithmic small
values down to subnormal numbers, values around 0.1 and its adjacent floats,
values approaching one from both sides, and interior values. It is a finite
grid, not exhaustive coverage. Four invalid inputs were rejected. Separately,
174 physical-family cases include theta=0,1e-10,1e-16,1e-162 and values
through pi/4. Unary and underflowed-small-row cases were also retained. No
Monte Carlo, parameter fitting, local model or QPU was used. CPU time was
1.282181 seconds, below the authorized120-second bound; no rerun sweep followed.

Observed results:

- At theta=1e-10, M is approximately2e-20 and delta2e-20 rather than zero.
  The direct Gram estimate is2.0000000003771235e-20, above the reference
  physical TV2.0000000000000001457e-20. The original witness is corrected.
- At sigma=0.8542372881355932, the returned scalar value is
  0.9599333324186494 versus high-precision reference approximately
  0.9599333324186495829448448605. The deficit is approximately1.62e-16.
  Thus even the scalar envelope function is not always rounded upward.
- Of 588 scalar cases,395 lie below the high-precision scalar reference;
  241 positive-reference cases return zero through underflow. These counts
  describe this grid, not a failure probability or a physical error rate.
- At the 0.1 branch boundary there is a small downward jump: the preceding
  float0.09999999999999999 returns0.0026874544644571023, while0.1 returns
  0.0026874544644219863. The conservative exact-series tail accounts for the
  extra approximately3.5e-14 just below the cutoff. Both of these values are
  above their references, but the computed function is not monotone there.
- At theta=1e-16, direct/support/refined estimates are
  1.9999999999999998e-32, below the ideal physical TV by approximately7.8e-49.
  This illustrates ordinary rounding/frame error, not a sizeable absolute
  failure. The coarse density estimate still has ample slack in this case.
- At theta=1e-162, all returned estimates are zero while the ideal physical
  family's TV is approximately2e-324. This is below the smallest positive
  binary64 subnormal, so a zero approximation is unsurprising; an exact upper
  enclosure would nevertheless need a nonzero conservative value.
- 146 of the174 family cases have at least one estimate below the ideal
  physical-family TV. This aggregates tiny rounding and underflow effects;
  it is not evidence against the exact theorem.

Near sigma=1 the cap returned one throughout the tested saturated region;
no NaN, overflow, or exception occurred on this finite valid-input grid. No
universal error bound or guarantee outside the tested inputs is inferred.

## Artifacts, command and provenance limitation

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python experiments/P33_density_float_review/check.py
```

Python3.11.15, NumPy2.4.6; exact mpmath version and platform are in the retained
manifest. Source and script hashes recorded before and after execution agree.
The complete scalar and family results are retained, including negative
findings. No production source or tests were changed.

| Artifact | SHA256 |
|---|---|
| `check.py` | `4f7ff3813eff12e7fb3b12c159a7bbe50064e28eefc50a44277b5dc49e841285` |
| `receipt.json` | `014b4e38244393c8c7c0e50f160651c3b746b91a3c9a2e8810ef81180818dab9` |
| `summary.json` | `e54a081902dfce998de256ddc605e795a4934dc7b2625711746edefe4f64d59a` |
| `manifest.json` | `5f1ce2a77973ef0c78ce75e3eeb7d9e302b2f748cbd6419094836c2221f8427a` |

Provenance limitation retained explicitly: although the manifest records run
status completed and stable hashes, its `declared_results` list is empty.
The v2 validator therefore rejects it with "result outputs must have been
declared before execution". It is **not a valid v2 evidence record**. The
script's fixed output paths, full receipts and input hashes remain inspectable;
this report does not silently repair or relabel that original run. No numerical
rerun was needed or performed to conceal the metadata defect.

The safe conclusion is numerical robustness improved at the original witness,
with ordinary float64 limitations correctly acknowledged by the machine-readable
status. Rigorous outward-rounded certification would require a separate design
and error analysis. Larger sweeps or hardware cannot supply that missing proof.
