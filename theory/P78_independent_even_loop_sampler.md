# P78: exact PNR sampling by even closed walks for nonnegative pair matrices

Primary verdict: **proved as written below** in an explicitly stated ideal
real-arithmetic sampling model. The full normalized PNR law has a positive
compound-Poisson representation. The proposed Perron-walk construction
samples it exactly, with the stated expected proposed-step bound.
Finite-bit efficiency, preprocessing and matched hardware timing are
separate obligations, not supplied by an exact real-valued distribution
identity.

Independent static derivation of ROOT's P78 candidate, 2026-11-25, branch
`research/p66-dark-barrier`, starting checkpoint
`c532655f6e2418b8f6067288cd6c8eb31b028f42`. No other P78 author file,
derivation or verdict was read. Only this file is written. The Gaussian
PGF, Perron-vector existence and marked-Poisson identities needed below
are derived internally. No scientific code/import, AST, test, graph,
RNG draw, probability query, numerical/native run, QPU or manuscript
action was performed. ROOT's separate literature work is not a premise
and no novelty claim is made here.

## 1. Class and complete PNR generating function

Let Z be a finite m-by-m REAL SYMMETRIC, entrywise NONNEGATIVE matrix,
including possible diagonal entries, with ||Z||op<1. The pure,
zero-displacement Gaussian state is

    |psi_Z>=det(I-Z^2)^(1/4)
                     exp(1/2 a^dagger Z a^dagger)|0>.

Real orthogonal diagonalization reduces its squared unnormalized norm
to the product of the one-mode series
sum_n binom(2n,n)(s^2/4)^n=(1-s^2)^(-1/2). Signed eigenvalues are
allowed; their squares enter the norm. This proves the normalization.

Let n=(n_1,...,n_m) be the COMPLETE photon-number record, with vacuum,
collisions and all total photon numbers retained. For z_i in [0,1], put
D_z=diag(z_i), and define G(z)=E product_i z_i^(n_i). Applying
product_i z_i^(N_i/2) to the pair exponential replaces Z by

    Z_z=sqrt(D_z) Z sqrt(D_z).

Its operator norm is at most ||Z||<1. Taking that unnormalized state's
squared norm gives

    G(z)=sqrt(det(I-Z^2))/sqrt(det(I-Z_z^2))
        =sqrt(det(I-Z^2))/sqrt(det(I-(D_z Z)^2)).

For strictly positive z_i, D_z Z and Z_z are similar by sqrt(D_z);
the equality extends to zero coordinates by determinant continuity.
All square roots here are positive real roots on [0,1]^m. In particular
G(1)=1 and G(0)=sqrt(det(I-Z^2)), the raw vacuum probability. This is
one source's full law, not a conditional CF law or a two-color product.

Let r=||Z||op, temporarily with r>0. Expanding scalar log(1-x) on
the eigenvalues of the two symmetric squares gives

    log G(z)=sum_{l>=1}
       [Tr((D_z Z)^(2l))-Tr(Z^(2l))]/(2l).

Both weighted and unweighted matrices have norm at most r<1, so the
absolute series is dominated by a constant times
sum_l m r^(2l)/(2l)<infinity. Thus the trace expansion and exchanges of
the finite vertex sums and infinite length sum are justified.

## 2. Positive rooted-walk intensities

A rooted walk of length 2l is an ordered tuple

    w=(i_0,i_1,...,i_(2l-1),i_(2l)),   i_(2l)=i_0.

Use each tuple of intermediate indices as it appears in the trace sum;
there is no additional quotient by rotations, reversal or primitive
period. Define

    a_w=product_{t=0}^{2l-1} Z_(i_t,i_(t+1)),
    nu_w=a_w/(2l),
    c_i(w)=number of t in {0,...,2l-1} with i_t=i.

The terminal repeat i_(2l) is NOT counted again. Thus sum_i c_i(w)=2l,
including repeated visits or self-loop steps. Nonnegativity of Z makes
every nu_w nonnegative. Expanding the trace gives exactly

    log G(z)=sum_closed_w nu_w [product_i z_i^(c_i(w))-1].

The total accepted-walk intensity is finite:

    A=sum_w nu_w=sum_l Tr(Z^(2l))/(2l)
       =-(1/2)log det(I-Z^2).

