# P69/P70 bounded primary-source comparison

Checked 2026-11-25, branch `research/p66-dark-barrier`, starting at
`1e2e69d7d64f477482ff05a1586bcdce37504438`. This is a bounded attribution
and applicability check, not a new proof audit or a priority certificate.
The `mathbox:literature-check` skill was applied. Only this report is added.

Conclusion: established permanent/Gaussian and bunching ingredients have
direct overlap. The exact P69 transport composition and the supplied P70
candidate were not located as statements in the three primary versions
below. Their literature priority remains **OPEN**; absence from this search
is not evidence of global novelty. No “apparently new” label is assigned.

## Questions and project claims being compared

P69 source for this comparison is
`research/P69_low_rank_transport_obstruction.md`, SHA256
`37e59633734c16277ed2649c4761fa84a86a8006b164fd4263963e37d7759de4`.
Its independent proofs/reviews remain separate evidence. The source bound
uses a rank-r PSD contraction's permanent, bounded by

    min(1,r(r+1)...(r+L-1)/L^L).

Its target argument uses, for an orthogonal projector P and 0<=s<1,

    per(I+sP) <= det(I-sP)^(-1) = (1-s)^(-rank P).

These are combined with different input/output dark projectors for a NET
unitary with bounded cross rank, a specified L/L CF input and two full-CF
one-block targets. Cayley cross-rank preservation is an additional
block-resolvent ingredient. None of those compositions is attributed to
a paper merely because the paper contains a permanent identity.

P70 is only the candidate supplied by ROOT for this search, not an
accepted proof or a versioned literature result: a randomly selected
occupied/vacant clique-pair bright-mode swap is proposed to give
B_good=(L!/L^L)^2/2, while all common-unitary rank-one D controls are
claimed to satisfy D_good<=2L!/L^(2L). The supplied classical whole-clique
move and rank-L D permutation each give 1/2. Even if the restricted
rank-one comparison is proved, those controls leave the full optimizer
advantage gate failed. This report neither proves those formulas nor
upgrades the candidate's status.

## Three authenticated primary versions

### S1 — PSD Gaussian permanent and the shifted permanent

