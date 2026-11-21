# P3 washout: proof, source, and computation audit

Date: 2026-11-21. Author and reviewer: the same theory agent; **self-review**.
Exact target: `theory/phase3_penalty_washout.md`, P3.1 and equations (3)–(10),
on branch `phase3-theory`, based on `8edfca70f03555479ea62ef9c49d727a27cc1861`.
The containing Git commit pins the reviewed text and experiment together.

Primary verdict: **proved as written**, by the internal elementary proof for
the restricted fixed-input, fixed-order static kernel. This is author
self-review, not an independent proof certificate. The decoder corollary is
conditional on its explicitly stated positive gaps and `graph_val=0` branch.
The broader assertions “the full solver becomes graph blind”, “all anchor
eigenvectors converge”, “decoder gaps are automatic”, and “this proves quantum
optimization hardness or advantage” are unsupported or refuted below.

## Claim card and dependency graph

Objects: fixed nonnegative symmetric zero-diagonal (w\in\mathbb R^{m\times m}),
even (m\ge4), zero off-diagonal minimum, canonical balance QUBO with (k=m/2),
fixed (R\in\mathbb Z_{\ge1}), variant (v\in\{1,2\}), and fixed pair order.
Large-penalty regime: (m\lambda>d_++w_+), and additionally (w_+/D\le1/2)
for the displayed (R\ge2) constant. Source: one common normalized pure input
in the (N)-photon symmetric sector, not necessarily the all-ones input.
Conclusion: mode-unitary bounds (4),(5), Fock lift (7), raw measurement TV (8),
and necessary physical discrimination-copy bound (10). Norms and squared
fidelity convention are explicit in the proof. (m,w,R,v,\pi,N) are fixed
for the stated asymptotic rates; no joint scalable theorem is inferred.

Dependency chain:

1. QUBO identity (1) and global normalization: direct real algebra.
2. Gate definition (2): authenticated archive and Perceval convention.
3. Exact regime (3): extrema comparison, proved internally.
4. Gate norm and product telescoping: elementary matrix proof, no spectrum.
5. Endpoint identity (R=1), derivative bound (R\ge2): elementary calculus.
6. Tensor telescoping and symmetric-subspace restriction: internal proof.
7. Pure-state overlap, two-dimensional trace-distance calculation, and
   measurement contraction: elementary finite-dimensional quantum mechanics.
   The latter also follows by writing each event probability difference as
   (\operatorname{tr}E(\rho-\sigma)), (0\le E\le I), bounded by the sum of
   the positive eigenvalues of the traceless Hermitian difference.
8. Decoder corollary: separate event bounds, explicit gaps, and nonnegative cut
   bounded by total edge weight. Not an inference from convergence alone.
9. Finite computation: corroboration and falsifier, not a universal proof leaf.

## Obligation matrix and adversarial attempts

| Obligation | Result | Evidence or correction |
|---|---|---|
| Symmetric QUBO factors and additive constant | passed | Expanding ((|x|-k)^2) gives diagonal (1-2k=1-m) and off-diagonal (lambda), since (x^TQx) doubles unordered pairs. |
| Normalization min/max use diagonal entries | passed | Explicit strict regime; min offdiag weight zero is a real hypothesis. |
| Archive/paper angle factor | passed with variant labels | Perceval uses cos(beta/2); literal uses half the paper's intended Rx parameter. No silent repair. |
| Original pair order, gate multiplication | passed | Fixed serialized order; gate product on left. Three orders retained in raw evidence. |
| Eigenvector degeneracy invalidates static theorem | refuted objection | No eigenvectors in definition. Rotating-eigenvector counterexample retained for spectral extensions. |
| Uniform (O(1/\lambda)) at (R=1) | failed | Endpoint angle has a square-root term; corrected bound is (O(1/\sqrt\lambda)). |
| All matrix-distance bounds are sharp asymptotics | not claimed | Triangle inequalities may be loose or cancel; empty graph gives distance exactly zero. |
| Fock factorial normalization | passed | Symmetric-tensor proof; independent creation recursion includes (sqrt{n_i+1}). Distinct inputs need no input factorial. Identity and HOM controls pass. |
| Copy-cost (\lambda) vs (\lambda^2) | passed in restricted interpretation | Pure-state fidelity and independent copies, not a solver lower bound and not an adaptive-query theorem. |
| Same graph-aware decoder on both compared states | passed | Common channel contracts at fixed graph. Distribution-level argmax/ranking needs separate gaps. |
| Different graph-aware decoders preserve graph blindness | failed | Even constant graph-dependent output maps are a counterexample. |
| Strict marginal gaps automatic | failed | Exact matching-order (m=4) counterexample, equation (11). |
| Pool of at most two feasible candidates | conditional | Requires unrestricted prefix branch, kth marginal gap, modal Fock gap, (\lambda>W), ideal distribution. Final graph scoring remains graph aware. |
| Hybrid source selection covered | failed | Distinct source states can remain orthogonal under identical limiting circuit. |
| Loss postselection covered for free | failed | Conditional laws require acceptance control. Only common trace-preserving noise is included. |
| Supported original QUBO class | restricted | Weighted regular graphs give constant diagonal; irregular numerical graphs are labeled extensions. |
| Prior-art absence implies novelty | rejected | Bounded search is not exhaustive. Novelty remains OPEN. |

