# P132 — Three changed mechanisms, with a paid large-graph bridge

2026-11-26. Author P66; parent f5d1d519a8aa5ca165af09f05d8e84df8241a83a.
Manual mechanism design under research-program; no positive result or run.
Read P114/P115, P118's ROOT/soft-return records, P122, P120, P105's source
cards, and ROOT's P86/P87/P99/P100 checkpoints. P126/P129 are separately
reviewed. Their negative results and source restrictions remain intact.
This note changes no code, paper, raw data or shared research status.

## Target and common residual, without a solved initialization

The goal remains a reproducible interference-dependent optimization benefit
against independently optimized D/groups and strong classical feasible search,
under measured total resource costs. A few-photon contrast alone is insufficient.
Polynomial classical simulation does not prove absence of practical benefit;
conversely changing the mode count supplies no complexity advantage.

For a loopless nonnegative weighted graph and balanced current S, choose a marked
source subset R subset S of size k, put S0=S\R, and choose r receivers B
outside S0, without an optimum mask or cut-minimizing spectral initialization.
Marks are public and transported under relabeling. In n4/k2 and n6/k3 whole-graph
qualification take R=S,B=V. At n24 the default is B subset S^c with k4,r12:
genuine four-swap proposals, rather than another three-cut toy.
Prepare k CF photons in abstract input ports associated with the ordered R.
These are source indices, not a claim that receivers B already belong to S.
For a CF receiver set Y of size k, lift to S'=(S\R) union Y.

Put S0=S\R. The exact lifted cut is

    C(S0 union Y)=C(S0)+sum_(j in Y) d_j-2sum_(j<h in Y) w_jh,
    d_j=sum_(h outside S0,h!=j)w_jh-sum_(i in S0)w_ji.       (1)

Boundary fields, pair weights, source/pool selection, memory, setup and every
score are paid and shared with all controls. O(n*r+r^2) feature work does not
mean all binom(r,k) subset scores were performed, nor does it make their
subsequent classical evaluation expensive. k4,r12 has 495 candidate subsets.
The strongest baseline may evaluate all 495 if its measured grant permits it.
No feature/compilation time is a free quantum-only grant.

