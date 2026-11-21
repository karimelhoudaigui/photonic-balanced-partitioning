# Phase 3 threshold and photon-budget audit

**PASS within the declared domain:** both draft loss formulas and the threshold channel agree with independent calculations. **NO-GO for extrapolating Haar counting into graph-optimization or quantum advantage.** The lossless plateau is correctly scoped in the original draft; the counterexamples below reject extending it to a different loss model or resource criterion.

Base checkpoint: `8edfca70f03555479ea62ef9c49d727a27cc1861`. Worktree: `.qwen/worktrees/phase3-threshold`, branch `research/phase3-threshold`. No principal source, manuscript, QPU interface, or shared scientific status was edited. New algebraic corollaries are self-derived and self-reviewed here; coordinator reconstruction remains the independent acceptance step. Novelty is not claimed.

## What the audit establishes

Three operational questions select different encodings: maximize success per attempt; minimize expected injected photons until success; maximize success before a fixed total photon budget is exhausted. A fourth distinction—accepting k threshold clicks versus additionally detecting every injected photon—can reverse the ranking. These distinctions matter even before graph-specific training.

The source domain also matters. Haar counting permits a fixed normalized N-photon input with N>m, including bunched inputs. The audited `ThresholdEvaluator` instead prepares one photon in each of the first N modes and is limited to even m and N<=m. Optimizers outside this cap are statements about a different source requirement, not executable circuits in that evaluator.

## Exact counterexamples and decision rules

For m=4,k=2 and uniform efficiency eta=1/2, the probabilities are:

| injected N | inclusive k-click probability | success per injected photon | expected photons until first success | all-N-detected probability |
|---:|---:|---:|---:|---:|
| 2 | 3/20 | 3/40 | 40/3 | 3/20 |
| 3 | 3/10 | 1/10 | 10 | 3/40 |
| 4 | 57/140 | 57/560 | 560/57 | 9/280 |

Thus N=4 has 19/14 times the minimal encoding’s expected feasible hits per photon in the independent-Haar model, and 14/19 times its expected first-success photon cost. Requiring all N photons to be detected reverses the comparison: the N=4 probability drops below N=2. Threshold-only detectors cannot generally observe that additional all-N condition for N>k; a separate number-resolving/heralding assumption is required. The result is a protocol comparison, not an optimization advantage.

For the same four-mode source cap, the exact efficiency phase diagram is:

| criterion | eta range | optimal N |
|---|---|---|
| probability per attempt | 0<eta<(21-sqrt(21))/20 | 4 |
| probability per attempt | (21-sqrt(21))/20<eta<1 | 3 |
| expected injected photons | 0<eta<(28-sqrt(154))/30 | 4 |
| expected injected photons | (28-sqrt(154))/30<eta<3/4 | 3 |
| expected injected photons | 3/4<eta<=1 | 2 |

There are adjacent ties at the transition points, approximately 0.8208712153, 0.5196775451, and 0.75. At eta=1 the per-attempt maximizers are N=2,3; at eta=0 no finite expected success cost exists. The polynomial formulas and pairwise comparisons are in the [contract](../research/phase3_threshold_contract.md).

Without loss, the balanced per-attempt maximizers are N=m-2,m-1, as in the draft. Per-photon efficiency instead selects N=2 for m=4, N=3,4 for m=6, and uniquely N=m-3 for even m>=8. The ratio proof covers every integer N>=k, including N>m; a finite exact search through 4m independently checks even m=4,...,40.

Finite budgets use a different criterion. At m=8,eta=1,B=30, N=5 uniquely maximizes success per photon, but N=6 maximizes stationary success within B. Both divide 30, so this comparison is not caused by rounding unused photons:

| stationary N | probability per attempt | success within B=30 |
|---:|---:|---:|
| 5 | 35/99 | 872760672665/941480149401 |
| 6 | 175/429 | 13473469652125/14530697473149 |

The exact difference is `81330985365280/349564989111545493`, approximately 0.0002326634. The raw record also evaluates an exact dynamic program allowing different N on successive failed attempts; it does not confuse that allocation problem with a stationary sampler.

A fixed interferometer need not follow the Haar ranking. With U=identity,m=4,eta=1/2, the inclusive probabilities for N=2,3,4 are 1/4,3/8,3/8. Their photon efficiencies select N=2,3, whereas the Haar model selects N=4. Likewise, replacing nonuniform detector efficiencies by their average is invalid: with m=2,N=2, efficiencies (1,0), two clicks are impossible, while substituting average eta=1/2 into the uniform-loss law gives 1/12.

## Operational grid with explicit source caps

These rows are exact rational maximizations; the displayed photon cost is rounded for reading. The complete grid additionally includes eta=3/4,9/10 and three finite-budget allocations per row. A cap of 4m is a bounded generalized-source search, not a proof of unrestricted lossy optimality.

