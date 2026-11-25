# Live positive-discovery continuation — 25-Nov-2026

Objective: research/P45_POSITIVE_TARGET.md, positive optimizer ONLY before
held-out/independent replication, paper update and later QPU stage. P44 is
preserved background, not completion. Original source8f83f2b, root branch
research/p45-positive-discovery. No positive acceptance or hardware gate.

## Executed new mechanisms

- P45-B full-Fock stars/bars: source92d542b, completed17.303786s,9 unchanged
  inputs,800 B draws including730 collisions, all feasible. B finds NEW cuts
  below the shared precomputed frontend, but a SINGLE fixed annealing control
  beats it on all four DEV graphs:78/38/96/33 versus B89/47/116/52. Fresh gain
  B87 equals D87; phase109, inclusion105. Nonzero phase is not selected for B.
  Reject this cost-hop generator/budget, not all full-Fock mechanisms. See
  P45_encoding_result.md, original commit2587e2a, immutable experiments/P45_encoding/.
- P45-A count/cavity completion: source19a9902, completed17.36936s,9 unchanged
  inputs. All256 B draws, including194 collisions, decode; ZERO improvements.
  D gain12, phase52, hybrid22, Gaussian37, iid73, species4 gain2. Permuted B
  gain74, explicitly charged extra decoder work (an initial message incorrectly
  added84; the raw audit/result uses74). Every marginal and cut is counted.
  Zero-field decoder's100->96 discovery is common CLASSICAL preprocessing.
  Reject this network/standardization/decoder at the budget. See
  P45_adaptive_result.md, original commitfd9a69f, immutable experiments/P45_adaptive/.
- P45-C analytic: symmetric exactly half-transfer proposals admit a polynomial
  CF-plus-failure orbit sampler for growing block size, not just tiny blocks.
  Original4c1bad2, theory/P45_C_balanced_suppression_attempt.md and blind claim
  card. Root independently read the algebra; fresh full audit still pending.
  No doomed small numerical pilot executed. Arbitrary collision-aware decoding
  is not covered by this particular orbit-sampler claim.

Both new physical pilots have valid completed v2 manifests, separate preflight
and author scalar raw checks. Author checks are not fresh independent physical
replication. Root read code/closure/raw summaries and validated both manifests
after integration. No held-out graph was opened. These are DEV negatives.

## Completed changed bottleneck: P46

Physics derived a spectrum-flat hollow Hamiltonian H=[[0,W],[W*,0]]: H²=I,
U=sqrt(1-p)I-i sqrt(p)H transfers Binomial(K,p) photons exactly, for every W.
This escapes the single Perron mode/weak transfer issue; no constant spectators.
Graph W=polar(F+i zeta J Delta J/||J Delta J||), zeta0/.25, J=I-11*/K,
uses charged swap data and keeps its graph-blind ablation. Orders are fixed
before outcomes, all degenerate cases retained. Extensive transfer or nonzero
phase quartets are physical diagnostics, never an optimization result.

P45-A suggests a separate scaling/discreteness bottleneck: aligned B values
were less useful than their permutation. Proposed P46 decoder uses randomized
MARGINAL probability-integral transforms (PIT) then the same charged completion.
B/D/species PMFs are computable univariately; exact PIT makes each marginal
uniform, preserving the remaining copula. Gaussian uses Phi with a proper
zero-variance branch, iid is uniform. A conditional classical phase sampler
must reproduce the exact old Bernoulli/transfer-subset structure; calibration
of its empirical CDF is approximate and fully charged, not an exact PIT claim.

P46 is now completed and preserved at original source642d9f7; its Gaussian
variance correction b1535f8 preceded all DEV outcomes. Two preflights and
independent exact-code static review b7b64c6 are retained. Main manifest is
completed19.968032s,9 unchanged inputs, all1536 proposals, with256 per model.
Root revalidated that manifest after integration on25-Nov-2026. Total gains
B21,D14,b4=20,Gaussian32,IID19,conditional phase21; independent DEV setting
selection gives B7,D9,Gaussian8. Selected B guide is the graph-blind Fourier
ablation. There is no positive accepted result. Strong baselines and Gaussian
reproduce all best B cut values; no single baseline is claimed to dominate
every graph. See research/P46_bulk_pit_result.md and immutable
experiments/P46_bulk_pit/. These four DEV graphs are not held-out validation.

