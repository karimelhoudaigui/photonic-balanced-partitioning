# Independent Astra review of the first Qwen research cycle

Date: 2026-11-21. Scientific decision: **INCONCLUSIVE**. Operational decision:
**REJECT advancement to QPU or manuscript writing from this diagnostic.**
The observed calculations are accepted within their finite scope. Qwen's
scientific narrative is rejected. No general impossibility result follows.

## Contract and actual execution

Question: does the current collision-aware n4 protocol demonstrate a useful
interference-dependent optimization mechanism?

The protocol was supplied by Astra before execution: three fixed graphs
(path, cycle, weighted), two photons in four modes, a full rectangular mesh,
three initial seeds and three separate replication seeds, and both bosonic and
reoptimized distinguishable controls. Each run receives 32 exact objective
evaluations. Input phases are fixed to zero; twelve active parameters remain.
All graphs, seeds and both statistics are retained; no favorable subset was selected.

The training loss is conditional cut energy plus `2*(1-P_CF)`. The optimum is
enumerated only for diagnostics and does not enter the training loss. This avoids
the old subnormalized-energy bug. The historical physics/objective repairs
already exist; this cycle did not need another rewrite of the scientific package.
The script's hardcoded INCONCLUSIVE label is a safeguard, not experimental evidence.

Actual Qwen commands in the retained stream logs include:

```sh
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest tests/test_hom.py tests/test_objectives.py tests/test_perceval_cross_validation.py -q 2>&1 | head -50
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python scripts/qwen_n4_probe.py --output results/qwen_n4_first_cycle
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python scripts/qwen_n4_probe.py --seed-offset 100 --output results/qwen_n4_replication
```

The pytest tool response contains **58 passed**. The two probe commands each
produced 18 runs and 576 objective evaluations. There were no physical shots.
The first worker timed out after generating data and an incorrect report.
The critic reached its time/turn limit without a report. Astra then dispatched
only the previously unstarted replication, within the original absolute
20-minute deadline; it generated data but failed to finish its report. These
process failures remain INCONCLUSIVE in their original records. They are not
silently converted into successful autonomous cycles.

Initial seeds: 20261121, 20261122, 20261123.
Replication seeds: 20261221, 20261222, 20261223.

Evidence is preserved under `results/qwen_cycles/20261121T002702Z-cycle/`,
`20261121T003401Z-cycle-resume/` and `20261121T004103Z-supervised-replication/`.
Raw scientific files were copied byte-for-byte into
`results/qwen_n4_supervisor/{initial,replication}/`; hashes and original locations
are in `results/qwen_n4_supervisor/provenance.json`. The isolated worker branch
retains its own original files. No automatic merge occurred.

## Independently checked results

These are arithmetic means over three specified seeds per cell, **without
estimated uncertainty or population significance**. Success is unconditional
physical probability on optimal collision-free outcomes, not postselected success.

| Fixed graph | Initial bosonic | Initial distinguishable | Replication bosonic | Replication distinguishable | Uniform feasible |
|---|---:|---:|---:|---:|---:|
| path | 0.796055 | 0.919437 | 0.864640 | 0.667158 | 1/3 |
| cycle | 0.988357 | 0.974014 | 0.715280 | 0.984862 | 2/3 |
| weighted | 0.676180 | 0.728681 | 0.731545 | 0.896827 | 1/3 |

Here “initial” means the first seed batch's **final trained sampler**, not the
unoptimized circuit. Original and replication summaries retain the unoptimized
metrics separately. The small initial cycle advantage reverses on fresh seeds.
Path also reverses ordering. Weighted favors distinguishable sampling in both
batches. These observations do not establish a stable interference benefit.

Astra ran `scripts/audit_qwen_n4.py` on the retained copies. It independently
enumerates graph cuts and uses explicit two-photon formulas, instead of the
training evaluator, to recompute every recorded metric and loss at all **1,152**
parameter evaluations. It checks the exact graph/seed/model grid, identical
paired initial parameters, best-loss iterate selection, original source hash,
physical normalization bounds and disjoint replication seeds.

For all **18** best bosonic circuits, it additionally reconstructs full Perceval
SLOS distributions. Maximum probability discrepancy: **3.3306690738754696e-16**.
Maximum absolute discrepancy across recomputed metrics: **5.684341886080802e-14**.
The operator preflight and Qwen's initial scientific rows also match exactly.

Canonical audit: `results/qwen_n4_supervisor/audit/audit.json` and its v2
`manifest.json`. The Mathbox manifest validator passes with current input/output
hashes. An earlier audit's numerical outputs are retained in
`results/qwen_n4_independent_audit/`; its absolute-path manifest was superseded
by the validated project-relative canonical record. It is not the acceptance record.

## Refutation and report rejection

The unmodified Qwen narrative is preserved as
`results/qwen_n4_supervisor/REJECTED_QWEN_CYCLE_RESULT.md`. It invented ± values,
mixed path and cycle results, incorrectly used 1/3 as a universal uniform
baseline, and gave an incorrect trials/seeds explanation of 576 evaluations.
None of those assertions is accepted or promoted into CLAIMS.md. The lead's
initial proposed decision rule is likewise not an independent scientific gate.

The numerical improvement from untrained to trained samplers is compatible with
ordinary optimization in both statistics. This n4 problem has only six feasible
bitstrings: exact classical enumeration can solve it with six cut evaluations.
The photonic training evaluations each inspect an exact feasible distribution.
Equal optimizer-call counts are useful local controls but do not establish an
equal total classical computation or physical-shot budget. Absence of physical
shots is not by itself a refutation of every possible simulation result; it
limits the claims about sampling and hardware here.

There is no verified novelty claim, scaling benefit, equal-shot training benefit,
noise robustness or hardware result. A new mechanism must first be stated and
tested against strong feasible classical and reoptimized distinguishable controls.
The current generic n4 protocol supplies no reason to reopen the manuscript or QPU gate.

## Supervisor disposition

- KEEP: observed tool execution, raw data, finite numerical checks and Perceval agreement.
- REJECT: invented narrative quantities and autonomous scientific acceptance by the local 2B model.
- FOLLOW-UP: a changed optimum-blind, label-invariant mechanism from OPEN_QUESTIONS.md;
  this infrastructure installation does not supply that mechanism.

The full working repository passes **192 tests**. The canonical evidence audit is
independent of Qwen's prose. Manuscript hashes were unchanged in the root and
worker checkout; the OS guard denied manuscript writes. No QPU calls occurred.
`PAPER_READY=FALSE`; `QPU_GATE=CLOSED`. The overall research objective remains open.
