"""Prospective N6 exact phase response; no graphs, sampling, LP or float proof.

Coefficient pairs represent a+b*xi, xi^2=xi-1. Entry triples append the
zeta exponent. All six-photon occupations, including zeros, are retained.
"""
import argparse
from fractions import Fraction as F
import gzip
import itertools
import json
import math
from pathlib import Path
import platform
import time
import traceback


ZERO, ONE = (0, 0), (1, 0)
N, PHOTONS, K, DEN = 6, 6, 3, 150**6
EDGES = tuple(itertools.combinations(range(N), 2))
SUBSETS = tuple(itertools.combinations(range(N), K))
CLASSES = tuple(s for s in SUBSETS if 0 in s)
SPEC_PATH = "research/P59_exact_fixed_response_spec.json"
OUTPUT_CAP = 4*1024**2


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def integer(value):
    require(type(value) is int, "Exact Python integer required")
    return value


def add(a, b):
    return a[0]+b[0], a[1]+b[1]


def scale(a, k):
    return a[0]*k, a[1]*k


def mul(a, b):
    return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]+a[1]*b[1]


def conj(a):
    return a[0]+a[1], -a[1]


def norm(a):
    return a[0]**2+a[0]*a[1]+a[1]**2


def occupations(modes, total):
    require(type(modes) is type(total) is int and modes > 0 and total >= 0,
            "Nonnegative integer occupation domain required")
    for slots in itertools.combinations_with_replacement(range(modes), total):
        row = [0]*modes
        for i in slots:
            row[i] += 1
        yield tuple(row)


