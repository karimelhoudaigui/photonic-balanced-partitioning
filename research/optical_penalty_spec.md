# Authenticated optical penalty references

Base: `99f82e367ef079e4d52f763d615476698727b739`. Checked 2026-11-20.
This document specifies references and audits their translation to minimum
bisection. It does not claim a competitor has been reimplemented or run.
No downloaded external program was executed and no QPU was contacted.

## Source identity and exact extraction

ObliQ paper: Ranjan et al., PACM MACS 9(3), Article 58 (2025),
[DOI 10.1145/3771573](https://doi.org/10.1145/3771573).
The [Rice author-repository PDF](https://repository.rice.edu/server/api/core/bitstreams/0c308cfa-0cac-4b03-ba49-9effdba0799b/content)
was downloaded and read in full relevant sections: 3, 4.1–4.4 and 5.
SHA256 `61f3fb1f26a9553845b75d0fc7b6e973c28d30cc06c1c7e730c108a3d7a2da86`;
25 pages. Its implementation link identifies the original Zenodo deposit.
The authenticated versioned artifact is
[Zenodo 17343439](https://zenodo.org/records/17343439), `ObliQ.zip`,
SHA256 `8e5afe41c4d19c92b6a6aa1797b5b8391061cf6978216c9f9affad5e755fb948`.
Files were inspected as text, never imported. The archive's requirements pin
Perceval 0.11.0, whereas the paper describes 0.10.4. The
[Perceval v0.11.0 BS implementation](https://raw.githubusercontent.com/Quandela/Perceval/v0.11.0/perceval/components/unitary_components.py)
was independently downloaded, SHA256
`d7d4a187fea8daf4a53008dd0e87b8f33264d3cb8dc41d24790044ef2d8bf554`.
PDF extraction used isolated `/tmp` installation `pypdf==6.4.0`; shared
project dependencies were not changed. Sources currently remain in `/tmp`,
not a portable repository cache.

BBS reference: Makarovskiy et al.,
[arXiv:2510.08274v1](https://arxiv.org/html/2510.08274v1), 2025-10-09,
Algorithm 1, Sec. II.1, III.1, IV and Appendix B. Those primary full-text
sections were read. No original BBS code artifact was located or audited.

## What the original ObliQ artifact actually defines

Static and baseline VQC inputs are `N=m` photons, one per mode. Hybrid training
uses the anchor's selected binary string as its new occupied input modes,
so its photon count is variable. Readout is threshold `x_i=1[t_i>=1]`.
The loss is the original QUBO expectation over threshold patterns. The static
circuit min–max normalizes the matrix, repeats all unordered pairs `R=10`
times by default, and uses API parameter
`beta_ij=(1/2)acos(sqrt(1-A_ij/R^2))`. Nonadjacent pairs are routed by
permutations. The variational tail has `8m-6` parameters: two passes, each
with `m` phases, `m-1` forward beamsplitters, `m` phases and `m-2` backward
beamsplitters. Final decoding tests marginal-click-ranked prefixes and a modal
pattern. The paper includes the empty prefix; the archive omits it. Its
training uses two shifted circuits per parameter and Adam; anchor search is
an additional sampled stage. These mechanics are sourced from the original
artifact, not a generic class bearing the same name.

### Independently derived audit: reachable space

For a lossless passive circuit with `N>0` photons and threshold detection,
every raw output has Hamming weight

\[
1\le |x|\le\min(N,m).
\]

Thus `N=k` cannot explore all binary strings. Weight-`k` feasibility then is
exactly the collision-free event. For `N=m`, collisions can produce all
nonzero support sizes; the empty string is impossible without losses or
classical postprocessing. A generic fixed `U` need not assign nonzero mass
to every nonzero bitstring, so even this statement is a domain allowance,
not a full-support guarantee for each circuit. Prefix decoding can return
strings never physically sampled; they must be counted as classical proposals.

The hybrid's anchor changes `N`, not just the continuous circuit parameters.
A fair ablation must freeze and report the chosen source pattern and the
cost of finding it. Fixed `N=k` substituted for the original `N=m` static
input is a different algorithm.

### Independently derived audit: beamsplitter convention mismatch

The artifact API's default Rx beamsplitter has diagonal `cos(beta/2)` and
off-diagonal `i sin(beta/2)`. For input `|1,1>`, its coincidence probability
is `cos^2(beta)`. The paper's derivation instead writes a mixing angle
`theta` with `cos(theta),sin(theta)`, giving `cos^2(2theta)`.
Consequently, for a single pair with normalized coupling `a` and `R=1`,

\[
P_{11}^{\rm archive}=\cos^2\left(\tfrac12\arccos\sqrt{1-a}\right)
=\tfrac12(1+\sqrt{1-a}),
\]

whereas the paper's intended local identity is `P_11=1-a`.
For `a=1`, these are respectively `1/2` and `0`. To realize the stated local
identity in this API, use `beta=acos(sqrt(1-a))`, twice the archive parameter.
This discrepancy is exact and does not depend on a simulator implementation.
The installed Perceval 1.3.0 has the same half-angle convention; only its
local BS matrix was inspected, without using any remote processor.

Keep a literal-archive reproduction and an explicitly corrected-physics
variant separate. Do not silently repair the reference and present its
results as the original implementation. The paper's incremental-kernel
description also does not uniquely fix whether to scale the physical angle
by `1/R` or substitute `a/R^2`; the archive is the unambiguous executable
definition for that choice. Its unordered pair set should be serialized
before reproduction rather than assumed identical across runtimes.

### Independently derived audit: bisection matrix and normalization

For nonnegative undirected edge weights, let `d_i=sum_j w_ij`, absent edges
have `w_ij=0`, and use the symmetric QUBO convention `x^T Q x`. Then

\[
C_G(x)+\lambda(|x|-k)^2
=x^TQ_\lambda x+\lambda k^2,
\quad (Q_\lambda)_{ii}=d_i+\lambda(1-2k),
\quad (Q_\lambda)_{ij}=\lambda-w_{ij}\ (i\ne j).
\]

The factor two from off-diagonal entries of `x^TQx` is essential.
On irregular weighted graphs the diagonal is nonconstant. Such instances
fall outside the constant/zero-diagonal anchor class stated by the paper.
Applying its off-diagonal construction anyway is an **extension heuristic**,
not authenticated support for a general minimum-bisection benchmark.

Global entrywise min–max normalization obeys

\[
x^T\!\left(\frac{Q-q_{\min}J}{q_{\max}-q_{\min}}\right)x
=\frac{x^TQx-q_{\min}|x|^2}{q_{\max}-q_{\min}}.
\]

It preserves fixed-weight ranking but generally changes ranking across
weights. The original loss uses `Q`, so a faithful implementation retains
that loss rather than optimizing its min–max transformed version.
The large-penalty optical washout question is derived in
`theory/phase2_candidates.md`; it is distinct from this objective correction.

### Physical resource accounting required by the translation

Each lossless raw shot of static ObliQ consumes `m` injected photons;
fixed-particle bisection consumes `k=m/2`. Equal shots therefore do not
mean equal photon budget. With transmission `eta`, an all-photon detection
gate costs an additional factor `eta^N`; accepting threshold strings of
weight `k` after losses is a different acceptance rule and includes several
survivor sectors. The artifact sets a minimum detected-photon filter of one.
Its returned distribution under loss can therefore condition away empty
attempts; restore their physical frequency before comparing success rates.

For `P=8m-6` trainable parameters, `T` updates and `S` attempts per circuit,
the gradient/forward design costs approximately `TS(2P+1)` raw attempts,
plus anchor and final-test stages. Count actual completed evaluations,
cached-cost hits, prefix proposals, optimizer work and photons `N` separately.
This formula counts attempts, not a package's postselected sample count.
The source's two-shift formula is approximate; do not label it an exact
multiphonon gradient rule merely because it is called parameter shift.

## BBS: a genuinely full binary optical-plus-classical reference

The verified primary specification uses `N=m/2` alternating single-photon
inputs, threshold readout, then independent flips with probabilities
`f_i=sigmoid(alpha_i)`. Optical parameters start uniformly in `[0,2pi)` and
`f_i=1/2`. The expected supplied cost trains both sets by SGD; the simulator
benchmarks use 200 updates, 50 samples, learning rates 0.01 and 0.05, and
delay lengths 1,3,9. Raw samples are reused for flip-gradient evaluations.
The paper's general optical shift is a first-order approximation, not an
exact universal two-shift formula. Missing small-mode delay layers must be
omitted explicitly. No exact numerical shift magnitude was authenticated.

### Independent mathematical translation and checks

For threshold pattern `y`, the final output law is

\[
P_{\theta,\alpha}(x)
=\sum_y p_\theta(y)
\prod_i f_i^{x_i\oplus y_i}(1-f_i)^{1-(x_i\oplus y_i)}.
\]

When all `0<f_i<1`, every binary `x` has positive probability, irrespective
of photon count or collisions. At `f_i=1/2`, it is exactly uniform and
independent of the optical circuit, so the exact optical gradient is zero
at initialization. This forces a flip-only ablation to identify useful
photonic training. A circuit receiving a generic penalty cost is a proper
penalty reference; a classical Bernoulli model alone is not BBS.

Let `P=sum_(ell in delays, ell<m)(m-ell)`. For the untiled single-device
algorithm, `T` updates use `TS(2P+1)` optical attempts and at most
`TS(2P+2m+1)` classical cost calls, before optional caching, plus any extra
validation stages. Reused flip-gradient proposals add classical evaluations
without additional optical shots. These counters follow Algorithm 1 and
Appendix B, and should be measured rather than inferred from optimizer
iterations. All gradient-generated candidates enter its best-found solution.

## Minimal reproduction acceptance conditions

| Check | Required interpretation |
|---|---|
| Photon source state | Save exact occupations and source changes, including anchor discovery cost. |
| BS convention | Test the `|1,1>` single-pair coincidence before larger circuits. |
| QUBO convention | Exhaustively match direct penalty energies for all `2^m` strings at small m. |
| Decoder support | Test threshold versus threshold-plus-flips; never claim raw threshold has unrestricted support at N=k. |
| Distribution denominator | Retain empty/lost/colliding attempts in physical success accounting. |
| Comparison labels | Distinguish literal archive, corrected-physics extension, BBS-style mesh adaptation and authenticated original architecture. |
| Classical work | Charge ranked prefixes, flips, oracle evaluations, hyperparameter selection and classical initialization. |

No QPU preparation gate is passed merely by having this specification.
