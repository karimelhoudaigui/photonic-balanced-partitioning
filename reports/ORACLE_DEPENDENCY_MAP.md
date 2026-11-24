# Optimum information: training/evaluation map — 24 November 2026

The project has two intentionally separate paths. New reusable training code uses `optimization.training_loss`, which accepts costs and feasibility and has no optimum, optimal-partition or optimal-mask argument. Existing archived diagnostic code retains success-to-known-optimum experiments for traceability.

| Path / call site | Optimum information | Allowed interpretation |
| --- | --- | --- |
| `problems/min_bisection.py`, exact enumerators | Solves the tiny reference instance | Classical reference cost, never a free input to an unknown-optimum algorithm |
| `photonic/objectives.py:distribution_metrics` | Computes/accepts exact optimal energy on supplied CF rows | Retrospective reference diagnostic; caller must supply full balanced support for a global reference |
| `photonic/objectives.py:objective_value`, success/physical_success/factorized/conditional_success | Uses reference success or optimal-conditional mass | Oracle-assisted objective only; legacy compatibility retained and documented |
| `optimization/objectives.py:training_loss` | No optimum input; oracle objective names rejected | Accessible ideal/observed loss; full distribution/cost computation is still charged |
| `photonic/collision_aware.py:expected_objective/optimize` | Uses the new loss, no retrospective metrics call | Optimum-blind library random-search reference; not a claim of a newly validated optimizer |
| `experiments/run_research.py:loss` and E02/E03/E04/E07 success arms | A reference optimum enters the diagnostic and success target | State preparation; classify each objective arm, not every campaign as one algorithm |
| E01 and `run_research.py` retrospective metrics | Reference optimum for Haar scoring | Ensemble calibration, no trained solver claim |
| `experiments/run_equal_budget.py` E05b | Computes reference during setup; sampled training loss fixed before hit labels; selection minimizes recorded loss | Training optimum-blind; reference setup/cost tables still classical resources, labels retrospective |
| `experiments/run_label_control.py` E09 | Exact optimum and structural reachability/success | Oracle/label diagnostic, not blind search generalization |
| `experiments/phase2_classical_search.py` P21 | Reference construction/scoring separated from fixed-budget search with no optimum argument/stopping | Classical optimum-blind search; count preprocessing and cut queries separately |
| `hardware/offline.py` reference and result analysis | Exact four-node cuts to annotate pilot outcomes | Calibration/decoding diagnostic; circuits fixed, no optimization or oracle advantage |
| P33/P37 theory and probes | No graph optimum needed for certificate or feasibility | No graph-quality enrichment follows |
| P40 fixed sharpness pilot | Analytic path optimum and known-optimum identity control | Fixed-circuit physical predictions and countercontrol, not search evidence |

The anti-oracle tests reject all success-target names in the new interface and monkeypatch the retrospective oracle to fail while the public CollisionAwareSolver still evaluates and trains. The numerical reconciliation separately reconstructs every E05b training loss and selection. These checks enforce the audited interfaces/protocol; Python cannot prevent a caller from encoding hidden answers into an arbitrary supplied cost table.

The setup reference in E05b means the simulation is not an end-to-end black-box runtime benchmark. Heldout means new draws at the trained graph, not new test graphs. All oracle arms, reference enumeration, failures and negative controls remain in the archive.
