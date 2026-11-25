# P64 independent static implementation review

2026-11-25, initial review at19:48 UTC, followed by the pre-qualification delta
review below. **Primary verdict: proved as written for the ideal-arithmetic
construction.** The corrected rounded candidate has no remaining static blocker
to its declared capped qualification. The initial reference-coverage gap was
corrected before any P64 execution. Numerical assertions remain unexecuted;
no N18 precision or cost certificate is supplied. No module, test, numerical
computation, phase/count draw, graph, calibration or QPU operation was executed
for this review.

## Exact revision and normalized claim

Audited base commit: `bff4a48bcfdc0e4639dc8ba66ee210b864733f0d`.
All377 source lines, all234 test lines, the complete implementation contract,
JSON qualification contract and P64 proof were read. Author files are unchanged.

| Artifact | SHA256 |
| --- | --- |
| `research/P64_structured_sampler.py` | `68055f83ead4f54303b90933ed5ebb5940a548a19cb72f496da374ad2e25780d` |
| `tests/test_p64_structured_sampler.py` | `23e48812d95f01f391ccb793e29f4b52ae8100df0edfb2908933ef8cd5f3e35b` |
| `research/P64_IMPLEMENTATION_CONTRACT.md` | `c95a2156639fceda1b6495a0f44cc31e5eff5d1c69ae6acd36bfbaa607d867d6` |
| `research/P64_qualification_contract.json` | `8e60d18e3debc2576cb1062ab29974bbd6cbfa3131e087f6c93600fc2efef86f` |
| `theory/P64_fixed_phase_complete_structured_sampler.md` | `9e29d7818c709d4c6814ef8735ca3bb4e7a17bbfa932b270229d7c3dcf997b3c` |

The mathematical target is the complete ideal fixed-Theta PNR law of
`V(F3 tensor I6)D_Theta(I3 tensor F6)` on input1^18, including collisions.
The implemented domains are d6/N18 and the d2/N6 qualification analogue.
Source/tritter polynomial coefficients are exact integer pairs; phases,
amplitudes, conditioning and categorical CDFs use rounded arithmetic.
No actual nonzero F6 support cardinality, N18 TV bound or runtime is assumed.

Dependencies, all internal: normalized Fock creation convention -> Fourier
source expansion -> exact source integer law -> joint color-total law;
colorwise factorization -> coarse-M coherent conditioning -> suffix Born
probabilities/projection -> full PNR law in ideal arithmetic. Source residue
and ordered-pair reconstruction give the finite width bound. The numerical
implementation additionally depends on its frozen guards and unexecuted
qualification. There is no unchecked external theorem or observed result leaf.

## Passed mathematical and implementation obligations

| Obligation | Static finding |
| --- | --- |
| Z[xi], lines24-57 | Passed: xi^2=xi-1, the six powers, product and norm u^2+uv+v^2 agree with xi=exp(pi imaginary_unit/3) |
| Source, lines136-156 | Passed: polynomial c_n yields A(n)=c_n sqrt(prod(n!)/d^d); exact weight prod(n!) norm(c_n), denominator d^d, hence6^6 at d6 |
| Source zeros / sampling, lines149-173 | Passed: all occupations are retained in rows, zero removal is exact, support<=80 is an upper bound, integer CDF has total d^d; three independent rows supply ONLY M |
| Mixed tritter, lines176-231 | Passed: the mixed raw matrix divided by5 sqrt(3) equals V0 F3; squared scale75 is required |
| Bunched normalization | Passed: coefficient c_o gives amplitude c_o sqrt(prod(o!)/(scale^T prod(x!))); both normalized-Fock factorials are present |
| Coherent reconstruction, lines261-287 | Passed: ordered first/second rows determine the third, and the transposed complete key is injective, so assignment never drops a duplicate amplitude; all compatible phases are restored |
| Conditional norm | Passed in ideal arithmetic: exact P(M)=integer_mass/(d^d)^3; rounded mass is checked relatively, then its square root normalizes the candidate state explicitly |
| Local law, lines289-320 | Passed: inputs with the SAME suffix add coherently; distinct suffixes contribute squared magnitudes because their remaining normalized Fock kets are orthogonal |
| Projection, lines322-333 | Passed: one amplitude per suffix, divided by sqrt(selected raw mass); measured local input removed, with no residual source-row-sum constraint |
| Full output ranges | Passed: cache inputs remain within0..d, while outputs enumerate every composition of their total; outputs above6 are retained |
| Cache / width scope | Passed as combinatorial guards: no S^3 table, no suffix-by-output matrix, initial width<=6400 and lazy entries<=2*7^3*190; no hard Python RSS claim follows |
| Exact small reference formula | Passed: independent dense positive-Fourier six-mode factorization and full six-input Ryser formula, repeated output rows and output factorial denominator |
| Floating precision / measured cost | Conditional: mass guards and finite N6 comparison do not certify arbitrary N18 branches, phase points, adaptive paths or cold/warm resource cost |

