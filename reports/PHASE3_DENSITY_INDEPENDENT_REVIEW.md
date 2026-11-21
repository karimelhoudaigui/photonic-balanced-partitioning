# Independent review of the density / expected-collision certificate

**Primary verdict: proved as written**, for the exact mathematical claims in
`theory/phase3_density_certificate.md` at commit
`75e5831a34b7bbf82ae21bb88894a2c12d4a6d47`. The floating-point function implements
these formulas, but its returned numbers are not rigorous outward-rounded upper
bounds. A reproducible cancellation witness is recorded below. This distinction
does not change the exact-theorem verdict. Novelty is not assessed here.

## Target, provenance and independence

The quantified object is an arbitrary complex Stiefel frame V in C^(m x k),
1 <= k <= m. The input contains exactly one photon in each of its k orthogonal
occupied orbitals. Both compared laws retain every k-photon Fock occupation;
the distinguishable law forgets particle labels after independent scattering
through the same columns. The positive number c must be a lower bound on
**every** positive row intensity. It is fixed in each asserted small-M
asymptotic. Zero rows may be removed; small positive rows may not be removed.

This review was performed by `/root/physics` in a new sparse isolated worktree
`phase3-density-review`, starting from the raw statement and reconstructing the
Fock laws rather than importing the implementation as their definition. The
reviewer did not author this density proof or its implementation. The reviewer
previously reviewed N1/N2; those are shared dependencies, not independent third
party evidence, and their unchanged source was checked again below. A different
agent identity or agreement is not itself evidence of correctness. No manuscript,
proof source, production source or test was edited; no QPU was called.

SHA256 of the exact inputs:

| Artifact | SHA256 |
|---|---|
| `theory/phase3_density_certificate.md` | `7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c` |
| `theory/near_collisionless_bound.md` | `30dc286d6a112c98a2be6c08d1a7223daad0ddb91eba6355966bbc31748ebbd3` |
| `src/photonic_balanced_partitioning/photonic/density_certificate.py` | `d301cc247726e49e32d09393cedb4167655debd40fceb0e9a501c863e0c9e26b` |

## Dependency graph and obligations

The exact proof has the following dependency graph; none of its leaves is a
numerical experiment or an unchecked external theorem:

1. Normalized bosonic creation-operator state -> full Fock probabilities and
   number moments -> definition of M as expected unordered collision pairs.
2. Full Fock probabilities -> spatial-Gram permanent bound N1.
3. Nonnegative weighted permutation cycles -> finite coefficient bound N2 ->
   convergent infinite-cycle envelope f(sigma).
4. Dominant row partition -> sigma <= 2 sqrt(delta)+delta -> TV envelope.
5. Row second moments and positive-density floor -> delta <= M/c.
6. Stronger row estimate + the preceding global bound -> small quadratic branch.
7. Explicit two-orbital rotation -> sharp leading support/refined constant.

| Obligation | Status | Decisive check |
|---|---|---|
| Fock factorials and M's factor of two | Passed | Creation-operator derivation below |
| N1 source in exact required form | Passed | Full outcomes, spatial Gram, halved TV reconstructed |
| N2 source in exact required form | Passed | Nonnegative cycles and Frobenius square root reconstructed |
| Dominant-support comparison | Passed | Entrywise Gram comparison and Frobenius inequalities |
| Density floor implication | Passed | Each nonzero row separately satisfies the inequality |
| Refined quadratic branch | Passed | Small branch follows from the independent coarse bound |
| Claimed Taylor coefficients | Passed | Envelope expansion; no per-circuit equivalence inferred |
| Independent weaker construction | Passed | Transformed row intensities <= 1 and number deviations |
| Balanced sharp family | Passed | All 10 Fock outcomes derived explicitly |
| Unary inputs, zero rows, ties, endpoint branches | Passed | Checked below |
| Floating implementation as exact numerical certification | Failed | Tiny-angle cancellation witness; no error padding |
| General utility, hardness, novelty or hardware performance | Out of scope | Not consequences of the theorem |

## Fresh derivation from Fock states

Write b_a^dagger = sum_i V_ia a_i^dagger. Orthogonality makes
`|Psi> = product_a b_a^dagger |0>` a normalized state: the b_a are independent
canonical occupied modes. For an occupation t with sum_i t_i=k, choose a list y
having these multiplicities. Expanding the product of creation operators gives

    p_b(t) = |sum_sigma product_j V[y_j,sigma(j)]|^2 / product_i t_i!.
    p_d(t) = sum_sigma product_j q[y_j,sigma(j)] / product_i t_i!.

The second formula counts independent labeled assignments with exactly the
required multiplicities; it is not a permanent amplitude. These formulas include
repeated output rows. They immediately give normalized laws on the same space.

For number moments, annihilating one photon gives E_b n_i = a_i. Annihilating
two selects an unordered pair of distinct occupied input orbitals; its two
orders add coherently. Orthogonality of the remaining input Fock states gives

    E_b[n_i(n_i-1)] = 4 sum_(a<b) q_ia q_ib
                    = 2(a_i^2 - sum_a q_ia^2).

