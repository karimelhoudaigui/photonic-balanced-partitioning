"""Authenticated ObliQ static-anchor component, with explicit variant labels.

This reproduces only the static pair kernel, not ObliQ's variational training,
anchor-source selection or classical prefix decoder. The archive's half-angle
is preserved in ``literal_archive``. ``corrected_physics`` doubles its Rx API
parameter to realize the paper's initial two-photon coincidence identity.
There is no remote processor or QPU access in this module.
"""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
import math
from numbers import Integral
from pathlib import Path
import platform
from types import SimpleNamespace
import zipfile

import numpy as np

AUTHENTICATED_ZIP_SHA256 = '8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948'
VARIANTS = ('literal_archive', 'corrected_physics')
NORMALIZATIONS = ('global', 'offdiag_extension')


def _symmetric_matrix(matrix):
    q = np.asarray(matrix, dtype=float)
    if q.ndim != 2 or q.shape[0] != q.shape[1] or len(q) < 2:
        raise ValueError('Expected a square matrix of size at least two')
    if not np.all(np.isfinite(q)) or not np.allclose(q, q.T, atol=1e-12, rtol=0):
        raise ValueError('Expected finite real symmetric coefficients')
    return q


def penalty_qubo(adjacency, lam, k=None):
    """Return Q, constant with cut+lambda(weight-k)^2 = x.T Q x+constant."""
    a = _symmetric_matrix(adjacency)
    m = len(a)
    k = m//2 if k is None else k
    if (not isinstance(k, Integral) or not 0 <= k <= m or not np.isfinite(lam) or lam < 0
            or np.any(a < 0) or not np.allclose(np.diag(a), 0, atol=1e-12, rtol=0)):
        raise ValueError('Require nonnegative simple adjacency, lambda>=0, integer 0<=k<=m')
    q = float(lam)*np.ones_like(a)-a
    np.fill_diagonal(q, a.sum(axis=1)+float(lam)*(1-2*k))
    return q, float(lam)*k*k


def normalize_qubo(qubo, normalization='global'):
    """Coupling construction only. The objective must retain the ORIGINAL Q.

    Global entrywise min-max is literal-archive behavior. Off-diagonal-only
    min-max is an explicitly labeled extension and does not normalize the loss.
    """
    q = _symmetric_matrix(qubo)
    if normalization not in NORMALIZATIONS:
        raise ValueError('Unknown normalization')
    if normalization == 'global':
        low, high = float(q.min()), float(q.max())
        return np.zeros_like(q) if high == low else (q-low)/(high-low)
    mask = ~np.eye(len(q), dtype=bool)
    low, high = float(q[mask].min()), float(q[mask].max())
    result = np.zeros_like(q)
    if high != low:
        result[mask] = (q[mask]-low)/(high-low)
    return result


def rx_beamsplitter(beta):
    """Perceval Rx, all auxiliary phases zero: diagonal cos(beta/2)."""
    if not np.isfinite(beta):
        raise ValueError('Expected finite Rx API angle')
    c, s = np.cos(beta/2), np.sin(beta/2)
    return np.array([[c, 1j*s], [1j*s, c]], dtype=complex)


def coupling_angle(coupling, repeats=10, variant='literal_archive'):
    if (not isinstance(repeats, Integral) or isinstance(repeats, bool) or repeats < 1
            or not np.isfinite(coupling) or not 0 <= coupling <= 1 or variant not in VARIANTS):
        raise ValueError('Require normalized coupling in [0,1], integer R>=1 and an explicit valid variant')
    angle = float(np.arccos(np.sqrt(1-float(coupling)/int(repeats)**2)))
    return .5*angle if variant == 'literal_archive' else angle