| m | eta | N cap | best per-attempt N | best expected-photon N | minimum expected photons |
|---:|---:|---:|---|---|---:|
| 4 | 1/4 | 4 | 4 | 4 | 25.5271 |
| 4 | 1/4 | 16 | 14 | 7 | 21.4868 |
| 4 | 1/2 | 4 | 4 | 4 | 9.82456 |
| 4 | 1/2 | 16 | 7 | 4 | 9.82456 |
| 4 | 1 | 4 | 2,3 | 2 | 3.33333 |
| 4 | 1 | 16 | 2,3 | 2 | 3.33333 |
| 6 | 1/4 | 6 | 6 | 6 | 92.3399 |
| 6 | 1/4 | 24 | 22 | 14 | 45.7274 |
| 6 | 1/2 | 6 | 6 | 6 | 21.8483 |
| 6 | 1/2 | 24 | 10 | 7 | 21.0448 |
| 6 | 1 | 6 | 4,5 | 3,4 | 8.4 |
| 6 | 1 | 24 | 4,5 | 3,4 | 8.4 |
| 8 | 1/4 | 8 | 8 | 8 | 283.362 |
| 8 | 1/4 | 32 | 30 | 21 | 75.6295 |
| 8 | 1/2 | 8 | 8 | 8 | 41.1969 |
| 8 | 1/2 | 32 | 14 | 11 | 35.1086 |
| 8 | 1 | 8 | 6,7 | 5 | 14.1429 |
| 8 | 1 | 32 | 6,7 | 5 | 14.1429 |
| 10 | 1/4 | 10 | 10 | 10 | 793.234 |
| 10 | 1/4 | 40 | 38 | 29 | 110.249 |
| 10 | 1/2 | 10 | 10 | 10 | 70.8473 |
| 10 | 1/2 | 40 | 18 | 15 | 51.5454 |
| 10 | 1 | 10 | 8,9 | 7 | 21.1852 |
| 10 | 1 | 40 | 8,9 | 7 | 21.1852 |
| 12 | 1/4 | 12 | 12 | 12 | 2093.88 |
| 12 | 1/4 | 48 | 46 | 37 | 149.158 |
| 12 | 1/2 | 12 | 12 | 12 | 114.874 |
| 12 | 1/2 | 48 | 22 | 18 | 69.8933 |
| 12 | 1 | 12 | 10,11 | 9 | 29.2138 |
| 12 | 1 | 48 | 10,11 | 9 | 29.2138 |

In particular, at eta=1/2 a source cap of 4m selects per-attempt N=7,10,14,18,22 for m=4,6,8,10,12. These all exceed m. The current evaluator cannot prepare them. Quoting an unconstrained Haar optimum as a hardware choice would therefore miss a material source constraint.

## Proof and prior-work boundary

