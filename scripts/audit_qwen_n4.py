#!/usr/bin/env python3
"""Independently check the fixed n4 Qwen diagnostic; never promote a claim."""
import argparse
import datetime as dt
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np
import perceval as pcvl
import scipy

from photonic_balanced_partitioning.photonic.mesh import RectangularMesh


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(paths, output):
    output.mkdir(parents=True, exist_ok=False)
    root = Path(__file__).resolve().parents[1]
    relative = lambda p: str(p.resolve().relative_to(root))
    sources = [Path(__file__), root/'scripts/qwen_n4_probe.py',
               root/'src/photonic_balanced_partitioning/photonic/mesh.py'] + paths
    before = {str(p): digest(p) for p in sources}
    started = dt.datetime.now(dt.timezone.utc).isoformat(); clock = time.monotonic()
    mesh = RectangularMesh(4); partitions = list(combinations(range(4), 2))
    graphs={'path':[[0,1,1.],[1,2,1.],[2,3,1.]],
            'cycle':[[0,1,1.],[1,2,1.],[2,3,1.],[3,0,1.]],
            'weighted':[[0,1,.7],[0,2,1.2],[1,3,.9],[2,3,1.6]]}
    comparisons = []; all_seeds = []; checked = 0; max_error = 0.; max_pcvl_error = 0.
    for index, path in enumerate(paths):
        raw = json.loads(path.read_text()); rows = raw['rows']
        offset = 100*index
        expected_seeds = {20261121+offset, 20261122+offset, 20261123+offset}
        assert len(rows) == 18 and raw['physical_shots'] == 0
        assert raw['source_sha256'] == before[str(root/'scripts/qwen_n4_probe.py')]
        assert raw['hom_p_cf'] < 1e-12
        assert {(r['family'],r['model'],r['seed']) for r in rows} == {
            (f,m,s) for f in ['path','cycle','weighted']
            for m in ['bosonic','distinguishable'] for s in expected_seeds}
        all_seeds.append(expected_seeds)
        for row in rows:
            assert row['edges'] == graphs[row['family']]
            # Independent graph cut enumeration, not CollisionFreeEvaluator.
            costs = np.array([sum(w for i,j,w in row['edges'] if (i in subset)!=(j in subset))
                              for subset in partitions])
            optimum = costs.min()
            assert abs(row['optimum_diagnostic']-optimum) < 1e-12
            assert abs(row['uniform_feasible_success']-np.isclose(costs,optimum,atol=1e-9,rtol=0).mean()) < 1e-12
            assert row['n_evaluations'] == len(row['history']) == 32
            initial = np.random.default_rng(row['seed']).uniform(-np.pi,np.pi,mesh.num_parameters-4)
            assert np.array_equal(initial, row['history'][0]['parameters'])
            assert row['initial'] == row['history'][0]['metrics']
            best_index = int(np.argmin([h['loss'] for h in row['history']]))
            assert row['final'] == row['history'][best_index]['metrics']
            for history in row['history']:
                u = mesh.unitary(np.r_[history['parameters'],np.zeros(4)])
                probs = []
                for i,j in partitions:
                    if row['model']=='bosonic':
                        p = abs(u[i,0]*u[j,1]+u[j,0]*u[i,1])**2
                    else:
                        p = abs(u[i,0]*u[j,1])**2+abs(u[j,0]*u[i,1])**2
                    probs.append(p)
                probs = np.array(probs); p_cf=float(probs.sum())
                success=float(probs[np.isclose(costs,optimum,atol=1e-9,rtol=0)].sum())
                energy=float(probs@costs/p_cf)
                independent={'p_cf':p_cf,'p_success':success,'p_opt_given_cf':success/p_cf,
                             'conditional_energy':energy,'unconditional_cf_energy':float(probs@costs),
                             'expected_shots':1/success if success else None}
                assert 0 <= success <= p_cf+1e-12 <= 1+1e-10
                for key,value in independent.items():
                    actual=history['metrics'][key]
                    if value is None:assert actual is None
                    else:
                        error=abs(actual-value);max_error=max(max_error,error)
                        assert error < 1e-9*max(1.,abs(value)), (key,error)
                assert abs(history['loss']-(energy+2*(1-p_cf))) < 1e-10
                if row['model']=='bosonic' and history is row['history'][best_index]:
                    backend=pcvl.SLOSBackend();backend.set_circuit(pcvl.Unitary(pcvl.Matrix(u)))
                    backend.set_input_state(pcvl.BasicState([1,1,0,0]))
                    reference=backend.prob_distribution()
                    assert abs(sum(reference.values())-1) < 1e-10
                    for subset,p in zip(partitions,probs):
                        occupation=[int(i in subset) for i in range(4)]
                        error=abs(p-reference.get(pcvl.BasicState(occupation),0))
                        max_pcvl_error=max(max_pcvl_error,error);assert error < 1e-10
                checked+=1
        for family in ['path','cycle','weighted']:
            group={m:[r for r in rows if r['family']==family and r['model']==m]
                   for m in ['bosonic','distinguishable']}
            means={m:float(np.mean([r['final']['p_success'] for r in group[m]])) for m in group}
            comparisons.append(dict(batch=index,family=family,seeds=sorted(expected_seeds),
                bosonic_success_mean=means['bosonic'],distinguishable_success_mean=means['distinguishable'],
                paired_bosonic_minus_distinguishable=means['bosonic']-means['distinguishable'],
                uniform_feasible_success=group['bosonic'][0]['uniform_feasible_success']))
    assert len(all_seeds)==2 and not all_seeds[0]&all_seeds[1]
    assert before == {str(p):digest(p) for p in sources}
    result=dict(status='FINITE_ASSERTION_VERIFIED',hypothesis_decision='INCONCLUSIVE',
        histories_checked=checked,raw_runs=36,objective_evaluations=1152,
        best_bosonic_circuits_cross_validated_against_perceval=18,
        maximum_metric_absolute_error=max_error,maximum_perceval_probability_error=max_pcvl_error,
        comparisons=comparisons,
        limitations=['Fixed three graphs and six seeds only; no population inference or intervals.',
                     'Equal exact objective-call budgets do not establish equal physical-shot or total classical cost.',
                     'n4 exact feasible enumeration costs only six cut evaluations.',
                     'No novelty, general no-go theorem, computational advantage, noise or hardware claim.'])
    result_path=output/'audit.json';result_path.write_text(json.dumps(result,indent=2)+'\n')
    manifest=dict(schema_version=2,claim_id='QWEN-N4-DIAGNOSTIC',
        repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),
                        dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip())),
        command=[str(root/'.venv/bin/python'),str(Path(__file__).relative_to(root)),
                 '--initial',str(paths[0]),'--replication',str(paths[1]),'--output',str(output)],
        environment=dict(software=[dict(name='python',version=platform.python_version()),
            dict(name='numpy',version=np.__version__),dict(name='scipy',version=scipy.__version__),
            dict(name='perceval',version=pcvl.__version__)],hardware='Apple M2, 8GiB unified RAM, macOS arm64'),
        mathematics=dict(assertion_tested='Every recorded two-photon probability, loss and selected iterate is consistent with independent n4 formulas; best bosonic distributions match Perceval.',
            coefficient_domain='complex128 and float64',conventions='Input |1,1,0,0>; rows are output modes; all collision-free probabilities retain physical mass.',
            inputs=[str(p) for p in paths],bounds=dict(n=4,k=2,graphs=3,seeds=6,models=2,evaluations_per_run=32),
            non_claims=result['limitations']),randomness=dict(used=True,generator='numpy.default_rng/PCG64',seed=sorted(set.union(*all_seeds))),
        run=dict(started_at=started,runtime_seconds=time.monotonic()-clock,exit_status=0,status='completed',
            resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),
        outputs=[dict(path=relative(result_path),sha256=digest(result_path),kind='result')],
        checks=['independent two-photon formulas','all 1152 recorded parameter evaluations',
                'graph cuts and seed starts','best-loss selection','18 Perceval SLOS distributions',
                'fresh disjoint seeds','unchanged input hashes'],
        result='Finite recorded calculations verified; useful interference-dependent optimization remains INCONCLUSIVE.',
        residual_risks=result['limitations'],
        input_artifacts=[dict(path=relative(p),sha256=before[str(p)],sha256_after=digest(p)) for p in sources],
        declared_results=[relative(result_path)])
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--initial',type=Path,required=True)
    parser.add_argument('--replication',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();audit([args.initial,args.replication],args.output)
