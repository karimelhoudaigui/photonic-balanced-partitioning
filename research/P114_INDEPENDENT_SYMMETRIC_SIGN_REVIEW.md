# P114 independent symmetric-sign proof review

2026-11-26. Non-author adversarial MANUAL proof audit.
Full source: ROOT `b61b6a9c60943f937541a67d77dab7de112919dc`,
`research/P114_SYMMETRIC_FILTER_SIGN_PROOF.md`, 137 lines.
SHA256 `32e3a726357ee583c71ff7600300b4427b24fdc1485ea5f2a8de4b26a1be74a5`.
Review parent: `7267e6a4ce544772cf8f5018988e142940c9586e`.

**PROVED AS WRITTEN for the two explicitly defined rational polynomials.**
The complete manual conversion from sealed producer mean coefficients to
the defining table also checks. Physical identification remains a separate
dependency on independent P113 reconstruction; this audit does not execute
P113 or independently recompute the underlying Fock law. No universal
photonic/optimizer, hardware, novelty or measured-cost theorem follows.

## 1. Domain and the three rational maxima

With u=(x-y)^2, v=xy, x,y in [0,1], direct expansion gives
(1-v)^2-u=1-x^2-y^2+x^2y^2=(1-x^2)(1-y^2)>=0.
Thus 0<=v<=1 and 0<=u<=(1-v)^2<=1. No substitution treats u,v
as independent unrestricted nonnegative numbers. The proof only needs
this enclosing domain, so further feasibility constraints are unnecessary.
Completing a square proves v(1-v)<=1/4. The derivatives of v^2(1-v)
and v(1-v)^4 are v(2-3v) and (1-v)^3(1-5v). Including the endpoints,
their maxima are 4/27 at 2/3 and 256/3125 at 1/5, respectively.
All bounds apply on the closed domain; no floating estimates are needed.

## 2. Diagonal multiplication independently reconstructed

Multiplying v(1-2v+v^2) by the proposed QP yields the coefficient list
(0,1060,-1752,796,-720,540,296,-220), exactly A0P. For QT it yields
(0,552,-832,280,-256,152,192,-88), exactly A0T. In particular no hidden
nonzero constant or higher-degree term is omitted.
Since negative coefficients require the correct inequality direction,
-144v^3-220v^4>=-364v^2, giving
QP>=1060+368v+108v^2>=1060. Similarly -88v^4>=-88v^2 gives
QT>=552+272v+184v^2+16v^3>=552. Multiplication by v(1-v)^2>=0
preserves both lower bounds, including v=0 and v=1.

## 3. PNR off-diagonal remainder

For GP=A1P+uA2P+u^2A3P, discard positive terms only and use v^3,v^5<=v^2:
A1P>=581-1130v+(3451-1324-106)v^2=581-1130v+2021v^2.
After subtracting 423, the discriminant is
1130^2-4*2021*158=1276900-1277272=-372. Positive leading coefficient
therefore puts this quadratic strictly above 423 on all real v, and gives
A1P>423 on [0,1] where the preceding comparison holds.

A2P>=-228-1280v^2-36v^4. Nonnegative u preserves the inequality, and
u<=1, uv^2<=[v(1-v)]^2<=1/16,
uv^4<=[v^2(1-v)]^2<=16/729 imply
uA2P>=-228-80-576/729=-308-64/81>-309.
A3P>=-230v, so u^2A3P>=-230v(1-v)^4>=-58880/3125>-19.
Thus GP>423-309-19=95, which implies the stated non-strict bound
6144fP>=1060v(1-v)^2+95u. Every discarded term has the required sign;
no assumption that A2P or A3P themselves are positive is made.

## 4. Threshold remainder and exact zero set

A1T>=290-444v+(1662-520-34)v^2=290-444v+1108v^2.
After subtracting 245, its discriminant is
444^2-4*1108*45=197136-199440=-2304, so A1T>245.
A2T>=-81-502v^2 gives uA2T>=-81-502/16=-899/8>-113.
A3T>=-92v gives u^2A3T>=-23552/3125>-8. Therefore GT>124, proving
3072fT>=552v(1-v)^2+124u. The denominators 6144 and 3072 are positive.

