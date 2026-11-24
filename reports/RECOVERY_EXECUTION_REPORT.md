# Recovery execution report — 24 November 2026

**Delivered: a rebuilt16-page article, corrected tested software, immutable reconciled evidence, three source-review perspectives and a working offline QPU handoff.** The original optimization-benefit goal remains open. The local preparation is operational; no hardware result or certified submission readiness is claimed.

Branch: `scientific-recovery-publication`. Starting commit: `6154b460e1c8b37cf2a7023fcbfff35d31a7220c`. Manuscript/build commit: `18ceacc`.

## Principal deliverables

| Deliverable | Location |
| --- | --- |
| Article PDF and complete LaTeX | [paper/main.pdf](../paper/main.pdf), [paper/main.tex](../paper/main.tex) |
| Claim-by-claim integrity audit | [SCIENTIFIC_INTEGRITY_AUDIT.md](SCIENTIFIC_INTEGRITY_AUDIT.md) |
| Single publication thesis | [PUBLICATION_THESIS.md](PUBLICATION_THESIS.md) |
| Actual submission limitations | [PUBLICATION_READINESS.md](PUBLICATION_READINESS.md) |
| Full numerical census and reconciliation | [NUMERICAL_RECONCILIATION.md](NUMERICAL_RECONCILIATION.md), results/validated/recovery_2026-11-24/ |
| Source-review reports, findings and responses | [final referee synthesis](manuscript_review_2026-11-24/v3/report.md) and v1/v2/v3 JSON artifacts |
| Model, experiment and reproduction documentation | docs/SCIENTIFIC_OVERVIEW.md, MATHEMATICAL_MODEL.md, EXPERIMENTAL_PROTOCOL.md, REPRODUCIBILITY.md |
| Standalone Laurent dossier | [docs/LAURENT_HANDOFF.md](../docs/LAURENT_HANDOFF.md), qpu/README.md and QPU_COMPATIBILITY.md |
| Honest hardware gates | [QPU_READINESS.md](QPU_READINESS.md) |
| Physical sharpness calibration and portable replay | docs/DENSITY_PILOT.md, [P40_REPRODUCTION.md](../docs/P40_REPRODUCTION.md), results/validated/P40_* |

## Scientific outcome and corrected errors

The main article is a certificate-and-resource analysis. P33 relates a positive floor on every nonzero output intensity and expected colliding pairs to absolute-TV proximity of the complete bosonic law to independent particles. The full proof, balanced sharpness family and balanced low-collision counterexample are included. Established permanent/cycle/rounding ingredients are attributed; full-composition originality remains open.

P37 proves that Haar-averaged source optima depend on the resource: two candidates per attempt, four per injected photon, with unique ordered transitions and a specifically fixed-lambda boundary scaling. Its known Haar input and absence of graph enrichment are explicit.

The empirical result is negative: the full756-run E05b reconstruction has bosonic/distinguishable mean final probabilities .652313/.713285 at n4, .279549/.536614 at n6 and .067873/.137707 at n8. All runs already find an optimum during training. These findings do not demonstrate the originally sought benefit; they do not refute every photonic algorithm.

Corrections include K4 optimum4/six optimal strings/Haar success.6; K2,2 optimum2/four optimal strings; identity conditional probability0or1; the actual spatial amplitude-magnitude Gram; pair moment versus collision probability; the k2 identity M=1-P_CF; oracle-assisted preparation versus blind search; exact selected probabilities versus heldout rates; graph duplicates/bootstrap units; physical versus classical-control denominators; the uniform-loss arithmetic.3523257; and physical internal-Gram noise instead of a generic global mixture.

Unsupported n10/12 optimization,4.8× bosonic advantage,227× speedup, unverified noise tables and HPC/device projections were withdrawn. Their prior versions remain in Git. Full authentic ObliQ training/source/prefix decoding remains incomplete; its validated static component is identified correctly.

## Actual computations and tests

