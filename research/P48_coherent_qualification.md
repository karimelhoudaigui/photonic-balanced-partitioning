# P48 coherent marginal helper — exact-fixture qualification

Result: **26 tests PASS in0.17s**:24 independent exact fixtures and2 additional
subunit/invariant/input-validation tests. This qualifies the new numerical
helper on the stated small inputs. It is not an optimization result, independent
physical replication, numerical high-r benchmark, novelty claim or QPU gate.

The source and contract froze BEFORE execution at
`6c980d3f684ef32295eeb394272f6218fbbc2402`, branch `research/p48-adaptive`.
Module: `research/P48_coherent_marginals.py`, SHA256
`a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac`.
Neither that module nor the old427d984 conditional-phase oracle was modified
after qualification.

The APIs are `fixed_phase_marginal(q,precision=80)` and
`spherical_marginal(mu,r,precision=80)`. They return Decimal PMF/CDF and
explicit correction diagnostics. Phase preserves subunit sum(q)=mu, with ZERO
input normalization; sphere uses a positive beta-binomial/thinning mixture.
Fraction validation preserves exact rational row masses before Decimal work.
The source photon count/dimension is r; r0, r1, mu0 and mu1 are explicit.
In particular mu1,r>1 is not automatically a deterministic occupation.

One coordinator-authorized run used the bounded Mathbox runner with exactly
three frozen inputs, CPU30/wall50/thread1/log4MiB, clean source and a fresh
output directory. The actual child command was

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q \
  tests/test_p48_coherent_marginals.py \
  --junitxml=research/P48_coherent_qualification/run_001/data/junit.xml
```

The v2 manifest at `research/P48_coherent_qualification/run_001/manifest.json`
records `completed`, exit0, observed wall0.438374s, all results present and all
three before/after hashes unchanged. Its validator passed against this worktree.
The numerical slot was explicitly released before log/hash aggregation.

The12 phase reference cases exhaust all(r+1)^r phase tuples at r<=3 and
use exact cyclotomic norms plus exact binomial probabilities. They include
vacuum, uniform full/subunit rows, pointmass and a nonuniform subunit row.
These are averaged-count equivalents of continuous phases; a four-root sampler
at r>=4 is a DIFFERENT model and is not qualified by these marginal tables.

The12 spherical reference cases instead integrate Binomial(r,mu*x) directly
against the Beta(1,r-1) density by rational polynomial expansion. This is
independent of the production positive-mixture recurrence. r0/r1 are tested
separately, with mu0 and mu1 included. Both models agree with their exact
references within1e-60 and retain correct means mu. Additional checks reject
invalid rows/parameters and explicitly catch an accidental row-to-one map.

All qualification arithmetic references use Fraction; production uses Decimal80
on supplied numerical inputs. Returned PMF/CDF corrections have a strict small
budget, but this is not interval arithmetic or a relative-tail certificate.
If a caller projects a tiny row-mass overflow from numerical matrix error, that
is separate EXPLICIT caller work: it must be recorded and cannot rescale any
genuinely subunit row. No development graph, eigensolver, photon sample,
historical experiment, P46/P47 sampler or manuscript was used or changed here.

The active P48-B spectral-basis card is a prospective hypothesis. These helpers
make its classical coherent-field controls analytically calibrated; they do
not establish a bosonic graph-optimization mechanism. All development and
held-out scientific/resource/replication gates remain separate obligations.
