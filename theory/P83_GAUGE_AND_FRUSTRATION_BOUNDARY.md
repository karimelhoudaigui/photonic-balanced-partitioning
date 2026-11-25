# P83: diagonal phase gauges and the even-loop frustration boundary

Primary verdict: **proved as stated below**. Vertex phase congruences
Z=D B D with B entrywise real nonnegative preserve the ENTIRE raw PNR
law and cannot escape the P78/P80 source controls. Such a factorization
has an exact support/phase criterion, including loops and odd cycles.
The proposed frustrated four-mode source is physical and its log-PGF
coefficient of z_1 z_2 z_3 z_4 is -2t^4. Thus that law is not a
compound-Poisson law with nonnegative count increments. This is not a
hardness result or an exhaustive boundary of classical simulation.

Independent static reconstruction of ROOT's candidate, 26 November 2026,
starting at `0a51544a1a449c64b87cb48e82bf637583402278` on
`research/p66-dark-barrier`. ROOT supplied the gauge and four-mode
candidate formulas before this derivation. No other P83 source or verdict
was read; P82 was not contacted or read. This is not an independent
discovery or originality certification. Only this file is written.
No scientific code/import, AST, test, random draw, matrix numerics,
native backend, QPU, new hardware preparation or manuscript action was
performed. No P79/P75 output was read. All calculations are hand algebra.

## 1. The exact gauge class and raw-count invariance

For a symmetric pair matrix Z let its support contain precisely the
nonzero entries, with an undirected edge ij for i!=j and a loop for
nonzero Z_ii. Zeros carry no phase constraint. In the factorization

    Z=D B D,    D=diag(d_i),    |d_i|=1,    B_ij>=0 real,

B is necessarily the entrywise magnitude matrix |Z|. This is a diagonal
CONGRUENCE, not D B D^dagger. Its edge equations are phase SUMS.
It preserves the operator norm because left and right phase matrices
are unitary, so physical ||Z||op<1 implies ||B||op<1.

Let R_D=exp(i sum_i theta_i N_i), d_i=exp(i theta_i). Conjugating a
creation operator by R_D multiplies it by d_i, and the vacuum is fixed.
Consequently the pair-exponential state for Z is R_D times that for B.
Its norm is unchanged. In particular

    Z Z^dagger=D B^2 D^dagger,
    det(I-Z Z^dagger)=det(I-B^2),

consistent with the Gaussian normalization. The normalization and norm
here can be established directly from B's real orthogonal diagonalization
and the one-mode binomial series, then transported by R_D; no general
complex Takagi theorem is a missing premise for this gauge class.

For a number record n, expand Z by repeating each label i exactly n_i
times. Every perfect matching uses every occurrence exactly once, even
when two occurrences have the same physical label. Hence

    haf(Z_n)=(product_i d_i^(n_i))*haf(B_n).

The normalized Fock amplitudes differ only by this unit-modulus factor.
Vacuum, collisions, all photon totals and every PNR event have exactly
the same probabilities. Equivalently R_D is diagonal in the measured
number basis. A classical decoder or graph score applied to those raw
counts therefore has the same distribution, with failures retained.

If B is within P78's nonnegative real class, the ideal even-loop sampler
applies unchanged. If B is rational, P80's rational killed-walk variant
also applies without using the phases in its stochastic transitions.
This does not certify the cost of recognizing arbitrary encoded phases,
or remove those samplers' separate finite-bit/resource obligations.
There is no proposal-count or raw-acceptance improvement hidden in a
vertex phase: every raw event probability is invariant, not only a
conditional CF distribution.

## 2. Necessary and sufficient phase criterion, with all support cases

Work in the additive circle R/(2*pi*Z). Write

    phi_ij=arg Z_ij,     theta_i+theta_j=phi_ij,

on every support edge, with 2 theta_i=phi_ii on a loop. Treat connected
support components separately; an isolated zero mode has no constraint.
Choose a root r and a spanning tree of the non-loop edges in a component.
For a singleton the tree is empty. Define

    sigma_v=(-1)^(tree distance from r),
    alpha_r=0,
    alpha_v=phi_(parent,v)-alpha_parent along each tree edge.

