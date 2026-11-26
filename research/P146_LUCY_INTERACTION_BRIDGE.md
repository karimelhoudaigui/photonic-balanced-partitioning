# P146 — Lucy logical-interaction bridge, public evidence and local alternative

27-Nov-2026; bounded primary-source/read-only package inspection.
Branch `research/p146-c-digital-lucy`; P146-C171 and the weighted-recycling
supplement remain unchanged. No import, code execution, account/platform
query, credential access, message to Laurent/support, job or QPU action.

**Verdict:** Lucy's advertised universal digital gates are real public claims,
not evidence of 24 logical qubits or of our particular remote instrument.
A concrete local heralded CZ is available in Perceval. The weighted-memory
recycling route additionally requires controllable surviving quantum memory;
its direct implementation on the current Lucy service remains UNVERIFIED.
This is a missing capability certificate, not a claim that Lucy lacks gates.

## Evidence ladder: model, remote transport, actual Lucy feature

| Checked primary source/version | Verified content | Transfer limit |
| --- | --- | --- |
| [Quandela Lucy](https://www.quandela.com/qpus/lucy/), live 27-Nov-2026, specifications/fidelity panels | MOSAIQ-12, 12 data qubits, 24 modes, universal/all-to-all chip; advertised 2-qubit fidelity 99.0±0.8% | A fidelity panel supplies neither accepted Kraus maps nor account-level gate/ancilla/feedback permissions |
| [GENCI, 19-Nov-2026](https://www.genci.fr/en/node/407), Lucy sections | 24-mode Lucy in production since May; French access since May and EuroHPC access since August; dual-rail use cases | Confirms operational use, not a stationary-spin API or a particular composable cost gate |
| [TGCC public stack](https://www-hpc.cea.fr/tgcc-public/en/html/toc/QuantumSoftwareStack.html), build2026-09-08.1512, Using Lucy | Irene/myQLM dispatch, Perceval experiment to `MyQLMHelper.make_job`, terminal `sample_count`; `get_specs` is documented separately | Its worked hardware example is a beam splitter, not a measured/conditional CZ circuit. Qaptiva/local CNOT examples elsewhere are simulation |
| [Perceval-interop v1.2 MyQLMConverter/QuandelaQPUHandler](https://perceval.quandela.net/interopdocs/v1.2/reference/myqlm.html) | Gate-based conversion exists: default `use_postselection=True` combines postprocessed/heralded CNOT; False selects heralded CNOT only. Handler translates requests to a selected remote Quandela platform | Software gate compilation and remote transport are distinct from successful Lucy deployment. This is explicitly v1.2; the v1.3 page was discoverable but its body could not be fetched here |
| [Perceval v1.3 CNOT tomography](https://perceval.quandela.net/docs/v1.3/notebooks/Tomography_walkthrough.html), §§I–IV | Catalog Knill CNOT, local `SimulatedComputer("SLOS")`; normalized conditional chi is separated from `chi_unnormalized` and `gate_efficiency`, ideal efficiency 2/27 | A normalized process fidelity of one is not a deterministic gate or a remote Lucy result |

[Perceval v1.3 configurators](https://perceval.quandela.net/docs/v1.3/reference/components/feed_forward_configurator.html)
provide conditional circuits after detected classical modes and a default
branch; their example is local SLOS. [Computer v1.3](https://perceval.quandela.net/docs/v1.3/reference/runtime/computer.html)
distinguishes local simulation from platform-dependent remote parameters.
Thus neither a converter, a configurator nor a successful local experiment
alone establishes an intrashot adaptive hardware primitive. No remote client
was instantiated. TGCC's indicative mean 2% transmission is not a spectral
certificate, per-gate success probability or current loss calibration.

## Small local heralded digital alternative with all failure branches

Use the known Knill heralded CZ, independently of Lucy availability. Primary
[Knill, quant-ph/0110144v1](https://arxiv.org/pdf/quant-ph/0110144v1),
24-Oct-2001, *A Note on Linear Optics Gates by Post-Selection*, §III Eq.(11),
printed pp.5–6: conditional sign with two helper photons, ideal success2/27;
counters distinguish zero, one and more than one. This improves the separate
elementary KLM1/16 construction quoted in P146-C, without changing that note.

Read as TEXT ONLY from installed Perceval1.3.0, whose METADATA names Quandela:

- `.venv/lib/python3.11/site-packages/perceval/components/core_catalog/heralded_cz.py`
  SHA256 `b1c0bdee32442243ec9db27e286b96fcbb3769e91b51ddd58a5980cc86a17e8a`:
  `build_circuit` supplies a six-mode unitary; `build_experiment` declares
  dual-rail data ports0–3 and helpers4,5, each input/output heralded at one.
- Corresponding `postprocessed_cz.py`, SHA256
  `6e7a8f832cff1c8bc259bf055a804f95ddf4de35a4f866d2fa634ab5da8d8a80`,
  instead uses vacuum helper modes AND a data-code postselection. These are
  different physical resource/acceptance contracts, despite similar names.

A future local qualification can use two dual-rail data photons and two
helpers: six modes, four total photons. Local Hadamards prepare encoded
`|+,+>` without entangled-input credit. Retain the BARE six-mode unitary and
the complete four-photon output law, all126 PNR occupations including zeros,
before any herald filter. For helper record (r,s), the full data Kraus map is

    K_(r,s)=<r,s| Gamma(U) |1,1>_helpers.

The ideal accepted map on the entire two-qubit code is
`K_(1,1)=sqrt(2/27)*CZ`, up to a common phase/conventions. Its success2/27
and failure25/27 are unconditional ideal probabilities, not hardware rates.
All other helper records and their associated data photon deficits/bunching/leakage
remain paid outputs. These Kraus maps complete a trace-preserving instrument
when all records are included. Do not use an Experiment's filtered normalized
law as the full reference. Future noise/loss models require their extra outcomes.
This paragraph is a prospective definition, not an authorized run/population.

This one gate prepares a two-node graph state conditionally; it is an exact
small classical-simulation target, not optimizer evidence. CZ plus local phases
supplies a discrete ZZ angle. General weighted ZZ needs a specified synthesis
and fresh resources. Failure is NOT automatically identity/recoverable, so this
does not implement weighted local recycling or a memory-based RUS module.
With terminal-only detection it verifies the postselected circuit; it cannot
certify that an undetected surviving resource was adaptively reused.

## Exact capability certificate for Laurent to obtain, without guessing

The requested answer is a dated platform/software contract or an explicit
unsupported/unavailable response for each item, without secrets. This is a
question list for an authorized follow-up, not an external message sent here.

1. Identify the actual Lucy endpoint/allocation and supported stack versions.
   Does the service accept gate-based circuits directly, converted passive
   circuits with explicit helpers, or both? Which CZ/CNOT implementation and
   arbitrary ZZ synthesis are supported, with what public compilation limits?
2. Give total mode/photon limits INCLUDING ancillary/vacuum/herald resources;
   distinguish twelve advertised data qubits from what remains after helpers.
   State permitted input routing, source states, circuit depth and calibration.
3. Specify detector response: threshold, true PNR or multiplexed pseudo-PNR,
   count range, inefficiency/dark events, and accessible per-mode herald records.
   Can one request the unfiltered joint data/helper law and rejected records?
4. Separate intrashot measurement-dependent circuit switching from adaptation
   between independent jobs. State supported conditionals/default branches,
   latency, available delays and whether surviving data remain coherent.
5. For weighted recycling specifically: is any emitter-spin/storage register
   exposed for preparation/rotation, spin-photon emission, Z readout/reset and
   later reuse after a failed optical attempt? For how long and with what noise?
   Otherwise, what explicit flying-photon storage/reuse primitive substitutes?
6. Give each logical gate's all-branch physical model: accepted map and success,
   recoverable failures, destructive failures and loss/herald ambiguity. Does
   a reported gate fidelity condition on accepted detections/corrections?
7. Define counters/costs: source pulses, zero detections, shots, retained samples,
   filters/mitigations, helper photons, resets, job/compile/communication time.
   TGCC's documented sample limits do not themselves settle all those counters.

An authorized specifications-only query could retrieve the documented platform
commands/constraints/options and characterize what fields are absent; such a
query is NOT performed or newly authorized by this note. Instrument semantics
and memory may still require an operator answer beyond machine-readable specs.

**Next gate:** if the service only offers fixed passive circuits plus terminal
readout, the local Knill/all-output comparison remains meaningful; it does not
implement the weighted-memory compiler. If reusable matter memory or an explicit
equivalent is confirmed, bind its loss/feedback instrument before applying the
recycling theorem. Keep independently retuned D/species, exact classical controls
and every branch/setup cost. Neither public universality nor a conditional gate
fidelity passes that resource or optimization gate. Hardware bridge remains OPEN.
