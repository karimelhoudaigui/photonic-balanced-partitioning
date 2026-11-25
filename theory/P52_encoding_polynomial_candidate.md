# P52 candidate reduction: exact low-degree polynomials for the continuous phase family

25-Nov-2026. Analytic source-only derivation, after the four-cell P52 run but
without any new numerical operation, source import, graph, sample or data edit.
This is a proposed exact reduction for independent review, not a proved
continuous convex replacement, optimizer result or novelty claim. It does not
modify the frozen P52 experiment. The phase source and CF/Fock conventions are
those of `research/P52_COLLECTIVE_PHASE_CARD.md`.

## Integer creation polynomials and normalization

Write x=exp(i theta), and let z0,...,z7 be commuting creation indeterminates.
Every source-matrix entry is

    U_ia(x)=s_ia x^(e_ia)/sqrt(8),   s_ia in{+1,-1},
    e_ia=0 for a<4, and e_ia=i mod4 for a>=4.

The source occupies every input ONCE. Therefore its unnormalized creation
polynomial before applying the vacuum is

    F_x(z)=1/8^4 * product_(a=0)^7 sum_(i=0)^7 s_ia x^(e_ia) z_i
          =1/8^4 * sum_(|n|=8) c_n(x) z^n.

Each c_n is an INTEGER polynomial of degree at most12: only the last four
input factors carry an x power, each at most3. No square root is necessary
when computing these monomial coefficients. Normalized Fock amplitudes then
are

    A_n(theta)=sqrt(product_i n_i!)*c_n(exp(i theta))/8^4,
    p_n(theta)=product_i n_i! /8^8 * c_n(x)c_n(x^-1).                (1)

Here c_n is the UNNORMALIZED INTEGER numerator coefficient: the actual
coefficient of z^n in F_x is c_n/8^4. The output factorial multiplies (1)
because monomial creation on the vacuum has norm sqrt(product_i n_i!).
Equivalently, the permanent of U with output rows repeated n_i times is
product_i n_i! * c_n/8^4; its probability divides by the output factorial.
Input factorials are1 for this CF source.

## Exact evenness and the six-degree real parameter

For the given W, diag(1,-1,1,-1)W=W P_sigma with sigma=(0 2)(1 3).
Consequently replacing x by-x permutes the last four source factors of F_x.
Bosonic creation factors commute, so

    F_(-x)(z)=F_x(z),   c_n(-x)=c_n(x)                             (2)

as formal polynomial identities, not merely equality on the unit circle.
Thus c_n(x)=d_n(x^2) with d_n integer of degree at most6. All coefficients
are real. Multiplying d_n(t)d_n(t^-1), t=exp(2i theta), gives a symmetric
integer Laurent polynomial with powers-6,...,6. On the unit circle,

    p_n(theta)=product_i n_i!/8^8 *
        [a_n0 + 2 sum_(h=1)^6 a_nh cos(2h theta)],   a_nh integer.

With y=cos(2 theta) and integer Chebyshev polynomials T_h, every individual
occupation probability is an element of 8^-8 Z[y], degree at most6. This
statement covers ALL6435 occupations, including zero polynomials; it does not
truncate a harmonic or discard a collision sector.

## Exact uniform ties preserve degree and a fixed denominator lattice

For a fixed occupation n, the top4 pushforward T_n,S is0 or1/binom(t,b),
where t is the number tied at the fourth-count threshold, h the number
strictly higher, and b=4-h. Necessarily0<=h<=3, h+t<=8 and1<=b<=t.
Enumerating only these small integer constraints gives possible denominators
within

    {1,2,3,4,5,6,10,15,20,35,70},

all dividing420. This list is a safe superset; realizing each denominator
with a physical occupation is not needed for the common-denominator claim.
The tie rule is independent of theta. Consequently every ranked subset
probability q_S(theta)=sum_n T_n,S p_n(theta), and every edge-crossing mean,
is a polynomial in y=cos(2 theta) of degree at most6 with rational
coefficients in

    1/(420*8^8) Z.

Every such kernel also satisfies the exact linear identities: incident edge
sum4 at each vertex and total28-edge sum16. These relations constrain the
coefficient vectors but alone imply no convex replacement or favorable sign.

## What this would and would not settle

The frozen four cells evaluate y at1,0,-1,0. They are only THREE distinct
abscissae. A degree-six bound therefore does NOT justify interpolating a
continuous family from those cells, and four successful numerical mean fits
do not prove continuous convex inclusion. Terms vanishing at-1,0,1 could
still remain; no conclusion about them is inserted into P52's report.

An exact integer-coefficient creation DP could construct (1), autocorrelate
its short coefficient arrays, and average ties with denominator420. That is
a FUTURE computation requiring a new frozen contract/review/slot, not work
executed by this note. Its exact polynomial identities could then be reviewed
without interpreting small floating residuals as proofs.

For a possible continuous certificate, b4 controls at fixed phases0 andpi/2
have rational mean kernels as well (their entries are signs or i times
1/sqrt8). Let M contain those70 kernels plus uniform4/7. Finding polynomial
weights lambda_v(y) with

    M.T lambda(y)=c_B(y),   sum_v lambda_v(y)=1,
    lambda_v(y)>=0 for all y in[-1,1]

would be sufficient for a continuous mean replacement. It is NOT asserted
that such weights exist. Exact rational facet inequalities or explicit
nonnegative Bernstein/SOS/interval certificates are alternative future
routes. Neither the current floating coefficients nor a solver status
provides that certificate. Full70-subset laws, tails, best-of-shots,
arbitrary modes/sources/decoders, efficient graph optimization and the user's
hardware objective remain outside this candidate reduction.
