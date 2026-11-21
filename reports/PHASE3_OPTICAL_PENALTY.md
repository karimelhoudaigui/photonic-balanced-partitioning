# Phase 3 optical-penalty component audit

**Verdict: PASS for the declared finite ideal static-component checks.** The literal archive builder, independently assembled Rx matrices and complete Fock probabilities agree in the tested domain. The archive's angle mapping does not realize the paper's initial two-photon coincidence identity: at normalized coupling one, it gives coincidence probability one half rather than zero. The separately labeled corrected variant realizes the intended local identity. This discrepancy was already identified in the authenticated specification and is **not a novelty claim**.

No QPU, noise experiment, manuscript edit, complete ObliQ optimizer reproduction, or optimization advantage claim is part of this audit.

## Scope and review independence

Reviewed on 2026-11-21 in the isolated worktree `.qwen/worktrees/phase3-physics`, base commit `8edfca70f03555479ea62ef9c49d727a27cc1861`.

Exact reviewed inputs:

| Artifact | SHA256 |
|---|---|
| `src/photonic_balanced_partitioning/photonic/optical_penalty.py` | `62fc56996132754187d581f6dd3003a7e8f74c951ac241c55b5cd801ecb4919f` |
| `tests/test_optical_penalty.py` | `15c790051304139d0654fd02d9f290af2be358093f776f6b98bf8c0c7be065c6` |
| Authenticated `ObliQ.zip` | `8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948` |
| Original archive `ObliQ/circ_init.py` | `8526955119d0fc74506aa4952289bf0a65bf1ebe820331d024c53fb5583fe8ad` |

The audit inspected the implementation and coordinator-authored tests read-only and wrote only this report in the worktree. The physics auditor authored the component earlier; this is therefore **not a fresh blind review of the author's own source**. Independence comes from the mathematical reconstruction, the original archive builder, Perceval SLOS, a separate explicit-permutation computation, and tests written by the coordinator. Agreement of these methods is finite numerical validation, not a formal proof certificate.

## Component contract and conventions

`OpticalPenaltyAnchor` is only the static coupling kernel. It does not implement variational training, graph-aware marginal-prefix decoding, hybrid input discovery, or the complete original algorithm. Its default source is one photon in every mode, `N=m`, followed by threshold detection `x_i=1[t_i>0]`. Collisions remain in the complete occupation distribution and contribute to their threshold patterns. They are not discarded or renormalized into a fictitious collision-free sampler. Nonvacuum lossless inputs cannot yield the all-zero threshold string.

The API parameter is the Perceval Rx angle `beta`, with zero auxiliary phases:

\[
G(\beta)=\begin{pmatrix}
\cos(\beta/2)&i\sin(\beta/2)\\
i\sin(\beta/2)&\cos(\beta/2)
\end{pmatrix}.
\]

Rows label output modes and columns label input modes. Chronological gates multiply the current unitary on the left. The static construction repeats the same complete unordered-pair sequence `R` times. Nonadjacent pairs are routed by a swap permutation, an adjacent Rx gate, and the inverse permutation. Since that permutation is a transposition, the two routing permutations are the same; direct embedding and archive routing are equivalent.

The two variants are intentionally separate:

\[
\beta_{\rm archive}(a,R)=\tfrac12\arccos\sqrt{1-a/R^2},
\qquad \beta_{\rm corrected}(a,R)=2\beta_{\rm archive}(a,R).
\]

Global entrywise min–max normalization of the supplied QUBO reproduces the archive's coupling construction. `offdiag_extension` normalizes only off-diagonal entries and is an explicit algorithm extension. Neither normalization replaces the original objective, which remains `x.T Q x`.

The default reproducibility order is lexicographic. It is **not** presented as the archive's runtime `list(set(...))` order. For four modes:

- Default lexicographic order: `[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]`; compact-JSON SHA256 `26ed3c7fdf671e0b91dd5901e24b78d798c55cfb6adca1493df4ae8128ca754b`.
- Archive runtime order used in the direct reproduction: `[(0,1),(1,2),(0,3),(2,3),(0,2),(1,3)]`; compact-JSON SHA256 `d074cf436377785448f29625daf0b2c5a8f23108a8ce708e7e91250f62fd44b8`.

Callers claiming literal runtime reproduction must pass the serialized archive order explicitly. Convergence comparisons must keep order, variant, repetitions and source fixed.

## Independent reconstruction of the physics and energy conventions

For input `|1,1>`, the coincidence amplitude is the 2-by-2 permanent of `G(beta)`, namely `cos(beta)`. Thus `P_11=cos^2(beta)`. At `R=1` this gives

\[
P_{11}^{\rm archive}=\tfrac12(1+\sqrt{1-a}),
\qquad P_{11}^{\rm corrected}=1-a.
\]

