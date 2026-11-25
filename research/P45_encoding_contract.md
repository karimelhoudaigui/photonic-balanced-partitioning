# P45-B — full-Fock graph walk DEV discriminator

Date:25-Nov-2026. Base:e93dfa2, descended from root8f83f2b. Isolated branch:
research/p45-encoding. No execution, positive claim or hardware claim at freeze.
This contract is subordinate to research/P45_POSITIVE_TARGET.md.

## Hypothesis and changed physics/readout

K distinct single photons enter K+1 spatial modes in source nu=(1,...,1,0).
Every ideal output occupation n with total K is decoded by

    D(n)=1^n0 0 1^n1 0 ... 0 1^nK.

It has K ones and K zeros. Its fixed bit positions label the2K graph vertices.
This is the established stars/bars bijection, not a novelty claim. All
collisions are useful candidates rather than discarded outcomes. This changes
the occupation-to-partition mechanism and mode count, not the passive gate set.
The target observable is global under this decoder; no claim follows merely
from a different expectation. No postselection denominator is used at eta=1.

The specific hypothesis is that a finite-angle graph-dependent walk can
combine scored single-gap moves into beneficial multi-gap outcomes through
many-photon interference. Its signal must survive optimized D, coherent fields,
classical bunching and explicit gap moves. A mean/gain change relative to an
uncredited starting anchor does not count.

## Exactly what graph information enters U

For each graph choose S0 as the lexicographic best(cost,sortedsubset,index)
of four uniformly sampled balanced candidates. Score and retain all four.
Independently shuffle S0 and its complement using the declared case/order
seed and interleave them. This ordering maps nu to S0. It has no spectral
seriation or hidden additional score. The physical source/order remain fixed
after this point; there is no recursive reanchoring.

For EVERY j<K and i!=j in0..K, score D(nu+e_i-e_j). There are exactly K^2
such physical one-hop candidates. Retain their occupations, subsets and costs.
Let Delta_ij be this cost minus C(S0), and

    C_front=min(all four anchor costs, all K^2 hop costs),
    s=max(1, median over all K^2 |Delta_ij|).

Every algorithm receives the best common subset, all these discoveries and
the same ordering. Every algorithm is charged4+K^2 common score evaluations,
the graph/ordering/feature construction and its recorded time. The optical
source can still encode S0 even when C_front<C(S0). Only improvements below
C_front are useful new discoveries.

For occupied modes i<j<K define

    a_ij=2/[1+exp(clip((Delta_ij+Delta_ji)/(2s),-8,8))],
    phi_ij=kappa*tanh((Delta_ji-Delta_ij)/(2s)),
    H_ij=a_ij exp(i phi_ij), H_ji=conj(H_ij).

For i<K and empty mode K use

    H_iK=H_Ki=2/[1+exp(clip(Delta_Ki/s,-8,8))].

Set the diagonal to zero, normalize H by its spectral norm, and use
U_G(t,kappa)=exp(-it H). Norms and residuals are recorded. The kappa phases
can create nonzero cycle flux, but one-particle wave interference is not
itself a many-photon advantage. There is no optimal cut cost/mask, no exact
solver, no known-optimum circuit preparation and no withheld score table.

## Fixed DEV design and competing explanations

The JSON spec fixes four fresh DEV graphs:16/20 vertices, weighted ER(p=.35)
and degree4 regular topologies; all present edge weights are integers1..9.
Topology/weight seeds4501601,4501602,4502001,4502002 are frozen. No held-out
graph outcomes are generated. There are no favorable graph substitutions.

One family has six settings: t in{.7,1.4,2.1}, kappa in{0,pi/2}, in the exact
JSON order. Each model gets12 draws per setting per graph. Independent
GLOBAL selection across the four DEV graphs maximizes the sum of
mean max(0,C_front-C_sample)/max(1,C_front). Ties minimize normalized raw
mean cost and then setting index. Every cut is feasible and raw costs remain
reported; there is no CF-conditioned mean. C_front is a measured incumbent,
not C*. Training itself can discover useful candidates and all are retained.

Models reoptimized INDEPENDENTLY over that same setting grid:

- B:Perceval/Exqalibur Clifford2017 full-Fock sampler, fully identical photons.
- D:independently route each labeled input photon using |U_ia|^2.
- Phase-multinomial:field U[:,0:K] z with iid z in{1,-1,i,-i}; draw K counts
  multinomially using its normalized squared field.
