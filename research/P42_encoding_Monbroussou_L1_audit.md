# P42 — Monbroussou v1 audit for the L1 occupation proposal

Date checked: 2026-11-24. Scope: the source-dependent implication from
arXiv:2607.24728v1 to the CURRENT lossless L1 occupation mean, not a whole-paper
referee report. The new proof is in
[P42_encoding_local_L1_oracle.md](../theory/P42_encoding_local_L1_oracle.md).
No numerical validation, full-output sampling experiment or QPU call was run.

## 1. Authentication and provenance

- **Source:** Léo Monbroussou, Hugo Thomas, Hela Mhiri, Zoë Holmes and Elham
  Kashefi, *Classical simulation and model concentration in passive linear
  optics*, [arXiv:2607.24728v1](https://arxiv.org/pdf/2607.24728v1), 27 July 2026.
- **Version:** v1, 43 PDF pages. Title, authors, version/date marker and relevant
  full text were checked against the primary arXiv PDF response. The arXiv
  HTML request timed out. Relevant model, simulation and appendix sections
  were read; this does not claim every proof of the 43-page paper was audited.
- **Existing local PDF SHA-256:**
  `4c7d63d1f9c22da4124025bc0d8648143d179f195629a2cc71ad9d49ae4961e9`.
  It agrees with the prior record in `research/phase3_density_novelty.md`.
  A newly fetched remote PDF binary was not independently hashed.
- **Existing extracted text SHA-256:**
  `a47ee3e7e75a3f0f5691f8bf51bc7e6cd0fdd2ca4780d615847fddec0dbc25f3`.
  Its local page markers and the arXiv PDF extraction agree on the inspected
  passages. Its null/control characters required treating it as text explicitly.
- **Cache:** a read-only exact-ID Mathbox cache query returned no cache.
  The already existing temporary PDF/text were read; no permanent source
  cache, tracked full text or new `.mathbox` evidence entry was created.

The prior project source record concerned output-law TV bounds. Its verdict
does not answer the new L1 objective question. This check therefore adds a
new application rather than overwriting that earlier record.

## 2. Exact source locators

| Result | Locator, using PRINTED pages | Extracted contract |
|---|---|---|
| Technique 1 | Section IV, p. 8; Proposition 1, p. 8 | Efficiently constructible shared polynomial-dimensional irrep support permits exact arbitrary-U evaluation. |
| Technique 2 | pp. 9; Eqs. 30–34 | Truncation gives Haar mean-square error; Eq. 33 measures error relative to landscape standard deviation. |
| Technique 3 | p. 9 | Product input; controlled local observable norm and reduced purity; worst-case additive approximation. |
| Technique 4 | pp. 9–10, Eq. 35 | Product-state transition amplitudes and passive-phase expectations admit additive approximation. |
| Technique 5 | p. 10, Eqs. 36–38 | Exact monomial regimes: constant degree, constant input occupation support, constant locality, or both degree/support logarithmic. |
| Supporting expansion | Appendix C, pp. 23–24, Eq. C1, Proposition 10, Techniques 6–7 | The summand count and permanent rank are separate complexity quantities. |
| Nonlocal lead | Section V.B.4, Eq. 48; Appendix G, Lemma 5, Eqs. G8–G13 | Collective quadratic number-phase readouts can have growing Fourier weight; no optimization benefit is proved. |

The source's photon count n corresponds to our K. Its monomial/irrep k
does not. Its asymptotic setup uses m=ceil(2.1n); the separate algebraic
application below is proved directly for m=2K. These distinctions prevent
an unsupported translation of concentration statements.

## 3. Application to the current project: verdicts

**VERIFIED by an explicit project bridge:** every term |n_i-n_j| depends on
two modes. At fixed total K its local support has (K+1)(K+2)/2 occupations,
and its squared Hilbert–Schmidt norm is at most

    K^2 (K+1)(K+2)/2.

One can set it to zero outside local total occupation <=K without changing
the physical expectation. Thus the apparent nonsmooth nonlinearity is not
an extensive-mode observable. The sum over graph edges, and R_K's sum over
all pairs, contains only polynomially many such terms. Polynomially bounded
weights and lambda preserve a polynomial additive oracle; rescaling them
must rescale the requested accuracy and shot noise too.

Technique 3 is an appropriate pointer, but no efficient phase-space sampling
assumption for an arbitrary supplied local matrix should be smuggled into
the argument. The checked underlying source, Lim–Oh
[arXiv:2502.12882v1](https://arxiv.org/pdf/2502.12882v1), 18 February 2025,
*Efficient classical algorithms for linear optical circuits*, assumes product
operators in its setup. A two-mode |n_i-n_j| operator is not itself a product.
It does have an explicit polynomial sum of joint-number projectors; more
directly, the Fourier construction in the companion proof invokes the
phase-amplitude route and has a complete bounded estimator. Hence the
present implication does not rely on an unchecked generalization of
Technique 3.

For the ACTUAL distinct-single-photon source, the companion proof derives

    E[z^ni w^nj]=per[I_K+(z-1)aa*+(w-1)bb*],
    a_alpha=conj(U_i,alpha), b_alpha=conj(U_j,alpha).

A finite-rank coefficient DP evaluates all two-mode probabilities using
O(K^4) arithmetic per pair. Summing over pairs gives E F_G, E R_K and E J_G
exactly in the arithmetic model. Its coefficient normalization is explicit:

    [x^r y^s]E[(1+x)^ni(1+y)^nj]=r!s!d_(r,s,r,s),
    E[(ni)_r(nj)_s]=(r!s!)^2d_(r,s,r,s).

This is an exact polynomial oracle for the MEAN, not an efficient minimizer
of that mean or the underlying balanced-cut problem. Exact bit computation
is verified only with controlled rational/algebraic representations. A
floating-point implementation with alternating inversion requires stability
checks; generic double inputs do not make its numerical answer exact.

**Independent primary cross-check:** Aaronson–Arkhipov,
[author PDF](https://www.scottaaronson.com/papers/optics.pdf), Appendix 12,
Lemma 68 and Theorem 69, printed pp. 97–98, Eqs. 465–468, gives the established
fixed-mode marginal framework with n^{O(d)} scaling for d observed modes.
The author PDF is not asserted byte-identical to a particular arXiv version.
The displayed proof there invokes a Gurvits lemma; the explicit companion
DP removes that dependency for d=2 and this project's source. Overlap label:
**formal corollary not stated** for the particular graph L1 regularizer.

## 4. Source caution: a rank bound is not a summation algorithm

Appendix C's Technique 7 ends after a bound on individual permanent rank.
For K occupied single-photon inputs and degree d, Eq. C1 still contains
binom(K,d) summands. Low permanent rank alone does not make their direct
enumeration polynomial. Accordingly this audit does not certify that
displayed proof as a sufficient justification for constant-locality case
5(iii). This is a missing bridge in the displayed argument, not a
counterexample to the statement. The aggregate DP supplies the bridge for
the two-mode diagonal observables and input class needed here.

## 5. Additive, relative, exact and sampling are different claims

For a cost scale A=sum_(i<j)(w_ij+lambda), the companion Fourier estimator
has range length O(AK) and uses O((AK/delta)^2 log(1/zeta)) draws for additive
error delta with failure probability zeta. A phase draw uses O(K) arithmetic
for the distinct-input source. Circuit construction, pair/Fourier sampling
tables, precision and optimization calls remain charged.

An inverse-polynomial additive tolerance therefore remains polynomial for
polynomial cost scales. Relative error in an exponentially small quantity
or resolving exponentially small differences is not obtained at constant
cost. The source's Eq. 33 signal-relative Haar RMS criterion is also not a
multiplicative approximation to every fixed-circuit cost or rare-event
probability. A small mean-square truncation error under Haar does not
certify a graph-trained finite-angle circuit selected adversarially.

The exact DP has a constant exponent only because the observed mode count
is fixed at two. Growing photon count alone does not break it. A collective
observable supported on d growing modes generally incurs K^{O(d)} tables,
and a Fourier expansion needs bounded TOTAL coefficient weight, not merely
polynomially many written terms.

Neither a fixed-mode marginal oracle nor an additive amplitude estimator
generates the full joint Fock law. They do not establish equal realized
query costs, equal wall time, domination by distinguishable photons, or a
classical feasible-search advantage. They do establish that training the
L1 MEAN is not an unprovided hard quantum subroutine.

## 6. Remaining optimum-blind physical target

The first clean discriminator is to optimize the GLOBAL improvement event

    Pr[CF and C_G(support n)<C_G(S0)],

where S0 is a charged scored incumbent, rather than optimize E J alone.
The event is measured from full photon output, counts collisions as failures,
and uses no C* or optimal-state mask. It is not a two-mode additive utility;
the companion proof explains why the local oracle does not evaluate it.
This is a precisely identified uncovered target, not a hardness or novelty
claim. Low-transmission P42 domination, strong classical feasible search,
independently optimized distinguishable photons, held-out graphs and matched
total costs still need to be defeated. If the per-attempt improvement event
is exponentially rare, calling the readout global does not make it useful.

A second route would physically alternate passive mixing with genuine
graph-dependent nonlinear occupation phases. Such a device leaves the
single-passive-U model; sample postprocessing alone does not. Ancilla source,
heralding, discarded attempts, feedforward and available gates need a full
resource contract before treating it as feasible on Quandela hardware.
No such implementation or positive result is asserted in this audit.

## 7. Disposition and coverage boundary

**Verified:** primary version authenticated; simulation passages and relevant
appendix text extracted; notation translated; explicit bridge to the actual
L1 source/observable proved. **Conditional:** numerical stability, practical
resource comparison and any broader-input exact statement. **Inapplicable:**
using the mean oracle result as a full-output sampler, a global optimization
solver or a universal no-go for every graph-dependent photonic mechanism.

The overlap is known fixed-mode marginal algebra applied to this objective.
No novelty claim is made for that oracle. The search was a source-directed
audit of the exact Monbroussou v1 plus its Lim–Oh dependency and the
Aaronson–Arkhipov marginal framework; it was not a new global literature
review. Relevant examples elsewhere in the source do not prove a positive
optimization mechanism for this project.

Checks performed here were analytic/source checks and Git whitespace/status
checks. No test-suite run, numerical corroboration, manuscript revision,
source-cache installation or QPU access was performed by this lane.
