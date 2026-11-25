# P59 — independent claim-card-only static reconstruction

Source: ROOT's fixed N6 matrix/phase/rotation claim card, before execution.
The adaptive reviewer did not author the encoding implementation and has
not imported/read its future code or run any experiment. Broad context is
shared within the team; this is independent construction, not a blind
physical replication. ROOT independently confirmed the PNR fixture below
before any P59 result. No graph, optimum mask, known partition or draw used.

STATIC VERDICT: the FULL PNR law need not be even in phi; the fixture proves
this. No nonzero decoded edge slope or mean-cut gain is established yet.
An exact cancellation in the top3 aggregation remains a live possibility.

## Fixed circuit and exact coefficient convention

Modes are2a+i, a,b in Z3 and i,j in{0,1}. Let omega=exp(2*pi*i/3) and
H2 be the unnormalized real Walsh matrix. Start with

    U0[(a,i),(b,j)]=omega^(a*b)*exp(i theta[b,i])*H2[i,j]/sqrt6,

where only theta[1,1]=phi is nonzero. Apply the FIXED real output rotation
[[3/5,-4/5],[4/5,3/5]] on modes0,2. Its sign is not chosen from results.
For creation variables x0,...,x5 define

    E_b=((3-4*omega^b)*x0+(4+3*omega^b)*x2)/5+omega^(2b)*x4,
    O_b=x1+omega^b*x3+omega^(2b)*x5.

The unnormalized polynomial is

    P=prod_b (E_b^2-exp(2i theta[b,1])*O_b^2)=C0+C2*exp(2i phi).

There is NO exp(i phi) coefficient. For occupation n, use its scalar
coefficients c0(n),c2(n). The normalized Fock amplitude is
sqrt(prod n!)*(c0+c2 exp(2i phi))/6^3. Probability MULTIPLIES by prod n!
and divides by6^6; denominators already inside c0,c2 must not be counted
again or silently omitted. Every one of C(11,6)=462 outputs is retained.

## Fixed intensities and what symmetry does not prove

The two mixed-row intensities are[1∓(24/25)cos(2*pi*b/3)]/6; the other
rows have1/6. They are independent of phi, not uniform. Each row sum is1.
The mixed row's squared-intensity sum is1/6+(24/25)^2/12, giving B variance
5/3-(24/25)^2/6, different from unmixed mode4's5/3. The count law is not
C3-invariant. P=U U^dagger=I and mean counts1 remain exact.

The D Poisson-multinomial law and all B single-mode PGFs are fixed in phi.
For a full single-occupancy source, diagonal count moments through degree3
depend only on q and P=I, hence are fixed too. This does not constrain the
nonlinear top3 readout to be constant. Conversely a varying PNR event alone
does not prove a varying feasible cut law.

Conjugation exchanges input blocks b1,b2 and reverses their phases; it does
not identify this fixed b1-only perturbation with its negative. A row swap
would need to transform the fixed noncirculant rotation as well. No such
unproved symmetry is a valid reason to set the15 edge slopes to zero.

## Analytic pre-execution fixture and general derivative formula

For n=(4,2,0,0,0,0), direct coefficient extraction gives

    c0=(-1362+40*omega)/625,
    c2=(-33-40*omega)/625,
    c0+c2=-279/125,
    c2*conjugate(c0)=(44666+55800*omega)/390625.

Therefore p'_n(0)/sqrt3=-124/421875 after the factor4!*2!/6^6. This is a
guard for sign, exponent2 and Fock normalization, NOT an edge-slope result.

In the author's convenient xi=exp(i*pi/3) basis, omega=xi-1 and xi^2=xi-1:

    c0=(-1402+40*xi)/625,       c2=(7-40*xi)/625.

For arbitrary rational a,b,c,d with c0=a+b*xi and c2=c+d*xi, write
D_n=a*d-b*c. Since Im(c2*conjugate(c0))=sqrt3*D_n/2,

    p'_n(0)/sqrt3 = -2*(prod n!)*D_n/6^6.

If integer coefficients share a stored denominator, divide D_n by its
SQUARE. The entire event law has only constant, cos(2phi), sin(2phi):
its constant/cosine coefficients are rational and its sine coefficient
is sqrt3 times a rational. It is pi-periodic, but generally not even.

## Exact top3 obligations; all15 edge slopes still unknown

For every count vector select the3 largest modes uniformly at ties. Let
t_e(n) be its EXACT edge-crossing probability. Do not select just one tie
partition, discard collisions or condition on a favorable subset. A safe
common denominator for all eligible tie weights is60: the positive-count
and threshold-zero cases include denominators20,10,6,4,3,2,1.

The actual quantity to close is

    d_e/sqrt3 = -(2/6^6)*sum_n (prod n!)*t_e(n)*D_n.

It requires ALL462 rows and ALL15 edges. The single PNR fixture cannot
replace this sum. Necessary independent consistency checks are:

- sum_n p'_n=0; each one-mode marginal bin's derivative is zero;
- every joint factorial moment of total order<=3 has derivative zero;
- at each of SIX vertices, sum_(edges incident) d_e=0;
- total sum_(15 edges) d_e=0 (implied by the incident identities).

The decoder identities hold for every phase: incident crossing sums3 and
total crossing sum9. They apply separately to constant/cosine/sine data.
The six incidence constraints leave at most9 independent edge slopes.

There are10 UNORIENTED balanced cuts (identify S and S^c). Their crossing
vectors satisfy inner product9 for the same cut and5 for different cuts.
Thus their output probabilities obey

    pi_S(phi)=(sum_(e crossing S) f_e(phi)-5)/4,
    pi'_S(0)=(sum_(e crossing S) d_e)/4.

This is a useful second aggregation check. A PNR derivative can cancel
inside every unoriented cut class; no mean gain follows until this is
excluded. If all d_e vanish, only the sine response vanishes. A nonzero
cos(2phi) coefficient would still make the decoded law phase dependent.
Both sine AND cosine coefficients must vanish to assert complete cut-law
phase blindness. A zero slope at0 must not trigger an unregistered center
or phase-direction change.

## Conditional graph rule and calibrated scientific scope

Only after deriving the actual coefficients let
f_e(phi)=a_e+b_e*cos(2phi)+c_e*sin(2phi). For a graph define
h_A=sum A_e*d_e=2*sum A_e*c_e and a globally valid curvature bound, e.g.

    M_A=4*(|sum A_e*b_e|+|sum A_e*c_e|).

If M_A>0, phi(A)=-h_A/M_A and Taylor's inequality give
f_A(phi(A))<=f_A(0)-h_A^2/(2*M_A). If M_A=0 the function is constant and
h_A=0; no division or gain claim. This is O(E) using calibrated coefficients,
but is conditional on a NONZERO actual edge response, not the PNR fixture.
The exact calibration, storage and phase control are paid resources.

At N6 only10 unoriented feasible cuts exist; classical search is trivial.
Physical phase-dependent correlations or a mean-descent rule do not imply
optimization/resource advantage. Phase/sphere and independently reoptimized
species controls remain necessary. Nothing here authorizes code, samples,+held-out tests, paper/QPU work or completion of the larger research goal.
