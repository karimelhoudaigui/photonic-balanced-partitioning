# P46: centered full-source transport and a copula discriminator

Owner physics, 2026-11-25. Base checkpoint
`4c1bad243cb1ce5066bae24c393bc263c03fab89` preserves the P45-C exact symmetric
CF-plus-failure replacement. This is a DISTINCT analytic candidate, not a
positive optimization result. No P46 code, numerical raw, pilot or QPU run
exists. Encoding has numerical priority; its live pilot is not modified.
Results described by the coordinator motivate this discriminator but their
raw was not inspected or revalidated here. Mathematical derivations below
are author self-checks awaiting claim-first cross-review.

## 1. The transport obstruction that is actually removed

Use b occupied anchor modes A and b empty modes B, with one photon in each
occupied mode. There are NO spectator photons in this construction. For any
passive U, fixed CF input implies the exact first-moment identity

    E[N_B]=||P_B U P_A||_F^2.

It is the same for bosons, distinguishable photons and internal species;
no interference advantage follows from this quantity. For H=vv*, ||v||=1,

    exp(-itH)=I+(exp(-it)-1)vv*,
    E[N_B]=4sin^2(t/2)||P_Av||^2||P_Bv||^2<=1.

More generally, rank(H)=r gives E[N_B]<=4r, and
E[N_B]<=t^2||H||_F^2 follows from |exp(-it lambda)-1|<=|t lambda|.
Thus opnorm-normalizing a dense positive generator with bounded stable rank
can leave only O(1) transported photons at fixed t. This is an invariant,
not a blanket statement about every positive graph or every decoder. For
direct CF support moves, l new vertices require N_B>=l, so Markov gives
Pr(l-or-more new vertices)<=E[N_B]/l. A decoder that fills unclicked vertices
is outside that inference.

Now take a b-by-b unitary W and define the hollow Hermitian matrix

    H=[[0,W],[W*,0]],
    H^2=I, Tr(H)=0, spectrum(H)={+1 repeated b,-1 repeated b},
    U(t)=cos(t)I-i sin(t)H.

No large isolated Perron eigenvalue remains. Fix p=sin^2(t) BEFORE outcomes,
using the two initial settings p in{1/4,1/2}, t in{pi/6,pi/4}. Then

    E[N_B]=bp,  N_B has exactly Binomial(b,p) law.                (H1)

These are constant coupling strengths, not t decreasing with b. The result
holds for a common internal-blind map even with internal correlations; only
the destination statistics change. It removes the thin-transport bottleneck,
not the optimization bottleneck.

## 2. An explicit optimum-blind graph map

Let S0 be a charged classical 1-swap minimum on a graph with2b vertices.
Choose random ordered lists (u_1,...,u_b) for S0 and(v_1,...,v_b) for its
complement BEFORE outcomes. Node priorities/order are metadata that must
be carried under graph relabelings; do not use a hidden canonical-labeling
oracle or favorable labeling. The classical controls receive the same lists.

For graph cut C(x)=d^T x-x^T A x, let ell=d-2Ax at the anchor. Compute ALL

    Delta_(v,u)=C(S0-u+v)-C(S0)=ell_v-ell_u+2A_uv.

All b^2 exact deltas are credited as scored classical moves. The common
incumbent includes every actually scored candidate; if they already improve
the anchor, that discovery belongs to the frontend. At a verified 1-swap
minimum the deltas are nonnegative, but their centered interaction is signed.
Put

    Z=I-11*/b,
    R=Z Delta Z=2 Z A_(B,A) Z,
    sigma=||R||_op, zeta=1/4,
    F_(j,a)=exp(2pi i(j-1)(a-1)/b)/sqrt(b),
    M=F+i zeta R/sigma, W=polar(M)=M(M*M)^(-1/2), if sigma>0,
    W=F if R=0.                                                (H2)

The two separable ell fields and uniform Perron directions are removed
EXACTLY by Z. Matrix construction and polar/SVD/norm work are charged
classically (dense arithmetic O(b^3)). Spectral and matching controls may
use the SAME Delta,R and decompositions. Graph data are not a forbidden
oracle, but their classical processing cannot disappear from the budget.

The reference Fourier unitary is fixed; its graph-free phases are not flipped
when R changes sign. This avoids the automatic W(-R)=conj(W(R)) null symmetry
of an isolated real exponential. It does NOT prove any favorable orientation
of the resulting search distribution. Orders are randomized before outcomes
to test label robustness; the Fourier reference is not secretly aligned to
known optimum vertices. R=0/low-rank/weak-response cases remain in the test
population and are labeled, never filtered after outcomes.