All solutions on the tree have precisely the form

    theta_v=alpha_v+sigma_v*theta_r.                         (3)

For each remaining edge uv, including loops, put
tau_uv=phi_uv-alpha_u-alpha_v. The following conditions are necessary
and sufficient:

1. If sigma_u=-sigma_v, require tau_uv=0.
2. If sigma_u=sigma_v, every such edge must prescribe the SAME value
   beta=sigma_u*tau_uv for 2 theta_r.

All equalities are modulo 2*pi. If there is no edge of the second kind,
theta_r is arbitrary. Otherwise choose either square root of exp(i beta),
that is either solution of 2 theta_r=beta, and use (3). This explicitly
constructs the gauge and proves sufficiency. Conversely substituting
(3) in each edge equation proves necessity.

The second kind includes loops: uv=uu gives
beta=sigma_u*(phi_uu-2 alpha_u). A single nonzero diagonal entry is
always removable by taking its half phase. Multiple loops or odd cycles
can prescribe incompatible half phases. No phase is assigned to a zero
entry, and disconnected components have independent root choices.

A connected loop-free bipartite support has no second-kind edge. Its
gauge has one free circle parameter, acting with opposite phases on
the two parts. Trees are always gaugeable. A connected nonbipartite
support, including one with a loop, has a second-kind edge; a compatible
gauge then has two root choices, differing by a common sign on that
component. An isolated odd cycle imposes just one half-phase condition
and is always gaugeable. Odd cycles alone are not obstructions.

## 3. Equivalent alternating-walk statement and misleading shortcuts

For a closed support walk W=(v_0,...,v_q=v_0), allow repeated edges,
vertices and loops, and define

    A(W)=sum_(j=0..q-1) (-1)^j phi_(v_j,v_(j+1)).

If the edge equations hold, cancellation of interior vertex phases gives

    A(W)=0 for even q,
    A(W)=2 theta_(v_0) for odd q.                            (4)

Thus every even CLOSED WALK, not merely every simple even cycle, must
have trivial alternating phase. This criterion is also sufficient.
To see this, use the rooted tree of section 2. The walk from r to u,
then along a nontree edge uv, then from v back to r has alternating
phase sigma_u*tau_uv. For opposite parity it is even and forces the
first condition. For equal parity it is odd. Concatenating any two
such odd rooted walks gives an even walk whose alternating phase is
their difference, forcing the common beta in the second condition.
Section 2 then constructs theta. This proof covers loops as odd walks
of length one, without excluding backtracking.

Checking only simple even cycles is insufficient on general supports.
For example take triangles (1,2,3,1) and (1,4,5,1), all edge phases zero
except phi_51=pi. There is no simple even cycle. The two odd walks based
at 1 prescribe respectively 2 theta_1=0 and 2 theta_1=pi. Their length-six
concatenation is the missing frustrated even walk. Magnitudes can be
scaled small enough to make the symmetric pair matrix physical, without
changing this phase obstruction.

For two connected vertices with both loops, the invariant condition is

    phi_11+phi_22-2 phi_12=0.

It is the alternating phase of the loop/edge/loop/return-edge walk.
The phase pattern Z proportional to [[1,i],[i,1]] violates it: each
loop demands a real sign for d_i, but the edge demands d_1*d_2=i.
Its squared singular values are twice the squared proportionality
constant, so this obstruction also occurs inside the physical domain.

Do not replace (4) by ordinary directed-cycle flux or by signed-graph
switching rules for D B D^dagger. For example a triangle with all
negative real edges is gaugeable using D=iI. A diagonal phase is
allowed to be complex, and odd-cycle signs are not individually gauge
invariants for this symmetric congruence problem.

For a loopless simple four-cycle 1-2-3-4-1 the sole obstruction is

    Phi=phi_12+phi_34-phi_14-phi_23,

and gaugeability is equivalent to Phi=0. It is the relative phase of
the two nonzero perfect-matching products Z_12 Z_34 and Z_14 Z_23.
Four vertices are minimal for a loopless simple-support obstruction:
components on at most three vertices are trees or a single triangle.
With diagonal entries allowed, the two-mode example above shows that
four modes are not the absolute minimum for gauge frustration.

