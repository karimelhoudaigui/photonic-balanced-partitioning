# P53 — exact continuous mean-kernel question

2026-11-25. ROOT follow-up to P52 sealed762877a, after observing its four
numerical mean replacements. This is NOT a preregistered prediction of P52,
held-out evidence, or the requested positive optimizer result. No P53 code,
integer computation, graph, stochastic sample or certificate exists yet.

## Algebraic target and scope

For the SAME U8(theta), full8-CF input and uniform-tie top4, determine whether
the28 edge-crossing means admit a convex replacement for EVERY real theta,
using a FIXED library of the35 b4 groupings at theta0 and atpi/2, plus uniform70.
No new graph, C*, optimal mask, circuit training or quantum/MC draws. Keep all
P52 raw data unchanged. A proof would close only this family/mean objective;
it would not prove full-rank-law or tail equality, total-cost domination,
arbitrary-N impossibility, novelty, or the user's positive objective.

The first algebraic step, independently reconstructed by ROOT and adaptive:
let a_j=X_j+X_(j+4), b_j=X_j-X_(j+4), z=exp(i2theta), and

    F(v)=sum_j v_j^4-2 sum_(j<k) v_j^2 v_k^2+8 prod_j v_j.
    C(X,z)=F(a) [sum_j z^(2j)b_j^4
                   -2 sum_(j<k) z^(j+k)b_j^2 b_k^2+8 z^3 prod_j b_j].

The normalized quantum wave polynomial is C/8^4. F is the product of the
four UNNORMALIZED Walsh linear forms; prove that identity and normalization,
do not infer them from the P52 floats. Each factor has90 monomials, so at
most8100 integer monomial products produce all C_n(z), degree<=6. Equivalently
a full eight-column DP in exp(i theta) has odd coefficients cancel exactly.
For output n the amplitude is C_n(z)*sqrt(prod n!)/8^4. Thus

    P_n(theta)=(prod n!)/8^8 * [sum_j c_nj^2
                 +2 sum_(h=1)^6 sum_j c_nj c_n,j+h cos(2h theta)].

All coefficients are integer/rational. |c_nj|<=8!/prod n!<=40320. Use exact
Python integers/Fractions downstream: degree12 Bernstein intermediates need
not fit int64. Never round a floating coefficient into a proof. Preserve ALL
6435 occupations, including zeros, and exact normalization polynomial.

Uniform tie denominators ADMISSIBLE to top4 in8 divide420. Exact rank70 and
edge28 coefficients therefore have common denominator dividing420*8^8.
Fixed b4 theta0/pi2 kernels likewise have rational coefficients: use Gaussian-
integer four-photon polynomial creation, multiply by output factorials/8^4,
and convolve PROBABILITIES with denominator8^8. Enumerate all35 groupings per
phase, no favorable support selection. Normalization/nonnegativity and
incident-row4/total16 identities must be verified exactly.

## Sufficient certificate, and an explicit possible failure

Set x=(1+cos2theta)/2 in[0,1]. Convert cosine coefficients to polynomials in x
using exact Chebyshev recurrences, then to Bernstein degree6. If EVERY one of
the7 Bernstein control vectors lies in the fixed71-vertex classical convex
hull, the continuous curve does too. Search for each coefficient vector with
a <=1s, native-thread1 LP using the immutable qualified P52 convex-fit helper.
Use floating candidates only to propose a support, solve its29 equalities
(28 coordinates plus sum1) over Fractions, and VERIFY every equality and
nonnegativity EXACTLY. Status alone, tolerances, rounded rational guesses or
least-squares residuals cannot prove membership. Keep raw candidates/failures.

If degree6 does not certify all7 points, try the PREDECLARED degree12 elevation
and its13 control vectors. Maximum20 native fits total, no further degree,
solver replacement or cap increase in this run. If degree6 succeeds, no
redundant degree12 search is necessary. Preserve failed lower-degree witnesses.
Any timeout/failure remains inconclusive; exact candidate details are retained
separately, not silently promoted into a solved fit. No random source is used.

Bernstein membership is SUFFICIENT, NOT necessary. In particular a curve can
touch a hull face internally without lying in that face, making every finite
global-degree certificate fail. Degree12 is no guarantee. Failure or inability
to exactify a floating support is INCONCLUSIVE, not a separating graph,
positive optimization mechanism or proof that the continuous curve leaves
the hull. A future interval/subdivision route would be a separately bounded
question, not an automatic retry here.

If successful, save all exact rational convex vectors lambda_j. The explicit
continuous replacement is Lambda_c(x)=sum_j Bernstein_j(x)*lambda_jc: it is
nonnegative, sums1 and reconstructs every mean coordinate identically. Verify
this polynomial identity independently from the LP. For every nonnegative
weighted graph, the actual mean cut then equals that of this fixed mixture;
at least one component has no higher mean. This is an EXPRESSIVITY statement,
not a training/latency/photon-cost theorem or a full decoded sampler.

## Evidence and implementation gate

Adaptive owns NEW P53 source/spec/contracts/tests on an isolated branch;
encoding audits exact arithmetic/certificate reconstruction and physics the
Fock/F-polynomial/input normalization. Reuse P52 solver helper unchanged only;
do not import its floating creation/decoding results as the proof. Sealed P52
data may be read ONLY for an explicitly secondary numerical cross-check at
the four original angles, not for constructing or rationalizing identities.
Perceval Naive verification is a distinct pending physical-probability check.

Freeze proof derivation/source/input closure before import/run. Qualifications:
Walsh F identity, exact factorial normalization, small rational source fixtures,
Chebyshev/Bernstein evaluation/elevation identities, admissible tie fractions,
Gaussian-integer b4 convolution, independent rational solver positive/negative/
inconsistent cases and exact polynomial verification. Preserve all failures.
Root + independent code review + targeted PASS + explicit exclusive slot are
required before main. One worker/native threads1, pinned environment, CPU60/
wall90, planned arrays256MiB/newoutput32MiB, <=20 fits <=1s each. Project work
before execution; no hard Darwin memory/affinity promise. No automatic retry,
new model install, paper update, QPU call or claim of achieved positive goal.
