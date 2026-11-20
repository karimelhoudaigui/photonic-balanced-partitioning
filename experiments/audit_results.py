#!/usr/bin/env python3
"""Read-only scientific data checks, with historical Git source validation."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        sha=hashlib.sha256()
        for chunk in iter(lambda:stream.read(1024*1024),b''):sha.update(chunk)
    return sha.hexdigest()


def main():
    provenance=[];checks=[]
    for manifest in sorted((ROOT/'experiments').glob('*/manifest.json')):
        value=json.loads(manifest.read_text());commit=value['repository']['commit']
        evidence=[]
        for artifact in value['input_artifacts']:
            path=artifact['path'];expected=artifact['sha256']
            assert artifact['sha256_after']==expected,(manifest,path,'changed during execution')
            if (ROOT/path).exists() and digest(ROOT/path)==expected:
                evidence.append(dict(path=path,verified='current source'))
            else:
                historic=subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=ROOT)
                assert hashlib.sha256(historic).hexdigest()==expected,(manifest,path,'not preserved in Git')
                evidence.append(dict(path=path,verified=f'historical Git {commit}'))
        for artifact in value['outputs']:
            assert digest(ROOT/artifact['path'])==artifact['sha256'],(manifest,'output hash mismatch')
        provenance.append(dict(manifest=str(manifest.relative_to(ROOT)),status=value['run']['status'],
                               commit=commit,inputs=evidence,outputs_verified=len(value['outputs'])))
    # Exact-budget data: inspect every trace, not just published summaries.
    count=attempts=all_found=0;models={}
    for line in (ROOT/'experiments/E05b_exact_equal_budget/runs.jsonl').open():
        r=json.loads(line);count+=1;attempts+=r['total_shots']
        assert len(r['trace'])==r['n_evaluations']==120
        assert r['training_shots']==30720 and r['heldout_shots']==4096 and r['total_shots']==34816
        assert all(sum(t['counts'])==256 for t in r['trace'])
        assert sum(r['heldout_counts'])==4096
        assert sum(t['optimal_count'] for t in r['trace'])==r['training_optimal_count']
        assert sum(t['feasible_count'] for t in r['trace'])==r['training_feasible_count']
        assert all(0<=t['optimal_count']<=t['feasible_count']<=256 for t in r['trace'])
        first=r['first_optimum_attempt']
        if first is not None:
            assert 1<=first<=r['total_shots']
            if first<=30720:
                block=(first-1)//256
                assert all(t['optimal_count']==0 for t in r['trace'][:block])
                assert r['trace'][block]['optimal_count']>0
        all_found+=r['training_optimal_count']>0
        assert r['best_valid_cost']>=r['optimum']-1e-8
        assert r['final_p_success']<=r['final_p_feasible']+1e-10
        key=(r['n'],r['family'],r['instance'],r['seed'])
        models.setdefault(key,[]).append((r['model'],r['lambda_value']))
    assert count==756 and attempts==26320896 and len(models)==108
    assert all(len(v)==7 for v in models.values())
    checks.append(dict(experiment='E05b',model_runs=count,simulated_attempts=attempts,
                       all_model_runs_found_optimum_during_training=all_found,
                       exact_budget_and_trace_invariants='PASS'))
    # Same-circuit physical success must obey CF factorization for every ideal trace.
    traces=0;oracle_runs=0
    for name in ['E02_ideal_optimization','E03_objectives_pareto','E04_optimizers_depths','E07_spectral_hybrid']:
        for line in (ROOT/'experiments'/name/'runs.jsonl').open():
            r=json.loads(line)
            for item in r['trace']:
                m=item['exact'];traces+=1
                assert -1e-10<=m['p_success']<=m['p_cf']+1e-10<=1+2e-10
                if m['p_opt_given_cf'] is not None:
                    assert abs(m['p_success']-m['p_cf']*m['p_opt_given_cf'])<1e-10
            if r['objective']=='success':
                oracle_runs+=1
                assert r['after']['p_success']>=r['before']['p_success']-1e-10
    checks.append(dict(ideal_trace_evaluations=traces,oracle_monotonic_runs=oracle_runs,
                       probability_bounds_and_factorization='PASS'))
    output=dict(status='PASS',provenance=provenance,scientific_checks=checks,
                limitations=['Failed original E06 is retained as a failed run, not evidence of theorem failure',
                             'Hashes and finite consistency checks do not establish novelty or algorithm advantage'])
    (ROOT/'reports/RESULTS_AUDIT.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',manifests=len(provenance),checks=checks),indent=2))


if __name__=='__main__': main()
