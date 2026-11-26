# P137 — independent audit of the explicit weak-reflection window

Reviewed 2026-11-26; complete130-line Git source
`research/P137_WEAK_RATIONAL_REFLECTION_OBSTRUCTION.md` at
`c24a5b8ddd7c381d4f9060f3696a69c00ba4e290`, independently hashed SHA256
`fb1ffcfa694a34d03a4482477417e65a95b0add82000ba4d65106b097cf2eccb`.
Reviewer did not author P137 and read no separate author verdict.
ROOT supplied the candidate. No program/import/AST, graph draw or numerical matrix evaluation, RNG, native call,
P134 implementation/outcome/raw access, external priority search, or source edit occurred.

**Primary verdict: proved as written.**
The explicit raw CF/hold inequality and its uniform constants survive a cold reconstruction.
The conclusion is the stated fixed-incumbent utility obstruction, not a total-cost or universal optimizer result.

## 1. Normalized claim and physical transfer

Require 2<=K<=4, m>=K+1, canonical isometry E into receiver prototype R,
Hermitian H with ||H||op<=1, and |H_ja|>=d>0 for EVERY outside j and source a.
Both arms use the same family and decoder, with D actually allowed to choose2*kappa.
All non-CF records hold R, and utility satisfies h(R)=0, h>=0 elsewhere.
These are load-bearing conditions, not consequences of approximate column means or a sparse support graph.

Set B=E†H²E. Then 0<=B<=I and

    F_x†F_x=E†(I-i*x*H)(I+i*x*H)E=I+x²B,
    A_x=(I+x²B/2)^(-1),  T_x=(E+i*x*HE)A_x.

No commutation between H and a compressed source-space matrix is needed.
A_x is a positive contraction, commutes with B, and ||A_x-I||<=x²/2.
Moreover

    I-T_x†T_x = A_x[(I+x²B/2)²-(I+x²B)]A_x
               = x^4 A_x B² A_x/4 >=0.

Thus both x=kappa and x=2*kappa are legitimate contractions with their P133 reflection dilations.
The D comparator is a changed parameter setting, not an assumed scalar amplification of T_kappa.
In P133 notation `D_x=-x² B A_x/2`; the ACTUAL occupied dump block is `-D_x=+x² B A_x/2`.
Its squared norm is <=x^4/4, so the CF-source dump mean is at most K*x^4/4.
For an integer dump count, Pr(dump>=1)<=E[dump], proving the source's probability bound.
The same first-moment bound holds for distinguishable input. No independent-loss coins are assumed.
Rational H and x give encoded rational targets; the analytic inequality itself permits arbitrary complex H and real x under its hypotheses.
No finite-bit mesh/clock guarantee is supplied by that observation.

## 2. Critical outside-row normalization

For Y of size K, put J=Y\R, C=R\Y and s=|J|=|C|>=1.
For x>0 divide EACH outside row of T_x[Y,:] by x, obtaining M_x.
Define M_0 as the limit, not by dividing at zero: its inside rows are basis rows e_i†,
and outside rows are i*H[j,R].

Inside entries of M_x have modulus<=1 because ||T_x||<=1.
Outside rows satisfy `T_x[j,:]/x=i*(HEA_x)[j,:]`, also with every entry bounded by1.
M_0 has the same bound. No row-sum estimate proportional to m is required.
For inside rows, entry error is <=||A_x-I||+x||HEA_x||<=x²/2+x.
For outside rows it is <=||HE(A_x-I)||<=x²/2.
Hence for 0<x<=1 the global entry error is at most3x/2.

In M_0 every retained inside row forces its OWN source column.
The remaining columns are precisely C; there is no omitted sum over which sources move.
Thus `per(M_0)=i^s per(H[J,C])` and `per(|M_0|²)=L=per(|H[J,C]|²)`.
Every one of the s! nonnegative intensity terms is >=d^(2s), giving L>=s!*d^(2s)>0.
Cauchy on those s! amplitude terms gives `|per(H[J,C])|²<=s!*L`.
The leading factor is s!, not K!; this is why single replacements retain a positive gap at K4.

## 3. Remainders and every explicit constant

For entry-bounded-by1 K-by-K matrices with entry error e, product telescoping gives
permanent error <=K*K!*e. Also each permanent has modulus<=K!.
Therefore squared-modulus error <=2*K!*K*K!*e, valid for complex phases and zeros.
At x=kappa this gives

    p_B(Y;kappa)/kappa^(2s) <= s!*L + 3K(K!)²*kappa.

For N_x=|M_x|², entries lie in[0,1] and their difference from N_0 is <=3x.
The real permanent error is <=3K*K!*x, so at x=2*kappa,

    p_D(Y;2*kappa)/kappa^(2s) >=4^s*(L-6K*K!*kappa).

There is no extra receiver factorial because Y is CF, and no survival denominator.
Subtracting yields exactly

    normalized difference >=(4^s-s!)*L - 3K*K!*(2*4^s+K!)*kappa.

For s=1,2,3,4, the first factors are3,14,58,232.
Since d<=1 and s<=K, the leading term is >=3*d^(2K).
The error coefficient is <=3K*K!*(2*4^K+K!).
Substitution of `kappa0=d^(2K)/(2K*K!*(2*4^K+K!))` makes its error strictly <(3/2)*d^(2K).
Multiplication by kappa^(2s)>0 proves the claimed margin; the displayed >= is safe even though this derivation gives >.
The denominators272,4824,102912 are correct for K2,K3,K4.
Also kappa0<=1/272, so both needed entry estimates have 2*kappa<1.
The bounds are independent of m except through the supplied floor d; a vanishing complex leading permanent is harmless because L stays positive.

## 4. Consequences, boundary attacks and limits

The simultaneous pointwise order on every Y!=R implies order for every positive utility threshold and every nonnegative h with h(R)=0.
Summing the explicit gaps is strict if some alternative has positive utility.
Dump and collision attempts remain charged; D may have a larger dump bound at2*kappa, but the comparison already includes their hold mass.
It is an attempt/K-photon comparison at a fixed incumbent. No adaptive-chain, annealing, absolute mixing-time or equal-wall result follows.
Any IID best-of-T transfer still needs a separately declared repeated-trial/stopping protocol.

The floor is on the DIRECT H outside-to-source entries, not on the eventual T entries or a mean transmission.
Without it, H=diag(0,...,0,1) on an outside mode has HE=0, B=0, T_x=E.
All off-prototype probabilities then vanish for both arms, refuting strictness without refuting this theorem.
No general non-strict sparse-H statement follows from that counterexample or this proof.
The dimension constraint (m-K)d²<=1 is necessary; additional constraints may hold and are not needed by the estimates.
As d shrinks, the certified window shrinks; no uniform all-strength conclusion follows.

If R is not the incumbent or h(R)>0, its omitted probability difference can matter and the utility conclusion is not established.
Beta-dependent diagonal loading, sparse couplings, finite-strength settings and grids lacking2*kappa are outside the theorem.
The same nominal matrix family must be accessible to D; actual source/tag/detector response and compilation errors need their own certificates.
Different preparation, synthesis, inverse work, physical loss, calibration, internal-tag resources and wall clocks have not been equated.
Nothing here evaluates or rejects P134's fixed contexts, provides a native/QPU gate, or certifies novelty/optimizer advantage.
