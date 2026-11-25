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

## Active changed bottleneck: P47

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
all six primary controls and four feasible searches remain. Physics is
independently auditing this exact implementation before preflight/main.

Separately, adaptive froze427d984 for an analytic one-mode conditional-phase
control, with a positive-coefficient dynamic program and Fraction-based
independent small fixtures. It models continuous phases or (active_count+1)
roots, not the four-root calibrated control in P46/P47. Qualification is
authorized in the sole numerical slot. It does not change either frozen pilot
or supply an optimization result. At this record no P47 DEV outcomes exist.

Do not rerun a rejected grid unchanged, publish a positive claim, modify the
paper or use QPU credentials. No total-hardware-cost or novelty clearance is
implied by a development observation. Keep all original worker refs; manifests
name pre-run worker commits, not root cherry-picks. Existing602 historical
scientific files and paper bytes must remain unchanged. No arbitrary global
attempt quota; successive new discriminators continue while executable.
