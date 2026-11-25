"""Quarantined POST-HOC P47-only MILP; scalar exports, no optimum partitions.

Execution requires the coordinator's explicit post-freeze numerical-slot grant.
This file imports no encoder, decoder, training, P48 or primary probe module.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import warnings

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
EXPECTED = {
    "primary_manifest.json": "991b561e6186fbd27ace880e4ee503b0aa75766d362ce5fc1f04f4127853be8a",
    "summary.json": "e2187b5c2a2c3abd79bc8d02076e0fe0e0b1a0a071c8520589e0705df66dad2e",
    "context_n26_ER_4702601.json": "3aba076a05be1553ffdf2be02666affd6f035477d01b523425f17789d3f88318",
    "context_n26_RR_4702602.json": "d0b09872f11865c9803fee342d259cc97896177dcb50ff592049794ea66cdf53",
    "context_n34_ER_4703401.json": "7af0a793f084e2ec0fb4bd5a9a86bb349ef5ab70dc851a876ae098654c503b3d",
    "context_n34_RR_4703402.json": "97f6de5ec542386b8e6cf43ae50030598bab9c473503baedd730215a3765623b",
}
CASES = ("n26_ER_4702601", "n26_RR_4702602", "n34_ER_4703401", "n34_RR_4703402")
CLASSICAL = {"anneal", "spectral_swap", "KL_collective", "block_matching"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def finite(value):
    return float(value) if value is not None and math.isfinite(float(value)) else None


def observed(summary, context, case):
    by_method = {}
    for row in summary["records"]:
        if row["case"].split(":")[0] == case:
            name = row["model"]
            by_method[name] = min(by_method.get(name, context["Cref"]), int(row["best_cut"]))
    if not CLASSICAL.issubset(by_method):
        raise ValueError("Closed P47 classical population missing")
    return {
        "frozen_Cref": int(context["Cref"]),
        "observed_best_by_method": by_method,
        "observed_best_all": min([int(context["Cref"])]+list(by_method.values())),
        "observed_best_classical": min(by_method[name] for name in CLASSICAL),
    }


def solve_case(context):
    # Numerical imports happen only after immutable-input and destination guards.
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, OptimizeWarning, milp
    from scipy.sparse import coo_matrix

    a = np.asarray(context["adjacency"], dtype=float)
    n = len(a)
    if n not in (26, 34) or a.shape != (n, n) or not np.array_equal(a, a.T):
        raise ValueError("Unexpected quarantined graph shape")
    if np.any(a < 0) or not np.all(a == np.rint(a)) or np.any(np.diag(a)):
        raise ValueError("Expected nonnegative integer undirected graph without loops")
    edges = [(i, j, int(a[i, j])) for i in range(n) for j in range(i+1, n) if a[i, j] > 0]
    variables = n+len(edges)
    objective = np.zeros(variables)
    objective[n:] = [w for _, _, w in edges]
    integrality = np.zeros(variables, dtype=np.uint8)
    integrality[:n] = 1
    row_indices, col_indices, coefficients = [], [], []
    for i in range(n):
        row_indices.append(0); col_indices.append(i); coefficients.append(1.)
    row_indices.append(1); col_indices.append(0); coefficients.append(1.)
    lower = [n//2, 1.]; upper = [n//2, 1.]
    for e, (i, j, _) in enumerate(edges):
        for sign in (1., -1.):
            row = len(lower)
            # z_e - sign*(x_i-x_j) >= 0.
            row_indices.extend((row, row, row))
            col_indices.extend((n+e, i, j))
            coefficients.extend((1., -sign, sign))
            lower.append(0.); upper.append(np.inf)
    matrix = coo_matrix((coefficients, (row_indices, col_indices)),
                        shape=(len(lower), variables)).tocsc()
    # The pinned _milp_iv passes CSC index arrays through; keep their exact
    # int32 representation explicit for these small models/native bindings.
    matrix.indices = matrix.indices.astype(np.int32, copy=False)
    matrix.indptr = matrix.indptr.astype(np.int32, copy=False)
    started = time.perf_counter()
    with warnings.catch_warnings(record=True) as forwarded:
        # The public SciPy RuntimeWarning about forwarded options is retained;
        # a HiGHS OptimizeWarning that an option is ignored/invalid is a failure.
        warnings.simplefilter("error", OptimizeWarning)
        warnings.simplefilter("always", RuntimeWarning)
        result = milp(objective, integrality=integrality, bounds=Bounds(0., 1.),
                      constraints=LinearConstraint(matrix, lower, upper),
                      options={"time_limit": 5., "mip_rel_gap": 0., "presolve": True,
                               "disp": False, "threads": 1, "parallel": False, "random_seed": 47047})
    # threads/parallel/random_seed are HiGHS options forwarded by SciPy; its
    # warning is retained in the scalar row, not mistaken for a test PASS.
    incumbent = None
    feasible_checked = False
    if result.x is not None:
        vertices = np.asarray(result.x[:n])
        rounded = np.rint(vertices).astype(int)
        if (np.max(abs(vertices-rounded)) > 1e-6 or rounded.sum() != n//2
                or rounded[0] != 1 or np.any((rounded < 0) | (rounded > 1))):
            raise ArithmeticError("Solver incumbent fails scalar feasibility check")
        exact_cost = sum(w*abs(int(rounded[i])-int(rounded[j])) for i, j, w in edges)
        if result.fun is None or abs(float(result.fun)-exact_cost) > 1e-5:
            raise ArithmeticError("Solver objective disagrees with direct integer cut")
        incumbent = int(exact_cost)
        feasible_checked = True
        # No vertex set, assignment, edge pattern or partition digest is exported.
        del vertices, rounded
    answer = {
        "status_code": int(result.status),
        "solver_reports_optimal_float64": bool(result.status == 0 and result.success),
        "solver_dual_bound_float64_estimate": finite(getattr(result, "mip_dual_bound", None)),
        "solver_incumbent_cost_scalar_only": incumbent,
        "incumbent_integer_cut_checked_in_memory": feasible_checked,
        "solver_relative_gap_float64": finite(getattr(result, "mip_gap", None)),
        "solver_node_count": int(result.mip_node_count) if getattr(result, "mip_node_count", None) is not None else None,
        "elapsed_solver_wall_seconds": time.perf_counter()-started,
        "vertices": n, "positive_edges": len(edges),
        "csc_indices_dtype": str(matrix.indices.dtype), "csc_indptr_dtype": str(matrix.indptr.dtype),
        "scipy_forwarding_warnings": [str(w.message) for w in forwarded],
        "partition_exported": False,
    }
    del result
    return answer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execute-posthoc-p47-only", action="store_true", required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output != (HERE/"run_001"/"data").resolve() or output.exists():
        raise ValueError("Only a fresh quarantined P47 run_001/data destination is allowed")
    inputs = HERE/"inputs"
    if set(p.name for p in inputs.iterdir()) != set(EXPECTED):
        raise ValueError("Immutable P47 input closure mismatch; no P48 inputs allowed")
    hashes = {name: digest(inputs/name) for name in EXPECTED}
    if hashes != EXPECTED:
        raise ValueError("Frozen CLOSED P47 input hashes differ")
    primary = json.loads((inputs/"primary_manifest.json").read_text())
    summary = json.loads((inputs/"summary.json").read_text())
    if (primary["run"]["status"] != "completed" or summary["positive_accepted"]
            or summary["code_sha256"] != "fac164f64a3ba15a061c56547be58f5c540486852c9016ccc70a129637ca53b1"):
        raise ValueError("Expected frozen completed P47 DEV archive")
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS",
                 "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[name] = "1"
    import numpy as np
    import scipy
    if (sys.version_info[:3] != (3, 11, 15) or np.__version__ != "2.4.6"
            or scipy.__version__ != "1.17.1"):
        raise RuntimeError("Unreviewed numerical environment; no automatic replacement")
    # This is the same bundled native options object/readback path used by the
    # pinned SciPy wrapper. No model is loaded or solved by this configuration check.
    import scipy.optimize._highspy._core as native_highs
    native = native_highs._Highs()
    native_options = native_highs.HighsOptions()
    native_options.threads = 1
    native_options.parallel = "off"
    if native.passOptions(native_options) != native_highs.HighsStatus.kOk:
        raise RuntimeError("Native HiGHS rejected single-thread options")
    thread_status, native_threads = native.getOptionValue("threads")
    parallel_status, native_parallel = native.getOptionValue("parallel")
    if (thread_status != native_highs.HighsStatus.kOk or native_threads != 1
            or parallel_status != native_highs.HighsStatus.kOk or native_parallel != "off"):
        raise RuntimeError("Native HiGHS single-thread readback failed")
    del native, native_options
    output.mkdir(parents=True, exist_ok=False)
    cpu, wall = time.process_time(), time.perf_counter()
    rows = []
    with (output/"records.jsonl").open("x") as stream:
        for case in CASES:
            context = json.loads((inputs/f"context_{case}.json").read_text())
            row = {"case": case, **observed(summary, context, case)}
            try:
                row.update(solve_case(context))
                bound = row["solver_dual_bound_float64_estimate"]
                if bound is not None:
                    row["observed_best_minus_solver_bound_estimate"] = row["observed_best_all"]-bound
                    row["classical_best_minus_solver_bound_estimate"] = row["observed_best_classical"]-bound
                    if bound > row["observed_best_all"]+1e-5:
                        raise ArithmeticError("Solver lower-bound estimate exceeds known feasible scalar")
                row["interpretation"] = ("FLOAT64_SOLVER_OPTIMAL_NOT_EXACT_CERTIFICATE"
                    if row["solver_reports_optimal_float64"] else "BOUNDED_OR_UNRESOLVED_FLOAT64_DIAGNOSTIC")
                if row["status_code"] not in (0, 1):
                    row["interpretation"] = "INCONSISTENT_OR_SOLVER_FAILURE_KNOWN_FEASIBLE_GRAPH"
            except Exception as exc:
                row["interpretation"] = "INCONCLUSIVE_EXCEPTION_RETAINED"
                row["error_type"] = type(exc).__name__
            row["posthoc_only"] = True
            stream.write(json.dumps(row, allow_nan=False)+"\n"); stream.flush()
            rows.append(row)
    if {name: digest(inputs/name) for name in EXPECTED} != hashes:
        raise RuntimeError("Quarantined inputs changed during run")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO, text=True).strip()
    receipt = {"status": "POSTHOC_FLOAT64_DIAGNOSTIC_ONLY", "utc_finished": datetime.now(timezone.utc).isoformat(),
               "source_commit": head, "input_sha256_before_after": hashes,
               "script_sha256": digest(Path(__file__)), "rows": rows,
               "actual_QPU_calls": 0, "P48_inputs_opened": False,
               "partitions_exported": False, "optimum_used_for_training": False,
               "cpu_seconds_after_environment_guard": time.process_time()-cpu,
               "wall_seconds_after_environment_guard": time.perf_counter()-wall,
               "software": {"Python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__},
               "native_HiGHS_options_readback": {"threads": native_threads, "parallel": native_parallel},
               "non_claims": ["No exact/interval certificate", "No new encoder, guide, held-out evaluation or advantage",
                              "A gap to an estimated lower bound is not a proved distance from optimum",
                              "No partitions, masks or solver assignments exported"]}
    (output/"summary.json").write_text(json.dumps(receipt, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": receipt["status"], "cases": len(rows), "partitions_exported": False}))
    return int(any("EXCEPTION" in row["interpretation"] or "FAILURE" in row["interpretation"] for row in rows))


if __name__ == "__main__":
    raise SystemExit(main())
