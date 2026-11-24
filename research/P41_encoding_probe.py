"""Exact finite falsification of grouped-output domination; no optimizer/QPU.

Run under the computation-audit bounded runner, with its fresh output directory.
All Gaussian-rational matrices, Fock sectors and transversal outcomes retained.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import importlib.metadata
from itertools import combinations, permutations, product
import json
import math
from pathlib import Path
import random
import time

ZERO = (F(0), F(0))
ONE = (F(1), F(0))


def g(value):
    return value if isinstance(value, tuple) else (F(value), F(0))


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def mul(a, b):
    return a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def scale(a, value):
    return a[0]*value, a[1]*value


def conj(a):
    return a[0], -a[1]


def norm(a):
    return a[0]*a[0] + a[1]*a[1]


def total(values):
    answer = ZERO
    for value in values:
        answer = add(answer, value)
    return answer


def scalar_product(values):
    answer = ONE
    for value in values:
        answer = mul(answer, value)
    return answer


def permanent(matrix):
    k = len(matrix)
    return total(scalar_product(matrix[i][pi[i]] for i in range(k))
                 for pi in permutations(range(k)))


def identity(m):
    return [[ONE if i == j else ZERO for j in range(m)] for i in range(m)]


def rotate(u, i, j, t, phase=ONE):
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    old_i, old_j = u[i][:], u[j][:]
    u[i] = [add(scale(a, c), scale(mul(phase, b), s)) for a, b in zip(old_i, old_j)]
    u[j] = [add(scale(mul(conj(phase), a), -s), scale(b, c)) for a, b in zip(old_i, old_j)]


def random_unitary(m, seed, complex_phases):
    rng = random.Random(seed)
    u = identity(m)
    strengths = (F(1, 5), F(1, 3), F(1, 2), F(1))
    phases = (ONE, (F(0), F(1)), (F(3, 5), F(4, 5))) if complex_phases else (ONE,)
    for _ in range(m+2):
        i, j = rng.sample(range(m), 2)
        rotate(u, i, j, rng.choice(strengths), rng.choice(phases))
    return u


def column_frame(u, k):
    return [row[:k] for row in u]


def validate_frame(u, k):
    v = column_frame(u, k)
    assert all(total(mul(conj(v[i][a]), v[i][b]) for i in range(len(v)))
               == (ONE if a == b else ZERO) for a in range(k) for b in range(k))


def fock_law(v):
    """Creation-polynomial recursion, independent of permanent summation."""
    m, k = len(v), len(v[0])
    coefficients = {(0,)*m: ONE}
    for a in range(k):
        nxt = {}
        for occupation, value in coefficients.items():
            for i in range(m):
                target = list(occupation); target[i] += 1; target = tuple(target)
                nxt[target] = add(nxt.get(target, ZERO), mul(value, v[i][a]))
        coefficients = nxt
    return {state: norm(value)*math.prod(math.factorial(n) for n in state)
            for state, value in coefficients.items()}


def frame_case(name, k, u, groups, seed=None, attenuation=None):
    validate_frame(u, k)
    v = column_frame(u, k)
    if attenuation is not None:
        assert all(F(0) <= a <= F(1) for a in attenuation)
        v = [[scale(value, attenuation[i]) for value in row] for i, row in enumerate(v)]
    flat = [i for group in groups for i in group]
    assert len(groups) == k and len(flat) == len(set(flat))
    assert all(group and all(0 <= i < len(u) for i in group) for group in groups)
    return dict(name=name, k=k, u=u, v=v, groups=tuple(map(tuple, groups)),
                seed=seed, attenuation=attenuation)


def cases():
    u = identity(2); rotate(u, 0, 1, F(1, 3), (F(0), F(1)))
    rows = [frame_case('one_photon_complex', 1, u, ((0, 1),))]
    u = identity(4); u[1], u[2] = u[2], u[1]
    rotate(u, 0, 1, F(1, 3)); rotate(u, 2, 3, F(1, 5), (F(0), F(1)))
    rows.append(frame_case('product_dualrail', 2, u, ((0, 1), (2, 3))))
    signs = ((1, 1, 1, 1), (1, -1, 1, -1), (1, 1, -1, -1), (1, -1, -1, 1))
    u = [[g(F(x, 2)) for x in row] for row in signs]
    rows.append(frame_case('walsh_bell_readout', 2, u, ((0, 1), (2, 3))))
    for c, s in ((F(3, 5), F(4, 5)), (F(12, 13), F(5, 13))):
        u = [[g(c), ZERO, g(-s), ZERO], [ZERO, g(s), ZERO, g(-c)],
             [g(s), ZERO, g(c), ZERO], [ZERO, g(c), ZERO, g(s)]]
        rows.append(frame_case('sharp_frontier_'+str(c).replace('/', '_'), 2, u, ((0, 1), (2, 3))))
    for index, (k, complex_phases) in enumerate(((2, False), (2, True), (3, False),
                                               (3, True), (4, False), (4, True)), start=1):
        seed = 2026112400 + index
        u = random_unitary(2*k, seed, complex_phases)
        rows.append(frame_case(f'random_k{k}_complex{int(complex_phases)}', k, u,
                               tuple((2*i, 2*i+1) for i in range(k)), seed))
    u = random_unitary(8, 2026112407, True)
    rows.append(frame_case('variable_group_sizes', 3, u, ((0, 1, 2), (3, 4), (5, 6, 7)), 2026112407))
    u = random_unitary(8, 2026112408, True)
    rows.append(frame_case('singleton_herald_vacuum_remainder', 3, u,
                           ((0, 1), (2, 3), (4,)), 2026112408))
    u = random_unitary(8, 2026112409, True)
    rows.append(frame_case('contractive_losses', 3, u, ((0, 1), (2, 3), (4, 5)),
                           2026112409, (F(1), F(3, 5), F(4, 5), F(1), F(3, 5), F(4, 5), F(1), F(3, 5))))
    for original, pi in ((rows[2], (2, 0, 3, 1)),
                         (rows[8], (4, 1, 5, 0, 3, 2))):
        u = [None]*len(pi)
        for i, j in enumerate(pi):
            u[j] = original['u'][i][:]
        groups = tuple(tuple(pi[i] for i in group) for group in original['groups'])
        row = frame_case(original['name']+'_relabel', original['k'], u, groups, original['seed'])
        row['relabel_of'] = original['name']; row['permutation_old_to_new'] = pi
        rows.append(row)
    assert len(rows) == 16
    return rows


def exact_case(case):
    v, k, groups = case['v'], case['k'], case['groups']
    m = len(v)
    law = fock_law(v)
    assert len(law) == math.comb(m+k-1, k)
    total_photon_sector = sum(law.values())
    assert F(0) <= total_photon_sector <= F(1)
    if case['attenuation'] is None:
        assert total_photon_sector == 1
    # Check ALL Fock occupations using an independent explicit permutation sum.
    for occupation, probability in law.items():
        indices = [i for i, n in enumerate(occupation) for _ in range(n)]
        factorial = math.prod(math.factorial(n) for n in occupation)
        assert norm(permanent([v[i] for i in indices])) / factorial == probability
    sign_data = []
    for signs in product((-1, 1), repeat=k):
        beta = [total(scale(value, signs[a]) for a, value in enumerate(row)) for row in v]
        intensities = tuple(sum(norm(beta[i]) for i in group) for group in groups)
        w = math.prod(intensities)
        assert sum(intensities) <= k and F(0) <= w <= F(1)
        sign_data.append((signs, beta, intensities, w))
    accepted = []
    for x in product(*groups):
        amplitude = permanent([v[i] for i in x])
        coefficient = ZERO
        q = F(0); r = F(0)
        for signs, beta, intensities, w in sign_data:
            f = scalar_product(beta[i] for i in x)
            coefficient = add(coefficient, scale(f, math.prod(signs)))
            q += norm(f)
            # Always-feasible sampler, including its specified uniform fallback.
            mass = F(1)
            for i, group, intensity in zip(x, groups, intensities):
                mass *= norm(beta[i])/intensity if intensity else F(1, len(group))
            r += mass
        coefficient = scale(coefficient, F(1, 2**k)); q /= 2**k; r /= 2**k
        pb = norm(amplitude)
        pd = sum(math.prod(norm(v[x[i]][pi[i]]) for i in range(k)) for pi in permutations(range(k)))
        assert coefficient == amplitude and r >= q >= pb
        accepted.append({'x': x, 'bosonic': pb, 'distinguishable': pd,
                         'classical_rejecting': q, 'classical_always_feasible': r})
    pf = sum(row['bosonic'] for row in accepted)
    qf = sum(row['classical_rejecting'] for row in accepted)
    assert pf <= qf <= 1 and sum(row['classical_always_feasible'] for row in accepted) == 1
    assert qf == sum(row[3] for row in sign_data)/2**k
    frontier = None
    if k == 2 and m == 4 and all(len(group) == 2 for group in groups) and case['attenuation'] is None:
        t = [[permanent([v[i], v[j]]) for j in groups[1]] for i in groups[0]]
        determinant = add(mul(t[0][0], t[1][1]), scale(mul(t[0][1], t[1][0]), -1))
        slack = (1-pf)**2 - 4*norm(determinant)
        assert slack >= 0
        if case['name'].startswith('sharp_frontier') or case['name'] == 'walsh_bell_readout':
            assert slack == 0
        frontier = {'concurrence_squared': 4*norm(determinant)/(pf*pf) if pf else None,
                    'squared_frontier_slack': slack}
    return {'name': case['name'], 'k': k, 'm': m, 'groups': groups,
            'seed': case['seed'], 'frame': v, 'attenuation': case['attenuation'],
            'full_fock_law': [{'occupation': s, 'probability': p} for s, p in law.items()],
            'accepted': accepted, 'acceptance_bosonic': pf,
            'acceptance_classical_rejecting': qf,
            'loss_failure_probability': 1-total_photon_sector,
            'all_sign_weights': [row[3] for row in sign_data],
            'two_qubit_frontier': frontier,
            'all_fock_permutations_match': True, 'all_pointwise_inequalities_exact': True}


def float_sample(v, groups, rng, reject=True):
    import numpy as np
    signs = rng.choice((-1, 1), size=v.shape[1])
    beta = v @ signs
    intensities = np.abs(beta)**2
    totals = [float(intensities[list(group)].sum()) for group in groups]
    w = math.prod(totals)
    if w > 1+1e-10 or w < -1e-10:
        raise ArithmeticError('Invalid classical acceptance weight')
    if reject and rng.random() >= min(1., max(0., w)):
        return None
    return tuple(int(rng.choice(group, p=intensities[list(group)]/mass)) if mass else int(rng.choice(group))
                 for group, mass in zip(groups, totals))


def to_complex(v):
    import numpy as np
    return np.array([[complex(float(z[0]), float(z[1])) for z in row] for row in v], dtype=complex)


def perceval_checks(all_cases, all_results):
    from photonic_balanced_partitioning.hardware.offline import local_perceval, network_denied
    pcvl = local_perceval()
    values = []
    for name in ('walsh_bell_readout', 'random_k3_complex1'):
        case = next(c for c in all_cases if c['name'] == name)
        result = next(r for r in all_results if r['name'] == name)
        circuit = pcvl.Circuit(len(case['u'])).add(0, pcvl.Unitary(pcvl.Matrix(to_complex(case['u']))))
        with network_denied():
            backend = pcvl.SLOSBackend(); backend.set_circuit(circuit)
            backend.set_input_state(pcvl.BasicState([1]*case['k']+[0]*(len(case['u'])-case['k'])))
            distribution = backend.prob_distribution()
        err = max(abs(float(row['probability'])-float(distribution.get(pcvl.BasicState(row['occupation']), 0)))
                  for row in result['full_fock_law'])
        assert err < 1e-10
        values.append({'case': name, 'max_full_fock_error': err,
                       'occupations_compared': len(result['full_fock_law'])})
    return values


def encode(value):
    if isinstance(value, F):
        return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    if isinstance(value, dict):
        return {key: encode(v) for key, v in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # The bounded runner creates this directory; its declared results are new.
    args.output.mkdir(parents=True, exist_ok=True)
    all_cases = cases(); results = []
    with (args.output/'raw.jsonl').open('x') as stream:
        for case in all_cases:
            result = exact_case(case); results.append(result)
            stream.write(json.dumps(encode(result), sort_keys=True)+'\n'); stream.flush()
    for case, row in zip(all_cases, results):
        if 'relabel_of' in case:
            old = next(r for r in results if r['name'] == case['relabel_of'])
            assert [r['bosonic'] for r in old['accepted']] == [r['bosonic'] for r in row['accepted']]
            assert [r['classical_rejecting'] for r in old['accepted']] == [r['classical_rejecting'] for r in row['accepted']]
    bell = next(r for r in results if r['name'] == 'walsh_bell_readout')
    a = bell['accepted']; good = [(0, 2), (1, 3)]
    diagnostic = {model: sum(r[model] for r in a if r['x'] in good)
                  for model in ('bosonic', 'distinguishable', 'classical_rejecting', 'classical_always_feasible')}
    assert diagnostic == dict(bosonic=F(1, 2), distinguishable=F(1, 4),
                             classical_rejecting=F(1), classical_always_feasible=F(1))
    # Outside-scope countercontrol: unstratified ALL collision-free subsets.
    intensities = (F(9, 25), F(16, 25), F(9, 25), F(16, 25))
    naive_mass = sum(math.prod(intensities[i] for i in pair) for pair in combinations(range(4), 2))
    assert naive_mass == F(913, 625) > 1
    # Execute the actual floating sampler on the deterministic hand control.
    import numpy as np
    rng = np.random.default_rng(2026112411)
    v = to_complex(next(c for c in all_cases if c['name'] == 'walsh_bell_readout')['v'])
    counts = {}
    started = time.perf_counter()
    for _ in range(2048):
        outcome = float_sample(v, ((0, 1), (2, 3)), rng)
        key = 'failure' if outcome is None else ','.join(map(str, outcome))
        counts[key] = counts.get(key, 0)+1
    sampling_seconds = time.perf_counter()-started
    slos = perceval_checks(all_cases, results)
    summary = {'cases': len(results), 'full_fock_comparisons': sum(len(r['full_fock_law']) for r in results),
               'accepted_outcomes_checked': sum(len(r['accepted']) for r in results),
               'result': 'EXACT_FINITE_ASSERTIONS_PASS', 'independent_proof_review': False,
               'sharp_walsh_same_circuit_diagnostic': diagnostic,
               'arbitrary_collision_free_naive_mass': naive_mass,
               'perceval_checks': slos, 'sampler_attempts': 2048, 'sampler_seed': 2026112411,
               'sampler_counts': counts, 'sampler_wall_seconds': sampling_seconds,
               'sampler_counts_are': 'local classical simulation; not QPU',
               'optimization_training': False, 'heldout_advantage_claim': False,
               'qpu_calls': 0, 'non_claims': ['No universal adaptive-training no-go',
                   'No equality of realized objective-query costs', 'No general k-of-m CF normalization',
                   'No novelty assertion', 'No hardware advantage'],
               'software': {name: importlib.metadata.version(name) for name in ('numpy', 'perceval-quandela', 'exqalibur')}}
    (args.output/'summary.json').write_text(json.dumps(encode(summary), sort_keys=True, indent=2)+'\n')
    assert sum(p.stat().st_size for p in args.output.iterdir() if p.is_file()) < 32*1024**2
    print(json.dumps({'result': summary['result'], 'cases': summary['cases'],
                      'full_fock_comparisons': summary['full_fock_comparisons'],
                      'accepted_outcomes_checked': summary['accepted_outcomes_checked'],
                      'qpu_calls': 0}))


if __name__ == '__main__':
    main()
