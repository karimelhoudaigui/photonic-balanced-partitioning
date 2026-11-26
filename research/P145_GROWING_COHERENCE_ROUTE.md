# P145 — Two coherent tritter layers: width and collision discriminators

26-Nov-2026. MANUAL reconstruction, parent 136350e5a5fb2abd19b90b2675d195b815011a3c.
Self-reviewed proof candidate awaiting non-author review. ROOT suggested the
architecture and collision bound; graph typing and tensor details are below.
No code/import/AST, numerical/symbolic run, graph draw, RNG, native/QPU or
P145 qualification-data access. Prior P145 note/core/review/data are unchanged.
P65 already studies global measured passive proposals: no new physical class,
positive optimizer, novelty or equal-wall-time assertion is made here.

## 1. Precisely which graph can be a forest?

Fix L>=1, M=6L modes, K=3L photons in DISTINCT CF inputs R, other inputs vacuum.
The pure identical-photon input is a tensor product of mode Fock states.
Let A and B each be a direct sum of 2L arbitrary three-mode unitaries.
Between them apply a supplied permutation P_G, chosen using paid public graph
features; U=B*P_G*A. Edges retain their physical port positions. There is NO
intermediate measurement. At the end retain
ALL PNR counts; output CF gives a candidate, everything else is a paid hold.

The wire multigraph has first/second-cell vertices and ONE edge per intermediate
mode: 4L vertices,6L edges, degree3 at every vertex. Parallel wires are distinct.
Its cycle rank is 2L+c, c=number of components, so it is never a multigraph forest.
Do NOT confuse this with the SIMPLE intersection graph: an edge there bundles
r_ab in {1,2,3} wires, and each vertex has WEIGHTED degree3.
If a component of that simple graph is a tree, choose a leaf. Its sole edge
has weight3, exhausting its neighbor's weighted degree too. Thus the component
is just TWO cells joined by three wires. A complete simple-forest architecture
is therefore a matching of independent three-mode blocks, not a growing network.

Vacuum-pruned graphs differ: remove first cells with no occupied input and fix
their wire occupations to zero. Second cells then have weighted degree<=3,
so nontrivial SIMPLE trees can occur; apply the width algorithm below.
If every active first cell can populate all three wires, q active cells give
3q edges, q>=L, b<=2L nonisolated second cells: multigraph cycle rank
2q-b+c>=c>0. This only counts mode-wire cycles, NOT simple cycles or hardness.

## 2. Exact component veto, specialized from the existing block principle

A disconnected wire component C defines disjoint initial/final mode sets;
U has no cross-component entries. Put K_C=number of occupied inputs in C.
Its fixed-input bosonic output law factors over components. Give all sources
within C one tag and distinct components orthogonal tags: the ENTIRE spatial
PNR law is unchanged. The factorization includes collisions, not a CF law
divided by survival. Any common global cut decoder/hold utility preserves it.
With >=2 SOURCE-containing components this is a proper-species control;
vacuum-only components do not count. If K_C<=3 throughout, groups of size<=3
already reproduce B. The simple-forest case above has exactly that bound.
If only one component contains sources it contains at most three photons in
that forest case, returning to the tiny classical kernel rather than a veto
based on fictitious vacuum components.

This is the same disjoint-mode reasoning used in P136, not its reflection
formula applied to a different matrix. Wiring connectivity is only a
necessary screen: gate zeros/cancellations can disconnect the ACTUAL occupied
source-to-output support further. Gram zeros alone are still insufficient.
Equality of spatial laws does not make physical tag preparation free.

## 3. Explicit raw probability contraction and sampler at supplied width

First cell a contains k_a<=3 occupied inputs R_a. Each intermediate wire
occupation s_e is in {0,1,2,3}; enforce sum_(e incident a)s_e=k_a.
Second cell b receives at most9 photons and its output triple n_b has total<=9.
Define local tensors in an unnormalized creation-polynomial basis:

    alpha_a(s)=per(A_a[s,R_a])/product_(e incident a) s_e!,
    beta_b(n_b;s)=per(B_b[n_b,s]),

