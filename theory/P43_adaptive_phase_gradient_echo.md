# P43 — finite-angle phase-gradient echo: frozen exploratory discriminator

Status: DESIGN ONLY. No P43 experiment has been run in this lane. This card is
an optimum-blind, development-only veto of a concrete mechanism, not a positive
result, novelty claim, resource advantage, hardware gate, or manuscript revision.
Author: adaptive lane; same broad project context as P41/P42. Root will implement
an independently written harness and close its execution contract before any run.
Machine-readable population and parameters: `research/P43_adaptive_contract.json`.

## 1. What changes, and what remains open

P41 established a collision-gap certificate for a graph total-variation cost,
but neither this certificate nor lower same-frame bosonic mean proves better
optimization. In particular, a sum of two-mode nonlinear observables is not, by
itself, an escape from classical additive estimation of local means. This pilot
therefore trains on actual incumbent improvement, a global clipped payoff, and
uses finite coherent echoes involving all source photons. It retains strong
global correlated classical proposals. No hardness of the clipped payoff or its
sampling is asserted. Its graph score is itself easy to compute classically.

The decisive question is whether the frozen family has any reproducible
improving-candidate signal that survives independently tuned distinguishable
particles, bounded-order interference, correlated feasible proposals, and
ordinary feasible search. Failure closes only this family and pilot budget.

## 2. Fixed common source and exactly physical payoff

Let G have m=2k vertices, k>=2, symmetric nonnegative adjacency A and zero diagonal.
For binary x with sum x_i=k, define

    C(x) = sum_(i<j) A_ij |x_i-x_j|.

For each graph, construct ONE common anchor S0: a seeded uniform balanced set,
followed by charged, budgeted best one-swap descent. Every move delta examined,
initial/final score, scan stopping reason, and preprocessing time is recorded.
Use strict improvement only and deterministic tie-breaking. The final anchor is
fixed throughout all tuning, all models, all seeds, and the relabel probes; the
pilot has no adaptive source replacement. Root's execution contract must freeze
the descent budget and tie rules before graph generation or outcomes. A scan
that exhausts its budget must not be called a certified one-swap local minimum.

Inject k fully identical photons, one in each mode in S0, with input photon order
the sorted original S0. Transport that order under relabeling rather than sorting
the permuted labels anew. The fixed anchor has charged cost C0. All methods start
with it as an already known classical discovery. If C0=0, the graph is retained
as already classically solved; it is not replaced by a harder graph.

For lossless occupations n with sum n_i=k define

    F_G(n) = sum_(i<j) A_ij |n_i-n_j|,
    R_k(n) = sum_(i<j) |n_i-n_j| - k^2,
    epsilon = 1/4,
    lambda = (C0+epsilon)/(2(k-1)),
    J_G(n) = F_G(n) + lambda R_k(n),
    L_G(n) = min(C0, J_G(n)),      gain(n) = C0-L_G(n).

The coarea identity gives R_k=k^2-sum_l |{i:n_i>=l}|^2. It is zero at every
collision-free (CF) occupation; every collision has R_k>=2(k-1). Nonnegative
weights imply J_G>C0 on collisions, whereas J_G=C(S) on CF. Therefore, EXACTLY,

    gain(n) = max(0, C0-C(support(n))) if n is CF with k photons;
              0 otherwise.

This equality is the entire role of the certificate. Implement the right-hand
side directly; no numerical J or penalty arithmetic is necessary. It neither
uses C*, optimal-state masks, optimal partitions nor conditions the shot count
on acceptance. All rejected attempts consume budget and hold the incumbent.
The global clipping is essential to the stated objective; no inference from
cheap classical local-mean estimation is used to declare it hard.

The pilot is ideal and lossless. Wrong detected photon totals must be rejected
BEFORE any future use of R_k: the vacuum would have negative R_k. Existing P42
low-survival obstructions remain relevant to a later physical direct-CF protocol.

## 3. A genuine graph-dependent finite-angle echo

Let x=1_S0, d=A1, and ell=d-2Ax. This ell is the LINEAR cut gradient; it is not
the signed single-flip increment (1-2x_i)ell_i. For a in S0, b outside S0,

    C(S0-a+b)-C0 = ell_b-ell_a+2A_ab.

Thus the device is supplied charged one-body graph information, not a hidden
optimal partition. Let P=diag(x) and Q=I-P. Set

    H_cross = P A Q + Q A P,
    H_intra = P A P + Q A Q,
    D = diag(ell-mean(ell)).

