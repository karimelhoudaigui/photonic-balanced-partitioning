# P49 isolated HOM/NOON pair: exact classical control

Analytic check, 2026-11-25. Target is the coordinator's auxiliary ordered-law
claim for ONE isolated pi/4 HOM pair followed by two orthonormal columns
u=E_a,v=E_b. Verdict: **proved as written**, with the real-E qualification
for K=-iP at phi=pi/2. No numerical code, sampling, P49 result or QPU is used.
This is a mechanism control, not a global classical-simulation theorem.

Use the already fixed output-row/input-column convention. The normalized
state immediately after the source pair mixer is

    (-exp(i phi)|20>+exp(-i phi)|02>)/sqrt2.

After E define the COMPLEX SYMMETRIC matrix

    K=-exp(i phi)u u^T+exp(-i phi)v v^T,
    P_pair=u u*+v v*, mu_i=(P_pair)_ii.

The transpose in K is essential; star denotes conjugate transpose.
Orthonormality u*u=v*v=1,u*v=0 implies u^T conj(v)=0. Hence

    K K*=P_pair, Tr(KK*)=2.                            (1)

In an ordered two-particle representation the normalized amplitude is
K_ij/sqrt2. Thus

    p_ordered(i,j)=|K_ij|^2/2,                         (2)
    Pr(n_i=n_j=1)=|K_ij|^2 for i<j,
    Pr(n_i=2)=|K_ii|^2/2.                             (3)

The off-diagonal Fock probability sums the TWO orderings. A collision has
only one ordering, so it keeps the factor1/2. Equations (1)-(3) sum to one;
no CF conditioning, collision removal, factorial correction beyond (3),
or hidden herald is required.

The first auxiliary particle index therefore has law

    Pr(I=i)=sum_j |K_ij|^2/2=mu_i/2,
    Pr(J=j | I=i)=|K_ij|^2/mu_i, for mu_i>0.           (4)

If mu_i=0, both u_i and v_i vanish, the entire K row vanishes, and I never
selects that row. A sampler must skip it rather than evaluate0/0. Conditional
row probabilities in (4) sum exactly to one. Sampling the two auxiliary
indices and forgetting their order reproduces the complete Fock law.
E[n_i]=mu_i, as expected for two photons. The auxiliary ordering is only
a classical construction, not a physical which-photon observation.

Given u,v, computing mu and a first-index CDF costs O(N) arithmetic/memory.
After drawing I, evaluating K_(I,j) for every j and sampling the second
index costs O(N). Thus every pair draw has linear arithmetic cost after E
is supplied, without a large permanent or graph-objective oracle. “Exact”
describes the categorical law in ideal arithmetic; it is not a floating-
point interval guarantee or a bit-complexity claim for arbitrary real inputs.
No implementation or numerical validation is supplied by this note.

For REAL E and phi=pi/2,

    K=-i(u u^T+v v^T)=-iP_pair,
    p_ordered(i,j)=|(P_pair)_ij|^2/2,
    total collision probability=(1/2)sum_i mu_i^2.     (5)

For complex E the first equality is -i(u u^T+v v^T), which is generally
NOT -iP_pair. Equation (1) and the sampler (4) still hold. As hand checks,
E equal to identity on this pair gives only the two bunched outcomes,
each with probability1/2. A real Hadamard analyzer at phi0 instead gives
one photon at each analyzer output; phi=pi/2 gives the bunched law again.
These are reproducible two-photon interference effects with the classical
control above, not an optimization advantage.

## Exact scope of the control

If multiple pair components are ORTHOGONAL INTERNAL SPECIES and independent,
their detected occupation laws convolve: sample each pair by (4), then sum
the counts. The cost is O(number_of_pairs times N). More generally, any
fixed maximum internal species size admits an exact polynomial enumeration
of that species' finite Fock law and independent convolution. This is why
a bounded-species control is scientifically material.

Disjoint gates, orthogonal spatial columns or an algebraic product of
creation-operator polynomials do NOT themselves make indistinguishable
pairs independent under the common spatial occupation measurement. Cross-
pair exchange terms can remain. P49's two OVERLAPPING layers followed by
a dense E are not replaced by independently sampling isolated pairs here.
No efficient exact sampler, hardness or useful-search theorem for that full
source follows from (1)-(5).

Consequently a label such as “NOON” or a verified isolated HOM pair cannot
support an advantage claim. Surviving the declared species4, coherent-phase/
sphere and honestly budgeted classical searches is necessary evidence;
those controls alone would still not prove advantage or global novelty.
This note changes no P49 card, source, code, raw or acceptance gate.

Provenance: direct operator/Fock derivation, normalization and collision
factor checks were sent before this note. Only text/whitespace/hash/Git
checks accompany its commit. No matrix evaluation, test, graph generation,
numerical sampling or QPU was executed. The reviewer authored prior P49
physics notes; this is a fresh auxiliary derivation rather than third-party
revalidation of that earlier work.
