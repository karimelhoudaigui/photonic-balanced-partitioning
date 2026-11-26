# P96 independent positive-surrogate proof audit

Reviewer `/root/p66_dark_audit`, 2026-11-26; `proof-audit` workflow.
Primary verdict: **PROVED AS WRITTEN** under the stated CF-source,
passive-vacuum, explicitly available T and certified trace-budget hypotheses.
No finite-bit implementation, timing result or optimization advantage follows.

Exact source: `research/P96_COLUMN_LOSS_CLASSICAL_SURROGATE.md`, all 169 lines,
commit `6f4e7fb90e284a8e358c55886ddd2032d45811f9`, SHA256
`b378ebd6bb0bb6f981e9fe395938e3a43aec7775f761b81cda7b394f6dc1e94e`.
The derivation below was reconstructed independently from the frozen statement;
no parent/author verdict, numerical fixture or prior-source attribution is a leaf.

## Claim card and obligation map

Input: K distinct singly occupied known modes of identical photons, vacuum in
every other input. T is the m-by-K observed occupied-column matrix of a passive
vacuum-environment channel, C=T^dagger T<=I, c_i=C_ii, mu=sum c_i<=1/2.
P is the complete observed PNR law; N<=K and total loss is K-N, not a conditioned
survival variable. The proposed q uses only sectors 0,1,2 and the exact first
and second factorial moments of P. Complex entries and repeated output modes
are included. This is not a claim for arbitrary weak-light or correlated inputs.

Dependency graph: CF annihilation contractions -> moments/positive pair masses;
PSD trace bound -> positive singleton masses -> normalized q;
moment-to-sector identities -> signs of every discrepancy -> exact TV;
vacuum dilation/Gram permanent -> factorial moments -> 24 e3(c) -> 4 mu^3;
fresh common-history kernels -> sequential coupling -> transcript bound.
Obligations moments / positivity / normalization / TV equality / constants /
boundary cases / adaptive interpretation passed. Bit complexity and measured
resource costs are not addressed; external priority and QPU claims are out of scope.

## First/second moments, normalization and the trace threshold

For normal ordering write b_j=sum_i T_ji a_i; unused-vacuum annihilators vanish.
The one-particle input matrix is identity on the K occupied modes, so
lambda_j=E n_j=sum_i |T_ji|^2. Write p_ji=|T_ji|^2 and A=TT^dagger.
Applying b_l b_j removes an unordered distinct input pair {i,h}; different
removed pairs leave orthogonal CF states. Its coefficient is
T_ji T_lh+T_jh T_li. Therefore, even for j=l,
g_jl=E[n_j(n_l-delta_jl)]=sum_(i<h)|T_ji T_lh+T_jh T_li|^2>=0.
The squared-modulus terms sum to lambda_j lambda_l-sum_i p_ji p_li;
the cross terms sum to |A_jl|^2-sum_i p_ji p_li, proving (1).
For j=l the amplitude is 2T_ji T_jh and g_jj=4 sum_(i<h)p_ji p_jh.
Thus the repeated-output category 2e_j must have mass g_jj/2; a distinct-output
category e_j+e_l has mass g_jl once, with j<l. There is no missing factorial.

Summing g_jl over l gives
G_j=mu lambda_j+(A^2)_jj-2 sum_i p_ji c_i.
PSD A has ||A||<=Tr A=mu, hence A^2<=mu A. Since the last sum is nonnegative,
0<=G_j<=2mu lambda_j. Thus q(e_j)=lambda_j-G_j>=lambda_j(1-2mu)>=0.
All pair masses are nonnegative and q(0)=1-mu+G/2>=1-mu>=1/2,
where G=sum_j G_j. Sector totals are exactly 1-mu+G/2, mu-G, G/2;
they sum to one, so no rejection, clipping or renormalization is required.
mu=1/2 is included. Zero rows/columns cause no division or undefined category.
The trace condition is sufficient, not necessary for each individual channel.

## Exact TV: every sign and displaced low-sector mass

For a fixed j, sum_l n_j(n_l-delta_jl)=n_j(N-1), so
q(e_j)=E[n_j(2-N)]=P(e_j)-E[n_j(N-2);N>=3].
Hence every singleton is a deficit (possibly zero). For each N=2 category,
its corresponding factorial weight is one on that category, zero on every
other N<=2 category, and nonnegative for N>=3. Thus q(n)>=P(n) on sector two.
Also 1-N+N(N-1)/2=(N-1)(N-2)/2 is one at N=0 and zero at N=1,2, so
q(0)=P(0)+E[(N-1)(N-2)/2;N>=3]>=P(0).
These exhaust all categories; q=0 on H={N>=3}. Both laws are normalized and
nonnegative, so TV is the sum of their deficits, not the sum of all discrepancies:
TV=P(H)+sum_j E[n_j(N-2);H]=E[(N-1)^2;H].
This proves the equality, not merely a high-sector-tail upper bound.
For n>=3, (2/3)(n)_3-(n-1)^2=(n-1)(n-3)(2n-1)/3>=0,
with equality at n=3, proving the first inequality in (3).

## Factorial moments and the constants 24 and 4

