"""Independent exact F6 source polynomial, using three paired quadratics.

Pure standard library. No production sampler, creation-polynomial recurrence,
native backend, scientific module, RNG or data is imported here.
"""
from __future__ import annotations

import itertools
import math

ROOT_POWERS = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))


def product(left, right):
    # xi^2=xi-1 for xi=exp(pi*imaginary_unit/3).
    a, b = left
    c, d = right
    return a*c-b*d, a*d+b*c+b*d


def modulus_squared(value):
    a, b = value
    return a*a+a*b+b*b


def all_occupations():
    # Independent multiset enumerator, not the production composition recursion.
    return tuple(sorted(tuple(labels.count(i) for i in range(6))
                        for labels in itertools.combinations_with_replacement(range(6), 6)))


def quadratic_terms(j):
    """L_j L_(j+3)=E_j^2-O_j^2: six even and six odd monomials."""
    if j not in (0, 1, 2):
        raise ValueError("Three fixed Fourier column pairs only")
    answer = []
    for variables, sign in (((0, 2, 4), 1), ((1, 3, 5), -1)):
        for first, second in itertools.combinations_with_replacement(variables, 2):
            exponent = [0]*6
            exponent[first] += 1
            exponent[second] += 1
            multiplier = sign*(1 if first == second else 2)
            root = ROOT_POWERS[(j*(first+second)) % 6]
            answer.append((tuple(exponent), (multiplier*root[0], multiplier*root[1])))
    if len(answer) != 12:
        raise ArithmeticError("Each paired quadratic must have exactly12 terms")
    return tuple(answer)


def exact_source_table():
    coefficients = {n: (0, 0) for n in all_occupations()}
    factors = tuple(quadratic_terms(j) for j in range(3))
    visited = 0
    # Exactly12^3 products, with ordered physical columns paired j,j+3.
    for first, second, third in itertools.product(*factors):
        visited += 1
        n = tuple(a+b+c for a, b, c in zip(first[0], second[0], third[0]))
        value = product(product(first[1], second[1]), third[1])
        old = coefficients[n]
        coefficients[n] = old[0]+value[0], old[1]+value[1]
    rows = []
    for occupation, coefficient in coefficients.items():
        weight = math.prod(math.factorial(x) for x in occupation)*modulus_squared(coefficient)
        rows.append({"occupation": occupation, "coefficient": coefficient, "weight": weight})
    normalization = sum(row["weight"] for row in rows)
    return {"method": "three_Ej_squared_minus_Oj_squared_quadratics_no_production_DP",
            "denominator": 6**6, "products_visited": visited, "all_occupations": len(rows),
            "normalization_numerator": normalization,
            "checks": {"products_1728": visited == 1728, "rows_462": len(rows) == 462,
                       "exact_normalization": normalization == 6**6},
            "observed_nonzero_support": sum(row["weight"] != 0 for row in rows),
            "quadratics": factors, "rows": rows}


def comparison(independent, reference):
    """Exact all-row comparison; return every discrepancy before caller asserts."""
    primary = {tuple(row["occupation"]): row for row in reference["rows"]}
    independent_keys = {tuple(row["occupation"]) for row in independent["rows"]}
    discrepancies = []
    for row in independent["rows"]:
        n = tuple(row["occupation"])
        other = primary.get(n)
        if other is None or tuple(other["coefficient"]) != tuple(row["coefficient"]) or other["weight"] != row["weight"]:
            discrepancies.append({"occupation": n, "independent": row, "primary": other})
    extras = sorted(set(primary)-independent_keys)
    return {"all_rows_equal": not discrepancies and not extras and reference["denominator"] == independent["denominator"],
            "discrepancies": discrepancies, "extra_primary_occupations": extras,
            "primary_occupations": len(primary), "independent_occupations": len(independent_keys)}
