"""One bounded tool-isolation diagnostic, not a research or model search."""
import datetime as dt
import fcntl
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import time

ROOT=Path('/Users/karimelhoudaigui/Desktop/pasqal')
spec=importlib.util.spec_from_file_location('runner',ROOT/'scripts/run_research_cycle.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
lock=(r.STATE/'cycle.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
cycle=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-native-tool-isolation'
out=ROOT/'results/qwen_cycles'/cycle;out.mkdir();shutil.copyfile(__file__,out/'supervised_probe.py')
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
worktree=ROOT/'.qwen/worktrees'/cycle;r.prepare_worktree(ROOT,worktree,'qwen/'+cycle,commit)
before=r.paper_hashes(worktree);root_before=r.paper_hashes(ROOT)
prefix=r.confinement(worktree,out/'sandbox.sb')
excluded=r.BASE_TOOLS+[t for t in r.CONTROL_TOOLS if t!='agent']
payload={'description':'Verify native child execution','subagent_type':'physics-auditor',
         'prompt':'Infrastructure test only. Return exactly PHYSICS_AUDITOR_READY. Do not use tools,read files,inspect memory or perform research. No delegation.',
         'run_in_background':False}
argv=prefix+['qwen','--auth-type','openai','--model',r.MODEL,'--output-format','stream-json',
    '--openai-base-url',r.URL+'/v1','--openai-api-key','local-placeholder-not-a-credential',
    '--approval-mode','auto-edit','--allowed-tools','agent','--core-tools','agent',
    '--exclude-tools',','.join(excluded),'--max-session-turns','2','--max-tool-calls','1',
    '--max-subagent-depth','1','--max-wall-time','175',
    '--system-prompt','Call the agent tool exactly once with the user-supplied JSON. This is an explicitly authorized delegation capability test. Do not perform the child task yourself. Do not use memory or another tool. Wait for its actual result and report it.',
    '-p','Call agent now with these exact arguments: '+json.dumps(payload)]
record=dict(cycle=cycle,mode='subagent',base_commit=commit,worktree=str(worktree),
    started_at=dt.datetime.now(dt.timezone.utc).isoformat(),limits={'wall_time':180,'max_parallel_workers':1,'max_failed_retries':0},
    purpose='Final supervised diagnostic removes parent self-execution tools; no scientific experiment.',
    runs=[],status='RUNNING',supervisor_verdict='PENDING_ASTRA_REVIEW')
started=time.monotonic()
try:
    run=r.execute(argv,worktree,r.environment(),out/'00-native-subagent',180,0);record['runs'].append(run)
    record['status']='EXECUTED_PENDING_REVIEW' if run['exit_code']==0 else 'INCONCLUSIVE'
finally:
    record['paper_hashes_before']=before;record['paper_hashes_after']=r.paper_hashes(worktree)
    record['root_paper_unchanged']=root_before==r.paper_hashes(ROOT)
    record['runtime_seconds']=time.monotonic()-started
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    try:r.post('/api/generate',{'model':r.MODEL,'keep_alive':0})
    except OSError:pass
    print(json.dumps({'directory':str(out),'status':record['status']}))
