"""P21 bounded-block classical spoofing control and matched phase-1 query audit."""
from datetime import datetime,timezone
import hashlib,itertools,json,platform,subprocess,sys,time
from pathlib import Path
import numpy as np
import scipy
from photonic_balanced_partitioning.photonic.fixed_photon_obliq import FixedPhotonObliq

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
INPUTS=[Path(__file__).relative_to(ROOT),OUT.relative_to(ROOT)/'runs.jsonl',
    OUT.relative_to(ROOT)/'graphs.json',Path('experiments/E05b_exact_equal_budget/runs.jsonl'),
    Path('src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py')]
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
before={str(p):sha(p) for p in INPUTS};started=datetime.now(timezone.utc).isoformat();start=time.perf_counter()
block_rows=[]
for b in (4,6):
    r=b//2;n=2*b;k=2*r
    sa=FixedPhotonObliq(b,r);sb=FixedPhotonObliq(b,r)
    ua=sa.random_interferometer(20261120+b);ub=sb.random_interferometer(20261220+b)
    pa=abs(sa.output_state(ua))**2;pb=abs(sb.output_state(ub))**2
    U=np.zeros((n,n),dtype=complex)
    U[:b,:r]=ua[:,:r];U[b:,r:2*r]=ub[:,:r]
    U[:b,2*r:2*r+b-r]=ua[:,r:];U[b:,2*r+b-r:]=ub[:,r:]
    full=FixedPhotonObliq(n,k);p=abs(full.output_state(U))**2
    local_states=sa._enumerate_all_fock_states();index={s:i for i,s in enumerate(local_states)}
    product=[]
    for state in full._enumerate_all_fock_states():
        a,c=state[:b],state[b:]
        product.append(pa[index[a]]*pb[index[c]] if a in index and c in index else 0.)
    product=np.array(product)
    residual=float(np.max(abs(p-product)))
    assert residual<1e-12
    rng=np.random.default_rng(20261120+100*b)
    a_draw=rng.choice(len(pa),size=10000,p=pa/pa.sum())
    b_draw=rng.choice(len(pb),size=10000,p=pb/pb.sum())
    counts=np.bincount(a_draw*len(pb)+b_draw,minlength=len(pa)*len(pb))
    assert counts.sum()==10000
    block_rows.append(dict(n=n,k=k,block_modes=b,photons_per_block=r,
        local_table_size=len(pa),joint_product_table_size=len(pa)*len(pb),
        global_full_fock_size=len(p),max_full_distribution_difference=residual,
        exact_total_variation=float(abs(p-product).sum()/2),
        occupied_column_order='first r in block A, next r in block B',
        seeds=[20261120+b,20261220+b,20261120+100*b],
        ua_real=ua.real.tolist(),ua_imag=ua.imag.tolist(),ub_real=ub.real.tolist(),ub_imag=ub.imag.tolist(),
        local_occupations=local_states,pa=pa.tolist(),pb=pb.tolist(),
        sampled_joint_counts=counts.tolist(),sampler_shots=10000,
        interpretation='Exact factorization; finite frequencies not used to establish equality'))
reference={g['graph_id']:g for g in json.loads((OUT/'graphs.json').read_text())}
classical=[];per_family=[]
with (OUT/'runs.jsonl').open() as stream:
    for line in stream:
        r=json.loads(line)
        if r['n'] in (4,6,8) and r['label_id']==0 and r['instance']<2 and r['repeat']<3:
            classical.append({k:v for k,v in r.items() if k!='trace'})
        if r['n']==12:
            per_family.append({k:v for k,v in r.items() if k!='trace'})
old=[]
with (ROOT/'experiments/E05b_exact_equal_budget/runs.jsonl').open() as stream:
    for line in stream:
        r=json.loads(line)
        if r['model'] in ('bosonic','distinguishable','random_balanced'):
            gid=f"n{r['n']}-{r['family']}-i{r['instance']}-L0"
            norm=lambda edges:sorted((min(i,j),max(i,j),float(w)) for i,j,w in edges)
            assert norm(reference[gid]['edges'])==norm(r['edges'])
            old.append(dict(n=r['n'],family=r['family'],instance=r['instance'],seed=r['seed'],
                model=r['model'],first_optimum_attempt=r['first_optimum_attempt'],total_shots=r['total_shots'],
                final_p_success=r['final_p_success']))
