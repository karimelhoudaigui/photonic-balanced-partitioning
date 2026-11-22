#!/usr/bin/env python3
"""Retain native contexts and attest plumbing, separately from scientific truth."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]


def main(directory):
    directory=directory.resolve();record=json.loads((directory/'run.json').read_text())
    events=[json.loads(line) for line in (directory/'00-research-lead.jsonl').read_text().splitlines()]
    session=next(e['session_id'] for e in events if e.get('subtype')=='init')
    result=None
    for event in events:
        for part in event.get('message',{}).get('content',[]):
            if isinstance(part,dict) and part.get('type')=='tool_result' and not part.get('is_error'):
                match=re.search(r'```json\s*',str(part.get('content','')))
                if match:
                    candidate,_=json.JSONDecoder().raw_decode(str(part['content'])[match.end():].lstrip())
                    if isinstance(candidate,dict) and 'runId' in candidate:result=candidate
    worktree=Path(record['worktree']);project=re.sub(r'[^A-Za-z0-9_-]','-',str(worktree))
    runtime=ROOT/'.local/qwen/home/projects'/project
    if result is None:
        # A killed parent may never emit a tool result. Retain the sole native
        # checkpoint without pretending its still-running metadata is a return.
        checkpoints=list((runtime/'workflows').glob('*/checkpoint.json'))
        persisted=[p for p in (runtime/'workflows').glob('*.json')
                   if json.loads(p.read_text()).get('parentSessionId')==session]
        if len(checkpoints)==1:runid=checkpoints[0].parent.name
        elif len(persisted)==1:runid=persisted[0].stem
        else:raise ValueError('No unique native state for interrupted parent session')
        result={'runId':runid,'result':{'status':'NO_RETURN_OBSERVED'}}
    runid=result['runId'];target=directory/'native_evidence';target.mkdir(exist_ok=True)
    files=[runtime/'workflows'/f'{runid}.json',runtime/'workflows'/runid/'journal.jsonl',
           runtime/'workflows'/runid/'checkpoint.json',
           *sorted((runtime/'subagents'/session).glob('*')),
           *sorted((worktree/'reports').glob('QWEN_P33*.md'))]
    retained=[]
    for source in files:
        if not source.is_file():continue
        destination=target/source.name
        digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        if not destination.exists():shutil.copyfile(source,destination)
        if digest(source)!=digest(destination):raise ValueError('Retained evidence changed')
        retained.append(dict(source=str(source.relative_to(ROOT)),copy=str(destination.relative_to(ROOT)),sha256=digest(destination)))
    children=[json.loads(p.read_text()) for p in target.glob('*.meta.json')]
    ordered=sorted(children,key=lambda c:c['createdAt'])
    sequential=all(a['lastUpdatedAt']<=b['createdAt'] for a,b in zip(ordered,ordered[1:]))
    required={'research-lead','physics-auditor','mathematical-researcher','experiment-runner',
              'algorithm-designer','adversarial-reviewer','literature-reviewer'}
    roles={c['agentType'] for c in children}
    science={}
    for mode in ['primary','replication']:
        p=worktree/'results'/f'P33_density_{mode}'/'manifest.json'
        science[mode]=json.loads(p.read_text())['run']['status'] if p.exists() else 'NOT_OBSERVED'
    output=dict(workflow_run_id=runid,process_status=record['status'],
        workflow_semantic_status=result.get('result',{}).get('status'),
        native_child_count=len(children),native_roles=sorted(roles),all_seven_roles_observed=required<=roles,
        native_children=[dict(id=c['agentId'],role=c['agentType'],status=c['status'],
                             started=c['createdAt'],finished=c['lastUpdatedAt']) for c in ordered],
        sequential_execution=sequential,scientific_command_statuses=science,
        complete_execution_observed=bool(required<=roles and sequential and len(children)==9 and
            all(c.get('status')=='completed' for c in children) and
            result.get('result',{}).get('status')=='EXECUTED_PENDING_ASTRA_REVIEW' and
            all(value=='completed' for value in science.values())),
        scientific_acceptance='PENDING_INDEPENDENT_ASTRA_REVIEW',evidence=retained)
    (directory/'native_execution_audit.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({key:value for key,value in output.items() if key!='evidence'},indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=Path)
    main(parser.parse_args().directory)
