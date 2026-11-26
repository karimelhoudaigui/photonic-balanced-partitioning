# P127 — Primary-source check for a few-loss, gauge-positive transcript

Date checked: 2026-11-26. Author: independent literature reviewer P66.
Parent: bfef3aa3514cd60ea3ae3d8676a2bdd1070284e0. Method: literature-check.
P126's moving construction and all experimental outcomes were not read.
This file records source applicability, not an audit or acceptance of P126.
No program, import, test, RNG, native probability call or QPU was executed.

## 1. Exact question and notation

Let A be the supplied rational, entrywise nonnegative m-by-K occupied-input
matrix, A^T A <= I. Inject K indistinguishable photons in distinct input modes,
with vacuum in all other inputs; environment modes are unobserved.
For a fixed nonnegative integer r0, observe the complete signal PNR occupation n
when |n| >= K-r0, including collisions, and otherwise report one FAIL symbol.
When r0 >= K this retains the whole signal law. Gauge positivity means a known
input/output phase conjugation reduces the occupied block to such an A.
The proposed guarantee is for every such supplied A, with genuine sector masses,
polynomial resource/error dependence explicitly specified, and no free conditioning.
It differs from drawing n conditional on a chosen |n|, from a Haar-average result,
and from keeping only collision-free output events.

Throughout, TV is one half of the l1 distance. Source n/l/k conventions are
translated below rather than silently identified with this K and r0.

## 2. Checked primary sources and exact arrows

### S1. Positive amplitudes at a fixed detected number

