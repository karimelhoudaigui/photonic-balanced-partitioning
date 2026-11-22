# P33 fixed contract: density/collision certificate

Owner: Astra; local execution and criticism by the existing seven Qwen roles.
Starting evidence: P30 static physics validated, P31 restricted washout proof
independently reviewed, P32 resource-accounting counterexamples retained. Those
results do not establish novelty of the new density implication.

Question: does the supplied density/collision bound survive exact full-outcome
checks and known counterexamples? The proof and implementation can be rejected.
No result is required to validate the original optimization hypothesis.

Model: one photon per distinct occupied input, passive lossless unitary,
complete bosonic versus distinguishable occupation laws. M is expected unordered
collision pairs; c is minimum positive mean output occupancy. It is not legitimate
to substitute collision probability for M or omit small-intensity modes.
The certificate only bounds absolute output-law differences, not relative rare
success, optimization superiority or classical hardness.

Source: `theory/phase3_density_certificate.md`,
`src/photonic_balanced_partitioning/photonic/density_certificate.py`,
`experiments/phase3_density_probe.py`. The proof is coordinator-derived;
the exact theorem at75e5831 has a fresh independent review in
`reports/PHASE3_DENSITY_INDEPENDENT_REVIEW.md` (4420e17). Novelty remains OPEN.
The subsequent floating implementation fix77a8588 removes observed cancellation;
its outputs remain FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED. Its Gram/cycle
dependency has previous independent reviews. Do not present new simulation
assertions as a proof or interval certification.

Preregistered finite scope:

- Full Fock distributions: m=4,6,8,10,12, k=m/2; three seeds; five strengths;
  global-output mixing and exactly flat-intensity fixed-projector families.
- Ten selected full Fock comparisons against Perceval, fixed before execution.
- Seven analytic m4/k2 sharpness cases.
- Six balanced dilute/spectator counterexamples, using exact active-block
  factorization; these must not receive a false nontrivial certificate.
- m=32,64,128: 36 certificate calculations only. No full distribution is
  computed or validated at these sizes; no sampling-hardness inference follows.
- All cases retained. There is no optimizer or favorable seed selection.
- Primary seed offset 0; independent replication offset 100000. Same case grid.
- Zero physical shots, no noise campaign, no QPU, no manuscript edits.

Falsifier: a probability normalization, moment identity, source convention or
TV inequality fails beyond the script's stated tolerance. Such failure makes
the finite experiment unsuccessful; retain the failure and inspect the raw
command. Do not repair a failed run's output in place.

Each simulation has a 300-second command budget. Native Qwen roles run
sequentially on the one local model, with four turns each and no stall retries.
One workflow has at most nine dispatches (seven unique roles plus replication
and final lead). Total launch is capped at 1500 seconds. Hypothesis verdicts
SUPPORTED/REJECTED/INCONCLUSIVE refer only to the stated finite assertion;
scientific acceptance, proof correctness, novelty and paper/QPU gates belong
to Astra after reading actual child transcripts, raw data and reports.