Each bunched outcome has probability `(1-P_11)/2`. The latter identity is a **single initial pair** statement. It is not asserted to hold for each correlation after other gates, nor for the net effect of repeating a pair `R` times.

The complete-state recurrence is also correctly normalized. When inserting the `j`th photon in source mode `a`, creation into output mode `i` multiplies an existing amplitude by `U[i,a]*sqrt((t_i+1)/j)`. The output occupation factor comes from a normalized Fock creation operator. Repeated division by `sqrt(j)` supplies the input `sqrt(s_a!)` denominator. By expansion, the resulting amplitudes equal `Per(U[t,s])/sqrt(prod(s_a!) prod(t_i!))`. The implementation checks the raw full norm and never rescales amplitudes to conceal an error. Vacuum and collisional source inputs have the proper meanings.

For a nonnegative simple weighted adjacency and target weight `k`, expansion gives

\[
C_G(x)+\lambda(|x|-k)^2=x^TQx+\lambda k^2,
\quad Q_{ii}=d_i+\lambda(1-2k),\quad Q_{ij}=\lambda-w_{ij}.
\]

The off-diagonal factor two is correctly supplied by `x.T Q x`. The tests exhaust the entire 16-string cube of a weighted four-vertex graph. They do not restrict the check to already balanced strings. `expected_original_qubo` retains the original Q; the constant `lambda*k^2` must be restored externally when reporting total cut-plus-penalty energy. Irregular-degree graphs are executable by this component but remain an extension relative to the paper's constant-diagonal anchor class.

## Evidence inspected and numerical outcomes

The coordinator executed the new test file with **18 passing parameterized cases**. The read-only review checked that these tests cover the two variants and five couplings, Rx matrix convention, `R=1,2,10` complete circuit comparisons against Perceval, nonadjacent routing, the all-ones source, a bunched source, vacuum, complete threshold normalization and full-cube QUBO identity. They explicitly retain the endpoint mismatch rather than silently fixing the archive.

The bounded audited component run is stored in [P30 raw data](../experiments/P30_optical_component/raw.json) and [v2 manifest](../experiments/P30_optical_component/manifest.json). Its raw output SHA256 is `28b2b1655f52352256f288d9d376daeae46b3fc04531d48c751f967485a65172`. The runner records Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1, Perceval 1.3.0 and exqalibur 1.4.2 on arm64 macOS.

The executed run contains:

- Ten two-mode coincidence cases. Maximum analytic discrepancy `2.220446049250313e-16`; maximum discrepancy against Perceval `1.1102230246251565e-16`.
- Nine original-builder comparisons, three fixed seeds `1901,1902,1903` times `R=1,2,10`. All 35 output occupations of the four-photon/four-mode source are compared in every case, 315 occupation comparisons total. Maximum unitary entry discrepancy is exactly zero in the recorded run; maximum full-Fock probability discrepancy is `2.220446049250313e-16`.
- Forty-eight convergence cases: two variants, three repetition counts and eight penalties on the fixed weighted-regular four-cycle described below.

The original builder comparison checks the complete archive SHA256 before extracting **only** `PhotoCircuit.build_circuit` through the AST. It executes that isolated function with local NumPy/Perceval circuit constructors. It does not import the original program, call a forward method, initialize a remote processor, or access its external storage/optimizer machinery.

The archive pins Perceval 0.11.0, while this execution uses installed Perceval 1.3.0. The old version's independently authenticated BS source has SHA256 `d7d4a187fea8daf4a53008dd0e87b8f33264d3cb8dc41d24790044ef2d8bf554`; its Rx half-angle formula matches the installed matrix. This is an authenticated builder reproduction under the checked modern gate convention, **not an execution of the entire old dependency environment**.

The measured coincidence table is:

| a | Literal archive P_11 | Corrected P_11 | Paper's intended initial 1-a |
|---:|---:|---:|---:|
| 0 | 1.0000000000 | 1.0000000000 | 1.00 |
| 0.25 | 0.9330127019 | 0.7500000000 | 0.75 |
| 0.50 | 0.8535533906 | 0.5000000000 | 0.50 |
| 0.75 | 0.7500000000 | 0.2500000000 | 0.25 |
| 1 | 0.5000000000 | approximately 0 | 0.00 |

## Additional independent falsification checks

To challenge the new recurrence beyond the existing test fixtures, the reviewer used fresh seeded QUBOs, reversed pair order, and explicit permutation permanents with repeated rows and columns. This calculation did not call the component's recurrence to construct its reference probabilities, nor Perceval or the pre-existing simulator. It used `R=2`, literal-archive angles and seed formula `683100+m+sum(source)`.

