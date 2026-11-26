# P99 bounded primary-source attribution: optical and Markov ordering

Checked 2026-11-26. **The Markov ordering consequences are established
theory. The exact combined optical P99 statement has unverified external
priority, not a novelty certificate.** This literature note neither changes
the self-contained proof nor supplies its pending independent proof verdict.
Target: research/P99_WEAK_PASSIVE_REOPTIMIZED_D_CARD.md, 198 lines,
`a8e80a10d5ae9e1f54e371c613240276a79b40f4`, SHA256
`8543039fc6346a8beb6f8fcb626863067c13b3e43a5e8f47dd03b168bf8e8bb1`.

Question: which arrows are already known when symmetric unconditioned class
proposals obey Q_D(2t)(x,y)>Q_B(t)(x,y), x!=y, with a common finite-alpha
Metropolis target? Optical premise: global real symmetric dense H, known
CF source, uniform random orientation of an unoriented bisection, losses/
collisions as self-loops, K<=12 and an admissible doubled parameter.

## Acquisition and bounded strategies

Literature-check/cache instructions were reused. Read-only filename/topic
checks found no dedicated local Peskun/Tierney record or literature/records
cache at root/this worktree. The existing P99 proof was consulted first.
Eight English queries were split between strategy A (Peskun/Tierney,
Dirichlet/killed inverse and stationary hitting) and strategy B (bosonic
permanent factors, weak-coupling distinguishable controls). Primary texts
below were read at the indicated theorem/formula and nearby proof passages.
No new PDF was retained locally; browser PDF extraction is not a local
byte-authentication claim. New retained-source SHA256: NONE. No large cache,
download, checkout or research-state ledger was created.

Query scope included `Peskun 1973 optimum Monte Carlo sampling using Markov
chains Tierney 1998 comparison Metropolis Hastings kernels pdf`, `reversible
Markov chains mean hitting time stationary distribution variational principle
Dirichlet killed inverse`, `Tierney 1998 A note Metropolis pdf theorem`,
`boson sampling permanent distinguishable n! Cauchy`, `boson sampling weak
coupling distinguishable transition probabilities`, `bosons Cauchy N!
permanent distinguishable probability`, `boson distinguishable permanent
Cauchy-Schwarz factorial`, and `bosonic transition probability enhancement
bound N! Tichy distinguishable`. Secondary hits served discovery only.

## S1: Peskun's original finite-state ordering

