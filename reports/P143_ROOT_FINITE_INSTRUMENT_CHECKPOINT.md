# P143 ROOT checkpoint — finite tag-blind instruments in a weak window

26-Nov-2026. ROOT FULL read103-line source82682862 and103-line non-author
review83d06aee, with independent manual reconstruction of the operator
bound, detector-sink model, analytic cases and exclusions. Original hashes
are recorded in the review. No scientific program, RNG, new graph/matrix,
native/QPU call or paper edit was used. This is agent mathematical review,
not external peer review, physical replication or a claim of priority.

## Accepted statement

K photons initially occupy distinct orthogonal CF source modes; count ALL
prepared helpers in K. In first quantization the K! ordered source-mode
permutations span projector P. Physical internal states give a positive
trace-one spatial density supported on P. Fully orthogonal source tags give
rho_D=P/K!, hence rho_J<=P=K!*rho_D, even for kappa-dependent internal states.
The labelled spatial space is essential; rho_D is not a symmetric pure
spatial Fock state. Common positive spatial effects therefore give

    p_J(z;kappa)<=K!*q_D(z;kappa).

Finite ideal tag-blind passive gates/count detection/conditional routing
admit such common INITIAL effects. Detected photons can be retained in
private non-reinteracting virtual sink modes until the final trace. This
reproduces destructive statistics and avoids an unjustified Markov model
for only the surviving spatial density. It is a mathematical construction,
not a proposed QND or storage capability on Lucy.

For a FIXED finite raw alphabet, require q_D(z;0)=delta_z,z0, real-analytic
probabilities through zero, and admitted retuning c*kappa. Every nonzero
off-null germ has positive leading coefficient and integer valuation>=1.
With c=K!+1, a finite common window has q_D(z;c*kappa)>p_J(z;kappa) on all
reachable off-null events. Identical-zero germs and their neighborhoods
remain included. A common nonnegative utility h with h(z0)=0 inherits this
raw-attempt order. The radius is not explicit or uniform in dimensions.

If a finite analytic Kraus realization is supplied, off-null probabilities
are sums of squared analytic norms and their valuations are even>=2.
Then c=ceil(sqrt(K!+1)) suffices. Probability analyticity alone does not give
that smaller factor; a linear kappa probability has a sqrt(kappa) amplitude.
ROOT independently checked this distinction and the physical one-photon
tag-router counterexample to an assumed common spatial channel.

## Decision and practical limits

ACCEPT CLAIM-143-INSTRUMENT as PROVEN under these hypotheses. The statement
extends the weak-regime obstruction beyond static interferometers, including
finite ideal within-attempt feedback. It does not prove an all-strength or
across-attempt adaptive-optimizer no-go. A common API/controller name or
unreported tags does not establish the required spatial effects: tag-sensitive
optics, detectors, erasure, unknown conditional ancillas and normalized rare
success sectors require different models. Every helper must be charged and
orthogonally tagged in D or covered by a verified equivalent reduction.

The factorial factor may be enormous; no inexpensive D hardware/source,
efficient simulator, useful precision, matched setup/latency/wall cost or
measured device certificate follows. The deterministic D null must be checked
for the actual alphabet/decoder. P140's strong-prefix witness is not refuted
without that check. Standard operator/permutation ingredients are known;
P144's bounded primary-source audit is separate and priority stays UNVERIFIED.
The finite-strength P141 negative is a separate experiment, not inferred
from this local theorem. CLAIM-042 OPEN; no QPU or manuscript gate is opened.