## 4. The explicit physical four-mode falsifier

Let Z=t A, where 0<t<1/sqrt(2) and

    A=[[ 0, 1, 0,-1],
       [ 1, 0, 1, 0],
       [ 0, 1, 0, 1],
       [-1, 0, 1, 0]].

Each row has squared norm two. The only potentially nonzero off-diagonal
entries of A^2 join opposite vertices, and their two contributions cancel:
for instance (A^2)_13=1-1=0 and (A^2)_24=-1+1=0. Thus

    Z^2=2t^2 I_4,       ||Z||op=sqrt(2)*t<1.

The normalized real Gaussian pair state is therefore well defined.
Its raw vacuum probability is

    p_0=sqrt(det(I-Z^2))=(1-2t^2)^2>0.

Here Phi=pi, so no diagonal phase gauge removes the sign. The four
distinct-mode hafnian is exactly

    haf(Z)=Z_12 Z_34+Z_13 Z_24+Z_14 Z_23
          =t^2+0-t^2=0.

Consequently p_(1,1,1,1)=0 at EVERY stated physical t, not merely at a
weak-source limit. The other allowed low-sector probabilities and raw
vacuum are retained; this is no postselection identity.

The magnitude matrix |Z| is t times the positive four-cycle adjacency,
with norm 2t. On 0<t<1/2 it is itself physical, yet its corresponding
hafnian is 2t^2 rather than zero. Thus the obstruction is present even
when both sign choices define valid Gaussian sources. On the remaining
physical interval the signed source is still valid while its magnitude
matrix is not a contraction; phase gauges could not have changed that
norm either.

## 5. Two independent hand computations of the negative log coefficient

For real symmetric Z, the pair-state norm argument gives

    G(z)=sqrt(det(I-Z^2))/sqrt(det(I-(D_z Z)^2)),
    log G(z)=sum_(l>=1)
          [Tr((D_z Z)^(2l))-Tr(Z^(2l))]/(2l).

Entrywise nonnegativity was needed for positive intensities in P78,
not for this real signed trace identity. The symmetric weighted matrix
sqrt(D_z) Z sqrt(D_z) remains a contraction, so the trace-log series
converges absolutely. Only the length-four term contributes to the
squarefree degree-four coefficient.

Trace calculation: the closed length-four walks visiting each vertex
once are the four roots times two orientations of this four-cycle.
Each has edge product -t^4. Their trace coefficient is -8t^4, and division
by four gives

    [z_1 z_2 z_3 z_4] log G=-2t^4.                           (5)

Probability calculation: divide G by p_0 only as a formal coefficient
normalization, not an optical acceptance rule. Its degree-two part is

    F_2=t^2*(z_1 z_2+z_2 z_3+z_3 z_4+z_1 z_4).

The degree-four coefficient at 1111 is zero by the hafnian cancellation.
In log(G/p_0), degree four is F_4-F_2^2/2. The two disjoint edge pairings
give four ordered products in F_2^2, totaling 4t^4. The same coefficient
is therefore 0-(4t^4)/2=-2t^4, independently checking the trace roots
and factor 1/(2l). The constant log p_0 does not affect (5).

## 6. What the negative coefficient actually excludes

A compound-Poisson count law with nonnegative jumps k in N^4 minus {0}
and intensities nu_k>=0 has

    G_CP(z)=exp(sum_k nu_k*(z^k-1)).

Its nonzero vacuum mass forces sum_k nu_k=-log p_0<infinity; a nonzero
deterministic drift is likewise incompatible with p_0>0. The analytic
log near zero then has coefficient nu_k at every nonzero monomial.
All such coefficients must be nonnegative. Equation (5) contradicts
this requirement for k=(1,1,1,1). Hence this source law admits no such
positive compound-Poisson representation, even with arbitrary positive
count-vector jumps rather than only loop-visit jumps.

