# Quantitative collisionless-limit certificate and its failure under scaling

Research checkpoint: continuation from `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`;
reviewed 2026-11-20. This is a mathematical research result, not a manuscript
section. **Proof status: PROVEN by the arguments below. Novelty: OPEN.**

## Exact setting and quantities

Let `m>=k>=1`, and send one indistinguishable photon into each of `k` distinct
input modes of a passive lossless `m`-mode unitary `U`. Relabel the occupied
columns `1,...,k`. Let `p(t)` be the complete output occupation distribution,
including collisions. Let `d(t)` be the distribution obtained by scattering
the `k` photons independently using probabilities `q_ia=|U_ia|^2` and forgetting
their labels. No distribution is conditioned on collision-free detection.
Define

\[
\operatorname{TV}(p,d)=\tfrac12\sum_{t:\,|t|=k}|p(t)-d(t)|,
\quad B_{ab}=\sum_{i=1}^m|U_{ia}U_{ib}|,
\quad A=B-I_k,
\quad S=\|A\|_F^2=2\sum_{a<b}B_{ab}^2.
\]

Thus `B` is the Gram matrix of the nonnegative unit vectors
`(|U_1a|,...,|U_ma|)`, `B_aa=1`, and `A` is real symmetric, nonnegative
and zero-diagonal. These are spatial intensity-overlap quantities, **not**
the photons' internal distinguishability Gram matrix.

## N1 — Permanent certificate for the complete output distribution

\[
\boxed{\operatorname{TV}(p,d)
\le\min\left(1,\frac{\operatorname{Per}(B)-1}{2}\right).}
\]

Proof, with all factorials explicit. For any occupation vector `t`, choose an
ordered output list `y=(y_1,...,y_k)` with multiplicities `t`; put
`t!=prod_i t_i!` and `a_sigma(y)=prod_j U_(y_j,sigma(j))`. Since the input
factorials are all one,

\[
p(t)=\frac{|\sum_{\sigma\in S_k}a_\sigma(y)|^2}{t!},
\qquad d(t)=\frac{\sum_{\sigma\in S_k}|a_\sigma(y)|^2}{t!}.
\]

Subtract the diagonal terms and apply the triangle inequality. The resulting
nonnegative summand `F(y)=sum_(sigma!=tau)|a_sigma(y)a_tau(y)|` is invariant
under permutation of `y`. There are `k!/t!` ordered lists for occupation `t`.
Therefore

\[
\begin{aligned}
2\operatorname{TV}(p,d)
&\le\sum_t\frac{F(y(t))}{t!}
=\frac1{k!}\sum_{y\in\{1,\ldots,m\}^k}F(y)\\
&=\frac1{k!}\sum_{\sigma\ne\tau}
\prod_{j=1}^k\sum_i|U_{i,\sigma(j)}U_{i,\tau(j)}|\\
&=\sum_{\pi\ne\mathrm{id}}\prod_{a=1}^kB_{a,\pi(a)}
=\operatorname{Per}(B)-1.
\end{aligned}
\]

For the penultimate equality set `pi=tau o sigma^{-1}`; each relative
permutation occurs `k!` times. The identity term is one because every diagonal
entry of `B` is one. The case `k=1` gives zero exactly. This proof neither
omits repeated output rows nor treats the collision-free sector as normalized.

## N2 — Polynomial-time certificate without a permanent

Write `!r` for the number of derangements of `r` objects and

\[
H_k(s)=\sum_{r=2}^k\frac{!r}{r!}\,s^{r/2}
=\frac{s}{2}+\frac{s^{3/2}}3+\frac{3s^2}{8}+\cdots.
\]

Then for every `S>=0`,

\[
\boxed{\operatorname{TV}(p,d)\le
\min\bigl(1,\tfrac12 H_k(S)\bigr).}
\]

Proof. `Per(I+zA)` is a polynomial whose coefficient of `z^r` counts weighted
permutations moving `r` vertices. Each such permutation is a collection of
vertex-disjoint directed simple cycles of length at least two. Let `C_l` be
the sum of the weights of all directed simple cycles of length `l`, counting
a cycle only once up to cyclic rotation. All weights are nonnegative.
Allowing cycles to repeat and to overlap gives the coefficientwise inequality
of formal power series

\[
\operatorname{Per}(I+zA)
\preceq\prod_{c}\exp(w_cz^{|c|})
=\exp\left(\sum_{l=2}^k C_lz^l\right)
\preceq\exp\left(\sum_{l=2}^\infty
\frac{\operatorname{tr}(A^l)}{l}z^l\right).
\]

Indeed each simple cycle contributes exactly `l` terms to `tr(A^l)`; all
additional closed walks contribute nonnegative weight. A disjoint collection
appears with coefficient one in the exponential expansion, so the factorials
of repeated cycles cannot undercount that collection.

Since `A` is real symmetric, for every integer `l>=2`,

\[
0\le\operatorname{tr}(A^l)
\le\sum_j|\lambda_j(A)|^l
\le\left(\sum_j\lambda_j(A)^2\right)^{l/2}=S^{l/2}.
\]

Nonnegativity on the left follows from the closed-walk expansion, also for
odd `l`; the last inequality is monotonicity of finite-dimensional `ell_p`
norms. Substitute this coefficientwise bound into the exponential, then use

\[
\exp\left(\sum_{l=2}^\infty\frac{x^l}{l}\right)
=\frac{e^{-x}}{1-x}
=\sum_{r=0}^\infty\frac{!r}{r!}x^r.
\]

