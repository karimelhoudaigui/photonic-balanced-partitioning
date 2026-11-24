# P41 encoding checkpoint — grouped classical control

Base f09c7ec; pre-execution proof/code/contract commit
`4f499b487855cab05009a0c66e066950ac7167ad`.

## Result and interpretation

The route has a complete standalone proof of a normalized correlated
classical sampler dominating every unconditioned accepted output probability
of a passive single-photon circuit restricted to one photon per fixed output
group. Its efficient proposal uses random signs, one matrix-vector multiply,
one acceptance Bernoulli and independent categorical draws within groups.
This is a substantive obstruction to attributing a paired-output circuit's
per-attempt improvement tail to an irreproducible bosonic sampling mechanism.
It uses the known Gurvits random-sign permanent identity; composition novelty
remains OPEN. The proof has not yet received an independent audit.

The theorem is about attempted proposals/nonnegative utility. It is NOT a
global obstruction to optimum-blind graph optimization: arbitrary CF decoding,
adaptive training, quantum feedforward and total realized query/time costs
need further work. Two explicit non-implications and a failed all-CF extension
are in `theory/P41_encoding_scope_counterexamples.md`.

## Executed finite assertion

One registered run only: `experiments/P41_encoding/run_001/manifest.json`.
The Mathbox v2 runner records clean pre-execution Git state, exact argv,
input hashes before/after, versions, resources and result hashes. Its status
is completed and the manifest validator accepts it. Wall time19.853602s,
CPU cap60s, wall cap90s, one conventional numerical-library thread. Array
planning was bounded; no process address-space limit or CPU affinity was
requested. Result/log size is below32MiB. All declared inputs stayed unchanged.

- 16 Gaussian-rational cases, k<=4,m<=8, including real/complex phases,
  variable group sizes, singleton herald/vacuum remainder, a lossy contraction
  and two row relabelings. This is an exact finite matrix set, not Haar sampling.
- 1260 complete Fock occupations agree between creation-polynomial recursion
  and independent explicit permutation sums, with correct occupation factorials.
- 116 accepted outputs satisfy p_b<=q_rejecting<=q_always exactly in Q(i).
  All16 sign-weight populations obey0<=w<=1 and normalize with failure mass.
- Two Perceval SLOS full-law checks cover10 and56 Fock outcomes. Max error
  is8.326672684688674e-17, below the fixed1e-10 tolerance.
- Two rational sharp-frontier families and the Walsh Bell control saturate
  the checked squared form of pC<=1-p; all tested two-group frames obey it.
- The all-CF extension fails normalization exactly:913/625>1, as predicted.
- The actual classical sampler ran2048 attempts with seed2026112411 on the
  Walsh hand control, returning990 outputs(0,2) and1058 outputs(1,3), no
  failures. These are classical simulated counts, not measured photon counts.

The hand control has unconditioned success1/2 for bosons versus1/4 for
same-circuit distinguishable photons, but the new correlated control succeeds
with probability1. This is a diagnostic of an inadequate baseline, not an
optimum-blind trained algorithm or an advantage result. Independently optimized
distinguishable circuits can of course do better than this particular fixed
distinguishable circuit; no contrary comparison is implied.

## Audit provenance and next work

The author supplied the proof and probe. The two rational constructions and
Perceval backend are separate implementations, but this is not an independent
human/agent replication. The source record discloses primary versions and
limited search coverage. The numerical record does not certify novelty.

No pre-existing files, P33/P37/E05b data or manuscript sources changed. No
QPU, account query, paid provider, model download or GitHub push was used.

Next: independent proof reconstruction and finite replication; exact prior-art
comparison for stratified mean-field/coherent-light sampling; integrate this
control in any paired-output proposal benchmark. Investigate mechanisms outside
the theorem rather than rerunning the same16 cases or claiming the unrestricted
goal complete.

## Reproduction command

The frozen exact command and input closure are in the manifest. To reproduce,
use the installed computation-audit runner, the seven listed --input files,
the frozen contract and a NEW output destination; retain the60CPU/90wall/one-
thread caps. The runner's --result paths and the probe's --output must all use
that new destination. No command executes hardware or overwrites old outputs.

On the recorded machine, from this worktree, the exact fresh-output replay is:

```sh
P41_PYTHON=/private/tmp/pbp-clean-venv-20261124/bin/python
P41_RUN=experiments/P41_encoding/reproduction_001
PYTHONPATH=src OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "$P41_PYTHON" \
 /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
 --root "$PWD" --contract research/P41_encoding_probe_contract.json \
 --input research/P41_encoding_probe.py \
 --input theory/P41_encoding_grouped_domination.md \
 --input research/P41_encoding_sources.md \
 --input src/photonic_balanced_partitioning/hardware/offline.py \
 --input src/photonic_balanced_partitioning/photonic/fixed_photon_obliq.py \
 --input pyproject.toml --input requirements-research-lock.txt \
 --output "$P41_RUN" --result "$P41_RUN/raw.jsonl" --result "$P41_RUN/summary.json" \
 --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1 \
 -- "$P41_PYTHON" research/P41_encoding_probe.py --output "$P41_RUN"
```