- Source-multinomial:draw K counts from q_i=sum_(a<K)|U_ia|^2/K.
- Source-Pólya:draw p~Dirichlet(Kq) on strictly positive q entries, then
  counts~Multinomial(K,p). This reproduces bunching without bosonic permanents.
- Inclusion walk:classical continuous-time occupation process from nu with
  rates n_j(n_i+1)|H_ij|^2, run for time t^2. Its leading small-t single-hop
  probabilities match bosonic stimulated hopping. It has no coherent phases
  beyond their influence on the common norm. Gillespie event cap4096 per
  proposal is a resource failure if reached, never a silently clipped result.

Selection.json is written and hashes the raw training prefix BEFORE any fresh
draw. Every selected model then has two batches of64 fresh DEV draws on each
graph: original labels and a declared independent vertex relabeling. The
relabeling transports the EXACT SAME ordering, so it checks covariance/fresh
sampling, not robustness to a new seriation. Same physical U is appropriate.
Fresh-order robustness and held-out graphs require a subsequent frozen study.

Each model therefore scores200 new candidates/graph, plus the shared common
front. The comparison also runs200-score uniform, two-swap, swap-descent,
annealing and spectral-swap searches using the already frozen P43 helper,
starting at the common best. New gap-descent/gap-annealing controls operate
on exactly the SAME composition/order space, also starting at that best.
Finally an independent Dirichlet(1,...,1)→multinomial control runs200 draws.
Its Fock occupations are EXACTLY uniform, hence exactly uniform balanced
partitions under this bijection. Haar-average uniformity cannot count as gain.

All classical controls keep their incumbent over their full200-score search.
For every model final best cost is the minimum of common-front, training
and fresh costs. No previously scored Delta candidate can be credited to B.
There is no automatic advantage declaration: complete tables and raw data
return to root for adversarial assessment. One small DEV screen can only
reject this protocol or motivate follow-up. No statistical, held-out,
independent-replication, hardware or novelty gate is passed by this pilot.

## Resource/provenance contract

The executable imports only cut, seeded graph generation, SHA seed_for and
the established classical controls from the immutable base P43 script. That
file is part of the source closure. Packages use the existing pinned venv;
there is no installation or remote client. Expected optical simulated B draws:
800 total, K8/10 in9/11 modes; all data remain simulation, actual QPU photons0.
Native/backend versions and all closure hashes are recorded by the script.

Execution requires root's explicit single CPU slot and a precommitted source
revision. Use the Mathbox bounded v2 runner:1 thread,60CPU/90wall seconds,
32MiB outputs and planned arrays<=256MiB. Write a fresh run directory with
an unoccupied data/ subdirectory for the script, preserving any incomplete
prefix/failure. No rerun, enlarged cap or different seed without a new
information-gain decision. Source/spec hashes must agree before/after.

Scores, ideal attempted samples, modeled injected photons, simulation runtime,
setup, graph preprocessing and decode work are distinct quantities. This pilot
does NOT establish equal actual hardware costs. Requiring all K surviving
photons later costs eta^K under uniform survival and the known survival-tail
analysis applies. No nonempty-detection shots are substituted for emission
attempts. True PNR, source capability, loss and backend compilation are
unverified. No QPU submission or manuscript edit is authorized by the test.

## Analytic discriminator and prior-art boundary

The inclusion process is reversible with the uniform composition measure:
the forward rate n_j(n_i+1)|H_ij|^2 equals the reverse rate at the moved state.
Its initial time-t^2 transitions match the O(t^2) bosonic hop weights. Thus
mere stimulated hopping or a drift toward uniform Fock occupations is already
covered by a positive classical process. A candidate signal must exceed it,
the phase-field control, reoptimized D and strong feasible searches at finite
t, with all common discoveries credited.

The combinatorics is known; Clifford–Clifford, *Faster classical boson
sampling*, Phys. Scr.99(2024)065121, Theorem3/Section6, explicitly relates
Haar-average Fock uniformity to stars/bars. Binary variational boson-sampling
encodings and parity readouts also predate this work. This specific cost-hop
composition has no novelty clearance. The bounded source search and primary
locators will be recorded separately; the present freeze is an experiment
design, not a novelty claim.
