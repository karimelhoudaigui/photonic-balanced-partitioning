# P48-B exact-card physics review, before code inspection

2026-11-25. Target: root commit
`e30f75ced16e61fbb69ebe2f6d9509f90a7aa4ae`, file
`research/P48_SPECTRAL_BASIS_CLAIM_CARD.md`, SHA256
`3a93f44f007870cc5b08fc05d57bad77f389ccf3d38ec2b21926132c2a92bd6b`.
The inspected root file has no diff from that commit. No P48 code, raw,
numerical run or proof by computation was inspected/executed. This is an
independent reconstruction relative to the card author, but the reviewer
authored the preceding P48-A physics note and supplies no new third-party
validation of that note. Source-card claims remain hypotheses where labeled.

Primary verdict: the exact encoder/card is **mathematically coherent under
its stated continuous-mark and numerical-inconclusive qualifications**;
the useful nonlinear/PIT optimization hypothesis is **incomplete**, with
no implied improvement sign. There is one gauge-invariance qualification
for a possible discrete-root version of the rounding control, detailed below.
This is a prospective physics checkpoint, not authorization or validation
of an executable implementation.

## Construction and changes from heat-Haar card A

For symmetric nonnegative A, L=diag(A1)-A is PSD. For L!=0, Lhat has spectrum
in [0,1]; for L=0 it is declared zero. With gamma=10^-3 and real marks
xi_i in [0,1], M=Lhat+gamma diag(xi) is real symmetric PSD with spectrum
in [0,1+gamma]. Its first r orthonormal eigenvectors form an N-by-r isometry
V. Completing V with vacuum columns defines a passive unitary, and the
count law of the r distinct occupied source ports depends only on V.
There is no anchor partition loaded into this optical state.

For fixed L and independent CONTINUOUS marks with densities on an open
box, the eigenvalues are simple almost surely. One elementary proof is
that the discriminant of the characteristic polynomial is a polynomial
in the diagonal entries. It is not identically zero: arbitrarily widely
separated diagonal shifts give a simple spectrum by disjoint Gershgorin
disks. A nonzero polynomial cannot vanish on an open box except on a
measure-zero set. This proves generic simplicity even though gamma is
fixed; it does not give a useful minimum spectral gap in the bounded box.

Finite PRNG/float marks do not inherit an exact almost-sure certificate.
Every internal gap among selected eigenvalues matters, as well as the
r/r+1 boundary gap. Internal rotations can leave P=VV* unchanged while
changing the CF source. Residuals and gap diagnostics, preservation of
all cases and numerical-inconclusive handling are therefore necessary.
The card requests them; their implementation remains to be reviewed.

Under a vertex permutation Q carrying both A and marks, M->QMQ*. For a
simple ordered spectrum, V->QV times column signs/phases. Those column
phases multiply the CF state by an overall phase and do not affect the
B/D/species count laws. The carried Fourier row order is also necessary
for the graph-blind encoder. Regenerating marks/order without carrying
them gives distributional, not pathwise, covariance. No arbitrary choice
inside an unresolved degenerate eigenspace may be called source-invariant.

The deterministic marked eigenbasis has no Haar-right-basis invariance.
Thus the P48-A conditional Haar twirl does not identify this fixed B law
with the spherical law. It is a real architectural distinction, not proof
that the new law is useful. The graph-blind Fourier and real spectral
encoders also differ structurally; their comparison alone cannot identify
a bosonic mechanism. The within-encoder B/D/coherent comparisons are needed.

## Boundaries and wording

The diagonal marks break the exact constant eigenvector in general.
No mu_i>=1/N bound follows. The exact row leverage bound is only
0<=mu_i=sum_a|V_ia|^2=P_ii<=1. The card correctly retains mu0/mu1 and
subunit-row helpers. It must not normalize each row to total one.
P need not have nonzero offdiagonals on EVERY pair/branch. For example
L=0 with distinct marks selects coordinate eigenvectors and gives a
diagonal rank-r projector; some rows have mu0 and the occupied coordinate
source has B=D exactly. This is a valid retained branch, not a reason to
redraw marks or a counterexample to an explicitly exploratory hypothesis.

