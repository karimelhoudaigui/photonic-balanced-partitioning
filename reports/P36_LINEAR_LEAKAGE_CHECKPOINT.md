# P36: finite checks pass; the general linear bound remains open

Target: TV(p_b,p_d)<=min(1,delta), where delta is dominant-support leakage.
This is a conjectural strengthening of the independently proved P33 envelope.
No optimization, manuscript, hardware or quantum-advantage result follows.

The frozen256-circuit protocol bfa5a22 was actually executed. The first launch
failed before mathematics because the runner had already created the requested
output directory. Its manifest/stderr remain in `run/`. Corrected argv placed
data in a fresh `run_002/data/`; source and case grid were unchanged. This
completed in1.834seconds, with all256 full occupation laws retained, zero
physical shots, maximum normalization error8.993e-15, and no excess over the
proposed bound beyond the1e-9 falsifier. The largest observed excess was
-1.483e-7. All cases, including trivial delta>=1 cases, are retained.

`experiments/check_linear_leakage_grid.py` independently recomputes complete
bases, normalizations, row leakage and TV from the saved unitaries/probabilities.
Twelve predefined circuits are checked against Perceval; sixteen collective
rank-one cases also satisfy independent closed permanent formulas for the
all-one occupation. Its completed review manifest is in
`experiments/P36_linear_leakage/review/`. These checks do not turn a finite grid
into a proof. All probability calculations are floating estimates, not interval
enclosures or sampling confidence statements.

Two analytic checkpoints were proposed in partial physics messages and
reconstructed in full by the coordinator after that agent hit its quota:

- For k2, N1 plus a binary-fidelity/Cauchy inequality gives the exact sharp
  bound TV<=delta-delta²/2. The retained pair-rotation family attains it. This
  proof uses standard ingredients and carries no new algorithmic-benefit claim.
- The attempted auxiliary inequality per(B)-1<=2delta is false, even for a
  physical rank-one three-mode unitary with delta1/17. The excess is exactly
  265/9826, although the actual full-law TV remains below delta. Adding three
  idle vacuum modes embeds the same witness in a balanced m6,k3 source. Thus
  the positive-permanent shortcut cannot settle general P36.

The complete arguments are `theory/phase3_linear_leakage_attempt.md`; their
exact rational witness and seven sharp-family checks are in
`experiments/P36_analytic_attempt/root_check/`, completed with valid v2 evidence.
This is a coordinator reconstruction, not a completed fresh independent proof
audit. No phase or full-Fock collision term was removed to obtain these results.

A retained literature-reviewer draft at
`research/phase3_linear_leakage_sources.md` compares which-way/internal-state
and spatial-localization bounds with the exact target. Its turn was quota
interrupted before commit. It identifies relevant but different statements;
no authenticated exact source theorem or counterexample closes general P36.
Source absence is not a novelty finding.

Decision: KEEP finite checks, exact k2 subcase and proof-route obstruction.
General k>=3 remains OPEN. A continuation must either control occupation
measurement while retaining phase cancellations, or produce a new analytic
counterexample. Repeating this unchanged numerical grid is not a proof route.
