# Synthetic N13/17 qualification of the continuous-phase marginal oracle

Result: **PASS on all12 frozen synthetic cases /24 oracle evaluations.** This
qualifies finite numerical consistency and observed row costs, not a graph
optimizer, independent physical replication, hardware readiness or a new
mathematical theorem. No P46/P47 development observation entered the run.

Oracle source remains UNCHANGED at427d984, SHA256
`263cfe954645f4a5de6edb5beedcaa4b8766d1a364d46f45d150639977c6efb0`.
The resource script and contract froze before execution at
`cccad410c9ab9a9fe7bbd26fe8be57bc8fb33129`. The actual run repository revision
is4d4195e, which only adds the separate mathematical review after that freeze.
All three execution-artifact hashes match before/after.

One authorized bounded Mathbox run, with CPU15/wall25/thread1/log2MiB, is saved
at `research/P47_conditional_phase_resource/run_001`. Its v2 manifest validates
against this worktree: `completed`, exit0, all results present, unchanged inputs.
Observed runner wall0.315399s; inside-script CPU0.140589s and wall0.219204s.
All saved files total209981 bytes, below2MiB. The numerical slot was explicitly
released after completion; no automatic retry occurred.

The actual child command was

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python research/P47_conditional_phase_resource.py \
  --output research/P47_conditional_phase_resource/run_001/data
```

Inputs are N13/17, each with uniform q, normalized ramp1..N, or pointmass q,
at transfer probability1/4 and1/2. Each is evaluated at80 and120 digits.
Uniform rows are ALSO checked against a distinct exact Fraction calculation:
univariate polynomial powers conditional on the active count, weighted by its
Binomial distribution. Pointmass rows use an exact binomial-mixture reference.
Ramp rows have no independent exact high-N reference here; they receive the
cross-precision, positivity, normalization, c0, mean and active-sector checks.

| Observed quantity | Decimal80 | Decimal120 |
|---|---:|---:|
| Maximum error against available exact references | 3.24e-80 | 4.38e-120 |
| Maximum mean error against p | 3.51e-80 | 2.87e-120 |
| Maximum PMF normalization error | 2.46e-80 | 2.55e-120 |
| Minimum raw PMF entry over these inputs | 7.04e-32 | 7.04e-32 |
| Maximum measured oracle time per row | 14.6ms | 34.4ms |
| Sum of12 measured oracle row times | 74.4ms | 103.1ms |

Maximum80-versus120 discrepancy: PMF3.24e-80, CDF2.82e-80. All first coefficients
c0 are1, active-count laws match the exact Binomial source selection, and CDFs
are normalized/nondecreasing. Raw records and individual timings are retained;
do not call a maximum/aggregate from these few rows a throughput guarantee.

These errors concern rational synthetic inputs, not uncertainty in a numerical
physical matrix or actual hardware. The API explicitly allows only tiny
row-sum corrections, reports them and rejects gross input/PMF errors. It uses
Decimal arithmetic rather than intervals and makes no relative-tail certificate.
At120 digits the test's reference conversion uses160-digit arithmetic; the
comparison is a finite rational reference, not another Decimal80 DP.

The control model is continuous uniform phases, equivalently l+1-th roots in
each l-active sector. Replacing P46/P47's four-root sampler would CHANGE that
control model at l>=4 and requires a new explicit frozen source/spec; it is not
a new CDF for the old distribution. For a general isometry row of mass mu<1,
this API's unit-sum q requirement is not satisfied: do not silently renormalize
that row or identify mu with the Bernoulli transfer probability. A separate
global mean-field marginal with subunit row mass needs its own API/contract.
No existing P46/P47 data, manuscript or shared scientific state was modified.
