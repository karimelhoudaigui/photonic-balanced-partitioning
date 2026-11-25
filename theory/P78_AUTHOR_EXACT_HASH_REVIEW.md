# P78 exact-source review: full PNR sampling by nonnegative even loops

Primary verdict: **proved as written**, for the author's explicitly stated
ideal real-arithmetic/random-primitive model. For every finite real symmetric
entrywise nonnegative contraction Z, the specified procedure samples the
complete normalized undisplaced pure-Gaussian PNR law exactly. Its proposed
Markov-transition expectation is at most m times the mean emitted photon
number. This is not a finite-bit or total hardware-runtime theorem. No
material correction to the reviewed source is required.

## 1. Exact target, provenance and independence

The entire 183-line source was read:

- File: `research/P78_nonnegative_Gaussian_even_loop_sampler.md` in ROOT.
- Original source commit supplied by ROOT: `d42b4b3`.
- SHA256 independently checked from those bytes:
  `118c88279e01bb13b81450b7f30c2cb55ad852e3a34cfcffbdc56c1c64df7c4a`.
- Source line numbers below refer to precisely that version.

My before-reading reconstruction is preserved unchanged in
`theory/P78_independent_even_loop_sampler.md`, 360 lines, commit
`05b10613a1cea1bb8ac68ed3b5e4972f4a6afdb8`, SHA256
`e00cf6fd1003cce8fd7006d422c0b5615f6ddca98cec2f31861e604df228f00f`.
It was committed and communicated before the author's source was opened.
ROOT supplied the candidate formulas and requested critical implications
before that reconstruction. Thus this is an independent before-source
derivation and subsequent exact-source audit, not independent discovery
or an originality certification. A shared model error remains possible.

Only this new review file is written. Neither source nor the 360-line
reconstruction is changed. No other P78 verdict, P79 code/results or P75
output was opened. No scientific import, AST, test, RNG, graph, numerical
probability query, native run, QPU or manuscript action was performed.
The proof-audit and mathematical proofreading workflows were applied.

## 2. Normalized claim and dependency graph

Objects and hypotheses: finite m-by-m REAL SYMMETRIC Z with every entry
nonnegative, including allowed diagonal entries, and operator norm less
than one. The state has zero displacement and pair amplitude Z in the
actual PNR measurement basis. Counts include vacuum, collisions and all
even total photon numbers. No CF or cut event conditions the input law.

The source's load-bearing chain is:

1. Pair-exponential norm and number weighting give the full determinant
   PGF (lines 31-43).
2. An absolutely convergent trace-log expands that PGF into nonnegative
   rooted even-walk intensities (45-67).
3. A positive Perron vector makes the closed-walk weights stochastic
   path weights (71-84).
4. Poisson population, logarithmic lengths and a uniform root produce
   exactly those intensities after the return test (86-105).
5. PGF uniqueness identifies the entire count law. Length expectation
   and a PGF derivative give the mean-photon transition bound (114-138).
6. Block factorization covers reducible and zero matrices (107-112),
   and independent color products preserve raw failure probabilities
   under the same classical decoding (150-155).

All mathematical leaves used here are internal arguments or elementary
finite-dimensional spectral/probability identities. No external loop
theorem, hafnian algorithm, numerical validator or literature-priority
claim is a premise. The assumptions of exact Perron data and exact random
primitives belong explicitly to the computational model, not to an
unproved claim that floating computation supplies them for free.

## 3. Decisive checks against the before-reading reconstruction

### Pair-state normalization and determinant ordering: passed

Real orthogonal diagonalization of Z preserves the vacuum and reduces
the squared exponential norm to the product of
`sum_n binom(2n,n)(s^2/4)^n=(1-s^2)^(-1/2)`.
Signed eigenvalues cause no change to that expression. Consequently
the state's prefactor `det(I-Z^2)^(1/4)` is correct.

