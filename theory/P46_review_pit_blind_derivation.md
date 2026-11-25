# P46 — blind reconstruction of marginal calibration and its limits

Reviewer: adaptive lane, after its completed negative P45-A pilot. Shared broad
project context is disclosed. This derivation uses only the coordinator's card:
CF source, N=12/14 photons, m=24/28 graph modes, arbitrary current passive U,
marginal PIT, D/b4/Gaussian/iid controls. No P46 physics-author proof or encoding
implementation was read before this file was frozen. No numerical work occurs
here. This is a calibration review, not a proposed research-program closure or
claim of novelty/positive optimization.

## 1. One-mode probabilities from the source definition

Condition on the graph, all past history, chosen source and current network
BEFORE this attempt is drawn. Source has one photon in each of N distinct modes
A. With uniform fresh loss eta set p_a=eta*|U_ia|^2 for a fixed measured mode i.
More generally p_a=|T_ia|^2 for a passive vacuum-environment contraction T.
Repeated input photons, false clicks, different internal-state structures and
conditional same-attempt operations require different formulas.

For identical photons let b_i=sum_a T_ia a_a+vacuum terms. Acting b_i^r on the
binary source removes r distinct photons. Each r-subset R has amplitude
r!*product_(a in R)T_ia and different hole sets are orthogonal. Consequently

    E[(n_i)_r]=(r!)^2*e_r(p_1,...,p_N),  0<=r<=N.

For every integer n>=0, z^n=sum_r (n)_r*(z-1)^r/r!. Thus the EXACT marginal PGF is

    G_B(z)=sum_(r=0)^N r!*e_r(p)*(z-1)^r.

For distinguishable photons, n_i is a sum of independent Bernoulli(p_a), so

    G_D(z)=product_a[1+p_a(z-1)]=sum_r e_r(p)*(z-1)^r.

For mutually orthogonal b4 species groups, compute a B PGF for EACH group and
multiply them; equivalently convolve their ordinary PMFs. Cross-group counts
are independent, even though photons within each group interfere. Do not use
one factorial for the total b4 photon number. Source membership must match the
ACTUAL species partition and remain transported under relabeling.

Writing c_r=r!*e_r for B, or c_r=e_r for D, the ordinary PMF is

    P(n_i=j)=sum_(r=j)^N (-1)^(r-j)*binom(r,j)*c_r.

All photon numbers0..N, including collisions and zeros, remain in these laws.
Using the CF-conditioned output distribution instead would calibrate the wrong
random variable. At eta=0, every marginal is delta_0. At an ideal deterministic
row it can be delta_1 or delta_0; these are valid atoms, not errors to remove.

## 2. Exact randomized PIT, including atoms and adaptation

Let p_i(j) be the TRUE current marginal and F_i its CDF, F_i(-1)=0. Draw xi_i
uniform on(0,1), independently for every mode and shot, independent of the
ENTIRE count vector and preexisting history. Set

    u_i=F_i(n_i-1)+xi_i*p_i(n_i).

Conditional on n_i=j this is uniform in the CDF interval of length p_i(j).
Those intervals partition[0,1], with mixture weights equal to their lengths;
therefore u_i is exactly uniform, conditional on the pre-attempt history.
Probability-zero values p_i(j)=0 cannot occur under the specified physical law.
An observed such atom is a model/numerical inconsistency to record, not a reason
to reject the shot, replace it, or invent a convenient interval.

Independent per-mode jitter matters. Reusing ONE xi across modes creates an
artificial dependence even for independent inputs. Cross-MODEL common random
numbers may be used as an explicitly paired comparison if independent of all
observations, but they do not make experiments independent replications. Seeds
for physical counts, PIT jitter and optional tie-breaking need distinct roles.

The vector u is GENERALLY NOT iid. Conditioning on the count vector gives a
uniform product rectangle, but mixing those rectangles with joint count
probabilities retains a checkerboard/distributional-transform copula. Fixed
total photons, graph-sensitive joint fluctuations, correlations within species,
and high-order effects can all survive. Marginal normalization alone proves
neither optimization usefulness nor exclusively many-body origin.

PIT removes all one-mode distributions, not just means/variances. Consequently
any surviving advantage of this declared decoder over D cannot be credited to
merely stronger individual bosonic variance. Gaussian, b4, phase-field and iid
controls remain needed to distinguish classical correlated copulas from an
interference-dependent optimization mechanism.

Use CURRENT conditional PMFs after each adaptive source/network choice. A
mixture CDF across settings, a source from another incumbent, or a CDF fitted
using current held-out counts is not justified by this proof. Selection of a
winning setting on the same training outcomes can bias winner-only diagnostics;
fresh frozen tests are still necessary even though each original row used a
correct analytic transform.

## 3. Gaussian and iid controls; the eta=0 invariant

For a Gaussian coordinate g_i with actual mean mu_i and POSITIVE variance v_i,
u_i=Phi((g_i-mu_i)/sqrt(v_i)) has the exact uniform marginal. Singular JOINT
covariance is harmless when this coordinate variance is positive. If v_i=0,
the coordinate is an atom: its randomized PIT is a fresh independent xi_i,
not Phi(0)=1/2. Replacing a zero variance by an arbitrary floor and applying
Phi does not give uniformity. A continuous NON-Gaussian hybrid with matched
moments also cannot be calibrated by Phi merely because its covariance matches.

If eigenvalue clipping changes a Gaussian factor L, its actual marginal
variance is sum_j L_ij^2. Calibrate that sampled Gaussian variance, while
separately reporting the discrepancy from the intended B covariance. Do not
quietly mix a clipped sampler with unclipped theoretical variances in its CDF.

