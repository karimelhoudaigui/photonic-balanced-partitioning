# P48-B: a fixed graph spectral basis, not a Haar input basis

Root/Astra,25-Nov-2026. Prospective replacement BEFORE P48 code or outcomes.
The earlier P48_HEAT_SUBSPACE_CLAIM_CARD.md is preserved at42572d4. Physics
identified an important objection: heat filtering of a Gaussian frame followed
by rectangular polar decomposition leaves the input basis Haar conditional on
its subspace. Averaged raw B counts then equal a classical spherical-coherent
mixture. A V-dependent PIT prevents extending that statement to the complete
pipeline, but the original card supplies no clear physical reason to rely on
that loophole. We do not spend a DEV run on that random-basis hypothesis.

## New fixed basis and physical mechanism to falsify

Retain ALL four prospective graphs, photon counts, sample budgets, resource
caps, controls and positive gates of the first card. Only the two encoders
and directly corresponding classical rounding baseline change. The active
grid is encoder={Fourier_blind,spectral_graph}, decoder lambda={0,1}.

For nonnegative weighted graph adjacency A on N=2K vertices, r=K input photons,
let L=diag(A1)-A, Lhat=L/||L||op (zero if L=0). Draw role-seeded marks
xi_i independently uniform[0,1], and form

    B=Lhat+10^(-3) diag(xi).

The graph encoder V is the N-by-r matrix of the FIRST r eigenvectors of B,
in increasing eigenvalue order. It is NOT multiplied by a Haar source-basis
rotation. The fixed tiny marks remove arbitrary degenerate-basis conventions;
they are shared with all controls, carried under relabeling and charged.
The marker coefficient is fixed before outcomes, not tuned or selected.
Column signs/phases do not change a CF source state or any of the stated
controls. Simplicity is an almost-sure generic property with continuous
marks, not a floating-point certificate. Record every spectral gap and
eigen/unitary residual; if gaps<=1e-12 or residuals exceed declared preflight
tolerances, retain a numerical-inconclusive case rather than redrawing it.
All near-degenerate/zero graph branches are retained and preflight-tested.

For the graph-blind reference choose a role-seeded vertex order pi and
V_(pi(i),a)=exp(2pi i i a/N)/sqrt(N), a=0,...,r-1. Carry that order under
relabeling. The two encoders use the same r source ports0,...,r-1 and exact
vacuum unitary completion [V,Vperp]. There is no transfer-loss filter, old
anchor block or discarded collision. The isometry depends on graph/marks,
not on an optimum or a partition found by the classical frontend.

Now the source basis is graph-determined rather than Haar. Its projector
P=VV* has nondiagonal elements on all vertex outputs. The exact count formula
and covariance in the first card hold. Spectral graph correlations may be
useful after feasible decoding; this is the hypothesis, not a consequence
of the covariance formula. The PSD-Laplacian raw-energy obstruction remains.
Spectral filtering itself and the matrix eigensolver are established classical
tools. No novelty, computational advantage or physical compatibility is claimed.

## Controls and common discoveries

The seven arms remain B,D,species4,Gaussian_Bcov,IID uniform,continuous-phase
multinomial,spherical-coherent multinomial. Each independently selects its
encoder/lambda setting on DEV data. The coherent arms use the SAME V and
their own analytic unconditional marginal PIT. These are essential tests of
whether ordinary classical coherent bunching already explains a gain.

The first card's phase and sphere PGF coefficients/positive mixture apply
with q_ia=|V_ia|^2 summing to mu_i<=1. A NEW pure helper is needed; do not
pass such rows to the old unit-row oracle or renormalize them to one. Use
continuous phases or r+1 roots, not four roots. Independently check r0/r1,
mu0/mu1, nonuniform subunit rows and all small phase assignments before DEV.
Every marginal table, correction, source grouping and seed separation is saved.

Before proposals, score and share all planned frontend discoveries: capped
best-swap anchor, all K^2 anchor swaps, zero/greedy/vacuum-mid-PIT decoders,
plus top-K AND bottom-K rounding of each of the r+1 available lowest marked
Laplacian eigenvectors. Count these scores and share the best Cref/subset.
No such scored partition is loaded into the optical input. All preparation
costs and classical discoveries are credited before measuring gain.

Strong feasible baselines: anneal,spectral+swap,collective KL,shared-Delta
block matching, and spectral_coherent_rounding. The new baseline uses the
already shared V for BOTH encoders, independent Gaussian-spherical or
fixed-modulus phase coefficients (alternating deterministically), rounds
top-K |Vz|^2, then improves by feasible swaps within the declared score budget.
All rounding/scoring/local work is charged. Each baseline gets its own full
budget; do not take a free oracle portfolio maximum. Record actual measured
time prefixes separately. The old score units remain informative scored
queries, not an exact count of every repeated helper call or a QPU latency.

## Frozen execution population

Four NEW DEV graphs, not held-out, all weights1..9 and no replacement:
N26/r13 ER4802601, RR4802602; N34/r17 ER4803401, RR4803402. ERp=.35,RRdegree4.
Two trial seeds0/1, four encoder/lambda settings, eight draws each:256 per
primary arm;3840 injected simulated photons per optical arm. Decoder target
K=N/2, seed-size q=ceil(K/2). Baseline budget3200/5536 informative scores per
graph/trial. Grid, seeds and all conventions are frozen in JSON before code
execution. No known optimum, optimum mask, held-out graph, QPU call or paper.

One numerical worker/thread, CPU60/wall90/output32MiB/planned arrays256MiB.
Code/helper/spec/contracts/tests committed before preflight; independent
static review followed by targeted physics/decoder tests before unique main.
All negative/partial/failure outputs survive; no automatic retry. A finite
DEV signal can only trigger FOLLOW-UP; held-out and independent resampling
with matched total costs are still mandatory before paper/hardware steps.

Pre-code clarification after independent physics reading: production phase
coefficients are CONTINUOUS uniform angles, including the coherent-rounding
baseline. An r+1-root grid integrates the multinomial count law exactly but
need not preserve column-phase invariance of the nonpolynomial top-K rounding
rule; it is used only for finite marginal fixtures. A zero graph may have a
diagonal projector. No universal nonzero offdiagonal or lower bound on mu_i
is imposed. No P48 numerical execution or DEV outcome preceded this clarification.

Pre-execution preparation amendment (the unexecuted first source snapshot
e87035a is preserved; a new source freeze must include this amendment): for EACH
V also score/share top-K and bottom-K sets of mu and of EVERY column |V[:,a]|^2.
Signed spectral-vector roundings do not generally cover those squares. Add one
rectangular assignment maximizing the product of the K selected source-to-row
intensities, using cost -log(max(q,1e-300)), and score its selected K output rows.
These are graph/encoding-dependent CLASSICAL discoveries, charged to the shared
frontend/Cref, never extra optical successes. Record the log-floor and matrix
costs. This prevents a preparation/intensity bias from becoming a reported
optimization benefit. No graph seed, parameter grid or sample budget changes.
