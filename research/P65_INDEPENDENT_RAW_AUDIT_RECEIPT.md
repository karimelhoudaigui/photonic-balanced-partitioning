# P65 independent recorded-data audit

25 November 2026. **PASS_RECORDED_CONSISTENCY**:9251 checks, zero
discrepancies. Recorded negative gate `DEV_REJECTED_FIXED_FAST` verified for
both fixed random and spectral modes on both registered graphs.

Independent checker freeze `0d7224feeba89307b13c7be33e99db3aff9c1a19`, SHA256
`71ae8141c8a73fe23cd16d2a45d5c74ab2254a5b4d1e2b6bf56ca5206d875ef6`.
Its author had not opened P65 data at freeze. ROOT inspected the full707-line
source, nine synthetic fixtures and both contracts before qualification.
Nine fixtures PASS at clean0d7224f, pytest0.41s/runner0.827565s, raw2824d13.
Primary outputs were imported afterward; binding changes only metadata,
without changing checker source, scope, tolerances, seeds or caps.

One audit at clean `b2114d106f0e0d7e0aad34e9769444f8f02be1db`:

```text
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python research/P65_independent_raw_audit.py --root . --binding research/P65_independent_raw_audit_input_binding.json --output research/P65_independent_raw_audit/run_001/data/audit.json
```

Raw outputs sealed before interpretation at `397e241`. Runner completed/exit0,
WALL0.330294s; inside-audit CPU0.120502s. CPU20/wall30/env-thread1, log4MiB,
logical64MiB plan, zero retries. All23 execution inputs unchanged; all13 bound
primary artifacts also rehashed before and after. Both v2 audit/qualification
manifests validate with `--root .`.

Coverage:80 requested/completed counts and fresh factories;16 Cayley matrices
independently rebuilt by eigendecomposition rather than production solve;
820 owned seed roles; current-source/coin/collision/acceptance state machine;
all exact fitnesses, first ties, chain resets and separate local/global bests;
199 paid components per case;414 FAST checkpoints, packed K10 masks/scalar
cuts,100-delta scans, recorded CPU-prefix eligibility and fixed-mode gate.
The original producer has17 unchanged inputs and all12 scientific outputs.
No optimum was used; actual QPU calls0, no held-out or optional-arm opening.

Limits: no NetworkX topology regeneration (canonical edge weights and RR degree
checked), no physical samples/permanents or native sampling-law verification,
no authentication of recorded clocks/online causality or unseen FAST proposals.
Recorded cost closure is not matched real hardware cost. Cayley checks use
absolute3e-12, not interval arithmetic. This is not blind independent physical
replication, optimizer advantage or a universal negative result.

Audit manifest SHA256:
`a7031801630b123814367ad54e0a899b97b9aa4020cd786ebebce06ab837ef5c`.
Audit report SHA256:
`b2e52ba90dadd69af1202280c5c8d5b5d3b12f52a0704b35507be57941199d58`.
Qualification manifest SHA256:
`c0266c49622880d0c7fd13ac3f6569797da7adfdba23a388ca3b79a3f440307b`.

Full existing regression at397e241: **1092 PASS**, six retained cache warnings,
pytest41.97s/total43.024621792s, env/native thread1 before/after, exit0.
Commands and logs: `reports/P65_independent_combined_validation/`.
Integration with other already validated branches still needs its combined
regression; no scientific primary run is automatically repeated.