At eta=0 the physical B/D/b4 counts are all zero; correct randomized PIT gives
independent uniform u_i for ALL these models. A Gaussian with zero covariance
must give the SAME iid control after atom randomization. Any graph-sensitive
output difference beyond independently sampled iid noise is a calibration,
seed, parameter, or resource mismatch. This is a decisive implementation check,
not an experimental advantage or a reason to submit photons to hardware.

The iid control can sample uniform coordinates directly. It does not need to
pay for an unnecessary PMF calculation. All shared graph/incumbent setup and
all model-specific calibration/sampling/decoding costs must be reported; equal
marginal laws do not make preprocessing costs equal.

## 4. Optional cheap exact-PMF correlated classical control

The known CONTINUOUS-phase mean-field sampler also admits a polynomial marginal
CDF, so calibration alone is not a reason to omit a correlated classical field.
Use phases uniform on[0,2pi), intensity I_i=|sum_a sqrt(p_a)*exp(i theta_a)|^2,
then N conditionally iid particles with probability I_i/N in mode i (loss is
an additional category). Define

    h_r=[t^r] product_a sum_(l=0)^r p_a^l*t^l/(l!)^2.

Phase orthogonality gives E[I_i^r]=(r!)^2 h_r. Its marginal factorial moments
are (N)_r E[I_i^r]/N^r, hence its PGF coefficients in(z-1)^r are

    c_r^MF = (N)_r * r! * h_r / N^r.

These determine its PMF by the SAME coefficient conversion. Product-polynomial
DP is O(N^3) per row, practical as a small-model control. This formula concerns
CONTINUOUS uniform phases; four-root phases can alias high powers and must not
be silently substituted at N12/14. A Gaussian CDF applied to this non-Gaussian
count/field law would likewise fail the exact uniform-marginal contract.
The mean-field model and phase-twirl ingredients are known, as already recorded
in P41/P45; this is a proposed implementation dictionary, not a novelty claim.

## 5. Cost, roundoff and auditable invariants

Elementary-symmetric DP and conversion to PMF each cost O(N^2) per output row,
O(mN^2) total. b4 PMFs need group DPs plus ordinary convolution; charge their
construction and cache keys. A cache key must include actual U/T, occupied
source, eta, model, b4 partition and precision. Adaptation that changes these
objects invalidates that cache. No photon measurements are needed to compute
these analytic PMFs, but their classical time and memory are not free.

The conversion has alternating sums. Negative coefficients, small atoms and
CDF endpoints near1 can suffer cancellation in float64; a polynomial-sized
computation is not automatically numerically stable or exact. Validate against
high-precision/exact small references; record normalization residuals, minimum
coefficient and largest correction. Clipping/renormalizing without such a
check makes this an approximate CDF and may change model comparison.

For a normalized nonnegative approximate marginal q with TV(p,q)<=epsilon,
its randomized PIT applied to data n~p is within epsilon TV of uniform: couple
n~p to n'~q with error epsilon and use the same jitter, for which the q-PIT of
n' is uniform. This is a ONE-MODE statement. Separately, if sup_j|F_q(j)-F_p(j)|
<=delta, then on the same n,xi the exact and approximate PIT values differ at
most delta because u=(1-xi)F(n-1)+xi F(n). Near ranking ties even tiny errors may
alter the decoder, so log a tolerance/margin diagnostic where appropriate.

Finite PRNG grids, floating-point Phi and endpoint clipping give approximate
machine versions of continuous uniformity. If inverse-normal transforms are
used, explicitly handle0/1 rather than produce infinities or drop the shot.
Never use an empirical same-sample rank transform to certify the claimed
analytic PMF: ranks can look uniform even for a wrong physical model.

Minimum preflight obligations: independent small full-Fock marginal reference
for B; independent Bernoulli enumeration for D; species convolution fixture;
normalization/positivity/moment checks; deterministic row and eta0; iid jitter
independence; current-source cache isolation; and cost/accounting metadata.
No fresh DEV or held-out numerical sample was used in this derivation.

## 6. A small-loss sanity bound, not a route-closing obstruction

For any nonnegative discrete count vector define q_i=Pr(n_i>0) and v=Pr(n=0).
On the lower rectangle R=product_i[0,1-q_i], randomized PIT has constant density
v/volume(R), since only the all-zero vector can reach its interior. Its overlap
with iid uniform density on that rectangle is min(v,volume(R)). Both v and
volume(R) are at least1-sum_i q_i, so

    TV(Law(u), iidUniform) <= min(1,sum_i q_i)
                          <= min(1,E sum_i n_i).

Uniform pure loss gives E total=N*eta and therefore the bound min(1,N*eta).
Zero-volume rectangles give the trivial bound1 and no division is needed.
Any fixed common decoder preserves this TV bound. It is weak/trivial at the
proposed ideal N12/14 pilot and does not order arbitrary finite-cost adaptive
optimizers. It supplies the eta0 endpoint sanity check and an explicit limit
to attributing a large low-loss effect to surviving optical copulas.

Finally, pointwise domination of RAW bosonic counts by a mean-field law does
NOT automatically survive MODEL-SPECIFIC PIT maps: f(F_B(n),xi) and
f(F_MF(n),xi) are different kernels. A unit-coefficient/no-go claim would need
its own comparison. Every proposed positive still faces reoptimized D,
correlated controls, strong feasible search, held-out graphs, labels/seeds,
independent replication and actual costs before any hardware or paper step.
