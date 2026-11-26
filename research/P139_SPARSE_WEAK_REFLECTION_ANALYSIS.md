# P139 — Sparse weak reflections and an analytic-incumbent obstruction

2026-11-26. ROOT suggested the valuation route; reconstructed manually.
Parent da18f7366be56acc6528f521879430345ecb8336. PROOF CANDIDATE pending review.
No novelty claim, source overwrite, code/import/AST, numerical/symbolic run,
computational graph/matrix evaluation, RNG, raw read, native/QPU or paper work.

## 1. Fixed sparse reflection: no false two-hop escape

Keep F_x=(I+i*x*H)E and T_x=(E+i*x*HE)(I+x^2*B/2)^-1,
B=E^dagger H^2 E, with H Hermitian and the same current receiver set R.
If HE has zero rows outside R, those rows of F_x are IDENTICALLY zero.
Right multiplication by the source-space inverse cannot populate them.
Thus T_x never explores outside R; an H^2 term is not a new receiver hop.
The same applies to any particular entirely zero outside row of HE.

If only some entries or matchings are absent, source-space mixing and
off-diagonal prototype rows can instead create higher-order NONZERO paths.
These paths are not a counterexample to a retuned-D weak-regime obstruction.
The following argument actually needs only an analytic curve T_x at E.

## 2. A general local theorem, with no dense-entry floor

Fix finite K>=2 and finite m>=K+1. Let T_x in C^(m-by-K) have real-analytic
entries on (-rho,rho), T_0=E the current prototype injection,
and be a physical contraction for 0<=x<rho. Use K CF source photons.
For receiver-CF Y, p_B(Y;x)=|per T_x[Y,:]|^2 and
p_D(Y;x)=per(|T_x[Y,:]|^2). Every non-CF event holds R; no postselection.
Choose the INTEGER

    c=ceil(sqrt(K!+1)), so c^2>K!.                     (1)

Then there EXISTS kappa0>0, depending on this fixed analytic curve and finite
pool, such that for every Y!=R and 0<kappa<kappa0:
p_D(Y;c*kappa)>=p_B(Y;kappa), STRICT if Y's D probability germ is nonzero.
If the D germ is identically zero, both germs are identically zero instead.
The theorem requires that the comparator family allow the setting c*kappa.

For each permutation sigma write its path amplitude
a_sigma(x)=product_j T_x[Y_j,sigma(j)]. It is analytic. At least one row is
outside R, so EVERY path has zero constant term. A nonzero path germ has
a finite valuation v_sigma>=s=|Y\R|>=1 and expansion
a_sigma(x)=alpha_sigma*x^(v_sigma)+O(x^(v_sigma+1)), alpha_sigma!=0.
Identically zero path germs can be omitted. If no path remains, B=D=0.
Include those finitely many zero-germ neighborhoods in the final minimum too.

Otherwise put v_Y=min v_sigma. Since D is a SUM OF SQUARED MODULI,

    p_D(Y;x)=a_Y*x^(2v_Y)*f_Y(x),
    a_Y=sum_(v_sigma=v_Y)|alpha_sigma|^2>0, f_Y(0)=1. (2)

Here f_Y is real analytic near zero. No leading-coefficient cancellation is
possible in a_Y. Such cancellation IS possible in the bosonic permanent,
but can only help D; universally, Cauchy-Schwarz gives

    p_B(Y;x)<=K!*sum_sigma|a_sigma(x)|^2=K!*p_D(Y;x). (3)

Equations (1)-(2) imply p_D(Y;c*x)/p_D(Y;x) tends to c^(2v_Y)>=c^2>K!.
This already proves a positive local window for each reachable Y.
For an explicit existence argument, choose
eta=(c^2-K!)/(2*(c^2+K!)) in (0,1). Continuity gives radius r_Y>0 with
1-eta<=f_Y(x)<=1+eta for |x|<r_Y. At both x=kappa and c*kappa,

    p_D(Y;c*kappa)/p_D(Y;kappa)>=c^2*(1-eta)/(1+eta)>K!.

The finite minimum of rho/c and these r_Y/c is positive. Decrease it if
needed for open endpoint conventions and obtain common kappa0. There is
no growing-dimension or H-uniform lower bound in this existence argument.
In particular it is not a free method to locate/compute that radius.

For the rational reflection, I+x^2 B/2 is invertible at zero and positive
for real x, so its entries are analytic near zero and all T_x are contractions.
Thus EVERY fixed sparse H is covered, with identical-zero alternatives retained.
The safe c for K=2,3,4 is respectively 2,3,5. The dense P137 window remains
stronger: explicit, uniform in supplied d, and c=2 for all three cases.

## 3. A connected, missing-matching hand example

Let K=2,m=3,R={0,1}, H=(1/2)*[[0,1,0],[1,0,1],[0,1,0]].
Its eigenvalues are 0,+/-1/sqrt(2), so ||H||<=1. For x>0, F's source-containing
bipartite support is connected. For Y={1,2}, J={2}, C={0}, H[J,C]=0:
the naive direct leading matching is absent. But B=diag(1/4,1/2), so writing
a=(1+x^2/8)^-1,b=(1+x^2/4)^-1 gives the exact receiver submatrix

    T_x[Y,:]=[[i*x*a/2,b],[0,i*x*b/2]],
    p_B(Y;x)=p_D(Y;x)=x^4/[16*(1+x^2/8)^2*(1+x^2/4)^2]. (4)

The sole nonzero assignment uses the old inside off-diagonal row; v_Y=2
even though only one receiver is replaced. This is a genuine higher-order
path, not a gain. At small x the doubled-D ratio tends to 16. At large x,
the ratio p_D(Y;c*x)/p_B(Y;x) tends to c^-4<1, illustrating why the local
fixed-factor conclusion cannot be promoted to an all-strength statement.

## 4. Interpretation and exclusions

All raw CF alternatives are compared simultaneously, hence every common
nonnegative utility h with h(R)=0 is dominated at the retuned D setting,
strictly when it is positive on a reachable alternative. No C*, mask or
known improving partition enters the argument. This does not rule out a
same-setting interference witness. K=1 has no bosonic/D distinction at the
same setting and is outside the strict theorem's choice/claim.

Analyticity matters. Merely C-infinity entries can be flat and oscillatory.
For a manual caution, rotate source 0 toward receiver 2 by
theta(x)=exp(-1/x^2)*cos(1/x), extended by theta(0)=0; keep source 1 fixed.
This is a smooth physical isometry with T_0=E. For Y={1,2}, B=D=sin^2 theta.
At x_n=1/[(2n+1)*pi], theta(x_n)!=0 but theta(2*x_n)=0, defeating the
prescribed c=2 near-zero inequality. This only refutes that nonanalytic
extension, not every possible retuning of this smooth example.

The theorem is for a FIXED curve, finite pool, known-incumbent endpoint and
common CF/hold observation. Varying H/marks with kappa, growing dimension,
arbitrary all-output repair, rare conditional probabilities, a nonanalytic
control law or a grid excluding c*kappa needs separate hypotheses.
Both modeled attempts inject K photons; no preparation/precision/compilation,
wall-time, calibrated loss or tag cost is matched or implemented by this proof.
It is a scoped weak-regime obstruction, not an efficient simulation theorem,
global optimizer impossibility, positive advantage or QPU-readiness claim.
Only this candidate note was written; previous proofs and evidence are intact.
