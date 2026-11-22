# P37: source selection for Haar-averaged threshold feasibility under loss

Base checkpoint: b5a1eba. This is a resource corollary of a known Haar law,
not a graph-optimization or quantum-advantage result. Proof author: Astra;
fresh independent review is outstanding. Numerical checks cannot supply it.

## Domain and external input

Let m>=8 be even and k=m/2. An attempt injects N distinct single photons,
k<=N<=m, independently of a Haar mode unitary. Uniform independent survival
has probability eta in (0,1). Acceptance means exactly k threshold clicks;
all attempts, including complete loss, count. Put

    h(l)=C(m,k)C(l-1,k-1)/C(m+l-1,l) for l>=k, and h(l)=0 otherwise,
    S_N(eta)=E h(L), L~Bin(N,eta), and b_N(eta)=S_N(eta)/N.

The lossless Haar formula is known: Bouland et al., arXiv:2312.00286v2,
Lemma1, Eq6. The loss mixture follows by commuting uniform loss through the
passive unitary and Haar-twirling each survivor sector. The previously audited
independent coefficient formula is in research/phase3_threshold_contract.md.
None of these facts is a project novelty claim.

Maximizing S_N concerns successes per attempt. Maximizing b_N concerns mean
successes per injected photon. N/S_N is an expected first-success photon cost
only for independently refreshed Haar draws per attempt, not for a random
interferometer drawn once and kept fixed. A fixed total photon budget is a
different optimization. Source preparation, programming and classical costs
are additional resources. Nonuniform loss, dark counts and conditional
all-photons-detected experiments are outside the claim.

## A one-crossing lemma

If a real sequence c_0,...,c_n has positive entries followed by negative
entries, with possible zero entries anywhere and both signs present, then
E c_R for R~Bin(n,eta) has exactly one zero in (0,1), provided its last
nonzero entry is negative. Its sign changes from positive to negative.

Indeed set t=eta/(1-eta). After removing the positive factor (1-eta)^n,
the expression is Q(t)=sum_r C(n,r)c_r t^r. Let a be the first index with
a negative coefficient. Q(t)/t^a is strictly decreasing for t>0: positive
terms have strictly negative powers, and negative terms have nonnegative
powers. It tends to +infinity at zero and to a negative limit or -infinity
at infinity. This proves existence, uniqueness and signs without invoking
an unverified root-counting theorem. Initial zero coefficients cause no issue.

For a fixed sequence of that sign form, zeros strictly decrease as n
increases, if all newly included coefficients are negative. At an interior
zero for n, compare the probabilities for Bin(n+1,eta) and Bin(n,eta):

    p_(n+1)(r)/p_n(r)=(1-eta)(n+1)/(n+1-r), 0<=r<=n.

This ratio is strictly increasing in r. Subtract its value at the sign
boundary times the old zero expectation: every remaining term is nonpositive,
and at least one is strictly negative. The additional r=n+1 term is also
negative. Thus the new expectation is negative at the old root, and its
unique root is strictly smaller. This argument concerns signed expectations,
not a claim that the coefficient sequence itself is monotone.

## Theorem 1: two per-attempt candidates

For 0<eta<1, S_N strictly increases through N=m-1. Its maximum over k<=N<=m
is attained among {m-1,m}. There is a unique a_m in (0,1) satisfying
S_m(a_m)=S_(m-1)(a_m). The maximum is uniquely N=m below a_m, uniquely N=m-1
above it, and those two tie at a_m.

Proof. For l>=k,

    h(l+1)/h(l)=l(l+1)/[(l-k+1)(m+l)],
    h(l+1)/h(l)-1=k(m-2-l)/[(l-k+1)(m+l)].

The differences d(l)=h(l+1)-h(l) are zero below k-1, positive for
k-1<=l<=m-3, zero at m-2, and negative at m-1. Couple one additional
input photon to obtain

    S_(N+1)-S_N=eta E[d(L)], L~Bin(N,eta).

For N<=m-2 all terms are nonnegative and at least one strictly positive
term has positive mass. For N=m-1 the one-crossing lemma applies to d(l).
The limiting sign at eta=1 is d(m-1)<0. This proves the assertion. At
eta=1 the known extra tie N=m-2,m-1 must be restored; eta=0 is excluded.

## Theorem 2: four per-photon candidates and their order

