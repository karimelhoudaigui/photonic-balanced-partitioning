# P90 exact-source static mathematical review

**Primary verdict: proved as written, for the displayed analytic identities,
unitarity construction and full-raw-cost witness.** The prospective optimizer
hypothesis is explicitly unproved in the source and remains OPEN. This verdict
does not certify an initializer benefit, hardware readiness or novelty.

Audited source: `/Users/karimelhoudaigui/Desktop/pasqal/.local/p81-exact-review/research/P90_SOURCE_AWARE_NONFLAT_DESIGN.md`,
commit `c52afab21bd4a1d4645f359619e510f118cb944b`, SHA256
`b3c0b04c486f3368a0cbbc7e2030d8225d015f182cbfb00e0a9b63e0a0b2f173`.
All171 lines were read, including the scope/veto statements. No author file or
P82 artifact was changed. No code/import/AST/test, RNG, seed, numerical scan,
backend, DEV graph, external source, QPU or manuscript was used in this audit.

## Normalized claim and dependency map

The model has a real symmetric weighted graph on disjoint K-sets S,T, a lossless
K-mode receiver unitary V, one photon per occupied source input, and uniform
completion of receiver support to a feasible r-subset Y of T. B and D in (1)/(5)
share V, removed pair R and the same repair. The full splitter witness uses a
common probability0<p<1. Conditional formulas require a positive-probability r.
The toy's plain-text `K4` means K=4 and eight graph vertices, not the complete
graph K_4; its sole edge is s2--t2.

Dependency chain: normalized two-photon Fock probabilities + uniform repair
→ repaired pair/inclusion differences(1) → flat cross-edge barrier and cut
decomposition → (5). Independent port transport + label-blind splitting → (3).
Real swap deltas + Hermitian exponential → (4). A block-diagonal two-mode mixer
+ the complete splitter law → (6). These leaves were reconstructed by hand;
there is no load-bearing external theorem or numerical experiment here.

| Obligation | Outcome |
|---|---|
| Distinct-output permanent and bunched factorial normalization | passed |
| Uniform repair, repaired pair mass and inclusion sum | passed |
| Flat fixed-R cross-edge barrier | passed |
| Transported-column joint law, including nonuniform physical loading | passed under the stated label-blind/transport meaning below |
| Full-graph swap deltas, Hermiticity and pre-R construction | passed |
| Linear cut coefficient and exact conditional r2 mean | passed |
| All-attempt witness, including R=013 and remaining split sectors | passed |
| Positive optimizer/total-cost benefit, hardware capability, priority | not proved in source; out of this mathematical verdict |

## Permanent, repair and cost identities

Write u=V[:,i], v=V[:,j] for distinct occupied columns. For a≠b, B has probability
`|u_a v_b+u_b v_a|²`, while D has `|u_a v_b|²+|u_b v_a|²`. Their difference is
`2 Re(c_a conj(c_b))`, with c_a=u_a conj(v_a). At occupation2a, the normalized
bosonic amplitude is `sqrt(2)u_a v_a`, giving2d_a versus D'sd_a. There is no
missing2! factor and no conditional-on-collision-free denominator.

A bunch at2a keeps a and selects each other receiver with probability1/(K-1).
Thus the repaired pair difference is exactly
`2 Re(c_a conj(c_b))+(d_a+d_b)/(K-1)`. Since column orthogonality gives sum c=0,
the exchange contribution to inclusion of a sums to -2d_a; repair contributes
`((K-2)d_a+D)/(K-1)`. Their sum is `(D-Kd_a)/(K-1)`, proving (1).
Pair differences sum to zero: exchange sums to -D, repair to D. K≥2 is required;
at K2 both repaired outputs are the whole receiver set, so both differences
vanish. At disjoint column support D=0, they also vanish.

For flat V, d_a=1/K² and D=1/K, so every fixed-R inclusion difference vanishes.
That kills all S/T-cross-edge and one-vertex contributions to the r2 mean,
even for source-aware phases. Conditional receiving-pair differences can remain;
they are not a new scalable optimizer claim. With a single fixed flat V and
uniform removed pairs, even their averaged receiving-pair difference cancels by
row orthogonality. This strengthens, rather than defeats, the stated barrier.

Let B0=S\R. Expanding the cut directly gives
`A_R=w(B0,R)+w(B0,T)` and
`L_a=degree_(G[T])(a)-sum_(s in B0)w_sa+sum_(s in R)w_sa`.
The latter is exactly the source's `degree_T(a)+2sum_R w_sa-sum_S w_sa`.
The term `-2sum_{a<b in Y}w_ab` corrects double-counted internal receiver edges.
Taking the B-minus-D expectation cancels A_R and inserts (1), yielding (5)
with its stated sign and factor2. It is conditional on the specified R and V;
it has no guaranteed favorable sign and no implication about quench endpoints.

## Transported ports and the initializer

