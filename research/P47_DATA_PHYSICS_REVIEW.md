# P47 completed DEV data: bounded independent physics/interpretation read

2026-11-25. This receipt extends the static source review
`research/P47_PHYSICS_CODE_REVIEW.md` (commit
`20384eee7d848366c37a08c47af087db15ee2dd4`). It is a READ-ONLY review of
archived diagnostics, manifests, existing summary records and improving
raw proposals. No new sampling, cut recomputation, matrix computation,
statistical test or full raw-audit execution was performed here.

Verdict: **finite DEV signal only; no accepted optimization advantage**.
The numerical directed-proxy checks and recorded preflight pass support
the intended implemented mechanism in this run. B exceeds D on the
observed gain metric, but its selected effect is sparse and concentrated;
the anneal baseline alone matches or beats B's end-best in every observed
graph/trial. This is an observed finite comparison, not a probability-law
dominance theorem, known optimum statement or a universal impossibility.

The coordinator disclosed the B/control aggregate before this raw read.
The reviewer also authored the P47 guide mathematics, and therefore does
not count as a fresh independent validator of that theory. Independence
here is implementation/data interpretation relative to the encoder author,
within the same team's/model's limitations. No author's result prose was
used to reach the comparison below. The separately produced author
stdlib raw-audit source/receipt was read only AFTER the improving proposals
and diagnostic contexts were inspected; its exhaustive checks are attributed,
not rebranded as work rerun by this reviewer.

## 1. Exact archive and chronology

Primary script SHA256 remains
`fac164f64a3ba15a061c56547be58f5c540486852c9016ccc70a129637ca53b1`,
the reviewed freeze `695b5d2f49c5bb90d070a38c31abc0a697fbedd4`.
The preflight manifest reports that commit, 13 tests passed, 17.434909s
runner wall time. The main manifest reports clean commit
`7a4cd49fa6b46f989b64a3309ecf833a6af2eafe`, whose change seals those
preflight artifacts only. It starts at 2026-11-25T04:20:48.417579Z,
exits0, and reports 23.057314s runner wall time. Script/spec/helper hashes
before/after match the frozen closure. The scientific program reports
8.458426s process CPU and 22.1738045s wall time inside main, including
asymmetric first cold-import cost. No hardware latency is inferred.

The six primary result hashes were independently checked by shasum:

| Path relative to experiments/P47_directed_pit/run_001/data | SHA256 |
|---|---|
| raw.jsonl.gz | aa1386b93104ba1941ebc9d0cdde8488278f86a9bfeb7cd6f0632a83b359d562 |
| summary.json | e2187b5c2a2c3abd79bc8d02076e0fe0e0b1a0a071c8520589e0705df66dad2e |
| context_n26_ER_4702601.json | 3aba076a05be1553ffdf2be02666affd6f035477d01b523425f17789d3f88318 |
| context_n26_RR_4702602.json | d0b09872f11865c9803fee342d259cc97896177dcb50ff592049794ea66cdf53 |
| context_n34_ER_4703401.json | 7af0a793f084e2ec0fb4bd5a9a86bb349ef5ab70dc851a876ae098654c503b3d |
| context_n34_RR_4703402.json | 97f6de5ec542386b8e6cf43ae50030598bab9c473503baedd730215a3765623b |

The main manifest hash is
`991b561e6186fbd27ace880e4ee503b0aa75766d362ce5fc1f04f4127853be8a`;
preflight manifest hash
`ba411e8d8e7989a2e11eb49a56816c676e9781475483a073872b15baafc4d06a`.
The author's raw-audit receipt hash is
`3996222045c08d53c74e38a43e6dec3408fe122601037df5dedab1f329803218`.
The initial read used the encoding worktree; it subsequently switched
branch/sparse coverage for P48 and its P47 data paths disappeared. Later
reads/hashes used the ROOT archive, verified against the same six immutable
result hashes above. Failed read-only file lookups were not experiment
failures, retries or modifications of scientific data.

## 2. Physical implementation diagnostics and retained outcomes

All four nonzero centered signals have a guided polar factor distinct
from Fourier and a substantial negative numerical proxy residual. The
guided values (identical W at p=.25/.5) read from contexts are:

| Case | ||W-F||F squared | normalized proxy change | input sigma_min |
|---|---:|---:|---:|
| n26 ER | .0367728043 | -.1322642481 | .9333826121 |
| n26 RR | .0092330659 | -.0630905923 | .9659114776 |
| n34 ER | .0540833877 | -.1627497423 | .9243970465 |
| n34 RR | .0086643287 | -.0606301542 | .9678619070 |