where rows/columns are repeated according to occupations, empty per=1, and
beta=0 unless input/output totals agree. Input CF factorials are1. The exact
normalized amplitude is

    amplitude(n)=(product_j n_j!)^(-1/2)
                       *sum_s product_a alpha_a(s_a)*product_b beta_b(n_b;s_b).

The intermediate factorial appears ONCE: normalized first/second Fock
transitions each supply its square root. Squaring introduces edge variables
(s_e,t_e), dimension<=16, first factor alpha_a(s)conj(alpha_a(t)), and
second factor beta_b(n;s)conj(beta_b(n;t))/product_(j in b)n_j!.
Summing a second factor over unobserved output triples gives
product_e s_e! times delta_(s,t), by unitary Fock normalization. This proves
raw marginalization/normalization without dropping collision sectors.

Supply a polynomial-size tree decomposition of the SIMPLE cell graph of
width w. Replace every cell in a bag by all its incident MODE EDGES, at most
3(w+1) variables, retaining parallel wires. Every factor's scope fits a bag.
For edge uv, bags containing it are the union of u-bags and v-bags; these
subtrees intersect because a bag contains u,v. The running-intersection
condition therefore holds. Sum-product elimination costs at most

    poly(L, arithmetic bit cost) * 16^[3(w+1)].

Complex signs do not permit positive-only message heuristics, but cause no
logical problem for EXACT contraction. For Gaussian-rational cell entries of
supplied bit length, local permanents have sizes<=9, factorials are bounded
constants, and contraction numerator/denominator lengths are polynomial in
the total input description. A supplied fixed-degree algebraic field is a
possible separate representation; arbitrary exact-real oracles are not assumed.
Obtaining/validating a good decomposition and all graph features are paid.

Sample one second-cell output triple at a time from conditional prefix masses;
there are at most sum_(r=0..9)C(r+2,2)=220 choices. Each mass is the SAME
contraction with fixed/local summed output factors. Recomputing all candidates
for all2L cells adds only polynomial overhead. Positive-prefix ratios and
rational categorical weights give an exact expected-fair-bit sampler.
Zero-prefix branches are never sampled. The sampler draws RAW records directly;
it never repeats until CF, so no hidden 1/P_CF conditioning cost. Exact sampling does not
imply a deterministic finite wall cap. Approximate gates/rounding require a
separate controlled-error argument; no interval or hardware certificate exists.

Hence bounded w, or supplied w=O(log L), gives a polynomial algorithm for this
model. Large connected components/loops alone do not escape it. For example
the Cartesian prism C_(2L) x K2, L>=2, is connected bipartite cubic with 4L vertices
and6L wires, yet has a width<=5 decomposition: two successive columns plus
the fixed first column. All L can grow while this upper bound stays polynomial.
This is not a measured claim that the coarse upper bound is fast on this host.

## 4. A depth-two collision bound even when width grows

Use FULL input lightcones, including vacuum modes, not just occupied sources.
Each output depends on <=9 input modes, and each input can affect <=9 outputs.
Let q_ja=|U_ja|^2. Supply q0>0 and a set H of A_count outputs, each having TWO
distinct OCCUPIED input modes with q_ja,q_jb>=q0 in the ACTUAL U.
Structural reachability alone does not certify this numerical/intensity floor.

For each such output j, CF identical input gives

    M_j=E[binom(n_j,2)]=2sum_(a<b in R)q_ja*q_jb>=2*q0^2.

Its full input cone initially contains <=9 photons, so n_j<=9 on the supported
state. Since binom(n_j,2)<=36*1_(n_j>=2),

    Pr(n_j>=2)>=q0^2/18.                                           (1)

