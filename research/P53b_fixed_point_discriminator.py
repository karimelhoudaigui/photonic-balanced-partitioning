"""One exact rational point versus the fixed ENDPOINT71 mean library.

LPs propose supports/vectors only. No source/kernel is rounded into proof data.
Any separating graph is a POSTHOC witness, never an optimizer benchmark.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import time
import warnings

import numpy as np
from scipy.optimize import linprog, OptimizeWarning

import P53_exact_continuous_phase as exact_provider

lp_provider = exact_provider.lp_provider
X_FIXED = Q(1, 4)
EDGES = tuple(itertools.combinations(range(8), 2))
KERNEL_DEN = 420 * 8**8
SOURCE_PATH = "experiments/P53_exact_phase/run_001/data/exact_source.json.gz"
LIBRARY_PATH = "experiments/P53_exact_phase/run_001/data/exact_library.json.gz"
SOURCE_SHA = "2a593abba088327ccb8b54f5f14bab6f8edcf5fc42128de6c31f394bf454d7a0"
LIBRARY_SHA = "cb210de13928e365b8983c2a17b882623a346975b522293fd549b6980871963b"
EXACT_PROVIDER_SHA = "aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692"
LP_PROVIDER_SHA = "56a71f048973cae7d4922d9da7d3952943c52f5a11597fc46bbb1a2bab84d242"
MAX_INFLATED_INPUT = 16 * 1024**2
MAX_OUTPUT = 4 * 1024**2
LP_OPTIONS = {"time_limit": 1., "threads": 1, "parallel": False,
              "random_seed": 5201001, "presolve": True,
              "dual_feasibility_tolerance": 1e-9,
              "primal_feasibility_tolerance": 1e-9}


def frozen_spec():
    return {"x_numerator": 1, "x_denominator": 4, "theta_label": "pi/3",
            "library": "ENDPOINT71", "maximum_LP_calls": 2,
            "LP_seconds_per_call": 1, "maximum_cpu_seconds": 20,
            "maximum_wall_seconds": 30, "maximum_threads": 1,
            "maximum_planned_arrays_bytes": 67108864,
            "maximum_new_output_bytes": MAX_OUTPUT,
            "dual_rationalization": "Fraction.from_float signed-coordinate binary exact; rescale L1 only if >1",
            "positive_optimizer_accepted": False}


def validate_spec(value):
    if value != frozen_spec():
        raise ValueError("Frozen P53b point, library, caps or witness rule changed")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024**2), b""):
            digest.update(block)
    return digest.hexdigest()


def _reject_noninteger_json(value):
    raise TypeError("Proof JSON must not contain floating or nonfinite numbers")


def read_pinned_json(path, expected_sha):
    if sha256(path) != expected_sha:
        raise ValueError("Pinned exact P53 artifact hash mismatch")
    with gzip.open(path, "rb") as stream:
        payload = stream.read(MAX_INFLATED_INPUT + 1)
    if len(payload) > MAX_INFLATED_INPUT:
        raise ValueError("Inflated exact input exceeds frozen bound")
    return json.loads(payload, parse_float=_reject_noninteger_json,
                      parse_constant=_reject_noninteger_json)


def rational_pair(value):
    if (not isinstance(value, dict) or set(value) != {"numerator", "denominator"}
            or type(value["numerator"]) is not int or type(value["denominator"]) is not int
            or value["denominator"] <= 0
            or math.gcd(value["numerator"], value["denominator"]) != 1):
        raise TypeError("Canonical integer numerator/positive-denominator pair required")
    return Q(value["numerator"], value["denominator"])


def validate_incident(vector, total=Q(16)):
    return (len(vector) == 28 and sum(vector, Q(0)) == total
            and all(sum((vector[e] for e, edge in enumerate(EDGES) if i in edge), Q(0)) == total / 4
                    for i in range(8)))


def extract_proof_data(source, controls):
    if source.get("kernel_denominator") != KERNEL_DEN or controls.get("denominator") != KERNEL_DEN:
        raise ValueError("Exact denominator convention changed")
    rows = source.get("crossing_power", [])
    if len(rows) != 28 or any(len(row) != 7 for row in rows):
        raise ValueError("Expected every degree-six crossing polynomial")
    power = tuple(tuple(rational_pair(value) for value in row) for row in rows)
    for h in range(7):
        if not validate_incident(tuple(row[h] for row in power), Q(16) if h == 0 else Q(0)):
            raise ArithmeticError("Exact source incident polynomial identity failed")
    expected_labels = []
    for endpoint in ("0", "pi/2"):
        for other in itertools.combinations(range(1, 8), 3):
            first = (0,) + other
            second = tuple(i for i in range(8) if i not in first)
            expected_labels.append({"kind": "b4", "theta": endpoint, "groups": [list(first), list(second)]})
    expected_labels.append({"kind": "uniform70"})
    if controls.get("labels") != expected_labels:
        raise ValueError("All 35 groupings at both fixed endpoints plus uniform are required")
    integers = controls.get("crossing_numerators", [])
    if len(integers) != 71 or any(len(row) != 28 for row in integers):
        raise ValueError("The full ENDPOINT71 library is required")
    if any(type(value) is not int or not 0 <= value <= KERNEL_DEN for row in integers for value in row):
        raise TypeError("Physical library numerators must be bounded integers")
    library = tuple(tuple(Q(value, KERNEL_DEN) for value in row) for row in integers)
    if any(not validate_incident(row) for row in library) or library[-1] != (Q(4, 7),) * 28:
        raise ArithmeticError("Library incident/total/uniform identities failed")
    return power, library, expected_labels


def fixed_target(power):
    """Only x=1/4 exists in this interface; no graph or phase search."""
    result = []
    for row in power:
        value = Q(0)
        for coefficient in reversed(row):
            value = value * X_FIXED + exact_provider.exact_q(coefficient)
        result.append(value)
    target = tuple(result)
    if any(value < 0 or value > 1 for value in target) or not validate_incident(target):
        raise ArithmeticError("Fixed-point physical mean identities failed")
    return target


def dual_proposal(library, target):
    """min w.b-t, t<=w.v_c, ||w||1<=1; one bounded support proposer."""
    started_cpu, started_wall = time.process_time(), time.perf_counter()
    try:
        native = lp_provider.native_single_thread_check()
        vertices, target_float = np.asarray(library, dtype=float), np.asarray(target, dtype=float)
        if vertices.shape != (len(library), 28) or target_float.shape != (28,):
            raise ValueError("Dual shape mismatch")
        objective = np.r_[target_float, -target_float, -1.]
        matrix = np.vstack((np.column_stack((-vertices, vertices, np.ones(len(vertices)))),
                            np.r_[np.ones(56), 0.][None, :]))
        bound = np.r_[np.zeros(len(vertices)), 1.]
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter("always", OptimizeWarning)
            result = linprog(objective, A_ub=matrix, b_ub=bound,
                             bounds=[(0., None)] * 56 + [(None, None)],
                             method="highs-ds", options=dict(LP_OPTIONS))
        invalid = [warning for warning in seen if not (
            issubclass(warning.category, OptimizeWarning)
            and str(warning.message).startswith("Unrecognized options detected: ")
            and str(warning.message).endswith("These will be passed to HiGHS verbatim."))]
        if invalid:
            raise RuntimeError("Invalid/ignored HiGHS option: " + " | ".join(str(w.message) for w in invalid))
        raw = None if result.x is None else np.asarray(result.x, dtype=float)
        available = bool(raw is not None and raw.shape == (57,) and np.isfinite(raw).all())
        signed = None if not available else [float(raw[i]) - float(raw[28+i]) for i in range(28)]
        if signed is not None and not all(math.isfinite(x) for x in signed):
            available, signed = False, None
        solved = int(result.status) == 0 and bool(result.success)
        return {"status": "DUAL_NUMERICAL_PROPOSAL" if solved else
                ("INCONCLUSIVE_SOLVER_LIMIT" if int(result.status) == 1 else "INCONCLUSIVE_SOLVER_FAILURE"),
                "solver_status": int(result.status), "solver_success": bool(result.success),
                "solver_fit_solved": solved, "solver_message": str(result.message),
                "solver_objective": None if result.fun is None else float(result.fun),
                "raw_split_vector": None if raw is None else [float(x) if np.isfinite(x) else str(x) for x in raw],
                "signed_float_coordinates": signed, "candidate_available": available,
                "options": dict(LP_OPTIONS), "native_options_readback": native,
                "warnings": [str(w.message) for w in seen],
                "CPU_seconds": time.process_time() - started_cpu,
                "wall_seconds": time.perf_counter() - started_wall}
    except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as error:
        return {"status": "INCONCLUSIVE_SOLVER", "error": repr(error),
                "solver_fit_solved": False, "candidate_available": False,
                "options": dict(LP_OPTIONS), "CPU_seconds": time.process_time() - started_cpu,
                "wall_seconds": time.perf_counter() - started_wall}


def dot(first, second):
    if len(first) != len(second):
        raise ValueError("Exact dot product dimensions differ")
    return sum((exact_provider.exact_q(a) * exact_provider.exact_q(b) for a, b in zip(first, second)), Q(0))


def verify_dual(library, target, proposed_w):
    if len(target) != 28 or not library or any(len(row) != 28 for row in library):
        raise ValueError("Exact dual inputs must contain complete 28-coordinate kernels")
    if (not isinstance(proposed_w, (list, tuple)) or len(proposed_w) != 28
            or not all(isinstance(x, (float, int)) and math.isfinite(x) for x in proposed_w)):
        return {"verified": False, "reason": "invalid_finite_signed_coordinate_proposal"}
    binary = tuple(Q.from_float(float(value)) for value in proposed_w)
    norm = sum(map(abs, binary), Q(0))
    divisor = max(Q(1), norm)
    weights = tuple(value / divisor for value in binary)
    products = tuple(dot(weights, vertex) for vertex in library)
    level, target_value = min(products), dot(weights, target)
    margins = tuple(value - target_value for value in products)
    gap = level - target_value
    verified = bool(sum(map(abs, weights), Q(0)) <= 1 and gap > 0 and all(value > 0 for value in margins))
    return {"verified": verified, "binary_signed_coordinates": binary,
            "binary_L1": norm, "exact_rescaling_divisor": divisor,
            "signed_weights": weights, "exact_L1": sum(map(abs, weights), Q(0)),
            "level": level, "target_mean": target_value, "strict_margin": gap,
            "all_vertex_margins": margins, "all_strict_inequalities": all(value > 0 for value in margins),
            "reason": "exact_strict_separation" if verified else "no_exact_strict_separation"}


def nonnegative_graph(dual, library, target):
    if not dual.get("verified"):
        raise ValueError("A strict rational separator is required")
    if sum(target, Q(0)) != 16 or any(sum(vertex, Q(0)) != 16 for vertex in library):
        raise ArithmeticError("The common balanced crossing total is required for shifting")
    weights = tuple(dual["signed_weights"])
    shift = max(Q(0), -min(weights))
    nonnegative = tuple(value + shift for value in weights)
    normalization = sum(nonnegative, Q(0))
    if min(nonnegative) < 0 or normalization <= 0:
        raise ArithmeticError("A strict separator must yield a nonzero nonnegative graph")
    normalized = tuple(value / normalization for value in nonnegative)
    graph_margins = tuple(dot(nonnegative, vertex) - dot(nonnegative, target) for vertex in library)
    if (min(graph_margins) != dual["strict_margin"] or any(value <= 0 for value in graph_margins)
            or min(dot(normalized, vertex) - dot(normalized, target) for vertex in library)
            != dual["strict_margin"] / normalization):
        raise ArithmeticError("Exact graph shift/normalization did not preserve the gap")
    return {"label": "POSTHOC_ADVERSARIAL_GRAPH_WITNESS_ENDPOINT71_ONLY",
            "edges_lexicographic": EDGES, "uniform_edge_shift": shift,
            "weights_nonnegative": nonnegative, "weight_sum": normalization,
            "weights_normalized_sum_one": normalized,
            "strict_mean_gap": dual["strict_margin"],
            "normalized_strict_mean_gap": dual["strict_margin"] / normalization,
            "all_graph_margins": graph_margins,
            "not_DEV_heldout_or_fully_reoptimized_b4": True}


def solver_gate(proposal):
    return bool(proposal.get("solver_fit_solved") and proposal.get("solver_status") == 0
                and proposal.get("solver_success") is True)


def classify(primal_exact, dual_exact, primal_gate, dual_gate):
    if primal_exact and dual_exact:
        return "INCONSISTENCY_EXACT_PRIMAL_AND_DUAL"
    if primal_exact and primal_gate:
        return "EXACT_POINT_MEMBERSHIP_CERTIFIED"
    if dual_exact and dual_gate:
        return "EXACT_POINT_ENDPOINT71_SEPARATION_CERTIFIED"
    return "INCONCLUSIVE_AT_FIXED_X"


def discriminate(library, target):
    """Exactly two provider calls, even if the first proposes membership."""
    primal = lp_provider.convex_fit([[float(x) for x in row] for row in library], [float(x) for x in target])
    proposal = primal.get("verification", {})
    primal_exact = (exact_provider.exactify_support(library, target, proposal.get("used_coefficients", []))
                    if proposal.get("verified") else {"verified": False, "reason": "no_float_support"})
    dual = dual_proposal(library, target)
    dual_exact = verify_dual(library, target, dual.get("signed_float_coordinates"))
    primal_gate, dual_gate = solver_gate(primal), solver_gate(dual)
    status = classify(primal_exact["verified"], dual_exact["verified"], primal_gate, dual_gate)
    return {"status": status, "LP_provider_calls": 2, "native_LP_calls_upper_bound": 2, "x": X_FIXED,
            "primal_proposal": primal, "primal_exact": primal_exact,
            "primal_solver_gate": primal_gate, "dual_proposal": dual,
            "dual_exact": dual_exact, "dual_solver_gate": dual_gate,
            "nonnegative_graph_witness": nonnegative_graph(dual_exact, library, target)
                if dual_exact["verified"] else None,
            "exact_witness_retained_even_if_solver_gate_inconclusive": True}


def verify_providers():
    actual = {"exact_provider": sha256(exact_provider.__file__), "LP_provider": sha256(lp_provider.__file__)}
    if actual != {"exact_provider": EXACT_PROVIDER_SHA, "LP_provider": LP_PROVIDER_SHA}:
        raise ValueError("Immutable qualified provider source changed")
    return actual


def save_bounded_gzip(path, payload, maximum_bytes=MAX_OUTPUT):
    encoded = (json.dumps(exact_provider.encoded(payload), separators=(",", ":"), allow_nan=False) + "\n").encode()
    if len(encoded) > maximum_bytes:
        raise RuntimeError("Uncompressed scientific output exceeds frozen cap")
    with Path(path).open("xb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0, compresslevel=3) as stream:
        stream.write(encoded)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    validate_spec(json.loads(args.spec.read_text()))
    providers = verify_providers()
    root = Path(__file__).resolve().parents[1]
    source = read_pinned_json(root / SOURCE_PATH, SOURCE_SHA)
    controls = read_pinned_json(root / LIBRARY_PATH, LIBRARY_SHA)
    power, library, labels = extract_proof_data(source, controls)
    del source, controls
    args.output.mkdir(parents=True, exist_ok=False)
    started_cpu, started_wall = time.process_time(), time.perf_counter()
    target = fixed_target(power)
    evidence = discriminate(library, target)
    evidence.update({"scope": "ONE x=1/4, fixed N8 fullCF uniform-top4 EDGE-MEAN ENDPOINT71 only",
                     "target_exact": target, "library_labels": labels, "library_exact": library,
                     "source_artifact": {"path": SOURCE_PATH, "sha256": SOURCE_SHA},
                     "library_artifact": {"path": LIBRARY_PATH, "sha256": LIBRARY_SHA}})
    save_bounded_gzip(args.output / "certificate.json.gz", evidence, MAX_OUTPUT - 65536)
    summary = {"status": evidence["status"], "x_numerator": 1, "x_denominator": 4,
               "theta_label": "pi/3", "LP_provider_calls": evidence["LP_provider_calls"],
               "native_LP_calls_upper_bound": 2, "library_vertices": 71,
               "source_and_library_hashes_verified": True, "all_exact_incident_identities_verified": True,
               "primal_exact_witness": bool(evidence["primal_exact"]["verified"]),
               "dual_exact_witness": bool(evidence["dual_exact"]["verified"]),
               "primal_solver_gate": evidence["primal_solver_gate"], "dual_solver_gate": evidence["dual_solver_gate"],
               "CPU_seconds_point_and_LPs": time.process_time() - started_cpu,
               "wall_seconds_point_and_LPs": time.perf_counter() - started_wall,
               "source_sha256": sha256(__file__), "spec_sha256": sha256(args.spec),
               "immutable_provider_sha256": providers,
               "positive_optimizer_accepted": False, "independent_exact_review_required": True,
               "not_continuous_curve_full_law_reoptimized_b4_or_hardware_claim": True,
               "no_physical_MC_sample_graph_search_or_Cstar": True}
    text = json.dumps(summary, indent=2, allow_nan=False) + "\n"
    if len(text.encode()) > 65536:
        raise RuntimeError("Summary cap exceeded")
    (args.output / "summary.json").write_text(text)
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > MAX_OUTPUT:
        raise RuntimeError("Frozen total scientific output cap exceeded")
    print(json.dumps(summary, allow_nan=False))
    if evidence["status"] == "INCONSISTENCY_EXACT_PRIMAL_AND_DUAL":
        raise ArithmeticError("Contradictory exact witnesses; neither result accepted")


if __name__ == "__main__":
    main()
