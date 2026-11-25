# P49 candidate if P48 fails — occupied-basis mixing, not a proxy-cost step

Prospective analytic note only. No P49 code, numerical evaluation, tuning,
graph, parameter search, QPU call or manuscript change is authorized here.

Let E be P48's fixed marked graph eigenbasis, with r occupied columns. Use
V=E R(theta,phi), where R has two staggered nearest-neighbor Givens layers on
these columns, including all r modes when r is odd. theta0 gives P48. For one
pair choose the convention

    G=[[cos(theta),-exp(i phi)sin(theta)],
       [exp(-i phi)sin(theta),cos(theta)]].

On |11> this gives cos(2theta)|11> plus
sin(2theta)[-exp(i phi)|20>+exp(-i phi)|02>]/sqrt(2). At theta=pi/4 the
coincidence amplitude vanishes: an elementary HOM/NOON pair in the SPECTRAL
basis. The subsequent dense E acts on all photons; this is not a claim that
vertex outputs form independent pairs or that this familiar physics is new.

**Gauge first.** Reuse the existing P48 pivot convention BEFORE multiplying
by R: pick a maximum-magnitude component in each eigenvector, resolve ties
within1e-12 by the carried vertex priority, and multiply the column by the
conjugate pivot phase to make that entry positive. Carry marks and priority
under relabeling. Freeze eigenvalue order/gap and pivot-tie rules; retain
ambiguous numerical cases. E diag(phases) R generally prepares a DIFFERENT
state from E R, so arbitrary eigensolver signs are not harmless after mixing.
Do not select a favorable gauge/priority after observing scores.

The projector P=VV*=EE* and mean mu_i=P_ii remain IDENTICAL for every R.
But q_ia=|V_ia|^2 changes, hence B/D covariance and higher count cumulants can
change. For example Cov_B=diag(mu)+|P|^2-2qq^T. A possible gain is therefore
in SOURCE-BASIS-dependent correlations, not a new subspace or one-body mean.
The fixed-source raw PSD-quadratic obstruction still applies. It does not
automatically order the nonlinear feasible decoder's outcomes.

Train on the mean of C(decoded count) over ALL raw shots, with every collision
decoded and every cost charged. Do not use C*, optimal masks, known solutions,
CF conditioning or a cut proxy in place of those actual feasible scores.
Every training estimate, parameter choice and scored candidate is retained.
A lower training mean alone does not prove better best-so-far search: evaluate
that separately under the future resource/held-out/replication gates.

Essential falsifiers and nulls:

- D, phase and Gaussian controls must optimize their OWN R/decoder policies
  under the same TOTAL budget. Their laws also change with q; comparison to
  theta0 alone would handicap them. Use efficient CPU controls, not old logged
  cut counters or simulator time as hardware time.
- Spherical-coherent sampling and its marginal CDF are EXACTLY invariant under
  R, since a Haar complex vector is invariant under right unitary rotation.
  Allow it to use saved redundant tuning work for additional feasible search.
- Monomial R only permutes/phases the all-one CF input and adds no new count
  law. With real E, conjugating all controlled phases also preserves counts.
  These are declared nulls/aliases, not independent mechanisms.
- Compare bounded species with fixed random AND gate-aligned groups, and a
  dephased pair-source/control if it can be physically specified and costed.
  Reproducing a gain with small correlated blocks vetoes a growing-order claim.
  Easy pair preparation alone is insufficient; conversely constant-depth R
  alone does not classically simulate the later dense E measurement.
- Do not average R over a Haar source basis and call the averaged raw effect
  quantum: that recovers the spherical null. A learned R must be frozen before
  fresh data. All classical phase/CDF/eigensolver work remains accessible to
  controls and cannot be attributed to interference.

Contribution to test: whether a graph-trained, gauge-fixed source-basis change
improves real feasible search beyond those nulls, with P fixed. No such benefit
is predicted or established here. P48 stays untouched; a new claim card and
independent review are required before implementation or any numerical test.

Bounded literature context, abstracts ONLY checked25-Nov-2026:
[Cazalis et al.,2412.14783v1](https://arxiv.org/abs/2412.14783v1) already proposes
variational GBS/threshold/CVaR, including a classically accessible low-degree
mean-cost regime and a proof of concept against guessing. It does not validate
this CF/spectral/PIT mechanism. [Lopena et al.,2607.19279v1](https://arxiv.org/abs/2607.19279v1)
addresses financial clustering. Neither abstract settles our contribution or
its novelty. Merely adding the word variational is not a new scientific result;
global novelty and full proof/source comparisons remain OPEN.
