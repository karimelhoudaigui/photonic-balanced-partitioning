# P20 integration review

**Verdict: accept the preserved archives as evidence for the stated, bounded negative result.** The saved arithmetic, parameter choices and finite metrics are consistent with the current historical sources. They do not establish a quantum optimization advantage, total-resource superiority, general impossibility of photonic optimization, or measured adaptive search performance. The original report already makes most of these exclusions. Preserve its exploratory continuation and training-coverage failure.

This review used Mathbox computation-audit. Base: `e201f1c337cb780225bdcdd0a806cfd7d20d2fe2`; isolated branch `research/p20-integration-review`. The auditor did not author the P20 module, drivers, tests or original report, but authored earlier objective/penalty helpers and classical-control work in this project. This is an implementation-independent review of P20, not a project-blind external review or independent hardware replication. No campaign, source modification, manuscript change or QPU call was performed.

## Contract and tested scope

Read the two original v2 manifests, contracts, summaries, frozen parameters, training scores, graph instances, local blocks and CSV metrics under `experiments/P20_structured_probe/` and its `larger_training/` child; also the historical module, both drivers, tests and report. Their primary files were read by absolute path in the principal checkout, where they were still untracked. Both original v2 manifests validate against that checkout's current hashes with status `completed`. This confirms present source/output consistency, not external preregistration or historical attestation.

The authorized check rebuilt the fixed 4/6-mode kernel bank, checked all stored local cut labels with a separate upper-triangular edge-difference calculation, reaggregated all saved training scores, verified the saved selection/tie rule, and recomputed all expected CSV metrics. It also replayed the first and last stored test case of each run, for eight methods each: **32 finite-count spot checks**, not a repeat of either campaign. It did not call either campaign's `main`, `prepare_cases`, `train` or `evaluate`.

| Audited quantity | Initial | Larger-training continuation |
|---|---:|---:|
| Training instances | 72 | 480 |
| Test instances | 288 | 480 |
| Training blocks | 288 | 1,920 |
| Test blocks | 1,152 | 1,920 |
| Test metric rows, eight methods per block | 9,216 | 15,360 |
| Synthetic attempts, 64 per row | 589,824 | 983,040 |
| Training instance-kernel evaluations | 12,960 | 86,400 |
| Shared training local labels | 3,744 | 24,960 |
| Evaluation-only test local labels | 14,976 | 24,960 |
| Training anchor swap deltas scored | 15,944 | 213,700 |
| Test anchor swap deltas scored | 127,968 | 215,512 |

All six declared graph families and both anchor regimes are retained. The initial run uses training sizes 8/12/16 and seeds 0–3, test sizes 8/12/16/24 and seeds 100–111. The continuation uses both splits' sizes 8/12/16/24, training seeds 0–19 and fresh test seeds 200–219. Seed sets and graph identifiers are disjoint across train/test within each run. The continuation follows inspection of the first run and is correctly described as exploratory.

## What passes

1. **Train/test ordering.** In the initial driver, `frozen_parameters.json` is written and hashed before test construction (lines 220–223); the continuation follows the same order (lines 48–52). The hash is checked again afterward. Training selects only mean positive accepted gain divided by `max(total edge weight,1)`, over training blocks. No global optimum or `Cstar` label enters this procedure. The saved choices match the recorded scores and tie rule.
2. **Graph arithmetic.** Stored graphs are finite, nonnegative, symmetric, zero diagonal; relabelings are permutations. Local candidate partitions remain balanced. The independent cut reconstruction agrees to at most `4.974e-14`; anchor energies agree to at most `4.264e-14`. Saved single-swap minima have no improving single swap at the checked tolerance. Anchor work fields match `(steps+1)*(n/2)^2`.
3. **Physical attempt accounting.** Expected improvement and accepted gain use unconditioned outcome mass. Collisions consume attempts and contribute zero gain. Every row has 64 synthetic attempts and zero QPU shots; collision plus feasible counts equal 64. The saved budget-success formula is `1-(1-p_improve)^64` for repeated independent proposals at the same anchor. No collision-free renormalization is used to inflate that probability.
4. **Local probability construction.** The separate routing enumerator covers all `binom(3r-1,r)` Fock outcomes, with output occupation factorials, for distinct single-photon inputs: 10 states at r=2, 56 at r=3. Its bank comparison to the main simulator has maximum absolute error `6.661338147750939e-16`. This validates floating implementation consistency, not literal exact arithmetic.
5. **Stored results.** Recomputed training scores agree within `9.836e-18` initially and `6.377e-18` in the continuation. Expected CSV fields agree within `4.264e-14` and `5.685e-14`. All 32 count spot checks match. Every selected interaction angle is zero. Bosonic versus separately trained product-control expected metrics are identical case by case in both archives.
6. **Focused tests.** The existing 16 structured-search tests pass, including independent routing, complex random blocks, collision mass, analytic swap deltas, the Walsh interference diagnostic and Perceval comparison. The saved test stdout and receipt give the actual command and result. Test wall time was 17.70 s (pytest: 17.04 s), child CPU 16.06 s. Arithmetic review took 2.06 s wall and 1.72 s CPU. The combined CPU work remains below the authorized 60 s discriminating-check cap; neither campaign was rerun.

