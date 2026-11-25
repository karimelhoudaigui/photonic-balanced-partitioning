# P49 prospective source mixing: physics and null controls

Physics review, 2026-11-25, no numerical work. Initial root card reviewed:
`7b791bf9d819d88cf517eec81e4fdb0bb2d3f93d`,
`research/P49_TRAINED_SPECTRAL_SOURCE.md`, SHA256
`dcf5d21fab6e6c30a62b936f644601363d16fac8c800dd647ec9926d29f369c2`.
Its generic-phi HOM formula had the conjugate phase under U[output,input].
It was corrected BEFORE execution, with grid unchanged, at
`dc85fa5b49b095de3ba39c37f35d0cada70b47dd`, card SHA256
`1278f53b2ba9512c189a6bc3098db0233153b22c72edaceba679694b76755b61`.
The exact one-hunk correction was read. Old and new card provenance remain
distinct. No P49 code, DEV graph or output was inspected/generated here.

Verdict: the corrected physical map/invariance and reduced control grids
are **proved as written** under the stated conventions. The hypothesized
useful feasible-search gain is **incomplete**: source interference has a
computable local sign, but no favorable aggregate cut/tail sign follows.
No advantage, novelty, global-search or hardware claim is supplied.

## Map, order, source and pair phase

Use output rows/input columns. The declared G is unitary with determinant1.
The rightmost odd layer in R=G_even G_odd acts FIRST on pairs(1,2),(3,4),...
with zero-based indices; the even layer next acts on(0,1),(2,3),... . End
modes not paired by a layer remain identities. No different product order
or pair orientation may be silently used. R is unitary, so for V=ER,

    VV*=EE*=P, sum_a|V_ia|^2=P_ii=mu_i.                 (1)

CF input remains one photon per port0,...,K-1. A basis rotation is physical
for this bosonic state even though its one-particle density remains I_K.
R uses O(K) beam splitters; it needs neither ancilla photons nor herald
conditioning in the ideal passive model. This says nothing about measured
loss/compilation cost. Completing vacuum columns does not change the state.

Creation-operator expansion for an ISOLATED pair gives exactly

    Gamma(G)|11> = cos(2theta)|11>
      +(sin(2theta)/sqrt2)(-exp(i phi)|20>+exp(-i phi)|02>). (2)

At theta=pi/4, phi0 yields the antisymmetric NOON up to a global phase;
phi=pi/2 yields -i(|20>+|02>)/sqrt2. The two overlapping layers generally
do NOT produce a product of independent NOON pairs. Tests must check the
isolated identity separately from the full R construction.

The initial card's conjugated expression agrees up to a global phase at
the two frozen phi0/pi2 values, explaining why only those fixtures could
miss its generic sign. A phi=.37 test must inspect amplitudes/coherence,
not merely p20=p02=1/2. The global-phase-invariant coherence is

    rho_(20,02)=-exp(2i phi)/2.                         (3)

A complex analyzer can also reveal this sign through probabilities.
A real analyzer alone can leave only cos(2phi), again failing to distinguish
phi from -phi. No additional production phase is requested by this check.

## Gauge, genuine parameter changes and exact nulls

Fixing E's carried-priority pivot gauge BEFORE mixing is part of the new
physical protocol. E->ED with R held fixed is generally NOT a null source
transformation. A change of coordinates E->ED must carry R->D*RD to give
the frame ERD=(ER)D, only a phase change of the occupied input columns.
Arbitrary post-V column phases remain null. Mixing, gauge or eigenvalue
order must never be retuned after outcomes under the label of convention.

For the real spectral E, R(-phi)=conj(R(phi)), hence V(-phi)=conj(V(phi)).
All Fock probabilities, D/species laws and continuous-phase/sphere controls
are conjugation invariant; Gaussian covariance and numerical PMF targets
also agree. Thus +/-phi is a redundant physical law here. The chosen
phi0 versus pi2 is not removed by this null. theta0 gives R=I. At theta=pi/2
each layer is monomial: B and fully D with all K input modes occupied are
unchanged up to input permutation/phases. A fixed species partition needs
its group assignments carried under a permutation before calling that
same null for species4. These are mathematical boundary fixtures, not
extra production settings or outcome-driven exclusions.

