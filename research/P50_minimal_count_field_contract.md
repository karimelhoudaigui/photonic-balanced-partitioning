# P50: new prospective minimal count-field test

Implementation-only checkpoint, 25-Nov-2026. No P50 graph, numerical import,
test, sample or outcome has been generated at this checkpoint. ROOT cards
1b4479f/7b188e7/f9689d2/79d3550/ded2cfb and the subsequent notation clarification
ff32ba6 define this protocol. All previous P49 data and its cost-scope review
remain immutable; this is not retrospective repricing of that pipeline.

## Finite question and scope

On four NEW DEV graphs N50/r13 and N100/r17 (ER/RR; fixed seeds below), test
whether a B-specific useful count dependence survives ten separately trained
models and two independently budgeted from-raw classical searches. Decoder:
top K=N/2 of H(n-mu)+beta*zeta, H=I-alpha L/dmax (identity if dmax=0), alpha0/1,
beta0/.1, independent Uniform[-1,1] jitter. All counts/collisions are retained;
r is not K. eta=1 is an ideal simulation, no physical loss/cost claim.

Tie rule is the PRE-DATA root79d3550 rule: subtract max(y), then
floor((y-max(y))/1e-12+.5); rank descending buckets, then ascending carried
priority. This rule is common-offset invariant in exact arithmetic. Floating
equivalence at a bucket boundary is not guaranteed; tests separate both sides
and avoid such boundaries for the carried-relabeling fixture. A positive
unquantized support gap alone does not imply bucket retention.

Population: weighted ER p=8/(N-1), RR degree8, sorted edges and independent
seed_for(seed,"weights") PCG64 weights in integers1..5 inclusive, following
the old deterministic generator convention with the NEW frozen parameters.
Seeds: 5005001/5005002 at N50, 5010001/5010002 at N100. No filtering or replacing
graphs. Matrices are independently copied/validated by every arm.

Source frames: Fourier rows ordered by the carried priority permutation;
first r marked spectral eigenvectors, and the two fixed P49 right rotations.
Marked operator is L/||L||op+.001 diag(marks), zero L handled explicitly.
Occupied pivot gauges are carried and fixed BEFORE R. The full eigen/Fourier
frame provides an orthogonal vacuum complement, avoiding any source choice
from a classical or trained partition. All occupied and boundary gaps are
saved/guarded1e-12; residual guard3e-12. Missing/numerically invalid cases
prevent full-panel interpretation, not grounds to substitute a new graph.

Training roots5020001, evaluation5030001; marks5040001, carried priority and
Fourier row order5040002, from-raw classical5050001. Hash with immutable P43
seed_for(case,model,policy,trial,role). No extra unregistered namespace.

## Controls, selection, and cost independence

Six 16-policy models plus the new independent-marginal arm: B, D, contiguous
b4, continuous phase, Gaussian_Bcov, independent final-variance Gaussian,
independent_B_marginals. Every one has four bases xalpha2 xbeta2, two train
draws per cell. Sphere and static have eight nonredundant cells x4. Pure jitter
has two beta cells x16. Each pays32 training draws/graph and32 fresh fixed-policy
draws (two fresh16-draw trials); equal256 campaign draws per model.

The model-specific global loss is EXACT Fraction mean of every cut divided
by its graph total weight, with equal four-graph weight. Canonical first ID
breaks exact ties. Selection freezes before every fresh shot. No Cref, C*,
optimum, mask, improvement filter, greedy completion or evaluation reselection.
The private paid train/eval/total minima contain only actually sampled cuts.

Covariance control uses diag(mu)+|VV*|^2-2 QQ.T. Gaussian factor clips only
eigenvalues in [-1e-10,0], otherwise fails; exact empty/one-hot-unit rows are
masked in F BEFORE H. Independent final variance is ||(H F)[i,:]||^2 of this
ACTUAL factor. A mode deterministic before diffusion may fluctuate afterward.
No post-H mask or reuse merely because P/mu is invariant under R.

Independent B marginals use only unchanged p48.repair_probability_row and
p48.factorial_marginal(row,True), including its expansion of the (z-1) basis
into actual count probabilities. Decimal80 input/PMF repairs and CDF float
corrections are saved. Counts are independent, sum(n) NOT conditioned to r;
matching is before H, not a claim of matching diffused marginals. All this
setup and sampling belongs solely to that classical arm; B never calls it.

Fourier static preparation duplicates the pure-jitter/tie law for either
alpha, and the declared duplicate cells remain. Monomial B/D/b4 outputs are
deterministic; phase/sphere are not. Column phases after full V and complex
conjugation assert equal count laws, not same-seed sampler equality. A K_{k,k}
fixture shows alpha1 can return a maximal cut, so diffusion has no generic
energy-improvement guarantee. These are falsifying nulls, not positive claims.