One may therefore draw a Poisson number with mean A and select independent
walk marks proportional to nu_w, adding their visit counts. Its PGF is
G. This statement alone is not yet an efficient way to select a mark;
section 4 supplies the proposed constructive rejection mechanism.

For clarity, the marked-Poisson identity follows directly from a power
series. If M is Poisson with mean Lambda and each independent mark has
PGF F(z), then

    E[F(z)^M]=sum_M exp(-Lambda) Lambda^M F(z)^M/M!
             =exp(Lambda[F(z)-1]).

This proves the counting identity without an assumed loop-soup theorem.
The countable walk index is harmless: the total intensity is finite,
so the number of selected marks is finite almost surely. Equality of
the PGFs on [0,1)^m identifies all probabilities by their convergent
power-series coefficients.

## 3. Perron vector and stochastic transition matrix, proved directly

First suppose the undirected positive-entry support is connected and
the block is nonzero. Maximize x^T Z x over real unit vectors. Replacing
x by |x| cannot reduce that quadratic form. Hence a maximizer v can
be chosen nonnegative and satisfies Zv=r0 v by the stationary equation.
Here r0>0 for a nonzero block. If v_i=0, its eigenvector equation forces
Z_ij v_j=0 for all neighbors; connectivity propagates a zero to every
coordinate, contradicting ||v||=1. Thus v is strictly positive.

For any real unit x,

    |x^T Z x|<=|x|^T Z |x|<=r0.

All eigenvalues therefore have absolute value at most r0, while r0
is itself an eigenvalue. Thus r0=rho(Z)=||Z||op=r in (0,1). This supplies
the Perron existence/radius statement needed here, without importing it
as an external theorem or assuming primitivity.

Define

    P_ij=Z_ij v_j/(r v_i).

Every row sums to one by Zv=rv; its entries are nonnegative. The matrix
is reversible with stationary weights proportional to v_i^2 because
v_i^2 P_ij=Z_ij v_i v_j/r is symmetric in i,j. Scaling v changes nothing.
Reversibility is a consistency check, not a stationarity requirement for
the sampler. Its starting vertex below is UNIFORM, not drawn from v_i^2.
No mixing-time or burn-in assertion is needed.

## 4. The constructive proposal/thinning sampler

For this connected block define

    L_r=-log(1-r^2)>0,       Lambda=(m/2)L_r.

Start its output counts at zero and perform the following mathematical
random construction:

1. Draw M from Poisson(Lambda).
2. Independently for each proposal draw l>=1 with
   P(l)=r^(2l)/(l L_r), and draw i_0 uniformly among the m vertices.
3. Generate exactly 2l transitions with P, obtaining i_1,...,i_(2l).
4. If i_(2l)!=i_0 discard this INTERNAL proposal. If it returns, add
   one photon for each departure visit i_0,...,i_(2l-1), counting repeats.
5. Return the accumulated full PNR count vector after all M proposals.

The length probabilities sum to one since integrating the geometric
series gives sum_{l>=1} x^l/l=-log(1-x), x=r^2<1.
For a particular closed tuple w,

    product_t P_(i_t,i_(t+1))
       =r^(-2l) a_w * v_(i_(2l))/v_(i_0)
       =r^(-2l) a_w.

Its proposal intensity is consequently

    Lambda * [r^(2l)/(l L_r)] * (1/m) * product_t P_(i_t,i_(t+1))
       =a_w/(2l)=nu_w.

Nonreturning marks contribute count zero and hence mark-PGF value one.
The marked-Poisson calculation in section 2 now gives log G exactly.
There is no missing factor two or extra root/orientation multiplicity.
Choosing the stationary root distribution instead of the stated uniform
root, or counting the final root twice, would generally give a wrong law.

This is an exact FULL count sampler in the ideal random-primitive model.
Its return tests are computational rejections used to generate latent
walks, not optical CF conditioning or discarded Gaussian shots. No
hafnian, prescribed-photon-number success event or rare target is used
to define a sampled optical record.

## 5. Work and photon-number identities

The expected proposed length is

    E[2l]=[2/L_r] sum_{l>=1}r^(2l)
          =2r^2/[(1-r^2)L_r].

Multiplying by E M=Lambda gives the exact expected number of PROPOSED
Markov transitions per full sample,

    E steps=m r^2/(1-r^2).

