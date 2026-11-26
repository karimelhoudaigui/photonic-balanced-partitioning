# P124: permanent FPRAS sources and the finite-bit boundary

26 November 2026; source-only audit, no program or experiment. **JSV2004
alone: the requested explicit rational/Turing interface remains UNVERIFIED.
A separate pinned2026 source verifies a finite-bit0/1 primitive. The
polynomial-size rational-weight reduction remains a separate obligation.**
This does not refute JSV or claim finite-bit implementations impossible.

Context: P108_FINITE_BIT_BRIDGE_OPEN.md read in full, SHA256
f13ad7ce690758b01c91d5f936b1bd5ee14ca73f194144f373a2b65355a6755d;
P104's source/model paragraphs and its existing conditional audit were read,
not re-proved. Audit SHA2562ab8113a48e95b09a8937ba3eccfea22403512459dd6829f1e74afd5ec6d0f6c.
P123's proposed gadget/proof was NOT read, so it receives no verdict here.

## Acquisition, identity and actual reading depth

The literature-check workflow was reused. Manual metadata lookup in project/
own expected cache locations and existing sibling records found no exact
retained source artifact for these identifiers. No Python cache helper ran,
no cache was created, and no full PDF/text was saved. Retained source SHA: NONE.

S1: Jerrum/Sinclair/Vigoda, *A Polynomial-Time Approximation Algorithm for
the Permanent of a Matrix with Nonnegative Entries*, JACM51(4),671--697,
July2004, DOI10.1145/1008731.1008738. The [27-page published scan](https://www.math.cmu.edu/users/af1p/Teaching/MCC17/Papers/approxpermanent.pdf)
has journal pagination/copyright and received-Aug2003/accepted-Jan2004 marks.
Read Th1.1 p673, definition2.1 p674, capped sampler Fig1 p675,
activities/Metropolis pp678--681, Section5 pp690--693 and Section7 p694.
DOI retrieval returned403; browser PDF screenshots failed cache lookup.
The authenticated scan's extracted text was used; no full mixing-proof audit.

S2: Chen/Guo/Vigoda/Yang, *An O-tilde(n^3)-time FPRAS for the Permanent*,
[arXiv2609.20717v2](https://arxiv.org/abs/2609.20717v2), revised16-Oct-2026,
62 pages; official metadata matches authors/title/version. Read [pinned v2 HTML](https://arxiv.org/html/2609.20717v2):
Theorem1/Corollary2 and model paragraph, Section8.2--8.3 relevant proof
passages, and FULL Section8.4 including all four implementation subsections.
This is a preprint, not a checked publication or an audit of all62 pages.

S3: Doron/Ta-Shma, *On the de-randomization of space-bounded approximate
counting problems*, IPL115(2015),750--753, [published author-hosted PDF](https://www.cs.tau.ac.il/~amnon/Papers/DT.IPL15.pdf),
Definition2 and preceding output convention, p751. Read that model leaf,
not its derandomization proof. No secondary search result is theorem evidence.

## Exact extraction: do not equate the two models

S1 Th1.1 asserts the nonnegative permanent FPRAS. Definition2.1 uses
exponential relative error, success3/4 and polynomial time in n,epsilon^-1;
median amplification adds log inverse failure. Section5 fixes polynomial
sample/chain lengths. Section7 gives dependence on log(a_max/a_min), then
an entry-magnitude-independent variant, explicitly
“assuming arithmetic operations are treated as unit cost”. Cooling uses
exp(-1/2). No rational input encoding, intermediate/output bit bound or
finite-fair-coin transition implementation was extracted. This verifies the
stated probabilistic/arithmetic result, not the stronger bit interface. [S1](https://www.math.cmu.edu/users/af1p/Teaching/MCC17/Papers/approxpermanent.pdf)

S2 explicitly separates its nonnegative UNIT-COST extension from its0/1
bit implementation. Section8.4 caps total operations D, returning0 on
overflow; schedules lie on rational grids, stored weights have guarded
ranges, and b=C log(n/epsilon) significant bits are used. Discrete choices
consume O(b) random bits; clock approximations have tail/boundary budgets.
Output observations, including exact zeros, use finite floating arithmetic.
The stated total bit cost is O(n^3 epsilon^-2 log^8(n/epsilon)); accuracy
is epsilon and failure<=1/8+1/32<1/4. This is explicitly0/1 ONLY. [S2 §8.4](https://arxiv.org/html/2609.20717v2#S8.SS4)

S3 Definition2 explicitly uses a randomized Turing machine, dyadic output
strings, and polynomial time in encoded input size, inverse accuracy,
log inverse confidence and log range. It establishes a suitable interface
DEFINITION; sharing its acronym does not supply an implementation of S1. [S3 p751](https://www.cs.tau.ac.il/~amnon/Papers/DT.IPL15.pdf)

## Independent interface checks and notation dictionary

Project: n=matrix dimension, B=matrix encoding budget, delta=relative
accuracy in(0,1), rho=failure target. S1's epsilon is an exponential accuracy;
using epsilon=delta/2 safely implies usual1+/-delta accuracy. Its confidence
symbol delta must not be confused with project delta. S2 epsilon can be
project delta directly. All Turing bounds also include the lengths of the
encoded accuracy/confidence parameters, or assume their short encodings.

For rational entries with positive numerators/denominators of at most B bits,
2^-B<=a_ij<=2^B on positive support. Thus log(a_max/a_min_positive)<=2B
and, when nonzero, per(A)>=2^(-nB); also per(A)<=n!2^(nB).
These elementary bounds control the INPUT range. They do not bound the
bit size of an arbitrary sequence of real arithmetic operations. Zeros need
a support-matching test/separate zero branch; log(a_max/0) is not a bound.

For S2's0/1 input, zero is detected by support matching; otherwise
1<=per(A)<=n!. Its output observations are n! times exp(-s), with
0<=s<=n*beta_max and beta_max=ceil(log2(n!)). Hence exponent magnitudes
are polynomial in n (plus precision/averaging indices). A bounded-mantissa
binary float is an exact dyadic rational; expanding its exponent into an
ordinary numerator/denominator takes polynomially many bits, including
failure outputs0. This is our interface inference, not a weighted theorem.

## Finite fair bits for the clock step: explicit audit inference

The following ROOT-suggested translation was manually checked; it is NOT
quoted as S2 pseudocode. For a stage's cap R, use its existing thresholds

    alpha=1/[128D(R+1)], Delta<=1/[256D W_max(R+1)].

Couple ideal U uniform(0,1) to U_b=floor(2^b U)/2^b, generated by b fair
bits. Choose2^-b<=min(alpha/2,alpha*Delta/4); abort if U_b<alpha/2.
Abort is a subset of the already budgeted event U<alpha. On U>=alpha,

    U_b>=alpha/2,
    |log U-log U_b|<=2*2^-b/alpha<=Delta/2.

The exact rate W is an integer>=1, so dividing by W cannot enlarge that
error. Reserve the other Delta/2 for logarithm/division evaluation. This
meets the existing waiting-time error budget; no extra failure event is
charged. Polynomial D,R,W_max require b=O(log(n/delta)). With the global
operation cap, uniform-bit consumption and every clock computation are
finite on ALL branches, not only with high probability. Tiny-clock-input
aborts retain output0 as a failure value; they are not claimed correct draws.

Accepting S2's theorem/Section8.4 proof, these interface checks support a
0/1 randomized Turing primitive. Odd-median amplification of independent
base runs supplies1-rho confidence with O(log(1/rho)) repetitions; rational
comparisons and output/coin lengths remain polynomial. No real-RAM oracle
is imported to generate an exact continuous uniform or exponential clock.

## Expected time is a different conditional bridge

Neither an arithmetic-operation count nor expected real work proves an
expected BIT-time bound. S1 does not state an expected-time-only guarantee;
S2 supplies explicit caps. If some alternative Turing primitive has uniform
E(time)<=P and base correctness>=3/4, cap each copy at8P steps and emit0
on timeout. Markov adds<=1/8 failure, leaving correctness>=5/8. The median
of m independent copies fails with probability<=exp(-m/32). Thus
m>=32log(1/rho), made odd, gives worst-case polynomial time, coin and output
caps. This generic argument requires a proved uniform polynomial P; it
does not establish such a P for JSV's unimplemented real transitions.

## Arrow disposition for P104/P108

| Arrow | Verdict |
|---|---|
| S1's stated relative permanent guarantee/confidence amplification | Verified in its extracted model |
| S1 alone -> requested rational bit/coin/output interface | Unverified; no blanket upgrade |
| S2 v2 ->0/1 finite-bit counting primitive | Verified as stated, with explicit clock-interface inference above |
| S2 nonnegative extension ->general rational finite-bit primitive | Not established by that extension |
| Polynomial binary-weight/rational ->0/1 reduction with known exact scale | Separate unreviewed P123 obligation |
| Entire P104 weighted occupation sampler/finite transcript law | Still conditional pending all required reductions/self-reductions |

Known after notation translation: confidence/accuracy interfaces. The
rational weighted bridge is not a novelty claim or a counterexample to
classical simulation. A genuine parsimonious/AP reduction must preserve
zero/nonzero, scale, polynomial instance size/bit size and output errors;
it cannot be replaced by the name FPRAS. No P104/P108/paper source was edited.
Only this audit was written; no program/import/AST/test/scientific computation,
RNG, graph/native/runner/QPU, manuscript edit, checkout, delegation or push.