Number weighting multiplies each creation operator by sqrt(z_i), so the
weighted pair matrix is B=sqrt(D) Z sqrt(D), not DZ treated as symmetric.
The inequality `||B||<=||Z||<1` holds for every z_i in [0,1]. For D positive,
`DZ=sqrt(D) B sqrt(D)^(-1)`, establishing the determinant conversion in
39; determinant continuity covers singular D. Thus the square-root
determinant ratio has the stated ordering, and both vacuum and z=1
normalization are right. No invertibility of D at the boundary is assumed.

The trace-log is absolutely convergent: the symmetric B has all eigenvalue
magnitudes at most r=||Z||, so each trace term is bounded in magnitude by
m*r^(2l). The same bound holds for Z. This justifies the length and finite
vertex-sum exchanges without using positivity of eigenvalues.

### Root, orientation and occupation multiplicities: passed

Expanding Tr((DZ)^(2l)) yields one factor z for each departure index
`i_0,...,i_(2l-1)`. The equal terminal index i_(2l)=i_0 contributes no
extra visit. Repeated vertices and diagonal self-loops are included.
The tuples are precisely trace tuples, with no cyclic or reversal
quotient. The logarithm contributes exactly 1/(2l); there is no further
orientation factor or correction for periodic words.

Each tuple intensity is nonnegative because entries of Z are nonnegative,
even when Z has negative eigenvalues. Their total is
`-1/2 log det(I-Z^2)<infinity`. Hence a finite compound-Poisson mark
construction is legitimate. The elementary identity
`E F(z)^J=exp(Lambda*(F(z)-1))` identifies its PGF. Equality of the
convergent nonnegative PGFs determines all PNR probabilities, not just
some moments or selected collision-free coefficients.

### Perron radius, positive coordinates and exceptional blocks: passed

At 72 the notation r is already ||Z||; the following argument correctly
identifies it with the top Rayleigh eigenvalue. A Rayleigh maximizer can
be replaced by its componentwise absolute value. Its eigenvector equation
and connected nonzero support force all coordinates positive: a zero
coordinate forces zero at every neighbor and therefore throughout the
component. For any unit real x,
`|x^T Z x|<=|x|^T Z |x|<=r_top`.
Thus no negative eigenvalue has larger magnitude and r_top=||Z||>0.
There is no circular positive-eigenvector assumption in this argument.

The rows of P sum to one by Zv=rv. Detailed balance with v_i^2 follows
from symmetry of Z but is not used to select the root. Irreducibility
does not imply or require aperiodicity. A bipartite block and eigenvalue
-r are allowed. Reducible blocks must be processed independently, as
the author specifies; dividing by a global vector that vanishes on a
smaller component would be invalid and is not proposed. A zero singleton
outputs vacuum; a positive diagonal singleton uses P=[1].

### Poisson population, length law and thinning: passed

Put L_r=-log(1-r^2). The proposed population has mean m*L_r/2, not
L_r/2, and the length probabilities r^(2l)/(l*L_r) sum to one. For a
closed tuple, the Perron-coordinate ratios telescope. Its intensity is

    (m*L_r/2) * [r^(2l)/(l*L_r)] * (1/m)
             * [r^(-2l) product_j Z_(i_j,i_(j+1))]
      =product_j Z_(i_j,i_(j+1))/(2l).

The root must be uniform. Substitution of the stationary distribution
v_i^2 would generally change the intensities. A rejected nonreturning
mark contributes the zero count vector, so its mark PGF equals one;
this is computational thinning, not optical-shot conditioning.
Poisson marking yields independent accepted counts per tuple, and the
full marked-Poisson PGF is exactly the one already derived from the state.

The source's symbolic one-mode and two-mode checks, lines 142-148, agree
with my sealed derivation. Single-mode jumps have intensity s^(2l)/(2l).
For Z=[[0,s],[s,0]], both roots together give intensity s^(2l)/l and
increment (l,l), yielding the geometric pair PGF stated in the source.
These checks support the factors; the general trace/mark proof, not two
examples, supplies the universal conclusion.

