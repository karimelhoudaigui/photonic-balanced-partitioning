"""Posthoc NONBLIND exact replay of the TRIANGLE-only P53d4+4 candidate.

No production imports, creation DP, LP, RNG or phase optimization. Creation
coefficients come from24 permanent monomials divided by output factorials;
the decoder comes from direct enumeration of all70 balanced subsets.
"""
from fractions import Fraction as Q
import argparse
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np

PINS = {
    "experiments/P53d_all_b4_phases/run_001/data/certificate.json.gz": "44df171ef03e6886900cbf105c555cb2e5de0a2a4944d47b3065b23d1e57cc6b",
    "experiments/P53d_all_b4_phases/run_001/manifest.json": "91923621989bfbb90a586a51968d20248c3366c1863fa8dc90a0b9d897ee5030",
    "experiments/P53_exact_phase/run_001/data/exact_source.json.gz": "2a593abba088327ccb8b54f5f14bab6f8edcf5fc42128de6c31f394bf454d7a0",
    "experiments/P53_exact_phase/run_001/data/exact_library.json.gz": "cb210de13928e365b8983c2a17b882623a346975b522293fd549b6980871963b",
    "experiments/P53b_fixed_point/run_001/data/certificate.json.gz": "bd9874399ffed241b045f09a5a4f155d7d60263e7314a55e1bfd2358c9022dbe",
    "experiments/P53c_same_phase/run_001/data/certificate.json.gz": "408140f0a1a3865e374256d2a1e797961adcf6742cd8b1d234c2c7b4b2cbc065",
    "research/P53d_fixed_w_all_phase.py": "67789e2a2fee0549f94ab948476a6d27190fb3ef0a2a2ab66cd88709178402b5",
    "research/P53_exact_continuous_phase.py": "aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692",
    "research/P53b_fixed_point_discriminator.py": "66ed6abdb1005c961d9bb54fe70008241ef37fe56d8d548e48173d5e9c01c908",
    "research/P53c_same_phase_controls.py": "737d6743f184661c4352d93c40410679bec5b5e739aa2cd964a63b919eaa53e2"}
SOURCE = "experiments/P53_exact_phase/run_001/data/exact_source.json.gz"
LIBRARY = "experiments/P53_exact_phase/run_001/data/exact_library.json.gz"
CHECKPOINT = "experiments/P53b_fixed_point/run_001/data/certificate.json.gz"
ANCHORS = "experiments/P53c_same_phase/run_001/data/certificate.json.gz"
CANDIDATE = "experiments/P53d_all_b4_phases/run_001/data/certificate.json.gz"
REFERENCE_MANIFEST = "experiments/P53d_all_b4_phases/run_001/manifest.json"
KERNEL_DEN, SCALAR_DEN = 420*8**8, 840*8**8


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def q(value):
    if type(value) is int:
        return Q(value)
    require(isinstance(value, dict) and set(value) == {"numerator", "denominator"}, "Canonical rational pair required")
    n, d = value["numerator"], value["denominator"]
    require(type(n) is int and type(d) is int and d > 0 and math.gcd(n, d) == 1, "Noncanonical/noninteger proof rational")
    return Q(n, d)


def integers(row, length=None):
    require(isinstance(row, (list, tuple)) and all(type(x) is int for x in row), "Python integers required")
    require(length is None or len(row) == length, "Integer vector length changed")
    return tuple(row)


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024**2), b""):
            digest.update(block)
    return digest.hexdigest()


def reject_float(text):
    raise TypeError("Floating proof data forbidden: " + text)


def read_json(path, maximum=16*1024**2, historical=False):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rb") as stream:
        payload = stream.read(maximum+1)
    require(len(payload) <= maximum, "Input inflation cap exceeded")
    # Ignored historical LP decimals remain opaque strings, never float proof values.
    parser = (lambda text: "UNUSED_HISTORICAL_DECIMAL:"+text) if historical else reject_float
    return json.loads(payload, parse_float=parser, parse_constant=reject_float)


def occupations(photons):
    """Independent multiset-of-output-slots enumeration, not composition DP."""
    for slots in itertools.combinations_with_replacement(range(8), photons):
        n = [0]*8
        for mode in slots:
            n[mode] += 1
        yield tuple(n)


