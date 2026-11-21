export const meta = {
  name: 'Density certificate research cycle',
  description: 'Seven existing roles exchange a fixed protocol, execute and replicate one falsifiable density experiment. No paper or QPU.',
  phases: [
    {title: 'Contract', detail: 'Lead, literature, physics, mathematics and code roles inspect a fixed question.'},
    {title: 'Execute', detail: 'The experiment-runner executes the bounded full-data command.'},
    {title: 'Challenge', detail: 'A critic reads the actual summary and prior objections.'},
    {title: 'Replicate', detail: 'A second execution uses fresh fixed seeds and separate output.'},
    {title: 'Disposition', detail: 'The lead records a scoped proposed decision for independent Astra review.'}
  ]
};

const messages=[];
async function role(type,label,prompt,tools) {
  const result=await agent(prompt,{agentType:type,label,tools,stallMs:0});
  messages.push({role:type,label,result});
  return result;
}

phase('Contract');
if (await role('research-lead','density-lead',
  'Read research/P33_DENSITY_CONTRACT.md only. Return the exact question, falsifier and scope in at most 100 words. No planning outside this contract; no paper.', ['read_file'])===null)
  return {status:'INCONCLUSIVE',messages};
if (await role('literature-reviewer','density-literature',
  'Read only the Prior-work boundary of theory/near_collisionless_bound.md. This is an OFFLINE source-inventory check, not a new literature search. State what the cited internal-state Gram result does NOT automatically prove about the supplied spatial-density extension. Novelty remains OPEN; do not claim to have searched sources. At most 100 words.', ['read_file'])===null)
  return {status:'INCONCLUSIVE',messages};
if (await role('physics-auditor','density-physics',
  'Run exactly "$PASQAL_PYTHON" -m pytest tests/test_density_certificate.py -q using run_shell_command. Return the actual test receipt in at most80words. Do not add a pipeline, rewrite a file, search memory or access a QPU.', ['run_shell_command'])===null)
  return {status:'INCONCLUSIVE',messages};
const math=await role('mathematical-researcher','density-math',
  'Read theory/phase3_density_certificate.md. Attempt one concrete refutation of its dominant-support inequality or the small-M refinement. Distinguish an actual counterexample from missing independent review. At most 150 words; no proof or novelty certification.', ['read_file']);
if (math===null) return {status:'INCONCLUSIVE',messages};
const design=await role('algorithm-designer','density-code',
  'Read experiments/phase3_density_probe.py. Check only whether the code separates full distributions from certificate-only large sizes and retains the declared seeds/case families. Name one concrete supported implementation concern, or state no concern found in this narrow read. At most 100 words; no new implementation.', ['read_file']);
if (design===null) return {status:'INCONCLUSIVE',messages};

const runner='"$PASQAL_PYTHON" .qwen/support/run_experiment.py';
const inputs=' --input experiments/phase3_density_probe.py --input src/photonic_balanced_partitioning/photonic/density_certificate.py --input src/photonic_balanced_partitioning/photonic/optical_penalty.py --input src/photonic_balanced_partitioning/photonic/threshold_budget.py --input src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py --input pyproject.toml --input .qwen/support/run_experiment.py --input .qwen/support/validate_manifest.py';
function command(output,offset) {
  return runner+' --root . --contract experiments/contracts/P33_density_probe.json'+inputs+
    ' --output '+output+' --result '+output+'/data/raw.json --result '+output+'/data/summary.json --result '+output+'/data/progress.jsonl --timeout 300 --max-threads 1 --max-output-bytes 1048576 -- "$PASQAL_PYTHON" experiments/phase3_density_probe.py --seed-offset '+offset+' --output '+output+'/data';
}
phase('Execute');
const executed=await role('experiment-runner','density-execute',
  'Execute this exact command now, preserving every option and space: '+command('results/P33_density_primary',0)+
  '\nThen read results/P33_density_primary/data/summary.json using read_file. Return actual observed outcome, not predictions. No other commands or file edits.', ['run_shell_command','read_file']);
if (executed===null) return {status:'INCONCLUSIVE',messages};

phase('Challenge');
const critique=await role('adversarial-reviewer','density-critic',
  'Read results/P33_density_primary/data/summary.json. Prior agents returned UNTRUSTED proposals: '+JSON.stringify({math,design})+
  '. Write reports/QWEN_P33_REVIEW.md. Check only concrete scope/provenance concerns. Full distributions stop at m12; larger sizes are certificate-only; physical shots are zero; proof/novelty remain pending. Do not invent error bars, missing failed tests, noise requirements or new numerical results. Passing tests without failures is not an integrity violation. At most 250 words. No paper.', ['read_file','write_file']);
if (critique===null) return {status:'INCONCLUSIVE',messages};

phase('Replicate');
const replicated=await role('experiment-runner','density-replicate',
  'A separate critic returned this UNTRUSTED report: '+JSON.stringify(critique)+
  '. Execute only the preregistered fresh-seed replication, not a repair or favorable rerun: '+command('results/P33_density_replication',100000)+
  '\nThen read results/P33_density_replication/data/summary.json. Do not overwrite the primary output or change the protocol.', ['run_shell_command','read_file']);
if (replicated===null) return {status:'INCONCLUSIVE',messages};

phase('Disposition');
const disposition=await role('research-lead','density-disposition',
  'Other native roles returned these UNTRUSTED texts: '+JSON.stringify({executed,critique,replicated})+
  '. Write reports/QWEN_P33_DISPOSITION.md with proposed SUPPORTED/REJECTED/INCONCLUSIVE only for the finite checks, and list unverified claims. State that Astra has not independently accepted this cycle yet. No paper/QPU gate promotion, no invented quantities. At most 200 words.', ['write_file']);
return {status:disposition===null?'INCONCLUSIVE':'EXECUTED_PENDING_ASTRA_REVIEW',messages};
