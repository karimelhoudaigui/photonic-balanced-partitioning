# P44 encoding lane — exact source audit of the nonuniform-loss moment cap

Date checked: 2026-11-24. Companion argument:
[P44_encoding_moment_cap.md](../theory/P44_encoding_moment_cap.md).
The coordinator supplied the proposed cap before this check. Physics was
assigned a separate reconstruction; this lane does not represent itself as
blind or as the independent physics review.

## Source question and disposition

For distinct observed output modes S, |S|=k, occupied single-photon inputs A
and a pure-loss transfer contraction T, determine whether

    E prod_(i in S)n_i
      =sum_(R subset A, |R|=k)|per T[S,R]|^2
      <=per((T P_A T*)[S,S])
      <=||T[:,A]||_op^(2k)

is justified, and whether its interpretation is established thermal/Gaussian
moment mathematics. **VERDICT: verified for identical photons under the
explicit contract.** The sharp uniform constant follows from established
ingredients; no new permanent or Gaussian identity should be claimed.
The partial-distinguishability extension without a factor is false; a
separate k! bound and an exact physical counterexample are provided.

## S1: permanent Cauchy–Binet — exact first inequality

- **Primary source:** Ulysse Chabaud, Abhinav Deshpande, Saeed Mehraban,
  *Quantum-inspired permanent identities*,
  [arXiv:2208.00327v3](https://arxiv.org/pdf/2208.00327v3), version marker
  10 December 2022. Journal record: Quantum 6, 877 (2022),
  [DOI 10.22331/q-2022-12-19-877](https://doi.org/10.22331/q-2022-12-19-877).
- **Exact locator:** Section 5.3, printed p. 14, Eqs. 58–59 and proof.
  Eq. 10, p. 4, gives the Fock-amplitude normalization.
- **Source content:** Eq. 58 expands a product-matrix permanent over repeated
  intermediate occupations, weighted by inverse occupation factorials.
  Its proof covers arbitrary matrices by unitary embedding, not only unitary
  inputs. The section presents it as an established Cauchy–Binet identity.
- **Translation:** let Y=T[S,A], and specialize the product to YY*. Each
  summand becomes |per Y[:,r]|^2/r!; binary r give the physical sum and
  nonbinary r are nonnegative extra terms. Zero padding handles rectangular Y.
- **Checks:** exact v3 primary PDF opened, title/authors/version authenticated;
  formula and proof read; factorial and rectangular translation checked.
- **Overlap:** **known after translation of notation** for the identity;
  **formal corollary not stated** for the Fock/thermal moment inequality.
- **Retention:** source was browsed, not newly cached or copied into Git;
  no new PDF hash is asserted. The publisher landing-page open timed out;
  its indexed DOI record agrees with the arXiv authors/title/journal data.

## S2: operator-norm permanent bound — exact second inequality

- **Primary source:** Scott Aaronson, Alex Arkhipov, *The Computational
  Complexity of Linear Optics*, [author-hosted PDF](https://www.scottaaronson.com/papers/optics.pdf),
  101-page author version accessed 2026-11-24.
- **Exact locator:** Appendix 12, Lemmas 64–65 and Corollary 66, printed
  pp. 95–96. Corollary 66 bounds |per C| by ||C||_op^k for every complex
  k-by-k matrix C. The proof uses the random-sign identity and norm control.
- **Translation:** C=(T P_A T*)[S,S] is PSD; its permanent is nonnegative by
  S1. Compression gives ||C||<=||T[:,A]||^2. Thus its k-th norm power is
  the desired cap. The companion note gives a self-contained symmetric-tensor
  proof as well, so no unverified external representation result is needed.
- **Checks:** primary statement and proof read. The attempted exact
  arXiv:1011.3245v3 PDF URL returned a cache miss; this record therefore does
  not equate the accessible author PDF to that uninspected version. The
  theorem numbering here belongs specifically to the linked author PDF.
- **Overlap:** **known after translation of notation** for the norm inequality.
  No novelty is asserted for the symmetric-power argument.
- **Retention:** no new author PDF was downloaded/hashed for P44. A previous
  local file labeled arXiv v1 exists but was not silently substituted as v3.

## S3: proper complex Gaussian and permanental Cox moments

- **Primary source:** J. Ben Hough, Manjunath Krishnapur, Yuval Peres,
  Bálint Virág, *Determinantal Processes and Independence*,
  [arXiv:math/0503110v2](https://arxiv.org/pdf/math/0503110v2), 19 May 2006.
  Probability Surveys 3 (2006), 206–229,
  DOI 10.1214/154957806000000078.
- **Exact locator:** Definition 1/Eqs. 1–3, pp. 208–209; Proposition 35,
  Remark 36 and proof, pp. 223–224.
- **Source content:** a Cox process with squared complex-Gaussian intensity
  has permanental joint intensities; the proof applies Wick's formula.
- **Translation:** use independent standard CIRCULAR complex normal z_a,
  F=Xz and covariance B=XX*. For distinct discrete modes S, its joint
  intensity is E prod_i |F_i|^2=per B[S,S]. This is the auxiliary thermal
  moment, not the fixed-N Fock output law. No anomalous/squeezed covariance
  or source-state ordering is supplied by this result.
- **Checks:** both discovery and exact-v2 PDF URLs opened; version/date,
  title/authors and proof authenticated; finite discrete-mode specialization
  and zero pseudo-covariance hypotheses made explicit.
- **Overlap:** **known after translation of notation** for the Gaussian moment.
  Calling the Fock law a permanental process would be **inapplicable**.
- **Retention:** no source cache was created and no new PDF hash is asserted.

## S4: input Fock factorial moments — prior authenticated dependency

- **Primary source:** Monbroussou et al.,
  [arXiv:2607.24728v1](https://arxiv.org/pdf/2607.24728v1), 27 July 2026,
  Appendix C, Eq. C1, printed p. 23.
- **Prior local PDF SHA-256:**
  `4c7d63d1f9c22da4124025bc0d8648143d179f195629a2cc71ad9d49ae4961e9`.
  The exact-version authentication and limitations were recorded in
  `research/P42_encoding_Monbroussou_L1_audit.md`.
- **Translation:** select a degree-k normally ordered output monomial with
  binary output exponents and binary input occupations. Its factors reduce
  to one on distinct input subsets and vanish on repeated annihilations.
  The companion proof also derives this directly from orthogonal residual
  Fock states, including vacuum loss dilation.
- **Disposition:** **formal corollary not stated** for the physical contraction
  version. The previously identified complexity-proof gap in Technique 7
  does not affect this finite moment identity; no summation algorithm is
  inferred from it here.

## Calibration, resources and remaining boundaries

The cap requires a genuine upper bound on ||T[:,A]||^2. Mean throughput,
postselected device shots and the largest single-column transmission are
different quantities. The companion note gives an exact matrix example
separating them and the safe phase-free Frobenius upper bound from the SUM
of occupied-column transmissions. No platform statistic has been promoted
to a calibrated spectral bound.

The graph-search consequence uses raw emission attempts, a fixed support
decoder and target set, fresh product-spatial-Fock preparations, and measured
resource ceilings. Its history-independent uniform control allows classical
adaptation of T and A, but does not equate physical attempts, scored feasible
candidates or wall time. A common frontend's extra classically evaluated
candidates cannot be hidden in the optical support count.

For arbitrary internal states, the note supplies a DIFFERENT Cauchy–Schwarz
argument on permutation operators. It does not extend S1's scalar permanent
interpretation blindly. Its hypothesis is an internal-independent channel
T tensor I, one photon per spatial input and internal-unresolved detection.
The DFT6 direct-sum I2 example proves that the identical eta^k cap can fail
physically under partial distinguishability, even at small uniform loss.

## Search scope and novelty status

Searches used the public English web index on 2026-11-24, with queries for
permanent Cauchy–Binet, Fock/thermal factorial-moment bounds, Gaussian
permanental point processes and normally ordered domination. Primary
versions above were inspected; no global citation-chain exhaustion or
independent second literature search was performed. Exact-ID cache lookups
were read-only and found no Mathbox source cache.

The scalar identities and thermal interpretation are established. The
composed nonuniform-loss benchmark is a **formal corollary not stated** in
these inspected passages, not a new identity or a certified globally novel
no-go theorem. A broader claim of novelty for the adaptive balanced-graph
application requires additional targeted review. No numerical experiment,
QPU validation, manuscript revision or `.mathbox` acceptance is recorded.
