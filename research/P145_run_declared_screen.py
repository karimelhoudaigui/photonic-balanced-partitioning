"""Bounded prospective P145 mechanism screen; never an advantage experiment."""
from __future__ import annotations

import argparse
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import random
import traceback


def cut(edges, selected):
    return sum(w for i, j, w in edges if (i in selected) != (j in selected))


def descend(edges, marks, budget=20000):
    current = set(marks[:12])
    value = cut(edges, current)
    queries, trace = 1, []
    while True:
        inside = [i for i in marks if i in current]
        outside = [j for j in marks if j not in current]
        if queries + len(inside) * len(outside) > budget:
            return current, value, queries, trace, None
        neighbors = []
        for i, j in product(inside, outside):
            target = (current - {i}) | {j}
            score = cut(edges, target)
            queries += 1
            neighbors.append({'remove': i, 'add': j, 'cut': score, 'delta': score - value})
        # Enumeration follows transported public ranks; first tie is fixed.
        best = min(neighbors, key=lambda row: row['cut'])
        trace.append({'current': sorted(current), 'cut': value, 'queries': queries, 'neighbors': neighbors})
        if best['delta'] >= 0:
            return current, value, queries, trace, neighbors
        current = (current - {best['remove']}) | {best['add']}
        value = best['cut']


def blocks(current, marks, neighbors):
    public = [i for i in marks if i in current][:3] + [i for i in marks if i not in current][:3]
    ranks = {v: i for i, v in enumerate(marks)}
    used_inside, used_outside = set(), set()
    for row in sorted(neighbors, key=lambda r: (r['delta'], ranks[r['remove']], ranks[r['add']])):
        i, j = row['remove'], row['add']
        if i in used_inside or j in used_outside:
            continue
        used_inside.add(i)
        used_outside.add(j)
        if len(used_inside) == 3:
            break
    assert len(used_inside) == len(used_outside) == 3
    near = [i for i in marks if i in used_inside] + [i for i in marks if i in used_outside]
    return [('public', public), ('paid_near_barrier', near)]


def features(edges, current, block):
    weights = {(min(i, j), max(i, j)): w for i, j, w in edges}
    def weight(i, j):
        return weights.get((min(i, j), max(i, j)), 0) if i != j else 0
    active = set(block)
    a = [[weight(i, j) for j in block] for i in block]
    h = [sum(weight(i, j) * (1 - 2 * (j in current)) for j in range(24) if j not in active) for i in block]
    return a, h


def laws_json(laws):
    return {arm: [[n, probability] for n, probability in law.items()]
            for arm, law in laws.items()}


