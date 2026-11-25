# P52 JSON-boundary correction, frozen before run_003

ROOT authorized this minimal delta after failed run_002, sealed at
`50991abfbd0fa4af69121d21f5e0edc0bf09df5d`. Its manifest, stderr, six-PASS
JUnit and absent report remain unchanged. No eleven-check/API PASS is inferred
from that run. Historical run_001, its source revision and the first rejected
administrative argv also remain preserved.

The former nested check built `pass` from a foreign scalar comparison without
conversion. A new pure-stdlib `check_record` explicitly returns builtin string,
float coordinates from builtin complex, builtin float residual and builtin
bool comparison. The eleven check calls and their expected values/tolerance
are unchanged. The other report numeric scalars already use builtin casts or
stdlib values; no generic JSON fallback silently converts unsupported objects.
NaN still fails strict JSON and does not become a favorable numerical result.

The seventh guard uses simulated foreign float and bool-like classes to check
true/false records, builtin types and strict stdlib JSON roundtrip, without
NumPy, ps or a permanent call. Its source is frozen but has **not been imported
or executed** at this checkpoint. Qualification now plans seven guards plus
the original eleven API checks, in fresh run_003 only after review/slot.

ROOT additionally authorized resource-only Matplotlib configuration before
imports. Explicit `MPLCONFIGDIR` is preserved. If absent, the validator creates
its writable persistent worktree `ROOT/.local/mplconfig`, here
`/Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication/.local/mplconfig`.
Path/ownership/preexistence are recorded in the report. No cache was created or
scientific module imported in preparing this amendment. This may avoid
repeated temporary cold font-cache initialization seen in run_002, but neither
qualification nor full-run CPU feasibility is established. The same CPU20 /
wall30 / log4MiB caps apply, including initialization. Full25,740 is still
separately unauthorized; no cap increase or warm-import accounting is proposed.

No backend/vendor, repeated-submatrix/factorial convention, matrix/circuit,
photon source, four phases, six reference files, tolerance, iterator choice,
output law, production destination or scientific interpretation changed. The
full contract changes only its cache resource note. The qualification JSON/MD
changes prospectively to run_003 and guard count7, with the same eleven inputs.

Amended source SHA256:
`a68f969ff3b943c5d2d3bd475652a260caf446469aa913cd4c476b347fa4be52`.
Tests SHA256:
`aa74800b04e5a959cda58aa6595d4f72747931cfbf05dd9189a452496d07cd4c`.
Qualification JSON SHA256:
`3beb25ca2ba2cf7e17406b627082f39ac0e1b3966a5742e9dfdc261550b077c3`.
Full JSON SHA256:
`a3760bd36ab6706814fa0f12084cb66175d91b0e98c92ad828f7e4b803ef33df`.
MD contract SHA256:
`754bd421eb307c5b347585e98cb4e4773b80c0c9a76184edf362d6f0161887a0`.

Static `git diff --check` passed. No pytest, API import, scientific calculation,
native thread observation or retry occurred. Awaiting ROOT delta review and
an explicit qualification slot. The native-thread caveat remains unchanged.
