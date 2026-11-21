# Exact threshold-QUBO expectation from two-mode vacuum marginals

Date: 2026-11-21. Base: `2996904f861a5db2a732e38dbc97bd6c91e5708b`.
Status: internal constructive proof and author self-review; independent numeric
and proof review are separate. This is a **known marginal-computation mechanism**,
not a claim of a newly discovered classical simulation principle. Exact source
overlap is recorded in `research/phase3_lowrank_sources.md`.

## 1. Quantifiers and conventions

Let (U\in\mathbb C^{m\times m}) be a passive lossless mode unitary, with
(U_{i,c}) the amplitude from input (c) to output (i). Put (N\le m)
indistinguishable photons into **distinct** inputs (C=(c_1,\ldots,c_N)), one
photon per input. The normalized input is \(\prod_{j=1}^N a_{c_j}^\dagger|0\rangle\).
All probabilities below are unconditioned, retaining output collisions.
Let (x_i=\mathbf1[n_i>0]) be a threshold bit. For an output set
(A=\{a_1,\ldots,a_r\}), define (V=U[A,C]\in\mathbb C^{r\times N}) and

\[
p_0(A)=\Pr[n_i=0\text{ for every }i\in A].
\]

The empty-output-set and vacuum-source conventions are (p_0(\varnothing)=1)
and (p_0(A)=1) when (N=0). Treat them separately in complexity formulas.
Input data must be available classically: a real-arithmetic oracle model and
an exact rational-bit model are different statements, distinguished in §5.

## 2. Vacuum permanent, including the normalization

**Proposition L1.** For the distinct-input source,

\[
\boxed{p_0(A)=\operatorname{per}(I_N-V^\dagger V).}
\tag{1}
\]

There is no modulus square or extra (N!) multiplying this permanent.
The matrix is a positive semidefinite contraction, although some entries can
be complex or negative.

Proof. The output is
\(\prod_{j=1}^N a^\dagger(u_j)|0\rangle\), where (u_j=U[:,c_j]) are
orthonormal. Projection onto zero photons in (A) replaces every vector (u_j)
by (q_j=P_{A^c}u_j). The squared norm of the resulting product of creation
operators equals the permanent of their Gram matrix: commute annihilators to
the vacuum; each permutation contributes exactly
\(\prod_j\langle q_j,q_{\sigma(j)}\rangle\). Their Gram matrix is

\[
\langle q_i,q_j\rangle
=\delta_{ij}-\sum_{a\in A}\overline{U_{a,c_i}}U_{a,c_j}
=(I_N-V^\dagger V)_{ij}.
\]

The input norm is one because the occupied inputs are distinct. Output
occupation factorials are already present in the creation-operator norm;
they must not be removed by replacing bosons with independent particles. □

## 3. Explicit fixed-rank polynomial algorithm

For multi-indices (p,q\in\mathbb Z_{\ge0}^r), write (p!=\prod_a p_a!).
Define a polynomial in (2r) **formal commuting variables**:

\[
F(x,y)=\prod_{j=1}^N\left[
1-\left(\sum_{a=1}^r\overline{V_{aj}}x_a\right)
\left(\sum_{b=1}^r V_{bj}y_b\right)\right]
=\sum_{p,q} f_{p,q}x^p y^q.
\tag{2}
\]

**Proposition L2.** The exact extraction rule is

\[
p_0(A)=\sum_{|p|\le N}p!\,f_{p,p}.
\tag{3}
\]

Proof. Multilinearity in the identity part gives

\[
\operatorname{per}(I_N-V^\dagger V)
=\sum_{S\subseteq[N]}(-1)^{|S|}
\operatorname{per}((V^\dagger V)[S,S]).
\tag{4}
\]

For a fixed (S), expand the Gram factors using labels in ([r]).
The conjugated and unconjugated factors must have the same label-count vector
(p); for any such pair of label assignments, precisely (p!) permutations
match equal labels. Expanding the selected nonconstant factors in (2) gives
these two assignments and sign ((-1)^{|S|}). Summing the diagonal coefficients
with weight (p!) therefore yields (4). □

A direct coefficient DP starts at (f^{(0)}_{0,0}=1) and, for (j=1,\ldots,N),
uses a fresh array (or safely ordered in-place updates) to apply

\[
f^{(j)}_{p,q}=f^{(j-1)}_{p,q}
-\sum_{a,b=1}^r\overline{V_{aj}}V_{bj}
 f^{(j-1)}_{p-e_a,q-e_b},
\tag{5}
\]

where invalid or negative indices contribute zero. Keep **off-diagonal**
(p\ne q) states: later multiplications can turn them into diagonal states.
Every retained state has (|p|=|q|\le j). Thus the array size is

\[
S_r(j)=\sum_{s=0}^j\binom{s+r-1}{r-1}^2
=O_r((j+1)^{2r-1}).
\tag{6}
\]