The known Haar occupation law is authenticated in Bouland et al., [2312.00286v2, Sec. 4, Lemma 1 and Eq. (6)](https://arxiv.org/html/2312.00286v2). The notation dictionary is their photon count n -> N and their click count c -> k. Arkhipov–Kuperberg, [1106.0849v1, Proposition 1 and Corollary 2](https://arxiv.org/html/1106.0849v1), supplies the general fixed-input Haar twirl. Exact primary versions were read; no statement about saturated-regime computational hardness is imported into this encoding comparison.

The loss mixture follows by uniform-loss covariance and conditioning on Binomial(N,eta) survivors. An independent derivation explicitly thins every uniformly weighted Fock occupation and forms its click-count polynomial. That derivation yields the draft coefficient identity and verifies normalization. Equivalently, for a detected occupation s with L photons, summing all original occupations t>=s gives the factor binom(m+N-1,N-L), independent of the profile of s; division by D_N makes its probability Binomial(N,eta)[L]/D_L. This directly derives the uniform survivor mixture without requiring a separate loss-commutation theorem. The [contract](../research/phase3_threshold_contract.md) gives the formulas, domain, proofs, and the expected-photon optimality argument for adaptive choices of N after previous failures.

Fresh independent Haar draws are essential to the waiting-time interpretation N/p. Sampling U once and holding it fixed requires averaging N/p_U, not inverting the average probability. Expected success counts at a prescribed number of attempts do not require the same renewal assumption, but first-hit probabilities do. Classical reprogramming, preparation, training, and graph-repair costs are excluded from this photon-only theorem and must be counted in any eventual algorithm benchmark.

The averaged marginal used here can be sampled classically by drawing a uniform weak composition, independently thinning its photons, and thresholding. Arkhipov–Kuperberg Theorem 5/Corollary 6 already relates the same mixed-state law to a classical random-simplex multinomial model. This observation does not simulate the conditional output of an arbitrary specified U or an optimized circuit. The present operational results are corollaries of known counting, not evidence of quantum optimization or a new complexity result. No exhaustive novelty claim is made.

## Actual execution and reproducibility

Canonical recorder status: **completed**, exit 0. Exact audit runtime 5.008s; manifest start `2026-11-21T10:29:28.278029+00:00`.

- 195 exact occupation/loss cases and 965 click probabilities: all three independent rational routes agree exactly. This includes N>m in the theorem domain.
- Two draft floating formulas: maximum discrepancy from the rational reference `1.1102230246251565e-16`.
- Lossless maximizers: all 19 even sizes m=4,...,40 checked through the declared cap 4m, with exact ties retained.
- 50 exact operational grid rows, each with source cap, a minimal-encoding reference efficiency, and three finite photon budgets. The full grid is retained; maxima are not reported as outcomes of circuit optimization.
- 120 circuit/loss comparisons: independent explicit permanents and every detected suboccupation, bosonic and distinguishable photons. Maximum Fock discrepancy `3.3306690738754696e-16`; maximum threshold/loss discrepancy `9.4368957093138306e-16` (tolerance 1e-10).
- Existing isolated-worktree tests: **150 passed**. Principal draft threshold tests: **20 passed**, including its local Perceval distribution comparison. These are separate suites, not 170 new tests.
- No QPU, noise fitting, optimizer, or hardware resource call was performed. All numerical random circuits use the three predeclared seeds; exact identities have no sampling uncertainty.

Primary artifacts:

- [Durable audit script](../experiments/phase3_threshold_audit.py)
- [Machine-readable contract](../experiments/P32_threshold_audit/contract.json)
- [Canonical full raw data](../experiments/P32_threshold_audit/run/raw.json)
- [Mathbox v2 manifest](../experiments/P32_threshold_audit/run/manifest.json)
- [Unchanged audited source/theory/tests snapshots](../experiments/P32_threshold_audit/audited_draft/)
- [Initial external-source run](../experiments/P32_threshold_audit/initial_external_raw.json) and its [exact executed script](../experiments/P32_threshold_audit/initial_executed_script.py). The archival rerun changes only paths/receipt wording, not mathematics or seeds. Both successful executions are retained.

The canonical manifest pins the archived drafts and all package Python sources, with observed before/after hashes. Its validator returns `valid evidence record (run status: completed)`. Re-run calculations with a new output file; the script refuses overwrites:

```sh
PYTHONPATH=src ../../../.venv/bin/python -B experiments/phase3_threshold_audit.py \
  --draft-root experiments/P32_threshold_audit/audited_draft \
  --output /private/tmp/pasqal-threshold-reproduction-new.json
../../../.venv/bin/python -B /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  experiments/P32_threshold_audit/run/manifest.json --root .
```

Use the project’s pinned .venv interpreter if this branch is checked out elsewhere. Receipt timestamps, paths, and runtimes naturally differ on replay; the mathematical records should agree. The recorder wrapper requires the installed Mathbox skill at the versioned path, while the audit itself runs directly from the durable script.

Hashes:

- Canonical raw JSON: `2cdd17aaf3dcf0789064cdac097f9d58fb70b76794351ed9395bfa2ae48d872f`.
- Audit script: `8287c57502cac023ef7a1fa590fa97cf26df3f19f23ff12506e3d7e428f4b997`.
- Mathematical contract: `00ef816e77d1238590b8cddccde1eda3b0822620c2d6b4cbdd66879cf9dbddc9`.
- Audited threshold draft: `69891841598a25285a2fddb6586d6da4d3ad7035c2d10ee26cb25d646b842d47`.
- Complete remaining hashes, versions, command, and dirty state are in the receipts.

## Decision

**KEEP as an operational encoding/resource audit; NO-GO as a claimed new Haar result or demonstrated optimization benefit.** No formula correction to the audited threshold draft is required within the tested domain. Its lossless maximizer helper already says it is lossless. Callers must specify the actual source cap, decoder/gate, uniform-loss placement, and the resource objective; those choices cannot be silently interchanged.

A subsequent graph experiment needs optimum-blind encoding/training, locked families and seeds, retained unfavorable instances, genuinely comparable classical/distinguishable samplers, and both injected-photon and classical/preprocessing budgets. The audit neither prepares hardware nor changes the existing QPU/manuscript gates.

Self-review: mathematical notation, boundary cases eta=0/1,N=0,N>m, all-N gate, fixed-U versus renewed Haar, and the three budget criteria were checked. Primary-source extraction is limited to the specific counting/twirl leaves above; a novelty audit of an optimization mechanism remains outside this result.
