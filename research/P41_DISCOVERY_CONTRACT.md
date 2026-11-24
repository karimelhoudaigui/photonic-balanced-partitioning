# P41 — optimum-blind mechanism discovery

Base checkpoint: `27443954fb7491a293399f0417d05185009f5c9a`.
Owner: Astra/root. User authorization: 2026-11-24 research restart, after the
Lucy handoff. This phase supersedes paper polishing as the active objective.

## Target and acceptance

Discover an interference-dependent photonic mechanism for minimum balanced
partitioning, or prove a substantial obstruction for a precisely defined
approach class. A scoped no-go cannot close the unrestricted discovery target
unless it covers the class actually proposed as a solution. Existing P33/P37,
the occupation-mean identity and E05b are inputs, not new discoveries.

Training sees the graph, scored feasible candidates and classical history.
It never receives C*, optimal masks or an optimal partition. Retrospective
exact solution, if computed, lives strictly in evaluation after decisions are
frozen. A circuit loading scores already obtained classically must charge
those scores and compare to the best candidate already discovered.

A positive result must survive independently reoptimized distinguishable
photons, a correlated feasible sampler, balanced random search, feasible swap
descent/annealing and relevant spectral controls. Charge graph processing,
training shots and scores, every rejected/lost optical attempt, reoptimization,
hyperparameter search and final sampling. Report query/attempt/photon counts
and measured classical time separately; do not identify these resource units.

Circuit/optimizer choices freeze on development graphs before any held-out
scores. Held-out graph seeds, random labels, fresh optimizer seeds, all graph
slots, failures and physical normalization are retained. A finite positive
pilot is only a candidate until source checking and independent replication.
Only then prepare a frozen hardware experiment; no QPU calls in this phase.
The existing manuscript and all historical raw scientific files stay intact.

## Initial distinct routes

1. R1 — adaptive interference proposals. Change the old small-block model:
   investigate phase-sensitive or larger correlated feasible proposals driven
   by graph features rather than optimal-state information. First derive a
   discriminator separating coherent dynamics from independently optimized
   labelled particles and the classical information used to construct it.
2. R2 — feasibility-preserving encoding. Investigate pair/dual-rail or changed
   decoders with balanced output by construction. First determine whether a
   genuine interference degree of freedom remains after feasibility and full
   preparation/heralding cost. Exact sampling equivalence rejects a mechanism.
3. R3 — structural obstruction. Seek a quantitative extension beyond the known
   convex-quadratic same-frame dominance, or a rigorously scoped classical
   replacement that closes a material newly proposed class. A trivial equality
   of global expressivity or failure of a single optimizer is insufficient.

Each owner may revise its route after a decisive check, recording the changed
bottleneck. No arbitrary global attempt count is imposed. Bounded individual
calculations and substantive checkpoints permit successive routes.

## Resource and provenance policy

Current disk observation: about1.7GiB free. Use sparse isolated Git worktrees,
not full500MB copies. Saved machine audit reports M2/8GiB; current sysctl read
is sandbox denied. One numerical worker at a time. Analytic agents may work
concurrently but must obtain the numerical slot from the coordinator.
Initial calculation caps:1 BLAS/OpenMP thread, at most60CPU/90wall seconds,
at most256MiB new outputs and256MiB planned arrays. Larger checks require a
new specific information-gain justification, not user reauthorization.

Before a load-bearing run, commit its contract/code/seed set, save exact argv,
input/code hashes, versions, git revision/dirty state and caps. Never overwrite
an existing run directory. Exploratory versus confirmatory status is explicit.
No statistical advantage claim from development tuning. All proof conclusions
require a separate adversarial audit and external dependencies require exact
source checks. Reviews disclose shared context and implementation involvement.

## Initial state

Original goal OPEN. New routes NOT EXECUTED. No positive claim or new
obstruction accepted. Paper remains the validated24-November snapshot.
