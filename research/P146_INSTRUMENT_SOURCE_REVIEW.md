# P146 — Independent implementation review of the full mediator check

27-Nov-2026. Static, non-author CODE review; audited, NOT EXECUTED.
Reviewer authored P146-A mathematics with shared ROOT proposals. This is
therefore not an independent replication of that mathematical derivation.
Only this report is added; frozen A and every prior source/result remain.

Initial target: ROOT `research/P146_full_instrument_check.py`, ALL 370 lines,
SHA256 `1285dbed35bcceef24ed44a593ae0e07e397ce90d2e575e24d4de4d47361a311`.
Final target: SAME path, ALL 410 lines, compared with that full initial text,
commit `65114fc998fbb1ee99ae6d1d88e3810bfd794939`, SHA256
`6653116e8aa39b7bde7db8c7bf1642ba3b8777bd07808713a7c34b91c93ee567`.
Also FULL read at that commit: P146_EXPERIMENT_CARD.md100 lines and
P146_instrument_contract.json60 lines; run_authorized remains false.
Dependencies: P146-A c0b950c079e3146fc5128da7b72f4fb1c6d5c4d3, 311 lines;
mathbox computation-audit and its implementation checklist read/applied.
No import, AST, evaluation, test, numerical/native/RNG/QPU execution or raw
payload reading performed. This report supplies no launch authorization.

## 1. Finite assertion and manually reconstructed implementation

The claim tested prospectively is a finite instrument/resource qualification,
not graph optimization. The exact optical domain is three unit-circle phases
`1,i,(3+4i)/5` crossed with three rational survival/loss amplitude pairs.
Only `i` is subsequently compared with local Perceval, for all three losses.

`G` performs exact Q(i) arithmetic, not floating normalization. The dilation is
`[[s H,-l H],[l I,s I]]`, with s^2+l^2=1 and the stated H4 unitary. Its occupied
first four columns implement attenuation BEFORE the analyzer; the environment
rails retain the original encoded bit. The full 8-column Gram is checked.

There are C(9,2)=36 two-photon occupations, including zeros and bunching.
For input rails `2x,1+2y`, the two assignment amplitudes are added coherently.
Their squared modulus is divided by2 exactly for a repeated output row;
computational source occupations are distinct, so no input factorial is missing.
The explicit two-detection formulas, the two suppressed coincidences, one-
detection environment labels and vacuum label projectors reconstruct correctly.
For z=i each nonzero two-detection record has probability s^4/8, independent
of the memory bits. At z=1 each nonzero cross record has rank2, not a unitary.

Fully D iterates all 8^2=64 ORDERED tag destinations, including j=k ONCE.
It uses one product Kraus per assignment, without bosonic sqrt2 enhancement;
coarse-graining traces tags/environment incoherently, keeping all 15 detected
PNR records. The determinant test of the 2x2 logical-amplitude array correctly
checks factorization. Its product |++> output has normalized total trace.
The partial transpose is `rho[xv,uy]`; all 15 nonempty principal minors are
checked. The B normalized Bell-equivalent branch has PT determinant -1/16.
These are resource witnesses, not an optimization score or a retuned-D trial.

## 2. Purge and capped resource identities

The purge fixture retains three sites of a known five-site weighted cycle.
It covers loss in either native CZ, before/after a temporary wrong-sign phase,
every fine loss occupation and all eight measured ancilla/endpoint bitstrings.
After conditioning these bits, loss amplitudes, unfinished uv phases and the
completed first CZ are scalars on the remaining sites. The cross-product
comparison correctly tests proportionality, retaining the known neighbor
rotations explicitly. Zero-probability branches are included and vacuous.
This does not repair arbitrary unknown data, nor test a whole feedback run.
The non-diagonal H-center parity example correctly illustrates the exclusion.

The two Y outcomes of the ancilla parity gadget have equal norms; the omitted
common 1/sqrt2 is stated. Dyadic success after k-1 wrong signs, and the local
terminal pi/2 correction, are checked for every terminating history m<=8.
Those angle checks are FLOATING with tolerance1e-12, not exact pi arithmetic.

Native stopping probabilities are success p^j, loss p^(j-1)(1-tau), timeout
p^R, where p=tau/2. Their exact normalization and mean give the stated r_R,c_R.
Two-CZ stage recursion is `S<-a(1+S)/2`, `C<-c(1+r)+a*C/2`, a=r_R^2.
It agrees with the closed forms, including m=1 and eta=1 with finite caps.
The degree3 drift calculation preserves a nonpositive delta as a reported
outcome. The general recovery/drift theorem is a mathematical dependency,
not established by these finite recursion comparisons or the one purge fixture.

## 3. Coverage, provenance and remaining pre-execution findings

Nominal optical raw: 9*36=324 B records and 9*64=576 D records.
Native: 3*4*36=432 amplitudes, all environment outputs, z=i ONLY.
Nine final-version optics_input records bring nominal raw records to1341.
D PPT tests9*15*15=2025 principal minors; nominal checks38.
Purge cases26*2*2*8=832; dyadic histories sum(m+1,m=1..8)=44;
capped resource contexts3*2*3=18. No hidden graph, seed or favorable filter.
Native compares independently evaluated Naive amplitudes against this same
source's analytic dilation; it is no separate verification of emitter physics.

Two concrete failure-diagnostic deficiencies were sent to ROOT before any run:

1. Exact B branch append follows its assertions; a failing branch and its
   expected operand are absent from the saved prefix. The Gram assertions
   likewise precede any matrix/context record. AssertionError often has no
   message. The missing operands/context were a pre-execution deficiency.
2. In finally, an encoded-size excess raises BEFORE writing any of the three
   files. Thus that cap path loses records, checks AND failure diagnostics.
   Missing scientific output must never be interpreted as a negative result.

Both are CORRECTED in the final SHA, before any execution. Input V is retained
before Gram checks; B/D raw append precedes checks. Gram, fine branches, loss
masses, PPT, witness, purge, ancilla and resource calculations supply failure
context plus traceback. The cap fallback writes explicitly truncated first-
record/first-check prefixes and a bounded failure receipt, THEN raises. This
is an incomplete failed output, never a complete law or scientific rejection.
No physical formula, population, tolerance or predicate was relaxed. Native
handling remains unchanged. Initial and final identities are distinguished
here; no claim that the uncommitted initial draft was a separate Git artifact.

Native nonfinite actual/expected/error values are preserved as repr strings
with a finite flag BEFORE assertion; thread readback follows every point.
The source itself sets no CPU/wall/FSIZE/environment limits: ROOT's separate
contract/runner must establish those before imports and preserve logs,
statuses, input hashes and any partial/absent outputs. A completed source run
also requires its declared output files and independently checked manifest.
Read card/contract agree on CPU90s/wall120s, one worker/thread, logs1MiB,
science3MiB, zero failed retries, 432 native points and fresh declared outputs.
The inactive contract names both pending independent reviews as inputs.

Disposition for FINAL SHA: STATIC IMPLEMENTATION REVIEW ACCEPTED in this finite
domain, with the external-runner and independent-math-review conditions above;
not executed, computationally qualified or authorized here. No residual
material implementation blocker identified by this reading.
No optimizer advantage, held-out replication, Lucy capability, recovery of
unknown data or superiority over the identical per-attempt group2 is implied.