P. H. Peskun, *Optimum Monte-Carlo sampling using Markov chains*,
Biometrika 60(3),607–612 (1973), DOI10.1093/biomet/60.3.607.
[Original article scan](https://hedibert.org/wp-content/uploads/2013/12/1973Peskun.pdf),
journal p.609, Theorem 2.1.1: irreducible transition matrices reversible for
the SAME stationary distribution, ordered entrywise off the diagonal, have
ordered asymptotic variances for sample means of every state function.
Theorem 2.2.1 then optimizes acceptance for a fixed proposal. These are
distinct claims: P99 compares two proposals with a common acceptance rule,
so the general ordering theorem is the relevant one. Original-page identity
and statement were authenticated from the scan; the OUP page/DOI fetch
failed, and no false publisher-full-text access is claimed.
Overlap: known after translation, with P1=P_D and P2=P_B. It does not assert
ordering of optimizer best-of-T quality, arbitrary starts or physical costs.

## S2: Tierney's operator and asymptotic-variance formulation

Luke Tierney, *A note on Metropolis-Hastings kernels for general state spaces*,
Ann. Appl. Probab.8(1),1–9 (February1998),
[DOI/publisher record](https://doi.org/10.1214/aoap/1027961031),
[published article scan](https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TransdimMCMC/TierneyAAP1998.pdf).
Section3, pp.4–6, defines off-diagonal domination. Lemma3 states that
P2-P1 is positive as a quadratic form when P1 dominates P2; with common
reversibility this is exactly P99's Dirichlet form order for I-P.
Theorem4 extends the asymptotic-variance result to general state spaces,
for centered L2(pi) functions and stationary initialization; the limit may
be infinite. Finite P99 falls inside this classical result.

The paragraph on p.7 explicitly says higher-lag correlations/finite-sample
variances need not be ordered. On p.8 the mixture-proposal discussion warns
that fewer iterations can cost more CPU per iteration. Thus neither a
finite-horizon performance claim nor an equal-time claim follows from
Peskun ordering. The publisher landing page exposes only an iframe here;
the actual theorem extraction used the academic-hosted original scan.
Authentication/extraction/application: verified. Overlap: known after translation.

## S3: Rayleigh and stationary hitting-time variational principles

David Aldous and James Allen Fill, *Reversible Markov Chains and Random
Walks on Graphs*, author-hosted unfinished monograph, Chapter3 headed
10-September-2002. [Section3.6](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S6.html),
equations(3.74)–(3.75), Theorem3.25: the Dirichlet form determines
1-lambda2 by the usual Rayleigh quotient. This is the right spectral gap,
not the absolute-eigenvalue gap without an additional nonnegative-spectrum
condition. P99's spectral step is established theory.
[Section3.7.2](https://www.stat.berkeley.edu/~aldous/RWG/Book_Ralph/Ch3.S7.html),
Proposition3.41 explicitly characterizes E_pi T_A by a supremum of inverse
Dirichlet energies with g=1 on A and pi(g)=0, and gives the extremizing
function 1-E_x T_A/E_pi T_A. It treats a set A, not only one target vertex.

Dictionary: weights w_xy=pi(x)P(x,y); use the same pi in both chains.
Dirichlet domination immediately decreases this stationary mean. Divide by
pi(A^c) to obtain P99's conditional-stationary-outside mean, since T_A=0
on A. The killed inverse/square-completion proof in P99 is an equivalent
finite-dimensional formulation, not a new hitting-time comparison principle.
Overlap: known after translation/formal corollary not stated in that notation.
No arbitrary-start or hitting-time-distribution order is imported.

## S4: optical amplitudes and factorial enhancement

Nicolò Spagnolo et al., *General rules for bosonic bunching in multimode
interferometers*, [1305.3188v2](https://arxiv.org/abs/1305.3188v2),
26-Sep-2013; Phys. Rev. Lett.111,130503, DOI10.1103/PhysRevLett.111.130503.
[Primary text](https://arxiv.org/html/1305.3188v2), equations(2)–(3), gives
normalized bosonic permanent amplitudes and distinguishable intensity
permanents. For CF inputs/outputs, all occupation factorials are one.
Applying elementary Cauchy–Schwarz to the r! permutation products gives
|per M|^2<=r! per|M|^2 for ANY complex r-by-r M. This is a formal algebraic
corollary, not a new permanent inequality; no historical-first claim is made.
The paper's Theorem2/equation(7) is instead an exact n! enhancement for
FULL bunching in ONE output mode (CF input). It is adjacent, not a theorem
about CF moves between graph bisections. Its Haar birthday theorem is unused.

## Exact combined arrow and cost boundary

No inspected primary passage supplies the entire construction: orientation
average on [S], r=min swaps, two-versus-four minimal routes, positive dense
intensity leading coefficients, 4^r>r! through r<=6, and a UNIFORM explicit
small-t window comparing D(2t) against B(t), with common Metropolis cost.
External attribution of that particular composition remains unverified.
The weak-coupling query did not establish an earlier reoptimized-parameter
ordering theorem; that limited search failure is not evidence of novelty.
The factorial bound alone cannot compare full kernels at unequal parameters;
the routing expansion/remainder, symmetry and admitted2t remain internal
load-bearing P99 steps, subject to its separate proof audit.

Even if those premises pass, the downstream Dirichlet, Rayleigh, stationary
hitting and asymptotic-variance ordering is classical theory above. It does
not compare graph-query counts, compilation, doubled optical duration, CPU
or total wall time. Orientation/source preparation and every raw loss,
collision and scored candidate remain paid. Nothing here supplies a
hardware certificate, all-start/annealing optimizer veto or positive result.
This is a same-searcher two-strategy bounded check, not exhaustive forward
citations or a global quantum-MCMC survey. Novelty and positive goal OPEN.
Only this note changed; no import/AST/scientific execution/RNG/graph/native/test/runner/QPU/paper/push/checkout/delegation or frozen P99 edit occurred.
