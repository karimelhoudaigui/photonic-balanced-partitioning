# Physics and noise recovery, 2026-11-24

The new `photonic_balanced_partitioning.noise` package implements a physical
pure-internal-state Gram model and independent output losses on the complete
Fock distribution. **37 new physical tests pass; all324 tests in the isolated
base plus this module pass.** No noisy device-performance result or Belenos
calibration is claimed. No QPU, local model, manuscript or existing raw dataset
was modified or called.

Base: `6154b460e1c8b37cf2a7023fcbfff35d31a7220c`.
Worktree: `.qwen/worktrees/recovery-physics-20261124`.
Branch: `recovery/physics-20261124`.

## Implemented physical contract

U has output rows and input columns and must be square/unitary. Inputs are
explicit distinct singly occupied spatial modes; repeated spatial inputs are
rejected by the interference routine. Internal photon states are normalized,
pure and uncorrelated, with unresolved ideal detection. Their Gram matrix
S_ab=<phi_a|phi_b> must be Hermitian PSD with diagonal one. Arbitrary complex
phases are retained. Mixed/correlated internal states, multiphoton source
contamination, drift and dark counts are not covered.

For an occupation t and repeated output list y, amplitudes A_sigma are products
of the corresponding U entries. The probability is

    p_S(t) = sum_(sigma,tau) A_sigma conjugate(A_tau)
             product_j S[tau(j),sigma(j)] / product_i t_i!.

