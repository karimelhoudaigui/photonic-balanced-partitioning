# P64 fixed-phase complete classical sampler for the P63 architecture

25-Nov-2026. STATIC derivation and self-review of ROOT's candidate sampler.
Base revision: `682d3573c47ffe4261ae4c018d2132af8e5d8a8e`.
Authoritative architecture: `P63_extensive_phase_structural_checks.md` and
`../research/P63_EXTENSIVE_PHASE_ARCHITECTURE_CARD.md` at that revision.
No import, numerical computation, matrix evaluation, graph, phase/count draw,
simulation, calibration or QPU call was performed. No runtime is measured.

**Normalized claim and primary verdict: proved as written**, for the
mathematical distribution and ideal exact probability/arithmetic operations
specified below. At each FIXED full ten-parameter Theta, the construction
samples the COMPLETE 18-mode PNR law of P63, with every collision retained.
It is stronger than a phase-average sampler. Finite-precision qualification,
bit complexity and measured cost are separate open implementation obligations.
The sharper support and cost bounds below are new internal consequences of
the definitions, self-reviewed here; they are not independently replicated.

## 1. Exact domain, conventions and dependencies

Ports are `(b,i)`, with b=0,1,2 and i=0,...,5. The source is the normalized
occupation state with one photon in every one of the 18 modes, all photons
indistinguishable, lossless passive linear optics and ideal complete PNR.
The single-particle matrix uses U[output,input] and is

    U_Theta = V (F3 tensor I6) D_Theta (I3 tensor F6).

Let imagunit=sqrt(-1). Use the positive Fourier convention in P63. V acts only at color i=0;
embedded in its three modes it is

    V0 = [[3/5,-4/5,0], [4/5,3/5,0], [0,0,1]].

Thus, after the three F6 preparations and D_Theta, the remaining operations
are independent colorwise three-mode unitaries W_0=V0 F3 and W_i=F3 for
i=1,...,5. Fix theta[0,i]=theta[b,0]=0 as in P63. The proof actually allows
any real intermediate phases; the gauge restriction is not needed for it.

Write Gamma(W) for the occupation-space action obtained by replacing each
input creation operator a_b^dagger by sum_a W[a,b] c_a^dagger. All occupation
kets below are NORMALIZED: |n> = prod_i (a_i^dagger)^n_i / sqrt(prod_i n_i!).
The coefficient domain is C for the theorem. Exact source zeros can instead
be decided in Z[xi], xi=exp(pi*imagunit/3), as proved in section 5. Arbitrary real
Theta is a mathematical input, not a promise of bounded finite-bit access.

Dependency graph (every leaf is internal or a declared convention):

    normalized Fock/creation convention + Fourier matrices [conventions]
       -> three independent F6 source amplitudes [internal expansion]
       -> joint M law, coherent conditional state [orthogonality]
    local W_i + M conservation [matrix factorization]
       -> nondestructive M conditioning preserves final PNR law [projectors]
    normalized conditional amplitudes + suffix orthogonality
       -> local conditional probabilities and state update [Born rule]
       -> complete joint PNR law [induction]
    cyclic column permutation of F6 [direct algebra]
       -> necessary residue rule -> s<=80 [generating function]
       -> R_M<=s^2 [third row determined by first two]
       -> finite sparse arithmetic/storage bounds [explicit loops]

There is no external theorem, numerical evidence or Fock-width hardness
assumption on a load-bearing leaf of this derivation.

## 2. Source expansion and the correct coarse conditioning

For a six-mode occupation n with sum_i n_i=6 let

    A(n) = <n|Gamma(F6)|1,1,1,1,1,1>,
    p(n) = |A(n)|^2,
    S = {n : sum_i n_i=6 and A(n) != 0}.

