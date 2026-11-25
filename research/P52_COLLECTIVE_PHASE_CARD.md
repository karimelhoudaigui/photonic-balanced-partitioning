# P52 — collective phase response at fixed low moments

2026-11-25. ROOT continuation after P50, base4ebfd90. This is a bounded
mathematical discriminator, not another graph benchmark or accepted optimizer
positive. P50 failed even with its lean budget; its results remain immutable.
P51's general flat-source invariance/loss derivations require independent review.

## New uncertain implication

H4 has a real fourth-order ranked-cut response but its whole decoded law has
an O(1) classical mixture and b4 is exact. Can a GLOBAL eight-photon phase
family produce a ranked-cut mean kernel beyond independently regrouped b4,
continuous phase and exchangeable classical kernels, or does a new classical
convex replacement already close this family? A finite signal cannot satisfy
the user's strong-search/held-out/replication/hardware goal by itself.

Let W=the real H4(1) matrix in theory/P50_Hadamard4_ranked_cut_checkpoint.md.
For theta in {0,pi/4,pi/2,3pi/4}, D=diag(exp(i*j*theta),j=0..3), set

    U(theta) = 1/sqrt(2) [[W, D W], [W, -D W]].

N=r=8, one identical photon in EACH input; target balanced K=4. Source input
does not encode a feasible partition. All occupations, collisions and the
uniform pattern remain; no postselection or failed-shot discard. eta=1 in
this diagnostic. U is unitary, Q=J8/8, P=I8, mu=1, Sigma_B=2I8-J8/4.
The phases act between layers, not as an unobservable final row/source phase.
These facts and source/gauge conventions must be independently checked.

Decoder: top4 of n-1, with UNIFORM independent tie-breaking (equivalently
continuous iid jitter0<beta<1/2). Integrate over ties EXACTLY, no P50 buckets,
fixed priority or graph diffusion. Save the resulting probability of EVERY
one of the70 balanced subsets and the28 edge-crossing probabilities. For any
nonnegative weighted graph, mean normalized cut is the corresponding linear
form in those28 numbers. No graph, optimum, masks, training or planted solution
is generated here. Cost/preparation and exact enumeration are simulator work,
not a quantum optimization gain.

## Controls and deterministic probabilities

Compute B's FULL6435-pattern occupation law by an independent polynomial
creation-operator recurrence (or equivalent bounded exact-support algorithm).
Float64/complex128, retain all patterns including zeros; no amplitude pruning.
Require nonnegativity/normalization and qualification against small direct
permanents/HOM/H4. This is finite numerical evidence, not interval arithmetic.

b4: enumerate ALL35 unordered splits of the8 input labels into two groups of4.
Each group has a330-pattern four-photon law; convolve their counts as mutually
distinguishable species. No favorable fixed grouping or uncharged regrouping
optimization is hidden. Compute all35x4 phase kernels. The canonical split
{0,1,2,3}|{4,5,6,7} should be phase-INVARIANT: its second group differs only
by output row phases when treated alone. Test that null independently.
Other groupings need not be invariant. D, sphere, Gaussian_Bcov, independent
variance, product-one-mode-B and static/jitter are exchangeable here and have
exact uniform70-subset rank law; prove/qualify rather than simulate duplicates.

Continuous phase control: independent phi_j uniform[0,2pi), z_j=exp(i phi_j)/sqrt8,
counts Multinomial(8,|U z|^2). For EACH theta use262144 draws, batches<=4096,
role-separated PCG64 roots5201001, per-theta seed_for(root,index). Retain full
6435-bin count histograms and batch records/digests, not favorable surviving
events. Apply the same EXACT tie pushforward to the histogram. No adaptive
stopping, extra seed, retries or draw increase. These are classical Monte Carlo
calibration draws, not photonic optimization shots or a model-selection stage.

For ALL4*(70+28)=392 phase probability estimates simultaneously, record the
Hoeffding/union absolute error epsilon=sqrt(log(2*392/.01)/(2*262144)) with
failure probability .01. Each tie-averaged indicator lies in[0,1]. This bound
is absolute, not a relative-tail guarantee; deterministic source/roundoff
errors are separate. In particular a weighted normalized cut has error<=epsilon.

## Closure check and interpretation

For each B theta, seek a NONNEGATIVE convex combination of ALL deterministic
b4 phase/grouping kernels and uniform70 which reproduces its28 crossing means.
An optional separate fit may add the four phase-MC kernels, with their error
explicitly propagated; never call that an exact certificate. Minimize Linfty
residual or return verified feasible coefficients. Save ALL coefficients,
nonnegativity/sum errors and reconstructed residual; do not trust a solver
status alone. A small numerical residual proves only a finite tolerance
statement for these mean kernels, not full-law classical simulation, tail
dominance or an arbitrary-size theorem. No graph is selected by a separating
hyperplane and no known minimum is computed.

Any LP solver must use native threads1, a fixed <=1s solver limit per fit,
and documented actually supported options (the prior P47 HiGHS fixture records
the local wrapper convention). If unavailable, keep the fit INCONCLUSIVE;
the independently computed kernels remain evidence. No outcome-driven solver
replacement/cap increase. A nonzero residual is NOT by itself a separating
certificate or an optimization advantage.

Even an unmatched B response is only a necessary mechanism checkpoint:
continuous-phase confidence, strong feasible search, a graph-dependent
optimum-blind construction, total source/circuit/shot/loss costs, held-out
graphs and independent physical sampling all remain. Exact enumeration of70
feasible cuts is trivial at this size, so NO runtime/search advantage is claimed.
Do not freeze hardware or revise paper based on this diagnostic.

## Execution gate

Encoding owns new P52 primary source/spec/contracts/tests in its isolated
worktree, adaptive independently audits resources/statistics/caller and physics
the source/null/low-moment interpretation. IMPLEMENTATION ONLY until source
freeze, projection, reviews, targeted PASS and explicit exclusive slot.
No graphs or P52 draws before that. Existing37-pin Python, one worker/native
thread1; CPU60/wall90, planned arrays256MiB/newoutput32MiB. Use compact
convolution index maps, not dense6435x6435 matrices or9^8 hist arrays. Project
time/memory before running and preserve any bounded failure with no automatic
retry. All commands, inputs and raw histograms must be sealed in a v2 manifest.
Keep all P33/P37/E05b/P45–P50 data and paper bytes unchanged.
