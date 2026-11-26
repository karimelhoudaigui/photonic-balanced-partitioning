# P101 exact-source independent manual proof review

26-Nov-2026. **PROVED AS WRITTEN for the internal scoped algebraic,
decoder, weak-endpoint, rank-one/continuity and three-cut claims.**
This verdict does not determine the finite b=1 B/D sign, prove domination
for all b, certify hardware, or establish an optimizer impossibility beyond
the stated frontier budget. The separate external attribution below is inherited.

## Exact target, dependencies and independence

Source: research/P101_FINITE_FILTER_ALL_OUTPUT_CARD.md in
`.local/p81-exact-review`, commit `69e4a6fe434a677acfc5a7e616471990b16db86b`,
parent `b4efbe5e9944b66ef3126192889c5e9db400ce0c`, clean at reading,
113 lines, SHA256
`65e4199fb468d02eec4155072a60b8d7818ee0d57ef6205e83c2da51bc60027c`.
The exact source was read fully ONLY after its author supplied that freeze.
No moving P101 or another P101 verdict/P107 result was read.

The entire128-line P95 source was read first, ROOT source commit
`e204e010c46f4307b153228bd6c45a943b91f318`, SHA256
`67a75774988f992df286b3f40965273907a98532f7040b45528cff2c1ad18fe3`;
the identical bytes in the P101 commit were checked by hash. The required
exchange stencil and remainder were reconstructed below, not merely accepted
from an earlier review. This is manual independent reconstruction of the
provided candidate, not blind research discovery or an independent model.

## Obligation disposition

| Obligation | Disposition |
|---|---|
| PSD compiler, real-spin cut identity, passive dilation | Passed |
| Counterexample cut values, magnetic gauge, eigenordering | Passed |
| Full PNR and threshold tie kernels; no event conditioning | Passed |
| Both quadratic coefficients and inherited hard remainder | Passed |
| Simple-ground isometry continuity and rank-one signal law | Passed |
| Gauge-nonnegative obstruction at every finite b>0 on this example | Passed |
| Three-candidate optimum after three paid scores | Passed, budget-qualified |
| b=1 sign, all-b mean ordering, larger-graph optimizer advantage | Not proved; correctly left open |
| Anand theorem attribution/algorithmic transfer | Inherited ROOT/P103 source check; not freshly reverified here |

## Compiler and spectrum reconstructed

Each edge term a_ij|x_i-exp(i theta_ij)x_j|^2 is PSD. For real spins,
cos(theta)=-1/2 gives 2a_ij+a_ij x_i x_j. Summing gives
3 sum a-2C_complement=3 sum a-8+2C_G for a balanced four-vertex cut.
This uses exactly four cross pairs, not an unconstrained spin relaxation.
Subtracting the least eigenvalue and dividing by Lambda preserves PSD and
places H's spectrum in [0,1]; it is paid compilation, not restored transmission.
T and sqrt(I-T^2) commute, so the stated block matrix squares to identity
and is Hermitian/unitary even though T is complex.

For the example, the three classes represented by12,13,14 have costs3,2,3.
Complement edges12,23,34,41 all have weight1/2. Their oriented phase sum is
4pi/3+4pi/3+4pi/3-4pi/3=8pi/3, equivalent to2pi/3. With indices0..3,
D_jj=exp[i j(pi/6-4pi/3)] gives forward L' entries -exp(i pi/6)/2,
including the closing edge. For F_jr=exp(-i pi jr/2)/2 the eigenvalues
are 1-cos(pi/6-pi r/2), IN FOURIER ORDER:

    [1-sqrt(3)/2, 1/2, 1+sqrt(3)/2, 3/2].

Thus Lambda=sqrt(3), and H eigenvalues are
[0,(sqrt(3)-1)/(2sqrt(3)),1,(sqrt(3)+1)/(2sqrt(3))]. They are not sorted
in Fourier order. Their filter factors are exactly [1,x,xy,y] in that order;
xy=exp(-b/2). The gap and equation(6), including the sign of its imaginary
forward-neighbor entry, are correct for the DECLARED Fourier convention.

## All-output decoders and the weak signed comparison

Both decoders are defined for every signal count, including vacuum, bunching,
partial loss and all four clicks. PNR uniform priorities choose uniformly
within each tied count level. Threshold selection uses only the click set;
it never infers lost photon number. Their coins are fresh, independent and
common in law for B/D. For fixed G their expected decoded score is a bounded
function f(n,ell) independent of b, as required by P95.

Let S=C_ij+C_ik+C_il, using complement equality C_ij=C_kl. The base and
either one-loss PNR record have expected score S/3. A double loss of i,j
scores C_ij. The two directed bunch records each score (C_ik+C_il)/2.
Substituting into the COMPLETE P95 stencil gives

    H_ij[f_P]=(2C_ij-C_ik-C_il)/4.

