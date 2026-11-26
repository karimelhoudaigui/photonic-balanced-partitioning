# P92 exact-source adversarial hand audit

**Primary verdict: proved as written.** The stated passive-vacuum example has
all24 individual input efficiencies eta=1/50, but its raw four-photon tail
strictly exceeds the envelope `binom(12,4)eta^4`. It refutes the substitution
of a mean/max-column efficiency for a spectral certificate, not P91 itself.

Exact target: `.local/p81-exact-review/theory/P92_INDEPENDENT_COLUMN_EFFICIENCY_COUNTEREXAMPLE.md`,
commit `eca20b5031089786a35ba31a7c9ddc1a2238a34d`, SHA256
`2bed2ba5e760aa6105065b4c6371e4da54fdcdff3817516e437a38333d79e146`.
All131 lines were read. ROOT supplied the candidate and numbers; this is an
independent derivation/check, not discovery or a blind-parameter search.
No other P92 review was read; no delegation, import/AST/test, numerical
execution, RNG, graph, native backend, experiment, paper or QPU was used.

## Objects, physicality and normalization

Let T be24×24 with first row all sqrt(eta) and other rows zero. Then
`T†T=eta J24`, so its eigenvalues are24eta and23 zeros. Thus every column has
squared norm eta, the mean is eta, yet `||T||op²=24eta=12/25<1`.
For the first k12 occupied columns, `T_A†T_A=eta J12` has norm12eta=6/25.
These are intensity-transmission eigenvalues, not amplitude norms.

Set `E=(I24-T†T)^(1/2)`. The48×24 matrix obtained by stacking T above E has
orthonormal columns and extends to a48×48 passive unitary. Its24 auxiliary
input modes are vacuum. Observing the first24 outputs and tracing the rest
therefore realizes a physical vacuum-loss channel, with no gain or helper
photons. Equivalently, mix the24 inputs into their normalized uniform bright
mode, attenuate that mode with intensity24eta, and discard all dark modes.
No per-column factorization at intensity eta is justified by this construction.

Input is the normalized identical-boson state with one photon in each of the
first12 physical modes, all other inputs and the environment initially vacuum.
There is no input factorial other than1. Outputs2..24 annihilate this state
because they contain only vacuum-input terms; their observed counts are zero
with probability1. The complete observed law is therefore `(N,0,...,0)` with
0≤N≤12. The global unitary preserves12 photons including the traced loss ports;
normalization is not conditioned on loss, vacuum, collisions or a herald.

## Both factorials in the moment calculation

The physical output operator is
`b=sqrt(eta)sum_(i=1..24)a_i + vacuum-noise annihilators`.
The noise is essential for `[b,b†]=1`. In normal-ordered expectations its
annihilators kill the initial environment vacuum; a_i for i>12 also kill vacuum.
This is a Heisenberg-input calculation, not a claim that the output loss ports
remain empty or have been postselected to vacuum.

For j≤k, expanding b^j leaves only j distinct occupied annihilators. Each hole
subset J has j! ordered terms, all the same normalized residual CF state.
Different hole subsets are orthogonal. Hence

    ||b^j|1_A,vac>||²=(j!)² binom(k,j)eta^j,
    E binom(N,j)=E[(b†)^j b^j]/j!=j! binom(k,j)eta^j.

Both moments vanish for j>k. In particular E N=k eta, identical to the mean
of Bin(k,eta); matching that mean cannot match higher factorial moments.
At j=k, `P(N=k)=k!eta^k`, also obtained from the repeated-row permanent squared
divided by the output factorial k!, which independently checks normalization.
The derivation needs identical photons in the stated CF source and makes no
claim for arbitrary internal distinguishability or coherent source families.

## Pointwise inequality and exact hand comparison

For nonnegative integers n, let binomial coefficients vanish when n is below
their lower index. The proposed inequality
`1_(n≥4)≥binom(n,4)-4binom(n,5)` holds on the ENTIRE count alphabet:

| n | Right side | Indicator comparison |
|---|---|---|
| 0..3 | 0 | equality |
| 4 | 1 | equality |
| 5 | 5-4=1 | equality |
| ≥6 | `binom(n,4)(21-4n)/5<0` | below the indicator1 |

Taking the unconditioned expectation with k12 gives

    Pr(N≥4)≥4! binom(12,4)eta^4-4*5! binom(12,5)eta^5
            =11880eta^4-380160eta^5.

The coefficients are24*495 and4*120*792. Dividing this lower bound by
`495eta^4` gives `24-768eta`; at eta=1/50 this is216/25=8.64.
Directly the lower bound is
`(594000-380160)/50^5=213840/312500000=0.000684288`, whereas
`495/50^4=0.0000792`. The source claims a lower bound, not an exact tail;
the strict comparison is already decisive. Since the actual Bin(12,eta)
upper tail is at most495eta^4, it is also below this physical raw tail.

This event counts at least four photons bunched into ONE observed mode. It
does not mean four distinct clicks, four distinct occupied receiver modes,
or a balanced feasible optimizer output. No collision or loss sector is dropped.

## Scope and classical countercontrol

This strengthens the earlier four-bright-mode mean counterexample: there the
column efficiencies differed and could be detected by individual-input tests;
here ALL individual efficiencies equal eta. Off-diagonal entries of `T†T`
remain unconstrained by those measurements and attain the maximal coherent
rank-one accumulation. Full/occupied norm certificates are .48/.24, not .02.
P91 remains valid when given either applicable certified spectral bound; its
eta=.02 small-survivor illustration simply cannot use these column data.

The example is classically simple. From the finite binomial expansion of z^N,

    G(z)=E z^N=sum_(j=0..k) j! binom(k,j)eta^j (z-1)^j,
    P(N=n)=sum_(j=n..k)(-1)^(j-n)binom(j,n)j!binom(k,j)eta^j.

Expanding these triangular sums costs O(k²) scalar arithmetic operations.
Physicality proves coefficient nonnegativity, and G(1)=1 proves total mass1.
For eta=1/50 all coefficients are rational, with denominator dividing50^k;
they define an ordinary exact finite classical sampling problem after paid
construction/random-bit costs. No numerical evaluation, sampler implementation,
wall-clock benchmark or hardware-performance comparison was performed here.

The authenticated claim is the mathematical calibration counterexample only.
It is not a Lucy/source/detector model or calibration, a graph optimizer, a
classically hard sampling family, quantum advantage, or a novelty/priority
certificate. All12 prepared photons remain charged on every raw attempt.
The source requires no correction for the audited statements, and no P91 or
P90/P82 manuscript, code, data or execution permission is changed by this review.
