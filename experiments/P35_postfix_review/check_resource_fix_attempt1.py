"""Separate post-fix API check. Does not replay P35 scientific calculations."""
from datetime import datetime,timezone
from enum import IntEnum
from fractions import Fraction as F
import hashlib,importlib.util,json,resource,subprocess,sys,time
from pathlib import Path

ROOT=Path('/Users/karimelhoudaigui/Desktop/pasqal')
COMMIT='b5d2888f8b7f8cac32e3b5f2cc23ba0d3aa7a547'
REL='src/photonic_balanced_partitioning/photonic/threshold_marginals.py'
OUTPUT=Path(__file__).resolve().parent/'receipt.json'
if OUTPUT.exists():raise FileExistsError('Refusing to overwrite post-fix receipt')
resource.setrlimit(resource.RLIMIT_CPU,(10,10))
started=datetime.now(timezone.utc).isoformat();clock=time.monotonic()
sha=lambda data:hashlib.sha256(data).hexdigest()
source=ROOT/REL;before=sha(source.read_bytes())
committed=sha(subprocess.check_output(['git','-C',str(ROOT),'show',f'{COMMIT}:{REL}']))
assert before==committed
spec=importlib.util.spec_from_file_location('_p35_postfix_review',source)
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
checks=[]
class Unreadable:
    def __iter__(self):raise AssertionError('Frame consumed before invalid limit rejected')
invalid=[('NaN',float('nan')),('+infinity',float('inf')),('-infinity',float('-inf')),
         ('float 1.0',1.0),('Fraction 1/2',F(1,2)),('Fraction 1',F(1)),
         ('string 4','4'),('None',None),('bool true',True),('bool false',False),('complex 1',1+0j)]
for name in ('max_states','max_transitions'):
    for label,value in invalid:
        for endpoint in (mod.vacuum_probability,mod.ThresholdMarginals):
            try:endpoint(Unreadable(),**{name:value})
            except ValueError as error:assert name in str(error)
            else:raise AssertionError((name,label,endpoint.__name__,'not rejected'))
            checks.append(dict(endpoint=endpoint.__name__,argument=name,value=label,
                               rejected_before_frame_read=True))
for name,value in [('max_states',0),('max_states',-1),('max_transitions',-1)]:
    for endpoint in (mod.vacuum_probability,mod.ThresholdMarginals):
        try:endpoint(Unreadable(),**{name:value})
        except ValueError as error:assert name in str(error)
        else:raise AssertionError((name,value,'invalid boundary accepted'))
        checks.append(dict(endpoint=endpoint.__name__,argument=name,value=str(value),
                           rejected_before_frame_read=True))
rows=[[F(1,2),F(1,2)]]
assert mod.vacuum_probability(rows)==F(5,8)
assert mod.vacuum_probability(rows,max_states=3,max_transitions=3)==F(5,8)
class Three(IntEnum):VALUE=3
assert mod.vacuum_probability(rows,max_states=Three.VALUE,max_transitions=Three.VALUE)==F(5,8)
assert mod.vacuum_probability([[0,0]],max_states=1,max_transitions=0)==1
assert mod.vacuum_probability([[]],max_states=1,max_transitions=0)==1
for limits in [dict(max_states=2),dict(max_transitions=2)]:
    try:mod.vacuum_probability(rows,**limits)
    except RuntimeError:pass
    else:raise AssertionError(('budget guard disabled',limits))
for limits in [dict(),dict(max_states=1,max_transitions=1)]:
    evaluator=mod.ThresholdMarginals([[1],[0]],**limits)
    assert evaluator.click_means()==[1,0]
assert mod.ThresholdMarginals([[]],max_states=1,max_transitions=0).click_means()==[0]
after=sha(source.read_bytes());assert before==after
receipt=dict(status='POSTFIX_RESOURCE_API_CHECKS_PASS',started_at=started,
             runtime_seconds=time.monotonic()-clock,reviewed_commit=COMMIT,
             executed_absolute_module=str(source),sha256_before=before,sha256_after=after,
             committed_blob_sha256=committed,python=sys.version.split()[0],
             command=[sys.executable,'-B',str(Path(__file__).resolve())],
             cpu_limit_seconds=10,invalid_guard_checks=checks,
             invalid_guard_check_count=len(checks),integer_default_boundary_checks_pass=True,
             script_sha256=sha(Path(__file__).read_bytes()),
             scientific_campaign_rerun=False,pytest_rerun=False,physical_shots=0)
OUTPUT.write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
print(json.dumps({key:value for key,value in receipt.items() if key!='invalid_guard_checks'},indent=2))