Choose R with R^dagger R=I-C. The occupied full columns [T;R] are orthonormal.
Multiplying only observed amplitudes by sqrt(z), for real z>=0, gives Gram
I+(z-1)C. The squared norm of the product of their creation operators is its
permanent, including all repeated-output normalizations. Thus
F(z)=E z^N=per(I+(z-1)C).
Expanding identity-or-C in each row fixes every index outside a chosen I:
F(z)=sum_I (z-1)^|I| per(C_I). This polynomial identity holds also formally.
Differentiation at one yields E(N)_r=r! sum_(|I|=r)per(C_I), not just the sum.

Each C_I is Gram, so its permanent is an unnormalized bosonic squared norm >=0.
PSD C gives |C_ih|<=sqrt(c_i c_h); every permutation product then has modulus
at most product_(i in I)c_i. Summing r! terms proves
E(N)_r<=(r!)^2 e_r(c), including zero columns and impossible r>K.
At r=3, (2/3)(3!)^2=24. Expanding mu^3 shows six times each distinct triple
plus nonnegative repeated-index terms, hence 24 e3(c)<=4mu^3.
No independent-Bernoulli survival assumption was inserted into this argument.

For K=3,m=1,T_i=sqrt(alpha), C=alpha J and 3alpha<=1/2 ensure physicality.
Here F(z)=1+3alpha t+6alpha^2 t^2+6alpha^3 t^3, t=z-1.
In particular P(N=3)=6alpha^3 and the exact TV is 4P(N=3)=24alpha^3.
Since e3(c)=alpha^3, coefficient 24 is attained exactly, including nonzero loss.
Expanding the same polynomial gives precisely the displayed four probabilities
and q's three masses; the singleton deficit is 18alpha^3, tail deficit 6alpha^3.

For equal rank-one columns c_i=mu/K, the sole nonzero eigenvalue of C is mu,
so all examples with mu<=1/2 are physical. At fixed K>=3 as mu decreases to zero,
P(N=3)=6 binom(K,3)(mu/K)^3+O(mu^4), and higher sectors contribute O(mu^4).
Consequently TV/mu^3 ->24 binom(K,3)/K^3 ->4 as K then tends to infinity.
This proves that no smaller uniform coefficient of mu^3 works. The limits are
ordered; no uniform-in-K O(mu^4) remainder or interchange of limits was assumed.

## Countercases and boundary checks

K=0: certain vacuum, empty sums zero. K=1: g is identically zero and q is the
exact vacuum/single-photon law. For every K<=2, H is empty; the same moment
identities give q=P exactly for every physical T, even if mu>1/2.
Complex phases were retained in the second-moment modulus and Gram permanent;
there was no real/nonnegative-T restriction. Diagonal C makes the TOTAL survivor
number a sum of independent Bernoullis, but does not remove spatial interference.

Outside the trace cutoff, K=3,m=1,T_i=1/sqrt(3) is physical: C=J/3<=I.
It has mu=1 and q(e_1)=1-4/3=-1/3, so normalization alone is insufficient.
In the rank-one equal-column family q(e_1)=mu[1-2mu(1-1/K)]; for every
fixed 1/2<mu<=1 it becomes negative at sufficiently large K. At mu=1/2 its
value is 1/(2K)>=0. Thus 1/2 cannot be increased as a uniform trace-only cutoff.
Individual bounds c_i<=eta imply mu<=K eta; they do NOT imply ||T||^2<=eta.
Parallel observed columns attain ||T||^2=K eta when physical. This distinction
prevents substitution of a public per-photon efficiency for a spectral certificate.

## Classical work, decoders and conditional-history composition

A, lambda and row-product sums can be accumulated column by column in
O(m^2 K) arithmetic and O(m^2) additional workspace beyond T; no K-by-K C or
full p table is necessary. The 1+m+m(m+1)/2 categories are a genuinely positive
correlated classical law retaining two-photon interference, not distinguishable
photons, a small-species physical device, or a moment estimate credited as a cut.
Complex T, its certified intensities and any setup/calibration are paid inputs.
Categorical draws, mode processing, decoding/scoring/quenching and actual memory
must also be paid. Arbitrary exact real T is an arithmetic/oracle description;
finite-bit evaluation, rounding/positivity and exact sampling costs remain open.
Near-zero masses cannot be clipped without a separate TV error certificate.

Any SAME fixed stochastic decoder is a Markov kernel and contracts TV: summing
absolute output discrepancies and using its nonnegative row sums proves this.
This includes loss/collision handling and quenching only when both models use
the identical kernel and its actual computational work is counted.
For adaptive use, couple identical policy coins and fresh CF/vacuum trials while
the observed histories agree. Conditional on common h, maximally couple the
raw laws with mismatch probability <=epsilon_t(h). The chance of a first
mismatch by time t is bounded by sum_s sup_h epsilon_s(h), capped at one.
Every reached common history must satisfy the relevant certified trace budget;
the rule choosing T and the information supplied to it must be common.
This does not cover coherent memory, model-specific hidden side information,
postselected renormalization, unseen calibration drift, or wall-clock transcripts.

The hypothetical K=12,c_i=1/50 example has trace 12/50<=1/2 and bound
24 binom(12,3)/50^3=0.04224 per raw attempt; its 96-step capped union bound is
vacuous. It is not a hardware estimate. No broad advantage/no-go, novelty or
QPU claim follows. No import, AST, code execution, RNG, numerical/native/test/
runner call, B raw access, delegation, manuscript edit or external proof leaf
was used. The remaining gap is implementation/resource validation, not the
stated analytical inequality or its exact low-sector error accounting.
