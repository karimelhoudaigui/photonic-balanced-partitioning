# Quarantined P47 post-hoc headroom contract

2026-11-25, AFTER P47 source, DEV outcomes and physics interpretation were
frozen. This is an evaluation-only diagnostic on ALL FOUR closed P47 graphs,
not a new guide, training signal, held-out result or proposed positive.
Coordinator requested contract/code freeze before calculation and an explicit
ROOT slot grant after that freeze. **No MILP has been run at this checkpoint.**

The isolated copies in `experiments/P47_headroom_quarantine/inputs/` are
BYTE IDENTICAL to the P47 manifest, summary and four context files. Their
six SHA256 values are hardcoded in solve.py and pinned as runner inputs.
The primary manifest identifies the closed source run; the primary raw hash
is aa1386b93104ba1941ebc9d0cdde8488278f86a9bfeb7cd6f0632a83b359d562.
No P48 graph, encoder, code, data or optimum is read. No graph regeneration,
label selection, random instance replacement or solver-result training occurs.

## Finite mathematical question and model

For each old N26/34 integer-weight undirected graph, estimate how much room
remains below the observed best cut and below the classical best. Binary
x_i are vertices on one side, sum_i x_i=N/2, x_0=1. For each positive
undirected edge i<j introduce continuous z_ij in[0,1] with

    z_ij >= x_i-x_j,  z_ij >= x_j-x_i.

Minimize sum_(i<j) w_ij z_ij. Positive weights imply z=|x_i-x_j| at an
optimum, so this MILP models balanced minimum cut exactly over the REALS
with x integral. The symmetry break x0=1 is harmless for an undirected
balanced cut: exactly one of a partition/complement has vertex0 on that
side and both have the same cut. Feasibility is already known from the
archived scored candidates, independently of solver success.

The solver itself is FLOAT64 SciPy milp/HiGHS. Its reported dual bound,
optimal status and gaps are estimates, not rational, interval or exact
optimality proofs. No flooring/rounding of a dual bound is promoted into
an exact certificate. An incumbent is checked in memory for binary/balance/
x0 consistency and its scalar objective is recomputed as an integer graph
cut. Only that SCALAR, status, lower-bound estimate, observed costs, gap
estimates and provenance/timing are exported. No assignment, partition,
vertex mask, partition hash or solver OptimizeResult repr is saved/printed.

The quantities C_observed-LB and C_classical-LB are gaps TO AN ESTIMATED
LOWER BOUND. They are not known distances from the true optimum. Limit/
failure/unresolved cases remain; a lower estimate exceeding a known
feasible scalar flags inconsistency. No runner PASS makes these exact.

## Leakage guard and resources

The script has no configurable graph source and imports no encoder/training
or primary calculation module. Its strict input-name/hash allowlist rejects
P48 and changed inputs. Only fresh
`experiments/P47_headroom_quarantine/run_001/data` is accepted, and a
posthoc-specific CLI flag is mandatory. Scalar results stay in this
quarantine and evaluation receipt; they must not feed P48 settings, decoder,
source preparation, incumbent, graph selection or later held-out claims.
They may describe ONLY the already closed four P47 graphs. The flag does
not substitute for the explicit coordinator authorization still pending.

Each of four HiGHS solves has time_limit5s. Runner limits are global CPU25s,
wall40s, one thread and logs/data1MiB. No hard macOS affinity/memory claim is
made. SciPy forwards HiGHS threads1, parallel off, random_seed47047;
the pinned SciPy wrapper requires boolean parallel=False and converts it
to native "off". The bundled native HiGHS options object is configured and
read back as threads1/parallel off before any solve. A native-wrapper
OptimizeWarning about ignored/invalid options is treated as a failure;
the expected public RuntimeWarning about forwarded options is retained
in each scalar row. Cases process in fixed
order and flush one scalar row at a time, preserving partial output if
the global runner limit interrupts. No automatic retry or replacement.

The declared environment is Python3.11.15, NumPy2.4.6, SciPy1.17.1, checked
again before solving. Official
[SciPy 1.17 milp documentation](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.optimize.milp.html)
defines the mixed integer constraints, statuses and estimated dual bound.
Installed _milp.py and its generic HiGHS option forwarding were inspected
read-only; _milp_iv passes CSC index arrays through rather than promising
an int32 cast. The script constructs CSC with explicit int32 indices/indptr
and records those dtypes. The local solver/version has not been executed
by this package.

Code, this note, JSON runner contract and six input copies must be committed
BEFORE a run. Use the Mathbox v2 bounded runner under the replication
worktree, with the exact nine execution_artifacts repeated as --input.
Planned child argv (NOT EXECUTED):

    /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P47_headroom_quarantine/solve.py --output experiments/P47_headroom_quarantine/run_001/data --execute-posthoc-p47-only

Runner output: `experiments/P47_headroom_quarantine/run_001`; declared
results: its `data/records.jsonl` and `data/summary.json`. Manifest validation
with --root is required afterwards. A resource-limited run is inconclusive;
solver time limits are reported per case. Genuine bugs/failures and all
negative diagnostics remain preserved. No paper, raw, QPU, push or registry
change is authorized by this diagnostic. Results do not settle any general
physical difficulty or algorithmic advantage question.