If u>0, either lower bound is strictly positive. If u=0, x=y and
0<v<1 gives strictly positive diagonal term. The only remaining points
are (0,0),(1,1); direct A0 factorization gives value zero there. This
proves strict positivity and the exact zero set on the entire unit square,
not just its ordered triangle or the P101 physical curve.

## 5. Complete MANUAL coefficient conversion from the original archive

After P113 source freeze `7267e6a4ce544772cf8f5018988e142940c9586e`, ROOT
explicitly authorized this audit to read P107 mean_coefficient records.
I read all 162 rows from original seal
`99f2d98d93f13c7fc088218bfb06ff39af4c40e9`, path
`research/P107_symbolic_filter_main/run_001/data/records.jsonl`, using text
filters only: 74 nonzero differences and 88 zero differences, covering all
81 exponent pairs per decoder. No other raw records were inspected here.
This was POSTDATA reading for this proof review, not P113 blind authoring.

Let F be 6144fP or 3072fT. Write
F=D(v)+B2(v)(x^2+y^2)+B4(v)(x^4+y^4)+B6(v)(x^6+y^6).
A pair x^(b+d)y^b+x^by^(b+d) contributes its coefficient times v^b to Bd.
The COMPLETE scaled lists, ascending in v, are:

| List | PNR, scale 6144 | Threshold, scale 3072 |
|---|---|---|
| D | 0,-102,-860,-1958,-1152,730,292,-230,0 | 0,-28,-430,-1044,-388,300,146,-92,0 |
| B2 | 581,-218,694,346,-138,38,5 | 290,-120,332,108,-84,8,2 |
| B4 | -228,678,100,38,-36 | -81,328,50,8,15 |
| B6 | 5,-230,5 | 2,-92,2 |

All opposite-parity coefficients and the possible degree-difference-eight
pair are zero in the archive. Each model has 22 nonzero canonical entries
across these lists, including seven diagonal ones, hence 37 monomials;
the other 44 are zero. Symmetric orientations agree exactly.
The identities x^2+y^2=u+2v, x^4+y^4=u^2+4uv+2v^2,
x^6+y^6=u^3+6u^2v+9uv^2+2v^3 follow from a=x^2,b=y^2,
a+b=u+2v,ab=v^2. Hence direct coefficient collection gives

    A3=B6,
    A2=B4+6vB6,
    A1=B2+4vB4+9v^2B6,
    A0=D+2vB2+2v^2B4+2v^3B6.

I checked every coefficient in these four relations against BOTH complete
P114 tables. Examples: A1P's v^2 coefficient is 694+4*678+9*5=3451;
A0T's v^3 coefficient is -1044+2*332+2*328+2*2=280. The relations also
check every final zero/tail coefficient; no unmatched monomial remains.
Thus the table equals the recorded producer B-minus-D mean polynomials
by manual exact algebra. This is NOT independent production of those means.

## 6. Dependency boundary and disposition

No algebraic or domain gap remains in P114's explicit-polynomial theorem.
The remaining physical dependency is whether the sealed P107 coefficient
records equal the stated passive-Fock/decoder means. Future authorized P113
must independently reconstruct those means, rather than use this table;
P113 code and its blind freeze remain unmodified. This audit does not count
as an independently executed replication, hardware validation or proof of
producer completeness beyond the 162 coefficient records inspected.
The original rectangular-certificate INCONCLUSIVE finding is preserved.
This different analytic proof neither deletes its negative coefficients
nor claims that its registered Bernstein procedure succeeded.

If the physical dependency closes, the conditional implication concerns
this fixed graph, this transfer family and these two fixed all-output
decoders at identical B/D settings. Reoptimized controls, arbitrary graph
encodings, altered losses/preparation, adaptive policies and total resource
costs need their own statements. No QPU/paper/main edit or call occurred.
Only manual algebra, text reads/filters, hashes and Git metadata were used;
no import/AST/test/RNG/native/numerical/symbolic program was executed.