Konrad Anand, Zongchen Chen, Mary Cryan, Graham Freifeld, Leslie Ann Goldberg,
Heng Guo and Xinyuan Zhang, *Simulating Gaussian boson sampling on graphs in
polynomial time*, [arXiv:2511.16558v3](https://arxiv.org/abs/2511.16558v3),
revised 2026-11-06. Checked official HTML Theorem 1.3 and Section 3, Eq. (5).
The theorem takes a nonnegative real m-by-n matrix, n<m, and approximates the
normalized fixed-n distribution proportional to per(A_z)^2 / product(z_i!).
It does not prescribe vacuum-environment loss probabilities or lower-number masses.
Thus its nonzero normalized all-K component is **known after translation of notation**.
A full-K-or-FAIL law additionally needs its mass and unconditional error budget;
P104/P123 are separate project bridges. For r0>0, an immediate appeal to
Theorem 1.3 is **conditional**, missing a lower-sector representation and sampler.
The source does not establish that bridge merely by accepting arbitrary A.

### S2. Constant lost photons: a conditional hardness statement

Scott Aaronson and Daniel J. Brod, *BosonSampling with Lost Photons*,
[arXiv:1510.05245v2](https://arxiv.org/abs/1510.05245v2), 2015-11-02;
related published PRA 93, 012335 (2016). Checked Section 2, Eqs. (5)-(7), and
Theorem 1. Their n detected photons follow loss of exactly k uniformly unknown
input photons from n+k initial photons, followed by a complex Haar interferometer.
The law averages squared permanents over surviving input subsets; their
collision-free analysis uses the dilute-mode regime. The text explicitly limits
the input-loss model; arbitrary internal losses need not have that formula.
For k=O(1), Theorem 1 supplies a permanent-estimation reduction under the stated
Gaussian/permanent assumptions and precision requirements, not a classical sampler.
Overlap: **partial or adjacent result only**. Its complex random matrices and
conditional loss model prevent applying its hardness conclusion directly to A>=0.
Constant lost photons must not be confused with a constant number that survive.

### S3. A classical graph proxy is a different optical distribution

Changhun Oh, Bill Fefferman, Liang Jiang and Nicolás Quesada,
*Quantum-Inspired Classical Algorithm for Graph Problems by Gaussian Boson
Sampling*, [PRX Quantum 5, 020341](https://doi.org/10.1103/PRXQuantum.5.020341),
published 2024-05-23. Checked published PDF Section III, Eqs. (3)-(11), and
Section IV's loss comparisons (printed pp. 020341-3 through 020341-7).
The classical construction repeatedly samples pairs and erases pair labels.
Its collision-free graph-set weight is proportional to a nonnegative hafnian,
where the GBS comparison uses its square. The benchmark fixes a postselected
detected count and adjusts squeezing in lossy comparisons.
Overlap: **partial or adjacent result only**. This is a relevant, paid classical
graph control, not a TV sampler of the same lossy CF-input channel or its raw
top-number sectors. A positive graph bias in either distribution proves no
few-loss theorem for the other.

### S4. Few surviving particles, rather than few lost particles

Michał Oszmaniec and Daniel J. Brod, *Classical simulation of photonic linear
optics with lost particles*, [arXiv:1801.06166v1](https://arxiv.org/abs/1801.06166v1),
2018-01-18; related NJP 20, 092002 (2018). Checked Section III.1 and Section IV.1,
Theorem 1, Eqs. (20)-(24), Corollary 2. After uniform loss, l surviving particles
from an n-photon CF input form the uniform mixture of l-element input subsets.
Their separable-state approximation has trace-distance error
Delta(l,n)=1-n!/[n^l (n-l)!], hence the same output-TV upper bound for every U.
The useful small-error regime is l=o(sqrt(n)). With l=n-r0, r0 fixed, this
particular bound tends to one. Overlap: **partial or adjacent result only**;
it does not furnish the desired few-lost guarantee. This comparison uses the
exact displayed expression, not an extrapolation of an asymptotic expansion.

### S5. Nonuniform physical paths: a geometry-dependent sufficient condition

Daniel Jost Brod and Michał Oszmaniec, *Classical simulation of linear optics
subject to nonuniform losses*, [arXiv:1906.06696v4](https://arxiv.org/abs/1906.06696v4),
2020-05-11, accepted version; Quantum 4, 267 (2020).
Checked Theorems 1, 2 and 4, especially Eqs. (3), (21)-(23), and Section 7.
Theorem 1 constructively extracts input losses depending on shortest optical paths;
a residual network may remain lossy. Theorem 4 gives a small-TV simulator when
all but O(log n) occupied input paths have sufficient logarithmic lossy depth.
The bunched-input exact sampler and few-protected-input results support this regime.
Overlap: **partial or adjacent result only**. Arbitrary positive A with only a
fixed number lost need not satisfy those geometric or substantial-loss hypotheses.
Extracting some input loss is not proof that all remaining loss becomes an
independent subset mixture or that the residual network is positive.

### S6. Distinguishability order is not a lost-photon count

Alexandra E. Moylett et al., *Classically simulating near-term partially-
distinguishable and lossy boson sampling*, 2019 accepted manuscript,
[institutional primary PDF](https://ris.utwente.nl/ws/portalfiles/portal/155733757/Moylett_et_al_2019_Quantum_Sci._Technol._10.1088_2058_9565_ab5555.pdf),
[DOI](https://doi.org/10.1088/2058-9565/ab5555).
Checked Sections IV-VI, Eqs. (67)-(82), and the discussion after Eq. (82).
The positive state-truncation method treats at most k photons as indistinguishable;
for their uniform-loss model its worst-case error is bounded by
Pr[Bin(n,eta*x)>k], with x their common-overlap parameter. This includes collisions.
Their text notes that the relevant k can grow linearly with n, giving exponential
state-sampling work. At x=1, eta=1-O(1/n), a fixed small k does not control this tail.
Their different probability-truncation method invokes nonnegative permanents of
intensity matrices and has different error/positivity issues.
Overlap: **partial or adjacent result only**. Nonnegative intensities |U_ij|^2
are not the assumption of nonnegative amplitudes A_ij in S1 or this question.

### S7. Recent full-raw sampler, with an average-case quantifier

Youngrong Lim, *Boson sampling is fragile to loss*,
[arXiv:2611.01434v1](https://arxiv.org/abs/2611.01434v1), 2026-11-01, preprint.
Checked Sections II and IV.1, Theorem 1, and Appendix F.1-F.2/G.1.
For distinct single-photon inputs and vacuum elsewhere, uniform fixed transmission
eta in (0,1), the theorem approximates the full PNR law with TV error averaged
over a Haar interferometer. The arithmetic runtime is polynomial, with dependence
on eta not uniform as eta tends to one. Its discussion distinguishes individual
structured instances, nonuniform attenuation, and postselection on rare sectors.
Coarsening that output to the present transcript is a **formal corollary not
stated**, retaining exactly those average-case and fixed-eta hypotheses.
For worst-case positive A or eta_K tending to one with O(1) mean losses, this is
**partial or adjacent result only**, not a directly applicable polynomial theorem.
This recent preprint is not treated as a peer-reviewed result or a priority verdict.

## 3. Translation checks that prevent a false source application

These are manual channel identities, not computational evidence or claims of novelty.
Write G=A^T A and E=I-G, the environment Gram matrix on occupied input columns.
Although G is nonnegative, E can have negative off-diagonal entries. Consequently,
the positive-matrix theorem cannot simply be applied to a loss dilation.
If all occupied columns of a dilation were entrywise nonnegative, their mutual
orthogonality would force disjoint supports. That extra premise removes the
overlapping-column case; it is not a harmless choice of environment basis.

Explicit check: K=m=2 and A=(1/2)J_2 is a rational contraction. Then
G=(1/2)J_2 and E=[[1/2,-1/2],[-1/2,1/2]]. The total-number generating function is
per(E+zG)=(1+z^2)/2. Hence (P0,P1,P2)=(1/2,0,1/2).
Independent input survival with each probability 1/2 instead has P1=1/2.
This counterexample blocks an independent-survivor translation for general A;
it does not refute a different, correctly constructed few-loss algorithm.
If G is diagonal and A>=0, disjoint signal-column supports instead make the
entire raw law an elementary independent-particle case, **known after translation of notation**.

Under the additional uniform-loss model A=sqrt(eta)U_occ, the retained mass is
p_top=sum_{j=0}^{min(r0,K)} binom(K,j) eta^(K-j)(1-eta)^j.
For fixed eta<1 and fixed r0 it is polynomial(K) times eta^K. Returning FAIL alone
then has TV exactly p_top. This elementary **formal corollary not stated** covers
only tolerances at least that mass; it supplies no high-transmission or relative
rare-sector guarantee. A mean transmission is not a channel-wide certificate.

Coarsening contracts TV without changing its source quantifiers. Conditioning
on an event of mass p can amplify an unconditional TV error by order 1/p.
Therefore neither a normalized conditional sampler nor a full-raw average-case
theorem may silently be upgraded to a worst-case, rare-sector guarantee.

## 4. Verdict, search scope and remaining blind spot

**Source verdict:** none of the checked primary statements directly establishes
the proposed worst-case positive-contraction, few-loss raw-transcript theorem.
S1 establishes its normalized all-K core; S2-S7 establish adjacent statements
or the restricted corollaries explicitly listed above. The extension remains
**unverified here**, not apparently new and not contradicted by S2's hardness claim.
If P126 proves a bridge, its statement must identify exactly which arrow is added.

English web/arXiv primary-source search, as of this date, used nonnegative /
non-negative boson sampling with loss, constant lost photons, few losses,
nonuniform loss, lossy Fock sampling, and exact-title searches for the sources above.
Checked theorem passages rather than search snippets; followed adjacent loss and
distinguishability literature in a second pass. No external index was exhaustively
searched and no independent searcher's priority clearance is asserted.
The genuine blind spot is an equivalent positive weighted-matching or environmental
Gram representation already implying this finite-r0 law under different terminology;
this search has not ruled that out. It has also not audited all cited supplementary
algorithms or forward citations, particularly the November 2026 preprints.

Before acceptance, a construction still needs actual lower-sector masses,
interference/cancellation control for E, a sampler with unconditional additive-TV
accounting including zero/rare sectors, and an explicit arithmetic or finite-bit
model. Enumerating O(K^r0) subsets alone supplies none of those missing arrows.
No P126 proof was inspected, no source-derived impossibility is claimed, and no
reproducible optimization advantage, matched wall-time result or QPU readiness follows.

Authentication: official versioned arXiv metadata and primary HTML/PDF passages
were checked; the Moylett copy identifies itself as an accepted manuscript.
Extraction/application depths are the locators above, not full-paper proof audits.
No full text was retained locally or copied into tracked files; retained source
hashes: NONE. This Markdown is the only newly persisted evidence record.
