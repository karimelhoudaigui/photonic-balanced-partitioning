# P77: exact positive-hafnian countercontrol and a finite-strength screen

25 November 2026. ROOT static derivation from the P73 source law. No
scientific code, graph instance, RNG, test, sampler, numerical probability,
hardware preparation or QPU call is executed. This is a new finite-strength
route, not a consequence of the unproved general P75 Gaussian overlap cap.
Independent derivation/review is PENDING; no novelty claim is made.

Question: can P73's nonnegative pair amplitudes provide a conditional law
that is inaccessible to an ordinary optimum-blind classical control after
raw source failures? The first uncertainty is the exact classical proposal
mass, followed by its normalization/resource comparison. Both are derived
below. The conclusion is scoped to positive amplitudes and raw attempt
counts, not measured total-cost advantage.

## 1. Source, positivity and a common normalization

Let k>=2 be even, N=2k, D=binom(2k,k), and m=(k-1)!!. Let W be real
symmetric with zero diagonal and strictly positive off-diagonal entries.
Set a=min_(i<j) W_ij>0, b=max_(i<j) W_ij and rho=b/a>=1. P73's
W=J-I+epsilon A, A>=0, is included at every finite epsilon with this ratio.
Let lambda>0, lambda||W||<1. Two independent Gaussian colors with pair
matrix Z=lambda W supply the full-count raw probability

    q_B(S)=c_B*f(S),
    c_B=det(I-lambda^2 W^2)*lambda^(2k),
    f(S)=haf(W_S)^2*haf(W_Sc)^2,       |S|=k.

Every source cycle starts before preparation/readout. Vacuum, collisions,
wrong number and invalid colors remain failures. No Pacc division appears.
The only normalization used here is P73's internally proved one.
The explicit rescaling W'=W/a and lambda'=a*lambda preserves Z;
a is not assumed1.

## 2. An exact classical latent rejection proposal

One classical raw trial is the following:

1. Draw S uniformly among the D oriented balanced subsets.
2. Independently draw TWO uniform perfect matchings on S and TWO on Sc.
   A uniform matching is direct: pair the least remaining vertex with a
   uniform other remaining vertex, remove both, and continue.
3. For each of the 2k matching-edge occurrences (including repetitions),
   pass an independent coin with probability W_ij/b. Return S only if
   all coins pass; otherwise record the failed prefix and no candidate.

There are m choices for each matching; every tuple has probability m^-4.
Conditional on that tuple, pass probability is the product of its weights
divided by b^(2k). Summing its nonnegative terms gives EXACTLY

    q_C(S)=f(S)/(D*m^4*b^(2k)).

No hafnian is evaluated by this algorithm. Products of two independently
chosen matching amplitudes are legitimate nonnegative latent weights.
This is a mathematical CLASSICAL control, not a physical distinguishable
Gaussian source, and does not assume independent photons in the optical
model. If W has zeros the same sampling identity still holds for b>0;
the finite-range certificate below needs a>0.

When sum_T f(T)>0, both conditional accepted laws are exactly f(S)/sum_T f(T).
This is automatic in the main strictly positive model; otherwise neither
conditional law exists when that sum is zero. Squeezing
lambda cancels there but remains in q_B and its source costs. The classical
acceptance rate can be small: this construction is not declared a rapid
or polynomial expected-time exact sampler for arbitrary W. Every latent
trial and failure is paid.

## 3. A source-independent sufficient coefficient comparison

The all-ones unit vector gives Rayleigh quotient at least a(N-1), hence
||W||>=a(N-1) and lambda<1/[a(N-1)]. All determinant eigenvalue factors
1-lambda^2 omega_i^2 are in(0,1], so

    c_B <= [a(N-1)]^(-2k).

Therefore the dimension/range certificate

    B(k,rho)=D*m^4*[rho/(2k-1)]^(2k) <= 1

