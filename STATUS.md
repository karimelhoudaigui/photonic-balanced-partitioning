# Current research status — 2026-11-20

PAPER_READY = FALSE. QPU_GATE = CLOSED.
NO-GO for claiming computational benefit from the tested generic bosonic mesh.
The general research question remains OPEN. No QPU or noise experiment was run.

[Scientific checkpoint and figures](reports/RESEARCH_CYCLE_2026-11-20.md)
are authoritative; older feasibility text is historical and superseded.

Completed and actually executed:

- Full Fock/HOM/phase/vacuum validation; Perceval PASS,8464 outcomes, max probability error1.776e-15.
- Objectives, collision-aware solver, weighted conditional lower CVaR and full binary classical penalty repaired.
- 142 tests pass in the pinned .venv.
- E01:3250 Haar circuits, n4/6/8/10.
- E02/E03/E04: optimization, objectives, depths, optimizers and distinguishability controls.
- E05b:756 runs at exactly34816 ideal draws each;26,320,896 simulated attempts including training discovery.
- E06b:pair-moment checks; original failed tolerance assertion preserved.
- E07:spectral hybrid;27/36 graph slots already classically solved by the anchor.
- E08:TV certificate and balanced counterexample;240 full-distribution checks,9rational cases, full Fock n4/8/12.
- E09:240 relabeling/reachability runs.
- Raw data, commands, commits, seeds, hashes, independent reviews and five PNG/PDF figures retained.

Validated theoretical checkpoint: P_CF->1 does not force TV to distinguishable
statistics to zero uniformly, even for k=m/2. Spatial-overlap TV certificates and
a counterexample have independently checked proofs. Novelty is OPEN.

Still open / deferred:

- Exact optical ObliQ dynamics and a physically comparable penalty encoding.
- Literature novelty audit of the new mathematical notes.
- Useful optimum-blind, label-invariant graph-informed search beating feasible classical discovery.
- Hardware source/detection loss accounting and noise; deferred because ideal benefit is unestablished.
- Optimized n10 studies, larger/harder preregistered populations and graph-cluster inference.

Continuation contract: OPEN_QUESTIONS.md; decisions: DECISIONS.md;
all scientific claims and statuses: CLAIMS.md. Manuscript remains frozen.

## 2026-11-21 — supervised local Qwen infrastructure

Qwen Code0.28.0 and Ollama0.32.0 are installed externally,with one Qwen3.5-1.9B
Q4_K_M model on the measured M2/8GiB host. Seven roles and a bounded worktree
launcher are versioned. Basic repo access,tool calls,Python tests and report
creation PASS;native SUBAGENTS and AGENT TEAM probes FAIL. Do not call this a
validated autonomous research team. No paid API or QPU was used.

The first supplied n4 diagnostic and fresh-seed replication actually generated
36 runs/1152 exact objective evaluations. Astra verified every recorded metric
and18best bosonic circuits against Perceval. Qwen's prose report was rejected
for invented uncertainty and mixed graph results;critic/report completion also
failed its caps. A stable interference benefit was not established. Scientific
decision:INCONCLUSIVE;no manuscript/QPU advancement. See
reports/ASTRA_QWEN_FIRST_CYCLE_AUDIT.md and reports/QWEN_INFRASTRUCTURE_VALIDATION.md.
The complete working tree passes192 tests,including42 earlier Phase2 draft tests
outside the scoped infrastructure changes. The142-test scientific checkpoint
above remains historical;the infrastructure adds8guardrail tests.