Thus the paper's M is indeed E_b sum_i choose(n_i,2). In the independent law
the expected unordered pair count is M/2. M is not generally the probability of
any collision: configurations may contain several pairs. The source's
normalization has the correct bosonic enhancement.

### N1 and N2 checked from their exact source

Subtracting the diagonal amplitude products in the two displayed laws leaves
terms indexed by sigma != tau. The triangle inequality gives a nonnegative
function F(y) invariant under permuting y. The number of ordered lists of type t
is k!/t!, so summing F(y(t))/t! equals (1/k!) sum_y F(y). Summing each output
coordinate then contributes B_ab = sum_i |V_ia V_ib|. Each nonidentity relative
permutation occurs k! times. Consequently

    2 TV(p_b,p_d) <= Per(B)-1.

In particular the factorial and TV factors in N1 are correct. B is the Gram
matrix of the spatial amplitude moduli; it is not an internal distinguishability
Gram matrix. Its diagonal is exactly one.

For N2, let A=B-I, sigma=||A||_F, and count the nontrivial cycles in a
permutation contributing to Per(I+zA). Allowing cycles to overlap or repeat
only increases each coefficient, because all entries are nonnegative. The
simple cycles of length l contribute at most tr(A^l)/l. Symmetry of A gives
`0 <= tr(A^l) <= sum_j |lambda_j|^l <= sigma^l` for every integer l>=2;
the first inequality also holds for odd l by the closed-walk expansion.
Coefficientwise domination by

    exp(sum_(l>=2) (sigma*z)^l/l) = exp(-sigma*z)/(1-sigma*z)

follows. Comparison through degree k is formal and needs no convergence
assumption. Evaluating the full infinite majorant at z=1 needs sigma<1 and
gives `TV <= f(sigma)`. The density proof uses exactly this form of N2:
N2's earlier variable S equals sigma^2, not sigma. There is no missing square
root or unhalved-TV convention. These local N1/N2 proofs suffice without relying
on a literature attribution or an earlier review's verdict.

### Dominant support, density and the quadratic branch

Choose a maximizing column for each row, including any fixed tie choice.
For its groups S_g set C_ga=sqrt(sum_(i in S_g) q_ia). Every column of C has
norm one. Writing C=D+E with D diagonal gives ||D||op<=1 and
`||E||_F^2 = sum_a l_a = delta`; empty groups cause no problem. Groupwise
Cauchy gives B_ab <= (C^T C)_ab entrywise. Both diagonals equal one, so deleting
them preserves the comparison of nonnegative off-diagonal entries. Therefore

    sigma <= ||off(C^T C)||_F
          <= ||DE||_F + ||E^T D||_F + ||off(E^T E)||_F
          <= 2 sqrt(delta) + delta.

For the last step, the squared singular values of E give
`||E^T E||_F <= ||E||_F^2`. No dimension factor is hidden. Since
`f'(s)=exp(-s)*s/[2(1-s)^2] >= 0`, the claimed support envelope follows on
rho(delta)<1; otherwise only the trivial bound one is used.

For each row let h_i=max_a q_ia and d_i=a_i-h_i. Then
`sum_a q_ia^2 <= h_i a_i`, whence `M_i >= a_i d_i >= c d_i` on every
positive row. Zero rows contribute zero. Summing proves delta<=M/c.

The sharper estimate uses `sum_(a != maximizer) q_ia^2 <= d_i^2`:

    M >= sum_i 2 d_i(a_i-d_i)
      >= 2c delta - 2 sum_i d_i^2
      >= 2c delta - 2 delta^2.

This inequality alone would permit a large-root branch and would not prove
the stated refinement. The proof correctly first invokes delta<=M/c and
M<c^2/2, implying delta<c/2. The quadratic 2x(c-x) is increasing there;
its lower inverse is exactly
`d_c(M)=(c-sqrt(c^2-2M))/2=M/(c+sqrt(c^2-2M))`. The strict domain in the
statement is sufficient. No refinement is asserted beyond it.

Expanding the analytic envelope gives
`f(s)=s^2/4+s^3/6+O(s^4)` and hence
`f(2sqrt(x)+x)=x+O(x^(3/2))` as x->0. Also
`d_c(M)=M/(2c)+O(M^2)` for fixed positive c. These are upper-envelope
asymptotics, not equivalences for arbitrary physical laws. Letting c decay with
M would invalidate the fixed-c reading.

### Independent weaker argument and boundaries

For delta<1, l_a<=delta ensures every normalized restriction w_a exists.
Their disjoint supports make them orthonormal. In a basis extending them, put
q'_ia=|<w_i,v_a>|^2. Occupied diagonal entries are 1-l_i, and the total mass
of off-diagonal entries plus rows outside the first k is delta. Orthogonality
of the transformed frame implies a'_i<=1 (a diagonal entry of a projection).
For an occupied row, with off-diagonal mass r_i and diagonal d=1-l_i,
`M'_i <= (a'_i)^2-d^2 <= 2r_i`; thus
`E(n_i-1)^2 = 2M'_i-a'_i+1 <= l_i+3r_i`.
Outside the occupied rows, `E n_i^2=2M'_i+a'_i<=3a'_i`.
Their sum is at most 4delta. Every other fixed-number occupation has squared
integer distance at least two from (1,...,1,0,...), so its total probability
is at most 2delta. Pure-state trace distance is therefore at most sqrt(2delta)
(trivial when this exceeds one). Measurement cannot increase it. Coupling the
independent categorical draws to their restrictions fails with probability at
most `1-product_a(1-l_a)<=delta`. Disjoint supports make the two restricted
laws identical. The triangle bound in the source follows.

