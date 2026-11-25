# P50: minimal count fields fail the declared positive gate

25-Nov-2026. Primary data and independent-code consistency checks are complete.
**No positive accepted on this DEV panel.** The cheap decoder
is a real change from P45--49: it uses all counts, no Cref/PIT/greedy completion,
and separately measures B-only preparation and classical decoding. Nevertheless
it fails both the preparation-null mean comparison and the separately budgeted
from-raw feasible-search comparison. This is a finite rejection of THIS family
and campaign, not an impossibility theorem for photonic optimization.

## Frozen physical question and actual evidence

New weighted ER/RR graphs N50/r13 (seeds5005001/5005002) and N100/r17
(5010001/5010002), K=N/2. New generator, not the old hard-coded generator:
ER p=8/(N-1), RR degree8, sorted-edge PCG64 weights1..5. The source is optimum
blind: Fourier, marked spectral E and the two frozen E R source rotations.
Gauges precede R, all occupations/collisions remain useful, ideal eta=1.
Decoder is balanced ranking of H(n-mu)+beta*zeta, alpha0/1 and beta0/.1, using
the prospective max-anchored1e-12 buckets and carried priority. No optimum,
reference partition, trained incumbent or evaluated result enters the source.

Primary source frozen0fbe635, independent pre-outcome caller/physics reviews
d6ce9fc/2e83846 PASS statically. Card02041c3 synchronization and a DOCONLY
dense-H correction preceded tests. Qualification at clean c5805d7:
**74 PASS** (53 primary +21 independent FAST cases), validated v2 record,
20 unchanged inputs,1.329261s runner wall. Qualification alone is not a full
suite or a positive scientific result. Receipt:
`research/P50_minimal_count_field_preflight_receipt.md`.

The ONE main ran on clean **53102576e4aebf9ed633b9055f64715e7a479324**;
script SHA256
`6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf`.
Result **completed/exit0**,21.615873s runner wall, script6.595232s CPU /
20.703017958s wall. All19 input hashes unchanged, all14 declared results
present/regular; v2 manifest validated with --root. Enforced CPU60/wall90,
thread1/log32MiB, planned arrays256MiB (not a hard Darwin memory/affinity cap).
New output18,687,071 bytes, below32MiB. All4 cases and all2,560 proposals
completed; no retries, cap changes or graph substitutions. Perceval/cache/font
warnings from local cold imports remain in stderr and are not QPU timing.

Data sealed BEFORE raw audit in **fb5a36ec0746c3465dc7ee3a3c6b88a86b490e7d**:
`experiments/P50_minimal_count_field/run_001/` (14 results +3 runner records).
Raw SHA256:
`c19f8cc9f890ece810dad0549c0ca8b3d7785ed6a41f210ef51d10b4f54dc77b`.
Summary SHA256:
`f55b64daa9e9eff7c821023433f9ee48c3ccaf33e0ec99e3189bc81bd457682b`.
Manifest SHA256:
`b0a748292d39076321401863dd53dfad9f692dc9f9ab1b32752583896040b60f`.

## Actual all-shot selection and fresh evaluation

Every arm paid32 training and32 NEW evaluation draws per graph,128+128 total.
Seven full grids have16 settings x2 training draws; sphere/static have8x4,
pure jitter2x16. Model-specific selection minimizes the exact Fraction mean
of ALL cuts divided by their graph weights, equally across all4 graphs.
Each frozen policy is then evaluated with two fresh16-draw seeds per graph.
No minimum/improvement label or evaluation result enters training/selection.
The numbers below are finite DEV observations without significance claims.

