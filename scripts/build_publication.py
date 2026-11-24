#!/usr/bin/env python3
"""Deterministic publication artifacts from reconciled, preserved evidence only.

--root is the repository/output root. --archive-root is an optional read-only
fallback for historical inputs absent from a sparse checkout. --check renders
nothing and detects changed inputs, generator or output bytes using SHA256.
"""
from __future__ import annotations
import argparse,csv,hashlib,importlib.metadata,itertools,json,math,statistics,sys
from datetime import datetime,timezone
from fractions import Fraction
from pathlib import Path

VALIDATED='results/validated/recovery_2026-11-24'
DENSITY='results/P33_density_supervised/20261122T014822Z'
LOSS='experiments/P37_loss_source/run'
GENERATOR='scripts/build_publication.py'
MANIFEST='paper/publication_manifest.json'
OUTPUTS=('paper/tables/validated_numbers.tex','paper/tables/table_graphs.tex',
         'paper/tables/table_e05b.tex','paper/tables/table_losses.tex',
         'paper/figures/fig_e05b.pdf','paper/figures/fig_density.pdf','paper/figures/fig_loss_source.pdf')
INPUTS=tuple(f'{VALIDATED}/{name}' for name in ('summary.json','benchmark.csv','campaigns.json','source_hashes.json','manifest.json'))+tuple(
    f'{DENSITY}/{mode}/{name}' for mode in ('primary','replication') for name in ('data/raw.json','manifest.json'))+(
    f'{DENSITY}/audit/raw.json',f'{DENSITY}/audit/manifest.json',f'{LOSS}/data/raw.json',f'{LOSS}/manifest.json')
LABELS={'bosonic':'Bosonic','distinguishable':'Distinguishable','multinomial':'Classical iid multinomial',
        'classical_penalty':'Product Bernoulli penalty','random_balanced':'Uniform feasible'}
FIXED_DATE=datetime(2000,1,1,tzinfo=timezone.utc)

class PublicationError(ValueError):pass

def require(condition,message):
    if not condition:raise PublicationError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def fraction(value):return Fraction(int(value['numerator']),int(value['denominator']))
def latex_fraction(value):
    value=Fraction(value)
    return str(value.numerator) if value.denominator==1 else rf'\frac{{{value.numerator}}}{{{value.denominator}}}'
def tex_set(values):return ', '.join(str(x) for x in values)

def resolve(root,archive,logical):
    relative=Path(logical)
    require(not relative.is_absolute() and '..' not in relative.parts,'Unsafe artifact path')
    for base in (root,archive):
        if base is not None and (base/relative).is_file():return base/relative
    raise PublicationError('Missing input: '+logical)


def declared_hash(manifest,basename):
    matches=[r['sha256'] for r in manifest['outputs'] if r['path'].endswith('/'+basename)]
    require(len(matches)==1,'Ambiguous/missing original result pin: '+basename)
    return matches[0]


