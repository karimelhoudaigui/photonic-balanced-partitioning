# P94 bounded primary-source check: parity mean oracle

Checked2026-11-26. **The random-sign estimator is established, and its use
for photonic counting characteristics has direct prior art.** A parity-based
graph-cost mean is a formal application, not a new permanent identity or a
verified full-law sampler. No blanket novelty or optimizer advantage follows.
This is source verification/translation, not an audit of another P94 proof.

## Scope and provenance

The literature-check skill and cache/source-record instructions were read.
Read-only checks found no .research-cache/literature/records at project root
or this worktree. Existing P41/P43 source notes and the P90 literature note
were consulted before browsing. The P90 note SHA256 is
`fa1c2be4a2b148450653207befe4cd4647dfef10f1147b0d1b03ce978a94e831`;
P41 sources `cb9d5ea1e0e3390737682283fbb13e25abe3dd807ae900159dc25b8aedcdb934`;
P43 review `b970dc9d876b783dd7b67d044522b003a44da23a58a2c58d6af67baea50a21ee`.
Only the three publications below were substantively checked, via official
versioned arXiv HTML/abstracts and the publisher's bibliographic page.
Retained external-source SHA256:NONE; selected online extraction available,
no full PDF retained or locally byte-authenticated. No cache, checkout,
research-state ledger or second report was created. Disk showed about1.2GiB
free; no large download or scientific allocation was attempted.

## S1: exact complex-matrix estimator and norm bound

Scott Aaronson and **Travis Hance**, *Generalizing and Derandomizing Gurvits's
Approximation Algorithm for the Permanent*, arXiv:1212.0025v2,
4-Dec-2012. [Version record](https://arxiv.org/abs/1212.0025v2);
[primary text](https://arxiv.org/html/1212.0025v2), section2,
equations(20)–(27), Proposition1, and the paragraph after equation(28).
The paper proves the following for complex square A, k>=1, with operator
2-norm; neither nonnegative entries nor unitarity is required:

    Z_A(x)=(product_i x_i) product_i(Ax)_i,
    x uniform in {-1,+1}^k;
    E Z_A=per(A),       |Z_A|<=||A||^k.

Equations(22) and(25)–(27) supply the sign-expansion and AM-GM/operator-norm
arguments. For a contraction the bound is1. Averaging gives additive error
epsilon at fixed high confidence in O(k^2/epsilon^2) arithmetic operations;
confidence amplification adds the usual log(1/delta) factor. This estimates
per(A), not its modulus squared, and is not a photon-output draw.
Authentication/extraction/application:verified. Overlap:known verbatim.
The authors credit Gurvits's2005 mixed-discriminant algorithm and Glynn's2010
formula. Those originals were not independently retrieved here; historical
priority is reported through this explicit primary proof, not reinvented.

## S2: photonic counting-characteristic oracle already using Gurvits

Benoit Seron, Leonardo Novo, Alex Arkhipov and Nicolas J. Cerf,
*Efficient validation of Boson Sampling from binned photon-number
distributions*, arXiv:2212.09643v2,13-Sep-2024; Quantum8,1479,
19-Sep-2024, DOI10.22331/q-2024-09-19-1479.
[Version](https://arxiv.org/abs/2212.09643v2),
[primary text](https://arxiv.org/html/2212.09643v2),
[publisher](https://quantum-journal.org/papers/q-2024-09-19-1479/).
Section2.1 equations(4),(14)–(20) express the characteristic function as
per(V_n), V=U-dagger Lambda U, for indistinguishable single photons in
distinct occupied inputs. Section2.3 explicitly invokes Gurvits; equation(31)
gives the contraction bound. AppendixA supplies the characteristic derivation.
Theorem1 concerns approximate distributions for a CONSTANT number of bins;
it must not be promoted to polynomial simulation of all output modes.

Dictionary: relabel occupied inputs, let T=U[:,occupied] in output-row/input-
column convention, T-dagger T=I, and P_A project onto any output subset A.
Taking phase pi on A and zero elsewhere specializes their formula to

    chi_A(n)=(-1)^(sum_{j in A} n_j),
    E chi_A=per(M_A),   M_A=I-2 T-dagger P_A T,   ||M_A||<=1.

This is the UNCONDITIONED full PNR expectation: collisions remain included,
with no collision-free denominator. Authentication/extraction:verified;
parity specialization:verified, known after translation of notation.
The paper already connects these Fourier observables to additive classical
estimation; parity is not a newly discovered escape from that connection.

## S3: prior parity decoding and photonic optimization

Kamil Brádler and Hugo Wallner, *Certain properties and applications of
shallow bosonic circuits*, arXiv:2112.09766v1,17-Dec-2021.
[Version](https://arxiv.org/abs/2112.09766v1),
[primary text](https://arxiv.org/html/2112.09766v1): section2.2 equation(1)
maps occupation parity to bits; section2.3, Algorithm1 and equations(2)–(4)
use the decoded mean energy for circuit feedback and retain best sampled
configurations. This verifies prior Fock/parity/cost-feedback optimization.
It does not by itself supply this project's graph-balanced decoder or a
Gurvits replacement for finding its best configuration. Overlap:known after
translation for the framework; partial or adjacent result only for that
specific decoder/optimizer. No whole-paper correctness audit is claimed.

## Application boundary and strongest classical control

For spins s_v=sign_v chi_{A_v}, the character product uses symmetric
difference: s_u s_v=sign_u sign_v chi_{A_u triangle A_v}. Thus a quadratic
cut mean, or a supplied sparse character expansion, is an affine sum of S2
permanents to which S1 applies (take Re Z for these real means).
Overlap:formal corollary not stated in the
checked optimizer passages. This source-supported translation is a strong
classical MEAN oracle, even when the compressed matrix has large rank.
Exact balance of a proposed decoder is a separate premise, not implied by
ordinary parity bits. Formation/access to T, compilation, graph preparation,
precision, RNG and all oracle evaluations still have to be paid.

For coefficient sum W=sum|c_l|, additive errors scale with W; a polynomial
normalized mean-oracle bound needs controlled coefficient mass and a sparse
or efficiently sampleable expansion. Arbitrary nonlinear repair/quenching,
rare-event conditioning, best-of-shot utility, relative gaps and adaptive
search trajectories are not automatically covered. Replacing M_A by an
arbitrary nonisometric T-dagger D T also loses the displayed leading I unless
the physical loss/dilation model is supplied. Finite-bit and matched wall/
hardware-cost guarantees require their own contracts. Signed/complex draws
are not a normalized sampler for decoded solutions or full Fock outcomes.

Search scope: five initial English discovery queries on Gurvits/Rademacher, parity
photonic optimization and binned characteristics, followed by the three
primary versions above and their selected backward references. The same
searcher performed both strategies; no independent second search, exhaustive
forward-citation, patent or non-English survey. Failed phrase searches prove
no novelty. The exact proposed balanced-decoder composition remains priority
unverified; the basic mean-oracle obstruction has clear prior ingredients.
No code/import/AST/test, RNG, graph, native query, model, runner, QPU,
manuscript or modification of existing P90 inputs/raws occurred here.
The positive optimizer goal remains OPEN.