Every arm independently pays its own validation/conversion, source preparation,
mu/H, necessary completion, RNG setup, generation if classical, ranking and
cut, aggregation and selection. B never computes covariance, other-model PMFs,
classical searches or per-source diagnostic residuals inside its grant. Optical
backend setup/cold import and synthetic count generation are separately timed
and grant ZERO CPU, not claimed to be zero real latency. Raw/context/trace JSON
is outside search clocks. No common reference partition or free solver priority.

Two independent FAST calls, random-first and spectral-first, start from raw A.
Each receives CPU equal to the measured B-only classical WALL (preparation,
classical batch setup, ranking/cuts/aggregation, one-quarter of global selection),
minus measured adapter CPU. Every helper validates/converts and initializes
inside its own CPU timer, performs best-pair descent FIRST, then annealing and
perturbations/restarts. Only completed deadline-eligible results are credited;
no eligible init, early100M guard or safeguard => no positive interpretation.
No free best-of-classical portfolio. Full helpers/API are independently owned
and reviewed; the primary code only calls the frozen interface.

## Projection before outcomes

Fixed work: 2,560 primary decoded cuts total; B/D/b4 each256 draws/3,840 injected
SIMULATED photons (1,920 each train/eval). At most36 marked eigensolves of size
<=100 across the nine source-dependent arms; Gaussian controls add32 covariance
eigensolves, all excluded from B. Independent marginal DP covers1,200 rows of
<=17 photons in O(N r^2), not full Fock enumeration. Each optical arm uses72
batch setups; b4 has324 small-group backends, B72. Serial Clifford2017 only.

P49 completed the same256 samples at r13/17 per optical arm in9.584 CPU/23.402
wall seconds including much heavier greedy completion, marginal tables and
174,720 legacy scored proposals. P50 keeps the photon range/sample count but
increases modes to100 and local backend initializations10 to18 per graph.
Removing greedy/legacy work is not assumed to cancel these costs exactly.
A conservative engineering projection is CPU<=45s/wall<=75s, not an observed
benchmark or certificate; caps remain CPU60/wall90 with no automatic retry.

Dense arrays: source frames/contexts up to100x100 complex128, covariance/factor
100x100 float64 and sparse H. Even retaining all independent per-arm copies,
planned arrays<32MiB plus local backend/transient headroom within256MiB planned
live arrays; this is not a hard Darwin resident-memory guarantee. Raw2560
rows, compressed per-case contexts and compact FAST traces are projected
<28MiB NEW data. Script checks32MiB and retains partial files on failure.
No near-cap or incomplete run is a complete-panel result; no seed/cap retry.

## Freeze, qualification, evidence

New primary script/spec/contracts/tests must be committed before any scientific
import/test/sample. Complete transitive execution artifacts include the unchanged
P49 source, P49 FAST (import only), P48 source/coherent helper, P45 source and
P43 source, plus the independently frozen P50 from-raw helper and pinned project
metadata/lock. Immutable helper tests are not silently edited. Root/physics
review source, caller/cost closure and projection before the exclusive slot.
Finite preflight checks hand-computable Fock laws, PGFs, Gaussian invariants,
phase/gauge/HOM, tied/relabeled decoders, ALL-shot selection/fresh roles and
from-raw eligible initialization/first scan. A PASS is not a DEV positive.
The current authored preflight contains53 primary finite cases plus the21
independently qualified FAST cases,74 total. None has been run by this author
before the source freeze; static Python AST/JSON authoring imported no project
or scientific module and opened no graph population.

Reproduction commands (only AFTER explicit source review + numerical slot):

```text
/private/tmp/pbp-clean-venv-20261124/bin/python -m pytest -q tests/test_p50_minimal_count_field.py tests/test_p50_fast_from_scratch.py --junitxml=research/P50_minimal_count_field_preflight/run_001/junit.xml
/private/tmp/pbp-clean-venv-20261124/bin/python research/P50_minimal_count_field_probe.py --spec research/P50_minimal_count_field_spec.json --output experiments/P50_minimal_count_field/run_001/data
```

Run under the installed Mathbox bounded v2 runner, CPU60/wall90/thread1/log32MiB,
exact frozen input closure; parent run_001 is distinct from child run_001/data.
All declared results, raw collisions/counts/fields/jitter/masks/cuts/seeds and
losing cells retained with fresh output and hashes. No positive accepted here:
DEV signal only licenses a new held-out design, independent physical replication,
adversarial review, total resource/loss closure and eventual authorized QPU.
No manuscript, external message or hardware call is part of this protocol.