Recorded unitary residuals are below 8e-16. These are archived float checks,
not interval certification or independent numerical reconstruction here.
The finite theorem and primality do not turn this response into cut descent.

All six arms report 256 decoded proposals; each physical arm reports 3840
simulated injected photons, while 65536 extra phase-calibration draws are
classical common work. The author's full raw audit reports 189/256 B
collision samples, 142 D, 144 species and 180 conditional phase. Those
counts were not independently recounted here. Improving B raw proposals
include an event with a mode occupied by5 photons and another occupied
by2, plus a separate blind-network gain with an occupation2. They survived
the pipeline; there is no apparent hidden CF rejection in those records.

The completion can output UNCLICKED vertices. For example the selected
setting6 event on ER26/trial0 outputs vertices11,21,25 despite zero raw
counts there. It is an optical-count-informed classical completion, not
a direct CF support success event. Click-contained-decoder bounds do not
automatically cover this pipeline.

## 3. Selected versus all-settings effects

Direct summary/raw reads give:

| Arm | All-settings gain | Selected-setting gain | Selected index |
|---|---:|---:|---:|
| B | 22 | 10 | 6 |
| D | 0 | 0 | none |
| species4 | 9 | 4 | 2 |
| Gaussian B covariance | 2 | 2 | 3 |
| IID uniform | 14 | 6 | 2 |
| conditional phase | 9 | 6 | 2 |

This is not a held-out table. All eight settings and their entire tuning
effort must remain charged. Comparing B all-settings gain22 to a control's
selected gain would mix metrics. B has just five improving proposals:
four on ER26 and one on RR26; no B improvement appears on either N34 graph.
The selected setting6 is p=.5,guided1,lambda0. Its gains6 and4 both occur
on ER26. B's BEST absolute cut146 instead comes from the BLIND setting4
on ER26/trial1 (gain8). lambda0 still uses the PIT field to choose initial
top-q seeds; it is not an optical-free completion.

Small outcome counts, one labeling/order per graph, the pooled DEV selection
and approximate phase-control CDFs prevent a statistical positive conclusion.
Different raw sample/seed realizations could change the rank ordering.
The phase marginal calibration error does not certify joint-copula accuracy;
this limits interpretation of tiny B/phase differences, without proving a
specific direction of bias or invalidating all archived comparisons.

## 4. A single classical baseline suffices for the observed search comparison

The following is read from the B improving raw records and baseline summary
records. B end-best includes ALL eight charged settings in each graph/trial.
Anneal's listed best is also reached under the stored JOINT B online-time
and score caps, so this comparison does not require a free portfolio.

| Case/trial | Cref | B end-best | Anneal end-best within B joint caps |
|---|---:|---:|---:|
| n26 ER /0 |154|148|146|
| n26 ER /1 |154|146|146|
| n26 RR /0 |37|37|37|
| n26 RR /1 |37|35|35|
| n34 ER /0 |359|359|359|
| n34 ER /1 |359|359|359|
| n34 RR /0 |66|66|49|
| n34 RR /1 |66|66|49|

Thus anneal weakly beats B's observed end-best at every one of these eight
paths. This does not refute the empirical B/D kernel discriminator, nor
prove stochastic dominance or global classical simulability. It does show
that the present completed search run has not surpassed even that one
declared feasible classical baseline at the recorded budgets. Whether some
cases are saturated near their true optima is a DIFFERENT post-hoc headroom
question; no optimum was known or used in the training/selection run.

## 5. Limits of this read and checks actually executed

The separate author audit reconstructs 147811 feasible cut records,
1536 completions, 1024 saved count-PIT fields, 256 Gaussian fields,
incumbents and timing frontiers using a standalone stdlib implementation.
Its source was read and uses direct integer adjacency sums instead of
the production cut helper, plus a separate greedy reconstruction. These
are useful consistency checks, not a resampling/distribution replication.
This review did NOT rerun those 147811 computations or certify sampled
laws at K13/17; it only checked the code's declared logic, inspected its
receipt and manually compared the small extracted improving/summary rows.

Actual commands: read-only cat/git-show, jq FIELD SELECTION from existing
JSON, gzip decompression piped to jq to read improving proposals, and
shasum checks. No new scientific numerical program or statistical test was
run. The archived 13-test result satisfies the targeted preflight condition
in the prior static review; no full-suite result is newly claimed here.
Raw/archive files were not written. No QPU, credentials, held-out graph,
P48 data or optimum information was accessed. This receipt alone is a new
file in the isolated replication worktree.
