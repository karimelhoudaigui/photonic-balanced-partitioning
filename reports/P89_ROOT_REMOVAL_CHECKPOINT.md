# P89: source-removal limitation accepted, full optimizer open

ROOT read all215 lines of the frozen reconstruction and149 lines of the
exact-source review, and separately checked the counting argument, edge
indicators and both K4 examples by hand. The scoped result is accepted.

Primary sourcef775f68233279cd3551f28a1176275596f607ed1, SHA256
e99a1e32ca6ea64c4b038fda1ef31ce8ee8e902cfa7feaa27737567d31ab7350.
Exact audit68baaeb8ed06466dbad688b4306e17c97bae8491, SHA256
eef75599183c17428ce3c7785c5e84a173c38f3b3db4235a6abfe684dd0d38d2.
ROOT supplied the candidate/formulas before reconstruction. Reviewers
use separate agent contexts, not independent discovery, external referees
or novelty clearance. Neither author opened a DEV result or ran numerics.

With ideal fresh uniform independent source marks, the frozen compiler's
source-label blindness gives an exact product law, for every loading eta:

    Pr(R,Y | G,S,r)=mu_(G[T],r)(Y)/binom(K,r).

R is the physical labeled removal BEFORE complement canonicalization.
The proof averages the source ordering; it does not claim that a fixed
PCG seed is a source of mathematically independent randomness. The photon
receiver law mu can retain high-order interference and is not proved
efficiently classically samplable. For a prescribed desired removal,
conditioning on Y cannot increase its chance above1/binom(K,r).
At K8,r4 that is1/70, not a bound on optimization success.

The exact raw cut mean is

    a_r W(S)+(1-r/K)Wcross+E_mu cut_G[T](Y)
       +(2r/K-1) sum_(j in T) d_S(j)Pr_mu(j in Y),
    a_r=2r(K-r)/(K(K-1)).

At half replacement the receiver-dependent cross-edge term vanishes.
At both endpoints it returns the old cut. Complement orientation
preserves these cost identities, not a new removal-mask distribution.
Nonlinear quench, acceptance, resource-selected subsets and adaptive
incumbents need not obey the product law or the raw mean formula.

Source-aware receivers can break R/Y independence while R remains
marginally uniform under fixed port loading. Cross-edge access alone
preserves independence but can make mu depend on the full graph. The
two explicit marked K4 witnesses have raw size-weighted differences
-1/2700 and-1/675; they are not conditional normalized covariances or
relabeling-robust optimizers. Steering marginal removals requires changing
the loading or assignment policy. Such classical information must be
charged and exposed to the distinguishable/classical controls.

This identifies a precise design limitation and potential escape; it
does not reject the full P82 optimizer without its controlled screen.
The frozen pilot is unchanged, its main remains unrun at this checkpoint,
and no positive, QPU or manuscript claim follows. CLAIM-042 remains OPEN.
