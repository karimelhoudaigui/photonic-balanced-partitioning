# P48 pre-experiment mathematics: heat frames, source basis and two coherent controls

Physics reconstruction, 2026-11-25. No code/run/QPU. The coordinator's
latest card replaces a low-eigenvector basis by a heat-filtered Gaussian
polar frame; that later card is the target below. It prospectively proposes
N=26/34, r=N/2, tau=0/4 and new graph seeds, not a completed result. This
note neither fixes additional settings nor infers a performance sign.
The prior hollow cancellation is separately preserved in
`theory/P47_collective_quartet_obligation.md`, commit
`cd8cbb3c0b52593d9ee621620c86fc07bc87d86a`.

## 1. Heat-polar construction and its exact covariance

Let L be the combinatorial Laplacian of a real, symmetric graph with
nonnegative edge weights. L>=0. Define Lhat=L/||L||op when L!=0, and 0
otherwise. Its spectrum lies in [0,1]. For an N-by-r complex Gaussian
matrix Z, with 1<=r<=N, put

    E_tau=exp(-tau Lhat), Y_tau=E_tau Z,
    V_tau=Y_tau(Y_tau*Y_tau)^(-1/2), tau>=0.             (1)

For full COLUMN rank Z (not full row rank when r<N), E_tau is invertible,
V_tau*V_tau=I_r, and

    sigma_min(Y_tau)>=exp(-tau)sigma_min(Z),
    sigma_max(Y_tau)<=sigma_max(Z),
    cond(Y_tau)<=exp(tau)cond(Z).                      (2)

These follow from exp(-tau)I<=E_tau<=I and singular-value inequalities.
Continuous independent complex Gaussians have full column rank almost
surely. Finite PRNG/float implementations still need rank/residual checks;
no failed/ill-conditioned case may be silently replaced by another Z.
The L=0 branch is V_tau=polar(Z) for all tau. Using the SAME Z for tau0/4
isolates the graph filter; the tau0 network is graph-blind, while its graph-
aware completion decoder need not be graph-blind.

For any vertex permutation Q, carrying L to QLQ* and Z to QZ gives
Y_tau->QY_tau and V_tau->QV_tau exactly. Fresh isotropic Z has the same
distribution after this row permutation, but exact pathwise relabeling
requires carrying Z and all decoder priorities, not merely reusing a seed
to regenerate an unrelated row order.

Complete V to an N-by-N unitary U=[V,Vperp] and inject one photon in each
of its first r ports. All other inputs are vacuum. Occupation laws depend
only on V, not on the arbitrary vacuum-column completion. Record the frame
and the actually used numerical completion/residuals. This is a passive
spatial construction, not preparation of a known partition. Construction,
matrix exponentiation, polar factors and decoder preprocessing are classical
work shared with baselines, not free optical input.

## 2. Source-basis rotations are physical, unlike column phases

For a unitary R on C^r, V->VR leaves P=VV* and row norms
mu_i=P_ii=sum_a|V_ia|^2 unchanged. It generally changes the distinct-input
CF state and its law: the state is the product of r DIFFERENT creation
operators, not a basis-invariant filled fermionic shell. Pure column
phases only multiply the CF state by one global phase and have no effect.

The heat-polar map has an additional exact symmetry:

    polar(YR)=polar(Y)R.                               (3)

Since ZR has the same Gaussian law as Z, V_tau is right-unitarily invariant.
Conditional on its projector P, its orthonormal basis is Haar distributed
on that subspace (the unique invariant law on its U(r) fiber). This holds
for the heat-guided case too; the filter changes the subspace distribution,
not this right-basis symmetry. No claim that P itself is graph-blind follows.

## 3. Spherical control and its coefficients

Let z be uniform on the complex unit sphere C^r, sample intensities
p_i=|(Vz)_i|^2 and then draw Multinomial(r,p). Sum_i p_i=1; every draw
retains exactly r counts. The method is classically sampled using a
normalized complex Gaussian z, one Vz product and a multinomial. For r>=2,

    p_i has law mu_i B, B~Beta(1,r-1),
    E[p_i^h]=mu_i^h h!/(r)_(rise,h).

With (r)_(fall,h)=r(r-1)...(r-h+1), its one-mode PGF is

    E[zeta^(n_i)]=sum_(h=0)^r c_h(zeta-1)^h,
    c_h=(r)_(fall,h) mu_i^h/(r)_(rise,h), c_0=1.        (4)

These are SHIFTED-PGF coefficients, not unscaled factorial moments:
E[(n_i)_(fall,h)]=h! c_h. At r=1, p_i=mu_i deterministically and the
marginal is Bernoulli(mu_i); Beta(1,0) is not a distribution. r=0, if
included, is a separate vacuum branch with PGF1 and pure randomized-PIT
noise, rather than division by a zero rising factorial.

A cancellation-free marginal evaluation is available. Draw
L~BetaBinomial(r,1,r-1), then n_i|L~Binomial(L,mu_i), for r>=2. This
has the same mixture representation as Binomial(r,mu_i B). Explicitly

    w_l=Pr(L=l)
       =r!(r-1)(2r-l-2)!/[(r-l)!(2r-1)!], 0<=l<=r,
    w_0=(r-1)/(2r-1),
    w_(l+1)/w_l=(r-l)/(2r-l-2), 0<=l<r,
    Pr(n_i=s)=sum_(l=s)^r w_l binom(l,s)mu_i^s(1-mu_i)^(l-s). (5)

All terms are nonnegative; this costs O(r^2) arithmetic per row. Endpoint
mu=0/1 can be handled exactly. Float evaluation still needs residual/error
accounting; a positive formula alone is not an interval certificate.

