# P96 ROOT static review before qualification or native execution

Reviewed original code freezeac67650ceaa2bf7639ed72ef6fddb28a02067749,
ROOT integration97eb7c0: all5 files/550 lines, source346/tests100/static
contract37/preflight24/population43. No source import, AST parse, test
collection, matrix construction, RNG, exact calculation or native call
was used for this review. Independent source review is still pending.

Source SHA3a9e92668bd573b8397a457eaa46923246c2d26a4a83685362a764f477291fe0;
tests148770d282d3365677d3748c5e250f8f96531051726aab23d633edf09e32c3b8.
The exact169-line theory and157-line proof review were already fully read.
All8 project inputs and8 critical external pins were checked by streamed
SHA256. Metadata and nine literal test names are in
P96_validation_review/predata_metadata.json; future binding/outputs absent.
One overescaped regex in an initial metadata scanner failed before output
creation and was corrected; this was not a scientific import or trial.

## Reconstructed objects and population

The rational polynomial expansion implements per(I+T^t(Z-I)T), independently
of the moment-based q formula. It initializes every occupation of0..K,
retaining exact zeros despite sparse intermediate multiplication. At K0
the empty permutation gives vacuum1. Fixture trace<=1 proves physical
contraction even for the explicit outside-domain negative-q counterexample.
The bunch factor1/2, first/second moments and exact TV/tail/factorial bounds
are consistent with the proof. q is never clipped or renormalized.

ROOT checked every hand table and reconstructed162 valid+5 outside bins,
13 fixed cases, five native cases/159 full outcomes/28 signal marginals.
Nine pure tests include explicit tables rather than only formula restatement.
The tests load only the stdlib source and do not call native-bearing methods.
No conftest or project autoload introduces a native dependency into this
qualification; third-party pytest plugin autoload is explicitly disabled.

The native Halmos block has columns K+m and rows m+K; occupied FIRST K
inputs and observed FIRST m outputs are correct even for rectangular T.
Both full Gram residuals are checked, no eigenvalue clipping is allowed,
and all full-K Fock occupations are enumerated. Environment aggregation is
unconditional. The installed pinned Naive source was read: n0 explicitly
returns a1-by-1 ones submatrix, so its vacuum amplitude is defined. All
states including zeros are evaluated individually, without sparse cutoff.
Binary64/Naive comparisons have absolute1e-11 and relative0 tolerances.
This finite evidence will cover real rational fixtures, not all complex T.

## Resources, provenance and pending gates

Main sets hard/soft FSIZE8MiB/CPU60 before scientific imports. Exact cases
precede native imports. Environment1 is set before exqalibur, its initial
config is recorded, then set1 before NumPy/Perceval/native computation.
Every attempted point has before/after readbacks, including finally after
exceptions. This is configuration evidence, not OS thread/RSS measurement.
Eight preimport pins and actual critical loaded identities are recorded;
all inputs/external pins are rechecked after success. Transitive modules
are not claimed fully authenticated.

Three scientific files have aggregate8MiB guard and128KiB final reserve;
runner logs separately4MiB. Output data must be exclusive under a fresh
run parent. Failures preserve prefixes and never imply retry permission.
Preflight is a different pure9-test command with FSIZE512KiB before pytest,
CPU30/wall60. Main needs its later immutable8-input/actual-theory binding
and separate authorization; neither static contract is changed after qual.

No material static blocker found by ROOT. This is NOT execution authority.
Independent full review must be read before a separate qualification
authorization. Raw seal precedes interpretation, then a separate receipt;
only later may ROOT bind/authorize one native main. Full existing tests
must pass before publishing new code. No positive graph result, theorem
by tests, novelty, calibrated Lucy transmission or QPU gate follows.
