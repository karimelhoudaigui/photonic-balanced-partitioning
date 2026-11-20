# Verified theory checkpoints

Base checkpoint: `847d7a0e05cdf7fa8ca50c68f51f8d7e03158508`.
Date checked: 2026-11-20. Scope: ideal, passive, lossless linear optics;
indistinguishable photons; no ancillary photons, adaptive measurements or nonlinearities.
Proof status below concerns mathematical correctness, **not novelty**. These are
research notes; the manuscript remains frozen.

## T-Haar — Haar-averaged collision-free probability

**Status: PROVEN. Attribution: known after translation of notation.**
Let `m >= 1`, `0 <= k <= m`, and let `rho` be any fixed trace-one density
operator on `H_k = Sym^k(C^m)`, chosen independently of `U`. Write
`D = binom(m+k-1,k)` and `d = binom(m,k)`. For Haar `U in U(m)`,

\[
\mathbb E_U P_{\rm CF}(U)=\frac dD.
\]

Proof. Haar averaging `Gamma_k(U) rho Gamma_k(U)^dagger` gives an operator
`T` commuting with every mode unitary. Commutation with diagonal mode phases
makes `T` diagonal in the occupation basis: distinct occupation vectors have
distinct characters `exp(i sum_j t_j phi_j)`. Commutation with the generators
`a_i^dagger a_j` forces any two diagonal entries connected by moving one
photon to coincide, because their connecting matrix element is nonzero.
Every weak composition of `k` is connected to every other by such moves.
Thus `T=c I`; trace one gives `c=1/D`. Taking the trace against the
rank-`d` CF projector proves the formula. For `k=0` the space is one-dimensional
and both probabilities are one. No assumption of a Haar-random vector in the
full Fock space was used: the Haar action is only the mode-unitary action.