## 4. Fixed-modulus phase control: continuous phases matter

Let z_a=exp(i theta_a)/sqrt(r), with INDEPENDENT UNIFORM CONTINUOUS theta_a,
then sample Multinomial(r,|Vz|^2). Again normalization follows from V*V=I.
Writing q_a=|V_ia|^2 and mu_i=sum_a q_a<=1, expansion and phase integration
retain exactly the monomials with matching exponents for every a. Hence

    E[|(Vz)_i|^(2h)]
       =(h!)^2/r^h [t^h] product_a sum_(m=0)^h q_a^m t^m/(m!)^2,
    c_h=(r)_(fall,h) h!/r^h
       *[t^h] product_a sum_(m=0)^h q_a^m t^m/(m!)^2.   (6)

The coordinator's formula is correct under those phase assumptions.
It does NOT apply to P46's four roots of unity for r>=4: exponent
differences divisible by4 survive that discrete average, adding alias
terms. A grid of Q-th roots with Q>r suffices for all h<=r; continuous
phases are another valid choice. An unchanged fourth-root sampler would
instead need its own correctly calibrated/countable PMF, not formula (6).
The two coherent controls are distinct from independent distinguishable
photons, although all three have mean count mu_i.

Naive truncated polynomial products give (6) in O(r^3) arithmetic per row,
followed by a signed binomial inversion. Precision and coefficient
cancellation must be tracked separately from the exact algebra. The
spherical positive construction (5) is available without such inversion.

## 5. An exact raw-law obstruction, with an important PIT boundary

There is a strong classical explanation to test, not assume away. In
r input modes with r identical photons, Haar-averaging the rotated CF
state gives

    integral_R Gamma(R)|1,...,1><1,...,1|Gamma(R)* dR
       =I_(Sym^r C^r)/binom(2r-1,r).                  (7)

The same state is obtained by averaging |z>^(tensor r) over uniform
unit sphere z. To justify this without a numerical twirl: either average
is invariant under all U(r); commuting with mode phases makes its Fock
matrix diagonal, and commuting with two-mode mixing generators forces
equal diagonal entries along every connected occupation move. The trace
is1 and there are binom(2r-1,r) occupations. This proves (7) for both
ensembles. A condensate |z>^(tensor r) measured after V has exactly the
multinomial law used by the spherical control.

After embedding by V, the common normalized OUTPUT density matrix is

    Pi_(Sym^r range(P))/d_r, d_r=binom(2r-1,r),          (7a)

where Pi is the orthogonal projector on Sym^r range(P), inside the
N-output r-photon Fock space. Its rank and trace are d_r; division by
d_r makes trace exactly one. Vacuum modes outside the subspace do not
multiply this dimension by N or r!. In an ordered tensor representation
the same operator acts on the symmetric subspace, embedded isometrically;
no additional factorial normalization is inserted. Equations (7)/(7a)
concern a Haar basis average CONDITIONAL ON P, not the density matrix at
an individual basis and not an average over graphs or projectors.

Therefore, conditional on P, the B raw count law averaged over its Haar
source basis is EXACTLY the spherical raw count law. The heat-polar Z
construction has this basis symmetry. The phase-control law has the same
Haar-basis average too, since Rz is uniform on the sphere for any fixed
unit vector z. This does not equate the laws for an individual frozen V.

For a fixed postprocessing rule depending only on graph/P/counts and
fresh common randomness, let q_R be the B probability of an improving
event in basis R. For T iid attempts with that basis fixed,

    E_R[1-(1-q_R)^T] <= 1-(1-E_R q_R)^T,               (8)

by concavity. The right side is the success probability of the iid
spherical control under that SAME rule. This gives an averaged best-of
comparison, conditional on P, under precisely this fixed-rule assumption.

Do NOT apply (7)/(8) blindly to the planned model-specific PIT. Exact B
marginal PMFs depend on V's basis, while the spherical PMFs depend only
on mu_i. If the B decoder uses those basis-dependent CDFs, its map itself
depends on R: averaging the raw state does not commute with that changing
postprocessing. No P48 impossibility theorem or dominance after own-PIT
follows here. This is the smallest explicit loophole/obligation, not a
reason to omit the spherical control. r=1 is a useful boundary: B, D,
spherical and continuous-phase raw count laws all coincide exactly.

## 6. Remaining scientific and accounting obligations

The B, D and spherical off-diagonal second moments are respectively

    mu_i mu_j+|P_ij|^2-2sum_a q_ia q_ja,
    mu_i mu_j-sum_a q_ia q_ja,
    (r-1)/(r+1)*(mu_i mu_j+|P_ij|^2), i!=j.           (9)

A graph/program can change these means; their exact polynomial evaluation
does not solve global optimization or certify useful best-of tails.
The planned question must be explicitly NONLINEAR/PIT/search performance,
with separately retuned D, Gaussian, spherical and phase controls plus
strong spectral/rounding/local and collective feasible searches. The same
V/P/eigenspace or heat preprocessing, priorities, decoder grid, every
scored candidate and all calibration/PMF work are shared and charged.
The classical spectral family must receive the same low-L information.
No favorable basis, ordering, failed-rank or graph filtering is licensed.

Nothing in (1)-(9) supplies a positive performance sign. Heat-polar frame
construction, precise coherent baselines and the basis/PIT distinction are
the pre-experiment mathematical checkpoint; the useful collective gain
remains open. This note is self-derived before any P48 code/raw, with no
new external theorem or novelty claim and no numerical evidence.
