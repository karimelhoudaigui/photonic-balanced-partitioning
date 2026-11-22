"""Exploratory P20 continuation: distinguish a small training set from physics.

Original P20 data are preserved. Twenty train seeds and entirely new test seeds
200..219 are used. No test optimum is supplied. Run from the repository root:
MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/P20_structured_probe/run_larger_training.py
"""
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent/'larger_training'
spec=importlib.util.spec_from_file_location('p20_probe',ROOT/'experiments/phase2_structured_probe.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    sources=p.SOURCES+[Path(__file__).relative_to(ROOT)]
    before={str(path):sha(path) for path in sources}
    tic=time.monotonic();started=datetime.now(timezone.utc).isoformat()
    contract=dict(question='Does the no-interference selection survive larger training and a fresh test set?',
                  status='Exploratory continuation after initial P20, not an untouched confirmatory hypothesis.',
                  train_sizes=[8,12,16,24],test_sizes=[8,12,16,24],train_seeds=list(range(20)),
                  test_seeds=list(range(200,220)),families=p.FAMILIES,regimes=p.REGIMES,
                  parameter_grid=dict(pair_angles=p.ANGLES,interactions=p.INTERACTIONS),
                  shots_per_case_method=p.SHOTS,global_optimum_used=False,
                  selection='Training mean accepted gain normalized by total graph weight; ties prefer less collision mass.',
                  non_claims=['No QPU or noise result','No complexity advantage of fixed-size interacting blocks',
                              'No universal graph-family claim','Exact-moment tuning is simulation work, not zero-cost hardware optimization'])
    (OUT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    bank,error=p.kernel_bank()
    training,train_instances=p.prepare_cases('train',contract['train_sizes'],contract['train_seeds'])
    frozen,scores=p.train(training,bank)
    frozen_serial=[dict(r=r,regime=regime,model=model,**{k:v for k,v in bank[(r,model)][index].items() if k!='p'})
                   for (r,regime,model),index in frozen.items()]
    frozen_path=OUT/'frozen_parameters.json'
    frozen_path.write_text(json.dumps(frozen_serial,indent=2)+'\n')
    frozen_hash=sha(frozen_path.relative_to(ROOT))
    # Fresh test graphs are created only after the selected parameters are saved.
    test,test_instances=p.prepare_cases('test',contract['test_sizes'],contract['test_seeds'])
    rows=p.evaluate(test,bank,frozen)
    aggregates,differences=p.aggregate(rows)
    with (OUT/'test_metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'training_scores.json').write_text(json.dumps(scores,indent=2)+'\n')
    (OUT/'instances.json').write_text(json.dumps(train_instances+test_instances,indent=2)+'\n')
    block_data=[]
    for c in training+test:
        block_data.append(dict(graph_id=c['graph_id'],split=c['split'],regime=c['regime'],r=c['r'],
                               anchor=c['anchor']['partition'],occupied=c['proposal'].occupied,vacant=c['proposal'].vacant,
                               energies=c['label']['energies'].tolist(),gains=c['label']['gains'].tolist(),
                               anchor_energy=c['anchor']['energy'],anchor_steps=c['anchor']['steps'],
                               swap_deltas_scored=c['anchor']['swap_deltas_scored'],normalizer=c['normalizer']))
    (OUT/'blocks.json').write_text(json.dumps(block_data,indent=2)+'\n')
    after={str(path):sha(path) for path in sources}
    assert before==after
    assert frozen_hash==sha(frozen_path.relative_to(ROOT))
    command='MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/P20_structured_probe/run_larger_training.py'
    summary=dict(status='completed',started_utc=started,ended_utc=datetime.now(timezone.utc).isoformat(),
                 runtime_seconds=time.monotonic()-tic,command=command,source_hashes_before=before,source_hashes_after=after,
                 git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                 git_dirty=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).splitlines(),
                 python=platform.python_version(),platform=platform.platform(),
                 versions={name:p.importlib.metadata.version(name) for name in ['numpy','scipy','perceval-quandela']},
                 frozen_parameters=frozen_serial,frozen_parameters_sha256=frozen_hash,
                 training_graph_label_instances=len(train_instances),test_graph_label_instances=len(test_instances),
                 training_blocks=len(training),test_blocks=len(test),
                 exact_training_objective_evaluations=len(training)*45,
                 training_local_cut_labels=sum(c['label']['local_cost_labels'] for c in training),
                 evaluation_only_test_local_cut_labels=sum(c['label']['local_cost_labels'] for c in test),
                 training_anchor_swap_deltas_scored=sum(c['anchor']['swap_deltas_scored'] for c in training if c['r']==2),
                 test_anchor_swap_deltas_scored=sum(c['anchor']['swap_deltas_scored'] for c in test if c['r']==2),
                 total_test_synthetic_attempts=sum(row['physical_attempts_simulated'] for row in rows),real_qpu_shots=0,
                 max_exact_classical_replacement_error=error,aggregates=aggregates,paired_differences=differences,
                 non_claims=contract['non_claims'])
    files=['contract.json','frozen_parameters.json','test_metrics.csv','training_scores.json','instances.json','blocks.json']
    summary['output_hashes']={str((OUT/file).relative_to(ROOT)):sha((OUT/file).relative_to(ROOT)) for file in files}
    summary_path=OUT/'summary.json';summary_path.write_text(json.dumps(summary,indent=2)+'\n')
    declared=list(summary['output_hashes'])+[str(summary_path.relative_to(ROOT))]
    manifest=dict(schema_version=2,claim_id='P20_LOCAL_BLOCK_REPLICATION',
                  repository=dict(commit=summary['git_commit'],dirty=bool(summary['git_dirty'])),command=command,
                  environment=dict(software=[dict(name='Python',version=summary['python'])]+
                                   [dict(name=k,version=v) for k,v in summary['versions'].items()],hardware=summary['platform']),
                  mathematics=dict(assertion_tested='Finite local-proposal comparison, actual collision mass, accepted cut gains, and exact classical replacement.',
                                   coefficient_domain='Complex128 amplitudes and Float64 graph costs/probabilities',
                                   conventions='One photon per active occupied mode; full local Fock outputs; collisions fail an attempt; no global optimum labels.',
                                   inputs=['Predeclared six graph families, random labels, two classical anchor regimes, r=2/3 block photons'],
                                   bounds=dict(n=[8,12,16,24],train_graphs=480,test_graphs=480,train_blocks=1920,test_blocks=1920,shots_per_method_case=64),
                                   non_claims=contract['non_claims']),
                  randomness=dict(used=True,generator='numpy.random.default_rng PCG64',seed='Train graph0..19; test200..219; label,anchor,block,shot formulas pinned in source'),
                  run=dict(started_at=started,runtime_seconds=summary['runtime_seconds'],exit_status=0,status='completed',
                           resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=None)),
                  outputs=[dict(path=path,sha256=sha(Path(path)),kind='result') for path in declared],
                  checks=['Source hashes stable before/after','Parameters persisted before test labels','Disjoint train/test seeds',
                          'Collision mass retained','Independent exact classical replacement matched every local kernel'],
                  result='Actual metrics and frozen parameter selections are reported in summary.json; no universal performance claim.',
                  residual_risks=contract['non_claims']+['Repeated path/cycle seeds change labels and anchor randomness, not graph topology'],
                  input_artifacts=[dict(path=path,sha256=h,sha256_after=after[path]) for path,h in before.items()],declared_results=declared)
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:summary[k] for k in ['status','runtime_seconds','training_blocks','test_blocks','exact_training_objective_evaluations',
                                          'total_test_synthetic_attempts','max_exact_classical_replacement_error']},indent=2))
    print('Parameters',json.dumps(frozen_serial))
    for row in aggregates:
        if row['model'] in ['bosonic_fixed','pair_product_fixed','uniform_feasible','classical_best_local']:print(json.dumps(row))


if __name__=='__main__':main()
