# P52 finite preflight: 45 PASS

25-Nov-2026. ONE targeted qualification under explicit ROOT exclusive-slot
authorization, not a production phase calibration or optimizer result.

Source was frozen at67db4a1 before every scientific import. Pre-data caller
review requested only a conservative solver-status correction, preserved in
d7f8e2f: timeout/failure keeps numerical candidate weights/residual but always
marks the fit inconclusive. Six new mocks cover deterministic/MC candidates
with limit/failure/successFalse. No source circuit, grid, MC effort/seed, solver
options or cap changed. Full code/caller/physics static reviews passed before
the qualification (13ce129,0237b70,ea037bf; copied into this branch intact).

Actual source HEAD was clean
`8eabbc684a146e1700f29c1018e21083473e4b95`.
Primary SHA256:
`56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242`.
Tests SHA256:
`3342f6c4839640a1d296553fd860269a1287601ed1009a4831f85c153cb6346a`.

Actual pinned Python3.11.15 pytest command used the contract's12 EXACT input
artifacts under the installed Mathbox v2 runner. Observed **45 passed in1.02s**,
runner completed/exit0,1.312742s wall. Limits CPU60/wall90/thread1/log32MiB;
no hard Darwin memory/affinity promise. All12 before/after input hashes match,
JUnit present/regular, no retry or missing/invalid result. v2 validator --root
returned valid evidence record, completed.

Checks include small independent complex permanents/HOM/H4 normalization,
complete compact support/convolution, canonical/input-permutation phase nulls,
pre-data analytic eight-photon fourth-order witness and Walsh0 crossing means,
exact uniform ties and row/total invariants, a nonproduction identity-U MC
fixture with overridden seed, and confidence/convex-candidate accounting.
The actual tiny native LP fixture passed threads1/paralleloff/time_limit1
readback and reconstructed coefficients; false-success/invalid-warning and
timeout cases remained correctly qualified. No unknown phase-ranked effect
or production MC stream is asserted from these fixtures.

Evidence: `research/P52_collective_phase_preflight/run_001/`.
Manifest SHA256:
`ae8104c725cf94c671a2c940e0165e1c446a5c5be7404ea2df56ab981b4a0a1d`.
JUnit SHA256:
`23536f5d73ba9e6c2cfea2093e5e1cdb7fbc0cc4322d199cca8058cb79082ad1`.
Logs/argv/software/hardware/limits are retained. This is a targeted preflight,
not a full-suite, interval/sampler theorem, graph benchmark, held-out physical
replication, accepted positive or QPU validation. Main still requires a new
explicit ROOT authorization; no production run was chained automatically.
