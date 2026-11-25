# P55 proposal: balanced neutrality of photon defects

25-Nov-2026. STATIC proposal/proof, no graph, sampler, physical or Monte Carlo
draw, pilot or new optimization result. ROOT authorizes a short INTEGER DECODER
prototype plus exact synthetic qualifications after this card is frozen; no
import/test execution before new source freeze, review and exclusive slot.
This is a real change from ranked-count decoders, not a P52 rerun. P52/P53 data
and the existing manuscript remain immutable; their narrower mean statements
do not establish or refute this proposal.

## Decoder and one falsifiable future question

For even N>=2, K=N/2, measured nonnegative INTEGER counts n=(n_0,...,n_(N-1))
and M=sum n, define

    error_n(S)=|2 sum_(i in S)n_i-M|,  |S|=K,
    A(n)=ALL K-subsets minimizing this error.

Return a UNIFORM element of A(n). Every physical attempt returns a balanced
partition, including vacuum, odd M, bunching and loss. Do not condition on
error0, M=N, collision freedom, detection or a favorable graph cut. No graph
weight, optimum/mask, previous partition or cut query enters the decoder.

One future question, not a benchmark authorized by this card: for a
graph-dependent passive walk U_G(t)=exp(it H_G), (H_G)_ij=sqrt(w_ij), diagonal0,
full-CF source r=N, can FINITE coherent multi-defect correlations under this
neutrality decoder improve fresh feasible-cut performance beyond fully retuned
D, b4, the existing Bose-inclusion/phase/product-marginal controls and strong
classical search at matched total costs? Mere small-t improvement is explicitly
NOT a positive: its whole leading gain has a classical replacement below.
No N8 runtime claim:70 partitions are trivial. A later panel must be larger
(e.g. N>=20), prospectively frozen with fresh labels/seeds/budgets/held-out
gates, not chosen from outcomes. No graph family/grid or pilot is fixed here.

The mechanism being tested is conservation across graph flows: a doublon and
a hole from an internal transfer should be co-clustered, rather than placed
on opposite sides by topK. At finite t, permanents coherently combine distinct
multi-photon transfer paths with the same observed defects. A useful signal
would have to survive classical occupation stimulation, one-mode shape and
all preparation/decoding explanations. Disconnected-community conservation is
also present in D and classical flows and is NOT an interference advantage.

## Exact DP and uniformity proof

Let F[i,k,s] count subsets of the FIRST i vertices of size k and photon sum s.
Initialize F[0,0,0]=1 and other entries0. Recurrence:

    F[i,k,s]=F[i-1,k,s]
        + 1_(k>=1,s>=n_(i-1))*F[i-1,k-1,s-n_(i-1)].

Compute d=min{|2s-M|:F[N,K,s]>0}; retain ALL target sums with this d and set
Z=sum_(s:|2s-M|=d) F[N,K,s]. Z>0 because K-subsets exist. Do not select target
sums uniformly unless their counts are known equal. Instead draw ONE exact
uniform integer r in[0,Z), select a target by its cumulative count, and unrank
backwards using exclude-block size F[i-1,k,s] then include-block size
F[i-1,k-1,s-n_(i-1)]. Subtract earlier block sizes and update k,s on inclusion.

These blocks partition the solutions bijectively. Each final subset therefore
has one integer rank and probability1/Z. No floating count ratios or repeated
physical-shot rejection is involved. A caller RNG must supply uniform arbitrary-
size randbelow(Z); float uniform*Z and fixed64-bit integer APIs are not generally
valid. The integer rank interface makes every mock route exhaustively testable.

At K=N/2, S->complement sends sum s to M-s, preserves error, and is a bijection.
The full output law is complement symmetric and equivariant in vertex labels;
same-seed unranking order is not a pathwise relabeling claim. When M is odd,
d is odd but need not be1. No exact-neutral subset may exist, and minimum-error
fallback is the rule, not a discarded event. M0, M1 and all-bunched counts give
UNIFORM ALL K-subsets. Counts all1 do too. A single doublon/hole with N>=4
has error0 exactly when their endpoints are on the SAME side.

DP construction is O(N*K*(M+1)) integer additions, with full-table O(N*K*(M+1))
integer storage for backwards unranking. Entries are at most C(N,K), with
O(N) bits, so bit work/storage can carry another O(N) factor. This classically
paid work, random-bit generation, validation and the final cut score cannot
be treated as free photon processing. Python integers prevent combinatorial
overflow; do not assume64-bit counts. Synthetic N70/M0 already exceeds64 bits.

