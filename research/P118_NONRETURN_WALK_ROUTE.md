# P118: strict edge-memory walk within eight passive modes — bounded rejection

26 November 2026. **MANUAL ROUTE: no surviving bosonic mechanism in the
canonical strict no-return class below.** One concrete8-mode/2-photon
architecture is specified and solved. The obstruction also covers10 modes;
it is not a theorem about every eight-mode passive unitary or every memory rule.
No source, circuit, experiment, graph/seed population or QPU run is registered.

Prior framework is REUSED, not rediscovered: P105 source4058cec54d92604d79cd19eece97e2774f676dbc,
research/P105_NEIGHBORING_MECHANISMS_SOURCES.md174l, SHA256
4cd966e0f3f2da603845e7143ab068de1b257cfcf43d8e266ec0da2cb58c5216.
Its authenticated primary S1 is Harrison/Smilansky/Winn, *Quantum graphs
where back-scattering is prohibited*, [arXiv0708.0839v1](https://arxiv.org/html/0708.0839v1), Definition1.1/
Proposition3.2/section1: directed-bond state space and zero-diagonal scattering;
classical counterpart|U|^2. S2, Alon et al. math/0610550v1, proves qualified
regular-graph mixing facts, NOT an optimizer improvement. No fresh source
authentication, mixing transfer or novelty assertion is needed for the direct
finite proofs here. P100's cubic optical route is not reused.

## One exact architecture, including its memory and decoder

Task graph G: four unit-mass vertices with arbitrary finite nonnegative
weights w_ij. Public vertex marks fix order0,1,2,3 and travel under relabeling.
The AUXILIARY move graph is the cycle0--1--2--3--0. It is not claimed to
be the support of G or an optimum-informed sparsification. Eight orthogonal
modes encode ALL directed arcs|u,v>, meaning previous vertex u,current v.
Empty arcs count as modes. Nothing is hidden in an uncounted coherent register.

At vertex v, order its two neighbors by their public marks. Given incoming
neighbor u, let other(v,u) be its other cycle neighbor. Compile

    W=sum_(i<j)w_ij, gamma_(v,u)=2pi*w_(v,other(v,u))/(1+W),
    U_G|u,v>=exp(i gamma_(v,u)) |v,other(v,u)>.             (1)

This is a vertex-local coin followed by the directed-arc shift. Its2x2
coin in ordered neighbor bases has zero diagonal and two unit-modulus
off-diagonal entries. The direction (u,v) is explicit memory; the rule
forbids v->u, not merely staying on a vertex. The phase/compiler uses only
G, and reads/normalizes its six weights; all preprocessing and routing is paid.
No cost optimum, favorable mask, hidden graph feature or training oracle enters.

Choose the initial balanced set S classically and record it. Place one CF
photon in an arc ending at each of S's two vertices; select each predecessor
independently uniformly from its two neighbors and archive the two memory coins.
All mode/source settings are paid. Apply ONE U_G and read all eight counts.
For continuing proposals, retain/reprepare the observed ARC occupation as
memory and pay that preparation; there is no coherent inter-shot state or
within-shot feed-forward. A restart from a new S is a paid public policy,
not the continuation of the previous arc path. No acceptance filter is used.

For n_uv define vertex counts n_v=sum_u n_uv. Rank the four vertices by
decreasing n_v with fresh independent uniform tie priorities and return the
first2. Score its actual G cut and retain BEST of all scored candidates.
This is total: a two-photon vertex bunch chooses its vertex plus a uniform
other vertex. All eight-port records and coarse vertex collisions remain.
There is no CF-output selection, discard/retry, or conditioning on detection.
Actual source/detector failure would require separately recorded flags and
a declared fallback; no unknown device failure is silently the ideal input.

## Smallest useful balanced case, solved by hand

Take S={0,1}; let signs+/- denote clockwise/counterclockwise input arcs.
For vertex0 these are|3,0>/|1,0>; for vertex1 they are|0,1>/|2,1>.
Equation(1) gives the following exhaustive four equally likely initial memories:

| Memory signs | Output arcs | Decoded pair | Unoriented partition |
|---|---|---|---|
|+,+| (0,1) and (1,2)|{1,2}|class{0,3}|
|+,-| (0,1) and (1,0)|{0,1}|class{0,1}|
|-,+| (0,3) and (1,2)|{2,3}|class{0,1}|
|-,-| (0,3) and (1,0)|{0,3}|class{0,3}|

Thus the initial class has probability1/2, the class{0,3} probability1/2,
and the remaining class{0,2} probability0. The same table holds for B,
independent D and two classical no-return walkers. No bunch occurs in THIS
adjacent-source case, but the decoder above also includes vertex bunches for
other sources. Phases gamma are invisible to every probability in the table.
This is an exact finite negative, not a simulated frequency or a graph-sign claim.

## Why the obstruction is structural, not just this phase choice

Define the class precisely: simple undirected loopless auxiliary graph,
vertex-local LOSSLESS scattering unitary C_v, one mode per directed arc,
and strict no immediate return for EVERY incoming basis arc. This means
(C_v)_(u,u)=0 when outgoing/incoming neighbors use the same ordered labels.
No nonvacuum helper, coherent prepared path superposition or measurement gate
is assumed. The occupied input is a known CF state of2--4 photons.

A degree1 vertex has no such coin: the only diagonal entry must have
modulus1, contradicting zero return. A degree2 zero-diagonal unitary is a
swap with phases. A degree3 zero-diagonal unitary is ALSO monomial: two
different rows can share only the third column; their inner product is a
single product and must vanish. Thus no column supports two rows. Each
row/column must be nonzero, leaving exactly one unit-modulus entry per row.

Consequently a nonmonomial coin needs degree at least4. With no leaves,
such a vertex has at least four distinct neighbors, each of degree at least2.
Degree sum is at least4+4*2=12, hence|E|>=6 and the optical arc space
m=2|E|>=12. In particular EVERY allowed coin at m<=10 is monomial.
Disconnected components do not help; apply the bound to the component
containing a nonmonomial coin. Isolated vertices have no arc modes.

The lower bound is combinatorially sharp: two triangles sharing one hub
have6 edges, hub degree4 and all other degrees2. At the hub one can use
C=[[0_2,H_2],[H_2,0_2]], H_2=[[1,1],[1,-1]]/sqrt(2), a nonmonomial
unitary with zero diagonal; outer vertices use swaps. This checks sharpness,
NOT a twelve-mode proposal, capability assumption or new experiment.

An arc shift is a permutation. Multiplying it by monomial local coins,
or taking any finite prescribed sequence of such steps, remains monomial:

    U|a>=exp(i theta_a)|p(a)>,
    P_B(n_out|n_in)=P_D(n_out|n_in)=1_(n_out=p_*n_in).     (2)

For CF input each output mode has0 or1 photons. Vertex aggregation may
bunch, and all such records survive the equality. Shared classical source,
memory and tie coins can couple the entire B/D/classical transcript exactly.
Every common decoder, scored-best rule, or common classical quench therefore
has the same law, not merely a matching mean or leading cubic expansion.

## Six questions and the explicit veto

1. **Graph structure/encoding?** Public C4 arc memory plus the graph-weight
   phase compiler(1). Any adaptive selection/compilation that remains in this
   class still has equality(2); graph-derived choices must be shared/paid.
2. **Why B?** There is NO surviving B reason. No paths branch under a
   monomial unitary. The hoped-for multiphoton nonlocal statistic vanishes
   exactly, before repair/mark averaging; there is no P100 cubic term to exploit.
3. **Reoptimized D?** Its family contains the identical U_G/controller and
   may independently choose coins, steps, initial memory and preprocessing.
   Already that one allowed D member reproduces the full B raw law. No free
   best-of-portfolio or unpaid compiler optimum is needed for this null.
4. **Classical information/cost?** The NB-intensity control updates each
   occupied arc by p, records the identical counts, then uses the same paid
   decoder/RNG/cut evaluator. Charge graph loading, all coins, source settings,
   memories and every score. On four vertices also pay/credit the three-cut
   exhaustive frontier once its three scores fit; no all-budget clock claim.
5. **Hardware?** Eight arc modes, two known single photons, passive phases/
   permutations and full number records suffice in the ideal model. Actual
   routing, source, PNR/attempt denominator and latency remain unverified;
   measured-reset memory is paid. No postselection repairs those unknowns.
6. **First gap/kill?** The first missing ingredient is a NONMONOMIAL strict
   edge-memory step under the cap, and the proof above rules it out in this
   class. Thus no useful bosonic statistic is left to test: REJECT this route
   before DEV/native allocation. A proposed effect would falsify a model/
   implementation assumption or reveal a different source/coin, not establish
   advantage. Relaxing vertex locality or strict no-return changes the task
   and needs a separate full all-output design and independently optimized
   D/classical-memory controls; none is silently supplied here.

Soft-return walks remain OPEN outside this strict class; no universal
eight-mode no-go is claimed. No import/AST, scripted calculation,
test, simulation, RNG, graph draw, native/DEV/runner/QPU, manuscript edit,
push or other source/contract/raw change occurred. Only this note is written.
