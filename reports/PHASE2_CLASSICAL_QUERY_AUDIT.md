# P21 classical search evidence: supervised integration

The previously executed Phase2 dataset is retained unchanged. Its v2 manifest
passes current source/output hash validation. The coordinator inspected the
optimum-blind search code and its tests before making it available as a control
for the next optical experiment. No new experiment or QPU call was run here.

P21 covers n=4,6,8,10,12; six declared graph families; four graph seeds; original
and one permuted labeling; four search seeds; and three classical algorithms.
All 2,880 searches spend exactly 120 scored feasible-partition queries, including
repeats and rejected moves. The spectral method separately records its eigensolve
and setup time. Exact enumeration is evaluation-only, is not a stopping rule,
and records 61,056 additional reference evaluations. Total search evaluations:
345,600. Physical photonic attempts: zero.

The search routines never receive the optimum. The implementation has independent
known-cut, feasibility, exact-budget, repeatability and relabeling tests. All six
tests were included in the prior 192-test working-tree run. The validated manifest
is `experiments/P21_classical_search/manifest.json`; raw proposals and scores are
in its `runs.jsonl`. All unfavorable and censored searches remain present.

This is a finite classical diagnostic, not a comparison at an equivalent hardware
shot budget or a general complexity result. The graph generator is not a uniform
graph-population sampler. Path/cycle repeats and paired labels are dependent;
the recorded success fractions are descriptive. It provides stronger relevant
controls than comparing a photonic sampler only with its random initialization.
The accompanying phase/gauge probes are exploratory and are not advantage evidence.

Decision: KEEP as a reproducible control. No manuscript or hardware gate changes.
