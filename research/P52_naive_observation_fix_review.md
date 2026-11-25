# P52 observation-only correction, before qualification run_002

Parent failure archive: `51712a591a6baf08cf7163ecafcf364c80f07cfc`.
The entire `run_001`, stderr and first administratively rejected runner argv
are preserved unchanged and described in
`P52_naive_qualification_run_001_review.md`. Its actual child reached neither
the original five pytest guards nor the eleven API/numerical checks.

ROOT explicitly authorized this narrow correction after inspecting the failed
record. No automatic rerun is authorized. This checkpoint contains no imports,
pytest invocation, process observations or scientific calculations.

Delta from the reviewed source SHA256
`ca46ea81afa171cfd528e9ca61ee48e50bcd9bc99edd80b54e58097a46de4de4`:

- `thread_snapshot` catches `OSError` (including `PermissionError`) and
  `subprocess.TimeoutExpired`, returning `available=false`, error type, errno
  where available and message. All three existing call sites use this helper.
  A completed ps process records whether exit status was zero. No thread count
  or single-worker guarantee is inferred from unavailable observations.
- Optional `platform.platform()` metadata tolerates `OSError` analogously.
- One new pytest guard mocks EPERM, timeout and denied platform metadata,
  without invoking real ps. Planned guard count becomes six; the same eleven
  numerical checks are unchanged.
- The qualification's prospective output becomes the fresh
  `research/P52_naive_qualification/run_002/data`. The MD and qualification JSON
  record this path/count and the historical failure. The full-run command and
  contract, Perceval/vendor code, backend API, matrix construction, source,
  phases, probabilities, tolerances, references, caps and native-thread caveat
  are unchanged.

Frozen amended bytes:

| Artifact | SHA256 |
|---|---|
| research/P52_naive_replication.py | 3242986191a797c25693195c9a3d8af4acc027ba5ad1a1c92bd71f4c49d10400 |
| tests/test_p52_naive_replication.py | c64fbda5c8c74c205631743d9ab04fc64661445dfeaf53203ded590a0e25e043 |
| research/P52_naive_qualification_contract.json | 8d24e3380d0a69c4e79029267db53c8687e9b66ba138d05530e60771fe6d0215 |
| research/P52_naive_validation_contract.md | b852a57cecdb5c3d14b4b31f4cf33747565ec8d29f7b36c6338d2f9687110cd9 |

Unchanged historical failure manifest SHA256:
`c3cd30053b0426fbc14dbf4234bb4ac40c2deaf51bd08b26f307054698c0425b`.
Unchanged stderr SHA256:
`efdeb800f4b6038e593ae8c66b65e60970aa453c6ebc2327afaf7c8d28f72272`.
The historical record's input closure refers to d96009f, not the amended source;
its prior validator PASS is a validation of a failed record at that revision.

Static self-review only: `git diff --check` passed. Qualification run_002 is
pending ROOT delta review and a new exclusive slot. Full25,740 remains separately
unauthorized regardless of this wrapper fix.
