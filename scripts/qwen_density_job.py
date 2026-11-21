#!/usr/bin/env python3
"""Short, fixed native-agent commands; retain the actual full scientific argv."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def run(mode):
    output='results/P33_density_'+mode
    contract_path=ROOT/'experiments/contracts/P33_density_probe.json'
    contract=json.loads(contract_path.read_text())
    command=[sys.executable,str(ROOT/'.qwen/support/run_experiment.py'),'--root',str(ROOT),
             '--contract',str(contract_path)]
    for path in contract['execution_artifacts']:command+=['--input',path]
    command+=['--output',output]
    for name in ['raw.json','summary.json','progress.jsonl']:command+=['--result',output+'/data/'+name]
    command+=['--timeout','300','--max-threads','1','--max-output-bytes','1048576','--',
              sys.executable,'experiments/phase3_density_probe.py','--seed-offset',
              '0' if mode=='primary' else '100000','--output',output+'/data']
    result=subprocess.run(command,cwd=ROOT,check=False)
    if result.returncode:return result.returncode
    print((ROOT/output/'data/summary.json').read_text())
    return 0


def audit_one(mode):
    output=ROOT/'results'/('P33_density_'+mode)
    manifest=json.loads((output/'manifest.json').read_text())
    if manifest['run']['status']!='completed':raise ValueError('Scientific command did not complete')
    subprocess.run([sys.executable,str(ROOT/'.qwen/support/validate_manifest.py'),str(output/'manifest.json'),
                    '--root',str(ROOT)],cwd=ROOT,check=True)
    raw=json.loads((output/'data/raw.json').read_text());rows=raw['full_checks']
    assert len(rows)==150 and len(raw['balanced_sharpness'])==7
    assert len(raw['scalable_certificate_only'])==36 and len(raw['dilute_counterexamples'])==6
    offset=0 if mode=='primary' else 100000
    expected={(m,family,2026112100+100*m+repeat+offset,round(float(scale/np.sqrt(m//2)),12))
              for m in [4,6,8,10,12] for family in ['global_output_mix','flat_fixed_projector']
              for repeat in range(3) for scale in [0.,.02,.06,.2,.6]}
    assert {(r['certificate']['m'],r['family'],r['seed'],round(r['strength'],12)) for r in rows}==expected
    actual_tv_error=0.;pair_error=0.
    for row in rows+raw['balanced_sharpness']:
        pb=np.array(row['bosonic_probabilities']);pd=np.array(row['distinguishable_probabilities'])
        assert abs(pb.sum()-1)<1e-9 and abs(pd.sum()-1)<1e-9
        tv=float(abs(pb-pd).sum()/2);actual_tv_error=max(actual_tv_error,abs(tv-row['actual_tv']))
        assert actual_tv_error<1e-12
        states=np.array(raw['full_fock_bases'][str(row['certificate']['m'])])
        pairs=np.sum(states*(states-1)/2,axis=1)
        error=abs(float(pb@pairs)-row['certificate']['expected_collision_pairs'])
        pair_error=max(pair_error,error);assert error<1e-9
        for name,value in row['certificate'].items():
            if name.endswith('_tv_bound'):assert tv<=value+1e-9
    assert all(r['full_distribution_executed'] is False for r in raw['scalable_certificate_only'])
    assert raw['physical_shots']==0
    return dict(mode=mode,status='FINITE_RECORDS_VERIFIED',full_grid_cases=150,sharpness_cases=7,
                scalable_cases_are_certificate_only=True,physical_shots=0,
                tv_recomputation_error=actual_tv_error,collision_moment_error=pair_error,
                seed_offset=offset,proof_acceptance='SEPARATE_INDEPENDENT_REVIEW',novelty='OPEN',
                floating_bounds='ESTIMATES_WITH_1e-9_VALIDATION_TOLERANCE_NOT_INTERVAL_CERTIFICATES',
                raw_sha256=hashlib.sha256((output/'data/raw.json').read_bytes()).hexdigest())


def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['primary','replication','audit-primary','audit-pair'])
    mode=parser.parse_args().mode
    if mode in ['primary','replication']:return run(mode)
    results=[audit_one('primary')]
    if mode=='audit-pair':
        results.append(audit_one('replication'))
        primary=json.loads((ROOT/'results/P33_density_primary/data/raw.json').read_text())
        replica=json.loads((ROOT/'results/P33_density_replication/data/raw.json').read_text())
        assert not ({r['seed'] for r in primary['full_checks']} & {r['seed'] for r in replica['full_checks']})
    report=ROOT/'reports'/('QWEN_P33_REVIEW.md' if mode=='audit-primary' else 'QWEN_P33_DISPOSITION.md')
    payload=dict(status='FINITE_CHECKS_SUPPORTED',evidence=results,
                 scientific_acceptance='PENDING_ASTRA',PAPER_READY=False,QPU_GATE='CLOSED')
    if report.exists():raise FileExistsError('Do not overwrite an earlier review')
    report.write_text('# Script-generated evidence review invoked by the native Qwen role\n\n'+
                      'Finite recorded checks only. Proof and novelty are separate obligations.\n\n```json\n'+
                      json.dumps(payload,indent=2)+'\n```\n')
    print(json.dumps(payload,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