Expanding spatial-times-internal creation operators establishes the bra/ket
orientation and output factorial. Distinct occupied spatial inputs make the
initial state normalized without an input multiplicity factor. This matches
Tichy, arXiv:1410.7687v3, Eq.(19), with the multiplicity factor explicitly
restored as discussed immediately before Eq.(17). Its SectionIII.6 explains
why arbitrary mixed-state sources require more than averaged pure overlaps.
[Primary source](https://arxiv.org/html/1410.7687v3)

The all-ones S yields full bosonic interference; identity S yields independent
particle routing with labels forgotten. Pair and triple exchange factors
retain |S_ab|^2 and complex triad products respectively. The implementation
does not use a global interpolation between the two limiting distributions.

Independent loss acts by the binomial thinning kernel on each spatial
occupation, retaining every detected-number sector and vacuum. Eta is either
a common survival or an output-mode survival vector. Only uniform loss may
be commuted through the interferometer. The complete N-detected sector is
exactly eta^N times the lossless law for uniform eta. Thus a fixed-N success
event requiring all photons scales by eta^N. The requested arithmetic is
verified: `.537*.9**4 = .3523257`. Here .537 is an illustrative input quoted
from the old manuscript table, not a newly validated circuit result.

Full mathematical/API documentation and a correct environmental unitary
dilation are in `docs/NOISE_MODEL.md`. API:

- `partial_distinguishability_distribution(U,input_modes,S=None)`;
- `apply_independent_loss(law,eta)`;
- `noisy_distribution(U,input_modes,S=None,eta=...)`;
- Gram validation/construction helpers and an immutable full-Fock mapping.

Hard guards are five photons,32 modes,2,000,000 permutation-pair or thinning
terms per stage. User max_terms may lower, not raise, this limit. Unitarity,
Gram and distribution checks use explicit1e-10 tolerances. Tiny negative
roundoff within tolerance is clipped with its mass recorded; no positive
probability rescaling or hidden normalization occurs. Every result reports
`FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED` and raw normalization, minimum
probability, imaginary residual and clipping diagnostics. These diagnostics
are not rigorous numerical enclosures or calibration confidence intervals.

## Validation performed

`tests/test_noise_physical.py` covers:

- HOM coincidence `(1-|S12|^2)/2`, including complex overlaps and both endpoints.
- Vacuum and one-through-four-photon ideal/distinguishable limits, with all
  Fock output factorials and no conditioned distribution.
- A complex three-photon Gram checked against a separate creation-operator
  expansion in spatial-times-internal modes. This reference has no Gram
  permutation-weight implementation. Internal phase gauge invariance and a
  demonstrably different result for the incorrectly conjugated Gram are checked.
- A k3 Gram whose output cannot be reproduced by any scalar global B/D
  interpolation, even the least-squares best unconstrained scalar.
- Gram shape/Hermiticity/diagonal/PSD/finiteness rejection, nonunitary and
  malformed/repeated spatial inputs, survival endpoints/range, and work limits.
- Every loss sector and vacuum, full normalization, eta0/eta1, eta^N mass and
  per-occupation scaling, bunched-output thinning and mode-dependent loss.
- Uniform-loss commutation against the independent mixture over all surviving
  input subsets and their principal internal Gram matrices.
- The requested four-photon arithmetic and an identity-circuit all-detected
  event. A subnormalized CF-only input to the loss function is rejected.
- Ideal full distributions for three small circuits against the installed
  Perceval SLOS backend: m2/k2, m3/k2 and m4/k3,29 occupations total, tolerance
  2e-12. Perceval was available, so this check actually ran rather than skipped.

The installed Perceval1.3.0 `components/source.py` was inspected. Its Source
documents a phenomenological quantum-dot source and two-photon mean-wavepacket
overlap parameter; generated distributions can be probability-filtered. That
API was not assumed to represent an arbitrary complex Gram. Perceval validates
the ideal limits here; the independent internal-mode reference validates the
partial-distinguishability phases. No remote processor or credentials are used.

The seeds are fixed in the tests; there is no training or parameter tuning.
The final full-suite receipt records input hashes before/after and software
versions. Python3.11.15, NumPy2.4.6, SciPy1.17.1, pytest8.4.2,
Perceval-quandela1.3.0, Exqalibur1.4.2. The final run reports324 passed in
3.15 seconds pytest time; measured CPU2.118515 seconds, elapsed3.557379292.
BLAS/OpenMP thread counts were set to one. All recovery checks, including
collection failures and initial imports/font setup, stayed below120 CPU seconds.
There was no large noisy campaign.

## Commands and failed sparse attempts retained

The initial new-test command actually executed was:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MPLCONFIGDIR=/private/tmp/pasqal-mpl-noise PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python -m pytest tests/test_noise_physical.py -q
```

It returned37 PASS. Subsequent hard-limit guard edits were covered by the final
complete run. The full-suite invocation used the same environment and a
Python here-document that called `pytest.main(['tests/','-q'])` under
`resource.setrlimit(resource.RLIMIT_CPU,(75,75))`. Its exact validation body was:

```python
import datetime,hashlib,importlib.metadata,json,platform,resource,time
from pathlib import Path
import pytest
resource.setrlimit(resource.RLIMIT_CPU,(75,75))
old=Path('reports/noise_recovery_validation.json')
old.rename('reports/noise_recovery_validation_sparse_failure.json')
paths=list(Path('src/photonic_balanced_partitioning/noise').glob('*.py'))+[Path('tests/test_noise_physical.py')]
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
started=datetime.datetime.now(datetime.timezone.utc).isoformat(); start=time.monotonic(); cpu=time.process_time()
status=pytest.main(['tests/','-q'])
receipt={'base_commit':'6154b460e1c8b37cf2a7023fcbfff35d31a7220c','started_utc':started,'argv':['pytest','tests/','-q'],'exit_status':int(status),'wall_seconds':time.monotonic()-start,'cpu_seconds':time.process_time()-cpu,'cpu_limit_seconds':75,'threads':1,'python':platform.python_version(),'versions':{p:importlib.metadata.version(p) for p in ['numpy','scipy','pytest','perceval-quandela','exqalibur']},'input_sha256_before':before,'input_sha256_after':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}
Path('reports/noise_recovery_validation.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('RECOVERY_VALIDATION',json.dumps(receipt))
raise SystemExit(status)
```

For normal reproduction use the pytest command with `tests/ -q`; the above
historical body renames the prior receipt and should not overwrite evidence.
Two earlier full-suite collection attempts lacked the tracked experiment
script imported by test_phase2_classical.py. A further run passed322 tests but
failed two infrastructure checks because the sparse checkout omitted tracked
`.qwen/settings.json` and `.qwen/agents`. Those failures were environmental,
not silently skipped. The failing receipt is retained unchanged as
`noise_recovery_validation_sparse_failure.json` (its historical `started_utc`
field was captured at completion, not startup). The required tracked files
were materialized unchanged; final suite324 PASS. No agent runtime was launched.
The cone-mode add command first failed, then the explicit non-cone sparse
configuration succeeded. No experimental script or agent configuration was edited.

A separate read-only Python command called
`BalancedGraphPartitioning.complete_graph(4).solve_exact()` and
`BalancedGraphPartitioning.complete_bipartite(2,2).solve_exact()`: energies4
and2 respectively, partitions(0,1) and(0,2). No graph bug was found at this
base and no core mutation was performed. Root owns any further graph changes.

## Old manuscript consistency and review independence

The initially read paper05 and08 hashes were respectively
`07c849e179a0332311d32f05ca64f57c5fd955625de0de5edbe3c45ae05c1f3e` and
`d2fe16e930b7b4655eeae279049a8bc36aee87c4cf52d77eb15359023c447954`.
The coordinator was notified of these issues without this agent editing paper:

1. The old N1 bound used an incorrect output-intensity-squared Gram. The
   proved spatial Gram is B_ab=sum_i |V_ia V_ib| on occupied input columns.
2. Identity produces a deterministic partition, so its optimal-conditional
   success need not equal1/C(m,k). That is a Haar/uniform comparison, not an
   identity-circuit fact. The epsilon-regularized log barrier also remains
   finite at zero CF; its asserted divergence needs qualification.
3. The old noise section's global xi interpolation is not the implemented
   pure-state partial-distinguishability model, and its direct sum of
   attenuated blocks is not a loss-channel unitary dilation.
4. Its quoted uniform-loss success0.381 does not follow from0.537 at eta0.9
   for a four-photon-required event: the arithmetic gives0.3523257. Under
   that event the conditional valid-CF law does not change from loss alone.
5. Vacuum and lower-photon states can satisfy the no-collision predicate.
   For the N=k balanced pipeline, validity additionally requires detected
   photon number k. Inclusive threshold acceptance is a different event.

P33's proof and prior review hashes read here are
`7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c` and
`d5773cef7b017f5a68cd7b54c00a300443c029c573a1c928c0e24ec56fc3645e`.
P37's proof/review hashes are
`fda5160d1d4eb232f67eae09cfcfabf3024822ea1e0720ef639267374a642807` and
`29a3a991af108a0330616bf9e0c787e119f182171018473bfac1c84c4d672184`.
This agent previously reviewed those proofs. Re-reading them in this recovery
is a continuity/consistency check, not a new independent review or a second
vote. Their exact ideal-source/Haar assumptions must not be automatically
extended to partially distinguishable photons. This agent authored the new
noise code; its testing is self-validation using independently implemented
physical formulas, not an independent external code review.

## Code and evidence hashes

| Artifact | SHA256 |
|---|---|
| noise `__init__.py` | `9142f60bd4e8596af9acfb6e9ae4dd66fa2abf62cbfb73591e0db79dde708e52` |
| noise `physical.py` | `2023e469e0eb0d4d4900def41f93fbfcc4fa5e91f63aebb6ec6d61dc0c382cb3` |
| `test_noise_physical.py` | `065362d0c7a6e5269fd9b9117dddad46ed953feb2d90a72d7abcce9f92fc083a` |
| successful receipt | `2183b3fd443048a73000cebeed273bfe29864667e5150e112fb9dcb5faf5eaa1` |
| sparse-failure receipt | `1ac4b3d0b13228ee2368c7e715d8d69573294e561184622320672451197d7174` |

The new package is ready for integration and bounded article-model review.
It supplies physical scenario calculations; it does not validate the old noisy
table or supply calibration data for a hardware go/no-go decision.