Here S denotes a SET; write s=|S| when counting it. Unitarity gives
sum_n p(n)=1. With alpha=(n_0,n_1,n_2), the state after D_Theta is

    |psi_Theta> = sum_alpha C_Theta(alpha) |alpha>,
    C_Theta(alpha) = prod_b A(n_b)
                     * exp(imagunit sum_(b,i) theta[b,i] n_b[i]).

The intermediate |alpha> form an orthonormal basis. Define color totals

    M_i = sum_b n_b[i],
    C(M) = {alpha in S^3 : sum_b n_b[i]=M_i for every i},
    P(M) = sum_(alpha in C(M)) prod_b p(n_b).

Consequently the JOINT M law is exactly that obtained by independently
drawing three occupations with law p and summing them. P(M) is independent
of Theta; no independence between different M_i is asserted. For P(M)>0,
the normalized coherent state conditional on the coarse total M is

    |psi_Theta,M> = sum_(alpha in C(M)) a_alpha |alpha>,
    a_alpha = C_Theta(alpha) / sqrt(P(M)).                 (1)

The amplitude divisor is sqrt(P(M)), not P(M). Equivalently, form every
compatible coefficient first and normalize by its Euclidean norm. The
projectors onto M commute with every remaining W_i. Each final PNR vector
o belongs to exactly one M sector, so inserting this coarse measurement
does not change any final PNR probability. It follows that sampling M and
then its coherent conditional law reproduces the unconditioned law.

**Essential implementation distinction:** the three source-row draws are
used ONLY to obtain M. Discard their latent individual rows. Reconstruct
ALL compatible alpha in (1). Retaining the one sampled alpha and running
six independent tritters would destroy the coherences and yield the
phase-average law from P63, rather than the fixed-Theta law.

## 3. Exact sequential color measurement

Take the fixed color order 0,...,5; any fixed permutation is valid. After
the already selected output prefix, keep a normalized sparse amplitude map
on the unmeasured INPUT occupations. For the current color i write a key
as (x,tau), where x=(n_0[i],n_1[i],n_2[i]) and tau contains every remaining
unmeasured color. Different tau label orthonormal normalized Fock kets.
The first map is precisely (1), after regrouping its coordinates by color.

For |x|=|o|=M_i, the normalized three-mode transition amplitude is

    T_i(o,x) = <o|Gamma(W_i)|x>
             = per(W_i[o|x]) / sqrt(prod_a o_a! prod_b x_b!)
             = sqrt(prod_a o_a! / prod_b x_b!)
               * [z^o] prod_b (sum_a W_i[a,b] z_a)^x_b.   (2)

Repeated rows and columns are included in the permanent. Equation (2)
also specifies a creation-polynomial/three-mode bosonic DP implementation;
there is no distinguishable multinomial replacement for a bunched input.
For M_i=0 it gives the scalar vacuum transition 1.

For each candidate output triplet o define

    b_(tau,o) = sum_x a_(x,tau) T_i(o,x),
    q_i(o | prefix,M) = sum_tau |b_(tau,o)|^2.            (3)

