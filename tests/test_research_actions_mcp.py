"""Protocol and authority boundaries, without invoking expensive research."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('research_bridge',ROOT/'scripts/research_actions_mcp.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)


def test_stdio_handshake_discovery_and_health():
    messages=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05'}},
              {'jsonrpc':'2.0','method':'notifications/initialized'},
              {'jsonrpc':'2.0','id':2,'method':'tools/list'},
              {'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'health','arguments':{}}}]
    result=subprocess.run([sys.executable,str(ROOT/'scripts/research_actions_mcp.py')],
        input=''.join(json.dumps(m)+'\n' for m in messages),capture_output=True,text=True,check=True,timeout=5)
    responses=[json.loads(line) for line in result.stdout.splitlines()]
    assert [r['id'] for r in responses]==[1,2,3]
    assert responses[0]['result']['protocolVersion']=='2024-11-05'
    assert {t['name'] for t in responses[1]['result']['tools']}==set(bridge.ACTIONS)|{'health'}
    assert responses[2]['result']['isError'] is False


def test_no_arbitrary_commands_arguments_or_replay_annotations():
    with pytest.raises(ValueError):bridge.call('run_density_primary',{'command':'arbitrary'})
    with pytest.raises(ValueError):bridge.call('arbitrary',{})
    for tool in bridge.tool_list():
        if tool['name']!='health':
            assert tool['annotations']['idempotentHint'] is False
            assert tool['inputSchema']['additionalProperties'] is False


def test_bridge_uses_fixed_argv_and_pinned_python(monkeypatch):
    calls=[];monkeypatch.setenv('PASQAL_PYTHON','/pinned/scientific/python')
    def fake(command,**kwargs):
        calls.append((command,kwargs));return subprocess.CompletedProcess(command,0,'observed','')
    monkeypatch.setattr(bridge.subprocess,'run',fake)
    result=bridge.call('run_density_replication',{})
    assert result['isError'] is False
    assert calls[0][0]==['/pinned/scientific/python',str(ROOT/'scripts/qwen_density_job.py'),'replication']
    assert calls[0][1].get('shell',False) is False
    assert calls[0][1]['timeout']==340
