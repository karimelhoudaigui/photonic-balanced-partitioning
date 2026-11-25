# P55 finite-coherence DEV pilot: static proposal

25-Nov-2026. **STATIC ONLY. No pilot code, new graph, phase draw, import,
sampler calibration or simulation has been executed for this proposal.**
Root must accept the card before implementation; new source/tests/contracts
then require freezing, independent review and an exclusive numerical slot.
The qualified decoder is unchanged at `4812e881`; its29-test evidence is
`3f8ed4ad`. Existing results, raw data and manuscript remain immutable.

## Question and indispensable discriminator

Can finite coherent multi-defect interference in a full-CF passive walk improve
the neutral-count decoder beyond independently selected distinguishable,
limited-species, coherent-field, marginal-only and inclusion controls, while
surviving a strong from-raw classical search under B's own classical cost?
Small-time gain alone is already classical: D at sqrt(2)*t matches the leading
decoded law and the P45 inclusion process matches the entire count law at
order t^2. Those exact leading replacements motivate mandatory retimed grids
below. No positive is accepted from this small DEV pilot.

Use N=r=20, K=10, ideal eta=1 and full input (1,...,1). For each supplied
weighted graph define H_ii=0, H_ij=sqrt(w_ij), rho=||H||op and

    Hbar=H/rho,    U_G(t)=exp(i*t*Hbar).

For rho=0, retain the graph and use U=I. No source state, partition, optimum,
incumbent or cut query enters U. The full-source mean is identically one in
every output mode, so direct intensity preparation cannot supply a cut.
Compute the real-symmetric eigensystem once per arm and build each matrix
exponential from its spectral phases; charge both operations. Degenerate
eigenvalues require no selected-eigenspace gap convention for this full
matrix function. Retain residuals and reject nonfinite or >3e-12 unitary
max-entry residuals as INCONCLUSIVE, without replacing graphs or samples.

## Prospective population, source and exact decoder

Two previously unopened DEV cases only: N20 weighted ER, seed5502001, with
p=4/19; N20 weighted RR degree4, seed5502002. Use the pinned NetworkX
generators, sorted edges and PCG64 weights integers1..5 inclusive, seeded by
the existing `P43.seed_for(case_seed,"weights")` convention. Do not silently
reuse the old generator's fixed density/degree/weight range. Disconnected,
zero-weight or easy graphs remain in the population; no optimum is computed.
This is not held-out evidence or a claim that two graphs represent a family.

Every nonnegative integer occupation goes to the SAME qualified
`NeutralityDecoder(counts)`: sample uniformly from all balanced subsets
minimizing |2*sum_selected(counts)-sum(counts)|. A private Python
`random.Random(seed).randrange` oracle supplies the one exact rank, under an
independent recorded rank-seed namespace. Record that rank, boundZ, all
target counts, output subset and raw cut. All collisions and every completed
attempt count. Product-marginal totals vary and are NOT conditioned to20.
An out-of-domain/resource/numerical failure is retained and makes the full
pilot INCONCLUSIVE; it is never a resampled shot or a favorable subpopulation.

Theoretical domain bounds are unchanged. Physical models have M20 and4851 DP
cells. Product-B marginals have each count<=20, hence M<=400 and at most92631
cells, below the qualified prototype's2-million-cell guard. No DP cache across
shots is assumed; construction, validation, exact-rank generation and one
actual graph cut score are charged every time.

## Six independently selected models; eighty draws each

Each model receives24 training and16 NEW evaluation draws PER GRAPH, thus80
draws/model and480 total. B accounts for80*20=1600 ideal simulated injected
photons. D and b4 have the same attempts and20-photon source cost. Actual QPU
calls/photons are zero. Classical count surrogates are computational controls,
not experiments that have physically emitted those photons.

| Model | Training policy grid | Draws/policy/graph |
| --- | --- | ---: |
| B, all20 identical | t=1,2,4 |8 |
| D, independently selected | t=1,sqrt(2),2,2sqrt(2),4,4sqrt(2) |4 |
| b4, five species of four | t=1,2,4 times grouping ID0/1 |4 |
| Continuous phase plus FULL counts | t=1,2,4 |8 |
| Independent B one-mode marginals | t=1,2,4 |8 |
| Bose-inclusion CTMC | horizon tau=1,2,4,8,16,32 |4 |

