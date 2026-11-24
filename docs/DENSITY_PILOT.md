# P40: a testable sharpness-family calibration pilot

This is a frozen theoretical pilot for four modes and two injected photons.
Its45 cells are model predictions plus controls, not a hardware result or an
optimization discovery. The contract was committed before any pilot calculation:
`efd1718a6a8b8e8ffac1ad84360566bf4346648a`, SHA256
`30dbbdae5aa2d0c89eb936f7700e5808cde49f215c5118011f10f8fd2e70c4a2`.

## Source, circuit and physical events

Put c=(1-r^2)/(1+r^2), s=2r/(1+r^2), with
r in {0,1/20,1/10,1/5,1/3}. Inject one photon in each of modes0,1.
The fixed Perceval sequence is BS.Rx(4atan(r)) on0,1;
PERM([0,2,1,3]); and BS.Rx(pi/2) on0,1 and2,3. Rx has diagonal
cos(theta/2), off-diagonal i sin(theta/2). The occupied columns of the resulting
unitary are

    v0 = (c, i*c, i*s, -s)/sqrt(2),
    v1 = (i*s, -s, c, i*c)/sqrt(2).

The two output groups are {0,1} and {2,3}. Each row has ideal mean intensity
1/2. The ideal indistinguishable source has dominant leakage delta=2s^2 and
expected unordered pair count M_ideal=2c^2s^2. Since there are two photons,
this pair count also equals its physical collision probability. These are the
flat-density P33 sharpness-family quantities, not quantities redefined after loss.
For the lossless identical source, TV=M_ideal=delta(1-delta/2), which saturates
the two-column spatial-Gram bound and approaches unit slope in delta near zero.

Internal states have S=[[1,sqrt(x)],[sqrt(x),1]], x in {0,1/2,1}.
Uniform independent survival eta is in {1,9/10,1/2}. All detected-number
sectors and vacuum count per injected attempt. Eta and x are known by
assumption in this calculation; they are not Belenos calibration values.

The path has unit edges(0,1),(1,2),(2,3). Its optimal balanced cut is1,
with the two oriented chains(1,1,0,0) and(0,0,1,1). "Path success" counts
exactly those occupations. "Collision" counts any spatial occupation>=2.
TV compares the complete noisy law with the distinguishable control at the
same unitary and survival, including lower photon sectors.

## Predictions and their derivation

For two photons the pair-exchange factor is exactly x=|S12|^2. Distinct
physical output modes i,j have their independent routing probability plus
`2x Re(U_i0 U_j1 conjugate(U_i1 U_j0))`. A repeated output i has probability
`(1+x)|U_i0 U_i1|^2`. This gives

    TV = eta^2 x M_ideal,
    P_collision = eta^2(1+x)M_ideal/2,
    P_path_success = eta^2(1+x)M_ideal/2.

In the lossless source, both photons entering the same group have probability
(1+x)M_ideal in total. Balanced splitting inside that group sends half of
this probability to a physical collision and half to the two distinct modes
of that group, which are precisely the path's optimal chains. For x=1 the
full-law boson/distinguishable TV is M_ideal; two-photon dependence on x is
linear. Uniform loss multiplies the two-photon law by eta^2. The one-photon
probability at i is eta(1-eta)(|U_i0|^2+|U_i1|^2), independent of x, and
vacuum is(1-eta)^2. Thus those sectors cancel in the full-law TV, explaining
the exact eta^2 factor. This is a two-photon derivation, not a global
interpolation model for three or more photons.

The pilot does not substitute noisy/unconditioned moments into the ideal
fixed-N density theorem. In particular sqrt(eta)*V is not an orthonormal
occupied frame, and the detected law has variable photon number. Applying
that theorem requires the appropriate source assumptions/conditioning and a
separate justified noise argument; the present identities were derived directly.

## Countercontrols and interpretation

Uniform feasible sampling has two optimal outcomes among six, hence success
eta^2/3 with the same two-photon survival charge. Identity with the already
known optimal input chain succeeds with eta^2. The latter is a diagnostic
that uses known optimal structure, not a discovery procedure. Both controls
are exported as complete laws.

At x=1 and r>0, the same-unitary bosonic path success is twice the
distinguishable value. That ratio alone is not an algorithmic advantage.
The r=0 source has zero path success and zero collisions and is retained.
The grouping itself matches this small path's optimal chains; this pilot
does not test an optimum-blind optimizer on unknown graph instances.

