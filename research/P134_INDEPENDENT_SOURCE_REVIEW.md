# P134 — Independent frozen-source review

2026-11-26. Non-author STATIC audit, parent 3f735a63902e600998630f6d972edbb88233272a.
FULL frozen package c44338937f3cd49012d5291492075b83af0c2129 read:

| research/ file | Lines | SHA256 |
|---|---:|---|
| P134_rational_frame_discriminator.py |513| 0f9dce56cecac9d7701953577adce1d5bf0c6cc2807083eca45c3ba47f1856f3 |
| P134_POPULATION.md |132| 182499dfc7170a4c048ce219ca3f0a66c12326cdbc5a8c9833d38da17eb6dda8 |
| P134_contract_TEMPLATE.json |32| fa588fa6815d5d3989e90efdeb59b040c060983aa63aa0eb3613ac3f842e02ce |

All 677 lines and three blob hashes checked. FULL P134 design (128 lines) at c9cbb758,
P133 reflection (93 lines) at f0930074 and ROOT checkpoint 9ef2b3d were also read.
The three source-pinned design/checkpoint hashes match their exact blobs.
No import/AST/evaluation, graph draw, RNG, numerical/native test or raw preview.

**STATIC ACCEPT, conditional on completing the distinct active v2 manifest.**
No blocking mathematical or implementation error found. The inactive TEMPLATE
does not itself satisfy all v2 randomness fields: see the precise condition
below. No qualification or launch follows from this review.

## Physical construction and independently checked amplitudes

C arithmetic is exact Q(i) with rational real/imaginary coordinates. Its
division uses the complex modulus squared, with the correct conjugation sign.
Gauss-Jordan inversion preserves the pivot row, checks both inverse products,
and stores its input/work/answer in failure state. Sizes are bounded by four.
The frame is formed from public prototype marks, weights, d and W ONLY.
Although the graph object later contains scores, build_frame never reads them.
No minimum/argmin, optimal-state mask or known optimal partition is used.

I reconstructed H=F^dagger F, Q=(I+H)^-1, T=2FQ, D=(I-H)Q and
V=[F;-I]. The source constructs U=I-2VQV^dagger, not an inverse-root variant.
Its occupied LAST four columns are [T;-D], with signal rows 0..5 and dump 6..9.
The exact Hermitian, full unitary, occupied-column and Gram-completion checks
are recorded BEFORE rejection. Matrix operands also survive construction errors.
This establishes the modeled static instrument, not measured device fidelity.

The row/source-subset DP assigns each row to an unused labeled column. Ryser
instead sums products of row sums over nonempty column subsets, with sign
(-1)^(n-|subset|). Both return one for the empty permanent and enforce n<=4.
For species groups, convolution allocates disjoint output subsets of the
correct group sizes; all subsets retain sorted indices and the cache keys agree.
Its product of squared species permanents is independently checked against
24 path amplitudes bucketed by the color sequence at the receiver outputs.
No CF output factorial or extra factor for equal species is required.

All 15 literal restricted-growth strings are complete: B plus six 2+1+1,
three 2+2, four 3+1 and D. This is every one of the 14 proper source partitions,
not merely one representative for each size pattern. Grouped sources retain
single-photon path coherence; they are not an effective-gate permanent swap.

The six generated relative permutations are exactly single four-cycles.
For each tau, sigma(j)=tau(rho(j)), hence tau=sigma o rho^-1. Summing over
all 24 rho gives 144 ordered cross terms, paired with their conjugates in the
full C4 sum. The code checks its imaginary part is zero, preserves each
oriented coefficient and never clips its real sign. A proper source coloring
cannot be invariant under a transitive four-cycle. Double transpositions are
excluded, and C4/J4 is not mislabeled as a nonnegative probability.

## Raw probabilities, hands and fixed full-PNR check

For G=T^dagger T, a species block's all-signal probability is per(G[A,A]);
orthogonal species are independent, giving the product used by the code.
CF is the complete sum over all 15 receiver sets, collision=all-signal-CF,
and dump=1-all-signal. These nonnegative bins sum to one. An event with any
dump photon is in DUMP even if signal modes collide. All non-CF events hold
the same incumbent and every attempted injection costs four modeled photons.
No survival denominator, unmodeled-loss correction or retry-until-CF appears.

H_ID gives the sole prototype CF set with mass one and zero C4. For H_HOM,
T's first block is (2/3)[[1,i],[i,1]], spectators are identities, so all-signal
is 64/81 and dump 17/81 for every species profile. If the first two sources
share a species their CF amplitude cancels; otherwise CF is 32/81. The resulting
collision masses 64/81 or 32/81 and zero four-cycles agree with the literal hands.
At every graph kappa=0 setting, only the prototype CF set can occur and all
species laws agree. The beta=0/kappa=0 deterministic endpoint is retained.

