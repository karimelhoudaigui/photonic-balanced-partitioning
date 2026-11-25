# P53d exact triangle candidate: independent reconstruction PASS

25-Nov-2026. **EXACT_INDEPENDENT_TRIANGLE_REPLAY_PASS**, one authorized replay,
no failure/retry. Signed uniform lower bound **57/32768** and the same old
normalized-graph lower bound **57/458752** are independently confirmed.

For the ONE fixed N8 B point at pi/3, same saved w=(X04-X15)/2 and same U8
architecture, the reconstructed inequalities are

    E[b4(G),phi](w)-E[B,pi/3](w) >= 57/32768 > 0

for all35 complementary4+4 species groupings and every real phi, with the
included uniform control also above this bound. The saved nonnegative graph's
corresponding expected-cut gap is at least57/458752. These are proved lower
bounds, not claims to have optimized or attained the minimum phase margin.
The fixed B mean is exactly -767/327680 under w.

## Independence and exact scope

The checker imports NO production module. It rebuilt every four-photon
creation coefficient from24 monomials of the permanent, dividing exactly by
output multiplicity factorials, and reconstructed all Laurent probabilities.
It rebuilt the decoded scalar by enumerating all70 balanced subsets and ALL
max-count ties, then M and the scalar spectra using two bounded integer
einsum calls and Python-int anti-diagonal folds. All35 proofs used the
triangle inequality; no unused Bernstein branch, phase search or LP ran.

Actual verified coverage:23100 creation patterns,300300 Laurent coefficients,
6435 decoder states,108900 M entries,35 scalar spectra/triangles and105 exact
old phase anchors. Every pinned source/data hash matched. All comparisons
and signed/normalized bounds are exact integer/Fraction equalities.

This is an **algorithmically independent, posthoc NONBLIND control-side
reconstruction**: the checker author already knew the candidate sign/bound
and reviewed production. The B point is explicitly conditional on the pinned,
previously validated P53 exact source and checkpoints; it was not recomputed
from all8-photon permanents here. Sources were hashed, never imported.

The conclusion concerns this fixed linear MEAN/w/graph against b4(4+4) only.
It does not establish7+1/6+2/5+3 cases, genuine order8 indistinguishability,
all classical models, full laws/tails, strong feasible-search benefit,
algorithmic quantum advantage, held-out effects or hardware validity. No QPU,
manuscript change or scientific optimization-goal completion follows.

## Actual execution and immutable record

Clean launch HEAD: `bd76b12ded7f078bc25a3eecae5ac2c9b4a016a3`, after the
separate13-guard qualification and ROOT's distinct replay authorization.
Checker SHA256
`047ff5d95c947d159eca551e298fae07fb3db2acaf6f5c9807fca629d3bde5d2`.
The bounded runner pinned EXACTLY17 inputs from
`P53d_independent_check_execution_contract.json` and executed:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P53d_independent_check.py --output research/P53d_independent_check/run_001/data/verification.json
```

Runner completed/exit0, wall1.664462s, UTC start
`2026-11-25T14:03:07.610855+00:00`. Checker CPU1.523102s and
wall1.526861208s. Enforced CPU20/wall30/thread1/log4MiB; planned scientific
workspace64MiB, no measured peak-RSS or hard Darwin memory/affinity claim.
All17 input hashes unchanged; result present/regular; stderr empty; installed
schema-v2 manifest validator accepted the record against this isolated root.

| File under research/P53d_independent_check/run_001 | Bytes | SHA256 |
| --- | ---: | --- |
| data/verification.json |2348| `6620e81164ab52657ae70fad3b19e3708195d49d3674c829fb22f8d46a2a67c4` |
| manifest.json |11345| `b988c3d201e419b411182cc38fa7ac8a94b189ce48e8bdcd2de9c1043ba08f23` |
| stdout.txt |2224| `3dab09820a2c9c46eee64ae809de6ef5bc133101dc21bb8cab9bc8c1cd4f3349` |
| stderr.txt |0| `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Four evidence files total15917 bytes. Only metadata/result inspection and
receipt sealing followed; no additional guard/replay/control was run. All
original archives remain unchanged, and the numerical worker is released.
