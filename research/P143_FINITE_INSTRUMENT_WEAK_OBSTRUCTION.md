# P143 — finite tag-blind instruments near a deterministic incumbent

2026-11-26. ROOT supplied the candidate; this is manual reconstruction of elementary operator-order/analytic ingredients.
No novelty claim, program/import/AST, matrix evaluation, RNG, native call, scientific raw read or experiment.
This note does not authorize P141 or change any frozen population. Its final code review remains the priority when assigned.

**Verdict: proved under the explicit common-spatial-effect and analytic endpoint hypotheses below.**
Standard finite tag-blind passive optics, number detection and classical feed-forward admit that reduction.
It is not implied by using the same controller name or by failing to report the tags.

## 1. Input density and the uniform factorial bound

Let K>=1 photons occupy DISTINCT orthogonal spatial source modes, with all other inputs vacuum.
Include EVERY prepared CF helper/reservoir photon in K; non-CF, uncounted or unknown conditional ancillas are outside this input model.
In first quantization let |sigma> run over the N=K! orthonormal ordered permutations of those occupied modes,
and let P be their spatial projector. Particle labels here are mathematical bookkeeping, not resolved detector records.
After tracing a normalized physical internal state, rho_J is positive, trace1 and supported on P.
Fully orthogonal source tags give rho_D=P/N: the permuted internal tag tensors are mutually orthogonal.
Therefore, including a parameter-dependent internal family,

    0<=rho_J(kappa)<=P=N*rho_D.                         (1)

The inequality is simply that every eigenvalue of a trace-one positive density is<=1.
For fully identical B the spatial state is the rank-one symmetric vector; no extra factorial can be dropped universally.
The spatial density may have components outside the fully symmetric SPATIAL sector when tags are traced.
Thus one must use the labelled K-particle spatial space, not apply a bosonic-only Fock channel to rho_D by fiat.

Assume a spatial instrument has common effects E_z(kappa)>=0 with sum_z E_z=I,
on that input space, independent of internal tags and identical between arms at each common kappa.
Then positivity/linearity gives

    p_J(z;kappa)=Tr(E_z rho_J(kappa))
               <=N*Tr(E_z rho_D)=N*q_D(z;kappa).        (2)

The same statement follows by applying each common CP branch map to (1) before tracing its output.
No analyticity of rho_J, or of its permutation kernel, is needed for (2).

## 2. Why destructive adaptive counts can have common initial effects

For internal-blind passive gates the first-quantized action is U^tensorK on space and identity on internal degrees.
Spatial number projectors are likewise spatial-only. A finite record-conditioned sequence remains a linear instrument on UNNORMALIZED branches.
Replace destruction by count measurement and transfer to private, non-reinteracting detector-sink modes.
Future gates act only on active modes; reused detector ports get fresh vacuum modes.
Tracing the protected photons at the end reproduces destructive detection statistics without coherently erasing their internal tags.
With finite modes/rounds/records this uses a finite enlarged spatial space and common branch effects on the INITIAL density.
Thus a standard finite passive count/feedback protocol, including removed photons and vacuum flags, satisfies (2).
This is a mathematical dilation, not an asserted QND/storage hardware capability.

This proof does not assume a Markov channel on only the surviving reduced spatial density after every click.
All photon helpers must be in a declared fixed CF input model, or have a separately proved equivalent reduction with their full counts included.
Tag filtering/resolution/coherent erasure or a polarization-dependent router can break the spatial-only hypothesis.
Already at K1, H/V-dependent routing distinguishes states with the SAME initial spatial density: discarding the tag record does not repair it.
Fresh source preparation with unaccounted internal/spatial correlations is not automatically a common channel.
Nor may one condition on successful records and divide by different success probabilities; all failures stay in the raw alphabet.

## 3. Finite-outcome analytic retuning

Fix a finite outcome alphabet Z, independent of kappa, and one admitted instrument family on 0<=kappa<rho.
Assume every q_D(z;kappa) has a real-analytic extension through0 and q_D(z;0)=delta_(z,z0).
Physicality is required for nonnegative kappa; the analytic extension need not be a physical probability at negative kappa.
By (2) and normalization, every admitted internal family also has deterministic null outcome z0.

For z!=z0, either its analytic D germ is zero on a neighborhood, or

    q_D(z;kappa)=a_z*kappa^nu_z*f_z(kappa),
    a_z>0, integer nu_z>=1, f_z(0)=1.                 (3)

The positive leading sign follows from one-sided nonnegativity.
Choose integer c=N+1. For each nonzero germ the ratio q_D(z;c*kappa)/q_D(z;kappa)
tends to c^nu_z>=c>N. Thus, at sufficiently small positive kappa,
q_D(z;c*kappa)>N*q_D(z;kappa)>=p_J(z;kappa), uniformly over ALL rho_J(kappa).
Zero D germs also force p_J zero. Choose radii r_z for every zero-germ neighborhood or nonzero-germ continuity enclosure,
then take kappa0 less than min{rho/c, all r_z/c}; both evaluated settings stay inside every needed neighborhood.
This gives ONE positive kappa0 for all z!=z0. No effective or uniform lower bound is asserted.
The comparator family must actually admit c*kappa; a finite grid may omit it.

## 4. Smaller factor for a finite analytic Kraus realization

Suppose the finite-dimensional spatial instrument has finitely many Kraus matrices A_(z,l)(kappa), real-analytic through0.
Then `q_D(z;kappa)=N^(-1) sum_l ||A_(z,l)(kappa)P||_HS²`.
For z!=z0, endpoint zero forces every A_(z,l)(0)P=0.
A nonzero analytic Kraus germ has a finite positive integer order; the positive squared-norm sum has EVEN leading valuation nu_z>=2.
Hence c=ceil(sqrt(N+1)) suffices: c^nu_z>=c²>N, with the same finite-minimum proof.
Finite analytic optical gates, fixed count projectors and fixed record-dependent gate prescriptions provide such branch products.
Probability analyticity alone does not justify this smaller factor: e.g. a probability kappa can require a nonanalytic sqrt(kappa) Kraus amplitude.
Zero-germ branches must still constrain the shared window; no rare branch is removed.

## 5. Utility and non-claims

For a bounded NONNEGATIVE h on the common raw alphabet require h(z0)=0, identical across arms and strengths.
Summing the off-null inequalities proves E_D,c*kappa[h]>=E_J,kappa[h], strict when some nonzero D germ has h(z)>0.
For a common classical decoder L, this means h(z)=sum_y L(y|z)g(y) must satisfy the same null-zero requirement.
The null atom is not pointwise ordered and cannot carry a free known-solution benefit.
At K1 the common spatial laws are identical at the SAME setting; any retuning gain is ordinary parameter change, not exchange physics.

The D input must distinguish ALL K photons in the comparison, helpers included, or use a verified simulator of that law.
A partial-D hardware source with different fixed helpers is not rho_D=P/N without another argument.
Source/tag preparation, detector storage, synthesis, feedback latency, classical work and wall clocks are not matched here.
Infinite transcripts, unbounded helper photons, tag-sensitive devices, postselection, or across-attempt adaptive performance need separate analysis.
A strong prefix need not have a deterministic D null; the declared alphabet/decoder must be checked rather than inferred from a few B suppressions.
No conclusion about P140 is made without that check; a prefix alone is neither a certified escape nor a positive result.
Analyticity and the deterministic null require model proofs, not inference from finite samples; the label D alone proves no implementation efficiency.
This is a nonuniform weak-regime existence obstruction for a fixed finite instrument, not a universal no-go, efficient sampler, novelty or QPU claim.
