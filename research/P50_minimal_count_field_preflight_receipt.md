# P50 targeted preflight: 74 PASS

25-Nov-2026. ONE explicitly authorized targeted qualification, not a DEV run.
The source, population, costs, seeds and tests were frozen before any project
import/test at0fbe635; the independent caller/physics reviews PASS statically
(d6ce9fc and2e83846), followed by ROOT approval. Card02041c3 was synchronized
and DOCONLY sparse-to-dense H corrected before execution; no code or scientific
parameter changed after those reviews.

Actual clean run source: `c5805d72848f73ca3308f37482a529b2c35952e5`.
Script SHA256:
`6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf`.
Tests SHA256:
`a4c6dce0cb3e213fd9530420486f37efd488e5ae544aa8decb36b23f8022f371`.
The independently qualified FAST helper remained6def5c0f..., unchanged.

Real command used the frozen planned pytest argv under pinned Python3.11.15
and the installed Mathbox v2 bounded runner, with20 EXACT declared inputs,
CPU60s/wall90s/thread1/log33,554,432 bytes. No hard Darwin memory/affinity limit
is claimed. New output `research/P50_minimal_count_field_preflight/run_001/`.

Observed: **74 passed in1.02s**, runner **completed/exit0**, **1.329261s wall**.
That is53 new primary hand/caller/cost cases plus21 separately owned FAST
cases. All20 input hashes remained unchanged; JUnit present/regular, no missing
or invalid result. The installed validate_manifest.py checked the v2 manifest
with --root and returned valid evidence record, completed. No retry occurred.

Raw pytest stdout, stderr, JUnit and full argv/versions/hardware/limits/hash
manifest are preserved alongside this receipt. The qualification covers the
stated small fixtures, not full-suite integration, distribution certification,
the P50 DEV graphs or a positive scientific result. No DEV graph, held-out panel,
manuscript, physical QPU call or numerical benchmark was opened by these tests.
The separately authorized MAIN is still pending ROOT review of this result.
