# P107 degenerate-corner prediction: independent manual check

26 November 2026. **PROVED AS WRITTEN for the declared finite corner.**
ROOT-suggested prediction checked adversarially, not blind discovery or a run.
Exact target: research/P107_PRE_DATA_DEGENERATE_PREDICTION.md,55 lines,
commit4aed2332b4437cf98b6853d78bb528914132754b, SHA256
565d9fb4e904d7bcf0342c99f3661d835349dafaeffbd352efdf53de1a4e0153.
The whole source was read after that identity; original source is untouched.
Decoder identities: our98c76e34d228e8a70800b76e7b20e036f4a04906,
research/P107_DECODER_IDENTITIES_REVIEW.md102l, SHA256
9dca56e56c724b67493199f637094dfa59f17e2d12b1d01d93493735fbded9f9.

## Projector and void permanents

Write a=1/2,b=(1+i)/4,c=conjugate(b). The literal four-cycle matrix in the
target has T†=T,T^2=T,trace2: a rank-two physical signal contraction.
Use b*c=1/8,b^2=i/8,c^2=-i/8,b^4=c^4=-1/64. Four filled CF input ports
are retained; all lost/bunched/vacuum signal outcomes enter its PGF.

For opposite excluded ports, M=I-T†QT has diagonal3/4, opposite entries0,
and forward neighboring entries -b/2 (reverse conjugates). In its permanent,
the identity is81/256; the four single transpositions contribute9/128;
the two double transpositions contribute1/512. The two oriented four-cycles
contribute-1/512 and cancel the latter. Triple cycles vanish. Consequently

    O_B=99/256, O_D=81/256.

For adjacent excluded ports3,4, the diagonal is(7/8,7/8,5/8,5/8).
The upper off-diagonal entries in order12,13,14,23,24,34 are

    (0, i/8, -c/2, -b/2, -i/8, -b).

The diagonal product is1225/4096. The five nonzero single-transposition
numerators over4096 are35,70,70,35,392, totaling602. Double-transposition
terms give1+4=5. The two supported triangle pairs contribute-56 each,
and the surviving oriented four-cycle pair contributes4. Hence the extra
permanent numerator is602+5-112+4=499, and

    A_B=(1225+499)/4096=431/1024, A_D=1225/4096.

These are void probabilities INCLUDING vacuum/one-photon records, not
probabilities of exactly two clicks or conditional all-survival values.

## The two individual 2110 probabilities

For doubled port1 and opposite empty port3, the repeated-row amplitude is
2a^2(b^2+c^2)=0. For doubled1 and adjacent empty2 it is3b/8; the reflected
record has3c/8, explaining the conjugated representative in ROOT's note.
The input factorial is1 and the repeated output factorial is2, giving

    q_B,opp=0, q_B,adj=|3b/8|^2/2=9/1024.

For D put A=|a|^2=1/4,B=|b|^2=1/8. The repeated-row intensity permanents
are4A^2B^2+4B^4=5/1024 (opposite) and
2A^3B+6AB^3=7/1024 (adjacent). Divide by the SAME output factorial2:

    q_D,opp=5/2048, q_D,adj=7/2048.

These q values are for ONE occupation each, not class-summed probabilities;
all four source photons survive for these particular records, but other
records remain in the final means. There is no survival renormalization.

## Decoder means and exact scope

The independently proved four-port identities give, for either model,

    E_T=8/3+(4/3)(A-O),
    E_P=E_T+(4/3)(q_opp-q_adj).

Substitution yields the complete unconditioned prediction:

| Mean | B | D | B minus D |
|---|---|---|---|
| Threshold |2083/768|8121/3072|211/3072|
| PNR |1037/384|8117/3072|179/3072|

Both contrasts are positive, hence unfavorable to B for minimizing this cut.
The point(1,0) is the previously registered degenerate corner, not P101's
finite-b curve point or a new numerical case. The rank-one/simple-ground
surrogate cannot be substituted here. This verifies no sign over the square,
no b1 claim, reoptimized-control comparison, hard tail or cost advantage.
No imports/AST/symbolic or numerical execution/RNG/native/test/runner/raw-data/
QPU/manuscript/push occurred, and no fixtures/population were changed.
No prediction numbers were transmitted to the P107 source author.
