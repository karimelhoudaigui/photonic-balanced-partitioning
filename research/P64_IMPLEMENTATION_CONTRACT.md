# P64 executable candidate: frozen qualification contract

25-Nov-2026. Base worktree `research/p64-structured-sampler`, proof commit
`4ef4242ae252ad9bce8be6379bc5bc22230f4f6a`. CODE ONLY at this checkpoint.
No module has been imported, no test run, no source support enumerated and no
phase/count/graph draw made while preparing these files. ROOT must review and
allocate one numerical-worker slot before the command below can be executed.

## Implemented mathematical interface

`research/P64_structured_sampler.py` implements the proof's full, fixed-Theta
conditional sampler for the stated lossless indistinguishable-photon model,
with d6/N18 and a d2/N6 qualification analogue. Ports are `a*d+i`; positive
Fourier convention; the output mixer is `[[3,-4],[4,3]]/5` on ports0,d.
The intermediate phase is theta[b,i]. Every collision is kept.

Fourier source coefficients use Python integer pairs in Z[xi], xi²=xi−1.
All462 d6 occupations, including exact zeros, have integer probability
weights with denominator6^6. The necessary suppression rule and support
upper bound80 are checked; the actual nonzero count is deliberately unknown
until an authorized qualification. No admissibility filter substitutes for
the polynomial or its zeros. Source sampling uses integer ranks, so this
part does not threshold floating probabilities.

Sampling three source rows supplies only M. The code discards those rows,
enumerates S² ordered row pairs and reconstructs every compatible third
row. The conditional coherent amplitude uses sqrt(P(M)), with P(M) computed
as an exact Fraction. The rounded state norm is compared relatively against
that exact mass before an explicit normalization. No S³ cache exists.

Every local tritter column is constructed by an exact three-variable
creation-polynomial DP. Unmixed raw F3 has squared scale3; mixed raw
`5*V0*F3` has squared scale75. For input x, the exact norm denominator is
scale^sum(x) times product(x!). Output coefficients include product(o!).
Integer mass is checked before conversion to floating amplitudes. This
checks the bunched-input factorial rather than relying on a distinguishable
multinomial. Inputs are in0..d, but every full output triplet is retained,
including one mode containing all18 photons. Columns are cached lazily.

The live state is a sparse map, grouped by orthogonal unmeasured suffix.
Each group's current inputs are summed coherently before squaring. Distinct
suffixes are traced by adding squared magnitudes. A selected output projects
and normalizes that suffix state. No residual row-sum-six condition is added.
Only exact source zeros are excluded. Rounded cancellation zeros remain in
the live map; no amplitude threshold or support trimming is allowed.

## Precision and resource boundary

The source and tritter coefficient work is exact. Phase evaluation, complex
amplitudes, conditional sums, normalized CDFs and float quantiles are rounded
binary64 arithmetic. This is an APPROXIMATE implementation of the proved
ideal-probability sampler, without a certified global TV bound. Checking a
small law against a separate permanent reference does not certify all N18
phase points, conditional branches or adaptive trajectories.

Constants frozen before data:

- finite/nonnegative probability checks; mass drift tolerance2e-10;
- N6 individual-probability reference tolerance2e-11 and full-law half-L1
  tolerance2e-9 at phases0,pi/6,pi/3,-0.4;
- support at most80, compatible width at most6400, transition entries at most
  `2*7^3*190=130340`; no whole-sector matrices or fullN18-PNR table;
- complete-law enumeration allowed only d2/N6; N18 random draws0 in this
  qualification; no graph, optimum, training or decoded selection;
- CPU60s, wall90s, thread1, logical plan256MiB, logs/scientific outputs32MiB,
  one numerical worker, failed retries0. Logical bytes are not a Darwin RSS cap.

Nonfinite/negative mass, a mass drift beyond the fixed tolerance, inaccessible
CDF bins, zero requested conditioning mass, invalid RNG output, exceeded
support/cache bounds or reference failure must stop and be preserved. No
seed replacement, precision relaxation, omitted branch, retry, calibration
or new phase is automatic. Normalization within tolerance is explicit in
the code and still contributes rounding error; it is not exact simulation.

