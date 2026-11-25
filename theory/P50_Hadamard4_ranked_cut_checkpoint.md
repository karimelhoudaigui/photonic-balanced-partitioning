# A fourth-order effect survives balanced ranking at fixed Q, P and covariance

2026-11-25. Independent analytic checkpoint, separate from the frozen P50
pilot. No code, permanent enumeration script, graph generation, numerical run
or hardware call was used. The calculations below are finite algebra over
z on the unit circle. This is an illustrative FOUR-photon block; b4 and a
constant-size exact classical table reproduce it. It is NOT an optimizer
advantage or a new pilot/graph selection for P50.

## Frame and invariant lower-order data

For z=exp(i phi), define the passive unitary

    H(z)=1/2 [[1, 1,  1,  1],
              [1, z, -1, -z],
              [1,-1,  1, -1],
              [1,-z, -1,  z]].

Inject four identical photons, one in EACH input. All row norms are1 and
distinct rows are orthogonal when |z|=1. For every phi,

    Q_ia=1/4, P=H H*=I4, mu_i=1,
    Sigma_B=2 I4-J4/2,   Sigma_D=I4-J4/4.

The entire one-mode B law, not just its mean/variance, is phi independent:

    (p(0),p(1),p(2),p(3),p(4))=(15/32,1/4,3/16,0,3/32).

It follows either from the table below or from
G_i(zeta)=sum_h h! binom(4,h) (zeta-1)^h/4^h. However,

    per H(z)=(1+z^2)/4,
    P_B(1,1,1,1)=cos^2(phi)/4.                                    (1)

For a quick derivation of the permanent, expand along rows0 and2. Only
column subsets{0,2} and{1,3} have nonzero two-row permanents. Their unscaled
contributions are4z^2 and4; the overall1/16 gives (1).

## All35 Fock patterns and their compensations

Let O={{0,2},{1,3}} be the two opposite pairs and let X be the four remaining
cross pairs. Set t=cos^2(phi), u=sin^2(phi)=1-t. Probabilities below are PER
individual occupation pattern, including output factorial normalization.

| Occupation type | Which modes | Number | Probability |
|---|---|---:|---:|
| 4000 | any four-photon mode |4|3/32|
| 3100 | any ordered triple/single modes |12|0|
| 2200 | occupied pair in O |2|1/16|
| 2200 | occupied pair in X |4|t/16|
| 2110 | double mode and empty mode are opposite |4|u/8|
| 2110 | all other double/empty choices |8|0|
| 1111 | all four modes |1|t/4|

The35 patterns exhaust the full Fock space. Their mass is
3/8+1/8+t/4+u/2+t/4=1; no collision pattern is removed.

Here are independent amplitude reductions supporting the table. For rows a,b,
write rho_j=H_bj/H_aj. Flat unitarity gives sum_j rho_j=0. Then

    per(H with rows a,a,a,b)=3! prod_j H_aj sum_j rho_j=0,
    per(H with rows a,a,b,b)=4 prod_j H_aj e2(rho).

Thus P(2a,2b)=|e2(rho)|^2/64: opposite pairs have e2=-2, while cross pairs
have modulus |1+z^2|. For rows a,a,b,c, again using the vanishing ratio sums,

    per=-2 prod_j H_aj sum_j (H_bj H_cj/H_aj^2),
    P(2a,1b,1c)=|sum_j (H_bj H_cj/H_aj^2)|^2/128.

The latter sum vanishes unless the empty mode is opposite a, in which case
its squared modulus is16u. A repeated row four times gives per=4!prod_jH_aj
and probability3/32 after dividing by4!. These establish every table entry.

This variation really starts at total moment order4: all factorial moments
of total order<=3 are independent of phi. One-mode moments follow the fixed
PMF; for distinct modes the remaining third-order cases reduce from the table to

    E[(n_i)_2 n_j]=1/4,    E[n_i n_j n_k]=1/4.

In contrast E[n0 n1 n2 n3]=t/4, and for a cross pair
E[(n_i)_2(n_j)_2]=t/4. No covariance-only conclusion determines the full law.

## Exact top2 law: the compensations are not complete

Take alpha0, mu=1, and y_i=n_i-1+beta*zeta_i, with fresh iid continuous
Uniform[-1,1] jitter and **0<beta<1/2**. Integer count differences cannot
be inverted; tied counts are ranked uniformly. Equivalently use exact counts
with uniformly random tie-breaking. A fixed priority with beta0 is a DIFFERENT
rule and is not covered by these formulas. No1e-12 bucket is imposed here.

- 4000 includes its occupied mode and one of the other3 uniformly. For EVERY
  output pair, its two possible bunch origins contribute1/16 in total.
- 2200 returns its occupied pair with probability1.
- 2110 returns the double mode and either single uniformly. Only cross
  pairs receive this contribution; each receives u/8 from two possible doubles.
- 1111 returns each of the six pairs with probability1/6, adding t/24.

Consequently the output law is

    P_top2(O pair)=1/8+t/24,            each of2 pairs,
    P_top2(X pair)=3/16-t/48,           each of4 pairs.               (2)

Its total is1. At phi0 it is uniform1/6. At phi=pi/2 opposite pairs have1/8
and cross pairs3/16. Its TV from uniform is u/12, so the change in (1) DOES
survive the complete35-pattern ranking calculation; the compensations are
only partial. The two opposite pairs are complementary to each other, and
each cross pair has a complementary cross pair, so forgetting the side of
a balanced bisection also does not erase this change.

## Actual feasible-cut signs, controls and limits

For the unweighted graph K2,2 whose edge set is X, an O subset cuts4 edges
and an X subset cuts2. The true feasible mean therefore is

    E_B[C]=8/3-u/6.

For the complementary matching with edge set O, the costs instead are0 on
O subsets and2 on X subsets, giving

    E_B[C]=4/3+u/6.

Thus the same count change helps one fixed graph and hurts the other.
This is a sign calculation for actual feasible cuts, not a raw occupation
energy inference or a universal favorable encoding.

D is multinomial with uniform output probabilities, hence its top2 law is
uniform. Sphere is invariant under the full unitary H and is exchangeable;
the Gaussian with Sigma_B, independent final-variance Gaussian and independent
B-marginal product are also exchangeable here. All give uniform top2, with
means8/3 and4/3 on these graphs. Continuous fixed-modulus phase sampling is
NOT claimed invariant merely from P/Q; its law has not been derived here.
Most decisively, r4 is ONE b4 species block, so b4 is EXACTLY B. The35-entry
table itself is an exact constant-size classical sampler. These controls
prevent treating (2) or its1/6 improvement as an algorithmic positive.

This example refutes only a proposed closure of nonlinear feasible ranking
by Q/P/covariance, even by all one-mode laws and all moments of total order3.
It does not refute any scoped raw-quadratic identity or establish a scalable
route. The N4/r4/top2 setting is outside P50's fixed r<K panel and changes
none of its graphs, parameters or controls.

A larger flat Hadamard family would still keep Q/P and one-mode PMFs fixed,
but a useful continuation must FIRST establish a global ranked-cut effect
beyond b4/phase and constant-size/tensor/orbit classical controls, with a
graph-informed optimum-blind construction and paid preparation. Tensoring or
duplicating this block is not evidence of that implication. No such extension,
advantage, novelty or hardware feasibility is asserted or numerically tested.
