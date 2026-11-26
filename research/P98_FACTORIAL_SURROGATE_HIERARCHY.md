# P98: positive classical hierarchy from truncated factorial moments

Owner `/root/p66_dark_audit`, 2026-11-26; parent `35e1cf9d56a97242ecd46220ff32136ffadfa1cc`.
Status: **shared ROOT candidate proved below in its stated model**, by static
derivation/self-review; this new proof has not received independent review.
This is a scoped classical approximation result, not an optimization advantage,
matched-time conclusion, hardware certificate or novelty claim.

## Model and theorem

Use P96's known CF source: one identical photon in each of K distinct inputs,
vacuum elsewhere, observed occupied-column matrix T in C^(m by K),
C=T^dagger T<=I, c_i=C_ii, mu=Tr C. P is the complete observed PNR law;
N=|n|<=K, and total lost count is K-N. T is available and paid, not an oracle
obtained free from hardware. Complex phases, vacuum and repeated outputs remain.
Let s be a nonnegative integer, with s<=K sufficient. Define multivariate moments
a_r=E_P product_j binom(n_j,r_j), a_0=1, and the formal polynomial
Q_s(z)=sum_(|r|<=s) a_r product_j(z_j-1)^r_j.
Let q_s(n) be its REAL coefficients, zero above degree s. They sum to one
but need not be nonnegative. Put alpha=sum_n max(-q_s(n),0) and
r_s(n)=max(q_s(n),0)/(1+alpha).
Then r_s is a positive normalized classical law, and
TV(P,r_s)<=L_s:=(1/2)||P-q_s||_1
 =E[V_s(N) 1_(N>s)]
 <=2^s E binom(N,s+1)<=2^s(s+1)! e_(s+1)(c)<=mu(2mu)^s.       (A)
The equality concerns a signed q_s; L_s need not itself be <=1. The repaired
law's TV can always be capped at one. s>=K gives exact P and alpha=0.

## Exact coefficients and sectorwise signs

First take P concentrated at one occupation y, |y|=N. The coefficient of z^n,
|n|=j<=s, is zero unless n<=y componentwise. Otherwise it is
sum_(n<=r<=y, |r|<=s) binom(y,r)binom(r,n)(-1)^(|r|-j)
 =binom(y,n) sum_(k=0..s-j)(-1)^k binom(N-j,k).
For N>s, Pascal cancellation makes this exactly
(-1)^(s-j) binom(y,n) binom(N-j-1,s-j).                         (B)
For N<=s the untruncated binomial expansion is z^y: there is no error at all.
No generalized binomial with a negative upper argument is needed in (B).

Average over y. In each low sector j, q_s-P has sign (-1)^(s-j);
in high sectors it equals -P. Thus no cancellation occurs between different
y in the same sector. Since the signed discrepancy has total mass zero,
its half-l1 norm is its positive mass, from j<=s with j congruent to s mod2.
Vandermonde gives sum_(|n|=j)binom(y,n)=binom(N,j), hence
V_s(N)=sum_(0<=j<=s, j congruent s mod2)
              binom(N,j)binom(N-j-1,s-j), N>s.                (C)
This proves the equality in (A), retaining displaced masses in all low sectors.
Examples: V_0(N)=1; V_1(N)=N; V_2(N)=(N-1)^2, recovering P96's exact TV.

For N>=s+1 direct factorial cancellation yields
V_s(N)/binom(N,s+1)
 =(s+1)sum_(j congruent s mod2)binom(s,j)/(N-j).
Every denominator increases with N; the maximum is at N=s+1. There each
summand becomes binom(s+1,j), and the parity half of the binomial sum is 2^s.
Therefore V_s(N)<=2^s binom(N,s+1), including s=0.

For completeness, weighting observed columns by sqrt(z) in a vacuum dilation
gives E z^N=per(I+(z-1)C). Expanding identity-or-C factors and differentiating
at one gives E(N)_d=d! sum_(|I|=d)per(C_I). Gram positivity and
|C_ih|<=sqrt(c_i c_h) bound each permanent by d! product_(i in I)c_i.
Thus E binom(N,d)<=d! e_d(c). Finally mu^d>=d! e_d(c), by expansion of
the nonnegative sum. These facts prove all inequalities of (A), not only a tail bound.

## Positive repair: no extra factor two

The mass of q_s^+ is 1+alpha because sum q_s=1. For any positive probability P,
on coordinates where q_s<0, replacing it by r_s=0 reduces l1 distance exactly
by sum(-q_s)=alpha. On other coordinates r_s=q_s/(1+alpha)<=q_s, and the
triangle inequality permits an increase at most
sum_(q_s>=0)(q_s-r_s)=alpha. Thus ||P-r_s||_1<=||P-q_s||_1.
This uses neither unknown values of P nor a sampling oracle for it. The repair
is a proved approximation operation, not unjustified clipping of roundoff.
It is valid even outside the useful low-trace regime, though (A) may be vacuous.

## Constructive moments, repeated-output normalization and work

