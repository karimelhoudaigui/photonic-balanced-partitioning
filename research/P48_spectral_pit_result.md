# P48-B result: fixed spectral CF basis fails the positive gate

2026-11-25. Decision: **REJECT this frozen P48-B mechanism/population/budget
as a positive optimization result.** The physical subspace change is valid,
but the bosonic outputs do not beat strong classical controls. All evidence
is retained. This is not a no-go for all passive encodings, trained source
bases, feasible decoders or larger resource budgets. No P48 sweep, held-out
claim, QPU call or manuscript change follows from this result.

## Frozen protocol and real execution

Authoritative card: ROOT bfdff40926ad395a14f64260513b6ef21a1257f5, preserving
the earlier heat/Haar card42572d4 that was not run. The spectral source basis
was fixed before any P48 graph outcomes: first K eigenvectors of normalized
Laplacian plus0.001 diagonal marks, compared with a graph-blind Fourier basis;
fixed input ports0..K-1, orthonormal vacuum completion, no Haar source rotation.
The map never uses S0, Cref, optimal masks or a known partition.

Source history is retained: e87035a first unexecuted snapshot,4a199f8 adds
shared intensity/assignment preparation discoveries,5e06e8f fixes a Gaussian
deterministic-row risk identified STATICALLY BEFORE EXECUTION (not an
observed DEV bug). The exact structural mask and its injected-leakage fixture
received independent physics review. The coherent helper remains unchanged:
source6c980d3f684ef32295eeb394272f6218fbbc2402, SHA256
`a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac`;
26 independently qualified exact/control cases are preserved locally.

Combined preflight: **52 PASS** in16.03s,12 inputs unchanged, validated v2
manifest, committed **b0231b6**. One main ran on that CLEAN commit, with11
unchanged inputs and6 declared regular results. Source SHA256:
`b123bec4f67feb8ffc2255e0a56bc1181748a80bb716fe92328954a6f4d538ca`.
Runner status **completed**, exit0, wall **23.364239s**; script CPU **8.245435s**,
wall **22.429533s**. Enforced limits CPU60/wall90/thread1/log32MiB; planned
arrays256MiB, no hard memory/affinity promise. Directory **14,117,992 bytes**,
below32MiB. No retry, cap increase, truncation or case substitution occurred.

All4 cases passed numerical guards and all1792 proposals ran:256 per arm.
There was no numerical-inconclusive subpopulation. All collisions/zero counts
were retained, ideal eta=1 only; zero physical QPU calls/photons, no held-out
graph or exact optimum access. The primary manifest validated against inputs.
Primary raw/data and the subsequent audit contract were committed **95c2fa6**.

Data: `experiments/P48_spectral_pit/run_001/data/`.
Raw SHA256:
`5e423f0f649e58aad5fb21ca5af36f89e6bfdd55d0710258db9b6e05450e5b77`.
Summary SHA256:
`6cdb1e5c1cf8a05f549df6c770b052211c7846b87f27d78f4a10586ae242e5ea`.
Actual argv, versions, seeds, limits and hashes are in the manifest. Use its
frozen source/spec with a NEW output directory to reproduce the experiment.

## Optimization and classical explanations

Gain is max(0,Cref-cut), after sharing all actual common discoveries. Observed
minima below use each arm's complete declared budget over both trials.

| Graph | S0 cut | Common Cref | B | D | b4 | Gaussian | IID | Continuous phase | Sphere |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| n26 ER4802601 |168|168|168|168|168|168|168|166|166|
| n26 RR4802602 |52|48|46|48|39|48|44|44|48|
| n34 ER4803401 |347|315|312|312|315|315|309|314|315|
| n34 RR4803402 |73|56|56|56|56|56|56|56|56|

The decisive check is a SINGLE fixed feasible baseline, not an oracle portfolio:

| Graph | B | Anneal | Spectral+swap | Collective KL | Block matching | Spectral coherent rounding |
|---|---:|---:|---:|---:|---:|---:|
| n26 ER |168|166|166|168|168|168|
| n26 RR |46|39|46|48|48|48|
| n34 ER |312|301|312|313|315|315|
| n34 RR |56|56|56|56|56|56|

**Anneal equals or beats B on all four graphs** at the same declared informative
score ceiling. Full-K interference therefore fails the intended control gate.
The small B>D difference on n26 RR has stronger explanations in bounded species,
IID fields, continuous phases and feasible search. It is not a replicated
interference-dependent optimization result.

