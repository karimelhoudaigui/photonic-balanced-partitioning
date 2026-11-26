# P112: independent manual audit of the origin Bernstein obstruction

26 November 2026. **PROVED AS WRITTEN as an analytic lemma and CONDITIONAL
application to the archived formal polynomials.** The physical identification
of their coefficients is an inherited, not independently reconstructed, leaf.
This is postdata review; no blind/predata-discovery claim is made.

Exact source: research/P112_ORIGIN_BERNSTEIN_OBSTRUCTION.md,70 lines,
ROOT commit535dd43ad67bd58749af189e73af9161e1f52004, SHA256
0c63d0ee9673d1c02a4265898d26d460473ed5efdee1a10b935774eb6497313b.
All70 lines were read. No original source, P110 code or contract was edited.

## Normalized statement and dependency graph

Let f=sum a_rs x^r y^s be a finite polynomial over Q, with
a_00=a_10=a_01=0 and a_11<0. For EVERY h,k>0 and finite integers
n>=deg_x(f),m>=deg_y(f), its unique tensor Bernstein expansion on
[0,h] times[0,k] has b_11=a_11 hk/(nm)<0. In particular n,m>=1.
No symmetry, sign of the other coefficients or positivity of f is required.
Rectangles may have unequal sides, and degrees may differ between boxes.

Dependencies: elementary binomial identity -> origin coefficient formula ->
failure of all-coefficients-nonnegative on a corner box -> failure of a WHOLE
finite rectangular certificate. Polynomial-specific application additionally
requires the stated archived low coefficients to be the physical mean contrast.
That last arrow is explicitly conditional, not supplied by this lemma.

## General lemma reconstructed

For degree n, the identity

    u^r=sum_(i=r..n) [binom(i,r)/binom(n,r)] B_i^n(u)

follows from binom(n,i)binom(i,r)=binom(n,r)binom(n-r,i-r)
and the binomial theorem. Tensor the two identities after x=hu,y=kv.
At index(1,1), only r,s<=1 survive. The three assumed zero coefficients
remove1,x,y, leaving precisely a_11 hk/(nm). The representation is unique
because the Bernstein products form a basis of coordinate degrees<=n,m.
Increasing either degree decreases the negative magnitude but never its sign.
The assertion is exact finite arithmetic, not a floating-point stopping rule.

Every complete P107 dyadic level contains [0,2^-L] squared. Its coefficient
is a_11 2^-2L/(nm), strictly negative for every finite L,n,m admissible.
More generally, any finite axis-aligned certificate containing a positive-area
origin rectangle fails the all-coefficients test on that rectangle. Adaptive
degrees or unequal rectangle widths do not rescue that SAME requirement.
Infinite limiting meshes, zero-area boxes, nonrectangular coordinates, or a
separate analytic treatment of the origin are outside this conclusion.

This is not a polynomial-negativity theorem: x^2+y^2-xy is positive away
from0 on the quadrant, yet satisfies this same obstruction. By itself a
negative Bernstein coefficient does not prove a negative function value.

## Literal archive checks and their limits

P110 was already frozen at0171e4622b7f7bb68831ad0cc65669dc07f8db09
before ROOT authorized this separate raw reading. I inspected the20
mean_coefficient rows with total degree<=3 and the two level0/box[0,0]/
index[1,1] Bernstein rows from the ORIGINAL P107 seal
99f2d98d93f13c7fc088218bfb06ff39af4c40e9, records file
research/P107_symbolic_filter_main/run_001/data/records.jsonl,
Git blob dc16e266095d6c64bce55d7a7a573b451eddcd1c, SHA256
b28ca55e337201240da88149d24ebabb8a5174481bd2821448e34c7f9d57b7b6.
These were text reads/hash metadata, not polynomial evaluation or execution.

| Archived coefficients of B minus D | PNR | Threshold |
|---|---|---|
| a00,a10,a01 |0,0,0|0,0,0|
| a20=a02 |581/6144|145/1536|
| a11 |-17/1024|-7/768|
| a30,a21,a12,a03 |0,0,0,0|0,0,0,0|
| degree(8,8), h=k=1, b11 |-17/65536|-7/49152|

Manual denominator conversion gives -102/6144=-17/1024 and
-14/1536=-7/768. Dividing a11 by64 reproduces both archived Bernstein
values. Thus the polynomial premises are faithfully quoted; no hidden cubic
term invalidates the displayed leading expansion. I did NOT independently
reconstruct all70 physical probabilities, all162 mean rows, or the complete
P107 provenance/engine. P113/another exact reconstruction remains a real
dependency for identifying this formal f with its optical mean contrast.

The two leading-form decompositions are exact: 51+530=581,-2*51=-102;
7+138=145,-2*7=-14. Both forms are positive definite. This supports local
positivity after a separate higher-order bound, not a sign on the square.

## Application and continuation scope

Conditioned on the coefficient identification, neither decoder can obtain
a complete direct rectangular Bernstein certificate by ANY finite extension
of levels/degrees that retains an origin box. This explains a limitation
of that method; it does not prove negativity, an all-filter no-go, a b1
result, a best-of-T comparison or a resource advantage. Original negatives
and INCONCLUSIVE evidence remain valid records, not failed physics to erase.

The proposed triangular charts cover the square and are algebraically sound:
x=u,y=uv sends x^i y^j to u^(i+j)v^j. Coordinate degrees<=8 therefore give
degrees<=(16,8); if every total degree is>=2, exact division by u^2 gives
degrees<=(14,8). The second chart swaps x,y. Their u=0 leading edge is a
positive quadratic in v under the quoted forms. This removes THIS original
coefficient argument only. It does not certify the transformed coefficients,
control the(1,1) boundary zero, or authorize a new computational population.

## Optional different route: prospective, NOT audited as a global proof

If the entire contrast is symmetric, write f=P(s,p), s=x+y,p=xy, using
x^r+y^r=s(x^(r-1)+y^(r-1))-p(x^(r-2)+y^(r-2)) for r>=2, starting at2,s.
The exact square domain is
0<=s<=2 and max(0,s-1)<=p<=s^2/4. A sufficient, sharply testable route is
to prove partial_p P<=0 on this domain and P(s,s^2/4)>=0 for0<=s<=2.
Monotonicity would then reduce the full square to a single univariate boundary.
Neither derivative sign nor the boundary inequality has been proved here;
failure of either sufficient test would not refute f>=0. The leading forms
become(581s^2-1264p)/6144 and(145s^2-304p)/1536, but leading-order
monotonicity must not be substituted for the missing global derivative bound.
This is a manual research obligation, not an executed plan or a new certificate.

Only this review was written. No import, AST, symbolic/numerical script, RNG,
native, test, graph, runner, QPU, manuscript, push or P110 modification occurred.
