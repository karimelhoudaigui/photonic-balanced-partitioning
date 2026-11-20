# Research checkpoint — 2026-11-20

**Decision: NO-GO for a photonic computational-benefit claim and QPU preparation.
PAPER_READY = FALSE.** This closes the tested small-instance optimization route,
not the general research question. No hardware was contacted and no noise
results or manuscript sections were written.

## What was learned

The strongest theoretical checkpoint is a quantitative certificate for proximity
to an independent-particle sampler, together with a counterexample to inferring
such proximity from a high collision-free probability alone. At balanced density
`m=2k`, an explicit family has

\[
1-P_{\rm CF}=\frac{2}{k+2}\longrightarrow0,
\qquad \operatorname{TV}(p_{\rm boson},p_{\rm dist})=\tfrac12.
\]

Two photons interfere over `k+2` modes; `k-2` photons are deterministic spectators.
The example is easy to sample classically. It disproves a proposed diagnostic,
not efficient classical simulation or quantum optimization advantage. Its proof
and a spatial-overlap certificate appear in
[near_collisionless_bound.md](../theory/near_collisionless_bound.md).
An independent reconstruction passed in
[NEAR_COLLISIONLESS_INDEPENDENT_REVIEW.md](NEAR_COLLISIONLESS_INDEPENDENT_REVIEW.md).
**Novelty remains OPEN:** the permanent/triangle technique has close precedent
in Tichy's work on internal distinguishability, which is a different Gram matrix.

The optimization experiments provide a negative computational result in their
stated range. Optimized distinguishable photons are competitive or better;
direct classical feasible sampling discovers optima before the variational
training budget is spent. High final sampler success therefore cannot be treated
as a computational benefit of the bosonic interference.

## Validation and corrections

The starting suite had 40 passing tests despite defective wrappers. Corrections
cover odd-photon permanent phase, the actual input basis index, vacuum,
nonunitary input rejection, unrenormalized full Fock amplitudes, actual collisions,
the seed/edges positional mix-up, conditional weighted lower-tail CVaR including
partial quantile atoms, and the full binary penalty space.

Perceval 1.3.0 / exqalibur 1.4.2 independently reproduced **8,464 Fock outcomes
across 125 input/circuit cases on 60 Haar circuits**. Maximum probability error
was `1.776e-15`, amplitude error `2.135e-15`, and raw normalization error
`4.219e-15` at tolerance `1e-10`. The separate permutation-sum CF evaluator and
Perceval mesh export passed 80 Haar/mesh cases through `n=10`. These are simulator
checks, not hardware evidence.

`PenaltyProductBernoulli` samples all `2**n` strings. The old `PenaltyObliq` name
now warns that it is a classical compatibility alias. No genuine optical ObliQ
dynamics, optical circuit depth, or hardware-equivalent resource comparison is
claimed. QUBO coefficients, cancellations, lambda sensitivity and negative trials
are retained in [PENALTY_BASELINE_AUDIT.md](PENALTY_BASELINE_AUDIT.md).

The graph generator previously discarded self-loops/duplicates and could produce
nonregular graphs. It now preserves the requested degree using edge switches;
this **is not a uniform random-regular graph ensemble**. Exact penalty enumeration
now searches unbalanced strings, greedy swap gains were corrected, and missing
partition complements were repaired. All future datasets record actual edges.

## E01 — Haar scaling, actually executed

Input is one photon per first `k=n/2` modes, ideal lossless passive optics.
Mean intervals are marginal Student-t intervals over independent Haar draws.

| n | Haar circuits | Measured mean P_CF | Marginal 95% CI | Known expectation |
|---:|---:|---:|---|---:|
| 4 | 1,000 | 0.598496 | [0.589348, 0.607645] | 0.600000 |
| 6 | 1,000 | 0.358447 | [0.354071, 0.362824] | 0.357143 |
| 8 | 1,000 | 0.212118 | [0.210153, 0.214083] | 0.212121 |
| 10 | 250 | 0.125882 | [0.123940, 0.127824] | 0.125874 |

