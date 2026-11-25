# P49 efficient feasible control — qualification receipt

**PASS: 15 tests in 0.43s**, with independent scalar edge-sum references.
No DEV graph, held-out graph, photonic simulation or performance comparison was
run. This establishes the bounded qualification below, not an optimality,
speed, optimization-advantage, hardware or novelty claim.

API card froze at `9765ff9`; module/tests froze at
`0bc492e2442e9b5146fa52e275ed058dbfa9832e`. The first bounded-run invocation
failed its contract schema BEFORE starting pytest: `random runs need generator
and seed`. The singular `randomness.seed` field had been omitted while the
fixed list was already in `randomness.seeds`. Full argv, stderr and original
source/input hashes are preserved at
`research/P49_fast_classical_qualification/prelaunch_001.json`. No test or
scientific result was produced by that refusal, and no automatic retry occurred.

ROOT explicitly authorized adding ONLY the missing seed field and running a
second fresh output with identical tests and caps. The contract fix and failure
receipt froze at `82de1cba1662e6bbb2a42039d5b61cedf880f5c4`; source was clean.
The actual second command was

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q \
  tests/test_p49_fast_classical.py \
  --junitxml=research/P49_fast_classical_qualification/run_002/data/junit.xml
```

The contract's original illustrative `planned_command` retains `run_001`;
the runner manifest records the actual authorized argv/output `run_002`.
Bounded Mathbox runner: CPU30s, wall50s, threads1, logs4MiB, exactly three
declared inputs, fresh output. Manifest `run_002/manifest.json` records completed,
exit0, wall0.680146s and all before/after hashes unchanged. Its v2 validator
returned `valid evidence record`. Timing here is a receipt, not a benchmark.
The numerical slot was explicitly released immediately after validation.

Qualified input SHA256 values:

- `research/P49_fast_classical.py`:
  `018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff`
- `tests/test_p49_fast_classical.py`:
  `50bb0c50234934260ccd88cf065dd9752b959a7f447f81fda1a63c132f437621`
- `research/P49_fast_classical_contract.json`:
  `5f5e670e512c891945c83fd4e46419fcde4527330b31bb6bd9a21a92dbce1021`

On seeded N6/N10 integer fixtures, all balanced states and cross-swaps were
checked against scalar undirected edge sums. No minimum/known optimum was
computed or passed into search. Independent signed-neighbour sums and direct
cuts also verified 100-swap cached-update sequences per size. Fixed-count runs
verify identical seeded trajectories/counters, every packed trace incumbent's
feasibility and exact cut, monotone best cuts and complete safety-cap accounting.
There are no elapsed-runtime assertions. Deterministic virtual clocks test late
batch exclusion and inconclusive early cap/wall safeguards. Further cases cover
priority-carried relabeling, zero graphs/N2, source/Cref/type/overflow validation
and JSON conversion after solve.

Integration API:

```python
solve_balanced(adjacency_int64, incumbent_subset, *, seed, max_proposals,
               cpu_budget_seconds=None, wall_budget_seconds=None,
               incumbent_cost=None, vertex_priority=None)
json_safe_result(result)  # outside measured compute
```

**`vertex_priority[v]` is the priority/rank of vertex v.** It is not a list
`order[rank]=vertex`. Convert such an order via `np.argsort(order)` and carry
the resulting per-vertex vector under relabeling. The qualified relabel test
uses that convention. Graph conversion to int64, if needed, is caller work.

Return `best_cut/best_subset` is the best completed pre-deadline checkpoint,
with overall late discoveries separately labelled for audit. Full K² scan and
anneal-chunk improvements are credited at completion, not backdated. CPU and
wall cover validation/setup/search/compact traces; JSON conversion and disk I/O
are outside. The finite proposal cap is only a guardrail: if reached before
the CPU allowance, `early_cap_inconclusive` prevents using this comparison to
accept a positive. `early_wall_inconclusive` handles an early wall safeguard.
Root's conservative allowance convention may grant CPU equal to the measured
B common-frontend plus classical processing WALL, excluding optical-backend
simulation and audit serialization. This must remain explicit; the helper
does not establish total-resource equivalence or fill in hardware costs.
