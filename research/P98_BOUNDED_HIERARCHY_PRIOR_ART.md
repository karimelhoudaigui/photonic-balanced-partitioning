# P98 bounded primary-source attribution: factorial surrogate hierarchy

Checked 2026-11-26. **Moment inversion and low-correlation lossy simulation
have substantial prior art. Attribution of P98's exact combined, worst-case
trace-certified hierarchy remains UNVERIFIED.** This is not a novelty
certificate or a correctness verdict on the independently pending P98 proof.

Target: research/P98_FACTORIAL_SURROGATE_HIERARCHY.md, 160 lines, commit
`8a01023fcf55d06c4f421fe98d72154d4e39ff44`, SHA256
`918d721f33a691351aa0ab2b4618f3fde0101341de87b719d2ecdfea23038c8d`.
Candidate: CF occupied inputs, vacuum loss, known complex transfer T;
C=T†T, c_i=C_ii, mu=Tr C. Taylor-truncate the factorial PGF at total degree s,
obtain a signed mass-one q_s, then normalize its positive part to r_s.
The proposed arrow is TV(P,r_s)<=2^s(s+1)!e_(s+1)(c)<=mu(2mu)^s,
with constructive low-order moments and a rational-bit implementation.
Here Gaussian-rational means T entries in Q(i), not a Gaussian optical source.

## Acquisition and bounded scope

The literature-check/cache instructions were read; P96's Kuna/loss and P94's Seron records were reused before browsing.
Their report hashes are respectively
`c77d5f15332fdd408f073c7e5a9c98b2914079d92678b2625aa92073a9fe8eeb`
and `bf52c6cb6b84bbc2f08cddba818aca48ef0cda840b7c509519cdf95c0dbd0367`.
An initially missed legacy record was identified by ROOT during this check:
LATE2026_LOSS_SOURCE_AUDIT.md, SHA256
`463f6454c63b8315cf2632f2e545abdab1ff4d768d1f8fc7eadc5c107bd613fa`,
and P49_loss_simulation_literature_check.md, SHA256
`f4859a36ae8d0965e85e1301116fe5da84e9afdfda8b9f4f9d0295e45a8fe79a`.
Their relevant passages were read before this freeze; Lim is already known
in the repository, not a new discovery. No literature/records cache directory
exists here/root; their legacy cache paths were unavailable at root. No Python
helper, new PDF/cache retention or local source-byte verification occurred.
Official versioned HTML/abstracts supplied selected theorem/equation/context
extracts, not whole-paper proof audits. New retained external SHA256: NONE.
About 1.0 GiB was free; no large download, checkout or ledger was created.

Strategy A: Brun/Bonferroni/factorial/Janossy truncation and signed-mass repair.
Strategy B: severe/nonuniform photon loss and low-order full-law simulation.
Six English queries: `factorial moment truncation signed probability approximation total variation Brun sieve Janossy`;
`Janossy truncation probability correlation functions approximation`; `Brun sieve total variation factorial probability`;
`positive part renormalization boson sampling signed`; `boson sampling factorial truncation simulation`;
`boson sampling severe nonuniform losses constant mean photon number classical simulation low order correlations`.
Secondary hits were discovery aids only; legacy records were consulted late, explicitly correcting acquisition order.

## S1: established factorial-correlation inversion