## Completed changed bottleneck: P47

The prospective graph map now uses a real cost-directed polar step,
W=polar(F-epsilon*(C elementwise F)), C=J Delta J/opnorm(J Delta J),
epsilon=1/(4 max(opnorm(C elementwise F),maxabs(C))). A direct finite-step
proof guarantees nonincrease of the single-swap routing proxy. This is a
classically solvable assignment proxy, not the actual collective cut or an
interference advantage. A realizable strict-local-minimum graph at K4 stalls
exactly despite a better two-swap partition; that counterexample is preserved.
Prime Fourier dimensions K13/17 remove nonzero centered stationary directions
in exact arithmetic, with explicit known Fourier-defect attribution. Weak
signals under the declared numerical threshold are retained as zero branches.

Physics proofs are integrated as theory/P47_cost_directed_polar_step.md and
theory/P47_prime_Fourier_stationarity_review.md. Root read them and the new
network/decoder/accounting code. Adaptive separately reconstructed the finite
bound, prime implication and graph witness before reading the author proof.
Encoding froze695b5d2 before any numerical execution: new DEV graphs n26/34,
ER/RR seeds4702601/02,4703401/02; guide on/off, p=.25/.5, lambda0/1;
All six primary controls and four feasible searches remained. Physics audited
the exact implementation20384ee before execution;13 preflight tests passed,
then the main ran once on original source7a4cd49.

Separately, adaptive froze427d984 for an analytic one-mode conditional-phase
control, with a positive-coefficient dynamic program and Fraction-based
independent small fixtures. It models continuous phases or (active_count+1)
roots, not the four-root calibrated control in P46/P47. Qualification is
completed:24 exact fixtures and12 synthetic N13/17 cases at80/120 digits
passed. Maximum precision difference3.24e-80. This does not change either
frozen pilot or supply an optimization result.

P47 is now a completed DEV negative against the full positive gate. Total
gains B22,D0,b4=9,Gaussian2,IID14,phase9; independently chosen setting gains
B10,D0,b4=4,Gaussian2,IID6,phase6. B best cuts146/35/359/66 against common
Cref154/37/359/66. A SINGLE fixed annealing control achieves146/35/359/49 at
its stated score ceiling: it equals or beats B on all four graphs. The B-D
separation is exploratory and unconfirmed, not a quantum or total-cost gain.
Guided proxies decrease as proved; their squared Frobenius response remains
small, .0368/.00923/.0541/.00866. Raw SHA
aa1386b93104ba1941ebc9d0cdde8488278f86a9bfeb7cd6f0632a83b359d562.
Author audit reconstructs147811 cuts and1536 decoders; this is not independent
resampling. See research/P47_directed_pit_result.md. Integrated suite583 PASS,
reports/P47_validation/; all602 historical scientific files still match.

## Completed changed bottleneck: P48-B

P48 moves the occupied subspace over ALL output vertices: its projection Gram
need not be diagonal on a separate new block. The first heat/Gaussian-frame
card is preserved unchanged at42572d4, but not implemented: conditional on
the subspace its input basis is Haar, making averaged raw counts exactly a
classical spherical-coherent mixture. Own-model PIT prevents extending that
objection to the entire pipeline, yet supplies no compelling mechanism by
itself. See theory/P48_heat_frame_and_classical_controls_review.md.

The NEW graph basis is first K eigenvectors of normalized Laplacian plus fixed
1e-3 diagonal random marks, with a graph-blind Fourier ablation. Source ports
are fixed and do not encode the frontend's incumbent. Marks/order are shared
and carried under labels; gaps/residuals and zero-row cases remain explicit.
This breaks the Haar-basis symmetry, but guarantees no useful cut distribution.
Seven controls include analytic continuous-phase and spherical-coherent
multinomials; five strong feasible searches include direct coherent spectral
rounding. All frontend discoveries/costs are shared before gain is measured.