### Controlled invertibility and a delocalization bound

||M-F||<=zeta<1 ensures sigma_min(M)>=1-zeta=3/4. No arbitrary nullspace
completion of a singular polar factor is required. To bound its unitary
factor, write F*M=I+E=V K with V=F*W unitary and K positive, ||E||<=zeta.
For a unit eigenvector Vx=exp(i theta)x,

    x*(I+E)x=exp(i theta)h, h=x*Kx>0.

The left side lies in the radius-zeta disk centered at1. Hence cos(theta)>0,
|sin(theta)|<=zeta and

    ||W-F||_op<=c_zeta=sqrt(2-2sqrt(1-zeta^2)).                  (H3)

For zeta=1/4 this is about0.252. Therefore

    |W_ia|<=b^(-1/2)+c_zeta,
    I4(W):=sum_(i,a)|W_ia|^4<=b(b^(-1/2)+c_zeta)^2.             (H4)

In particular it cannot approach a monomial permutation at growing b.
The dense Fourier reference thus prevents a quasi-permutation escape by
construction. It does not certify extensive GRAPH response: polar factors
can ignore special perturbations. Record stable-rank(R)=||R||_F^2/sigma^2,
||W-F||_F^2 and I4 before outcomes; none is an optimization gain. When R has
low rank, W-F has rank at most2rank(R): M*M-I is supported on the span of
F*range(R) and range(R*), and its square-root correction stays there. This
flags a thin graph-controlled sector, without asserting a full classical
simulation of the graph-blind Fourier background.

Numerically computing polar factors, Fourier entries or CDFs does not turn
them into exact rational unitaries. Any implementation must record input
precision/unitarity error; the exact invariants refer to the defined matrices.

## 3. Exact transport decomposition and the collision tradeoff

At terminal measurement, the old output block is cos(t)I times its occupied
input. Thus the old missing-index set T is known from old detections. Its
probability is p^|T|(1-p)^(b-|T|); conditioned on T, the new modes contain the
|T|-photon input pattern T propagated through W*. This proves(H1). It is also
the mandatory matched classical cover: every method can sample the same T.
The only remaining quantum subkernel is a growing |T|=Theta(b) bosonic
destination law, INCLUDING collisions. A bounded-component W or bounded
photon groups again admit exact classical replacement; spectators do not
change that. Conditional kernel complexity does not by itself prove hardness
of the unconditional sampler or usefulness of a rare conditional event.

For identical photons, a second cheap invariant is

    E[sum_(new i) binom(n_i,2)]=p^2[b-I4(W)].                    (H5)

Derivation: E[(n_i)_2]=4p^2 sum_(a<c)|W_ai|^2|W_ci|^2;
sum_a|W_ai|^2=1. Distinguishable photons give HALF of(H5). This is a real
extensive collision correlation for delocalized W, not a favorable search
signal. An extensive mean collision count alone does NOT prove exponentially
small CF probability.

As a separate Haar REFERENCE only, for |T|=l the standard fixed-photon Haar
twirl gives mean CF probability

    binom(b,l)/binom(b+l-1,l).

That average becomes exponentially small at l=Theta(b), so merely replacing
W by a dense Haar matrix does not address the problem. It is not a theorem
that every graph-programmed W has the same CF cost. A useful construction
needs raw improvement mass surviving collisions and the classical controls,
or a completion decoder whose classical work is honestly charged.

The output one-particle Gram matrix is

    G=[[ (1-p)I, i sqrt(p(1-p)) W ],
       [ -i sqrt(p(1-p))W*, pI ]].

Every off-diagonal THREE-cycle product of G is zero: its graph is bipartite.
The first possible loops are quartets
p^2(1-p)^2 W_ij W_kl conj(W_kj)conj(W_il). Record gauge-invariant real parts
and magnitudes of imaginary parts, not a gauge phase alone. These Gram facts
do not determine non-Gaussian CF-source higher moments; some genuine phase
effects in two-mode laws are already classically accessible by P43.

## 4. One-mode PMFs, including loss and internal species

This statement does not require uniform loss. Let T be any common passive
transmission contraction with vacuum environments, N distinct CF inputs and
q_a=|T_ia|^2 for one detected mode i. Marginalizing all other system AND
environment outputs in the full isometry gives

    E[z^n_i]=per(I+(z-1)aa*)
       =sum_(r=0)^N r! e_r(q)(z-1)^r, a_a=conj(T_ia),
    pi_i(s)=Pr(n_i=s)=[z^s]sum_r r! e_r(q)(z-1)^r.              (P1)

