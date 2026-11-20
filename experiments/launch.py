#!/usr/bin/env python3
"""Launch one declared research cycle through the Mathbox v2 recorder."""
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
RECORDER=Path('/Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
RUNS={
 'E01_haar_collision_baseline': ['haar'],
 'E02_ideal_optimization': ['optimization','--instances','2','--repeats','3','--budget','120','--methods','COBYLA','haar'],
 'E03_objectives_pareto': ['optimization','--sizes','4','--instances','2','--repeats','3','--budget','120',
      '--models','bosonic','--objectives','bad','conditional','success','factorized','p_cf','conditional_success','collision','barrier','cvar'],
 'E04_optimizers_depths': ['optimization','--sizes','4','6','--instances','1','--repeats','3','--budget','120',
      '--models','bosonic','--methods','COBYLA','Nelder-Mead','SPSA','random','--depths','0','2'],
 'E05_equal_shots': ['shots','--instances','2','--repeats','3','--budget','120','--shots','256','--heldout','4096'],
 'E06_structural_checks': ['structure'],
 'E07_spectral_hybrid': ['optimization','--anchor','--instances','2','--repeats','3','--budget','120',
      '--models','bosonic','distinguishable','--objectives','success','conditional'],
}


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in RUNS:
        raise SystemExit('Usage: .venv/bin/python experiments/launch.py '+ '|'.join(RUNS))
    name=sys.argv[1]
    output=Path('experiments')/name
    if (ROOT/output).exists(): raise SystemExit('Refusing to overwrite a research run')
    artifacts=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'src').rglob('*.py'))
    artifacts+=['experiments/run_research.py','experiments/launch.py','pyproject.toml']
    contract=dict(claim_id=name,
        mathematics=dict(assertion_tested='Measure Haar loss, optimizer enrichment, model ablations or collision-moment bounds on the explicit finite command domain.',
          coefficient_domain='complex128/float64; exact Fock enumeration, numerical optimization or ideal multinomial sampling',
          conventions='lossless, first k=n/2 input modes each contain one photon; all collisions count as physical attempts; output order documented in code',
          inputs=['graph families path, cycle, regular (degree-preserving edge swaps, not uniform), Erdos-Renyi, weighted, planted; generator seeds in raw data'],
          bounds=dict(argv=RUNS[name],base_seed=20261120),
          non_claims=['Not a quantum advantage or hardware experiment','Oracle success training is a state-preparation diagnostic','Finite data do not prove scalable speedup','Product-Bernoulli penalty is classical, not genuine ObliQ dynamics']),
        execution_artifacts=artifacts,
        software=[dict(name=p,version=version(p)) for p in ['numpy','scipy','perceval-quandela','exqalibur']],
        randomness=dict(used=True,generator='numpy.default_rng PCG64',seed=20261120))
    contract_path=ROOT/'experiments'/'contracts'/f'{name}.json'
    contract_path.parent.mkdir(exist_ok=True)
    contract_path.write_text(json.dumps(contract,indent=2)+'\n')
    command=[sys.executable,str(RECORDER),'--root',str(ROOT),'--contract',str(contract_path),
             '--output',str(output),'--result',str(output/'summary.json'),
             '--timeout','1800','--max-output-bytes','4194304','--max-threads','1']
    if RUNS[name][0] in ['optimization','shots']:
        command+=['--result',str(output/'runs.jsonl')]
    if RUNS[name][0]=='haar':command+=['--result',str(output/'raw.csv')]
    for artifact in artifacts: command+=['--input',artifact]
    command+=['--',sys.executable,'experiments/run_research.py',*RUNS[name],'--output',str(output)]
    raise SystemExit(subprocess.call(command,cwd=ROOT))


if __name__=='__main__': main()
