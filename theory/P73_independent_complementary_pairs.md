# P73: complementary colored Gaussian pairs, coherence and raw cost

Independent static derivation, 2026-11-25, branch
`research/p66-dark-barrier`, starting at
`cd59bcfd96eedb8dbf76c258e63f996ee6987567`. No other P73 file or verdict
was read. ROOT's candidate, including its source-feasibility scope point,
is the question examined here, not accepted evidence. Only this file is
written. All Gaussian, hafnian, matching and resource identities below
are derived internally; no primary lookup was needed. No scientific
import, script, test, numerical calculation, graph generation, seed/draw,
backend experiment, manuscript edit or QPU call was performed.

Decision: **REJECT the first-order conditional cut tilt as evidence of a
distinct coherent optimization mechanism.** The incoherent matching control
has the same first order. **KEEP** the normalized raw law and the explicit
second-order diagnostic proved below. A genuinely different source or
fixed-number preparation is **FOLLOWUP only under a new normalization,
preparation and raw-cost contract**. This does not reject all Gaussian
sources or establish an all-graphs no-go, positive optimizer, full sampler,
hardware feasibility or novelty.

## 1. Model and normalization conventions

Let k>=2 be even, N=2k, and let A be the real symmetric, nonnegative,
zero-diagonal weighted adjacency of an undirected cost graph. Symmetry
is essential for the pair matrix used here. Put

    W=J-I+epsilon A,       Z=lambda W,
    lambda>0,             ||Z||op<1.

Each of two resolved colors has N vertex modes. Its normalized pure,
zero-displacement Gaussian pair state is defined by

    |G(Z)> = det(I-Z Z^dagger)^(1/4)
                  exp(1/2 a^dagger Z a^dagger)|0>.

The two colors are independent copies. The accepted event is exactly:
red has k photons occupying a CF subset S, and blue has k photons
occupying its complement. There is one photon in total at every vertex,
with color and vertex both resolved. There are binom(2k,k) distinct
oriented red subsets; S and its complement are different color records.
Vacuum, other photon totals and all failed/collided patterns remain raw
rejections. Color resolution requires 2N orthogonal resolved degrees of
freedom, or equivalent color-resolving readout, not an unlabeled N-mode
count vector with a different acceptance rule.

For perturbation theory fix k,A and lambda strictly inside the allowed
interval at epsilon=0. Continuity gives a neighborhood with ||Z||<1.
The Taylor remainders below are for that fixed finite instance, not a
uniform estimate in k or graph weights. A valid lambda(epsilon) changes
only common factors of accepted weights and hence not their conditional
spatial law.

## 2. Deriving the Gaussian prefactor and accepted raw weight

Real symmetry gives W=O diag(omega_j) O^T with O orthogonal. In the
corresponding passive modes the unnormalized state is a product of
single-mode factors exp(z_j b_j^dagger^2/2)|0>, z_j=lambda omega_j.
Negative omega_j are allowed; their phases do not change the norm.
For one mode,

    exp(z b^dagger^2/2)|0>
      =sum_{n>=0} z^n sqrt((2n)!)/(2^n n!) |2n>,
    norm^2=sum_{n>=0} binom(2n,n)(|z|^2/4)^n
          =(1-|z|^2)^(-1/2).

The last binomial series follows, for example, by its coefficient
recursion and the differential equation (1-q)f'(q)=f(q)/2, f(0)=1.
Multiplying over modes proves the normalization in section 1. In this
real case Z Z^dagger=lambda^2 W^2 and the determinant is positive.

Define the hafnian of an even-indexed submatrix as the sum, over its
unordered perfect matchings, of products of pair entries. For a CF subset
S of size k, the coefficient of product_{i in S} a_i^dagger in the
exponential is haf(Z[S]). In the term of order k/2, the factorial of
the exponential cancels the orders of its unordered pair factors. The
1/2 in the symmetric quadratic form cancels the two orientations of
each pair. CF output occupation factorials are one. Thus

    amplitude_red(S)=det(I-lambda^2 W^2)^(1/4)
                              lambda^(k/2) haf(W[S]).

Its squared probability has the square-root determinant and lambda^k.
The blue amplitude has the same formula with S replaced by Sc. Their
independence proves the exact accepted-record raw probability

    P_raw(S,Sc)=det(I-lambda^2 W^2) lambda^(2k)
                         haf(W[S])^2 haf(W[Sc])^2.

The proposed determinant exponent and power of lambda are therefore
correct. Absolute squares would be required for general complex W;
the real symmetric W here permits ordinary squares. Gaussian normalization
already includes every photon-number sector and collision outcome.

