# Proposed single-point discriminator — NOT execution authorization

Post-P53 bounded follow-up for ROOT arbitration. No additional curve value,
LP, graph or sample has been computed. Keep P53's inconclusive global search
unchanged. This note proposes ONE new point, not automatic subdivision.

Fix **x0=1/4**, equivalently theta=pi/3, before opening/evaluating its value.
It is a simple rational point absent from P52's x0,1/2,1 cells; no search over
x or outcome-dependent replacement is proposed. Evaluate b=B_crossing(x0)
from the sealed exact rational P53 power polynomial. Keep EXACTLY the71 fixed
vertices (35 b4 groupings at theta0 andpi/2 plus uniform), not reoptimized b4
over continuous theta, other encodings or strong feasible graph search.

Predeclare at most TWO1s/thread1 native LP calls with the same pinned solver:
one primal membership-support proposal and one dual separating proposal at
this SAME point, without retries or alternative points. Root may choose to
freeze only the dual arm; no command/source is authorized by this note.

Primal: reuse the bounded support-only exactification. Accept membership ONLY
with lambda>=0,sumlambda1, V.Tlambda=b verified over Fractions. This certifies
the point, not the entire continuous curve. Failure alone stays inconclusive.

Dual: propose a signed w in28 edge coordinates, with ||w||1<=1, maximizing

    gamma = t-w.b,     t<=w.v_c for every one of the71 vertices.

Use w=wplus-wminus, wplus/wminus>=0 and sum(wplus+wminus)<=1. The LP is only
a proposer. Convert its witness w to exact rationals under a SINGLE fixed
rule (e.g. exact binary Fraction.from_float on each finite proposed coordinate),
never convert the source/target from floats. Rescale w by its EXACT L1 norm
if needed. Set t_exact=min_c(w.v_c), then check

    gamma_exact=t_exact-w.b > 0

EXACTLY. No floating residual or tolerance establishes strict separation.
Any verified rational w works, irrespective of how it was proposed; the
certificate is the strict rational inequalities themselves. Retain solver
status/failure separately under ROOT's conservative gate. If neither exact
primal nor strict dual witness verifies, report INCONCLUSIVE_AT_FIXED_X.
If both verify, flag a logical/implementation inconsistency and accept neither.

Nonnegative weighted-graph interpretation is algebraic, not a benchmark.
All balanced kernels have sum_e crossing_e=16. Let

    c=max(0,-min_e w_e),    a_e=w_e+c>=0.

Then every kernel's mean shifts by the SAME16c, so
min_c(a.v_c)-a.b=gamma_exact>0. If gamma_exact>0, sum_e a_e>0; dividing by that
sum gives a normalized mean gap. Multiplying rational weights by their common
denominator makes integer weights if desired, with arbitrary precision.
This constructs an N8 graph WITNESS from the separator, without computing C*
or a known optimal partition. It is explicitly a posthoc constructive witness,
not a held-out graph, planted-instance-free optimizer benchmark or evidence
against fully reoptimized classical/continuous-b4 controls. Exhaustive70-cut
classical search remains trivial at this size.

Possible outcomes therefore distinguish membership/nonmembership at ONE new
rational point only. No result from this proposed question could by itself
close the user's positive/held-out/replication/total-resources/hardware goal.
