# Perceval validation

Status: **PASS**

Executed 2026-11-20T17:41:41.582434+00:00 from Git `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508` plus recorded source hashes.
Local Perceval 1.3.0 SLOS backend; no remote processor, token, QPU, or postselection.

The gate compares all 8464 Fock outcomes in 125 input/circuit cases: 60 seeded Haar circuits across (m,k)=(2,1),(2,2),(4,2),(4,3),(6,3),(8,4), each with first-k single-photon input AND fully bunched input. Identity, permutation, odd-k phase, HOM and vacuum are added. Zeros are compared too.

- Maximum absolute probability error: 1.77636e-15.
- Maximum complex amplitude error: 2.13502e-15.
- Maximum raw normalization error: 4.21885e-15.
- Acceptance tolerance: 1e-10, absolute.
- Custom output was never renormalized.

Full matrices, input occupations, output occupations, custom and SLOS complex amplitudes and probabilities: [raw distributions](../experiments/validation/full_fock_distributions.json).
Versions, timestamps, source/output SHA256 and exact command: [summary](../experiments/validation/summary.json).

Reproduce:
```sh
MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python experiments/validation/run_physics_validation.py
MPLCONFIGDIR=/tmp/pasqal-matplotlib .venv/bin/python -m pytest tests/test_hom.py tests/test_permanent_normalization.py tests/test_perceval_cross_validation.py -q
```

This PASS is an ideal small-system simulation gate only. It does not authorize QPU work or validate other objective/baseline gates. Perceval absence causes test skips, which do not satisfy this gate.

API checked against [official SLOS documentation](https://perceval.quandela.net/docs/v1.3/reference/backends/slos.html); installation package is [perceval-quandela](https://perceval.quandela.net/docs/v1.3/getting_started.html).
