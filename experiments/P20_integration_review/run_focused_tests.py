"""Run only the existing 16 P20 component tests, with bounded CPU and no cache writes."""
import json,os,resource,subprocess,sys,time
from pathlib import Path
ROOT=Path('/Users/karimelhoudaigui/Desktop/pasqal');OUT=Path(__file__).resolve().parent
for name in ('pytest_stdout.txt','pytest_stderr.txt','pytest_receipt.json'):
    if (OUT/name).exists():raise SystemExit('Refusing to overwrite test evidence')
resource.setrlimit(resource.RLIMIT_CPU,(30,30))
start=time.perf_counter();before=resource.getrusage(resource.RUSAGE_CHILDREN)
command=[sys.executable,'-B','-m','pytest',str(ROOT/'tests/test_structured_search.py'),'-q','-p','no:cacheprovider']
run=subprocess.run(command,cwd=ROOT,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','MPLCONFIGDIR':'/private/tmp/pasqal-p20-review-mpl'},capture_output=True,text=True)
after=resource.getrusage(resource.RUSAGE_CHILDREN)
(OUT/'pytest_stdout.txt').write_text(run.stdout);(OUT/'pytest_stderr.txt').write_text(run.stderr)
record=dict(command=command,cwd=str(ROOT),exit_status=run.returncode,wall_seconds=time.perf_counter()-start,
            child_cpu_seconds=(after.ru_utime+after.ru_stime)-(before.ru_utime+before.ru_stime),
            child_cpu_limit_seconds=30,existing_campaigns_rerun=False)
(OUT/'pytest_receipt.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
raise SystemExit(run.returncode)