The continuation's exact expected per-attempt improvement means are:

| Active photons and anchor | Cases admitting improvement | Bosonic = product | Best local, with enumeration |
|---|---:|---:|---:|
| r=2, two swaps | 175/480 | 0.2000000000 | 0.3645833333 |
| r=2, single-swap minimum | 7/480 | 0.0145833333 | 0.0145833333 |
| r=3, two swaps | 199/480 | 0.1260338081 | 0.4145833333 |
| r=3, single-swap minimum | 38/480 | 0.0070312500 | 0.0791666667 |

The initial r=2 minimum training blocks had no improvements, so the tie rule selected identity and missed eight improving test blocks. The continuation selected a deterministic full batch swap there, still at zero interaction. This is a preserved coverage artifact. At a two-photon single-swap minimum, among the six feasible local states only full replacement can improve: the anchor and four single swaps cannot. That explains this narrow constructive classical control without claiming that all interference mechanisms fail.

## Interpretation constraints for integration

**A. This is a fixed-anchor proposal probe, not an executed adaptive optimizer.** Each case draws 64 proposals around one unchanged anchor. Accepted outcomes do not become the next state. Its `p_improve_by_budget` is the chance of finding an improvement in that batch, not an adaptive hitting-time or optimization-quality curve.

The report's separate bounded-block proposition is sound in the ideal arithmetic model: for known local U and fixed r, explicitly enumerate all local occupations and sample their exact categorical law. Equal conditional next-outcome kernels imply equal adaptive transcript laws by induction, including collision failures. The `O(D r r!)` bound counts arithmetic operations in the supplied local unitary; graph selection/scoring, access to U, numerical precision and random-bit costs remain additional. Complete outcomes must be retained if a policy reads collision patterns. The P20 proposal interface coarsens collisions to one failure category, although its full-Fock helper retains the detailed occupations. Thus the implemented batch check supports its coarse observation model; it is not an adaptive transcript experiment. This is the exact-kernel case epsilon=0, distinct from an approximate floating-TV certificate or a nonzero-error adaptive replacement theorem.

**B. The replacement CSV equality is constructed.** `evaluate` reuses `chosen_b['p']` for `classical_exact_replacement` and assigns it the same count RNG seed as bosons (initial driver lines 140, 148–149). Its identical counts therefore are not independent finite-shot evidence. The genuinely separate check is the routing-versus-Ryser/Perceval probability construction. Equal exact kernels are a mathematical construction; the observed `6.67e-16` tolerance alone does not prove exact equality or a universal transcript bound.

**C. Equal attempts do not equal total computational or photon resources.** Bosons and independently tuned distinguishable particles each search 20 grid circuits; the product model searches five. There are 180 aggregate grid-score computations (four regime/block-size cells times 45 candidates), each averaging many block instances; the recorded 12,960/86,400 counts instead count instance-kernel evaluations. Shared label counts and probability computations are separate resources. The common dense anchor scans and informed block selection must also be charged. For n=24, a single scan scores 144 swaps, already larger than six/twenty local candidates.

`classical_best_local` pays six/twenty upfront labels. Its recorded cached proposal count is one distinct selected state; once that label was computed upfront, an actual persistent cache needs zero *additional* objective queries for its repeated selected proposal. Similarly, uncached 64-per-row values describe an alternative hypothetical implementation. Do not add these fields blindly as actual total executed function calls. The record is useful logical accounting, not a CPU benchmark.