implies c_B<=1/(D*m^4*b^(2k)), and q_C(S)>=q_B(S) for EVERY feasible S,
at every physical lambda, with no known optimum, training mask or choice
of favorable graph. In fact uniform feasible search already satisfies

    q_B(S) <= m^4*[rho/(2k-1)]^(2k) <= 1/D,

because haf(W_T)<=m*b^(k/2). Thus the certificate gives both an exact
conditional-law countercontrol and the simpler pointwise uniform screen.
The two statements are related consequences, not separate empirical wins.

This is a sufficient certificate. Failure of B<=1 proves no positive
advantage and does not refute either sampler identity.

## 4. Nonzero-strength asymptotic scope

The elementary factorial integral bounds used in P73 give

    m <= k*(k/e)^(k/2),       D<=4^k.

Consequently

    B(k,rho) <= k^4*(rho/e)^(2k)*[2k/(2k-1)]^(2k)
              <= e^2*k^4*(rho/e)^(2k).

For every fixed rho<e this tends to zero exponentially and is below one
for all sufficiently large EVEN k. This is a finite-strength bounded-
dynamic-range result, not merely a Taylor derivative at epsilon0. It is
uniform over all graphs/weights with that same ratio cap and all valid
source strengths. The actual finite k uses the exact B certificate;
the displayed coarse sufficient bound may be vacuous at small sizes.

For W=J-I+epsilon A with max A_ij<=Amax and epsilon>=0, the simpler cap
rho<=1+epsilon*Amax follows from a>=1. Any fixed cap
1+epsilon*Amax<e therefore falls in the stated asymptotic regime. If the
minimum exceeds1, using the actual a sharpens the criterion. No endpoint
rho=e assertion or all-epsilon/all-Gaussian theorem is made.

## 5. Adaptive search and costs

If every history uses a new source satisfying the same finite certificate,
q_B(S|history)<=1/D continues to hold. For any cost threshold below a
common initial incumbent, its sublevel hit hazard is at most its uniform
balanced fraction. Conditional survival induction gives best-cost
stochastic domination by T iid uniform feasible proposals after T fixed
raw attempts. All training attempts count. The controller never needs to
know a sublevel cardinality or C*: these are analysis notation only.

One latent classical trial uses a balanced subset, four direct matchings,
at most2k elementary coin tests and a score only if credited; graph reading,
normalization, RNG/bit precision, every rejected prefix and data movement
remain paid. With rational weights, exact Bernoulli implementation is a
separate bit-cost question; no constant-time arbitrary-real coin is assumed.
Uniform feasible search is an even simpler allowed control and can score
every draw. Classical candidates generated during any optical preprocessing
must be shared/accounted, not attributed as fresh optical successes.

The comparison is between credited candidates per raw mathematical trial.
It does NOT equate one optical pulse with one CPU operation or settle
matched wall time, energy, total photons, source compilation or parallel
hardware throughput. Those need actual ledgers. For repeated iid fixed W,
the classical accepted-law construction is exact but its expected trials
must still include all rejection; it is not an accepted-shot cost claim.

## 6. What changed and what remains open

P73's weak-order countercontrol extends here to an EXACT positive-amplitude
conditional-law construction and a uniform finite-strength/raw-count screen
for bounded amplitude range. These do not need the general P75 conjecture
or a new experiment. They close only the declared positive dense-pair source
class when its finite certificate passes.

Complex/sign-changing pair amplitudes remove the nonnegative latent-weight
identity and the positive Rayleigh lower bound used here. Zero-minimum or
large-range sparse sources may fail this certificate; that is an OPEN
boundary, not evidence of advantage. Correlated colors, non-Gaussian
preparation, displacement, accepting more count sectors, coherent mixers
and other encodings change the model and need new laws and full budgets.
The general six-mode Gaussian cap remains a different unresolved question.

KEEP the exact classical identity and finite certificate pending independent
review. REJECT free conditional-source claims in the certified class.
No positive optimizer result, novelty, held-out confirmation, physical
replication, manuscript revision or hardware authorization follows.