comparison=[]
for n in (4,6,8):
    for algorithm in ('random_feasible','swap_anneal','spectral_swap_local'):
        sub=[r for r in classical if r['n']==n and r['algorithm']==algorithm]
        first=[r['first_optimum_query'] for r in sub if r['first_optimum_query'] is not None]
        comparison.append(dict(n=n,method=algorithm,cost_unit='classical cut queries',runs=len(sub),found=len(first),
            median_first_given_found=float(np.median(first)) if first else None,
            max_query_budget=120,physical_qpu_attempts=0))
    for model in ('bosonic','distinguishable','random_balanced'):
        sub=[r for r in old if r['n']==n and r['model']==model]
        first=[r['first_optimum_attempt'] for r in sub if r['first_optimum_attempt'] is not None]
        comparison.append(dict(n=n,method='E05b_'+model,cost_unit='ideal simulated draws including optical collisions',
            runs=len(sub),found=len(first),median_first_given_found=float(np.median(first)) if first else None,
            max_attempt_budget=34816,physical_qpu_attempts=0))
n12=[]
for family in ('path','cycle','regular','erdos_renyi','weighted','planted'):
    for alg in ('random_feasible','swap_anneal','spectral_swap_local'):
        sub=[r for r in per_family if r['family']==family and r['algorithm']==alg]
        n12.append(dict(family=family,algorithm=alg,runs=len(sub),found=sum(r['found_optimum'] for r in sub),
            mean_gap=float(np.mean([r['best_normalized_gap'] for r in sub]))))
after={str(p):sha(p) for p in INPUTS};assert before==after
result=dict(status='completed',assertion_tested='Block-product sampler equals complete bosonic Fock distribution for two fixed block sizes; classical/phase1 matched-instance cost audit',
    classical_block_controls=block_rows,matched_instance_cost_summary=comparison,n12_family_summary=n12,
    non_claims=['Classical cut queries and optical shots are different cost units','No physical or quantum advantage conclusion from small blocks','Table enumeration is efficient only for bounded block size'],
    source_hashes_before=before,source_hashes_after=after,runtime_seconds=time.perf_counter()-start)
path=OUT/'smallblock_and_comparison.json';path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
manifest=dict(schema_version=2,claim_id='P21_supplementary_blocks_and_comparison',
    repository=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),dirty=True),
    command=[sys.executable,*sys.argv],environment=dict(software=[dict(name='Python',version=platform.python_version()),dict(name='NumPy',version=np.__version__),dict(name='SciPy',version=scipy.__version__)],hardware=platform.platform()),
    mathematics=dict(assertion_tested=result['assertion_tested'],coefficient_domain='complex128/float64',
        conventions='Full Fock probabilities unconditioned on CF; input photons in first k global modes',inputs=['two 4-mode 2-photon blocks','two 6-mode 3-photon blocks','matched E05b/P21 instances n4/6/8'],bounds=dict(block_sizes=[4,6],shots_per_sampler=10000),non_claims=result['non_claims']),
    randomness=dict(used=True,generator='NumPy default_rng PCG64',seed=20261120),
    run=dict(started_at=started,runtime_seconds=time.perf_counter()-start,exit_status=0,status='completed',resource_limits=dict(memory_bytes=None,cpu_seconds=None,max_cores=None,max_threads=1)),
    outputs=[dict(path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),kind='result')],
    checks=[dict(check='input hashes unchanged',passed=True),dict(check='full distribution equals product table within 1e-12',passed=True)],
    result='Finite assertion verified',residual_risks=['Manual v2 recorder without hard memory/time caps','No iid population inference'],
    input_artifacts=[dict(path=p,sha256=before[p],sha256_after=after[p]) for p in before],declared_results=[str(path.relative_to(ROOT))])
(OUT/'supplementary_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'blocks':[(r['n'],r['local_table_size'],r['max_full_distribution_difference']) for r in block_rows],'comparison':comparison,'runtime':time.perf_counter()-start},indent=2))
