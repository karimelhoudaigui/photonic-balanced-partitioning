# P137 — A uniform weak-reflection domination candidate

2026-11-26. Manual derivation of ROOT's conjecture; parent de6fd0209c1351df74e3ac2a5265495d0322fa9f.
PROOF CANDIDATE pending ROOT and non-author review. No novelty claim.
No code/import/AST, graph/matrix evaluation, RNG, native/QPU, raw read or paper edit.

## Statement with an explicit window

Let 2<=K<=4, m>=K+1, E embed C^K as the first K receiver coordinates,
R={0,...,K-1}, and H=H^dagger in C^(m-by-m), ||H||op<=1.
Assume a supplied d>0 satisfies |H_ja|>=d for EVERY j outside R and a in R.
The norm assumption implies d<=1; consistency also forces (m-K)d^2<=1.
Use the rational-reflection family

    F_x=(I+i*x*H)E, B=E^dagger H^2 E, A_x=(I+x^2*B/2)^-1,
    T_x=2F_x(I+F_x^dagger F_x)^-1=(E+i*x*HE)A_x.         (1)

For these CF source photons, fully indistinguishable B and distinguishable D
share this physical family, receiver labels and CF/otherwise-hold-R decoder.
For a receiver K-set Y, define raw p_B(Y;x)=|per(T_x[Y,:])|^2 and
p_D(Y;x)=per(|T_x[Y,:]|^2); no survival normalization is allowed.
Set

    kappa0(K,d)=d^(2K)/[2*K*K!*(2*4^K+K!)].             (2)

Its denominators for K=2,3,4 are respectively 272,4824,102912.
The candidate theorem is: for EVERY Y!=R and 0<kappa<kappa0,

    p_D(Y;2*kappa)-p_B(Y;kappa)
       >= (3/2)*d^(2K)*kappa^(2s) >0, s=|Y\R|.         (3)

If not enough outside rows exist for some s, there simply is no such Y.
The bound is independent of receiver dimension except through supplied d.
The window is deliberately conservative, not a practical crossover prediction.

## Physical admissibility and dimension-free entry bounds

Since H is Hermitian, F_x^dagger F_x=I+x^2 B and 0<=B<=I.
Thus 0<A_x<=I and ||A_x-I||<=x^2/2. Directly,

    I-T_x^dagger T_x=(x^4/4)*A_x B^2 A_x >=0.          (4)

Every T_x is therefore a contraction and its reflection supplies a passive
unitary dilation. In particular the D setting 2*kappa is genuinely admissible;
it is not an unphysical scalar rescaling of T_kappa. The reflection's dump
transfer is -x^2*B*A_x/2 before the occupied-column sign, with norm<=x^2/2.
For these CF inputs the mean number of dump photons is<=K*x^4/4,
so dump probability is also<=K*x^4/4, without independent-loss assumptions.
All dump and collisional outcomes still count as paid hold attempts.

For x in (0,1], scale each outside row of T_x[Y,:] by 1/x, leaving rows
inside R unchanged; call the resulting K-by-K matrix M_x. Its limit M_0
has inside rows e_i^dagger and outside rows i*H_j,R. Every entry of BOTH
M_x and M_0 has modulus<=1: use ||T_x||<=1 on inside rows and
T_x[j,:]/x=i*(HEA_x)[j,:], ||HEA_x||<=1, on outside rows.

For inside rows, (T_x-E)=E(A_x-I)+i*x*HEA_x gives entry error<=x+x^2/2.
For outside rows, M_x-M_0=i*HE(A_x-I) gives error<=x^2/2.
Consequently ALL entry errors are<=3x/2. These are uniform operator-derived
bounds; summing m entries, bounding individual graph coefficients or using
a floating small-entry threshold is unnecessary.

## Permanent remainder and the leading factorial comparison

Elementary lemma: if two K-by-K matrices have entries of modulus<=1 and
entrywise difference<=e, each product in their permanents differs by<=K*e
by product telescoping. Summing K! terms gives permanent error<=K!*K*e.
Since each permanent has modulus<=K!, its squared-modulus error is
<=2*(K!)*permanent_error. This lemma permits complex phases and zeros.

Put J=Y\R, C=R\Y, |J|=|C|=s>=1, and

    L=per(|H[J,C]|^2) >= s!*d^(2s).

In M_0, all unchanged inside rows force their own columns. Therefore
per(M_0)=i^s*per(H[J,C]); no sum over missing-source choices is omitted.
Cauchy-Schwarz on its s! terms gives |per(H[J,C])|^2<=s!*L.
The elementary lemma at x=kappa yields

    p_B(Y;kappa)/kappa^(2s) <= s!*L+3*K*(K!)^2*kappa. (5)

For D define N_x=|M_x|^2 entrywise, N_0=|M_0|^2. Both have entries in[0,1],
and ||N_x-N_0||max<=2*||M_x-M_0||max<=3x.
Thus |per(N_x)-per(N_0)|<=3*K*K!*x, with per(N_0)=L.
Exactly p_D(Y;x)=x^(2s)*per(N_x), so at x=2*kappa,

    p_D(Y;2*kappa)/kappa^(2s) >=4^s*(L-6*K*K!*kappa). (6)

Both estimates hold because 2*kappa<1 in (2). Subtraction gives the explicit
non-asymptotic bound

    (p_D(Y;2*kappa)-p_B(Y;kappa))/kappa^(2s)
      >=(4^s-s!)*L-3*K*K!*(2*4^s+K!)*kappa.           (7)

For s=1,2,3,4, the positive factors 4^s-s! are 3,14,58,232.
With d<=1, the leading term is>=3*d^(2K). The error term is bounded by
3*K*K!*(2*4^K+K!)*kappa, which is<3*d^(2K)/2 by (2).
This proves (3), including its explicit margin, without an unspecified Taylor
remainder or dependence on m. It also covers a vanishing complex permanent:
L remains positive, so destructive B interference cannot invalidate the bound.

## Optimization consequence and essential qualifications

Let h(R)=0 and every h(Y)>=0, with all non-CF outcomes also assigned zero.
Summing (3) against h gives E_D,2kappa[h]>=E_B,kappa[h], strictly if at least
one alternative has positive utility. No C*, optimal-state mask or partition
oracle is used: the inequality holds simultaneously for ALL these utilities.
More generally, every positive utility threshold has at least as much D mass.
This is a one-attempt fixed-incumbent obstruction; any IID repetition transfer
requires its own declared stopping/acceptance rule, not adaptive extrapolation.

The comparator family must ALLOW 2*kappa. This does not automatically refute
a finite grid omitting that point, the beta-dependent P133 family in general,
or any sparse/finite-strength/hardware protocol. Both arms use K injected
photons per modeled attempt. Different synthesis, preparation, calibration,
wall-time, detector loss or internal-tag costs are not matched by this proof.
No external attenuation is undone, and no empirical positive result is claimed.

The dense floor is essential to the STRICT statement and its uniform gap:
take H=diag(0,...,0,1) supported on an outside mode. Then F_x=E,T_x=E;
every Y!=R has both probabilities zero, for every x. This violates d>0 and
disproves the strict conclusion without that premise. It does NOT disprove
weaker non-strict dominance or establish what happens for a fixed sparse H.
If d tends to zero across a family, the certified window here tends to zero;
no d-independent or all-strength claim is licensed by the estimate.

Status: an explicit proposed weak-rational-reflection obstruction, suitable
for independent proof review. It is not P99 by citation, P109 attenuation
domination, a universal photonic no-go, a simulation result or a QPU gate.
Only this source was written; all existing negative/validated data are intact.
