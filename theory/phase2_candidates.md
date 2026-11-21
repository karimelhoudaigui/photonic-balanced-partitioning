# Phase 2 research candidates: encoding resources and penalty washout

Base checkpoint: `99f82e367ef079e4d52f763d615476698727b739`.
Date: 2026-11-20. These are research routes, not manuscript claims.
Mathematics below is self-derived and self-reviewed; coordinator cross-review
and numerical falsification remain required. Novelty of every candidate is OPEN.

## Route P2-A — Choose photon budget and decoder jointly for bisection

Question: under loss and a fixed total injected-photon budget, which photon
number `N` and decoder give the highest probability of returning a bisection
of specified quality after charging training and classical postprocessing?
Compare minimal-photon CF decoding (`N=k=m/2`) with threshold decoding at
larger `N`, and threshold-plus-flips as an authentic BBS-style penalty model.

The Haar click count

\[
f_N(m,k)=\frac{\binom mk\binom{N-1}{k-1}}{\binom{m+N-1}{N}}
\]

is **known**, explicitly in Bouland et al.,
[2312.00286v2](https://arxiv.org/html/2312.00286v2), Lemma 1, Eq. (6).
It is a validation input, not the proposed contribution. Its ratio

\[
\frac{f_{N+1}(m,k)}{f_N(m,k)}
=\frac{N(N+1)}{(N-k+1)(m+N)}
\]

shows that for `m=2k`, `k>=2`, the unconstrained positive-integer N maximizers
are `N=m-2` and `N=m-1` (a plateau); thus `N=m` is not exactly optimal even
for Haar feasibility. This statement optimizes feasible *probability*, not
probability per photon or optimized circuit performance. The counting proof
also permits general Fock inputs, but hardware restricted to one photon per
mode requires `N<=m`.

For nonuniform source or detector efficiencies, loss cannot be represented
by an undifferentiated postselection multiplier. Uniform independent loss
allows a survivor mixture; source-specific loss needs the actual input-state
mixture and appropriate circuit model. An all-photon detection gate and a
weight-k threshold gate are different physical protocols. The coordinator
owns the detailed loss laws and experiments in separate files.

Cheapest discriminating experiment: fixed graph/seed list, `m=4,6,8`, sweep
`N=k,...,m`, use both Haar and optimum-blind trained meshes, and report
`P_valid`, `P_opt|valid`, physical `P_success`, attempts and injected photons.
Track source preparation assumptions separately from detector acceptance.
If the larger feasible fraction has no benefit for good bisections after
charging resources, preserve that failure. The experiment must include
direct random balanced and swap-search references, not only penalty methods.

Possible QPU question, after simulation gates: does the calibrated hardware
ranking of minimal-photon versus redundant-threshold encodings match a
preregistered photon-budget/loss prediction on locked graph instances?
This is an encoding-and-optimization question, not merely a bunching witness.
No QPU claim follows from the ideal Haar count alone.

## Route P2-B — Strong penalties erase graph information in the ObliQ anchor

This route targets a concrete algorithmic mechanism in the authenticated
original code, rather than claiming that all penalties or all optical
optimization fail. A graph-aware classical decoder can still recover graph
information from its own access to the problem; that possibility is charged
and ablated, not excluded by the theorem.

### Candidate proposition: canonical balanced penalty normalization

Fix an even `m>=4`, a noncomplete undirected nonnegative weighted graph,
and its weights `w_ij`, including absent edges as zero. Let `k=m/2`,
`d_i=sum_j w_ij`, `d_min=min_i d_i`, `d_max=max_i d_i` and
`w_max=max_(i<j) w_ij`. For
`m lambda>d_max+w_max`, all diagonal QUBO coefficients are below all
off-diagonal coefficients, and

\[
(Q_\lambda)_{ii}=d_i-(m-1)\lambda,
\qquad (Q_\lambda)_{ij}=\lambda-w_{ij}.
\]

Because the graph is noncomplete, its largest off-diagonal coefficient is
`lambda`, and its smallest diagonal coefficient is
`d_min-(m-1)lambda`. The exact min–max denominator is
`D_lambda=m lambda-d_min>0`, so

\[
(A_\lambda)_{ij}=1-\frac{w_{ij}}{D_\lambda}\quad(i\ne j),
\qquad (A_\lambda)_{ii}=\frac{d_i-d_{\min}}{D_\lambda}.
\]

Every off-diagonal coefficient converges to one at rate `O(1/lambda)`.
Hence graph contrast disappears from the optical anchor's normalized
couplings. On weighted-regular graphs the diagonal is constant, so this
proposition remains inside the original paper's stated anchor class.
Using an irregular graph requires the extension label discussed in the spec.

### Candidate proposition: endpoint-dependent circuit convergence

Fix a pair order, repetition number `R`, and the original archive's Rx
beamsplitter convention. Its API angle for normalized coupling `a` is

\[
g_R(a)=\tfrac12\arccos\sqrt{1-a/R^2}.
\]

Let `U_lambda` be the ordered R-repeat product and `U_infty` the same product
with every off-diagonal `a=1`. The latter depends on `m,R` and pair order,
but not the graph. Routing permutations, if any, are identical in the two
products and preserve operator norms.

For fixed `R>=2`, on `a in [1/2,1]`,

\[
g'_R(a)=\frac{1}{4R\sqrt a\sqrt{1-a/R^2}}
\le L_R:=\frac{1}{4R\sqrt{1/2}\sqrt{1-1/R^2}}.
\]

Assume additionally `w_max/D_lambda<=1/2`. Since an Rx gate has
`||G(beta)-G(beta')||<=|beta-beta'|/2`, telescoping the product gives

\[
\|U_\lambda-U_\infty\|
\le\frac{R L_R}{2D_\lambda}\sum_{i<j}w_{ij}
=O(\lambda^{-1}).
\]

At `R=1` the derivative is unbounded at `a=1`; the preceding rate cannot
be claimed. Instead the exact identity is

\[
g_1(1-s)=\frac\pi4-\frac12\arcsin\sqrt s,
\]

and therefore

\[
\|U_\lambda-U_\infty\|
\le\frac14\sum_{i<j}\arcsin\sqrt{\frac{w_{ij}}{D_\lambda}}
=O(\lambda^{-1/2}).
\]

These are upper bounds, not lower asymptotic equivalences. Commuting or
cancelling gate sequences can make convergence faster. Doubling the API
angle to correct the paper's local coincidence identity changes constants,
not these endpoint-dependent upper-bound exponents.

### Candidate consequence: shot cost of detecting optical graph contrast

Use a fixed normalized N-photon input independent of the graph and lambda.
The N-photon representation is a restriction of `U^(tensor N)` to the
symmetric sector, so tensor-product telescoping gives

\[
\|\Gamma_N(U_\lambda)-\Gamma_N(U_\infty)\|
\le N\|U_\lambda-U_\infty\|=:e_\lambda.
\]

For the two pure output states, their vector distance is at most
`e_lambda`, whence squared fidelity `F>=1-e_lambda^2` for sufficiently
small `e_lambda`. For `T` independent copies,

\[
\operatorname{TV}(\hbox{any measured T-copy outputs})
\le\sqrt{1-F^T}\le\sqrt T\,e_\lambda.
\]

Thus achieving a fixed nonzero discrimination distance `c` requires
`T>=c^2/e_lambda^2`, yielding necessary asymptotic shot scalings
`Omega(lambda^2/N^2)` for fixed `R>=2` and `Omega(lambda/N^2)` for `R=1`,
with fixed graph, m, R and the displayed graph-dependent constants.
The theorem also holds after an identical lambda-independent channel.
It does not automatically cover parameter-dependent hardware noise.

This is a distinguishability lower bound under the specified fixed input,
not a lower bound for solving minimum bisection when the graph is already
known classically. It excludes graph-dependent hybrid source changes and
graph-aware output processing from the compared quantum state; those must
be evaluated separately in optimization experiments. Independent graph pairs
can be compared to their shared `U_infty` by another triangle inequality.

### Falsifiable experiment and operational significance

Use connected weighted-regular graphs or a declared extension set; freeze
the graph and pair order before choosing penalties. Sweep lambda across a
geometric grid, test `R=1,2,10`, and compare to `U_infty` with the same input.
Measure `||U_lambda-U_infty||`, output TV, feasible/optimal probabilities,
and bisection quality before and after the classical prefix decoder.
Check whether any observed slope saturates or merely stays below the upper
bound. Separate oracle state comparison from optimum-blind optimization.

A useful corrective control is off-diagonal-only normalization:

\[
\widetilde A_{ij}
=\frac{(Q_\lambda)_{ij}-\min_{a<b}(Q_\lambda)_{ab}}
{\max_{a<b}(Q_\lambda)_{ab}-\min_{a<b}(Q_\lambda)_{ab}}
=\frac{w_{\max}-w_{ij}}{w_{\max}-w_{\min}},
\]

when `w_max>w_min`. This removes lambda from the static couplings while
retaining the original penalty in the loss. It is an explicit algorithm
extension, not a faithful reproduction of the original normalization.
Whether it improves useful bisection sampling is an empirical question.

Possible QPU question: does increasing a valid penalty beyond a locked
range destroy graph-dependent sampling contrast and useful bisection
enrichment at the predicted shot cost, and does the control preserve them?
The circuit family and graph choices must be fixed before hardware runs;
the result may be negative. A comparison that only detects a known BS angle
bug is insufficient for an original optimization result.

Stop this route as a contribution if existing literature already proves the
same optical limit, if the bound is vacuous at every relevant operating
point, or if all bisection-quality behavior is explained by classical
prefix decoding. Retain the mathematical mechanism and failed experiments.

## Route P2-C — Task-dependent use of the spatial-overlap certificate

The prior N1/N2 certificate bounds every fixed event, hence
`|P_success^boson(U)-P_success^dist(U)|` for the same U. Test whether
trained good-bisection meshes retain a certificate small enough to exclude
a meaningful interference benefit. Reoptimize distinguishable circuits
separately and include classical feasible search. A vacuous bound is
inconclusive, not a positive interference result.

This route's novelty remains weaker: its ingredients are standard and the
exact spatial-B bound has not passed exhaustive prior-art review. It is a
diagnostic supporting P2-A/P2-B, not a reason to replace graph optimization
with a generic photonic witness or run a QPU without a task prediction.