Tobias Kuna, Joel L. Lebowitz and Eugene R. Speer, *Realizability of point
processes*, [math-ph/0612075v2](https://arxiv.org/abs/math-ph/0612075v2),
20-Mar-2007; [primary text](https://arxiv.org/html/math-ph/0612075v2),
section 3, equation (3.19): configuration densities are alternating sums
of integrated higher correlation functions, with coefficients (-1)^k/k!.
The surrounding paragraphs explicitly make positivity a separate task.
This is the inclusion-exclusion/Janossy reconstruction underlying q_s:
setting correlations above s to zero gives a signed finite reconstruction.
For P98's bunched mode counts the dictionary uses factorial measures or
distinct auxiliary marks before merging them into modes, retaining all
output factorial divisors. Their simple configurations alone are not PNR.
Overlap: known after translation for inversion; formal corollary not stated
for this finite truncation. Their small-density realization theorem uses
stability/integrability and a higher-correlation ansatz, not Tr C<1/2.
The exact sector-sign V_s error identity and the normalized-positive-part
distance inequality were not extracted from this source. Brun's original
papers and historical priority for that exact remainder were not authenticated.

## S2: established photonic counting characteristic

Benoit Seron, Leonardo Novo, Alex Arkhipov and Nicolas J. Cerf,
*Efficient validation of Boson Sampling from binned photon-number distributions*,
[2212.09643v2](https://arxiv.org/abs/2212.09643v2), 13-Sep-2024;
Quantum 8,1479, DOI10.22331/q-2024-09-19-1479.
[Primary text](https://arxiv.org/html/2212.09643v2), sections 2.1–2.2,
equations (14)–(22), Appendix A: CF Fock counting characteristics are
permanents of occupied-input compressions of U†Lambda U. Section 2.2
explicitly handles general vacuum loss by a unitary dilation/environment bin.
P98's per(I+T†(diag(z)-I)T), and its one-variable total-count version,
are formal polynomial specializations of this ingredient, retaining losses
and collisions. This supports attribution of the PGF, not the surrogate
hierarchy or its TV constant. The paper's efficient constant-bin validation
theorem does not itself assert simulation of every output mode. Overlap:
known after translation for the PGF; partial or adjacent for P98's sampler.

## S3: constant mean under uniform loss was already simulable

Michał Oszmaniec and Daniel J. Brod, *Classical simulation of photonic linear
optics with lost particles*, [1801.06166v1](https://arxiv.org/abs/1801.06166v1),
18-Jan-2018; New J. Phys.20,092002, DOI10.1088/1367-2630/aadfa8.
[Primary text](https://arxiv.org/html/1801.06166v1), section IV.2,
Lemma 1/equation (29), Corollary 3: a particle-separable approximation can
be efficiently sampled, with trace-error upper bound
Delta(eta,K)<=eta^2 K/2+eta(1-eta)/2, hence also an output-TV bound.
Setting eta=mu/K gives an O((mu^2+mu)/K) upper bound for fixed mean mu;
this is our explicit corollary of their bound, not their quoted formula.
Thus a blanket claim that constant-mean full-law classical simulation is new
would be wrong. Their uniform input loss has C=eta I; P98 permits coherent,
nonorthogonal observed columns with arbitrary C and a certified trace budget.
These are distinct hypotheses. Overlap: partial or adjacent for the proposed
combined P98 theorem. No equality of output TV with input trace distance,
or uniform polynomial dependence on requested inverse error, is imported.

## S4: previously recorded low-correlation/clipping prior art

Youngrong Lim, *Boson sampling is fragile to loss*,
[2611.01434v1](https://arxiv.org/abs/2611.01434v1), 1-Nov-2026,
[primary text](https://arxiv.org/html/2611.01434v1); preprint already recorded
above. Theorem 1/equations (3)–(4) states full-PNR simulation
with E_Haar TV<=epsilon and poly_eta(M,K,1/epsilon) cost for fixed
0<eta<1, CF inputs and vacuum ancillas. Sections V.1–V.3 truncate
correlation orders, not total photon number. Appendix D.1 clips signed
estimates then uses finite rejection; D.4 supplies a finite-bit analysis.
Appendix F.1 explicitly restricts accuracy to Haar-average. F.2 allows supplied
output/source profiles bounded by fixed eta_*<1 (source profiles independent of U);
general internal path-dependent losses require additional analysis.
This is strong prior art for the framework, including inverse-error and
bit-cost treatment. Its structured-circuit accuracy is not supplied by the
theorem, so it does not directly prove P98 for arbitrary specified T with
Tr C<1/2. Overlap: partial or adjacent for that exact arrow. Selected source
statements/explanations were authenticated, not the entire 39-page proof.

## Disposition and boundaries

Known ingredients: factorial inversion (S1), permanent PGF (S2), efficient
strong-loss simulation (S3), and low-order signed approximations converted
to samples with controlled error (S4). Exact external attribution remains
unverified for P98's sectorwise L1 identity, the no-extra-factor repair
relative to every true positive P, and their combination with
2^s(s+1)!e_(s+1)(c) under an arbitrary coherent occupied-column trace budget.
That repair claim is not a claim that normalization is globally L1-Lipschitz.
The rational arithmetic/category-table bridge is elementary algorithmic work;
no inspected source was extracted as the exact complete P98 statement.

Any P98 application stays conditional on its separate proof audit and exact
T/access/certificate model. Fixed mu<=rho<1/2 and fixed epsilon imply the
candidate's polynomial dimension cost; inverse-polynomial epsilon gives its
quasi-polynomial construction, not a joint FPTAS. Neither mean efficiency nor
individual column estimates certify independent uniform losses. Rare herald
conditioning, coherent memory, hardware timing and paid setup are separate.
This bounded same-searcher two-strategy check is not exhaustive forward
citation/patent/non-English coverage. Absence is not novelty; priority OPEN.
Only this note was written: no code/import/AST/scientific execution/RNG/graph/
native/test/runner/QPU/paper/push/delegation or P96 proof/contract/raw edit.