Conditional on acceptance, all determinant and lambda factors cancel.
Its spatial weight is

    w_B(S;epsilon)=haf(W[S])^2 haf(W[Sc])^2.

This cancellation is not a statement that the discarded attempts or
their photons cost nothing.

## 3. First order is shared with an incoherent matching control

For any k-vertex set T let H=(k-1)!! be its number of perfect matchings.
Let M be a uniform perfect matching on T, and define

    X_T(M)=sum_{e in M} A_e,       Y_T(M)=sum_{e in M} A_e^2,
    mu_T=E_M X_T,                nu_T=E_M Y_T,
    v_T=Var_M X_T.

Then

    haf(W[T])=H E_M product_{e in M}(1+epsilon A_e).

A fixed edge belongs to a uniform matching with probability 1/(k-1),
by pairing its first endpoint uniformly. Write

    t_T=sum_{i<j in T} A_ij,       q_T=sum_{i<j in T} A_ij^2.

Consequently mu_T=t_T/(k-1) and nu_T=q_T/(k-1). If C_A(S) is the
undirected cut and t_A the total graph edge weight, then
t_S+t_Sc=t_A-C_A(S). Expanding the two squared hafnians gives

    log w_B(S;epsilon)
       =4log H + 2epsilon(t_A-C_A(S))/(k-1)+O(epsilon^2).

At epsilon=0 the accepted spatial law is uniform over all red k-subsets.
Let E_0 denote that uniform law. Normalizing the weights therefore gives

    log P_B(S | accepted)
       =-log binom(2k,k)
         -2epsilon[C_A(S)-E_0 C_A]/(k-1)+O(epsilon^2),

    d/d epsilon E_B[C_A | accepted] at epsilon=0
       =-2 Var_0(C_A)/(k-1).

The derivative is strictly negative only when the uniform cut variance
is nonzero. It is a real conditional response, not by itself evidence
of interference benefit.

Define the candidate incoherent matching weight precisely as

    w_C(S;epsilon)=haf((W elementwise-squared)[S])
                         haf((W elementwise-squared)[Sc]).

Each factor is H E_M product_{e in M}(1+epsilon A_e)^2. Its logarithmic
linear coefficient is 2mu_T, the same as a squared coherent hafnian.
Hence its normalized spatial law has exactly the same first-order log
tilt and expected-cut derivative. This is a classical comparison of
positive weights; no efficient exact sampler or physical normalization
for a separate incoherent photon source is assumed here.

## 4. First possible coherent difference: second order and its centering

For one subset T, expansion through order two gives

    log haf(W[T])
      =log H +epsilon mu_T
                  +epsilon^2(v_T-nu_T)/2+O(epsilon^3),

    log haf((W elementwise-squared)[T])
      =log H +2epsilon mu_T
                  +epsilon^2(2v_T-nu_T)+O(epsilon^3).

For the first identity, the product's quadratic coefficient is
E(X_T^2-Y_T)/2 and the logarithm subtracts mu_T^2/2. For the second,
write the product of squared factors as
exp(2epsilon X_T-epsilon^2 Y_T+O(epsilon^3)); its cumulant expansion
has quadratic coefficient 2v_T-nu_T. Both arguments are finite
polynomial/Taylor identities with a positive value at epsilon=0.

Put V(S)=v_S+v_Sc. The literal UNNORMALIZED weight difference is

    log w_B(S;epsilon)-log w_C(S;epsilon)
       =2log H -epsilon^2 V(S)+O(epsilon^3).

Thus ROOT's suggested expression without a constant is correct only
after removing the S-independent baseline 2log H, or when log weights
are explicitly understood modulo a common constant. For the normalized
conditional laws, there is a different essential qualification:

    log P_B(S | accepted)-log P_C(S)
       =-epsilon^2[V(S)-E_0 V]+O(epsilon^3).

Partition-function normalization centers V. Omitting that centering
cannot be a literal normalized-law identity. This distinction does not
change the negative matching-variance coefficient as a relative score.
The first different order is generically two, not necessarily two for
every A: V may vanish or be constant across subsets.

For k=2 each induced set has a unique matching. Its squared hafnian
equals the hafnian of its squared entries exactly, and H=1. Therefore
w_B=w_C for every valid epsilon, and the conditional laws coincide at
all orders. For k=4, an induced set with exactly one nonzero edge of
weight a has v_T=2a^2/9; a set with no such edge has variance zero.
Taking a single-edge cost graph on N=8 makes V(S) nonconstant according
to whether that edge is internal or crosses the cut. This verifies a
genuine second-order difference without a numerical experiment.