The law `binom(m,k)/binom(m+k-1,k)` is already known from
[Arkhipov–Kuperberg](https://arxiv.org/html/1106.0849v1), Proposition 1,
Corollary 2 and the distinct-birthday formula. Its balanced asymptotic is
`sqrt(3)*(16/27)^(m/2)*(1-1/(18m)+O(m^-2))`. It is an ensemble mean, not
an upper bound on optimized circuits. A permutation has P_CF=1 at every size.
Nor is `1/E[P_CF]` the mean waiting time for a Haar circuit drawn once and held
fixed. The notes also prove conditional Haar means by symmetry, rather than
incorrectly exchanging expectation and division. One of the 16 marginal
metric intervals misses its theoretical value; no simultaneous coverage was
promised. The four P_CF intervals all include their predictions.

Raw: [E01](../experiments/E01_haar_collision_baseline/summary.json).
Figure: [Haar scaling](figures/haar_scaling.png).

## E02/E04 — Does optimized state preparation improve?

Six families (path, cycle, regular, Erdos–Renyi, weighted, planted), two graph
seeds and three initial seeds per slot were declared before measurement. At
`n=4,6,8`, E02 compares full rectangular adjacent meshes and best-of-120 Haar.
COBYLA has a maximum of 120 calls; actual calls are retained. Here the loss is
minus the true optimal success probability: **this is an oracle state-preparation
diagnostic**, not an unknown-optimum algorithm.

| n | Bosonic COBYLA mean success | Distinguishable COBYLA | Bosonic best-of-120 Haar |
|---:|---:|---:|---:|
| 4 | 0.999789 | 0.999737 | 0.717213 |
| 6 | 0.795737 | 0.951101 | 0.186303 |
| 8 | 0.294974 | 0.691744 | 0.034819 |

Rounded values should be read with the raw summaries as authoritative. These
are descriptive averages over a fixed grid. Improvement relative to the first
circuit alone is partly imposed by best-so-far selection. The independently
budgeted Haar comparator is the relevant enrichment control.

E04 executes COBYLA, Nelder–Mead, SPSA and random mesh search at full and depth-2
meshes. Shallow performance is label-sensitive: fewer admissible outputs are
reachable. This can create apparent success on path/community labels. It is not
evidence that a shallow bosonic ansatz has a superior mechanism.

## E03 — Objectives and the algorithmic Pareto cloud

For `n=4`, all nine losses were actually optimized on the six-family grid.

| Loss | Mean P_CF | Mean physical success |
|---|---:|---:|
| Bad subnormalized CF moment | 0.013038 | 0.013005 |
| Conditional energy | 0.609711 | 0.607640 |
| Physical success (oracle) | 0.999877 | 0.999789 |
| Collision-aware energy, mu=2 | 0.999671 | 0.960115 |
| Log barrier, gamma=2 | 0.999522 | 0.960795 |
| Conditional lower CVaR, alpha=.25 | 0.683155 | 0.457878 |

The bad objective primarily suppresses accepted probability. Conditional energy
can become good without preserving acceptance. CVaR is correctly implemented but
its lower-tail saturation need not concentrate all probability on optima. Physical
success and its factorization are mathematically identical objectives; tiny
floating differences can alter optimizer trajectories and are not distinct
scientific formulations.

The plotted cloud is a **finite-budget algorithmic** comparison. There is no
unrestricted Pareto obstruction: a known optimum can be prepared with a mode
permutation, giving `(P_CF,P_opt|CF)=(1,1)`. The discovery cost is then classical.
See [the cloud](figures/objectives_pareto.png).

## E05b — Exactly matched ideal attempt counts, including training discovery

The first E05 compared maximum allocations, allowed early termination, and used
an analytic uniform training control. Its raw data are retained, but it is
**superseded for equal-cost claims**. Independent review required a new protocol.

E05b actually draws every training batch for every baseline: **120 calls x 256
ideal attempts + 4,096 independent heldout attempts = 34,816 per run**. There are
756 model runs and **26,320,896 simulated attempts**, with all sampled count
vectors retained. If COBYLA stops early, a fixed local-proposal rule fills the
remaining calls for every fitted model. Training uses conditional energy plus
`2*(1-P_CF)`, or the penalty QUBO energy; no true optimum enters either loss.
Each lambda is reported independently; choosing the best lambda would incur
all its training costs.

| n | Bosonic final mean success | Distinguishable | Uniform feasible | Median first optimum: bosonic / distinguishable / uniform |
|---:|---:|---:|---:|---|
| 4 | 0.652313 | 0.713285 | 0.527778 | 2 / 2 / 1 |
| 6 | 0.279549 | 0.536614 | 0.175000 | 15.5 / 11 / 4 |
| 8 | 0.067873 | 0.137707 | 0.059524 | 89 / 27 / 17.5 |

Every one of the 756 runs had already observed an optimum during training.
Final `1/P_success` describes repeat sampling after training; it does not describe
the cost of discovering the first optimum. Also, averaging `1/P_success` must
not be replaced by taking the reciprocal of average success: at n=8 the former
is about 806 bosonic attempts, 59.6 distinguishable attempts and 23.6 uniform
feasible attempts across this grid. Variation and outliers matter.

Wilson intervals apply to independent heldout counts for each fixed circuit.
Pooled intervals are descriptive; graph families, repeated path/cycle instances
and shared initial seeds are not iid draws from a graph population. No broad
significance or wall-clock speedup is claimed. Simulation uses enumerated cost
tables, including an optimum for retrospective scoring. Setup/runtime and score
lookups are retained; this exponential simulator is not an efficient hardware
implementation. Ideal attempts omit source/detection losses and are not QPU shots.

Figures: [final success](figures/equal_budget_success.png),
[first discovery](figures/discovery_cost.png).

## E07/E09 — Classical anchors and label falsification

Spectral partitioning alone solves 27 of 36 declared graph slots; a permutation
prepares each such solution with probability one without bosonic interference.
The hybrid's high mean success is therefore primarily a classical anchor result.
Remaining cases can have zero-start higher-order plateaus. No anchor was secretly
chosen using the true optimum, and no hard instance was removed.

E09 reoptimizes 12 underlying n=6 graph slots after the original labeling and
four independently seeded permutations, at two depths and two particle models:
240 model runs. For the depth-2 bosonic mesh, mean success changes from 0.875
on original labels to 0.802 on the permuted-label grid; **5 of 48 permuted slots
have a structurally unreachable optimum**. Full-depth meshes have no such
structural zeros in these cases. This demonstrates a reachability artifact;
it does not show that all shallow enrichment disappears after relabeling.

## E06/E08 — Falsification of the proposed mechanism

The collision-pair moment identity and its probability bounds pass 120 Haar
cases plus four disjoint-support controls. The initial E06 failed because the
upper-bound tolerance was accidentally cancelled in a chained assertion. Its
failed manifest and traceback are preserved; E06b fixes only that assertion and
passes. This was an implementation error, not a theoretical counterexample.

E08 checks 240 full-distribution circuits interpolating from disjoint support,
the spatial-overlap permanent bound and its efficiently computable cycle bound,
nine exact rational balanced counterexamples, and full Fock counterexamples at
n=4,8,12. All pass at tolerance `1e-10`. See
[counterexample figure](figures/collision_counterexample.png).

## Gates, limits and continuation

| Gate | Result |
|---|---|
| Physics / Perceval | PASS within documented ideal small cases |
| Objectives / weighted CVaR | PASS |
| Full binary classical penalty reference | PASS |
| Authentic optical ObliQ comparison | OPEN; no substitute has been relabelled as ObliQ |
| Ideal computational benefit dependent on interference | NO-GO for the tested route |
| New theoretical contribution relative to literature | OPEN |
| Noise study | DEFERRED: ideal signal does not justify it |
| QPU / Laurent handoff | CLOSED / withdrawn |
| Paper | FROZEN; PAPER_READY=FALSE |

Three live routes are distinguished: (1) the tested generic mesh/known-optimum
route is rejected as evidence for computational benefit; (2) the overlap
certificate/counterexample is mathematically validated, but its novelty audit
remains open; (3) useful optimum-blind, label-invariant, graph-informed search
against serious feasible classical algorithms remains open. Next work should
authenticate the exact optical ObliQ dynamics and compare query/discovery budgets
on harder preregistered instances. Scaling an unsuccessful optimizer or adding
noise would not close either gap.

## Reproduction and review

Environment: Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Perceval 1.3.0,
exqalibur 1.4.2. Direct dependencies are pinned in `pyproject.toml`; the full
installed environment is in `requirements-research-lock.txt`. Every main run
has a v2 manifest with command, seeds, timestamps, source commit, source hashes
before/after, package versions and raw-output hashes. Historical scripts are
retained at their recorded Git commits; later improvements do not overwrite runs.

For a portable replay, create a fresh output directory and use the command in
the selected manifest, replacing its interpreter with the local `.venv/bin/python`.
`PYTHONPATH=src` is required. The convenience launchers require the installed
Mathbox recorder at the documented path; the numerical scripts do not.

Independent reviews: [physics](PHYSICS_VALIDATION.md),
[Perceval](PERCEVAL_VALIDATION.md), [objectives](OBJECTIVE_VALIDATION.md),
[protocol](EXPERIMENT_PROTOCOL_AUDIT.md),
[new proof](NEAR_COLLISIONLESS_INDEPENDENT_REVIEW.md).
`experiments/audit_results.py` verifies stored hashes against current sources or
the exact historical Git commit, checks every equal-budget count vector and
first-hit block, and validates ideal probability bounds/factorization.
`experiments/plot_results.py` reproduces five standalone PNG/PDF figures.

The manuscript contains historical unvalidated text and is not an evidence
source. Earlier unsupported numerical claims are retained with withdrawal
annotations in `NEGATIVE_RESULTS.md` and `reports/feasibility_n4.md`.