For 0<eta<1 all maxima of b_N lie in {m-3,m-2,m-1,m}. Write tau_j for the
unique interior solution b_(j+1)=b_j, j=m-3,m-2,m-1. Then

    0<tau_(m-1)<tau_(m-2)<tau_(m-3)<1.

As eta decreases from one to zero, the unique maximizer is respectively
m-3, m-2, m-1 and m on the intervals separated by these roots. At a root
only the two adjacent candidates tie.

Proof. Let g(l)=h(l)/l for l>=1, with g(0)=0. Binomial size bias gives

    b_N=eta E[g(R+1)], R~Bin(N-1,eta),
    b_(N+1)-b_N=eta^2 E[g(R+2)-g(R+1)].

For l>=k,

    g(l+1)/g(l)=l^2/[(l-k+1)(m+l)].

The numerator of this ratio minus one is
[m(m-2)-(m+2)l]/2. Its zero is m-4+8/(m+2), strictly between m-4 and m-3
for m>=8. Thus Delta g(l) is zero below k-1, positive for k-1<=l<=m-4,
and negative for m-3<=l<=m-1. Consequently b_N strictly increases through
N=m-3. Each of the next three adjacent differences has exactly one interior
root by the lemma, applied to c_r=Delta g(r+1). The second part of the
lemma gives the asserted root order. Above/below the corresponding root each
adjacent difference is negative/positive. The ordered roots therefore make
the finite candidate sequence strictly increase and then strictly decrease,
with precisely the stated boundary ties. No nonadjacent crossing can create
an omitted global maximum. At eta=1, N=m-3 is the known unique optimum.

## Boundary scaling: losses of order one photon

For fixed lambda>=0 and a fixed integer s>=1, take eta=1-lambda/m and N=m-s.
As even m tends to infinity,

    S_(N+1)/S_N -1 = (s+lambda-2)/(2m)+O(m^-2),
    b_(N+1)/b_N -1 = (s+lambda-4)/(2m)+O(m^-2).

Here constants can depend on s and lambda. This is not a fixed-loss asymptotic.
To justify the expansion, let T be the lost-photon count, Bin(m-s,lambda/m)
in the first identity and Bin(m-s-1,lambda/m) in the size-biased second.
Its fixed factorial moments are bounded, its mean is lambda+O(1/m), and
its exponential moment at any fixed positive argument is bounded uniformly
in m. For l=m-s-T>=3m/4 the exact ratios above give, uniformly,

    Delta h(l)/h(l)=(s+T-2)/(2m)+O((1+s+T)^2/m^2),
    Delta g(l)/g(l)=(s+T-4)/(2m)+O((1+s+T)^2/m^2).

Moreover h(l)/h(m-1)=1+O((1+s+T)^2/m) and
g(l)/g(m-3)=1+O((1+s+T)^2/m). One can bound these errors by summing the
adjacent lossless relative differences between l and the respective peak;
the peak-normalized values are at most one. A bounded number of terms above
the peak in the g case obeys the same bound. The event T>m/4-s has
exponentially small probability by the exponential-moment bound, and both
functions, as well as their adjacent differences, are bounded by a constant
times their own peak. Its contribution after peak normalization is negligible
compared with m^-2. Taking expectations in the coupling identities, dividing
by the mean of h or g, and using bounded fixed moments yields the expansions.
The exceptional l=k-1 term is wholly inside that negligible tail.

For any fixed epsilon>0 smaller than the proposed positive limit, evaluating
the two signs at lambda equal to the limit plus/minus epsilon and invoking
the finite unique-root theorem sandwiches each critical root. Therefore

    m(1-a_m) ->1,
    m(1-tau_(m-3))->1,
    m(1-tau_(m-2))->2,
    m(1-tau_(m-1))->3.

## Interpretation and remaining review

This is a finite source phase diagram and a boundary scaling for a known,
classically calculable ensemble marginal. Output symmetry makes the accepted
Haar-averaged k-subset uniform. Increasing feasibility supplies no graph-quality
enrichment. Fixed losses can make feasibility small even with optimal N;
the present proof does not quantify that exponential rate.

The exact validation is experiments/phase3_loss_source_probe.py under the
P37 contract. Its finite sign brackets do not prove the asymptotic or replace
the argument above. Fresh proof review and bounded exact prior-art comparison
remain necessary before promoting this to a paper contribution.