def load_evidence(root,archive=None):
    paths={name:resolve(root,archive,name) for name in INPUTS}
    hashes={name:sha(path) for name,path in paths.items()}
    def read(name):return json.loads(paths[name].read_text())
    summary=read(f'{VALIDATED}/summary.json');campaigns=read(f'{VALIDATED}/campaigns.json')
    sources=read(f'{VALIDATED}/source_hashes.json');reconciliation=read(f'{VALIDATED}/manifest.json')
    require(summary['e05b']['all_runs_audit_pass'] and sources['all_observed_inputs_unchanged'],'Reconciliation is not accepted')
    require(not summary['publication_policy']['root_P33_performance_evidence_accepted'],'Excluded root P33 cannot supply this publication')
    for name in ('summary.json','benchmark.csv','campaigns.json','source_hashes.json'):
        require(hashes[f'{VALIDATED}/{name}']==declared_hash(reconciliation,name),'Reconciled input pin mismatch: '+name)
    with paths[f'{VALIDATED}/benchmark.csv'].open(newline='') as f:benchmark=list(csv.DictReader(f))
    require(len(benchmark)==summary['e05b']['raw_runs'],'CSV/summary run count differs')
    for group in summary['e05b']['groups']:
        selected=[r for r in benchmark if int(r['n'])==group['n'] and r['model']==group['model'] and
                  (float(r['lambda_value']) if r['lambda_value'] else None)==group['lambda_value']]
        require(len(selected)==group['runs'],'Group coverage mismatch')
        require(abs(statistics.mean(float(r['final_p_success']) for r in selected)-group['final_p_success_mean'])<1e-13,'CSV/group mean differs')
    density={}
    for mode in ('primary','replication'):
        name=f'{DENSITY}/{mode}/data/raw.json';original=read(f'{DENSITY}/{mode}/manifest.json')
        require(hashes[name]==declared_hash(original,'data/raw.json'),'Supervised density pin mismatch: '+mode)
        density[mode]=read(name)
    audit=read(f'{DENSITY}/audit/raw.json');audit_manifest=read(f'{DENSITY}/audit/manifest.json')
    require(hashes[f'{DENSITY}/audit/raw.json']==declared_hash(audit_manifest,'raw.json'),'Density audit pin mismatch')
    require(audit['all_collisions_retained'],'Density audit does not retain collisions')
    require(audit['verdict']=='IMPLEMENTATION_AND_FINITE_ASSERTION_VERIFIED_WITHIN_STATED_FLOAT_TOLERANCES','Density capture is not accepted for finite illustration')
    for batch in audit['batches']:
        require(batch['raw_sha256']==hashes[f'{DENSITY}/{batch["mode"]}/data/raw.json'],'Density audit targets different raw bytes')
    loss=read(f'{LOSS}/data/raw.json');original=read(f'{LOSS}/manifest.json')
    require(hashes[f'{LOSS}/data/raw.json']==declared_hash(original,'data/raw.json'),'P37 raw pin mismatch')
    require(sum(len(cell['values']) for cell in loss['grid'])==loss['summary']['source_probabilities_crosschecked'],'P37 probability count differs')
    require(len(loss['transitions'])==loss['summary']['transition_brackets'],'P37 bracket count differs')
    return dict(summary=summary,benchmark=benchmark,campaigns=campaigns,density=density,loss=loss,input_paths=paths,input_hashes=hashes)


def graph_rows():
    """Enumerate balanced bitstrings, including complements as distinct strings."""
    n=4;k=n//2
    edges={'Path':[(i,i+1) for i in range(n-1)],'Cycle':[(i,(i+1)%n) for i in range(n)],
           'K4':list(itertools.combinations(range(n),2)),
           'K22':[(i,j) for i in range(k) for j in range(k,n)],'Star':[(0,j) for j in range(1,n)]}
    rows=[]
    for label,graph in edges.items():
        costs=[sum((i in selected)!=(j in selected) for i,j in graph) for selected in itertools.combinations(range(n),k)]
        optimum=min(costs);g=costs.count(optimum)
        rows.append(dict(label=label,n=n,k=k,optimum=optimum,optimal_strings=g,haar_denominator=math.comb(n+k-1,k)))
    return rows


def loss_rows(loss):
    selected=[]
    for eta in (Fraction(3,4),Fraction(9,10),Fraction(99,100),Fraction(1)):
        matching=[cell for cell in loss['grid'] if cell['m']==8 and fraction(cell['eta'])==eta]
        require(len(matching)==1,'Requested P37 cell missing or duplicated')
        cell=matching[0];choices={}
        for criterion,field in (('per_attempt','probability'),('per_photon','per_photon')):
            values=[(int(row['source']),fraction(row[field])) for row in cell['values']]
            maximum=max(value for _,value in values);choices[criterion]=[n for n,value in values if value==maximum]
            require(choices[criterion]==cell[criterion+'_maximizers'],'Recorded P37 source maximizers differ')
        selected.append(dict(eta=eta,**choices))
    return selected


