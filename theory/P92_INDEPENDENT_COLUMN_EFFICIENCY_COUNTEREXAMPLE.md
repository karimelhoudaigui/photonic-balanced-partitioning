# P92: even every column efficiency does not certify uniform-loss tails

**Primary verdict: the proposed physical counterexample is correct.**
A passive vacuum-loss channel can have every single-input intensity
efficiency exactly eta, yet its identical-CF-input probability of four
or more detected photons exceeds `binom(k,4)eta^4`. A spectral bound
cannot be replaced by the mean or the largest individual column norm.
This does not refute P91, whose hypothesis is spectral.

ROOT supplied the matrix, moment route and proposed numbers before this
independent hand reconstruction. No other P92 draft was read. This is
not independent discovery, a hardware calibration or a novelty claim.
No scientific code/import, AST, RNG, graph/seed generation, numerical
matrix/probability computation, backend, pilot data, QPU or paper was used.

## 1. A contractive physical channel with uniformly small columns

Let m=24, eta=1/50, and let T be a 24-by-24 accessible transmission
matrix with only its first row nonzero:

    T_(1,i)=sqrt(eta) for every i=1,...,24,
    T_(a,i)=0 for a=2,...,24.

Then `T^dagger T=eta J_24`, with eigenvalues 24eta and zero. Thus

    ||T||op^2=24eta=12/25=.48<1,
    sum_a |T_ai|^2=eta=.02 for EVERY individual input i,
    Tr(T^dagger T)/24=eta.

It is a legitimate passive-vacuum channel: stack T above
`E=(I-T^dagger T)^(1/2)`. Those columns are orthonormal and extend
to a unitary with additional vacuum inputs. Tracing the environment
produces the stated loss channel. No gain or auxiliary photons appear.

Inject k=12 identical photons, one into each of the first twelve input
modes, with all other inputs vacuum. For this occupied-input restriction,

    ||T[:,A]||op^2=12eta=6/25=.24,

still strictly larger than its individual column efficiencies eta.
The remaining measured modes are vacuum, so the full observed output
is determined by the single count N in output mode 1. Every raw source
attempt injects twelve photons; N counts only detections. Collisions
are retained, and no event is discarded or conditioned away.

## 2. Exact factorial moments from annihilation operators

Write b for that output annihilator. It has the form

    b=sqrt(eta) sum_(i=1..24) a_i + vacuum-environment terms.

The environment supplies the commutator required by a physical output
mode. Its annihilation terms, and a_i for i>12, kill the input vacuum.
For the normalized CF source `|1_A>`, expansion of b^j gives

    b^j |1_A,vac>
      =j! eta^(j/2) sum_(J subset A, |J|=j) |1_(A\J),vac>.

Only distinct occupied annihilators survive. Each chosen source subset
has j! orderings, and different hole subsets are orthogonal. Consequently

    E[(b^dagger)^j b^j]=(j!)^2 binom(k,j)eta^j,
    E binom(N,j)=j! binom(k,j)eta^j.                       (1)

For j>k both sides are zero. The factor j! in the second line is
essential; independent Bernoulli transmission would not have it.
Identical photons and the specified CF input are hypotheses. No
monotone extension to arbitrary internal states is being asserted.

## 3. A certified raw tail lower bound

For every nonnegative integer n, with binomial coefficients zero below
their lower index,

    1_(n>=4) >= binom(n,4)-4 binom(n,5).                  (2)

For n<=3 both sides vanish. At n=4 the right side is 1; at n=5 it is
`5-4=1`. For n>=6 it equals `binom(n,4)(21-4n)/5`, which is negative.
Thus (2) is a pointwise inequality on the entire raw count alphabet.

Taking its expectation and using (1), k=12 gives

    Pr(N>=4)
      >= 24*495 eta^4-4*120*792 eta^5
       =11880 eta^4-380160 eta^5
       =11880 eta^4(1-32eta).

At eta=1/50 the exact hand arithmetic is

    Pr(N>=4) >= (594000-380160)/50^5
               =213840/312500000
               =0.000684288.

The improperly substituted binomial factorial-moment bound would be

    binom(12,4)eta^4=495/6250000=0.0000792.

The proved lower bound is 216/25=8.64 times that quantity, hence
strictly exceeds it. It also exceeds the actual Bin(12,eta) upper tail,
since that binomial tail is at most the latter factorial-moment bound.
No exact event probability, Monte Carlo estimate or rounded numerical
matrix was invented; only the displayed analytical lower bound is claimed.

## 4. Exact scope and consequences

Even perfect calibration of ALL individual input efficiencies at two
percent would therefore not supply the two-percent spectral certificate
needed for P91's small-survivor replacement. In this example the true
full/occupied certificates are .48/.24, respectively. Using those
larger values in P91 is consistent with the counterexample; replacing
them by the smaller per-column value is the invalid step.

This is a toy rank-one channel, not a model or calibration of Lucy,
its detectors or its sources. Its large output counts are bunching in
one mode, not four distinct clicked modes or balanced feasible outputs.
There is no graph optimization, hard instance or advantage claim.

Indeed the single-count distribution is classically simple. Since
N<=k, its exact generating polynomial follows from (1):

    E z^N=sum_(j=0..k) j! binom(k,j)eta^j (z-1)^j.

Expanding this finite polynomial determines its complete scalar count
law with O(k^2) arithmetic operations; physicality guarantees the
resulting probabilities are nonnegative and normalized. The example
therefore falsifies a calibration implication, not classical simulation.
All photon preparation/attempt accounting remains unchanged.

Only this new proof is written. Hand proofreading checked the full and
occupied spectra, source CF normalization, both j! factors, every case
of (2), the exact rational comparisons and the absence of postselection.