def _fock_amplitudes(unitary, occupation, max_states):
    """Independent creation-operator recurrence, with input/output factorials.

    This is exact ideal finite Fock simulation in floating arithmetic. It does
    not compute a normalized/postselected surrogate. Repeated input creation
    operators are divided by sqrt(1),sqrt(2),...,sqrt(s_a).
    """
    u = np.asarray(unitary, dtype=complex)
    m = len(u)
    occupation = tuple(occupation)
    if (len(occupation) != m or any(not isinstance(c, Integral) or c < 0 for c in occupation)):
        raise ValueError('Occupation must have m nonnegative integer entries')
    photons = sum(occupation)
    dimension = math.comb(m+photons-1, photons)
    if dimension > max_states:
        raise ValueError(f'Full Fock simulation capped at {max_states} states; requested {dimension}')
    amplitudes = {(0,)*m: 1.+0j}
    for source, count in enumerate(occupation):
        for inserted in range(1, count+1):
            updated = {}
            for state, amplitude in amplitudes.items():
                for target in range(m):
                    new_state = list(state)
                    new_state[target] += 1
                    factor = u[target, source]*math.sqrt(new_state[target]/inserted)
                    key = tuple(new_state)
                    updated[key] = updated.get(key, 0j)+amplitude*factor
            amplitudes = updated
    norm = sum(abs(amplitude)**2 for amplitude in amplitudes.values())
    if abs(norm-1) > 1e-9:
        raise ArithmeticError(f'Raw full Fock norm failed: {norm}')
    return amplitudes


class OpticalPenaltyAnchor:
    """Static optical coupling kernel with fixed serialized unordered-pair order.

    The default is lexicographic pair order, an explicit reproducibility choice.
    To reproduce a particular archive runtime's list(set(...)) pass that exact
    serialized list as pair_order. Matrix entries are U[output,input].
    """
    def __init__(self, qubo, repeats=10, variant='literal_archive', normalization='global', pair_order=None):
        self.qubo = _symmetric_matrix(qubo).copy()
        self.m = len(self.qubo)
        if variant not in VARIANTS or normalization not in NORMALIZATIONS:
            raise ValueError('Unknown variant or normalization')
        coupling_angle(0., repeats, variant)
        self.repeats, self.variant, self.normalization = int(repeats), variant, normalization
        expected = tuple(combinations(range(self.m), 2))
        order = expected if pair_order is None else tuple(tuple(pair) for pair in pair_order)
        if len(order) != len(expected) or set(order) != set(expected):
            raise ValueError('pair_order must contain every i<j pair exactly once')
        self.pair_order = order
        self.couplings = normalize_qubo(self.qubo, normalization)
        self.pair_order_sha256 = hashlib.sha256(json.dumps(order, separators=(',', ':')).encode()).hexdigest()

    def _unitary_from(self, couplings):
        u = np.eye(self.m, dtype=complex)
        for _ in range(self.repeats):
            for i, j in self.pair_order:
                gate = rx_beamsplitter(coupling_angle(couplings[i, j], self.repeats, self.variant))
                u[[i, j], :] = gate @ u[[i, j], :]
        return u

    def unitary(self):
        return self._unitary_from(self.couplings)

    def graph_blind_limit(self):
        """Same order/variant/repeats with all off-diagonal couplings equal one."""
        return self._unitary_from(np.ones((self.m, self.m)))

    def to_perceval(self):
        """Local circuit, with archive-style permutation routing of nonadjacent pairs."""
        import perceval as pcvl
        circuit = pcvl.Circuit(self.m)
        for _ in range(self.repeats):
            for i, j in self.pair_order:
                beta = coupling_angle(self.couplings[i, j], self.repeats, self.variant)
                if j != i+1:
                    permutation = list(range(self.m))
                    permutation[j], permutation[i+1] = i+1, j
                    circuit.add(tuple(range(self.m)), pcvl.PERM(permutation))
                circuit.add((i, i+1), pcvl.BS.Rx(theta=beta))
                if j != i+1:
                    circuit.add(tuple(range(self.m)), pcvl.PERM(permutation))
        return circuit

    def fock_probabilities(self, occupation=None, max_states=10000):
        """Unconditioned complete distribution. Static source defaults to N=m."""
        source = (1,)*self.m if occupation is None else tuple(occupation)
        amplitudes = _fock_amplitudes(self.unitary(), source, max_states)
        return {state: float(abs(amplitude)**2) for state, amplitude in sorted(amplitudes.items())}

    def threshold_probabilities(self, occupation=None, max_states=10000):
        result = {}
        for state, probability in self.fock_probabilities(occupation, max_states).items():
            binary = tuple(int(c > 0) for c in state)
            result[binary] = result.get(binary, 0.)+probability
        return result

    def expected_original_qubo(self, occupation=None, max_states=10000):
        """Original x.T Q x, no min-max transformed loss or prefix decoding."""
        return float(sum(probability*(np.asarray(x) @ self.qubo @ np.asarray(x))
                         for x, probability in self.threshold_probabilities(occupation, max_states).items()))