For thresholding, both bunch records have three clicks and score S/3,
giving H_ij[f_T]=(2C_ij-C_ik-C_il)/3. No survival denominator appears.
All four complement-cycle pairs have C_ij=3 and numerator1;
|H_ij|^2=(1/2)^2/3=1/12. Summing independently reproduces +b^2/12 and
+b^2/9. The first derivative difference vanishes; these coefficients concern
the full declared optical attempt, not only collisions or accepted subsets.

P95's passive-loss generator has Hermitian trace-norm bound2K||H||;
contractivity gives the degree-two remainder without an exponential factor.
Centering f and adding B/D errors gives R_f(2K||H||b)^3/6.
Here R_f=1,K=4,||H||=1, hence absolute error<=512b^3/6. Subtraction gives
exactly b^2(1-1024b)/12 and b^2(1-768b)/9 as lower bounds. Both are positive
for0<b<1/1024: B has HIGHER cost than an allowed same-T D member there.
Neither bound answers b=1; a loose/negative lower bound is not a sign proof.

The detector distinction is also correct: n=(2,1,1,0) yields the cost2
class with probability1/2 under PNR, while (1,2,1,0) yields probability0.
Both threshold records click on1,2,3 and yield probability1/3. This confirms
that one detector's signed prediction cannot be silently used for the other.

## Rank-one raw law, continuity and phase-erasure limit

For a simple ground P=vv†, the common spectral basis gives V_b-V_infinity
zero on v and squared singular value
t_r^2+(sqrt(1-t_r^2)-1)^2=2-2sqrt(1-t_r^2)<=2t_r^2 on each excited mode.
Thus its norm is <=sqrt(2)exp(-bDelta/2). Tensor telescoping on the normalized
four-photon sector gives vector error<=4 times that norm. Pure-state trace
distance, measurement and removal of resolved environment labels contract
this bound, proving the stated capped TV estimate and range-R cost bound.
No generic square-root continuity theorem or rare-event normalization is used.
Degenerate grounds are explicitly excluded from this rank-one statement.

In the limit, only the bright signal mode survives. For c_i=|v_i|^2,
per(P_I)=|I|! product_(i in I)c_i. Expanding per(I+(z-1)P) therefore gives
sum_d d!e_d(c)(z-1)^d. Conditional on N, the signal occupies the single
mode v, so PNR is Multinomial(N;|v_j|^2). This proves the proposed raw
signal/total-loss sampler; it is not a resolved-dump sampler.

For this uniform-bright example, manual expansion gives
P_B(N=0,1,2,3,4)=(15/32,1/4,3/16,0,3/32), normalized with mean1.
These are NOT D's Binomial(4,1/4) weights. Nonetheless each raw law is
permutation invariant spatially; either equivariant uniform-tie decoder
must output each of the six balanced subsets with probability1/6. Its cost
mean is8/3. This conclusion uses symmetry of the DECODED law, not equality
of B/D raw laws or a claim that strong filtering never has interference.

For every finite b>0, x>y>0, x<1, and the forward entry has real part
1-xy and imaginary part x-y. Since (1-xy)-(x-y)=(1-x)(1+y)>0, its argument
lies in(0,pi/4); its four-edge product has argument in(0,pi), hence is nonreal.
Positive diagonal entries force any nonnegative row/column phase transform
to be diagonal conjugation. The cycle product then contradicts it. Gauge
invariance for CF-input count probabilities is valid; the b->infinity
gauge-positive limit does not make the finite-b matrices gauge-positive.

## Scope of the negative conclusions and remaining gates

Only three unoriented balanced cuts exist. Three actual paid cut evaluations
return their minimum2 deterministically. This defeats any strict best-cost
advantage once that frontier fits the allowance; it proves no equal-clock or
smaller-query-budget theorem. The spectral bridge never supplies an optimum
mask, and a compiler's discovered candidate belongs to its classical credit.

The ideal trace is sum_r exp(-b lambda_r(H))>1 at finite b because at least
one zero eigenvalue contributes1 and the other exponentials remain positive.
Thus the low-trace P96/P98 sufficient regimes are inapplicable to this ideal
filter. Additional attenuation can change that; a public mean efficiency
is not an occupied-column trace certificate. Being outside a sufficient
classical regime is not evidence of hardness or useful optimization.

The named Anand all-survival nonnegative-matrix transfer is an external
attribution inherited from ROOT's source check, not independently certified
by this manual audit. No internal conclusion above depends on it. Its scope
must remain conditional all-four-survival; a nonnegative signal T does not
automatically give nonnegative environment Gram or a whole-loss-PNR sampler.
Physical preparation failures, PNR/dump availability, model error, emission
denominators and actual compilation/shot costs are separately unverified.
The displayed optical predictions assume the declared verified CF input;
adding preparation flags requires their actual mixing law and all costs.

No material internal mathematical gap was found. No numerical P107 argument,
b=1 sign, total-resource advantage or global finite-filter no-go was assumed.
Only this report was written; no scientific execution/import/AST/code/test,
RNG/graph/native/runner/raw-data/QPU/paper/push/delegation occurred. The
source, P100/P105 and all archived data remain untouched by this reviewer.
