# P53b fixed-point card: physics normalization and exact dual audit plan

Static card verdict: **mathematically coherent, implementation review pending**.
No x-value of the quantum curve was evaluated, no raw target read, and no
source import, test, LP, witness computation or numerical experiment occurred.
This is not a verdict that the selected point lies inside or outside a hull.

Cards read: initial
`a0a6881bfe4ca0f0b0a003e698009dd786f28911` and final
`1dbb3f93a337d6357d4c3397a8a560b9420e00e2`, file
`research/P53_next_fixed_x_dual_proposal.md`, final SHA256
`a3c8684d30344e2246026c40343446fa9f2d8ba6ece6e43affe3e119d668acfa`.
The final card fixes a single rationalization rule, rather than leaving a
choice after seeing candidate coordinates. ROOT separately authorized source
implementation only. Full source/caller/fixtures will be reviewed at their
announced freeze before any import or execution.

## Mathematical preconditions to preserve in source

The coordinate x=(1+cos2theta)/2=cos²theta from P53 gives x=1/4 at theta=pi/3.
This is a new fixed point compared with P52's x=0,1/2,1 values, but the follow-up
is explicitly post-P53, not a held-out optimization experiment. The target must
be evaluated exactly from the sealed rational `crossing_power`, at Fraction1/4.
It must not be a Bernstein control vector, an interpolated float, a P52 NPZ
kernel or a rounded LP input. All28 edge coordinates use the same lexicographic
combinations(range8,2) convention as the exact source and library.

The physical source audited separately is full8-CF in the fixed lossless U8,
all occupations retained, uniform top4 ties. Creation coefficients multiply
occupation factorials; the rank/edge common denominator is420*8^8. The exact
library contains all35 b4 splits at each of theta0 andpi/2 plus uniform70,
71 fixed vertices. This audit does not reconstruct/rationalize those source
coefficients from floating output. Input byte/source hashes, dimensions and
denominators need explicit verification in the future caller.

For a primal witness lambda>=0,sumlambda1,V^Tlambda=b, exact verification of
all coordinates proves membership of this point. Failure of support selection,
free-zero RREF or LP status does not prove nonmembership.

For any exact rational vector w, defining t=min_c w·v_c makes
gamma=t-w·b>0 a strict separator from the whole fixed convex hull: every
mixture obeys w·(V^Tlambda)>=t. LP strong duality is not needed for accepting
the witness; it only proposes coordinates. Exact binary Fraction.from_float
is permitted for the finite proposed **w** coordinates, not source/target.
Implementation must fix the advertised signed-coordinate convention before
rounding, retain raw plus/minus values and avoid outcome-dependent alternative
rationalization. If exact L1 norm exceeds1, scaling by that positive norm
preserves the sign; a zero vector has gamma0 and must not be divided by zero.
The threshold for proof is exact gamma>0, not a floating residual tolerance.

Primal and strict dual witnesses cannot both be valid for the same exact
library/target: the primal implies w·b>=min_c w·v_c. A simultaneous success
must therefore be recorded as inconsistency, accepting neither. Exact witness
validity and the conservative solver-status/run gate must remain separate;
an LP timeout cannot be silently relabelled solved, nor should its raw exact
candidate be discarded.

## Nonnegative graph witness: correct only with exact common totals

Every balanced subset of size4 in8 crosses exactly16 unordered edges. Thus
the physical target and **each** control vertex must have exact coordinate
sum16. Incident-row sum4 and coordinate bounds0..1 are useful additional
normalization checks. These identities protect the common-offset argument;
checking only a floating sum or only the library is insufficient.

Let c=max(0,-min_e w_e) and a_e=w_e+c. Then a>=0 and for every kernel z with
sumz=16, a·z=w·z+16c. Hence the minimum-control-minus-target gap is exactly
gamma after this shift, with no change of optimization orientation. Strict
gamma implies a is nonzero: otherwise w is a constant vector and both sides
are identical. Therefore sum a>0 and dividing all a by this exact sum gives
normalized gap gamma/(sum a)>0. Clearing rational denominators can produce
integer weights but makes no bound on bit length, physical dynamic range,
robustness to noise or preparation runtime.

The witness is an undirected nonnegative-weight N8 graph in the same edge
ordering, constructed posthoc from a separator, not a fresh benchmark. It
would show a mean advantage over these71 fixed vertices and their mixtures
at this one point, **not** over all classical distributions or fully retuned
b4/phase/sphere/graph search. With70 feasible subsets, exhaustive classical
optimization is trivial. No C* or optimum partition is needed for the
algebraic graph conversion, and none should enter the code as an oracle.

## Pending focused implementation checks

At the announced source freeze I will check exact physical source/file pins,
28/71 dimensions/order/normalization, rational point evaluation and all exact
primal/dual/nonnegative-weight verifiers; LP signs, L1 constraints, finite
float proposal extraction and status separation; contradictory-certificate
handling; and fixtures for gaps, offsets, binary rationalization and failure.
Execution remains at most two fixed-point native LP calls of1s, CPU20/wall30,
thread1, array64MiB/output4MiB, with no alternative x or automatic retry. This
checkpoint has not run even a toy certificate and adds no simulation/QPU or
scientific-goal-completion claim.
