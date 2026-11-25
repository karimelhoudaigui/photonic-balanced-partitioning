# P49: train the feasible-cut mean after coherent spectral-source mixing

25-Nov-2026, ROOT. New prospective DEV cycle after P48's failed control gate;
not a repeat of its fixed encoder grid or an accepted positive. P48 remains
immutable: B gain7, phase13,IID12,b4=11, and one annealing control equals or
beats its best cuts on all four graphs. P33/P37/E05b and later negatives remain.

## Physical hypothesis and fixed circuit family

P48 changed the occupied subspace but did not train its source basis on the
actual feasible-cut objective. Let E be its first K marked-Laplacian eigenmodes,
with the already declared carried-priority pivot gauge fixed BEFORE mixing.
For adjacent occupied mode indices use

    G(theta,phi)=[[cos(theta),-exp(i phi)sin(theta)],
                  [exp(-i phi)sin(theta),cos(theta)]].

Let R=G_even G_odd, where the even layer acts on(0,1),(2,3),... and the odd
layer on(1,2),(3,4),... . This product order is fixed. Use only R=I and
R(pi/4,0),R(pi/4,pi/2). V=E R keeps projector P and row mean mu EXACTLY fixed,
but changes q=|V|^2 and higher count correlations. An isolated pi/4 pair maps
|1,1> to (exp(-i phi)|2,0>-exp(i phi)|0,2>)/sqrt(2), up to convention/global
phase; the full overlapping layers are not assumed to factor into such pairs.
This is established HOM physics, not a new theorem or a guaranteed cut gain.

Four bases, in order: Fourier_blind without source mixing; spectral E; spectral
E R(pi/4,0); spectral E R(pi/4,pi/2). Complete the vacuum modes as P48, fixed
input ports0..K-1, all output occupations and collisions observed. No known
partition is loaded into a source. The hypothesis is that coherent mixing and
training the ACTUAL feasible mean yields a useful proposal law that survives
classical explanations. All intensity/preparation discoveries are still shared.

P,mu invariance does not make D or Gaussian invariant: q enters their laws.
Spherical coherent sampling IS invariant under right-unitary R. IID does not
depend on V. Avoid forcing these controls to tune redundant circuit labels.
Source column phases BEFORE mixing are physically relevant; gauge fixing is
essential. Physical source-output column phases AFTER the complete V remain
irrelevant. Raw quadratic occupation-energy no-go results still apply; here
every scored output is a balanced feasible partition after the same decoder.

## Objective, separate tuning and fresh evaluation

Seven arms: B,D,b4,Gaussian_Bcov,continuous_phase,spherical_coherent,IID. Use
the qualified P48 marginal helpers and exact deterministic-Gaussian defense.
PIT and completion target K=N/2, seed-size ceil(K/2), lambda0/1 remain. b4 uses
contiguous source-port groups of at most4, declared BEFORE outcomes, to give
this structured preparation an architecture-aware partial-coherence control.
Phases are continuous everywhere. Never normalize a subunit row to mass1.

TRAINING LOSS is the mean of cut(S)/sum_(i<j) A_ij, averaged EQUALLY over four
DEV graphs, using ALL shots including worse solutions. A zero-weight fixture
uses denominator1. This uses no C*, optimum masks, success labels or conditioned
energy. Select each model independently by minimum loss, deterministic first
canonical setting for ties. Save every cut, loss, setting and training cost.

- B,D,b4,Gaussian,phase:8 meaningful base/lambda settings,4 training draws per
  setting per graph =32 per graph.
- Sphere:4 settings (Fourier or unmixed spectral, each lambda),8 draws each;
  the two extra spectral rotations are the same law and require no tuning.
- IID:2 lambda settings,16 draws each, no circuit tuning/preparation requirement.

After GLOBAL model-specific selection, run32 FRESH evaluation draws per graph
(two new sampling seeds,16 each) at that fixed policy. Thus every arm uses128
training+128 evaluation=256 total proposals,3840 simulated injected photons per
optical arm. These graphs remain DEV, not held-out. Record own training incumbent
and evaluation incumbent separately; retaining a scored training partition is
legitimate only with all its cost. It never becomes the optical input or a mask.
Primary report includes both chosen-policy fresh evaluation and best total
deployment including paid training. Do not select a new policy after evaluation.

## Population, controls and resource discriminator

Four NEW graphs: N26/K13 ER4902601,RR4902602; N34/K17 ER4903401,RR4903402.
Generation still ERp=.35,RRdegree4,weights1..9. Preserve ALL graphs/seeds/failed
cases. Role namespaces, trial seeds, policy IDs and stopping rules must be fixed
in JSON before executing code. No P49 graph has yet been generated or opened.

Common frontend includes P48 capped anchor, all anchor swaps, signed eigenvector
rounding, top/bottom mu/q columns, labelled max-product assignments and declared
zero/greedy/vacuum-PIT discoveries for ALL four bases. All costs/discoveries are
charged and shared before training. The optical map ignores S0,Cref and every
partition obtained by this frontend. Classical methods may bypass unnecessary
optical preparation; they receive shared Cref freely as a conservative test.

Retain the five declared feasible searches, each its own full score ceiling
(6400/11072 units per N26/N34 graph across the whole train/evaluation campaign).
These legacy units are diagnostic, not an equivalent CPU price or a hardware
advantage. Do not claim a free best-of-five portfolio. Add the independently
authored FAST classical control: vectorized K^2 deltas, incremental swaps,
annealing/multistarts/perturbations, compact traces outside serialization timing.
It receives at least B's observed common-frontend plus training/evaluation
CLASSICAL postprocessing time, excluding optical simulation/backend time.
This grants optical sampling zero latency: failure even in that envelope vetoes
a practical total-resource claim. A nonzero residual allowance is only a
conditional break-even envelope until physical costs/losses are measured.

Primary code must separate count-generation time from PIT/decoder/selection,
and distinguish experimental-spending and deployable-policy ledgers. If using
wall-time measurements to grant the fast baseline a conservative allowance,
state that exactly. Audit overhead and old per-candidate JSON must not inflate
a claim against the fast baseline. A fast-control proposal cap hit BEFORE its
CPU allowance expires makes that comparison inconclusive for accepting a gain.

## Execution and acceptance

New P49 files import immutable P48 helpers; never edit old sources/results.
Freeze code/spec/contracts/tests before numerical work; independent math/code
review followed by targeted preflight. Test G/R unitarity, an exact two-photon
HOM pair, projector invariance, gauge/relabel covariance, null rotations, mean
objective/selection without evaluation leakage, meaningful sphere/IID grids,
resource accounting and independent fast-control deltas/cut reconstruction.

One numerical worker/thread, main CPU60/wall90/output32MiB/planned arrays256MiB.
No automatic retry, graph substitution or successful-subpopulation acceptance.
If resource projection cannot fit, amend BEFORE outcomes rather than silently
truncate. Raw counts, all training/evaluation data, timings and failures survive.
REJECT or INCONCLUSIVE unless a specific reproducible signal merits FOLLOW-UP.
This pilot cannot accept a positive. Confirmation follows the program-alpha,
reserved graphs, independent sampler and total-cost gates in
research/P48_review_future_acceptance.md, with a new candidate namespace.
Only after those gates: update paper/TeX/PDF and GitHub as SIMULATION VALIDATED,
QPU PENDING, then prepare authorized hardware testing. No QPU or manuscript now.
