# Occupation objective and bosonic mean-dominance audit

**The moment formulas and fixed-photon ground-state encoding pass this audit. The proposed same-frame bosonic mean advantage is rejected by an exact positive-semidefinite covariance identity.** This does not order optimum probabilities, tails, conditional CF costs, or independently trained optimizers.

Base: `2996904f861a5db2a732e38dbc97bd6c91e5708b`; isolated worktree `.qwen/worktrees/phase3-moment-objective`, branch `research/phase3-moment-objective`. No main/shared-status, manuscript, QPU, or prior data was changed. The root proposed the dominance identity; this agent reconstructed it and audited the component with independent finite references. This is not an author-blind proof certificate.

## Result and precise scope

For one photon in each of k distinct input modes, let V be the m-by-k occupied-column frame with V*V=I. The complete ideal output occupations n include every collision. The implemented cost is

    H(n)=sum_edges w_ij (n_i-n_j)^2 + mu sum_i n_i(n_i-1)/2.

All weights and mu must be finite and nonnegative. With total photon number k fixed, mu>W=sum_edges w ensures every ground state is collision-free: collisions have cost at least mu, while every CF cut has cost at most W. On CF states this is precisely the cardinality-k cut, hence minimum bisection for m=2k. The theorem is restricted to the fixed-k sector; losses and threshold-only measurements do not supply the same occupation objective automatically.

The penalty assumption and weight domain are substantive. With a negative edge -1, W=-1 and mu=1, collision (2,0,0,0) costs -3 while the best CF cut is -1, despite mu>W. The module rejects negative weights. With a triangle and an isolated vertex, omitting mu lets a two-photon bunch on the isolated mode beat every balanced cut. These failures are preserved in the proof notes/tests rather than hidden.

For q_ia=|V_ia|^2, a_i=sum_a q_ia, b_i=sum_a q_ia^2, P=VV*, C_ij=sum_a q_ia q_ja, the moment formulas are:

| quantity | bosonic | distinguishable |
|---|---|---|
| E[n_i] | a_i | a_i |
| E[n_i^2] | a_i+2(a_i^2-b_i) | a_i+(a_i^2-b_i) |
| E[n_i n_j], i!=j | a_i a_j+|P_ij|^2-2C_ij | a_i a_j-C_ij |
| mean collision pairs | sum_i(a_i^2-b_i) | half that value |

The distinguishable control uses a separate categorical distribution for each occupied column. Averaging columns into an iid multinomial would be a different model. Exact expectation evaluation is O((m+|E|)k) after O(mk^2) frame validation; a full moment matrix uses O(m^2) storage. Neither path needs a permanent, a sampling call, or C*. This is an inexpensive classical quartic objective, not a demonstrated efficient solution of its nonconvex global search problem.

## Why the same-frame mean cannot favor bosons

For each a<b define z_i=V_ia conjugate(V_ib). Both means agree, and

    Cov_b(n)-Cov_d(n)=2 sum_(a<b) Re[z z*] >= 0.

For any real c its quadratic form is 2 sum_(a<b)|sum_i c_i z_i|^2. Consequently

    E_b[H]-E_d[H]
      =2 sum_(a<b) sum_edges w_ij |z_i-z_j|^2
       +mu sum_(a<b) sum_i |z_i|^2 >=0.

With mu>0, equality holds exactly when the occupied-column supports are pairwise disjoint (the zero/one-photon cases are vacuous). The full output statistics then agree with independent scattering. For mu=0 a disconnected graph admits other equality cases; this boundary is explicitly tested. The [proof notes](../theory/phase3_occupation_dominance.md) include both directions, fixed-number conservation, and the ground-state argument.

Thus increasing bosonic fluctuations cannot lower this positive quadratic occupation cost relative to distinguishable photons at the same V. No grand optimization benchmark was launched after identifying this obstruction. Both families can attain the same global minimum using a permutation routing to a known optimal subset, which does not discover that subset.

## A retained exception: optimum success can still be larger

Take m=4,k=2, the unit-weight path 0-1-2-3, mu=4, and the normalized four-mode Walsh matrix. Its first occupied columns are (1,1,1,1)/2 and (1,1,-1,-1)/2. Bosons yield only the two optimal CF cuts 01 and 23, together with four bunching outputs. The distinguishable model also yields the four nonoptimal CF cuts.

| metric | bosonic | distinguishable |
|---|---:|---:|
| mean H | 11/2 | 4 |
| physical optimum probability | 1/2 | 1/4 |
| CF probability | 1/2 | 3/4 |

The cost mean and success probability therefore rank the statistics differently in an explicit nonnegative graph example. This counterexample is structural, not a selected benchmark demonstrating useful computational performance. Its full distributions are retained in the raw record.

A further implementation guard: V must remain a frame, not merely the projector VV*. Mixing occupied columns can change the two-photon Fock state and the quartic moments while preserving VV*. Identity and an HOM rotation provide a tested example with identical projectors and different cost.

## Implemented interface

