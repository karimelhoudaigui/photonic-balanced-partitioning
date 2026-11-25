# P46 result: bulk transport and PIT do not pass the positive gate

2026-11-25. Decision: **REJECT the frozen P46 family/grid/budget as a positive
optimization result.** Preserve the data; proceed to a physically different,
mathematically directed graph map. This is not a theorem excluding every
completion decoder, graph map, photon source or passive photonic algorithm.

## What was actually run

Source freeze7c1c36c; first preflight9 PASS preserved4208316. Independent
review found Gaussian PIT must normalize by the actual eigensystem factor
variance after clipping, rather than the target diagonal. That correction,
its target/residual diagnostics and an extra test were committedb1535f8
before any development outcomes. Second preflight10 PASS preserved642d9f7.
Adaptive exact-hash static PASS is recorded independently inb7b64c680b4eff290dd1ef4bba50cdaa83424fa2
(`research/P46_review_encoding_b1535f8.md`, reviewer's isolated worktree).

The one permitted main run used a clean642d9f7 checkout, code SHA256
`721cc9f3ee6ba1d604ae29130fb25d092a21bcc756e8d4b4a42e6238d47c315c`.
All4 development graphs and all planned1536 proposals were completed:
256 each for B, D, b4, Gaussian_Bcov, IID and conditional_phase. Every arm
used the same8 settings, two trial seeds, charged decoder and common incumbent.
No exact optimum, optimal mask, held-out graph, loss gate or hardware was used.

Runner: `experiments/P46_bulk_pit/run_001/manifest.json`, v2, **completed**,
19.968032s total wall,9 unchanged input hashes,6 declared results present,
CPU60/wall90/thread1 caps. Script-internal CPU5.222698s, wall18.957089s;
directory5.8MiB, below32MiB. The validator passed against current inputs.
Cold Perceval/Matplotlib imports and temporary cache warnings affected the
observed timing; this is not a QPU latency or runtime-advantage measurement.

Raw SHA256:
`de3ae25390ef9358467ae416414d48d548cdd975b50b041bcc01844b6dd8b2a5`.
Summary SHA256:
`7337f26fbe9e5fa3b4f330fe1576b47fe6aef952532aeb3f403553cd0fc4dabb`.
Data/contexts, true argv, seeds, versions, output hashes and both preflights
are retained unchanged. Reproduction uses the frozen source/spec and the
runner command in the manifest, with a NEW output directory.

## Optimization results and shared discoveries

Gain is max(0,Cref-cut); every scored common discovery is credited first.

| Graph | Source cut | Common Cref | B best observed | D best observed | Gaussian best observed |
|---|---:|---:|---:|---:|---:|
| n24 ER4602401 |143|142|135|135|135|
| n24 RR4602402 |45|38|38|38|38|
| n28 ER4602801 |232|229|226|229|226|
| n28 RR4602802 |72|48|47|47|47|

These are observed best cuts over each arm's full development budget, not
held-out performance or favorable graph selection. The strongest gains over
S0 often came from the shared classical completion frontend itself, especially
72→48 on n28 RR; B's additional unit gain there is reproduced by D/Gaussian
and the annealing baseline. The n28 ER B excursion is reproduced by Gaussian
and several feasible searches. There is no interference-specific discovery.

| Model | Total gain across all8 settings | Gain of independently selected DEV setting | Improvement events /256 |
|---|---:|---:|---:|
| B |21|7|7|
| D |14|9|5|
| b4 |20|7|5|
| Gaussian_Bcov |32|8|8|
| IID |19|8|8|
| conditional_phase |21|7|6|

The selected B setting is index5: **p=.5,zeta=0,lambda=1**, the graph-blind
Fourier ablation. The guided-zeta settings did not create a stable positive
signal. All settings and negative outcomes are retained; these small samples
do not supply a statistically certified ranking. Phase PIT uses the declared
approximate unconditional4096-draw marginal calibration; no exact-copula or
relative-tail guarantee is inferred.

## Feasible searches and resources

Each baseline independently used3008/4064 actual feasible cut queries per
n24/n28 graph/trial, equal to the primary arm's partial-marginal plus final-cut
budget. The table lists the observed minimum over both trials, including Cref.

| Graph | Anneal | Spectral+swap | Collective KL | Shared-Delta block matching |
|---|---:|---:|---:|---:|
| n24 ER |140|140|135|142|
| n24 RR |38|38|38|38|
| n28 ER |226|226|226|226|
| n28 RR |47|48|48|48|

No one baseline dominates B on every graph in this table; taking the best of
all baselines would require its complete combined budget. That qualification
does not rescue P46: the independently selected D and simple Gaussian/IID arms
already match or exceed B's selected pooled gain, the selected B network is
graph-blind, and all best B cut values have classical explanations in the tested
controls. Per-query observed-time prefixes and score caps are saved separately;
they do not turn this pilot into a throughput or hardware result.

Each primary arm consumed28032 inspected partial cut marginals and256 final
cut scores. B/D/b4 each used256 simulated optical attempts and3328 injected
simulated photons; all collisions were retained. The common setup used65536
classical calibration draws. These are not QPU shots. Common score units by
graph were4046,4478,5866,5670, charged once and shared with every method.
Numerical marginal evaluation/calibration, matrix work, ordering and all known
frontend candidates were included in that common account.

A read-only stdlib consistency pass over all119244 raw records independently
recomputed every recorded feasible cut from saved integer adjacency and subset
(reconstructing common-anchor swaps from their saved source trace), using40888
distinct subset/cache entries. Counts:3740 anchor,680 swaps,136 decoder
frontend,1536 development and113152 classical-query records. Every sample count,
saved PIT field, gain sum and baseline-query count matched the summary.
Its receipt is `research/P46_bulk_pit_raw_audit_receipt.json`; this is a data
consistency check, not independent resampling or a distribution certificate.
Collision samples: B159,D133,b4=150,conditional_phase159, all useful to the
decoder without postselection. Strong physical/cost conclusions remain open.

## Consequence

P46 fixes thin photon transport and marginal-scale imbalance, but its chosen
complex polar perturbation has no certified descent direction for the shared
cut proxy. Better transport, changed collisions and standardized marginals do
not imply useful graph correlations. The next route must change that graph
map with an independently checked mathematical discriminator, rather than
retuning this negative grid or editing the manuscript. No QPU gate is opened.
