"""Independent finite audit of fixed-input, fixed-order optical penalty washout.

No project simulator or original competitor program is imported. State evolution
uses creation-operator recursion, independently of the project's permanent code.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
from pathlib import Path

import numpy as np
import sympy as sp


SEED = 20261121
LAMBDAS = (16.0, 64.0, 256.0, 1024.0, 4096.0, 16384.0)


def pair_order(m, name):
    pairs = list(itertools.combinations(range(m), 2))
    if name == "reverse":
        pairs.reverse()
    elif name == "archive_runtime":
        pairs = list(set(pairs))
    return pairs


def build(weights, lam, repeats, variant, order="lex", limit=False):
    m = len(weights)
    q = (np.diag(weights.sum(1) - (m - 1) * lam)
         + lam * (np.ones((m, m)) - np.eye(m)) - weights)
    normalized = (q - q.min()) / (q.max() - q.min())
    unitary = np.eye(m, dtype=complex)
    for _ in range(repeats):
        for i, j in pair_order(m, order):
            a = 1.0 if limit else normalized[i, j]
            # Stable equivalent of the archive's acos(sqrt(1-a/R^2))/2.
            beta = variant * 0.5 * math.asin(math.sqrt(a) / repeats)
            c, s = math.cos(beta / 2), 1j * math.sin(beta / 2)
            old = unitary[[i, j]].copy()
            unitary[i] = c * old[0] + s * old[1]
            unitary[j] = s * old[0] + c * old[1]
    denominator = m * lam - weights.sum(1).min()
    upper_weights = weights[np.triu_indices(m, 1)]
    expected = 1 - upper_weights / denominator
    if repeats == 1:
        bound = variant / 4 * sum(math.asin(math.sqrt(w / denominator))
                                  for w in upper_weights)
    else:
        lipschitz = 1 / (4 * repeats * math.sqrt(0.5)
                          * math.sqrt(1 - 1 / repeats**2))
        bound = variant * repeats * lipschitz * sum(upper_weights) / (2 * denominator)
    error = np.max(abs(normalized[np.triu_indices(m, 1)] - expected))
    return unitary, float(bound), float(error)


def fock_state(unitary, photons):
    """Apply distinct occupied input creation operators, retaining collisions."""
    m = len(unitary)
    amplitudes = {(0,) * m: 1.0 + 0j}
    for a in range(photons):
        updated = {}
        for occupation, amplitude in amplitudes.items():
            for i in range(m):
                new = list(occupation)
                new[i] += 1
                new = tuple(new)
                updated[new] = (updated.get(new, 0j)
                                + amplitude * unitary[i, a]
                                * math.sqrt(occupation[i] + 1))
        amplitudes = updated
    keys = sorted(amplitudes)
    return np.array(keys), np.array([amplitudes[t] for t in keys])


def exact_matching_identity():
    """A real degeneracy of an admissible anchor, using exact SymPy arithmetic."""
    beta = sp.pi / 2  # corrected-physics R=1 limit
    unitary = sp.eye(4)
    matching = ((0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2))
    generators = []
    for layer in (matching[:2], matching[2:4], matching[4:]):
        generator = sp.zeros(4)
        for i, j in layer:
            generator[i, j] = generator[j, i] = 1
        generators.append(generator)
    assert all(matrix**2 == sp.eye(4) for matrix in generators)
    assert all(a*b == b*a for a in generators for b in generators)
    assert sum(generators, sp.zeros(4)) == sp.ones(4) - sp.eye(4)
    for i, j in matching:
        gate = sp.eye(4)
        gate[i, i] = gate[j, j] = sp.cos(beta / 2)
        gate[i, j] = gate[j, i] = sp.I * sp.sin(beta / 2)
        unitary = gate * unitary
    expected = sp.exp(-sp.I * beta / 2) * (
        sp.eye(4) + (sp.exp(2 * sp.I * beta) - 1) * sp.ones(4) / 4)
    identity = all(sp.simplify(sp.expand_complex(x)) == 0 for x in unitary - expected)
    commutators = []
    for permutation in ((1, 0, 2, 3), (0, 2, 1, 3), (0, 1, 3, 2)):
        matrix = sp.zeros(4)
        for i, j in enumerate(permutation):
            matrix[i, j] = 1
        commutators.append(all(sp.simplify(sp.expand_complex(x)) == 0
                               for x in expected * matrix - matrix * expected))
    assert identity and all(commutators)
    return {"pair_order": matching, "beta": "pi/2", "identity_exact": identity,
            "commuting_matching_generators_exact": True,
            "generator_sum_J_minus_I_exact": True,
            "adjacent_transposition_commutators_exact": commutators}


def analytic_controls():
    states, amplitudes = fock_state(np.eye(4), 4)
    identity_error = max(abs(amplitudes - np.all(states == 1, axis=1)))
    gate = np.array([[1, 1j], [1j, 1]], dtype=complex) / math.sqrt(2)
    states, amplitudes = fock_state(gate, 2)
    expected = np.array([0.5 if max(s) == 2 else 0.0 for s in states])
    hom_error = float(max(abs(abs(amplitudes)**2 - expected)))
    assert identity_error < 1e-12 and hom_error < 1e-12
    return {"identity_all_ones_amplitude_error": float(identity_error),
            "two_photon_HOM_probability_error": hom_error,
            "eigenvector_counterexample": {
                "formula": "V(t)=rotation(t), U(t)=V(t)diag(exp(i/t),exp(-i/t))V(t)^T",
                "distance_to_identity": "2*sin(1/(2*t)) <= 1/t for t>=1",
                "eigenvector_subsequences": "t=2*pi*n and t=2*pi*n+pi/4"}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    unitary_rows, state_rows, gap_rows, graphs = [], [], [], []
    maximum = dict(normalization=0.0, normalized_qubo=0.0, unitary_bound=0.0,
                   fock_lift=0.0, tv_trace=0.0)
    for m in (4, 6, 8):
        cycle = np.zeros((m, m))
        for i in range(m):
            cycle[i, (i + 1) % m] = cycle[(i + 1) % m, i] = 1.0 + i % 2
        random_graph = np.zeros((m, m))
        for i, j in pair_order(m, "lex"):
            if rng.random() < 0.5:
                random_graph[i, j] = random_graph[j, i] = rng.uniform(0.1, 2.0)
        random_graph[0, 1] = random_graph[1, 0] = 0.0
        for graph, weights in (("alternating_cycle", cycle),
                               ("random_sparse", random_graph), ("empty", np.zeros((m, m)))):
            graphs.append(dict(m=m, graph=graph, adjacency=weights.tolist()))
            for order in ("lex", "reverse", "archive_runtime"):
                for repeats in (1, 2, 10):
                    for variant in (1, 2):
                        reference, _, _ = build(weights, 16.0, repeats, variant, order, True)
                        for lam in LAMBDAS:
                            unitary, bound, q_error = build(weights, lam, repeats, variant, order)
                            distance = float(np.linalg.norm(unitary - reference, 2))
                            maximum["unitary_bound"] = max(maximum["unitary_bound"], distance - bound)
                            maximum["normalized_qubo"] = max(maximum["normalized_qubo"], q_error)
                            row = dict(m=m, graph=graph, order=order, repeats=repeats,
                                       variant=variant, lam=lam, distance=distance, bound=bound,
                                       normalized_qubo_error=q_error)
                            unitary_rows.append(row)
                            if m == 4 and graph != "empty" and order == "lex" and lam in (16.0, 256.0, 16384.0):
                                states, a = fock_state(unitary, m)
                                _, b = fock_state(reference, m)
                                norm_error = max(abs(np.vdot(a, a).real - 1), abs(np.vdot(b, b).real - 1))
                                trace = math.sqrt(max(0.0, 1 - min(1.0, abs(np.vdot(a, b))**2)))
                                tv = 0.5 * float(np.sum(abs(abs(a)**2 - abs(b)**2)))
                                lift = float(np.linalg.norm(a - b))
                                maximum["normalization"] = max(maximum["normalization"], norm_error)
                                maximum["fock_lift"] = max(maximum["fock_lift"], lift - m * distance)
                                maximum["tv_trace"] = max(maximum["tv_trace"], tv - trace)
                                state_rows.append(dict(**row, states=states.tolist(),
                                    amplitudes=[[z.real, z.imag] for z in a],
                                    reference_amplitudes=[[z.real, z.imag] for z in b],
                                    normalization_error=float(norm_error), vector_distance=lift,
                                    trace_distance=trace, tv=tv))
        for order in ("lex", "archive_runtime"):
            for repeats in (1, 2, 10):
                for variant in (1, 2):
                    unitary, _, _ = build(cycle, 16.0, repeats, variant, order, True)
                    states, amplitude = fock_state(unitary, m)
                    probability = abs(amplitude)**2
                    marginal = probability @ (states > 0)
                    ranked = np.sort(marginal)[::-1]
                    sorted_p = np.sort(probability)[::-1]
                    norm_error = float(abs(probability.sum() - 1))
                    maximum["normalization"] = max(maximum["normalization"], norm_error)
                    gap_rows.append(dict(m=m, repeats=repeats, variant=variant, order=order,
                        marginal=marginal.tolist(), kth_gap=float(ranked[m // 2 - 1] - ranked[m // 2]),
                        mode_gap=float(sorted_p[0] - sorted_p[1]),
                        mode=states[np.argmax(probability)].tolist(), normalization_error=norm_error))
    exact = exact_matching_identity()
    controls = analytic_controls()
    orders = {str(m): {name: pair_order(m, name) for name in ("lex", "reverse", "archive_runtime")}
              for m in (4, 6, 8)}
    summary = dict(seed=SEED, generator="numpy.default_rng/PCG64",
        versions={"python": platform.python_version(), "numpy": np.__version__, "sympy": sp.__version__},
        unitary_cases=len(unitary_rows), full_fock_cases=len(state_rows), limit_gap_cases=len(gap_rows),
        tolerance=1e-10, max_positive_violations=maximum, exact_matching_counterexample=exact,
        analytic_controls=controls,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    raw = dict(summary=summary, graphs=graphs, pair_orders=orders,
               unitary_rows=unitary_rows, full_fock_rows=state_rows, limit_gap_rows=gap_rows)
    (args.output / "raw.json").write_text(json.dumps(raw, indent=2) + "\n")
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    assert len(unitary_rows) == 972 and len(state_rows) == 36 and len(gap_rows) == 36
    assert max(maximum.values()) < 1e-10


if __name__ == "__main__":
    main()
