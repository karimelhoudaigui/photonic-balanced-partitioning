# Independent audit of the near-collisionless certificates

**Primary verdict: proved as written**, for N1–N4 under the stated ideal passive lossless model and a Fock input with one photon in each of `k` distinct modes. No internal mathematical gap was found. This verdict does not address novelty, hardness, hardware performance, or the prior-work attribution paragraph.

Reviewed source: `theory/near_collisionless_bound.md`, SHA256
`30dc286d6a112c98a2be6c08d1a7223daad0ddb91eba6355966bbc31748ebbd3`.
The source hash was checked before and after the independent numerical checks and did not change. Review date: 2026-11-20. Review performed by a separate physics-auditor agent, using an independent derivation and an autonomous `/tmp` implementation. This is an independent agent review, not a formal proof certificate; the reviewer and author can share model errors.

## Claim card and conventions

For every `m>=k>=1`, let the first `k` columns of a unitary describe `k` initially distinct occupied modes. Compare the complete bosonic occupation distribution `p` with the complete independent labeled-particle distribution after forgetting labels, `d`. Both are normalized over all weak compositions of `k` into `m` parts. Total variation is the **halved** L1 distance, not L1 itself. Neither distribution is conditioned on collision-free events.

The proposed certificates use the real spatial-overlap Gram matrix
`B_ab=sum_i |U_ia||U_ib|`, its zero-diagonal off-diagonal part `A=B-I`, and `S=sum_ab A_ab^2`. These quantities are not an internal-photon distinguishability matrix. N1 bounds TV by `(Per(B)-1)/2`; N2 replaces the permanent with `H_k(S)/2`; N3 gives a weaker dimension-dependent bound from the bosonic collision probability. N4 disproves a dimension-uniform implication from small bosonic collision probability to closeness to the distinguishable distribution, including at balanced density.

The input assumption is essential. This audit does not extend the claims to bunched inputs, arbitrary entangled input states, loss, additional photons, or adaptive devices.

## Dependency graph

- Normalized Fock transition amplitudes and labeled-particle occupation counting -> N1.
- Directed-cycle decomposition of permutations, nonnegative coefficients, symmetric spectral bound -> `Per(B)-1 <= H_k(S)` -> N2 using N1.
- Direct bosonic second factorial moment, bounded pair-count observable, Cauchy–Schwarz -> `S <= m*binom(k,2)*delta` -> N3 using N2.
- Explicit two orthonormal occupied columns and direct two-photon probabilities -> fixed-TV low-collision family; tensoring with deterministic spectator modes -> balanced N4.

Every leaf needed for N1–N4 is internal and elementary. The moment identity was rederived below rather than accepted solely by reference to T-Pairs. No literature theorem or numerical result is load-bearing in the universal conclusions.

## Obligation matrix

| Obligation | Finding |
|---|---|
| Correct complete-output sample space and TV convention | Passed |
| Input/output factorials, including repeated output modes | Passed |
| Relative-permutation multiplicity in N1 | Passed |
| Identity term `Per(B)` equals one | Passed |
| Cycle orientations and rotation multiplicities in N2 | Passed |
| Exponential coefficient domination despite factorial denominators | Passed |
| Trace bound for odd as well as even powers | Passed |
| Formal-series argument when `S>=1` | Passed |
| Derangement coefficients and geometric simplifications | Passed |
| Arithmetic-operation complexity claim | Passed, in the stated arithmetic-operation model |
| Bosonic moment factor two/four and collision inequality | Passed |
| Fixed-size versus dimension-uniform limits | Passed |
| Physical realizability and normalization of N4 | Passed |
| Spectator mode/particle counts and TV invariance | Passed |
| Internal-variable versus spatial-overlap distinction | Passed |
| Novelty, attribution, useful computational speedup | Out of scope |

## Independent reconstruction of N1

For an occupation `t`, fix any ordered list `y` containing its repeated output rows. A routing permutation contributes `a_sigma=prod_j U[y_j,sigma(j)]`. The bosonic probability is `|sum_sigma a_sigma|^2/t!` where `t!=prod_i t_i!`. The independent occupation probability is `sum_sigma |a_sigma|^2/t!`: each distinct assignment of labeled particles to output modes occurs `t!` times when the repeated row positions are permuted. Thus the same denominator is required in both expressions.

