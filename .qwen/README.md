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

After the initial diagnostic, Astra can supply another small mission:

```sh
scripts/run_research_cycle.sh --mode cycle --mission-file /path/to/mission.txt
```

Each cycle remains one experiment family with bounded time, one active worker,
fixed seeds, adversarial review and fresh-seed replication. No automatic merge.