## Execution, records and possible future measurement

The entry point refuses an existing output directory. The45-cell population,
three predictions and1e-10 error threshold cannot be changed by CLI flags.
CPU is capped at60 seconds, wall at90 seconds, with one BLAS/OpenMP thread.
No sampling, tuning, local model, network processor or QPU is used. The
primary calculations use the physical noise package. Five ideal bosonic
circuits are independently checked with local Perceval SLOS, and all full
partial/distinguishable laws are checked against the two-photon formula.

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/pasqal-mpl-noise PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python experiments/scripts/validate_sharpness_pilot.py
```

Outputs are new and immutable under
`results/validated/P40_sharpness_pilot_2026-11-24/`: raw.jsonl retains all
45 cells and all-sector laws; circuits.json contains every U, angle, gate
serialization, native Perceval serialization and ideal reference law;
summary.json records every rejection/error and the countercontrols;
manifest.json pins the committed contract, actual command, versions, resource
use and input/output hashes. PASS means all declared checks met1e-10; it is
not interval certification or experimental evidence. The export-audit tests
read those records rather than rerunning another45-cell campaign.

Availability of PNR detection, loss heralding or the needed QPU configuration
is unknown. Full Fock TV and collision-vs-loss discrimination generally need
PNR or an equivalent independently validated measurement arrangement.
Threshold-only single clicks cannot distinguish a bunched pair from one
surviving photon. Path success with two distinct clicks from a two-photon
source is observable under a suitable threshold setup, but that alone does
not measure all pilot observables. Any hardware experiment needs a separately
authorized protocol and actual eta/internal-state calibration; none is supplied
or inferred here.

## Executed frozen validation

The single prescribed run returned **PASS:45/45 cells,5/5 local SLOS circuits**.
No failed or zero-valued cell was filtered. Actual CPU was1.004904 seconds,
elapsed2.02185499999905 seconds, with the declared60/90-second hard limits.
Maximum absolute errors were9.71445146547012e-17 for the TV identity,
5.551115123125783e-17 for each collision/path identity,
4.163336342344337e-17 for the ideal Perceval check,
1.1102230246251565e-16 for the independent complete pair law, and
4.440892098500626e-16 for normalization. Unitary and independent-builder
residuals were1.1102230246251565e-16; serialization roundtrip error was zero.

At eta=x=1, exported path success (equal to collision probability and TV) is:

| r | Value |
|---|---:|
| 0 | 0 |
| 1/20 | 0.01970236131612222 |
| 1/10 | 0.07534854685020868 |
| 1/5 | 0.2520920135849585 |
| 1/3 | 0.46080000000000004 |

These are computed scenario probabilities, not measurements. In particular the
same-U factor2 remains accompanied by the uniform-feasible and known-optimum
controls. There is no optimizer or unknown-graph experiment in this run.

The exact validation command above executed once. The v2 evidence validator
returned a valid completed record. The additional test command actually run was:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/pasqal-mpl-noise PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -c 'import resource,pytest; resource.setrlimit(resource.RLIMIT_CPU,(30,30)); raise SystemExit(pytest.main(["tests/","-q"]))'
```

It returned330 PASS, including six export/immutability tests and the noise
physics tests. It did not rerun the45-cell experiment: the output guard was
tested by confirming a second invocation is rejected before computation.

The manifest records the pre-execution contract commit and a dirty tree because
the new script had not yet been committed; its exact hash was frozen before
execution and checked unchanged afterward. The final artifact commit pins that
same script. This is disclosed rather than relabeling the run as a clean-tree
execution at a later revision.

| Artifact | SHA256 |
|---|---|
| script | `2e9dba7c14beafd37901dc1917f59a7354a84dbfa0d45ccdfee09adb4d0c01d0` |
| raw.jsonl | `b3189ac6143c31654d97d06209a94494281b25c43b37c5cd33782014bd277658` |
| circuits.json | `f945154043ff220ca18d105a9528a9a404664a992da107707ab9c0927036e598` |
| summary.json | `852a43b4ff28d855c3822f13e7060e7c773f445b74eb3b4d9d48e6878d285e53` |
| manifest.json | `d29fd7a401d6415e18ddd49cf070bbd7ac3e5f1072182d74abba8b2c5bc68b84` |
