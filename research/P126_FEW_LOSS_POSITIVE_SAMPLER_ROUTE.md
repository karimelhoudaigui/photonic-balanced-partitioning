# P126: fixed-few-loss positive-transfer sampler candidate

2026-11-26. ROOT proposed the sector/Rayleigh route; this is manual
reconstruction, falsification and a non-oracular completion, not independent
discovery. No P123 moving source/outcomes were read. One file only; no code,
imports/AST, numerical/symbolic program, RNG, native/QPU call or paper edit.
The count identities are derived below. An efficient implementation is
CONDITIONAL on the weighted nonnegative rational permanent/matching and
finite-bit primitives being independently authenticated; no novelty claim.

## 1. Model and the environmental Gram matrix

Let A>=0 be rational m-by-K with G=A^T A<=I. Start with K distinct CF input
photons and vacuum environment. Observe every signal occupation n with
K-r0<=|n|<=K, where r0 is a FIXED constant, and aggregate larger loss as FAIL.
Use r in {0,...,min(r0,K)}, N=K-r and D_r=binom(K,r). Collisions remain.
The actual contraction/source promise is essential; unknown preparation,
detector effects or a matrix approximation require their own error model.

Choose any environmental transfer E with E^dagger E=H=I-G. Such an isometry
(A;E) exists; no irrational square root must be constructed by the sampler.
Expanding the K transformed creation operators chooses a surviving source
subset S of size N and its lost complement Sbar of size r. For fixed n,
its signal amplitude is a_S(n)/sqrt(n!), a_S=per(A_(n,S)). The remaining
environmental vector is the creation product of columns E_i, i in Sbar.
Its inner product with the vector for Tbar is per(H_(Tbar,Sbar)). H is real
symmetric, so the complete sector probability is exactly

    p_N(n)=a(n)^T L_r a(n)/n!,
    L_r[S,T]=per(H_(Sbar,Tbar)).                         (1)

There is no extra r!, N! or binom(K,r) prefactor. Source subset states are
normalized CF states. Their environment norms already include every lost
output bunching pattern. Normalized CF matrix elements of Gamma_r(H) are
exactly these permanents. Thus L_r is its compression (up to complement
indexing), and 0<=H<=I implies

    0<=L_r<=I.                                         (2)

For r=0 this is the scalar one. Negative off-diagonal entries of H or L_r
are NOT probabilities and must not be removed. Each L entry is an exact
SIGNED r-by-r permanent; D_r^2 r! arithmetic is polynomial only for fixed
r0. All rational cancellation is retained; no FPRAS on signed H is assumed.

## 2. A positive proposal and exact rejection identity

Define q_N(n)=sum_S a_S(n)^2/n!, Q_N=sum_S per(G_(S,S)). Applying the
full-survival identity separately to A_S proves sum_n q_N(n)=Q_N. Equation
(2) gives 0<=p_N(n)<=q_N(n). To sample q_N/Q_N, choose S with weight
per(G_(S,S)) and use P125's CONDITIONAL positive-transfer sampler on A_S.
Do not repeat an unconditioned A_S optical/count sampler until it survives;
that would introduce an uncontrolled inverse-small-survival cost.

On q_N(n)>0, accept the proposed n with rational probability

    R_N(n)=a^T L_r a/(a^T a),  0<=R_N(n)<=1.             (3)

Then one trial's accepted mass is p_N(n)/Q_N and its total acceptance is
P_N/Q_N, P_N=sum_n p_N(n). Repetition gives p_N/P_N if P_N>0. For zero
proposal density define acceptance zero. This exact rejection identity by
itself is NOT an efficient algorithm: P_N can be zero or arbitrarily rare.
The next sections bound work without testing true P_N against an oracle.

## 3. Sector masses from top binomial moments

The full signal-number PGF is

    F(z)=per(H+zG)=per(I+(z-1)G)
        =sum_(l=0..K) M_l (z-1)^l,
    M_l=sum_(|S|=l) per(G_(S,S))=E binom(N_signal,l).

One derivation weights each signal creation amplitude by sqrt(z), for z>=0:
the resulting norm has Gram H+zG, while its number expansion is the PGF.
Expansion of per(I+tG) fixes all identity-selected rows/columns, leaving
precisely the principal permanents. Equality as polynomials then gives

    Q_N=M_N<=D_r,
    P_N=sum_(l=N..K)(-1)^(l-N)binom(l,N)M_l.             (4)

