# P65 Cayley--Markov DEV card: B80 first, fixed FAST veto

25-Nov-2026. DESIGN ONLY, before source code, imports, tests, graph generation,
calibration, counts or measurements. Base43dd87345790af2b07bbe83c784f84f63bfd2704.
Authoritative prospective spec: `P65_cayley_markov_dev_spec.json`.
The frozen proof at43dd873 is unchanged: SHA256
3ffb2be9e19b6d9acb49b6d376a7cbe1fc294940a24ee50313b840b3bf522271.
This card is not an execution contract, completed evidence or QPU authorization.

## Question, graph panel and circuit

Does a graph-dependent finite-angle bosonic proposal chain survive a strong
from-scratch classical veto, then independently selected D/species and cheap
correlated feasible replacements? The claim is finite, optimum-blind and
exploratory. No DEV outcome can accept the user's positive objective.

Two NEW N20/K10 cases are frozen: ER seed6502001,p6/19, and RR seed6502002,
degree6. Generate once with the pinned NetworkX seed API. On canonical sorted
undirected edges `(min(u,v),max(u,v))`, assign independent PCG64 integer
weights1..5 inclusive, using seed_for(graph_seed,"weights"). Never filter,
replace or regenerate a case. W=sum_(i<j)A_ij. W=0 is retained inconclusive,
not resampled. Graph generation is experiment setup, excluded from the B
allowance; every algorithm pays its own raw copy/validation/preparation.

Logical graph vertices are physical mode labels0..19 at this DEV stage.
No embedding search, known partition or optimal-state mask is used. Later
relabeling/fresh-embedding tests remain mandatory, not passed by covariance.
For all eight lexicographically ordered `(t,lambda)` candidates use

    t in {1/4,1/2,1,2}, lambda in {0,1/4},
    D=max(1,max_degree(A)+lambda*(N-1)),
    H=(A+lambda*(J-I))/D,
    U=(I+i*t*H)*(I-i*t*H)^(-1).

Compile all eight private matrices per case/model inside its paid boundary,
with complex128 linear solve; no exact Q(i) main-run claim. Never import the
full70-state diagnostic, enumerate feasible partitions, solve an optimum or
use C*. Check finiteness, both Gram matrices, symmetry U=U^T and row/column q
masses at absolute tolerance3e-12, rtol0. Diagnostics are separately metered
and excluded from FAST funding; no symmetrization, polar repair or retry.

## Source, attempt and acceptance

At each optical attempt inject TEN photons, one in each CURRENT occupied
vertex, with sorted source ports. Source routing/request/validation is paid.
The immutable P43 factory already accepts arbitrary distinct source ports;
it must be called anew for EVERY attempt, because current S can change.
No closure prepared at an old source may be reused for a new current state.
Only the circuit's case/model-private candidate U is cached.

The local models are B=`bosonic`, D=`distinguishable`, species=`species4`.
The latter slices the sorted current input list into4/4/2 groups in P43.
Every full integer count vector is archived and checked: length20,
nonnegative integers, total10, no fallback. In this ideal eta1 experiment,
wrong photon total is a first failure, not an invented loss model.
Collisions become self-loops consuming the complete attempt and photons.
No conditional-CF renormalization, retry, repaired subset or postselection.

A collision-free vector gives T={ports with count1}. Score it exactly. Draw
a fresh independent coin for EVERY CF outcome, even if T=S or acceptance1:
accept if u<min(1,exp(-beta*(C(T)-C(S)))). Collided shots record coin=None
and its predeclared unused seed. Keep current S on any rejection.
After EVERY attempt recompute the current cut using the exact integer cut
function, including collision/rejection, and pay that actual call. Initial
cuts and every CF proposal score are also paid and counted separately.
No score cache or saved cut is credited as an unperformed evaluation.

## Frozen trajectories and selection

B, D and species have the same40-attempt recipe per case, selected separately.
Their RNG counts/coins are independent; their initial subsets are shared by
the explicit arm-independent start-seed recipe below, copied/validated/scored
inside each arm's paid boundary. Initial states are known CURRENT states,
not known optima or gains attributed to optical preparation.