After subtracting, the diagonal routing pairs cancel. The triangle inequality bounds `|p(t)-d(t)|` by `F(y)/t!`, where `F` sums the magnitudes of all ordered unequal routing pairs. Since `F` is invariant under permutations of `y`, summing over occupations equals `1/k!` times summing over all ordered output lists: each occupation contributes `k!/t!` such lists. This removes the output-factorial issue exactly, including collisions.

For fixed routing permutations `sigma,tau`, the sum over all output lists factorizes into `prod_j B[sigma(j),tau(j)]`. Define the relative permutation on input labels by `pi(a)=tau(sigma^{-1}(a))`. Each `pi` occurs for exactly `k!` choices of `sigma`, so the factor `1/k!` cancels. Removing `pi=id` removes precisely the unit diagonal product. Consequently `sum_t |p(t)-d(t)| <= Per(B)-1`, and halving gives N1. The general cap TV<=1 and the case `k=1` are correctly handled.

## Independent reconstruction of N2

For any nonnegative symmetric zero-diagonal matrix `A`, a term in `Per(I+zA)` is a set of disjoint directed cycles on moved vertices. Cycles are counted modulo rotation, not modulo reversal. This convention handles 2-cycles correctly: a 2-cycle is one object and contributes twice to `tr(A^2)`.

In `exp(sum_c w_c z^{length(c)})`, every disjoint cycle collection appears with its full weight and coefficient one: its cycles are distinct and each is selected once. Terms with overlapping or repeated cycles add nonnegative contributions. The factorial denominators for repeated cycles therefore do not reduce the coefficient of any legal disjoint collection. This proves the first coefficientwise bound independently of numerical data.

Every simple directed cycle of length `l` occurs `l` times in `tr(A^l)`, with other closed walks adding nonnegative weight. Hence `C_l <= tr(A^l)/l`. As `A` is real symmetric, its eigenvalues are real. For every `l>=2`, including odd `l`,

`0 <= tr(A^l) <= sum_j |lambda_j|^l <= (sum_j lambda_j^2)^(l/2) = S^(l/2)`.

The left inequality uses entrywise nonnegativity and the closed-walk interpretation, rather than incorrectly assuming all eigenvalues are nonnegative. The last inequality is the finite-dimensional norm inequality. Substitution into an exponential of formal series with nonnegative coefficients preserves coefficientwise domination.

Finally, `exp(sum_{l>=2} x^l/l)=e^{-x}/(1-x)`. Its coefficient of `x^r` is `!r/r!`, either by multiplying the two series and using inclusion-exclusion, or by counting permutations with no 1-cycles. Only coefficients through degree `k` are used. There is no evaluation of a divergent infinite series at `z=1` when `S>=1`; the permanent polynomial's finite coefficient sum is bounded by the finite polynomial `H_k(S)`. This is the critical justification for N2 over all `S>=0`.

The secondary closed form is appropriately restricted to `S<1`. Using `!r/r!<=1/2` gives `TV<=S/[4(1-sqrt(S))]`. At `S<=1/4` this is at most `S/2`. The stated leading expansion `S/4+O(S^(3/2))` is an asymptotic statement, not an incorrectly truncated global upper bound. Exact connected components factor the permanent, so the stated component tightening is valid if components use exact zeros.

## Independent reconstruction of N3

Write `n_i=b_i^dagger b_i`, with `b_i=sum_a U_ia a_a`. On the stated Fock input, equal-input double annihilation vanishes. For two different occupied inputs, two annihilation orders and two matching creation orders contribute. Therefore

`E[n_i(n_i-1)] = 4 sum_{a<b} |U_ia|^2 |U_ib|^2`.

After division by two and summation over `i`, `E[M]=2 sum_{i,a<b}q_ia q_ib`. Pointwise, `M=0` on CF states and `1<=M<=binom(k,2)` on collisional states. Thus `E[M]<=K*delta` with the **bosonic** `delta` in the claim. Pairwise Cauchy–Schwarz gives `B_ab^2<=m sum_i q_ia q_ib`. Summing both orientations gives `S<=m E[M]<=mK delta`, without a missing factor of two.

For `k=2`, `H_2(s)=s/2`, so the unclipped N3 bound reduces to `TV<=m*delta/4`. At fixed `m,k`, this tends to zero. For `m=2k`, its sufficient small-argument regime is of order `delta~m^-3`, with the stated conservative small constant. None of this implies a uniform modulus of continuity in `delta` across dimensions.

For every fixed event, including a fixed optimum set, the event-probability difference is at most TV. The text correctly avoids extending this to reoptimized circuits or to a ratio of waiting times.

