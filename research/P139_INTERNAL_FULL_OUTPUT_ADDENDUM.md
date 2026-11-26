# P139 — Internal states and full-PNR addendum

2026-11-26. Manual reconstruction of ROOT's extension; parent
35d84e4966da882d0782290030d7e2233d6203a9. PROOF CANDIDATE pending peer review.
The original 119-line P139 source is unchanged. No novelty, implementation,
import/AST, code/numerical/symbolic execution, graph/RNG/raw read, native/QPU
or manuscript work is claimed or performed.

## Explicit instrument and endpoint hypotheses

Fix K>=2 CF source photons, finitely many FULL output modes M>=K, vacuum
auxiliaries, and a real-analytic occupied isometry W_x in C^(M-by-K) on
(-rho,rho), physical for 0<=x<rho. A full unitary with these columns suffices.
All spatial output counts are considered, including dump modes and collisions.
Assume W_0 is MONOMIAL on its occupied columns: each column has exactly one
unit-modulus entry and these K nonzero entries occupy DISTINCT output rows.
Denote that deterministic CF output pattern n0. Both fully B and D, and all
internal states admitted below, consequently produce n0 with probability one.
This explicit premise is stronger than observing suppression of a few events.

For any count vector n with total K, repeat W_x's rows according to n;
n!=product_j n_j!, and a_sigma(x) is the product of entries for assignment
sigma of the K distinct source columns to these ordered output slots.
For a normalized physical internal state, assume the standard internal-blind,
species-independent passive spatial law

    p_J(n;x)=(1/n!)*sum_(sigma,tau)
                   a_sigma(x)*conj(a_tau(x))*J_(sigma,tau)(x),
    p_D(n;x)=(1/n!)*sum_sigma |a_sigma(x)|^2.          (1)

The physical normalized kernel has diagonal 1 and |J_(sigma,tau)|<=1.
It may describe B, proper species groups, mixtures or partial internal
distinguishability, and may depend on x; no analyticity of J is required.
An internal-state-dependent spatial device is outside these hypotheses.

## Uniform internal-state bound and analytic retuning

Triangle and Cauchy-Schwarz, with the SAME output divisor in both arms, give

    0<=p_J(n;x)<=(sum_sigma|a_sigma(x)|)^2/n!
                 <=K!*p_D(n;x).                    (2)

For n different from n0, the monomial endpoint forces EVERY a_sigma(0)=0, even for repeated
output rows. Either every analytic path germ vanishes identically or the
positive D sum has p_D(n;x)=a_n*x^(2v_n)*f_n(x), a_n>0,v_n>=1,f_n(0)=1.
There is no cancellation of its leading coefficient. The constant n! only
changes a_n, not v_n or the ratio p_D(n;c*x)/p_D(n;x).
For a nonzero D germ choose c=ceil(sqrt(K!+1)), as in the original. The ratio
tends to c^(2v_n)>=c^2>K!, so p_D(n;c*kappa)>p_J(n;kappa) for sufficiently
small kappa, simultaneously for ALL admitted J(kappa). Identical-zero D
germs also force p_J to be zero there by (2). There are only C(M+K-1,K) output
counts; the finite-radius argument of P139, including zero-germ neighborhoods
and kappa<rho/c, gives ONE common positive window for every n different from n0.
This window need not be explicit or uniform in M,K or the spatial curve.

## Common decoding, resource scope and exclusions

Let L(z|n) be a classical count kernel IDENTICAL between the two arms AND
between kappa and c*kappa. For bounded g(z)>=0 define h(n)=sum_z L(z|n)g(z)
and require h(n0)=0. Summing the pointwise inequalities yields raw D utility
>=raw J utility, strictly if some reachable nonzero D germ has h(n)>0.
This permits a specified repair of non-CF records, unlike the original hold
rule, but not a parameter-dependent repair applied differently to the arms.
Known-incumbent preparation at n0 is not credited as optimization benefit.

The D comparator must admit c*kappa along the SAME spatial curve. Both
modeled attempts inject K photons; setup, tag preparation, synthesis,
precision, wall costs and calibrated hardware effects are not matched here.
External loss already present at zero generally destroys the monomial FULL
endpoint. It is not silently removed: any transfer via a terminal count
kernel must separately establish that it is common and still induces h(n0)=0.
No arbitrary noisy channel, rare conditioned sector, adaptive continuation,
growing-dimension uniformity, efficient sampler or complexity advantage follows.
This is a local analytic obstruction near a known deterministic incumbent,
not an all-strength/global optimizer no-go or a QPU validation. Only this
addendum was written; earlier sources, negative results and raw data are intact.
