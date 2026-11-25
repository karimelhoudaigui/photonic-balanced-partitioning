"""Prospective P75b six-mode Gaussian-CF falsifier; import performs no science."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import importlib.metadata
import importlib.util
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
SEEDS = (7510001, 7510002, 7510003, 7510004, 7510005, 7510006)
N = 6
PER_START = 300
FLOAT_BOUND = 1 / 64
FLOAT_MARGIN = 1e-8
EXACT_BOUND_SQUARED = F(1, 4096)
ROUND_DENOMINATOR = 10**12
MAX_RECORD_BYTES = 7 * 1024 * 1024
MAX_SCIENTIFIC_BYTES = 8 * 1024 * 1024
THREAD_KEYS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS',
               'VECLIB_MAXIMUM_THREADS', 'NUMEXPR_NUM_THREADS')
_EXACT_C = None
_NP = None


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def exact_class():
    global _EXACT_C
    if _EXACT_C is None:
        path = ROOT / 'research/P66_exact_finite_check.py'
        if digest(path) != HELPER_SHA:
            raise RuntimeError('frozen P66 exact-field input changed')
        spec = importlib.util.spec_from_file_location('p75b_exact_field', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _EXACT_C = module.C
    return _EXACT_C


def numpy_module():
    global _NP
    if _NP is not None:
        return _NP
    for name, version in (('numpy', '2.4.6'), ('scipy', '1.17.1')):
        if importlib.metadata.version(name) != version:
            raise RuntimeError('pinned numerical package version differs: ' + name)
    import numpy as np
    _NP = np
    return np


def cli_profile():
    if (Path(sys.executable).resolve() != PYTHON.resolve()
            or Path(sys.prefix).resolve() != PYTHON.parent.parent.resolve()
            or sys.version_info[:3] != (3, 11, 15)):
        raise RuntimeError('use contracted persistent Python 3.11.15')
    if any(os.environ.get(key) != '1' for key in THREAD_KEYS):
        raise RuntimeError('contracted numerical thread environment must be one')


def hafnian(a):
    n = len(a)
    if n % 2 or n > 6 or any(len(row) != n for row in a):
        raise ValueError('even square hafnian dimension at most six')
    if n == 0:
        return 1
    total = 0
    for j in range(1, n):
        keep = [i for i in range(1, n) if i != j]
        total = total + a[0][j] * hafnian([[a[u][v] for v in keep] for u in keep])
    return total


def decode(params, n):
    np = numpy_module()
    p = np.asarray(params, dtype=float)
    if n not in (2, 6) or p.shape != (n * (n + 1) + 1,) or not np.isfinite(p).all():
        raise ValueError('invalid frozen parameter dimension or nonfinite value')
    if (p[:-1] < -1).any() or (p[:-1] > 1).any() or not 0 <= p[-1] <= 3:
        raise ValueError('parameter outside registered bounds')
    b = np.zeros((n, n), dtype=complex)
    index = 0
    for i in range(n):
        for j in range(i, n):
            b[i, j] = b[j, i] = complex(float(p[index]), float(p[index + 1]))
            index += 2
    norm = float(np.linalg.svd(b, compute_uv=False)[0])
    alpha = math.tanh(float(p[-1]))
    z = np.zeros_like(b) if norm == 0 else (alpha / norm) * b
    return z, {'B_operator_norm': norm, 'alpha': alpha, 'zero_B': norm == 0}


class PhysicalInvariantFailure(ArithmeticError):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics
        super().__init__('physical Gaussian invariant failed')


def probability(z):
    np = numpy_module()
    z = np.asarray(z, dtype=complex)
    n = len(z)
    if n not in (2, 6) or z.shape != (n, n) or not np.isfinite(z).all():
        raise ValueError('invalid Gaussian matrix')
    symmetry = bool(np.array_equal(z, z.T))
    singular = np.linalg.svd(z, compute_uv=False)
    qmat = np.eye(n, dtype=complex) - z @ z.conjugate().T
    residual = float(np.max(np.abs(qmat - qmat.conjugate().T)))
    eigen = np.linalg.eigvalsh(qmat)
    det = complex(np.linalg.det(qmat))
    flags = {'symmetric': symmetry, 'strict_contraction': bool(singular[0] < 1),
             'positive_Q_eigenvalues': bool(eigen[0] > 0),
             'Hermitian_Q_residual_ok': residual <= 1e-12,
             'real_positive_determinant': abs(det.imag) <= 1e-12 and det.real > 0}
    diagnostics = {'physical_flags': flags, 'singular_values': singular.tolist(),
                   'Q_eigenvalues': eigen.tolist(), 'Q_Hermitian_residual': residual,
                   'determinant_Q': [det.real, det.imag]}
    if not all(flags.values()):
        raise PhysicalInvariantFailure(diagnostics)
    amplitude = complex(hafnian(z.tolist()))
    value = math.sqrt(det.real) * abs(amplitude)**2
    if not math.isfinite(value) or not 0 <= value <= 1 + 1e-12:
        raise ArithmeticError('nonfinite or invalid Gaussian probability')
    return value, {**diagnostics, 'hafnian': [amplitude.real, amplitude.imag]}


def exact_ldl(q):
    C = exact_class()
    n = len(q)
    if not 1 <= n <= 6 or any(len(row) != n for row in q):
        raise ValueError('exact LDL dimension guard')
    if any(C(q[i][j]) != C(q[j][i]).conjugate() for i in range(n) for j in range(n)):
        return {'positive_definite': False, 'reason': 'not Hermitian', 'pivots': [], 'leading_minors': []}
    lower = [[C() for _ in range(n)] for _ in range(n)]
    pivots, minors, determinant = [], [], F(1)
    for i in range(n):
        pivot = C(q[i][i]) - sum((lower[i][k] * lower[i][k].conjugate() * pivots[k]
                                  for k in range(i)), C())
        if pivot.i:
            raise ArithmeticError('nonreal exact Hermitian LDL pivot')
        pivots.append(pivot.r)
        determinant *= pivot.r
        minors.append(determinant)
        if pivot.r <= 0:
            return {'positive_definite': False, 'reason': 'nonpositive leading pivot',
                    'pivots': pivots, 'leading_minors': minors}
        lower[i][i] = C(1)
        for j in range(i + 1, n):
            numerator = C(q[j][i]) - sum((lower[j][k] * lower[i][k].conjugate() * pivots[k]
                                          for k in range(i)), C())
            lower[j][i] = numerator / pivot.r
    for i in range(n):
        for j in range(n):
            rebuilt = sum((lower[i][k] * pivots[k] * lower[j][k].conjugate()
                           for k in range(n)), C())
            if rebuilt != C(q[i][j]):
                raise ArithmeticError('exact LDL reconstruction failed')
    return {'positive_definite': True, 'reason': None, 'pivots': pivots,
            'leading_minors': minors, 'determinant': determinant}


def exact_witness(z):
    C = exact_class()
    n = len(z)
    if n not in (2, 6) or any(len(row) != n for row in z):
        raise ValueError('exact witness domain')
    z = [[C(value) for value in row] for row in z]
    symmetric = all(z[i][j] == z[j][i] for i in range(n) for j in range(n))
    if not symmetric:
        return {'physical': False, 'reason': 'not symmetric', 'Z': z}
    q = [[C(int(i == j)) - sum((z[i][k] * z[j][k].conjugate() for k in range(n)), C())
          for j in range(n)] for i in range(n)]
    factor = exact_ldl(q)
    result = {'Z': z, 'Q': q, 'LDL': factor, 'physical': factor['positive_definite']}
    if not factor['positive_definite']:
        result['reason'] = 'rounded matrix not a strict contraction'
        return result
    amplitude = C(hafnian(z))
    result.update({'reason': None, 'hafnian': amplitude, 'hafnian_norm_squared': amplitude.norm2(),
                   'probability_squared': factor['determinant'] * amplitude.norm2()**2,
                   'field_membership': {
                       'diagonal_zero': all(z[i][i] == 0 for i in range(n)),
                       'real': all(z[i][j].i == 0 for i in range(n) for j in range(n)),
                       'real_nonnegative': all(z[i][j].i == 0 and z[i][j].r >= 0
                                               for i in range(n) for j in range(n)),
                       'strictly_positive_real_offdiagonal': all(z[i][j].i == 0 and z[i][j].r > 0
                                                                for i in range(n) for j in range(n) if i != j)}})
    return result


def rounded_witness(z):
    C = exact_class()
    def rounded(x):
        return F(round(F.from_float(float(x)) * ROUND_DENOMINATOR), ROUND_DENOMINATOR)
    rational = [[C(rounded(value.real), rounded(value.imag)) for value in row] for row in z]
    return exact_witness(rational)


def json_default(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, 'r') and hasattr(value, 'i') and isinstance(value.r, F):
        return [str(value.r), str(value.i)]
    raise TypeError(type(value).__name__)


def encoded(value):
    return (json.dumps(value, default=json_default, allow_nan=False,
                       sort_keys=True, separators=(',', ':')) + '\n').encode()


class BudgetStop(Exception):
    pass


class FloatCandidate(Exception):
    def __init__(self, record, z):
        self.record, self.z = record, z
        super().__init__('registered float threshold exceeded')


class Counter:
    def __init__(self, maximum):
        self.maximum, self.count = maximum, 0

    def reserve(self):
        if self.count >= self.maximum:
            raise BudgetStop('strict objective-evaluation budget reached')
        self.count += 1
        return self.count


class Ledger:
    def __init__(self, output):
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=False)
        self.handle = (self.output / 'evaluations.jsonl').open('xb')
        self.bytes = self.total = 0
        self.best = None
        self.context = {}

    def emit(self, record):
        payload = encoded(record)
        if self.bytes + len(payload) > MAX_RECORD_BYTES:
            raise RuntimeError('scientific evaluation record byte cap')
        self.handle.write(payload)
        self.handle.flush()
        self.bytes += len(payload)

    def evaluate(self, params, label, counter):
        index = counter.reserve()
        self.total += 1
        self.context = {'start': label, 'local_evaluation': index, 'global_evaluation': self.total}
        z = None
        try:
            z, mapping = decode(params, N)
            value, diagnostics = probability(z)
        except Exception as error:
            self.emit({'kind': 'evaluation_failure', **self.context,
                       'parameters': [float(x) for x in params],
                       'Z_real': None if z is None else z.real.tolist(),
                       'Z_imag': None if z is None else z.imag.tolist(),
                       'probability': None,
                       'diagnostics': getattr(error, 'diagnostics', {'physical_flags': None}),
                       'error_type': type(error).__name__, 'error': str(error)})
            raise
        record = {'kind': 'evaluation', **self.context, 'parameters': [float(x) for x in params],
                  'Z_real': z.real.tolist(), 'Z_imag': z.imag.tolist(), 'probability': value,
                  'mapping': mapping, **diagnostics}
        self.emit(record)
        if self.best is None or value > self.best['probability']:
            self.best = {'probability': value, **self.context}
        if value > FLOAT_BOUND + FLOAT_MARGIN:
            raise FloatCandidate(record, z)
        return -value


def baseline_parameters():
    params = []
    for i in range(N):
        for j in range(i, N):
            params.extend((1.0 if (i, j) in ((0, 1), (2, 3), (4, 5)) else 0.0, 0.0))
    params.append(math.atanh(1 / math.sqrt(2)))
    return params


def run(output):
    started, cpu = time.perf_counter(), time.process_time()
    ledger = Ledger(output)
    reports = [{'seed': seed, 'status': 'NOT_RUN', 'objective_evaluations': 0,
                'maximum_objective_evaluations': PER_START} for seed in SEEDS]
    status, failure, certificate = 'INCONCLUSIVE_FIRST_FAILURE', None, None
    runtime = None
    base = None
    try:
        np = numpy_module()
        from scipy.optimize import minimize
        import scipy
        runtime = {'Python': sys.version.split()[0], 'numpy': importlib.metadata.version('numpy'),
                   'scipy': importlib.metadata.version('scipy'),
                   'interpreter': str(Path(sys.executable).resolve()),
                   'interpreter_sha256': digest(sys.executable),
                   'numpy_file_sha256': digest(np.__file__),
                   'scipy_file_sha256': digest(scipy.__file__),
                   'threads': {key: os.environ.get(key) for key in THREAD_KEYS},
                   'optimizer': 'scipy.optimize.minimize/L-BFGS-B',
                   'options': {'maxiter': 50, 'maxfun': 300, 'maxls': 20,
                               'ftol': 2.220446049250313e-9, 'gtol': 1e-5, 'eps': 1e-8}}
        base = Counter(1)
        baseline_value = -ledger.evaluate(baseline_parameters(), 'analytic_three_pair_baseline', base)
        if abs(baseline_value - FLOAT_BOUND) > 1e-12:
            raise ArithmeticError('registered three-pair baseline differs from analytic 1/64')
        bounds = [(-1.0, 1.0)] * (N * (N + 1)) + [(0.0, 3.0)]
        for report in reports:
            report['status'] = 'RUNNING'
            ledger.context = {'stage': 'start_initialization', 'seed': report['seed']}
            counter = Counter(PER_START)
            rng = np.random.Generator(np.random.PCG64(report['seed']))
            initial = np.r_[rng.uniform(-1, 1, N * (N + 1)), rng.uniform(0, 3)]
            try:
                result = minimize(lambda point: ledger.evaluate(point, report['seed'], counter),
                                  initial, method='L-BFGS-B', bounds=bounds, options=dict(runtime['options']))
                report.update({'status': 'OPTIMIZER_RETURNED', 'scipy_status': int(result.status),
                               'scipy_success': bool(result.success), 'message': str(result.message),
                               'iterations': int(result.nit), 'scipy_nfev': int(result.nfev),
                               'final_parameters': result.x.tolist(), 'final_probability': -float(result.fun)})
                if int(result.status) not in (0, 1):
                    report['status'] = 'STOPPED_UNEXPECTED_OPTIMIZER_STATUS'
                    raise RuntimeError('unregistered optimizer termination: ' + str(result.message))
            except BudgetStop:
                report['status'] = 'EVALUATION_BUDGET_EXHAUSTED'
            finally:
                report['objective_evaluations'] = counter.count
            ledger.emit({'kind': 'start_termination', **report})
        if ledger.total != 1 + sum(item['objective_evaluations'] for item in reports):
            raise ArithmeticError('evaluation count reconstruction failed')
        status = 'NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH'
    except FloatCandidate as found:
        certificate = {'round_denominator': ROUND_DENOMINATOR,
                       'round_rule': 'nearest rational with fixed denominator, exact ties to even',
                       'float_candidate': found.record, 'exact_squared_bound': EXACT_BOUND_SQUARED}
        certified = False
        try:
            witness = rounded_witness(found.z)
            certificate['witness'] = witness
            certified = bool(witness['physical'] and witness['probability_squared'] > EXACT_BOUND_SQUARED)
            status = 'COUNTEREXAMPLE_CERTIFIED' if certified else 'INCONCLUSIVE_FLOAT_CANDIDATE'
        except Exception as error:
            failure = {'context': ledger.context, 'type': type(error).__name__, 'message': str(error),
                       'traceback': traceback.format_exc(limit=8), 'retry_permitted': False,
                       'stage': 'single_fixed_exact_certificate'}
            certificate['certificate_error'] = failure
            status = 'INCONCLUSIVE_FIRST_FAILURE'
        for item in reports:
            if item['status'] == 'RUNNING':
                item['status'] = ('STOPPED_FIRST_FAILURE' if failure else 'STOPPED_ON_FLOAT_CANDIDATE')
            elif item['status'] == 'NOT_RUN':
                item['status'] = ('CANCELLED_AFTER_FIRST_FAILURE' if failure else
                                  'CANCELLED_AFTER_CERTIFIED_COUNTEREXAMPLE' if certified
                                  else 'CANCELLED_AFTER_UNCERTIFIED_FLOAT_CANDIDATE')
    except Exception as error:
        failure = {'context': ledger.context, 'type': type(error).__name__, 'message': str(error),
                   'traceback': traceback.format_exc(limit=8), 'retry_permitted': False}
        for item in reports:
            if item['status'] == 'RUNNING':
                item['status'] = 'STOPPED_FIRST_FAILURE'
            elif item['status'] == 'NOT_RUN':
                item['status'] = 'CANCELLED_AFTER_FIRST_FAILURE'
    finally:
        ledger.handle.close()
    summary = {'status': status, 'registered_starts': reports, 'total_objective_evaluations': ledger.total,
               'baseline_objective_evaluations': 0 if base is None else base.count,
               'maximum_objective_evaluations': 1801, 'best_observed': ledger.best,
               'runtime': runtime, 'wall_seconds': time.perf_counter() - started,
               'cpu_seconds': time.process_time() - cpu, 'source_sha256': digest(__file__),
               'records_sha256': digest(ledger.output / 'evaluations.jsonl'), 'first_failure': failure,
               'universal_theorem_proved': False, 'optimizer_advantage_claimed': False,
               'QPU_calls': 0, 'Perceval_calls': 0, 'certificate_attempts': int(certificate is not None)}
    for name, data in (('summary.json', summary), ('certificate.json', certificate), ('failure.json', failure)):
        payload = encoded(data)
        if ledger.bytes + len(payload) > MAX_SCIENTIFIC_BYTES:
            raise RuntimeError('scientific output byte cap')
        with (ledger.output / name).open('xb') as handle:
            handle.write(payload)
        ledger.bytes += len(payload)
    return 0 if status in ('COUNTEREXAMPLE_CERTIFIED', 'NO_COUNTEREXAMPLE_IN_REGISTERED_SEARCH') else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    path = args.output.resolve()
    if path == ROOT or not path.is_relative_to(ROOT):
        raise ValueError('output must be a fresh worktree subdirectory')
    cli_profile()
    return run(path)


if __name__ == '__main__':
    raise SystemExit(main())
