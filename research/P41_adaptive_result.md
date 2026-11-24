# P41/R1 checkpoint — cubic chiral drift has a feasible classical proxy

Base program f09c7ec; pre-execution theory/code/contract commit e664191.
Owner p41_adaptive, isolated branch research/p41-adaptive.

## Exact contribution and status

The proposed changed mechanism used graph-dependent complex hopping phases
to bias adaptive optical proposals. A derived identity isolates a cubic
bosonic exchange current on occupied/occupied/vacant triangles. It can alter
feasible one-swap probabilities while summing to zero at cubic order.

A positive classical feasible sampler reproduces this current. For
|t|||H||<=1/(2sqrt(k)), its repaired-kernel TV error is bounded by

    exp(2k|t|h)(2k|t|h)^4/48 + (9/4)k(|t|h)^4.

Full derivation: [P41_adaptive_chiral_proxy.md](../theory/P41_adaptive_chiral_proxy.md).
**Proof status: derived by this worker, awaiting independent adversarial audit.**
This is a constructive local obstruction to using the leading chiral current
as irreducible optimization benefit. It is not a global no-go, independently
reoptimized benchmark or accepted new theorem. Known time-reversal/chiral
transport is explicitly attributed to Zimboras et al., arXiv:1208.4049v2;
overlap of the full proxy statement has not been exhaustively assessed.

## Finite calculation actually executed

Contract [P41_adaptive_contract.json](P41_adaptive_contract.json), code
[P41_adaptive_probe.py](P41_adaptive_probe.py), retained run
[P41_adaptive_runs/run001/manifest.json](P41_adaptive_runs/run001/manifest.json).
The command is recorded verbatim in the v2 manifest. A bounded external runner
enforced60CPU seconds,90wall seconds and numerical threads1. macOS affinity
is unsupported, so none is claimed. No address-space limit is represented as
a physical array limit; the planned arrays are far below256MiB.

All8 registered frames and72 time cells were retained: weighted complete
graphs m8/k4 and m10/k5, two fresh graph/initial-partition seeds each,
phases0 and pi/3, t0 and signed geometric times .005,.01,.02,.04.
Every photon participates in the dense graph-dependent unitary. The explicit
four-mode triangle serves only as a hand coefficient control.

Reference1 is the project Ryser full-Fock amplitude. Reference2 independently
constructs dGamma(H) with bosonic creation/annihilation coefficients and evolves
its sparse matrix with expm_multiply. Labelled probabilities use a categorical
routing DP, not a column-averaged multinomial. Every collisional outcome is
saved; raw rejection mass is mapped to the current partition for search only.

| Check | Observation |
| --- | --- |
| Population |8 frames,72 cells, no rejected/filtered cases |
| Ryser vs independent Fock amplitudes | max7.00127e-16 |
| Cubic coefficient identity | max1.38778e-17 |
| Classical proxy vs repaired bosonic law | max TV2.03198e-6 |
| Explicit upper bound | max8.24440e-4, informative (<1) for every cell |
| Ratio TV/|t|^4 | max.794266 among nonzero cells |
| Conjugation/time reversal | max recorded probability error0 |
| Relabel covariance | H max6.20634e-17; proxy TV max1.49502e-19 |
| Resource | child wall.83725s; runner wall2.91153s; about6.5MiB raw outputs |

The v2 manifest validates against unchanged before/after inputs and actual
output hashes. The finite outcome is computational verification within1e-10,
not interval certification or a universal theorem inferred from samples.

Expected improvement is evaluated retrospectively using graph cut costs of
the output partitions. No C*, optimum mask or known optimum is constructed,
and there is no optimizer training in this discriminator. These quantities
are diagnostic functionals, not equal-budget discovery outcomes.

The exchange current reverses with time/flux. Selecting that direction after
examining these development outputs would be post hoc. A same-unitary positive
B-vs-D signal in such a direction cannot be accepted as optimization benefit:
the explicit classical proxy captures its leading term. No held-out benchmark
or independently reoptimized D advantage is claimed by this run.

## Disposition and continuation

**KEEP** the cubic identity and classical proxy as candidate mathematical
countercontrols. **REJECT** the inference that leading cubic chiral drift alone
demonstrates useful quantum search. Full research target remains OPEN.

Next decisive obligations: independent proof reconstruction of the proxy and
trace-norm bound; bounded source comparison of this exact statement; and a
changed finite-angle or multi-swap mechanism whose signal survives this proxy
and strong feasible search after all preprocessing/scoring is charged.
No unchanged extra short-time grid is justified. No paper or QPU gate opens.
