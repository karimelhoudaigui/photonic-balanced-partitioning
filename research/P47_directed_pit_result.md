# P47: a valid proxy direction does not pass the optimization gate

2026-11-25. Decision: **REJECT this frozen P47 population/grid/budget as a
positive optimization result.** Preserve the exploratory B-versus-D difference
without presenting it as an advantage. No P47 rerun, held-out test, paper edit
or QPU call is authorized by this result. A different route needs its own
mathematical discriminator and preregistration.

## Frozen source, reviews and execution

P47 is a NEW copy of P46, whose complete negative evidence remains preserved
in fa3740c. The new real, cost-directed polar step and prime K=13/17 protocol
were committed in **695b5d2** before numerical work. Physics independently
checked that exact code/hash and the 13 finite test cases. Source SHA256:
`fac164f64a3ba15a061c56547be58f5c540486852c9016ccc70a129637ca53b1`.

Targeted preflight: **13 PASS**, 16.92 s, unchanged eleven inputs, runner v2
completed; receipt committed **7a4cd49**. This is a targeted preflight, not a
claim that the full repository suite had already run. The one authorized main
ran on clean 7a4cd49, with ten exact input artifacts, CPU60/wall90/thread1,
six declared results and no truncation. Runner wall **23.057314 s**, script
CPU **8.458426 s**, script wall **22.1738045 s**, directory **7.3 MiB**.
The primary manifest validated against current inputs. Raw and its later
consistency-audit contract were committed **6bbaed9** before that audit.

Primary data: `experiments/P47_directed_pit/run_001/data/`.
Raw SHA256:
`aa1386b93104ba1941ebc9d0cdde8488278f86a9bfeb7cd6f0632a83b359d562`.
Summary SHA256:
`e2187b5c2a2c3abd79bc8d02076e0fe0e0b1a0a071c8520589e0705df66dad2e`.
The manifest records the actual argv, versions, seeds and all result hashes.
Every graph, setting, collision and failed proposal was retained. No optimum
value, optimum mask, favorable graph filter, CF postselection or known-solution
preparation entered the algorithm. Transmission was ideal eta=1 only.

## Routing proxy: the new mathematical discriminator works

All four nonzero centered graph signals produced a numerical strict decrease
of the correctly oriented single-swap routing proxy. At either p, guided1 gives:

| Graph | Normalized proxy change | Squared Frobenius response ||W-F||² |
|---|---:|---:|
| n26 ER 4702601 | -0.1322642481 | 0.0367728043 |
| n26 RR 4702602 | -0.0630905923 | 0.0092330659 |
| n34 ER 4703401 | -0.1627497423 | 0.0540833877 |
| n34 RR 4703402 | -0.0606301542 | 0.0086643287 |

The graph-blind Fourier ablation changes that proxy only at roundoff scale.
The finite inequality, physical graph-index intensity reconstruction and
prime/composite boundary fixtures passed the declared checks. The prime
condition avoids exact centered stationary directions; it gives no extensive
response guarantee. Small response remains visible in this table.

This is a classical routing/assignment proxy, shared with D and all classical
methods. Its reduction does not equal the cut of a simultaneous exchange,
does not certify favorable nonlinear decoder behavior, and does not itself
demonstrate any optical or computational advantage.

## Optimization results

Gain is max(0,Cref-cut), after crediting every common frontend discovery.
Each primary arm has 256 proposals over four graphs, eight settings and two
fixed trials. Selection is independent per arm on this same DEVELOPMENT data.

| Model | Gain over all settings | Gain of selected setting | Positive events /256 |
|---|---:|---:|---:|
| B | 22 | 10 | 5 |
| D | 0 | 0 (selection null) | 0 |
| Species of size at most4 | 9 | 4 | 4 |
| Gaussian_Bcov | 2 | 2 | 1 |
| IID uniform | 14 | 6 | 4 |
| Conditional phase, four roots | 9 | 6 | 3 |

B selects index6: p=.5, guided1, decoder lambda0. The other non-null indices
are b4=2, Gaussian=3, IID=2 and phase=2. All settings and their full exploration
costs remain in the data. B's separation from D is a small exploratory signal,
not independently replicated or statistically accepted. It is based on five
improvement events on two n26 graphs; neither n34 graph improves under B.
The phase comparison retains the exact frozen FOUR-root sampler and its
approximate unconditional 4096-draw PIT calibration. No continuous-phase
oracle was substituted, and no joint calibration or interval guarantee is
asserted.

The decisive feasible-search check rejects the positive gate:

| Graph | Source S0 | Common Cref | B best | Anneal best | Spectral+swap best | KL best | Block matching best |
|---|---:|---:|---:|---:|---:|---:|---:|
| n26 ER |154|154|146|146|150|146|148|
| n26 RR |48|37|35|35|37|35|37|
| n34 ER |359|359|359|359|351|357|359|
| n34 RR |69|66|66|49|49|57|66|

These minima use each method's complete declared budget over both trials.
**One fixed baseline, anneal, equals or beats B on all four graphs.** This
comparison does not select a different winning baseline per graph. Spectral
and KL also reveal missed improvements on n34 ER, and conventional searches
substantially outperform B on n34 RR. A valid routing-proxy direction plus
B>D on development data is therefore insufficient for the intended result.

## Costs and limits

Every primary arm used 34,688 inspected partial cut marginals plus 256 final
cut scores. n26/n34 decoded proposals cost 100/173 declared informative units;
each baseline received 3200/5536 feasible candidate evaluations per graph/trial.
These units track informative evaluations, not every function invocation:
some already known initial cuts are recomputed inside the observed wall time.
Such repeats create no uncredited new discovery. Common frontend score units
are 4576,4576,8754,7887 in the table's graph order, shared once across all arms.

B, D and b4 each used 256 simulated optical attempts and 3840 injected
simulated photons. B had 189 collision-containing samples, D142, b4=144,
phase180; all were retained. The common phase setup used 65,536 classical
calibration draws, plus charged PMF, ordering, matrix and decoder work.
No physical source/loss/latency or resource advantage is established.
Per-query observed-time frontiers are in the raw/summary and were checked;
cold imports, filesystem caches and recording costs prevent treating one
offline timing run as a hardware-performance result.

## Independent data consistency reconstruction

The author ran one separate, bounded **stdlib-only, read-only** checker after
freezing its source/contract. It is not an independent resampling of B and
does not supply a statistical replication. Evidence:
`research/P47_directed_pit_raw_audit/run_001/manifest.json` and
`research/P47_directed_pit_raw_audit/run_001/data/receipt.json`.
Runner v2 completed and validated, all nine inputs unchanged; internal wall
2.425166 s. Every six primary result hashes matched both before and after.

All **147,811 raw records** were inspected: 5447 anchor candidates,916 shared
swaps,136 shared decoder candidates,1536 primary proposals,139776 classical
queries. Every recorded feasible cut was independently recomputed from integer
adjacency and the subset, with anchor sources reconstructed from their trace.
The cache covered 60,509 distinct subsets. All1536 complete decoders were
independently reconstructed, including every greedy choice, marginal, tie
priority and score count. All1024 saved count-PIT fields and256 Gaussian-PIT
fields matched their saved tables/factor variances. Common incumbents, gain
totals, baseline query counts/time frontiers and graph-index routing-proxy
identities matched. This confirms data consistency within the declared numeric
tolerances; it does not certify the full sampler, rare tails or empirical copula.

P47 is archived as a failed positive gate with a retained, unconfirmed B>D
development signal. The next mechanism must change more than a tuning grid
and must again survive strong classical search before opening held-out/QPU work.
