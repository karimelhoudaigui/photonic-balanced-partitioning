# P141 recorded-reader V2 — independent static correction review

26-Nov-2026. Non-author review; parent 10d3f8a10a520f2b23fcb7ad383c8892995ca39f.
FULL 191 lines read at afbbddb9c7e1c5ff38d5b9fb854963d07b86cb29:
research/P141_recorded_consistency_reader_v2.py, SHA256
c8a455ec784d546d551e28e57c3fc4e05f7501963baad5b5ffba79bcb74e74dd.
FULL diff against final V1 edd472a2cd7d7912e1e63269f0afdaeeed416eda
(188 lines) read. Commit metadata confirms one new V2 file, no V1 edit.
No raw/result payload, program/import/AST/test, RNG, graph draw, matrix
calculation, permanent, native, QPU or manuscript was accessed/executed.

**STATIC ACCEPT for the schema correction and recorded-consistency scope.**
This is neither a runtime PASS nor authority for a V2 attempt.

## Failure preserved, source correction checked

ROOT reports that V1 actually FAILED after 58443 recorded rows in 0.932594 s,
with its outputs and metadata sealed at 9efe143 before interpretation.
The reported cause is equality of complete graph-decision dictionaries:
the JSONL dispatch field kind was stored in decisions, while the summary's
scientific decision dictionary has no dispatch field. I did not open either
payload or the failure receipt; these execution facts are ROOT's report.
My previous V1 static acceptance missed this schema mismatch. It must not
be retrospectively described as a successful reader execution.

The sole processing change is:

    decisions[row["case"]] = {k: v for k, v in row.items() if k != "kind"}

The branch is still selected only after registered-kind validation; kind
still contributes to semantic keys, uniqueness and all exact kind counts.
Every other key/value, including unknown extra fields and all scientific
decision values, is preserved verbatim. No numeric conversion, tolerance,
mask, favorable selection or comparison-field whitelist was introduced.
The later WHOLE-dictionary equality against summary.decisions is unchanged.
Thus a differing scientific or other non-kind field still fails equality.

All other executable differences are the fresh exclusive output path
reports/P141_validation_review/recorded_consistency_v2.json and the V2
provenance label explicitly retaining the V1 failure. Three added header
lines explain the correction, immutability and need for NEW ROOT authority.
The first output path and its failed contents are never opened or replaced.

## Exact inherited checks and limits

The six RAW SHA256/blob literals, original seal 737321d, 58443 counts,
36 contexts, 540 totals, 30 maxima, 140 cuts, 1365 PNR rows, 17 inputs,
11 external descriptors and all comparison expressions are byte-unchanged.
The corrected field membership/common-baseline checks from edd472a2 remain.
Signed first-minus-second reconstruction, denominator powers, occupation
factorials, collision/dump accounting, independent profile grid retuning
and exact first-index tie handling have not been relaxed.
The q breakdown remains explicitly post-outcome, raw and unrenormalized.

CPU 20 s, FSIZE/output 1 MiB, no-overwrite/canonical-parent guards, caught
audit-failure traceback and last-row prefix are unchanged. ROOT must supply
a separately pinned source/argv authority, outer wall limit 30 s and sealed
execution/stdout/stderr metadata before interpreting any possible V2 output.
V1 authority is not reusable; the CLI flag alone is insufficient.
No main rerun, new optical point, altered seed/cap or result edit follows.

The reader remains post-seal work by the PRIMARY producer author. It checks
recorded algebra/provenance, not a new optical calculation or independent
physics/optimizer replication. Matrix certificates remain flags-only;
recorded PNR/C4 consistency is not independent permanent verification.
My earlier separate metadata-only Git authentication of the six original
blob IDs still applies because those literals are identical. I have not
reopened raw bytes. Runtime success and any scientific conclusion remain
separate from this static acceptance; V1 and its negative receipt stay kept.