def write_tables(root,evidence):
    summary=evidence['summary'];loss=evidence['loss'];groups=summary['e05b']['groups']
    counts=dict(ErunCount=len(evidence['benchmark']),SourceProbabilityCount=sum(len(c['values']) for c in loss['grid']),SourceBracketCount=len(loss['transitions']))
    macros='% Generated by scripts/build_publication.py; all counts extracted from validated evidence.\n'+''.join(rf'\providecommand{{\{name}}}{{{value}}}'+'\n' for name,value in counts.items())
    (root/OUTPUTS[0]).write_text(macros)
    graph_lines=[r'\begin{table}[t]',r'\centering',r'\begin{tabular}{lrrc}',r'\hline',r'Graph & $C^*$ & Optimal strings $g$ & Haar $\mathbb{E}[P_{\rm opt}]$ \\',r'\hline']
    labels={'K4':r'$K_4$','K22':r'$K_{2,2}$'}
    for row in graph_rows():graph_lines.append(f"{labels.get(row['label'],row['label'])} & {row['optimum']} & {row['optimal_strings']} & $\\frac{{{row['optimal_strings']}}}{{{row['haar_denominator']}}}$ \\\\")
    graph_lines.extend([r'\hline',r'\end{tabular}',r'\caption{Computed four-vertex, two-photon controls. Balanced bitstrings and their complements are counted separately. The last column is a Haar ensemble expectation, not a trained or measured hardware success rate.}',r'\label{tab:graphs}',r'\end{table}'])
    (root/OUTPUTS[1]).write_text('\n'.join(graph_lines)+'\n')
    sizes=sorted({g['n'] for g in groups});methods=[]
    for g in groups:
        key=(g['model'],g['lambda_value'])
        if key not in methods:methods.append(key)
    lines=[r'\begin{table}[t]',r'\centering\scriptsize',r'\setlength{\tabcolsep}{3pt}',r'\begin{tabular}{l'+'c'*len(sizes)+'}',r'\hline',
           'Method & '+' & '.join(f'$n={n}$' for n in sizes)+r' \\',r'\hline']
    for model,lam in methods:
        label=LABELS[model]+(rf' ($\lambda={lam:g}$)' if lam is not None else '')
        cells=[]
        for n in sizes:
            g=next(g for g in groups if (g['n'],g['model'],g['lambda_value'])==(n,model,lam));low,high=g['instance_interval']
            cells.append(r'\shortstack{'+f"{g['final_p_success_mean']:.3f}"+r'\\{'+f'[{low:.3f}, {high:.3f}]'+'}}')
        lines.append(label+' & '+' & '.join(cells)+r' \\')
    first=groups[0];batch=first['training_attempts_per_run']//first['objective_calls_per_run']
    unique=[next(g['unique_graphs'] for g in groups if g['n']==n) for n in sizes]
    caption=(f"Ideal final success means over {first['runs']} runs per method and size, with descriptive graph-cluster percentile intervals. "
             f"There are {first['nominal_instance_slots']} nominal graph slots per size but $G="+','.join(map(str,unique))+"$ unique labeled weighted graphs, respectively. "
             f"Every run uses {first['objective_calls_per_run']} calls of {batch} training draws plus {first['heldout_attempts_per_run']} heldout draws ({first['total_attempts_per_run']} ideal attempts). "
             "Optimizer repeats stay in the same graph cluster; these are not population significance intervals. Each penalty parameter is a separate fully charged run. No hardware shots.")
    lines.extend([r'\hline',r'\end{tabular}',r'\caption{'+caption+'}',r'\label{tab:e05b}',r'\end{table}'])
    (root/OUTPUTS[2]).write_text('\n'.join(lines)+'\n')
    lines=[r'\begin{table}[t]',r'\centering',r'\begin{tabular}{ccc}',r'\hline',r'$\eta$ & Best $N$ per attempt & Best $N$ per injected photon \\',r'\hline']
    for row in loss_rows(loss):lines.append('$'+latex_fraction(row['eta'])+'$ & $'+tex_set(row['per_attempt'])+'$ & $'+tex_set(row['per_photon'])+r'$ \\')
    lines.extend([r'\hline',r'\end{tabular}',r'\caption{Exact source choices from the preserved P37 rational grid at $m=8$, targeting exactly $m/2$ threshold clicks. All maximizing sources are listed, including ties. The criteria maximize success per attempt and success divided by injected photon number, respectively. This is Haar-averaged feasibility with loss, not graph optimization or a fixed-device waiting-time claim.}',r'\label{tab:losses}',r'\end{table}'])
    (root/OUTPUTS[3]).write_text('\n'.join(lines)+'\n')
    return counts


def pyplot():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'pdf.compression':9,'axes.grid':True,'grid.alpha':.2})
    return plt

def save_pdf(fig,path,title):
    fig.savefig(path,metadata={'Title':title,'Author':'Photonic balanced partitioning evidence build',
                              'Creator':'scripts/build_publication.py','CreationDate':FIXED_DATE,'ModDate':FIXED_DATE})


