# P44 independent passive-dilation validation receipt

## Outcome and separation from the proof

**Finite numerical assertion passed at absolute tolerance 1e-10.** The single
run_001 has Mathbox v2 status `completed`, exit 0, and genuine clean execution
commit `068791232198ea576fa0bee4f0a3b3a36bb77bd8`. All four contract/code/case
inputs were committed before execution. Their before/after hashes agree.
There was no second physical run, replacement of a failure, or changed-code
rerun. The manifest validator accepted the completed evidence record.

The analytic author-proof review is a SEPARATE commit
`9b240c3f722d5a7ac4d3483886f5308bf34ad365`, reviewing source SHA256
`5407871a6afe5f6d7eb478792c88b73c964918bd593dbd19ef6d56e82204730b`.
Its independent derivation was already frozen at
`2d15012abdfdb96cac6fface3eac326a0d3f191a`, before author-file reading.
The proof verdict does not derive from this run or from its pass flag.
No proof/source/raw/manuscript file was modified to obtain the result.

Numerical independence: this program uses only standard library and NumPy.
No root/project physical module, primary numerical code, previous P42 code or
primary raw result is imported or copied. No primary P44 numerical code/raw
was read before or after this run. The analytic author proof was read before
this numerical design; its knowledge is disclosed rather than called complete
author blindness. The reviewer authored older noise/P40 components and
reviewed P33/P37; none is executed here or relabeled third-party evidence.

## What was physically constructed

There are 190 fixed small cases, all preserved: system m=2/3, photon N=0..3,
internal dimension 1..3. The population includes 88 equal-internal, 34 orthogonal,
34 partial-complex-product and 34 genuinely correlated-internal configurations.
The correlated fixtures are 22 two-input singlets and 12 complex cyclic
three-input states. Their local internal purities are checked against 1/2 and
1/3, versus 1 for product states. There are 88 nonuniform-loss configurations
and 102 zero/unit/uniform-quarter control configurations. The full list and
fresh seeds 2026112483/2026112484 were frozen in cases.json.

For each singular-intensity profile, complex QR mixers L,R give T=LDR* and
the explicit passive unitary

    W = [[LDR*, -LE], [ER*, D]],
    D^2+E^2=I.

The environment input modes are vacuum. The full combined spatial/internal
bosonic source is formed by symmetrizing its N-tensor and normalizing the
actual amplitude. W acts on each spatial particle axis, with identity on
internal states. Internal degrees are traced by amplitude matricization and
AA*. No full joint-density matrix of the internal space is allocated.

The complete spatial occupation law on all 2m system/environment output modes
is exported FIRST. Global photon number remains N. System laws are then
obtained by summing the environment counts. All loss sectors, vacuum sectors,
collision outcomes and exact zeros are retained. This is not a commutation or
binomial approximation to nonuniform loss, and no detected law is normalized
after rejecting anything. Uniform controls alone are compared to binomial
sector weights. The occupied-column norm, full norm and mean input survival
are distinct saved quantities; no mean transmission is substituted for a
spectral bound.

All 1240 possible output support rows across the population are saved, including
empty diagnostic supports. Exact support, all-S-click and a decoder choosing
the first k actual clicks are compared separately. Each fixed k defines one
candidate decoder, not a batch of free optimization candidates. Environment
outputs are unobserved by that decoder; their counts remain in the raw law.
No graph score, optimum, parameter optimization, sampling shots or QPU appears.

## Independent invariants and observed residuals

Full tensor evaluation supplies the moments and event probabilities. Separate
small permutation sums supply identical-source distinct-column permanents,
repeated-column Cauchy--Binet and the algebraic permanental envelope per(BB*).
Opaque internal cases use only the proven robust routing/spectral caps; their
comparison to the identical envelope is saved as a diagnostic, not enforced.
Product states are additionally checked with the COMPLEX double-permutation
Gram formula; singlets with determinants and collision suppression. The
all-photons-detected probability is checked through the appropriate product-
internal permanent or singlet determinant. This does not simulate a thermal
source, supply a thermal sampler or dominate its whole occupation law.

| Check | Largest absolute residual |
|---|---:|
| Dilation unitarity | 8.881784197001252e-16 |
| Declared singular-intensity profile | 6.661338147750939e-16 |
| Internal/source normalization | 4.440892098500626e-16 |
| Symmetrization norm squared versus N! | 8.881784197001252e-16 |
| Global/system output-law normalization | 1.3322676295501878e-15 |
| Detected mean versus Tr(T_A*T_A) | 1.1102230246251565e-15 |
| Uniform-control sector weights | 1.1102230246251565e-15 |
| Product-internal all-detected probability | 4.440892098500626e-16 |
| Permanent Cauchy--Binet with repetitions | 3.3306690738754696e-16 |
| Identical physical moment versus distinct-column sum | 1.2212453270876722e-15 |
| Complex product-Gram moment identity | 1.3322676295501878e-15 |
| Correlated singlet moment versus determinant | 4.440892098500626e-16 |
| Singlet full-physical-mode collision probability | 9.303523555925372e-34 |

