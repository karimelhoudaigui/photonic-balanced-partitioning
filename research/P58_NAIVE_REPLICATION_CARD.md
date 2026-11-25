# P58 complete permanent-engine replication: prospective execution card

Status: code/contract preparation only; **no scientific import, guard,
amplitude, tie computation or convolution has been executed**. ROOT disclosed
the candidate result (all127 strict; minimum649/327680) before this work.
The reviewer already statically reviewed P58 and earlier P53b/c computations.
This is explicitly posthoc and not blind, held-out, hardware or novelty work.

Target primary commit cc58f9a, source54ff30d. Four immutable reference pins
are in the standalone script: source_laws.json.gz0efca069..., tie archive
52bb7247..., summary7f82c318..., primary manifestf03c242c.... Bytes were
copied by git archive and hashed, without importing any primary module.
The archived input columns use the original Walsh port order.

## Independent engines and exact comparisons

The scalar matrix is built using trig exp(i*row_color*pi/3) and crossed bit
characters, not the archive's Eisenstein ring or creation recurrence. It is
aligned entrywise to the archived matrix at5e-12, but the independently
constructed matrix is used by the backend throughout. Every nonempty source
mask sets its own input Fock state, one photon at each selected input.

Local Perceval1.3 NaiveBackend.prob_amplitude invokes
exqalibur.permanent_cx and the documented Fock factorial normalization.
The installed Naive source was read before implementation, without import.
No creation DP, production helper, probability iterator, mask/pruning,
CF filter, fallback, global-phase fitting or renormalization is used.
Own multisets enumerate every output occupation and align by its tuple.

All255 groups and157183 amplitudes are mandatory, including all exact zero
reference amplitudes. Compare each native amplitude to

    (a+b*exp(i*pi/3))*sqrt(prod n!)/(sqrt(8)^r),

where the pinned archive stores the unnormalized polynomial coefficient.
Absolute amplitude tolerance5e-10 and each full source mass tolerance5e-10
are numerical cross-checks, not interval certificates or relative guarantees.
No zero is clipped. Every native amplitude is saved as real/imaginary
numbers in gzip JSONL, one complete group per line. A finite mismatch retains
all complete native data before failing the checks; an exception preserves
its partial archive and failure report without retry.

Recompute every one of6435 uniform-top4 tie scalars using the fourth-largest
count threshold: vertices above it are forced, and tied vertices have a
uniform hypergeometric inclusion law. For boundary size b and remaining k,
single inclusion is k/b and two-boundary joint inclusion k(k-1)/(b(b-1)).
Crossing uses p_i+p_j-2p_ij. This does not enumerate the primary's70 subsets.
All scalar values must match exactly, including the nontrivial-280 fixture.

After all native checks pass, use the engine-checked exact integer weights
for all127 two-species convolutions. Encode occupations in base16 (four bits
per output), not base9; total8 prevents digit carries. Numeric mask pairs
mask=1..127 versus255^mask are a different complete unordered enumeration.
All exact means/gaps, full-B mean-767/327680, minimum and status must match
the immutable archive. Reconstruct all11083116 convolution terms. No LP,
replacement graph, new witness or optimized mean is introduced.

## Separate qualification and main authorization

First authorize ONE fresh qualification only:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P58_naive_replication.py --mode qualify --output research/P58_naive_qualification/run_001/data
```

Six stdlib guards: all-zero/unique/nontrivial ties, base16 no-carry, metadata
state count157183, and existing-output refusal. Five tiny API/math checks:
HOM CF zero, HOM bunch factorial, complex partial-source orientation, vacuum,
and the independently built eight-mode Gram. Qualification opens NO P58
reference file and evaluates NO P58 source probability, including no N8
amplitude. Native source order/complex convention are checked with at most
two photons. All eleven guards/checks are prospective until that run.

Only after ROOT reviews the actual qualification report/manifest may it
authorize ONE full run at the frozen separate command:

```text
/private/tmp/pbp-clean-venv-20261124/bin/python research/P58_naive_replication.py --mode full --output experiments/P58_naive_replication/run_001/data
```

Full mode requires the exact-source completed qualification report and its
v2 output/source hashes; no automatic chaining or authorization is implied.
Existing/historical outputs are rejected before backend import. No vendor
patch, unsupported nthreads argument, ancestry/chronology fiction or retry.

Official exqalibur.Config.compute_max_thread_count is set to1 and read back
before any permanent; it is read again after work. Thread metadata states
this documented maximum, not observed OS scheduling. Conventional thread
environment variables are also capped by the runner. No ps subprocess.
If MPLCONFIGDIR is absent, use the documented existing ROOT/.local/mplconfig
persistent config/cache; record it and make no cold/warm performance claim.

Both planned runs: CPU60/wall90/envthread1/output16MiB, planned logical
workspace128MiB. The full projection uses earlier P52's25k Naive checks as
engineering evidence only, not calibration for this157k run. Groupwise gzip
streaming avoids retaining every native float in RAM; all mathematical data
remain in the archive. Python/library/RSS overhead is observed, not a hard
Darwin memory/affinity guarantee. Preserve all failures and missing results.
Separate v2 contracts pin qualification's five inputs and full's eleven
inputs, including the future actual qualification manifest/report.

Outcome interpretation is limited to finite numerical source-engine
corroboration plus independently reconstructed exact ties/convolutions.
No physical random shots, arbitrary finer-species convexity, genuine-order8
witness, optimized balanced-cut advantage, matched hardware cost or QPU
capability is certified. Actual QPU calls and new physical draws are zero.
