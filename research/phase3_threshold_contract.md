# P3-T: photon budget, losses, and threshold decoding

Base: `8edfca70f03555479ea62ef9c49d727a27cc1861`. Isolated branch
`research/phase3-threshold`. This contract audits the uncommitted P2-A drafts in
the principal checkout without editing them. No manuscript, QPU, or shared-state
write is authorized here. Correctness is distinct from novelty.

## Exact target and domains

Fix m modes and a target k-click event, with 1 <= k < m. In balanced examples
m=2k>=4. Each attempt injects exactly N photons *before* an independent uniform
survival channel of efficiency eta, then observes threshold bits x_i=1 if at
least one photon is detected in mode i. Every failed attempt and all N injected
photons are charged. Dark counts, source impurity, nonuniform loss, and classical
repair/bit flips are excluded. Eta is transmission/detection survival after the
resource count; interpreting it as source-emission probability would change what
an injected-photon budget means.

There are two different source domains:

- The Haar theorem permits any fixed normalized N-photon state independent of
  the new Haar mode unitary, including bunched inputs with N>m.
- `ThresholdEvaluator(m,N)` prepares the first N input modes singly occupied and
  uses the existing even-mode simulator: its physical simulation domain is even
  m and 0<=N<=m. A theorem evaluated at N>m does not extend that implementation.

Minimal encoding uses N=k and accepts k threshold clicks; this is exactly
collision-free, loss-free detection. Redundant threshold encoding uses N>k and
accepts k clicks even when some photons collide or are lost. These encodings
have different input resources and acceptance maps. They are not identified with
one another or with an original ObliQ/BBS threshold-plus-flips implementation.

## Prior-work input and audited loss formula

Write D_N=binom(m+N-1,N). The known Haar click law is

    f_N(m,k) = binom(m,k) binom(N-1,k-1) / D_N,  N>=k.

