# P95 independent dissipative-filter proof audit

Reviewer `/root/p66_dark_audit`, 2026-11-26; `proof-audit` workflow.
Primary verdict: **PROVED AS WRITTEN** for (1)–(8), with their explicitly
fixed-channel, full-raw-PNR, bounded-decoder and arithmetic/resource scope.
No favorable optimization sign or efficient classical dominance is established.

Exact source: `research/P95_DISSIPATIVE_FILTER_DISCRIMINATOR.md`, all 128 lines,
commit `f145aca1994856ec065bfc83ad144852f34612fa`, SHA256
`67a75774988f992df286b3f40965273907a98532f7040b45528cff2c1ad18fe3`.
This is an independent reconstruction of the frozen author's proof, not an
acceptance of another reviewer's conclusion. No P90a data was opened.

## Typed claim and dependency obligations

L is fixed Hermitian PSD, beta>=0, T=exp(-beta L/2), and A has K distinct
singly occupied modes, vacuum elsewhere. B is identical bosons; D has independent
orthogonal product internal labels, all experiencing exactly the same T.
Species are independent across groups and indistinguishable within each group.
The observed complete signal counts n determine total lost ell=K-|n|.
f(n,ell) is bounded real, fixed independently of beta and common to every control.
No survival-conditioned probability or resolved dump/time record is substituted.

Dependency graph: vacuum dilation/normalized Fock contractions -> (1) ->
matrix Taylor expansion/nonidentity permutation support -> (2)–(5);
pure-loss semigroup/Jordan decomposition -> trace remainder -> (6);
centering a self-loop decoder -> (7); CF amplitude minimal routing order -> (8).
Obligations (1)–(8), group2 counterexample and the stated finite frontiers passed.
External priority, device realization, measured runtime, efficient replacement,
independent reoptimization and positive optimization acceptance are out of scope.
No external theorem or computational output is a load-bearing leaf here.

## Full raw PGF and coefficients through degree three

Dilate occupied input columns to V=[T[:,A];E_A], E_A^dagger E_A=I-(T^2)[A,A].
They are orthonormal, so their K distinct creation operators produce a normalized
input image. Weight signal modes by z_a and every environment mode by v.
The weighted Fock inner product is the permanent of
V^dagger diag(Z,vI) V = [T(Z-vI)T+vI][A,A].
This proves (1), including output PNR normalization; no extra K! factor occurs.
Independent labels multiply the individual diagonal factors; species multiply
principal-block permanents. Every monomial has total degree K in (z,v).
At z_a=v=1 the compressed matrix is I, so each raw PGF normalizes to one.
The choice of E_A cannot alter this aggregate-loss PGF. Resolving individual
dump modes or loss times would require additional physical data and a new proof.

Writing D0=Z-vI, direct multiplication gives
T D0 T=D0-beta(LD0+D0L)/2
 +beta^2[(L^2D0+D0L^2)/8+LD0L/4]+O(beta^3).
Thus a_ij=L_ij[v-(z_i+z_j)/2] and
b_ij=sum_a L_ia L_aj(z_i+z_j+2z_a-4v)/8, exactly as stated.
In the diagonal product, the first derivative replaces one z_i by
L_ii(v-z_i). All nonidentity permutations move at least two indices.
This proves (2): only a one-loss atom and the unchanged-state decrement appear
at first order in PNR. It is not a claim about arbitrary coherent measurements
or individual environmental channels before aggregation.

A transposition ij contributes beta^2 |L_ij|^2 h_ij^2 z_(A\{i,j}).
Here h_ij^2=v^2-vz_i-vz_j+z_i^2/4+z_i z_j/2+z_j^2/4.
Its six terms give exactly the two-loss, two negative one-loss, two directed
bunch and unchanged atoms in (3). Coefficients sum to zero; positive mass=2,
negative mass=2. Across pairs no positive atom is a negative atom: the total
lost count separates loss sectors, and collisions differ from unchanged CF.
Shared one-loss atoms have the same negative sign. Consequently the leading
TV coefficient is indeed 2 sum_(i<j)|L_ij|^2, not half that value.
The finite count domain permits an O(beta^3) remainder in this TV expansion.
f=1_(ell=2) and its complement give opposite quadratic signs, with no graph
optimization implication. Fixed magnitudes/diagonals remove phase dependence
from this order. Describing this stencil as collisions alone would be false.

At order three, a transposition contributes (a_ij b_ji+b_ij a_ji)z_rest
plus |L_ij|^2 h_ij^2 times one diagonal spectator a_kk z_remaining.
Since conjugation acts on coefficients, not the formal variables, the first
term equals 2h_ij Re(L_ji b_ij)z_rest. A three-cycle and its reverse give
2Re(L_ij L_jk L_ki)h_ij h_jk h_ki z_rest. No other moved-index pattern can
contribute at degree three. Identity terms cancel against G_D. These are all
three lines of (4), proving (5) as a signed coefficient functional, not a law.

## Species countercontrol and magnetic-flux attribution

