# P80 finite-bit bridge: exact-source conditional proof review

**Primary verdict: proved as written as a conditional theorem on A and B.**
A supplies the optical-law identification; B converts the work parameter S
to m^2 times the mean emitted photons. The finite-bit construction and its
5epsilon/8 total-variation bound have no remaining load-bearing gap in the
reviewed source. No correction is requested. This is not an implementation,
exact Turing sampler, practical runtime measurement or positive optimizer.

## Artifact and review provenance

Reviewed ALL155 lines of
`.local/p65-independent-audit/research/P80_finite_precision_loop_sampling_route.md`,
SHA256
`5fa9ce9441691b639a8208b536172fa67ba6972edb01ea7bb45990eb0050b10b`,
original commit
`57b3ecceb366dd7cc6e69b55eae7451eaed67ec3`.
The exact hash was independently checked. The author source was not changed.
The author recorded no access to another P80 derivation and treated A and B
as separate supplied premises. ROOT supplied this reviewer with the exact
source and critical questions after that freeze. This is the first subsequent
independent exact-source audit, not a second before-author proof, independent
discovery or a priority claim. The author's stated verdict was visible.

26 November 2026, worktree `.local/p75c-code-review`, starting at
`1db79063c76089353f724befd3bf33e75a74d824`. Only this report is written.
Applicable AGENTS.md and proof-audit obligations apply. Inspection used
source text, hashes, Git metadata and hand algebra. No import, AST, program,
test, RNG, numerical query, native backend, QPU or manuscript action occurred.
No other P80 finite-bit proof, run, P79 file or P75 output was read. The
earlier rational audit is separate; A/B remain named premises in this review.

## Conditional claim and proof dependencies

Let m>=1 and rational Z be real symmetric, entrywise nonnegative and
||Z||<1. Rational0<epsilon<1 and its encoding length are part of the input.
Use the supplied Gaussian PGF/positive-loop law A, and the separately
established resolvent construction v,kappa,P. Its rational parameter is

    p=kappa^2, S=m*p/(1-p),
    nbar=Tr[Z^2(I-Z^2)^(-1)], S<=m^2*nbar under B.

The algorithm produces a law on count vectors plus FLAG. The target law
is embedded with zero FLAG mass. Setup, memory, bit use and worst-case
arithmetic work are polynomial in m,B,S,1/epsilon; B includes epsilon's
encoding. Substitution of premise B yields the stated polynomial dependence
on nbar. This does NOT mean polynomial work in B and log(1/epsilon) alone.

The implication chain is:

    positive-loop identification A -> independent rational Poisson lengths
    rational expected total length S -> finite T/M reference with flags
    explicit exponential upper sum -> rational capped-Poisson approximation
    downward dyadic rounding -> bounded-bit normalized probability tables
    sequential couplings ->5epsilon/8 error including all flagged failures
    finite enumerations/bit lengths -> polynomial worst-case construction.

Premise B is needed only for the final resource conversion, not the finite
construction or its error bound in terms of S. The proof does not claim to
reprove either A or B by approximation or agreement between agents.

## Rational intensities and the reference law

Independent Poisson marking of the ideal process gives
a_l=m*p^l/(2l), l>=1. The logarithms in the original population/length
primitive cancel EXACTLY. Uniform root selection contributes1/m, and the
killed-chain transition product along an alive closed walk contributes
kappa^(-2l) times its Z-edge product. The v ratios telescope on return.
Thus its intensity is weight(w)/(2l), with the correct rooted/periodic
multiplicities. Dead and nonreturning paths add no counts but retain their
planned length. The total planned expectation is

    E W=sum_l 2l*a_l=m*sum_l p^l=S.

Take T=2max(1,ceil(4S/epsilon)), M=T/2 and beta=S/(T+2).
Then T>=8S/epsilon, so S/T<=epsilon/8, and beta<epsilon/8. This also
covers arbitrarily small positive S; Z=0 is handled separately as true
vacuum. No rounded floating value of S is used to choose the cap.

Let L be the event that any length l>M proposal exists. Its probability
theta is at most sum_(l>M) a_l, which is at most
E[long planned length]/[2(M+1)]<=beta. The short and long Poisson
collections are independent. The crucial coupling sets F=1 on L and,
on its complement, with probability(beta-theta)/(1-theta). This is valid
because0<=theta<=beta<1. It gives marginal F~Bernoulli(beta).