For a multi-index r of size d, write T[r,I] for a d-by-d matrix with output
row j repeated r_j times and distinct occupied input columns I. Normal ordering
and CF annihilation leave orthogonal states for different removed subsets I.
The coefficient of each is the permanent, so
a_r=[sum_(|I|=d)|per(T[r,I])|^2]/product_j r_j!.                (D)
There is exactly one output factorial divisor, not d! and not its square.
d=0 gives one; d>K gives zero. For d=2 repeated output, the squared amplitude
has factor four and division by 2! gives P96's g_jj/2, as required.

For each d<=s there are binom(m+d-1,d) moments and binom(K,d) input subsets.
A d-by-d permanent costs O(d2^d) arithmetic: expand
(-1)^d sum_(J subset [d])(-1)^|J| product_i sum_(j in J)B_ij;
inclusion-exclusion kills maps missing a column, leaving exactly bijections.
Subset row sums and products give the stated work, also with repeated rows.
Computing all (D), then expanding each product(z_j-1)^r_j into at most 2^d
monomials, therefore costs (mK)^{O(s)} arithmetic for s<=K (trivial cases apart).
There are binom(m+s,s) low categories to store, plus T and setup workspace.
This is not polynomial jointly in dimensions and 1/epsilon.

For 0<mu<1/2 and epsilon>0: if epsilon>=mu use s=0; otherwise choose
s=min(K,ceil[log(mu/epsilon)/log(1/(2mu))]). If the cap K is selected, exactness
replaces the geometric bound. mu=0 means certain vacuum; K=0 is the same case.
K=1,2 are included without special moment normalization. epsilon=0 requires
s=K unless other exact structure is proved. At mu=1/2 the geometric denominator
vanishes: this trace-only bound does not certify accuracy improvement with s,
though s=K is exact and the explicit e_d bound may be sharper.
m=0 is trivial vacuum; s>=K can simply be replaced by K.

With a fixed certificate mu<=rho<1/2 independent of input size, fixed positive
epsilon needs constant s, giving polynomial dimension work. Inverse-polynomial
epsilon needs s=O(log input_size), hence quasi-polynomial work under this
construction. No uniform polynomial claim holds as rho approaches 1/2, nor is
this a relative-error sampler for arbitrarily rare outcomes.

## Exact rational version and bounded-randomness qualification

If T is Gaussian-rational (entries in Q(i), NOT a Gaussian-state source), put
its real/imaginary integer numerators over a common integer denominator D>0.
Every a_r has denominator dividing D^(2d) product_j r_j!; thus
M=D^(2s)s! is one common denominator for all q_s coefficients.
These coefficients can be constructed and signed exactly, then written k_n/M.
The repaired probabilities are max(k_n,0)/W, W=sum_n max(k_n,0), an integer >=1.
No approximation is added by this exact repair. Intermediate bit lengths are
polynomial in s, input encoding length and log dimensions: products have degree
at most 2s, and subset/binomial sums add only logarithms of their term counts.
Consequently the fixed-degree polynomial / logarithmic-degree quasi-polynomial
claims also admit exact rational bit implementations, with their actual costs.

Given ideal independent fair bits, use b=ceil(log2 W) bits per uniform integer
proposal and reject values >=W. Acceptance is at least 1/2; expected blocks <=2,
and a cumulative integer-weight table samples the category exactly. W=1 is
deterministic. This is an expected finite-bit algorithm, not a hard wall-time bound.
If a future contract caps proposals at B blocks, the explicit FAILURE probability
is <=2^-B. Keep that flag; the extended raw-law TV bound gains at most 2^-B.
No hidden rerun, discarded failure or conditional-only report is permitted.
Rounding an irrational/uncertain physical T adds a SEPARATE channel error budget;
this proof does not certify a floating-point repair, calibration or finite PRNG law.
Given a separate input-law TV certificate xi, the total bound becomes
xi+mu(2mu)^s+2^-B, using the certified rational model's mu; no xi is supplied here.

## Scientific interpretation and adaptive limits

Every common decoder/score kernel contracts this whole-law TV bound, including
vacuum/loss/collision treatment and common paid quenching. A bounded statistic
of known range F changes in expectation by at most F times the bound. This
does not provide relative accuracy after rare herald conditioning.
For fresh CF/vacuum attempts under the SAME policy and observed classical
history, apply the construction conditionally to T_t(h), with certified budgets.
Couple equal histories until first mismatch; transcript TV is at most the sum
of per-step worst-history bounds, capped at one. All moment/table construction
and policy work must be charged anew when inputs change, unless truly cached.
For polynomially many steps, inverse-polynomial per-step error generally invokes
the quasi-polynomial regime, not a free polynomial entire-trajectory simulator.
Coherent memory, hidden physical information, model-specific clocks and drift
are outside this argument. Exact complex T access/certification, source and
calibration costs, categorical draws and actual graph decoding/scoring are paid.

This constructs a constant-error classical approximation under the CERTIFIED
low-trace input/access assumptions; it proves no matched-wall-time domination and
no universal impossibility beyond that regime. The optimization objective remains
open elsewhere; independent review and primary attribution are required before
claiming a new theorem. P97 and all negatives are untouched. No imports/AST,
RNG, numerical/code/native/test/runner execution, data read, QPU, manuscript,
push, checkout or delegation occurred. No experiment is authorized by this card.