The inverse is signed; relative accuracy of moments does not give relative
accuracy of a rare P_N. But each principal permanent lies in [0,1], since
A_S is a contraction with a normalized CF input. If all their estimates
have relative error <=theta, the absolute error of the reconstructed P_N
is at most theta B_r, where

    B_r=sum_(l=N..K)binom(l,N)binom(K,l)=2^r binom(K,r).

The last identity chooses N vertices first and then any extra subset among
the remaining r. Only subsets missing at most r0 sources occur: there are
sum_(r<=min(r0,K)) D_r polynomially many. The queried matrices are weighted
NONNEGATIVE rational Gram minors, not necessarily zero/one matrices.

## 4. Non-oracular sector selection and paid rare-sector omission

Let s=min(r0,K)+1, desired raw TV error epsilon in (0,1), and choose
tau=epsilon/(8s), Delta=epsilon/(16s). Use a fixed relative precision
theta<=Delta/max_r B_r and per-query failure budgets whose union is <=beta0.
On the joint good precomputation event, every rational mass estimate e_r
obeys |e_r-P_(K-r)|<=Delta. Define the GOOD-EVENT lower bounds

    l_r=max(0,e_r-Delta),
    w_r=l_r if l_r>=tau, otherwise w_r=0.

On that event 0<=w_r<=P_(K-r), hence sum w_r<=1. Select one retained sector
with mass w_r and FAIL with remaining mass 1-sum w_r. This requires only
rational comparisons/categorical choices, not knowing the true mass.
If precomputed weights exceed one or leave a retained sector with no usable
proposal mass, use a declared FAIL fallback; this cannot occur on the good
precomputation event and costs at most beta0 in TV. Later primitive failures
are separately charged in (7). All estimates/fallbacks remain visible.

For a dropped sector, P_(K-r)<tau+2Delta; for a retained sector its omitted
mass is at most 2Delta. Therefore the TOTAL raw mass moved to FAIL is

    sum_r(P_(K-r)-w_r)<=s tau+2s Delta=epsilon/4.         (5)

A retained sector has P_N>=tau and Q_N<=D_r. The ideal rejection acceptance
is consequently >=tau/D_r, without ever computing their ratio as an oracle.
QN itself can exceed one; it is a proposal normalizer, not a physical yield.

## 5. Rayleigh approximation without relative cancellation error

For a true proposal, a!=0. Suppose every nonnegative amplitude estimate
has |hat_a_S-a_S|<=delta a_S, delta<1, with true zeros estimated as zero.
Then ||hat_a-a||<=delta||a||. Normalize u=a/||a|| and v=hat_a/||hat_a||;
triangle/reverse-triangle inequalities give ||v-u||<=2delta. With (2),

    |v^T L_r v-u^T L_r u|<=2||v-u||<=4delta.             (6)

This is ADDITIVE even if the numerator cancels to zero. It never demands
a relative approximation to a signed permanent or to p_N. The computed
Rayleigh quotient uses only exact rational arithmetic in L and hat_a;
it lies in [0,1] whenever hat_a!=0. If all estimates vanish use acceptance
zero. A nonzero true a then implies a primitive bad event, explicitly paid.
No clipping of an invalid physical L or assumption of positive L entries
repairs a violated contraction premise.

Each amplitude permanent is a NONNEGATIVE repeated-row matrix A_(n,S),
so a weighted permanent FPRAS is the only counting primitive requested.
With failure probability b per amplitude, union over D_r estimates adds
at most D_r b to a trial's acceptance-kernel TV. The guarantee must hold
uniformly for adaptively selected n, using fresh oracle randomness. Zero
behavior/support handling is part of the still-conditional primitive.

The same principal estimates used for (4) give the subset-mixture weights:
on the good precomputation event their normalized categorical TV error is
<=theta/(1-theta). P125 conditional-sampler error eta, the error (6), and
finite categorical/Bernoulli errors xi give a total trial-kernel bound

    e_trial<=theta/(1-theta)+eta+4delta+D_r b+xi.        (7)

QN=0 implies p_N=0 and the sector is absent on a good event. Principal
Gram mass is zero exactly when S contains a zero column of A. Exclude these
subsets by that exact test before calling P125; if estimated remaining
weights vanish, return FAIL. All unusable branches are total, never retries.

## 6. Finite caps and one explicit global error budget