Frozen card and all unexecuted source snapshots are preserved. Final source
5e06e8f corrected a STATIC pre-run Gaussian zero-variance obligation: an exact
occupied deterministic row also needs independent jitter, to avoid magnifying
tiny factor leakage. Empty/occupied deterministic and mu1-spread cases are
independently tested. Helper6c980d3 is unchanged;52 preflight tests passed
b0231b6. Main completed23.364239s,11 unchanged inputs, all4 graphs and1792
proposals (256 per7 arms), no numerical exclusions, retry or truncation.

P48 also fails the positive gate. Total gains B7,D3,b4=11,Gaussian0,IID12,
continuous phase13,sphere2. B minima168/46/312/56; one fixed anneal baseline
166/39/301/56 equals or beats B on every graph at its declared score ceiling.
Common Cref168/48/315/56; source347->315 on ER34 is PURE GREEDY, not photons,
and73->56 on RR34 is signed spectral rounding. All264 direct preparation
candidates were shared; none improved Cref further. All255 collisional B
observations were retained. Raw SHA
5e423f0f649e58aad5fb21ca5af36f89e6bfdd55d0710258db9b6e05450e5b77.
Author audit reconstructs184080 cuts and1792 decoders plus88 frontend decoders;
this is not independent physical resampling. Original finalaf9f6fd, report
research/P48_spectral_pit_result.md, immutable experiments/P48_spectral_pit/.
Integrated full suite635 PASS, reports/P48_validation/, before any P49 code.

The quarantined P47 post-hoc MILP is also archived: sourceb394a0d/resultb9d252c,
four OLD P47 graphs only, no optimum partitions exported or training use.
Three float64 optimal statuses support saturation by classical controls;
ER34 stopped at5s with dual297/incumbent351 and is unresolved. These are NOT
exact optimality certificates and never feed any P48/P49 graph or parameter.

## Active changed bottleneck: P49

Prospective contract research/P49_TRAINED_SPECTRAL_SOURCE.md, root7b791bf with
phase-convention correctiondc85fa5 BEFORE any P49 execution. New source
V=E R mixes adjacent occupied spectral modes in two explicit Givens layers.
R=I or pi/4 with phase0/pi2; Fourier without mixing is the fourth ablation.
P and mu remain fixed within the spectral family; q and higher correlations
can change. Source gauge is fixed BEFORE R. HOM itself is established physics;
neither this mechanism nor a practical optimization benefit is proven new.

Actual training loss now averages ALL FEASIBLE cuts divided by graph total
weight, not the single-swap proxy or positive-tail gain. Models select separate
policies on128 training proposals;128 fresh evaluation proposals use that
frozen choice on the same DEV graphs. Sphere/IID bypass redundant R tuning.
b4 groups are contiguous source-port blocks for this structured architecture.
Fresh graph seeds4902601/02 and4903401/02; no P49 graph is opened yet.

Encoding implements new P49 files on research/p49-encoding, importing immutable
P48 functions. Adaptive owns an independent fast integer classical solver on
research/p49-fast-classical: incremental swaps, vectorized full scans,
multistarts and compact traces, CPU allowance excluding optical simulation.
Its API card9765ff9 is frozen; source/tests/qualification still pending.
Physics independently audits the Givens/gauge/null and source-code claims.
No P49 numerical worker is authorized yet. Root's635-test slot is released.

Acceptance plan research/P48_review_future_acceptance.md now includes efficient
CPU controls, independent count implementation and reserved graph panels,
program alpha spending, no reused opened panel and no confirmation launched by
that document. Latest user order applies: after held-out AND independent
simulation confirmation, update paper/TeX/PDF/GitHub as QPU PENDING, then prepare
authorized hardware. No positive accepted result, held-out graph or QPU yet.

Do not rerun a rejected grid unchanged, publish an unearned positive claim,
modify the paper before confirmation, or use QPU credentials. No total-cost or novelty clearance is
implied by a development observation. Keep all original worker refs; manifests
name pre-run worker commits, not root cherry-picks. Existing602 historical
scientific files and paper bytes must remain unchanged. No arbitrary global
attempt quota; successive new discriminators continue while executable.
