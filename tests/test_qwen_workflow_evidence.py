"""A native workflow needs child receipts, ordering and actual result handoff."""
import importlib.util
import json
from pathlib import Path

spec=importlib.util.spec_from_file_location('workflow_auditor',Path(__file__).resolve().parents[1]/'scripts/audit_qwen_workflow.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)


def fixture(directory,*,receipt=True,handoff=True,ordered=True):
    roles=['experiment-runner','adversarial-reviewer']
    for index,role in enumerate(roles):
        name=f'child-{index}';meta=dict(agentId=name,agentType=role,status='completed',
            createdAt=f'2026-01-01T00:00:0{index*2 if ordered else 0}Z',
            lastUpdatedAt=f'2026-01-01T00:00:0{index*2+1}Z',
            description='Prior worker: EVIDENCE' if handoff else 'No prior result supplied')
        (directory/f'{name}.meta.json').write_text(json.dumps(meta))
        tool='run_shell_command' if index==0 else 'write_file'
        args={'command':'python -m pytest tests/test_hom.py -q'} if index==0 else {'file_path':'reports/QWEN_RELAY_REVIEW.md'}
        rows=[{'message':{'parts':[{'functionCall':{'id':name,'name':tool,'args':args}}]}}]
        if receipt or index:
            text='8 passed in 1s\nExit Code: 0' if index==0 else 'Successfully created and wrote to new file'
            rows.append({'message':{'parts':[{'functionResponse':{'id':name,'name':tool,'response':{'output':text}}}]}})
        (directory/f'{name}.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))


def test_workflow_accepts_verified_native_children_and_exact_handoff(tmp_path):
    fixture(tmp_path)
    assert audit.inspect_children(tmp_path,'EVIDENCE')['native_workflow_smoke_pass'] is True


def test_workflow_rejects_claimed_execution_without_tool_receipt(tmp_path):
    fixture(tmp_path,receipt=False)
    assert audit.inspect_children(tmp_path,'EVIDENCE')['native_workflow_smoke_pass'] is False


def test_workflow_rejects_missing_handoff_or_overlapping_workers(tmp_path):
    one=tmp_path/'one';one.mkdir();fixture(one,handoff=False)
    assert audit.inspect_children(one,'EVIDENCE')['native_workflow_smoke_pass'] is False
    two=tmp_path/'two';two.mkdir();fixture(two,ordered=False)
    assert audit.inspect_children(two,'EVIDENCE')['native_workflow_smoke_pass'] is False