For fixed (r\ge1), define the exact number of state visits

\[
T_r(N)=\sum_{j=0}^{N-1}S_r(j).
\]

Precomputing the (r^2N) products in (5), each visit requires at most (r^2)
multiplications and (r^2) additions, plus copying/initialization of the carry.
The final extraction visits \(\binom{N+r}{r}\) diagonal states. Hence a concrete
complex-field arithmetic bound is

\[
2r^2 T_r(N)+O\!\left(r^2N+r\binom{N+r}{r}+N\right)
=O_r(N^{2r})\quad\text{operations},
\tag{7}
\]

with (O_r(N^{2r-1})) field elements of storage (two arrays suffice).
State indexing has (O(r\log(N+1)))-bit indices; polynomial indexing overhead
does not change polynomial bit computability. For the relevant ranks:

| r | (S_r(N)) | (T_r(N)) | Dominant arithmetic bound |
|---|---|---|---|
| 1 | (N+1) | (N(N+1)/2) | (N(N+1)+O(N)) |
| 2 | ((N+1)(N+2)(2N+3)/6) | (N(N+1)^2(N+2)/12) | (8T_2(N)+O(N^2)) |

The state-count refinement uses the equal-total-degree constraint. Earlier
sources already give this polynomial algorithm with a looser monomial count;
this elementary counting refinement is not presented as a certified research
novelty. The factorial table is computed once. Forming an (N\times N) Gram
matrix is unnecessary for this algorithm.

## 4. Threshold moments and the optimization objective

Write (p_i=p_0(\{i\})), (p_{ij}=p_0(\{i,j\})). Inclusion–exclusion gives

\[
\mathbb E[x_i]=1-p_i,\qquad
\mathbb E[x_ix_j]=1-p_i-p_j+p_{ij}\quad(i\ne j).
\tag{8}
\]

Consequently for arbitrary real coefficients

\[
H(x)=c+\sum_i h_i x_i+\sum_{i<j}J_{ij}x_ix_j,
\]

its expectation is obtained exactly from (m) rank-one and at most
\(\binom m2\) rank-two evaluations. The arithmetic cost is

\[
O(mN^2+m^2N^4),
\tag{9}
\]

and workspace can be reused with (O(N^3+m^2)) field elements, besides the
classically supplied matrix. Sparse (J) requires only its nonzero pairs.
For symmetric (Q), set (h_i=Q_{ii}), (J_{ij}=2Q_{ij}): this is
\(\mathbb E[x^TQx]\), with no missing factor two. In particular, canonical
cut-plus-quadratic-balance-penalty expectation is included for every penalty
value, without any large-penalty or collision-free approximation.

The original static ObliQ source, one photon per mode ((N=m)), satisfies
the distinct-input assumption. So does a known hybrid prefix source with
one photon in each selected mode; obtaining that source remains a separate
classical/physical stage. Any passive variational stage can be absorbed into
(U), so the same expectation evaluation remains available at every chosen
parameter value. Computing (U) from a polynomial-size classical gate list
has its own polynomial cost, added to (9).

This removes a purported need to sample an exponentially large Fock law merely
to evaluate the **ideal unconditioned threshold-QUBO expectation**. It does not
efficiently solve the nonconvex global parameter optimization. It does not
reproduce the finite-shot noise of a training procedure or prove equal solver
performance under a different oracle budget. The modal Fock candidate and best
of many sampled cuts use information beyond (8). Prefix marginal rankings are
available from rank one, but ties and finite precision remain relevant.

More generally, any fixed-degree (d) threshold polynomial follows by
inclusion–exclusion from output vacuum sets of size at most (d), giving a
polynomial bound at fixed (d), with an exponent depending on (d). No such
bound is asserted when conditioning on a global feasibility event: that event
can involve all modes, and its normalization/numerators are not given by (8).

## 5. Rational bit complexity and sufficient precision

Arithmetic operations on arbitrary real numbers are not unit-cost physical
computations. The following supplies a deliberately conservative, explicit
bit guarantee; it does not certify an ordinary float64 implementation.

First suppose the real and imaginary parts of each (V_{aj}) are rationals
with numerators and denominators of at most (b) bits, and (|V_{aj}|\le2).
Let (D_0) be a common denominator, e.g. the product of the (2rN) positive
denominators. It has (h\le2rNb+1) bits. Write (V_{aj}=z_{aj}/D_0) with
Gaussian integers (z_{aj}). At DP stage (j), use common denominator
(D_0^{2j}); the carry in (5) multiplies its numerator by (D_0^2), and a
transition multiplies by (-\overline z_{aj}z_{bj}). Thus all operations can
be performed with integers, avoiding repeated uncontrolled denominator growth.

