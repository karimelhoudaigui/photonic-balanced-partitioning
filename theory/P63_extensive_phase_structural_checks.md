# P63 extensive phase family: static structural checks

25-Nov-2026. Analytic derivation only. No code, imports, matrix evaluation,
graph, phase/count draw or simulation. A decoded-mean benefit at N18 is
UNKNOWN. These checks do not transfer the small P59 response or prove novelty.

## Fixed full-CF architecture and actual phase support

Let d=6,N=3d=18, ports(a,i)->ad+i, inputs(b,j)->bd+j, a,b0..2;i,j0..d-1.
F3[a,b]=omega^(ab)/sqrt3, omega=exp(2pi*i/3), and
Fd[i,j]=exp(2pi*imagunit*i*j/d)/sqrt(d),imagunit=sqrt(-1).
Equivalently Fd[i,j]=xi^(i*j)/sqrt6,xi=exp(pi*imagunit/3),d6.
Use source1^18 and

    U_Theta=V (F3 tensor I_d) D_Theta (I3 tensor Fd),
    U_Theta[(a,i),(b,j)]=omega^(ab)*exp(i theta[b,i])*Fd[i,j]/sqrt3
                       before V.

V acts on ordered OUTPUT ports(0,6) by[[3,-4],[4,3]]/5. Fix gauges
theta[0,i]=theta[b,0]=0. The TEN real controls theta[b,i],b1/2,i1..5 are
all present; the five-control alternative is not an outcome-dependent option.
This is a square unitary by composition. q=|U|² is phase independent:

    row0: b-block values(1,37,37)/450, each repeated over six j;
    row6: b-block values(49,13,13)/450, each repeated over six j;
    other16 rows: all1/18.

All row/column sums are1, so full-source means remain1. Complete D count
law, complete B single-mode PMFs and all joint factorial moments<=3 are
constant in Theta. The full-square P56 lemma applies. Mixed-row variance
2[1-2739/(5625*d)] differs from unmixed2[1-1/(3d)], breaking the old C3
count symmetry. It does not establish a phase-dependent decoded mean.

Changing Theta after a reference preparation is a product of five local
THREE-mode output operations, one per i1..5. Their generators are the ten
orthogonal projectors |f_b,i><f_b,i|,b1/2, where f_b is a Fourier column ofF3.
They commute; V acts only in color0 and commutes with these generators.
The union of active outputs is exactly15, NOT18. Outputs{0,6,12} have a
fixed JOINT marginal. More strongly, all six color totals

    M_i=sum_(a=0..2)n_(a,i)

have one fixed JOINT law: every phase operation, F3 and V preserves them.
It is the distribution obtained by measuring and summing three independent
Fd|1^d> preparations before the final colorwise tritters. This block-total
constraint is a required classical control opportunity, not an escape claim.

The preexisting P62 s=3/eight-frontier argument no longer gives a constant
cost for global updates: here s=N-3 grows with N. Yet its frontier coupling
still applies with s15. With N18,K9 there are at most

    sum_(t=6..9) binomial(15,t)=22880

oriented candidates per fixed outside order, and at most2^15 in general.
Do not infer hardness from this larger bound or from binomial(35,17) Fock
states. There are only48620 oriented balanced vertex subsets at N18.

## Cheap exact j-aligned partial-species control

Group inputs by j: G_j={(0,j),(1,j),(2,j)}. Let D_j be the diagonal output
phase with entry exp(2pi*imagunit*i*j/d) on port(a,i). Then

    U[:,G_j]=D_j U[:,G_0].

V mixes color0 only, where D_j=1, so the identity survives V exactly. A
three-photon output Fock amplitude changes by a global occupation phase;
its entire PNR law is IDENTICAL for every j, at each Theta. Thus six fully
distinguishable species, each with three indistinguishable photons, can be
sampled as SIX IID independent copies of one three-photon/18-mode law,
then summed modewise. No conditioning or occupation filter is involved.

Each copy has1140 Fock outcomes, or may use a native three-photon sampler;
the photon number per permanent is3, hence this model is polynomially
samplable even as the mode count grows. Its tables/native setup and all six
copies remain paid. This does not imply the full18-photon law factorizes.
The grouped model can itself have Theta-dependent low moments; its training
must be independent, not copied from the B optimum. Separation from this
ONE grouping is not a genuine18-photon-indistinguishability certificate.

## Four controls are exactly flat in the trainable phases

1. D is fixed by q; there is no Theta optimizer to improve it within this
   family. This is full reoptimization of the specified phase-only ansatz,
   not a guarantee against other distinguishable architectures/embeddings.
2. Independent B-marginal counts are fixed by q; their TOTAL can vary and
   must not be reconditioned to18. Uniform top9 ties remain feasible.
3. A complex spherical field is unitarily invariant. Its multinomial18-count
   law is Dirichlet-multinomial with alpha1, hence UNIFORM Fock occupations.
   Symmetry plus uniform top9 ties gives a UNIFORM feasible balanced subset.
   A direct uniform subset is an equivalent, cheaper feasible-search control;
   this fact does not make independently phased fixed-radius fields spherical.
4. Full averaging over the ten relative phases is independent of Theta.
   It also has a concrete finite classical block sampler, described next.

Do not spend a fake training budget on these four flat laws and then discard
their training cuts. Give them their whole shot budget as fresh iid proposals.
Only full B, the j-aligned species model and continuous input-phase field
need separately trained trajectories in the proposed first pilot.

## Classical full phase-average block control

Adding the SAME phase to all b at each i only multiplies that output color
by a row phase, commuting with V and invisible to complete PNR measurement.
Column b phases also multiply the full Fock input by one global phase.
Consequently uniformly dephasing ALL3d intermediate ports is equivalent,
for measurement probabilities, to averaging the ten gauge-fixed phases.

This gives an operational CLASSICAL sampler at this finite d6:

- Independently draw three d-photon Fd|1^d> occupations (one per b). At d6
  their COMMON exact distribution has462 outcomes and can be pretabulated.
- For each i, take its three input occupancies and sample the three-mode
  tritter F3; use V F3 at i0. Conditional on those intermediate occupations,
  these six blocks are independent. Retain every collision and total18.
- Concatenate counts and apply the SAME uniform top9 decoder/embedding.

Three-mode bunching inputs may contain up to18 photons in total, but their
output table has at most190 outcomes. At d6 each input tuple lies in0..6
in every coordinate. A bounded paid lazy cache suffices; there is no need
to build any18-mode full law. The source table and cache must be charged
to this classical arm, never to B. This is a law-level phase-average control,
not an iid-shot stochastic-domination theorem or free target-law rejection
sampler. A target likelihood can still require a large permanent.

For growing d, sampling Fd|1^d> is not established easy by this argument;
the finite d6 construction is not a universal classical simulation theorem.
Coherences between color blocks persist in the unaveraged quantum family.
Whether they improve graph cuts beyond the cheap controls is the open test.

## First scientific falsifiers before any positive interpretation

All phase-sensitive claims must involve the actual unconditioned feasible
cut mean, not a changing count moment. At fixed center, a single zero
gradient need not imply a globally constant law. Conversely fixed q and
low moments do not imply a useful high-order mean channel at N18.

A later pilot must first survive a fixed strong classical feasible-search
veto with B-only classical costs, then j-aligned species/continuous phase,
the four flat controls and exact block-total explanations. Count conservation,
q invariance, the six joint block totals and the j-aligned identity are
indispensable synthetic pre-data checks. Their failure is implementation or
construction failure, never evidence for interference. Hardware source18,
PNR, loss survival and noise capabilities are unverified; no QPU readiness.
