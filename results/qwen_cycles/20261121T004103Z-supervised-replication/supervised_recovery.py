"""One supervised execution of the unstarted replication, not a critic retry."""
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
original=ROOT/'results/qwen_cycles/20261121T002702Z-cycle'
recovery=ROOT/'results/qwen_cycles/20261121T003401Z-cycle-resume'
prior=json.loads((original/'run.json').read_text())
first_recovery=json.loads((recovery/'run.json').read_text())
deadline=dt.datetime.fromisoformat(prior['started_at'])+dt.timedelta(seconds=prior['limits']['wall_time'])
remaining=(deadline-dt.datetime.now(dt.timezone.utc)).total_seconds()
if remaining<60:raise SystemExit('Original absolute wall budget expired')
lock=(r.STATE/'cycle.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
cycle=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-supervised-replication'
out=ROOT/'results/qwen_cycles'/cycle;out.mkdir()
shutil.copyfile(__file__,out/'supervised_recovery.py')
worktree=Path(prior['worktree']);before=r.paper_hashes(worktree);root_before=r.paper_hashes(ROOT)
prefix=r.confinement(worktree,out/'sandbox.sb')
command=prior['runs'][1]['argv'][:]
command[2]=str(out/'sandbox.sb')
command[command.index('--max-session-turns')+1]='3'
command[command.index('--max-tool-calls')+1]='3'
command[command.index('--max-wall-time')+1]=str(int(min(remaining-10,240)))
command[command.index('--system-prompt')+1]='Execute exactly the requested shell command now. Then write the short requested execution record. Do not read any files or memory, plan, interpret numbers or run another experiment. Paper is frozen. No QPU or remote API.'
py=ROOT/'.venv/bin/python'
command[command.index('-p')+1]=f'First call run_shell_command with command: {py} scripts/qwen_n4_probe.py --seed-offset 100 --output results/qwen_n4_replication\nThen write reports/QWEN_REPLICATION.md with the exact command and the actual returned runs/evaluations/HOM values. Say: Fresh seeds 20261221,20261222,20261223. Interpretation pending independent Astra audit. Do not add error bars or scientific conclusions. No other tools.'
record=dict(cycle=cycle,mode='cycle',started_at=dt.datetime.now(dt.timezone.utc).isoformat(),
    worktree=str(worktree),base_commit=prior['base_commit'],controller_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    continued_from=str(recovery),original_cycle=str(original),
    intervention='Astra executes only the unstarted replication after failed critic; no critic retry and no new experiment family',
    original_absolute_deadline=deadline.isoformat(),max_seconds=min(remaining-10,240),
    supervisor_verdict='PENDING_ASTRA_REVIEW',status='RUNNING',runs=[])
started=time.monotonic()
try:
    run=r.execute(command,worktree,r.environment(),out/'03-experiment-runner',record['max_seconds'],0)
    record['runs'].append(run)
    record['status']='EXECUTED_PENDING_REVIEW' if run['exit_code']==0 else 'INCONCLUSIVE'
finally:
    record['paper_hashes_before']=before;record['paper_hashes_after']=r.paper_hashes(worktree)
    record['root_paper_unchanged']=root_before==r.paper_hashes(ROOT)
    record['runtime_seconds']=time.monotonic()-started
    (out/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    try:r.post('/api/generate',{'model':r.MODEL,'keep_alive':0})
    except OSError:pass
    print(json.dumps({'directory':str(out),'status':record['status']}))
