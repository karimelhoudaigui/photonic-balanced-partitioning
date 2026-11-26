# P129 — Independent finite-phase replacement review

2026-11-26. Reviewer P66, non-author of P129. Method: proof-audit.
Exact target: research/P129_FINITE_PHASE_MULTINOMIAL_REPLACEMENT.md,
ALL 190 lines at 6bee40d85ea941818959e4641cabffa009bbf480, SHA256
515d2c2ac9b2e4763d17d591691ff8aa71e004fd77400b0d8364e2d5092870b8.
Own parent: 25b19a0fca6ef0f2e5af540819f4fa1c60b3b623.
Original source and all other routes/experimental artifacts were left unchanged.

## Claim and verdict

For a known CF K-photon source, a complex occupied-input contraction T with
certified ||T||op^2<=eta<1, and vacuum loss, the stated finite-phase mixture of
K categorical draws approximates the full raw signal PNR law within
tau(K,eta)=E[1-(K)_L/K^L], L~Bin(K,eta).
The additional implementation error is <=epsilon for encoded T in Q(i), with
deterministic polynomial bit work and a fixed finite number of fair bits.
All collisions and vacuum remain in the count alphabet; no postselection occurs.

**Primary verdict: proved as written under the stated input model.**
No material correction requested. I independently reconstruct the trace-distance,
folding, rounding and bit arguments below. This is a structural-error sampler:
the extra epsilon is controllable, while tau need not be small. The statement
is not an arbitrary-accuracy FPRAS for the original bosonic law at fixed eta/K.

Dependencies: normalized CF input and passive vacuum channel conventions;
finite root orthogonality; elementary diagonal trace distance/CPTP contraction;
binomial thinning; rational Taylor/arctangent bounds and exact integer sampling.
No permanent-estimation oracle, native backend or load-bearing computation occurs.
The known Oszmaniec/Brod separable construction is attributed, not assumed novel.

| Obligation | Target section | Result |
| --- | --- | --- |
| Finite phase twirl without aliasing | 1, Eqs. (2)-(3) | passed |
| Fixed-l trace distance and endpoints | 1, Eq. (4) | passed |
| Spectral loss factor and binomial mixture | 2 | passed |
| Folded multinomial sampler | 2 | passed |
| Birthday bound and ideal means | 2-3, Eqs. (1),(5) | passed |
| Disk-constrained rational roots | 4 | passed |
| Categorical TV and finite dyadic coins | 4, Eq. (6) | passed |
| Encoded-input bit length and fixed caps | 4 | passed |
| Perturbed T surrogate-law coupling | 4 | passed |
| Source scope and resource interpretation | 3,5 | passed with stated limits |

## 1. Reconstructed states and channel law

In normalized Fock coordinates the l-fold orbital tensor has amplitude
sqrt(l!/(product_i n_i!))*product_i z_i^(n_i)/K^(l/2).
For an off-diagonal pair of occupations the phase difference in each coordinate
is an integer between -l and l. Because l<=K<M, the only multiple of M in
that interval is zero. Independent M-root averaging therefore kills exactly
all unequal occupation pairs. Merely taking M=K would not establish this.
The surviving diagonal is the multinomial l!/(K^l product_i n_i!).

Each CF occupation has surrogate-to-target ratio (K)_l/K^l. Its sum over the
binom(K,l) CF occupations is precisely that ratio; every other occupation has
zero target mass. The two states are diagonal, so half their l1 difference is
one minus this overlap. This proves Eq. (4), including l=0 and l=1 giving zero.
No claim of globally optimal separable approximation is needed for this proof.

For eta>0, R=T/sqrt(eta) is a contraction. Composing uniform vacuum loss of
intensity eta with its passive vacuum channel gives the same occupied transfer
T and hence the same signal channel. Independent losses before R turn the CF
source into the uniform CF-subset state rho_l conditional on l, with binomial
weights. Orthogonal input number sectors make the mixed input trace distance
exactly tau. After R, different input number sectors can feed the same output
number: only contraction of distance, not equality of output TV, is justified.

For fixed phase z and l, a condensate through R has multinomial signal/loss
probabilities |(Rz)_j|^2/K and the remaining loss probability. Draw z before l.
Replace the binomial choice of l by K independent Bernoulli survivals and then
apply the same single-particle categorical distribution to each survivor.
Each resulting signal probability is eta*|(Rz)_j|^2/K=|(Tz)_j|^2/K.
The other outcomes collapse into a single per-trial loss category. This proves
the direct K-trial sampler exactly, not a Poisson approximation.
Its probability vector is valid since ||Tz||^2/K<=||T||op^2<=eta.
The K trials share z; their unconditional dependence must not be discarded.

The fixed-l distance is a collision probability for l uniform labels on K
source positions. Its union bound is binom(l,2)/K. Averaging over L yields
E[L(L-1)]/(2K)=(K-1)eta^2/2, with the independent upper bound one.
K=2 gives exactly tau=eta^2/2; K=1 has no structural error. K=0 is a separate
vacuum branch. The eta=0 certificate forces T=0, so direct vacuum is exact.