def execute(output):
    output.mkdir(parents=True, exist_ok=False)
    records, graphs = [], []
    failure = None
    summary = {'status': 'NOT_COMPLETED', 'optimizer_advantage': False}
    try:
        if not __debug__:
            raise RuntimeError('Optimized Python is refused')
        import networkx as nx
        if nx.__version__ != '3.6.1':
            raise RuntimeError('Frozen NetworkX version differs')
        spec = importlib.util.spec_from_file_location('p145_engine', Path(__file__).with_name('P145_collective_lns_probe.py'))
        engine = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(engine)
        for graph_index, name in enumerate(('ER', 'RR'), 1):
            topology_seed = 1451000 + graph_index
            g = (nx.gnp_random_graph(24, .25, seed=topology_seed, backend='networkx') if name == 'ER'
                 else nx.random_regular_graph(4, 24, seed=topology_seed, backend='networkx'))
            weights = random.Random(1452000 + graph_index)
            edges = [(i, j, weights.randint(1, 5)) for i, j in sorted((min(i, j), max(i, j)) for i, j in g.edges)]
            marks = list(range(24))
            random.Random(1453000 + graph_index).shuffle(marks)
            current, value, queries, trace, neighbors = descend(edges, marks)
            graph_row = {'name': name, 'edges': edges, 'marks': marks, 'current': sorted(current),
                         'cut': value, 'descent_queries': queries, 'descent_trace': trace,
                         'one_swap_minimum_certified': neighbors is not None}
            graphs.append(graph_row)
            if neighbors is None:
                graph_row['status'] = 'INCONCLUSIVE_DESCENT_BUDGET'
                continue
            for rule, block in blocks(current, marks, neighbors):
                source = (0, 1, 2)
                retained = current - set(block[:3])
                a, h = features(edges, current, block)
                candidates, gains = [], {}
                for support in combinations(range(6), 3):
                    target = retained | {block[i] for i in support}
                    score = cut(edges, target)
                    delta_formula = sum((sum(a[i]) + h[i]) for i in support)
                    delta_formula -= 2 * sum(a[i][j] for i, j in combinations(support, 2))
                    original_formula = sum((sum(a[i]) + h[i]) for i in source)
                    original_formula -= 2 * sum(a[i][j] for i, j in combinations(source, 2))
                    candidates.append({'support': support, 'cut': score, 'gain': max(0, value - score)})
                    assert score - value == delta_formula - original_formula
                    gains[support] = max(0, value - score)
                contexts = []
                for grid_index, (alpha, beta, t) in enumerate(product((-1, 1), (0, 1), (0., .5, 1., 2., 4.))):
                    u = engine.unitary_from_features(a, h, alpha, beta, t)
                    diagnostic = engine.density_diagnostics(u, source, value)
                    for eta in (1., .8):
                        result = engine.same_circuit_scores(u, source, gains, eta)
                        mirror = engine.feasible_mirror_kernel(result['laws']['B'])
                        mirror_score = sum(mirror[support] * gain for support, gain in gains.items())
                        assert abs(mirror_score - result['scores']['B']) < 1e-9
                        if eta == 1.:
                            contexts.append(result)
                        records.append({'graph': name, 'block_rule': rule, 'block': block, 'A': a, 'h': h,
                            'current_cut': value, 'candidate_costs_credited_to_all_controls': candidates,
                            'grid_index': grid_index, 'alpha': alpha, 'beta': beta, 't': t, 'eta': eta,
                            'scores': result['scores'], 'hazards': result['hazards'],
                            'same_circuit_I3': result['same_circuit_I3'],
                            'I3_numeric_sign': result['I3_numeric_sign'], 'full_laws': laws_json(result['laws']),
                            'U_complex_pairs': [[[z.real, z.imag] for z in row] for row in u],
                            'mirror_score': mirror_score, 'P33_diagnostic': diagnostic,
                            'P33_diagnostic_applies_to': 'LOSSLESS_SAME_U_ONLY_NOT_A_DEVICE_CERTIFICATE'})
                envelope = engine.validation_envelopes(contexts)
                b_index = envelope['B']['grid_index']
                selected = contexts[b_index]
                best_control = max(v['score'] for arm, v in envelope.items() if arm != 'B')
                graph_row.setdefault('block_summaries', []).append({'rule': rule, 'block': block,
                    'improving_candidates': sum(gain > 0 for gain in gains.values()),
                    'classical_exact_block_gain': max(gains.values()), 'validation_cut_queries': 20,
                    'envelope_eta1': envelope, 'selected_same_circuit_I3': selected['same_circuit_I3'],
                    'strict_floating_group_survivor': envelope['B']['score'] > best_control + 1e-9,
                    'exact_law_mirror_matches_B': True, 'optimizer_advantage': False})
        completed = sum(len(g.get('block_summaries', [])) for g in graphs)
        summary = {'status': 'FINITE_FLOAT_SCREEN_COMPLETED' if completed == 4 else 'INCONCLUSIVE_DESCENT_BUDGET',
                   'graphs': graphs, 'contexts': len(records), 'modeled_optical_trials': 0,
                   'all_positive_I3_contexts': sum(r['same_circuit_I3'] > 1e-9 for r in records),
                   'optimizer_advantage': False,
                   'semantics': 'Finite exhaustive floating model screen, not interval-certified signs or sampled training',
                   'scope': 'All20 residual costs credited classically; exact-law mirror preserves the same proposal utility'}
    except Exception as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc), 'traceback': traceback.format_exc()}
        summary = {'status': 'FAILED', 'completed_contexts': len(records), 'optimizer_advantage': False}
        raise
    finally:
        (output / 'records.json').write_text(json.dumps(records, separators=(',', ':'), allow_nan=False) + '\n')
        (output / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
        (output / 'failure.json').write_text(json.dumps(failure, indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    execute(p.parse_args().output)