For arbitrary computable phases a certified interval/refinement categorical
sampler remains a possible separate implementation, not a completed feature.
No wall-clock, CPU speed, memory RSS or fixed-total-resource advantage has
been measured here.

## Qualification and independent reference

The tests use a separately written dense six-mode factorization and a
six-input Ryser permanent, rather than the production source recurrence,
tritter polynomial, conditional trace or an imported production sampler.
It checks all462 full probabilities at each fixed phase above. This is a
separate numerical formula within this code authoring task, not a blind
fresh-agent replication, exact interval proof or new physical measurement.

Other synthetic guards cover Fourier HOM, every source zero/mass/residue,
vacuum and bunched tritters including input(6,6,6), orthogonal columns,
coherent versus dephased current inputs, orthogonal suffixes, all18 photons
in one color without a random draw, zero-mass/invalid-phase/resource/CDF
failures, a retained phase response and reproducible N6-only draw paths.
The seed6400001 is fixed for two identical twelve-draw N6 synthetic paths;
seed6400002 is used only in failure guards. No optional scientific comparison
is passed by these tests. `source_table.json` preserves all462 exact rows.
Four separate fixed files `phase_0.json` through `phase_3.json` preserve every
one of the462 occupations with both actual and independent-reference
probabilities at the corresponding phase, plus maximum absolute error,
half-L1 error, both total norms and the binary64 phase value/hex. Each law is
written before its comparison assertions. A session fixture creates the data
directory once with `exist_ok=False`; every artifact uses exclusive `x`
creation. Existing directories/files cause failure, never overwriting.

This provenance-only delta was prepared after candidatebff4a48 and before
qualification. Sampler mathematics, phases, tolerances and seeds are unchanged;
the scientific source file retains SHA256
`68055f83ead4f54303b90933ed5ebb5940a548a19cb72f496da374ad2e25780d`.

ROOT review must precede this prospective command from the worktree root:

```bash
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root "$PWD" --contract research/P64_qualification_contract.json \
  --input research/P64_structured_sampler.py \
  --input tests/test_p64_structured_sampler.py \
  --input research/P64_IMPLEMENTATION_CONTRACT.md \
  --input theory/P64_fixed_phase_complete_structured_sampler.md \
  --input research/P64_STRUCTURED_CLASSICAL_ADVERSE_CARD.md \
  --input pyproject.toml --input requirements-research-lock.txt \
  --input research/P64_qualification_contract.json \
  --output research/P64_qualification/run_001 \
  --result research/P64_qualification/run_001/junit.xml \
  --result research/P64_qualification/run_001/data/source_table.json \
  --result research/P64_qualification/run_001/data/phase_0.json \
  --result research/P64_qualification/run_001/data/phase_1.json \
  --result research/P64_qualification/run_001/data/phase_2.json \
  --result research/P64_qualification/run_001/data/phase_3.json \
  --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 \
  --max-threads 1 -- /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python \
  -c 'import os; os.environ["P64_QUALIFICATION_ARTIFACT"]="research/P64_qualification/run_001/data"; import pytest; raise SystemExit(pytest.main(["-q","tests/test_p64_structured_sampler.py","--junitxml=research/P64_qualification/run_001/junit.xml"]))'
```

The input closure and result paths must match the contract exactly. Any
failed execution retains the original manifest/logs/results. The contract
and command are prospective, not evidence of execution or permission for a
subsequent graph pilot. ROOT must inspect actual results and validate v2.

## Total-cost obligation before any research use

A future cost adapter must start before constructor/source setup, source and
transition DP, imports, initial/cold work, cache allocations and RNG creation.
It must include each M draw, all S² reconstruction, phases at each Theta,
norm/precision checks, groups/sorting, both trace/projection passes, cache
misses, final count collection, rank/tie decoder, graph score and optimizer
updates. Reusing a trained Theta or warm cache must follow the identical
paid boundary used for the competing procedure; neither is a free frontend.
This candidate has no cost-adapter claim and never reports a warm draw as
the complete algorithm's measured cost. Exact-law equality does not imply
pathwise identical seeded samples or fixed-budget dominance.

No paper, previous raw data, known optimum, graph panel, hardware credential,
QPU or external message is touched. Positive optimization objective OPEN.
