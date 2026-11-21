# P3: fixed-input penalty washout of the authenticated static ObliQ kernel

Date: 2026-11-21. Base revision: `8edfca70f03555479ea62ef9c49d727a27cc1861`.
Status: internal proof below, author self-review; independent review pending.
Novelty: **OPEN**, with no claim of exhaustive prior-art coverage.

The precise result is an upper bound on the physical information remaining in a
fixed static optical kernel as a quadratic balance penalty grows. It is not a
lower bound on optimization time. The algorithm already receives the graph
classically, and its classical source selection and decoder can retain graph
information independently of the optical state.

## 1. Scope and authenticated conventions

Let (m\ge4) be even, (k=m/2), and let (w=(w_{ij})) be a fixed real symmetric
matrix with nonnegative off-diagonal entries, zero diagonal, and
\(\min_{i<j}w_{ij}=0\). Define

\[
d_i=\sum_jw_{ij},\quad d_- =\min_i d_i,\quad d_+=\max_i d_i,
\quad w_+=\max_{i<j}w_{ij},\quad W=\sum_{i<j}w_{ij}.
\]

For (x\in\{0,1\}^m), use the canonical symmetric QUBO

\[
E_\lambda(x)=\operatorname{cut}_w(x)+\lambda(|x|-k)^2
=x^\mathsf TQ_\lambda x+\lambda k^2,
\quad (Q_\lambda)_{ii}=d_i-(m-1)\lambda,
\quad (Q_\lambda)_{ij}=\lambda-w_{ij}\ (i\ne j).
\tag{1}
\]

The literal archive globally normalizes **all entries** of (Q), then uses
only its normalized off-diagonal entries for optical gates. Fix an integer
(R\ge1), a permutation (\pi) of the unordered mode pairs, and variant
(v=1) (literal archive) or (v=2) (corrected physical angle). Neither (R),
(v), nor (\pi) varies with (\lambda). The Rx API matrix is

\[
G_{ij}(\beta)|_{\{i,j\}}=
\begin{pmatrix}\cos(\beta/2)&i\sin(\beta/2)\\
i\sin(\beta/2)&\cos(\beta/2)\end{pmatrix},\qquad
\beta_{ij}=v g_R(a_{ij}),\quad
g_R(a)=\tfrac12\arcsin(\sqrt a/R).
\tag{2}
\]

Each gate multiplies on the left, in order (\pi), repeated (R) times.
This is the archive's expression
\(\tfrac12\arccos\sqrt{1-a/R^2}\), with the actual Perceval half-angle convention.
The paper's physical mixing angle and this API parameter differ by a factor
two; both variants are kept explicit. The archive obtains (\pi) through
`list(set(...))`; lexicographic order is a separate reproducibility choice.
All bounds below hold for every fixed order, but their limits can differ.
Nonadjacent routing by the archive's two inverse permutations implements the
same two-mode gate. No eigenvector or eigendecomposition occurs here.

ObliQ's stated supported problem class has constant diagonal QUBOs. Thus the
direct graph-bisection specialization is the weighted-regular case (d_i=d).
Equations and proofs also apply mathematically to irregular graphs passed
through this kernel; that is an explicitly labeled extension, not an assertion
that the original algorithm implements arbitrary diagonal costs faithfully.
The literal static source is one photon per mode, (N=m). The theorem allows
any common normalized pure (N)-photon input, fixed as (\lambda) varies.