Alexander Barvinok, *A remark on approximating permanents of positive
definite matrices*, **arXiv:2005.06344v1**, submitted 13 May 2020
(manuscript 12 May). [Version metadata](https://arxiv.org/abs/2005.06344v1),
[primary HTML](https://arxiv.org/html/2005.06344v1),
[versioned PDF](https://arxiv.org/pdf/2005.06344v1).

Exact locators: section 2.1, equation (2.1.1); section 2.3, proof of
Theorem 1.1(1). For standard circular complex Gaussian g and covariance
B=TT*, the paper records per(B)=E product_i |(Tg)_i|^2. It derives
per(I+B)=E product_i(1+|(Tg)_i|^2). The theorem assumes I<=A=I+B<=2I;
the covariance identity applies to PSD B.

Dictionary: B=sP for the target; B=P[S,S] for the source. The source's
PSD Gaussian identity is **known after translation of notation**. Adding
AM-GM and Gaussian radial moments yields P69's rising-factorial estimate;
adding 1+x<=exp(x) and Gaussian integration yields its determinant envelope.
These are **formal corollaries not stated** there. Extraction and these
applications are **verified**; the transport and Cayley results are not
proved there.

### S2 — all particles in a mode subset as a PSD permanent

V. S. Shchesnovich, *Universality of Generalized Bunching and Efficient
Assessment of Boson Sampling*, **arXiv:1509.01561v7**, 15 March 2016;
*Physical Review Letters* **116**, 123601 (2016),
DOI `10.1103/PhysRevLett.116.123601`.
[Version metadata](https://arxiv.org/abs/1509.01561v7),
[primary full text](https://arxiv.org/html/1509.01561v7).

Exact locators: main-text equations (6)–(8), Appendix II equations
(36)–(40). For fixed lossless U, distinct occupied inputs k_alpha and
an output bin K, define H_alpha,beta=sum_{l in K} U_kalpha,l
conjugate(U_kbeta,l). The probabilities that all particles land in K
are per(H) for completely indistinguishable bosons and product H_ii for
independent distinguishable particles. Repeated inputs require the
input-occupation factorial in Appendix equation (38).

Dictionary: transpose its input-row convention to P69's output rows;
N=L for a source-block projection, H=P[S,S], or H the selected crossing
Gram matrix. This formula is **known after translation of notation**;
extraction and this application are **verified**. A bin event includes
collisions and differs from P69's specific full-CF target. No comparison
over separately optimized networks, cross-rank obstruction, or Cayley
result follows. The paper's broader extremality claims are not invoked.
Overall overlap with the complete P69/P70 claims: **partial or adjacent
result only**.

### S3 — full-bunching factorial enhancement at the same network

N. Spagnolo et al., *General rules for bosonic bunching in multimode
interferometers*, **arXiv:1305.3188v2**, 26 September 2013;
*Physical Review Letters* **111**, 130503 (2013),
DOI `10.1103/PhysRevLett.111.130503`.
[Version metadata](https://arxiv.org/abs/1305.3188v2),
[primary full text](https://arxiv.org/html/1305.3188v2).

Exact locator: Theorem 2 and equations (2)–(7), including its proof.
For a lossless m-mode U, n input photons with mode occupations g_k, and
the event that all photons exit mode j, the proved identity is
q_B(j)=[n!/product_k g_k!]q_D(j). The ratio is read where q_D>0;
the multiplicative identity also handles zeros.

Dictionary: n=L, all occupied g_k=1, and equal magnitudes 1/sqrt(L)
in the relevant row give L!/L^L versus L^(-L). The factorial ingredient
is **known after translation of notation**. The inverse-unitary unbunching
probability follows by elementary amplitude reciprocity, a **formal
corollary not stated** here. Extraction/application are **verified**.
This same-U single-mode identity does not prove P70's coherent two-block
product, random-pair factor, or an upper bound over all independently
optimized rank-one D matrices. Overall overlap: **partial or adjacent
result only**.

## Exact arrows these citations do not supply

| Project arrow | Result of this bounded check |
|---|---|
| Gaussian PSD permanent and shifted-permanent representation | Verified ingredient in S1 |
| P69 rising-factorial and determinant envelopes | Formal corollaries of S1 plus the explicitly supplied elementary steps; not located as named bounds |
| Moving IN/OUT dark projectors, two-support CS and uniform NET-rank transport bound | Exact primary match not verified; attribution/priority OPEN |
| Cayley resolvent cross-rank preservation | No exact primary attribution authenticated in this three-source check; the project has a direct Schur-complement proof |
| L! full-bunch enhancement | Verified in S3 for the same U and event |
| P70 all independently optimized rank-one D bound | Not established by S2 or S3; remains a separate project proof obligation |
| Adaptive optimizer, classical controls, runtime or quantum advantage | Not supplied by any cited result |

The Cayley identity is elementary block inversion in the project proof;
failure to locate its precise historical attribution does not make that
matrix-algebra step a novelty claim. Likewise, recognition of Gaussian
or factorial ingredients neither supplies nor disproves priority for
the complete composition. Any originality statement before a paper needs
a separate, wider check.

## Search boundary and retention

Discovery used a general web index, then authenticated arXiv version
metadata and primary full text for the three extracted sources. Search
passes used exact and neighboring vocabulary, including:

- `permanent positive semidefinite matrix rank Gaussian moments bound rising factorial`
- `MacMahon master theorem Gaussian permanent determinant inverse moments`
- `positive semidefinite permanent Gaussian representation rank bound Barvinok permanent vectors`
- `permanent rising factorial rank`
- `bosonic bunching factorial enhancement n! arbitrary interferometer Tichy full bunching probability`
- `Shchesnovich Universality generalized bunching 1509.01561 permanent H equation`
- `low rank bosonic transport permanent`
- `rank one bosonic bunching distinguishable optimized`
- `linear optical rank limited many boson transport Cayley Schur complement`
- `quasiseparable Cayley rank`

These summarize the query families; quoted exact-term variants were also
used. Coverage was English permanent/probability, photonic bunching and
matrix-rank vocabulary available on the date checked. Primary full text,
not discovery snippets, supports S1–S3. S1's backward bibliographic Wick
pointer and S3's fixed-U versus Haar-average distinction were inspected.
The book behind that pointer was not separately extracted or authenticated.
Historical MacMahon and structured-matrix/quasiseparable hits remained
discovery leads, not additional verified theorem evidence. No exhaustive
forward-citation chain, independent bibliographic index, non-English
search or second literature reviewer was completed. The second search
pass was by the same reviewer, so it is not independent corroboration.

The existing P66 literature record was read for context. Read-only
standard-library cache lookups for the three exact arXiv IDs returned
`cache_present:false`; a legacy local filename search found no matching
retained candidate. No PDF, extracted source text, new cache or ledger
record was retained, consistent with authorization to write only this
report. Accordingly there is **no retained-source SHA256** to report.
The versioned URLs above pin the consulted primary editions. An author
PDF dated 20 June 2020 was a discovery candidate for S1; it was not
conflated with the authenticated May arXiv v1 used here.

Only browser research, text reads, metadata/cache lookup and text-integrity
checks were used. The cache helper was read-only and used no scientific
backend. No science code, numerical query/experiment, test, source change,
graph, random draw, manuscript edit or QPU call was run. This record
preserves the distinction between known ingredients, project composition,
candidate P70 formulas and the still-open bounded priority question.
