> Retained reviewer draft, not a final returned review. The reviewer turn was
> quota-interrupted before committing this packet. The coordinator preserved
> the draft from `phase3-linear-leakage-sources`, original SHA256
> `86f64900c4c918bbd05a1d5b2fcf6db1dfeb81211dfb5e00ae4e689eaa6be3b5`, and corrected one obvious `+identifies` typo.
> Source-extraction provenance remains the reviewer's; the general P36
> implication remains unverified. No absent source is novelty evidence.

# P36: exact linear leakage bound, targeted source check

Checked 2026-11-22, approximately 02:24 UTC, using `mathbox:literature-check`.
Isolated base `de77a1404cbab6f98d3187bad4ab42b772789f29`, branch
`research/phase3-linear-leakage-sources`. Only this report is changed.
This is a bounded external-source and implication review. It does not
certify the proposed inequality or replace the separate proof/counterexample
and numerical routes.

## Contract and current verdict

Let V be any m-by-k complex orthonormal frame. A lossless passive circuit
receives one indistinguishable photon in each of the k distinct occupied
inputs. Let p_b be its complete Fock output law, and p_d the law of k
independent categorical draws through the same occupied columns, with labels
forgotten. Set

    q_ia=|V_ia|²,     a_i=sum_a q_ia,
    delta=sum_i(a_i-max_a q_ia).

The question is the exact, finite, uniform statement

    TV(p_b,p_d) <= min(1,delta),         TV=||p_b-p_d||_1/2.

No collision-free conditioning, loss postselection, ensemble average,
minimum intensity floor, locality assumption or internal distinguishability
parameter is included. Delta>=1 is trivial; the unresolved part is
0<delta<1 for general k>=3. For k=1 the laws agree. A restricted k=2
reduction is given below.

**Source verdict: UNVERIFIED for the general exact statement.** The checked
primary sources below establish relevant but different bounds. No source
theorem or authenticated source counterexample settling the displayed
inequality was extracted. This does not imply that the inequality is true,
unknown to the field, or novel. Searches cannot decide its mathematical
validity by absence of a match.

The source question was communicated to the separate physics reviewer with
the full-Fock, same-frame and distinct-input quantifiers. Their evolving
investigation is not used as external evidence here.

## Why the preceding Gram certificate does not establish P36

The previous target, `theory/phase3_density_certificate.md`, SHA256
`7b2bee10ab5a738dfdcd16d657409be5eebdf7745b19a0bba91aace62a13e61c`,
gives TV<=f(rho(delta)) on its convergent branch, with

    rho(x)=2sqrt(x)+x,
    f(s)=(exp(-s)/(1-s)-1)/2,       0<=s<1.

For s>=0, -s-log(1-s)>=s²/2 and exp(t)-1>=t. Consequently

    f(rho(delta)) >= rho(delta)²/4
                  = delta+delta^(3/2)+delta²/4 > delta

whenever delta>0 and rho(delta)<1. Thus the scalar envelope itself is
strictly larger than the proposed linear bound. An asymptotically linear
upper envelope does not remove the positive higher-order terms. This
calculation rejects that deduction, not P36.

## D: many-particle which-way information and label dephasing