def figures(root,evidence):
    plt=pyplot();groups=evidence['summary']['e05b']['groups']
    fig,ax=plt.subplots(figsize=(6.5,4.4),constrained_layout=True)
    for model,marker in [('bosonic','o'),('distinguishable','s'),('random_balanced','^'),('multinomial','D')]:
        points=sorted((g for g in groups if g['model']==model),key=lambda g:g['n'])
        means=[g['final_p_success_mean'] for g in points]
        ax.errorbar([g['n'] for g in points],means,yerr=[[mean-g['instance_interval'][0] for mean,g in zip(means,points)],
                    [g['instance_interval'][1]-mean for mean,g in zip(means,points)]],marker=marker,capsize=3,label=LABELS[model])
    ax.set(xlabel='Modes n (photons n/2)',ylabel='Final ideal success probability',ylim=(0,1),xticks=sorted({g['n'] for g in groups}),
           title='Equal ideal-attempt budget: finite-shot blind training')
    ax.legend(fontsize=8);fig.supxlabel('Descriptive graph-cluster intervals; no hardware shots. Penalty controls are retained in the table.',fontsize=7)
    save_pdf(fig,root/OUTPUTS[4],'E05b validated ideal final success');plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(8.5,3.9),constrained_layout=True)
    for mode,marker in [('primary','o'),('replication','x')]:
        raw=evidence['density'][mode];values=[]
        for row in raw['full_checks']:
            measured=.5*sum(abs(a-b) for a,b in zip(row['bosonic_probabilities'],row['distinguishable_probabilities']))
            require(abs(measured-row['actual_tv'])<1e-12,'Density raw TV differs from full probabilities')
            bound=row['certificate']['density_cycle_tv_bound'];require(measured<=bound+1e-10,'Density bound exceeded beyond preserved tolerance')
            values.append((bound,measured))
        axes[0].scatter([x for x,y in values],[y for x,y in values],s=12,marker=marker,alpha=.65,label=f'{mode} ({len(values)} cases)')
    axes[0].plot([0,1],[0,1],'k:',linewidth=1);axes[0].set(xlabel='Density-based absolute-TV bound',ylabel='Full-law boson–distinguishable TV',title='Preserved supervised finite checks',xlim=(0,1),ylim=(0,1));axes[0].legend(fontsize=7)
    dilute=evidence['density']['primary']['dilute_counterexamples']
    axes[1].semilogx([r['certificate']['expected_collision_pairs'] for r in dilute],[r['actual_tv'] for r in dilute],'o-')
    from matplotlib.ticker import NullFormatter
    masses=sorted({r['certificate']['expected_collision_pairs'] for r in dilute})
    ticks=[masses[0],masses[len(masses)//2],masses[-1]]
    axes[1].set_xticks(ticks,[f'{value:.3g}' for value in ticks]);axes[1].xaxis.set_minor_formatter(NullFormatter())
    axes[1].set(xlabel='Mean collision pairs M',ylabel='Full-law TV',title='Dilution alone is insufficient',ylim=(0,1))
    fig.supxlabel('All collisions retained. Float estimates are not interval certificates, performance gains or novelty evidence.',fontsize=7)
    save_pdf(fig,root/OUTPUTS[5],'Supervised density finite evidence and dilution control');plt.close(fig)
    loss=evidence['loss'];fig,axes=plt.subplots(1,2,figsize=(8.5,3.9),constrained_layout=True)
    keys=sorted({(r['criterion'],r['m']-r['source']) for r in loss['transitions']})
    for criterion,deficit in keys:
        rows=sorted([r for r in loss['transitions'] if (r['criterion'],r['m']-r['source'])==(criterion,deficit)],key=lambda r:r['m'])
        mids=[float((fraction(r['scaled_loss_low'])+fraction(r['scaled_loss_high']))/2) for r in rows]
        errors=[float((fraction(r['scaled_loss_high'])-fraction(r['scaled_loss_low']))/2) for r in rows]
        label=('Attempt' if criterion=='per_attempt' else 'Photon')+f': deficit {deficit} to {deficit-1}'
        axes[0].errorbar([r['m'] for r in rows],mids,yerr=errors,marker='o',markersize=3,label=label)
    axes[0].set(xlabel='Modes m',ylabel='Critical scaled loss m(1−η)',title='Exact rational brackets; midpoint display');axes[0].legend(fontsize=6)
    m=max(r['m'] for r in loss['transitions']);end=max(float(fraction(r['scaled_loss_high'])) for r in loss['transitions'] if r['m']==m)*1.2
    for criterion in sorted({r['criterion'] for r in loss['transitions']}):
        rows=sorted([r for r in loss['transitions'] if r['m']==m and r['criterion']==criterion],key=lambda r:fraction(r['scaled_loss_low']))
        boundaries=[float((fraction(r['scaled_loss_low'])+fraction(r['scaled_loss_high']))/2) for r in rows]
        deficits=[m-r['source'] for r in rows]
        axes[1].step([0,*boundaries,end],[*deficits,0,0],where='post',label='Per attempt' if criterion=='per_attempt' else 'Per photon')
    axes[1].set(xlabel=f'Scaled loss {m}(1−η)',ylabel='Optimal source deficit m−N',title=f'Open phase intervals, m={m}');axes[1].legend(fontsize=7)
    fig.supxlabel('Haar-averaged threshold feasibility. Brackets are exact; plotted steps show open phase intervals.',fontsize=7)
    save_pdf(fig,root/OUTPUTS[6],'P37 exact source-transition brackets');plt.close(fig)


def check(root,archive=None):
    path=root/MANIFEST;require(path.is_file(),'Publication manifest missing; build first')
    manifest=json.loads(path.read_text());require(manifest.get('schema_version')==1,'Unsupported publication manifest')
    require(manifest['generator']['path']==GENERATOR,'Unexpected generator path')
    require(sha(resolve(root,archive,GENERATOR))==manifest['generator']['sha256'],'Generator SHA mismatch')
    require({r['path'] for r in manifest['inputs']}==set(INPUTS),'Input set differs')
    require({r['path'] for r in manifest['outputs']}==set(OUTPUTS),'Output set differs')
    for row in manifest['inputs']:require(sha(resolve(root,archive,row['path']))==row['sha256'],'Input SHA mismatch: '+row['path'])
    for row in manifest['outputs']:require((root/row['path']).is_file() and sha(root/row['path'])==row['sha256'],'Output SHA mismatch: '+row['path'])
    return manifest


def build(root,archive=None):
    require(sha(resolve(root,archive,GENERATOR))==sha(Path(__file__)),'Executed generator differs from requested root')
    evidence=load_evidence(root,archive)
    for name in OUTPUTS:(root/name).parent.mkdir(parents=True,exist_ok=True)
    counts=write_tables(root,evidence);figures(root,evidence)
    for name,path in evidence['input_paths'].items():require(sha(path)==evidence['input_hashes'][name],'Input changed during build: '+name)
    manifest=dict(schema_version=1,generator=dict(path=GENERATOR,sha256=sha(Path(__file__))),
                  inputs=[dict(path=name,sha256=digest) for name,digest in sorted(evidence['input_hashes'].items())],
                  outputs=[dict(path=name,sha256=sha(root/name)) for name in OUTPUTS],counts=counts,
                  software={name:importlib.metadata.version(name) for name in ('matplotlib','numpy')},
                  pdf_metadata=dict(CreationDate=FIXED_DATE.isoformat(),ModDate=FIXED_DATE.isoformat(),font_family='DejaVu Sans',fonttype=42),
                  semantics=['No manually supplied performance values','Exact rational source selection and computed four-vertex graph controls',
                             'E05b intervals are descriptive graph-cluster intervals; same graphs trained and evaluated',
                             'Only supervised preserved P33 captures; no root P33 data','No new scientific experiment or hardware result'])
    (root/MANIFEST).write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n');check(root,archive);return manifest


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);parser.add_argument('--archive-root',type=Path);parser.add_argument('--check',action='store_true')
    args=parser.parse_args(argv);root=args.root.resolve();archive=args.archive_root.resolve() if args.archive_root else None
    try:manifest=check(root,archive) if args.check else build(root,archive)
    except (PublicationError,KeyError,FileNotFoundError) as error:print(str(error),file=sys.stderr);return 1
    print(json.dumps(dict(status='CHECK_PASS' if args.check else 'BUILD_PASS',outputs=len(manifest['outputs']),counts=manifest['counts'])))
    return 0
if __name__=='__main__':raise SystemExit(main())