## Independent reconstruction of N4 and attempted falsification

The proposed active columns have unit norms and zero inner product for even `L`. They are therefore valid occupied columns of a unitary by orthonormal completion.

For a repeated output `i`, the bosonic probability is `2|u_i v_i|^2=2/L^2`, and the distinguishable probability is `|u_i v_i|^2=1/L^2`. For distinct outputs `i<j`, the bosonic amplitude is `(sign_i+sign_j)/L`, giving probabilities `4/L^2` for equal signs and zero for opposite signs. The independent probability is always `2/L^2`.

There are `L` repeated-mode outcomes, `2*binom(L/2,2)=L(L-2)/4` equal-sign pairs, and `L^2/4` opposite-sign pairs. Both distributions sum to one. Positive probability difference is `1/L+(L-2)/(2L)=1/2`; the negative difference is also `1/2`. Hence halved L1 distance is exactly `1/2`, while bosonic collision probability is `2/L`. This also confirms the two saturation claims: `Per(B)-1=1` and `m*delta/4=1/2`.

For balanced density, `L=k+2` active modes plus `k-2` spectator modes gives exactly `m=2k` modes and `k` photons. The spectators occupy separate deterministic modes. Their output law is identical in both models and introduces no extra collisions. Tensoring with this deterministic law preserves TV and preserves the active collision probability. Reordering input columns merely restores the standard first-`k` occupied-input convention. Even `k` supplies an infinite balanced sequence; this is sufficient to refute any dimension-uniform bound tending to zero with `delta`.

The construction is easy to classically sample. Its conclusion is correctly limited to failure of the independent-particle approximation based on collision probability alone.

## Executed autonomous falsification checks

A separate implementation used explicit routing permutations and independently generated weak compositions; it imported neither the repository's bosonic simulator nor its CF evaluator. No QPU was used.

Command:

```sh
MPLCONFIGDIR=/tmp/pasqal-matplotlib PYTHONPATH=src .venv/bin/python /tmp/near_collisionless_independent_audit.py
```

Script SHA256: `fbc556d4e992772152e1acce57397a8ac9e900fadd8a1ebe0e93cc533a0d5bcf`.
Output: `/tmp/near_collisionless_independent_audit_results.json`. Seed: `472019` using NumPy `default_rng`/PCG64. Environment: Python 3.11, NumPy 2.4.6, SciPy 1.17.1. Actual runtime was approximately 1.96 seconds, exit status zero. These `/tmp` checks are supporting falsification attempts, not the durable experiment dataset or a substitute for the analytic argument.

- **84 physical cases:** `(m,k)=(2,1),(2,2),(3,2),(4,2),(4,3),(6,3),(8,4)`, each with six Haar matrices and six near-identity Hermitian exponentials at parameters `0,1e-5,.001,.01,.1,.5`. Checked complete normalization, N1, N2, N3 and the bosonic pair-count identity. No violations at the explicit floating tolerances `1e-10`/`1e-9`.
- **140 coefficient tests:** twenty nonnegative symmetric zero-diagonal matrices at each `k=2,...,8`, including sparse and small-magnitude cases. Enumerated all permutations and each moved-vertex coefficient of `Per(I+zA)`; none exceeded the corresponding `!r/r! * S^(r/2)` coefficient bound. This is broader than physical Gram matrices but still finite sampling.
- **Active counterexample:** full distributions at `L=2,4,6,8,16,32,64` produced `(delta,TV)` equal to `(2/L,1/2)` up to floating roundoff. At `L=64`, `delta=.03125`, `TV=.5`.
- **Balanced embedding:** explicit full `m=8,k=4` Fock distribution produced `delta=.33333333333333354`, `TV=.5000000000000003`, agreeing with `2/(k+2)` and `1/2`.

These checks are conditional on floating-point arithmetic and sampled matrix families. They do not establish the universal theorem; the independently reconstructed inequalities above do.

## Remaining obligations and strongest safe interpretation

No missing implication remains in N1–N4 under their stated assumptions. The safe result is a sufficient, efficiently computable spatial-overlap certificate for closeness to one particular classical independent-particle sampler, together with an explicit obstruction to obtaining such closeness from low collision probability uniformly over growing balanced systems. Bounds can be vacuous for many useful circuits. Failure of a certificate says nothing about hardness or quantum utility. Novelty and practical usefulness remain separate open research obligations.
