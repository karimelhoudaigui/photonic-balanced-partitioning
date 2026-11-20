# Hardware gates — CLOSED

PAPER_READY=FALSE. No QPU execution authorized or performed.

| Gate | Current evidence |
|---|---|
| Physics validation | PASS ideal cases; PHYSICS_VALIDATION.md |
| Perceval cross-validation | PASS; PERCEVAL_VALIDATION.md |
| Objective validation | PASS; OBJECTIVE_VALIDATION.md |
| Serious comparable baselines | PARTIAL:classical full-cube, Haar, uniform feasible and distinguishable controls; authentic optical ObliQ OPEN |
| Interesting ideal interference-dependent optimization signal | NO-GO for tested mesh; RESEARCH_CYCLE_2026-11-20.md |
| Precise hardware scientific hypothesis | OPEN |
| Final circuit and parameters frozen | NO |
| No tuning after QPU | Not applicable; no hardware protocol approved |
| Explicit authorization | NOT GIVEN |

The old connectivity and QPU scripts claimed local simulation as hardware evidence.
They now return status2 without network calls or result creation. The old Laurent
handoff is withdrawn. No token, backend connection or hardware preparation is
needed to continue the ideal research program. Source/detection losses, impurity,
detectors and phase noise have not been measured or modelled in this cycle.

Do not reopen this gate merely because simulator tests pass or an optimum is
prepared using its known bitstring. All scientific gates and explicit authorization
are required before implementing/launching a real Perceval remote backend.