One-body mean counts equal mu for B,D,spherical and continuous-phase
multinomial. In particular their one-body Laplacian energy is the same
Tr(V*LV); low spectral energy does not by itself distinguish these models.
Raw number-cut polynomials can be invalid feasible-partition objectives
on bunched occupations. Threshold/PIT/completion and best-of performance
are different observables; their useful sign has not been proved here.

## Coherent controls and one needed phase qualification

The sphere and phase PGF coefficients and positive sphere mixture in
`theory/P48_heat_frame_and_classical_controls_review.md`, commit
`517ed020283028a2bcc397a173401a7cc7b01829`, apply to this V as well. They
require no Haar distribution of V. For r>=2 the sphere marginal uses
mu_i Beta(1,r-1); r1 is Bernoulli(mu_i), r0 is vacuum. The phase formula
requires independent continuous phases or Q>r roots for the multinomial
law. Four roots are insufficient in general at r>=4. Both controls are
cheap polynomial classical samplers on the SAME frame.

The sentence that column signs/phases do not affect any stated controls
is exact for continuous-phase sampling and spherical sampling. A Q=r+1
root grid also gives the correct column-phase-invariant MULTINOMIAL(r)
law: its probabilities are polynomials of total phase exponent at most r.
However the NEW top-K |Vz|^2 ROUNDING baseline is not such a polynomial.
Replacing its continuous phases with a finite root grid need not preserve
its law under arbitrary column phases. Continuous phases should be used
for that rounding claim, or its invariance should be restricted explicitly.

For example take r=2,N=4 with V rows (1,1),(1,-1),(1,1),(1,-1), all divided
by2. For relative phases uniform on the third roots, top-2 intensity
rounding selects rows {0,2} with probability1/3. Flipping the sign of the
second column changes that probability to2/3. The CF source itself is
unchanged by this column sign. The actual prospective r13/17 have Q14/18,
so their even root grid is sign-invariant, but arbitrary phase invariance
of a rounding distribution is still not implied by the multinomial moment
argument. This example is analytic, not a numerical experiment. The card
already names continuous-phase arms, so using continuous phases for its
rounding baseline avoids this ambiguity without changing the hypothesis.

## Comparison obligations and exact remaining gap

The seven separately retuned arms, both encoders, shared decoder lambda/
priority, all-count conservation, exact conditional marginal PIT tables,
all K^2 charged anchor swaps and scored spectral/decoder frontends are
appropriate controls. Eigenbasis and marks must be shared with the
spectral/coherent rounding and feasible-search baselines; every actually
scored discovery belongs to Cref before any optical gain is counted.
Column signs cannot be tuned as new physical source parameters. A true
basis rotation, in contrast, would be another tuned source with costs and
data selection to retain.

No model gets a free best-of-baselines portfolio. Independent DEV selection
across encoder/lambda settings is tuning, not held-out evidence. All 256
proposals/arm, 3840 simulated photons/optical arm, score/time budgets,
preprocessing and failures must be retained as declared. A tiny finite
separation would justify at most the prospective FOLLOW-UP status; no
quantum/hardware or novelty conclusion is supplied by this card or review.

The smallest remaining scientific obligation is to exhibit a nonlinear
feasible-search statistic whose B improvement at matched total resources
survives the same-frame D, bounded species, Gaussian, spherical, continuous-
phase and strong classical spectral/nonlocal explanations. Spectral source
construction alone supplies no such sign. No counterexample here refutes
all possible nonlinear improvements; no moment argument is promoted into
that universal claim.

Actual review commands were read-only cat/git-show/git-diff/shasum on the
exact root card, plus algebraic reconstruction. No P48 source implementation,
pytest, numerical sampler or resource slot was used. This new note alone
is written/committed in the isolated replication worktree.
