"""Read-only bounded audit of existing P20 outputs; never calls either campaign.

Does not call prepare_cases/train/evaluate/main, regenerate datasets, or rerun
training. Reconstructs stored arithmetic, frozen selection, and a few counts.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.util,json,platform,resource,sys,time,traceback
from pathlib import Path
START=time.perf_counter();CPU_START=time.process_time()
resource.setrlimit(resource.RLIMIT_CPU,(55,55))
ROOT=Path('/Users/karimelhoudaigui/Desktop/pasqal')
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from photonic_balanced_partitioning.photonic.structured_search import LocalBlockProposal,swap_deltas
spec=importlib.util.spec_from_file_location('_p20_audit_readonly',ROOT/'experiments/phase2_structured_probe.py')
p20=importlib.util.module_from_spec(spec);spec.loader.exec_module(p20)
BASE=ROOT/'experiments/P20_structured_probe'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def jload(p):return json.loads(p.read_text())

def boolean(x):return x=='True'

def local_energies(a,parts):
    i,j=np.triu_indices(len(a),1);w=a[i,j]
    bits=np.zeros((len(parts),len(a)),dtype=bool)
    for row,part in enumerate(parts):bits[row,list(part)]=True
    return ((bits[:,i]!=bits[:,j])*w).sum(axis=1)


def run(folder,bank):
    summary=jload(folder/'summary.json');contract=jload(folder/'contract.json')
    frozen=jload(folder/'frozen_parameters.json');scores=jload(folder/'training_scores.json')
    instances=jload(folder/'instances.json');blocks=jload(folder/'blocks.json')
    with (folder/'test_metrics.csv').open() as f:metrics=list(csv.DictReader(f))
    graphs={g['graph_id']:g for g in instances};assert len(graphs)==len(instances)
    train_ids={g['graph_id'] for g in instances if g['split']=='train'}
    test_ids={g['graph_id'] for g in instances if g['split']=='test'}
    assert not train_ids&test_ids
    assert {g['seed'] for g in instances if g['split']=='train'}==set(contract['train_seeds'])
    assert {g['seed'] for g in instances if g['split']=='test'}==set(contract['test_seeds'])
    assert not set(contract['train_seeds'])&set(contract['test_seeds'])
    assert sha(folder/'frozen_parameters.json')==summary['frozen_parameters_sha256']
    table={};max_label_error=max_anchor_error=0.;local_min_bad=0
    for b in blocks:
        key=(b['graph_id'],b['regime'],int(b['r']));assert key not in table
        g=graphs[b['graph_id']];a=np.asarray(g['adjacency'])
        assert np.isfinite(a).all() and np.min(a)>=0 and np.allclose(a,a.T) and np.all(np.diag(a)==0)
        assert sorted(g['label_permutation'])==list(range(g['n']))
        proposal=LocalBlockProposal(tuple(b['anchor']),tuple(b['occupied']),tuple(b['vacant']))
        assert all(len(S)==g['n']//2 for S in proposal.candidates)
        energies=local_energies(a,proposal.candidates);current=float(local_energies(a,[b['anchor']])[0])
        stored=np.asarray(b.get('cut_energies',b.get('energies')))
        max_label_error=max(max_label_error,float(np.max(abs(energies-stored))))
        max_anchor_error=max(max_anchor_error,abs(current-b['anchor_energy']))
        assert np.max(abs(energies-stored))<2e-9 and abs(current-b['anchor_energy'])<2e-9
        assert abs(b['normalizer']-max(float(a.sum()/2),1.))<1e-12
        scored=b.get('anchor_swap_deltas_scored',b.get('swap_deltas_scored'))
        assert scored==(b['anchor_steps']+1)*(g['n']//2)**2
        if b['regime']=='two_swaps':assert b['anchor_steps']<=2
        else:
            _,_,delta=swap_deltas(a,b['anchor'])
            local_min_bad+=int(delta.min() < -1e-9)
        table[key]=dict(block=b,energies=energies,current=current,gains=np.maximum(current-energies,0),
                        improve=energies<current-1e-10,normalizer=b['normalizer'],label_count=len(energies))
    assert local_min_bad==0
    train=[t for t in table.values() if t['block']['split']=='train']
    test=[t for t in table.values() if t['block']['split']=='test']
    assert len(train)==summary['training_blocks'] and len(test)==summary['test_blocks']
    frozen_index={};max_score_error=0.;selections=[]
    for f in frozen:
        r=f['r'];regime=f['regime'];model=f['model']
        subset=[s for s in scores if (s['r'],s['regime'],s['model'])==(r,regime,model)]
        entries=bank[(r,model)]
        assert len(subset)==len(entries)
        labels=[t for t in train if (t['block']['r'],t['block']['regime'])==(r,regime)]
        for s in subset:
            entry=entries[s['index']]
            value=float(np.mean([entry['p'][:-1]@t['gains']/t['normalizer'] for t in labels]))
            max_score_error=max(max_score_error,abs(value-s['score']))
            assert abs(value-s['score'])<2e-12
        best=max(s['score'] for s in subset)
        chosen=min((s for s in subset if s['score']>=best-1e-14),key=lambda s:(s['collision_probability'],s['index']))
        assert chosen['pair_angle']==f['pair_angle'] and chosen['interaction_angle']==f['interaction_angle']
        frozen_index[(r,regime,model)]=chosen['index']
        selections.append(dict(r=r,regime=regime,model=model,index=chosen['index'],score=chosen['score'],interaction_angle=chosen['interaction_angle']))
    assert all(f['interaction_angle']==0 for f in frozen)
    max_metric_error=0.;observed_spot_checks=0;by_key={}
    models=['bosonic_fixed','distinguishable_fixed','distinguishable_same_circuit','pair_product_fixed',
            'uniform_feasible','correlated_batch','classical_exact_replacement','classical_best_local']
    assert len(metrics)==len(test)*len(models)
    test_order=[(t['block']['graph_id'],t['block']['regime'],t['block']['r']) for t in test]
    for row in metrics:
        key=(row['graph_id'],row['regime'],int(row['r']));t=table[key];r=key[2];regime=key[1];model=row['model']
        b=bank[(r,'bosonic')][frozen_index[(r,regime,'bosonic')]]['p']
        if model in ('bosonic_fixed','classical_exact_replacement'):p=b
        elif model=='distinguishable_same_circuit':p=bank[(r,'distinguishable')][frozen_index[(r,regime,'bosonic')]]['p']
        elif model=='distinguishable_fixed':p=bank[(r,'distinguishable')][frozen_index[(r,regime,'distinguishable')]]['p']
        elif model=='pair_product_fixed':p=bank[(r,'pair')][frozen_index[(r,regime,'pair')]]['p']
        elif model in ('uniform_feasible','correlated_batch'):p=bank[(r,model)][0]['p']
        else:
            assert model=='classical_best_local';p=np.zeros(len(b));p[int(np.argmin(t['energies']))]=1
        improve=float(p[:-1][t['improve']].sum());gain=float(p[:-1]@t['gains'])
        expected={'p_cf':float(p[:-1].sum()),'p_improve':improve,'expected_accepted_gain':gain,
            'normalized_gain':gain/t['normalizer'],'expected_cost_after_one_attempt':t['current']-gain,
            'p_improve_by_budget':1-(1-improve)**64,'local_best_gain':float(t['gains'].max())}
        for field,value in expected.items():
            error=abs(float(row[field])-value);max_metric_error=max(max_metric_error,error);assert error<2e-9,(key,model,field,error)
        assert int(row['physical_attempts_simulated'])==64 and int(row['real_qpu_shots'])==0
        assert int(row['collisions'])+int(row['feasible_draws'])==64
        assert int(row['proposal_cut_evaluations_uncached'])==int(row['feasible_draws'])
        assert int(row['proposal_cut_evaluations_cached'])==int(row['distinct_feasible_draws'])
        assert int(row['evaluation_only_local_cut_labels'])==t['label_count']
        assert int(row['algorithm_upfront_local_cut_evaluations'])==(t['label_count'] if model=='classical_best_local' else 0)
        assert boolean(row['local_improvement_possible'])==bool(t['improve'].any())
        assert int(row['observed_improvement_count'])<=int(row['feasible_draws'])
        # Only two archived cases per run are replayed, not the campaigns.
        case_index=test_order.index(key)
        if case_index in (0,len(test)-1):
            offset=0 if model=='classical_exact_replacement' else models.index(model)
            counts=np.random.default_rng(1200000+case_index*101+offset).multinomial(64,p/p.sum())
            assert int(counts[-1])==int(row['collisions'])
            assert int(counts[:-1][t['improve']].sum())==int(row['observed_improvement_count'])
            assert int(np.count_nonzero(counts[:-1]))==int(row['distinct_feasible_draws'])
            observed_spot_checks+=1
        by_key[(key,model)]=row
    assert len(by_key)==len(metrics)
    max_pair_difference=max(abs(float(by_key[(key,'bosonic_fixed')][field])-float(by_key[(key,'pair_product_fixed')][field]))
        for key in test_order for field in ('p_cf','p_improve','expected_accepted_gain','normalized_gain'))
    assert max_pair_difference<1e-12
    total_attempts=sum(int(row['physical_attempts_simulated']) for row in metrics)
    assert total_attempts==summary['total_test_synthetic_attempts']
    assert sum(t['label_count'] for t in train)==summary['training_local_cut_labels']
    assert sum(t['label_count'] for t in test)==summary['evaluation_only_test_local_cut_labels']
    assert len(train)*45==summary['exact_training_objective_evaluations']
    for split,ts in [('training',train),('test',test)]:
        actual=sum(t['block'].get('anchor_swap_deltas_scored',t['block'].get('swap_deltas_scored')) for t in ts if t['block']['r']==2)
        assert actual==summary[split+'_anchor_swap_deltas_scored']
    return dict(run=str(folder.relative_to(ROOT)),train_instances=len(train_ids),test_instances=len(test_ids),
        train_blocks=len(train),test_blocks=len(test),metric_rows=len(metrics),attempts=total_attempts,
        training_parameters=selections,max_saved_label_error=max_label_error,max_anchor_error=max_anchor_error,
        max_recomputed_training_score_error=max_score_error,max_recomputed_metric_error=max_metric_error,
        max_bosonic_product_expected_metric_difference=max_pair_difference,count_spot_replays=observed_spot_checks,
        all_selected_interactions_zero=True,global_optimum_used=False)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error('Refusing to overwrite review evidence')
    paths=[ROOT/'experiments/phase2_structured_probe.py',ROOT/'src/photonic_balanced_partitioning/photonic/structured_search.py',
        ROOT/'src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py',ROOT/'src/photonic_balanced_partitioning/problems/min_bisection.py',
        ROOT/'experiments/P20_structured_probe/run_larger_training.py',ROOT/'tests/test_structured_search.py',ROOT/'reports/PHASE2_STRUCTURED_PROBE.md']
    for folder in (BASE,BASE/'larger_training'):
        paths += [folder/name for name in ('manifest.json','summary.json','frozen_parameters.json','training_scores.json','instances.json','blocks.json','test_metrics.csv','contract.json')]
    before={str(p):sha(p) for p in paths};result=dict(status='running',input_hashes_before=before)
    code=0
    try:
        bank,error=p20.kernel_bank() # bounded fixed block check only; no dataset regeneration or training
        result['local_kernel_max_replacement_error']=error
        result['runs']=[run(BASE,bank),run(BASE/'larger_training',bank)]
        result['status']='completed'
    except Exception as error:
        result['status']='failed';result['error']=repr(error);result['traceback']=traceback.format_exc();code=1
    after={str(p):sha(p) for p in paths};result['input_hashes_after']=after
    if before!=after:result['status']='inputs-changed';code=1
    result.update(wall_seconds=time.perf_counter()-START,cpu_seconds=time.process_time()-CPU_START,
        hardware=platform.platform(),python=platform.python_version(),numpy=np.__version__,
        no_campaign_rerun=True,only_two_stored_test_cases_per_run_resampled=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('input_hashes_before','input_hashes_after','runs')},indent=2))
    raise SystemExit(code)

if __name__=='__main__':main()
