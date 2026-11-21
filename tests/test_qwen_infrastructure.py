"""Guardrails for an external local-agent runtime, without requiring inference."""
import importlib.util
import json
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
