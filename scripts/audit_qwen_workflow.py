#!/usr/bin/env python3
"""Retain native child receipts and verify the two-role Qwen smoke handoff."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


def load_lines(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def child_calls(path):
    calls=[];responses={}
    for event in load_lines(path):
        for part in event.get('message',{}).get('parts',[]):
            if 'functionCall' in part:calls.append(part['functionCall'])
            if 'functionResponse' in part:
                response=part['functionResponse'];responses[response['id']]=response
    return calls,responses


def inspect_children(directory, execution_text):
    children=[]
    for path in sorted(directory.glob('*.meta.json')):
        meta=json.loads(path.read_text());transcript=path.with_name(path.name.replace('.meta.json','.jsonl'))
        calls,responses=child_calls(transcript)
        children.append(dict(meta=meta,calls=calls,responses=responses))
    roles={child['meta']['agentType']:child for child in children}
    executor=roles.get('experiment-runner');critic=roles.get('adversarial-reviewer')
    tests=[];writes=[]
    if executor:
        for call in executor['calls']:
            response=executor['responses'].get(call['id'],{}).get('response',{})
            output=str(response.get('output',''))
            if (call['name']=='run_shell_command' and 'pytest tests/test_hom.py' in call.get('args',{}).get('command','')
                    and '8 passed' in output and 'Exit Code: 0' in output
                    and not re.search(r'\d+ (?:failed|errors?)(?:\W|$)',output)):
                tests.append(dict(command=call['args']['command'],output=output))
    if critic:
        for call in critic['calls']:
            response=critic['responses'].get(call['id'],{}).get('response',{})
            if call['name']=='write_file' and 'Successfully created and wrote' in str(response.get('output','')):
                writes.append(call['args'].get('file_path'))
    ids=[c['meta']['agentId'] for c in children]
    sequential=bool(executor and critic and executor['meta']['lastUpdatedAt']<=critic['meta']['createdAt'])
    handoff=bool(execution_text and critic and execution_text in critic['meta'].get('description',''))
    completed=len(children)==2 and len(set(ids))==2 and all(c['meta'].get('status')=='completed' for c in children)
    return dict(native_roles=[c['meta']['agentType'] for c in children],
                child_ids=ids,native_children_completed=completed,sequential_execution=sequential,
                exact_worker_text_in_critic_prompt=handoff,observed_pytest_receipts=tests,
                observed_report_write_receipts=writes,
                native_workflow_smoke_pass=bool(completed and sequential and handoff and tests and writes))


def audit(directory):
    root=Path(__file__).resolve().parents[1]
    directory=directory.resolve()
    record=json.loads((directory/'run.json').read_text());worktree=Path(record['worktree'])
    events=load_lines(directory/'00-research-lead.jsonl')
    init=next(e for e in events if e.get('subtype')=='init');session=init['session_id']
    runtime=root/'.local/qwen/home/projects'/re.sub(r'[^A-Za-z0-9_-]','-',str(worktree))
    workflow_results=[]
    for event in events:
        for part in event.get('message',{}).get('content',[]):
            if isinstance(part,dict) and part.get('type')=='tool_result' and not part.get('is_error'):
                match=re.search(r'```json\s*(.*?)\s*```',str(part.get('content','')),re.S)
                if match:
                    value=json.loads(match.group(1))
                    if 'runId' in value:workflow_results.append(value)
    if len(workflow_results)!=1:raise ValueError('Expected one observed saved-workflow result')
    workflow=workflow_results[0];runid=workflow['runId']
    target=directory/'native_evidence';target.mkdir(exist_ok=True)
    sources=[runtime/'workflows'/f'{runid}.json',runtime/'workflows'/runid/'journal.jsonl',
             *sorted((runtime/'subagents'/session).glob('*.jsonl')),
             *sorted((runtime/'subagents'/session).glob('*.meta.json')),
             worktree/'reports/QWEN_RELAY_REVIEW.md']
    checksums=[]
    for source in sources:
        dest=target/source.name
        checksum=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        if not dest.exists():shutil.copyfile(source,dest)
        assert checksum(source)==checksum(dest)
        checksums.append(dict(original=str(source.relative_to(root)),retained=str(dest.relative_to(root)),sha256=checksum(dest)))
    result=inspect_children(target,workflow['result']['execution'])
    result.update(workflow_run_id=runid,evidence_files=checksums,
                  process_status=record['status'],scientific_acceptance='NOT_ESTABLISHED',
                  manuscript_hashes_unchanged=record['paper_hashes_before']==record['paper_hashes_after'],
                  native_agent_team_lifecycle='NOT_TESTED_BY_THIS_WORKFLOW',
                  narrative_review='Supervisor must reject unsupported critic statements; communication is not scientific correctness.')
    result['native_workflow_smoke_pass'] &= result['manuscript_hashes_unchanged']
    (directory/'supervisor_workflow_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    result=audit(parser.parse_args().directory)
    print(json.dumps({k:v for k,v in result.items() if k!='evidence_files'},indent=2))