| Modes | Source | Fock outcomes | Maximum reference discrepancy | Raw probability sum |
|---:|---|---:|---:|---:|
| 3 | `(1,1,1)` | 10 | `4.163336342344337e-17` | `1.0` |
| 3 | `(2,0,2)` | 15 | `6.661338147750939e-16` | `1.0000000000000002` |
| 4 | `(2,1,1,1)` | 56 | `5.551115123125783e-16` | `1.0000000000000004` |

All 81 outcomes passed the predeclared `1e-11` absolute discrepancy and norm tolerances. The odd mode count and `N>m` bunched sources specifically challenge hidden one-photon-per-mode assumptions. They are validation cases, not proposed hardware input resources.

Preserved receipt: `/private/tmp/phase3_optical_penalty_independent_receipt.json`, SHA256 `c8bb7068550d6f1c3806093c6de99ed74aae0f7a2317691f717cad9200c6c14b`.

Preserved reproduction script: `/private/tmp/phase3_optical_penalty_independent_check.py`, SHA256 `c6e6cbc18e588a46b29379749c063c56c882ed0d727c367908c63d3a2cd1ff72`. It records the reviewed module hash and checks it again after computation. These temporary files are supporting review receipts; the component, tests, P30 data and this report are the durable deliverables.

## Bounded washout probe: interpretation only

The P30 sweep fixes source `(1,1,1,1)`, lexicographic pair order and the connected weighted-regular cycle with edge weights `w_01=1,w_12=2,w_23=1,w_30=2`, so every weighted degree is three. Penalties are `4,16,64,256,1024,4096,16384,65536`. It compares each circuit with the same-variant/repetition/order unitary whose off-diagonal normalized couplings all equal one. No graph-aware classical prefix decoder is applied.

Selected endpoints for the literal archive are:

| R | ||U_lambda-U_limit|| at lambda=4 | At lambda=65536 | Full-Fock TV at lambda=65536 |
|---:|---:|---:|---:|
| 1 | 0.1778781229 | 0.0012365701 | 0.0009751155 |
| 2 | 0.0341909745 | 0.0000016572 | 0.0000019096 |
| 10 | 0.0299838363 | 0.0000014379 | 0.0000016502 |

The off-diagonal-only extension produces exactly unchanged unitaries across this particular penalty grid in both variants and all three repetition counts; its recorded maximum change is zero. This is consistent with the algebraic cancellation of the common penalty shift in that control. It does not prove superior sampling quality, an optimal penalty choice, a graph-independent convergence theorem, or a general lower bound on optimization resources. Those questions belong to the separately reviewed theory and subsequent task experiments.

## Nonblocking limitations and provenance notes

1. **Timestamp:** the embedded `ended_utc` is evaluated before the archive-builder comparison is called. It is not the completion time of all comparisons. The runner's start/runtime/exit record is the authoritative execution envelope. This is a provenance issue, not a physics discrepancy; no source was edited during this review.
2. **Acceptance:** `component_validation` returns errors but does not turn every tolerance violation into a nonzero exit. A runner status of `completed` alone is not a physics PASS. The verdict above follows from inspecting actual numerical discrepancies, analytic formulas and the tests.
3. **Pair order:** the default lexicographic order and the serialized archive runtime order are different. Results must retain that distinction.
4. **Dependency version:** the full original Perceval 0.11 environment was not executed. The relevant legacy gate formula was independently inspected and checked against current Perceval.
5. **Scope:** finite floating-point validation is not a universal correctness proof, and a static kernel does not satisfy the full authentic optical-baseline gate. Classical decoding and training remain separate work and cost obligations.

No blocking scientific or implementation error was found in the audited static component under its stated scope. A later full-baseline comparison must keep the literal, corrected and off-diagonal-extension labels separate, preserve photon/source resources and charge all classical postprocessing. Nothing in this report authorizes QPU preparation.

## Reproduction commands

From the isolated worktree, using the shared pinned project environment:

```sh
MPLCONFIGDIR=/private/tmp/pasqal-matplotlib PYTHONPATH=src \
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python \
-m photonic_balanced_partitioning.photonic.optical_penalty \
--validate-archive .local/references/pasqal_obliq_primary.zip \
--output /private/tmp/phase3_optical_penalty_reproduction.json

MPLCONFIGDIR=/private/tmp/pasqal-matplotlib PYTHONPATH=src \
/Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python \
/private/tmp/phase3_optical_penalty_independent_check.py
```

The first command is the recorded component command with a new output path so the existing P30 raw record is preserved. The coordinator separately ran `python -m pytest tests/test_optical_penalty.py -q` and recorded 18 passes. Final source/data commit creation and integration remain with the coordinator; the exact audited dirty-tree source/test hashes above bind this report to its inputs without guessing a future commit identifier.
