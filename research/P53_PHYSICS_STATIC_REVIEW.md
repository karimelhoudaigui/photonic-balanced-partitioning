# P53 exact source / classical-control physics: static review

Verdict: **STATIC PASS for the declared targeted qualification**, with no
physical normalization/phase blocker found in commit
`a8f93a0187e9ea99e3663d66d6c8b2477028e835`. No P53 import, integer construction,
test, LP, probability comparison or sample was executed in this review. No
continuous replacement certificate is claimed to exist before its construction
and verification. A finite exact certificate, if obtained, retains the narrow
edge-MEAN scope below.

Exact sources read via git objects, rather than a moving worktree:

| File at a8f93a | SHA256 |
|---|---|
| research/P53_exact_continuous_phase.py | aedbc561c900bcbed8f9eff3bbfa7d2fd47bd640502966d132898ea68f261692 |
| tests/test_p53_exact_phase.py | 68df52198d1916fda23e32ea6ae89a031500288ed84ed2d5ed3afe67c727cf81 |
| research/P53_exact_phase_contract.md | 84fbe8f5314ff2fa3dbb464cf43e82940ace67d4b1ecfb59c0ac007c5d4ca54d |

I also read the complete frozen claim card and execution JSON. I did not write
this implementation or its tests. I previously reviewed P52 and derived its
phase/quartic conventions, so this is an independent implementation/physics
recheck within the same team, not a new blind external validation of earlier
work or novelty. No primary P52 raw probabilities were consulted for the
derivation below; the P52 LP provider's recorded SHA is an implementation
dependency, not a definition of the physics.

## Fresh normalization and phase reconstruction

Use U[out,input]. Write normalized output creation variables X_j and
X_(j+4), A_j=X_j+X_(j+4), B_j=X_j-X_(j+4). The four unnormalized Walsh linear
forms have product

    F(v)=sum_j v_j^4 - 2 sum_(j<k) v_j^2 v_k^2 + 8 v0 v1 v2 v3.

This follows by pairing the two forms with opposite signs on v2,v3 and then
the other pair; coefficients are integers. Each physical column is divided
by sqrt8. The first four occupied columns therefore give F(A)/8^2; the last
four give F(D B)/8^2, where D_jj=exp(i j theta). Expanding the latter quartic,
all powers of exp(i theta) are even: 4j, 2(j+k), or6. With z=exp(2i theta),
this is exactly the source's phased factor: exponents2j, j+k,3.

Consequently the complete input product creation operator has wave polynomial

    C(X,z)/8^4 = F(A) F_z(B)/8^4.

There is no input sqrt(8!) divisor: the eight single photons occupy distinct
input modes. If C_n(z) is its monomial coefficient, the normalized Fock ket
relation (a†)^n|0>=sqrt(prod n!)|n> gives amplitude
C_n(z)*sqrt(prod n!)/8^4. Thus probability **multiplies** prod n!, divided by
8^8. Dividing instead would confuse creation coefficients with a permanent.
The source's `probability_cosine` uses the correct multiplier. The c_nh are
real signed integers; their autocorrelation gives constant sum_h c_nh^2 and
cos(2h theta) coefficient2 sum_j c_nj c_n,j+h, exactly as implemented.

Independent diagnostic checks from these conventions, not executed here:
an all-eight-bunched output at row j has C_n(z)=z^(2j), so probability is
8!/8^8 independent of theta. The listed quartic target1+cos(2theta)/2 equals
the earlier .5+cos²theta, without a factor-of-two discrepancy. Degree<=6,
all6435 compositions, and exact-zero arrays are consistent with fixed N8.
The assignment bound sum_h|c_nh|<=8!/prod n! is valid because each labelled
source routing contributes a unit-modulus signed monomial before grouping.

## Endpoint controls and the occupation measurement

`_gaussian_columns(0)` is the same matrix without sqrt8; endpoint1 uses i^j
on the last four columns, hence theta=pi/2, not pi/4. The lower-block minus
sign and source-column orientation match the full source. Four distinct
occupied inputs of one species yield probability numerator
prod n! * ((Re C_n)^2 + (Im C_n)^2), denominator8^4, as implemented.

For two mutually distinguishable four-photon species, the detector forgets
species after their independent occupation laws are convolved. The correct
full count law is sum_(u+v=n) p_A(u)p_B(v); there is **no extra total-output
factorial**. `classical_library` follows this probability convolution, unlike
the coherent multiplication used for the eight-identical source. All35
complementary splits (the group containing0 fixes the representative), both
endpoints, and all6435 occupation rows are retained. The library has70 such
controls plus uniform70, not an assumed arbitrary-internal-state envelope.

Uniform top4 ties are a stochastic map of each integer count tuple. If h
entries are strictly higher and t tied at the boundary, every completion has
weight1/binom(t,4-h). Since h+t<=8, the possible denominators divide420;
`tie_scaled_rows` also checks this and exact row mass. No collision filtering,
click conditioning, jitter approximation or fixed-label tie preference is
introduced. Each balanced subset has exactly16 crossing edges and each
vertex has4 incident crossings, explaining the exact structural identities.
Uniform70 has each edge crossing with probability4/7, not an assertion that
the quantum ranked law is uniform70.

## Algebraic certificate and scope checks

The shifted Chebyshev recurrence uses cos(2theta)=2x-1, x=cos²theta in[0,1].
It therefore covers every real theta with the source's cosine frequencies.
Power/Bernstein conversion, degree elevation and reconstruction formulas are
the standard exact binomial identities, with Python integers/Fractions and no
floating target coefficients. The final coefficient-by-coefficient check
does not infer a continuum identity from a grid.

RREF/free-variables0 can miss a nonnegative solution; the two chosen supports
can also fail even when membership holds. These are explicitly conservative
limitations. Accepted weights are checked nonnegative, sum1 and reconstruct
all28 exact coordinates; their Bernstein mixture is nonnegative and sums1 on
[0,1], and the independently reconstructed power polynomial must match the
source. Failed/time-limited LP proposals remain inconclusive under the run
gate, even if an exact candidate is separately retained. Degree6 then12 has
at most7+13=20 proposals. No failed-global-Bernstein inference to an outside
hull/separating graph is justified or made in the source/contract.

A verified identity implies equality of expected weighted cut for each fixed
graph and theta, hence some library component has no larger mean. It does
not equate ranked distributions, tails, best-of-shot statistics, adaptive
histories or budgets, and gives no arbitrary-N/loss/hardware/novelty result.
The source/contract explicitly preserve these exclusions. Finite N8 endpoint
controls and uniform70 are cheap references, not a new optimization positive.

## Qualification coverage and residual obligations

Seventeen planned cases (including parametrized endpoints/degrees/statuses)
cover independent four/eight-column products, odd-phase cancellation, Fock
factorials/bunching, exact normalization, the quartic witness, admissible
ties/rank mass, Gaussian controls, complete endpoint library, exact polynomial
transforms/elevation, RREF/support limitations, polynomial corruption and
conservative mocked solver gates. They were only read, **not run** here.
The direct-column test shares the sign table with production; this review's
independent U convention/column reconstruction above supplies its physics
interpretation rather than treating that shared table as a separate source.

Required next evidence is targeted qualification, actual input closure,
bounded main execution if authorized, and separate checking of any emitted
exact witness. This review does not establish numerical performance, an LP
outcome or the integrity of as-yet unproduced raw files. Prior P52 Naive API
qualification remains distinct and its full physical-probability replication
is still pending. No primary file, proof, raw data or manuscript was modified.
