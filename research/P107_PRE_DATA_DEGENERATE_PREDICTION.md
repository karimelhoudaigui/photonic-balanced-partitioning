# P107: manual predata prediction at the degenerate corner

26-Nov-2026, ROOT, before P107 freeze or any execution. This is an exact
manual prediction, not a run result; independent review is pending.
The point(1,0) is ALREADY in the registered25-point square grid, not a new
chosen experiment. It is not the finite b1 point of P101. No code change
or extra execution is requested by this note.

Set x1,y0 in T=Fdiag(1,x,xy,y)F†. In the declared Fourier convention,

    T=[[a,b,0,b*],[b*,a,b,0],[0,b*,a,b],[b,0,b*,a]],
    a=1/2, b=(1+i)/4.

It is a rank-two Hermitian projector, a physical contraction. Use P101's
known four-CF source, full signal law and two uniform-tie decoders. For
each model X, let A_X be probability that ALL signal photons lie in ONE
specified adjacent pair, and O_X the same for ONE opposite pair. Include
vacuum/one-photon outcomes in those void probabilities. Let q_adj/q_opp
be ONE2110 occupation with doubled/empty vertices adjacent/opposite.

Using M=I-T†Q T for the two excluded ports, direct four-by-four permanent
expansion minus its diagonal product gives the following rational predictions:

| Quantity | B | D |
|---|---|---|
| O |99/256|81/256|
| A |431/1024|1225/4096|
| q_opp |0|5/2048|
| q_adj |9/1024|7/2048|

Checks on the permanent calculation: for opposite excluded ports all four
diagonal entries of M are3/4, same-parity off-diagonals vanish, and adjacent
off-diagonals have modulus squared1/32. Pair-of-pair terms cancel the
four-cycle contribution; B-D=9/128. For adjacent excluded ports the diagonal
is(7/8,7/8,5/8,5/8), in an appropriate cyclic labeling. The B-D numerator
over4096 consists of pair terms602, pair-pair5, triples-112, cycle4, total499.

For q_opp the repeated-row permanent amplitude is zero; the labeled
permanent is5/1024 before dividing by occupation factorial2. For q_adj,
the B permanent is3conjugate(b)/8, so |per|²/2=9/1024; the D repeated-row
permanent is7/1024, again divided by2. These divisors are essential.

The independently reconstructed mean identities in
P107_DECODER_IDENTITIES_REVIEW.md then predict

    E_B C(D_T)=2083/768, E_D C(D_T)=8121/3072,
    E_B C(D_P)=1037/384, E_D C(D_P)=8117/3072,
    delta_T=211/3072, delta_P=179/3072.                     (1)

Thus both mean contrasts should be UNFAVORABLE to B at this corner, despite
being outside P101's simple-ground rank-one limit. This is not a sign proof
on the square, not a finite-b curve result, and not a control-cost theorem.
The literal prediction may be falsified by the independently coded P107
calculation; discrepancies must be diagnosed, not patched to match this note.
No P107 source/raw has been imported, evaluated or read to obtain it.