At quadratic order a species partition keeps precisely its intra-species pairs.
Groups<=2 select a matching; mixtures yield inclusion probabilities p_ij with
sum_(j!=i)p_ij<=1 (necessary, not the complete matching-polytope description).
For K=m=3 and L=3I-J, L is PSD because x^dagger Lx=3||x||^2-|sum x_i|^2>=0.
All three pair magnitudes squared are one, so full B-D on 1_(ell=2) has
coefficient three. A matching has at most one edge, hence any same-channel
group2 mixture has coefficient at most one. For irregular beta-dependent
weights, the precise statement is the uniform upper bound beta^2+O(beta^3),
or limsup coefficient<=1; differentiability of those weights is unnecessary.
This does not refute independently optimized L, beta, grouping or resource costs.
Summing pair corrections with signed weights is not a normalized experiment.

The genuine three-cycle needs three occupied sources in one species. In contrast
the pair-propagation correction contains Re(L_ji L_ia L_aj) even when a is empty.
Thus cubic flux dependence alone does not identify three-source interference.
For a magnetic Laplacian the product has the three off-diagonal minus signs
and a cosine of triangle flux; flux reversal gives no odd-flux term here.
With triangle-free off-diagonal support, only a=i,j diagonal/magnitude terms
remain in this coefficient. These phase-blindness claims require holding the
other matrix entries' magnitudes/diagonals fixed; they do not cover a compiler
that changes them while varying phases, nor higher-order/finite-beta effects.

## Remainder: valid trace-norm domain and constant

In loss eigenmodes, jump operators J_alpha=sqrt(lambda_alpha)c_alpha give
R=sum J_alpha^dagger J_alpha=dGamma(L)<=K lambda I, lambda=||L||op.
Vacuum attenuation composes by multiplication of T, hence gives the CPTP
semigroup with generator J(X)-{R,X}/2 on the finite <=K-photon space.
For Hermitian X, its Jordan decomposition gives
||J(X)||_1 <= tr(R|X|)<=K lambda ||X||_1;
the anticommutator half has norm at most K lambda ||X||_1.
Thus ||mathcal L(X)||_1<=2K lambda||X||_1. Iterates stay Hermitian.
CPTP maps contract this norm on Hermitian inputs by the same Jordan argument.
The integral remainder after degree p is
integral_0^beta (beta-s)^p/p! exp(s mathcal L) mathcal L^(p+1)(rho) ds,
whose norm is <=(2K lambda beta)^(p+1)/(p+1)! for normalized rho.
No exponential multiplier is needed because the remaining channel contracts.
Each remainder has trace zero, so centering the measured effect changes nothing.

B, D and species may be embedded in one finite internal-label Fock space
(at most K colors when K>=1), with one-particle loss matrix L tensor I_color.
The norm bound remains K lambda, independent of color dimension. Equivalently
one may bound each state's remainder in its own space and add scalar errors.
Use the label-blind diagonal effect F=f(n,K-|n|), centered at its range midpoint:
||F_centered||op<=R_f/2. Each state contributes at most R_f/2 times its trace
remainder, so the B-D sum gives exactly R_f times the above bound, proving (6).
General Hermitian effects admit this remainder inequality, but (2)–(5)'s PNR
cancellations/stencils must not be carried over to arbitrary coherent effects.
The result is unconditional in signal PNR plus total loss; no contraction claim
for a retained environment/time trajectory was invoked. A small measured mean
transmission is not a certificate of lambda or of an actual device channel.

## Self-loops, complete CF frontiers and acceptance order

Under the specified policy, center f at f0. Every monomial of P2 vanishes under
this functional. In P3 the spectator and genuine three-source lines use only
occupied-mode variables: they give unchanged CF, collisions or loss, all zero.
The same holds for pair propagation through a in A. For a outside A, the
z_a part of 2h_ij Re(L_ji b_ij) is
Re(L_ji L_ia L_aj)[v z_a/2-z_i z_a/4-z_j z_a/4].
The loss term is a self-loop. The two remaining CF atoms are exactly i->a
and j->a, proving the minus sign and factor 1/4 in (7).
This is a physical-one-replacement frontier, a graph one-swap only for direct
m=2K vertex occupation. A nonlinear decoder may map it to a larger graph move.

For complete CF target A' with r removed/replacement modes, no photons are lost,
and its raw amplitude is per(T[A',A]). Every new output row needs an off-diagonal
entry, hence at least r powers of beta. At exactly r powers every shared row
must keep its own input; the remaining r rows/columns give
(-beta/2)^r per(L[Y,R]). CF factorials are one. Squaring proves B's (8);
adding independent route probabilities gives D's per(|L[Y,R]|^2), with the same
4^-r factor. A zero permanent means a zero leading coefficient, not success.
r=0 uses the empty permanent one. There is no survival denominator.
If strict acceptance has no improving decoded member of the one-replacement
frontier, its delta f vanish. Improvement can then occur only at r>=2 and has
raw order at least beta^4; it need not have any nonzero coefficient at that order.
At r=2 its leading interference is still two-source exchange. A basin-changing
quench invalidates the no-improving-member premise unless evaluated in delta f.

The quadratic record count 1+K+3 binom(K,2), cubic O(K^2 m+K^3) term count,
and fixed-r frontier binom(K,r)binom(m-K,r) are valid upper/enumeration bounds.
Every actual decode, score, randomized-decoder average and quench must be paid;
an averaged value is not a discovered partition. Frontier dominance is only
available when that actual work fits. No timed dominance or useful sign follows.
beta=0,L=0,K=0 give zero difference; K=1 has B=D at every beta.
The finite-strength optimization implication remains open. No computation,
import/AST, RNG, native/test/runner call, delegation, paper or QPU action occurred.
