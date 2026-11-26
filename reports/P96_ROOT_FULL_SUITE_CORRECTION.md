# P96 integration-only correction after a preserved first failure

First full suite executed at ea7364d, rawfae05f1 sealed BEFORE reading:
1541PASS,6warnings,18 fixture SETUP errors,41.25s pytest/42.229016708s wrapper.
The common setup fails copying preserved P33 raw data: Errno27 File too large.
ROOT's new4MiB RLIMIT_FSIZE applies to EVERY regular file, including temporary
fixture copies, not just logs. The original P33 files are17,163,136 and
17,164,374 bytes, so the added integration wrapper cap caused these errors.
This is ROOT's test-wrapper error; it is not a scientific P96 failure.
All original raw/negative results and the full failed log remain unchanged.

Read the exact wrapper change: new run_full_suite_v2.py uses fresh
local_suite_run002 and32MiB per regular file, above the observed existing
fixture sizes; CPU120/wall180, env/native1, tests and1559 expected items
remain identical. This is not a4MiB log-only bound. Full-suite verification
has limits separate from pure qualification and the159-point native main.
No scientific source,8 static input, population, tolerance, physical budget
or native-main limit changes. Pure11PASS remains valid with its own512KiB.

ROOT authorizes ONE corrected full-suite check under this diagnosis. Preserve
raw BEFORE reading and issue a separate receipt; no automatic further retry.
The159-point native main still awaits its own actual binding/authorization.
No publication build runs on the original paper; tests use their temporary
copy. Main/paper/QPU remain frozen. No code is published before required
tests pass. The first failed source/helper/record stay in Git unmodified.