The sum over x is COHERENT, within one fixed suffix. The sum over tau is a
sum of squared magnitudes, because tracing an orthonormal suffix basis
gives delta_(tau,tau'). Remaining color unitaries would preserve the same
inner products and can be postponed. By unitarity of Gamma(W_i),

    sum_o q_i(o | prefix,M) = sum_(x,tau) |a_(x,tau)|^2 = 1.

Draw o with these probabilities. For a selected outcome of positive mass,
the next normalized suffix amplitude map is

    a'_tau = b_(tau,o) / sqrt(q_i(o | prefix,M)).         (4)

Contributions with the SAME suffix are summed before squaring or storing;
they are not stored as independent mixture components. The measured local
input is removed. No row-sum-six constraint may be newly imposed on this
suffix map: a measured output is a superposition of several local input
triplets, so its remaining rows do not have one fixed residual photon count.
The suffix support remains a projection of the initial compatible support.

Equations (3)-(4) are the ordinary projective measurement rule for the
current normalized pure state. Induction gives the exact product of
conditional probabilities for every full output prefix. Mixing over P(M)
then gives the complete P63 PNR distribution. No density matrix indexed by
two whole configurations is required. No physical postselection is used.

## 4. Adverse operation-order and boundary checks

The following are algebraic checks of the claim, not executed fixtures.

| Obligation | Status | Decisive reasoning |
|---|---|---|
| Source amplitudes and total mass | passed | Three normalized F6 preparations; occupation factorials in (2). |
| Joint M law independent of Theta | passed | Orthogonal alpha; phase factors have unit modulus. |
| Coarse M conditioning valid | passed | Every W_i preserves its M_i; final output fixes M. |
| Conditional source normalization | passed | Squared norm is P(M); divisor sqrt(P(M)). |
| Partial trace and phase coherence | passed | Sum amplitudes for identical tau, square, then sum over distinct tau. |
| Sequential normalization | passed | Unitary T_i on the full M_i-photon sector. |
| Residual state after output | passed | Project and renormalize; no artificial residual row-sum restriction. |
| M_i=0 | passed | Unique vacuum input/output; (3)-(4) reduce to identity. |
| All 18 photons in one color | passed | Compatible alpha=(6e_i,6e_i,6e_i) is unique and nonzero; one 18-photon tritter suffices. |
| Zero P(M) / zero conditional q | passed | Neither can be selected under exact draws; do not divide by zero or replace a draw. |
| Color measurement order | passed | Distinct W_i and final number projectors act on disjoint modes. |
| Approximate floating probabilities | conditional | Needs later precision/mass/CDF/error contract and qualification. |
| Practical runtime / positive scientific objective | not addressed | No execution or evidence of advantage; cost bounds below are prospective. |
| Loss, partial distinguishability, noise, QPU | out of scope | Those are different source/measurement laws. |

Why the distinctions in (3) matter: in a two-mode algebraic toy, a normalized
state (|1,0>+exp(imagunit phi)|0,1>)/sqrt(2) through the real Hadamard has probability
(1+cos(phi))/2 for |1,0>. Sampling one input basis ket first gives 1/2 and
erases this response. Conversely, attach distinct orthonormal suffixes to
the two input terms and the output marginal becomes a sum of two squared
transition amplitudes; coherently adding those suffixes is wrong. These
are exact toy counterexamples to the two erroneous replacements, not
numerical evidence that a P63 graph objective changes with Theta.

Common phase on every b at fixed i multiplies (1) by exp(imagunit phi_i M_i),
which does not alter the conditional PNR law. Common phase on a whole
source row multiplies every coefficient by exp(imagunit 6 phi_b). These gauge
checks agree with P63 and do not reduce its coherent conditioning to a
mixture over individual alpha.

## 5. Exact source zeros and a support UPPER bound, without an experiment

There are binomial(11,5)=462 possible six-photon/six-mode occupations.
With xi=exp(pi*imagunit/3), expand the UNNORMALIZED Fourier polynomial

    prod_(j=0..5) (sum_(i=0..5) xi^(i*j) z_i)
        = sum_n c_n z^n,          c_n in Z[xi], xi^2=xi-1.

Then

    A(n) = sqrt(prod_i n_i!) c_n / 6^3,
    p(n) = (prod_i n_i!) |c_n|^2 / 6^6.                 (5)

For c_n=u+v xi with integers u,v, |c_n|^2=u^2+u v+v^2.
Thus c_n=0 iff u=v=0. A future exact six-factor polynomial DP can decide
EVERY zero, all 462 occupations retained in its evidence, without a
floating threshold. It can supply the source PMF as integer weights over
the common denominator 6^6. No such DP was executed here.

There is also a direct necessary suppression rule. Cyclically permuting
the six input columns leaves the permanent unchanged because every input
is occupied once; the Fourier formula multiplies its output rows by
xi^i. Therefore

    A(n) = xi^(sum_i i*n_i) A(n),
    A(n) != 0  =>  sum_i i*n_i = 0 (mod 6).             (6)

To count only the occupations ADMISSIBLE under (6), use a roots-of-unity
filter. For a sixth root of unity of order r dividing 6,

    prod_(i=0..5) (1-z xi^(k*i))^(-1) = (1-z^r)^(-6/r),
    [z^6](1-z^r)^(-6/r) = binomial(12/r-1,6/r).

The orders r=1,2,3,6 occur 1,1,2,2 times, respectively. Hence the number
passing (6) is

    (462 + 10 + 2*3 + 2*1)/6 = 80.

This proves **s<=80**, not s=80. Additional exact cancellations are allowed
and the actual nonzero support cardinality remains UNEVALUATED here.
No runtime or correctness assumption may silently replace this necessary
condition by a sufficient one. Full bunching occupations 6e_i are nonzero
directly from the polynomial, so the support is not empty.

## 6. Stronger fixed-M reconstruction and prospective arithmetic bound

For any M, its first two source rows DETERMINE the third:

    n_2 = M - n_0 - n_1, coordinatewise.

Enumerate (n_0,n_1) in S^2, reject an invalid third occupation, and use exact
membership in S for the rest. The three rows remain ordered physical b
rows; do not identify permutations with a multiplicity shortcut. Therefore

    R_M := |C(M)| <= s^2 <= 6400.                       (7)

This is an exhaustive enumeration proof, not a sampled estimate. It needs
no stored S^3 product and no table for every possible M. Conditional
amplitudes at each shot need only the compatible rows, phases and norm.
The coarser bound without (6) would be 462^2; no unverified s=80 claim is
needed for (7). Computing exact support can only reduce the bound.

Let R_i be the number of live sparse keys before measuring color i. The
measurement update only projects away a color and merges keys, so
R_i<=R_M. Let D(T)=binomial(T+2,2), the FULL number of three-mode output
occupations with T photons. Each input triplet still has coordinates
0,...,6, since it is a projection of an initial alpha; its output is NOT
restricted to that cube. In particular D(M_i)<=190, and every collision
up to 18 in an output mode remains possible.

An implementation may group current keys by suffix tau and STREAM one
length-D(M_i) output vector per group. For each group use (3) to accumulate
the output probabilities. After selecting o, make a second pass computing
only b_(tau,o), writing one next-state key per suffix. Do not materialize
an array indexed by every (tau,o). Two passes give at most

    R_i D(M_i) + R_i

complex multiply-add contributions at that stage, apart from probability
accumulation, lookup, grouping, phase evaluation, RNG and normalization.
Since sum_i M_i=18 and all M_i are nonnegative,

    sum_i D(M_i) = (sum_i M_i^2 + 3*18 + 2*6)/2 <= 195.

Using (7), a conservative whole-shot bound for the indicated coefficient
products is

    sum_i R_i (D(M_i)+1) <= 6400*(195+6).

This is an arithmetic-operation bound for this fixed N18 architecture,
not a clock, bit-complexity or hardware bound. For example, dictionary
hashing, cancellation accuracy and building all needed transition columns
can dominate it. No CPU/walltime claim is made.

With color triples packed into nine low-to-high bits per color (three bits
per occupation 0,...,6), an input key fits in 54 bits. One initial key sort
can make equal suffixes contiguous when colors are removed in order:
current x uses the lowest nine bits and tau is the remaining key shifted
right by nine bits. After a selected outcome, the stored suffix keys are
already ordered. This is an optional compact data structure, not evidence
that a Python dictionary has its byte cost.

For a prospective complex128 implementation, a key-plus-amplitude buffer
of R_M records with eight-byte key and sixteen-byte complex value uses
at most 24*6400 bytes BEFORE object/alignment/allocator overhead. Two live
buffers and an equally sized initial-sort scratch buffer are bounded by
3*24*6400 logical bytes. This width does not include source setup, exact
source integer work, transitions, native allocations, imports or logs.

For transitions it is sufficient to store columns for x in {0,...,6}^3,
for each of the TWO fixed W. There are 7^3 such input triplets, with at
most 190 FULL outputs each. A conservative transition storage bound is

    2 * 7^3 * 190 complex entries,
    16 * 2 * 7^3 * 190 logical bytes at complex128.

A larger full-sector implementation has D(T)^2 entries per T and must
declare and charge that choice. Either transition route uses three-mode
creation-polynomial DP from (2); source/transition precomputation, testing,
memoization and repeated-shot amortization are paid resources. Numerical
mass and orthogonal-column checks do not establish exact floating output.

**Allocation guard:** a naive 462^3 product contains 98,611,128 triples;
even one complex128 per triple requires 1,577,778,048 raw bytes before keys
or Python overhead. It is unnecessary here and is NOT authorized. Even
an 80^3 admissible-product cache is optional work that needs a resource
contract; (7) avoids it altogether. The 18-mode Fock width is irrelevant
to the correctness and finite costs of this conditional construction.

## 7. Safe conclusion, open obligations and provenance

At the distribution level, this is an exact classical replacement for the
entire ideal fixed-Theta P63 count field, including coherent effects across
different color groups. It accepts Theta as input and can be called at
every parameter chosen by an adaptive optimizer. Conditional on the same
history its output law is the same, so the optimizer/decoder trajectory
law is reproduced by induction when all other RNG rules are identical in
law. This does not promise identical seeded samples from different RNG
consumption patterns, nor pathwise finite-shot score domination.

Charge source polynomial/PMF setup, transition setup, import/calibration,
data structures, conditional-pair enumeration, phase evaluation at EVERY
requested Theta, all passes/sorting, categorical RNG, decoding, graph
work and optimizer updates. Timing a warm final categorical draw alone
would not measure this algorithm. Setup amortization must follow the
same paid run boundary in every comparison.

Exact categorical operations with arbitrary real Theta are an ideal
mathematical interface. A rounded complex128 implementation samples an
approximation; its permitted error must be frozen and justified. For
computable phase inputs, certified refinement is a possible future route,
but no uniform comparison-bit or runtime bound is proved here. Tiny P(M)
or near-zero conditional outputs can require more precision even when
the combinatorial support is small. No unreported threshold pruning is
allowed. Zero tests for (5) remain exact and separate from those issues.

For growing d in the corresponding 3-by-d architecture, the source support
s_d can grow exponentially and even computing its table is not proved
polynomial. R_M<=s_d^2 persists, while the convenient N18 bounds do not.
This note is neither a universal efficient classical-simulation theorem
nor a no-go theorem for all optical architectures or scientific objectives.

The smallest remaining implementation obligation is a frozen, capped,
synthetic source/transition/conditional-state qualification, reviewed before
execution. It must use an independent small direct-permanent/Born-rule
reference for nontrivial phase-sensitive and suffix-orthogonality cases,
not only compare the implementation with itself. The actual F6 nonzero
cardinality and measured cold/warm full cost remain unknown. No graph or
pilot is needed to settle the algebraic claim above.

Review provenance: self-review of ROOT's candidate plus the sharper
source-support/pair-enumeration consequences stated here, following
`mathbox:proof-audit`; final changed-file proofreading followed
`mathbox:proofread-math`. The only proofreading mathematical-token fixes
were s for the cardinality in the dependency sketch and imagunit for the
imaginary unit, to distinguish it from the color index i. No independent
reviewer is represented as completed.
Only documentation was created. Existing pytest checks were NOT run,
consistent with the explicit static-only/no-import scope; no code change
or merge is proposed. No paper, old/raw data, credentials or external
messages were touched. The positive scientific goal remains OPEN.