Source: [Ranjan et al., author manuscript, §§4.1–4.4](https://repository.rice.edu/server/api/core/bitstreams/0c308cfa-0cac-4b03-ba49-9effdba0799b/content),
[Zenodo v2 artifact, `ObliQ/circ_init.py`, lines 35–63](https://zenodo.org/records/17343439),
and [Perceval v0.11 Rx implementation](https://raw.githubusercontent.com/Quandela/Perceval/v0.11.0/perceval/components/unitary_components.py).
Exact source hashes and limits of authentication are in the companion audit.

## 2. Exact normalization regime

If (m\lambda>d_++w_+), every diagonal entry is strictly below every
off-diagonal entry. Since a zero-weight pair exists,

\[
\min Q_\lambda=d_--(m-1)\lambda,\quad
\max Q_\lambda=\lambda,\quad D=m\lambda-d_->0.
\]

Consequently global entrywise min-max normalization gives exactly

\[
a_{ij}=1-\frac{w_{ij}}D\ (i\ne j),\qquad
a_{ii}=\frac{d_i-d_-}D.
\tag{3}
\]

Proof: (d_+-(m-1)\lambda<\lambda-w_+), and the minimum diagonal
and maximum off-diagonal are attained. Subtract the minimum and divide by
their difference (D). This establishes (3), including signs and the factor
(m). The argument is for the canonical (Q) in (1): QUBO gauge changes,
diagonal removal, or complement preprocessing can change the optical kernel.

## 3. Quantitative unitary convergence

Let (U_\lambda=U_{R,v,\pi}(a)) and let (U_\infty=U_{R,v,\pi}(1)) replace
every off-diagonal coupling by one. This limit depends on (m,R,v,\pi),
but not on the graph. Write \(\|\cdot\|\) for the operator norm.

**Proposition P3.1.** Under §1 and (m\lambda>d_++w_+):

\[
\|U_\lambda-U_\infty\|\le B_\lambda,
\quad B_\lambda=\frac v4\sum_{i<j}\arcsin\sqrt{w_{ij}/D}
\quad (R=1).
\tag{4}
\]

For (R\ge2), assume additionally (w_+/D\le1/2). Put

\[
L_R=\frac1{4R\sqrt{1/2}\sqrt{1-R^{-2}}}.
\quad\text{Then}\quad
\|U_\lambda-U_\infty\|\le B_\lambda
=\frac{vR L_R W}{2D}.
\tag{5}
\]

In particular, at fixed (m,w,R,v,\pi), the bounds are
(O(\lambda^{-1/2})) for (R=1) and (O(\lambda^{-1})) for (R\ge2).
These are upper bounds, not universal asymptotic equalities or lower bounds.
They need not be uniform in growing (m,W,N,R).

Proof. On the active two-mode block, (G(\beta)=e^{i\beta X/2}), so

\[
\|G(\beta)-G(\beta')\|=2|\sin((\beta-\beta')/4)|
\le\tfrac12|\beta-\beta'|.
\tag{6}
\]

Telescoping a product of unitaries bounds its difference by the sum of gate
differences, irrespective of their noncommutation. For (R=1),

\[
g_1(1)-g_1(1-z)=\tfrac12\arcsin\sqrt z,
\quad 0\le z\le1,
\]

and (6) immediately gives (4). In particular
\(\beta_{ij}=v\pi/4-(v/2)\sqrt{w_{ij}/D}+O(D^{-3/2})\)
for fixed positive (w_{ij}); replacing this by (O(D^{-1})) is wrong.
For (R\ge2),

\[
g_R'(a)=\frac1{4R\sqrt a\sqrt{1-a/R^2}}\le L_R,
\qquad a\in[1/2,1].
\]

The mean value theorem, (3), (6), and (R) repetitions give (5).
Zero-weight pairs contribute zero. For the empty graph (U_\lambda=U_\infty)
exactly. No spectral perturbation theorem or nondegenerate eigenvalue
assumption was used. □

## 4. From mode matrices to Fock states, measurements, and copy budgets

Let (\Gamma_N(U)) be the restriction of (U^{\otimes N}) to the symmetric
(N)-particle subspace, with normalized occupation states. The vacuum case
(N=0) is identically constant. For (N\ge1), telescope the tensor product:

\[
\|\Gamma_N(U)-\Gamma_N(V)\|\le N\|U-V\|.
\tag{7}
\]

Restriction cannot increase the norm. For the same normalized pure input
(|s\rangle), let \(|\psi_\lambda\rangle=\Gamma_N(U_\lambda)|s\rangle\),
(|\psi_\infty\rangle=\Gamma_N(U_\infty)|s\rangle\), and (e=NB_\lambda).
Then \(\|\psi_\lambda-\psi_\infty\|\le e\).
Use squared fidelity (F=|\langle\psi_\lambda|\psi_\infty\rangle|^2)
and trace distance \(T(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1\).
For (e\le1), the real part of the overlap is at least (1-e^2/2),
hence (F\ge(1-e^2/2)^2\ge1-e^2). For pure states their two-dimensional
span gives (T=\sqrt{1-F}\). Thus every common measurement has

\[
\operatorname{TV}(p_\lambda,p_\infty)
\le T(\rho_\lambda,\rho_\infty)\le\min(1,e).
\tag{8}
\]

For (t) independently prepared copies, even a collective measurement obeys

\[
\operatorname{TV}(p_\lambda^{(t)},p_\infty^{(t)})
\le\sqrt{1-F^t}\le\min(1,\sqrt t\,NB_\lambda).
\tag{9}
\]

The middle bound uses (1-(1-e^2)^t\le te^2) for (e\le1); for
(e>1) the capped bound is trivial. Consequently obtaining TV separation
at least (c\in(0,1]) requires

\[
t\ge\frac{c^2}{N^2B_\lambda^2}\quad\text{when }B_\lambda>0.
\tag{10}
\]

At fixed graph and fixed parameters these are necessary copy costs
\(\Omega(\lambda/N^2)\) for (R=1) and
\(\Omega(\lambda^2/N^2)\) for (R\ge2). They concern distinguishing this
physical family from its limit, not finding a graph cut when the graph is
already given. An upper bound on distance does not establish its tightness.
If (B_\lambda=0), the states coincide and the distinction is impossible.
Fock PNR measurement, threshold coarse-graining, and a common stochastic
decoder all satisfy (8). A common trace-preserving noise channel also preserves
the bound. Conditioning on successful detection is not trace preserving and
needs an explicit acceptance denominator; (8) does not freely transfer to
postselected laws.

For two fixed graphs (G,H), with the same (m,R,v,\pi,N,s), the triangle
inequality gives a raw-state distance bound (N(B_\lambda(G)+B_\lambda(H))).
This inter-graph comparison fails if their sources or subsequent channels differ.

## 5. What the actual classical decoder permits

At fixed (G), a graph-aware decoder (D_G) applied to both raw laws is a
common channel, so its output laws contract as in (8). There is no blanket
prohibition on graph-aware decoding. However (D_G(p_G)) and (D_H(p_H))
need not converge to a common output law: the classical maps can differ even
when the raw states coincide. A decoder changing with (\lambda) similarly
has no fixed output limit without additional conditions. If it is applied to
both compared laws at each (\lambda), contraction still holds pointwise.

The original ideal static decoder uses distribution-level statistics, rather
than a single-sample map: it ranks mode click marginals, tests their prefixes,
and tests the threshold of a modal raw Fock outcome. Here and in the candidate
pool conclusion below, use the archive's **`graph_val=0`** branch of
`utils.py:solution_guesses3`, with unrestricted prefixes. Its coloring and
assignment branches filter groups or rows/columns and are outside this claim.
Discrete rankings and
argmax need gaps. Let (g>0) be the difference between the kth and (k+1)th
reference click marginals, and (h>0) the reference modal Fock probability
minus the second largest. If raw Fock TV is (\varepsilon<\min(g,h)/2),
the reference kth prefix and unique modal Fock outcome remain unchanged.
Indeed every click marginal and every Fock-event probability changes by at
most (\varepsilon); pairwise differences change by at most (2\varepsilon).
No gaps elsewhere in the marginal ordering are needed just for the kth set.

If additionally (\lambda>W), every infeasible binary candidate has
(E_\lambda\ge\lambda>W\), whereas each feasible candidate has cost
at most (W). A kth prefix always supplies a feasible candidate. Therefore,
under the two strict gaps, the winning candidate is selected by classical
evaluation from at most two fixed feasible cuts: that kth prefix and, if
balanced, the modal threshold. The graph-dependent score and tie rule can
still make the winner depend on (G). This is an ideal exact-distribution
statement; estimating those statistics consumes shots and introduces errors.
It is not a uniform runtime bound or a claim covering the trained variational
or hybrid source-selection stages.

## 6. Counterexamples to tempting extensions

**No unconditional decoder gap.** Take (m=4) and the admissible fixed pair
order ((01,23,02,13,03,12)). Group its three perfect matchings into permutation
matrices (P_1,P_2,P_3). Directly (P_i^2=I), all (P_i) commute, and
(P_1+P_2+P_3=J-I). If each limiting pair gate has angle
(\beta=v g_R(1)), then

\[
U_\infty=\exp\!\big(iR\beta(J-I)/2\big)
=e^{-iR\beta/2}\left[I+\frac{e^{2iR\beta}-1}{4}J\right].
\tag{11}
\]

It commutes with every mode permutation. The static input \(|1111\rangle\)
is also permutation invariant; hence all reference click marginals coincide
exactly. In particular (g=0). This is a counterexample within the actual
finite-product definition, not an unrelated spectral surrogate. It invalidates
a claim that strict rank gaps are automatic. It does not by itself prove the
decoder fails to converge for every perturbation. The saved SymPy computation
checks the matching-generator identities exactly, and independently checks the
matrix identity for corrected (R=1).

**Eigenvectors may rotate although the unitary converges.** Set
(V(t)=\left(\begin{smallmatrix}\cos t&-\sin t\\\sin t&\cos t\end{smallmatrix}\right))
and (U(t)=V(t)\operatorname{diag}(e^{i/t},e^{-i/t})V(t)^\mathsf T), (t\ge1).
Then (\|U(t)-I\|=2\sin(1/(2t))\le1/t), but its eigenvector projector
has different limits along (t=2\pi n) and (t=2\pi n+\pi/4).
Thus convergence of matrices does not justify convergence of spectral anchors
without a gap. Authentic static ObliQ does not use these anchors, so this
counterexample is not an objection to P3.1.

**Sources and decoders can retain all classical information.** Two orthogonal
graph-dependent inputs remain orthogonal under a common (\Gamma_N(U_\infty));
their quantum trace distance is one. Inputs in different photon-number sectors
are orthogonal as well. This refutes extending the fixed-input state theorem
to arbitrary hybrid source selectors. It does not assert that threshold
measurement distinguishes every such pair. Even with identical raw laws,
deterministic decoders returning a graph-specific classically computed cut
can have completely different outputs. State washout cannot bound that
classical computation or prove solver failure.

**Different normalization, different question.** Off-diagonal-only normalization
instead gives ((w_+-w_{ij})/(w_+-w_-)\), independent of (\lambda), when
(w_+>w_-). This avoids this particular washout, while changing the algorithm.
If all off-diagonals are equal that normalization is undefined absent a
separately specified constant-range convention. No quality improvement follows
from avoiding this mechanism alone.

## 7. Finite falsifier and limits

The independent script `experiments/phase3_washout_bound_audit.py` stores all
972 unitary checks and 36 full-Fock comparisons, without renormalizing away
collisions, plus 36 limit-gap calculations. It tests (3)–(8), exact matching
identities, an identity-circuit control, and the two-photon HOM distribution.
Every tested graph, pair order, raw Fock amplitude, seed, version, timestamp,
and result hash is retained under `experiments/P31_washout_bound_audit/`.
The finite tests could refute a bound through an explicit violating case;
their passing cannot prove a universal statement. The analytic proof is the
universal evidence. There is no QPU result, no optimization benchmark, no
uniform scalable conclusion, and no certified novelty in this note.