The full physical check is registered ER1341001/g6, beta=1/2,kappa=1,B, with
no replacement point. Occupations enumerate all C(13,4)=715 ten-mode outputs.
Repeated rows use LAST four input columns; probability divides |per|^2 by the
product of output occupation factorials. Zero bins stay. CF rows match the
receiver table and all three disjoint sums match the separate Gram/CF totals.
This is an exact arithmetic check, not native replication or a noise model.

## Graphs, objective, tuning and exact population

Topology seeds 1341001/2, weights 1342001/2 and independent marks 1343001/2 are
unchanged; sorted min/max edges get integer weights in 1..5. One core factory
call per graph, with no connectedness/quality selection or graph replacement.
Pinned local NetworkX text confirms int seeds become random.Random before
its optional NumPy branch; explicit backend=networkx forces the core path.
Nonempty algos/generators/classes priorities reject BEFORE graph generation.
These are six used graph streams, not photon sampling or a held-out population.

S0 has eight vertices and is explicitly an IMBALANCED algebra helper. Only
current S and the 15 size-12 lifts are feasible. I reconstructed the residual
cut formula from crossing edges: C(S0)+sum d_j-2sum pair weights. All 30
candidate formulas compare with separate whole-edge cuts, charged 34 calls
including each current/helper cost. The entire frontier and prototype are
credited; executing the planned qualification solves this entire small pool.

Each profile independently maximizes its own exact raw utility over all eight
settings. Python max over increasing indices keeps the FIRST tie. Proper-grid
best is not evaluated only at B's chosen setting. h=max(0,current-candidate)
uses no optimum; hazard is secondary. The expected-utility frontier bound
and the deterministic prototype lower bound are checked for every envelope.
Both graphs and all settings complete before a signal status is selected.
The three grid-status branches match the card; optimizer/practical-positive
flags remain false even for a strict signal with positive selected J4.

Independent counters: 18 matrices;18*15=270 profiles and 270 C4 rows;
18*15*15=4050 CF comparisons; sum_l C(4,l)C(6,l)=210 caches/context,
giving 3780 DP/Ryser rows;18*(2^4-1)=270 Gram rows. Add provenance 1,
graphs 2, costs 30, full-PNR 715+total 1, hands 2, envelopes 30 and decisions 2:
TOTAL 9441. Tasks are setup+graphs+2hands+16grid+fullPNR+2envelopes+2final=25.
The count 23 before final_population, then 24/25, matches the task plan exactly.

## Authority, evidence and remaining administrative condition

Nine mandatory project inputs, optional frozen MD/JSON reviews, one separately
bound authority file and 11 distinct external roles are closed before imports.
The role map was compared with ROOT's 80-line metadata report 2a2a0d0 and the
relevant installed NetworkX factory/backend/RNG text, without importing them.
Source/metadata/module/interpreter paths, versions, hashes and byte sizes are
checked; all inputs/external descriptors are rechecked after the scientific work.
Local input paths reject symlinks. ROOT must also ensure the ENTIRE output
parent is fresh; source creates its exclusive data child. It reads no old raw.

ROOT identified the inactive TEMPLATE lacks randomness.used and randomness.seed.
I independently read installed validate_manifest.py lines 168..195: used must be bool,
and used=true requires a non-null seed and generator. BEFORE ANY launch, the
DISTINCT active binding/manifest must add used=true and seed={topology:[1341001,
1341002],weights:[1342001,1342002],marks:[1343001,1343002]}, preserving the six
existing literals and all frozen source/TEMPLATE bytes. This is prospective
metadata completion, not a scientific revision or a failed-run retry.

Every numerical comparison writes its operands/results before its rejecting
assertion; first failure stops with a prefix/state/traceback and FAILED_TASK/
NOT_RUN ledger. Missing hard-kill finals cannot pass. Earlier completed tasks
are not an accepted signal prefix. Matrix and signed cross-term zeros survive.
Final descriptor drift archives the observed hash/size via input_check; only
active-binding drift's new hash is not stored explicitly, so retain the outer
runner's before/after receipt. No false-PASS path was identified from this caveat.

Source hard CPU120/FSIZE16MiB and combined science16MiB/records15MiB+final1MiB
match the prospective ROOT allocation. Wall180/log4MiB, Python -B, entire fresh
parent, manifest-v2 validation and raw sealing remain outer-runner obligations.
Logical256MiB is a plan, not RSS or affinity. No measured runtime follows.
No source change is requested; no qualification, import, RNG or run was done.
This accepts the bounded exact engine design, not optimizer advantage, unique
four-cycle causality, continuous reoptimization, fresh replication or hardware.
