# QPU readiness — 24 November 2026

**OFFLINE_PILOT_READY=TRUE. HARDWARE_COMPATIBILITY_VERIFIED=FALSE. QPU_GATE=CLOSED.**
No real QPU job, hardware credit or external transmission has occurred.

Mise à jour livraison Lucy/TGCC : un [adaptateur distinct](../docs/LUCY_TGCC.md)
implémente la route officielle CEA et est testé localement avec un transport
simulé. Il exige un plan scellé, une autorisation opérateur, des confirmations
PNR/routage/calibration, un seul job et des plafonds explicites. L'accès réel
et la fidélité de ces confirmations restent inconnus. Le gate reste CLOSED.

| Gate | Status | Evidence / missing element |
| --- | --- | --- |
| Graph/physics definitions | PASS locally | n4k2 full Fock identity/HOM/pair mixing; K4 optimum4 and K2,2 optimum2 |
| Independent local references | PASS | analytic two-photon formula, project Ryser and Perceval SLOS |
| Circuit export and compilation | PASS locally | BS/PERM reconstruction and serialization round-trip, global-phase comparison; no native backend compilation claim |
| Reproducible preparation pipeline | PASS | seven commands; qpu/offline_pilot_20261124_v1/ and separate supervisor reproduction |
| Immutable synthetic result handling | PASS | full occupation counts, known/unknown attempt denominator tests, separate output and SHA records |
| Hardware result ingestion | Implemented bounded schema, unverified export | PNR internal schema works; actual provider export and anomalies must be validated |
| Actual backend/account availability | UNKNOWN | official docs do not inspect this account; no network/account call |
| Native routing, source and detector | UNKNOWN | supported inputs/modes, PNR versus threshold, recycling/filter/attempt semantics and compilation need confirmation |
| Hardware loss/overlap calibration | UNKNOWN | no invented Belenos noise parameters; theoretical simulator only |
| Optimization benefit gate | NO-GO for tested route | E05b and stronger classical controls do not demonstrate desired benefit |
| Execution authorization and credits | NOT GIVEN / ZERO CONSUMED | explicit future authorization required before any submission |
| Publication hardware claim | ABSENT | offline/synthetic evidence clearly labeled; no QPU data in paper |

The ready local deliverable is [the Laurent dossier](../docs/LAURENT_HANDOFF.md). It prepares a feasibility/calibration pilot. The original scripts under qpu/ remain closed; the historical offline module has no submission code. The separate Lucy adapter contains the guarded submission path and is never invoked by CI or the research agents. A local mock-transport test does not validate native hardware or a quantum speedup.

Supervision receipt: recovery_2026-11-24/supervisor_offline_pilot_receipt.json. Future submission additionally needs a reviewed provider adapter and authorized concrete job. No authorization is inferred from asking for a QPU section.
