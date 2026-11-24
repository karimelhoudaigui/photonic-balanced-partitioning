# P42 — independent threshold-sector reconstruction before author comparison

Reviewer/constructor p41_adaptive. Parent supplied the source card only:
m=2k graph modes, N single-input identical photons, fresh independent uniform
loss eta, passive U chosen from graph/prior history, and acceptance of exactly
k clicked modes with no others. This file is written before reading any
P42 author proof or parent computation. Shared P41/R3 context is disclosed.
No numerical command or QPU call was executed for this derivation.

## Precise hypotheses

Let k>=1 and m=2k. There are N distinct occupied input modes, each initially
containing one photon with the SAME pure internal state; hence N<=m when no
other physical modes exist. Assume k<=N<=Nmax, with any tighter physical
mode cap included in the allowed N set. N<k gives zero accepted probability.

The loss is the uniform passive pure-loss channel of survival eta, without
environment/which-loss information made available to choose the interferometer
of that same attempt. U may depend arbitrarily on the graph and the complete
PRIOR classical history. Uniform loss may be commuted before U. All survivor
output modes are observed; acceptance requires vacuum everywhere outside the
clicked support. There are no dark clicks, number fabrication, mitigation,+quantum memory, free retry, or classical completion from a shorter string.

This source/channel condition is stronger than knowing an average optical
transmission, or merely knowing the distribution of total survivor number.

## 1. Loss sectors from the environment, including their spectrum

Let I be the N occupied orthogonal input modes. For each a in I the loss
dilation maps its creation operator to

    sqrt(eta) a_a^dagger + sqrt(1-eta) e_a^dagger.

Expanding their product produces one system/environment basis pair for each
surviving subset J of I. Distinct lost subsets have orthogonal environment
Fock states. Tracing that environment therefore gives, in survivor sector ell,

    rho_ell = eta^ell(1-eta)^(N-ell)
               sum_(J subset I, |J|=ell) |1_J><1_J|.            (1)

Its trace is binom(N,ell) eta^ell(1-eta)^(N-ell), the binomial sector weight.
Conditional on ell, it is a uniform mixture of rank d_ell=binom(N,ell),
with eigenvalues1/d_ell. Photon indistinguishability does not remove the
orthogonality of different occupied-mode subsets J.

After passive U the sector is conjugated by its ell-photon Fock unitary.
Thus (1) remains a scalar times an orthogonal projector Q_ell of rank d_ell.
This argument uses no Haar average, objective value or optimal-state mask.

## 2. Exact threshold-support projector and its rank

Fix a k-element clicked support S. In sector ell>=k the occupation basis
accepted by ideal threshold detection is

    n_i>=1 for i in S, n_i=0 outside S, sum_i n_i=ell.

Subtracting one photon per clicked mode leaves ell-k indistinguishable photons
in k modes. Stars-and-bars gives the projector rank

    r_(ell,k) = binom(ell-1,k-1).                               (2)

For ell<k the projector is zero. Collisions inside S are INCLUDED; there is
no one-photon-per-click assumption. With no unobserved other modes, these are
all accepted Fock occupations for this support.

For any two orthogonal projectors P,Q,
0<=Tr(PQ)<=min(rankP,rankQ), by PQP<=P and QPQ<=Q. Therefore the unconditioned
probability for S at this fixed N obeys

    p_(U,N)(S) <= b_(N,k)(eta),
    b_(N,k) = sum_(ell=k)^N min{binom(N,ell),binom(ell-1,k-1)}
                                eta^ell(1-eta)^(N-ell).        (3)

This is a uniform upper bound, not an assertion that every projector overlap
can be attained by a passive single-particle U. Multiplying by an extra
binom(N,ell) would count the sector multiplicity twice. Conversely replacing
the threshold projector by rank1 would wrongly discard collisional outputs.

## 3. A photon-number-independent simple bound

For0<=eta<1, drop only the min in favor of r_(ell,k), the factor
(1-eta)^(N-ell)<=1, and extend the positive series to infinity:

    b_(N,k) <= sum_(ell=k)^infinity binom(ell-1,k-1) eta^ell
             = [eta/(1-eta)]^k =: b_simple.                   (4)

The equality follows by multiplying the k geometric power series, or the
standard coefficient count in (1-eta)^(-k). This bound is uniform in N;
at eta=0 it is zero. At eta=1 the exact finite cap (3) remains meaningful
but (4) is not used. A bound larger than1 is merely uninformative, not a
probability. Always cap probability upper bounds by1 where appropriate.

For bounded allowed N use b=max_N b_(N,k), which can improve (4). The maximum
cannot silently be assumed to occur at Nmax without proving monotonicity.

## 4. Uniform feasible search and all adaptive best-cost thresholds