Fix G,S,V and a physical-port probability vector p_i independent of a uniform
source permutation sigma. If I is the physical transferred set, then R=sigma(I).
For every I of size r and every labeled r-set R, exactly r!(K-r)! permutations
map I to R. Consequently `P(R|r)=1/binom(K,r)` even when the p_i are unequal.
This is marginal over sigma, not a statement conditional on a fixed sigma.

Under `W[a,i]=V[tau(a),sigma(i)]`, the measured physical permanent/factorials,
then label transport and uniform completion repair, give exactly nu_R for every
I,sigma,tau realizing that R. Therefore summing their split weights yields (3),
without washing out the dependence of nu_R on the actual source labels.
For example, already at r1, `P(Y={a}|R={i})=|V_ai|²`; its source correspondence
is classical and is present in the same-V D law.

The necessary interpretation is explicit: the labeled V is fixed before R and
has no additional sigma-dependence beyond coordinate transport. If loading
instead belongs to labeled vertices and is transported as `p_i=p_(sigma(i))`,
R generally is not uniform. If sigma is fixed or correlated with the loading,
the uniformity argument also fails. Those are different hypotheses, not silent
extensions of (3); the source separately identifies vertex-dependent steering
as a classical feature. Uniform marginal R by itself never proves nu_R uniform
or independent of R, and V does not steer that marginal under these hypotheses.

For s∈S,t∈T, removing s changes the cut by -ell_s; adding t after that removal
changes it by ell_t+2w_st. Hence M_ai is the actual one-swap delta as stated.
The fixed priority pairing makes M square and real. Its symmetric part is real
symmetric and its antisymmetric part real skew-symmetric, so H†=H. Dividing by
the real positive max(1,||H||op) preserves Hermiticity; exp(-iH/...) is unitary.
All quantities use G,S and paid priorities before R, not a lucky observed split.
Carrying priorities and physical coordinate maps through relabeling preserves
the construction's intended meaning.

M exposes K² actual feasible one-swap costs. Materializing their masks/cuts,
crediting every scored candidate and giving the whole compiler/features to the
classical controls are substantive obligations, correctly required at source
lines70–79 and148–151. Their execution/cost is not proved by this design note.
Unitarity is guaranteed; nonflatness or useful exchange is not guaranteed for
every graph: on the empty graph M=H=0 and V0=I. Nor does (4) claim to generate
the illustrative mixer in (6). A shared-circuit D comparison is a diagnostic,
not independent D reoptimization or a fair total-cost conclusion.

## Complete witness, with the three-photon repair event

For the balanced mixer on0,1, jointly transferred inputs0,1 bunch under B with
probability1. D bunches with probability1/2 and otherwise occupies both outputs.
Inputs2,3 have deterministic identity routes. If at most one of0,1 transfers,
the full B and D count laws agree: there is no interfering photon pair.
The four remaining split sets exhaust all possible differences:

| R | B inclusion of t2 | D inclusion of t2 | B−D one-edge cost |
|---|---:|---:|---:|
| 01 | 1/3 | 1/6 | -1/6 |
| 013 | 1/2 | 1/4 | -1/4 |
| 012 | 1 | 1 | 0 |
| 0123 | 1 | 1 | 0 |

For R=013 a B bunch occupies either0 or1 plus the deterministic3. Completion
chooses one of the two empty modes, so it includes2 with probability1/2.
D needs its probability1/2 bunch first and then the same completion, giving1/4.
For R=01 the corresponding completion has three options, giving1/3 and1/6.
In these two cases s2 stays inside, so the edge cost is1 minus inclusion of t2.
If2 transfers, t2 is already occupied and s2 is removed, giving edge cost1 in
both models. This covers all16 split sets, including all collisions and fills.

Multiplying by the **unconditioned** splitter probabilities gives
`-p²(1-p)²/6-p³(1-p)/4=-p²(1-p)(2+p)/12`, strictly negative for0<p<1 and zero
at p=0 or1. There is no postselection or feasibility denominator. Equivalently,
the conditional r2 and r3 contributions are -1/36 and -1/16, multiplied by their
full binomial sector probabilities. Repaired vertices are scored classical
labels, not extra photons created in those empty receiving modes.

The witness's full PNR law factors into one at-most-two-photon interfering
block and two one-mode blocks. An exact two-photon-group classical control can
therefore reproduce the complete raw/repair/cost law, not merely its mean.
The one-edge cost is classically trivial, and no quench or optimizer benefit
is proved. The first missing positive implication remains a growing-sector
benefit over independently optimized D/groups and full-feature classical search
after all compilation, photon, routing, loss, decoding and scoring costs.

## Review provenance

This reviewer independently reconstructed the algebra from the exact raw source
and did not read another P90 review or the WIP checker. The reviewer authored
and executed P82a and knows its outcomes: this is **not** a blind-outcome review
or an independent-discovery claim. A fresh read-only child session, given only
this source without an author verdict or P82 outcomes, independently confirmed
(1),(3),(5),(6), including fixed nonuniform physical loading and R=013. It did
not review (4); the swap/Hermiticity check above is this reviewer's own.
No external literature attribution, experiment or universal positive theorem
is supplied by this report.
