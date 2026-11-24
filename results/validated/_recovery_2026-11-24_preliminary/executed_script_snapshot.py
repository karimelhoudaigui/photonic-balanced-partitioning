#!/usr/bin/env python3
"""Read-only historical evidence reconciliation; never launches experiment drivers.

Use --archive-root for the original repository/archive, --output for a NEW
processed-results directory. Only --output is written. Historical source pins
are compared to git blobs at their recorded revision, not required to equal HEAD.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,math,statistics,subprocess,sys,time
from collections import Counter,defaultdict
from datetime import datetime,timezone
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.stats import t as student_t

SCHEMA_VERSION=1
FAMILIES=('path','cycle','regular','erdos_renyi','weighted','planted')
MODELS=(('bosonic',None),('distinguishable',None),('multinomial',None),
        ('classical_penalty',.1),('classical_penalty',1.),('classical_penalty',10.),('random_balanced',None))
EXCLUDED=('results/P33_density_primary/','results/P33_density_replication/')
ORACLE_OBJECTIVES={'success','factorized','conditional_success'}
class AuditError(ValueError):pass

def require(condition,message):
    if not condition:raise AuditError(message)
def sha_bytes(data):return hashlib.sha256(data).hexdigest()
def file_sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
    return h.hexdigest()
def dump(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False,sort_keys=True)+'\n')
def close(a,b,tol=1e-8):return a is not None and b is not None and abs(float(a)-float(b))<=tol

def graph_hash(n,edges):
    normalized=sorted((min(int(i),int(j)),max(int(i),int(j)),float(w)) for i,j,w in edges)
    return sha_bytes(json.dumps([n,normalized],separators=(',',':')).encode())

@lru_cache(maxsize=None)
def cost_table(n,edge_tuple,penalty):
    states=(list(itertools.product((0,1),repeat=n)) if penalty else
            [tuple(int(i in selected) for i in range(n)) for selected in itertools.combinations(range(n),n//2)])
    cuts=[sum(w for i,j,w in edge_tuple if bits[i]!=bits[j]) for bits in states]
    feasible=[sum(bits)==n//2 for bits in states]
    balance=[(sum(bits)-n//2)**2 for bits in states]
    if not penalty:cuts.append(None);feasible.append(False);balance.append(0)
    return cuts,feasible,balance

def wilson(successes,total):
    z=1.959963984540054;p=successes/total;den=1+z*z/total
    centre=(p+z*z/(2*total))/den
    half=z*math.sqrt(p*(1-p)/total+z*z/(4*total*total))/den
    return [max(0.,centre-half),min(1.,centre+half)]

def audit_equal_run(row,*,budget=120,batch=256,heldout=4096):
    """Reconstruct loss/count/best-found invariants; first-shot order is not saved."""
    n=row['n'];penalty=row['model']=='classical_penalty';uniform=row['model']=='random_balanced'
    edges=tuple((int(i),int(j),float(w)) for i,j,w in row['edges'])
    costs,feasible,balance=cost_table(n,edges,penalty)
    if uniform:costs,feasible,balance=costs[:-1],feasible[:-1],balance[:-1]
    optimum=min(c for c,f in zip(costs,feasible) if f)
    require(close(optimum,row['optimum']),'wrong retrospective optimum')
    optimum_mask=[f and abs(c-optimum)<=1e-9 for c,f in zip(costs,feasible)]
    trace=row['trace'];require(len(trace)==budget==row['n_evaluations'],'objective-call budget mismatch')
    require(row['training_shots']==budget*batch and row['heldout_shots']==heldout,'allocation mismatch')
    require(row['total_shots']==row['sample_score_lookups']==budget*batch+heldout,'total/lookup mismatch')
    require(row['reference_cost_table_size']==len(costs),'basis/table size mismatch')
    feasible_total=optimal_total=0;best=None;first_batch=None;first_saved=None;max_loss_error=0.
    def counts_check(counts,total):
        require(len(counts)==len(costs),'count basis mismatch')
        require(all(isinstance(x,int) and not isinstance(x,bool) and x>=0 for x in counts),'invalid counts')
        require(sum(counts)==total,'count total mismatch')
        valid=sum(x for x,f in zip(counts,feasible) if f)
        optimal=sum(x for x,f in zip(counts,optimum_mask) if f)
        seen=[c for c,f,x in zip(costs,feasible,counts) if f and x]
        return valid,optimal,min(seen) if seen else None
    for index,event in enumerate(trace):
        require(event['evaluation']==index+1,'evaluation index mismatch')
        counts=event['counts'];valid,opt,local_best=counts_check(counts,batch)
        require(valid==event['feasible_count'] and opt==event['optimal_count'],'retrospective count mismatch')
        if penalty:
            loss=sum(x*(c+row['lambda_value']*b) for x,c,b in zip(counts,costs,balance))/batch
        elif valid:
            loss=sum(x*c for x,c,f in zip(counts,costs,feasible) if f)/valid+2*(1-valid/batch)
        else:loss=sum(abs(w) for _,_,w in edges)+3
        max_loss_error=max(max_loss_error,abs(loss-event['loss']))
        require(close(loss,event['loss']),'loss differs from observed costs/feasibility only')
        if local_best is not None:best=local_best if best is None else min(best,local_best)
        require((best is None and event['best_valid_cost_so_far'] is None) or close(best,event['best_valid_cost_so_far']),
                'best-found training cost mismatch')
        if first_batch is None and opt:
            first_batch=index+1;first_saved=event['first_optimum_attempt_so_far']
            require(isinstance(first_saved,int) and index*batch<first_saved<=(index+1)*batch,'first hit outside first winning batch')
        require(event['first_optimum_attempt_so_far']==first_saved,'first-hit history changed or premature hit')
        feasible_total+=valid;optimal_total+=opt
    require(feasible_total==row['training_feasible_count'] and optimal_total==row['training_optimal_count'],
            'training aggregate count mismatch')
    chosen=min(range(len(trace)),key=lambda i:trace[i]['loss'])
    require(row['parameters']==trace[chosen]['parameters'],'selected parameters do not minimize observed training loss')
    valid,opt,local_best=counts_check(row['heldout_counts'],heldout)
    require(opt==row['heldout_optimal_count'],'heldout optimal count mismatch')
    if local_best is not None:best=local_best if best is None else min(best,local_best)
    require(close(best,row['best_valid_cost']),'best-found final cost mismatch')
    first=row['first_optimum_attempt']
    if first_saved is not None:require(first==first_saved,'final first hit changed after training')
    elif opt:require(isinstance(first,int) and budget*batch<first<=budget*batch+heldout,'heldout first hit invalid')
    else:require(first is None,'uncensored hit without success counts')
    require(all(close(a,b,1e-12) for a,b in zip(wilson(opt,heldout),row['success_ci95'])),'Wilson mismatch')
    ps=row['final_p_success'];pf=row['final_p_feasible']
    require(0<=ps<=pf+1e-10 and pf<=1+1e-9,'invalid saved final probabilities')
    if ps:require(close(1/ps,row['final_expected_shots'],max(1e-8,1e-10/ps)),'reciprocal metric mismatch')
    if uniform:
        require(close(ps,sum(optimum_mask)/len(costs),1e-12) and close(pf,1,1e-12),'uniform analytical result mismatch')
    return dict(audit_pass=True,max_loss_error=max_loss_error,first_training_success_batch=first_batch,
                heldout_feasible_count=valid,selected_evaluation=chosen+1,
                first_hit_validation='earliest_winning_batch_only; within-batch draw order not retained',
                graph_hash=graph_hash(n,edges),optimal_balanced_partitions=sum(optimum_mask))


def cluster_interval(rows,key,seed=20261124,resamples=2000):
    """Descriptive graph-cluster bootstrap; never treats optimizer repeats as graphs."""
    clusters=defaultdict(list)
    for r in rows:clusters[r['graph_hash']].append(float(r[key]))
    totals=np.array([sum(x) for _,x in sorted(clusters.items())]);sizes=np.array([len(x) for _,x in sorted(clusters.items())])
    if len(totals)<2:return None,len(totals)
    rng=np.random.default_rng(seed);indices=rng.integers(0,len(totals),(resamples,len(totals)))
    means=totals[indices].sum(axis=1)/sizes[indices].sum(axis=1)
    return [float(x) for x in np.quantile(means,[.025,.975])],len(totals)


class Archive:
    def __init__(self,root):self.root=root.resolve();self.inputs={};self.blobs={};self.sources={}
    def pin(self,path):
        path=path.resolve()
        if path not in self.inputs:self.inputs[path]=file_sha(path)
        return self.inputs[path]
    def read(self,path):self.pin(path);return json.loads(path.read_text())
    def blob(self,commit,path):
        key=(commit,path)
        if key not in self.blobs:
            run=subprocess.run(['git','-C',str(self.root),'show',f'{commit}:{path}'],capture_output=True)
            self.blobs[key]=run.stdout if run.returncode==0 else None
        return self.blobs[key]
    def source(self,commit,item):
        name=item.get('path','');expected=item.get('sha256');after=item.get('sha256_after')
        key=(commit,name,expected)
        if key in self.sources:return self.sources[key]
        blob=self.blob(commit,name) if commit else None;historical=sha_bytes(blob) if blob is not None else None
        actual=self.root/name if not Path(name).is_absolute() and '..' not in Path(name).parts else None
        current=self.pin(actual) if actual is not None and actual.is_file() else None
        status=('matched_recorded_commit' if historical==expected else
                'available_pinned_snapshot_only' if current==expected else 'unresolved_historical_snapshot')
        record=dict(recorded_commit=commit,path=name,expected_sha256=expected,recorded_after_sha256=after,
                    historical_commit_sha256=historical,current_snapshot_sha256=current,status=status,
                    original_before_after_equal=expected==after and after is not None)
        self.sources[key]=record;return record
    def output(self,manifest_path,manifest,item):
        name=item.get('path','');expected=item.get('sha256');candidates=[]
        path=Path(name)
        if not path.is_absolute() and '..' not in path.parts:candidates.append(self.root/path)
        output_dir=manifest.get('output_directory')
        if output_dir:
            try:candidates.insert(0,manifest_path.parent/path.relative_to(output_dir))
            except ValueError:pass
        candidates.append(manifest_path.parent/path.name)
        observed=[];seen=set()
        for candidate in candidates:
            if candidate in seen or not candidate.is_file():continue
            seen.add(candidate);digest=self.pin(candidate)
            observed.append(dict(path=str(candidate.relative_to(self.root)),sha256=digest))
            if digest==expected:return dict(path=name,expected_sha256=expected,status='verified',
                                          resolved_path=str(candidate.relative_to(self.root)),observed=observed)
        return dict(path=name,expected_sha256=expected,status='missing_or_mismatched',observed=observed)


def relevant(path):return any(part.startswith(('E0','P20','P21','P30','P31','P32','P33','P34','P35','P36','P37','P38','P39')) for part in path.parts)
def excerpt(summary):
    if not isinstance(summary,dict):return {'type':type(summary).__name__,'count':len(summary) if hasattr(summary,'__len__') else None}
    return {key:(value if isinstance(value,(str,int,float,bool,type(None))) else {'type':type(value).__name__,'count':len(value)})
            for key,value in summary.items()}


def inventory(archive):
    records=[]
    for top in ('experiments','results'):
        for p in sorted((archive.root/top).rglob('*manifest*.json')):
            rel=str(p.relative_to(archive.root))
            if not relevant(p.relative_to(archive.root)):continue
            m=archive.read(p)
            if not isinstance(m,dict) or 'schema_version' not in m:continue
            commit=m.get('repository',{}).get('commit');run=m.get('run',{});outputs=[archive.output(p,m,x) for x in m.get('outputs',[])]
            sources=[archive.source(commit,x) for x in m.get('input_artifacts',[])]
            summaries=[]
            for candidate in [p.parent/'summary.json',p.parent/'data/summary.json']:
                if candidate.is_file():summaries.append(dict(path=str(candidate.relative_to(archive.root)),content=excerpt(archive.read(candidate))))
            excluded=rel.startswith(EXCLUDED)
            ok=bool(outputs) and all(x['status']=='verified' for x in outputs)
            unresolved=sum(x['status']=='unresolved_historical_snapshot' for x in sources)
            status=('excluded_no_original_result_provenance' if excluded else
                    'preserved_failed_run' if run.get('status')!='completed' else
                    'output_hashes_verified_source_snapshot_gaps' if ok and unresolved else
                    'output_hashes_verified' if ok else 'output_hash_failure_or_missing')
            records.append(dict(manifest=rel,manifest_sha256=archive.inputs[p.resolve()],schema_version=m.get('schema_version'),
                claim_id=m.get('claim_id'),repository=m.get('repository'),run=run,classification=status,
                outputs=outputs,source_status_counts=dict(Counter(x['status'] for x in sources)),
                sources_before_after_stable=all(x['original_before_after_equal'] for x in sources),
                summary_metadata=summaries,publication_performance_eligible=False,
                scope='metadata/output-hash audit; no new scientific rerun',
                exclusion_reason='Root P33 raw/summary were added later without original declared result hashes; use only supervised preserved captures with their own provenance' if excluded else None))
    return records


def reconcile_haar(archive):
    path=archive.root/'experiments/E01_haar_collision_baseline/raw.csv';archive.pin(path)
    with path.open() as f:rows=list(csv.DictReader(f))
    groups=[]
    for n in sorted({int(r['n']) for r in rows}):
        selected=[r for r in rows if int(r['n'])==n];values=np.array([float(r['p_cf']) for r in selected]);k=n//2
        require(len({r['seed'] for r in selected})==len(selected),'duplicate Haar seeds')
        half=float(student_t.ppf(.975,len(values)-1)*values.std(ddof=1)/math.sqrt(len(values)))
        groups.append(dict(n=n,k=k,circuits=len(selected),p_cf_mean=float(values.mean()),
                           p_cf_ci95_independent_circuits=[float(values.mean()-half),float(values.mean()+half)],
                           theory_numerator=math.comb(n,k),theory_denominator=math.comb(n+k-1,k),
                           theory_p_cf=math.comb(n,k)/math.comb(n+k-1,k),
                           p_success_path_mean=float(np.mean([float(r['p_success']) for r in selected])),
                           interpretation='Ideal Haar-circuit ensemble mean; independent circuit uncertainty, not device shots'))
    return dict(raw_rows=len(rows),groups=groups,physical_qpu_attempts=0,n12_empirical_data=False)


def reconcile_equal(archive):
    path=archive.root/'experiments/E05b_exact_equal_budget/runs.jsonl';archive.pin(path)
    records=[];graphs={};errors=[];seen=set()
    with path.open() as stream:
        for index,line in enumerate(stream,1):
            row=json.loads(line);key=(row['n'],row['family'],row['instance'],row['seed'],row['model'],row['lambda_value'])
            require(key not in seen,'duplicate E05b run key');seen.add(key)
            try:check=audit_equal_run(row)
            except AuditError as error:check=dict(audit_pass=False,error=str(error),graph_hash=graph_hash(row['n'],row['edges']));errors.append(dict(line=index,error=str(error)))
            record={k:v for k,v in row.items() if k not in ('trace','edges','parameters','heldout_counts','success_ci95','expected_shots_ci95')}
            record.update(check);record['heldout_success_rate']=row['heldout_optimal_count']/row['heldout_shots']
            record['success_ci95_low'],record['success_ci95_high']=row['success_ci95']
            record['training_uses_optimum']=False;record['training_objective']='penalized_binary_energy' if row['model']=='classical_penalty' else 'sampled_conditional_cut_plus_2_collision_rate'
            records.append(record)
            slot=(row['n'],row['family'],row['instance'])
            value=dict(n=row['n'],family=row['family'],instance=row['instance'],graph_seed=row['graph_seed'],graph_hash=check['graph_hash'],edges=row['edges'],optimum_for_evaluation=row['optimum'])
            require(slot not in graphs or graphs[slot]==value,'graph changed between methods/repeats');graphs[slot]=value
    expected={(n,family,instance,20261120+100000*n+1000*instance+repeat,model,lam)
              for n in (4,6,8) for family in FAMILIES for instance in range(2) for repeat in range(3) for model,lam in MODELS}
    require(seen==expected,'E05b declared grid coverage differs from raw keys')
    groups=[]
    for n in (4,6,8):
        for groupindex,(model,lam) in enumerate(MODELS):
            subset=[r for r in records if (r['n'],r['model'],r['lambda_value'])==(n,model,lam)]
            interval,clusters=cluster_interval(subset,'final_p_success',20261124+n*100+groupindex)
            hits=[r['first_optimum_attempt'] for r in subset if r['first_optimum_attempt'] is not None]
            groups.append(dict(n=n,model=model,lambda_value=lam,runs=len(subset),nominal_instance_slots=12,
                unique_graphs=clusters,final_p_success_mean=statistics.mean(r['final_p_success'] for r in subset),
                instance_interval=interval,interval_kind='descriptive_95pct_graph_cluster_bootstrap_percentiles_2000',
                mean_final_p_feasible=statistics.mean(r['final_p_feasible'] for r in subset),
                mean_heldout_success_rate=statistics.mean(r['heldout_success_rate'] for r in subset),
                mean_reciprocal_final_success=statistics.mean(r['final_expected_shots'] for r in subset if r['final_expected_shots'] is not None),
                reciprocal_mean_final_success=1/statistics.mean(r['final_p_success'] for r in subset),
                found_optimum_runs=len(hits),found_in_training=sum(r['training_optimal_count']>0 for r in subset),
                censored_runs=len(subset)-len(hits),median_first_attempt_given_found=statistics.median(hits) if hits else None,
                best_valid_cost_mean=statistics.mean(r['best_valid_cost'] for r in subset),
                training_attempts_per_run=30720,heldout_attempts_per_run=4096,total_attempts_per_run=34816,
                objective_calls_per_run=120,all_runs_audit_pass=all(r['audit_pass'] for r in subset)))
    original=archive.read(archive.root/'experiments/E05b_exact_equal_budget/summary.json')
    for group in groups:
        old=next(x for x in original['results'] if (x['n'],x['model'],x['lambda_value'])==(group['n'],group['model'],group['lambda_value']))
        require(close(old['final_p_success']['mean'],group['final_p_success_mean'],1e-12),'original aggregate success differs from raw reconstruction')
    paired=[]
    for n in (4,6,8):
        left={(r['family'],r['instance'],r['seed']):r for r in records if r['n']==n and r['model']=='bosonic'}
        right={(r['family'],r['instance'],r['seed']):r for r in records if r['n']==n and r['model']=='distinguishable'}
        differences=[dict(graph_hash=r['graph_hash'],difference=r['final_p_success']-right[k]['final_p_success']) for k,r in left.items()]
        interval,clusters=cluster_interval(differences,'difference',20261124+n)
        paired.append(dict(n=n,mean_bosonic_minus_distinguishable=statistics.mean(r['difference'] for r in differences),
                           instance_interval=interval,unique_graphs=clusters,interval_kind='descriptive_graph_cluster_bootstrap'))
    return dict(raw_runs=len(records),all_runs_audit_pass=not errors,audit_errors=errors,groups=groups,graphs=list(graphs.values()),
                paired_bosonic_minus_distinguishable=paired,total_simulated_attempts=sum(r['total_shots'] for r in records),
                physical_qpu_attempts=0,all_optima_found_during_training=all(r['training_optimal_count']>0 for r in records),
                limitations=['Same graphs are trained and scored; heldout means independent measurement stream, not unseen graph generalization',
                 'Graph-cluster intervals are descriptive, not validated population confidence: fixed families, few unique graphs and reused generator seeds',
                 'All optimizer repeats for the same labeled weighted graph stay together in uncertainty calculations',
                 'Exact within-batch first-hit order is not reconstructible from count vectors',
                 'Attempts are ideal simulated source/detection-free draws; score lookups are not total classical query/setup cost',
                 'Each penalty lambda is a separate run; no free best-lambda selection',
                 'Penalty is classical product Bernoulli, not authentic optical ObliQ; no parameter-count or runtime matching']),records


def raw_catalogue(archive):
    result=[]
    for name in ['E02_ideal_optimization','E03_objectives_pareto','E04_optimizers_depths','E05_equal_shots','E07_spectral_hybrid','E09_label_control','P21_classical_search']:
        p=archive.root/'experiments'/name/'runs.jsonl'
        if not p.is_file():continue
        archive.pin(p);count=0;profiles=Counter();stats=defaultdict(list);familystats=defaultdict(list);oracle=0
        with p.open() as f:
            for line in f:
                r=json.loads(line);count+=1;obj=r.get('objective','success' if name.startswith('E09') else None)
                oracle+=obj in ORACLE_OBJECTIVES
                key=(r.get('n'),r.get('model',r.get('algorithm')),obj,r.get('method'),r.get('depth'))
                profiles[key]+=1
                value=r.get('after',{}).get('p_success',r.get('metrics',{}).get('p_success'))
                if value is not None:
                    stats[key].append(float(value));familystats[(r.get('family'),*key)].append(float(value))
        result.append(dict(campaign=name,raw_runs=count,explicit_oracle_objective_runs=oracle,
            profiles=[dict(n=k[0],model=k[1],objective=k[2],method=k[3],depth=k[4],runs=v,
                           p_success_mean=statistics.mean(stats[k]) if stats[k] else None) for k,v in sorted(profiles.items(),key=lambda x:str(x[0]))],
            family_profiles=[dict(family=k[0],n=k[1],model=k[2],objective=k[3],method=k[4],depth=k[5],runs=len(v),p_success_mean=statistics.mean(v),minimum=min(v),maximum=max(v)) for k,v in sorted(familystats.items(),key=lambda x:str(x[0]))],
            scope='raw row/domain/metric aggregation only; original optimizer not rerun'))
    return result


def claims(catalogue):
    claims=[]
    for n,claimed in [(4,1.),(6,.982),(8,.537),(10,.112),(12,.034)]:
        profiles=[r for c in catalogue if c['campaign']=='E02_ideal_optimization' for r in c['family_profiles'] if r['family']=='path' and r['n']==n and r['model']=='bosonic' and r['method']=='COBYLA']
        claims.append(dict(source='cf49741 reports/RESEARCH_CHECKPOINT_FINAL.md; path variational table',n=n,claimed_success=claimed,
            disposition='unsupported_by_identified_raw_trace' if n in (10,12) else ('rounded_oracle_aggregate_match_not_blind_solver_evidence' if any(round(r['p_success_mean'],3)==claimed for r in profiles) else 'untraced_number_cannot_substitute_oracle_E02_for_blind_E05b'),
            known_scope='No E05b runs at n10/12; E02 trains on true optimum success' if n in (10,12) else 'Available E02 values are optimum-oracle state-preparation diagnostics, not blind equal-cost optimization',
            available_E02_aggregate_profiles=profiles))
    claims.extend([dict(source='cf49741 final checkpoint',claim='Bosonic advantage emerges at n>=8, up to4.81x',disposition='unsupported_and_contradicted_by_blind_E05b_aggregate',note='No general superiority follows; E05b distinguishable mean exceeds bosonic mean at every tested n'),
                   dict(source='cf49741 experimental summary',claim='E05b200 evaluations,1.1x–10x gain',disposition='incorrect_protocol_and_unsupported_numbers',note='Raw E05b uses120 objective calls and34816 draws per run; lambdas separate; discovery already occurs in training'),
                   dict(source='cf49741 experimental summary',claim='E03objective table at n8/path',disposition='outside_recorded_campaign_domain',note='Recorded E03 is n4 only'),
                   dict(source='cf49741/6154b46',claim='Empirical Haar/variational scaling through n12 and hardware-like results',disposition='unsupported',note='Haar raw sizes4/6/8/10; E05b sizes4/6/8; no hardware attempts in these archives')])
    return claims


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--archive-root',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--runner-created-directory',action='store_true');args=parser.parse_args(argv)
    root=args.archive_root.resolve();output=args.output.resolve()
    require(root!=output,'invalid output')
    if output.exists() and (not args.runner_created_directory or any(p.name not in {'stdout.txt','stderr.txt'} for p in output.iterdir())):
        raise SystemExit('Refusing to overwrite processed results; use a new output directory')
    require(not any(output==root/x or (root/x) in output.parents for x in ('experiments','results/P33_density_primary','results/P33_density_replication')),'Refusing writes in historical evidence')
    started=datetime.now(timezone.utc).isoformat();clock=time.monotonic();archive=Archive(root)
    campaigns=inventory(archive);equal,bench=reconcile_equal(archive);haar=reconcile_haar(archive);catalogue=raw_catalogue(archive)
    summary=dict(schema_version=SCHEMA_VERSION,status='RECONCILED_WITH_EXPLICIT_LIMITATIONS' if equal['all_runs_audit_pass'] else 'AUDIT_FAILURE',
                 e05b=equal,haar=haar,raw_campaign_catalogue=catalogue,unsupported_claims=claims(catalogue),
                 publication_policy=dict(real_qpu_results=False,quantum_advantage_established=False,
                    oracle_success_optimization_is_solver_evidence=False,root_P33_performance_evidence_accepted=False),
                 provenance=dict(archive_root_argument=str(root),started_at=started,script_sha256=file_sha(Path(__file__)),
                                 command=[sys.executable,*sys.argv],no_experiment_driver_executed=True))
    changed=[]
    input_records=[]
    for path,before in sorted(archive.inputs.items(),key=lambda x:str(x[0])):
        after=file_sha(path)
        if before!=after:changed.append(str(path.relative_to(root)))
        input_records.append(dict(path=str(path.relative_to(root)),sha256_before=before,sha256_after=after))
    require(not changed,'Historical inputs changed while reconciling: '+str(changed))
    output.mkdir(parents=True,exist_ok=args.runner_created_directory)
    dump(output/'summary.json',summary)
    dump(output/'campaigns.json',dict(schema_version=SCHEMA_VERSION,campaign_manifests=campaigns,
                                    classification_counts=dict(Counter(x['classification'] for x in campaigns)),
                                    interpretation='Hash integrity/status audit is not a proof of each campaign scientific claim'))
    dump(output/'source_hashes.json',dict(schema_version=SCHEMA_VERSION,recorded_source_snapshots=list(archive.sources.values()),
                                       reconciliation_inputs=input_records,all_observed_inputs_unchanged=True,
                                       runtime_seconds=time.monotonic()-clock,software=dict(python=sys.version.split()[0],numpy=np.__version__),
                                       historical_sources_need_not_match_current_HEAD=True))
    fields=list(dict.fromkeys(k for r in bench for k in r))
    with (output/'benchmark.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(bench)
    print(json.dumps(dict(status=summary['status'],e05b_runs=len(bench),haar_circuits=haar['raw_rows'],
                          campaign_manifests=len(campaigns),historical_inputs=len(input_records),
                          runtime_seconds=time.monotonic()-clock,output=str(output))))
    return 0 if equal['all_runs_audit_pass'] else 1

if __name__=='__main__':raise SystemExit(main())
