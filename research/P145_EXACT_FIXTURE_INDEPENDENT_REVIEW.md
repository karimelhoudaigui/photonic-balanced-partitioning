# P145 — independent exact-fixture review

26-Nov-2026. **Primary mathematical verdict: proved as written for this designed diagnostic.**
Code outcome: **audited, not executed; STATIC PASS for the final bytes below.**
A genuine restricted-family interference/envelope contrast is defeated by a simple
classical move. It is not a graph-optimization advantage or a random-instance result.

## A. Exact target and coverage

FULL source read: `research/P145_exact_triad_fixture.py`,188 lines, SHA256
`77189d7d145bcb8ef4fbd77cb790ad1ca333f52f5deab03c517c174fcb3817da`.
FULL card read: `research/P145_EXPERIMENT_CARD.md`,99 lines, SHA256
`3161275a6b4487380f30c18234fcf3cd038446aadd9fe64831a51fa81eaa8bf3`.
The pending52-line contract was also text-read, SHA256
`f7e6bea684a49a70f4357ecb29d09470b4bd38c4319d21f84f0afd68df977554`.
At review, ROOT HEAD `5c36e24` still contained the older186-line source;
this verdict binds the188-line CONTENT HASH, not that older Git blob.
Any execution freeze must contain the exact reviewed bytes and separate authority.

The graph, transfer, color measurement and decoder were reconstructed BEFORE using
the expected polynomial assertions. No P66 draft implementation or P94 analysis
was read for sections A–F; this is not an independent numerical replication.

## B. The actual graph and strict one-swap trap — passed

S=0..2,T=3..5 are unit cliques; A=6..8,D=9..11 are weight3 cliques.
Three weight3 edges join T to vertex6. At X=S union A only those edges cross,
so C(X)=9. With A'=A minus {6}, the complete36 global swap deltas are:

| Removed / added | Number | C(new)-9 |
|---|---:|---:|
| S / T |9|1|
| S / D |9|8|
| A' / T |6|5|
| {6} / T |3|2|
| A' / D |6|12|
| {6} / D |3|3|

All are strictly positive. For any receiver3-subset with r vertices from T,
the S/T clique cut is 2r(3-r), and the star cut is 9-3r. Thus
`C(A union Y)-9=3r-2r^2`: gains for r=0,1,2,3 are 0,0,2,9.
The20 candidates have multiplicities 1,9,9,1. A is fixed classical background,
not an independently prepared optical candidate.

## C. Physical law, factorials and color buckets — passed

Let `F[j,a]=omega^(ja)/sqrt(3)`, omega^2+omega+1=0. Fourier orthogonality gives
F^dagger F=I, so V=[sqrt(1-p)I;-i sqrt(p)F] is an occupied-column isometry.
For example it completes to the passive unitary with blocks
`[[cI,-is F^dagger],[-is F,cI]]`, c=sqrt(1-p),s=sqrt(p).
No signal loss or postselection is needed for this diagnostic family.

An output occupation n repeats each row n_j times. Every surviving permutation
has common factor `c^(3-r)*(-is)^r/3^(r/2)`; an inside row j forces its source to j.
The remaining Fourier phase is exactly the exponent used in `coefficient`.
For orthogonal species, sum amplitudes coherently only for the SAME tuple of
colors at the ordered output slots; sum different tuples incoherently.
If a bucket has counts n0,n1,n2, its sum is a+b*omega with
a=n0-n2,b=n1-n2, hence abs-square `a^2-a*b+b^2`. Division by
`3^r*product_j n_j!` is correct, including repeated-output bins and all five profiles.

The recursion visits all C(8,3)=56 nonnegative occupations, not only the20 CF bins.
Every collision has zero gain; impossible and zero-probability bins remain.
The basis is the UN-SCALED `p^r(1-p)^(3-r)`, not the binomial-normalized Bernstein
basis. The total outside count is Bin(3,p): split each source into its two paths
first, then apply the outside Fourier unitary, which preserves outside number.
Therefore the four normalization coefficients are C(3,r), for every profile.
This independently proves the normalization assertion rather than assuming it.

## D. Utility polynomials and exact continuous envelopes — passed

Only r=2,3 contribute. For r=2, the remaining inside row fixes its input;
each distinct2x2 Fourier permanent has abs-square1/9, versus2/9 for D.
For a pair profile, one surviving-input choice leaves the coherent pair outside
and two leave distinguishable crossers. Summing the nine CF outputs gives:

| Profile | CF coefficient r=2 | CF coefficient r=3 | Utility polynomial |
|---|---:|---:|---|
| B |1|1/3|2p^2+p^3|
| D |2|2/9|4p^2-2p^3|
| each pair |5/3|1/9|(10p^2-7p^3)/3|

At r=3, per(F)=-1/sqrt(3); the D value is6/27, and the pair value is
three choices of its distinct photon times(1/3)(1/9)=1/9. Multiplying by
gains2 and9 and expanding (1-p) gives the displayed polynomials.
Consequently `I3=JB-J12-J13-J23+2JD=4p^3` exactly.
This subtraction isolates three-cycle terms of B versus species ablations;
it is distinct from P142's opposite-triad-phase comparison at fixed pair moduli.

B and D increase on[0,1], reaching3 and2 at p=1. The pair derivative is
`p(20-21p)/3`, giving maximum4000/3969 at20/21. The final code genuinely
checks endpoints and the rational stationary root of each cubic, then compares
the maxima with expectations; it no longer merely prints hardcoded maxima.

## E. Strong countercontrols and interpretation — passed

The deterministic feasible proposal Y=T yields C(A union T)=0 and gain9.
It needs only the public receiver block and current/candidate scoring, not C*.
All20 scores are already evaluated/credited, so the classical frontier is solved.
An unrestricted distinguishable passive PERMUTATION sending S inputs to T also
achieves gain9. It is outside the fixed-Fourier one-parameter envelope, which is
why the word RESTRICTED matters. Preserve the genuine B/group contrast without
promoting that restricted comparison to independent optimization over all circuits.

## F. Implementation, corrected failure handling and limits

Only stdlib is imported; neither a P66 implementation, quantum API nor optimizer
is called. Fraction arithmetic and elementary integer phase counts are exact.
The original147-line source lost all scientific arrays on an assertion failure;
the final wrapper now writes available records, graph/profile checks, summary
and failure before rethrowing. The failing candidate is appended before its guard.
An explicit `not __debug__` refusal inside try/finally prevents optimized Python
from silently stripping the mathematical checks. Normalization and utility
operands and computed maxima are retained before their comparison guards.

Fresh output is required; a normal result has280 probability records plus graph
checks and four JSON files. Exceptions remain nonzero. Traceback is retained by
outer stderr, not as a JSON traceback field. A write error or hard kill can still
prevent complete finals; a printed PASS alone is not sufficient execution evidence.
The pending contract's1MiB scientific figure is explicitly a PLAN; outer CPU10/
wall20, logs1MiB, one thread and zero retries require a separately frozen runner.
This static review neither runs that command nor asserts resource completion.
The24-vertex prospective screen is NOT validated here: its final block-selection
rule, implementation, qualification and execution authority remain separate.
No program/import/AST, RNG, matrix evaluation, raw-result read, test, native call,
QPU use or source/card/contract edit occurred. Only this review was written.