M>=2 gives E[z_i conjugate(z_h)]=delta_ih. Thus K*E p_j equals
sum_i |T_ji|^2, matching the CF source's one-body density matrix. This proves
every stated ideal mean. The rounded finite-bit law is not asserted to preserve
those means exactly, nor is the ideal phase-correlated law generally the
independently injected distinguishable-photon law.

## 2. Reconstructed finite-bit implementation

For delta=epsilon/(4K), a root approximant w within delta/2 of a unit root
has modulus <=1+delta/2. Dividing by 1+delta/2 gives a Gaussian-rational
zhat in the closed unit disk and root error <=delta/(1+delta/2)<=delta.
This radial contraction is essential: unconstrained coordinate rounding could
make the rational loss residual negative at a boundary contraction.

The proposed rational root computation has a deterministic accuracy schedule.
For theta=arctan(1/5), tan(4theta)=120/119. Subtracting arctan(1/239) gives
tangent one and an angle in (0,pi/2), proving the displayed Machin identity.
Arctangent series at those two rational arguments have geometric certified tails.
With the resulting bounded rational angles, sine/cosine factorial tails give
the required coordinate precision in polynomially many terms/bits in log(1/delta).
Both angular and Taylor errors must be included; for example pi error <=delta/32
and each Taylor error <=delta/8 already give complex error <delta/2.
M<=2K permits a polynomial table for all labels, with no real-number oracle.

Using the same root labels couples z and zhat with vector error <=sqrt(K)*delta.
After T/sqrt(K), v and vhat have norm <=1 and separation <=delta.
The signal-probability l1 error is bounded by
(||v||+||vhat||)||v-vhat||<=2delta. The loss difference is at most that signal
l1 error, so signal-plus-loss categorical TV is also <=2delta, not twice it.
The K-draw and aggregated-count error is <=2Kdelta=epsilon/2.
All probabilities actually computed use rationals |T zhat|^2/K; no sqrt(K)
is needed by the implementation. The loss residual is nonnegative exactly.

Rounding every signal probability downward to a denominator D moves only its
discarded mass to loss. Thus the categorical TV is exactly the total discarded
signal mass, <m/D. The chosen dyadic D>=2Km/epsilon makes K-draw error <=epsilon/2.
Integer weights sum exactly to D, so each CDF draw consumes exactly log2(D)
fair bits without rejection or an abort. Uniform M-root labels likewise use
exactly log2(M) bits per source coordinate. All K trials are performed.

The root table has polynomial length; exact rational products/sums in a matrix
vector multiplication and the subsequent floors have polynomial encoded size.
Taylor denominators/factorials also have polynomial bit length in their bounded
term counts. With K fixed-length CDF choices the random-bit total is exactly
K*(log2(M)+log2(D)); count output is m integers in [0,K]. Therefore the claim
is worst-case finite-bit, not an expected-time categorical sampler in disguise.
No dependence polynomial in 1/epsilon is hidden in the setup: its precision
and table computations have the claimed polynomial bit-length dependence.

## 3. Robustness, attribution and limits

For contraction Ttilde and ||T-Ttilde||op<=zeta, couple the SAME exact root
labels. The two vectors differ by <=zeta, so the same categorical argument gives
TV(Q_T,Q_Ttilde)<=2Kzeta. A rounded sampler for Ttilde consequently has target
error <=tau(K,eta)+2Kzeta+epsilon, with eta still certifying the target T.
This is a surrogate-law coupling, not an assertion about quantum-channel diamond
distance or hidden optical states. Arbitrary unencoded complex T has only the
ideal statement; undocumented eigenvectors or column efficiencies supply no bits.

Column averages cannot substitute for the spectral certificate. For example,
T=(1/2,0,...,0) has spectral eta=1/4 but mean column transmission 1/(4K).
The true total count is Bernoulli(1/4); the ideal surrogate count is
Bin(K,1/(4K)). Already K=2 gives TV=1/32, whereas substituting the column mean
would falsely promise 1/128. This does not refute the actual spectral bound,
which uses eta=1/4 and correctly permits tau=1/32 in that case.

The exact-version primary leaf previously extracted in P127 is Oszmaniec/Brod,
[arXiv:1801.06166v1](https://arxiv.org/html/1801.06166v1), Theorem 1/Eqs. (20)-(23)
and Section IV.2/Eqs. (25)-(29). Its separable approximation and mixed input
distance are already known; the present proof does not need its optimality claim.
Finite twirling, folding and bit arithmetic above are explicit project derivations.
No global novelty check or source-independent priority clearance is claimed.

Common decoding contracts TV. Common classical-observation adaptive policies can
sum uniform per-history errors when every call has a fresh specified CF source
and a valid supplied matrix/certificate; coherent memory and timing histories
are outside this consequence. Conditioning on rare events is not TV contraction.
Every classical setup/phase/decoder cost remains paid. This theorem supplies
neither cheap preparation of a condensate on hardware nor a graph-optimization
advantage, practical speed comparison, source/loss calibration or QPU permission.

Full exact source was read before verdict; its Git-blob SHA256 was verified.
Only manual derivation, text reads, metadata and this review's Git operations
were used. No scientific imports/AST, numerical program, RNG, tests, native calls,
raw outcomes, runner, manuscript or QPU activity. No other route was audited here.
