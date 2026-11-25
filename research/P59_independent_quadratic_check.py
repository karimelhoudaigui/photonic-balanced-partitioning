"""Independent P59 exact replication: three quadratic factors, no production imports.

The primary result is opened only as SHA-pinned data after source freeze.
No graph/optimum, RNG, floating proof, native numeric or optical backend.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

PROBABILITY_DENOMINATOR = 150**6
EDGES = tuple(itertools.combinations(range(6), 2))
CLASSES = tuple((0,)+pair for pair in itertools.combinations(range(1, 6), 2))
OUTPUT_CAP = 4*1024**2
INFLATED_CAP = 8*1024**2


def add(x, y): return x[0]+y[0], x[1]+y[1]
def mul(x, y): return x[0]*y[0]-x[1]*y[1], x[0]*y[1]+x[1]*y[0]+x[1]*y[1]
def conjugate(x): return x[0]+x[1], -x[1]
def norm(x): return x[0]**2+x[0]*x[1]+x[1]**2
def scale(x, k): return x[0]*k, x[1]*k


# Explicit 5*E_b and O_b in the independent paired-factor construction.
EVEN = (((-1, 0), (7, 0), (5, 0)),
        ((7, -4), (1, 3), (0, -5)),
        ((3, 4), (4, -3), (-5, 5)))
ODD = (((1, 0), (1, 0), (1, 0)),
       ((1, 0), (-1, 1), (0, -1)),
       ((1, 0), (0, -1), (-1, 1)))


def occupations():
    # A multiset of six output labels, not a production composition recursion.
    result = []
    for labels in itertools.combinations_with_replacement(range(6), 6):
        result.append(tuple(labels.count(i) for i in range(6)))
    return tuple(sorted(result))


def quadratic_factor(block):
    result = []
    for odd, variables, coefficients in ((False, (0, 2, 4), EVEN[block]), (True, (1, 3, 5), ODD[block])):
        for i in range(3):
            for j in range(i, 3):
                powers = [0]*6; powers[variables[i]] += 1; powers[variables[j]] += 1
                factor = (-25 if odd else 1)*(1 if i == j else 2)
                result.append((tuple(powers), 2 if odd and block == 1 else 0,
                               scale(mul(coefficients[i], coefficients[j]), factor)))
    if len(result) != 12:
        raise ArithmeticError("Each paired factor must have twelve terms")
    return tuple(result)


def coefficient_table(only=None):
    states = occupations() if only is None else tuple(only)
    result = {n: [(0, 0), (0, 0), (0, 0)] for n in states}
    products = 0
    for a, b, c in itertools.product(*(quadratic_factor(block) for block in range(3))):
        products += 1
        n = tuple(x+y+z for x, y, z in zip(a[0], b[0], c[0]))
        h = a[1]+b[1]+c[1]
        if h not in (0, 2):
            raise ArithmeticError("Paired source generated a forbidden phase exponent")
        if n in result:
            result[n][h] = add(result[n][h], mul(mul(a[2], b[2]), c[2]))
    if products != 1728 or any(row[1] != (0, 0) for row in result.values()):
        raise ArithmeticError("Paired-factor bound or c1=0 invariant failed")
    return {n: tuple(values) for n, values in result.items()}


def matrix_and_q():
    entries = []
    for row in range(6):
        a, i = divmod(row, 2); values = []
        for block in range(3):
            for j in range(2):
                pair = EVEN[block][a] if i == 0 else scale(ODD[block][a], 5*(-1)**j)
                values.append((*pair, 1 if i == 1 and block == 1 else 0))
        entries.append(values)
    for first in range(6):
        for second in range(6):
            gram = {}
            for row in range(6):
                a, b, h = entries[row][first]; c, d, k = entries[row][second]
                gram[k-h] = add(gram.get(k-h, (0, 0)), mul(conjugate((a, b)), (c, d)))
            if any(value != ((150, 0) if first == second and h == 0 else (0, 0)) for h, value in gram.items()):
                raise ArithmeticError("Independent Laurent Gram is not150I")
    q = tuple(tuple(F(norm((a, b)), 150) for a, b, _ in row) for row in entries)
    if any(sum(row) != 1 for row in q) or any(sum(q[i][j] for i in range(6)) != 1 for j in range(6)):
        raise ArithmeticError("Fixed q is not doubly stochastic")
    return entries, q


def response(accumulator):
    u, alpha, beta = accumulator
    cosine = 2*alpha+beta; derivative = -2*beta
    return {"u": u, "F2": (alpha, beta), "cos2": cosine,
            "derivative_over_sqrt3": derivative, "sin2_over_sqrt3": derivative/2,
            "center_mean": u+cosine, "curvature_upper": 4*(abs(cosine)+abs(derivative))}


def probability_spectrum(coefficients, factorial):
    (a, b), forbidden, (c, d) = coefficients
    if forbidden != (0, 0): raise ArithmeticError("Forbidden c1")
    factor = F(factorial, PROBABILITY_DENOMINATOR)
    # Positive harmonic is c2*conjugate(c0); use a determinant, not floating phases.
    return response((factor*(norm((a, b))+norm((c, d))),
                     factor*(c*(a+b)+b*d), factor*(a*d-b*c)))


def threshold_data(n, k=3):
    cutoff = sorted(n, reverse=True)[k-1]
    high = tuple(i for i, x in enumerate(n) if x > cutoff)
    tied = tuple(i for i, x in enumerate(n) if x == cutoff)
    return high, tied, k-len(high)


def edge_kernel(n, k=3):
    high, tied, needed = threshold_data(n, k); high, tied = set(high), set(tied)
    count = len(tied); answer = []
    for a, b in itertools.combinations(range(len(n)), 2):
        ta, tb = a in tied, b in tied
        if ta and tb:
            value = F(2*needed*(count-needed), count*(count-1))
        elif ta or tb:
            fixed = b if ta else a
            value = 1-F(needed, count) if fixed in high else F(needed, count)
        else:
            value = F(int((a in high) != (b in high)))
        answer.append(value)
    return tuple(answer)


def class_kernel(kernel):
    # Ten UNORIENTED classes; no enumeration of the primary's twenty subsets.
    result = tuple((sum((value for edge, value in zip(EDGES, kernel) if (edge[0] in subset) != (edge[1] in subset)), F(0))-5)/4
                   for subset in CLASSES)
    if min(result) < 0 or sum(result) != 1:
        raise ArithmeticError("Gram inversion did not produce a class law")
    return result


def falling(value, order):
    answer = 1
    for j in range(order): answer *= value-j
    return answer


def moment_powers():
    return tuple(tuple(labels.count(i) for i in range(6)) for order in (1, 2, 3)
                 for labels in itertools.combinations_with_replacement(range(6), order))


def q_moment(powers, q):
    modes = [i for i, power in enumerate(powers) if power]
    degree = sum(powers)
    product = lambda rows: sum((math.prod(row[a] for row in rows) for a in range(len(q[0]))), F(0))
    if degree == 1: return F(1)
    if degree == 2:
        return 2-2*product([q[modes[0]]]*2) if len(modes) == 1 else 1-2*product([q[i] for i in modes])
    if degree != 3: raise ValueError("Only moments1..3")
    if len(modes) == 1:
        row = q[modes[0]]; return 6-18*product([row]*2)+12*product([row]*3)
    if len(modes) == 2:
        twice = next(i for i in modes if powers[i] == 2); once = next(i for i in modes if powers[i] == 1)
        return 2-2*product([q[twice]]*2)-8*product([q[twice], q[once]])+12*product([q[twice], q[twice], q[once]])
    return 1-2*sum((product([q[i], q[j]]) for i, j in itertools.combinations(modes, 2)), F(0))+12*product([q[i] for i in modes])


def q_pmf(row):
    elementary = [F(1)]+[F(0)]*6
    for probability in row:
        for r in range(6, 0, -1): elementary[r] += probability*elementary[r-1]
    return tuple(sum((math.factorial(r)*elementary[r]*math.comb(r, n)*(-1)**(r-n) for r in range(n, 7)), F(0)) for n in range(7))


def derive():
    entries, q = matrix_and_q(); coefficients = coefficient_table(); states = []
    for n, values in coefficients.items():
        factorial = math.prod(math.factorial(x) for x in n)
        kernel = edge_kernel(n); classes = class_kernel(kernel)
        if any(sum((kernel[e] for e, edge in enumerate(EDGES) if vertex in edge), F(0)) != 3 for vertex in range(6)):
            raise ArithmeticError("Per-state balanced incidence failed")
        if sum(n[1::2]) % 2 and any(value != (0, 0) for value in values):
            raise ArithmeticError("Odd-color parity coefficient survived")
        spectrum = probability_spectrum(values, factorial)
        if spectrum["center_mean"] != F(factorial*norm(add(values[0], values[2])), PROBABILITY_DENOMINATOR):
            raise ArithmeticError("Per-state zero-phase Born identity failed")
        states.append({"n": n, "coefficients_zeta0_1_2": values, "fock_factorial": factorial,
                       "probability_spectrum": spectrum,
                       "edge_kernel": kernel, "class_kernel": classes})
    def statistic(weights):
        accumulator = [F(0), F(0), F(0)]
        for state, weight in zip(states, weights):
            spectrum = state["probability_spectrum"]
            accumulator[0] += spectrum["u"]*weight
            accumulator[1] += spectrum["F2"][0]*weight
            accumulator[2] += spectrum["F2"][1]*weight
        return response(tuple(accumulator))
    if len(states) != 462 or sum(sum(row["n"][1::2]) % 2 == 0 for row in states) != 236:
        raise ArithmeticError("Full occupation/parity population failed")
    mass = statistic([1]*462)
    if (mass["u"], mass["F2"]) != (1, (0, 0)): raise ArithmeticError("Full source all-phase normalization failed")
    fixture = next(row for row in states if row["n"] == (4, 2, 0, 0, 0, 0))
    if fixture["probability_spectrum"]["derivative_over_sqrt3"] != F(-124, 421875):
        raise ArithmeticError("Analytic pre-execution PNR fixture failed")
    edges = [{"edge": edge, **statistic([row["edge_kernel"][j] for row in states])} for j, edge in enumerate(EDGES)]
    classes = [{"subset_with_zero": subset, **statistic([row["class_kernel"][j] for row in states])} for j, subset in enumerate(CLASSES)]
    bins = []
    for mode in range(6):
        target = q_pmf(q[mode])
        if min(target) < 0 or sum(target) != 1: raise ArithmeticError("q-only PMF is not normalized")
        for count in range(7):
            observed = statistic([int(row["n"][mode] == count) for row in states])
            if observed["u"] != target[count] or observed["F2"] != (0, 0): raise ArithmeticError("Complete fixed marginal failed")
            bins.append({"mode": mode, "count": count, "spectrum": observed, "q_target": target[count]})
    moments = []
    for powers in moment_powers():
        observed = statistic([math.prod(falling(n, r) for n, r in zip(row["n"], powers)) for row in states])
        target = q_moment(powers, q)
        if observed["u"] != target or observed["F2"] != (0, 0): raise ArithmeticError("Degree<=3 harmonic/q moment failed")
        moments.append({"powers": powers, "spectrum": observed, "q_target": target})
    for vertex in range(6):
        incident = [row for row in edges if vertex in row["edge"]]
        if (sum(row["u"] for row in incident), sum(row["cos2"] for row in incident), sum(row["derivative_over_sqrt3"] for row in incident)) != (3, 0, 0):
            raise ArithmeticError("Decoded incidence harmonics failed")
    status = ("NONZERO_FIXED_CENTER_EDGE_RESPONSE" if any(row["derivative_over_sqrt3"] for row in edges) else
              "ZERO_CENTER_SLOPE_WITH_FINITE_PHASE_MEAN_CHANNEL" if any(row["cos2"] for row in edges) else
              "ALL_DECODED_EDGE_MEANS_PHASE_INVARIANT")
    return {"status": status, "Q_entries_a_b_zeta_degree": entries, "q": q, "states": states,
            "summary": {"edge_responses": edges, "class_responses": classes}, "diagonal_bins": bins,
            "factorial_moments": moments, "mass": mass,
            "structural_even_states": sum(sum(row["n"][1::2]) % 2 == 0 for row in states),
            "probability_denominator": PROBABILITY_DENOMINATOR, "method": "three12term quadratic factors;1728 products;hypergeometric ties;Gram classes"}


def rational(value):
    if (not isinstance(value, dict) or set(value) != {"numerator", "denominator"}
            or type(value["numerator"]) is not int or type(value["denominator"]) is not int
            or value["denominator"] <= 0 or math.gcd(value["numerator"], value["denominator"]) != 1):
        raise TypeError("Canonical exact rational pair required")
    return F(value["numerator"], value["denominator"])


def math_equal(actual, expected):
    if isinstance(expected, F): return rational(actual) == expected
    if type(expected) is int: return type(actual) is int and actual == expected
    if isinstance(expected, (tuple, list)):
        return isinstance(actual, (tuple, list)) and len(actual) == len(expected) and all(math_equal(a, b) for a, b in zip(actual, expected))
    if isinstance(expected, dict): return isinstance(actual, dict) and all(key in actual and math_equal(actual[key], value) for key, value in expected.items())
    raise TypeError("Unsupported proof comparison type")


def valid_winners(n, winners):
    high, tied, needed = threshold_data(n); high, tied = set(high), set(tied)
    if not isinstance(winners, list) or len(winners) != math.comb(len(tied), needed): return False
    canonical = set()
    for winner in winners:
        if (not isinstance(winner, list) or len(winner) != 3 or any(type(x) is not int for x in winner)
                or winner != sorted(set(winner)) or not high <= set(winner) <= high | tied): return False
        canonical.add(tuple(winner))
    return len(canonical) == len(winners)


def compare(primary, own):
    failures = []; checks = 0
    def check(label, actual, expected):
        nonlocal checks
        checks += 1
        try: passed = math_equal(actual, expected)
        except (TypeError, ValueError, KeyError): passed = False
        if not passed: failures.append(label)
    check("matrix", primary["Q_entries_a_b_zeta_degree"], own["Q_entries_a_b_zeta_degree"])
    check("q", primary["q"], own["q"])
    rows = {tuple(row["n"]): row for row in primary["states"]}
    if len(rows) != 462 or len(primary["states"]) != 462: failures.append("complete462occupationpopulation")
    for state in own["states"]:
        n = state["n"]; row = rows.get(n, {})
        for key in ("coefficients_zeta0_1_2", "fock_factorial", "probability_spectrum", "edge_kernel", "class_kernel"):
            check("state:"+str(n)+":"+key, row.get(key), state[key])
        checks += 1
        if not valid_winners(n, row.get("winning_subsets")): failures.append("winning_subsets:"+str(n))
    for name, key, target in (("edges", "edge", own["summary"]["edge_responses"]),
                              ("classes", "subset_with_zero", own["summary"]["class_responses"])):
        raw = primary["summary"]["edge_responses" if name == "edges" else "class_responses"]
        mapping = {tuple(row[key]): row for row in raw}
        if len(raw) != len(target) or len(mapping) != len(target): failures.append(name+"population")
        for expected in target: check(name+str(expected[key]), mapping.get(tuple(expected[key])), expected)
    for name, key in (("diagonal_bins", lambda row: (row["mode"], row["count"])),
                      ("factorial_moments", lambda row: tuple(row["powers"]))):
        raw = primary[name]; mapping = {key(row): row for row in raw}
        if len(raw) != len(own[name]) or len(mapping) != len(own[name]): failures.append(name+"population")
        for expected in own[name]: check(name+str(key(expected)), mapping.get(key(expected)), expected)
    return {"status": "PASS_EXACT_INDEPENDENT_REPLICATION" if not failures else "FAIL_EXACT_REPLICATION",
            "checks": checks, "failure_count": len(failures), "failures": failures,
            "physical_measurement_replication": False, "positive_optimizer_accepted": False}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024**2), b""): digest.update(block)
    return digest.hexdigest()


def encoded(value):
    if isinstance(value, F): return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict): return {str(k): encoded(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)): return [encoded(x) for x in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--primary", type=Path, required=True); parser.add_argument("--primary-sha256", required=True)
    parser.add_argument("--output", type=Path, required=True); args = parser.parse_args()
    if len(args.primary_sha256) != 64 or any(c not in "0123456789abcdef" for c in args.primary_sha256): raise ValueError("Frozen SHA256 required")
    if args.primary.stat().st_size > OUTPUT_CAP or sha256(args.primary) != args.primary_sha256: raise ValueError("Primary size/hash mismatch")
    args.output.mkdir(parents=True, exist_ok=False); cpu, wall = time.process_time(), time.perf_counter()
    own = derive()  # Full scientific construction precedes decoding primary scientific fields.
    with gzip.open(args.primary, "rb") as stream: payload = stream.read(INFLATED_CAP+1)
    if len(payload) > INFLATED_CAP: raise ValueError("Primary inflation bound exceeded")
    primary = json.loads(payload)
    report = compare(primary, own)
    own.update({"source_sha256": sha256(__file__), "primary_sha256": args.primary_sha256})
    raw = (json.dumps(encoded(own), separators=(",", ":"), allow_nan=False)+"\n").encode()
    if len(raw) > OUTPUT_CAP-65536: raise RuntimeError("Independent uncompressed output cap exceeded")
    with (args.output/"independent.json.gz").open("xb") as output, gzip.GzipFile(fileobj=output, mode="wb", mtime=0, compresslevel=3) as stream: stream.write(raw)
    report.update({"independent_outcome": own["status"], "CPU_seconds": time.process_time()-cpu,
                   "wall_seconds": time.perf_counter()-wall, "primary_sha256": args.primary_sha256,
                   "independent_source_sha256": sha256(__file__)})
    text = json.dumps(report, indent=2, allow_nan=False)+"\n"
    if len(text.encode()) > 65536: raise RuntimeError("Comparison report cap exceeded")
    (args.output/"comparison.json").write_text(text)
    if sum(p.stat().st_size for p in args.output.iterdir() if p.is_file()) > OUTPUT_CAP: raise RuntimeError("Total output cap exceeded")
    print(json.dumps(report, allow_nan=False))
    if report["failure_count"]: raise ArithmeticError("Primary and independent derivations disagree; preserve failure")


if __name__ == "__main__": main()
