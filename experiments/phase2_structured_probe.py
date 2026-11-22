"""P20: fixed interacting-block proposals versus feasible classical controls.

No optimum labels, global search oracle, loss model or QPU is used. Training
and test graph seeds are disjoint; parameters freeze before any test labels.
Run from root: MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/phase2_structured_probe.py
"""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import time

import numpy as np

from photonic_balanced_partitioning.problems.min_bisection import BalancedGraphPartitioning as Problem
from photonic_balanced_partitioning.photonic.structured_search import (
    LocalBlockProposal, classical_anchor, cut_energy, informed_block,
    interacting_unitary, pair_unitary,
)

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'experiments/P20_structured_probe'
ANGLES=[0.,float(np.pi/8),float(np.pi/4),float(3*np.pi/8),float(np.pi/2)]
INTERACTIONS=[0.,float(np.pi/8),float(np.pi/4),float(np.pi/2)]
FAMILIES=['path','cycle','regular','er','weighted','planted']
SIZES_TRAIN=[8,12,16]
SIZES_TEST=[8,12,16,24]
TRAIN_SEEDS=list(range(4))
TEST_SEEDS=list(range(100,112))
REGIMES={'two_swaps':2,'single_swap_local_minimum':None}
SHOTS=64
SOURCES=[Path(__file__).relative_to(ROOT),Path('src/photonic_balanced_partitioning/photonic/structured_search.py'),
         Path('src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py'),
         Path('src/photonic_balanced_partitioning/problems/min_bisection.py')]


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def make_graph(n,family,seed):
    if family=='path':p=Problem.path_graph(n)
    elif family=='cycle':p=Problem.cycle_graph(n)
    elif family=='regular':p=Problem.random_regular(n,3,seed)
    elif family=='er':p=Problem.erdos_renyi(n,.3,seed)
    elif family=='weighted':p=Problem.erdos_renyi(n,.4,seed,(.25,2.))
    else:p=Problem.planted_partition(n,n//2,seed=seed)
    # Independently shuffled labels; no sorted contiguous anchor supplies a hint.
    permutation=np.random.default_rng(710000+n*1000+seed*7+FAMILIES.index(family)).permutation(n)
    a=p.adjacency_matrix[np.ix_(permutation,permutation)]
    return a,permutation


def kernel_bank():
    bank={}
    maximum_replacement_error=0.
    for r in [2,3]:
        generic=LocalBlockProposal(tuple(range(r)),tuple(range(r)),tuple(range(r,2*r)))
        for model in ['bosonic','distinguishable']:
            bank[(r,model)]=[]
            for pair_angle in ANGLES:
                for interaction in INTERACTIONS:
                    u=interacting_unitary(r,pair_angle,interaction)
                    _,p=generic.distribution(u,model)
                    if model=='bosonic':
                        _,replacement=generic.distribution(u,'classical_exact_bosonic')
                        maximum_replacement_error=max(maximum_replacement_error,float(abs(p-replacement).max()))
                    bank[(r,model)].append(dict(pair_angle=pair_angle,interaction_angle=interaction,p=p))
        bank[(r,'pair')]=[]
        for angle in ANGLES:
            _,p=generic.distribution(pair_unitary(r,angle),'bosonic')
            bank[(r,'pair')].append(dict(pair_angle=angle,interaction_angle=0.,p=p))
        for model in ['uniform_feasible','correlated_batch']:
            _,p=generic.distribution(model=model)
            bank[(r,model)]=[dict(p=p)]
    assert maximum_replacement_error<1e-12
    return bank,maximum_replacement_error


def prepare_cases(split,sizes,seeds):
    cases=[];instances=[]
    for n in sizes:
        for family in FAMILIES:
            for seed in seeds:
                a,permutation=make_graph(n,family,seed)
                graph_id=f'{n}_{family}_{seed}'
                instances.append(dict(graph_id=graph_id,n=n,family=family,seed=seed,split=split,
                                      label_permutation=permutation.tolist(),adjacency=a.tolist()))
                anchor_seed=910000+n*10000+seed*10+FAMILIES.index(family)
                for regime,steps in REGIMES.items():
                    anchor=classical_anchor(a,anchor_seed,max_steps=steps)
                    for r in [2,3]:
                        occupied,vacant=informed_block(anchor,r,anchor_seed+r*997)
                        proposal=LocalBlockProposal(anchor['partition'],occupied,vacant)
                        label=proposal.statistics(a,proposal.distribution(model='uniform_feasible')[1])
                        cases.append(dict(graph_id=graph_id,n=n,family=family,seed=seed,split=split,
                                          regime=regime,r=r,anchor=anchor,proposal=proposal,
                                          normalizer=max(float(a.sum()/2),1.),label=label))
    return cases,instances


def train(cases,bank):
    frozen={};training=[]
    for r in [2,3]:
        for regime in REGIMES:
            subset=[c for c in cases if c['r']==r and c['regime']==regime]
            for model in ['bosonic','distinguishable','pair']:
                entries=bank[(r,model)]
                for index,entry in enumerate(entries):
                    score=float(np.mean([entry['p'][:-1]@c['label']['gains']/c['normalizer'] for c in subset]))
                    training.append(dict(r=r,regime=regime,model=model,index=index,score=score,
                                         pair_angle=entry['pair_angle'],interaction_angle=entry['interaction_angle'],
                                         collision_probability=float(entry['p'][-1]),cases=len(subset)))
                ranking=[t for t in training if t['r']==r and t['regime']==regime and t['model']==model]
                # Prefer fewer collisions only when training scores agree at 1e-14.
                best=max(t['score'] for t in ranking)
                selected=min((t for t in ranking if t['score']>=best-1e-14),key=lambda t:(t['collision_probability'],t['index']))
                frozen[(r,regime,model)]=selected['index']
    return frozen,training


def evaluate(cases,bank,frozen):
    rows=[]
    for case_index,c in enumerate(cases):
        r,regime=c['r'],c['regime'];label=c['label'];anchor=c['anchor']
        chosen_b=bank[(r,'bosonic')][frozen[(r,regime,'bosonic')]]
        chosen_d=bank[(r,'distinguishable')][frozen[(r,regime,'distinguishable')]]
        chosen_pair=bank[(r,'pair')][frozen[(r,regime,'pair')]]
        # Same parameter index exists in bosonic/distinguishable banks.
        same_d=bank[(r,'distinguishable')][frozen[(r,regime,'bosonic')]]
        models={'bosonic_fixed':chosen_b['p'], 'distinguishable_fixed':chosen_d['p'],
                'distinguishable_same_circuit':same_d['p'], 'pair_product_fixed':chosen_pair['p'],
                'uniform_feasible':bank[(r,'uniform_feasible')][0]['p'],
                'correlated_batch':bank[(r,'correlated_batch')][0]['p'],
                'classical_exact_replacement':chosen_b['p']}
        best=np.zeros(len(chosen_b['p']));best[int(np.argmin(label['energies']))]=1
        models['classical_best_local']=best
        for model_index,(model,p) in enumerate(models.items()):
            improving=p[:-1][label['improving_mask']].sum()
            accepted_gain=float(p[:-1]@label['gains'])
            # Couple exact classical replacement draws with the bosonic draws:
            # identical kernels must have identical trajectories, not only means.
            seed_offset=0 if model=='classical_exact_replacement' else model_index
            counts=np.random.default_rng(1200000+case_index*101+seed_offset).multinomial(SHOTS,p/p.sum())
            success_count=int(counts[:-1][label['improving_mask']].sum())
            observed_gain=float(max([gain for gain,count in zip(label['gains'],counts[:-1]) if count] or [0.]))
            rows.append(dict(graph_id=c['graph_id'],n=c['n'],family=c['family'],graph_seed=c['seed'],
                             regime=regime,r=r,model=model,p_cf=float(p[:-1].sum()),p_improve=float(improving),
                             expected_accepted_gain=accepted_gain,normalized_gain=accepted_gain/c['normalizer'],
                             expected_cost_after_one_attempt=float(anchor['energy']-accepted_gain),
                             p_improve_by_budget=float(1-(1-improving)**SHOTS),
                             anchor_energy=float(anchor['energy']),anchor_steps=anchor['steps'],
                             anchor_local_minimum=anchor['local_minimum'],
                             local_improvement_possible=label['improvement_possible'],local_best_gain=label['local_best_gain'],
                             physical_attempts_simulated=SHOTS,real_qpu_shots=0,observed_improvement_count=success_count,
                             observed_best_gain=observed_gain,collisions=int(counts[-1]),
                             feasible_draws=int(counts[:-1].sum()),distinct_feasible_draws=int(np.count_nonzero(counts[:-1])),
                             anchor_swap_deltas_scored=anchor['swap_deltas_scored'],anchor_full_cut_evaluations=1,
                             evaluation_only_local_cut_labels=label['local_cost_labels'],
                             algorithm_upfront_local_cut_evaluations=label['local_cost_labels'] if model=='classical_best_local' else 0,
                             proposal_cut_evaluations_uncached=int(counts[:-1].sum()),
                             proposal_cut_evaluations_cached=int(np.count_nonzero(counts[:-1]))))
    return rows


def aggregate(rows):
    out=[]
    for r in [2,3]:
        for regime in REGIMES:
            for model in sorted({row['model'] for row in rows}):
                subset=[row for row in rows if row['r']==r and row['regime']==regime and row['model']==model]
                out.append(dict(r=r,regime=regime,model=model,cases=len(subset),
                                improvement_possible=sum(row['local_improvement_possible'] for row in subset),
                                mean_p_cf=float(np.mean([row['p_cf'] for row in subset])),
                                mean_p_improve=float(np.mean([row['p_improve'] for row in subset])),
                                mean_normalized_gain=float(np.mean([row['normalized_gain'] for row in subset])),
                                mean_observed_best_gain=float(np.mean([row['observed_best_gain'] for row in subset]))))
    differences=[]
    for r in [2,3]:
        for regime in REGIMES:
            base=[row for row in rows if row['r']==r and row['regime']==regime and row['model']=='bosonic_fixed']
            lookup={(row['graph_id'],row['model']):row for row in rows if row['r']==r and row['regime']==regime}
            for control in ['distinguishable_same_circuit','distinguishable_fixed','pair_product_fixed',
                            'uniform_feasible','correlated_batch','classical_exact_replacement','classical_best_local']:
                values=np.array([row['p_improve']-lookup[(row['graph_id'],control)]['p_improve'] for row in base])
                rng=np.random.default_rng(620100+r*17+list(REGIMES).index(regime))
                # Each regime/r uses one row per graph+label/anchor draw.
                draws=rng.choice(values,size=(2000,len(values)),replace=True).mean(axis=1)
                differences.append(dict(r=r,regime=regime,control=control,cases=len(values),
                                        mean_delta_p_improve=float(values.mean()),
                                        ci95_low=float(np.quantile(draws,.025)),ci95_high=float(np.quantile(draws,.975)),
                                        positive_cases=int((values>1e-10).sum()),negative_cases=int((values< -1e-10).sum())))
    return out,differences


def main():
    OUT.mkdir(exist_ok=True)
    contract=dict(question='At a classically prepared partition, do fixed local bosonic proposal kernels enrich strictly improving moves per physical attempt over serious feasible controls?',
                  train_sizes=SIZES_TRAIN,test_sizes=SIZES_TEST,train_seeds=TRAIN_SEEDS,test_seeds=TEST_SEEDS,
                  families=FAMILIES,regimes=REGIMES,interacting_photons=[2,3],angles=ANGLES,interaction_angles=INTERACTIONS,
                  shots_per_test_kernel=SHOTS,target='Strict cut reduction from anchor; global optimum is never used.',
                  training_objective='Mean positive accepted cut gain divided by total graph weight; exact ideal objective on training cases only.',
                  controls=['same-circuit distinguishable','separately trained distinguishable','disjoint-pair product',
                            'uniform feasible block','correlated batch swap','exact classical block replacement','best of all feasible block states'],
                  non_claims=['No hardware evidence','No global optimum success comparison','No quantum speedup from fixed-size interacting blocks',
                              'Exact-moment training is not hardware shot-based tuning','Bootstrap intervals describe this predeclared graph/label/anchor ensemble; no universal graph claim'])
    (OUT/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    before={str(p):sha(p) for p in SOURCES}
    start=datetime.now(timezone.utc).isoformat();tic=time.monotonic()
    bank,replacement_error=kernel_bank()
    training_cases,training_instances=prepare_cases('train',SIZES_TRAIN,TRAIN_SEEDS)
    frozen,training_scores=train(training_cases,bank)
    frozen_serial=[dict(r=r,regime=regime,model=model,**{key:value for key,value in bank[(r,model)][index].items() if key!='p'})
                   for (r,regime,model),index in frozen.items()]
    (OUT/'frozen_parameters.json').write_text(json.dumps(frozen_serial,indent=2)+'\n')
    frozen_hash=sha(Path('experiments/P20_structured_probe/frozen_parameters.json'))
    # Test instances/labels are first constructed AFTER frozen parameters persist.
    test_cases,test_instances=prepare_cases('test',SIZES_TEST,TEST_SEEDS)
    rows=evaluate(test_cases,bank,frozen)
    summaries,differences=aggregate(rows)
    with (OUT/'test_metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'training_scores.json').write_text(json.dumps(training_scores,indent=2)+'\n')
    (OUT/'instances.json').write_text(json.dumps(training_instances+test_instances,indent=2)+'\n')
    diagnostics=[]
    for c in training_cases+test_cases:
        diagnostics.append(dict(graph_id=c['graph_id'],split=c['split'],regime=c['regime'],r=c['r'],
                                anchor=c['anchor']['partition'],occupied=c['proposal'].occupied,vacant=c['proposal'].vacant,
                                cut_energies=c['label']['energies'].tolist(),anchor_energy=c['anchor']['energy'],
                                initial_anchor_energy=c['anchor']['initial_energy'],anchor_steps=c['anchor']['steps'],
                                anchor_swap_deltas_scored=c['anchor']['swap_deltas_scored'],
                                initial_full_cut_evaluations=1,normalizer=c['normalizer']))
    (OUT/'blocks.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    after={str(p):sha(p) for p in SOURCES}
    assert before==after,'Source changed during experiment; rerun required'
    assert frozen_hash==sha(Path('experiments/P20_structured_probe/frozen_parameters.json'))
    summary=dict(status='completed',started_utc=start,ended_utc=datetime.now(timezone.utc).isoformat(),runtime_seconds=time.monotonic()-tic,
                 git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                 git_dirty=subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).splitlines(),
                 source_hashes_before=before,source_hashes_after=after,frozen_parameters_sha256=frozen_hash,
                 versions={p:importlib.metadata.version(p) for p in ['numpy','scipy','perceval-quandela']},
                 python=platform.python_version(),platform=platform.platform(),
                 training_graph_label_instances=len(training_instances),test_graph_label_instances=len(test_instances),
                 training_blocks=len(training_cases),test_blocks=len(test_cases),test_metric_rows=len(rows),
                 parameter_candidates_per_training_block={'bosonic':20,'distinguishable':20,'pair':5},
                 exact_training_objective_evaluations=len(training_cases)*45,
                 training_local_cut_labels=sum(c['label']['local_cost_labels'] for c in training_cases),
                 evaluation_only_test_local_cut_labels=sum(c['label']['local_cost_labels'] for c in test_cases),
                 training_anchor_swap_deltas_scored=sum(c['anchor']['swap_deltas_scored'] for c in training_cases if c['r']==2),
                 test_anchor_swap_deltas_scored=sum(c['anchor']['swap_deltas_scored'] for c in test_cases if c['r']==2),
                 total_test_synthetic_attempts=sum(row['physical_attempts_simulated'] for row in rows),real_qpu_shots=0,
                 max_exact_classical_replacement_error=replacement_error,aggregates=summaries,paired_differences=differences,
                 command='MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/phase2_structured_probe.py',
                 warning='Graph labels and initializers are randomized; path and cycle repeats share graph topology. No graph filtering or optimum-based selection.',
                 non_claims=contract['non_claims'])
    paths=['contract.json','frozen_parameters.json','test_metrics.csv','training_scores.json','instances.json','blocks.json']
    summary['output_hashes']={str(Path('experiments/P20_structured_probe')/path):sha(Path('experiments/P20_structured_probe')/path) for path in paths}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({key:summary[key] for key in ['status','runtime_seconds','training_blocks','test_blocks','exact_training_objective_evaluations',
                                                 'total_test_synthetic_attempts','max_exact_classical_replacement_error']},indent=2))
    print('Frozen parameters:',json.dumps(frozen_serial))
    for d in differences:
        if d['control'] in ['distinguishable_same_circuit','pair_product_fixed','correlated_batch','classical_exact_replacement']:
            print(json.dumps(d))


if __name__=='__main__':main()