There is no universally favorable sign for the resulting objective
response. Indeed the conditional expected-cut difference has coefficient

    E_B C_A-E_C C_A=-epsilon^2 Cov_0(C_A,V)+O(epsilon^3).

For the single-edge example, C_A is positive only when V=0 and V is
positive only when C_A=0, so that covariance is negative. The coherent
correction then increases expected cut relative to the incoherent control
at order two. A coherent difference is not automatically a useful one.

## 5. Matching variance is computable from elementary graph statistics

For a k-set T with even k>=4, additionally let

    r_i=sum_{j in T, j!=i} A_ij,       R_T=sum_{i in T} r_i^2.

Two disjoint fixed edges belong to the same uniform matching with
probability 1/[(k-1)(k-3)]. Edges sharing a vertex cannot both occur.
The sum over unordered disjoint edge pairs is

    D_T=(t_T^2+q_T-R_T)/2.

To see this, all distinct edge pairs sum to (t_T^2-q_T)/2, while
vertex-sharing pairs sum to (R_T-2q_T)/2. No pair of distinct simple
edges is counted as sharing two vertices. Hence

    v_T = q_T/(k-1)
           +(t_T^2+q_T-R_T)/[(k-1)(k-3)]
           -t_T^2/(k-1)^2

        =[(k-1)(k-2)q_T-(k-1)R_T+2t_T^2]
                              /[(k-1)^2(k-3)].

These quantities take O(k^2) arithmetic from the induced weighted graph.
For k=2 use the unique-matching value v_T=0 instead of the disjoint-edge
argument. The variance formula also makes explicit that matching
fluctuations need not be photon-number or sampling noise.

All terms in the bosonic log score through order two are therefore
classically computable per proposed subset:

    log w_B(S;epsilon), modulo its common constant,
      =2epsilon(t_A-C_A(S))/(k-1)
        +epsilon^2[V(S)-(q_S+q_Sc)/(k-1)]+O(epsilon^3).

One may reproduce this truncated score without hafnian evaluation. This
does not provide its partition function, rapid mixing, independent draws,
an exact full sampler, or uniform control of the Taylor remainder in a
growing-k limit. The full incoherent hafnian weights are likewise not
declared cheaply samplable. The first coherence correction is thus not
an algorithmically irreducible score, despite its genuine interference
origin in the coherent state.

## 6. Exact base acceptance and favorable raw-resource ceilings

At epsilon=0, W0=J-I has eigenvalue 2k-1 once and -1 with multiplicity
2k-1. Each induced k-set has hafnian H. Therefore, for
0<lambda<1/(2k-1), the exact acceptance probability per preparation is

    Pacc=binom(2k,k) H^4 lambda^(2k)
             [1-lambda^2(2k-1)^2] [1-lambda^2]^(2k-1).

No factor 1/2 divides the binomial coefficient: red and blue are resolved.
This is a raw probability, including Gaussian photon-number failures.

The integral bounds on factorials give

    e(n/e)^n <= n! <= e n(n/e)^n,       n>=1.

For k=2m and H=k!/(2^m m!), the upper bound in the numerator and lower
bound in the denominator yield

    H <= k(k/e)^(k/2).

Using binom(2k,k)<=4^k, the determinant factors at most one, and the
strict lambda cap,

    Pacc <= k^4 exp(-2k) [2k/(2k-1)]^(2k)
          <= e^2 k^4 exp(-2k),
    hence Pacc<=min(1,e^2 k^4 exp(-2k)).

In the last inequality log(1+x)<=x gives
[2k/(2k-1)]^(2k)<=exp(2k/(2k-1))<=e^2. Thus the supplied elementary
ceiling is valid uniformly over all allowed lambda, though it can be
vacuous for small k and is not a tight optimum.

For one diagonal squeezed mode, differentiating the norm series above
gives mean photon number |z|^2/(1-|z|^2). Both colors therefore have
total mean emitted photons

    mu=2 Tr[lambda^2 W^2 (I-lambda^2 W^2)^(-1)].

At W0 in particular,

    mu=2{lambda^2(2k-1)^2/[1-lambda^2(2k-1)^2]
                  +(2k-1)lambda^2/(1-lambda^2)}
       >=2lambda^2(2k-1)^2 >0.

Using that lower bound before maximizing the remaining positive power
of lambda gives

    Pacc/mu
       <=binom(2k,k) H^4 lambda^(2k-2)/[2(2k-1)^2]
       <=binom(2k,k) H^4/[2(2k-1)^(2k)]
       <=(e^2/2) k^4 exp(-2k).

This proves the requested uniform accepted-records-per-emitted-photon
ceiling. Lambda=0 is excluded, so no zero-over-zero ratio is used. The
stability boundary is also excluded because the Gaussian is not
normalizable there.

