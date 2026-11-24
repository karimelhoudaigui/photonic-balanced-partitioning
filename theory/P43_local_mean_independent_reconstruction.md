# P43 — independent reconstruction of two-mode occupation means

Analytic reconstruction, 2026-11-24, BEFORE reading any P43 encoding proof or
implementation. No numerical run is used. The critical derivation and its
qualification were first sent by message to the coordinator, then written here
for a committed freeze. This document does not modify P42 evidence.

## Claim card and verdict

Take K photons, one in each of K DISTINCT input modes alpha_1,...,alpha_K,
in a normalized, fully indiscernible spatial Fock state. Let U be a passive
spatial unitary, or its isometric selected-input-column matrix. Let i and j be
two DISTINCT output modes. All other modes are retained physically but their
counts are marginalized. There is no postselection. Then the exact two-mode
occupation law can be represented with polynomially many scalar arithmetic
operations in K, using the construction below.

**Verdict on the supplied card: correct only after stating these physical and
number-representation restrictions.** In particular, collision-free input
occupations alone do not imply full internal indistinguishability. The formula
is correct for coefficients of the factorial generating function, with the
factorial-moment convention distinguished below. Arithmetic complexity does
not by itself imply exact polynomial BIT complexity for arbitrary complex U.
No conclusion about optimization advantage or a full-law sampler follows.

## From normalized Fock states to a permanent

Write v_a=U|alpha_a>. These one-particle spatial states are orthonormal. The
normalized ordered K-particle source after U is

    |Psi> = 1/sqrt(K!) sum_(pi in S_K) v_(pi(1)) tensor ... tensor v_(pi(K)).

For D=I+x|i><i|+y|j><j|, its product action D tensorpower K multiplies an
occupation word by (1+x)^n_i(1+y)^n_j. Expansion of the normalized bra and ket
has K! equivalent relative permutations, giving

    G(x,y) = E[(1+x)^n_i(1+y)^n_j]
           = per(M(x,y)),
    M_ab   = delta_ab + x conj(U_i,alpha_a) U_i,alpha_b
                     + y conj(U_j,alpha_a) U_j,alpha_b.

Thus define a_i=(conj(U_i,alpha_a))_a as a COLUMN vector and similarly a_j;
then M=I+x a_i a_i^*+y a_j a_j^*. If instead a_i is the unconjugated row
transposed into a column, the displayed matrix is transposed. Transposing ALL
terms does preserve the permanent, but a mixed conjugation convention is not
justified. Here all definitions use the explicit M_ab above.

The edge cases matter: K=0 gives G=1; i=j would require D to contain
(x+y+xy)|i><i|, so the two-distinct-mode formula cannot be reused unchanged.
There is no constraint n_i+n_j=K unless these are the only possible outputs.
The valid general support is n_i,n_j>=0 and n_i+n_j<=K. In particular,
E[n_i]=sum_a |U_i,alpha_a|^2 and the means summed over all outputs equal K.

## Four-variable product and factorial conventions

Use four commuting formal variables s_1,s_2,t_1,t_2. Define

    Q = product_(a=1)^K [1 + (conj(U_i,alpha_a)s_1
                             +conj(U_j,alpha_a)s_2)
                            (U_i,alpha_a t_1+U_j,alpha_a t_2)],
    d_rs = [s_1^r s_2^s t_1^r t_2^s] Q.

Expand per(I+W) by the input subset T on which W is chosen. Within per(W_T),
choose which of its r+s factors use row i versus row j. The left coloring and
the right coloring must each contain r labels of type i and s of type j.
Each such pair of colorings is realized by exactly r!s! permutations matching
the two color classes. The product Q enumerates these pairs once each.
Consequently, for r+s<=K,

    A_rs := [x^r y^s]G = r!s! d_rs
         = E[binom(n_i,r) binom(n_j,s)],
    E[(n_i)_r (n_j)_s] = r!s! A_rs = (r!s!)^2 d_rs.

Here (n)_r is the falling factorial. Calling r!s!d_rs the RAW factorial moment
would therefore lose another factor r!s!. It is the correct GENERATING-FUNCTION
coefficient. A_00=1, G(0,0)=1. G(1,1) is not a normalization condition; it is
E[2^(n_i+n_j)]. The coefficients d_rs are nonnegative and real in exact
arithmetic: for a fixed T their contribution is the squared modulus of the
coefficient of z_1^r z_2^s in product_(a in T)(U_i,alpha_a z_1+U_j,alpha_a z_2).
That positivity does not remove cancellation within the amplitudes.

## Recovering the joint occupation probabilities

The ordinary probability generating function is H(z,w)=G(z-1,w-1). Hence

    P(n_i=p,n_j=q)
      = sum_(r>=p,s>=q,r+s<=K)
          (-1)^(r+s-p-q) binom(r,p) binom(s,q) A_rs.

It is an alternating binomial inversion, not an evaluation at positive
arguments. In exact physical arithmetic the probabilities are real,
nonnegative, sum to H(1,1)=G(0,0)=1, and vanish for p+q>K.

Manual normalization/factor test, with no numerical run: for two identical
photons on the balanced Rx splitter, the full law is half at (2,0), half at
(0,2). Thus G=1+x+y+(x^2+y^2)/2. For either individual output d_20=1/4,
A_20=2!*d_20=1/2, and E[(n_i)_2]=2!*A_20=1. The mixed coefficient A_11=0;
the complex splitter phases must cancel there. K=1 instead gives
G=1+q_i x+q_j y and P(0,0)=1-q_i-q_j, so the vacuum of this two-mode marginal
must not be dropped even though the global photon number is fixed.

