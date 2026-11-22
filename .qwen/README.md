# Local research team

The measured M2/8GiB host uses one Qwen3.5 2B Q4 model at a time.
This setup is free of paid inference tokens; it is not a claim of frontier
scientific reasoning. Read `QWEN.md` and the installation/validation reports.

External tool installation used:

```sh
npm install -g @qwen-code/qwen-code@latest
HOMEBREW_NO_AUTO_UPDATE=1 brew install ollama
qwen --version
```

Recreate the chosen alias only after auditing resources on the target machine.
In a terminal running from the repository, start the bounded local server:

```sh
OLLAMA_HOST=127.0.0.1:11435 OLLAMA_MODELS="$PWD/.local/ollama/models" \
OLLAMA_NO_CLOUD=1 OLLAMA_NUM_PARALLEL=1 OLLAMA_MAX_LOADED_MODELS=1 \
OLLAMA_CONTEXT_LENGTH=32768 OLLAMA_KEEP_ALIVE=60s ollama serve
```

In another terminal, with the same repository working directory:

```sh
export OLLAMA_HOST=127.0.0.1:11435
ollama pull qwen3.5:2b-q4_K_M
ollama create pasqal-qwen-research -f .qwen/Modelfile
scripts/run_research_cycle.sh --mode validation --wall-time 450
```

The source tag's checked digest and actual versions are in
`reports/LOCAL_MODEL_SELECTION.md`. The alias adds only parameter metadata.
Model blobs, nonsecret localhost SDK placeholder, logs and runtime state are
not credentials committed to this directory. Real credentials never belong here.
No QPU or cloud inference is enabled. The launcher uses its own git-ignored
Qwen runtime directory, strips caller credentials, and injects the localhost
placeholder into that child environment only.

`agents/` contains seven official YAML-frontmatter definitions. The experimental
Agent Team feature is enabled; actual delegation/team validation is a separate
gate from loading definitions. The small host runs role sessions sequentially.
See `scripts/QWEN_RESEARCH.md` for the bounded worktree/audit protocol and
`reports/QWEN_INFRASTRUCTURE_VALIDATION.md` for observed PASS/FAIL outcomes.

Validated seven-role execution path (2026-11-22):

```sh
scripts/run_research_cycle.sh --mode workflow --workflow-name density-research-cycle \
  --workflow-agents 9 --wall-time 1500 --max-failed-retries 0
```

The saved Workflow owns sequential dispatch. Four parameterless local MCP
actions supply fixed scientific argv and the pinned Python; they preserve
separate primary/replication data and generate factual finite-check reports.
The launcher approves only that reviewed stdio server inside its isolated
runtime. Scientific writes are non-idempotent and refuse overwrites. Agents
finish in plain text; their raw receipts and native contexts remain available
for independent review. Experimental Agent Team lifecycle remains FAIL.
This path produced300 complete grid simulations and fresh replication, audited
by Astra. The model's incorrect scientific explanations were rejected. See
`reports/ASTRA_P33_COMPLETED_CYCLE_REVIEW.md`; installed/executing agents do not
constitute autonomous scientific acceptance, novelty or an advantage result.

After the initial diagnostic, Astra can supply another small mission:

```sh
scripts/run_research_cycle.sh --mode cycle --mission-file /path/to/mission.txt
```

Each cycle remains one experiment family with bounded time, one active worker,
fixed seeds, adversarial review and fresh-seed replication. No automatic merge.
