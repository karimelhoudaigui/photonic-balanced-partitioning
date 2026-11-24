"""Recreate the tiny offline demo in a NEW destination. No QPU or account API."""
import argparse
import json
from pathlib import Path

import numpy as np

from photonic_balanced_partitioning.hardware import offline as h


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, help='New root directory, must not exist')
    args = parser.parse_args()
    destination = Path(args.output)
    destination.mkdir(parents=True, exist_ok=False)
    config = Path(__file__).resolve().parents[1] / 'configs/pilot_offline_n4.json'
    commands = [
        ['check_environment', '--output', str(destination/'environment')],
        ['validate_physics', '--config', str(config), '--output', str(destination/'physics')],
        ['generate_circuits', '--config', str(config), '--output', str(destination/'circuits')],
        ['simulate_reference', '--bundle', str(destination/'circuits'), '--output', str(destination/'reference')],
        ['validate_compilation', '--bundle', str(destination/'reference'), '--output', str(destination/'compiled')],
        ['prepare_qpu_job', '--bundle', str(destination/'compiled'), '--output', str(destination/'job-draft')],
    ]
    for command in commands:
        if h.main(command) != 0:
            raise RuntimeError(f'Offline stage failed: {command[0]}')
    payload, sha = h.read_bundle(destination/'reference')
    rng = np.random.default_rng(payload['config']['seed'])
    raw = {'schema': 'pbp.pnr-counts.v1', 'evidence_kind': 'local_synthetic',
           'reference_artifact_sha256': sha, 'records': [],
           'synthetic_generator': {'seed': payload['config']['seed'],
               'method': 'numpy Generator.multinomial; probabilities normalized only for floating-point drawing',
               'source': 'ideal lossless bosonic reference, not a physical acquisition'}}
    for circuit in payload['circuits']:
        probabilities = np.array(circuit['reference']['bosonic'])
        counts = rng.multinomial(1000, probabilities/probabilities.sum())
        raw['records'].append({'circuit_id': circuit['circuit_id'], 'detector': 'pnr',
            'input_occupation': circuit['input_occupation'], 'physical_attempts': 1000,
            'attempts_source': 'synthetic multinomial experiment with 1000 trials; not hardware',
            'filtering': {'kind': 'none', 'discarded_attempts': 0},
            'counts': [{'occupation': state, 'count': int(count)}
                       for state, count in zip(circuit['reference']['states'], counts)]})
    raw_path = destination/'counts-local-synthetic.json'
    raw_path.write_bytes(h.canonical(raw)+b'\n')
    if h.main(['analyze_qpu_results', '--bundle', str(destination/'reference'),
               '--results', str(raw_path), '--output', str(destination/'analysis-known-attempts')]) != 0:
        raise RuntimeError('Synthetic analysis failed')
    for record in raw['records']:
        record['physical_attempts'] = None
        record['attempts_source'] = None
        record['filtering'] = {'kind': 'min_detected_photons', 'minimum': 2, 'discarded_attempts': None}
    unknown = destination/'counts-local-synthetic-unknown-attempts.json'
    unknown.write_bytes(h.canonical(raw)+b'\n')
    if h.main(['analyze_qpu_results', '--bundle', str(destination/'reference'),
               '--results', str(unknown), '--output', str(destination/'analysis-unknown-attempts')]) != 0:
        raise RuntimeError('Unknown-denominator analysis failed')
    files = {str(p.relative_to(destination)): h.digest(p.read_bytes())
             for p in sorted(destination.rglob('*')) if p.is_file()}
    audit = {'schema': 'pbp.offline-demo.v1', 'evidence_kind': 'local_synthetic',
             'files': files, 'provenance': h.provenance(),
             'driver_sha256': h.digest(Path(__file__).read_bytes()),
             'network_used': False, 'authorization': False, 'credits_consumed': 0}
    (destination/'demo-manifest.json').write_bytes(h.canonical(audit)+b'\n')


if __name__ == '__main__':
    main()