For k=1, M=delta=sigma=TV=0, with any zero rows harmless. For delta=0,
each positive row belongs to one occupied column, so disjoint-support equality
holds directly, including tied zero rows. The infinite envelope is used only
for rho(delta)<1, equivalently delta<(sqrt(2)-1)^2; reaching the cap one sooner
does not extend a nontrivial claim. The weaker construction is not used at
delta=1, where a restricted column could disappear. The balanced spectator
family has c=M=2/(k+2), delta=1 and TV=1/2; it lies outside a fixed-c limit
and outside the refined small-M branch. It is not a counterexample.

## Sharp family: full outcomes, not just grouped outcomes

Put epsilon=sin(theta)^2, t=epsilon(1-epsilon), with 0<=theta<pi/4.
After the two-column rotation, direct use of the Fock formulas gives:

| Physical occupation type | Count | p_b per outcome | p_d per outcome |
|---|---:|---:|---:|
| Same physical mode | 4 | t/2 | t/4 |
| Distinct physical modes within one group | 2 | t | t/2 |
| One physical mode in each group | 4 | (1-2epsilon)^2/4 | ((1-epsilon)^2+epsilon^2)/4 |

Both columns of probabilities normalize to one. The positive differences sum
to 2t and the negative differences to -2t; hence TV=2t. The collision moment
is the sum of the four same-mode bosonic probabilities, also 2t. Each row
intensity is 1/2 and delta=2epsilon, proving
`TV=M=delta(1-delta/2)` on the full Fock space. Thus TV/delta tends to one.
At c=1/2 the refined leading coefficient 1/(2c)=1 cannot be uniformly reduced.
N1 is itself saturated here: B12=2cos(theta)sin(theta), and B12^2/2=M.
No many-body or complexity claim follows from this two-photon example.

## Implementation limitation and retained finite checks

`density_certificate.py` matches the exact formulas and domain branches. Its
checks accept orthogonality within 1e-10 and implication discrepancies within
1e-9. These checks do not make its outputs rigorous numerical upper bounds.
Subtraction in `a_i^2-sum q_ia^2` and `a_i-max q_ia` can erase small positive
terms, and a tolerance is not added to the returned envelope.

The retained witness uses the same physical family with theta=1e-10. Its
floating frame has orthogonality residual 3.1401849173675503e-16. The function
returns raw M=raw delta=0, all density/support bounds zero, but spatial Gram
sigma=2.82842712474619e-10 and direct Gram bound
2.0000012290007522e-20. The analytic physical family's TV is approximately
2.0000000000000002e-20. This is cancellation at negligible absolute scale,
not a counterexample to the exact Stiefel theorem. It does refute interpreting
every returned float as an exact certificate with no numerical allowance.
The raw fields alone do not reveal the lost positive contribution. No source
repair was made within this read-only review. For rigorous machine certification,
error propagation or outward rounding remains a separate implementation task.

The independent script uses rational Pythagorean rotations at parameters
0, 1/1000, 1/100, 1/10 and 1/3 and enumerates all 10 physical two-photon
occupations for each. It verifies exact normalization, the Fock collision
moment, M, delta, TV and the finite k=2 N1/N2 equality, retaining all 50
probabilities as rational strings. It includes both sides of the refined
small-M domain. These finite checks are not used as proof of the universal
inequalities. No random selection or optimization is involved.

Reproduction command, from this worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 /Users/karimelhoudaigui/Desktop/pasqal/.venv/bin/python experiments/P33_density_review/check.py
```

Environment: Python 3.11.15, NumPy 2.4.6. Result: five exact cases / 50 Fock
outcomes passed, and the floating-point limitation was reproduced. Receipt:
`experiments/P33_density_review/receipt.json`, SHA256
`47f725251fe992fe187da2557a45ce5e7d11bb4e20d9c2a8708e3c9687e1d7e5`.
Production tests were not rerun for this documentation-only review; no product
source changed. The initial full checkout failed for lack of disk space; a
sparse checkout of the same commit resolved that without deleting prior data.

## Remaining obligation and safe conclusion

There is no remaining mathematical gap identified in the stated exact claims.
The safe result is a sufficient absolute-TV certificate under the specified
source, density floor and branch conditions, with a sharp leading constant
at c=1/2. It is not a relative rare-event guarantee, a statement about
reoptimized interferometers, a necessary condition for classical simulation,
or a proof of useful experimental regimes. Numerical error certification and
novelty remain separate obligations. The cheapest next implementation check is
the retained tiny-angle witness with an explicit numerical error budget; no
larger sweep or hardware run is needed to establish that limitation.
