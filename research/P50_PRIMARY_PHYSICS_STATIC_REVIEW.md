# P50 primary: exact-freeze static physics review

2026-11-25. Target encoding commit
`0fbe635517cb2cbb32cb42fde7d9597943494ed1`; source SHA256
`6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf`.
The checked encoding worktree was clean at this commit. I read the ENTIRE
primary source, spec, both contracts, MD and all53 authored primary fixtures.
No import, test, DEV graph generation, numerical run or hardware call occurred.

**Verdict: no blocking physical/decoder/control-grid defect found; suitable
for the declared targeted qualification, conditional on its PASS and the
separate caller/resource review.** No numerical law, runtime, DEV outcome,
advantage or hardware capability is validated by this static receipt.

I did not author the primary code/tests. I supplied prior physics refinements,
the independent-marginal control definition and the bipartite counterexample,
and reviewed reused helpers. This is independent implementation review within
the same team, not a blind/external replication of my own earlier derivations.

## Physical source and every observation path

1. Source construction uses the full Fourier/eigenframe, with FIRST r columns
   occupied and the remaining columns vacuum. V=E R uses the frozen
   even@odd rotation and the gauge fixed BEFORE mixing. Keeping the original
   vacuum complement is correct because R preserves the occupied subspace.
   The source depends on the graph/independent marks, never a partition,
   incumbent, selected outcome or classical search. Occupied/boundary gaps
   and source/unitary/eigen residuals are guarded and saved.
2. Local B/D/b4 sampler ports are0..r-1. b4 uses contiguous source-port groups.
   No CF retry or herald is used. The batch checks retain the whole fixed-r
   integer count vector, including every collision. eta is1; r13/17 remains
   distinct from K25/50. Gaussian, coherent and product controls are not
   silently substituted as physical B sources.
3. Phase uses independent continuous phases and multinomial r counts; sphere
   uses a normalized complex Gaussian coefficient vector. Their mean is mu.
   Numerical categorical normalization is checked/reported. Sphere has only
   Fourier/E bases because right-unitary rotations give the same law.
4. Sigma_B=diag(mu)+|VV*|^2-2QQ^T is formed separately for each relevant V.
   Its actual real factor F clips only the declared numerical eigenvalue
   interval and masks exact empty/one-hot-one rows BEFORE H. Gaussian uses
   HFg, while the independent-final-variance arm uses sqrt(sum((HF)^2,row))*g.
   There is no post-H mask, reused nominal diagonal or R-invariance mistake.
5. Product-B marginals call the unchanged scalar row/PGF helper and sample
   the EXPANDED probabilities using independent uniforms/CDFs. They do not
   sample the shifted coefficients. Row/PMF/CDF repairs are saved; subunit
   rows are not rescaled. The classical total may differ from r, including0,
   and the batch deliberately permits that. Matching is before H, not a
   claim of matching final diffused marginals or an actual photon budget.

## Decoder, nulls and prospective population

H and the dmax=0 identity branch match the card. The max-anchored half-up
1e-12 bucket rule uses carried RANK-per-vertex, independently seeded jitter,
then returns exactly K sorted vertices. The tests cover boundaries separately
from relabel covariance, near-uniform fields and the subbucket inclusion
exception. Exact ranking requires positive click/empty margin; this bucket
requires margin>1e-12 plus numerical allowance. Fourier's gap1 or.8 is ample.
The reverse support inclusion is not misidentified as P44's clicked-only case.

One-photon categorical laws, monomial B/D determinism versus stochastic
phase/sphere, post-V phases, conjugation as a LAW (not same-seed backend
equality), generic-phi HOM amplitudes/coherence, pre-R gauge relevance,
actual covariance, deterministic-before-H fluctuations and the K3,3 maximal
cut witness are represented in finite fixtures. Their full-Fock checks use
untruncated small permanent enumeration in floating arithmetic, not exact
rational/interval certification. They remain tests to RUN, not observed PASSes.

The ten grids match ROOT02041c3: seven16-cell arms x2 train draws, sphere
and static8 cells x4, jitter2 cells x16. Every arm pays32 train+32 fresh
draws/case. Fourier static duplicates are deliberately retained and disclosed;
they are not independent discoveries or all nonredundant laws. Pure jitter
does not acquire a source/H parameter. All-shot equal-graph Fraction selection
and fresh role-separated evaluation do not use extrema, Cref or optima.
Private paid minima contain only their own scored training/evaluation cuts.

The NEW graph generator implements ER8/(N-1), RR8 and sorted-edge weights1..5
with the frozen seeds; it does not call the old hard-coded generator. All
four cases are prepared before training. Any numerical population failure
prevents successful-subpopulation selection/evaluation. Raw/partial files are
retained on failure; no automatic retry or graph substitution is implemented.

