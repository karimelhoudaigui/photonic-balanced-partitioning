# Ideal photonic physics validation

Status: **PASS** for the explicitly tested ideal finite systems. This is not hardware validation.

## Conventions and model

`U[j,i]` maps input mode `i` to output mode `j`. Input is one photon in each of the first `k` modes, unless an explicit occupation is supplied. All photons are indistinguishable, evolution passive and lossless, and all output occupations are retained. The state basis is the lexicographically ordered weak compositions of `k` into `m` parts.

The transition amplitude is

\[
\langle t|\Gamma_k(U)|s\rangle =
\frac{\operatorname{Per}(U_{t,s})}{\sqrt{\prod_i s_i!\prod_j t_j!}}.
\]

Input columns and output rows are repeated with their occupation multiplicities. The permanent of the empty matrix is one. Full amplitudes are not renormalized; failure of the raw norm check raises an error. Nonunitary matrices are rejected rather than silently interpreted as loss models.

The full space has dimension `binom(m+k-1,k)` while its collision-free sector has dimension `binom(m,k)`. These differ already at `(m,k)=(4,2)`: ten full Fock states versus six collision-free states. Conservation of total photons does not preserve the number of occupied modes. Sample `is_balanced` now denotes the decoded threshold-bitstring cardinality and is false for collisions. Invalid sample energies are `NaN`, never a spurious zero cut.

## Bugs found and corrected

1. Ryser included an additional `(-1)^k` despite already using `(-1)^(k-|S|)`. It flipped odd-photon amplitudes. Probabilities and norm-only tests missed it. The three-photon phase and explicit permutation-sum tests detect the error.
2. `input_state()` populated basis index zero, which was the fully bunched last-mode state in the actual basis. `output_state()` independently used the intended first-`k` single-photon input. The input-state test itself asserted the erroneous index; it now checks the physical occupation and identity evolution.
3. Vacuum amplitude incorrectly returned zero. It now equals one.
4. Full output was automatically renormalized, hiding normalization bugs. Raw norm is now checked, with no amplitude correction.
5. Fock enumeration visited `(k+1)^m` tuples and filtered them. It now generates weak compositions directly and caches basis information.
6. A fixed photon count was mislabeled balanced in collisional samples. Tests now check valid balanced decoded bitstrings rather than the unrelated total number operator.

The independently implemented CF path computes the physical probability mass, without conditioning it to one. CF energy is conditional on its nonzero mass; the subnormalized moment remains available under `compute_unconditional_energy` solely as a diagnostic.

## Executed checks

- Identity returns the documented input state in the same basis.
- Permutations route the input photons to the expected occupations.
- Phase shifters preserve probabilities and reproduce complex phases, including odd `k`.
- One-photon beamsplitter gives the analytic transmitted/reflected amplitudes.
- For `U=[[1,-1],[1,1]]/sqrt(2)`, HOM gives `(-|20>+|02>)/sqrt(2)`, zero coincidence and unit collision probability. Independent labeled photons give coincidence probability `1/2`.
- Permanents for sizes `k=0,...,5` match direct explicit permutation sums on fixed seeded complex matrices.
- A fully bunched three-photon input matches the analytic multinomial distribution.
- Raw full Fock norms and CF subsets are checked at `(m,k)=(2,0),(2,1),(4,2),(4,3),(6,3),(8,4),(10,5)`.
- Perceval SLOS compares every probability and complex amplitude in 125 input/circuit cases, covering 60 Haar circuits, 8464 occupations, bunched inputs, HOM, identity, permutations, phases and vacuum. Maximum probability discrepancy is `1.7763568394002505e-15`, amplitude discrepancy `2.1350154548329877e-15`, norm error `4.218847493575595e-15`, all below absolute `1e-10`.

Command executed:

```sh
MPLCONFIGDIR=/tmp/pasqal-matplotlib .venv/bin/python -m pytest tests/test_fixed_photon.py tests/test_hom.py tests/test_permanent_normalization.py tests/test_perceval_cross_validation.py -q
```

Result: **85 passed**, no skipped Perceval cases. Existing tests that asserted incorrect physical behavior were corrected as described above; passing the former suite alone did not validate the physics.

Raw matrices/distributions, exact seeds, versions, timestamps, source hashes, tested range and reproduction command are in [validation summary](../experiments/validation/summary.json), [raw distributions](../experiments/validation/full_fock_distributions.json) and [v2 computation manifest](../experiments/validation/manifest.json). The manifest was validated against current source and output hashes using the Mathbox computation validator.

## Additional independent evaluator and mesh review

The CF-only evaluator uses a direct permutation sum, independent of the full simulator's Ryser implementation. Across 80 seeded Haar/mesh matrices with `m=4,6,8,10`, its probabilities match the simulator's CF path, and the exported Perceval mesh matches the intended matrix. Numerical residuals and exact source hashes are in [CF/mesh audit](../experiments/validation/cf_mesh_validation.json); reproduction is `MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/validation/audit_cf_mesh.py`. The ten tests in `tests/test_mesh_comparison.py` also passed.

## Limits

These checks support finite ideal floating-point computations in the specified range. They do not prove a quantum optimization gain, a noise claim, hardware compatibility with a specific device topology, or fair penalty-baseline performance. No QPU was accessed. Other scientific gates remain separate.
