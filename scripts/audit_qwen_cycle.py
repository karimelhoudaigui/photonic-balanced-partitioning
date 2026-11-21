#!/usr/bin/env python3
"""Inspect observed Qwen tools and retained files; never trust exit0 alone."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def audit(directory):
    record=json.loads((directory/'run.json').read_text())
    uses=[];results={}
    for path in sorted(directory.glob('*.jsonl')):
        for line in path.read_text().splitlines():
            event=json.loads(line)
            for part in event.get('message',{}).get('content',[]):
                if not isinstance(part,dict):continue
                if part.get('type')=='tool_use':uses.append(part)
                if part.get('type')=='tool_result':results[part['tool_use_id']]=part
    def successful(use):
        response=results.get(use['id'],{})
        return bool(response) and not response.get('is_error',False)
    reads=[u for u in uses if u['name']=='read_file' and 'AGENTS.md' in json.dumps(u['input']) and successful(u)]
    tests=[u for u in uses if u['name']=='run_shell_command' and 'pytest' in u['input'].get('command','') and successful(u)]
    passed=[u for u in tests if re.search(r'\d+ passed',str(results[u['id']].get('content','')))]
    worktree=Path(record['worktree'])
    paper={str(p.relative_to(worktree)):hashlib.sha256(p.read_bytes()).hexdigest()
           for p in (worktree/'paper').rglob('*') if p.is_file()} if worktree.exists() else None
    unchanged=bool(record.get('paper_hashes_before')) and paper==record.get('paper_hashes_before')==record.get('paper_hashes_after')
    report_files=[str(p.relative_to(worktree)) for p in (worktree/'reports').glob('QWEN_*.md')] if worktree.exists() else []
    output={'cycle':record['cycle'],'process_status':record['status'],
            'observed_tool_calls':len(uses),'successful_AGENTS_reads':len(reads),
            'observed_pytest_commands':[u['input']['command'] for u in tests],
            'pytest_success_evidence':len(passed),'reports':report_files,
            'manuscript_hashes_unchanged':unchanged,
            'delegations':[u['input'] for u in uses if u['name']=='agent'],
            'team_tool_calls':[u['name'] for u in uses if u['name'] in ['team_create','task_create','task_update','team_delete','send_message','request_shutdown']],
            'automated_evidence_only':True,'scientific_acceptance':'PENDING_ASTRA_REVIEW'}
    native=[u for u in uses if u['name']=='agent' and successful(u)]
    team_names={u['name'] for u in uses if successful(u)}
    output['native_subagent_dispatch_observed']=bool(native)
    output['native_team_lifecycle_observed']=bool(native and {'team_create','task_create','task_update','team_delete'}<=team_names)
    if record['mode']=='validation':
        output['infrastructure_smoke_pass']=bool(reads and passed and report_files and unchanged)
    raw=worktree/'results/qwen_n4_first_cycle/raw.json';rep=worktree/'results/qwen_n4_replication/raw.json'
    if raw.exists() and rep.exists():
        first=json.loads(raw.read_text());second=json.loads(rep.read_text())
        output['replication_rows_equal']=first['rows']==second['rows']
        output['replication_uses_fresh_seeds']=not ({r['seed'] for r in first['rows']} & {r['seed'] for r in second['rows']})
        output['n4_runs']=len(first['rows'])
        output['n4_evaluations']=sum(r['n_evaluations'] for r in first['rows'])
        output['cycle_evidence_complete']=bool(passed and unchanged and
            output['replication_uses_fresh_seeds'] and len(first['rows'])==len(second['rows'])==18
            and (worktree/'reports/QWEN_ADVERSARIAL_REVIEW.md').is_file()
            and (worktree/'reports/QWEN_REPLICATION.md').is_file())
    (directory/'supervisor_evidence_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    return output


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    print(json.dumps(audit(parser.parse_args().directory),indent=2))
