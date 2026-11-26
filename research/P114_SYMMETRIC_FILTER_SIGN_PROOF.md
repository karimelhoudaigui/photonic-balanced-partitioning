# P114: an analytic sign certificate after the rectangular obstruction

26-Nov-2026. Manual postdata derivation for independent proof audit.
The theorem here is about two explicitly specified rational polynomials.
Their identification with the P107 physical raw means is a separate
computational dependency, pending independent P113 reconstruction. This
does not supersede the original P107 INCONCLUSIVE certificate result.

## Exact statement

For x,y in[0,1], define u=(x-y)^2 and v=xy. Define fP and fT by

    6144 fP = A0P(v)+u A1P(v)+u^2 A2P(v)+u^3 A3P(v),
    3072 fT = A0T(v)+u A1T(v)+u^2 A2T(v)+u^3 A3T(v),

with the following complete coefficient lists, in ASCENDING powers of v:

| Polynomial | Complete coefficients |
|---|---|
|A0P|0,1060,-1752,796,-720,540,296,-220|
|A1P|581,-1130,3451,-1324,59,-106,5|
|A2P|-228,708,-1280,68,-36|
|A3P|5,-230,5|
|A0T|0,552,-832,280,-256,152,192,-88|
|A1T|290,-444,1662,-520,-34,68,2|
|A2T|-81,340,-502,20,15|
|A3T|2,-92,2|

Then the following uniform lower bounds hold:

    6144 fP >= 1060 v(1-v)^2 +95u,
    3072 fT >= 552 v(1-v)^2 +124u.                 (1)

In particular both polynomials are strictly positive on the square except
at(x,y)=(0,0) and(1,1), where they vanish. No derivative monotonicity,
floating-point estimate, numerical positivity package or adaptive mesh is
used in the proof.

## Domain geometry

We have 0<=v<=1 and u>=0. More strongly,

    (1-v)^2-u=(1-x^2)(1-y^2)>=0.                 (2)

Thus 0<=u<=(1-v)^2<=1. For0<=v<=1 the elementary maximum bounds are

    v(1-v)<=1/4,
    v^2(1-v)<=4/27,
    v(1-v)^4<=256/3125.                         (3)

The first follows by completing the square. Differentiation gives the
second maximum at v=2/3, and the third at v=1/5; endpoints give zero.
These are exact rational inequalities, including all endpoints.

## Diagonal factors

Direct multiplication yields

    A0P=v(1-v)^2 QP,
    QP=1060+368v+472v^2-144v^3-220v^4,
    A0T=v(1-v)^2 QT,
    QT=552+272v+272v^2+16v^3-88v^4.

Since v^3,v^4<=v^2 on this interval,

    QP>=1060+368v+108v^2>=1060,
    QT>=552+272v+184v^2+16v^3>=552.              (4)

## Positive off-diagonal remainder: PNR polynomial

Let GP=A1P+u A2P+u^2 A3P, so6144 fP=A0P+u GP.
Dropping positive terms and using v^3,v^5<=v^2 gives

    A1P>=581-1130v+2021v^2>=423.                (5)

For the last inequality the quadratic after subtracting423 has leading
coefficient2021>0 and discriminant
1130^2-4*2021*158=-372<0; thus it is strictly positive on all real v.
Likewise A2P>=-228-1280v^2-36v^4. Using(2),(3),

    u A2P>=-228-1280/16-36*16/729
           =-308-64/81 > -309.                 (6)

Here uv^2<=[v(1-v)]^2 and uv^4<=[v^2(1-v)]^2;
the positive terms discarded from A2P do not invalidate the lower bound.
Finally A3P>=-230v, hence

    u^2 A3P>=-230 v(1-v)^4
             >=-58880/3125 > -19.             (7)

Equations(5)--(7) imply GP>=95, and(4) proves the first inequality(1).

## Positive off-diagonal remainder: threshold polynomial

Let GT=A1T+u A2T+u^2 A3T. Since v^3,v^4<=v^2,

    A1T>=290-444v+1108v^2>=245.                (8)

The quadratic after subtracting245 has discriminant
444^2-4*1108*45=-2304<0. Also A2T>=-81-502v^2 and A3T>=-92v.
Consequently

    u A2T>=-81-502/16=-899/8 > -113,
    u^2 A3T>=-92*256/3125=-23552/3125 > -8.    (9)

It follows that GT>=124. Equations(4),(8),(9) prove the second inequality(1).
If u>0 the bound is strictly positive; if u=0 then x=y, and
v(1-v)^2 is positive except when x=y=0 or x=y=1. This proves the stated
zero set as well as the sign. No negative Bernstein coefficient is removed
or reinterpreted by this different certificate.

## Computational identification still to close

The table was obtained MANUALLY from the symmetric nonzero P107
mean_coefficient records at original seal99f2d98d93f13c7fc088218bfb06ff39af4c40e9.
All powers have equal parity, so paired monomials reduce using

    x^2+y^2=u+2v,
    x^4+y^4=u^2+4uv+2v^2,
    x^6+y^6=u^3+6u^2v+9uv^2+2v^3.

Multiply each pair by v to the smaller original exponent; diagonal terms
are powers of v. These identities explain the table but do not replace a
complete independent coefficient comparison. P113 was frozen BLIND before
this derivation, using Ryser and void/2110 identities. Its future run must
close the physical identification, rather than taking this table as an
oracle. An additional exact table-identity check can be separately frozen
if needed. Current status: analytic proof candidate; independent review and
physical polynomial identification pending.

If identified, fP and fT are E_B[C]-E_D[C] for the SPECIFIC P101 weighted
four-vertex graph and its two fixed all-output decoders, at the SAME
T=Fdiag(1,x,xy,y)Fdagger. Positivity would refute a mean improvement on this
family for that graph; it would not refute all graph encodings, graph sizes,
adaptive hybrids, weighted cycles, detector policies or a quantum advantage
in general. No matched-clock claim, priority, hardware result or claim of
optimum-blind optimizer success follows. CLAIM-042 remains OPEN.