b4 groupings are two cut-blind, independent seeded permutations of ALL input
ports, chunked into five groups of four, fixed before training. They represent
two finite controls, not optimization over every possible species assignment.
Their preprocessing costs belong to b4 alone. Use namespaces551010/551011
and the case ID. Future positive screening must strengthen this finite control
rather than claim globally optimized b4 from two groupings.

Training seeds use namespace552000 plus case/model/policy ID; the8-draw cells
use two4-draw trials and4-draw cells one trial. Evaluation uses namespace553000
plus case/model/selected-policy ID and trial0/1, eight draws per trial. Optical,
field/count, CTMC and exact-rank roles have distinct derived seeds. Check role
collisions before draws; all batch order and seeds are recorded. The global
Perceval/exqalibur RNG is reseeded immediately before each optical batch,
with no interleaving between models or policies. This gives reproducibility,
not seedwise coupling of independently sampled physical laws.

For each model select ONE global policy after both graphs' training, minimizing

    L=(1/2)*sum_graph Fraction(sum_ALL_training_cuts,
                             draws_for_this_policy*max(1,total_edge_weight)).

Every cut, including bad ones, contributes. Use exact Fraction comparison and
canonical grid-ID ties; never C*, optimal masks, minima or postselection.
Archive selections before any fresh evaluation; do not change them afterward.
Each model's paid-best per graph includes ALL its own train+fresh cuts, without
giving those discoveries to another source, decoder or comparator. The
uniform-balanced normalized mean N/[2(N-1)]=10/19 for positive total weight
(zero for a zero-weight graph) is an analytic null, not an optimum and not a
reason to call a below-uniform result nontrivial.

## Existing local samplers and prospective numeric gates

Use local `Clifford2017Backend` via the already used P43 optical factory for B
and b4, and its independent per-input categorical law for D. Full source ports
are0..19 (permuted for b4 grouping); no Processor/RemoteProcessor. Explicitly
set `exqalibur.Config.compute_max_thread_count=1` BEFORE constructing backends,
in addition to all thread environment variables. Never enumerate the full
20-photon Fock space, use a SLOS probability distribution, or allocate a
2^20-by20 matrix as a convenience. Existing scalar `sample()` suffices.

The phase control is the actual P50/P48 full-count model: independent continuous
phases z_j=exp(i*phi_j)/sqrt(20), p=|Uz|^2, followed by Multinomial(20,p).
Use `P48.coherent_counts` unchanged on v=U or the identical audited P50 branch.
Record/guard mass correction<=3e-12 before roundoff normalization. DO NOT use
`P43.phase_field`: its fixed-cardinality weighted_subset returns all modes at
r=N and would be a trivial, invalid substitute for the intended control.

Product-B PMFs use ONLY the existing immutable P48 `repair_probability_row`
and `factorial_marginal(row,True)` helpers, per row of |U|^2; no all_marginals,
PIT or empirical calibration. The shift-PGF coefficients are h!*e_h(q), but
the probabilities are the expanded [z^s] coefficients, not those shift
coefficients themselves. Keep their Decimal80 arithmetic and prospectively
require input repairL1<=3e-12, PMF correctionL1<=3e-12 and final CDF
correctionMax<=3e-12. Preserve raw diagnostics; failure is INCONCLUSIVE, with
no precision/fallback/clipping change after data. A repaired row has sum<=1,
so h!*e_h<=1; the alternating expansion's absolute coefficient sum is bounded
by2^(r+1) at r20. This gives ample nominal Decimal80 headroom but is NOT a
validated interval or relative-error guarantee for near-zero probabilities.
Before DEV, separately freeze/qualify exact Fraction r20 identity and uniform
row fixtures and a mixed row, checking the full coefficient transform and
normalization against the Decimal helper. No N20 graph is used for calibration.
PMF preparation and all controls' numerical work contribute ZERO B allowance.

CTMC starts at all-one counts and uses off-diagonal rates
|Hbar_ij|^2*n_j*(n_i+1), the existing P45 Gillespie kernel. Its old factory's
source initializer is (1,...,1,0), so do NOT call it unchanged for fullCF.
Only adapt initialization to20 ones under later code review; retain exact
waiting-time/horizon semantics and charge the computation. A4096-event/shot
guard is prospective: retain elapsed/horizon/counts on failure and mark the
pilot INCONCLUSIVE, never decode a truncated chain as a completed draw.

