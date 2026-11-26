# P96 ROOT: one full integration check after pure qualification

ROOT read the sealed11PASS rawbd41d80 and wrote the separate pure receipt.
Authorize exactly ONE run of the already frozen eb13c5d helper
reports/P96_validation_review/run_full_suite.py using pinned Python -B.
Its only output is a fresh reports/P96_validation_review/local_suite_run001,
with stdout/stderr and execution.json. Expected population1559, to be
verified from the actual post-seal log, never treated as an observed result.

The helper uses child CPU120s/wall180s and4MiB per regular file, six thread
environment variables1 and configured native1 before and after the suite.
These test-suite caps are separate from pure qualification and main limits;
there is no hard RSS or OS-thread claim. ROOT owns the one numerical slot.
The tests repeat previously qualified small fixtures plus11 P96 pure tests;
they do not execute the P96 native main or a DEV optimizer/QPU workflow.

Seal all raw outputs in Git BEFORE interpreting the log; preserve any
failure without automatic retries. Do not change source/test/contract bytes
while this suite runs. A successful check is needed before publishing new
code. It creates no active P96 binding or native-main authorization.
paper/, main and QPU remain frozen; the positive optimizer objective is OPEN.