Sphere is invariant under ANY right-unitary R at the FULL joint count-law
level: Rz is again uniform on the complex unit sphere. Its marginal PIT
depends only on mu, so its COMPLETE same-decoder law is invariant too.
This does not use the P48-A Haar-average loophole: it is exact for each
fixed E and R. Sphere therefore needs only Fourier versus unmixed spectral,
with two lambdas; IID needs only its two lambdas. D, phase, species and B
Gaussian generally DO change because q=|ER|^2 enters their laws. The card's
8/4/2 distinct-setting grids avoid forced tuning of redundant labels while
equalizing total paid shots across arms.

In particular, mu1 can remain fixed while a one-hot q row becomes spread
under R. Recompute B/D/species/phase tables, covariance and deterministic-
Gaussian masks from EACH complete V; do not reuse those of E just because
P/mu are invariant. Sphere tables alone can be reused across spectral R.

## A real local discriminator, but no automatically useful cost sign

After an isolated NOON pair followed by E, for DISTINCT outputs i,j the
two-photon amplitude is

    -exp(i phi)E_(i,a)E_(j,a)+exp(-i phi)E_(i,b)E_(j,b).

For real E the probability difference between phi=pi/2 and phi0 is

    4 E_(i,a)E_(j,a)E_(i,b)E_(j,b).                    (4)

It can have either sign. Full normalization includes collisions and
compensating other outputs. With other indistinguishable photons present,
one cannot sum isolated-pair formulas as if there were no cross-pair
interference. The explicit isolated-pair kernel is cheap classically;
species4 and coherent controls test partial/local explanations, but finite
gate depth followed by a growing dense E is not proved globally classically
samplable here. No hardness conclusion follows either.

A simple warning example is E containing a two-mode Hadamard block: a real
pi/4 source rotation can undo that block into a monomial map, whereas the
pi/2 phase can give different interference. That can be an intensity/source
localization effect already exposed by q columns and labelled matching.
The card properly scores/shares preparation discoveries for EVERY rotated
frame before measuring gain. No such scored solution may be called an
optical discovery or loaded back into the input. The same spectral data
and all preparation work go to classical controls.

## Training and the remaining optimization obligation

The loss is a well-defined feasible-cut mean in[0,1] for positive total
edge weight; the zero-weight denominator1 branch yields0. All shots,
including collisions, worse solutions and filled unclicked modes, must
contribute. Equal graph weighting avoids a change of instance weighting
through raw cut scale. No C* or hinge/success oracle is required.

Independent model selection on paid training followed by FRESH sampling
seeds at fixed selected policy is a sound conditional-sampling comparison.
It is still the SAME DEV graph population, not held-out-instance evidence.
The 128 training+128 evaluation proposals/arm, total3840 simulated photons
per physical arm, preparation/PMF/selection work and all failed cells must
remain charged. Training discoveries and fresh evaluation incumbents are
reported separately; neither changes V or the source ports.

A lower feasible mean does not ensure better best-of tails. For example,
constant loss .4 has a lower mean than loss0 with probability1/4 and .6
otherwise (mean.45), yet the latter's expected best of TWO is .3375.
Thus chosen-policy fresh mean and deployment best-after-paid-training
are distinct predeclared metrics, not interchangeable positive gates.

The independently budgeted FAST classical control, granted at least B's
classical frontend/train/eval postprocessing allowance even with optical
sampling assigned zero latency, is an appropriate stringent resource
discriminator. A cap reached before its allowance expires is inconclusive,
not evidence of B superiority. Simulator/backend or audit serialization
overhead is not a hardware price. This review supplies no favorable sign
for that comparison; source/PIT correlation usefulness remains to be tested.

Actual checks were direct symbolic derivation, card/git-diff/hash reads
and explicit messages before/after the formula correction. No numerical
program, phase assignment enumeration, P49 test or QPU was executed. This
short note is self-derived by the physics reviewer, who authored earlier
P48 analyses; it is not independent revalidation of those prior sources.
