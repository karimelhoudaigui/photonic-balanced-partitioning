# P52 proposed independent finite probability cross-check (STATIC ONLY)

2026-11-25. Proposal prepared during primary qualification. No project or
scientific import, executable implementation, numerical timing, amplitude
calculation or hardware call was performed. Only installed source/metadata
were read. This document is NOT a run contract or execution authorization:
ROOT must freeze the actual reference inputs, implementation/criteria and
bounded-run card, then explicitly release the slot after P52 main is sealed.
Physics analysis of the primary result takes priority when it arrives.

## Representation and installed API

Target: ALL6435 occupations at r=N8, for ALL four original theta cells,
including the duplicate calibration cell and zero-amplitude patterns.
Use Perceval NaiveBackend's individual normalized permanent amplitudes,
not SLOS, a creation recurrence or an imported primary P52 function.

Installed metadata reports perceval-quandela1.3.0 and exqalibur1.4.2 in
/private/tmp/pbp-clean-venv-20261124. Static source confirms the public chain:
construct NaiveBackend; set_circuit(Unitary(U)); set_input_state with
FockState([1]*8); request prob_amplitude on each FockState occupation.
Unitary accepts a numeric ndarray and returns its matrix without phase
canonicalization. The backend uses U[output,input], constructing an8x8
matrix with output rows repeated by occupations. It returns

    permanent_cx(U_repeated)/sqrt(prod_i n_i! prod_a s_a!).

Here input factorials equal1. This normalization/orientation can be compared
directly with the primary complex amplitudes, without fitting a global phase.
The wrapper calls the native permanent_cx entry point, not its explicitly
separate Gurvits estimator. The compiled internal permanent algorithm was
NOT inspected; do not assert Ryser/Glynn or interval exactness from this read.

IMPORTANT: do not use prob_iterator (default min_p drops outcomes), masks,
prob_distribution with possible sparse conventions, or a CF-only iterator.
Call prob_amplitude ONCE per occupation and derive probability as abs².
Calling probability again repeats the permanent: Naive does not cache.

## Independent inputs, coverage and comparisons

After actual primary files are sealed, pin their manifest/source hashes,
geometry and four theta NPZs read-only. Reconstruct U independently from
the declared Walsh sign/phase formula and compare with archived U. For the
probability-engine check use the archived numeric U, preserving identical
matrix inputs while separating algorithms. Do not import primary code.

Enumerate occupations independently, e.g. from sorted output-mode multisets,
and align by the resulting eight-count TUPLE. Never assume the library and
primary enumeration orders agree. Assert6435 unique nonnegative tuples of
total8 and exact coverage equality. Save all Naive amplitudes/probabilities;
report maximum complex-amplitude error, maximum probability error, full
L1/TV difference, both masses and worst-state tuples for every cell. Include
zeros with absolute errors; do not discard small probabilities or use unstable
relative errors at suppressed events.

ROOT should freeze numerical tolerances before data comparison, with no
outcome-driven relaxation. These are float64/complex128 checks, not intervals.
A failure, timeout or incomplete phase/state coverage remains preserved and
INCONCLUSIVE for a full-law replication; no favorable subset or automatic
fallback/retry. The reviewer has previously read primary code and proposed
nulls, so this is algorithm/representation independence, NOT author blindness.

## Cost projection, not a benchmark

There are25,740 permanent calls of size8, plus four matrix setups and state
construction/validation. The known Python submatrix wrapper fills64 entries
per call. Native algorithm/speed is not inferred from that count. CPU20s,
wall30s, one worker/native-thread target and output4MiB are plausible bounds
to TEST, not demonstrated feasibility. Cold imports, input hashing/loading,
all calculations and finalization must be inside the run accounting.

Saving complex amplitudes and probabilities for all calls uses617,760 raw
bytes; common int16 occupations add102,960 bytes. Even retaining corresponding
reference amplitudes/probabilities and scalar diagnostics projects below2MiB
numeric payload. Do not copy the large b4 arrays into the output. Input NPZs
can be hashed/read lazily for needed keys. No MC draws, graphs, fitting,
tuning, optimizer or new P52 target is involved.

The runner must enforce the agreed thread environment. Native permanent
threading is not proved by the Python wrapper; establish its serial behavior
or supported control in the authorized qualification before claiming the
one-thread condition. No unverified new native option should be invented.

## Installed-source provenance

Read-only SHA256 values, site-packages paths relative to the above venv:

| File | SHA256 |
|---|---|
| perceval/backends/_naive.py | aaa26604b0866eeba61aaca80e83afe4df689711f4ce3bf965db1da74314ef4d |
| perceval/backends/_abstract_backends.py | 53f7c4db865c2e643b9ab461da0c71b2fbb9dc1a450ad917936ca0f4e25538f1 |
| perceval/components/unitary_components.py | 2f4bacd1d3d5c919b32eaaf28d1881a5f49be608ffca4be2ee53886a149786df |
| perceval/utils/states.py | 3913d2c6e6529b2edc23a1bfaede67432a0ac2042f98824813497d84ed97fbf9 |
| exqalibur/exqalibur.cpython-311-darwin.so | b4687bc81b37cb447eb0c9c4fa89523da7feed8584a31ca74798ac3bcee06749 |

Actual commands: rg/file listing, sed/cat of installed sources and METADATA,
shasum, and a bounded strings search of the native binary (which did not
establish a threading interface). No import or API call was made. This would
validate a FINITE physical probability calculation only, not held-out optimizer
performance, scalability, hardware compatibility or the unresolved positive goal.
