# P50 from-raw controls — qualification receipt

**21 tests PASS in 0.46s.** One authorized bounded qualification, no retry,
DEV graph, held-out panel, photonic sample or performance benchmark. This is
finite helper qualification, not a classical optimality or quantum claim.

API/prospective contract froze at `f34c9d3`; implementation at `acd6839`.
ROOT static review found the best should be available ONLINE before final
trace export. Its approved prequalification correction froze at
`5f6cce8d025fc1b438788619c2cbde2078d6a8fd`, with no RNG/search/seed change.
No tests or numerical work occurred before that correction/source review.

Source was clean at that commit. Exactly three unchanged before/after inputs:

- `research/P50_fast_from_scratch.py` SHA256
  `6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86`
- `tests/test_p50_fast_from_scratch.py` SHA256
  `d70a3a37856312177c0c8c6f905a5504ff2cd776d70de2e08bf663a941381aa8`
- `research/P50_fast_from_scratch_contract.json` SHA256
  `13e3f69d3073b5c5f42cc6a524e9566d9889b49d79f0b1708e65bce5d6fced5a`

Actual child command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q \
  tests/test_p50_fast_from_scratch.py \
  --junitxml=research/P50_fast_from_scratch_qualification/run_001/data/junit.xml
```

The Mathbox runner enforced CPU30s/wall50s/thread1/log4MiB with a fresh output.
Manifest `research/P50_fast_from_scratch_qualification/run_001/manifest.json`
records completed, exit0, observed wall0.706147s, all three hashes unchanged,
all declared results present. Its v2 validator returned `valid evidence record`.
The numerical slot was explicitly released immediately after validation.
Test duration is recorded provenance, not evidence of algorithm speed.

The helper is autonomous NumPy; it does not call/import P49's given-incumbent
solver. Its `solve_from_raw(adjacency, *, seed, initialization="random",
cpu_budget_seconds, max_proposals=100_000_000)` accepts NO incumbent, priority,
marks or eigensystem. Modes `random` and `spectral` run/pay separately. Raw
conversion/validation, own seeded priorities/marks, spectral preparation when
selected, actual initial cut and vectorized descent all precede annealing and
are measured from API entry. `json_safe_result` is called AFTER solve.

Independent Python edge sums verify all balanced states/cross-swaps on fixed
N6/N10 fixtures and100-swap cache sequences. These fixtures are predetermined
small tests, not graph-population searches and do not compute an optimum.
Other tests cover fixed-work reproducibility, every trace cut/mask, internal
carried-priority semantics, source-owned spectral construction, first scans,
zero/N2 graphs, restarts and safe raw-input casting/overflow/error cases.

Deterministic virtual clocks verify late validation/initialization returns
NO eligible result, late scans cannot improve an earlier prefix, and scans
without improvement still produce a checkpoint. An online-cache fixture
forbids unpacking a best from exported traces. CPU/wall export is separate;
compute totals/overruns remain visible. The best cost/subset is fully prepared
before its checkpoint clock and cached when admissible. This is an ANYTIME
RAM-prefix comparison, not a guarantee of physical return exactly at deadline.
Virtual clocks affect only this module, not pytest or the bounded runner;
there is no runtime performance assertion.

An early guard (including insufficient room for a full required scan) or no
eligible initialization sets acceptance flags false. `best_cut/best_subset`
can therefore be None. The caller must handle this, use only eligible cached
fields, and never use late overall best or a free best-of-two portfolio.
The caller owns its strictly B-only wall-derived CPU allowance and pays its
adapter; the helper never estimates/increases B's budget. No new P50 primary
run, held-out program, paper/GitHub or QPU operation is authorized by this
receipt. Full repository checks remain a separate pre-merge obligation.
