# Exact small-system noise model

This package provides theoretical scenarios, not a Belenos calibration or a
hardware prediction. It performs no remote call. All probabilities are per
injected attempt and retain collisions, lost photons and vacuum. There is no
automatic postselection or probability renormalization.

## Scope and conventions

`U[i,a]` maps spatial input mode a to output mode i. U is a square unitary.
`input_modes` lists distinct occupied spatial modes, one photon per entry;
repeated/bunched inputs are rejected by the interference routine. Arbitrary
mode order, odd numbers of modes, one mode, and the empty/vacuum source are
supported. The internal state of photon a is a normalized pure vector phi_a,
independent of the other internal states. Ideal detectors trace out this
internal degree of freedom. Correlated photons, arbitrary mixed internal states,
dark counts, multiphoton source contamination and drift are outside this model.

The internal Gram matrix is

    S[a,b] = <phi_a|phi_b>.

It must be finite, Hermitian, positive semidefinite and have diagonal one.
`gram_from_internal_states(states)` takes one normalized vector per row, without
normalizing the supplied vectors. `validate_internal_gram(S,k)` checks these
conditions without projecting S to another matrix. The all-ones Gram gives
fully indistinguishable photons; the identity gives fully distinguishable
photons. Neither convention refers to the spatial intensity-overlap Gram used
by the separate collision certificates.

## Probability formula, including complex phases

For k photons and output occupation t, choose an output list y with multiplicity
t_i for each mode i. Set

    A_sigma(y) = product_j U[y_j, input_modes[sigma(j)]].

Then the complete, internally unresolved Fock probability is

    p_S(t) = 1/(product_i t_i!)
             * sum_(sigma,tau in S_k)
                 A_sigma(y) conjugate(A_tau(y))
                 product_j S[tau(j),sigma(j)].

The orientation is `S[tau,sigma]`: it comes from the internal inner product
between the bra labeled tau and ket labeled sigma. The distinct occupied input
orbitals make the initial state normalized even when the internal vectors
overlap, so no input occupation factorial is needed. Repeated output rows
require the displayed output factorial. The formula is invariant under
rephasing each internal vector, while conjugating an entire complex Gram need
not preserve the distribution for a fixed complex U.

Derivation: expand the product of spatial/internal creation operators. For a
fixed ordered output list the internal vector is the sum, over assignments
sigma, of A_sigma times the tensor product of the assigned internal vectors.
Its squared norm produces the two permutations and their internal overlaps.
Dividing by the repeated-output factorial counts each Fock outcome once.
This agrees with Tichy's double-permutation formula, Eq.(19); here repeated
outputs and their factorial are kept explicitly. [Primary source, v3](https://arxiv.org/html/1410.7687v3#S3)

For a balanced two-mode beamsplitter the collision-free coincidence probability
is `(1-|S[0,1]|^2)/2`. At k>=3, pair exchanges involve products such as
`|S[a,b]|^2`, and three-cycles involve `S[0,1] S[1,2] S[2,0]` and its
conjugate. For the common real-overlap Gram with diagonal one and off-diagonal
r, these weights are r^2 and r^3 respectively. A single global interpolation
between the bosonic and distinguishable distributions does not implement that
model. A separately declared correlated source that randomly chooses between
two entire ensembles would be a different physical assumption.

An arbitrary mixed-state source generally needs a permutation distinguishability
kernel; substituting averaged overlaps into a pure-state Gram formula does not
provide that extension. [Tichy, Section III.6](https://arxiv.org/html/1410.7687v3#S3.SS6)

## Independent output losses

`apply_independent_loss(law, eta)` accepts a complete normalized distribution.
Each photon survives independently, without resolving its internal state. For
an initial occupation n and observed t with 0<=t_i<=n_i,

    L_eta(t|n) = product_i C(n_i,t_i) eta_i^t_i (1-eta_i)^(n_i-t_i),
    p_detected(t) = sum_n p_S(n) L_eta(t|n).

Eta may be a scalar or one survival probability per output mode. A vector
describes output-mode losses and cannot in general be commuted through U.
Uniform scalar loss does commute through passive optics. An equivalent
unitary dilation with environmental vacuum is

    [[sqrt(eta) U,       sqrt(1-eta) I],
     [-sqrt(1-eta) U,    sqrt(eta) I]],

followed by tracing the environment. A direct sum of two attenuated blocks
would not be this unitary dilation. The implementation evaluates the equivalent
classical thinning kernel after obtaining the full spatial distribution.

Uniform loss of a fixed N-photon source gives a Binomial(N,eta) detected-number
distribution, independently of U and S. Vacuum has probability `(1-eta)^N`.
The full N-detected sector is exactly `eta^N * p_S`, including its collisions.
Thus any success event requiring all N photons has probability `eta^N` times
its lossless probability, and its conditional statistics inside that sector
are unchanged. For example, `.537 * .9^4 = .3523257`. A threshold event that
accepts fewer than N clicks can receive additional contributions from lower
photon sectors and must instead be evaluated from the full lossy law.

The predicate `all(n_i <= 1)` also accepts vacuum and one-photon outcomes.
For the N=k balanced-partition pipeline, a valid collision-free outcome must
additionally satisfy `sum(n_i) == k`. Applying only the no-collision predicate
after loss would change the acceptance event.

## API and numerical/resource limits

```python
import numpy as np
from photonic_balanced_partitioning.noise import (
    gram_from_internal_states, noisy_distribution,
)

U = np.array([[1, 1j], [1j, 1]]) / np.sqrt(2)
states = np.array([[1, 0], [.6, .8]])
S = gram_from_internal_states(states)
law = noisy_distribution(U, [0, 1], S, eta=.9)
vacuum_probability = law[(0, 0)]
detected_number_probabilities = law.sector_probabilities()
```

The individual routines are `partial_distinguishability_distribution(U,modes,S)`
and `apply_independent_loss(law,eta)`. `noisy_distribution` composes them.
The result is an immutable mapping of occupation tuples to probabilities plus
`raw_total_probability`, `minimum_raw_probability`,
`maximum_imaginary_residual`, `roundoff_clipped_mass`, and the explicit status
`FLOAT64_ESTIMATE_NOT_INTERVAL_CERTIFIED`.

Unitarity, Hermiticity, diagonal-one and PSD validation use absolute tolerance
1e-10. There is no projection onto a physical matrix. Probability totals,
nonnegativity and imaginary residuals are checked to 1e-10. A violation raises
an exception. Tiny negative probabilities within this numerical tolerance are
clipped to zero and their mass is recorded; positive probabilities are never
rescaled. Diagnostics are not rigorous error intervals or experimental
confidence statements. A generic input mapping to the loss routine must be
nonnegative and normalized; a subnormalized collision-free selection is rejected.

The hard limits are five photons, 32 modes and 2,000,000 permutation-pair or
thinning terms per stage. `max_terms` can lower the work allowance but cannot
raise the hard cap. The interference work is
`C(m+k-1,k)*(k!)^2`; the loss work is `sum_n product_i(n_i+1)` over supplied
occupations. Inputs beyond these limits fail before enumeration. This is a
validation component, not a scalable many-photon simulator.

All parameter values in examples/tests are declared theoretical scenarios.
No transmission, internal overlap, detector efficiency, or phase distribution
is asserted to have been measured on Belenos. Perceval1.3.0's installed Source
uses a phenomenological source model and a two-photon mean-overlap parameter;
that parameter is not treated here as an arbitrary complex Gram calibration.
The local Perceval cross-check validates ideal full distributions only. The
complex Gram path is independently checked by explicit creation operators in
spatial-times-internal modes, then tracing out the internal occupations.