In particular, for x=(6,6,6), output(18,0,0) is present. Its mixed polynomial
coefficient is37^6 and its exact Born probability is
`18!*37^12/(75^18*(6!)^3)`. Without V the corresponding probability is
`18!/(3^18*(6!)^3)`. These are analytic expressions, not evaluated data.

Sampling M is legitimate because the final colorwise unitaries preserve its
joint projectors and each final PNR output belongs to one unique M sector.
Discarding latent rows followed by full coherent reconstruction implements
that coarse measurement. The subsequent sums retain interference between
compatible source configurations; this is the unaveraged fixed-Theta law.
After projection, different local inputs can contribute to one suffix, whose
source-row residual totals need not be fixed. The source imposes no false
row-sum-six restriction at that stage.

## Concrete reference-coverage gap at the audited revision

`draw_probabilities()` lines106-112 computes s=fsum(weights), checks it near1,
then samples CDF entries divided by s. However `complete_small_law()` lines369-375
recurses with `probability*p`, using RAW local masses. Thus the reference test
lines158-167 checks a rounded Born recursion, whereas sample() uses the
explicitly normalized categorical kernel. A tolerated s different from1 is
enough for those two recursions to differ. An asserted full-law tolerance for
one recursion cannot be assigned unchanged to the other without accounting
for that difference. The finite-bit RNG quantile adds a further separate
approximation, already acknowledged by the author.

ROOT accepted a minimal pre-qualification correction during this review:
at every enumerator node compute s=fsum(probs), then multiply by p/s, matching
the normalized real-probability kernel of the rounded masses. ROOT also
requested archival of all4*462 candidate and independent-reference
probabilities, maximum errors and normalization receipts. The exact delta
reviewed below closes this specific gap. Finite-bit quantiles and rounded
CDF boundaries still contribute numerical approximation; no literal discrete
PRNG-output law or N18 TV certificate is claimed by the corrected contract.

The N6 reference itself has the correct full-input permanent formula and
all462 outcomes at four prospectively fixed phases. It targets the d2
analogue, while the separate462-row exact source table is F6 for the N18
construction. Neither is a full N18-PNR enumeration or a proof of N18 TV
accuracy. Rounded cancellation zeros and within-tolerance normalization must
remain described as numerical approximations, without a true-zero claim.

## Exact pre-qualification delta reviewed

Final audited author revision:
`677348b7d3988183971350d195cf056cd87251a5`, preserving bff4a48 in history.
The complete four-file diff from bff4a48 was read without executing it.

| Corrected artifact | SHA256 |
| --- | --- |
| Source | `af2b016b9ce5dd71919a8745d21c7e7f363a1588a089f697770a29d5b9353543` |
| Tests | `0c53c31dfa3276dc4d7fef0c7dff29636bdf7801b3ce95c5d7dfea978644993d` |
| Implementation contract | `e79a24eeac96be25cc42df4fad77bc8df92144dc38c34016a71464b428d695b9` |
| JSON qualification contract | `eb43a24900cc12d4766e72dd082fb24148f6a1ea3053b2994171216b11261860` |

The scientific source delta is confined to the small-law enumerator's
`categorical_mass=fsum(probs)` and branch multiplier `p/categorical_mass`.
The source, tritter, coherent reconstruction, projection and guards are
unchanged. local_distribution already checks the mass before that division.
The pre-qualification provenance change e151573 supplies exclusive phase_0
through phase_3 artifacts, each with all462 actual/reference rows, norms,
max error, half-L1 error and the phase's float/hex representation, before
comparison assertions. A shared fresh session directory and exclusive file
creation prevent replacement. The complete source table remains separate.

The contract's six planned result paths match the six --result paths in its
bounded command: junit.xml, source_table.json and four fixed phase files,
all below the fresh runner parent. The unchanged eight input paths match
the listed execution closure. No calibration, new phase, seed or tolerance
was added. This exact delta is acceptable for the declared capped synthetic
qualification; ROOT retains execution authorization and the one-worker slot.

## Provenance, checks and remaining gate

Independent same-team review, with shared task context and the author's raw
proof/code available; not blind external replication. A separate isolated
subagent independently reconstructed only the exact coefficient/Fock layer
and reported agreement. That agreement is supporting review provenance,
not numerical evidence. Skills applied: proof-audit/computation-audit, then
proofread-math on this report only. The read-only git/hash/text inspections
and this single report write/commit are the whole executed scope.

ROOT's corrected isolation was honored: this report is in
`.local/p64-static-review`, branch `research/p64-static-review`, based on
the audited P64 commit. No P63 file/branch or P64 author source was modified.
Existing tests were not run; the repository test gate remains for ROOT's
authorized numerical worker. Both the original candidate and the exact
correction were reviewed statically; no successful qualification is represented.
No remaining blocking law/factorial/coherence error was found in the audited
scope. Complete fixed-Theta equality remains an ideal-arithmetic statement;
precision and paid full-resource comparison are the research-use obligations.
