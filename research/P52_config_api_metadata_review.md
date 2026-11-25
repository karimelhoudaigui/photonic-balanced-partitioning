# P52 official native thread interface: read-only metadata

ROOT authorized a single tiny read-only API process after successful
qualification68b8c83. Source/contract were frozen before execution at7286e9e.
No Config instance, assignment/setter, permanent, Fock or Perceval call occurred.
The installed exqalibur subtree contains no `.pyi` file (`rg --files` filtered
for `.pyi` returned no matches). No vendor change was made.

Actual class documentation identifies **static property
`exqalibur.Config.compute_max_thread_count`**, a maximum CPU thread count for
parallel algorithms including permanent computation. Its documented default
uses available CPU cores. The class requires no instance. The member appears
in `dir(Config)` and reading its class attribute yields an int. This is an
official interface, unlike an invented permanent keyword.

Precision of the frozen probe's scope label: it says "no ... getter ... call"
to mean no explicit getter **method invocation**. The authorized read-only
`getattr(Config, name)` can invoke a native property accessor; for this member
it returned an int, not a descriptor. Its value was not stored. Thus this was
a permitted class-member read, not proof that no native accessor ran. Raw
source/output are retained byte-identically; this clarification does not
retroactively change their provenance.

Prospective source proposal, **not executed here**:

```python
before = int(xq.Config.compute_max_thread_count)
xq.Config.compute_max_thread_count = 1
after = int(xq.Config.compute_max_thread_count)
if after != 1:
    raise RuntimeError("native maximum CPU thread readback is not one")
```

Place this after local imports but before any backend/permanent use, recording
before/after and documentation/binary hashes. A later numerical check should
verify readback again after work. It changes only the configured native
resource maximum, neither matrix/factorial formula nor floating precision.
The permanent doc from run_003 says the default method depends on allowed
threads (Glynn for1/2, otherwise Ryser); setting this maximum can therefore
also select the engine's default algorithm. No `ptype` override is proposed,
and a new qualification must cover this newly configured execution path.
It still does not measure OS thread scheduling or independently audit the
native engine's implementation. It needs a new source freeze/review and
qualification authorization before any full run. No source setter was added
to the production validator at this checkpoint.

Actual runner command, inside the isolated worktree:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P52_config_api_metadata_contract.json --output research/P52_config_api_metadata/run_001 --input research/P52_config_api_metadata.py --input research/P52_config_api_metadata_contract.json --result research/P52_config_api_metadata/run_001/data/api.json --timeout 10 --max-output-bytes 1048576 --max-cpu-seconds 5 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python research/P52_config_api_metadata.py --output research/P52_config_api_metadata/run_001/data/api.json
```

Runner completed exit0, within CPU5/wall10. Metadata reports Python3.11.15,
exqalibur1.4.2, processCPU0.011748s, wall0.02565725s, DarwinRSS32768000B,
Perceval not imported. BinarySHA256
`b4687bc81b37cb447eb0c9c4fa89523da7feed8584a31ca74798ac3bcee06749` agrees
with the earlier qualification. The exclusive slot was released immediately.

Durable files under `research/P52_config_api_metadata/run_001/`:

| File | SHA256 |
|---|---|
| manifest.json | 8d3526b5084e57203487e8a0e200bb9826ce94361ff8ee459e0d93682cad00e1 |
| data/api.json | 8d382d3501ce5c5aa6264067da50d1866e1cbc8b7a1f784552a9d45892e17392 |
| stdout.txt | 8d382d3501ce5c5aa6264067da50d1866e1cbc8b7a1f784552a9d45892e17392 |
| stderr.txt (empty) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

Both input hashes agree before/after. The actual Mathbox v2 validator command
on this manifest with `--root` the isolated worktree returned0, valid evidence
record status completed. This validates the metadata closure, not native
thread enforcement or physical probabilities. P52 full replication and P53
numerical work were not performed.
