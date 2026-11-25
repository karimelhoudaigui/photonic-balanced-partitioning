# P47: claim-first independent review card

Frozen mathematical card, 2026-11-25, base
`a6d7a278654099ac970b2defb0e06c0896fd6a02`. No P47 code/raw exists and no
P47 numerical run is claimed. Do not consult the owner's companion note
before reconstructing these statements. This does not replace any P46
architecture or outcome. Please audit/refute the claims and factors below;
do not infer global novelty or optimization advantage from them.

Let D be the real inside-by-outside b-by-b single-swap cost table for a
balanced graph anchor, with D_ij=J(A-u_i+v_j)-J(A). Use the SAME indices
for W_ij; there is no extra transpose. Set Z=I-11*/b, R=ZDZ,
sigma=||R||_op and C=R/sigma when sigma>0. F is the normalized positive-sign
complex Fourier matrix. Define G=C odot F, nu=||G||_op,
c=max_ij|C_ij|, h=max(nu,c),

    epsilon=1/(4h), Y=polar(F-epsilon G) when h>0;
    Y=F for R=0 or h=0.

This is an ambient step followed by polar projection, not the replacement
polar(F-epsilon Pi_F(G)). Use the real Frobenius metric. No randomized
reference selection after outcomes or removal of degenerate cases is
allowed. The quarter-step epsilon=1/4 is a comparison lemma only.

Claims to reconstruct independently:

1. For s_C(W)=sum C_ij|W_ij|^2, tangent projection is
   Pi_F(G)=G-F sym(F*G), and the derivative of s_C(polar(F-epsilon G))
   at epsilon=0 is -2||Pi_F(G)||_F^2. For S_D the factor is sigma times this.
2. The input to polar has smallest singular value at least 3/4 at the
   specified step. The finite bound is
   s_C(Y)-s_C(F)<=-(1/epsilon-c)||Y-F||_F^2,
   including signed real C. The corresponding S_D bound has factor sigma.
3. Centering changes S_D by a W-independent constant on unitary matrices.
   The maximum-entry/norm normalization requires no favorable labels.
4. The safe ambient step is stationary iff Pi_F(G)=0. Nonzero C does not
   suffice for strict descent.
5. For normalized C and flat F, ||G||_F<=1. A fixed quarter-step has
   ||Y-F||_F<=1/2, independent of b. The adaptive step removes that
   automatic bound but establishes no extensive-response lower bound.
6. The adaptive step retains the bound
   ||Y-F||_op<=sqrt(2-2sqrt(15/16)); assess the hypotheses and density meaning.

Explicit exact graph/check case: b=4, old vertices 0,1,2,3, new 4,5,6,7;
v=(1,-1,1,-1) on both lists. Every edge within a list has weight 17/16;
old i to new j has weight 1+v_i v_j/8. Reconstruct the anchor cut, all
single-swap deltas, the cut of {0,2,4,6}, centered C and the polar step.
Check this case without classifying it from a numerical tolerance.

Finally determine whether any of the above gives more than descent of the
classical doubly stochastic routing proxy: compare its global optimum to
assignment, its relation to a simultaneous graph cut, its B/D first moments,
and what remains to test after a common PIT/completion decoder. No claim
of a bosonic gain, CF yield, search advantage or hardware calibration is
part of this card. A future pilot is not authorized by the existence of
this analytic checkpoint.
