# P40 frozen sharpness pilot contract

Frozen before execution on2026-11-24, isolated branch
`recovery/physics-20261124`, following noise-module commit
`d36e2d2bba77bc64c1d8c6914fa5d4331d068cd3`. This file must be committed
before any pilot calculation. No sampling, optimization, QPU or hardware
calibration is authorized. No manuscript or historical raw data may be edited.

## Fixed hypothesis and event definitions

Use the flat four-mode, two-photon family with

    c=(1-r^2)/(1+r^2), s=2r/(1+r^2), M_ideal=2c^2s^2.

Inputs are modes0,1, singly occupied; their pure internal Gram is
`[[1,sqrt(x)],[sqrt(x),1]]`, with x=|S12|^2. Detection is unresolved in the
internal state. Eta is known uniform independent survival after the unitary.
Every injected attempt, every detected-number sector and vacuum is retained.

Groups are {0,1} and {2,3}. The path graph has edges(0,1),(1,2),(2,3),
each of weight1. Its minimum balanced cut is1, with the two oriented optimal
occupations(1,1,0,0) and(0,0,1,1). "Success" is exactly their probability.
"Collision" means at least one spatial mode has occupation>=2; with two
photons it can occur only in the two-detected sector. It is not a conditioned
collision fraction. "TV" compares complete noisy laws against the
distinguishable control at the same U and eta, including lower sectors.

Predictions to prove or reject without retuning:

    TV(noisy_S,noisy_D) = eta^2 x M_ideal,
    P_collision = eta^2(1+x)M_ideal/2,
    P_path_success = eta^2(1+x)M_ideal/2.

Countercontrols are uniform feasible sampling with success eta^2/3 and an
identity interferometer with the known optimal input occupation(1,1,0,0),
success eta^2. The latter uses known optimal structure and is a diagnostic,
not a discovery algorithm. No same-U boson/distinguishable ratio, including2,
establishes an algorithmic advantage against these controls.

## Population, no filters

The entire Cartesian product is fixed:

    r in {0,1/20,1/10,1/5,1/3},
    eta in {1,9/10,1/2},
    x in {0,1/2,1}.

Exactly45 cells will be evaluated once; all cells, including failed/zero cases,
will be retained. No random seed is needed because there is no sampling or
parameter selection. No angle, source or graph will be chosen after seeing a
result. Predictions use the exact rational c,s,eta,x before conversion to floats.

## Exact circuit convention and independent controls

The Perceval four-mode circuit order is fixed:

1. BS.Rx(theta=4atan(r)) on modes0,1;
2. PERM([0,2,1,3]) on all four modes;
3. BS.Rx(pi/2) on modes0,1;
4. BS.Rx(pi/2) on modes2,3.

BS.Rx(theta) has diagonal cos(theta/2) and off-diagonal i sin(theta/2).
Matrices multiply in propagation order, so the compiled unitary must match
the independent product of these four matrices. The native Perceval circuit
serialization, a canonical gate-list serialization, all angles, complex U and
input/output mode conventions will be exported for each of the five circuits.

Primary probabilities come from the new physical noise module, not from the
asserted metric formulas. Ideal bosonic laws of all five circuits will be
cross-checked against local Perceval SLOS. An independent two-photon formula
will check the full distinguishable laws and the pure-internal-state pair
interference, including every repeated-output factorial. Under uniform loss,
the two-photon sector is multiplied by eta^2, one-photon probability at i is
eta(1-eta)(|U_i0|^2+|U_i1|^2), and vacuum has probability(1-eta)^2. Those
expressions provide a separate all-sector check rather than reusing the loss
module as its own oracle.

## Acceptance and rejection

All metric prediction errors, independent full-law discrepancies, Perceval
discrepancies, total-probability errors and unitary residuals must be <1e-10.
All45 cells and all five circuits must be present. Any failure yields REJECT,
with the measured discrepancy and data preserved. There is no automatic
renormalization of measured/calculated laws to hide a failure. Float64 tests
are numerical checks, not interval-certified mathematical proof.

## Execution and output boundaries

Entry point: `experiments/scripts/validate_sharpness_pilot.py`.
Frozen results directory:
`results/validated/P40_sharpness_pilot_2026-11-24/`.
The script must refuse an existing output directory. Outputs are new and
immutable; no previous run is overwritten or silently relabeled. Raw JSONL
contains every cell and complete partial/distinguishable all-sector laws.
Circuit JSON contains all five matrices, angles, serializations and ideal
reference laws. Summary and manifest record actual command, versions, CPU/wall
time, numerical errors, source/contract hashes before and after, and the
contract commit. Result paths are declared before execution.

Hard run limits: CPU60 seconds, wall90 seconds, one BLAS/OpenMP thread.
Perceval is local SLOS only. Missing Perceval is a failed/unexecuted validation
gate, not a silently passed cross-check. The downstream tests read and audit
the exported45 cells; they do not launch another45-cell campaign.

Only this contract, the new script, its new results, tests/test_sharpness_pilot.py
and docs/DENSITY_PILOT.md are authorized writes. The documentation must say that
the loss model is known by assumption, the ideal fixed-N theorem cannot simply
be applied to unconditioned lossy moments, and PNR availability/QPU suitability
are unknown. These are testable calibration predictions plus controls against
an advantage illusion, not a new discovery or an authorization for hardware.
