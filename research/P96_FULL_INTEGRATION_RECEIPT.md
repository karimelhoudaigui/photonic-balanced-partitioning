# P96 full integration: separate receipt after sealed corrected run

The corrected complete suite passes1559 tests,6warnings,44.61s pytest;
wrapper45.714537959s, exit0, no timeout. Execution commit613c19a629aa30d3740872fa02d693a9ce3532ad;
raw98c71a6 sealed BEFORE reading. Six warnings are Perceval's known default-
storage fallback to temporary files. stderr is empty; total logs2976 bytes.
CPU120/wall180,32MiB per regular file, env/native configuration1 before/after.
No RSS/OS-thread limit is claimed. These are integration-only limits.

The earlier full check is preserved at rawfae05f1:1541PASS/18 setup errors,
caused by ROOT's4MiB regular-file cap blocking temporary copies of existing
17MiB P33 data. It was not hidden or called a scientific failure. The only
correction is a separate wrapper/output002 with32MiB file cap. Tests,
scientific source,8 static P96 inputs, tolerances and physics populations
did not change. No original paper/result file was built or edited by this
temporary-copy fixture. Original failed wrapper/raw remain in Git.

The11-item pure qualification remains separately valid: rawbd41d80,
receipt in P96_PURE_QUALIFICATION_RECEIPT.md,8 hashes unchanged/v2PASS.
Full suite includes those11 pure tests and old qualified tiny fixtures.
It does NOT execute the159-point P96 native main, which still requires an
actual immutable binding and separate ROOT authorization. No DEV graph
optimizer, positive replication, QPU or manuscript gate follows.
