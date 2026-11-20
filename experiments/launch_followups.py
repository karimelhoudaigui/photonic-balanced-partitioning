#!/usr/bin/env python3
"""v2 provenance for corrected equal-budget study and mathematical falsifiers."""
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
RECORDER=Path('/Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py')
TASKS={
    'E05b_exact_equal_budget': ('experiments/run_equal_budget.py',['summary.json','runs.jsonl']),
    'E08_coherence_certificate': ('experiments/run_coherence_check.py',['summary.json','counterexamples.json']),
}


def main():
    if len(sys.argv)!=2 or sys.argv[1] not in TASKS: raise SystemExit('Specify '+ '|'.join(TASKS))
    name=sys.argv[1];script,results=TASKS[name];output=Path('experiments')/name
    if (ROOT/output).exists(): raise SystemExit('Refusing to overwrite data')
    artifacts=sorted(str(p.relative_to(ROOT)) for p in (ROOT/'src').rglob('*.py'))
    artifacts+=['experiments/run_research.py','experiments/launch_followups.py',script,'pyproject.toml']
    if name=='E08_coherence_certificate':artifacts+=['theory/near_collisionless_bound.md']
    contract=dict(claim_id=name,mathematics=dict(
        assertion_tested=('Equal actual ideal simulated attempt budgets including every training batch and first discovery'
                         if name.startswith('E05') else 'Full Fock TV bounds and exact balanced-density counterexamples to collision-only approximation'),
        coefficient_domain='float64/complex128 with rational counterexample summaries',
        conventions='passive lossless, k distinct occupied inputs; no postselection renormalization; TV=half L1',
        inputs=[script,'fixed seeds and ranges hardcoded in the declared script'],bounds=dict(base_seed=20261120),
        non_claims=['Not QPU evidence or quantum advantage','Novelty open','Numerical tests not universal proof']),
        execution_artifacts=artifacts,software=[dict(name=p,version=version(p)) for p in ['numpy','scipy','perceval-quandela']],
        randomness=dict(used=True,generator='numpy.default_rng PCG64',seed=20261120))
    path=ROOT/'experiments'/'contracts'/f'{name}.json';path.write_text(json.dumps(contract,indent=2)+'\n')
    command=[sys.executable,str(RECORDER),'--root',str(ROOT),'--contract',str(path),
        '--output',str(output),'--timeout','1800','--max-output-bytes','4194304','--max-threads','1']
    for result in results:command+=['--result',str(output/result)]
    for artifact in artifacts:command+=['--input',artifact]
    command+=['--',sys.executable,script,'--output',str(output)]
    raise SystemExit(subprocess.call(command,cwd=ROOT))


if __name__=='__main__': main()