Training: draw ONE uniform ten-subset for the case and reuse it as the reset
start for each of the eight candidates. Score that common training start
once per case/arm; its exact cached cut can be copied on resets, with reset
copy/validation work paid but no fictitious extra score calls. Each gets exactly TWO sequential
attempts, beta=4*N/W. Its fitness is the exact Fraction mean of its two
POST-STEP CURRENT cut values divided by W. Collisions and rejects retain the
current cut in that mean. Select minimum fitness; exact ties choose first
lex candidate. Resetting after a candidate never creates a free better start.
All16 training attempts and all scored candidates enter the arm's paid best.
There are four actual initial-cut calls per optical case/arm (one training,
three fresh), forty post-step current-cut calls and one additional proposal
cut for every CF attempt. Report those counters; cache copies are not calls.

Fresh: freeze the selected candidate, then run THREE independent eight-step
chains, with distinct common start subsets. At step j=0..7 use
beta_j=(N/W)*2^(j/2), nonnegative. Their primary statistic is the exact mean
of THREE FINAL CHAIN-BEST cuts/W, including each initial cut. Report each
start, gain from that start, all current and raw proposal cuts, and all
collisions/rejections. The24 fresh attempts are correlated within chains;
they are not24 independent observations. The all-paid best includes actual
initial/training/fresh scores, including unselected training candidates.

The eight matrices are graph-dependent and all compilation/setup is paid;
no candidate is selected using the later FAST, D, species or held-out result.

## All RNG namespaces fixed before B data

seed_for is the immutable P43 SHA256 of slash-joined textual parts, first
four bytes little-endian. Every NumPy RNG explicitly uses PCG64.

| Role | Formula |
| --- | --- |
| graph weights | seed_for(graph_seed,"weights") |
| common training start | seed_for(65100000,case_id,"training",0) |
| common fresh chain c=0..4 | seed_for(65100000,case_id,"fresh",c) |
| optical count, training candidate p/step j | seed_for(65200000,case_id,arm,"training",p,0,j) |
| optical count, fresh chain c/step j | seed_for(65200000,case_id,arm,"fresh","selected",c,j) |
| acceptance coin | identical labels with root65300000 |
| r2/r3 proposal, fresh chain c/step j | seed_for(65400000,case_id,arm,"fresh","fixed",c,j) |
| r2/r3 acceptance coin | same fixed labels with root65300000 |
| FAST mode random/spectral | seed_for(65500000,case_id,mode) |

Arms are literal `bosonic`, `distinguishable`, `species4`, `r2`, `r3`.
Starts are sorted PCG64.permutation(20)[:10], freshly constructed in each
arm with the SAME common seed; first three fresh seeds are shared by ALL
arms, extra chains3/4 belong only to r controls. Common starts are deliberate
aliases, one logical stream per case/stage/chain, not accidental seed reuse.
All other logical stream seeds must be globally unique within this spec;
native-count seeds must be nonzero. Metadata-only checks precede graphs.
Hash collision/zero causes first failure, not salting or substitution.
The fresh optical seed uses literal "selected", not the selected index, so
parameter selection cannot change the predeclared fresh stream.

## Optional controls fixed now, unrun unless the first gate survives

D and species independently select among all eight candidates using the same
16+24 recipe, their own draw/coin streams and paid setup. They do not inherit
B's selected parameter. Re-sorted species labels are a heuristic control:
their aggregated proposal is not automatically symmetric at reverse states,
so no exact Gibbs-equilibrium claim is made for that arm. B and D retain the
ideal fixed-parameter symmetry argument. No noisy/hardware symmetry is assumed.

