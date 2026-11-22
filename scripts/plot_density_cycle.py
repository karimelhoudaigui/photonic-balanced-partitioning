#!/usr/bin/env python3
"""Derived scientific figures; no new simulation or manuscript edits."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main(root,output):
    output.mkdir(parents=True,exist_ok=False)
    files=[root/m/'data/raw.json' for m in ['primary','replication']]
    data=[json.loads(p.read_text()) for p in files];rows=sum([d['full_checks'] for d in data],[])
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'savefig.dpi':220,'pdf.fonttype':42})
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    ax=axes[0,0]
    for family,color,label in [('global_output_mix','#0072B2','Global output mixing'),
                               ('flat_fixed_projector','#D55E00','Flat fixed projector')]:
        selected=[r for r in rows if r['family']==family and r['strength']>0]
        ax.scatter([r['actual_tv'] for r in selected],
                   [r['certificate']['support_cycle_tv_bound'] for r in selected],
                   s=14,color=color,alpha=.65,label=label)
    ax.plot([1e-6,1],[1e-6,1],'k--',lw=1,label='Equality')
    ax.set(xscale='log',yscale='log',xlabel='Full-law TV from complete Fock data',
           ylabel='Dominant-support bound estimate',title='A  Complete distributions: 300 grid cases')
    ax.legend(fontsize=8);ax.text(.02,.98,'240 nonzero-strength cases shown\n60 zero-strength cases retained in raw data',
        transform=ax.transAxes,va='top',fontsize=8)
    ax=axes[0,1];r=[x for x in data[0]['balanced_sharpness'] if x['strength']>0]
    x=np.array([a['certificate']['expected_collision_pairs'] for a in r])
    ax.plot(x,[a['actual_tv']/a['certificate']['expected_collision_pairs'] for a in r],
            'o-',color='#0072B2',label='Actual TV / M')
    ax.plot(x,[a['certificate']['refined_density_cycle_tv_bound']/a['certificate']['expected_collision_pairs'] for a in r],
            's-',color='#D55E00',label='Refined bound / M')
    ax.set(xscale='log',yscale='log',xlabel='Expected collision pairs M',ylabel='Ratio to M',
           title='B  Balanced sharp family: c = 1/2')
    ax.legend(fontsize=8);ax.text(.02,.97,'Leading coefficient M/(2c) = M\nSix nonzero angles; zero case retained',
        transform=ax.transAxes,va='top',fontsize=8)
    ax=axes[1,0];r=data[0]['dilute_counterexamples'];x=[a['certificate']['k'] for a in r]
    ax.plot(x,[a['actual_tv'] for a in r],'o-',color='#D55E00',label='Actual TV = 1/2')
    ax.plot(x,[a['certificate']['expected_collision_pairs'] for a in r],'s-',color='#0072B2',label='M = c = 2/(k+2)')
    ax.plot(x,np.ones(len(x)),'k--',label='Density bound is trivial')
    ax.set(xscale='log',yscale='log',xlabel='Photons k (m = 2k)',ylabel='TV or moment / intensity',
           title='C  Dilute obstruction: density floor vanishes');ax.legend(fontsize=8)
    ax.set_xticks(x,labels=[str(k) for k in x]);ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax=axes[1,1];large=sum([d['scalable_certificate_only'] for d in data],[])
    for scale,color in zip([.02,.06,.2,.6],['#0072B2','#009E73','#E69F00','#D55E00']):
        values=[]
        for m in [32,64,128]:
            subset=[r['certificate']['support_cycle_tv_bound'] for r in large
                    if r['certificate']['m']==m and abs(r['strength']*np.sqrt(m//2)-scale)<1e-12]
            assert len(subset)==6
            values.append(subset)
        y=np.array(values);ax.plot([32,64,128],np.median(y,axis=1),'o-',color=color,label=f'Scaled strength {scale:g}')
        ax.fill_between([32,64,128],y.min(axis=1),y.max(axis=1),color=color,alpha=.12)
    ax.set(yscale='log',xlabel='Modes m (k = m/2)',ylabel='Support-bound estimate',
           title='D  Certificate calculations only; no full simulation')
    ax.set_xticks([32,64,128]);ax.legend(fontsize=8)
    for ax in axes.flat:ax.grid(alpha=.15,which='both')
    fig.suptitle('Density-conditioned classical replacement: finite checks and limitations',fontsize=14)
    for extension in ['png','pdf']:fig.savefig(output/f'density_checkpoint.{extension}')
    plt.close(fig)
    receipt={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'render_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'inputs':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files],
        'plotted_full_grid_cases':240,'unplotted_zero_strength_grid_cases':60,
        'large_cases_certificate_only':72,'non_claim':'Float estimates, not interval bounds. No full-law data beyond m12. No optimizer or advantage.'}
    (output/'render_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--evidence-root',type=Path,required=True)
    parser.add_argument('--output-dir',type=Path,required=True);a=parser.parse_args();main(a.evidence_root,a.output_dir)
