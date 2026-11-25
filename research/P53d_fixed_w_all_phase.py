"""Exact fixed-witness scalar bounds for all b4 phases; never optimizer benefit."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
import P53c_same_phase_controls as phase3

base, exact = phase3.previous, phase3.exact
PHASE3_SOURCE_SHA = "737d6743f184661c4352d93c40410679bec5b5e739aa2cd964a63b919eaa53e2"
PHASE3_PATH = "experiments/P53c_same_phase/run_001/data/certificate.json.gz"
PHASE3_SHA = "408140f0a1a3865e374256d2a1e797961adcf6742cd8b1d234c2c7b4b2cbc065"
SCALAR_DEN = 840*8**8
L1_LIMIT = 4096
BILINEAR_LIMIT = 420*4096**2
FOLD_LIMIT = 13*BILINEAR_LIMIT


def frozen_spec():
    return {"B_theta": "pi/3", "x_numerator": 1, "x_denominator": 4,
            "w": "(X04-X15)/2", "groupings": 35, "maximum_harmonic": 12,
            "global_Bernstein_degree": 12, "interval_Bernstein_degree": 24,
            "interval_count": 8, "maximum_LP_calls": 0,
            "maximum_cpu_seconds": 20, "maximum_wall_seconds": 30,
            "maximum_threads": 1, "maximum_planned_arrays_bytes": 67108864,
            "maximum_new_output_bytes": 4194304, "positive_optimizer_accepted": False}


def validate_spec(spec):
    if spec != frozen_spec():
        raise ValueError("Frozen fixed-witness ladder/point/caps changed")


def guard_bank(bank):
    if not bank or not bank[0] or len(bank[0]) % 2 != 1 or len(bank[0]) > 25:
        raise ValueError("Nonempty odd Laurent bank of width<=25 required")
    width = len(bank[0])
    if any(len(row) != width or any(type(x) is not int for x in row) for row in bank):
        raise TypeError("Python integer rectangular bank required BEFORE dtype conversion")
    bounds = tuple(sum(abs(row[j]) for row in bank) for j in range(width))
    if any(value > L1_LIMIT for value in bounds):
        raise ValueError("Per-column L1 bound violated before int64 conversion")
    return bounds


def group_spectrum(group, counts):
    if len(group) != 4 or len(set(group)) != 4 or any(type(a) is not int or not 0 <= a < 8 for a in group):
        raise ValueError("Four distinct input ports required")
    degree = 3*sum(a >= 4 for a in group)
    polynomial = {((0,)*8, 0): 1}
    for source in group:
        updated = {}
        for (n, h), coefficient in polynomial.items():
            for row in range(8):
                sign = exact.SIGNS[row % 4][source % 4]*(-1 if row >= 4 and source >= 4 else 1)
                changed = list(n); changed[row] += 1
                key = (tuple(changed), h+(row % 4 if source >= 4 else 0))
                updated[key] = updated.get(key, 0)+sign*coefficient
        polynomial = {key: value for key, value in updated.items() if value != 0}
    coefficients, bank = [], []
    for n in counts:
        c = tuple(polynomial.get((n, j), 0) for j in range(degree+1))
        factorial = exact.factorial_product(n)
        if sum(map(abs, c)) > math.factorial(4)//factorial:
            raise ArithmeticError("Creation coefficient assignment bound failed")
        nonnegative = tuple(factorial*sum(c[j]*c[j+k] for j in range(degree+1-k)) for k in range(degree+1))
        coefficients.append(c)
        bank.append(tuple(nonnegative[abs(k)] for k in range(-degree, degree+1)))
    masses = tuple(sum(row[k] for row in bank) for k in range(2*degree+1))
    if masses != tuple(4096 if k == degree else 0 for k in range(2*degree+1)):
        raise ArithmeticError("Exact all-phase group normalization/Parseval failed")
    bounds = guard_bank(bank)
    return {"group": group, "phase_degree": degree, "creation_coefficients": coefficients,
            "probability_laurent_numerators": bank, "probability_denominator": 4096,
            "normalization_harmonic_sums": masses, "per_column_L1": bounds}


def make_tie_matrix(counts4):
    counts8 = tuple(exact.compositions(8, 8))
    scalar = []
    for ties in exact.tie_scaled_rows(counts8):
        value = sum(weight*(int(((mask >> 0) & 1) != ((mask >> 4) & 1))
                            - int(((mask >> 1) & 1) != ((mask >> 5) & 1))) for mask, weight in ties)
        if type(value) is not int or abs(value) > 420:
            raise ArithmeticError("Exact tie scalar bound failed")
        scalar.append(value)
    lookup = dict(zip(counts8, scalar))
    matrix = [[lookup[tuple(a+b for a, b in zip(n, m))] for m in counts4] for n in counts4]
    # Python-integer bound check precedes dtype conversion.
    if any(type(x) is not int or abs(x) > 420 for row in matrix for x in row):
        raise ValueError("Bounded Python tie integers required")
    integer_matrix = np.asarray(matrix, dtype=np.int64)
    if not np.array_equal(integer_matrix, integer_matrix.T):
        raise ArithmeticError("Convolution tie matrix is not symmetric")
    return counts8, scalar, integer_matrix


def contract_scalar(first, second, matrix):
    first_l1, second_l1 = guard_bank(first), guard_bank(second)
    if (not isinstance(matrix, np.ndarray) or matrix.dtype != np.dtype(np.int64)
            or matrix.shape != (len(first), len(second)) or len(first) != len(second)
            or int(matrix.min()) < -420 or int(matrix.max()) > 420
            or not np.array_equal(matrix, matrix.T)):
        raise TypeError("Symmetric bounded int64 matrix required; no floating contraction")
    a, b = np.asarray(first, dtype=np.int64), np.asarray(second, dtype=np.int64)
    swapped = b.shape[1] > a.shape[1]
    if swapped:
        a, b = b, a
    span = (a.shape[1]+b.shape[1]-2)//2
    if span > 12:
        raise ValueError("Frozen maximum harmonic exceeded")
    middle = matrix @ b
    bilinear = a.T @ middle
    if middle.dtype != np.dtype(np.int64) or bilinear.dtype != np.dtype(np.int64):
        raise TypeError("Integer matrix multiplication changed dtype")
    if any(abs(int(x)) > 420*4096 for x in middle.flat) or any(abs(int(x)) > BILINEAR_LIMIT for x in bilinear.flat):
        raise ArithmeticError("Proved int64 product bounds failed")
    laurent = [0]*25
    for i in range(bilinear.shape[0]):
        for j in range(bilinear.shape[1]):
            laurent[i+j-span+12] += int(bilinear[i, j])  # Python-int accumulation, <=13 pairs/harmonic.
    if any(abs(x) > FOLD_LIMIT for x in laurent) or any(laurent[12+k] != laurent[12-k] for k in range(13)):
        raise ArithmeticError("Scalar accumulation bound/evenness failed")
    cosine = (laurent[12],)+tuple(2*laurent[12+k] for k in range(1, 13))
    return {"laurent_numerators": laurent, "cosine_numerators": cosine,
            "denominator": SCALAR_DEN, "bilinear_numerators": bilinear.tolist(),
            "shorter_bank_multiplied_first": swapped,
            "first_column_L1": first_l1, "second_column_L1": second_l1,
            "all_integer_product_and_fold_bounds_passed": True}


def cosines_at(label):
    cycles = {"0": (Q(1),), "pi/2": (Q(1), Q(0), Q(-1), Q(0)),
              "pi/3": (Q(1), Q(1, 2), Q(-1, 2), Q(-1), Q(-1, 2), Q(1, 2))}
    cycle = cycles[label]
    return tuple(cycle[k % len(cycle)] for k in range(13))


def exact_anchors(cosine, expected):
    if len(cosine) != 13 or set(expected) != {"0", "pi/2", "pi/3"}:
        raise ValueError("All13 harmonics and all three exact anchors required")
    records = {}
    for label in ("0", "pi/2", "pi/3"):
        value = sum((exact.exact_q(c)*t for c, t in zip(cosine, cosines_at(label))), Q(0))
        if value != exact.exact_q(expected[label]):
            raise ArithmeticError("Scalar polynomial disagrees with exact archived phase anchor")
        records[label] = {"spectrum_value": value, "archived_value": expected[label], "equal": True}
    return records


def evaluate_power(power, x):
    x = exact.exact_q(x); result = Q(0)
    for coefficient in reversed(power):
        result = result*x+exact.exact_q(coefficient)
    return result


def affine_power(power, left, right):
    left, right = exact.exact_q(left), exact.exact_q(right)
    if right <= left:
        raise ValueError("Positive interval width required")
    return tuple(sum((exact.exact_q(power[k])*math.comb(k, j)*left**(k-j)*(right-left)**j
                      for k in range(j, len(power))), Q(0)) for j in range(len(power)))


def verify_bernstein(power, degree, left, right, controls):
    left, right = exact.exact_q(left), exact.exact_q(right)
    local = affine_power(power, left, right)
    reconstructed = exact.bernstein_to_power(controls)
    if len(controls) != degree+1 or reconstructed != local+(Q(0),)*(degree+1-len(local)):
        return False
    restored = affine_power(reconstructed, -left/(right-left), (1-left)/(right-left))
    return restored == tuple(map(exact.exact_q, power))+(Q(0),)*(degree+1-len(power))


def bernstein_record(power, degree, left, right):
    controls = exact.power_to_bernstein(affine_power(power, left, right), degree)
    if not verify_bernstein(power, degree, left, right, controls):
        raise ArithmeticError("Exact Bernstein affine/original power identity failed")
    return {"degree": degree, "x_interval": (left, right), "controls": controls,
            "minimum_control": min(controls), "power_reconstruction_exact": True}


def certify_scalar(cosine, fixed_B_mean):
    cosine = tuple(map(exact.exact_q, cosine)); fixed_B_mean = exact.exact_q(fixed_B_mean)
    if len(cosine) != 13:
        raise ValueError("All13 scalar harmonic coefficients required")
    power = list(exact.cosine_to_power(cosine)); power[0] -= fixed_B_mean; power = tuple(power)
    nodes = tuple(evaluate_power(power, Q(j, 8)) for j in range(9))
    triangle = cosine[0]-sum(map(abs, cosine[1:]), Q(0))-fixed_B_mean
    evidence = {"margin_power_in_x_where_cos_phi_eq_2x_minus1": power, "triangle_lower_bound": triangle,
                "registered_nodes_t": tuple(Q(-1)+Q(j, 4) for j in range(9)),
                "registered_node_values": nodes, "negative_node_indices": [j for j, x in enumerate(nodes) if x < 0],
                "zero_node_indices": [j for j, x in enumerate(nodes) if x == 0], "Bernstein_stages": []}
    if evidence["negative_node_indices"]:
        return {**evidence, "status": "EXACT_NEGATIVE_REGISTERED_ENDPOINT", "lower_bound": None, "nonnegative_proven": False}
    if triangle >= 0:
        return {**evidence, "status": "STRICT_UNIFORM_GAP" if triangle > 0 else "NONNEGATIVE_WITHOUT_STRICT_BOUND",
                "lower_bound": triangle, "nonnegative_proven": True, "certificate_stage": "triangle"}
    global_record = bernstein_record(power, 12, Q(0), Q(1)); evidence["Bernstein_stages"].append(global_record)
    if global_record["minimum_control"] >= 0:
        bound = global_record["minimum_control"]
        return {**evidence, "status": "STRICT_UNIFORM_GAP" if bound > 0 else "NONNEGATIVE_WITHOUT_STRICT_BOUND",
                "lower_bound": bound, "nonnegative_proven": True, "certificate_stage": "Bernstein12_global"}
    records = [bernstein_record(power, 24, Q(j, 8), Q(j+1, 8)) for j in range(8)]
    evidence["Bernstein_stages"].extend(records); bound = min(row["minimum_control"] for row in records)
    if bound >= 0:
        return {**evidence, "status": "STRICT_UNIFORM_GAP" if bound > 0 else "NONNEGATIVE_WITHOUT_STRICT_BOUND",
                "lower_bound": bound, "nonnegative_proven": True, "certificate_stage": "Bernstein24_fixed8"}
    return {**evidence, "status": "EXACT_ZERO_REGISTERED_ENDPOINT" if evidence["zero_node_indices"] else "INCONCLUSIVE",
            "lower_bound": None, "nonnegative_proven": False}


def aggregate(decisions, uniform_gap, old_scale):
    if any(row["status"] == "EXACT_NEGATIVE_REGISTERED_ENDPOINT" for row in decisions):
        return {"status": "FIXED_W_FALSIFIED_BY_REGISTERED_B4_PHASE", "uniform_lower_bound": None}
    if all(row["nonnegative_proven"] for row in decisions) and uniform_gap >= 0:
        bound = min([uniform_gap]+[row["lower_bound"] for row in decisions])
        return {"status": "STRICT_UNIFORM_FIXED_W_B4_PHASE_GAP" if bound > 0 else
                "NONNEGATIVE_FIXED_W_B4_PHASE_GAP_WITHOUT_STRICT_BOUND", "uniform_lower_bound": bound,
                "same_old_normalized_graph_lower_bound": bound/old_scale}
    return {"status": "STRICTNESS_FALSIFIED_BY_REGISTERED_ZERO_OTHER_PHASES_UNRESOLVED" if
            any(row["zero_node_indices"] for row in decisions) else "INCONCLUSIVE_FIXED_W_B4_PHASE",
            "uniform_lower_bound": None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); validate_spec(json.loads(args.spec.read_text()))
    if base.sha256(phase3.__file__) != PHASE3_SOURCE_SHA or base.sha256(base.__file__) != phase3.PREVIOUS_SOURCE_SHA:
        raise ValueError("Immutable phase3/fixed-point helper changed")
    providers = base.verify_providers(); root = Path(__file__).resolve().parents[1]
    started_cpu, started_wall = time.process_time(), time.perf_counter()
    source = base.read_pinned_json(root/base.SOURCE_PATH, base.SOURCE_SHA)
    old = base.read_pinned_json(root/base.LIBRARY_PATH, base.LIBRARY_SHA)
    power, old_library, old_labels = base.extract_proof_data(source, old); del source, old
    target = base.fixed_target(power)
    checkpoint = phase3.read_checkpoint(root/phase3.CHECKPOINT_PATH)
    w, old_graph, old_scale = phase3.verify_checkpoint(checkpoint, old_library, target); del checkpoint
    expected_w = tuple(Q(1, 2) if edge == (0, 4) else Q(-1, 2) if edge == (1, 5) else Q(0) for edge in base.EDGES)
    if w != expected_w:
        raise ArithmeticError("The saved witness is not the preregistered X04-X15 functional")
    phi3 = phase3.read_checkpoint(root/PHASE3_PATH, expected_sha=PHASE3_SHA)
    decode = lambda row: tuple(base.rational_pair(x) for x in row)
    if decode(phi3["target_exact"]) != target or decode(phi3["saved_P53b_signed_weights"]) != w:
        raise ArithmeticError("The archived physical B point/w changed")
    new = phi3["new_controls_raw"]; combined = phase3.append_library(old_library, new)
    if tuple(decode(row) for row in phi3["library_exact"]) != combined:
        raise ArithmeticError("The exact archived expanded library changed")
    new_labels = new["labels"]; del new, phi3
    args.output.mkdir(parents=True, exist_ok=False)
    counts4 = tuple(exact.compositions(8, 4)); groups = tuple(itertools.combinations(range(8), 4))
    spectra = {group: group_spectrum(group, counts4) for group in groups}
    counts8, tie_scalar, matrix = make_tie_matrix(counts4)
    B_mean = base.dot(w, target); records = []
    for first in groups:
        if 0 not in first:
            continue
        second = tuple(i for i in range(8) if i not in first); j = len(records)
        label = {"kind": "b4", "theta": "pi/3", "groups": [list(first), list(second)]}
        if new_labels[j] != label or old_labels[j]["groups"] != label["groups"] or old_labels[j+35]["groups"] != label["groups"]:
            raise ArithmeticError("Anchor grouping order changed")
        contraction = contract_scalar(spectra[first]["probability_laurent_numerators"],
                                      spectra[second]["probability_laurent_numerators"], matrix)
        cosine = tuple(Q(x, SCALAR_DEN) for x in contraction["cosine_numerators"])
        anchors = exact_anchors(cosine, {"0": base.dot(w, old_library[j]), "pi/2": base.dot(w, old_library[j+35]),
                                         "pi/3": base.dot(w, combined[j+71])})
        records.append({"groups": (first, second), "contraction": contraction, "cosine_coefficients": cosine,
                        "exact_phase_anchors": anchors, "decision": certify_scalar(cosine, B_mean)})
    if len(records) != 35 or len(spectra) != 70:
        raise ArithmeticError("Full control population missing")
    decisions = [row["decision"] for row in records]
    outcome = aggregate(decisions, base.dot(w, old_library[-1])-B_mean, old_scale)
    evidence = {"scope": "FIXED_N8_B_PI3_SAVED_W_GRAPH_ALL35_B4_GROUPS_ALL_REAL_PHI_ONLY",
                "outcome": outcome, "fixed_B_mean": B_mean, "saved_w": w, "same_old_graph_normalized": old_graph,
                "counts4": counts4, "counts8": counts8, "tie_scalar_numerators_over840": tie_scalar,
                "M": matrix.tolist(), "groups": groups, "group_spectra": list(spectra.values()), "all35_records": records,
                "anchors": "EXACT archived0/pi2/pi3, not new physical replication", "LP_calls": 0,
                "control_family": "b4(4+4) only, same architecture, every real phase",
                "untested_species_bipartitions": ["7+1", "6+2", "5+3"],
                "not_all_classical_models_or_genuine_order8_witness": True}
    base.save_bounded_gzip(args.output/"certificate.json.gz", evidence, base.MAX_OUTPUT-65536)
    summary = {**outcome, "groupings": 35, "group_spectra": 70, "exact_anchors": 105,
               "decision_statuses": [row["status"] for row in decisions], "LP_calls": 0,
               "CPU_seconds_inside_main": time.process_time()-started_cpu, "wall_seconds_inside_main": time.perf_counter()-started_wall,
               "source_sha256": base.sha256(__file__), "spec_sha256": base.sha256(args.spec), "provider_sha256": providers,
               "positive_optimizer_accepted": False, "independent_exact_review_required": True,
               "not_optimizer_full_law_other_architecture_hardware_or_phase_optimum": True,
               "control_family": "b4(4+4) only, same architecture, every real phase",
               "untested_species_bipartitions": ["7+1", "6+2", "5+3"],
               "not_all_classical_models_or_genuine_order8_witness": True}
    text = json.dumps(exact.encoded(summary), indent=2, allow_nan=False)+"\n"
    if len(text.encode()) > 65536:
        raise RuntimeError("Summary cap exceeded")
    (args.output/"summary.json").write_text(text)
    if sum(path.stat().st_size for path in args.output.rglob("*") if path.is_file()) > base.MAX_OUTPUT:
        raise RuntimeError("Scientific output cap exceeded")
    print(json.dumps(exact.encoded(summary), allow_nan=False))


if __name__ == "__main__":
    main()