Under independent identical repeats until an accepted record, the mean
attempts are 1/Pacc and the mean total emitted photons are mu/Pacc.
The latter identity follows by summing contributions at each attempt:
reaching that attempt depends only on earlier outcomes and is independent
of its photon number. It does not assume independence of success and
photon number within the same attempt. These are already favorable
resource counts; preparation, detector, loss and classical costs are
additional. Conditional low-cut records alone cannot be used as a raw
benefit. These exponential ceilings were proved only at W0, not for every
perturbed W or every Gaussian source.

## 7. Preparation and pair-rank boundaries

For a pure two-photon state write its symmetric pair matrix M through

    |psi_2> proportional to (1/2)sum_ij M_ij a_i^dagger a_j^dagger|0>.

A passive unitary sends M to U M U^T and preserves rank. Two distinct
CF input photons have M=e_i e_j^T+e_j e_i^T of rank two. Padding vacuum
modes cannot increase this rank; passive propagation and vacuum heralding
cannot produce a generic rank-N W from that resource.

More generally start with m singly occupied CF input modes and vacuum
elsewhere, apply a passive unitary, and fix a photon-count herald with
m-2 photons detected. Let v_1,...,v_m be the input columns restricted
to retained modes. Expanding the product of their m creation factors
and contracting the detected factors leaves a two-photon polynomial
in the span of those v_i. Its pair matrix has the form

    M_res=V C V^T,       V=[v_1 ... v_m],

for some symmetric coefficient matrix C. Thus rank M_res<=m. This is a
necessary condition for a specified pure residual two-photon state,
not a preparation algorithm, sufficiency theorem or success-rate bound.
Whenever W is full rank N, this model requires m>=N to prepare its
two-photon sector. W0 is full rank and remains so in a neighborhood of
epsilon=0; special rank-deficient perturbations must be treated by their
actual rank. The bound concerns a two-photon pair matrix, not arbitrary
representations of a fixed k>2 photon state.

There is an additional photon-number obstruction for the FULL Gaussian
state: every nonzero diagonal squeezing coefficient z produces nonzero
amplitudes at arbitrarily large even photon numbers. Passive basis changes
preserve total number, so any nonzero |G(Z)> has unbounded photon-number
support. A finite-m Fock input with passive optics, vacuum ancillas and
photon-count heralding has retained photon number at most m. It therefore
cannot prepare that exact full Gaussian state. The rank-m observation
above concerns its two-photon sector or a model explicitly targeting that
two-photon matrix, not a way around this conservation statement.

A fixed-number hafnian state can be a different mathematical model. Its
normalization and preparation/heralding probability must then be supplied
afresh; the full-Gaussian determinant and acceptance formula cannot be
reused as if the source were unchanged. Generic Gaussian squeezers,
their mode count and their calibration are not assumed available on the
project's hardware. These boundaries do not prohibit legitimate active
Gaussian sources with explicitly paid resources.

## 8. Scoped disposition and remaining work

| Scope | Disposition |
|---|---|
| Normalized two-color raw formula and parity/color labels | KEEP: derived exactly |
| Conditional cut response at first order | KEEP as an identity; REJECT as evidence unique to coherence |
| Second-order matching-variance term | KEEP with the baseline constant or normalized-law centering |
| k=2 claimed coherent difference | REJECT: the two spatial weights agree exactly |
| Cheap second-order classical score | KEEP; no exact or fast full sampler follows |
| Base acceptance and emitted-photon ceilings | KEEP at epsilon=0, uniform in valid lambda |
| Free successful shots or reused Gaussian norm after source change | REJECT |
| Two-CF-photon preparation of generic full-rank pair matrix | REJECT within passive/vacuum model |
| Heralded m-photon route | Necessary rank bound only; preparation/rate remain FOLLOWUP |
| Exact nonzero Gaussian from finite Fock/passive/herald resources | REJECT by photon-number support |
| New active or fixed-number source with complete raw budget | FOLLOWUP under a new contract, not authorized here |
| All-Gaussian no-go, optimizer advantage, hardware or novelty | Not established |

The remaining physical questions are a specified available source, its
normalization, preparation probability, color resolution and complete
per-accepted-record costs. The remaining optimizer question is performance
against independent classical controls after all those costs. No answer
to those questions follows from a conditional hafnian tilt or the presence
of a nonzero interference term.

Final mathematical proofreading checked both determinant exponents,
lambda powers, color multiplicity, matching moments, the constant versus
centering distinction, k=2, raw photon accounting and the exact scope of
pair-rank versus full-Gaussian preparation. Only text/Git integrity checks
accompany this independent freeze. No scientific execution was performed.
