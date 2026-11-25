# P72 accepted: low-rank Hamiltonian transport at finite normalized time

25 November 2026. ROOT read all310 author lines,247 independently derived
lines and119 exact-review lines. The static theorem is accepted, using
the separately accepted P71 unitary approximation lemma. CLAIM-042 is OPEN.

Author `research/P72_low_rank_Hamiltonian_finite_time_transport.md`,
root8ab1e6c, SHA256
`f48f7cd39d67788635e8da60d84ebae7125a059f51a48079c49486bde035b76f`.
Independent `theory/P72_independent_finite_time_transport.md`, original3329c6a/
rootf25407d, SHA256
`c441aecb7a9b18539fa0764db39c15283e5edc9ffb590e30efddaf41e6c1c34a`.
Exact review `theory/P72_AUTHOR_EXACT_HASH_REVIEW.md`, original8df6dd8/
rootcc98f77, SHA256
`c16fbea54f96233156169ef2aab29a358189e690d99ce8fae5ffcd98016d3494`.
ROOT supplied the question and candidate route. The independent note's
historical conditional P71 status remains untouched; current P71 exact
reviewcd59bcf resolves that dependency for this acceptance.

## Accepted implication and asymptotic scopes

Let H=[X,Z;Z^dagger,Y] be Hermitian with rank(Z)<=h and
tau=|t| ||H||. For Taylor degree p, all ranges of (H^j)_AB,1<=j<=p,
lie in the COMMON block-Krylov span of X^a range(Z),0<=a<p. Its dimension
is at most ph, not p^2h. With q=ph below the block dimension, this implies

    s_(q+1)(exp(itH)_AB) <= E_p(tau),
    E_p(tau)=exp(tau)*tau^(p+1)/(p+1)!.

The Taylor polynomial only supplies a rank approximation and singular-value
estimate. P71 then constructs a UNITARY comparison circuit, giving for the
P69 source/targets

    P(good) <= min(1,p(L,q)+sqrt(2)K E_p(tau)).

The p=0, h=0 and t=0 endpoints are treated explicitly. For fixed h>=1,
choose p=floor(alpha L/h),0<alpha<1. If tau=o(L), the tail is
exp[-omega(L)], giving P(good)<=exp[-L I(alpha)+o(L)]. A small linear
window tau<=cp works when c+log(ec)<0. If h grows, h=o(L) and
tau=o(L/h) guarantee only the stated exp[-omega(L/h)] tail; calling
this automatically exponential in L would be false. The proof preserves
examples showing why its tail certificate may be weaker in that regime.

This concerns one STATIC H during an attempt. General time-dependent
segments need another argument. Tau is dimensionless and includes local
Hamiltonian scales; it is not elapsed CPU or QPU time. Predictable-history
optimization corollaries retain P66's shared bad warmstart, acceptance/gap,
thermal terms and uniform conditional time/rank hypotheses. No generic-start,
all-graphs, measured-cost, positive optimizer or novelty claim is accepted.
