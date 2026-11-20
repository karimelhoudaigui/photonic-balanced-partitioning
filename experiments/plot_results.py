#!/usr/bin/env python3
"""Standalone scientific figures from preserved raw results (no fitting)."""
import csv
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/figures'


def load(name):
    return json.loads((ROOT/'experiments'/name/'summary.json').read_text())


def raw(name):
    with (ROOT/'experiments'/name/'runs.jsonl').open() as stream:
        return [json.loads(line) for line in stream]


def finish(fig,name):
    fig.tight_layout()
    for extension in ['png','pdf']:fig.savefig(OUT/f'{name}.{extension}',dpi=180)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    haar=load('E01_haar_collision_baseline')['results']
    fig,ax=plt.subplots(figsize=(6,4))
    n=np.array([r['n'] for r in haar]);p=np.array([r['p_cf']['mean'] for r in haar])
    ci=np.array([r['p_cf']['ci95'] for r in haar])
    ax.errorbar(n,p,yerr=np.array([p-ci[:,0],ci[:,1]-p]),fmt='o',capsize=4,label='Measured Haar mean, marginal 95% CI')
    ax.plot(n,[r['haar_prediction'] for r in haar],color='black',label='Known exact Haar expectation')
    ax.set(xlabel='Modes n (k=n/2)',ylabel='Collision-free probability',xticks=n)
    ax.legend(fontsize=8);finish(fig,'haar_scaling')

    runs=raw('E03_objectives_pareto')
    fig,ax=plt.subplots(figsize=(7,5))
    labels={'bad':'Bad unnormalized moment','conditional':'Conditional energy','success':'Physical success (oracle)',
            'factorized':'Factorized success (same loss)','p_cf':'Collision-free probability',
            'conditional_success':'Conditional success (oracle)','collision':'Collision-aware energy','barrier':'Log barrier','cvar':'Conditional lower CVaR'}
    for name,label in labels.items():
        sub=[r for r in runs if r['objective']==name]
        ax.scatter([r['after']['p_cf'] for r in sub],[r['after']['p_opt_given_cf'] for r in sub],s=14,alpha=.65,label=label)
    ax.scatter([1],[1],marker='*',s=150,color='black',label='Known-target permutation')
    ax.set(xlabel='P(CF) per ideal attempt',ylabel='P(optimum | CF)',xlim=(-.03,1.03),ylim=(-.03,1.03),
           title='Finite-budget n=4 diagnostics; no universal Pareto tension')
    ax.legend(loc='center left',bbox_to_anchor=(1,0.5),fontsize=8)
    finish(fig,'objectives_pareto')

    shots=raw('E05b_exact_equal_budget')
    groups=[('bosonic',None,'Bosonic'),('distinguishable',None,'Distinguishable'),('multinomial',None,'Multinomial'),
            ('classical_penalty',.1,'Penalty .1'),('classical_penalty',1.,'Penalty 1'),('classical_penalty',10.,'Penalty 10'),
            ('random_balanced',None,'Uniform feasible')]
    fig,axes=plt.subplots(1,3,figsize=(13,4),sharey=True)
    for n,ax in zip([4,6,8],axes):
        values=[[r['final_p_success'] for r in shots if r['n']==n and r['model']==model and r['lambda_value']==lam] for model,lam,_ in groups]
        ax.boxplot(values,tick_labels=[g[2] for g in groups],showfliers=True)
        ax.set(title=f'n={n}; 36 fixed-grid runs/model',yscale='log',ylim=(1e-6,1.3))
        ax.tick_params(axis='x',rotation=70)
    axes[0].set_ylabel('Final ideal success per attempt')
    fig.suptitle('Exactly 30,720 training + 4,096 independent heldout attempts for every run')
    finish(fig,'equal_budget_success')

    fig,ax=plt.subplots(figsize=(6,4))
    for model,lam,label in groups:
        if model=='classical_penalty' and lam!=1.:continue
        x=np.sort([r['first_optimum_attempt'] for r in shots if r['n']==8 and r['model']==model and r['lambda_value']==lam])
        ax.step(x,np.arange(1,len(x)+1)/len(x),where='post',label=label)
    ax.set(xlabel='Ideal attempts through training to first optimum',ylabel='Observed fraction of 36 runs',
           xscale='log',ylim=(0,1.03),title='n=8 discovery; all runs found an optimum during training')
    ax.legend(fontsize=8);finish(fig,'discovery_cost')

    examples=json.loads((ROOT/'experiments/E08_coherence_certificate/counterexamples.json').read_text())['examples']
    fig,ax=plt.subplots(figsize=(6,4))
    x=[r['n'] for r in examples]
    ax.plot(x,[1-r['p_cf'] for r in examples],'o-',label='Collision probability = 2/(k+2)')
    ax.plot(x,[.5 for r in examples],'s-',label='TV(bosonic, distinguishable) = 1/2')
    ax.set(xlabel='Modes m=2k',ylabel='Probability / total variation',xscale='log',ylim=(0,.55),
           title='Exact balanced-density counterexample; no postselection')
    ax.legend(fontsize=8);finish(fig,'collision_counterexample')
    print(f'Wrote five figures as PNG and PDF to {OUT}')


if __name__=='__main__':main()
