# P42 independent ordered-state replication — advance contract

Frozen before execution, 2026-11-24. Worktree `.local/p42-replication`, branch
`research/p42-replication`, base `525e2549907a478623df7c0e49190c423e5e8291`.
The independent analytic derivation was sent before reading the author proofs.
Those proofs were subsequently reviewed; neither primary computation
`P42_loss_spectrum_probe.py` nor primary raw data has been read or imported.
No result is predicted from a previously inspected numerical population.

## Finite population and physical construction

`experiments/P42_replication/cases.json` lists ALL 42 configurations, in order.
There are four efficiencies, eta in {0,0.1,0.5,1}: exactly 168 complete laws.
Sources have m<=4, N<=4, fixed occupations including vacuum, distinct photons,
(2,0,0), (2,1,0), (2,1,1,0) and (4,0,0,0). Internals are common pure states,
orthogonal states, or the declared normalized complex nearest-neighbor vectors
in internal dimension N<=4. Complex phases are retained in amplitudes.
Unitary controls are identity, an Rx balanced first pair, and complex QR
unitaries from PCG64 seeds 2026112471 and 2026112472, generating dimensions
2,3,4 in that fixed order. These seeds differ from the primary seeds.

The implementation independently forms the actual sum over N! permutations of
the N spatial/internal one-particle factors and normalizes its full amplitude.
Repeated spatial/internal factors remain repeated in that sum. Tensor axes are
spatial0,internal0,spatial1,internal1,...; for each r it traces EVERY internal
degree and the last N-r spatial factors by amplitude matricization and AA*.
The conditional spatial density is then transformed by U tensorpower r.
All ordered output words are aggregated into occupation probabilities.
Uniform loss sectors are mixed using enumeration of all 2^N Bernoulli survivor
patterns. No probabilities are clipped or renormalized after measurement.

## Checks and interpretation

Check source normalization and bosonic symmetry; unitary and density invariants;
absence of coherence across different input remainders; input block traces
against indexed-survivor enumeration; its independent agreement with product
binomial multiplicities; binomial sector weights; all-photons-detected eta^N;
and output normalization, including vacuum and collisions. Equal internal
states must have all spatial mass in the symmetric subspace.

Enumerate every output support, including the empty set, for every r. Count
ordered words and unique occupations independently, and compare to the stated
Stirling/composition ranks. Threshold accepts all surviving r with exactly that
support; PNR total=k keeps only r=k. Compute the upper caps using directly
measured input-block traces sorted in decreasing order, with the appropriate
enumerated projector rank. Apply the symmetric rank only to the equal-internal
cases; use the ordered rank for arbitrary internals. Test HOM overlap in the
balanced distinct two-input controls. Retain the declared bunching falsifier
at eta=0.1: four photons from one mode split into two output modes can exceed
the DISTINCT-input cap0.01. This tests scope, not a failure of the general cap.

All invariant residuals must be below1e-10; probability-minus-cap must be at
most1e-10. Retain failures and complete laws; no favorable-case filtering.
A pass is finite floating-point validation of these constructed cases only,
not a universal proof, interval certificate, novelty or advantage claim.
No N8DFT experiment, source optimization, sampling, detector calibration,
production-code import or QPU is included. Author proof knowledge is disclosed;
numerical implementation/data independence must not be inflated into complete
author blindness.

## Freeze and execution command

Commit this contract, the JSON contract, complete case list and code BEFORE
the command below. Execution is already authorized after that freeze. Any
failure is preserved, and changes or reruns require a distinct declared record.
Every local execution dependency is among the four repeated --input paths;
the code imports only standard library and NumPy2.4.6 (Python3.11.15).

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P42_replication_contract.json --input research/P42_replication_contract.md --input research/P42_replication_contract.json --input experiments/P42_replication/cases.json --input experiments/P42_replication/ordered_replication.py --output experiments/P42_replication/run_001 --result experiments/P42_replication/run_001/laws.jsonl --result experiments/P42_replication/run_001/states_and_sectors.json --result experiments/P42_replication/run_001/summary.json --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P42_replication/ordered_replication.py --cases experiments/P42_replication/cases.json --output experiments/P42_replication/run_001
```

Limits: one sequential process; six numerical thread environment variables1;
CPU60 seconds and wall90 seconds; each array<=64MiB, all outputs<=32MiB.
Largest declared source is (m*d)^N=16^4 complex entries, 1MiB. Darwin cannot
enforce CPU affinity through the runner, so --max-cores is deliberately absent;
no CPU affinity guarantee is invented. This does not relax the sequential
calculation, one numerical thread or CPU-time bound. The runner records real
status, actual Git context, versions, input before/after hashes and outputs.

Validate its v2 manifest with the installed computation-audit
`scripts/validate_manifest.py MANIFEST --root WORKTREE`. Read completed status
before interpreting its result. No primary-code/data comparison occurs until
after this frozen independent execution; such a comparison, if requested,
must be reported separately with the boundary made explicit.
