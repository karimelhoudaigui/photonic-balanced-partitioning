# Corrected QPU preparation protocol — 24 November 2026

The earlier protocol's submission-ready and device capability assumptions are withdrawn. **No device access or execution is authorized.**

The operational local protocol is [docs/LAURENT_HANDOFF.md](../docs/LAURENT_HANDOFF.md), with [qpu/README.md](../qpu/README.md), [official compatibility matrix](../docs/QPU_COMPATIBILITY.md), and [QPU readiness](QPU_READINESS.md). It fixes a four-mode/two-photon identity/HOM/pair-mixing pilot, full Fock references, graph decoding, local BS/PERM compilation and serializable Perceval circuits.

Seven offline commands run from graph/configuration to synthetic count analysis. prepare_qpu_job produces an internal non-submitting draft; it is not a Quandela API request. No remote adapter or account-specific detector/route/compiler capability is claimed.

This pilot tests a small optical law and denominator accounting, not an optimization advantage. Known-optimum success may be scored retrospectively; it is forbidden as an unknown-optimum training target. Emission attempts and accepted coincidences must never share an implicit denominator.

Future device work requires Laurent's technical assessment, actual backend capabilities/calibration, a verified counts/attempts export and an explicit authorized credit/attempt cap. No message has been sent to Laurent.