## B-only cost and strong feasible-search veto

For each graph define T_B as B's measured CLASSICAL wall time for its OWN raw
graph conversion/validation, square roots/H, eigensolve/normalization/matrix
exponentials, own necessary residual guards, classical RNG/constructor setup,
every DP/exact-rank/cut score, aggregates and half of global B selection.
No comparator PMF, grouping, phase, CTMC, optional observable, diagnostic for
another model, recording, compression or raw-audit work inflates T_B.
Optical cold import, backend setup and bosonic count generation are recorded
separately and grant ZERO classical allowance: this deliberately favors B by
assuming zero optical latency, not a measurement of hardware runtime.

Run the QUALIFIED P50 `solve_from_raw` twice per graph, independently: fixed
random-first and fixed spectral-first initializations, each granted T_B CPU
seconds less its own measured adapter cost. Only raw adjacency and its own
seed(namespace554000,case,mode) enter. No B subset, eigensystem, priority or
incumbent is supplied. No free best-of-two portfolio is counted as one solver.
Compare only the helper's online deadline-eligible snapshot, never late best;
keep nullable/early-cap/first-scan flags and all actual overruns/export times.
Any insufficient eligible search result prevents acceptance of a positive.

**Mandatory veto:** if ONE fixed FAST algorithm equals or beats B's full
train+fresh paid-best on BOTH graphs, this frozen pilot cannot be positive,
whatever B>D contrast or favorable count observable is observed. One favorable
graph alone remains INCONCLUSIVE and does not open held-out testing.
If B does not improve fresh equal-graph mean against independently selected D
and inclusion, the finite interference mechanism fails this DEV screen; a gain
over uniform or over D at B's own time is insufficient. Report all other
controls as additional explanations and vetoes. Even clearing these screens
would be FOLLOW-UP ONLY: weak per-cell precision, two graphs and finite control
grids cannot establish a reproducible population effect or optimized advantage.

Record defect mass sum|n_i-1|/2 (integer for fixed M20), DP error/ways, collisions
and all raw cuts as descriptive diagnostics. Do not discard single-hop/no-hop
events or train on a multi-defect subset. Their frequencies cannot turn an
order-t^2 classical gain into a new interference claim.

## Resource projection and stopping rule

Caps: CPU60s, wall90s, one thread, total new output32 MiB, planned logical
workspace256 MiB. This is an engineering projection, not a calibrated N20
runtime or a hard Darwin RSS guarantee. P50's archived17-photon batches used
about0.306 CPU seconds for16 B draws; these are source/size-specific observations,
not transferable bounds. Budget a conservative0.3s per N20 B draw (24 CPU s
for80), then12s all classical count/CTMC/PGF work,8s decoding/selection/FAST,
and6s CPU import/overhead: about50 CPU s. Archived cold Perceval wall was about15s,
so a nominal65s total remains below90. Unknown native sampler workspace and
time variation remain risks; do not present this as measured feasibility.

Keep only20x20 matrices, small PMF tables and one decoder DP at a time. The
largest declared DP is92631 cells; no raw event stack is needed (stream to
gzip). Explicit arrays/tables should stay well below16 MiB; planned256 MiB
also reserves native workspace, which is not independently memory-profiled.
Expected480 shot records, contexts and compact search traces fit below8 MiB;
reserve32 MiB without saving exponentially large distributions or DP tables.

No hidden warmup/calibration API run is allowed. Freeze source/import closure,
tests, seeds, guards and the six-model policy table before any import or draw.
Qualify synthetic fixtures once under root's slot, then wait for explicit main
authorization. If caps/guards are hit, preserve the first run and partials,
mark INCONCLUSIVE and STOP; no automatic retry, reduced graph or cap increase.
This80-B-shot design is the PRE-DATA reduction. It promises an inexpensive
falsification attempt, not power to confirm a discovery. A later revision
requires a genuinely new prospectively reviewed card, never silent replacement.

Full20-photon preparation and PNR remain unverified at Lucy/TGCC. No QPU
compatibility, experiment submission, hardware handoff or paper revision is
authorized by this proposal, and eta1 does not establish robustness to loss.