Normalize each H by its operator norm and D by its maximum absolute diagonal
entry. A zero norm gives the zero generator, without selecting a new graph.
Keep all graph edges; no selected community or optimal label enters these maps.
For finite angles define

    W = exp(-i gamma H_intra) exp(-i beta H_cross),
    U = W^dagger exp(-i alpha D) W
      = exp(+i beta H_cross) exp(+i gamma H_intra)
        exp(-i alpha D) exp(-i gamma H_intra) exp(-i beta H_cross).

The signs and reversed order in W^dagger matter. At alpha=0 this is exactly
identity; a gradient phase applied directly to a fixed Fock input would carry
only a global phase. The echo instead conjugates it by a graph-dependent mixer.
All k photons traverse the same connected graph-wide interferometer, with no
constant-size interacting module plus spectator shortcut. A disconnected draw
is retained and its actual decomposition reported.

This is a passive one-particle optical construction, lifted to the full k-photon
law Gamma(U). It does NOT implement a nonlinear quantum cut-cost phase or an
imaginary-time descent. It could simply destroy a good anchor through collisions.
No perturbative chiral expansion is invoked for its finite-angle behavior.

The fixed grid, lexicographically ordered by (alpha,beta,gamma), is

    alpha in {-pi/2,+pi/2}, beta in {pi/4,pi/2}, gamma in {0,pi/2}.

These are 8 tuples. gamma=0 is the built-in intra-mixing ablation. alpha=0 is an
analytic identity control with known gain zero, requiring no extra sampled
photons or candidate score. If every estimated gain is zero, choose identity.
If a winning tuple has gamma=0, do not attribute it to the intra-mixing layer.

## 4. Frozen development population and exact sample allocation

Use four unique graphs, no graph selection on outcomes:

| Label | m | k | Family | Graph seed |
|---|---:|---:|---|---:|
| dev16_er | 16 | 8 | ER, p=0.35 | 4301601 |
| dev16_rr | 16 | 8 | simple random regular, degree 4 | 4301602 |
| dev20_er | 20 | 10 | ER, p=0.35 | 4302001 |
| dev20_rr | 20 | 10 | simple random regular, degree 4 | 4302002 |

Assign independent uniform integer weights 1..9 to existing edges in sorted
edge order. Root must freeze graph/RNG implementation and library versions in
the execution contract; all graph matrices are then saved and hashed. Retain
disconnected, easy, symmetric, zero-gradient and unproductive graphs alike.
Generator failure is a saved failure, never permission to inspect and reseed.

For each of B, D, phase-field and b4, use

    4 graphs x 2 sampling replicates x 8 tuples x 14 raw draws = 896 draws.

Each graph/replicate is a primary case with 112 raw attempts. Each model selects
its OWN global tuple by pooled mean actual gain over all four graphs and both
replicates. This is not per-instance retuning, copying B's winner, or an optimum
oracle. Use lexicographic index for positive ties; all-zero means select identity.
All valid discoveries made DURING tuning enter the anytime best-cost record;
none disappear when a final tuple is selected. The pooled 896-shot selection
expense is charged explicitly and is not amortized away on these same graphs.

Freeze selected tuples, raw-data hashes, code and decisions before the next
phase. Then relabel the PRESELECTED dev16_er and dev20_rr graphs once each,
carry the same anchor/input order, and use 2 FRESH sampling replicates x 32 raw
draws per graph/model at the frozen tuple. This adds 128 draws per model, for
exactly 1024 B draws and the same total cap for each of the three sampled
controls. Identity selections may stop without optical draws; do not replace
their unused budget with favorable extra settings.

Check U_(pi G)(pi S0)=P_pi U_G(S0) P_pi^T to numerical tolerance 1e-10 and
cost/gain invariance under permutation before interpreting relabel probes.
These two relabelings are NOT held-out graphs or new independent graph units.
There are only FOUR unique graph units, insufficient for an advantage claim.
No held-out graph outcomes are generated, read, or used in this pilot.

## 5. Mandatory, independently tuned controls

1. **D:** route each input particle independently using probabilities
   |U_(i,s_j)|^2, then sum occupations. This is an exact polynomial classical
   sampler of distinguishable particles, with all collisions retained. Optimize
   its 8 tuples separately using its own data and the same cap.