Although F is correlated with the LONG process in this proof coupling,
it is independent of the SHORT process: it is constructed only from the
long collection and an independent auxiliary coin. Its marginal law with
short counts is therefore exactly the reference algorithm's independent
rational flag. The algorithm never computes theta. This resolves the
apparent unknown-tail-probability issue without an irrational oracle.

On F=0, no long proposal exists. If short planned length also stays<=T,
using identical short walk marks gives the same counts as the full ideal
process. Consequently

    TV(R,iota(mu_Z))<=beta+Pr(W_short>T)
                     <=beta+S/T<=epsilon/4.

This also bounds reference FLAG mass. The omitted-long error is ALREADY
included in beta through L subset{F=1}; adding or requiring another theta
term would miss the stated coupling. Conversely, it is not legitimate to
couple F independently of the long process and retain this particular
agreement argument. No long/dead proposal is mislabeled as optical vacuum.

For each l<=M, K_l=floor(T/(2l)) is correct: J_l>K_l alone implies planned
length>T. A capped state* may therefore flag immediately; when no individual
overflow occurs, the aggregate planned sum must still be checked. This
finite description exactly realizes R before probability approximation.

## Capped Poisson lemma and dyadic normalization

For rational a>=0, let w_j=a^j/j! and

    n=max(2,ceil(6a),ceil(log2(4/delta))),
    U=sum_(j<n)w_j+2w_n, s=1/U.

Beyond w_n the term ratios are at most a/(n+1)<1/6, so the tail starting
at w_n is below2w_n. Thus U>=exp(a). The elementary factorial bound
n!>=(n/e)^n follows from integrating log(x); n>=6a and e<3 yield
w_n<=(ea/n)^n<=2^(-n)<=delta/4. Since U>=exp(a)>=1,

    0<=1-exp(a)/U=(U-exp(a))/U<=2w_n<=delta/2.

For capped states0,...,K, define q_j=s w_j and put the residual on*.
All masses are nonnegative and normalized because sum_(j<=K)w_j<=exp(a)<=U.
Every finite mass only decreases relative to the exact Poisson mass.
The overflow increases by precisely their total deficit, so TV is

    (exp(-a)-s)sum_(j<=K)w_j<=1-exp(a)/U<=delta/2.

Next round each of the K+1 finite masses DOWN to denominator2^b, with
2^b>=2(K+1)/delta. The residual again goes on*. Additional TV is exactly
the total removed finite mass, at most(K+1)2^(-b)<=delta/2. This proves
the lemma's delta bound without evaluating any exponential or tail constant.
The integer CDF is normalized and sampled with b fair bits, with no retry.

The cases a=0 and K=0 are valid. For a=0, w_0=1 and later terms vanish,
so U=1 and the exact zero-count distribution is recovered. K=0 simply
retains state0 and*. The formulas never divide by a. The logarithm used
to describe n is implemented by exact integer/rational comparisons to
powers of two, not a real-arithmetic oracle.

## Coupling all finite-bit errors

Use delta_Pois=epsilon/(8M). The M capped Poisson variables can be coupled
jointly to their exact versions with mismatch probability<=epsilon/8.
Early stopping on an overflow does not invalidate this: all M variables
may be regarded as latently drawn first and the final decision as a
deterministic function. Unused draws need not actually be performed.

For any rational categorical row, rounding the first d-1 entries down
and placing the residual on the last state adds TV at most(d-1)2^(-b).
All entries remain nonnegative. Absorption is the last state for a walk
row. A one-state categorical uses zero bits and is deterministic.
The Bernoulli flag's approximation contributes at most epsilon/8.

Once the planned cap is passed, total proposal number is at most T/2=M
and total transitions at most T. There are therefore at most T+M start/
row draws. Give each error delta_mark=epsilon/[8(T+M)]. Conditional on
an agreeing past, both processes request the same next row; maximal
coupling plus a union bound gives total mark mismatch<=epsilon/8. Early
death only reduces the number of actual draws. If the flag or capped counts
already disagree, that event is charged to its earlier coupling budget,
not silently continued as an agreeing branch.