| Arm | Gain across all four settings | Best independently selected DEV setting gain | Positive events /256 |
|---|---:|---:|---:|
| B |7|5|3|
| D |3|3|1|
| Species of size at most4 |11|9|2|
| Gaussian_Bcov |0|0 (null)|0|
| IID uniform |12|6|3|
| Continuous-phase multinomial |13|5|5|
| Spherical-coherent multinomial |2|2|1|

Index order is Fourier/lambda0,Fourier/lambda1,spectral/lambda0,spectral/lambda1.
Selections are B3,D1,b4=0,Gaussian null,IID0,phase2,sphere2. No favorable graph
or setting was discarded. These small DEVELOPMENT samples do not certify a
ranking or a positive; neither held-out testing nor independent resampling ran.

## Preparation credit and resource ledger

Before sampling, all methods received128 signed spectral roundings and264
direct preparation candidates: top/bottom mu, every source-intensity column,
and labelled maximum-product assignments with explicit1e-300 floor. Their
cuts, sort/matrix work and time were shared. They were not photon successes.
The assignment maximizes a labelled product, not the permanent D support sum.

The actual Cref witnesses were the anchor on n26 ER, signed eigenvector2 on
n26 RR, **pure greedy completion** on n34 ER and signed eigenvector1 on n34 RR.
Thus the347→315 common improvement is a classical greedy discovery;73→56 is
signed spectral rounding. The added mu/q/assignment guards were evaluated but
did not further lower those incumbent minima on this population. No benefit
is falsely attributed to direct optical preparation or counted twice.

Shared frontend informative units are3969,3969,5632,6788 in graph order.
Each primary arm used34,688 inspected partial marginals and256 final cut
scores. Every baseline separately received3200/5536 informative queries per
n26/n34 graph/trial; no free best-of-five portfolio is used. Informative
evaluations are not every repeated helper invocation: some known cuts are
recomputed inside measured time, without generating an uncredited discovery.
Query timestamps and joint observed-time/score prefixes are retained.

B,D,b4 each used256 simulated optical attempts and3840 injected simulated
photons. Collision-containing observations were B255,D250,b4=254,phase256,
sphere255, all retained. No CF postselection occurred. Both coherent PITs are
analytic Decimal80, with **zero empirical calibration draws**. Production phase
sampling and nonpolynomial coherent rounding used continuous angles throughout.
This does not establish physical preparation efficiency, loss tolerance,
throughput, hardware compatibility or a simulator-to-QPU time advantage.

## Physical/numerical mechanism and consistency checks

Every guarded gap was well above1e-12. Minimum gaps by graph were
0.01367619336,0.00498835740,0.00223529158,0.00528405098. All N-1 gaps were
saved; only internal occupied and boundary gaps entered the source guard.
Independent unitary residuals were<=1.78e-15, source spectral residuals
<=4.17e-16, covariance reconstruction residuals<=4.45e-16. No probability
row-mass repair was needed on these actual graphs. No empty/deterministic
Gaussian rows occurred in DEV; their defense was exercised by preflight.

Squared offdiagonal projector Frobenius mass for spectral V was
4.1388078365,5.9508345958,5.2532152097,7.7839815860; Fourier values were
6.5,6.5,8.5,8.5. The new nondiagonal occupied subspace is physically present.
Its presence, valid covariance and dense correlations do not imply useful
search beyond classical spectral/coherent preprocessing.

One bounded stdlib-only read-only audit ran after its source/contract freeze,
without any new sampling. Evidence:
`research/P48_spectral_pit_raw_audit/run_001/manifest.json` and
`research/P48_spectral_pit_raw_audit/run_001/data/receipt.json`.
Its v2 manifest completed/validated with9 unchanged inputs and all six primary
hashes matching before/after; internal wall3.527142s. It independently checked:

- ALL184,080 recorded feasible cuts, using94,411 distinct subset/cache entries;
- all1792 full primary decoders and88 common frontend decoders;
- all128 signed spectral and264 preparation candidates, including matching
  feasibility/log-cost/floor metadata (no extra claim of large-instance solver
  optimality beyond its preflight and implementation);
- all1280 count-PIT and256 Gaussian-PIT fields, all common incumbents/gain sums,
  and all174,720 baseline informative-query/time-prefix records;
- source-port/first-column equality, unitary/eigen/Gram/covariance identities,
  gap guards, subunit repairs and mean/normalization of all marginal tables.

This is data consistency reconstruction, not an independent sampler replication,
an interval proof, joint-copula certificate or significance test. P48 is archived
as a failed positive gate. Any next source-basis/training mechanism requires a
new frozen question and actual feasible-cut objective, not a rerun of this grid.
