# Supervised local Qwen research

Prerequisites:Node>=22,official Qwen Code0.28.0,Ollama0.32.0,and the selected
`qwen3.5:2b-q4_K_M` weights. External tools are not Python dependencies.
Alias`pasqal-qwen-research:latest` references those same blobs. No paid provider
or real API token is required. Re-run model/tool validation after upgrades.

Run from the repository root:

```sh
scripts/run_research_cycle.sh --mode validation --wall-time 450
scripts/run_research_cycle.sh --mode subagent --wall-time 450
scripts/run_research_cycle.sh --mode team --wall-time 600
scripts/run_research_cycle.sh --mode cycle --wall-time 900
```

Defaults:one experiment family per cycle,1200seconds,one active worker/inference,
at mostone failed provider retry. The1800second hard upper bound prevents an
accidental unbounded job. Distinct roles share one local model sequentially.
Every invocation acquires a lock and creates a separate Git branch/worktree.
No automatic merge,push or scientific claim promotion. Worktrees and raw logs
remain available to Astra after failure. Review before removing an old worktree;
never delete raw scientific evidence to make disk space automatically.

Astra must inspect `results/qwen_cycles/<id>/run.json`,streamed tool logs,
worktree diffs,tests and raw data;attempt falsification;verify replication;then
record accept/reject/rerun. `EXECUTED_PENDING_REVIEW` is not scientific completion.
The small initial n4 mission uses supplied fixed graphs/seeds and an optimum-blind
conditional collision-aware loss. It is a diagnostic,not a new contribution.

Each role is in `.qwen/agents/`;QWEN.md explains the repaired bugs and live
research state. The literature role requests missing sources from Astra because
workers have no external network. A local model cannot certify mathematical
correctness or novelty merely by writing a convincing report.

The launcher explicitly checks OS confinement with both a permitted write and
a denied manuscript write plus a successful localhost request before running
Qwen. Root and worktree manuscript hashes must match before/after. It strips
caller QPU/provider secrets,disables cloud inference,unloads the model after
work,and terminates a server it started. Do not replace this confinement with
unrestricted YOLO. The current launcher fails closed outside macOS;Docker/vLLM
were not installed as a substitute.

Observed capability limits are in `reports/QWEN_INFRASTRUCTURE_VALIDATION.md`.
Native subagent/team probes failed on this model;do not infer success from enabled
flags or an exit0. The first scientific raw data and replication executed,but
Qwen's report/critic stages failed quality or completion checks. Astra's separate
audit is authoritative. Future prompts restrict metric transcription to generated
JSON and give the critic a compact evidence bundle to reduce wandering. These
prompt changes do not retroactively turn failed runs into successful cycles.

That paragraph describes the initial direct-agent/team probes. The later
validated native path is a saved Workflow:

```sh
scripts/run_research_cycle.sh --mode workflow --workflow-name density-research-cycle \
  --workflow-agents 9 --wall-time 1500 --max-failed-retries 0
```

Nine sequential child contexts cover seven roles, with four typed local MCP
scientific actions. The bridge builds fixed argv, uses PASQAL_PYTHON and
separates primary/replication outputs. No shell command transcription is needed
for these actions. Their reports are mechanically generated finite checks,
explicitly separate from proof/novelty acceptance. The launcher approves only
the reviewed research server in its isolated runtime. It marks science writes
non-idempotent and refuses evidence overwrites. Plain completion is the observed
working route; native synthetic-schema probes remain failed evidence.

After a run, retain contexts with scripts/retain_qwen_research_run.py and verify
the actual MCP responses, complete raw grids and exact result handoffs. Read
reports/ASTRA_P33_COMPLETED_CYCLE_REVIEW.md for the completed20261122T014822Z
cycle, accepted finite calculations and rejected model explanations. Distinct
native workers and real communication do not make those explanations correct.
The separate native Agent Team lifecycle still has no passing validation.

An interrupted first n4 cycle can have at mostone explicitly requested recovery:
`--resume-cycle results/qwen_cycles/<original-id>`. It retains its worktree,
data and remaining budget. The historical one-off supervised replication script
is retained in its run directory;it was not an automatic retry loop. Recovery
cannot certify scientific conclusions. Do not resume a completed diagnostic or
spend cycles until a favorable sign appears.

Large historical raw JSONL/Fock distribution files are sparse-excluded in worker
checkouts to avoid duplicating hundreds of MB per cycle. Original data remain
in the primary checkout and Git history. Newly generated cycle evidence is never
sparse-excluded or discarded. Access to a historical raw file can be granted by
Astra when needed;do not infer a scientific absence from a sparse worktree.
