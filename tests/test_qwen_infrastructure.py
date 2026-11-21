"""Guardrails for an external local-agent runtime, without requiring inference."""
import importlib.util
import json
import subprocess
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('local_cycle_runner',ROOT/'scripts/run_research_cycle.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)


def test_runtime_environment_does_not_inherit_provider_or_qpu_credentials(monkeypatch):
    monkeypatch.setenv('QPU_TOKEN','test-sentinel-not-a-credential')
    monkeypatch.setenv('OPENAI_API_KEY','test-sentinel-not-a-credential')
    env=runner.environment()
    assert 'QPU_TOKEN' not in env and 'OPENAI_API_KEY' not in env
    assert env['OLLAMA_NO_CLOUD']=='1'
    assert env['OLLAMA_NUM_PARALLEL']=='1'
    assert env['OLLAMA_MAX_LOADED_MODELS']=='1'
    assert env['PYTHONPATH']=='src'


def test_project_configuration_is_local_and_teams_are_opted_in():
    settings=json.loads((ROOT/'.qwen/settings.json').read_text())
    assert settings['experimental']['agentTeam'] is True
    assert settings['agents']['defaultBackground'] is False
    assert settings['telemetry']['enabled'] is False
    routes=settings['modelProviders']['openai']
    assert len(routes)==1 and routes[0]['baseUrl']=='http://127.0.0.1:11435/v1'
    assert 'apiKey' not in routes[0]


def test_seven_roles_are_versionable_and_bound_their_turns():
    names={'research-lead','physics-auditor','mathematical-researcher','experiment-runner',
           'algorithm-designer','adversarial-reviewer','literature-reviewer'}
    assert {p.stem for p in (ROOT/'.qwen/agents').glob('*.md')}==names
    for name in names:
        source=(ROOT/'.qwen/agents'/f'{name}.md').read_text()
        assert source.startswith('---\nname: '+name+'\n')
        assert 'maxTurns: 8' in source
        assert 'background: false' in source
        assert 'paper/' in source


def test_paper_hashes_detect_change_without_touching_real_manuscript(tmp_path):
    (tmp_path/'paper').mkdir();p=tmp_path/'paper/example.tex';p.write_text('original')
    before=runner.paper_hashes(tmp_path);p.write_text('changed')
    assert runner.paper_hashes(tmp_path)!=before


def test_sparse_worktree_has_code_but_does_not_duplicate_large_historical_raw(tmp_path):
    repo=tmp_path/'repo';repo.mkdir()
    def git(*args):
        return subprocess.run(['git',*args],cwd=repo,check=True,capture_output=True,text=True)
    git('init');git('config','user.email','test@example.invalid');git('config','user.name','Infrastructure test')
    for path in ['AGENTS.md','reports/check.md','src/model.py','paper/frozen.tex','experiments/E01/runs.jsonl']:
        target=repo/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text('fixture')
    git('add','.');git('commit','-m','fixture')
    target=tmp_path/'worker'
    runner.prepare_worktree(repo,target,'worker-test','HEAD')
    assert (target/'AGENTS.md').read_text()=='fixture'
    assert (target/'src/model.py').is_file() and (target/'paper/frozen.tex').is_file()
    assert (target/'reports/check.md').is_file()
    assert not (target/'experiments/E01/runs.jsonl').exists()
    assert (repo/'experiments/E01/runs.jsonl').read_text()=='fixture'


def evidence_auditor():
    spec=importlib.util.spec_from_file_location('evidence_auditor',ROOT/'scripts/audit_qwen_cycle.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_evidence_audit_rejects_exit_zero_without_executed_tests(tmp_path):
    worker=tmp_path/'worker';(worker/'paper').mkdir(parents=True)
    (worker/'paper/frozen.tex').write_text('frozen');(worker/'reports').mkdir()
    (worker/'reports/QWEN_SMOKE_REPORT.md').write_text('I claim PASS')
    directory=tmp_path/'logs';directory.mkdir();hashes=runner.paper_hashes(worker)
    (directory/'run.json').write_text(json.dumps(dict(cycle='fixture',mode='validation',
        status='EXECUTED_PENDING_REVIEW',worktree=str(worker),paper_hashes_before=hashes,paper_hashes_after=hashes)))
    result=evidence_auditor().audit(directory)
    assert result['infrastructure_smoke_pass'] is False
    assert result['native_subagent_dispatch_observed'] is False


def test_evidence_audit_does_not_accept_partly_failing_pytest(tmp_path):
    worker=tmp_path/'worker';worker.mkdir();directory=tmp_path/'logs';directory.mkdir()
    (directory/'run.json').write_text(json.dumps(dict(cycle='fixture',mode='validation',
        status='EXECUTED_PENDING_REVIEW',worktree=str(worker))))
    events=[{'message':{'content':[{'type':'tool_use','id':'tests','name':'run_shell_command',
        'input':{'command':'python -m pytest tests/'}}]}},
        {'message':{'content':[{'type':'tool_result','tool_use_id':'tests','is_error':False,
                               'content':'2 failed, 8 passed in 1.0s'}]}}]
    (directory/'test.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
    assert evidence_auditor().audit(directory)['pytest_success_evidence']==0


def test_evidence_audit_resolves_all_continuations_and_rejects_cycles(tmp_path):
    worker=tmp_path/'worker';worker.mkdir();directories=[tmp_path/str(i) for i in range(3)]
    for index,directory in enumerate(directories):
        directory.mkdir();record=dict(cycle=str(index),mode='cycle',worktree=str(worker),status='INCONCLUSIVE')
        if index:record['continued_from']=str(directories[index-1])
        (directory/'run.json').write_text(json.dumps(record))
    events=[{'message':{'content':[{'type':'tool_use','id':'tests','name':'run_shell_command',
        'input':{'command':'python -m pytest tests/'}}]}},
        {'message':{'content':[{'type':'tool_result','tool_use_id':'tests','is_error':False,
                               'content':'8 passed in 1.0s'}]}}]
    (directories[0]/'test.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
    assert evidence_auditor().audit(directories[2])['pytest_success_evidence']==1
    first=json.loads((directories[0]/'run.json').read_text());first['continued_from']=str(directories[2])
    (directories[0]/'run.json').write_text(json.dumps(first))
    with pytest.raises(ValueError,match='Cyclic'):evidence_auditor().audit(directories[2])