This includes transitions in nonreturning proposals, not just accepted
walks. The expected output photon count is independently

    nbar=sum_w nu_w (2l(w))
         =sum_{l>=1}Tr(Z^(2l))
         =Tr[Z^2(I-Z^2)^(-1)].

The same nbar follows by differentiating the Gaussian PGF at z_i=u=1.
Because r is one eigenvalue, nbar>=r^2/(1-r^2), and therefore

    E proposed steps<=m nbar.

Also nbar<=E proposed steps because every squared eigenvalue is at most
r^2. This nbar is for ONE source and counts emitted photons, before any
detector loss. The loop method creates no photons; it is an operation-count
comparison with that physical source statistic.

The actual algorithm cost is not just that transition count. It includes
matrix input/support decomposition, Perron data, normalizers, transition
preprocessing, random-variate generation, output initialization and count
updates. With row probability tables/alias preparation, a row draw can
use constant ideal real primitives; without that preparation a row scan
can cost its degree, at most m. Both setup and transition costs must be
charged. Sparse Z only helps through its actual support and row access.

A proposal may store its 2l departure vertices and update output counts
only after the return test, using O(l) additional work and storage.
Rejected paths are still paid. Even simple inverse-CDF generation of the
length takes O(l) ideal arithmetic steps via its coefficient recurrence;
Poisson generation by its probability recurrence has O(M+1) steps under
the same exact-real/exponential primitives. These observations account
for variable-length draws rather than declaring them free constant-time
physical operations. There is no deterministic memory/time cap here;
long tails are unbounded though expectations are finite at r<1.

## 6. Zero, reducible, periodic and diagonal cases

- Z=0: output vacuum deterministically. No undefined r, log-series length
  or division by a Perron coordinate is evaluated.
- Reducible Z: permute its undirected support into connected blocks.
  The pair state and determinant PGF factor across those blocks. Sample
  the nonzero blocks independently by the construction above and put
  zero counts in zero singleton blocks. A single global Perron vector
  supported only on a maximal component must not be divided into zero
  coordinates of another component.
- Componentwise expected steps satisfy
  sum_b m_b r_b^2/(1-r_b^2)<=sum_b m_b nbar_b<=m nbar.
- Bipartite support is allowed. Its Markov chain may have period two and
  Z may have eigenvalue -r. The algorithm uses even lengths from the
  outset; no aperiodicity or stationary initialization is needed.
- Positive diagonal entries are allowed. A repeated self-loop can give
  multiple photons in one mode. Every accepted walk has even length, so
  total photon number is even, while individual occupations need not be.

Two exact checks fix the normalization:

1. One mode Z=[s], 0<s<1. Here P=[1] and every proposed walk returns.
   The output PGF is sqrt(1-s^2)/sqrt(1-s^2 z^2), exactly the single-mode
   squeezed even-photon law. The intensity of the length-two jump is
   s^2/2, confirming the one-half factor.
2. Two-mode pair Z=[0 t;t 0], 0<t<1. Here P swaps the two modes. Each
   accepted length-2l walk contributes l photons to each mode. Both
   uniform roots together give intensity t^(2l)/l, and
   G(z)=(1-t^2)/(1-t^2 z_1 z_2). Thus
   P(n_1=n_2=n)=(1-t^2)t^(2n), the exact TMSV pair law.

These are symbolic consistency checks, not samples or numerical evidence.

## 7. Exact-real construction versus finite-bit implementation

The probability construction is exact given the real parameters r,v,P
and exact draws from its Poisson, log-series and row distributions. It
has no minimum positive-entry, Perron-coordinate or extra small-radius
hypothesis below r<1 for mathematical validity. This is not yet a
finite-bit implementation theorem.

Perron existence does not make obtaining certified r,v free. Arbitrary
real input data need not even come with finite encodings. With computable
inputs, an implementation must state its norm/gap certificates, eigenvector
accuracy, tiny-coordinate ratios, transcendental probabilities, discrete
random-coin generation and any stopping/truncation error. Ordinary floating
eigenvectors and rounding of transition rows are not exact sampling.
This note proves no uniform polynomial expected bit complexity for all
such inputs, and supplies no executed approximate-TV contract.

