# P55 independent recorded-data checker: static preparation contract

Status: **FROZEN FOR ROOT REVIEW; NOT EXECUTED**. The plan was frozen
in6a5db45 and checker first committed in3f6ebc6 before opening any P55 MAIN
output or learning its outcome. ROOT subsequently supplied the sealed
commit8049fa37a872442242613ad54562c09bb75ab6a5. Its run directory was
extracted byte-identically with `git archive`, and hashes computed without
opening the raw, summary, selection, contexts, failure or stdout. Subsequent
static changes assert the declared NumPy/NetworkX versions, universal zero
QPU/positive flags and consistency of the duplicated selection clocks.
No execution slot has been granted; no import or recalculation occurred.

Entrypoint: `research/P55_independent_raw_checker.py`, no primary/helper
imports. The checker expands sparse prefix generating polynomials and
inverts the saved rank independently of the dense production DP/unranking.
It replays only the fixed graph/group recipes with pinned NumPy/NetworkX;
all observation, cut, selection, clock and status checks use stdlib.

Actual data closure: primary `raw.jsonl.gz`, `summary.json`, `failure.json`,
both context files and `selection.json`. All six outputs exist, but their
meaning/outcome remains unread at freeze. Their hashes are listed in
`research/P55_raw_audit_pins.json`. The sibling primary runner manifest
SHA256 is `2d14cd05fe14a8ab3136e6063ac3bbe74e3cbbc156d02def9cae8b383248d5ed`;
it is retained as provenance, not treated as a mathematical oracle.
A JSON dictionary maps every consumed data-relative filename to its
SHA256; the checker verifies all entries before checking mathematics.
Absent files after a failed primary are not fabricated. The actual
execution contract must list all present consumed inputs individually,
including checker, frozen plan, this contract and the pins dictionary.

Planned command, with actual paths filled and frozen before execution:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P55_independent_raw_checker.py --input experiments/P55_finite_neutrality/run_001/data --pins research/P55_raw_audit_pins.json --output experiments/P55_independent_raw_audit/run_001/data
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