Two outputs conflict if their FULL backward cones intersect. A cone has<=9
inputs, each in<=9 output cones: its closed conflict neighborhood has<=81
outputs. Greedy selection therefore supplies at least ceil(A_count/81)
pairwise disjoint-cone outputs. No counting assumption about independent
photons replaces this step.

Indeed the count pullback is b_j^dagger*b_j, b_j=sum_i U_ji*a_i, supported
on that cone's input-mode Fock factors. For disjoint cones these algebras act on disjoint
factors of the PRODUCT CF/vacuum input. Their number observables, hence their
collision events, are independent. Shared occupied inputs OR shared vacuum
inputs would invalidate this factor argument and must be excluded by full cones.
Multiplying the no-collision probabilities and then imposing the remaining
output constraints gives

    P_CF <= (1-q0^2/18)^ceil(A_count/81),
    E[raw accepted gain] <= R_gain*(1-q0^2/18)^ceil(A_count/81).      (2)

R_gain is a supplied bound on feasible improvement; no C* is needed. Divide
by3L for per-injected-photon utility, before any further paid setup costs.
If A_count grows linearly with L and q0 stays positive uniformly, the CF rate
decays exponentially; no such premise is inferred from a few fixed examples.
Vanishing q0, small A_count, coherent cancellation of U entries, entangled
inputs, growing depth or a changed repair decoder need separate analysis.
The statement is for the ideal specified circuit, not calibrated Lucy loss.

There is an automatic-floor specialization, not just a supplied-q0 test.
Assume both layers are BALANCED tritters (all entry intensities1/3), and
no first/second cell pair has parallel wires. Each reachable input-output
pair has ONE intermediate path, hence q_ja=1/9, with9 entries per row/column.
For second cell b let v_b count occupied inputs in its nine-input cone.
Each occupied source belongs to three second cells, so sum_b v_b=3K=9L.
If g cells have v_b>=2, then 9L<=9g+(2L-g), implying g>=ceil(7L/8).
Each gives three good outputs: A_count>=3g. For this family (L>=2),

    P_CF <= (1-1/1458)^ceil(7L/216).                                (3)

The constants are weak; this is no measured finite-size rejection threshold.
Port phases and graph-dependent wiring cannot cancel a UNIQUE one-particle
path. Parallel-wire interference or nonflat couplers remove this automatic
floor, so (3) must not be extended to them. General bound (2) retains its
own supplied hypotheses. Neither bound proves D dominance or a global no-go.

An endpoint caution: if FINAL collision expectation is EXACTLY zero, the
same positive pair-moment formula implies each output row supports at most
one occupied input column. B and D then have the same complete count law.
For small but nonzero collisions, P33 still needs its actual density/expected-
pairs hypotheses; low observed collision probability alone is not a TV theorem.

## 5. Known method, precise remaining question

The width method is established, not a project discovery. Primary checked:
Markov--Shi, [quant-ph/0511069v7](https://arxiv.org/pdf/quant-ph/0511069v7),
12-Jul-2009, PDF pp10–12, Proposition4.2, Lemma4.4 and Theorem4.6.
These give contraction/line-graph width and bounded-width circuit simulation;
our occupation cap, factorial tensors and classical bit assumptions supply
the bosonic translation above. Source authentication/extraction verified;
overlap is known after translation, not a novelty clearance. No local source
artifact was retained (SHA256 NONE), no cache/ledger edited or global search.

Before any new pilot, a candidate must expose: actual source components;
a paid supplied decomposition/classical tensor mirror; certified or honestly
unverified A_count,q0; full CF failure cost; and independently tuned D/proper
groups plus strong multi-exchange graph search. Growing width merely evades
one sampler bound; it does not give a useful gain sign or superiority.
The first UNRESOLVED lemma is an optimum-blind graph-to-wiring/gate rule
with a useful global raw transition benefit surviving those controls WITHOUT
entering a regime where (2) destroys the proposal rate. No such rule is derived
here. This is a concrete structural/collision falsifier, not a new optimizer,
all-depth impossibility theorem, empirical simulation result or QPU gate.
