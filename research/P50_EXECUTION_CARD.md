# P50 — prospective minimal count-field discriminator

2026-11-25. ROOT checkpoint b3e62ab, after the completed negative P49 and
677 passing tests. This card authorizes implementation, not an unreviewed run.
It fixes a new DEV question, not a retrospective repricing of P49.

## Question and mechanism

Can all-count, graph-diffused, balanced ranking extract useful interference
correlations at lower classical decoding cost than the P45–49 completions?
The mathematical proposal and its reverse-inclusion null are in
P50_MINIMAL_COUNT_FIELD_CARD.md. P44 does NOT cover this completion. The test
must discriminate a B effect from source preparation, continuous coherent
fields, second moments, independently optimized D and efficient search.
No positive result is accepted on this DEV panel.

## Frozen population and model grids

Four NEW DEV weighted simple graphs, generated only by the reviewed script:
N50/r13 ER seed5005001, N50/r13 RR seed5005002;
N100/r17 ER seed5010001, N100/r17 RR seed5010002. K=N/2.
ER p=8/(N-1); RR degree8; positive integer weights uniform1..5 via the
existing deterministic graph helper, with its exact convention saved.
No graph is omitted or replaced based on spectral gaps, output or runtime.
Numerical/resource failure is preserved and prevents a complete-panel claim.

Four isometries: graph-blind first r Fourier columns; first r eigenvectors of
normalized Laplacian +1e-3 diagonal independent marks; the same E times the
P49 R(pi/4,0) and R(pi/4,pi/2). Carry the pivot gauge BEFORE R. Source ports
are0..r-1, with no incumbent or partition input. All occupied and boundary
eigenvalue gaps are saved/guarded at1e-12. Preserve all occupations and losses
(this pilot uses eta=1); r is distinct from target partition size K.

H=I-alpha L/dmax, alpha0/1; beta0/.1; zeta_i iid Uniform[-1,1]. Output the
top K of H(n-mu)+beta*zeta using a fixed carried priority. Prospective tie
definition, clarified BEFORE implementation/data: set t=y-max(y), then bucket
floor(t/1e-12+.5), descending bucket and carried priority. The max anchor makes
the exact rule invariant under a common offset and safely ties nearly uniform
fields whose range is <.5e-12. Fixed bin boundaries can still be sensitive to
floating error; test both sides, do not assert tolerance gives universal exact
relabeling across a boundary. mu=sum_a |V_ia|^2. The Fourier static alpha0/1
cells are duplicate laws of pure jitter/ties, retained with the declared effort,
not separate discoveries. No posterior graph/policy substitution follows.

B, D, contiguous-source b4, continuous phase, Gaussian_Bcov, and independent
final-variance Gaussian each train16 basis/alpha/beta policies x2 draws/graph.
Sphere trains8 policies (Fourier/E only) x4. Static preparation trains8
(Fourier/E only, field -Hmu+beta*zeta) x4. Pure-jitter/tie control trains2
policies (beta0/.1, no source/H dependence) x16. Every arm pays32 training
draws per graph, then32 NEW fixed-policy draws, split across two fresh seeds.
Final independent variance uses row squared norms of H F, where F is the
ACTUAL Gaussian factor (including any documented numerical repair), not
diag(Sigma_B), a separately repaired covariance or an R-invariant assumption.
Gaussian uses H F g. Mask deterministic rows only in F BEFORE H; a formerly
empty row can fluctuate by diffusion from its neighbors. Monomial sources
make B/D/b4 deterministic, not phase/sphere; conjugation asserts equality of
laws, not equality of every same-seed realization.
Static and pure-jitter controls are physical-preparation nulls, not photons.

Global model-specific selection minimizes the EXACT Fraction mean of ALL
balanced cuts / graph total weight, with equal weight on all four graphs;
canonical first-policy tie break. Training and evaluation use disjoint role
namespaces, rooted at5020001 and5030001 respectively; marks/priority at
5040001/5040002, classical solvers at5050001. Derive per-role/case/policy/trial
seeds with the pinned P43 helper and save each seed. No objective uses C*,
optimal masks, an improvement filter, Cref, a classical incumbent or eval data.
Private paid training minima may be retained but never fed back to the source.

## Cost closure and strong controls

No shared search, Cref, swap table, marginal PIT/CDF or greedy decoder.
Meter B's OWN graph validation/conversion, marks/gauge/eigensolve, all source
matrices/necessary completion, mu/H, classical sampler RNG setup, jitter,
ranking, cut scores, training aggregation and selection. Other-model PMFs,
Gaussian covariance/factors and diagnostic calculations cannot enter B cost.
Graph generation is a supplied-instance cost, excluded symmetrically; input
conversion/validation is paid. Cache only within the actually executed arm.
Preserve both experimental spending and selected-policy deployment ledgers.
Optical numerical backend/count generation is timed separately, grants ZERO
CPU to classical controls, and is not asserted to be zero physical cost.
Serialization and read-only reporting are excluded from both search budgets.

Two independently budgeted, from-raw-A classical controls: random balanced
initialization + best-pair descent FIRST, and independently computed spectral
rounding + best-pair descent FIRST. Each then uses incremental annealing,
perturbations/restarts. Each receives CPU allowance equal to measured B-only
classical WALL including its share of global selection. No free initial cut,
priority, eigensystem, reference partition or timing from another control.
Only fully completed deadline-eligible initialization/search batches count;
retain late prefixes separately. A guard max100M proposals, no wall deadline
apart from enclosing runner. Early guard or missing eligible result prevents
any positive interpretation. Never select a free best-of-classical portfolio.
Both one fixed classical algorithm and the separate optical/coherent/null
arms must be beaten before a potential signal can progress.

## Evidence, qualification and limits

Save raw counts/fields, jitter, masks, integer cut, role seeds, policy/stage,
all losing training cells, fixed selections, collisions and time components.
Context records contain A, V, mu/H, covariance/factor only for arms needing
them; do not duplicate per-shot N by N arrays. Save compact solver traces.
Use deterministic gzip metadata; no raw file is modified after sealing.

Preflight requires exact one-photon and monomial laws, phase/conjugation/null
fixtures, source R/gauge/HOM checks, covariance/factor/PSD and deterministic-row
checks, all-shot selection/no-eval leakage, tie/uniform-mu and carried
relabeling, independent final variance, classical from-scratch deadline and
initial-scan behavior. Import old helpers unchanged, document the complete
transitive execution input closure, and qualify FAST separately if needed.
Root and independent physics/caller reviews precede the single DEV run.

Exclusive one worker, all native threads1. CPU60s/wall90s, planned live arrays
256MiB and new output32MiB, no hard Darwin memory/affinity promise. Projection
must justify these caps before execution; no outcome-driven retry or increase.
Use the existing pinned37-package Python environment. No new model/package,
manuscript, hardware call or branch merge. Root audits raw data/commands/tests
before any accepted interpretation. A DEV signal would only authorize a new
prospective held-out design and independent physical-sampler replication.

Owner: encoding implements primary new P50 files; adaptive owns disjoint FAST
helper/tests; physics audits. All edits isolated in their existing worktrees.
No simultaneous numerical workers. Unresolved goal remains a reproducible,
novel, interference-dependent optimizer gain at matched TOTAL resources.