r2 and r3 use FIVE fresh eight-step chains each:40 fresh proposals, no fake
training. Each proposal removes r uniform distinct occupied vertices and adds
r uniform distinct empty vertices, then uses the same beta_j and fresh coin.
Use sorted occupied/complement lists, independent PCG64 choice without
replacement, and exact scores. Their primary statistic is mean FIVE final
chain-best cuts/W. They inject no photons; actual proposal/score/setup costs
must be reported. Equal proposal counts alone do not establish equal cost.
All other controls before the user's goal remain mandatory: broader D
continuous reoptimization, other species choices, tempering/strong search,
fresh reserved graphs, relabeling/embeddings and independent replication.

## B80 first and four FAST calls

Stage1 runs ONLY40 B attempts per case,80 total/800 simulated injected photons,
then four FAST calls: random and spectral independently on each raw graph.
Any first implementation/numerical failure stops with
INCONCLUSIVE_FIRST_FAILURE; a runner resource/timeout status is authoritative
resource inconclusiveness. Partial outputs are retained, never called a
complete DEV gate or resumed automatically.
Neither receives a B start, incumbent, cut labels, routing or optical feature.
Each fixed mode gets its OWN B-only per-case classical WALL allowance minus
its actual adapter CPU, clipped at zero, with max10000 proposals per call.
Only eligible online checkpoints before that budget are credited. A timely
initialization can veto; survival requires a timely complete first scan and
no early proposal guard. No late overall best or best-of-modes portfolio.

For a completed stage, one SAME fixed mode matching/beating B's all-paid best on BOTH cases gives
DEV_REJECTED_FIXED_FAST. Optional D/species/r2/r3 are then
NOT_RUN_DUE_FAST_VETO. Without that veto, missing prefix eligibility or an
early cap gives INCONCLUSIVE_FAST_ELIGIBILITY; complete survival gives
STAGE1_OPTIONAL_CONTROLS_REQUIRED. No status is positive acceptance. Optional
execution still requires ROOT to review/authorize its separate bounded run;
its rules may not be changed using B outcomes.

## Cost boundary, provenance and risks

Pay B's own raw graph copy/validation, W/degrees/H, all eight solves and
private cache setup, start RNG/permutations/scores, per-attempt source/routing
requests, count/coin seed derivation and RNG setup, factory RNG/validation
prefix, count validation/CF checks, proposal/acceptance/current scores,
fitness/selection/chain-best/paid-best updates and final statistic aggregation.
Do not let optional-model metadata/preparation or evidence serialization
fund B. Actual B seeds/start/circuit work is performed in B's paid boundary,
even if a metadata seed table was generated earlier for integrity checks.

Imports/native setup, raw graph generation, separately metered diagnostics,
actual count generation and evidence IO are excluded. For each immutable
P43 factory call exclude ONLY its returned backend WALL, retaining total
factory CPU/WALL and nonnegative pre-clock RNG/validation prefix. Internal
backend versus prefix CPU is None, not guessed by subtracting WALL. No
temporary simulation, counter-generation or optional-control work funds FAST.
This deliberately favorable zero-optical-latency envelope is not measured
QPU timing, practical matched total cost or an accepted speed advantage.

All80 requests/counts, source sets, candidate U/H, start subsets, sorted
species recipes, coins/seeds, costs, exact fitnesses, selection, chain states,
raw/chain/all-paid bests and four FAST traces must be archived in fresh files.
Write requests before sampling, keep the first failing payload, preserve all
partial outputs, and seal raw data before interpretation. No overwrite/retry.
Limits: CPU60s/wall90s, one numerical worker, native Config maximum1 read
before/after, conventional threads1, logs/scientific outputs32MiB, logical
workspace256MiB and1MiB failure reserve. No hard Darwin RSS/affinity claim.
No N20 canary, hidden calibration or sampler draw before the registered main.
Qualification must use smaller synthetic fixtures and mocked timers only.

Remaining risks are explicit: only two DEV graphs/three fresh chains; small
parameter grid; possible large CF self-loop rate; binary64 matrix/acceptance;
source-dependent optional species groups; backend seeding; all per-state
factory costs; future routing, photon losses and feedback latency. A cap or
numerical failure is inconclusive, never reason to omit adverse controls.
No paper, held-out panel, known optimum, QPU call or Laurent message follows.
