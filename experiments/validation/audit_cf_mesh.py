"""Independent Ryser/permutation-sum/Perceval control for the research evaluators."""
import hashlib
import json
from pathlib import Path

import numpy as np
import perceval as pcvl

from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq
from photonic_balanced_partitioning.photonic.comparison import CollisionFreeEvaluator
from photonic_balanced_partitioning.photonic.mesh import RectangularMesh

ROOT = Path(__file__).resolve().parents[2]
inputs = [Path(__file__).relative_to(ROOT)] + [Path('src/photonic_balanced_partitioning/photonic') / f for f in ['fixed_photon_obliq.py', 'mesh.py', 'comparison.py']]
hashes = {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
rows = []
for n in [4, 6, 8, 10]:
    solver = FixedPhotonObliq(n)
    evaluator = CollisionFreeEvaluator(n)
    mesh = RectangularMesh(n)
    for seed in range(10):
        for model in ['haar', 'mesh']:
            p = np.random.default_rng(seed + n * 100).normal(size=mesh.num_parameters)
            u = solver.random_interferometer(seed) if model == 'haar' else mesh.unitary(p)
            expected = solver.collision_free_probabilities(u)
            actual = evaluator.probabilities(u)
            err = float(np.max(np.abs(expected-actual)))
            assert err < 1e-10
            entry = dict(n=n, seed=seed, model=model, max_probability_error=err)
            if model == 'mesh':
                circuit = mesh.to_perceval(p)
                unitary_error = float(np.max(np.abs(np.asarray(circuit.compute_unitary(), complex) - u)))
                assert unitary_error < 1e-10
                entry['perceval_mesh_unitary_error'] = unitary_error
            rows.append(entry)
assert hashes == {str(p): hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in inputs}
result = dict(status='PASS', source_hashes=hashes, cases=rows,
              max_probability_error=max(row['max_probability_error'] for row in rows),
              max_mesh_unitary_error=max(row.get('perceval_mesh_unitary_error', 0) for row in rows),
              command='MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/validation/audit_cf_mesh.py')
(ROOT / 'experiments/validation/cf_mesh_validation.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({key:result[key] for key in ['status','max_probability_error','max_mesh_unitary_error']}, indent=2))