Christoph Dittel, Gabriel Dufour, Gregor Weihs, Andreas Buchleitner,
*Wave-particle duality of many-body quantum states*, Phys. Rev. X 11,
031041 (2021), DOI
[10.1103/PhysRevX.11.031041](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.11.031041).
Checked [arXiv:1901.02810v3](https://arxiv.org/abs/1901.02810v3),
2021-08-24, 24-page PDF: §III.B, (27)–(29), and §IV.B–C, (60)–(65),
pp. 11–12. Their classical Kolmogorov distance includes the factor 1/2.

For R distinct particle assignments, they describe the ideal bosonic
external state as a uniform pure superposition and the distinguishable
external state as the maximally mixed assignment state. Equation (60) identifies trace distance to the ideal state with one minus squared
fidelity; (61) bounds measured distance, and (63)/(65) normalize the
distance to fully distinguishable particles. They explicitly obtain
TV<=1-1/R for the two extreme cases. **Verified extraction and application**:
our distinct-input contract has R=k!. This is a **partial or adjacent result
only** for P36.

The source's distinguishability measures concern unresolved internal
degrees of freedom. They are not the output-position MAP error derived
from q_ia. No replacement of those measures by delta is stated here.

### A precise obstruction to the global trace-distance shortcut

The following is an explicit translation of D, not a counterexample to P36.
Let the orthogonal product vectors |pi> enumerate the k! permutations of
the occupied distinct orbitals. Put

    |s>=(1/sqrt(k!)) sum_pi |pi>,
    rho_b=|s><s|,                rho_d=(1/k!)sum_pi |pi><pi|.

Their trace distance is 1-1/k! and is invariant under the common evolution
U^(tensor k). At U=I, delta=0 and the measured occupation laws coincide,
but the trace distance remains positive for k>=2. Hence the assertion

    trace-distance(rho_b,rho_d) <= delta

is false. Contractivity of measurement gives an upper bound in the wrong
direction for repairing this failure. A proof of P36 would need to exploit
the particular output-position occupation measurement, rather than bound
the full state distance by delta.

## S: a genuinely linear mixture-weight bound uses a different weight

Valery S. Shchesnovich, *Tight bound on trace distance between a realistic
device with partially indistinguishable bosons and the ideal Boson
Sampling*, [arXiv:1501.00850v4](https://arxiv.org/abs/1501.00850v4),
2015-05-21, eight-page PDF. **Theorem 1**, §II.B, p. 4, equations (12),
(13), (20), proves

    TV(p_ideal,p_partial) <= 1-p_s,
    J=p_s|s><s|+(1-p_s)J_perp.

Here p_s is the probability weight of the symmetric **internal** input
state; the exact convex decomposition removes cross terms. The source
allows identical nonideal detectors and conditions on detecting all
photons. Specialize to ideal detectors to avoid that conditioning.
The upper bound is proved; the paper's claimed tightness additionally
depends on its distinguishability conjecture. **Verified**, **partial or
adjacent result only** for P36. For fully distinguishable distinct inputs
p_s=1/k!, giving the same constant extreme-case bound as D. This does not
identify 1-p_s with spatial delta.

The established principle “distance is bounded by a bad mixture weight”
therefore cannot itself be claimed as new. Applying it to P36 requires an
actual positive mixture of the appropriate measured laws, with bad weight
at most delta. No such decomposition is supplied by this source for the
spatial dominant-support truncation.

## O: spatial leakage and independent-source regions

Changhun Oh, Youngrong Lim, Bill Fefferman, Liang Jiang, *Classical simulation
of boson sampling based on graph structure*,
[arXiv:2110.01564v2](https://arxiv.org/abs/2110.01564v2), 2022-02-22,
28-page PDF including supplement; Phys. Rev. Lett. 128, 190501 (2022).
Checked **Theorem 2**, the leakage discussion following Lemma 2, supplement
§S4, equations (S99)–(S101), and §S6, (S122), PDF pp. 20 and 23.

The source truncates distant source-to-output matrix entries, calls the
discarded squared Frobenius norm the sum of leakage rates, and embeds the
truncated nonunitary matrix into a larger physical circuit. For local
Haar-random arrays with sufficiently small leakage, sources occupy
disjoint approximate regions. The SPBS error bound displayed in (S122) is

    TVD <= poly(N)*sqrt(||dU||_F²+||dU||_F).

The comparison is with their physical truncated-circuit sampler, not p_d
for the original frame. The random-circuit leakage estimate has additional
depth, spacing and typical-instance hypotheses. **Verified extraction**;
**partial or adjacent result only** for P36. Their disconnected-source
mechanism is direct spatial prior art, but this displayed bound is not the
coefficient-one inequality requested here.

For a dominant-support truncation of occupied columns, the corresponding
discarded squared mass is delta. Even a formal substitution in the
displayed error expression would give poly(k)*sqrt(delta+sqrt(delta)), not
delta, before resolving the comparator and completion differences. This
observation is a comparison of formulas, not an assertion that all of the
source's algorithmic hypotheses automatically hold for our truncation.

## T: internal-state permanents require a separate spatial bridge

Malte C. Tichy, *Sampling of partially distinguishable bosons and the
relation to the multidimensional permanent*,
[arXiv:1410.7687v3](https://arxiv.org/abs/1410.7687v3), 2015-02-18,
15-page PDF; Phys. Rev. A 91, 022316 (2015). Checked §IV.B, **(51)**,
p. 9, and §IV.D, **(55)**, p. 10. The event bound is

    |P_dist(s)-P_internal-S(s)|
        <= P_dist(s)*(per(|S|)-1).

S is the Gram matrix of **internal** single-particle states; the absolute
value is entrywise. The source's d is the full L1 norm, twice our TV.
Equation (16) explains the occupation factorial normalization that is
subsequently suppressed for collision-free notation. Restoring that common
factor for repeated output rows is necessary before summing full-Fock
probabilities. None of this makes S the spatial magnitude Gram B.
For identical internal states |S| is all ones, giving only
TV<=min(1,(k!-1)/2). **Verified event-bound extraction**, **partial or
adjacent result only** for P36.

Version warning: the HTML conversion labels the same event bound (55)
and the L1 definition (59). This report pins the actual PDF numbering.
The PDF body date is also later than its arXiv revision stamp; the exact
version and hash below identify the checked bytes. No complex-Gram
generalization that the paper itself leaves conjectural is used.

## L: localization comparator agrees, but its theorem is weaker/different

The previously authenticated Deshpande et al. primary version,
[arXiv:1703.05332v3](https://arxiv.org/abs/1703.05332v3), 2018-08-05,
was re-read at supplement (S12)–(S20). It compares the full Fock law to
independent particles through interference pairs and ordered routings.
Its continuation bounds off-diagonal overlap row sums and uses locality,
separated initial inputs and Lieb–Robinson/Anderson localization estimates.
This supplies the established spatial-overlap/localization route, not the
stated arbitrary-frame bound with delta and coefficient one. **Verified
methodological overlap**, **partial or adjacent result only** for P36.
The first audit's factorial/orientation cautions about printed (S13)–(S16)
still apply; this re-read is not an endorsement of those lines verbatim.

## What the which-source interpretation does and does not supply

The classical channel Pr(A=a,I=i)=q_ia/k has posterior q_ia/a_i, so its
optimal single-label identification error is delta/k. Under independent
labeled scattering, the expected number of photons outside their assigned
dominant region is delta, and a union bound controls that classical bad
routing event by delta. These are established classification/coupling
ingredients, reviewed previously via Rioul.

That bad-routing statement is about p_d with particle labels retained.
It is not a verified positive-mixture statement for p_b. Coherent routing
amplitudes can contribute to the same measured occupation; deleting them
before taking absolute squares is not automatically an ordinary
probability coupling. Neither the source-identification dictionary nor
the word “dephasing” fills this missing implication.

As a restricted algebraic boundary, k=2 does follow from the project's
N1 certificate. Let l_1,l_2 be the two wrong-region column masses. Then
delta=l_1+l_2<=1 and Cauchy gives

    B_12 <= sqrt((1-l_1)l_2)+sqrt(l_1(1-l_2))
          <= sqrt(delta*(2-delta)),
    TV <= B_12²/2 <= delta-delta²/2 <= delta.

This is a direct comparison calculation, consistent with the separate
physics reviewer, not an external attribution or a proof for k>=3.

## Provenance and search limits

Primary PDF artifacts, retained temporarily for this check:

| Source | SHA256 |
|---|---|
| D, [1901.02810v3 PDF](https://arxiv.org/pdf/1901.02810v3) | `27300c1a36a0c0b7c4e158c6fc56fa7b1f8fc9d498f458184228309fa34ceee1` |
| S, [1501.00850v4 PDF](https://arxiv.org/pdf/1501.00850v4) | `a87707cdaff6c2d9662ffd894a383dd397bdcb59b12dd97d9bac39f33a4f1a25` |
| O, [2110.01564v2 PDF](https://arxiv.org/pdf/2110.01564v2) | `54bd5779e9b0a5bf02d24815f4a133764c73797eda62d2a142e16d3f5fa6920a` |
| T, [1410.7687v3 PDF](https://arxiv.org/pdf/1410.7687v3) | `9a1719c36eaa9b85e85265047aedb432fa50bec0fb61718c28153cb66f138cc7` |
| L, [1703.05332v3 PDF](https://arxiv.org/pdf/1703.05332v3) | `7493ed821279c9a344b2f3a3783ca5a0468bf649705c85cdb5a87bbe20df7ece` |

Text was extracted with pypdf 6.4.0 using the existing temporary dependency
directory and system Python. The default Homebrew Python's expat loader
failed; switching interpreters resolved extraction without changing the
project environment. Source hashes authenticate bytes, not theorem validity.

Search paths were (1) internal distinguishability/which-way/dephasing,
following D's reference to S and T; (2) source localization and spatial
truncation, including O and L; and (3) exact/synonym queries for leakage,
independent particles and source identification. Queries included
`boson sampling total variation distinguishable particles localization`,
`"boson sampling" "which-source"`,
`"boson sampling" "dephasing" labels distinguishable`,
`"boson sampling" "localization" "variation"`,
`"boson sampling" "source identification"`, and
`"boson" "independent particles" "leakage" variation`.

Coverage is bounded to English primary sources found through web/arXiv,
publisher pages and citation chains through 2026-11-22. Exhaustive forward
citations, non-English sources and all adjacent coherence inequalities were
not covered. No source absence, failed query or numerical fit is counted
as novelty evidence. No QPU, sampler implementation, numerical sweep,
manuscript or shared scientific state was changed. The general P36 source
implication and its attribution remain **UNVERIFIED/OPEN**.
