# P94 independent parity-mechanism proof audit

Reviewer `/root/p66_dark_audit`, 2026-11-26; `proof-audit` workflow.
Primary verdict: **PROVED AS WRITTEN** for A1, A2, the bounded additive-mean
control, and the finite RAW Walsh frontier, within their stated model/cost scope.
This is not a proof of efficient full-law replacement or optimization advantage.

Exact source: `research/P94_MECHANISM_PORTFOLIO.md`, all 120 lines, at
`b2b15069acbfd4257996f78fd0609258142df41d`, SHA256
`80d3252cf45b50eaf3be202c0c7482c86a9fb21b50284ae324e054b3a34c5925`.
This is an independent reconstruction after reading the frozen proof;
agreement of reviewers is not evidence in place of the arguments below.

## Claim card and dependencies

Inputs are K known, distinct singly occupied modes (CF input), vacuum elsewhere,
and a passive vacuum-environment channel T. All output counts are retained.
For a fixed binary mask r, Q selects accessible output modes, and
chi_r=(-1)^(sum_selected n). Fully distinguishable particles start independently
in those same input modes. The species variant assumes a product of CF species
states, not arbitrary entangled internal states. The A2 support theorem instead
assumes ideal lossless passive optics, m>=K, and independently permitted groups
of size at most two. Masks, pairing, graph and decoder are fixed/paid objects.

Dependency graph (all leaves reconstructed internally, not external citations):
vacuum dilation -> creation-operator contractions -> A1 -> contraction norm ->
bounded signed estimator -> additive mean control;
photon conservation + HOM blocks -> A2 -> convex hull -> linear-cost consequence;
paired-spin edge identity -> character aggregation -> parity-coordinate reduction
-> unnormalized Walsh transform -> paid RAW frontier.
No numerical result, prior literature priority, or P90a outcome is a proof leaf.
Obligation matrix: A1 / estimator / A2 / witness / RAW Walsh bounds **passed**;
finite-bit error and measured runtime **not addressed**; literature priority,
hardware realization and optimization-advantage acceptance **out of scope**.

## A1: full raw parity, including loss — passed

Put V=[T_A; E_A], with E_A^dagger E_A=I-T_A^dagger T_A, so V^dagger V=I.
The output pure state is product_j b_j^dagger|0>, where
b_j^dagger=sum_a V_aj c_a^dagger. Distinct occupied input modes give unit norm.
Parity lifts the one-particle reflection Z=diag(I-2Q,I_environment).
Expanding the K creation/annihilation contractions gives one term for each
permutation, hence <chi_r>=per(V^dagger Z V)=per(I-2 T_A^dagger Q T_A).
There is no K! divisor: every input occupancy factorial equals one.
Tracing the environment equals using identity there; no survival event was
conditioned upon. Independent labeled particles multiply their individual
expectations, giving product_j(1-2X_jj), X=T_A^dagger Q T_A.
Independent species multiply the principal-block permanents for their groups.
This identity does not apply unchanged to repeated occupied inputs or a general
internally entangled source; neither is assumed in the claim.

## Signed estimator and arithmetic costs — passed

For K>=1 let M=I-2X. Since 0<=X<=I, M is a Hermitian contraction and per(M) is
real (conjugation gives per(M^T)=per(M)). For independent Rademacher x_j define
Z(x)=(product_j x_j) product_i(Mx)_i. In its expansion a surviving monomial
requires every selected-column multiplicity to be odd; K selections distributed
among K positive odd multiplicities force every multiplicity to be one.
Thus E Z=per(M). AM-GM gives
|Z| <= (sum_i |(Mx)_i|^2/K)^(K/2) <= 1.
Apply concentration to Y=Re Z, not directly to a complex ordered interval.
For Y in [-1,1], the centered log-MGF has second derivative at most one,
so log E exp(t(Y-EY))<=t^2/2. Independent repetitions and the two Chernoff tails
give Pr(|mean Y-per(M)|>epsilon)<=2 exp(-n epsilon^2/2).
No complex-deviation bound with this same prefactor is claimed or needed.

For d nonzero aggregated characters, construction costs O(d m K^2), in addition
to graph/mask/mesh setup. Dense matrix-vector products cost O(d K^2) per shared
sign vector, plus K fresh random bits. A union bound across characters needs
n>=2 epsilon^-2 log(2d/delta); independence between characters is unnecessary.
Exact small-permanent evaluation alternatively costs O(d K 2^K) after setup.
For direct cost estimation, Y_C=b0+sum_r b_r Re Z_r lies in [b0-B,b0+B],
B=sum_nonzero |b_r|. Therefore its absolute-error tail is at most
2 exp(-n epsilon_abs^2/(2B^2)); B=0 is the exact constant-cost branch.
Nonnegative edge weights give B<=sum_e w_e/2. Accuracy relative to total edge
weight therefore has no exponential-in-K sample bound in this arithmetic model.
This is signed mean estimation, not positive-law sampling or relative accuracy
for rare events. Finite precision, random-bit generation, adaptive training and
reused fitted randomness require separate paid/error arguments.