It is Eq. (6), Lemma 1, of Bouland et al.,
[arXiv:2312.00286v2](https://arxiv.org/html/2312.00286v2), Sec. 4
(version 2025-03-19). Their n is our N and their c is our k. The Haar twirl
producing a uniform occupation law for any fixed input is also established in
Arkhipov–Kuperberg, [arXiv:1106.0849v1](https://arxiv.org/html/1106.0849v1),
Proposition 1 and Corollary 2. These are known results, not project contributions.

Set f_0(m,0)=1, and f_N=0 outside the possible click range. For 0<=eta<=1,

    F_N(m,k;eta) = sum_(L=0)^N binom(N,L) eta^L (1-eta)^(N-L) f_L(m,k).

Uniform loss commutes with passive mode unitaries. The survivor number is
Binomial(N,eta); conditional on L, Haar averaging makes the normalized survivor
state maximally mixed in the L-photon sector. This proves the mixture, including
bunched fixed-N inputs. It does not apply unchanged to a mode-dependent detector
channel or to a shot distribution conditioned on keeping all N photons.

An independent counting derivation starts with a uniform weak composition t of
N. For that t, the click-count probability generating polynomial is

    product_i [q^(t_i) + (1-q^(t_i)) z],  q=1-eta.

Averaging these polynomials gives the same F_N. Summing over all N and selecting
which k modes click yields

    F_N = binom(m,k) eta^k / D_N
          * [y^(N-k)] (1-y)^(-k) (1-q*y)^(-m),   k>=1.

For k=0 the result is q^N. This derives the second draft formula independently
of the survivor mixture. Summing over k gives one because the combined generating
function reduces to (1-y)^(-m). The bounded audit compares these three routes
using exact rational arithmetic, rather than only testing two similar floats.

## Operational propositions to audit

P3-T1 (lossless per-attempt optimum; known-law corollary). For m=2k>=4,

    f_(N+1)/f_N = N(N+1) / [(N-k+1)(m+N)].

The ratio is above, equal to, or below one according as N is below, equal to,
or above m-2. Thus the unrestricted positive-integer per-attempt maximizers are
N=m-2,m-1. A source cap must still be applied. This result says nothing about
positive loss or photon cost.

P3-T2 (lossless expected-photon optimum; formal corollary). The ratio of photon
efficiencies g_N=f_N/N is

    g_(N+1)/g_N = N^2 / [(N-k+1)(m+N)].

For balanced m=2k the sign of its excess over one is the sign of
2k(k-1)-(k+1)N. Consequently, over N>=k:

- m=4: N=2 uniquely;
- m=6: N=3,4;
- even m>=8: N=m-3 uniquely.

These maximizers lie below m, so the distinct-input source cap does not alter
this particular lossless conclusion.

P3-T3 (explicit loss/cost phase diagram; formal corollary). With m=4,k=2 and
source cap N<=4, writing e=eta,

    F_2 = (3/5)e^2,
    F_3 = (3/5)e^2(3-2e),
    F_4 = (18/5)e^2 - (24/5)e^3 + (12/7)e^4.

For 0<e<1 the per-attempt maximizer is N=4 below
b=(21-sqrt(21))/20, N=3 above b, with a tie at b. At e=1, N=2 and 3 tie.
For photon efficiency F_N/N, set a=(28-sqrt(154))/30. The maximizer is N=4
for 0<e<a, N=3 for a<e<3/4, and N=2 for 3/4<e<=1, with adjacent ties at the
two boundaries. At e=0 every success probability is zero, and no finite expected
photon cost is attainable. The statements follow by pairwise polynomial
factorization; they are not a new general optimization theorem.

In particular at e=1/2:

    (F_2,F_3,F_4) = (3/20,3/10,57/140).

N=4 beats the lossless plateau and minimizes expected injected photons among
the allowed N. If instead an all-N-detected gate is imposed, the probability
becomes e^N f_N. At N=4 it is 9/280, below the minimal encoding's 3/20. This is a
protocol-dependent ranking reversal. With threshold-only detectors the extra
all-N count is generally not observable for N>k; imposing it requires an extra
number-resolving/heralding assumption.

P3-T4 (expected cost versus fixed total budget). For an independent new Haar
unitary on every attempt and a fixed acceptance/quality set A of k-bitstrings,
let r=|A|/binom(m,k)>0. Output permutation symmetry gives success probability
q_N=r F_N. Conditional on k clicks, the Haar-averaged bitstring is uniform;
there is no graph-quality enrichment in this fact.

For a fixed N repeated until the first success, the expected injected-photon
cost is N/q_N. More generally any almost-surely successful adaptive choice of N
based on earlier failures has expected cost at least

    1 / max_N(q_N/N).

Proof: if I_j indicates that attempt j is reached, the number of successes up
to stopping is one. Conditional independence and nonnegative summation imply
1=E sum_j I_j q_(N_j) <= max_N(q_N/N) E sum_j I_j N_j. Repeating a maximizing N
achieves equality. This statement permits a declared photon cap and does not
charge interferometer reprogramming/classical work; those must be added for an
algorithmic comparison.

With a *fixed* budget B and stationary N the success probability is instead

    1-(1-q_N)^floor(B/N).

This does not generally select the same N. For example m=8,eta=1,B=30 has unique
per-photon maximizer N=5, but stationary budget success is larger at N=6. The
exact rationals f_5=35/99 and f_6=175/429 provide a cross-multiplication check.
Allowing different N within the finite budget gives the exact failure-probability
recursion S(B)=min_(N<=B) [(1-q_N) S(B-N)], with S(B)=1 when no admissible N
fits. This is a finite budget allocation problem, not variational graph solving.

The independent-Haar-per-attempt hypothesis matters: with a U sampled once and
then held fixed, expected first-success cost is E_U[N/p_U(A)], not N/E_U p_U(A).
For T repeats, the ensemble fixed-U success E[1-(1-p_U)^T] is at most
1-(1-E p_U)^T by concavity. A prescribed finite number of attempts has expected
success *count* T E p_U either way, but its first-hit probability and waiting
time cannot be inferred from the first moment alone.

## Experiment contract and falsification

Run `experiments/phase3_threshold_audit.py` in this worktree against the explicitly
identified principal-checkout drafts. No new dependency, remote service, or QPU
call is needed. All arithmetic comparisons of click laws and budget choices use
`fractions.Fraction`. Fixed seeds are used only for the small floating-circuit
checks. Hash the drafts, script, contract, and invoked simulator before/after.

Declared finite checks:

1. m=1,...,6, N=0,...,m+2, eta in {0,1/4,1/2,3/4,1}: normalize, compare known
   formula, survivor mixture, and direct uniform-occupation thinning at every k.
   This deliberately includes N>m for the theorem, not the distinct-input evaluator.
2. Compare both draft loss functions with exact rationals; check lossless maxima
   for even m=4,...,40 using a search cap 4m, including per-photon ties.
3. Exact operational sweeps for even m=4,6,8,10,12, eta in
   {1/4,1/2,3/4,9/10,1}, with source caps m and 4m. Report per-attempt, per-photon,
   stationary-B, and dynamic finite-B criteria separately. An N>m optimizer in
   the second cap is a source-demand result, not an implemented single-source input.
4. For m=4,N=0,...,4, three fixed random circuits and eta in {1/4,1/2,3/4,1},
   compare `ThresholdEvaluator` against an independent explicit sum over all
   detected Fock suboccupations, for bosonic and distinguishable photons.
   Record all comparisons and numerical tolerance; these checks are not proofs.
5. Exhibit the exact m4 loss/gate reversal and m8 finite-budget counterexample.
   Preserve any failed assertion rather than rewriting its values.

Acceptance: exact identities agree, floating checks agree within 1e-10, source
caps and protocols stay explicit. Reject any extrapolation from Haar count
improvement to graph-optimization benefit, novelty, or quantum advantage.

## Red-team boundary and continuation

All averaged output statistics used here admit an elementary classical sampler:
choose a uniform weak composition by stars and bars, independently thin its
photons, then threshold. This reproduces the Haar-*averaged marginal*, not the
joint law of a specified U and its samples or arbitrary trained interferometers.
Arkhipov–Kuperberg Theorem 5/Corollary 6 already relate the same mixed-state law
to a classical random-simplex multinomial model. The optimization over N and its
loss/gate crossovers are therefore operational corollaries of known counting.
No exhaustive novelty search or new-contribution claim is made.

KEEP the route as a resource/protocol audit. A nontrivial algorithmic continuation
must lock graph families, source state, decoder, loss model, N-selection/training
cost, and a total photon/attempt budget, then compare optimum-blind trained
encodings to independently reoptimized distinguishable and serious feasible
classical search. The present work does not satisfy those requirements or reopen
the manuscript/QPU gates.
