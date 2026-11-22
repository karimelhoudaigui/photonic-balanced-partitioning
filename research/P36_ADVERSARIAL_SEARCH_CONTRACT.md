# P36b: phase-sensitive adversarial search, not graph optimization

Checkpointc6c1807, 2026-11-22. The256-circuit grid did not refute TV<=delta,
but it does not settle the conjecture. A positive-permanent shortcut is
provably false. This continuation attacks nongeneric phase cancellations
directly with bounded classical counterexample search.

Two physical parameterizations, both with k3 distinct occupied columns:
all three-mode unitaries in standard three-angle/one-phase form, and general
six-by-three orthonormal frames obtained by QR around a disjoint-pair frame.
Every lossless complete Fock law is evaluated with explicit six routing terms;
the distinguishable law sums their squared moduli. No production sampler or
feasibility conditioning is used. The purpose is mathematical falsification,
not an efficient optimization algorithm for an unknown graph optimum.

Seeds20261140,20261141 and target leakages0.25,0.75 in both parameterizations.
Score=TV-min(1,delta)-10*(delta-target)^2. Record the score winner and the
largest unpenalized excess separately. Every call's parameters/delta/TV/score
goes to a raw JSONL trace; all runs are retained.
Three-mode search: differential evolution, population multiplier6,60iterations,
no polish, one worker. Six-mode search: Nelder-Mead, at most3000 evaluations.
At most18000 total calls, one thread,120-second external wall cap.

Falsifier: excess>1e-8 with normalization and orthogonality residuals<1e-11.
A candidate still needs independent Perceval and preferably exact rational
reconstruction before declaring a mathematical refutation. No counterexample
found means only this bounded search did not find one. No significance test,
universal proof, quantum advantage, physical shots or paper/QPU gate follows.