- Initial suite:356 PASS, preserved output.
- Graph/anti-oracle focused check:60 PASS.
- Integrated code stage:455 PASS; publication-inclusive stage482 PASS.
- **Final new-venv release suite:484 PASS in47.69s**. Six warnings concern Perceval's local persistent-cache fallback; no test failed. All tested Python source hashes were unchanged before/after. Exact command, environment, stdout/stderr and source hashes are in recovery_2026-11-24/release_clean_pytest_receipt.json.
- Clean installation: a newly created isolated Python3.11.15 venv installed the locked project from public PyPI. All37 locked versions match and pip check passes. This is an actual install, not an assumed reproducibility claim.
- E05b reanalysis:756 distinct run keys,90,720 objective batches and26,320,896 ideal simulated draws reconstructed. Training losses, selected parameters, count budgets and heldout intervals checked. No historical optimizer trajectory was rerun.
- E01 reaggregation:3250 recorded Haar circuits;1000 each n4/6/8 and250 n10. No empirical n12 point invented.
- Historical census:50 records at the starting archive;43 completed-output captures verified,2 source-snapshot gaps,3 preserved failures,2 root P33 copies excluded. This is not50 independent successful scientific replications.
- New physical noise software:37 dedicated tests include complex three-photon internal phases, independent internal-mode construction, full loss sectors and Perceval controls.
- P40 advance contract was committed before its single primary45-cell calculation; all45 and five SLOS circuits pass. Maximum TV prediction residual9.72e-17. All laws include zero/one/two-photon sectors and zero-valued cases.
- P40 portable replays are separately labeled reproduction. The worker and supervisor outputs match the archived laws with zero difference. The supervisor actually ran on the integration branch in the new venv:45 cells/five SLOS circuits, CPU1.122414s, wall2.691921291s. Original driver/contract/raw files are unchanged.
- Seven-command offline pipeline was actually reproduced by the supervisor into a new destination, including synthetic known/unknown-attempt count analyses. No synthetic count is labeled hardware data.
- Publication corruption tests and `build_publication.py --check` pass; all four tables/three figure PDFs derive from sealed evidence or explicit analytic definitions.
- CI YAML syntax checked locally. Remote CI was not triggered and Linux execution is not claimed.

## Manuscript and review evidence

Final source snapshot SHA256:
`98bf647e4f180cd2a1628106f5c621fa5d02ceebf33036317fb8e5cec4e27b7e`.

Final PDF SHA256:
`271946c9043d26c0e00a964591e9a47541d5816c399e7a52a62032630650243f`.

Tectonic0.16.9 compiled the full article. The PDF checker observes16 pages,14 cited keys, no undefined references, no significant overfull box, no blank page and no stale input. The final log and source/PDF hash receipt are retained. Build setup/layout failures are preserved separately; their fixes do not rewrite scientific results. All three plots and selected manuscript pages were rendered and visually inspected.

Three real native-agent readers covered mathematics/adversarial checks, optimization/statistics/reproducibility, and photonic physics/noise. Six raw v1/v2 passes contain11 findings, representing7 distinct local issues. All were repaired; targeted v3 confirmations and final coordinator synthesis record the dispositions. The fresh mathematical reader reconstructed both proofs without reading prior verdicts during that pass, while disclosing earlier project context.

These are not three uninvolved human referees. The numerical reader produced the dataset/table captions, the physics reader authored noise/P40 and had earlier proof-review involvement, and the mathematical reader authored the hardware CLI. Reused scopes, self-review, context checks and unknown native model settings are explicit. No reviewer agreement or test count certifies originality.

## Preservation, isolation and organization

The initial803-file inventory and supplied audit draft were saved before edits. **602 pre-existing experiment/result/theory/research files still match their original hashes**, with no missing file. Negative results and provenance gaps remain visible.

Three worker branches/worktrees were used, with disjoint editing scopes. Their original commits are additionally preserved in the verified416672-byte isolated-worker-history.bundle, with the6154b46 base prerequisite. This preserves original source/contract identifiers across cherry-picks. The final delivery manifest records integration commits.

Three identical .bak/.backup/.new files were consolidated into one byte-identical archived text plus a path/hash map. Generated setuptools egg-info was removed from Git tracking while retained locally. make clean now removes only explicit LaTeX auxiliaries and never results. The pre-existing .DS_Store working-tree change was left untouched.

Major touched areas are active paper sources/figures/tables; graph and optimum-blind API validation; new noise/hardware/replay modules and tests; source-linked publication/verification scripts and CI; current scientific registers/readiness/handoff documentation. Historical scientific inputs were preserved.

## QPU and publication gates

OFFLINE_PILOT_READY=TRUE. HARDWARE_COMPATIBILITY_VERIFIED=FALSE. QPU_GATE=CLOSED.
PAPER_READY_FOR_SUBMISSION=FALSE. Complete-composition novelty/significance remain open.

The local n4k2 pilot exports trusted circuit/unitary/reference bundles and analyzes explicit PNR count schemas. Native backend compilation, actual source/detector/routing, account availability, calibration, attempt counters and authorized credit cap remain unverified. P40 is a supplemental local study; the seven-command pilot still supports its three specified fixed circuits.

No real QPU, hardware credit, separate paid inference provider, article submission or message to Laurent was used. A QPU section is included; an executed QPU experiment is not fabricated.

## Concrete next work

1. Independently assess exact prior-art overlap and significance of the complete certificate composition; confirm author metadata and target scope before external circulation.
2. Develop finite-data/error certification for the density floor and moment, or register a changed optimum-blind mechanism with total-cost/held-out graph controls. Existing negative results remain the starting evidence.
3. Use the Laurent dossier to obtain actual capability/calibration/denominator information. Prepare a concrete provider-adapter/precision/credit proposal for explicit authorization before any device execution.
