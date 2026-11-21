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

Defaults:one experiment family per cycle,600seconds,one active worker/inference,
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

Large historical raw JSONL/Fock distribution files are sparse-excluded in worker
checkouts to avoid duplicating hundreds of MB per cycle. Original data remain
in the primary checkout and Git history. Newly generated cycle evidence is never
sparse-excluded or discarded. Access to a historical raw file can be granted by
Astra when needed;do not infer a scientific absence from a sparse worktree.