Set (K_r=1+4r^2). The coefficient \(\ell_1\) norm of each factor in (2)
is at most (K_r), so the coefficient norm after (j) factors is at most
(K_r^j). The final diagonal weights satisfy (p!\le N!). Therefore every
coefficient numerator and the final extracted numerator have at most

\[
B=2Nh+\lceil N\log_2 K_r\rceil
+\lceil\log_2(N!)\rceil+O(1)
=O_r(N^2b+N\log(N+1))
\tag{10}
\]

bits per real/imaginary component. This also bounds intermediate sums by
using the sum of absolute expanded terms. Integer multiplication on (B)
bits can conservatively use (O(B^2)) bit operations. Equations (6),(7),(10)
therefore give polynomial bit time and memory for fixed (r). For arbitrary
rational QUBO coefficients their bit lengths and their total encoded size
must also be counted when forming the final linear combination. No exact
finite-string representation of an arbitrary irrational unitary is assumed.

For a physical matrix (V), each (|V_{aj}|\le1). Let a dyadic approximation
(\widetilde V) satisfy entrywise complex error at most (\eta\le1).
Denote the polynomial extraction in (2),(3) by (f(V)); it equals the physical
probability at (V), while its value at (\widetilde V) is a formal polynomial
evaluation and need not itself be a valid probability. Factorwise,

\[
\|F_j(V)-F_j(\widetilde V)\|_1\le3r^2\eta,\qquad
\|F_j(V)\|_1,\|F_j(\widetilde V)\|_1\le K_r.
\]

The first inequality follows from
\(|\overline v_a v_b-\overline{\tilde v}_a\tilde v_b|\le3\eta\).
Telescoping the product and then applying the diagonal functional gives

\[
|f(V)-f(\widetilde V)|
\le 3Nr^2N!K_r^{N-1}\eta.
\tag{11}
\]

If each real/imaginary component is approximated to absolute error (2^{-b}),
its complex error is at most (2^{1-b}). For (N,r\ge1), it suffices to use

\[
b\ge\max\!\left(1,
\left\lceil\log_2\frac{6Nr^2N!K_r^{N-1}}\epsilon}\right\rceil\right)
=O_r(N\log(N+1)+\log(1/\epsilon))
\tag{12}
\]

and evaluate those dyadics exactly to obtain additive error at most
(\epsilon). Input production must supply these certified approximations;
calibration error or a mere binary64 matrix is not equivalent to such a
certificate. The polynomial may suffer cancellation, and probabilities can
be zero or arbitrarily small. No uniform relative-error guarantee, bounded
relative condition number, or blanket float64 stability follows from (12).

For the QUBO convention of §4, if each needed vacuum probability has absolute
error at most (\epsilon_0), the final energy error is at most

\[
\left(\sum_i|h_i|+3\sum_{i<j}|J_{ij}|\right)\epsilon_0.
\tag{13}
\]

For target energy error (\epsilon), use that coefficient factor in (12) to
choose (\epsilon_0); handle its zero value by returning the constant (c).
Thus large penalties enter the required precision through coefficient sizes,
not through an omitted unit-cost real-arithmetic assumption.

## 6. Falsification checks and non-claims

- For (N=1), (1) gives (1-\sum_a|V_{a1}|^2), as required.
- For (r=1,N=2), set (q_j=|V_{1j}|^2). Equations (2),(3) give
  (1-q_1-q_2+2q_1q_2). The factor (2!) is essential; omitting it fails
  the two-photon Hong–Ou–Mandel example ((q_1=q_2=1/2), vacuum probability
  (1/2), not (1/4)).
- If all output modes are in (A) and (N>0), (1) is the permanent of zero,
  hence zero. Here (r=m) can grow, so the fixed-(r) runtime conclusion
  cannot be applied.
- Repeated occupied input modes invalidate the identity term in (1). For two
  photons in the same input, single-output weight (q), the actual vacuum
  probability is ((1-q)^2), whereas incorrectly using (I_2-V^\dagger V)
  gives (1-2q+2q^2). General repeated-input marginal algorithms exist in the
  literature; this particular formula and proof impose distinct inputs.
- No full-distribution sampler, modal-output algorithm, finite-shot trajectory
  simulation, collision-free-conditioned expectation, optimum probability,
  or general device-noise simulator follows from this result. A generic
  partial-distinguishability model can destroy the stated low-rank structure.
- Independent output efficiency can be represented by (V\mapsto
  \operatorname{diag}(\sqrt{\eta_a})V) after adding vacuum loss ports to an
  isometry; the same Gram proof applies to no-click events. This narrow
  extension does not cover arbitrary correlated noise or postselection.

No numerical experiment is claimed in this note. Its evidence is the
constructive proof, elementary controls above, and exact primary-source overlap.
The parent agent's separate Perceval/full-Fock checks must have their own
recorded range and provenance. No code, QPU, manuscript, or shared state was
modified by this theory worktree.
