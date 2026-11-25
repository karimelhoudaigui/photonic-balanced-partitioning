# P53b synthetic exact qualification receipt

**20 tests PASS in 2.16s.** One authorized qualification, no retry. This
qualifies the wrapper's finite exact/mocked guards; no physical P53 x=1/4
target was evaluated and no native LP solve occurred. No point membership,
separation, optimization benefit or hardware result is established here.

Source froze at clean commit bb0ba2d6d08c31d096b79fac58886f113d24f8f3.
ROOT and physics independently read the complete source/tests/contracts and
returned static PASS before ROOT authorized the exact prospective command.

Frozen SHA256:

- Source: 66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908.
- Tests: ff5ff9b1723644e6f7838178f10321e5184fb74aaa540faa6b5521a2ddcf9c90.
- Preflight contract: ae227fc5bbaf88c4fc10a393fdd04df70a4bd4071a3e0d6b97d6565535ca98c1.

Actual child command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q \
  tests/test_p53b_fixed_point.py \
  --junitxml=research/P53b_fixed_point_preflight/run_001/junit.xml
```

The Mathbox runner enforced CPU20s/wall30s/thread1/log4MiB with a fresh output
directory. Manifest research/P53b_fixed_point_preflight/run_001/manifest.json
records completed/exit0, wall2.515677s, clean source, all 14 before/after input
hashes unchanged and declared JUnit present. The v2 validator returned
`valid evidence record`. Stderr is empty. The numerical slot was explicitly
released immediately after validation, before this documentary scellage.

The tests cover canonical rationals, synthetic balanced Horner identities,
complete endpoint labels/schema, hash/JSON/inflation rejection, binary dual
conversion/rescaling, all-vertex strict gaps, exact nonnegative graph shifts,
LP signs/options/readback via mocks, invalid warnings, timeout/failure gates,
changed exact primal weights despite a float NO_MATCH, contradiction guards,
fixed caps and exclusive bounded gzip output. Synthetic inputs and mocked
solvers supply every test case. The two real P53 gzip artifacts were hashed
by the runner only; tests did not decode them or compute their target.

The source, provider, spec, point, witness rule and budgets remain unchanged.
No main or extra LP/point/grid is authorized by this PASS. ROOT must inspect
this receipt and separately authorize the single bounded main. P53's prior
inconclusive continuous certificate search remains preserved.
