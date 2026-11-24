# P44 passive-dilation replication — advance contract

Frozen before execution, 2026-11-24, worktree `.local/p42-replication`, branch
`research/p42-replication`. The P44 analytic review is separately committed at
`9b240c3f722d5a7ac4d3483886f5308bf34ad365`; independent reconstruction preceded
author-proof reading at commit `2d15012abdfdb96cac6fface3eac326a0d3f191a`.
The proof source SHA256 is
`5407871a6afe5f6d7eb478792c88b73c964918bd593dbd19ef6d56e82204730b`.
This finite computation does not establish the theorem or replace that review.

## Population and independent physical representation

Exactly190 configurations are fully listed in the JSON case file. No case is
selected after execution. System modes m in{2,3}, N<=m, internal dimension<=3.
There are vacuum controls, one-photon sources, and fixed distinct two/three
input sources. Internals are equal pure, orthogonal pure, normalized complex
neighbor vectors, a two-input internal antisymmetric singlet, or a three-input
complex cyclic entangled state. These last two are correlated pure sources,
not substitutes by a product Gram matrix. Their one-factor purities are
checked (1/2 and1/3); product source factors have purity1.

Two fresh PCG64 seeds2026112483/2026112484 generate left/right complex QR
mixers in dimension order2then3. For each singular-intensity profile lambda_a,
put D=diag(sqrt(lambda)), E=diag(sqrt(1-lambda)), with L,R unitary, and use

    T = L D R*,
    W = [[L D R*, -L E], [E R*, D]].

Thus W is a passive unitary on2m spatial modes; the last m INPUT modes are
strictly vacuum. Profiles contain0,1, uniform1/4, and the nonuniform vectors
explicitly listed per case. No commutation of nonuniform loss is assumed.
The occupied-source norm ||T[:,A]||^2 is separately recorded from ||T||^2
and the input-mean transmission. Neither is a hardware calibration.

The program embeds the normalized internal N-tensor at its distinct source
mode labels, symmetrizes the COMBINED spatial/internal particle factors and
normalizes the actual amplitude. It applies W tensorpower N via individual
particle-axis contractions, retaining full system+environment amplitudes.
It then traces every internal factor by amplitude matricization and AA*.
Every global spatial occupation has total N; NONE of the environment/loss
occupations is discarded or conditioned away. System marginals and loss-number
sectors follow by summing this retained full distribution. Vacuum and all
collision occupations, including zero-probability entries, are saved.

The code imports only standard library and NumPy, not project/root numerical
or production code. No primary P44 numerical code or raw has been inspected.
Author-proof formulas were read before this numerical design: implementation
independence is not claimed as absence of author/theorem knowledge.

## Checks and acceptance criterion

Check normalized internal/source/output states; CF source symmetrization
norm N!; common-particle permutation symmetry; unitary dilation; declared
singular values; spatial density invariants; full-law and system-law sums;
global photon conservation and the detected mean Tr(T_A*T_A). Uniform-loss
controls additionally recover all Binomial(N,eta) sectors. Product-internal
no-loss probability is checked against per((T_A*T_A) Hadamard Gram), while
the internal singlet uses the determinant and has no physical-mode collisions.

For ALL2^m supports (1240 total rows, including empty controls), compute moments,
all-S-click probability, exact support and the decoder selecting the first k
clicked modes, rejecting fewer than k. External environmental counts are
unobserved by this decoder. Check event<=moment. Compute permanents by explicit
small permutation sums, not any imported permanent routine. Check repeated-
column Cauchy--Binet and the envelope per(BB*)<=eta_occupied^k. For identical
inputs check the distinct-column sum against the physical moment and its
spectral bound. For opaque internals check the robust k! times classical
injection/routing sum and k!*eta_occupied^k. Orthogonal product inputs have
their classical injection-sum identity; other product inputs have the full
complex double-permutation Gram identity. Singlet two-mode moments use the
independent determinant identity. Do NOT impose the identical/thermal bound
on unknown internal states; record any observed excess without filtering.

Every numerical residual and bound excess must be below1e-10. All values
remain float64 estimates, not interval-certified numbers. There is no clipping,
postselection normalization, parameter tuning, sampler comparison or graph
optimization. The permanental envelope is evaluated algebraically; no thermal
sampler is being simulated. Passing190 cases is not a universal proof.

## Freeze, execution and resource envelope

Commit these two contracts, code and COMPLETE case list BEFORE execution.
The coordinator has explicitly released the slot and authorized a single
bounded run after this freeze. Do not overwrite run_001. Preserve failures,
partial outputs and every completed configuration. Any changed-code rerun must
be a separately declared record; no failed run is silently replaced.

Exactly four execution inputs are pinned: MD contract, JSON contract, cases,
and code. NumPy2.4.6/Python3.11.15 versions were observed during preparation.
The installed Mathbox runner SHA256 is recorded in the JSON contract.

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P44_replication_contract.json --input research/P44_replication_contract.md --input research/P44_replication_contract.json --input experiments/P44_replication/cases.json --input experiments/P44_replication/dilation_replication.py --output experiments/P44_replication/run_001 --result experiments/P44_replication/run_001/full_laws.jsonl --result experiments/P44_replication/run_001/summary.json --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P44_replication/dilation_replication.py --cases experiments/P44_replication/cases.json --output experiments/P44_replication/run_001
```

One sequential child; all six numerical thread variables are1. CPU60 seconds,
wall90 seconds, each array<=64MiB and all outputs<=32MiB. The largest expected
explicit spatial density is216x216 complex128 entries (746496 bytes); largest
pure joint state has18^3 complex entries. No full joint-density matrix is
formed. Darwin cannot provide runner CPU affinity, and a64MiB virtual-address
limit would not mean a64MiB numerical-array budget: neither guarantee is
invented. Record actual RSS and the largest explicit array. The supported
CPU/wall/thread limits are enforced and recorded by the runner.

Validate the genuine v2 manifest with the installed `validate_manifest.py`,
`--root` this worktree. Check completed status, exact four-input closure,
before/after hashes, full coverage and output hashes before interpretation.
No QPU, paid model, external processor, manuscript or previous raw is touched.