| Arm | Selected setting | Training normalized mean | Fresh normalized mean |
|---|---|---:|---:|
| B | Fourier, alpha1, beta0 (ID2) |0.406241910|0.407747668|
| D, independently reoptimized | E, alpha1, beta0 (ID6) |0.408483065|0.414433450|
| b4 contiguous ports | Fourier, alpha1, beta.1 (ID3) |0.398461038|0.420696219|
| Continuous phase | E R(phi=pi/2), alpha1, beta0 (ID14) |0.390290098|0.405768478|
| Gaussian B covariance | Fourier, alpha1, beta.1 (ID3) |0.401969266|0.417533220|
| Independent final Gaussian variances | E R(phi=0), alpha1, beta.1 (ID11) |0.492064582|0.507099670|
| Independent B input marginals | E R(phi=0), alpha1, beta0 (ID10) |0.396740607|0.410770854|
| Spherical coherent | Fourier, alpha1, beta0 (ID2) |0.410095657|0.407206362|
| Static preparation | E, alpha1, beta0 (ID6) |0.362821548|0.362821548|
| Pure jitter/ties | beta0 (ID0) |0.502834911|0.502834911|

All exact fractions and losing training cells remain in summary/raw data.
The predeclared static E policy uses no photons, is deterministic at beta0,
and has a better observed global mean than B. Continuous phase and sphere
also have slightly better observed fresh means; no statistical ranking is
inferred from those small differences. B>D alone does not establish the target
mechanism. B chose the blind Fourier source rather than a graph spectral
source; H still uses the graph, so this fact does not remove graph dependence.

The independent marginal control matches the input B one-mode PMFs numerically,
not a fixed total count and not marginals after H. Gaussian independent final
variance uses row norms of the ACTUAL masked H F. It does not discard a row
that becomes fluctuating by diffusion. Fourier static cells duplicate the
pure-jitter/tie law; all preregistered cells/efforts were retained. No claims of
multiple independent discoveries are inferred from these duplicate settings.

## Private paid minima are separate from means

Each entry is **training / fixed-policy fresh evaluation / total paid minimum**.
Training minimum includes every paid setting; no minimum is gifted to another
model, inserted into a source or used to refresh an incumbent/Cref. Unlike P49,
there is NO free reference partition; every entry below was actually scored.

| Arm | N50 ER | N50 RR | N100 ER | N100 RR |
|---|---|---|---|---|
| B |206/203/203|231/217/217|381/353/353|444/403/403|
| D |205/196/196|230/210/210|378/385/378|450/390/390|
| b4 |186/167/167|214/221/214|404/384/384|437/429/429|
| Continuous phase |196/180/180|223/202/202|378/375/375|420/386/386|
| Gaussian B covariance |195/206/195|224/209/209|405/379/379|419/414/414|
| Independent final variance |225/201/201|286/273/273|483/463/463|546/561/546|
| Independent B input marginals |206/190/190|223/224/223|335/330/330|441/408/408|
| Spherical coherent |200/173/173|225/216/216|375/366/366|431/405/405|
| Static preparation |191/191/191|227/227/227|404/404/404|409/409/409|
| Pure jitter/ties |251/251/251|253/327/253|485/509/485|523/630/523|

Static's better mean does NOT imply that it beats B's minimum on every graph.
The optimization-search gate is instead directly refuted by each independent
FAST algorithm below. No favorable graph or free portfolio is needed.

## From-raw feasible search under the prospective B-only envelope

Every classical call pays raw conversion/validation, OWN seeded priority and
random or spectral initialization, complete best-pair descent FIRST, then
incremental annealing/perturbations/restarts. No paid B partition, eigensystem,
priority or reference is supplied. Both calls independently receive the same
B-only WALL-derived CPU envelope; they are not a free best-of-two portfolio.

| Graph | Paid B min | Random-first eligible min | Spectral-first eligible min | CPU grant EACH |
|---|---:|---:|---:|---:|
| N50 ER |203|138|138|0.016116658s|
| N50 RR |217|181|175|0.002911746s|
| N100 ER |353|254|244|0.009484743s|
| N100 RR |403|297|280|0.005415529s|