## Cost isolation and qualification boundary

Preparation is arm-local. B never constructs a covariance/factor, other-arm
PMF/CDF, anchor or search table. Its source/mu/H work, classical constructor
remainder, jitter/ranking/cut, aggregation and selection are metered; backend
setup/count generation and diagnostics/serialization are separated. Static
preparation and pure-jitter controls expose preparation/rounding effects.
The B-only allowance funds two separately invoked raw-A FAST algorithms,
without free features/partition; only eligible snapshots are used. Caller
and timing-envelope details also receive an independent adaptive review.

The source uses DENSE H matrices; the MD's phrase "sparse H" is not an
implementation description or an O(|E|) cost guarantee. Actual allocated H
and its multiplication are paid. The projected CPU45/wall75 and arrays/output
budgets are prospective engineering estimates, not measurements certified
here. Require74 actual preflight cases (53 primary+21 FAST), bounded runner
closure and all residuals/outputs before the single authorized main. A passing
qualification would still establish no useful optimizer signal.

## Exact execution closure

The contracts list19 main artifacts and20 preflight artifacts (the latter
adds its own contract). Checked SHA256 values follow; declared dependency
versions are pinned metadata, not re-imported/version-verified by this reviewer.

| Artifact | SHA256 |
|---|---|
| P50_minimal_count_field_probe.py | 6d0229c923c80ea4b29aa2075641540ddf6e983248dbadb76af0e1513c05d8cf |
| P50_minimal_count_field_spec.json | 5828c03c3a36855b5941bd8eb28771c49d84e6eb8321e570d936f44de0d07921 |
| P50_minimal_count_field_contract.md | 80ed6ba0b327fccf47e635b5d615c51d5f717b265137c5fd1675ec530b41096b |
| P50_minimal_count_field_execution_contract.json | d83cfe8b00475ba536bed1499bee287c855a1cf0e4f9f2730afd67ea2d69d01a |
| P50_minimal_count_field_preflight_contract.json | 8b7f18ecb5658c2ed8b2b195882fd88602494d8014140ee4dd424a797431f8ba |
| P50_EXECUTION_CARD.md (ROOT02041c3792a139cf294ca279f897ec9d6140e3bc) | c1616954b8a453530ddfc4481b2ce08f4b87a3c368f0784fb1c40efe69eff2bc |
| P50_MINIMAL_COUNT_FIELD_CARD.md | 2e856b07b68a6ec3af2f4a29897cde9ff115969f9156cf5aab79ee35c65f6235 |
| P50_FAST_FROM_RAW_API_CARD.md | 3a73269e3a98f853a2a7d0695f77e9efa06f65ad0914daf932ea1715c162ad91 |
| P50_fast_from_scratch_contract.json | 13e3f69d3073b5c5f42cc6a524e9566d9889b49d79f0b1708e65bce5d6fced5a |
| P50_fast_from_scratch.py | 6def5c0fe7c9fa41212e0584e151a654a2e606e7c090431530143523af100e86 |
| tests/test_p50_minimal_count_field.py | a4c6dce0cb3e213fd9530420486f37efd488e5ae544aa8decb36b23f8022f371 |
| tests/test_p50_fast_from_scratch.py | d70a3a37856312177c0c8c6f905a5504ff2cd776d70de2e08bf663a941381aa8 |
| P49_trained_source_probe.py | 384057373739a90bbe6ec0f37726324b222ceeed2609bec57ae0dfebd700b7f5 |
| P49_fast_classical.py | 018fef36d67ce31f14e9ed3e2e200ac11605dbffe9ed3670284862f3c9ba3fff |
| P48_spectral_pit_probe.py | b123bec4f67feb8ffc2255e0a56bc1181748a80bb716fe92328954a6f4d538ca |
| P48_coherent_marginals.py | a231a94578daf43993f62e393f1c58f90030a693ad2bf7722977ae65e181b2ac |
| P45_adaptive_probe.py | bb00ca61e45794ecea2333e0aa1864edfaec43128c1efa98dd8384c3d6889f92 |
| P43_global_gain_probe.py | b0507d36f56f3fedd92448043ec17fa7fcabf46c6efeaed40d23b61fc075f777 |
| pyproject.toml | 7d53e37a5ec3e59346cce1f8a4bb3319445c11647fa330ef7bf9547a82c3ebc4 |
| requirements-research-lock.txt | 3dcf2b0f35d6cc610243408ff2520f0b26a8545048f9b6c8ca45662f0f898ac1 |

Research filenames omit research/; pyproject.toml and the lock are at the root. Actual work:
read-only git-show/rev-parse/status, rg, complete sed/cat source/test/spec/
contract reads and shasum. No encoding/ROOT code, raw or paper was modified.
Only this new receipt is committed in the isolated replication worktree.