```python
from photonic_balanced_partitioning.photonic.occupation_objective import (
    occupation_cost, occupation_moments, occupation_expectation,
    occupation_statistics_gap,
)
# V.shape == (m, k), V.conj().T @ V == I_k
energy = occupation_expectation(V, edges, mu, model="bosonic")
moments = occupation_moments(V, model="distinguishable")
# moments.mean; moments.second == E[n_i n_j]; moments.collision_pairs
gap = occupation_statistics_gap(V, edges, mu)
# gap.graph, gap.collision, gap.total: explicit nonnegative square sums
```

The gap routine is an audit helper with O(k^2(m+|E|)) work; it is not the sparse training path. Invalid/nonorthonormal frames are rejected without QR correction or silent renormalization. No C* or threshold repair is used.

## Executed checks and provenance

Recorder status **completed**, exit 0; started `2026-11-21T20:30:18.579335+00:00`. Raw numeric runtime 0.071117s excludes dependency import/setup (recorder runtime retains those costs).

- 24 complex Haar circuits (m4/k2 and m6/k3, 12 declared seeds each), complete probabilities from the independent P30 creation-operator recurrence, and distinguishable independent-particle convolution.
- Eight additional local Perceval SLOS circuits. Their distinguishable control separately obtains each labelled particle’s one-photon Perceval distribution and convolves it; no indistinguishable backend output is mislabelled distinguishable.
- All 32 complete distributions were checked against the moment, cost, covariance-gap and positive-square formulas. The Walsh success counterexample and boundary/invalid-input cases are retained.
- Maximum raw-moment discrepancy: `1.1102230246251565e-15`.
- Maximum mean-cost discrepancy: `1.0658141036401503e-14`.
- Maximum Perceval probability discrepancy: `1.1102230246251565e-16`.
- Maximum positive-gap identity discrepancy: `1.1546319456101628e-14`.
- Minimum numerical covariance-gap eigenvalue: `-2.2846572207994663e-16`, consistent with rounding around the fixed-number null direction; the universal PSD conclusion rests on the proof, not this numerical value.
- Targeted tests: **43 passed** in 21.04s. Full isolated-worktree suite: **237 passed, 9 cache warnings** in 25.20s. No skipped Perceval tests in that run.
- **Zero physical shots, zero training evaluations.** Fixed RNG seeds, input/output hashes, package versions, and complete reference distributions are recorded. No new dependency was installed.

Artifacts: [module](../src/photonic_balanced_partitioning/photonic/occupation_objective.py), [tests](../tests/test_occupation_objective.py), [proof](../theory/phase3_occupation_dominance.md), [validation source](../experiments/occupation_objective_validation/validate_component.py), [contract](../experiments/occupation_objective_validation/contract.json), [raw distributions](../experiments/occupation_objective_validation/run/raw.json), [manifest](../experiments/occupation_objective_validation/run/manifest.json), and retained stdout/stderr in that run directory.

Reproduce from the isolated worktree, using a new output filename:

```sh
PYTHONPATH=src ../../../.venv/bin/python -B -m pytest tests/test_occupation_objective.py -q -p no:cacheprovider
PYTHONPATH=src ../../../.venv/bin/python -B -m pytest tests/ -q -p no:cacheprovider
PYTHONPATH=src ../../../.venv/bin/python -B experiments/occupation_objective_validation/validate_component.py \
  --output /private/tmp/pasqal-occupation-new.json
../../../.venv/bin/python -B /Users/karimelhoudaigui/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  experiments/occupation_objective_validation/run/manifest.json --root .
```

Numerical environment: Python3.11.15, NumPy2.4.6, SciPy1.17.1, Perceval1.3.0. A different checkout location should use the equivalent pinned project interpreter. Receipt paths/times change on replay; mathematical values should agree. The manifest validator reports a valid evidence record with completed status.

Hashes:

- Module: `afbb1378ff23fe65e38be70a68a7ba01c361ec656faa5cc34ef378a57f32e179`.
- Raw distributions: `679a69dfa74b06c3e86ab3f7e0f7d3228a7607df1a86fc01887ad1c00755abcc`.
- Proof notes: `5df0077c03900102cf405229b31be5f3432bfaed0c4bd1871fb2b117d15ea758`.
- The manifest pins the remaining sources and all observed before/after hashes.

## Prior work and decision

Walschaers et al., [Statistical benchmark for BosonSampling, New J. Phys.18,032001(2016), Eq.(3)/AppendixA](https://epub.uni-regensburg.de/33650/1/2016-NewJPhys-Walschaers-et-al.pdf), already gives classically computable bosonic/distinguishable output correlations. Its input-first matrix convention is transposed relative to V here. Martinez–Font-Segura, [2602.09894v1, Sec.3.6 Eqs.(39)–(41)](https://arxiv.org/html/2602.09894v1), also gives the general factorial/cross moments. These exact primary versions were inspected; their correlation formulas support the explicit derivation above. No exhaustive search authenticating novelty of the PSD specialization was performed. **Novelty remains OPEN; no new-contribution claim is made.**

**KEEP** the validated classical moment component and negative mechanism result. **REJECT** the proposed same-frame bosonic mean-cost improvement for this nonnegative quadratic objective. Stop this component before large training undertaken to demonstrate that impossible comparison. Do not infer a rejection of all graph optimization, of a tail-based mechanism, or of independently optimized discovery performance. Any such continuation needs a separately specified discriminator and fair classical budgets. No manuscript/QPU gate is changed.
