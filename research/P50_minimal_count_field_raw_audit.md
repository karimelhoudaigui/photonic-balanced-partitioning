# P50 post-hoc raw consistency receipt

**PASS_CONSISTENCY: 53,205 checks in113 groups on2,560 primary events; zero
failed checks/fatal errors.** This is consistency evidence, not a positive,
statistical confirmation, blinded audit or independent physical replication.

Provenance is explicitly POSTHOC. I had prepared the checking plan from the
frozen protocol/primary schema and communicated it before results, but received
the author's negative-sign summary before freezing audit source. No result
file was opened during authoring and no new budget/grid/graph/sample was
introduced. Do not describe this audit as preregistered before P50 outcomes.
I authored the FAST helper/proposed decoder; physics separately audited them.
This independent-code check does not remove that shared-context relationship.

Audit code/contract froze at `72009eae2182a9afa4b1066c95da288b639f251e`:

- `research/P50_minimal_count_field_raw_audit.py` SHA256
  `129128d37c04fb53dd9f3305d3d55c81fc090b127d78bab3d4ec979e0b48266b`
- `research/P50_minimal_count_field_raw_audit_contract.json` SHA256
  `43509bf72f186c358ca517207562a2bd2969d9d1710759bad83ecc7a26652777`

After ROOT reviewed the full code/contract, it authorized an immutable import
of data commit `fb5a36ec0746c3465dc7ee3a3c6b88a86b490e7d`. That exact cherry-pick
is local commit `a8e40641cea8b6c967b0bb4915c282d9b5d4d502`, clean before run.
It imports only sealed experiment data/manifest/logs. Audit source remained
unchanged. Original main source was5310257, primary SHA256
`6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf`.

ONE explicitly authorized run used the pinned Python and bounded Mathbox
runner: CPU20s/wall30s/thread1/log4MiB, fresh output, exactly17 inputs (code,
contract, main manifest and14 data files). Actual child command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python \
  research/P50_minimal_count_field_raw_audit.py \
  --data experiments/P50_minimal_count_field/run_001/data \
  --output research/P50_minimal_count_field_raw_audit/run_001/data/audit.json
```

Audit manifest `run_001/manifest.json` records completed/exit0, observed
wall1.579610s, all17 before/after input hashes unchanged, results present.
Its v2 validator returned `valid evidence record`. Audit CPU1.287177s is a
receipt, not a benchmark. No retry was needed. The exclusive numerical slot
was explicitly returned immediately after validation.

The auditor imports ONLY stdlib/NumPy, never primary/helper code. Independent
scalar edge sums and max-anchored bucket sorting validate all raw fitness and
decoded partitions. Exact Fraction aggregation checks all10 training grids,
equal graph weights, losing shots, canonical selections, fresh role hashes,
evaluation allocations and private paid minima. It checks recorded spending
subtotals and both B-only allowances without changing the budgets.

Vectorized identities check source geometry, occupied marked eigenvectors,
gauge/rotation, q/mu/H, actual Gaussian factors/propagated variances and PMF
mass/CDF/binomial moments. The latter uses
E[binom(n,h)]=h!e_h(q), not the author's alternating inversion routine.
Physical fixed-r counts and unconditioned independent-marginal totals are
distinguished. Every saved FAST best mask/cut and eligible/null/late prefix is
checked, with online-cache labels and export/total timing partition retained.
All main result hashes and the original unchanged-input declaration match.

Limits are preserved in `run_001/data/audit.json`: no RNG/graph trajectory
redraw, external timing profiler, every-proposal replay, interval/relative-tail
certificate, fresh simulation or hardware experiment. Observed fields are
checked against recorded observations; no claim of authenticating each random
draw from its seed follows. Geometry/PGF checks use the frozen tolerances,
not a general sampler theorem. Full-P50 scientific conclusions still require
their scoped negative interpretation; this consistency PASS does not meet the
user's unresolved positive/held-out/physical-replication objective.
