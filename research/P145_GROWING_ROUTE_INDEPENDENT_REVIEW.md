# P145 — Independent audit of the two-layer growing-coherence discriminator

P66; manual non-author proof review, 27-Nov-2026. Primary verdict: **proved as
written**, for the specified ideal product-Fock, passive depth-two model and
the explicitly supplied representation/width assumptions. No practical
threshold, graph-optimization advantage, novelty or hardware conclusion follows.

Exact target FULL203 lines: c1b59f64655047272d36957dc39660ec2c84bca0,
research/P145_GROWING_COHERENCE_ROUTE.md, SHA256
f887f3bbed072c02781fcacecae8923cca16a081bcd79ec12c92eb0ec0564bcb.
This review reconstructs the argument, rather than accepting the author's
verdict. I authored the earlier small P145 kernel, not this source. No kernel,
fixture or DEV output was used here. No import/AST/computation/test/native run.

## Claim and dependency audit

For L>=1, K=3L distinct occupied input modes among6L, U=BPA consists of two
disjoint three-mode-unitary layers with intermediate wiring and no measurement.
If A_count output rows each have two occupied-source intensities at leastq0>0,
the claim is PCF<=(1-q0^2/18)^ceil(A_count/81). Balanced couplers and simple
cell incidence give the stated automatic-floor specialization for L>=2.

| Obligation | Status | Decisive reason |
|---|---|---|
| Fock/product component law | Passed | Disjoint source/output mode factors |
| Collision moment and local probability | Passed | Pair contractions and n<=9 |
| Packing and independence | Passed | FULL cones, at most81 closed neighbors |
| Balanced unique-path corollary | Passed | Intensity1/9; occupied-cone count |
| Local tensor factorials | Passed | Each intermediate factorial occurs once |
| Supplied-width contraction | Passed | Edge-variable bags preserve connectivity |
| Exact sampling bit model | Passed under stated representation | Rational prefix masses; expected bits |
| External priority/source authentication | Not addressed | Not a load-bearing leaf of this reconstruction |
| Hardware/empirical utility | Out of scope | No calibration or observed data |

All load-bearing mathematical dependencies above are derived internally from
Fock CCRs, tensor-product input, unitary local matrices, finite sums and the
definition of a supplied tree decomposition. No numerical evidence is needed.

## Collision implication reconstructed

Write b_j=sum_a U_ja a_a. For CF inputs, only distinct occupied a,b survive
the normally ordered fourth moment. Thus E[n_j(n_j-1)]=4sum_(a<b)q_ja q_jb,
so E binom(n_j,2)>=2q0^2. Its backward cone has at most9 input modes;
the initial cone photon number is at most9. The supported n_j cannot exceed
that number: hence binom(n_j,2)<=36*1_(n_j>=2) and Pr(n_j>=2)>=q0^2/18.
This is a bosonic expectation identity, not a distinguishable-photon premise.

Every input reaches at most9 output modes. The union of outputs sharing any
input of a marked row's at-most9-mode cone therefore has size at most81.
Removing this closed neighborhood at each greedy step yields at least
ceil(A_count/81) marked rows with mutually disjoint FULL backward cones.
The pulled-back number observables act on disjoint input-mode tensor factors;
their spectral collision events are consequently independent in the product
CF/vacuum state. This remains valid for arbitrary gate phases. Sharing even
vacuum input factors would not justify this particular product argument.
Global CF implies every selected row is noncolliding; multiplication proves
the claimed bound. A bounded nonnegative accepted gain is at mostR_gain*PCF,
and dividing by3L charges every injected photon. No optimum oracle is used.

For simple incidence and balanced tritters, every reachable source-row pair
has exactly one intermediate wire path; amplitude modulus is1/3 and intensity
1/9. Each row has9 such sources, and each occupied source enters three second
cells. Therefore sum_b v_b=9L. If g cells have v_b>=2, the other2L-g have
v_b<=1, giving9L<=9g+2L-g and g>=ceil(7L/8). Each good cell supplies three
marked rows. Consequently ceil(A_count/81)>=ceil(7L/216), with base
1-(1/9)^2/18=1-1/1458. Rounding is in the safe direction. Simple incidence
is impossible atL=1 and is explicitly restricted toL>=2 in the source.

## Components, factorials and width

A wire component gives independent mode-Fock input/output subsystems; spatial
PNR laws factor even with collisions. Orthogonal tags between source-containing
components change no spatial law. At least two such components are needed to
make a proper source partition. Vacuum-only components cannot supply a veto.
The degree-three weighted simple-tree leaf has its sole edge of multiplicity3,
exhausting its neighbor too; the source's forest reduction is correct.

For intermediate s and final n, the normalized first transition is
per(A[s,R])/sqrt(prod s!), and the second is
per(B[n,s])/sqrt(prod n!*prod s!). Their product is exactly the displayed
alpha(s)*beta(n;s)/sqrt(prod n!), with ONE full intermediate factorial.
Unitary Fock normalization gives sum_n beta(n;s)conj(beta(n;t))/prod n!
=prod s!*delta_(s,t). This includes vacuum and all bunched occupations.

Squared amplitudes have variables(s_e,t_e) of dimension at most16. Replacing
each vertex bag by its incident mode edges creates at most3(w+1) variables.
The bags of an edge uv are the union of the connected u- and v-bag sets;
these intersect in a bag containing both, establishing running intersection.
Every local factor's scope fits. Thus the stated exponential-in-width bound
and polynomial bound for supplied w=O(log L) follow. Local totals at most9
make local factorial/permanent sizes constants; Gaussian-rational input
lengths admit a common product denominator with polynomial bit length.
This bit conclusion does not apply to arbitrary unspecified real phase oracles.

Each second-cell output has at most220 candidate triples. Fixing/summing those
local factors computes exact rational prefix masses by the same contraction.
Sampling positive-prefix ratios gives the RAW law with expected finite fair
bits; it gives neither a deterministic time cap nor a free CF rejection loop.
The prism width<=5 example has bags consisting of the first column plus two
successive columns; it is consistent with the supplied-decomposition premise.

## Safe scope and next obligation

No mathematical gap found in the audited implications. The cited Markov--Shi
version/priority is not reauthenticated here; the explicit tensor/bag proof
does not rely on its theorem statement. No novelty clearance is issued.
Zero final collision expectation forces at most one occupied input per output
row, eliminating every exchange ambiguity and giving B=D on the full law.
Small observed collision frequency is insufficient to infer that endpoint.
Uniform positiveq0 and linearly growing A_count are essential for exponential
decay: cancellation, parallel wires, changing depth or a repair decoder are
not covered by that corollary. Constants may be too weak at useful sizes.
The next actual research obligation remains a paid, optimum-blind graph rule
with a favorable raw utility against reoptimized groups/D and strong classical
search; connectivity or growing width alone supplies none. No experiment is
proposed or authorized by this audit, and all prior P145 records remain intact.
