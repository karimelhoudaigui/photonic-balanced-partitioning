# P46 encoding implementation — exact-hash pre-run review

Verdict: **STATIC ALIGNMENT PASS after the pre-outcome Gaussian correction**,
for the stated DEVELOPMENT VETO only. No blocking physics, optimum leakage,
PIT conditioning or budget defect was found in the corrected frozen code.
This is AUDITED, NOT EXECUTED by this reviewer: no P46 test, sample, development
graph, matrix evolution or result file was generated in this lane.

## Provenance and independence boundary

Original code read: `7c1c36c3b14f4669caee7a9a4c23c295bbb374b2`, script SHA256
`c99780ea7a13dd19f4f89dd1027d0868fb593ed47ccd827d146af727abef4167`.
Reviewed correction: `b1535f8a7bbcf3e2f8b09bafdf59f87bab881d1d`, final script SHA256
`721cc9f3ee6ba1d604ae29130fb25d092a21bcc756e8d4b4a42e6238d47c315c`.

| Frozen path at b1535f8 | Git blob |
|---|---|
| research/P46_bulk_pit_probe.py | 749abd2b19bb76e7f3d940652c55bb36dec8e155 |
| research/P46_bulk_pit_spec.json | 2e8eb63d0e448fabaff069d60fad3baef6b8f53e |
| research/P46_bulk_pit_contract.md | d975566ec2ae369f0aac24f53c1bba0fb2851921 |
| research/P46_bulk_pit_execution_contract.json | 8ffebf28d0e9a384895004de4b4962b14ea1127e |
| tests/test_p46_bulk_pit.py | 3128aed64aa9795212fc47887bef93cb5e55a3a8 |

The reviewer reconstructed the marginal/PIT formulas BEFORE reading author
code, frozen `ed5b1e5`; a hollow absolute-conditioning refinement was frozen
`c461270` after reading the statement card `a6d7a27`, still before code. The
physics-author proof has not been consulted here. Shared broad research context
is disclosed. The reviewer also authored the REUSED P45 decoder/KL helper, so
this is not independent authorship of that component or independent physical
optimizer replication. New P46 code was separately authored in the encoding lane.
The imported P43/P45 helper files are unchanged relative to19a9902.

The encoding lane reports nine tests passed on7c1 and ten on the corrected
b1535f8, with the first receipt preserved and the second receipt at642d9f7.
These are AUTHOR execution observations, not runs independently reproduced in
this lane. The tests themselves were read, including explicit-permutation Fock
and labelled-particle references rather than the production PMF routine.

## Physics, PMFs and PIT checked

1. **Block and graph orientation.** The physical old-to-new block is -i*sqrt(p)
   W*, matching Delta's inside-row/outside-column convention. SVD polar produces
   W; U is explicitly checked for unitarity. Source inputs are the fixed old
   vertices, one photon each. Random inside/outside orders and the b4 photon
   permutation are frozen per graph; no optimum solver/mask/value is accessed.
   Zero/weak centered response is kept and its diagnostics are not filters.
2. **Actual count laws.** B and b4 use the immutable local serial CC sampler;
   D is independent categorical routing. All full-K observations are retained,
   then decoded feasibly without a CF filter. Production has no full-Fock
   enumeration, QPU client or remote submission. The hand-sized test reference
   includes collision factorial denominators and normalizes the complete law.
3. **One-mode probabilities.** Decimal80 computes e_r and the B factorial
   coefficient r!; D omits it. Species PMFs convolve per-group B laws using the
   actual species-order/input-index dictionary, not an assumed sorted grouping.
   The old block is explicitly replaced by its analytic Bernoulli(1-p) PMF for
   all count models. This agrees with the independently reconstructed formulas.
4. **Randomization.** Counts, continuous fields and per-coordinate PIT jitters
   use distinct seed roles. Jitter is independently drawn per mode and shot.
   No same-batch empirical ranks or conditional-on-observed-A calibration is
   used for B/D/b4. The declared PIT uses unconditional current-source tables.
5. **Conditional phase.** A is independently Bernoulli(p); old counts are1-A.
   With l=|A|>0, new counts are multinomial(l,|(-iW*)[:,A]z|^2/l), with one
   shared four-root phase vector per draw, proper column restriction and
   normalization check. l=0 gives old all1/new all0 without division by zero.
   It is not physical eta=0 vacuum. Calibration averages independent A draws
   GLOBALLY, not a CDF conditional on a production A. Old marginals stay analytic.
