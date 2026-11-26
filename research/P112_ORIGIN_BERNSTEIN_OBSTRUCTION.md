# P112: origin obstruction to the direct rectangular certificate

26-Nov-2026. A manual postdata mathematical claim for independent review.
This concerns a certificate method, not the physical sign or all photonic
optimization. Polynomial-specific premises below are extracted from original
P107 raw seal99f2d98; independent reconstruction P113 is still pending.

## General lemma

Let f in Q[x,y] have constant coefficient and both linear coefficients zero,
and coefficient a11<0 of xy. On any positive-area origin rectangle
[0,h]x[0,k], h,k>0, its tensor Bernstein representation at any finite
bidegree(n,m) at least its actual bidegree has coefficient

    b11 = a11 h k / (n m) < 0.

Proof: substitute x=hu,y=kv. In degree(n,m), the monomial u^r v^s has
Bernstein coefficient at(i,j) equal to
binom(i,r)/binom(n,r) times binom(j,s)/binom(m,s), with value zero if
r>i or s>j. At(i,j)=(1,1), only monomials1,x,y,xy can contribute.
The first three have zero coefficients, proving the formula. The degrees
n,m are positive because a11 is nonzero. The identity follows directly
by the binomial theorem, so no external positivity theorem is required.

Consequently no complete finite dyadic level of positive-area rectangular
boxes of the form used in P107 can have all Bernstein coefficients
nonnegative: its origin box always fails. Arbitrary finite degree elevation
does not repair this. More generally this conclusion applies to any finite
axis-aligned rectangular subdivision containing an origin rectangle of
positive area. It is not a statement about every possible positivity method.

## Conditional application to P107

The exact PNR mean difference f=E_B[C]-E_D[C] begins

    f = [581(x^2+y^2)-102xy]/6144 + terms of total degree >=4.

The threshold difference begins

    f = [145(x^2+y^2)-14xy]/1536 + terms of total degree >=4.

Thus a11=-17/1024 and -7/768 respectively, while a00=a10=a01=0.
These are computational premises, not a new independent derivation of the
physical law. Conditional on them, the general lemma excludes completion
of the direct P107 rectangular method at any further finite subdivision
level or finite elevated tensor degree. This explains an INCONCLUSIVE
certificate; it does not mean that either function is ever negative.

Indeed the leading forms are positive definite:

    581(x^2+y^2)-102xy = 51(x-y)^2+530(x^2+y^2),
    145(x^2+y^2)-14xy = 7(x-y)^2+138(x^2+y^2).

They are strictly positive except at the origin. Higher-degree terms still
require global control, including other boundary zeros; this observation
alone is not a global proof.

## Changed route, not a rerun

A prospective continuation can exploit symmetry and use the two triangular
charts (x,y)=(u,uv) and (uv,u), 0<=u,v<=1. These cover the square, including
u=0. Actual substituted degrees can reach(16,8), and must not be truncated
to(8,8). If every monomial has total degree>=2, factor the exact common u^2;
the remaining polynomial has degree at most(14,8). Its u=0 edge is a
positive quadratic in v, avoiding the lemma's original xy premise. This
does not guarantee a certificate, handle the(1,1) zero or authorize execution.
An exact sum-of-squares decomposition is a different possible continuation.
Freeze a new method/population before any load-bearing computation. Keep
the original P107 verdict and all failed coefficients. No global no-go or
positive optimization result is claimed.
