# P43 — exact echo symmetry, derived before numerical outcomes

Status: analytic implementation check; no simulation or optimization result.
This does not change the 8-tuple allocation frozen at commit
`1811ad7a45b69fa3a08121d7a417e091474d9fed`.

Use the definitions of `P43_adaptive_phase_gradient_echo.md`. Let
R=P-Q, diagonal with +1 on the fixed source S0 and -1 elsewhere. Since the
normalized generators are real, diagonal/block-structured as specified,

    R H_cross R = -H_cross,
    R H_intra R = H_intra,
    R D R = D.

Write W_gamma=exp(-i gamma H_intra) exp(-i beta H_cross). Entrywise complex
conjugation then gives

    conjugate(W_gamma) = R W_(-gamma) R,
    conjugate(U_(alpha,beta,gamma)) = R U_(-alpha,beta,-gamma) R.

Multiplication of input/output modes by diagonal phases and entrywise complex
conjugation do not alter Fock transition probabilities. For a fixed input
occupation, they multiply each output amplitude by a phase or conjugate it;
the output probability is its squared modulus. Therefore

    Law_B(alpha,beta,gamma) = Law_B(-alpha,beta,-gamma).

The equality also holds for D because its routing probabilities are squared
matrix moduli. It holds for b4 species separately and hence their convolution.
For the phase-field control, source/output sign phases and conjugation preserve
the distribution because its independent phase alphabet {1,-1,i,-i} is invariant
under conjugation and sign changes. The weights and elementary-symmetric subset
law are consequently equal in distribution.

In particular, at gamma=0 the two alpha signs give EXACTLY the same occupation
law for every model in the pilot. The 8 tuples contain at most 6 distinct laws:
two gamma-zero alpha pairs duplicate laws, one pair at each beta. Preserve their
preallocated independent draws as internal replication; do not retrospectively
spend them elsewhere. Different finite sample estimates are expected, and a
noisy selection among equivalent tuples is not evidence of an alpha mechanism.

The root implementation can check the matrix conjugation/sign identity directly
at gamma=0 without enumerating occupations. This is separate from alpha-zero
identity and graph-relabel covariance. It remains necessary to validate the
sampler itself by an independently implemented small-size reference. None of
these algebraic checks replaces that validation or establishes optimization.