Let Omega be the D=binom(2k,k) balanced supports. Uniform feasible sampling
returns each S with probability1/D. It requires no score or optimum to
generate the candidate. For ANY fixed target set A subset Omega, (3) yields
at every matching prior history

    Pr(next optical candidate belongs to A | history) <= |A| b.

When the right side is below1, failure-history induction gives

    Pr(any optical candidate in A in nQ attempts)
           <= 1-(1-|A|b)^nQ.                                (5)

This holds despite arbitrary adaptive choices because the cap b is uniform
in histories and does not require a second algorithm to share those histories.
Uniform classical draws have exact target-hit probability

    1-(1-|A|/D)^nC.                                         (6)

For nC>=1,nQ>=1 put L=ceil(nQ/nC). The sufficient condition

    L D b <= 1                                              (7)

implies L|A|b<=|A|/D<=1 for every A, so integer Bernoulli gives domination
of (5) by (6), simultaneously for EVERY A. In particular take
A_z={S:C_G(S)<=z}. The classical best observed cut is then no worse in
first-order stochastic order than the best optical-stage cut, even for
adaptive controllers. The objective need not be a cut or complement-symmetric:
this proof works for every fixed real-valued cost on Omega.

If a common fixed frontend supplies an incumbent c0, both methods retain it;
for z>=c0 the best-cost event is automatic and for z<c0 the argument above
applies unchanged. Frontend discoveries/costs remain separate. A frontend
that adapts using optical measurements is not thereby a common initial stage.

This is stronger than merely pointwise-domination by a DIFFERENT classical
proposal at each circuit: here the comparator is the SAME uniform distribution
at every history. Thus the adaptive branch-trap non-extension from P41/R2
does not invalidate (5)-(7). No probability thinning or hard permanent ratio
is needed to run the classical comparator.

## 5. Explicit small-survival criterion and integer cost model

Using (4), a sufficient exact finite criterion is

    L binom(2k,k) [eta/(1-eta)]^k <= 1.                       (8)

Since binom(2k,k)<4^k, eta<=1/5 implies D b_simple<1, giving the one-for-one
attempt comparison for every k>=1. For eta<1/5, the more conservative simple
condition

    L <= [(1-eta)/(4eta)]^k

allows exponentially growing primitive cost ratios. The exact binomial
coefficient in (8) is stronger, including at the eta=1/5 boundary. eta0
is handled directly, without dividing by eta.

For remaining deterministic resource budget B, fixed primitive costs or
guaranteed upper-classical/lower-optical bounds give
nC=floor(B/cC), nQ=floor(B/cQ). Use their ACTUAL ceiling L in (7)-(8).
If nQ=0 domination is trivial; if nC=0<nQ no such certificate follows.
A ratio of mean measured times cannot replace these finite count conditions.
Cost units remain physical fresh attempts, injected photons, graph-score
queries and CPU/wall time; their conversion requires explicit accounting.

## 6. Falsification of broader readings

**Heralded current losses.** If the surviving subset J is revealed and U is
then chosen from that same-trial record, rho_ell conditional on J is pure,
not rank binom(N,ell). With N3,k2, routing the two identified survivors to a
fixed S whenever exactly two survive gives mass at least3eta^2(1-eta).
At eta1/10 this is27/1000, while (3) for the nonheralded N3,k2 case is1/100.
This breaks the broadened history interpretation, not the unheralded theorem.

**Bunched source.** Put four photons in one input and split that input equally
between two selected outputs. At eta1/10, the probability both are clicked is

    1-2(19/20)^4+(9/10)^4=2167/80000 > 1/81=b_simple.

Thus distinct single-occupation source modes are essential. The separate P41
grouped-Fock theorem does not grant this threshold result for bunched inputs.

**Other detector/internal models.** Dark counts, undisclosed output-mode
filtering, source multiphotons, or partial internal distinguishability change
the relevant POVM/state. Rank (2) is the spatial Fock rank for identical
photons; it cannot be silently applied to a detector ignoring a larger internal
Hilbert space. No monotonic worst-case claim in distinguishability is assumed.

**Nonempty vendor shots.** Conditioning away vacuum or other rejected events
divides by a success denominator. Such records are not unconditional attempts
and cannot instantiate (3)-(8) without restoring the missing cost/denominator.

**Changed decoding.** Mapping click supports many-to-one to a graph candidate,
completing <k clicks, or using unobserved ancilla modes changes the projector
or target preimage multiplicities. The stated cap and counting space must
then be rederived, not inherited.

## Status and independence

This is an internally derived candidate proof of (1)-(8), not a numerical
verification or novelty assessment. It is ready for exact author comparison
after this independent file is committed. No P42 author source was read before
this reconstruction. No actual Lucy loss parameter, internal-state calibration
or primitive-cost bound was established here. These regime assumptions cannot
be declared measured merely from a correct theorem.
