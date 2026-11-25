# P55 independent recorded-data checker: static preparation contract

Status: **NOT EXECUTABLE YET**. The plan is frozen in6a5db45 before reading
the MAIN outcome. This source preparation is also made without opening any
P55 MAIN output. No actual input manifest, data pins or execution slot has
yet been supplied. Those must be frozen in a following explicit contract
revision before one run; this document is not authorization to improvise
input hashes or run while the primary owns the worker.

Entrypoint: `research/P55_independent_raw_checker.py`, no primary/helper
imports. The checker expands sparse prefix generating polynomials and
inverts the saved rank independently of the dense production DP/unranking.
It replays only the fixed graph/group recipes with pinned NumPy/NetworkX;
all observation, cut, selection, clock and status checks use stdlib.

Required data closure, when supplied: primary `raw.jsonl.gz`, `summary.json`,
`failure.json`, both available context files, and `selection.json` if
present. The sealed primary runner manifest must also be retained as
provenance, with its exact hash, not treated as a mathematical oracle.
A JSON dictionary maps every consumed data-relative filename to its
SHA256; the checker verifies all entries before checking mathematics.
Absent files after a failed primary are not fabricated. The actual
execution contract must list all present consumed inputs individually,
including checker, frozen plan, this contract and the pins dictionary.

Planned command, with actual paths filled and frozen before execution:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P55_independent_raw_checker.py --input <sealed-copy-data> --pins <frozen-pins.json> --output experiments/P55_independent_raw_audit/run_001/data
```

One fresh run via Mathbox runner v2: CPU20 seconds, wall30 seconds,
environment threads1, outputs <=4MiB, no native backend or optical imports,
no new count/phase/CTMC draw, no physical state propagation or optimizer.
Only current fixed graph/group recipe randomness is replayed. No retry,
graph replacement, resource increase or primary modification is implied.
Retain all failures and validate the v2 manifest/hashes before committing.

The11 prospective integrated guards check four small GF/rank families,
one explicit cut, rejection of a corrupted cut, and five gate priorities.
They have not been executed at source preparation. The recorded-data
checks cover full or failed populations, all per-shot neutral ranks,
sequential private RNG usage, supplied graph/context copies, exact cuts,
policy Fraction losses, all paid/fresh bests, B-only WALL accounting and
unavailable CPU split, and each saved FAST trace subset/cut/deadline.
The checker recomputes the status; it never turns follow-up into advantage.

Limits: this is post-source-review code independence, not independent
physical sampling. Saved timestamps/caches/selection flags cannot alone
prove hidden chronology or no omitted work; the static source and runner
closure are complementary evidence. No calibration, QPU, held-out result,
population test, unknown optimum or global advantage follows.