## Complexity and representation of U

A dense grid with each of four exponents bounded by K uses O(K^4) scalar
states. Updating by each of K factors, each with five monomials, takes
O(K^5) scalar arithmetic operations. Extracting diagonals and naive binomial
inversion are polynomial as well. These are valid upper bounds.

A stronger count is available, without being needed for that conclusion:
every reachable monomial has total s-degree equal to total t-degree, ell.
At fixed ell there are (ell+1)^2 exponent choices. Up to degree K this is
sum_(ell=0)^K(ell+1)^2=O(K^3) states, and processing all factors is O(K^4)
arithmetic operations using that sparsity. Neither statement bounds the cost
of an arbitrary scalar operation for free.

For exact rational real and imaginary parts of the selected entries of U,
with at most b bits per component, an exact polynomial BIT algorithm follows.
Clear a common denominator separately for the bounded number of coefficients
of each input-column factor. The accumulated denominator has O(Kb) bits.
Numerators have polynomial bit length: sums of at most 5^K bounded-size
products add O(K) bits, and factorial multipliers add O(K log K) bits.
Binomial inversion preserves a polynomial bit-length bound. Exact rational
arithmetic therefore costs poly(K,b), not just polynomially many oracle calls.
Graph/penalty coefficients need their own controlled bit lengths too.

For a fixed algebraic number field with an effective polynomial-cost arithmetic
representation, an analogous qualified statement is possible. An arbitrary
compact circuit specification does NOT automatically supply such a field:
degrees of fields generated by its algebraic entries can grow, and arbitrary
real or transcendental entries need an explicit oracle or approximation model.
There is no exact finite bit algorithm for unspecified arbitrary complex U.
An exact arithmetic-expression circuit of polynomial size is also not by itself
a polynomial-cost sign/comparison procedure. Complexity is polynomial in K,
not a claim of polynomial complexity in log K.

## Precision and numerical stability

Float64 evaluation is not an exact implementation of this theorem. Complex
coefficient updates may cancel, and recovering probabilities requires alternating
sums. If each coefficient A_rs has absolute error at most epsilon, the error
in probability (p,q), even before subsequent summation roundoff, is bounded by

    epsilon sum_(r>=p,s>=q,r+s<=K) binom(r,p)binom(s,q)
      = epsilon binom(K+2,p+q+2).

The identity follows from the product of the two binomial generating series
and one cumulative-sum factor. Its worst value can grow exponentially in K.
This is an upper error bound, not a lower bound on every instance's condition
number; coefficient errors from the actual DP can be correlated. It suffices
to show that fixed-precision stability cannot be inferred from arithmetic
complexity. Tiny or exactly zero probabilities additionally preclude a uniform
relative-error claim. Input-entry errors and DP rounding require their own
bounds. Rigorous intervals, exact rational arithmetic, or explicit precision
analysis are needed for a numerical certificate. Clipping/renormalizing a
floating result does not certify the original result.

## Physical scope falsifiers

Fully distinguishable internal labels already refute extending the rank-two
permanent to arbitrary internal states. For two orthogonal internal photons
and a balanced splitter,

    G_D=(1+(x+y)/2)^2,

whose xy coefficient is1/2, whereas the identical-photon G above has xy
coefficient0. For pure PRODUCT internal states with Gram S, the correct
normalized CF expression is instead

    per((I+x a_i a_i^*+y a_j a_j^*) Hadamard S).

Since S_aa=1, its constant matrix is still I, but the two updates generally
have rank depending on S, not rank one. This does not assert hardness of that
generalization; the fully distinguishable limit itself is easily tractable.

Likewise, repeated spatial inputs cannot simply be substituted as repeated
columns in I plus the same update. Two photons in one input mode routed
deterministically to i physically give G=(1+x)^2. The invalid substitution
I_2+x J_2 gives permanent1+2x+2x^2. A general repeated-column permanent uses
the source Gram matrix and its normalization rather than an identity constant.
This is a counterexample to that substitution, not an impossibility theorem
for other bunched-source dynamic programs.

## Local means versus global search

For an UNCONDITIONAL objective written as a polynomial-size sum of functions
of one or two mode counts, these local laws suffice to evaluate its expectation.
Threshold click indicators and a quadratic penalty on the number of clicks
also expand into one/two-mode terms. Their tabulated values must themselves be
efficiently computable in the chosen number model. Repeating over O(m^2) pairs
gives a polynomial arithmetic evaluation of such a mean, subject to all the
physical/representation/precision restrictions above.

This does not supply a sample from the full joint occupation law, exact support
conditioning on a global feasibility event, or a polynomial optimizer over U.
It says nothing about the computational cost of globally minimizing that mean,
the chance of measuring an optimum, adaptive final-best-cost domination, or
quantum advantage. A globally conditioned mean requires a separately analyzed
numerator and denominator; unconditioned local marginals do not furnish them.
No P42 budget/search corollary is imported into this different assertion.

## Pending author comparison and provenance

No P43 author proof, implementation or numerical raw was read before this
freeze. Request its exact revision/hash only after committing this file; a
subsequent comparison must preserve this reconstruction and record its own
target separately. This is a card audit and derivation, not an external-source
novelty review. No novelty, hardware or global optimization obstruction is
claimed. No numeric experiment, QPU, source mutation or P42 input/raw change
was performed for this reconstruction.