Both fixed classical algorithms strictly beat paid B on all4 graphs. All eight
initializations, first scans AND initial descents completed before their CPU
deadlines; all comparisons have an eligible result and no early proposal cap
or wall safeguard. Completed informative work counts are random-first
109034/18477/225333/139133 and spectral-first102135/15881/144581/84085; these are
diagnostics, not CPU-equivalent score prices.

These are the deadline-eligible ANYTIME prefixes, available in RAM before the
timestamp. The full completed run/export may overrun its allowance; actual CPU,
wall/overruns, late results and complete compact traces remain recorded.
No exact physical stop-latency promise, post-deadline unpacked improvement or
overall-late best is credited. Here overall late minima happen to equal the
eligible minima, but eligibility is selected independently from those values.

B-only preparation WALL was0.011079125/0.000865752/0.006246627/0.002097624s.
Each graph's grant adds ONLY B classical constructor setup, ranking/cut and
aggregation across its32 training +32 evaluation =64 B proposals, plus one
quarter of global B selection. Other-model PMFs/covariances/diagnostics, cold
optical backend setup, count generation and serialization grant ZERO.
Measured adapter CPU2--5us is subtracted before each solver call.

Across all4 graphs B spent0.002020795s classical batch setup,0.011234754s
classical postprocessing,0.000166206s aggregation and0.000217792s selection.
Numerical backend setup14.890875585s wall and synthetic count generation
2.554108382s wall were separately recorded/excluded, not claimed free in real
hardware. First-case wall/CPU differences are retained rather than normalized
away. This is a prospectively declared implementation envelope, not a minimal
universal B cost or measured QPU speed comparison.

## Scientific conclusion and pending independent checks

All optical arms used3,840 simulated injected photons,1,920 each train/eval,
zero physical QPU photons. Count failures/collisions are not postselected.
The ideal experiment does not supply measured preparation, loss, detector,
programming or latency resources for a real circuit. No hardware-compatible
small circuit, held-out panel or independent physical-sampler replication is
licensed by this result. P33/P37/E05b and the existing manuscript are intact.

The independent-code audit is a POSTHOC consistency reconstruction of these sealed
data. Its author was told the negative sign before freezing that audit; it is
not a blind replication or a new physical sampler. No additional author raw
audit was run here. Audit source72009e was frozen before its unique execution:
1.579610s wall /1.287177s CPU, completed with17 unchanged inputs and no fatal or
failed check. It reconstructed2,560 events in113 groups and reported53,205
checks. Code SHA256 is
`129128d37c04fb53dd9f3305d3d55c81fc090b127d78bab3d4ec979e0b48266b`.
The audit receipt/results are sealed in
**041a206c34bcb17a867ea7810360ec1591c6e684**, integrated by ROOT and v2-validated
against its branch. Receipt: `research/P50_minimal_count_field_raw_audit.md`;
manifest/results: `research/P50_minimal_count_field_raw_audit/run_001/`.
Audit manifest SHA256:
`2e59a5bfdf68174daf75c95573d0622e800e23e76465574f9bb8c8a7f83da9cb`.
No primary data is edited.

The auditor imports no primary/helper implementation; scalar edge sums, exact
Fraction objectives and a different PGF binomial-moment check reconstruct the
recorded evidence. Its author also authored FAST/proposed this decoder, a
shared-context relationship explicitly disclosed in that receipt. Independent
physics/root reviews are separate. No RNG trajectory redraw, external timing
authentication, replay of unsaved FAST proposals, interval/tail certificate or
independent physical sampling follows from the consistency checks.

ROOT separately reported **751 PASS** for the full integrated suite and
verified602 historical artifacts plus the existing manuscript/PDF unchanged.
This is distinct from this author's74-test targeted preflight. No additional
sampling, new seed/cap, model variant or physical validation followed the result.
The finite conclusion remains: the declared P50 count-field optimizer does not
survive its strong controls. The broader discovery objective remains OPEN.