Near r=1 the mean photon count and proposed walk work can grow without
bound; polynomiality in m and nbar is not polynomiality in input-bit
length alone. At very weak source strength, setup can dominate all walk
work. Immutable data may be reused for a genuinely fixed Z, but a new
graph or changed pair matrix must pay its valid setup/control cost.
Hardware loading, optical preparation, classical cut scores and all
postprocessing also need explicit budgets before a timing comparison.

The first unimplemented implication is therefore a certified finite-bit
sampler and measured full-cost envelope for a specified input family.
It is not a missing coefficient, sign, normalization or sampling-law
identity in the theorem proved here. No implementation or experiment
is authorized by identifying that obligation.

## 8. P73 colors, postprocessing and independent loss

Two independent colors are sampled by two independent instances, reusing
only legitimate common setup for identical pair matrices. Their joint
full-count law is exactly the physical product law. The emitted means
add; for equal mode dimension m, the combined proposed-step expectation
is at most m times that total emitted mean. Color labels and both N-mode
records must be retained. Applying the same CF/complement acceptance rule
afterwards reproduces ALL its accepted and failed pulse probabilities,
without evaluating hafnians or assuming that acceptance is inexpensive.

Consequently the complete pure-source count model used by P73, with
Z=lambda(J-I+epsilon A) entrywise nonnegative and norm below one, has
this exact mathematical classical sampler at every valid finite strength,
not only a weak-perturbation or overlap-bound regime. Sparse nonnegative
pair matrices are covered too. A larger joint-color Gaussian also fits
the one-source theorem if its entire pair matrix has the same nonnegative
real property; arbitrary complex correlated sources do not follow.

The same fixed classical decoding, the independent detection loss specified
below, or postselection can be applied after a full sample, with all
their computational rejections charged.
Rare CF conditioning still has its real repetition cost. This is not
efficient relative hafnian evaluation or a promise of cheap normalized
conditional samples when the physical event is rare.

For uniform independent pure loss of transmissivity eta AFTER the encoded
source, draw each detected count independently as Binomial(n_i,eta).
This gives the exact detected PNR law: on an input number state, the
signal/environment beam splitter has binomial count weights, and the
environment trace removes cross terms between different input numbers
when computing a diagonal output probability. Equivalently its PGF is
G(1-eta+eta z_i). No pure-state approximation to the lossy state is needed.
The expected detected total is eta nbar, but the walk-work bound still
uses the emitted nbar, not only successful/detected photons. General
internal noise, subsequent coherent changes of the measured basis or
changed instruments are not silently included.

## 9. Exact scope and disposition

| Obligation | Result |
|---|---|
| Full Gaussian PGF and square-root determinant | Proved by weighted pair-state norm |
| Trace-log coefficient and positive even rooted walks | Proved with absolute convergence |
| Perron existence and spectral radius | Proved by Rayleigh maximum and connectivity |
| Log-series/Poisson proposal intensity | Exactly nu_w=a_w/(2l) |
| Full output law including vacuum, collisions and total-number tails | Exact PGF equality |
| Expected proposed steps and emitted mean | m r^2/(1-r^2)<=m nbar |
| Zero blocks, reducibility, period two and diagonal pairs | Explicitly handled |
| Independent colors and post-source loss | Exact count-law corollaries with raw costs |
| Finite-bit certification, setup and equal hardware clocks | Not established |
| General complex/signed Gaussian matrices or arbitrary measurements | Outside theorem |
| Positive optimizer, all-Gaussian classicality or novelty | Not established |

KEEP the exact full-PNR classical construction as a strong prospective
control for this nonnegative class. REJECT treating its hafnian-weighted
conditional bias alone as evidence that the complete source has no
classical sampling mechanism. A finite-bit resource qualification remains
FOLLOWUP before implementation-level or hardware-budget conclusions.

This does not express the quantum Gaussian state as a classical coherent-
state mixture. It samples one specified measurement law. General passive
mode transformations can produce signed or complex pair entries in the
measured basis; the positive walk intensities no longer follow from this
proof there. No all-unitaries or all-Gaussian no-go is inferred.

Final mathematical proofreading covered the pair-state norm, trace factors,
root multiplicities, terminal-visit exclusion, stochastic rows, component
decomposition, expectations and arithmetic/cost distinctions. Only text
and Git integrity checks accompany this independent freeze.
