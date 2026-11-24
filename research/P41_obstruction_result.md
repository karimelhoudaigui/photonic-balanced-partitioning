# P41/R3 handoff and evidence disposition

Worker branch research/p41-obstruction, base f09c7ec82b2fe23395116e21bd56614f3739107c.
All contributions are new P41-obstruction paths; no pre-existing science,
paper, shared register or hardware file was edited. No QPU/account call.

## Results actually obtained

- The proposed all-convex-occupation no-go is **refuted** by an exact connected
  m4,k2 example. Its penalized L1 objective has CF ground states without C*,
  yet E_B-E_D=-3/16. The optical law is the old Walsh law: this is a new
  observable/classification check, not a new optimizer benchmark.
- General two-photon cost dominance has an exact conditional-PSD kernel
  characterization. For L1+muM it becomes mu>=2lambda_max(A|1-perp).
  Analytic derivation/self-review only; independent proof audit still needed.
- Exact Fraction run verifies384 fixed cases plus64 graph classifications;
  all10 Fock outcomes retained, manifest valid/completed, sourcefe02f17 clean,
  wall0.142664s. The finite assertion is verified, not a general-k theorem.
- Two-photon raw proposals cannot strictly improve every nonself CF move
  against same-U distinguishable routing. This is a pointwise-transition
  obstruction, not a mixing-time or independently reoptimized comparison.
- Parent's R_k total-variation regularizer was reconstructed, with sharp
  2M<=R_k<=2(k-1)M and CF penalty certificate. A separate k3 identity gives
  Delta E R=4S2-30T>=(2/3)S2, sharp at a tritter. These are self-reviewed.
- The loss/oracle envelope and source-overhead entropy certificate are
  independently reconstructed and reviewed, with endpoint/cost clarifications
  applied ata432ca5. This closes stated loss/cost regimes conditionally, not
  ideal optimization, arbitrary encodings or a whole adaptive hybrid.
- A Gram-free classical routing/fallback comparator satisfiesQ(T)>=P(T)/k!
  for CF outputs under the normalized distinct-input model. Its loss conditions
  are derived but still await an independent audit.

## Independent loss-proof provenance

Sibling p41_adaptive first committed an independent reconstruction fd479d8
before reading the author proof. Its first audit ff1d067 identified eta=0 and
fixed-cost clarifications. The author applied both in a432ca5. The reviewer
then committed4506150, theory/P41_adaptive_loss_review_a432ca5.md, verdict
**proved as written** under the explicit scopes. The reviewer ran no numerical
experiment during this audit. It had shared high-level project context but
did not author the loss proof and did not read it before reconstructing the
critical steps. Review files live on the sibling branch, not copied here.

## Prior-art findings and remaining obligations

Hayashi etal.0710.1056v2 §III.2 Eqs(33)-(40) directly supplies the old Dicke
overlap coefficient k!/k^k and phase-twirling operator mechanism. The ideal
continuous-phase iid pointwise optical proxy is a formal corollary after
first-quantization translation. Do not label that coefficient or principle new.
The source relation also covers pure product internal states via the enlarged
single-particle space. Separate operational/WOR/loss/cost composition remains
subject to its own audit and novelty assessment.

Oh2025's per-layer quarter-loss simulation result and Solomons2023's variable
squeezing/no-postselection comparisons were checked and separated from the
source-capped end-to-end success certificate. No global novelty conclusion.

Useful next work: independent audit of L1/kernel and Gram-free comparator;
exact two-mode PNR marginal evaluation for the many-photon L1/R objective;
held-out many-body search with strongly charged classical correlated controls;
or a route that changes the loss/cost/encoding hypotheses. Do not repeat a
fixed-size block or substitute R(E[n]) for E[R(n)].

The user's original P41 target is **OPEN**. No interference-dependent
optimization advantage, manuscript integration or hardware gate is claimed.