def frozen_matrix():
    powers = (ONE, (-1, 1), (0, -1))
    raw = [[(*scale(powers[((r//2)*(s//2)) % 3], (-1)**((r % 2)*(s % 2))),
             int(s//2 == 1 and r % 2 == 1)) for s in range(N)] for r in range(N)]
    out = [[(*scale(entry[:2], 5), entry[2]) for entry in row] for row in raw]
    for s in range(N):
        require(raw[0][s][2] == raw[2][s][2] == 0, "Mixed rows must be phase free")
        out[0][s] = (*add(scale(raw[0][s][:2], 3), scale(raw[2][s][:2], -4)), 0)
        out[2][s] = (*add(scale(raw[0][s][:2], 4), scale(raw[2][s][:2], 3)), 0)
    return tuple(tuple(row) for row in out)


def validate_matrix(matrix):
    require(len(matrix) == N and all(len(row) == N for row in matrix), "Frozen6x6 matrix required")
    for row in matrix:
        for entry in row:
            require(len(entry) == 3 and all(type(x) is int for x in entry)
                    and entry[2] in (0, 1), "Integer monomial entry required")
    for a, b in itertools.product(range(N), repeat=2):
        gram = {}
        for row in matrix:
            exponent = row[b][2]-row[a][2]
            gram[exponent] = add(gram.get(exponent, ZERO), mul(conj(row[a][:2]), row[b][:2]))
        require(all(value == ((150, 0) if a == b and h == 0 else ZERO)
                    for h, value in gram.items()), "Laurent Gram150I failed")
    q = tuple(tuple(F(norm(entry[:2]), 150) for entry in row) for row in matrix)
    expected = tuple(tuple(F(x, 150) for x in row) for row in
                     ((1, 1, 37, 37, 37, 37), (25,)*6, (49, 49, 13, 13, 13, 13),
                      (25,)*6, (25,)*6, (25,)*6))
    require(q == expected and all(sum(row) == 1 for row in q)
            and all(sum(q[i][a] for i in range(N)) == 1 for a in range(N)), "Frozen q failed")
    return q


def creation_coefficients(matrix):
    """Multiply the actual input columns, not the pre-factored analytic formula."""
    modes = len(matrix)
    require(0 < modes <= N and all(len(row) == modes for row in matrix), "Square source<=6 required")
    terms = {((0,)*modes, 0): ONE}
    for source in range(modes):
        following = {}
        for (n, h), value in terms.items():
            for i in range(modes):
                entry = matrix[i][source]
                require(all(type(x) is int for x in entry) and entry[2] in (0, 1), "Integer source required")
                exponent = h+entry[2]
                require(exponent <= 2, "Frozen phase degree2 exceeded")
                target = n[:i]+(n[i]+1,)+n[i+1:]
                key = target, exponent
                following[key] = add(following.get(key, ZERO), mul(value, entry[:2]))
        terms = {key: value for key, value in following.items() if value != ZERO}
    return {n: tuple(terms.get((n, h), ZERO) for h in range(3)) for n in occupations(modes, modes)}


def permanent_coefficient(matrix, n):
    """Single-occupation independent guard: all720 monomial permutations/n!."""
    require(len(n) == N and all(type(x) is int and x >= 0 for x in n)
            and sum(n) == PHOTONS, "Six-photon fixture required")
    rows = tuple(i for i, count in enumerate(n) for _ in range(count))
    result = [ZERO]*3
    for assignment in itertools.permutations(range(N)):
        value, h = ONE, 0
        for row, source in zip(rows, assignment):
            entry = matrix[row][source]
            value, h = mul(value, entry[:2]), h+entry[2]
        require(h <= 2, "Fixture phase degree changed")
        result[h] = add(result[h], value)
    factorial = math.prod(math.factorial(x) for x in n)
    require(all(x % factorial == 0 for pair in result for x in pair), "Permanent/n! not integral")
    return tuple(tuple(x//factorial for x in pair) for pair in result)


def probability_spectrum(coefficients, n, denominator=DEN):
    c0, c1, c2 = coefficients
    require(c1 == ZERO, "Forbidden first source harmonic")
    factorial = math.prod(math.factorial(x) for x in n)
    cross = mul(c2, conj(c0))
    return (F(factorial*(norm(c0)+norm(c2)), denominator),
            F(factorial*cross[0], denominator), F(factorial*cross[1], denominator))


def sum_spectra(items):
    result = [F(0)]*3
    for weight, spectrum in items:
        for h in range(3):
            result[h] += weight*spectrum[h]
    return tuple(result)


def response(spectrum):
    u, alpha, beta = spectrum
    v, r = 2*alpha+beta, -2*beta
    return {"u": u, "F2": (alpha, beta), "cos2": v, "derivative_over_sqrt3": r,
            "sin2_over_sqrt3": r/2, "center_mean": u+v,
            "curvature_upper": 4*(abs(v)+abs(r))}


def decoder(n):
    require(len(n) == N and all(type(x) is int and x >= 0 for x in n)
            and sum(n) == PHOTONS, "Exact six-photon count vector required")
    scores = tuple(sum(n[i] for i in subset) for subset in SUBSETS)
    best = max(scores)
    winners = tuple(s for s, value in zip(SUBSETS, scores) if value == best)
    sets = tuple(set(s) for s in winners)
    edge = tuple(F(sum((i in s) != (j in s) for s in sets), len(sets)) for i, j in EDGES)
    classes = tuple(F(sum((tuple(sorted(s)) if 0 in s else tuple(i for i in range(N) if i not in s)) == c
                         for s in sets), len(sets)) for c in CLASSES)
    require(sum(classes) == 1 and sum(edge) == 9, "Decoder class/edge normalization")
    for i in range(N):
        require(sum(edge[e] for e, pair in enumerate(EDGES) if i in pair) == 3, "Per-state incidence3")
    return winners, edge, classes


def diagonal_pmf(row):
    e = [F(1)]+[F(0)]*len(row)
    for probability in row:
        for h in range(len(row), 0, -1):
            e[h] += probability*e[h-1]
    shifted = [math.factorial(h)*value for h, value in enumerate(e)]
    return tuple(sum(shifted[h]*math.comb(h, t)*(-1)**(h-t) for h in range(t, len(row)+1))
                 for t in range(len(row)+1))


def factorial_weight(n, powers):
    if any(power > value for power, value in zip(powers, n)):
        return 0
    return math.prod(math.factorial(value)//math.factorial(value-power) for value, power in zip(n, powers))


def moment_target(q, powers):
    """Derivatives of P1/P2/P3 from the independently audited full-square lemma."""
    indices = tuple(i for i, power in enumerate(powers) for _ in range(power))
    require(1 <= len(indices) <= 3, "Only factorial orders1..3")
    if len(indices) == 1:
        return F(1)
    def dot(i, j):
        return sum(q[i][a]*q[j][a] for a in range(len(q)))
    i, j = indices[:2]
    if len(indices) == 2:
        return 1+int(i == j)-2*dot(i, j)
    k = indices[2]
    return (1+int(i == j)+int(i == k)+int(j == k)+2*int(i == j == k)
            -2*(dot(i, j)+dot(i, k)+dot(j, k))
            -4*(int(i == j)*dot(i, k)+int(i == k)*dot(i, j)+int(j == k)*dot(i, j))
            +12*sum(q[i][a]*q[j][a]*q[k][a] for a in range(len(q))))


def hand_fixture(matrix):
    n = (4, 2, 0, 0, 0, 0)
    value = permanent_coefficient(matrix, n)
    require(value == ((-35050, 1000), ZERO, (175, -1000)), "Independent analytic PNR coefficients")
    spectrum = probability_spectrum(value, n)
    require(response(spectrum)["derivative_over_sqrt3"] == -F(124, 421875), "Independent PNR slope sign/Fock")
    return n, value


def exact_json(value):
    if isinstance(value, F):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [exact_json(item) for item in value]
    require(value is None or type(value) in (str, int, bool), "Unexpected/inexact JSON proof value")
    return value


def calibrate():
    matrix = frozen_matrix()
    q = validate_matrix(matrix)
    fixture_n, fixture_value = hand_fixture(matrix)
    creation = creation_coefficients(matrix)
    require(len(creation) == 462 and creation[fixture_n] == fixture_value, "Full462 source/fixture agreement")
    rows, spectra, edge_weights, class_weights, ways = [], [], [], [], []
    parity_allowed = 0
    for n, coefficients in creation.items():
        parity = sum(n[i] for i in (0, 2, 4))
        parity_allowed += int(parity % 2 == 0)
        require(parity % 2 == 0 or coefficients == (ZERO, ZERO, ZERO), "Forbidden even-color parity: "+repr(n))
        require(parity >= 2 or coefficients[0] == ZERO, "c0 even-sector lower bound: "+repr(n))
        require(parity <= 4 or coefficients[2] == ZERO, "c2 even-sector upper bound: "+repr(n))
        spectrum = probability_spectrum(coefficients, n)
        winners, edges, classes = decoder(n)
        rows.append({"n": n, "coefficients_zeta0_1_2": coefficients, "probability_spectrum": response(spectrum),
                     "fock_factorial": math.prod(math.factorial(x) for x in n),
                     "winning_subsets": winners, "edge_kernel": edges, "class_kernel": classes})
        spectra.append(spectrum); edge_weights.append(edges); class_weights.append(classes); ways.append(len(winners))
    require(parity_allowed == 236 and len(rows)-parity_allowed == 226, "All462 parity coverage")
    require(set(ways) == {1, 2, 3, 4, 6, 10, 20} and math.lcm(*ways) == 60, "Observed complete tie support/LCM60")
    require(sum_spectra((1, s) for s in spectra) == (F(1), F(0), F(0)), "All-phase source mass1")
    diagonal = []
    for i in range(N):
        target = diagonal_pmf(q[i])
        require(min(target) >= 0 and sum(target) == 1, "Exact q-PGF positivity/mass")
        for t in range(PHOTONS+1):
            actual = sum_spectra((int(row["n"][i] == t), s) for row, s in zip(rows, spectra))
            require(actual == (target[t], F(0), F(0)), "One-mode bin phase/q invariance: "+repr((i, t, actual, target[t])))
            diagonal.append({"mode": i, "count": t, "spectrum": response(actual), "q_target": target[t]})
    moments = []
    for degree in (1, 2, 3):
        for powers in occupations(N, degree):
            actual = sum_spectra((factorial_weight(row["n"], powers), s) for row, s in zip(rows, spectra))
            target = moment_target(q, powers)
            require(actual == (target, F(0), F(0)), "Joint factorial moment q-only identity: "+repr((powers, actual, target)))
            moments.append({"powers": powers, "spectrum": response(actual), "q_target": target})
    require(len(diagonal) == 42 and len(moments) == 83, "PMF/moment coverage")
    edge_spectra = tuple(sum_spectra((w[e], s) for w, s in zip(edge_weights, spectra)) for e in range(15))
    class_spectra = tuple(sum_spectra((w[c], s) for w, s in zip(class_weights, spectra)) for c in range(10))
    crossing = tuple(tuple(int((i in subset) != (j in subset)) for i, j in EDGES) for subset in CLASSES)
    require(all(sum(a*b for a, b in zip(first, second)) == (9 if c == d else 5)
                for c, first in enumerate(crossing) for d, second in enumerate(crossing)), "Cut Gram diagonal9/off5")
    for c, pattern in enumerate(crossing):
        via_edges = sum_spectra((pattern[e], s) for e, s in enumerate(edge_spectra))
        inverse = ((via_edges[0]-5)/4, via_edges[1]/4, via_edges[2]/4)
        require(inverse == class_spectra[c], "Class spectrum Gram inversion: "+repr((c, inverse, class_spectra[c])))
    require(sum_spectra((1, s) for s in class_spectra) == (F(1), F(0), F(0)), "Class mass1")
    for i in range(N):
        require(sum_spectra((int(i in pair), s) for pair, s in zip(EDGES, edge_spectra))
                == (F(3), F(0), F(0)), "All-phase edge incidence3")
    require(sum_spectra((1, s) for s in edge_spectra) == (F(9), F(0), F(0)), "All-phase total crossing9")
    edges = [{"edge": pair, **response(s)} for pair, s in zip(EDGES, edge_spectra)]
    classes = [{"subset_with_zero": subset, **response(s)} for subset, s in zip(CLASSES, class_spectra)]
    nonzero_slope = any(item["derivative_over_sqrt3"] != 0 for item in edges)
    nonconstant = any(item["cos2"] != 0 for item in edges)
    status = ("NONZERO_FIXED_CENTER_EDGE_RESPONSE" if nonzero_slope else
              "ZERO_CENTER_SLOPE_WITH_FINITE_PHASE_MEAN_CHANNEL" if nonconstant else
              "ALL_DECODED_EDGE_MEANS_PHASE_INVARIANT")
    summary = {"status": status, "phi_center": 0, "harmonics": [-2, 0, 2], "source": "1^6",
               "states": 462, "parity_allowed": 236, "parity_structural_zeros": 226,
               "source_denominator": DEN, "tie_LCM": 60, "diagonal_bins": 42, "joint_moments": 83,
               "edge_responses": edges, "class_responses": classes,
               "nonclaims": "No graph/optimum/advantage/genuine-six-photon witness/benchmark/hardware result"}
    raw = {"summary": summary, "Q_entries_a_b_zeta_degree": matrix, "q": q, "states": rows,
           "diagonal_bins": diagonal, "factorial_moments": moments,
           "guard_flags": {"gram150I": True, "mass_all_phi": True, "PNR_fixture": True,
                           "q_only_low_moments": True, "class_gram_inversion": True,
                           "all_decoder_ties": True, "incident_and_total_spectra": True}}
    return summary, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    started_cpu, started_wall = time.process_time(), time.perf_counter()
    try:
        spec = json.loads(Path(SPEC_PATH).read_text())
        require(spec["N"] == N and spec["photons"] == PHOTONS and spec["K"] == K
                and spec["rotation_block"] == [[3, -4], [4, 3]] and spec["rotation_denominator"] == 5
                and spec["phi_center"] == 0 and spec["source_denominator"] == DEN,
                "Frozen specification mismatch")
        summary, raw = calibrate()
        summary["metadata"] = {"python": platform.python_version(), "CPU_seconds": repr(time.process_time()-started_cpu),
                               "wall_seconds": repr(time.perf_counter()-started_wall),
                               "timing_scope": "Complete exact calibration; JSON/gzip/export excluded and runner time authoritative"}
        raw_bytes = json.dumps(exact_json(raw), sort_keys=True, separators=(",", ":")).encode()
        summary_bytes = json.dumps(exact_json(summary), sort_keys=True, indent=2).encode()
        require(len(raw_bytes)+len(summary_bytes)+5 <= OUTPUT_CAP, "Scientific output pre-compression cap")
        compressed = gzip.compress(raw_bytes, mtime=0)
        require(len(compressed)+len(summary_bytes)+5 <= OUTPUT_CAP, "Scientific compressed-output cap")
        (output/"raw.json.gz").write_bytes(compressed)
        (output/"summary.json").write_bytes(summary_bytes)
        (output/"failure.json").write_text("null\n")
        print(json.dumps(exact_json(summary), sort_keys=True))
    except Exception as error:
        failure = {"status": "IMPLEMENTATION_OR_CONSTRUCTION_FAILURE", "error_type": type(error).__name__,
                   "message": str(error), "traceback": traceback.format_exc(), "automatic_retry": False}
        (output/"failure.json").write_text(json.dumps(failure, sort_keys=True, indent=2))
        raise


if __name__ == "__main__":
    main()