This is already contained in Arkhipov and Kuperberg, *The bosonic birthday
paradox*, [arXiv:1106.0849v1](https://arxiv.org/html/1106.0849v1),
Proposition 1, Corollary 2 and the distinct-birthday formula following Theorem 3.
The [published version](https://msp.org/gtm/2012/18/gtm-2012-18-001s.pdf),
pp. 2–4, has the same statements. Their `n` is our `m`. The claim is an
ensemble expectation; it is neither a bound for every `U` nor evidence of
an optimization benefit.

| m | k | d | D | E[P_CF] | 1/E[P_CF] |
|---:|---:|---:|---:|---:|---:|
| 4 | 2 | 6 | 10 | 3/5 = 0.6000000000 | 1.6666666667 |
| 6 | 3 | 20 | 56 | 5/14 = 0.3571428571 | 2.8000000000 |
| 8 | 4 | 70 | 330 | 7/33 = 0.2121212121 | 4.7142857143 |
| 10 | 5 | 252 | 2002 | 18/143 = 0.1258741259 | 7.9444444444 |

The last column is the CF waiting time when a new independent Haar unitary
is drawn for every attempt. For a Haar unitary drawn once and held fixed,
the ensemble mean waiting time is `E[1/P_CF]`, generally larger. It must not
be replaced by `1/E[P_CF]`.

## T-Scaling — Balanced-density asymptotic

**Status: PROVEN. Attribution: elementary specialization of T-Haar;
not claimed new.** For `m=2r`, `k=r`,

\[
R_m=\frac{(2r)!(2r-1)!}{r!(3r-1)!}
=\frac32\frac{((2r)!)^2}{r!(3r)!}
=\sqrt3\left(\frac{16}{27}\right)^r
\left(1-\frac1{36r}+O(r^{-2})\right).
\]

Apply `log(n!)=(n+1/2)log n-n+(1/2)log(2pi)+1/(12n)+O(n^-3)`
to the middle expression. Terms linear in `r` give `r log(16/27)`,
the constant is `(1/2)log 3`, and the `1/r` correction is `-1/(36r)`.
Equivalently,

\[
R_m\sim\sqrt3\left(\frac4{3\sqrt3}\right)^m,
\qquad -\frac{\log R_m}{m}\longrightarrow
\tfrac12\log(27/16)\approx0.2616240719.
\]

This dense regime does not satisfy the sparse birthday approximation's
`k=o(m^(3/4))` hypothesis; substituting `k=m/2` into `exp(-k^2/m)` is invalid.
The exponential decay applies to Haar averages, not to optimized circuits:
identity and permutations have `P_CF=1` at every `m`.

## T-Haar-Metrics — What Haar can and cannot enrich

**Status: PROVEN. Attribution: formal corollary of T-Haar and output symmetry.**
Let `A` be any fixed subset of the weight-`k` bitstrings, with size `M`, and
let `C` be any fixed real cost function on those bitstrings. Then

\[
\mathbb E P_A=\frac{M}{D},\qquad
\mathbb E[P_{A\mid\mathrm{CF}}]=\frac{M}{d},\qquad
\mathbb E E_{\mathrm{CF}}=\frac1d\sum_{x:\,|x|=k} C(x).
\]

For the conditional statements suppose `k<=m`, so CF probability is positive
almost surely. Indeed it is a real analytic nonnegative function of `U`, not
identically zero, so its zero set has Haar measure zero. Output mode
permutations preserve Haar measure, preserve CF probability, and act
transitively on CF outcomes. Therefore every ratio `p_U(x)/P_CF(U)` has the
same expectation; summing the ratios gives one, which fixes it to `1/d`.
This argument is essential: expectation of a ratio was not replaced by ratio
of expectations. It also gives

\[
\operatorname{Cov}(P_{\rm CF},P_{A\mid\mathrm{CF}})=0.
\]

No independence of these two random variables is asserted. For weighted graph
cut cost the edge-cut probability of a uniform weight-`k` string is
`2k(m-k)/(m(m-1))`, so for `m>=2`,

\[
\mathbb E E_{\mathrm{CF}}
=\frac{2k(m-k)}{m(m-1)}\sum_{(i,j)\in E}w_{ij}.
\]

Thus untrained Haar circuits have no mean conditional enrichment over direct
uniform feasible sampling. Their mean physical success probability is lower
by exactly `d/D`. This does not compare optimized algorithms.

## T-Pairs — Collision witness and exact collisionless classification

**Status: PROVEN by direct argument; novelty OPEN.** Now impose the stronger
input hypothesis of one photon in each of `k` distinct input modes `a=1,...,k`.
Set `q_ia=|U_ia|^2` and

\[
Q(U)=\sum_{i=1}^m\sum_{a<b}q_{ia}q_{ib},\qquad
M(t)=\sum_i\binom{t_i}{2}.
\]

Expanding `b_i=sum_a U_ia a_a` on this Fock input gives

\[
\mathbb E[n_i(n_i-1)]
=4\sum_{a<b}q_{ia}q_{ib},\qquad \mathbb E M=2Q.
\]

The factor four comes from the two orders of annihilating each occupied pair
and the two matching creation orders; equal-input annihilations vanish.
For `k>=2`, every colliding outcome satisfies
`1 <= M(t) <= K=binom(k,2)`, and every CF outcome has `M(t)=0`. Consequently

\[
\frac{2Q}{K}\le1-P_{\rm CF}\le\min(2Q,1).
\]

For `k=2`, `1-P_CF=2Q` exactly. For all `k>=1`,

\[
P_{\rm CF}=1
\iff q_{ia}q_{ib}=0\ \text{for every }i\text{ and }a\ne b
\iff \operatorname{supp}(U_{\cdot a})\text{ are pairwise disjoint}.
\]

Necessity follows from `M>=0` and the sum of nonnegative pair products;
sufficiency follows because two injected photons then cannot reach the same
output mode. With disjoint supports, every allowed output has exactly one
nonzero routing term in the permanent. Its probability is the product of
the `k` single-particle probabilities. Drawing one output mode independently
from each occupied column reproduces the entire output distribution in
`O(mk)` time per sample using elementary categorical sampling. In this exact
collisionless limit the indistinguishable and distinguishable distributions
coincide. This does not say that every low-collision circuit is efficiently
simulable to a useful accuracy; a quantitative approximation theorem remains open.

The factorial-moment method is standard; related exact moments appear in
Martinez and Font-Segura, [arXiv:2602.09894v1](https://arxiv.org/html/2602.09894v1),
Sec. 3.6. No claim is made that the support classification or bounds are new.
They exclude arbitrary entangled inputs and multiple photons in an occupied
input mode. For `k=0` the output is vacuum; for `k=1` the disjointness condition
is vacuous and `P_CF=1`.

## T-Pareto — Why there is no unrestricted Pareto obstruction

**Status: PROVEN; elementary negative result.** Let `A` be any nonempty set
of target `k`-subsets. Pick `S in A`, and choose a mode permutation carrying
the occupied input modes to `S`. Its output is `S` deterministically, hence

\[
(P_{\rm CF},P_{A\mid\rm CF},P_A)=(1,1,1).
\]

It dominates every other attainable point in the two probability coordinates.
A nontrivial Pareto curve must therefore specify a restricted ansatz,
preparation restrictions, entropy/diversity requirements, or a training budget.
Training to a known optimum supplies an oracle and measures state preparation,
not the computational difficulty of finding that optimum.

One useful restricted consequence of T-Pairs is that for `k>=2` no exactly
collisionless output can be a nontrivial mixture supported only on two disjoint
target `k`-subsets `S` and `T`. Indeed, disjoint-column supports give a Cartesian
product of categorical choices; changing any one nondeterministic choice
produces two outcomes differing in only one selected vertex. They cannot be
the two disjoint `k`-subsets. Thus a circuit supported only on `S,T` must be
deterministic. This statement requires the *only two supported outcomes*
hypothesis; it is not a bound on the success probability when other outcomes
are allowed. Whether a useful robust quantitative version holds is OPEN.