The rank-one permanent uses a selected source subset of size r, hence r!
and no additional normalization. For fully distinguishable independent
particles the r! disappears. For a product of mutually orthogonal internal
species, the per-species PMFs convolve, because the number contributions
are independent across species. This is valid for any declared group sizes.
Exact full-law classical simulation by small species requires the NUMBER
OF PHOTONS PER GROUP to be bounded (e.g.3/4), not merely a bounded number
of species each containing Theta(N) photons. Correlated internal states
need a separate marginal formula; a generic Gram/convolution shortcut is
not asserted for them here.

The degree-N elementary-symmetric recurrence and binomial inversion take
O(N^2) arithmetic per mode, O(mN^2) over m outputs. All vacuum, collision
and loss counts are included; using a CF-conditioned calibration would be
a different, globally conditioned problem. Every new circuit/parameter
choice needs its own marginal calculation/calibration, charged to setup.

### A favorable ABSOLUTE conditioning fact for this hollow construction

Old modes are exactly Bernoulli(1-p), while a new row has total q-mass p.
For A_r=r!e_r(q), nonnegative coefficients satisfy A_r<=(sum q)^r=p^r.
Thus the absolute term sum for the probability of s new photons is bounded by

    sum_(r>=s) binom(r,s) A_r
      <=p^s/(1-p)^(s+1)<=2, if p<=1/2.                       (P2)

This bound is independent of b. The positive recurrence

    A_r(new)=A_r(old)+r q_a A_(r-1)(old)

avoids explicitly forming huge factorials. Relative coefficient error epsilon
therefore contributes at most2epsilon ABSOLUTE inversion error, before final
summation rounding. D and independent species have the same bound: their
generating coefficients are bounded by p^r via convolution and sum of group
means p. This is not a relative tail guarantee, an implemented roundoff proof,
or permission to clip and relabel numerical PMFs as certified. Exact row
normalization is used; numerical/unitarity/input errors require their own
finite bounds. Uniform or output loss preserves the old Bernoulli structure
and reduces the new mean. For arbitrary path losses use actual row means
and do not silently assume(P2)'s p bound.

## 5. Randomized marginal PIT: the exact discriminator

For each method, use its TRUE UNCONDITIONAL marginal PMF pi_i and CDF F_i.
With independent classical jitters xi_i~Uniform(0,1), independent of the
photon counts and each other, set

    U_i=F_i(n_i-1)+xi_i pi_i(n_i).                            (P3)

Each U_i is EXACTLY Uniform(0,1): on its interval of length pi_i(s), the
conditional uniform density times event mass pi_i(s) equals1. Intervals
partition[0,1], ignoring null boundaries. Zero-probability counts need no
division. This is the specified randomized/checkerboard copula for discrete
data; a discrete copula is not unique without that convention. Counts remain
recoverable from their own inverse CDF almost surely. PIT standardizes marginal
geometry, rather than erasing all information or proving quantum correlations.

Apply the SAME top-q then greedy completion/refinement decoder to U-1/2 for
B, D, declared species controls, Gaussian and iid baselines. The decoder's
graph work and any discoveries are credited identically.
Here q=b for a balanced b-of-2b partition; any different shortlist/completion
size needs its own explicitly shared decoder contract. PIT-uniform marginals
do NOT imply uniform top-q inclusion when the copula is nonexchangeable.
Measure decoded anchor overlap/inclusion frequencies and retain D/Ycov/nonlocal
controls. Only IID uniform fields give an exactly uniform q-subset before
the common greedy decoder.

For a genuinely Gaussian field Y_i with known mean/variance, Phi((Y_i-mu_i)/
sigma_i) is uniform when sigma_i>0. A zero-variance marginal must use independent
uniform jitter, not the fixed value Phi(0)=1/2. Matching Gaussian raw means and
covariances does not match arbitrary photonic PIT bivariate laws. A gain over
that surrogate alone may be a non-Gaussian two-mode effect accessible to P43,
not an irreducible large-order mechanism. A non-Gaussian mean-field count
baseline needs its actual CDF or a separately charged calibration; otherwise
keep it as an explicitly NON-PIT-exact raw control. Do not weaken strong
classical controls by forcing them to discard useful scored graph information.