### Mean photons and precise resource claim: passed with stated scope

For one nonzero connected block,

    E transitions=Lambda*E[2l]=m*r^2/(1-r^2),
    nbar=sum_l Tr(Z^(2l))=Tr[Z^2(I-Z^2)^(-1)].

The latter follows either by weighted loop visits or by differentiating
G(u,...,u) at u=1. It counts emitted photons of ONE source; there is no
extra factor two from pair creation or the square-root determinant.
The eigenvalue r contributes r^2/(1-r^2), proving the stated upper
bound m*nbar. All rejected proposed transitions are counted. Componentwise
summation and `-log(1-r^2)<=r^2/(1-r^2)` also prove lines 125-127,
including the proposal-count bound m*nbar/2.

The exact quantitative bound is a transition/proposal count, conditional
on the stated data and sampling primitives. It is not a statement that
the total time is m*nbar with zero additive setup or output cost. For
example, initialization has a dimension-dependent cost even at nbar=0;
row scans can multiply transition cost by up to m. Poisson and length
generation require their specified random primitives or a charged
implementation. The author's lines 128-138 and 164-168 correctly reserve
these obligations. PF computation/certification, tiny-coordinate ratios,
logarithms, finite bits, count sizes and truncation-TV guarantees are
not silently supplied by the probability identity.

## 4. Obligation summary and limits

| Obligation | Assessment |
|---|---|
| Complete pure-Gaussian norm and weighted PGF | Passed |
| Determinant conversion at singular D | Passed by continuity |
| Positive trace expansion and finite total intensity | Passed |
| Root/orientation/period multiplicities | Passed |
| PF existence, norm identification and stochastic rows | Passed |
| Uniform-root proposal intensity and return thinning | Passed |
| Reducible, zero, diagonal and periodic cases | Passed |
| Exact full law including vacuum and collisions | Passed |
| Proposed-transition/proposal expectation versus emitted mean | Passed |
| Independent P73 colors and same raw acceptance/decoding | Passed |
| Efficient samples conditioned on rare CF or small-cut events | Not claimed |
| Finite-bit certification or total measured runtime | Not established |
| Novelty, all-Gaussian classicality or optimizer advantage | Outside claim |

In particular, sparse support and arbitrarily small positive entries do
not invalidate the exact law; they can affect setup/representation costs.
Approaching r=1 can make nbar and proposed work arbitrarily large. Signed
or complex final pair matrices need not have positive loop weights.
Displacement, general subsequent interferometry and arbitrary quantum
measurements are not covered. A sampler for these fixed PNR statistics
does not express the underlying state as a classical coherent-state
mixture. Independent colors mean a product source, not generic correlated
colors. Postselection remains a paid operation on full raw samples.

## 5. Remaining gap, evidence boundary and disposition

There is no missing mathematical implication in the stated exact sampler
or its proposed-step bound. The strongest safe conclusion is an exact
classical construction for the stipulated full raw PNR source class in
the ideal model, including the nonnegative P73 product-source subclass.
It supplies a prospective classical control, not the project's requested
positive optimizer or a hardware resource conclusion.

The next implementation obligation is a separately frozen finite-bit
sampler and error/cost contract for specified inputs, including paid
setup and every source failure/conditioning cost. This review authorizes
no execution. A finite validator can check its implementation but is not
a premise of the analytic result. ROOT's bounded literature comparison
is separate; no Le Jan attribution/priority conclusion is adjudicated
here, and no claim of new mathematics follows from this review.

Source verification consisted of a full text/line-number read and SHA256
check; only text and Git integrity operations accompany this report.
Final mathematical proofreading checked determinant order, the one-half
factors, root/terminal conventions, the meaning of r, block exceptions,
raw versus conditioned counts and transition versus total-cost language.
