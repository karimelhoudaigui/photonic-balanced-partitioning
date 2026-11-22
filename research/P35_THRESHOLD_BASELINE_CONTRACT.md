# P35 known classical threshold-marginal baseline

Owner: coordinator; checkpointde77a14, 2026-11-22. The method is known, per
theory/phase3_threshold_lowrank.md and research/phase3_lowrank_sources.md.
The purpose is an executable fair classical control for authentic threshold-QUBO
objectives, not a new permanent algorithm or a quantum-benefit claim.

Question: can a pinned exact-arithmetic rank-one/rank-two implementation match
complete Fock/Perceval threshold moments and the original QUBO expectation,
including the authentic distinct-input N=m source, without full-law enumeration
in its own calculation? The proof already supplies a polynomial method. The
new obligation is correct implementation and explicitly charged arithmetic.

Implement the coefficient DP of equations2/3/5 in the existing theory note.
For selected output rows A, at most two, its input is V=U[A,C], with one photon
per DISTINCT occupied input in C. Compute per(I-V*V), not its modulus square,
by the diagonal-coefficient factorial extraction. Keep off-diagonal polynomial
states and both complex components. N=0 and empty A return one. A single-row
two-photon HOM case must give vacuum probability1/2, not1/4.

Prefer exact Gaussian-rational arithmetic with a common input denominator and
integer coefficients, so cancellation cannot be concealed by clipping. Exact
evaluation of a supplied binary float matrix is only exact for those encoded
entries; it is not automatically exact for an unknown physical unitary.
Include exactly rational orthogonal frames in the validation to obtain genuine
exact probability checks. Optional floating wrappers must state input/error
semantics. Do not claim relative accuracy or interval certification from floats.

Threshold means: E[x_i]=1-p0(i). Pair moments:
E[x_i x_j]=1-p0(i)-p0(j)+p0(i,j). For symmetric real Q, compute
E[x^TQx]=sum_i Q_ii E[x_i]+2sum_(i<j) Q_ij E[x_ix_j]. Include all collisions;
no feasibility conditioning, oracle optimum, source-selection freebie or loss
postselection. This component does not generate full output samples or modes.

Fixed first validation: vacuum/unary/HOM exact controls; rational real orthogonal
four-mode frames with N2 and N4; a six-mode N3 case; complex unitary cases
against Perceval, at most12 circuits, seeds20261122..20261133. Compare full
distributions only at these declared small sizes. Retain raw moments/objective,
integer operation/state counters, input hashes and all failures. No optimizer,
no physical shots. Code tests must cross independent complete laws or analytic
controls, rather than mirror the DP recurrence.

Cap each scientific run at120seconds, one CPU thread. No large benchmark or
new local model. Before scaling, inspect state growth and exact integer sizes.
The polynomial bit bound is already stated in the theory note; wall-clock or
hardware acceleration does not follow from it. A completed baseline is useful
even if it makes the proposed photonic mechanism less compelling.

Next integration target, not part of this first component: full authentic
ObliQ VQC/source/decoder comparison with every classical/physical cost charged.
Known marginal evaluation can supply the ideal mean objective and prefixes;
it does not reproduce finite-shot training noise or modal sampled candidates.
