# P53d independent checker: synthetic guards

25-Nov-2026. **13 PASS**, one authorized qualification, no retry. The complete
archived-candidate replay has NOT run. This is component qualification and
does not yet confirm the candidate uniform bound.

Clean launch HEAD: `0b556e1337fa8b1f3622dbddceb631e1c36df8cb`.
Checker SHA256
`047ff5d95c947d159eca551e298fae07fb3db2acaf6f5c9807fca629d3bde5d2`;
guards SHA256
`2da1f7699d81cee7c5a813b00685d1f24300995239b5f3ec28f4e31b7b7f876d`.
ROOT reviewed the complete source/tests/MD/contracts before the exclusive slot.

The installed bounded Mathbox runner pinned exactly17 inputs from
`research/P53d_independent_guards_contract.json` and ran:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q tests/test_p53d_independent_check.py --junitxml=research/P53d_independent_guards/run_001/junit.xml
```

Fresh result directory: `research/P53d_independent_guards/run_001/`.
Caps: CPU20s/wall30s/thread1/log4 MiB, planned scientific workspace64 MiB;
no hard Darwin RSS/affinity claim or observed CPU/peak-memory measurement.

- Runner: completed/exit0, wall0.561937s; UTC start
  `2026-11-25T14:00:24.995320+00:00`.
- Pytest:13 passed in0.28s. JUnit:13 tests, zero errors/failures/skips,
  aggregate test-body time0.151s; these timings have distinct envelopes.
- All17 input before/after hashes match. JUnit is present/regular; stderr is
  empty. Installed schema-v2 validator accepted the record against this root.
- Subsequent inspection used only existing stdout/XML/JSON/hash metadata.

The guards cover four hand permanent/Fock cases, exact multiplicity division,
slot enumeration, known uniform-max-subset tie scalars, pre-conversion integer
bounds, two-einsum versus small independent Python sums and worst13-fold
case, exact triangle/anchors and strict/opaque/bounded JSON handling.
No production module, archived proof payload, full70-group/35-spectrum replay,
phase search, LP, RNG, Perceval, hardware call or optimizer experiment occurred.
The main replay remains subject to ROOT's separate authorization.

| File under run_001 | Bytes | SHA256 |
| --- | ---: | --- |
| manifest.json |11235| `2ddbf5a5a9d9e18bb2baffc19fbc48e61f913c7ee92cdc440455944e6d484597` |
| junit.xml |2174| `883a5bb216d6baed8f758a54dea3ad0dd4231dedff389c93fe3c5e19cfc96c53` |
| stdout.txt |243| `65dad48a46517c40f265c6f42b58621d8230939ed7db07ba330e2c12765a7b29` |
| stderr.txt |0| `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Four immutable evidence files total13652 bytes. The numerical worker was
explicitly released after qualification. Checker independence is algorithmic
and posthoc NONBLIND; the old B point remains conditional on its pinned,
previously validated source. No discovery/optimization/hardware claim follows.