def _archive_builder_comparison(archive_path):
    """Execute ONLY the authenticated static build_circuit function, not its program.

    The exact archive hash is checked before AST extraction. No imports,
    forward methods, processors, storage clients or external optimizer run.
    """
    import perceval as pcvl
    path = Path(archive_path)
    if hashlib.sha256(path.read_bytes()).hexdigest() != AUTHENTICATED_ZIP_SHA256:
        raise ValueError('Archive SHA256 does not match the authenticated ObliQ artifact')
    with zipfile.ZipFile(path) as archive:
        source = archive.read('ObliQ/circ_init.py')
    tree = ast.parse(source.decode())
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'PhotoCircuit')
    builder = next(node for node in cls.body if isinstance(node, ast.FunctionDef) and node.name == 'build_circuit')
    isolated = ast.Module(body=[builder], type_ignores=[])
    namespace = {'np': np, 'pcvl': pcvl, 'BS': pcvl.BS, 'comp': SimpleNamespace(PERM=pcvl.PERM),
                 '__builtins__': {'print': lambda *args: None, 'range': range, 'list': list, 'tuple': tuple}}
    exec(compile(isolated, 'authenticated_ObliQ_build_circuit_only', 'exec'), namespace)
    order = tuple(list({(i, j) for i in range(4) for j in range(i+1, 4)}))
    rows = []
    for seed in [1901, 1902, 1903]:
        q = np.random.default_rng(seed).uniform(-2, 2, (4, 4))
        q = np.triu(q, 1); q += q.T
        for repeats in [1, 2, 10]:
            original = namespace['build_circuit'](SimpleNamespace(size=4, num_rep=repeats), q, None)
            own = OpticalPenaltyAnchor(q, repeats, pair_order=order)
            original_u = np.asarray(original.compute_unitary(), dtype=complex)
            matrix_error = float(np.max(abs(original_u-own.unitary())))
            backend = pcvl.SLOSBackend()
            backend.set_circuit(original)
            backend.set_input_state(pcvl.BasicState([1]*4))
            reference = backend.prob_distribution()
            custom = own.fock_probabilities()
            p_error = max(abs(p-reference.get(pcvl.BasicState(t), 0.)) for t, p in custom.items())
            rows.append(dict(seed=seed, repeats=repeats, max_unitary_error=matrix_error,
                             max_full_fock_probability_error=float(p_error), full_fock_outcomes=len(custom)))
    return dict(archive_sha256=AUTHENTICATED_ZIP_SHA256,
                builder_source_sha256=hashlib.sha256(source).hexdigest(), serialized_pair_order=order,
                pair_order_sha256=OpticalPenaltyAnchor(np.zeros((4, 4)), pair_order=order).pair_order_sha256, cases=rows)