For routes A/C, collisions, wrong photon totals and invalid receiver records
hold S; every attempt still costs k prepared photons, losses and setup.
For route B, the common explicitly defined completion decoder below is used.
The utility is raw h(Y)=[C(S)-C(S')]_+, zero on holds. No C* is needed.
Small n4/n6 cases qualify physics/normalization, not optimizer advantage.

## A. Receiver feature frame: graph correlations without an optimal mask

Choose k public receiver prototypes p_a independently of their cut quality.
With W=1+max_j|d_j|+sum_(j<h in B)w_jh, define

    F_ja=exp[-beta*d_j/(2W)] exp[i*kappa*w_(j,p_a)/W]/sqrt(r),
    Q=F(F^dagger F)^(-1/2),       T=sqrt(eta)*Q.           (2)

This specifies a row feature embedding, not a search over arbitrary U.
On full column rank Q^dagger Q=I. Predeclare c>0; when
lambda_min(F^dagger F)<c use Q0_ja=exp(2*pi*i*(j-1)*(a-1)/r)/sqrt(r).
This shared Fourier fallback and its conditioning check are paid; a bad frame cannot obtain
unlimited precision, free retries or favorable graph exclusion. Forming the
k-by-k Gram/orthogonalization and certifying its compiled error are paid.
No eigenvector is interpreted as a partition or prepared as a known solution.
Independent D can retune every admissible beta/kappa/prototype/scale choice.

The occupied isometry [sqrt(eta)Q; sqrt(1-eta)I_k] uses r signal and k dump
ports and has an ordinary passive unitary completion. Thus n4/k2 uses six
ports, n6/k3 nine; k4,r12 uses 16 ports and four photons, no helper or
within-shot control. eta=1 needs no intentional dump yield reduction.
Actual device attenuation is separate. This entire instrument is STATIC.
Complex rectangle phases of the actual Q must be checked; merely having
complex F entries does not prove it is outside the gauge-positive class.
If it is gauge positive, P126 applies. P129 always applies with a valid norm
certificate; at eta near one its structural bound may simply be uninformative.

For CF Y, raw p_B(Y)=eta^k |per Q_Y|^2 and
p_D(Y)=eta^k per(|Q_Y|^2). No CF normalization is allowed.
The first concrete mechanism is an exact pair identity, j!=h:

    E_B[n_j n_h]-E_D[n_j n_h]
      =Xi_jh:=|(TT^dagger)_jh|^2-sum_a |T_ja T_ha|^2.    (3)

For the occupation-polynomial extension of (1), the same-T mean contrast
is -2sum_(j<h)w_jh Xi_jh; unary means cancel. This is a computable sign
test for a proposed embedding. It is not the cut of a collisional outcome,
and it does not transfer automatically to the feasible/hold utility.
The exact classical pair-feature control receives Xi and all its work.
Bosonic clustering/permanental point processes are already known mechanisms.

Hand falsifier: the isometry with rows (1,1)/2,(1,-1)/2,(1,1)/2,(1,-1)/2
suppresses BOTH CF targets {1,2} and {3,4}, whereas D assigns each 1/8.
For edges w12=w34=1 and current {1,3}, those two targets improve cut 2 to 0.
B never improves; D's total improvement hazard is 1/4. B's other CF targets
and collisions all retain cut 2 under the stated decoder. Hence no universal
useful-correlation sign is asserted. This embeds into k4 with two spectator
columns/rows, so adding photons alone cannot rescue the claim.

First uncertain implication: can a fixed graph-feature compiler create useful
feasible FOUR-input exchange after all collisions, tuned groups2/3 and D,
rather than only a pair statistic reproducible from (3)? Status OPEN.
Fixed-k exact-law classical samplers remain mandatory timed controls; increasing
r does not turn their cost into exhaustive r^k enumeration.

## B. Measured taps and non-conjugate feedback, including removed photons

Use a six-port receiver compiler

    U_G=exp(-it H_G),
    H_jj=d_j/W, H_jh=(-w_jh+i*kappa*w_jh*Omega_jh)/W,
    Omega_jh=sign(mark_h-mark_j),                       (4)

which is Hermitian. No graph eigenstate/optimal partition is loaded.
Three CF data photons occupy fixed ordered input ports; two extra flag ports
start in vacuum. A graph-independent tap on two marked data modes gives
W_G=B_(a,f1)(R1) B_(b,f2)(R2) (U_G directsum I_2), where each tap on
(data,flag) is [[sqrt(R),sqrt(1-R)],[-sqrt(1-R),sqrt(R)]].
Measure only f=(f1,f2), preserving the remaining data coherently. Then apply
V_0=I if |f|=0, V_1=Hadamard_(u,v) if |f| is odd, and
V_2=exp(-i theta X_(x,y)) if |f| is positive even, on data modes only.
Set a=u=1,b=v=2,(x,y)=(3,4) in public mark order; Hadamard is
[[1,1],[1,-1]]/sqrt(2). These have different mixing magnitudes, not the conjugate sign
choices refuted by P122. Ports/pairs come from public marks, not the outcome's
best cut. All parameters are independently retunable in the D/control families.

For each complete ideal record (f,n), total |f|+|n|=3, define

    W_f=(V_f directsum I_2)W_G,
    p_B(f,n)=|per(W_f[(n,f),input])|^2/(n! f!),
    p_D(f,n)=per(|W_f[(n,f),input]|^2)/(n! f!).          (5)

Protected flag projectors commute with the later DATA unitary, making (5)
the causal probability, not a postselected approximation. Sum all 120
three-photon/eight-mode records. D retains single-photon path coherence;
traced internal tags are not coherently erased. Extra physical loss needs
the full extension, not an assumed three-photon table.
Decoder: choose the k largest DISTINCT receiver counts, uniformly resolve
all ties, including zero counts when fewer photons remain. Lift by (1).
Thus removed-photon branches are paid candidate attempts, not discarded;
their classical completion is explicitly credited to the baselines.
For n4/k2, four data plus two vacuum flags cost six modes/two photons;
the n24 k3,r6 residual costs eight modes/three photons, zero helpers.

Why this is more than P122: on two data modes a,b, tap only a into a vacuum flag,
with 0<R<1,
take V0=I and V1=Hadamard(a,b). The zero-flag one-photon map is diag(sqrt(R),1).
Any STATIC passive dilation reproducing this instrument has zero flag amplitude
from b and retains b in b. On input |1a,1b>, its one-flag branch must therefore
leave b; feedback leaves (a-b)/sqrt(2). This proves noncompilability of the full instrument
on the one/two-photon Fock domain. It does NOT rule out a static circuit matching
the terminal law of one fixed source. A branch-blind arbitrary static mesh is
therefore a mandatory control, not an excluded competitor.
If all V_f are equal it collapses exactly to a static mesh; for a real prefix
and conjugate-only V_f, P122 supplies the stronger count-null. Those cases are
pre-experiment vetoes. Nonzero taps plus non-conjugate feedback remain OPEN;
improved classical completion alone is not an interference contribution.
True PNR flags, latency/storage and in-shot unitary switching are unverified
Lucy capabilities. This route is deferred as hardware until explicitly certified.

## C. Product-source triad phase, with pairwise indistinguishability fixed

This changes internal-source overlaps, not a path-flux name. On three distinct
occupied spatial inputs prepare product internal states

    chi1=H, chi2=(H+V)/sqrt(2),
    chi3^+=(H+exp(i phi)V)/sqrt(2), chi3^-=conjugate(chi3^+).
    J_+=<chi1|chi2><chi2|chi3^+><chi3^+|chi1>
        =(1+exp(i phi))/4,             J_-=conjugate(J_+). (6)

All pair overlap MODULI agree between signs. Use a genuinely complex U_G,
for example formula (4) on the chosen r ports, and ignore internal labels in the terminal spatial decoder.
For output list o with multiplicities n, A_sigma=product_a U_(o_a,s_sigma(a)),

    p(n)=1/n! sum_(sigma,pi in S_k) A_sigma conjugate(A_pi)
                       product_a <chi_pi(a)|chi_sigma(a)>. (7)

For k=3, pair/identity terms are sign-invariant; write the remaining terms
as 2Re(J Z_n), defining Z_n by the oriented three-cycle terms in (7).
Then raw utility contrast is -4 Im(J_+) Im(sum_n h(n)Z_n). This is an
explicit graph-cost bridge to test, not an assumed favorable sign.
With real U the two full laws are conjugates and identical: an immediate
falsifier. Two photons cannot carry this three-cycle distinction.

A hand nonzero-contrast fixture exists: a 3-by-3 occupied submatrix
A=(I+q C3)/2 with C3 the cyclic permutation and q^3=i is a contraction.
For the three distinct indicated outputs only identity/cycle assignments remain,
giving sign-law contrast magnitude 4*(1/2)^6*|Im J|. Complete it passively to
six spatial modes and keep ALL outputs. This is a physics witness only; its
special outcome is not an optimum supplied to training or an optimizer success.

n6/k3 uses six spatial modes times two resolved path-color modes =12 total
orthogonal modes, three photons. Internal prep can be path couplers followed
by identical copies U_G directsum U_G, then classical color erasure; no
unverified native polarization control is silently required. n4/k2 is a null
qualification. At n24 use k4,r12 and chi4=H: 24 addressed path-color modes,
four photons. Three- and four-cycle terms must both be retained in (7).
This is exactly a STATIC enlarged passive matrix including the source couplers,
not a measurement-induced nonlinear instrument or an escape from all passive theory.

A two-sign adaptive estimator can choose the next sign from paid raw utility
observations, without C*. Two probes plus one proposal cost nine photons for
k3, twelve for k4; source prep, settings and all training draws count. Improved
estimation alone is not optimizer advantage. D, all group2/3 partitions and
the exact-law classical mirror can optimize independently, including using the
same feature/phase information. Orthogonal-tag preparation for a hardware D
control is an additional certified source/mode/time requirement, not free.
Common uniform transmission multiplies all-k feasible sign contrast by eta^k;
holding losses does not recover those missing photons for free.

Primary attribution checked: Menssen et al., *Distinguishability and many-particle
interference*, [1609.09804v1, 30-Sep-2016](https://arxiv.org/html/1609.09804v1),
Theory Eqs. (1)-(5), related PRL118,153603 (2017). Pair overlaps alone failing
to determine three-photon statistics and the triad phase are already known.
Our graph-utility application is OPEN, not claimed novel by a failed search.
No fetched full text retained; source SHA: NONE.

## Priority and a reusable negative continuation

Prioritize A's first bounded exact discriminator AFTER P130/P131: a k4,r6
receiver physics check inside an n24 residual (ten signal/dump modes).
Predeclare one Gaussian-rational realization/rounding of (2) and certify
T^dagger T<=I exactly; no precision retries. Its 15 CF targets have exact
size-four permanents; all other loss/collision mass is the paid hold event.
Compare the four-input contribution with the full raw utility, not only (3).
A small 15-state frontier is a physics/control check, not a positive-advantage
gate or a theorem about r12. The later k4,r12 residual-use card needs its own
measured practical-control gate. Use (1), all raw CF/hold events, independent D/groups,
the pair statistic (3), exact-law sampler, beam/pair/FAST feasible controls and
the full feasible frontier whenever its measured grant permits. A future card
must freeze graphs/marks/parameters/credits and errors before evaluation.
No population, parameter search, resource contract or execution is authorized here.
Reject advantage if the tuned controls reproduce it or if its source is only
unpaid preprocessing/repair/postselection. A same-T contrast can remain a valid
physics result even when the practical optimizer gate fails.

Expanded strict walk: for two triangles sharing a hub, every hub-to-hub path
has length three. Degree-two strict coins route deterministically, with phase.
At times 3L the four incoming hub modes evolve by (D P C_hub)^L, with P swapping
the two neighbors of each triangle and D the accumulated path phases. This is
exactly a four-mode static mesh on those inputs/outputs, even though the physical
walk uses 12 arc modes. It is not an independent memory mechanism at those
readouts. Other graphs/times/measurements are not refuted by this identity.

The current [Quandela Lucy specification](https://www.quandela.com/qpus/lucy/)
lists 24 modes; [CEA](https://www-hpc.cea.fr/fr/Calcul-Quantique.html) identifies
12-photon Lucy/Perceval at TGCC. These are dimension context only, not account
authorization, PNR/feed-forward, calibrated loss or throughput certificates.
All three routes remain OPEN mechanisms, with different first failures; none
passes the user's positive/held-out/replication/hardware gates. Only this file
was written; no imports/AST, numerical worker, RNG, tests, native/QPU, raw-data
read, paper edit or push occurred.