The matching example is admissible for the finite-product definition at every
fixed (R,v). Its generators commute, square to identity, and sum to (J-I).
Thus (11) commutes with every permutation, and the all-ones input forces equal
click marginals. This invalidates the missing-gap premise directly. The
separate family (V(t)\operatorname{diag}(e^{i/t},e^{-i/t})V(t)^T\) also shows
why a naive eigenvector-convergence extension would fail near a degenerate
limit. Neither counterexample refutes the actual unitary bounds.

## Exact external-source authentication and bounded novelty check

Inspected source bytes were read as text; the external program's processor,
network, storage and optimizer branches were not executed. Authentication means
the listed local bytes match these hashes and locators, not that the external
algorithm's claims have all been proved.

| Source/version | Locator and exact needed fact | SHA256 |
|---|---|---|
| Ranjan, Silver, Patel, Chickmagalurnanjun, Tiwari, *ObliQ: Solving Quadratic Unconstrained Binary Optimization Problems on Real Photonic Quantum Machines*, PACM MACS 9(3), Article 58 (December 2025), DOI 10.1145/3771573 | [Author PDF](https://repository.rice.edu/server/api/core/bitstreams/0c308cfa-0cac-4b03-ba49-9effdba0799b/content), 25 pages; §§4.1–4.4: constant-diagonal restriction, pair kernels, all-ones static source, threshold/prefix extraction, hybrid source selection. | `61f3fb1f26a9553845b75d0fc7b6e973c28d30cc06c1c7e730c108a3d7a2da86` |
| [Zenodo artifact v2](https://zenodo.org/records/17343439), DOI 10.5281/zenodo.17343439 | `ObliQ.zip`, version label v2, record modified 2025-10-13. | `8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948` |
| Artifact `ObliQ/circ_init.py` | Lines 35–63: runtime set order, global min/max, repeat and half-angle. Lines 105–131: threshold marginals, raw Fock mode, original-Q scoring. | `8526955119d0fc74506aa4952289bf0a65bf1ebe820331d024c53fb5583fe8ad` |
| Artifact `ObliQ/circ_init_vqc.py` | Same static construction; separate variational/hybrid stage not part of theorem. | `2f6fc3b34610d928bfea9661196a60a66622cb7e68c3e8f0efce12ae19b7975d` |
| Artifact `ObliQ/utils.py` | Lines 37–71: `graph_val=0` unrestricted prefixes; other branches filter coloring groups or assignment rows/columns. | `ef2518f9e1289f273a58bd18e0a22703b0404f43b605333de59ecf00e29d5c46` |
| [Perceval v0.11 source](https://raw.githubusercontent.com/Quandela/Perceval/v0.11.0/perceval/components/unitary_components.py) | Rx matrix uses cos(theta/2), i sin(theta/2). | `d7d4a187fea8daf4a53008dd0e87b8f33264d3cb8dc41d24790044ef2d8bf554` |

Earlier project inputs read from the main workspace, not modified here:

- `research/optical_penalty_spec.md`: `d00db87b4d27633106c447c5657a860cfbb263482fd2da7ebef1e980f854e4cf`.
- `research/phase2_novelty_audit.md`: `0b2615d70812aa4e84df1a38c6c70b76e6dd2ecb8f142f51c9672c9dc2513747`.
- `theory/phase2_candidates.md`: `b10a2c03c1c3239f80c8306c6e42607f210675e5e3b34c4bf3371fda3cb36888`.

The generic penalty/normalization issue is established prior art, rather than
a new research contribution: [Hristo N. Djidjev, arXiv:2301.12393v1](https://arxiv.org/html/2301.12393v1),
§1 and §3.2.1, explicitly discuss large penalties making objective coefficients
small after normalization and harming finite-resolution annealing. That source
does not provide the optical product/fidelity theorem needed here. Its analog
hardware mechanism is also different from the ideal lossless convergence
proved in this note. This distinction is an inference from reading the exact
source, not a claim that the optical specialization is necessarily novel.

Bounded web queries repeated on 2026-11-21:
`"ObliQ" "penalty" normalization graph`,
`"photonic" "QUBO" "large penalty" normalization`,
`"ObliQ" "diagonal" "normalization"`.
The ObliQ primary manuscript was returned. No exhaustive citation graph or
complete photonic-optimization survey was performed. Search noise, differing
terminology, and generic stability results prevent a novelty conclusion.
**Novelty stays OPEN.** No new theorem of a cited paper is attributed without
its hypotheses; external sources define the competitor, while the bound is
derived explicitly here.

## Preserved computation P31

Execution contract: `experiments/P31_washout_bound_audit/contract.json`.
Independent script: `experiments/phase3_washout_bound_audit.py`, SHA256
`442f8cf77a17ab6e61891d2ee1be334906426761b121c3271cb5ccc6c6f60b7f`.
Neither project simulation code nor the competitor archive is imported.
The scientific result is a floating-point finite check, plus exact SymPy
identities; it is not a formal verification of the general proof.

- Seed `20261121`, `numpy.default_rng/PCG64`; Python 3.11.15, NumPy 2.4.6,
  SymPy 1.14.0. Numerical requirements are pinned in the dedicated experiment
  requirements file; adding a project-wide SymPy optional dependency is outside
  this worktree's authorized scope.
- Nine disclosed graphs: for each (m=4,6,8), alternating weights 1,2 cycle,
  one seeded random sparse graph (weights 0.1–2, forced missing pair 01), empty
  graph. The random graph is not a broad ensemble claim; the cycle is weighted
  regular of degree 3. Every adjacency matrix is saved.
- Orders lex, reverse, runtime archive order; (R=1,2,10), (v=1,2),
  (\lambda=16,64,256,1024,4096,16384): **972** matrix checks. All satisfy the
  displayed normalization and derivative regimes.
- **36** full-Fock comparisons: (m=N=4), two nonempty graph families, lex,
  all (R,v), (\lambda=16,256,16384). The creation recursion retains every
  collision sector and records raw amplitudes, without normalizing afterward.
- **36** limit-gap checks: (m=4,6,8), lex/archive orders, all (R,v), source
  all ones. All photon numbers are conserved.
- Matching-generator identities and the corrected (R=1) matrix identity pass
  in exact SymPy arithmetic. Identity-source amplitude error is zero; HOM
  probability error is (1.11\times10^{-16}).

Run `run_001` started **2026-11-21T10:25:38.258389+00:00**, completed in
1.311233 seconds, exit 0. Recorded base commit is `8edfca7...`, dirty=true
because the new experiment files were uncommitted. The containing commit
preserves those exact files; the manifest is not retroactively edited to claim
a clean run. Input hashes were observed unchanged before/after execution.
Wall cap 60s, CPU cap 60s, log cap 1MiB, numerical-library thread cap 1;
no unsupported affinity or memory cap was silently assumed.

Maximum normalization error: (3.02\times10^{-14}). Maximum error in the
normalized-Q identity: (1.11\times10^{-16}). Maximum positive violation of
unitary bound, tensor bound, or measured-TV/trace bound: **0**, at tolerance
(10^{-10}). This means no tested violation, not exact floating-point proof.

For the (m=4) alternating cycle, lex, literal variant, the last grid point is:

| R | \(\|U_{16384}-U_\infty\|\) | Bound (B_{16384}) | Descriptive last-three-point log slope |
|---|---:|---:|---:|
| 1 | 0.0024730915843 | 0.0047153878090 | −0.5000574 |
| 2 | 0.0000066291023 | 0.0000186889792 | −1.0002704 |
| 10 | 0.0000057518719 | 0.0000162666684 | −1.0002818 |

The slopes corroborate the proposed upper-rate regimes on this example but
do not prove asymptotic equivalence. The raw gap data include exact/numerical
ties: at (m=4), archive-runtime order, corrected (R=1), both reported gaps
are 0; lex corrected (R=1) has modal gap (9.71\times10^{-17}), consistent
with a tie at floating precision. These are retained negative results.
The exact matching argument, not numerical near-zero gaps, establishes the
counterexample to guaranteed strictness.

### Output hashes and reproduction

All paths below lie under `experiments/P31_washout_bound_audit/run_001/`:

| File | SHA256 |
|---|---|
| `raw.json` | `8d49973baf0df4cebdcc35f3b8550eb8e117fd9cd455f3a230dcb8ea4fc9a4a8` |
| `summary.json` | `0284c936bbbe3f747b3c8bd6100156bb18ddcf5c630ea6d3c8a4830c7a31b70a` |
| `manifest.json` | `bef077cb9a1b4408ac8eeb4e6800594389755630e27d4854790b82c8c63f08d2` |

The manifest is schema v2 and passed `validate_manifest.py --root .` with
status `completed`; mathematical interpretation is explicitly still a review
obligation. `stdout.txt` and `stderr.txt` are preserved too. For a new bounded
run, with pinned requirements installed and `MATHBOX_AUDIT` pointing to the
installed computation-audit skill directory, run from the project worktree:

```sh
python "$MATHBOX_AUDIT/scripts/run_experiment.py" \
  --root . --contract experiments/P31_washout_bound_audit/contract.json \
  --input experiments/phase3_washout_bound_audit.py \
  --input experiments/P31_washout_bound_audit/requirements.txt \
  --output experiments/P31_washout_bound_audit/run_002 \
  --result experiments/P31_washout_bound_audit/run_002/raw.json \
  --result experiments/P31_washout_bound_audit/run_002/summary.json \
  --timeout 60 --max-output-bytes 1048576 --max-cpu-seconds 60 --max-threads 1 \
  -- python experiments/phase3_washout_bound_audit.py \
  --output experiments/P31_washout_bound_audit/run_002
python "$MATHBOX_AUDIT/scripts/validate_manifest.py" \
  experiments/P31_washout_bound_audit/run_002/manifest.json --root .
```

The new output directory must not exist. The manifest records the actual
interpreter and declared numerical versions; use the pinned versions above
for byte-level comparability. The serialized orders in `raw.json` define the
actual archive-runtime order used here, independently of future Python/set
implementation changes.

Existing suite: `PYTHONDONTWRITEBYTECODE=1 <root>/.venv/bin/python -m pytest tests/`
in this isolated worktree: **150 passed in 17.32s**, Python 3.11.15,
pytest 8.4.2. No project source, manuscript, QPU credentials, QPU program,
shared state, or physics implementation was changed.

## Strongest safe interpretation and remaining work

The authentic static kernel loses graph-dependent physical distinctions under
global penalty normalization, for a fixed common source and finite fixed gate
layout. The endpoint changes the available rate. This is a mechanism and
restricted copy-budget statement relevant to penalty encoding, not a theorem
that optimization fails. Classical decoding and hybrid source preparation
must be accounted for separately, including their computational and shot
budgets. The finite results justify a falsifiable local test of the mechanism;
they do not themselves justify a quantum-performance claim or QPU expenditure.

Remaining review: independent rederivation of P3.1 and its copy inequality,
review of the authenticated implementation in the physics worktree, and a
broader novelty audit. Cheapest falsifier: reproduce a domain-valid violating
matrix or full-Fock case with its explicit order; for the decoder extension,
attempt a gap-free proof and confront equation (11). No required mathematical
step is replaced by the largest observed numerical value.