Maximum positive bound excesses were 8.881784197001252e-16 for the identical
spectral/envelope and robust routing/spectral checks; the event-to-moment
excess was 0. Reduced density matrices retain a numerical minimum-eigenvalue
defect up to 7.026888608594574e-16; it is not rounded into an exact PSD claim.
Numerical semantics remain `FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED`.

The opaque cases' maximum excess over the permanental envelope was only
4.440892098500626e-16. That absence of a meaningful violation in this small
population does NOT establish the stronger identical bound for arbitrary
internals. The independently retained analytic DFT/species counterexample
remains relevant and lies beyond this m<=3,N<=3 validation range. No such
larger counterexample was rerun or quietly excluded from a declared grid.

## Actual command, manifest closure and resource observations

Worktree `/Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication`, branch
`research/p42-replication`. The actual single command was the frozen command:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py --root /Users/karimelhoudaigui/Desktop/pasqal/.local/p42-replication --contract research/P44_replication_contract.json --input research/P44_replication_contract.md --input research/P44_replication_contract.json --input experiments/P44_replication/cases.json --input experiments/P44_replication/dilation_replication.py --output experiments/P44_replication/run_001 --result experiments/P44_replication/run_001/full_laws.jsonl --result experiments/P44_replication/run_001/summary.json --timeout 90 --max-output-bytes 33554432 --max-cpu-seconds 60 --max-threads 1 -- /private/tmp/pbp-clean-venv-20261124/bin/python experiments/P44_replication/dilation_replication.py --cases experiments/P44_replication/cases.json --output experiments/P44_replication/run_001
```

The four execution_artifacts exactly match the four --input paths: both
contracts, case list and executed standalone code. The observed Python3.11.15
and NumPy2.4.6 versions are recorded. The installed runner's hash was pinned
in the JSON contract. Every input's observed SHA256 is unchanged afterward.
There are no missing or invalid results.

Run start 2026-11-24T21:41:56.985974+00:00, clean preregistration commit above.
Child timed CPU 0.35518 seconds; child timed wall 0.413643584 seconds; runner
launch-to-exit wall 0.617558 seconds. Child timings begin after NumPy import,
whereas the enforced CPU limit covers the whole child process. Limits were
CPU 60 seconds/wall 90 seconds and six numerical thread variables set to 1.
Observed maximum RSS was 40,009,728 bytes on Darwin. The largest explicit array
was 746,496 bytes, well below 64 MiB. Darwin affinity is unsupported and truthfully
recorded null; no hard virtual-address or CPU-affinity guarantee is fabricated.

The five outputs together occupy 1,448,866 bytes. A read-only stdlib receipt
check after the run verified that records exactly match all 190 frozen cases
in order, every joint law has binom(N+2m-1,N) occupations, and there are 4270
joint occupations total. No second physical calculation is hidden in that
serialization/hash check. All 190 completed cases, including endpoint/vacuum
and correlated cases, remain in immutable run_001.

| Artifact | SHA256 |
|---|---|
| Frozen MD contract | `827be0764f9e0d024e8d1c19f2b077ad55b2986e19f5375e1f74c468f05b091b` |
| Frozen JSON contract | `8aa2837c212785dfeb5a1b6ebc33a90fb7952f4b3970bf6bbd9086dac79653ba` |
| Frozen cases | `a59496755416f2b5ee1dd391a18cb616b183efc20c2aa3470a0600a71d462b4c` |
| Frozen code | `60a6bbbeeb3aaf410f448d428aad4f4afcbc582bf2d73d3d792831dced50b7ba` |
| `run_001/full_laws.jsonl` | `8647c0d1de318d13ba884142a00ceb26939686820955578031f180164e2498ae` |
| `run_001/summary.json` | `02e5571ebe0bac749e2156e17eb1ff2438f5ee4a69ece1fcac7bfbcdaac09714` |
| `run_001/manifest.json` | `e898d60137bcb85a5fe19511b254cc710d9a27bf19208488fd92fc3aa25095f9` |

Actual manifest validation returned a valid completed evidence record:

```sh
/private/tmp/pbp-clean-venv-20261124/bin/python /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py experiments/P44_replication/run_001/manifest.json --root .
```

## Interpretation and remaining limits

This checks normalization factors, complex phases, nonuniform passive dilation,
the environment trace, moment identities, decoder inclusions and correlated-
internal robust caps in a predeclared finite range. The complete analytic proof
is in separate receipts; this run does not prove its arbitrary-N quantifier.
Selected QR mixers and pure correlated fixtures are not exhaustive unitary,
internal or mixed-state coverage. No numerical stability/interval certificate,
thermal sampling theorem, optimization advantage, global novelty or actual
Lucy transmission/cost calibration follows. Previous P42/P43 raw and inputs
are unchanged. No manuscript, credentials or remote processor was touched.