Finite PMF/CDF estimates do not justify exact PIT language. For a valid
estimated pmf p_hat, the one-mode uniformity error is exactly TV(p,p_hat)
under that estimated randomized transform (zero-width atoms included).
No corresponding joint-copula accuracy is automatically certified here.
Empirical CDFs need independent calibration/test samples and calibration
shots/calls charged; self-calibration on a test batch can manufacture ranks.
The theoretical formulas need precision checks in an implementation even
with(P2); no P46 numerical PMF was calculated here.

### Zero-transmission limit and a finite-N TV bound

If eta0=||T[:,A]||^2=0, every count is0 and pi_i(0)=1. Then(P3) is exactly
the IID classical jitter vector, for every photon species. The common decoder
can still output a partition, but all its information/work is classical.
This completion decoder explicitly lies outside P44's selected-vertices-must-
click premise; it does not refute P44 or rescue a quantum signal at zero counts.

More quantitatively let M=E[total detected photons]<=N eta0. The true PIT law
C obeys

    TV(C,Uniform([0,1]^m))<=min(1,M)<=min(1,N eta0).           (P4)

If M>=1 the assertion is trivial. Otherwise vacuum mass alpha>=1-M, and
the PIT box for all-zero counts has uniform-reference volume
beta=prod_i pi_i(0)>=1-sum_i Pr(n_i>0)>=1-M. On that box, C has constant
density alpha/beta, so its overlap with the uniform density is at least
min(alpha,beta)>=1-M. This proves(P4). Data processing preserves the bound
after any common decoder. The limit is for fixed N or N eta0->0; it is NOT
a dimension-uniform low-efficiency no-go when N eta0 is large.

## 6. Future protocol and costs: no run is authorized by this note

The target remains a positive held-out SEARCH result, not a change in a mean,
collision rate, stable rank or quartet. Fix p in{1/4,1/2}, zeta=1/4, ordering
seeds and label permutations before outcomes. Include every graph/anchor,
including already optimal anchors, R=0 cases and weak graph-response cases.
No outcomes or optimum masks enter W or the decoder. Any later tuning uses a
training split and its complete calibration/circuit/score budget.

Record source preparation and physical attempts separately from accepted
supports, photons, marginal calibration, matrix preprocessing, decoder graph
queries and all scored classical proposals. Minimum of every actually scored
frontend/matching/spectral candidate is the common credited incumbent.
Per-attempt raw improvement probability and accepted gain after the common
decoder must survive the total-cost comparison. No CF-only renormalization.

Controls must include:

- Same-U distinguishable law and independently selected distinguishable
  parameters under the same fixed budget; declared small-photon species.
- Exact-PIT iid uniform fields; Gaussian/Ycov with its precise matched quantities
  stated; raw strong mean-field control unless its CDF is honestly calibrated.
- Nonlocal feasible block/matching and spectral proposals from the SAME Delta,R,
  with O(b^3) matrix preprocessing available to them too; actual scores charged.
- Graph-programmed W versus R=0 Fourier and fixed seed permutation/sign
  controls recomputed as valid unitaries. W* and row/column gauge twists are
  EXACT probability null controls, not candidate performance gains. A generic
  phase scramble followed by QR does not hold intensities fixed and must not
  be called a pure phase control.
- Exact classical candidate/full-law replacement at any tested small size,
  with preprocessing and reuse counted. For growing b, bounded components,
  small species and DP/low-rank approximations remain serious comparisons.

Only the global nonlinear decoder functional and its joint dependence escape
the immediate local-mean oracle; their classical hardness, useful raw rate,
trainability and wall-time value remain UNPROVED. Dense reference mixing may
create mostly graph-blind collisions, and the matching/spectral frontend may
already explain every benefit. These are failure possibilities to retain,
not reasons to filter cases. Root encoding's A/B results take priority before
any separate P46 implementation; no existing pilot is altered here.

## Handoff and provenance

Proved analytically here, pending external review: rank-one/thin transport
invariant, hollow spectrum and binomial transfer, explicit centered polar map
and delocalization bound, collision/quartet diagnostics, one-mode PMF/PIT and
zero-transmission TV boundary. Positive optimization/cost hypothesis: OPEN.
These statements neither overturn P45-C's narrow replacement nor derive
quantum advantage from an unproved sampler bottleneck. A blind reviewer should
receive the separate P46 claim card before this author's derivation.
No P46 code/raw exists and no CPU slot has been consumed.