Prototype resource domain, fixed before code:2<=N<=128 even,0<=M<=4096,
(N+1)*(K+1)*(M+1)<=2,000,000 cells before allocation. The mathematical rule
has no such bound; an out-of-domain attempt is a retained RESOURCE FAILURE,
not a resampled photon event or a favorable-subpopulation result. Allow M>N
within those bounds: independent product marginals are not fixed-total counts
and must not be silently conditioned back to N. No Gaussian float input.

## Analytic small-hop discriminator: a benefit, but classical at leading order

The gain statement assumes fixed even N>=4, ideal full-CF input, real symmetric
H_ij=sqrt(w_ij), w>=0, H_ii=0 and ordinary balanced graph cut C_w(S). Let pi be
uniform balanced subsets, p=N/[2(N-1)] its edge-crossing probability and
u=1-p=(N-2)/[2(N-1)] its same-side probability. Let mu=E_pi C_w.

One quantum hop j->i creates n_i2,n_j0, others1 with probability
2t^2 w_ij+O(t^4). Both orientations combined have4t^2 w_ij. The new decoder
then gives pi conditional on the endpoints being UNcut. The unchanged all1
event gives pi. Consequently

    P_B(S;t)=pi(S)*[1-(4t^2/u)(C_w(S)-mu)]+O(t^4),
    E_B C_w=mu-(4t^2/u) Var_pi(C_w)+O(t^4).

Real H makes count probabilities even in t; the remainder is for fixed N/H,
not a uniform-in-N performance bound. Complete/constant-cost cases have zero
variance and no asserted gain. For N2 every balanced cut cost is constant and
u=0, so this formula is not used. If H_ij=w_ij instead, the coefficient uses
Cov_pi(C_w,C_(w^2)); its sign is not universal. The sqrt coupling is explicit.

The classical leading replacement samples an edge with weight w, forces its
endpoints to the same side, and fills the remaining balanced membership
uniformly, mixed with pi at the same rare-event rate. D at time sqrt2*t has
the same leading decoded law. The existing P45 inclusion control, with rates
w_ij*n_j*(n_i+1), at Markov time tau=t^2 matches the ENTIRE count law through
this order. These are mandatory nulls, not new discoveries or accepted
interference gains. See research/P45_encoding_contract.md and immutable
P45_encoding_full_fock_probe.py; do not rebuild that known baseline here.

For ANY full-CF unitary, mu_B=mu_D=1 and Cov_B=2 Cov_D=2(I-QQ.T).
Continuous neutral-discrepancy decoding is invariant under a positive global
scale: correctly coupled Gaussian B/D fluxes therefore have the SAME law.
Integer rounding can break that equality; the integer prototype does not
accept generic Gaussian vectors. A later Gaussian-incidence control must
declare its solver/quantization/resolution/cost and never call a rounding
artifact a covariance advantage. Retain the product-B-marginal count control
because one-mode discreteness is a separate possible explanation.

The known efficient linear-count CDF theorem does not directly sample this
decoder: P(S)=E[1_(S in A(n))/Z(n)] contains a global count-dependent normalizer
and minimum over all subsets. That is not one fixed linear count CDF. This is
NOT a hardness/no-go statement; linear-CDF-based classical surrogates remain
relevant, with approximation and cost charged. ROOT source applicability note
theory/P53_linear_statistics_scope_check.md records the checked narrow theorem.

## Qualification and hardware boundaries

First prototype ONLY: compact pure-integer DP/unranking (<=150 source lines),
no graph, sampler, LP or optics. Tests will exhaust ALL input compositions
with M<=N and all mock ranks for N2/4/6, plus explicit vacuum/odd/bunch/defect,
complement/relabeling, M>N, arbitrary-integer and preallocation guard fixtures.
Freeze code/tests/contract before import; ROOT review and explicit exclusive
slot precede the unique targeted qualification. No pilot is chained to PASS.

This decoder requires actual photon MULTIPLICITIES (PNR), not threshold clicks.
docs/LUCY_TGCC.md and LAURENT_HANDOFF keep provider PNR/source maximum UNKNOWN.
Full r=N is an ideal source assumption, not a verified provider capability.
No hardware-compatible label, QPU green light, hardware preparation or paper
revision follows this proposal. Losses may change total M and every such shot
still decodes; the small-hop gain proof itself is eta1 only. All emitted
photons, failures, attempts and classical DP work must be paid in any later
experiment. Positive held-out/independent-replication/resource/hardware gates
remain unmet; the broader scientific goal is OPEN.