2. **Global feasible phase-field:** for V=U[:,S0], draw independent z_j uniformly
   from {1,-1,i,-i}, put w_i=|(Vz)_i|^2, and sample a k-subset T with probability
   proportional to product_(i in T) w_i. The elementary-symmetric recursion
   e_r(j)=e_r(j-1)+w_j e_(r-1)(j-1) and backward inclusion probability
   w_j e_(r-1)(j-1)/e_r(j) give an O(mk) sampler. Use stable scaling and a
   declared uniform-feasible fallback if e_k=0, not repeated favorable phase
   draws. This is a strong global correlated control, NOT a proved pointwise
   dominating sampler for arbitrary CF supports. Optimize its own grid.
3. **b4:** partition input photon identities into fixed seeded groups 4+4
   (k=8) or 4+4+2 (k=10). Sample photons within each group as identical using
   the SAME U, and groups as mutually orthogonal species; sum all occupations.
   Preserve cross-species collisions. Carry group identities under relabeling.
   This exact control has bounded interfering order 4; a tie with full B vetoes
   an attribution to growing many-photon interference in this experiment.
   Independently optimize its own grid under the same raw-attempt cap.
4. **Feasible classical search:** uniform balanced draws, randomized nonlocal
   two-swap proposals, balanced annealing, budgeted pair-exchange descent, and
   spectral initialization plus feasible descent. EACH receives 112 scored
   candidates/deltas per primary graph/replicate and 32 per relabel case, beyond
   the shared charged anchor. Every delta examined counts, including rejected
   moves, scans and spectral candidate scores. Record anytime traces for
   comparison at B's actual scored-feasible count as well as raw-attempt count.
   A budgeted partial scan must not be labeled an exhaustive local optimum.

The exact classical schedules, random seeds, delta accounting and stopping
behavior are implementation obligations for root's closed execution contract
BEFORE any experiment. Fixed graph-scale temperatures may use edge statistics,
never C*. Spectral eigensolvers, feature extraction, phase-field DP and model
selection all incur recorded time. A retrospective best-control envelope is a
diagnostic, not a free deployable baseline portfolio. Any positive follow-up
would need to charge baseline selection or freeze the selected baseline.

Use serial Clifford2017 `.sample()` for B and each b4 species if the installed
backend supports these sizes. Do not use a multithreaded `.samples()` pool or a
new exponential full-Fock distribution to fill this pilot's samples. D and
phase-field need no permanent enumeration. Do not conflate easy exact D
sampling with mean-only calculation or reweight D by optical acceptance.

## 6. Costs, stopping, and permitted decisions

Maintain separate ledgers for raw attempts, injected photons k*attempts,
collision-free candidates, graph scores/deltas, common anchor work, feature
construction, circuit compilation, model selection and sampler CPU/wall time.
Cached common computation is charged once explicitly and credited consistently
to controls that use it. Simulation CPU is NOT a measured QPU latency. This is a
generous optical veto, not matched total hardware-resource validation.

Initial root run limit: one numerical worker, one native/BLAS thread, 60 CPU
seconds / 90 wall seconds, arrays <=256 MiB, new outputs <=32 MiB. Preflight and
closure tests precede raw sampling. If k=10 or the full design exceeds this
limit, save partial raw data and declare RESOURCE_INCONCLUSIVE; do not silently
drop the graph, substitute an easier graph, truncate its photon number, or turn
an incomplete run into a scientific rejection. Any revised cap/design is a new
explicit contract before rerunning.

- All-zero B improvements selects identity and records NO_SIGNAL_AT_PILOT_BUDGET.
- A matched-control explanation or stronger feasible search rejects an advantage
  claim for this family at the tested budget; retain all failures and raw data.
- A hint merits another preregistered experiment only if pooled actual B gain
  exceeds independently selected D, phase-field and b4, improving cuts occur on
  at least 3 of the 4 unique graphs, and feasible-search traces do not explain
  the apparent signal at the recorded score/time frontiers. Inspect moved
  photon counts and the gamma ablation; no small-block mechanism claim follows
  from one successful sample. These are deliberately demanding veto conditions,
  not a significance test or accepted discovery threshold.
- A relabel failure, implementation discrepancy, or sensitive fresh-seed result
  is recorded and blocks a mechanistic conclusion. No favorable seed selection.

Every complete outcome remains `DEV_EXPLORATORY_MECHANISM_SCREEN`. There is NO
accepted-positive flag in this pilot. A future positive claim requires frozen
held-out graph tests, independent replication, independently retuned controls,
full resource accounting, and only then a separately authorized hardware plan.
No QPU submission, manuscript edit, or Laurent handoff follows from this card.
