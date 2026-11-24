"""Evidence regressions: counts, blind selection, graph units, historical pins."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reconcile_evidence',ROOT/'scripts/reconcile_experiments.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)


def tiny_run():
    events=[dict(evaluation=1,loss=1.5,parameters=[0],counts=[2,1,1],feasible_count=3,optimal_count=3,best_valid_cost_so_far=1.,first_optimum_attempt_so_far=1),
            dict(evaluation=2,loss=1.,parameters=[1],counts=[1,3,0],feasible_count=4,optimal_count=4,best_valid_cost_so_far=1.,first_optimum_attempt_so_far=1)]
    return dict(n=2,edges=[[0,1,1.]],model='bosonic',lambda_value=None,optimum=1.,trace=events,n_evaluations=2,
                training_shots=8,heldout_shots=4,total_shots=12,sample_score_lookups=12,reference_cost_table_size=3,
                training_feasible_count=7,training_optimal_count=7,parameters=[1],heldout_counts=[2,1,1],
                heldout_optimal_count=3,best_valid_cost=1.,first_optimum_attempt=1,success_ci95=m.wilson(3,4),
                final_p_success=.8,final_p_feasible=.8,final_expected_shots=1.25)


def audit(row):return m.audit_equal_run(row,budget=2,batch=4,heldout=4)

def test_reconstructs_observed_loss_and_earliest_winning_batch():
    result=audit(tiny_run());assert result['audit_pass'];assert result['first_training_success_batch']==1
    assert 'within-batch draw order not retained' in result['first_hit_validation']

@pytest.mark.parametrize('mutation', ['count','loss','selection','first_hit'])
def test_corrupted_budgets_or_oracle_selection_fail(mutation):
    row=tiny_run()
    if mutation=='count':row['trace'][0]['counts'][0]+=1
    elif mutation=='loss':row['trace'][0]['loss']=-.8
    elif mutation=='selection':row['parameters']=[0]
    else:row['first_optimum_attempt']=5
    with pytest.raises(m.AuditError):audit(row)


def test_optimizer_repeats_are_not_independent_graphs():
    rows=[dict(graph_hash='a',value=.2),dict(graph_hash='b',value=.8)]
    original,count=m.cluster_interval(rows,'value',seed=7,resamples=200)
    repeated,count2=m.cluster_interval(rows*10,'value',seed=7,resamples=200)
    assert count==count2==2;assert repeated==pytest.approx(original,abs=1e-15)
    assert m.cluster_interval(rows[:1]*30,'value')[0] is None


def test_historical_source_is_accepted_when_current_source_changed(tmp_path):
    p=tmp_path/'source.py';p.write_text('new source')
    archive=m.Archive(tmp_path);archive.blob=lambda commit,path:b'old source'
    expected=m.sha_bytes(b'old source')
    result=archive.source('historic',dict(path='source.py',sha256=expected,sha256_after=expected))
    assert result['status']=='matched_recorded_commit'
    assert result['current_snapshot_sha256']!=expected


def test_preserved_relocation_checked_by_hash_not_wrong_root_copy(tmp_path):
    (tmp_path/'old').mkdir();(tmp_path/'preserved').mkdir()
    (tmp_path/'old/raw.json').write_bytes(b'wrong')
    (tmp_path/'preserved/raw.json').write_bytes(b'preserved')
    result=m.Archive(tmp_path).output(tmp_path/'preserved/manifest.json',dict(output_directory='old'),
                                    dict(path='old/raw.json',sha256=m.sha_bytes(b'preserved')))
    assert result['status']=='verified' and result['resolved_path']=='preserved/raw.json'


def test_released_tables_retain_negative_results_and_actual_domains():
    output=ROOT/'results/validated/recovery_2026-11-24'
    if not output.exists():pytest.skip('Reconciliation has not run yet')
    summary=json.loads((output/'summary.json').read_text());e=summary['e05b']
    assert e['raw_runs']==756 and e['total_simulated_attempts']==26320896
    assert e['all_runs_audit_pass'] and len(e['groups'])==21
    assert len(e['graphs'])==36 and e['all_optima_found_during_training']
    assert {g['n'] for g in summary['haar']['groups']}=={4,6,8,10}
    for n in (4,6,8):
        b=next(g for g in e['groups'] if g['n']==n and g['model']=='bosonic')
        d=next(g for g in e['groups'] if g['n']==n and g['model']=='distinguishable')
        assert b['final_p_success_mean']<d['final_p_success_mean']
        assert b['unique_graphs']<b['runs']
    assert not summary['publication_policy']['root_P33_performance_evidence_accepted']