Physically retaining spectators would prepare n/2 photons per attempt; a local r-photon source with classical spectator bookkeeping is a different implementation. The archives supply no measured source, loss, latency or photon budget comparison between these choices. Their 64 synthetic draws cannot settle those resource questions.

**D. Bootstrap intervals are descriptive for this fixed grid.** Families and sizes are pooled, underlying seeds are reused across families/sizes, and path/cycle graphs repeat topology after relabeling. No independent-topology population sampling law is justified here. Do not interpret the generic paired bootstrap as a demonstrated nominal 95% interval for arbitrary future graphs. The boson/product `[0,0]` interval is explained by identical kernels, not statistical evidence of universal equivalence beyond the selected circuits.

**E. Preserve historical output before any future execution.** Both drivers use an existing fixed output directory and overwrite files; the report's original campaign commands are unsafe to replay in place. Archive the hashed versions as historical drivers. Any future execution should use a separate new-output wrapper/guard and a fresh directory, with its own receipt. Do not silently edit the historical drivers or manifests to retroactively describe a different run. No rerun is needed for this integration verdict.

**F. Provenance is internally consistent but has limits.** The historical run base was dirty with these P20 sources untracked. Manifests and source order support reproducibility but do not establish an external precommitment. The initial manifest was assembled after execution; the original campaigns do not retain runner-enforced cap receipts or complete stdout/stderr. CSV retains count summaries, not every raw categorical count vector or adaptive trajectory. This review retains the missing-observation limits and does not retroactively manufacture those records.

## Review evidence and hashes

The durable bounded checker is `experiments/P20_integration_review/check_archived_outputs.py`; its result is `arithmetic_receipt.json`. The latter records all 23 primary source/data SHA256 values observed before and after the check: unchanged. The review test wrapper, `pytest_stdout.txt`, `pytest_stderr.txt` and `pytest_receipt.json` preserve its focused test command and result. No original data file was written. The independent arithmetic reconstruction still uses the original kernel-bank constructor, swap-delta routine for the minimum check and NumPy/SciPy/Perceval stack; it is not a wholly independent implementation of the entire experiment.

| Primary artifact | SHA256 |
|---|---|
| Initial manifest | `a7422650d65dba399ed54879b305bb951720c660d02228fbb076e728776fca8a` |
| Continuation manifest | `6330df5b3425551cf5c2916d6a2cb25f02763da0a9b2a6d8305ad49bda488718` |
| Main P20 driver | `4324a2915f4d1079fb720e6d99c69a603d00d40dd85f3aa32ec44973bd080188` |
| Structured-search module | `7be43d9547a6a3e67fda6d3fd54d0de484d8840afa8d3497ee00a74af950827c` |
| Continuation driver | `8016bc4cc166b83a634f71e9ead92896c4bebb8506e328e891b155480820c49b` |
| Initial frozen parameters | `5a6cfb5690612ab3a82d385adb1d1b8f52c6bf18e2e4a849a51c993b614b6336` |
| Continuation frozen parameters | `ecc43276f87d7af4a3fb995b6acb2a5cb08ed4e0e487ea490810675be166e347` |

Safe review-only reproduction, from this worktree with the primary archive at the pinned absolute path, uses a **fresh** receipt filename; the checker refuses overwrite:

```sh
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -B experiments/P20_integration_review/check_archived_outputs.py --output experiments/P20_integration_review/recheck.json
```

This command is documented for reproduction, not executed again for this review. Python 3.11.15 and NumPy 2.4.6 were observed. The checker sets CPU limit 55 s; the focused-test wrapper sets child CPU limit 30 s. The arithmetic receipt records wall time, CPU time and platform. Full initial invocation argv and exact start timestamp were not retained by that outside-runner checker; this limitation is explicit in the manual review manifest. Its before/after input observations are authentic. The manual v2 wrapper resolves original inputs against the principal checkout and review outputs through the isolated worktree prefix; this location-specific wrapper must not be mistaken for a portable campaign manifest after cherry-pick. The underlying receipt's explicit hashes remain usable independently.

No additional sweep is justified by this review. Integrate the two preserved negative archives with the above scope: the finite grid selected classical product kernels, and fixed-size known local kernels admit an explicit classical replacement. Any future growing-component mechanism needs a new protocol and stronger resource comparison.