def component_validation(archive_path=None):
    """Bounded audit data for this new component, no optimization/hardware claim."""
    import importlib.metadata
    import perceval as pcvl
    started = datetime.now(timezone.utc).isoformat()
    module_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    local = []
    for a in [0., .25, .5, .75, 1.]:
        q = np.array([[0., a], [a, 1.]])
        for variant in VARIANTS:
            anchor = OpticalPenaltyAnchor(q, repeats=1, variant=variant)
            custom = anchor.fock_probabilities()
            circuit = anchor.to_perceval()
            backend = pcvl.SLOSBackend(); backend.set_circuit(circuit)
            backend.set_input_state(pcvl.BasicState([1, 1]))
            reference = backend.prob_distribution()
            beta = coupling_angle(a, 1, variant)
            p11 = custom[(1, 1)]
            analytic = .5*(1+math.sqrt(1-a)) if variant == 'literal_archive' else 1-a
            local.append(dict(coupling=a, variant=variant, beta=beta, coincidence=p11,
                              intended_coincidence=1-a, analytic_coincidence=analytic,
                              raw_fock_distribution=[dict(occupation=t, probability=p) for t, p in custom.items()],
                              max_perceval_error=float(max(abs(p-reference.get(pcvl.BasicState(t), 0.)) for t, p in custom.items()))))
    adjacency = np.zeros((4, 4))
    for i, j, weight in [(0, 1, 1.), (1, 2, 2.), (2, 3, 1.), (3, 0, 2.)]:
        adjacency[i, j] = adjacency[j, i] = weight
    convergence = []
    for variant in VARIANTS:
        for repeats in [1, 2, 10]:
            control_u = None
            for lam in [4., 16., 64., 256., 1024., 4096., 16384., 65536.]:
                q, _ = penalty_qubo(adjacency, lam)
                anchor = OpticalPenaltyAnchor(q, repeats, variant)
                u, limit = anchor.unitary(), anchor.graph_blind_limit()
                p = anchor.fock_probabilities()
                limit_amplitudes = _fock_amplitudes(limit, (1,)*4, 10000)
                limit_p = {t: float(abs(amplitude)**2) for t, amplitude in limit_amplitudes.items()}
                control = OpticalPenaltyAnchor(q, repeats, variant, 'offdiag_extension').unitary()
                if control_u is None:
                    control_u = control
                control_change = float(np.linalg.norm(control-control_u, 2))
                tv = float(.5*sum(abs(probability-limit_p[t]) for t, probability in p.items()))
                threshold, threshold_limit = {}, {}
                for t in p:
                    x = tuple(int(c > 0) for c in t)
                    threshold[x] = threshold.get(x, 0.)+p[t]
                    threshold_limit[x] = threshold_limit.get(x, 0.)+limit_p[t]
                tv_threshold = float(.5*sum(abs(prob-threshold_limit[x]) for x, prob in threshold.items()))
                convergence.append(dict(variant=variant, repeats=repeats, lam=lam,
                                        unitary_distance=float(np.linalg.norm(u-limit, 2)), full_fock_tv=tv,
                                        threshold_tv=tv_threshold, p_weight_two=float(sum(prob for x, prob in threshold.items() if sum(x)==2)),
                                        offdiag_control_unitary_change=control_change,
                                        lex_pair_order_sha256=anchor.pair_order_sha256))
    result = dict(started_utc=started, ended_utc=datetime.now(timezone.utc).isoformat(),
                  module_sha256=module_hash, python=platform.python_version(),
                  versions={name: importlib.metadata.version(name) for name in ['numpy', 'scipy', 'perceval-quandela', 'exqalibur']},
                  local_coincidence_cases=local, convergence_cases=convergence,
                  source_state=[1, 1, 1, 1], photon_number=4,
                  graph_adjacency=adjacency.tolist(), no_prefix_decoder=True,
                  archive_builder=None if archive_path is None else _archive_builder_comparison(archive_path),
                  non_claims=['Static kernel only, not the full ObliQ optimizer', 'Angle mismatch is already identified by the authenticated specification',
                              'Convergence sweep is one weighted-regular graph, not a scaling theorem', 'No QPU, noise or optimization advantage result'])
    assert module_hash == hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate-archive', type=Path, default=None)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = component_validation(args.validate_archive)
    serialized = json.dumps(result, indent=2)+'\n'
    if args.output is None:
        print(serialized, end='')
    else:
        args.output.write_text(serialized)
        print(json.dumps(dict(output=str(args.output), sha256=hashlib.sha256(serialized.encode()).hexdigest(),
                              local_cases=len(result['local_coincidence_cases']), convergence_cases=len(result['convergence_cases']),
                              archive_cases=0 if result['archive_builder'] is None else len(result['archive_builder']['cases'])), indent=2))


if __name__ == '__main__':
    main()
