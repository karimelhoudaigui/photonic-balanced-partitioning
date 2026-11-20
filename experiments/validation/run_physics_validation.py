"""Executed validation gate, with full distributions and reproducibility hashes.

Run from repository root:
MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/validation/run_physics_validation.py
Only local SLOS is used; no processor, authentication, or remote backend.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import perceval as pcvl

from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'experiments/validation'
INPUTS = [Path(__file__).relative_to(ROOT), Path('src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py')]


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def main():
    declared_results = ['experiments/validation/full_fock_distributions.json', 'experiments/validation/summary.json']
    started = datetime.now(timezone.utc).isoformat()
    tic = time.monotonic()
    hashes_before = {str(p): sha(p) for p in INPUTS}
    records = []
    probability_error = amplitude_error = norm_error = 0.
    random_circuit_count = 0
    for n, k in [(2, 1), (2, 2), (4, 2), (4, 3), (6, 3), (8, 4)]:
        solver = FixedPhotonObliq(n, k)
        for j in range(10):
            seed = 23000 + 100 * n + j
            u = solver.random_interferometer(seed=seed)
            random_circuit_count += 1
            for input_label, s in [('cf', tuple([1] * k + [0] * (n - k))),
                                   ('bunched', tuple([k] + [0] * (n - 1)))]:
                record, pe, ae, ne = validate_case(solver, u, s)
                record.update(seed=seed, input_label=input_label)
                records.append(record)
                probability_error = max(probability_error, pe)
                amplitude_error = max(amplitude_error, ae)
                norm_error = max(norm_error, ne)
    # Named analytic checks are explicitly cross-validated as well.
    analytic_cases = [
        ('identity', 4, 2, np.eye(4, dtype=complex), (1, 1, 0, 0)),
        ('permutation', 4, 2, np.eye(4, dtype=complex)[:, [3, 0, 2, 1]], (1, 1, 0, 0)),
        ('phase', 4, 3, np.diag(np.exp(1j * np.array([.17, -.3, .61, .8]))), (1, 1, 1, 0)),
        ('HOM', 2, 2, np.array([[1, -1], [1, 1]], complex) / np.sqrt(2), (1, 1)),
        ('vacuum', 2, 0, np.eye(2, dtype=complex), (0, 0)),
    ]
    for name, n, k, u, s in analytic_cases:
        record, pe, ae, ne = validate_case(FixedPhotonObliq(n, k), u, s)
        record.update(seed=None, input_label=name)
        records.append(record)
        probability_error = max(probability_error, pe)
        amplitude_error = max(amplitude_error, ae)
        norm_error = max(norm_error, ne)
    raw_path = OUT / 'full_fock_distributions.json'
    raw_path.write_text(json.dumps(records, indent=2) + '\n')
    tolerance = 1e-10
    hashes_after = {str(p): sha(p) for p in INPUTS}
    passed = max(probability_error, amplitude_error, norm_error) < tolerance and hashes_before == hashes_after
    summary = dict(
        assertion_tested='Raw full Fock probabilities AND complex amplitudes equal local Perceval SLOS, with normalization.',
        status='PASS' if passed else 'FAIL',
        started_utc=started, ended_utc=datetime.now(timezone.utc).isoformat(), runtime_seconds=time.monotonic()-tic,
        git_commit=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        git_dirty=subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).splitlines(),
        input_hashes_before=hashes_before, input_hashes_after=hashes_after,
        output_hashes={str(raw_path.relative_to(ROOT)): sha(raw_path.relative_to(ROOT))},
        python=platform.python_version(), platform=platform.platform(),
        versions={name: importlib.metadata.version(name) for name in ['numpy', 'scipy', 'perceval-quandela', 'exqalibur', 'pytest']},
        random_circuits=random_circuit_count, input_circuit_cases=len(records),
        fock_outcomes=sum(len(r['outputs']) for r in records),
        max_probability_error=probability_error, max_complex_amplitude_error=amplitude_error,
        max_raw_norm_error=norm_error, tolerance=tolerance,
        argv='MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/validation/run_physics_validation.py',
        non_claims=['No hardware executed', 'No losses or partial distinguishability modeled', 'Finite floating-point validation, not an asymptotic theorem'],
    )
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    manifest = {
        'schema_version': 2, 'claim_id': 'PHYSICS_PERCEVAL_SMALL_IDEAL',
        'repository': {'commit': summary['git_commit'], 'dirty': bool(summary['git_dirty'])},
        'command': summary['argv'],
        'environment': {'software': [{'name': 'Python', 'version': summary['python']}] +
                        [{'name': key, 'version': value} for key, value in summary['versions'].items()],
                        'hardware': summary['platform']},
        'mathematics': {'assertion_tested': summary['assertion_tested'],
                        'coefficient_domain': 'Complex IEEE binary64 amplitudes and real binary64 probabilities',
                        'conventions': 'Output rows, input columns; Per(U[t,s])/sqrt(prod(s_i!) prod(t_j!)); no amplitude renormalization',
                        'inputs': ['60 seeded Haar matrices; two Fock inputs per matrix', 'five named analytic input/circuit cases'],
                        'bounds': {'modes': [2, 4, 6, 8], 'max_photons': 4, 'cases': 125, 'tolerance': tolerance},
                        'non_claims': summary['non_claims']},
        'randomness': {'used': True, 'generator': 'numpy.random.default_rng PCG64 complex Gaussian QR',
                       'seed': '23000 + 100*m + j, j=0..9 for each (m,k) specified in script'},
        'run': {'started_at': started, 'runtime_seconds': summary['runtime_seconds'],
                'exit_status': 0 if passed else 1, 'status': 'completed' if passed else 'failed',
                'resource_limits': {'memory_bytes': None, 'cpu_seconds': None, 'max_cores': None, 'max_threads': None}},
        'outputs': [{'path': path, 'sha256': sha(path), 'kind': 'result'} for path in declared_results],
        'checks': ['All enumerated Fock outcomes including zeros', 'Raw normalization in both implementations',
                   'Complex amplitudes and probabilities; bunched and collision-free inputs',
                   'Source hashes identical before and after computation'],
        'result': f"{summary['status']}: max probability error {probability_error}; max amplitude error {amplitude_error}",
        'residual_risks': summary['non_claims'] + ['No externally enforced process resource cap; measured runtime recorded'],
        'input_artifacts': [{'path': path, 'sha256': before, 'sha256_after': hashes_after[path]}
                            for path, before in hashes_before.items()],
        'declared_results': declared_results,
    }
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    report = f'''# Perceval validation\n\nStatus: **{summary['status']}**\n\nExecuted {summary['ended_utc']} from Git `{summary['git_commit']}` plus recorded source hashes.\nLocal Perceval {summary['versions']['perceval-quandela']} SLOS backend; no remote processor, token, QPU, or postselection.\n\nThe gate compares all {summary['fock_outcomes']} Fock outcomes in {len(records)} input/circuit cases: 60 seeded Haar circuits across (m,k)=(2,1),(2,2),(4,2),(4,3),(6,3),(8,4), each with first-k single-photon input AND fully bunched input. Identity, permutation, odd-k phase, HOM and vacuum are added. Zeros are compared too.\n\n- Maximum absolute probability error: {probability_error:.6g}.\n- Maximum complex amplitude error: {amplitude_error:.6g}.\n- Maximum raw normalization error: {norm_error:.6g}.\n- Acceptance tolerance: {tolerance:g}, absolute.\n- Custom output was never renormalized.\n\nFull matrices, input occupations, output occupations, custom and SLOS complex amplitudes and probabilities: [raw distributions](../experiments/validation/full_fock_distributions.json).\nVersions, timestamps, source/output SHA256 and exact command: [summary](../experiments/validation/summary.json).\n\nReproduce:\n```sh\n{summary['argv']}\nMPLCONFIGDIR=/tmp/pasqal-matplotlib .venv/bin/python -m pytest tests/test_hom.py tests/test_permanent_normalization.py tests/test_perceval_cross_validation.py -q\n```\n\nThis PASS is an ideal small-system simulation gate only. It does not authorize QPU work or validate other objective/baseline gates. Perceval absence causes test skips, which do not satisfy this gate.\n\nAPI checked against [official SLOS documentation](https://perceval.quandela.net/docs/v1.3/reference/backends/slos.html); installation package is [perceval-quandela](https://perceval.quandela.net/docs/v1.3/getting_started.html).\n'''
    (ROOT / 'reports/PERCEVAL_VALIDATION.md').write_text(report)
    print(json.dumps({k: summary[k] for k in ['status', 'random_circuits', 'input_circuit_cases', 'fock_outcomes', 'max_probability_error', 'max_complex_amplitude_error', 'max_raw_norm_error', 'runtime_seconds']}, indent=2))
    if not passed:
        raise SystemExit(1)


def validate_case(solver, u, s):
    backend = pcvl.SLOSBackend()
    backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
    backend.set_input_state(pcvl.BasicState(s))
    ref = backend.prob_distribution()
    actual = solver.output_state(u, input_occupation=s)
    outputs = []
    pe = ae = 0.
    for t, amplitude in zip(solver._enumerate_all_fock_states(), actual):
        bs = pcvl.BasicState(t)
        probability = float(abs(amplitude) ** 2)
        ref_probability = float(ref.get(bs, 0.))
        ref_amplitude = complex(backend.prob_amplitude(bs))
        pe = max(pe, abs(probability - ref_probability))
        ae = max(ae, abs(amplitude - ref_amplitude))
        outputs.append(dict(occupation=t, custom_probability=probability, perceval_probability=ref_probability,
                            custom_amplitude=[float(amplitude.real), float(amplitude.imag)],
                            perceval_amplitude=[ref_amplitude.real, ref_amplitude.imag]))
    ne = max(abs(float(np.vdot(actual, actual).real) - 1), abs(float(sum(ref.values())) - 1))
    return dict(m=solver.n, k=solver.k, input_occupation=s, unitary_real=u.real.tolist(), unitary_imag=u.imag.tolist(), outputs=outputs), pe, ae, ne


if __name__ == '__main__':
    main()