The complete triangle bound is

    TV(hatR,iota(mu_Z))
      <=epsilon/4+epsilon/8+epsilon/8+epsilon/8
       =5epsilon/8<=epsilon.

The four terms are reference flags (including omitted long lengths), Poisson
tables, flag coin and marks. They neither omit the long tail nor count it
twice. The target has zero FLAG probability, so the same TV bound controls
finite-bit FLAG mass. No failed prefix or overflow is retried or conditioned
away to create an apparently exact accepted sample.

Mapping FLAG to a chosen vector and keeping the flag bit is legitimate.
The vector marginal's TV bound follows by deterministic data processing;
a flagged zero is a SUBSTITUTE, not a true vacuum observation. Conditioning
on no flag, CF or a rare cost event is a different law and has no free
unconditional error guarantee from this theorem.

## Worst-case bit work, including every table

Exact rational matrix setup has polynomial bit lengths and work in m,B.
The optional physical-promise check through I-Z>0 is valid in this symmetric
NONNEGATIVE class: for every real x, |x^T Zx|<=|x|^T Z|x|, so the largest
absolute eigenvalue is the nonnegative maximal Rayleigh value. Thus I-Z>0
implies ||Z||<1 here. This shortcut would require a different test for
arbitrary signed input, which the source does not permit.

T=O(1+S/epsilon), M=T/2. Each rational a_l has encoding length polynomial
in T,m,B because it uses a power p^l with l<=M. Its numerical value is
at most m/2. The Poisson truncation index is consequently
O(m+log(M/epsilon)), and K_l<=T/2. For L=max(K_l,n), denominators of
all terms w_j divide denominator(a_l)^L*L!, whose bit length is
O(L*bits(a_l)+L log L). Numerators, finite sums, U's reciprocal and dyadic
floors also have polynomial bit sizes. Reduced exact arithmetic suffices.

Even the crude bound M times the largest separate-table size is polynomial
in m,B,T,log(1/epsilon). The proof does not count just one Poisson table
or hide the M setup factor. Constructing all root/row CDFs is likewise
polynomial. Their precision is O(log(m(T+M)/epsilon)); row selection may
use a dense scan and still has polynomial bit work.

There are at most M capped Poisson draws, M start draws, T transition
draws and one flag draw. Every one uses a bounded number of fair bits;
all branches, including overflow and death, obey these bounds. Temporary
paths/counts need only polynomial storage; returned total photon count
is at most T. The target's unbounded support is covered by the preceding
TV/FLAG coupling, not by assuming it absent.

Thus the worst-case bit construction is polynomial in m,B,S,1/epsilon.
Small S requires the constant/minimum T=2 and paid matrix/output setup;
Z=0 has its separately exact vacuum branch. Large/near-critical S and
nbar can be numerically enormous despite short encodings. Substituting
S<=m^2*nbar does not give polynomial time only in the input bit length,
nor practical constants or measured QPU-comparator costs. Epsilon's own
encoding is explicitly charged, while numerical1/epsilon is an allowed
complexity parameter rather than hidden logarithmic dependence.

## Disposition

| Obligation | Review result |
|---|---|
| Exact155-line source and conditional A/B dependency | Passed; premises kept separate |
| Rational intensities and full raw optical identification | Correct conditional on A |
| Independent-of-short flag coupling and T/M overflow | Passed, unknown theta used only in proof |
| U/exponential enclosure, capped deficits and dyadic residual | Passed with all constants |
| M Poissons, flag coin and T+M sequential mark couplings | Passed, total5epsilon/8 |
| Flag probability and vector-marginal interpretation | Passed; no false vacuum/conditioning claim |
| All tables, bit sizes, fixed-bit branches and memory | Polynomial in stated numerical parameters |
| Conversion to nbar, exact sampler, implementation/throughput | B needed; latter claims not established |
| Positive optimizer, novelty, hardware or QPU | Not established |

The finite-bit approximation gap is closed by this conditional mathematical
construction, rather than an ideal random-variate assumption. The exact-law
and S-to-nbar dependencies remain separately named. Executable validation,
runtime constants, input calibration and matched resource comparisons are
future obligations; no implementation or experiment is authorized here.
Final hand proofreading checked the flag coupling, finite caps, factorial
enclosure, rounding direction, TV constants, zero/small/large cases, every
table's work and the raw-versus-conditioned distinction.