These are formal series identities, so no condition `S<1` is needed when
comparing coefficients through degree `k`. Summing those coefficient bounds
at `z=1` gives `Per(B)-1<=H_k(S)`. Combining with N1 proves N2.

Computing `B` and `S` costs `O(mk^2)` arithmetic operations; evaluating `H_k`
costs `O(k)`. The independent-particle distribution `d` can be sampled by
`k` categorical draws after `O(mk)` probability-table preparation. Hence N2
is an efficiently checkable sufficient condition for this **particular**
classical approximation. Failure of the bound says nothing about hardness.

For `0<=S<1`, a simpler but weaker closed form is

\[
\operatorname{TV}(p,d)\le
\min\left(1,\frac12\left[\frac{e^{-\sqrt S}}{1-\sqrt S}-1\right]\right).
\]

Since `!r/r!<=1/2` for `r>=2`, another convenient bound is
`TV<=S/[4(1-sqrt(S))]` for `S<1`. In particular `S<=1/4` implies
`TV<=S/2`. The local leading term of N2 is `S/4+O(S^(3/2))`,
not a standalone upper bound `S/4` for arbitrary `S`.

If the exact overlap graph has components `J`, N2 may be tightened using
`Per(B)=prod_J Per(B_J)`: substitute the bound
`prod_J [1+H_|J|(S_J)]` in N1. Exact zeros, rather than an uncharged numerical
threshold, define these components.

## N3 — A dimension-dependent bound from collision probability alone

Let `delta=1-P_CF(p)` and `K=binom(k,2)` with `k>=2`. For each pair,
Cauchy–Schwarz gives

\[
B_{ab}^2\le m\sum_iq_{ia}q_{ib}.
\]

The pair-collision identity from T-Pairs gives
`2 sum_(i,a<b)q_ia q_ib=E_p M<=K delta`. Consequently

\[
S\le mK\delta,\qquad
\boxed{\operatorname{TV}(p,d)
\le\min\left(1,\tfrac12H_k(mK\delta)\right).}
\]

This proves stability for **fixed** `m,k` as `delta->0`. It is nonvacuous,
for example, whenever `mK delta<=1/4`, yielding `TV<=mK delta/2<=1/8`.
For balanced density `m=2k`, this sufficient regime requires
`delta=O(m^-3)` with a small constant. The requirement is conservative and
not claimed necessary. Measuring the actual `S` can give a stronger certificate
than discarding structure via `mK delta`.

For any fixed optimization success event `E`, including the set of optimal
collision-free bisections, `|p(E)-d(E)|<=TV(p,d)`. Thus a small N2 bound
certifies a small absolute difference in success per physical attempt for
the **same interferometer**. It does not compare reoptimized circuits or
bound the ratio of waiting times when success probabilities are tiny.

## N4 — Counterexample to dimension-uniform low-collision reasoning

For every even `L>=2`, take two occupied columns on `L` active modes:

\[
u_i=L^{-1/2},\qquad
v_i=\begin{cases}L^{-1/2}&i\le L/2,\\-L^{-1/2}&i>L/2.\end{cases}
\]

They are orthonormal and can be completed to an `L`-mode unitary. For the
two-photon input the complete probabilities are

| Outcome | Bosons p | Distinguishable d | Number of outcomes |
|---|---:|---:|---:|
| Two photons in the same mode | `2/L^2` | `1/L^2` | `L` |
| Distinct modes with the same sign | `4/L^2` | `2/L^2` | `L(L-2)/4` |
| Distinct modes with opposite signs | `0` | `2/L^2` | `L^2/4` |

The probabilities in each column sum to one. The total bosonic collision
probability is `delta=2/L`, while the sum of the positive differences is

\[
L\frac1{L^2}+\frac{L(L-2)}4\frac2{L^2}=\frac12.
\]

Therefore `TV(p,d)=1/2` for every `L`, even though `delta->0`. Here
`B=[[1,1],[1,1]]`, so N1 is exactly saturated. The Cauchy bound in N3 is
also saturated: `mK delta=2` and `TV=m delta/4=1/2` for `k=2`.

The same obstruction exists at **balanced density**. For every even `k>=2`,
let `m=2k`, take an active block of `L=k+2` modes with the preceding two
photons, and add `k-2` isolated spectator modes, each with one deterministic
photon. The unitary is block diagonal; input modes can be permuted so the
occupied modes have the standard ordering. The spectators are identical in
both experiments, so

\[
m=2k,\quad \delta=\frac2{k+2}\longrightarrow0,
\quad\operatorname{TV}(p,d)=\frac12.
\]

Thus no bound depending only on `delta`, uniformly over balanced system
sizes and tending to zero with `delta`, can be valid. This does **not**
establish classical hardness: this counterexample itself has an elementary
classical sampler reproducing its interference pattern. It refutes only
approximation by independent distinguishable particles from low collision
probability alone.

## Prior-work boundary

Permanent/triangle bounds for deviations from distinguishable statistics are
already a literature technique. Tichy, [arXiv:1410.7687v3](https://arxiv.org/html/1410.7687v3),
Sec. IV.2 Eq. (55), gives a bound involving the permanent of the entrywise
modulus of the **internal** distinguishability Gram matrix. Sec. IV.4 uses
the unhalved L1 convention for variation distance. Our `B` instead contains
spatial intensity overlaps, and N1 is proved independently rather than
identified with that source's theorem. Exact overlap classification, the
cycle/Frobenius reduction and the balanced spectator construction have not
received an exhaustive novelty search. **Novelty remains OPEN.**
