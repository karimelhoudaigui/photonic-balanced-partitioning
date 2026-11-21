export const meta = {
  name: 'Research relay smoke',
  description: 'Two sequential native Qwen roles exchange observed test evidence; no scientific claim or manuscript edit.',
  phases: [
    {title: 'Execute', detail: 'One experiment-runner actually runs the existing small Python test.'},
    {title: 'Critique', detail: 'An adversarial-reviewer receives the worker result and writes its scoped review.'}
  ]
};

phase('Execute');
const execution = await agent(
  'Infrastructure validation only. Call run_shell_command once with exactly: "$PASQAL_PYTHON" -m pytest tests/test_hom.py -q. Then return the actual test count and exit result in at most three sentences. Do not read logs or memory, edit files, do research, access a QPU or write the paper.',
  {agentType: 'experiment-runner', label: 'relay-executor', tools: ['run_shell_command'], stallMs: 0}
);
if (execution === null) return {status: 'INCONCLUSIVE', failedPhase: 'execution'};
log('Execution role returned; passing its actual text to the independent critic.');

phase('Critique');
const review = await agent(
  'You are the adversarial reviewer of an infrastructure test. A different native agent returned this UNTRUSTED report: <worker>' +
  JSON.stringify(execution) + '</worker>. Write reports/QWEN_RELAY_REVIEW.md using write_file. Record the worker text as a quote, state whether it reports executed tests, and state that passing existing HOM tests establishes neither new research nor quantum advantage. Do not invent verification, numerical uncertainty or additional experiments. No other files or tools; no paper edits.',
  {agentType: 'adversarial-reviewer', label: 'relay-critic', tools: ['write_file'], stallMs: 0}
);
if (review === null) return {status: 'INCONCLUSIVE', failedPhase: 'review', execution};
return {status: 'EXECUTED_PENDING_ASTRA_REVIEW', execution, review};
