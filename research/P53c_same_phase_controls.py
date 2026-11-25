"""Exact same-phase four-body falsification, fixed x=1/4, expanded106 MEANS.

No replacement benchmark graph is constructed. The saved P53b graph is fixed.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import gzip
import itertools
import json
from pathlib import Path
import time

import P53b_fixed_point_discriminator as previous

exact = previous.exact_provider
DEN4, DEN8 = 8**4, 8**8
XI_POWERS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))
PREVIOUS_SOURCE_SHA = "66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908"
CHECKPOINT_PATH = "experiments/P53b_fixed_point/run_001/data/certificate.json.gz"
CHECKPOINT_SHA = "bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe"


def frozen_spec():
    return {"x_numerator": 1, "x_denominator": 4, "theta_label": "pi/3",
            "old_vertices": 71, "new_vertices": 35, "all_vertices": 106,
            "maximum_LP_calls": 2, "LP_seconds_per_call": 1,
            "maximum_cpu_seconds": 20, "maximum_wall_seconds": 30,
            "maximum_threads": 1, "maximum_planned_arrays_bytes": 67108864,
            "maximum_new_output_bytes": 4194304, "positive_optimizer_accepted": False}


def validate_spec(spec):
    if spec != frozen_spec():
        raise ValueError("Frozen P53c point/library/limits changed")


def ring_mul(first, second):
    a, b = first; c, d = second
    return a*c-b*d, a*d+b*c+b*d


def conjugate(value):
    a, b = value
    return a+b, -b


def norm(value):
    a, b = value
    return a*a+a*b+b*b


def columns_at_pi3():
    columns = []
    for source in range(8):
        column = []
        for row in range(8):
            sign = exact.SIGNS[row % 4][source % 4] * (-1 if row >= 4 and source >= 4 else 1)
            a, b = XI_POWERS[row % 4 if source >= 4 else 0]
            column.append((sign*a, sign*b))
        columns.append(tuple(column))
    return tuple(columns)


def four_photon_law(group, counts=None):
    if (len(group) != 4 or len(set(group)) != 4
            or any(type(source) is not int or not 0 <= source < 8 for source in group)):
        raise ValueError("Four distinct input ports in range0..7 required")
    counts = tuple(exact.compositions(8, 4)) if counts is None else counts
    columns = columns_at_pi3()
    polynomial = {(0,)*8: (1, 0)}
    for source in group:
        updated = {}
        for n, coefficient in polynomial.items():
            for row, value in enumerate(columns[source]):
                changed = list(n); changed[row] += 1; changed = tuple(changed)
                a, b = updated.get(changed, (0, 0))
                c, d = ring_mul(coefficient, value)
                updated[changed] = a+c, b+d
        polynomial = updated
    coefficients = tuple(polynomial.get(n, (0, 0)) for n in counts)
    probabilities = tuple(exact.factorial_product(n)*norm(value) for n, value in zip(counts, coefficients))
    if min(probabilities) < 0 or sum(probabilities) != DEN4:
        raise ArithmeticError("Exact four-photon ring/Fock normalization failed")
    return coefficients, probabilities


def probability_convolution(first, second, mapping, outputs):
    if (sum(first) != DEN4 or sum(second) != DEN4 or min(first) < 0 or min(second) < 0
            or len(mapping) != len(first) or any(len(row) != len(second) for row in mapping)):
        raise ValueError("Normalized group laws and full convolution map required")
    values = [0]*outputs
    for i, a in enumerate(first):
        if a:
            for j, b in enumerate(second):
                if b:
                    values[mapping[i][j]] += a*b
    if min(values) < 0 or sum(values) != DEN8:
        raise ArithmeticError("Probability convolution mass failed")
    return tuple(values)


def same_phase_controls():
    counts4, counts8 = tuple(exact.compositions(8, 4)), tuple(exact.compositions(8, 8))
    index = {n: i for i, n in enumerate(counts8)}
    mapping = tuple(tuple(index[tuple(a+b for a, b in zip(n, m))] for m in counts4) for n in counts4)
    groups = tuple(itertools.combinations(range(8), 4))
    laws = {group: four_photon_law(group, counts4) for group in groups}
    ties = exact.tie_scaled_rows(counts8)
    labels, occupation, rank, crossing = [], [], [], []
    for first in groups:
        if 0 not in first:
            continue  # Species exchange is the same complementary grouping.
        second = tuple(i for i in range(8) if i not in first)
        values = probability_convolution(laws[first][1], laws[second][1], mapping, len(counts8))
        ranked, mean = exact._push_scalar(values, ties)
        labels.append({"kind": "b4", "theta": "pi/3", "groups": (first, second)})
        occupation.append(values); rank.append(ranked); crossing.append(mean)
    if len(labels) != 35 or len(groups) != 70 or len(counts4) != 330 or len(counts8) != 6435:
        raise ArithmeticError("Full same-phase control population missing")
    return {"labels": labels, "groups": groups, "counts4": counts4, "counts8": counts8,
            "group_coefficients_xi": [laws[group][0] for group in groups],
            "group_probability_numerators": [laws[group][1] for group in groups],
            "occupation_numerators": occupation, "rank_numerators": rank,
            "crossing_numerators": crossing, "group_denominator": DEN4,
            "occupation_denominator": DEN8, "kernel_denominator": previous.KERNEL_DEN}


def append_library(old_library, new_controls):
    integers = new_controls["crossing_numerators"]
    if len(old_library) != 71 or len(integers) != 35 or len(new_controls["labels"]) != 35:
        raise ValueError("All71 old and35 new controls must be retained")
    if any(len(row) != 28 or any(type(x) is not int for x in row) for row in integers):
        raise TypeError("New exact integer mean coordinates required")
    new = tuple(tuple(Q(x, previous.KERNEL_DEN) for x in row) for row in integers)
    if any(min(row) < 0 or max(row) > 1 or not previous.validate_incident(row) for row in new):
        raise ArithmeticError("New mean incident/physical identities failed")
    return tuple(old_library)+new


def read_checkpoint(path, expected_sha=CHECKPOINT_SHA):
    if previous.sha256(path) != expected_sha:
        raise ValueError("P53b checkpoint hash mismatch")
    with gzip.open(path, "rb") as stream:
        payload = stream.read(previous.MAX_INFLATED_INPUT+1)
    if len(payload) > previous.MAX_INFLATED_INPUT:
        raise ValueError("P53b checkpoint inflation bound exceeded")
    # Historical LP floats may be present, but proof fields are decoded below as canonical Q only.
    return json.loads(payload, parse_constant=previous._reject_noninteger_json)


def verify_checkpoint(checkpoint, old_library, target):
    vector = lambda row: tuple(previous.rational_pair(x) for x in row)
    if (vector(checkpoint["target_exact"]) != tuple(target)
            or tuple(vector(row) for row in checkpoint["library_exact"]) != tuple(old_library)):
        raise ArithmeticError("The original B point or endpoint controls changed")
    saved = checkpoint["dual_exact"]
    w = vector(saved["signed_weights"])
    graph = checkpoint["nonnegative_graph_witness"]
    normalized = vector(graph["weights_normalized_sum_one"])
    shift, scale = previous.rational_pair(graph["uniform_edge_shift"]), previous.rational_pair(graph["weight_sum"])
    old_gap = min(previous.dot(w, row)-previous.dot(w, target) for row in old_library)
    if (len(w) != 28 or len(normalized) != 28 or scale <= 0 or min(normalized) < 0
            or sum(normalized) != 1 or sum(map(abs, w)) > 1
            or old_gap <= 0 or old_gap != previous.rational_pair(saved["strict_margin"])
            or normalized != tuple((x+shift)/scale for x in w)):
        raise ArithmeticError("The saved fixed P53b dual/graph failed exact checks")
    return w, normalized, scale


def fixed_graph_diagnostic(w, normalized, scale, target, new_library):
    signed = tuple(previous.dot(w, row)-previous.dot(w, target) for row in new_library)
    graph = tuple(previous.dot(normalized, row)-previous.dot(normalized, target) for row in new_library)
    if graph != tuple(value/scale for value in signed):
        raise ArithmeticError("Old fixed graph and dual margins disagree")
    minimum = min(graph)
    return {"scope": "SAVED_P53B_GRAPH_UNCHANGED_ON35_NEW_CONTROLS_ONLY",
            "signed_margins": signed, "normalized_graph_margins": graph,
            "minimum_normalized_margin": minimum,
            "new_controls_strictly_better_than_fixed_B_on_old_graph": sum(value < 0 for value in graph),
            "status": "OLD_GRAPH_BEATEN_BY_NEW_CONTROL" if minimum < 0 else
                ("OLD_GRAPH_TIED_BY_NEW_CONTROL" if minimum == 0 else "OLD_GRAPH_STRICT_GAP_RETAINS35"),
            "not_membership_or_optimizer_conclusion": True}


def classify106(primal_exact, dual_exact, primal_gate, dual_gate):
    if primal_exact and dual_exact:
        return "INCONSISTENCY_EXACT_PRIMAL_DUAL_EXPANDED106"
    if primal_exact and primal_gate:
        return "EXACT_POINT_EXPANDED106_MEMBERSHIP_CERTIFIED"
    if dual_exact and dual_gate:
        return "EXACT_POINT_EXPANDED106_SEPARATION_CERTIFIED"
    return "INCONCLUSIVE_AT_FIXED_X_EXPANDED106"


def solve106(library, target):
    if len(library) != 106:
        raise ValueError("The full106 library is required")
    primal = previous.lp_provider.convex_fit([[float(x) for x in row] for row in library], [float(x) for x in target])
    candidate = primal.get("verification", {})
    primal_exact = (exact.exactify_support(library, target, candidate.get("used_coefficients", []))
                    if candidate.get("verified") else {"verified": False, "reason": "no_float_support"})
    dual = previous.dual_proposal(library, target)
    dual_exact = previous.verify_dual(library, target, dual.get("signed_float_coordinates"))
    pg, dg = previous.solver_gate(primal), previous.solver_gate(dual)
    return {"status": classify106(primal_exact["verified"], dual_exact["verified"], pg, dg),
            "scope": "ONE_SAME_PHYSICAL_POINT_EDGE_MEAN_FIXED_EXPANDED106_ONLY",
            "LP_provider_calls": 2, "native_LP_calls_upper_bound": 2,
            "primal_proposal": primal, "primal_exact": primal_exact, "primal_solver_gate": pg,
            "dual_proposal": dual, "dual_exact": dual_exact, "dual_solver_gate": dg,
            "new_dual_is_functional_not_replacement_benchmark_graph": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, type=Path); parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(); validate_spec(json.loads(args.spec.read_text()))
    if previous.sha256(previous.__file__) != PREVIOUS_SOURCE_SHA:
        raise ValueError("Immutable P53b helper changed")
    providers = previous.verify_providers(); root = Path(__file__).resolve().parents[1]
    started_cpu, started_wall = time.process_time(), time.perf_counter()
    source = previous.read_pinned_json(root/previous.SOURCE_PATH, previous.SOURCE_SHA)
    controls = previous.read_pinned_json(root/previous.LIBRARY_PATH, previous.LIBRARY_SHA)
    power, old_library, old_labels = previous.extract_proof_data(source, controls)
    del source, controls
    target = previous.fixed_target(power)
    checkpoint = read_checkpoint(root/CHECKPOINT_PATH)
    w, normalized, scale = verify_checkpoint(checkpoint, old_library, target)
    del checkpoint
    args.output.mkdir(parents=True, exist_ok=False)
    new_controls = same_phase_controls(); library = append_library(old_library, new_controls)
    diagnostic = fixed_graph_diagnostic(w, normalized, scale, target, library[71:])
    evidence = solve106(library, target)
    evidence.update({"x": previous.X_FIXED, "target_exact": target, "library_exact": library,
                     "library_labels": old_labels+new_controls["labels"], "new_controls_raw": new_controls,
                     "saved_P53b_signed_weights": w, "saved_P53b_graph_normalized": normalized,
                     "fixed_old_graph_diagnostic": diagnostic, "P53b_checkpoint_sha256": CHECKPOINT_SHA})
    previous.save_bounded_gzip(args.output/"certificate.json.gz", evidence, previous.MAX_OUTPUT-65536)
    summary = {"status": evidence["status"], "x_numerator": 1, "x_denominator": 4, "theta_label": "pi/3",
               "old_vertices": 71, "new_vertices": 35, "all_vertices": 106, "all70_group_laws_normalized_exact": True,
               "all35_convolutions_normalized_exact": True, "LP_provider_calls": 2,
               "primal_exact_witness": evidence["primal_exact"]["verified"],
               "dual_exact_witness": evidence["dual_exact"]["verified"],
               "primal_solver_gate": evidence["primal_solver_gate"], "dual_solver_gate": evidence["dual_solver_gate"],
               "fixed_old_graph_diagnostic": diagnostic, "source_sha256": previous.sha256(__file__),
               "spec_sha256": previous.sha256(args.spec), "provider_sha256": providers,
               "CPU_seconds_inside_main": time.process_time()-started_cpu,
               "wall_seconds_inside_main": time.perf_counter()-started_wall,
               "positive_optimizer_accepted": False, "independent_exact_review_required": True,
               "not_continuous_theta_full_law_classical_optimization_or_hardware_claim": True}
    text = json.dumps(exact.encoded(summary), indent=2, allow_nan=False)+"\n"
    if len(text.encode()) > 65536:
        raise RuntimeError("Summary output cap exceeded")
    (args.output/"summary.json").write_text(text)
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > previous.MAX_OUTPUT:
        raise RuntimeError("Scientific total output cap exceeded")
    print(json.dumps(exact.encoded(summary), allow_nan=False))
    if evidence["status"] == "INCONSISTENCY_EXACT_PRIMAL_DUAL_EXPANDED106":
        raise ArithmeticError("Inconsistent exact witnesses; neither accepted")


if __name__ == "__main__":
    main()