## A2: support and zero expressivity gap — passed

Let h=|p|<=K and K-h be even. Send h individual occupied inputs to the h desired
odd output modes. Partition the other K-h inputs into pairs and give each pair
its own two-output balanced splitter, disjoint from all preceding outputs.
For its CF input, a^dagger b^dagger becomes, up to phases,
((c^dagger)^2-(d^dagger)^2)/2, i.e. normalized |2,0>-|0,2> over sqrt(2).
Both outcomes have even parity in both outputs. Exactly h+(K-h)=K modes suffice;
input/output permutations and identity on unused modes extend this to a unitary.
The construction is deterministic in PARITY, not in full counts. It works with
groups<=2 and also with full indistinguishability because the blocks are disjoint.
Conversely K=|p|+2 sum_a floor(n_a/2), proving necessity of the stated support.

Every full-B parity law is consequently a mixture of these deterministic
parity laws, using its own probability at each p as mixture weight. For any fixed
cost f(p), min_U E_B f = min_U E_group<=2 f = min_supported_p f(p): both classes
can prepare each parity, and expectations cannot beat their support minimum.
This is an existence/expressivity statement. It neither computes that minimizing
p nor supplies the mixture weights efficiently, with matched runtime or resources.
Finding a solution classically and preparing its parity is no optimization gain.
It gives no theorem for a prescribed lossy T or restricted fixed-species hardware.

## Four-photon witness — passed, but falsified as an advantage witness

With the occupied Hadamard row uniform, M=I-J/2 and
per(M)=1-2+3-3+3/2=1/2. Principal blocks give respectively 1/4,1/8,1/8,1/16
for species 2+2,3+1,2+1+1 and 1+1+1+1 at that same mesh.
For independently optimized D on four occupied/four total modes, q_j>=0 and
sum q_j=1. If any q_j>1/2, product_j(1-2q_j)<=0; otherwise its nonnegative
factors sum to two and AM-GM bounds the product by (1/2)^4=1/16.
A HOM pair with row probabilities (1/2,1/2,0,0), plus routed singleton photons,
has parity expectation one. Same photons/modes, groups<=2: the D separation
does not survive this stronger control. Extra vacuum modes invalidate the D
upper bound: a row disjoint from all occupied inputs already has expectation one.

## Walsh aggregation, support restriction and limits — passed

Each edge contributes w/2 to b0 and -w sigma tau/2 to b_(q_j xor q_l).
For an edge inside one vertex pair, sigma tau=-1 and the mask is zero, so the
two constant contributions sum to w exactly. Zero characters between distinct
pairs must likewise be aggregated into b0; they cannot be discarded as edges.
For lossless even K and m>=1 write x=p_1..p_(m-1), p_m=xor_i x_i.
Then chi_r(p)=chi_(r_<m xor r_m*1)(x). Aggregate these aliases BEFORE taking an
unnormalized length-2^(m-1) Walsh transform; no probability normalization factor.
Odd K instead has p_m=1 xor xor_i x_i and adds the coefficient sign (-1)^r_m.
Even support filtering uses |x|+(|x| mod 2)<=K; odd filtering uses
|x|+1-(|x| mod 2)<=K. Scanning/popcount costs O(m 2^(m-1)) naively,
already within the stated transform order for m>=2, not a free omitted step.
m=1 has only one coordinate-fixed parity and needs a constant-work branch;
m=0 is only the trivial K=0 vacuum. K=0 may always bypass the table entirely.
For general loss there is no fixed parity hyperplane: use m bits and, if desired,
|p|<=K. This is an outer reachable-support bound, not exact reachability for T.

The work bound includes O(|E|m) coefficient aggregation and O(m 2^(m-1)) table
work; table workspace is O(2^(m-1)) beyond given graph/masks. Decoding/writing an
actual N-vertex witness also costs Omega(N), and integer/rational bit sizes count.
At m=24 one eight-byte table has 2^23 entries =64 MiB; this is no RSS benchmark.
After a fully paid support scan the minimum dominates every RAW code candidate.
Nonlinear quench can leave the code: dominating its endpoints requires paying
those descents too. The sparse-character mean estimator does not automatically
estimate quenched cost, best-of-run, tail probabilities or adaptive trajectories.
A common fixed parity-only postprocessor does preserve the convex-hull identity;
a full-count/history-dependent policy is not supplied a free replacement by A2.

Boundary verdict: K=0 gives per(empty)=1 and fixed vacuum decoding; K=1 has no
HOM pair and the estimator is constant. Odd K and arbitrary vacuum loss are
covered only as distinguished above. No load-bearing source or computation was
assumed; literature priority remains a separate review. No B raw, import, AST,
RNG, numerical execution, native call, test, runner, QPU or manuscript action
occurred. The remaining gap is an efficient, optimum-blind, fully costed search
benefit against these controls, not a missing parity-expression identity.
