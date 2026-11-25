# P55 finite DEV: pre-data implementation clarifications

25-Nov-2026. These changes were required by independent physics/supervisor
review BEFORE the source/spec/tests/contracts freeze and before ANY import,
test, DEV graph, count or phase draw. No numerical outcome motivated them.
The original216-line proposal2f3569b remains in history.

1. CTMC receives the NAMED argument `horizon_tau` directly. No squaring or use
   of the old P45 factory's t parameter. The only source adaptation is N
   initial ones. A prospective4096-event cap saves counts, elapsed time,
   rate_total, proposed next-event time and horizon in raw/failure evidence
   and `failure.json`, then makes the whole pilot INCONCLUSIVE. No truncated
   chain is decoded or replaced. A zero-event fixture with proposed time3
   and horizon_tau2 explicitly detects accidental squaring.
2. Each policy's selection loss uses ALL of THAT policy's4 or8 training cuts
   per graph, with equal graph weight and exact Fraction arithmetic. It does
   not average the24 draws across different policies or use their minima.
   Selections are archived after all training and before any fresh evaluation.
3. The r20 PGF qualification has exact identity, uniform q_i=1/20 and
   mixed q_i=i/210 for i1..20. The mixed expected elementary coefficients are
   independently supplied by unsigned Stirling numbers of the first kind,
   rather than the production Decimal elementary recursion. Keep Decimal80
   and the previously frozen3e-12 input/PMF/CDF guards; no post-data fallback.
4. Full-source RAW row masses must obey |raw_mu-1|<=3e-12 on BOTH sides.
   The P48 row helper repairs tiny excesses only and NEVER scales deficits up.
   A larger deficit is a retained numerical failure, not hidden vacuum/loss.
   Save all20 raw means and both U*U and UU* Gram max-entry residuals per U.
5. A deadline-eligible paid FAST initialization may refute B without a scan.
   FOLLOW_UP_ONLY additionally requires each fixed search's first full scan
   before its CPU deadline, the helper's eligibility and no early cap. Keep
   separate `prefix_eligible_for_veto` and `comparison_acceptance_eligible`.
   Each allowance is explicitly max(0,T_B_CLASSICAL_WALL-adapter_CPU), with
   actual adapter CPU charged. Optical latency is assumed zero, never measured.

The screen is hierarchical, always with `positive_accepted=False`:

- Incomplete/missing model draws or a retained numerical/resource failure:
  INCONCLUSIVE. Missing/duplicate fixed FAST calls also remain INCONCLUSIVE.
- One fixed FAST algorithm's valid paid prefix equals/beats B's ALL-paid
  train+fresh minimum on BOTH graphs: REJECT, even with no completed scan.
- Otherwise B's fresh equal-graph mean is not STRICTLY smaller than D's OR
  inclusion's independently selected fresh equal-graph mean: REJECT.
- Otherwise FOLLOW_UP_ONLY requires B's fresh mean strictly smaller than
  EACH of the five count controls on EACH graph, and B's ALL-paid minimum
  strictly smaller than EACH fixed FAST algorithm on BOTH graphs. Every FAST
  must satisfy the stronger acceptance/first-scan condition.
- Every other favorable/mixed or insufficient-FAST combination: INCONCLUSIVE.

A FOLLOW_UP_ONLY label is not an accepted positive, significance result,
population claim or authorization to open held-out cases. A new reviewed
design is needed before any further experiment, replication or QPU step.

All80 B draws,480 total draws, the two graph seeds, policy time grids,
attempt/photon accounting, all-count exact decoder and frozen output/cost
caps are unchanged. Other models' work never funds B's FAST allowance.
