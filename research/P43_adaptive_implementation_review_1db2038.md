# P43 corrective pre-run review — 1db2038

Verdict: **AUDITED, NOT EXECUTED — STATIC ALIGNMENT PASS** for the frozen
development-only screen. No new blocking defect was found in the corrections.
The original review `P43_adaptive_implementation_review_7794798.md` remains an
unaltered receipt of the earlier code, not a review of this corrected revision.

Reviewed corrections, both declared before pilot outcomes:

- `b55444f963e28f0d1a179b5eb0edaf31b4bbab56`: generic sampler qualification test.
- `1db2038cc3b9ff0fff6f6441e9d7dab2798d7004`: actual spectral restart and
  additional cost timing.

At the latter revision, Git blobs are:

| File | Blob |
|---|---|
| research/P43_global_gain_probe.py | 3c3ad594fbc79b30c8a5c767caf4babe3512db15 |
| tests/test_p43_global_gain_probe.py | 5879580e8bb9ed49b86c49f888f8e227251dc1fb |
| src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py | 0ea3542c465d799b61a1bff91f3ee8ab7a2a8a75 |

## 1. Generic multi-photon sampler qualification

The new test constructs a seeded generic complex 4-mode unitary by QR. It
enumerates all C(6,3)=20 occupations of3 photons, and computes their probabilities
with `FixedPhotonObliq.output_state`, using its separate vectorized Ryser
permanent/Fock normalization path. That path does not call Clifford2017 or
exqalibur. It explicitly uses input (1,1,1,0), matching the sampler's input modes
[0,1,2]; all outputs, including collisions, are included without conditioning.
It compares4096 serial CC samples at another fixed seed against that law with
a maximum absolute cell-error threshold .04 fixed in the test before execution.

For ideal independent samples of the reference law, Hoeffding plus a union
bound over20 cells gives failure probability at most

    2*20*exp(-2*4096*(.04)^2) = 40*exp(-13.1072) < 9e-5.

This is a meaningful independent small-network law check beyond HOM/identity.
It is still a finite statistical software qualification at ONE generic unitary,
not exact certification of the entire CC implementation, all source conventions,
or the k8/k10 outcomes. Root reports that all8 P43 tests pass; this reviewer has
read the test and reference code but has NOT independently executed those tests
or inspected their finite samples. No new numerical observation is claimed here.

## 2. Spectral search reservation resolved

The corrected control tracks the best of its first16 spectral/noisy proposals
independently of whether they beat the common anchor. At that stage's end it
explicitly resets its current state to the best spectral candidate, including
when that state has greater cost than C0. Subsequent budgeted one-swap search
therefore genuinely refines that spectral basin. All16 proposals already incur
one score each; choosing a previously scored state requires no new cut score.
The best public cost remains min(C0, all evaluated candidate costs), so the
restart cannot erase or falsely improve an earlier discovery. Raw rows now
identify the restart and current cost, disambiguating acceptance versus reset.

This fixes the specific strength issue identified at7794798. It does not turn
the small pilot into a benchmark against all best classical multistart methods.

## 3. Cost timing and remaining scope

Global model-selection wall time and per-model probe covariance-check time are
now recorded explicitly. Thus the named omitted timing components are resolved;
shared setup, remaining bookkeeping and repeated known-anchor evaluations still
must be interpreted alongside the full run's CPU/wall receipt. Row timings are
not measured device time or a total hardware advantage metric.

The supervisor states the actual run will use the external bounded runner with
CPU60 / wall90 / one numerical thread and preserved partial failures. This
review does not itself execute or verify that future enforcement. The earlier
scope disclosures remain: b4 partition fixed per graph, development relabels
are not held-out graphs, automatic pre-probe hash freeze is not an independent
replication, and the pilot cannot accept a positive scientific result. None of
the correction deltas introduces optimal-state data or changes those gates.