def permanent_polynomial(n, group):
    n, group = integers(n, 8), integers(group, 4)
    require(min(n) >= 0 and sum(n) == 4 and len(set(group)) == 4 and min(group) >= 0 and max(group) < 8,
            "Four distinct input photons/nonnegative output multiplicities required")
    rows = tuple(mode for mode, count in enumerate(n) for _ in range(count))
    degree = 3*sum(source >= 4 for source in group)
    raw = [0]*(degree+1)
    for assigned in itertools.permutations(group):
        parity, exponent = 0, 0
        for row, source in zip(rows, assigned):
            parity += ((row >> 1) & 1)*(source & 1) + (row & 1)*((source >> 1) & 1) + (row >> 2)*(source >> 2)
            exponent += (row & 3)*(source >> 2)
        raw[exponent] += -1 if parity % 2 else 1
    factorial = math.prod(math.factorial(count) for count in n)
    require(all(value % factorial == 0 for value in raw), "Permanent not divisible by output multiplicity factorial")
    return tuple(value//factorial for value in raw)


def laurent_probability(c, n):
    factorial = math.prod(math.factorial(count) for count in n)
    degree = len(c)-1
    # Direct pairs of permanent monomials, rather than creation recurrence.
    out = [0]*(2*degree+1)
    for i, first in enumerate(c):
        for j, second in enumerate(c):
            out[i-j+degree] += factorial*first*second
    return tuple(out)


def column_bounds(bank):
    require(bool(bank) and bool(bank[0]), "Empty bank")
    width = len(bank[0])
    require(width <= 25 and width % 2 == 1, "Odd width<=25 required")
    rows = tuple(integers(row, width) for row in bank)
    bounds = tuple(sum(abs(row[j]) for row in rows) for j in range(width))
    require(max(bounds) <= 4096, "Column L1 exceeds4096 BEFORE conversion")
    return bounds


def direct_tie_scalar(n):
    n = integers(n, 8)
    require(min(n) >= 0 and sum(n) == 8, "Eight-photon integer occupation required")
    subsets = tuple(itertools.combinations(range(8), 4))
    scores = [sum(n[i] for i in subset) for subset in subsets]
    maximum = max(scores)
    winners = [subset for subset, value in zip(subsets, scores) if value == maximum]
    difference = sum(int((0 in s) != (4 in s)) - int((1 in s) != (5 in s)) for s in winners)
    numerator, remainder = divmod(420*difference, len(winners))
    require(remainder == 0 and abs(numerator) <= 420, "Exact uniform max-count scalar failed")
    return numerator


def two_einsum_spectrum(first, second, matrix):
    column_bounds(first); column_bounds(second)
    require(isinstance(matrix, np.ndarray) and matrix.dtype == np.dtype(np.int64)
            and matrix.shape == (len(first), len(second)) and len(first) == len(second)
            and np.array_equal(matrix, matrix.T) and all(abs(int(x)) <= 420 for x in matrix.flat), "Bounded symmetric int64 M required")
    a, b = np.asarray(first, dtype=np.int64), np.asarray(second, dtype=np.int64)
    if a.shape[1] < b.shape[1]:
        a, b = b, a
    span = (a.shape[1]+b.shape[1]-2)//2
    require(span <= 12, "Harmonic range changed")
    # TWO explicit contractions: no3-operand565M-term einsum and no @ kernel.
    middle = np.einsum("uv,vb->ub", matrix, b, dtype=np.int64, casting="no", optimize=False)
    pair = np.einsum("ua,ub->ab", a, middle, dtype=np.int64, casting="no", optimize=False)
    require(middle.dtype == pair.dtype == np.dtype(np.int64), "Noninteger contraction")
    require(all(abs(int(x)) <= 420*4096 for x in middle.flat)
            and all(abs(int(x)) <= 420*4096**2 for x in pair.flat), "Integer partial-sum bound failed")
    # Sum anti-diagonals independently for each harmonic, with Python integers.
    laurent = tuple(sum((int(pair[i, h+span-i]) for i in range(pair.shape[0])
                        if 0 <= h+span-i < pair.shape[1]), 0) for h in range(-12, 13))
    require(all(abs(x) <= 13*420*4096**2 for x in laurent)
            and laurent == tuple(reversed(laurent)), "Fold bound/evenness failed")
    cosine = (laurent[12],) + tuple(2*laurent[12+k] for k in range(1, 13))
    require(max(map(abs, cosine)) < 2**38, "Cosine numerator bound failed")
    return laurent, cosine


def edge_vector(row):
    values = tuple(q(value) for value in row)
    edges = tuple(itertools.combinations(range(8), 2))
    require(len(values) == 28 and min(values) >= 0 and max(values) <= 1 and sum(values) == 16,
            "Physical edge-mean vector failed")
    require(all(sum(values[e] for e, edge in enumerate(edges) if i in edge) == 4 for i in range(8)), "Incident mean identity failed")
    return values


def functional(vector):
    edges = tuple(itertools.combinations(range(8), 2))
    return (vector[edges.index((0, 4))] - vector[edges.index((1, 5))])/2


def triangle_margin(cosine, B):
    require(len(cosine) == 13 and all(type(x) is int or isinstance(x, Q) for x in (*cosine, B)), "Exact13-harmonic triangle inputs required")
    return Q(cosine[0]) - sum((abs(Q(x)) for x in cosine[1:]), Q(0)) - Q(B)


def fixed_inputs(root):
    source = read_json(root/SOURCE)
    require(source["kernel_denominator"] == KERNEL_DEN, "Source denominator changed")
    power = [tuple(q(c) for c in row) for row in source["crossing_power"]]
    require(len(power) == 28 and all(len(row) == 7 for row in power), "Source shape changed")
    target = edge_vector([{"numerator": value.numerator, "denominator": value.denominator}
                          for value in (sum((c*Q(1, 4)**h for h, c in enumerate(row)), Q(0)) for row in power)])
    del source
    checkpoint = read_json(root/CHECKPOINT, historical=True)
    require(tuple(map(q, checkpoint["target_exact"])) == target, "Old B target changed")
    edges = tuple(itertools.combinations(range(8), 2))
    w = tuple(Q(1, 2) if e == (0, 4) else Q(-1, 2) if e == (1, 5) else Q(0) for e in edges)
    require(tuple(map(q, checkpoint["dual_exact"]["signed_weights"])) == w, "Frozen w changed")
    graph = tuple(map(q, checkpoint["nonnegative_graph_witness"]["weights_normalized_sum_one"]))
    shift = q(checkpoint["nonnegative_graph_witness"]["uniform_edge_shift"])
    scale = q(checkpoint["nonnegative_graph_witness"]["weight_sum"])
    require(scale > 0 and min(graph) >= 0 and sum(graph) == 1 and graph == tuple((x+shift)/scale for x in w), "Old graph normalization changed")
    del checkpoint
    library = read_json(root/LIBRARY)
    require(library["denominator"] == KERNEL_DEN and len(library["labels"]) == len(library["crossing_numerators"]) == 71, "Old library changed")
    anchors, uniform_seen = {}, False
    for label, row in zip(library["labels"], library["crossing_numerators"]):
        values = edge_vector([{"numerator": Q(x, KERNEL_DEN).numerator, "denominator": Q(x, KERNEL_DEN).denominator}
                              for x in integers(row, 28)])
        if label["kind"] == "b4":
            first, second = (integers(g, 4) for g in label["groups"])
            require(label["theta"] in ("0", "pi/2") and second == tuple(i for i in range(8) if i not in first), "Endpoint grouping changed")
            key = (label["theta"], first)
            require(key not in anchors, "Duplicate endpoint anchor")
            anchors[key] = functional(values)
        else:
            require(not uniform_seen and label == {"kind": "uniform70"} and values == (Q(4, 7),)*28, "Uniform control changed")
            uniform_seen = True
    require(uniform_seen, "Uniform control missing")
    del library
    same_phase = read_json(root/ANCHORS, historical=True)
    require(tuple(map(q, same_phase["target_exact"])) == target and tuple(map(q, same_phase["saved_P53b_signed_weights"])) == w, "Same-phase B/w changed")
    controls = same_phase["new_controls_raw"]
    require(len(controls["labels"]) == len(controls["crossing_numerators"]) == 35, "Pi3 controls missing")
    for label, row in zip(controls["labels"], controls["crossing_numerators"]):
        require(label["kind"] == "b4" and label["theta"] == "pi/3", "Pi3 label changed")
        values = edge_vector([{"numerator": Q(x, KERNEL_DEN).numerator, "denominator": Q(x, KERNEL_DEN).denominator}
                              for x in integers(row, 28)])
        first, second = (integers(g, 4) for g in label["groups"])
        require(second == tuple(i for i in range(8) if i not in first), "Pi3 complementary grouping changed")
        key = ("pi/3", first)
        require(key not in anchors, "Duplicate pi3 anchor")
        anchors[key] = functional(values)
    return target, w, graph, scale, anchors


def anchor_value(cosine, value):
    require(len(cosine) == 13 and all(type(x) is int or isinstance(x, Q) for x in (*cosine, value)), "Exact13-harmonic anchor required")
    previous, current, total = Q(1), value, cosine[0] + cosine[1]*value
    for k in range(2, 13):
        previous, current = current, 2*value*current - previous
        total += cosine[k]*current
    return total


def replay(root):
    observed = {name: sha(root/name) for name in PINS}
    require(observed == PINS, "Pinned source/raw hash mismatch")
    manifest = read_json(root/REFERENCE_MANIFEST, historical=True)
    require(manifest["schema_version"] == 2 and manifest["run"]["status"] == "completed"
            and manifest["run"]["exit_status"] == 0, "Reference run not completed")
    target, w, graph, scale, anchors = fixed_inputs(root)
    data = read_json(root/CANDIDATE, maximum=4*1024**2)
    B = functional(target)
    require(q(data["fixed_B_mean"]) == B and tuple(map(q, data["saved_w"])) == w
            and tuple(map(q, data["same_old_graph_normalized"])) == graph, "Candidate B/w/graph mismatch")
    counts4, counts8 = tuple(occupations(4)), tuple(occupations(8))
    old4 = [integers(row, 8) for row in data["counts4"]]
    old8 = [integers(row, 8) for row in data["counts8"]]
    require(len(old4) == len(set(old4)) == 330 and set(old4) == set(counts4)
            and len(old8) == len(set(old8)) == 6435 and set(old8) == set(counts8), "Fock support missing/duplicate")
    index = {n: i for i, n in enumerate(old4)}
    scalars = {n: direct_tie_scalar(n) for n in counts8}
    require(tuple(integers(data["tie_scalar_numerators_over840"], 6435)) == tuple(scalars[n] for n in old8), "Direct70-subset scalar mismatch")
    raw_matrix = [[scalars[tuple(a+b for a, b in zip(n, m))] for m in counts4] for n in counts4]
    require(all(abs(x) <= 420 for row in raw_matrix for x in row), "Python M bound before cast failed")
    old_matrix = [integers(row, 330) for row in data["M"]]
    require(len(old_matrix) == 330 and all(raw_matrix[i][j] == old_matrix[index[n]][index[m]]
                                         for i, n in enumerate(counts4) for j, m in enumerate(counts4)), "Rebuilt M mismatch")
    matrix = np.asarray(raw_matrix, dtype=np.int64)
    groups = tuple(itertools.combinations(range(8), 4))
    archived = {integers(row["group"], 4): row for row in data["group_spectra"]}
    require(len(data["group_spectra"]) == len(archived) == 70 and set(archived) == set(groups)
            and len(data["groups"]) == 70 and {integers(g, 4) for g in data["groups"]} == set(groups), "Group support changed")
    banks, patterns, entries = {}, 0, 0
    for group in groups:
        item = archived[group]; bank = []
        require(item["probability_denominator"] == 4096 and item["phase_degree"] == 3*sum(a >= 4 for a in group), "Group convention changed")
        require(len(item["creation_coefficients"]) == len(item["probability_laurent_numerators"]) == 330, "Group rows missing")
        for n in counts4:
            c = permanent_polynomial(n, group); row = laurent_probability(c, n)
            require(c == integers(item["creation_coefficients"][index[n]], len(c))
                    and row == integers(item["probability_laurent_numerators"][index[n]], len(row)), "Independent permanent/Laurent mismatch")
            bank.append(row); patterns += 1; entries += len(row)
        bounds = column_bounds(bank)
        mass = tuple(sum(row[j] for row in bank) for j in range(len(bank[0])))
        require(mass == tuple(4096 if j == len(bank[0])//2 else 0 for j in range(len(bank[0])))
                and mass == integers(item["normalization_harmonic_sums"], len(mass))
                and bounds == integers(item["per_column_L1"], len(bounds)), "Parseval/L1 normalization mismatch")
        banks[group] = bank
    records = {integers(row["groups"][0], 4): row for row in data["all35_records"]}
    firsts = tuple(g for g in groups if 0 in g)
    require(len(data["all35_records"]) == len(records) == 35 and set(records) == set(firsts)
            and set(anchors) == {(phase, g) for phase in ("0", "pi/2", "pi/3") for g in firsts}, "35/105 coverage missing")
    bounds = []
    for first in firsts:
        second = tuple(i for i in range(8) if i not in first); item = records[first]
        require(integers(item["groups"][1], 4) == second, "Complementary species changed")
        laurent, cosine = two_einsum_spectrum(banks[first], banks[second], matrix)
        saved = item["contraction"]
        require(saved["denominator"] == SCALAR_DEN and laurent == integers(saved["laurent_numerators"], 25)
                and cosine == integers(saved["cosine_numerators"], 13), "Independent scalar contraction mismatch")
        exact_cosine = tuple(Q(x, SCALAR_DEN) for x in cosine)
        require(exact_cosine == tuple(map(q, item["cosine_coefficients"])), "Rational Fourier coefficients changed")
        for phase, t in (("0", Q(1)), ("pi/2", Q(0)), ("pi/3", Q(1, 2))):
            value = anchor_value(exact_cosine, t); saved_anchor = item["exact_phase_anchors"][phase]
            require(value == anchors[(phase, first)] == q(saved_anchor["spectrum_value"])
                    == q(saved_anchor["archived_value"]), "Independent exact anchor mismatch")
        lower = triangle_margin(exact_cosine, B)
        decision = item["decision"]
        require(lower > 0 and decision["status"] == "STRICT_UNIFORM_GAP" and decision["certificate_stage"] == "triangle"
                and decision["Bernstein_stages"] == [] and decision["nonnegative_proven"] is True
                and q(decision["lower_bound"]) == q(decision["triangle_lower_bound"]) == lower, "Triangle-only certificate failed")
        bounds.append(lower)
    lower = min(bounds + [-B])  # Included uniform kernel has functional mean0.
    outcome = data["outcome"]
    require(lower > 0 and outcome["status"] == "STRICT_UNIFORM_FIXED_W_B4_PHASE_GAP"
            and q(outcome["uniform_lower_bound"]) == lower
            and q(outcome["same_old_normalized_graph_lower_bound"]) == lower/scale, "Aggregate lower bound mismatch")
    require(data["control_family"] == "b4(4+4) only, same architecture, every real phase"
            and data["untested_species_bipartitions"] == ["7+1", "6+2", "5+3"], "Scientific scope changed")
    return {"status": "EXACT_INDEPENDENT_TRIANGLE_REPLAY_PASS", "uniform_signed_triangle_lower_bound": lower,
            "same_old_normalized_graph_lower_bound": lower/scale, "fixed_B_mean": B,
            "creation_patterns_checked": patterns, "Laurent_coefficients_checked": entries,
            "direct_decoder_states_checked": len(counts8), "M_entries_checked": 330**2,
            "scalar_spectra_checked": len(bounds), "exact_anchors_checked": 3*len(bounds),
            "pinned_SHA256": observed, "production_modules_imported": False, "LP_calls": 0,
            "posthoc_NONBLIND": True, "B_mean_depends_on_pinned_previously_validated_P53_source": True,
            "scope": "ONE fixed N8 B_pi3/w/graph versus35 b4(4+4) every_real_phi plus uniform, linear MEAN only",
            "unused_Bernstein_branch_replayed": False, "no_algorithmic_advantage_or_hardware_claim": True}


def encoded(value):
    if isinstance(value, Q): return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict): return {key: encoded(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)): return [encoded(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists(): raise FileExistsError("Fresh checker output required")
    cpu, wall = time.process_time(), time.perf_counter()
    try:
        report = replay(Path(__file__).resolve().parents[1])
    except Exception as error:
        report = {"status": "CHECK_FAILED", "error": repr(error), "posthoc_NONBLIND": True}
    report.update(CPU_seconds=time.process_time()-cpu, wall_seconds=time.perf_counter()-wall,
                  checker_source_SHA256=sha(__file__))
    text = json.dumps(encoded(report), indent=2, allow_nan=False)+"\n"
    require(len(text.encode()) <= 4*1024**2, "Output cap exceeded")
    with args.output.open("x") as stream: stream.write(text)
    print(json.dumps(encoded(report), allow_nan=False))
    return 0 if report["status"] == "EXACT_INDEPENDENT_TRIANGLE_REPLAY_PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
