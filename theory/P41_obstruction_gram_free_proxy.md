# P41/R3 — a Gram-free feasible comparator under loss

Status: self-derived, independent audit pending; elementary Cauchy/survival
ingredients are known. Scope is one fixed/common-state proposal or a frozen
sampling stage, not an automatic full adaptive-optimizer dequantization.

## Pointwise comparator without internal-state information

Inject k photons in distinct input modes of an isometry V. Their internal
state may be unknown, mixed or correlated, provided the normalized usual
distinct-input photon model applies. For any collision-free output set T,
let a_sigma=prod_i V_(t_i,sigma(i)). The unobserved internal amplitude is a
sum of k! terms, each multiplying a normalized internally permuted state.
For a mixed internal state, purify it and leave the purification register
unchanged. Hilbert-space Cauchy gives

    P_internal(T) <= k! sum_sigma |a_sigma|^2
                   = k! P_D(T).                            (1)

There is no assumption that internal distinguishability is described by a
known pure-state Gram matrix. The inputs must remain in distinct spatial
modes; arbitrary bunched inputs are not covered by this normalization.

Classically draw one independently routed output from |V_ia|^2 for each
input a. If all outputs differ, return their set. Otherwise return an
independent uniform feasible k-subset. This uses neither C* nor an optimal
mask. Its output law Q is always feasible and

    Q(T) = P_D(T)+P_D(collision)/binom(m,k)
         >= P_D(T) >= P_internal(T)/k!.                     (2)

All work is ordinary categorical sampling and a uniform subset draw. Naive
cost O(mk), or preprocessing plus alias draws, suffices; no permanent or
internal Hilbert tensor is computed. The fallback draw is charged. One may
always draw the fallback in parallel in the algorithmic schedule and select
it only on collision, keeping the number of high-level draws fixed.

## Fresh uniform loss

For exactly k injected photons, unconditioned physically useful probabilities
are eta^k P_internal(T) under independent uniform loss. Thus (2) dominates
pointwise when eta^k k!<=1. The condition is weaker than the sign-wave proxy
with known internal Gram, but it does not require that information.

For N>=k distinct injected inputs, genuine PNR-useful events have exactly k
survivors. Uniform loss commutes with passive optics, giving

    P_physical(T)=a_(N,k) E_R P_internal,R(T),
    a_(N,k)=binom(N,k)eta^k(1-eta)^(N-k),

where R is a uniform k-subset of source inputs. The source's residual internal
state after tracing lost photons may be mixed; (1) still applies. The classical
comparator first selects R uniformly, then uses the routing/fallback sampler.
Therefore Q(T)>=P_physical(T)/[k! a_(N,k)]. In particular

    k! a_(N,k) <= (N eta)^k,

so eta<=1/Nmax suffices uniformly for all N<=Nmax. This is a sufficient
condition, not a necessary threshold. It is also not a measured Lucy bound.

Threshold clicks masking extra surviving photons, recycling, dark counts,
classical completion from fewer photons and uncharged heralding are outside
this PNR-useful event definition. The provider's nonempty shots must not be
substituted for physical attempts.

## Cost and adaptation limitations

At a frozen circuit, every nonnegative feasible reward with failure reward0
inherits the pointwise comparison, including any retrospectively defined
optimal set. Cost ratios still matter: a classical draw can be slower than a
physical attempt, and the appropriate one-step or fixed-schedule rate/budget
inequality must be checked. Training and common preprocessing are charged.

Replacing a proposal inside an outcome-adaptive optimizer changes its future
history. (2) alone does not order entire adaptive runs, convergence rates or
finite-budget training trajectories. Exact thinning back to the optical law
could require unavailable probability evaluations. A trained circuit supplied
for free to a classical comparator also leaves a resource gap. These are
obligations, not assumptions to conceal in an impossibility claim.
