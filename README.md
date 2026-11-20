# Photonic Balanced Partitioning — research in progress

Can collision-aware fixed-particle optics improve graph bisection at equal
physical sampling and classical search cost? The tested generic-mesh route
currently gives **NO-GO for a benefit claim**. The manuscript is frozen and
hardware execution is disabled.

Read the [executed research checkpoint](reports/RESEARCH_CYCLE_2026-11-20.md),
[claims registry](CLAIMS.md) and [continuation questions](OPEN_QUESTIONS.md).

## Reproduce locally

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements-research-lock.txt
.venv/bin/python -m pip install -e '.[all]'
PYTHONPATH=src .venv/bin/python -m pytest tests/ -q
```

The pinned environment was actually tested with Python3.11.15, NumPy2.4.6,
SciPy1.17.1, Perceval1.3.0 and exqalibur1.4.2. The Perceval distribution package
is `perceval-quandela`. Installing it does not authorize any QPU access.

Every main run has a manifest with exact command, source commit, seed formulas,
source hashes and raw-output hashes. To replay a numerical run on another machine,
use its manifest command with a local interpreter and a **new** output directory:

```sh
PYTHONPATH=src .venv/bin/python experiments/run_research.py haar --output /tmp/haar-replay
PYTHONPATH=src .venv/bin/python experiments/run_equal_budget.py --output /tmp/budget-replay
PYTHONPATH=src .venv/bin/python experiments/run_coherence_check.py --output /tmp/coherence-replay
PYTHONPATH=src .venv/bin/python experiments/run_label_control.py --output /tmp/labels-replay
PYTHONPATH=src .venv/bin/python experiments/audit_results.py
MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/plot_results.py
```

The optional launchers use an installed Mathbox recorder and its environment-specific
path; direct numerical scripts are portable. Historical manifests verify against
their exact Git revision when newer scripts have changed. Raw data are never
silently replaced, including the failed E06 check and the superseded E05 protocol.

## Evidence and limitations

- Physics and Perceval validation PASS:8464 output states, maximum probability error1.776e-15.
- E01:3250 Haar circuits across n4/6/8/10 reproduce the known collision-free law.
- E05b:756 runs with exactly34816 simulated ideal attempts each; all training draws counted.
- A proved balanced-density counterexample has P_CF->1 but TV(bosonic,distinguishable)=1/2.
- Novelty of the new overlap certificate/counterexample is OPEN; Haar scaling is known.
- The full binary penalty baseline is explicitly classical. `PenaltyObliq` is a deprecated alias,
  not an implementation of actual optical ObliQ dynamics.
- The regular generator preserves degree through edge switches, but is not uniform.
- Tiny exact-enumeration simulations, descriptive fixed-grid summaries and oracle-success
  diagnostics cannot establish scalable advantage or hardware performance.

Plots and their standalone PDF counterparts are in `reports/figures/`.
No noise or hardware result is asserted. `LAURENT_HANDOFF.md` is withdrawn;
`qpu/` entrypoints fail closed. Earlier manuscript text is not validated evidence.
