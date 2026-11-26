"""Independent exact polynomial check of the declared P145 diagnostic.

No NumPy, source optimizer, random graph, optimum oracle, or QPU is used.
This is a designed counterexample to an insufficient acceptance criterion.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
import json
from math import comb, factorial
from pathlib import Path


PROFILES = {"B": (0, 0, 0), "D": (0, 1, 2),
            "P12": (0, 0, 1), "P13": (0, 1, 0), "P23": (0, 1, 1)}


def occupations(total=3, modes=6):
    if modes == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in occupations(total - first, modes - 1):
                yield (first,) + rest


def graph_edges():
    edges = []
    for start, weight in ((0, 1), (3, 1), (6, 3), (9, 3)):
        edges.extend((a, b, weight) for a, b in combinations(range(start, start + 3), 2))
    edges.extend((a, 6, 3) for a in range(3, 6))
    return edges


def cut(selected):
    selected = set(selected)
    return sum(w for a, b, w in graph_edges() if (a in selected) != (b in selected))


def coefficient(occupation, profile):
    """Coefficient of p**r*(1-p)**(3-r), with ALL Fock divisors.

    All amplitudes in a fixed outside-count sector share the same powers of
    sqrt(p),sqrt(1-p),-i and sqrt(3). Remaining phases are powers of omega.
    Coherent sums are grouped by the internal-color tuple at the output slots.
    """
    rows = [i for i, count in enumerate(occupation) for _ in range(count)]
    buckets = defaultdict(lambda: [0, 0, 0])
    for sigma in permutations(range(3)):
        if any(row < 3 and sigma[j] != row for j, row in enumerate(rows)):
            continue
        exponent = sum((row - 3) * sigma[j] for j, row in enumerate(rows) if row >= 3) % 3
        colors = tuple(profile[sigma[j]] for j in range(3))
        buckets[colors][exponent] += 1
    numerator = 0
    for n0, n1, n2 in buckets.values():
        a, b = n0 - n2, n1 - n2
        numerator += a * a - a * b + b * b
    divisor = 3 ** sum(occupation[3:])
    for n in occupation:
        divisor *= factorial(n)
    return Fraction(numerator, divisor)


def monomial(bernstein):
    result = [Fraction(0) for _ in range(4)]
    for r, value in enumerate(bernstein):
        for j in range(4 - r):
            result[r + j] += value * (-1) ** j * comb(3 - r, j)
    return result


def frac(value):
    value = Fraction(value)
    return f"{value.numerator}/{value.denominator}"


def compute(evidence):
    evidence['phase'] = 'graph_and_one_swap_check'
    current = {0, 1, 2, 6, 7, 8}
    current_cost = cut(current)
    evidence['current'] = sorted(current)
    evidence['current_cost'] = current_cost
    swaps = evidence['swaps']
    for a, b in product(sorted(current), sorted(set(range(12)) - current)):
        target = (current - {a}) | {b}
        swaps.append({"remove": a, "add": b, "delta": cut(target) - current_cost})
    assert current_cost == 9 and len(swaps) == 36 and min(row["delta"] for row in swaps) == 1
    evidence['phase'] = 'residual_candidate_check'
    candidates = evidence['candidates']
    gains = {}
    for support in combinations(range(6), 3):
        value = cut(set(support) | {6, 7, 8})
        r = sum(i >= 3 for i in support)
        delta = value - current_cost
        gains[support] = max(0, -delta)
        candidates.append({"support": support, "replacements": r, "cut": value, "gain": gains[support]})
        assert delta == 3 * r - 2 * r * r
    all_occ = list(occupations())
    assert len(all_occ) == 56 and len(candidates) == 20
    records = evidence['records']
    polys = {}
    expected = {"B": [0, 0, 2, 1], "D": [0, 0, 4, -2],
                "P12": [0, 0, Fraction(10, 3), Fraction(-7, 3)],
                "P13": [0, 0, Fraction(10, 3), Fraction(-7, 3)],
                "P23": [0, 0, Fraction(10, 3), Fraction(-7, 3)]}
    for name, profile in PROFILES.items():
        evidence['phase'] = 'profile_' + name
        normalization = [Fraction(0) for _ in range(4)]
        utility = [Fraction(0) for _ in range(4)]
        for n in all_occ:
            r = sum(n[3:])
            a = coefficient(n, profile)
            support = tuple(i for i, count in enumerate(n) if count)
            gain = gains[support] if max(n) <= 1 else 0
            normalization[r] += a
            utility[r] += a * gain
            records.append({"profile": name, "occupation": n, "outside_count": r,
                            "probability_basis_coefficient": frac(a), "raw_gain": gain})
        evidence['profile_checks'].append({'profile': name,
            'normalization_basis': [frac(x) for x in normalization],
            'utility_polynomial': [frac(x) for x in monomial(utility)]})
        assert normalization == [Fraction(comb(3, r)) for r in range(4)]
        assert monomial(normalization) == [1, 0, 0, 0]
        polys[name] = monomial(utility)
        assert polys[name] == expected[name]
    i3 = [polys['B'][j] - sum(polys[name][j] for name in ('P12', 'P13', 'P23'))
          + 2 * polys['D'][j] for j in range(4)]
    evidence['phase'] = 'envelope_check'
    assert i3 == [0, 0, 0, 4]
    maxima = {}
    for name, poly in polys.items():
        assert poly[:2] == [0, 0]
        points = {Fraction(0), Fraction(1)}
        if poly[3]:
            critical = -2 * poly[2] / (3 * poly[3])
            if 0 <= critical <= 1:
                points.add(critical)
        value, point = max((sum(c * p ** j for j, c in enumerate(poly)), p) for p in points)
        maxima[name] = {'gain': frac(value), 'p': frac(point)}
    evidence['maxima'] = maxima
    assert maxima['B'] == {'gain': '3/1', 'p': '1/1'}
    assert maxima['D'] == {'gain': '2/1', 'p': '1/1'}
    assert all(maxima[name] == {'gain': '4000/3969', 'p': '20/21'} for name in ('P12', 'P13', 'P23'))
    assert Fraction(4000, 3969) < 2 < 3 < gains[(3, 4, 5)] == 9
    # The common classical move needs only current/candidate scoring, not C*.
    summary = {"status": "FINITE_EXACT_POLYNOMIAL_CHECK_PASS", "current_cut": current_cost,
               "one_swap_neighbors": len(swaps), "minimum_one_swap_delta": 1,
               "full_fock_bins": len(all_occ), "profile_count": len(PROFILES),
               "raw_records": len(records), "polynomial_basis": "monomial coefficients p^0..p^3",
               "gain_polynomials": {name: [frac(x) for x in poly] for name, poly in polys.items()},
               "I3_polynomial": [frac(x) for x in i3],
               "restricted_family_maxima": maxima,
               "classical_whole_block_move_gain": 9, "optimizer_advantage": False,
               "scope": "Constructed mechanism diagnostic only; no novelty, learned policy, random-graph, timing or hardware claim"}
    return summary


def execute(output):
    output.mkdir(parents=True, exist_ok=False)
    evidence = {'records': [], 'swaps': [], 'candidates': [], 'profile_checks': []}
    failure = None
    summary = {'status': 'NOT_COMPLETED'}
    try:
        if not __debug__:
            raise RuntimeError('Optimized Python is refused: exact checks require assertions')
        summary = compute(evidence)
        print(summary['status'])
    except Exception as exc:
        failure = {'exception_type': type(exc).__name__, 'message': str(exc),
                   'phase': evidence.get('phase'), 'records_preserved': len(evidence['records'])}
        summary = {'status': 'FAILED', 'failure': failure}
        raise
    finally:
        # Preserve available observations even when an assertion fails.
        (output / 'records.json').write_text(json.dumps(evidence.pop('records'), indent=2) + '\n')
        (output / 'graph_checks.json').write_text(json.dumps({'edges': graph_edges(), **evidence}, indent=2) + '\n')
        (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        (output / 'failure.json').write_text(json.dumps(failure, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    execute(parser.parse_args().output)
