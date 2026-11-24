"""Exact two-photon L1 discriminator; no optimization, sampling or device call."""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations
import json
from pathlib import Path

EDGES = tuple(combinations(range(4), 2))
MU = (Q(0), Q(1), Q(3))


def frame_data():
    walsh = [[Q(x, 2) for x in row] for row in
             ((1, 1, 1, 1), (1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))]
    householder = [[Q(int(i == j)) - (Q(2, 3) if i < 3 and j < 3 else Q(0))
                    for j in range(4)] for i in range(4)]
    return {"walsh": walsh, "householder3": householder}


def outcomes():
    result = []
    for i, j in combinations_with_replacement(range(4), 2):
        n = [0] * 4
        n[i] += 1
        n[j] += 1
        result.append(tuple(n))
    return result


def full_laws(unitary):
    assert all(sum(unitary[i][a] * unitary[i][b] for i in range(4)) == int(a == b)
               for a in range(4) for b in range(4))
    u, v = [r[0] for r in unitary], [r[1] for r in unitary]
    bosonic, distinguishable = [], []
    for n in outcomes():
        i, j = [r for r, count in enumerate(n) for _ in range(count)]
        if i == j:
            direct = u[i] ** 2 * v[i] ** 2
            bosonic.append(2 * direct)
            distinguishable.append(direct)
        else:
            bosonic.append((u[i] * v[j] + u[j] * v[i]) ** 2)
            distinguishable.append(u[i] ** 2 * v[j] ** 2 + u[j] ** 2 * v[i] ** 2)
    assert sum(bosonic) == sum(distinguishable) == 1
    assert all(p >= 0 for p in bosonic + distinguishable)
    z = [a * b for a, b in zip(u, v)]
    assert sum(z) == 0
    return bosonic, distinguishable, z


def adjacency(mask):
    a = [[Q(0) for _ in range(4)] for _ in range(4)]
    for bit, (i, j) in enumerate(EDGES):
        a[i][j] = a[j][i] = Q((mask >> bit) & 1)
    return a


def cost(a, n, mu):
    return sum(a[i][j] * abs(n[i] - n[j]) for i, j in EDGES) + mu * sum(x * (x - 1) // 2 for x in n)


def determinant(a):
    n = len(a)
    total = Q(0)
    for sigma in permutations(range(n)):
        parity = sum(sigma[i] > sigma[j] for i, j in combinations(range(n), 2))
        product = Q(1)
        for i, j in enumerate(sigma):
            product *= a[i][j]
        total += (-1) ** parity * product
    return total


def negative_on_zero_sum(a):
    # Restrict -A to the rational basis e_i-e_3, then all principal minors.
    reduced = [[-(a[i][j] - a[i][3] - a[3][j] + a[3][3]) for j in range(3)] for i in range(3)]
    minors = []
    for size in (1, 2, 3):
        for subset in combinations(range(3), size):
            minors.append(determinant([[reduced[i][j] for j in subset] for i in subset]))
    return all(value >= 0 for value in minors), minors


def complete_multipartite(a):
    # Nonadjacency plus equality is an equivalence relation iff no induced
    # three-vertex set has exactly one edge.
    return not any(sum(a[i][j] for i, j in combinations(triple, 2)) == 1
                   for triple in combinations(range(4), 3))


def compare(a, mu, pb, pd, z):
    costs = [cost(a, n, mu) for n in outcomes()]
    eb, ed = sum(p * f for p, f in zip(pb, costs)), sum(p * f for p, f in zip(pd, costs))
    predicted = mu * sum(x * x for x in z) - 2 * sum(z[i] * a[i][j] * z[j] for i in range(4) for j in range(4))
    assert eb - ed == predicted
    return {"bosonic_mean": str(eb), "distinguishable_mean": str(ed),
            "difference": str(eb - ed), "predicted_difference": str(predicted),
            "costs_in_complete_fock_order": list(map(str, costs))}


def run():
    states = outcomes()
    frames = {}
    for name, unitary in frame_data().items():
        pb, pd, z = full_laws(unitary)
        frames[name] = {"unitary": [[str(x) for x in row] for row in unitary],
                        "z": list(map(str, z)), "bosonic": list(map(str, pb)),
                        "distinguishable": list(map(str, pd))}
    rows, classes = [], []
    for graph_mask in range(64):
        a = adjacency(graph_mask)
        cnd, minors = negative_on_zero_sum(a)
        multipartite = complete_multipartite(a)
        assert cnd == multipartite
        classes.append({"graph_mask": graph_mask, "adjacency_cnd": cnd,
                        "complete_multipartite": multipartite, "principal_minors": list(map(str, minors))})
        for frame_name, unitary in frame_data().items():
            pb, pd, z = full_laws(unitary)
            for mu in MU:
                row = compare(a, mu, pb, pd, z)
                rows.append({"graph_mask": graph_mask, "frame": frame_name, "mu": str(mu), **row})
                if mu == 0 and cnd:
                    assert Q(row["difference"]) >= 0
    a = [[Q(0) for _ in range(4)] for _ in range(4)]
    for i, j, weight in ((0, 1, Q(1)), (2, 3, Q(1)), (1, 2, Q(1, 4))):
        a[i][j] = a[j][i] = weight
    pb, pd, z = full_laws(frame_data()["walsh"])
    witness = compare(a, Q(1), pb, pd, z)
    assert Q(witness["difference"]) == Q(-3, 16)
    cf_costs = [cost(a, n, Q(1)) for n in states if max(n) <= 1]
    collision_costs = [cost(a, n, Q(1)) for n in states if max(n) > 1]
    assert cost(a, (1, 1, 0, 0), Q(1)) == Q(1, 4)
    assert min(collision_costs) > min(cf_costs) == Q(1, 4)
    witness.update({"epsilon": "1/4", "mu": "1", "known_feasible_upper_bound": "1/4",
                    "minimum_cf_cost_evaluation_only": str(min(cf_costs)),
                    "minimum_collision_cost": str(min(collision_costs))})
    assert len(rows) == 384 and len(classes) == 64 and len(states) == 10
    return {"result": "EXACT_FINITE_ASSERTIONS_PASS", "coefficient_domain": "Fraction(Q)",
            "states": states, "edge_bit_order": EDGES, "frames": frames,
            "rows": rows, "graph_classes": classes, "connected_witness": witness,
            "domain": {"graphs": 64, "frames": 2, "mu_values": ["0", "1", "3"], "rows": 384},
            "claims_not_made": ["optimization advantage", "independent replication",
                                "new optical distribution", "general-k theorem", "novelty", "hardware result"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Fresh JSON file path inside runner output")
    args = parser.parse_args()
    result = run()
    with args.output.open("x") as stream:
        json.dump(result, stream, separators=(",", ":"))
        stream.write("\n")
    print(json.dumps({"result": result["result"], "rows": len(result["rows"]),
                      "connected_difference": result["connected_witness"]["difference"]}))


if __name__ == "__main__":
    main()
