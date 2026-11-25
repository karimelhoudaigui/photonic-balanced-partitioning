# P48 coherent-control marginals: reconstruction from the frozen cards

Adaptive lane; the cards already supplied candidate formulas. This is their
independent derivation from the stated models, not discovery or a novelty claim.
No author physics proof, P48 code, graph outcome or numerical fixture was used.
Active construction is the fixed spectral basis in card e30f75c; the earlier
Gaussian heat-frame idea is preserved but is not assigned a DEV run here.

Let V be an m-by-r isometry, r photons, q_a=|V_ia|^2 for one output mode,
mu=sum_a q_a. Then0<=mu<=1; IMPORTANT: do not normalize this row to mass1.

## Fixed-amplitude phase control

Use z_a=exp(i theta_a)/sqrt(r), with independent continuous uniform phases.
Conditional counts are multinomial(r,|Vz|^2), so the one-mode count is
Binomial(r,I/r), I=|sum_a V_ia exp(i theta_a)|^2. Phase orthogonality gives

    E I^h=(h!)^2 H_h,
    H_h=[t^h] product_a sum_(j=0)^h q_a^j*t^j/(j!)^2.

Thus its PGF in(s-1)^h has coefficients

    c_0=1, c_h=(r)_fall_h*h!*H_h/r^h.

Mean is c1=mu. Ordinary PMF is sum_(h=j)^r (-1)^(h-j)binom(h,j)c_h.
The product-coefficient DP is nonnegative; PMF inversion still has alternating
sums. Cauchy gives I/r<=mu, so its absolute inversion term sum is at most
binom(r,j)*mu^j*(1+mu)^(r-j)<=3^r. This supports adequate absolute precision
at r13/17 with Decimal80 but is not a relative-tail/interval certificate.

r+1 independent roots give the same COMPLETE multinomial law as continuous
phases: all count probabilities have degree r in phases and conjugates, so
nonzero exponent differences have magnitude<=r and average to zero under both.
Four roots do not suffice in general at r>=4. Column phases and permutations
do not change the averaged law, including for this finite-root implementation.

## Spherical-coherent control

For r>=2 let z be uniform on the complex unit sphere in C^r. Rotational
invariance gives |(Vz)_i|^2=mu*B, B~Beta(1,r-1). Consequently

    c_h=binom(r,h)*mu^h*E B^h
       =(r)_fall_h*mu^h/(r)_rise_h, c0=1.

An entirely NONNEGATIVE PMF construction first draws L~BetaBinomial(r,1,r-1),
then n_i|L~Binomial(L,mu). The beta-binomial weights are

    pi_l=(r-1)*r!*(2r-2-l)!/((r-l)!*(2r-1)!), 0<=l<=r,
    pi_0=(r-1)/(2r-1), pi_(l+1)/pi_l=(r-l)/(2r-2-l).

This follows by integrating a Binomial(r,B) over Beta(1,r-1), then binomial
thinning by mu. Mean is again mu. At mu1 the PMF is exactly these weights;
at mu0 it is delta0. r1 is Bernoulli(mu), not Beta(1,0). r0 permits only
mu0 and gives delta0; no sphere normalization of an empty Gaussian is defined.
For fixed phase r1 is likewise Bernoulli(mu), and an empty q is vacuum.
At mu1,r>1 the phase PMF need NOT be deterministic: a pointmass row gives
Binomial(r,1/r), whereas sphere gives the above beta-binomial law.

## Computational and claim boundaries

The phase DP is O(r^3), sphere positive mixture O(r^2), with no graph score,
photon draw, empirical CDF or source-state fitting. Exact small fixtures can
enumerate all(r+1)^r phases with rational cyclotomic norms at r<=3; sphere
can be integrated independently using exact beta moments/rational integrals.
Input subunit row mass must survive these calculations unchanged.

Haar mixing of a source basis can equate averaged raw B counts to spherical
coherent counts, but a V-dependent PIT does not commute with that averaging.
No no-go for the complete decoder is inferred here. The fixed spectral basis
is invariant to column signs/phases; generic simple marked spectra still need
gap/residual checks and retained degeneracies in finite precision. None of
these marginal identities implies an optimization gain, accepted positive,
QPU readiness, or state-of-the-art novelty.