For every retained r choose
J_r=ceil(D_r/tau)*ceil(log2(1/zeta)). The ideal iid proposal/rejection loop
aborts after J_r trials with probability <=exp(-J_r tau/D_r)<=zeta.
The first accepted output, when present, has the correct sector law; map
an abort to FAIL. This is a charged simulator approximation, not a newly
free physical loss event. Coupling each trial kernel until the first error
gives total sector error <=zeta+J_r e_trial, with no hidden 1/P_N factor.

Let Jmax=max J_r and set beta0=zeta=epsilon/8. Choose e_trial<=epsilon/(8Jmax)
and the sector-selection categorical error <=epsilon/8. These choices give

    raw TV<=beta0+epsilon/4+zeta+max_r J_r e_trial+epsilon/8
          <=3epsilon/4 < epsilon.                     (8)

For example also require theta<=epsilon/(80Jmax), eta<=epsilon/(40Jmax),
delta<=epsilon/(160Jmax), b<=epsilon/(40Jmax max_r D_r),
xi<=epsilon/(40Jmax). Since theta<1/2, each of the five terms in (7) is
<=epsilon/(40Jmax). Allocate beta0 across the polynomially many principal
queries. Subsequent bad events are handled in (7), NOT by conditioning
the final output on a global event of successful estimators. Thresholding
uses only good-event lower bounds, not exact knowledge of rare P_N.

For fixed r0, Dmax and max B_r are polynomial in K, and Jmax is polynomial
in K and 1/epsilon. All requested accuracies/failure budgets therefore have
polynomial inverse/bit length. Conditional on verified weighted rational
FPRAS/P125 primitives with polynomial output bits/runtime, exact signed
r-by-r permanent evaluation and all rational Rayleigh operations remain
polynomial. Only D_r amplitudes of ONE proposed n are queried; no enumeration
of the exponentially large signal-occupation space is used.
Finite-bit categorical cutoffs can be included in eta/xi and
the selector budget. Gram/normalizer construction and every rejected trial
are computational work, not free preprocessing or fewer physical photons.
No measured runtime or hardware implementation is asserted.

## 7. Hand falsifiers, endpoints and exact scope

For m=1,K=2,A=[1/2,1/2], G has entries 1/4 and H diagonal3/4/off-diagonal-1/4.
At N=2, p2=per(A_n)^2/2!=1/8. At N=1, a=(1/2,1/2) and
a^T H a=1/4: retaining only diagonal environment terms would incorrectly
give 3/8. At N=0, a=1 and per(H)=9/16+1/16=5/8. Thus
(P2,P1,P0)=(1/8,1/4,5/8), summing to one. Moments M2=1/8,M1=1/2,M0=1
give the same inversion: P1=M1-2M2, P0=M0-M1+M2.

ROOT also suggested the reused rank-one fixture A=J2/2, norm one. Here
G=J2/2 and H=I-G has diagonal 1/2/off-diagonal -1/2. For EACH N=1
signal outcome, a=(1/2,1/2), so a^T H a=0 although Q1=Tr(G)=1.
The sector law is (P0,P1,P2)=(1/2,0,1/2); independent input-survival coins
of probability 1/2 would incorrectly predict P1=1/2. This is an exact
environmental-coherence cancellation, not an optional negative correction.
The lower-bound selector gives zero weight to that sector on a good event.
No relative-acceptance or relative-P1 estimate is requested at this zero.

If G=I, all loss-sector L_r with r>0 vanish although Q_N=D_r>0. Uncapped
rejection would run forever there; the lower-bound selector drops them on
a good event. If A=0, all photons are lost: report the zero signal vector
when r0>=K and otherwise FAIL. K=0 is deterministic vacuum. Zero columns,
m<K, singular G/H, full bunches and N=0 are permitted; N=0 uses the empty
signal permanent one and r=K<=r0, a constant-size special case.

The result deliberately loses rare-sector CONDITIONAL accuracy when those
sectors are omitted: their raw mass, rather than their quality, pays (5).
It does not justify free postselection on a retained/omitted herald sector.
Growing r0 destroys the polynomial argument: D_r, signed r! work and B_r
can be exponential. No general all-loss, complex-transfer, adaptive quantum-
instrument, resolved-environment or quantum-state simulation follows from
this fixed-few-loss construction. Source K photons and all losses remain
in the original ledger; N-source classical proposals are internal work.

Disposition: a self-reviewed conditional route beyond coarse FAIL, pending
independent proof/primitive review. It samples the specified few-loss raw
count alphabet up to an explicit error, not quantum states or a positive
optimizer result. No novelty, matched-cost advantage, native/QPU gate or
paper change is claimed; all prior failures and frozen sources are preserved.
