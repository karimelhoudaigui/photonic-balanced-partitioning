# Supervisor review of P40 — 24 November 2026

**Decision: retain as a known-model physical calibration prediction; no optimization or hardware advantage.**

The advance contract efd1718 was committed before the one45-cell execution. Its exact original text is preserved; none of its proposed formulas, grid points, tolerances or failed/zero cases was changed after execution. The script has the same hash as the input frozen before the run. Root integration b997182 retains raw b3189ac6143c31654d97d06209a94494281b25c43b37c5cd33782014bd277658 unchanged.

All45 stored full-sector laws and five Perceval circuit references pass the stated1e-10 comparisons; the TV/pair/path prediction errors are below1e-16. This supports implementation agreement with the supplied exact two-photon model. It is not a hardware measurement, a fit of unknown loss/overlap, an arbitrary multiphoton model or a graph-search trial.

The manuscript formula was independently derived by the mathematical reviewer without reading P40 outputs or earlier verdicts (v1 math-adversarial checks MA-C007/008). The noise/P40 author separately rechecked all stored metrics; that is disclosed self-authorship, not an independent new45-cell replication. Root ran the integrated export/provenance tests and inspected the actual commands, full laws, angle conventions, serialized U and data pins.

## Interpretive correction raised by the physics reviewer

The archived numeric control η²/3 is correct for a uniform classical choice of feasible Fock string followed by its optical preparation and the common loss channel. It is not the success probability of a standalone classical sampler, which has1/3 per classical draw and incurs no optical loss. The rate η² belongs to the optically prepared known-optimum identity control and is a state-preparation diagnostic.

This naming/denominator clarification leaves every data value and contract prediction unchanged. The paper and current explanatory dossier spell out the physical preparation step. Original contract/raw/run records remain unchanged; treating these as equal classical wall-clock costs would be unsupported.

P40 is an explicitly path-aligned two-photon calibration family. A same-U factor2 is neither unknown-optimum discovery nor an advantage over reoptimized/classically encoded controls. The local seven-command pilot separately supports only its three fixed circuits; the P40 exports are a supplemental local study, not a ready remote submission.

## Remaining gate

A real measurement requires account/backend compatibility, source/detector mapping, an authenticated physical-attempt denominator, independently supported loss/internal overlap, a prospective precision/shot plan and explicit authorization/credit cap. No device call, paid inference, article submission or message to Laurent was used.


## Portable reproduction verified

The original driver correctly remains frozen, but its exact-path and original-commit checks prevent a fresh integration-branch rerun. The separate scripts/replay_sharpness_pilot.py authenticates the archive and performs a new calculation without invoking or mocking those guards. Worker and supervisor runs are separately retained; they are reproductions, not new scientific campaigns.

The supervisor actually ran the new driver in a freshly installed pinned venv on scientific-recovery-publication. It returns REPLAY_MATCH for45 cells/five SLOS circuits, with zero archived full-law difference. CPU1.122414s, wall2.691921291s. Record: results/validated/P40_replay_supervisor_2026-11-24/. The unchanged archived source hash and original publication pins still validate.
