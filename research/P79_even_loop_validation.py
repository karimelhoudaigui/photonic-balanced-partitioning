"""Prospective P79 finite raw-PNR diagnostic. Import constructs no cases/RNG/native API."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.metadata
import importlib.util
from itertools import product
import json
import math
import os
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
PYTHON = Path('/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python')
HELPER_SHA = 'fb3cf959f022481d360c3371168e0b2f5b97e400b14a4324c43237a162677a9d'
CASE_IDS = ('G1', 'G2', 'G3', 'G4', 'G5', 'G6')
SEEDS = (7910001, 7910002, 7910003, 7910004, 7910005, 7910006)
DRAWS = 20000
MAX_STEPS = 5000000
MAX_RECORD_BYTES = 30 * 1024 * 1024
MAX_SCIENTIFIC_BYTES = 32 * 1024 * 1024
ABS_TOL, REL_TOL = 1e-12, 1e-7
FAMILY_ALPHA, TOTAL_BINS = 0.01, 272
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
_HELPER = None


def digest(path):
    result = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def cli_profile():
    if (Path(sys.executable).resolve() != PYTHON.resolve()
            or Path(sys.prefix).resolve() != PYTHON.parent.parent.resolve()
            or sys.version_info[:3] != (3, 11, 15)):
        raise RuntimeError('use contracted persistent Python 3.11.15')
    if any(os.environ.get(key) != '1' for key in THREAD_KEYS):
        raise RuntimeError('contracted numerical thread environment must be one')


def native_setup():
    global _HELPER
    if _HELPER is None:
        path = ROOT / 'research/P66_exact_finite_check.py'
        if digest(path) != HELPER_SHA:
            raise RuntimeError('frozen P66 native loader changed')
        spec = importlib.util.spec_from_file_location('p79_frozen_native_loader', path)
        _HELPER = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_HELPER)
    api, metadata = _HELPER.native_api()
    return api, metadata, _HELPER


def cases():
    """MAIN ONLY: the six literal registered cases; no adaptive selection."""
    def component(indices, r, v):
        return {'indices': tuple(indices), 'r': F(r), 'v': tuple(F(x) for x in v)}
    return [
        {'id': 'G1', 'Z': [[F(3, 10)]], 's': [F(3, 10)],
         'components': [component([0], F(3, 10), [1])]},
        {'id': 'G2', 'Z': [[F(0), F(3, 5)], [F(3, 5), F(0)]],
         's': [F(3, 5), F(-3, 5)], 'components': [component([0, 1], F(3, 5), [1, 1])]},
        {'id': 'G3', 'Z': [[F(1, 5), F(2, 5)], [F(2, 5), F(1, 5)]],
         's': [F(3, 5), F(-1, 5)], 'components': [component([0, 1], F(3, 5), [1, 1])]},
        {'id': 'G4', 'Z': [[F(1, 6)] * 3 for _ in range(3)], 's': [F(1, 2), F(0), F(0)],
         'components': [component([0, 1, 2], F(1, 2), [1, 1, 1])]},
        {'id': 'G5', 'Z': [[F(0), F(3, 10), F(0), F(0)],
                          [F(3, 10), F(0), F(0), F(0)],
                          [F(0), F(0), F(0), F(1, 2)],
                          [F(0), F(0), F(1, 2), F(0)]],
         's': [F(3, 10), F(-3, 10), F(1, 2), F(-1, 2)],
         'components': [component([0, 1], F(3, 10), [1, 1]),
                        component([2, 3], F(1, 2), [1, 1])]},
        {'id': 'G6', 'Z': [[F(1, 12), F(1, 6), F(1, 12)],
                          [F(1, 6), F(1, 3), F(1, 6)],
                          [F(1, 12), F(1, 6), F(1, 12)]],
         's': [F(1, 2), F(0), F(0)],
         'components': [component([0, 1, 2], F(1, 2), [1, 2, 1])]},
    ]


def occupations(total, modes):
    if total < 0 or modes < 1:
        raise ValueError('occupation domain')
    if modes == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in occupations(total - first, modes - 1):
                yield (first,) + rest


def hafnian(matrix):
    n = len(matrix)
    if n % 2 or n > 6 or any(len(row) != n for row in matrix):
        raise ValueError('even square hafnian dimension at most six')
    if n == 0:
        return F(1)
    value = F(0)
    for j in range(1, n):
        keep = [i for i in range(1, n) if i != j]
        value += matrix[0][j] * hafnian([[matrix[a][b] for b in keep] for a in keep])
    return value


def gaussian_coefficient(z, counts):
    if len(counts) != len(z) or any(n < 0 or not isinstance(n, int) for n in counts):
        raise ValueError('occupation vector domain')
    labels = [i for i, n in enumerate(counts) for _ in range(n)]
    expanded = [[z[i][j] for j in labels] for i in labels]
    return hafnian(expanded)**2 / math.prod(math.factorial(n) for n in counts)


def determinant(matrix):
    n = len(matrix)
    if not n or n > 4 or any(len(row) != n for row in matrix):
        raise ValueError('exact determinant dimension one through four')
    a = [[F(x) for x in row] for row in matrix]
    value = F(1)
    for k in range(n):
        pivot = next((j for j in range(k, n) if a[j][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            a[pivot], a[k] = a[k], a[pivot]
            value = -value
        lead = a[k][k]
        value *= lead
        for j in range(k + 1, n):
            factor = a[j][k] / lead
            for col in range(k + 1, n):
                a[j][col] -= factor * a[k][col]
    return value


def normalizer(z):
    m = len(z)
    if not 1 <= m <= 4 or any(len(row) != m for row in z):
        raise ValueError('registered matrix dimension')
    if any(z[i][j] < 0 or z[i][j] != z[j][i] for i in range(m) for j in range(m)):
        raise ValueError('nonnegative symmetric matrix required')
    q = [[F(int(i == j)) - sum((z[i][k] * z[k][j] for k in range(m)), F(0))
          for j in range(m)] for i in range(m)]
    minors = [determinant([row[:k] for row in q[:k]]) for k in range(1, m + 1)]
    if any(x <= 0 for x in minors):
        raise ValueError('I-Z^2 is not strictly positive definite')
    return {'determinant_Q': minors[-1], 'leading_minors': minors,
            'raw_prefactor': math.sqrt(float(minors[-1]))}


def poly_mul(a, b, degree=6):
    result = {}
    for x, cx in a.items():
        for y, cy in b.items():
            exponent = tuple(i + j for i, j in zip(x, y))
            if sum(exponent) <= degree:
                result[exponent] = result.get(exponent, F(0)) + cx * cy
    return {key: value for key, value in result.items() if value}


def loop_coefficients(z):
    """Trace polynomial of (D Z)^k, then exp; separate from expanded hafnian."""
    m = len(z)
    zero = (0,) * m
    base = [[{tuple(int(k == i) for k in range(m)): z[i][j]} if z[i][j] else {}
             for j in range(m)] for i in range(m)]
    power = [[{zero: F(int(i == j))} if i == j else {} for j in range(m)] for i in range(m)]
    logarithm = {}
    for length in range(1, 7):
        new = [[{} for _ in range(m)] for _ in range(m)]
        for i, j, k in product(range(m), repeat=3):
            for exponent, value in poly_mul(power[i][k], base[k][j]).items():
                new[i][j][exponent] = new[i][j].get(exponent, F(0)) + value
        power = new
        if length % 2 == 0:
            for i in range(m):
                for exponent, value in power[i][i].items():
                    logarithm[exponent] = logarithm.get(exponent, F(0)) + value / length
    result, power = {zero: F(1)}, {zero: F(1)}
    for order in range(1, 4):
        power = poly_mul(power, logarithm)
        for exponent, value in power.items():
            result[exponent] = result.get(exponent, F(0)) + value / math.factorial(order)
    return result, logarithm


def integer_cdf(row):
    row = [F(x) for x in row]
    if any(x < 0 for x in row) or sum(row, F(0)) != 1:
        raise ValueError('exact stochastic row required; no float normalization')
    denominator = math.lcm(*(x.denominator for x in row))
    if denominator > 2**63 - 1:
        raise ValueError('registered integer generator range exceeded')
    cumulative, total = [], 0
    for x in row:
        total += x.numerator * (denominator // x.denominator)
        cumulative.append(total)
    if total != denominator:
        raise ArithmeticError('integer CDF endpoint')
    return denominator, cumulative


def component_tables(z, components):
    m, used, tables = len(z), set(), []
    for comp in components:
        indices, r, v = comp['indices'], F(comp['r']), tuple(F(x) for x in comp['v'])
        if not 0 < r < 1 or len(indices) != len(v) or not indices or any(x <= 0 for x in v):
            raise ValueError('positive valid Perron component required')
        if len(set(indices)) != len(indices) or any(i not in range(m) or i in used for i in indices):
            raise ValueError('component partition')
        used.update(indices)
        p = [[z[i][j] * v[b] / (r * v[a]) for b, j in enumerate(indices)] for a, i in enumerate(indices)]
        cdf = [integer_cdf(row) for row in p]
        reached = {0}
        while True:
            enlarged = reached | {b for a in reached for b in range(len(indices)) if p[a][b]}
            if enlarged == reached:
                break
            reached = enlarged
        if len(reached) != len(indices):
            raise ValueError('component support not connected')
        if any(z[i][j] for i in indices for j in range(m) if j not in indices):
            raise ValueError('cross-component coupling')
        tables.append({'indices': indices, 'r': r, 'v': v, 'P': p, 'cdf': cdf,
                       'poisson_mean': -len(indices) * math.log1p(-float(r * r)) / 2})
    if used != set(range(m)):
        raise ValueError('component partition incomplete')
    return tables


def unitary(case):
    """Literal prospective decompositions, called only inside native phase."""
    name = case['id']
    half = math.sqrt(0.5)
    h = [[half, half], [half, -half]]
    if name == 'G1':
        return [[1.0]]
    if name in ('G2', 'G3'):
        return h
    if name == 'G4':
        omega = complex(-0.5, math.sqrt(3) / 2)
        return [[omega**(i * j) / math.sqrt(3) for j in range(3)] for i in range(3)]
    if name == 'G5':
        return [[h[i % 2][j % 2] if i // 2 == j // 2 else 0.0 for j in range(4)] for i in range(4)]
    if name == 'G6':
        return [[1 / math.sqrt(6), 1 / math.sqrt(2), -1 / math.sqrt(3)],
                [2 / math.sqrt(6), 0.0, 1 / math.sqrt(3)],
                [1 / math.sqrt(6), -1 / math.sqrt(2), -1 / math.sqrt(3)]]
    raise ValueError('unregistered native case')


def unitary_diagnostics(case, u):
    m = len(u)
    left = max(abs(sum(complex(u[k][i]).conjugate() * u[k][j] for k in range(m)) - int(i == j))
               for i in range(m) for j in range(m))
    right = max(abs(sum(u[i][k] * complex(u[j][k]).conjugate() for k in range(m)) - int(i == j))
                for i in range(m) for j in range(m))
    residual = max(abs(sum(u[i][k] * float(case['s'][k]) * u[j][k] for k in range(m)) - float(case['Z'][i][j]))
                   for i in range(m) for j in range(m))
    if not all(math.isfinite(x) and x <= 1e-12 for x in (left, right, residual)):
        raise ArithmeticError('native unitary/decomposition residual')
    return {'left_unitarity_residual': left, 'right_unitarity_residual': right,
            'pair_reconstruction_residual': residual}


def input_coefficient(signed_s, counts):
    if len(signed_s) != len(counts) or any(n < 0 or n % 2 for n in counts):
        raise ValueError('even input occupation required')
    return math.prod(float(s)**(n // 2) * math.sqrt(math.factorial(n)) /
                     (2**(n // 2) * math.factorial(n // 2)) for s, n in zip(signed_s, counts))


def mixed_tolerance(observed, reference):
    scale = max(abs(observed), abs(reference))
    bound = ABS_TOL + REL_TOL * scale
    return bound, ('ABS_DOMINANT' if ABS_TOL >= REL_TOL * scale else 'REL_DOMINANT')


def cp_interval(count, trials, delta):
    if not 0 <= count <= trials or trials < 1 or not 0 < delta < 1:
        raise ValueError('binomial interval domain')
    if importlib.metadata.version('scipy') != '1.17.1':
        raise RuntimeError('pinned scipy version differs')
    from scipy.stats import beta
    low = 0.0 if count == 0 else float(beta.ppf(delta / 2, count, trials - count + 1))
    high = 1.0 if count == trials else float(beta.ppf(1 - delta / 2, count + 1, trials - count))
    if not all(math.isfinite(x) for x in (low, high)) or not 0 <= low <= high <= 1:
        raise ArithmeticError('invalid Clopper-Pearson interval')
    return low, high


class FirstFailure(AssertionError):
    pass


class ResourceStop(RuntimeError):
    pass


class StatisticalDiscrepancy(AssertionError):
    pass


class StepBudget:
    def __init__(self, maximum):
        self.maximum, self.count = maximum, 0

    def reserve(self):
        if self.count >= self.maximum:
            raise ResourceStop('fixed global proposed-transition cap')
        self.count += 1


def json_default(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, complex):
        return [value.real, value.imag]
    raise TypeError(type(value).__name__)


def encoded(value):
    return (json.dumps(value, default=json_default, sort_keys=True,
                       separators=(',', ':'), allow_nan=False) + '\n').encode()


class Ledger:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=False)
        self.handle = (self.output / 'records.jsonl').open('xb')
        self.bytes = 0
        self.context = {}
        self.counts = {key: 0 for key in ('exact_points', 'native_points', 'native_amplitudes', 'draws', 'bins')}

    def emit(self, kind, **row):
        payload = encoded({'kind': kind, **row})
        if self.bytes + len(payload) > MAX_RECORD_BYTES:
            raise ResourceStop('fixed scientific record byte cap')
        self.handle.write(payload)
        self.handle.flush()
        self.bytes += len(payload)

    def require(self, condition, message):
        if not condition:
            raise FirstFailure(message)


def exact_phase(case, ledger):
    z, m = case['Z'], len(case['Z'])
    data = normalizer(z)
    ledger.require(data['determinant_Q'] == math.prod(1 - s * s for s in case['s']),
                   'independent signed-spectrum determinant identity')
    tables = component_tables(z, case['components'])
    loop, logarithm = loop_coefficients(z)
    ledger.emit('case_definition', case=case['id'], Z=z, signed_s=case['s'],
                components=tables, normalizer=data,
                loop_log_coefficients=[{'occupation': key, 'coefficient': val} for key, val in sorted(logarithm.items())])
    refs = {}
    for total in (0, 2, 4, 6):
        for target in occupations(total, m):
            ledger.context = {'phase': 'exact', 'case': case['id'], 'target': target}
            direct = gaussian_coefficient(z, target)
            proposed = loop.get(target, F(0))
            q = data['raw_prefactor'] * float(direct)
            ledger.emit('exact_point', case=case['id'], occupation=target,
                        hafnian_coefficient=direct, loop_coefficient=proposed, exact_equal=direct == proposed,
                        raw_probability=q, raw_prefactor=data['raw_prefactor'])
            ledger.counts['exact_points'] += 1
            ledger.require(direct == proposed and direct >= 0, 'exact coefficient disagreement')
            ledger.require(math.isfinite(q) and 0 <= q <= 1, 'raw Gaussian reference domain')
            refs[target] = q
    return {'refs': refs, 'normalizer': data, 'tables': tables}


def native_phase(case, data, ledger, api, helper):
    pcvl, xq, backend_type = api
    u = unitary(case)
    diag = unitary_diagnostics(case, u)
    helper.native_readback(xq)
    backend = backend_type()
    backend.set_circuit(pcvl.Circuit(len(u)).add(0, pcvl.Unitary(pcvl.Matrix(u))))
    ledger.emit('native_decomposition', case=case['id'], unitary=u, signed_s=case['s'], **diag)
    for total in (2, 4):
        sources = [tuple(2 * x for x in occ) for occ in occupations(total // 2, len(u))]
        for target in occupations(total, len(u)):
            ledger.context = {'phase': 'native', 'case': case['id'], 'total': total, 'target': target}
            coherent = 0j
            for source in sources:
                coefficient = input_coefficient(case['s'], source)
                helper.native_readback(xq)
                backend.set_input_state(pcvl.BasicState(list(source)))
                amplitude = complex(backend.prob_amplitude(pcvl.BasicState(list(target))))
                helper.native_readback(xq)
                term = coefficient * amplitude
                ledger.emit('native_amplitude', case=case['id'], source=source, target=target,
                            source_coefficient=coefficient, source_zero=coefficient == 0,
                            native_amplitude=amplitude, coherent_term=term)
                ledger.counts['native_amplitudes'] += 1
                ledger.require(all(math.isfinite(v) for v in (amplitude.real, amplitude.imag)), 'nonfinite native amplitude')
                coherent += term
            q = data['normalizer']['raw_prefactor'] * abs(coherent)**2
            ref = data['refs'][target]
            tolerance, branch = mixed_tolerance(q, ref)
            ledger.emit('native_point', case=case['id'], occupation=target, source_terms=len(sources),
                        coherent_sum=coherent, raw_probability=q, reference=ref,
                        reference_zero=ref == 0, absolute_error=abs(q - ref), tolerance=tolerance,
                        tolerance_branch=branch, passed=math.isfinite(q) and abs(q - ref) <= tolerance)
            ledger.counts['native_points'] += 1
            ledger.require(math.isfinite(q) and abs(q - ref) <= tolerance, 'Perceval coherent-sector discrepancy')


def draw_loop_counts(rng, m, tables, budget, ledger):
    counts, proposed_loops, accepted_loops, steps = [0] * m, 0, 0, 0
    for component_index, tab in enumerate(tables):
        indices = tab['indices']
        number = int(rng.poisson(tab['poisson_mean']))
        for proposal in range(number):
            proposed_loops += 1
            half_length = int(rng.logseries(float(tab['r'] * tab['r'])))
            if half_length < 1:
                raise ArithmeticError('invalid log-series length')
            start = current = int(rng.integers(len(indices)))
            visits = [0] * len(indices)
            for position in range(2 * half_length):
                ledger.context.update({'component': component_index, 'proposal': proposal,
                                       'planned_component_proposals': number, 'half_length': half_length,
                                       'position': position, 'partial_counts': counts[:],
                                       'partial_loop_visits': visits[:], 'partial_proposed_loops': proposed_loops,
                                       'partial_accepted_loops': accepted_loops, 'partial_proposed_steps': steps})
                budget.reserve()
                visits[current] += 1
                denominator, cdf = tab['cdf'][current]
                integer = int(rng.integers(denominator))
                current = next(j for j, endpoint in enumerate(cdf) if integer < endpoint)
                steps += 1
            if current == start:
                accepted_loops += 1
                for local, global_index in enumerate(indices):
                    counts[global_index] += visits[local]
    return counts, proposed_loops, accepted_loops, steps


def statistics(case, data, histogram, totals, ledger, report):
    refs = list(data['refs'].items())
    tail = 1 - math.fsum(q for _, q in refs)
    ledger.require(math.isfinite(tail) and 0 <= tail <= 1, 'unclipped full-PNR tail reference domain')
    refs.append(('TAIL_GT6', tail))
    mean_photons = sum((s * s / (1 - s * s) for s in case['s']), F(0))
    expected_steps = sum((len(t['indices']) * t['r']**2 / (1 - t['r']**2) for t in data['tables']), F(0))
    ledger.require(expected_steps <= len(case['Z']) * mean_photons, 'P78 stated transition expectation bound')
    ledger.emit('descriptive_costs', case=case['id'], draws=DRAWS, totals=totals,
                observed_mean_photons=totals['photons'] / DRAWS,
                observed_mean_proposed_steps=totals['steps'] / DRAWS,
                expected_mean_photons=mean_photons, expected_proposed_steps=expected_steps,
                P78_bound=len(case['Z']) * mean_photons, mean_confidence_interval=None)
    for label, q in refs:
        ledger.context = {'phase': 'statistics', 'case': case['id'], 'bin': label}
        count = histogram.get(label, 0)
        low, high = cp_interval(count, DRAWS, FAMILY_ALPHA / TOTAL_BINS)
        covered = low - 1e-12 <= q <= high + 1e-12
        ledger.emit('bin', case=case['id'], occupation=label, count=count, trials=DRAWS,
                    raw_reference=q, cp_low=low, cp_high=high, covered=covered,
                    family_alpha=FAMILY_ALPHA, family_size=TOTAL_BINS, floating_reference_tolerance=1e-12)
        ledger.counts['bins'] += 1
        report['completed_bins'] += 1
        if not covered:
            raise StatisticalDiscrepancy('fixed-family interval excludes reference; possible 1% family false alarm')


def stochastic_phase(case, data, seed, ledger, budget, report):
    if importlib.metadata.version('numpy') != '2.4.6':
        raise RuntimeError('pinned numpy version differs')
    import numpy as np
    rng = np.random.Generator(np.random.PCG64(seed))
    initial_steps = budget.count
    histogram, totals = {}, {'photons': 0, 'loops': 0, 'accepted_loops': 0, 'steps': 0}
    for draw_id in range(1, DRAWS + 1):
        ledger.context = {'phase': 'stochastic', 'case': case['id'], 'seed': seed, 'draw': draw_id}
        counts, loops, accepted, steps = draw_loop_counts(rng, len(case['Z']), data['tables'], budget, ledger)
        photons = sum(counts)
        ledger.emit('draw', case=case['id'], seed=seed, draw=draw_id, counts=counts,
                    total_photons=photons, proposed_loops=loops, accepted_loops=accepted, proposed_steps=steps)
        ledger.counts['draws'] += 1
        report['completed_draws'] += 1
        ledger.require(photons % 2 == 0 and all(x >= 0 for x in counts), 'raw count parity/domain')
        label = tuple(counts) if photons <= 6 else 'TAIL_GT6'
        histogram[label] = histogram.get(label, 0) + 1
        totals['photons'] += photons
        totals['loops'] += loops
        totals['accepted_loops'] += accepted
        totals['steps'] += steps
    ledger.require(sum(histogram.values()) == DRAWS, 'all raw draws counted without selection')
    ledger.require(totals['steps'] == budget.count - initial_steps, 'paid proposed-step reconstruction')
    report['stochastic'] = 'DRAWS_COMPLETE'
    report['statistics'] = 'RUNNING'
    ledger.context = {'phase': 'statistics_initialization', 'case': case['id']}
    statistics(case, data, histogram, totals, ledger, report)
    report['statistics'] = 'COMPLETE'


def run(output):
    started, cpu = time.perf_counter(), time.process_time()
    ledger, budget = Ledger(output), StepBudget(MAX_STEPS)
    reports = [{'case': name, 'exact': 'NOT_RUN', 'native': 'NOT_RUN', 'stochastic': 'NOT_RUN',
                'statistics': 'NOT_RUN', 'completed_draws': 0, 'completed_bins': 0, 'planned_bins': bins}
               for name, bins in zip(CASE_IDS, (5, 17, 17, 51, 131, 51))]
    status, failure, native_metadata = 'INCONCLUSIVE_FIRST_FAILURE', None, None
    try:
        population = cases()
        ledger.require(tuple(c['id'] for c in population) == CASE_IDS, 'fixed case order')
        prepared = {}
        for case, report in zip(population, reports):
            report['exact'] = 'RUNNING'
            ledger.context = {'phase': 'exact_initialization', 'case': case['id']}
            prepared[case['id']] = exact_phase(case, ledger)
            report['exact'] = 'COMPLETE'
        ledger.require(ledger.counts['exact_points'] == 266, 'predeclared exact population count')
        ledger.context = {'phase': 'native_initialization'}
        api, native_metadata, helper = native_setup()
        ledger.emit('native_runtime', metadata=native_metadata)
        for case, report in zip(population, reports):
            report['native'] = 'RUNNING'
            ledger.context = {'phase': 'native_decomposition', 'case': case['id']}
            native_phase(case, prepared[case['id']], ledger, api, helper)
            report['native'] = 'COMPLETE'
        ledger.require(ledger.counts['native_points'] == 105 and ledger.counts['native_amplitudes'] == 650,
                       'predeclared complete native population count')
        for case, report, seed in zip(population, reports, SEEDS):
            report['stochastic'] = 'RUNNING'
            stochastic_phase(case, prepared[case['id']], seed, ledger, budget, report)
            report['stochastic'] = 'COMPLETE'
        ledger.require(ledger.counts['draws'] == 120000 and ledger.counts['bins'] == 272,
                       'predeclared raw draw and fixed-bin populations')
        status = 'FINITE_VALIDATION_PASSED'
    except Exception as error:
        status = ('INCONCLUSIVE_RESOURCE_LIMIT' if isinstance(error, ResourceStop) else
                  'STATISTICAL_DISCREPANCY' if isinstance(error, StatisticalDiscrepancy) else
                  'INCONCLUSIVE_FIRST_FAILURE')
        failure = {'type': type(error).__name__, 'message': str(error), 'context': ledger.context,
                   'traceback': traceback.format_exc(limit=8), 'retry_permitted': False}
        for report in reports:
            for phase in ('exact', 'native', 'stochastic', 'statistics'):
                if report[phase] == 'RUNNING':
                    report[phase] = status
    finally:
        ledger.handle.close()
    summary = {'status': status, 'case_reports': reports, 'observed_counts': ledger.counts,
               'maximum_draws': 120000, 'global_proposed_steps': budget.count,
               'maximum_proposed_steps': MAX_STEPS, 'first_failure': failure,
               'wall_seconds': time.perf_counter() - started, 'cpu_seconds': time.process_time() - cpu,
               'source_sha256': digest(__file__), 'records_sha256': digest(ledger.output / 'records.jsonl'),
               'Python': sys.version.split()[0], 'interpreter': str(Path(sys.executable).resolve()),
               'interpreter_sha256': digest(sys.executable),
               'threads': {key: os.environ.get(key) for key in THREAD_KEYS},
               'native_runtime_recorded': native_metadata is not None, 'finite_bit_TV_certified': False,
               'universal_theorem_proved_by_run': False, 'optimizer_advantage_claimed': False,
               'QPU_calls': 0, 'Gaussian_native_sampler_calls': 0}
    for name, data in (('summary.json', summary), ('failure.json', failure)):
        payload = encoded(data)
        if ledger.bytes + len(payload) > MAX_SCIENTIFIC_BYTES:
            raise ResourceStop('fixed total scientific byte cap')
        with (ledger.output / name).open('xb') as handle:
            handle.write(payload)
        ledger.bytes += len(payload)
    return 0 if status == 'FINITE_VALIDATION_PASSED' else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or not output.is_relative_to(ROOT):
        raise ValueError('fresh output must be a worktree subdirectory')
    cli_profile()
    return run(output)


if __name__ == '__main__':
    raise SystemExit(main())