6. **Empirical qualification.** Only this control's new-mode PMFs use4096
   independent classical calibration draws per network. Full histograms/seeds,
   DKW and one-sided-subset Hoeffding TV radii, cost and approximate/joint-error
   qualifications are stored. Calibration and production namespaces differ.
   The two concentration expressions are correct as separate confidence bounds;
   do not infer a new simultaneous confidence claim for their conjunction
   without accounting for both families. They do not bound joint copula error.
7. **Gaussian correction resolved.** Original7c1 used the target covariance
   diagonal after sampling a clipped factor. Corrected b1535f8 calibrates Phi
   with sum_j factor_ij^2, the ACTUAL variance, and keeps target variance and
   factor/covariance discrepancies separately. A zero-variance coordinate uses
   fresh uniform jitter. The new finite test guards the original discrepancy.
   Neither Gaussian nor uniform controls claim to match every PIT pair/copula.

## Common discoveries, score costs and execution closure

- Source best-swap scans and all K^2 final-source swap candidates are scored,
  logged and credited. Actual swap cuts verify the Delta formula and orientation.
  A useful candidate discovered in matrix preparation cannot be attributed to B.
- Zero-field/pure-greedy and all discrete-model midpoint-vacuum completions enter
  the PUBLIC Cref before samples. The physical source S0 is not secretly changed.
  All PMFs/calibration work is common frontend work because it also supplies
  these public candidate discoveries; it is not free model-specific advice.
- All six models share q=ceil(K/2), lambda0/1 and the exact same greedy decoder.
  Each receives4*2*8*4=256 attempts/proposals, selects its OWN global setting and
  keeps every tuning discovery. Each proposal pays94 marginal+cut units at n24
  or127 at n28; no hidden unscored descent follows it.
- Each of four classical baselines receives3008 or4064 feasible cut queries per
  graph/replicate. The matching control uses shared Delta in a Hungarian solve,
  then scores the REAL balanced collective move; summed single deltas are not
  falsely substituted for its actual cut. Solver time and all queried cuts are
  retained. A retrospective best-baseline envelope is not a free portfolio.
- Conditional calibration costs65536 CLASSICAL draws over16 networks, no photon
  shots. B/D/b4 photon counts, field samples, marginal versus full cut scores,
  shared preprocessing and online times have distinct ledgers. Marginal and
  complete-cut units do not have identical CPU cost. Observed simulator-time
  prefixes exclude the COMMON frontend on both sides; they are not measured
  hardware budgets or an independently validated speedup.
- Main and preflight contracts list nine and ten input artifacts respectively.
  Imports are P43/P45 helpers, pinned packages and the declared source/spec;
  the small-Fock test is self-contained. Runner MUST create run_001 while the
  child creates run_001/data, since child mkdir uses exist_ok=False. Declare
  summary, gzip raw and all four contexts BELOW data. Inputs/outputs must remain
  unchanged and all source commits/refs preserved with their actual revisions.
- Gzip uses deterministic mtime0, small streaming buffers and a closed footer
  on normal completion. A killed run may leave a TRUNCATED gzip prefix; retain
  its bytes and classify resource-inconclusive, not a missing scientific result.
  The script checks scientific output size after every graph and at the end.
  CPU/wall/thread/log limits require actual bounded-runner flags, not metadata.

## Remaining interpretation limits — not blockers for this veto

Decimal80 operates on numerical U intensities, then float tables are minimally
clipped/normalized; no relative/interval PMF certificate is claimed. The hollow
absolute inversion bound2 supports good absolute conditioning but does not
justify silent rare-atom claims. Raw PMFs/counts/jitters allow reconstruction
of clipping effects, empirical zero-mass bins and exact field ties. If an
interesting B/control difference appears, explicitly audit these events and
calibration sensitivity before treating it as a mechanism. A sparse empirical
bin can collapse observations to a CDF boundary; this is not exact uniformity.

Carried-label covariance is tested. Robustness to fresh independent logical
inside/outside orders or graph embeddings is a further experiment, since a
fixed Fourier reference is tied to that logical order. Neither this pilot nor
a passed algebraic covariance check establishes the user's full relabel gate.
Full existing tests remain required before integration. Physical loss eta<1
is not implemented in this ideal pilot; delta0 PMF/PIT mathematics is not a
loss-robust optimization result or a calibrated Lucy channel.

The static PASS authorizes only the one coordinator-approved bounded veto after
its corrected preflight. It accepts no positive scientific discovery, held-out
validation, novelty, quantum advantage, hardware circuit or manuscript change.