This refutes a blanket extension of the P78 positive-loop construction
to all real signed matrices. It does NOT exclude other positive latent
variables, rejection, sequential algorithms or other classical methods.
Nor has gaugeability been proved necessary for every possible positive
compound-Poisson count law: the iff criterion in sections 2-3 classifies
Z=D|Z|D, not all distributions sharing some other classical model.
The explicit example is fixed dimension and exhibits elementary coherent
cancellation of two pairing paths. It is HOM-type destructive interference
in this qualitative sense, not a demonstrated reduction to a particular
two-photon HOM circuit, a hardness witness or a priority claim.

## 7. A gauge-invariant interference statistic and graph-cost limits

For any four distinct modes, pair-exponential expansion gives the
following raw-probability statistic, with p_0>0:

    Kappa_1234=p_1111/p_0
      -(p_1100*p_0011+p_1010*p_0101+p_1001*p_0110)/p_0^2.

These are COMPLETE PNR events, with every unlisted mode vacuum, and
p_0 is full-source vacuum. Marginalizing other modes does not automatically
preserve this formula.
It equals the 1111 log-PGF coefficient. Put
M_1=Z_12 Z_34, M_2=Z_13 Z_24, M_3=Z_14 Z_23. Since the two-photon
coefficients are |Z_ij|^2 and the four-photon coefficient is
|M_1+M_2+M_3|^2,

    Kappa_1234=2 Re(M_1*conj(M_2)+M_1*conj(M_3)+M_2*conj(M_3)).

All matching products acquire the same vertex phase, so their relative
phases and Kappa are gauge invariant. On the four-cycle this reduces to
2|M_1*M_3| cos(Phi); the signed example attains -2t^4. With loops, the
two-mode four-photon coefficient similarly contains interference through
haf(Z_(2,2))=Z_11 Z_22+2 Z_12^2, with invariant phase
arg(Z_11 Z_22*conj(Z_12)^2).

Four photons are the first pair-exponential coefficient order allowing
distinct perfect-matching monomials to interfere. This is not a claim
that raw vacuum or two-photon probabilities are phase independent:
their common source normalization can itself depend on frustration.
Ratios to p_0 above remove that common factor algebraically; they are
not probabilities conditioned on vacuum. Estimating them would still
require all raw pulses, a finite-sample contract and paid uncertainty.

No optimum is needed to define Kappa or a weighted sum over motifs
chosen from a graph's known edges and weights. Genuine edge phases can
therefore be specified by an optimum-blind graph rule or trained using
observed costs; vertex-only phases cannot change any such count score.
But negative Kappa does not imply a lower graph cut: cut cost concerns
decoded subset correlations, while this statistic concerns raw source
coincidences. Acceptance, the rest of the modes and source resources
must also be controlled. A small motif's phase dependence is explicitly
classically calculable and supplies a necessary baseline control.

For the independent complementary-color construction, when each accepted
color has only two CF photons its hafnian is one edge, so conditional
subset weights depend only on |Z_ij|^2|Z_kl|^2. Frustration cannot improve
that conditional cut law by itself, although raw normalization/acceptance
can change. At four or more photons per color there can be competing
matchings, but no favorable graph-cost theorem or full-cost benefit is
proved by the four-mode cancellation. Source control of nonseparable
edge phases is also not a hardware feature established here.

## 8. Disposition and first unresolved implication

KEEP the exact gauge-invariant extension of P78/P80 and the full support
criterion. KEEP the explicit frustrated source as a falsifier of universal
positive compound-Poisson extension. REJECT vertex phases alone as an
escape from those unchanged raw-count controls. The first unresolved
optimizer implication is a physically budgeted, optimum-blind frustrated
source whose cost-relevant raw distribution survives reoptimized strong
classical controls. Neither frustration nor a negative log coefficient
establishes that implication. The positive optimizer objective remains OPEN.

No novelty, classical hardness, all-Gaussian no-go, device capability,
equal-clock advantage or new experimental authorization is inferred.
Final mathematical proofreading checked congruence versus similarity,
zero/loop/odd-cycle cases, necessity and sufficiency, physical norm,
hafnian cancellation, both independent -2t^4 calculations, the CP
definition, and raw-versus-conditioned cost interpretation.
