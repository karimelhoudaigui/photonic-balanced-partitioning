# P53 algebra and certificate gate: static encoding audit

25-Nov-2026. **Verdict: conditional on exact source/control construction and a
fully verified rational Bernstein certificate.** The proposed implication is
mathematically sound. Existence of that certificate and correctness/resource
coverage of its future implementation are NOT established by this review.
No source import, integer enumeration, LP, graph or sample was run here.

Authoritative targets read in full: ROOT
`87abe69b21692e7fc0d48306ebc28517e59849a2`,
`research/P53_EXACT_CONTINUOUS_PHASE_CARD.md`; interface/derivation
`ef476a4`, `research/P53_EXACT_PHASE_API_CARD.md` and
`theory/P53_exact_phase_derivation.md`. This audits those frozen texts, not an
unseen implementation. P52 floating arrays/fits are motivation, not a proof
input. This audit changes none of those sources or the sealed P52 data.

## Typed claim and dependency graph

For the specified8-mode U(theta), CF11111111 input, ideal eta1, and exact
uniform-tie top4 decoder, let c_B(theta) be its28 crossing means. Fix71 controls:
all35 b4 groupings at each of theta0/pi2, plus uniform70. If exact arithmetic
constructs the physical polynomial c_B(x), x=(1+cos2theta)/2, and ALL Bernstein
control vectors at degree6 (or the bounded fallback12) have exact convex
weights over those fixed controls, the continuous mean identity follows for
EVERY real theta and EVERY weighted graph on these same8 labels.

The proof dependencies are:

```text
specified U, CF input, commuting creation/Fock convention
  -> Walsh quartic F identity + correct 8^-4 wave normalization
  -> all6435 integer coefficient polynomials C_n(z), z=e^(i2theta)
  -> exact nonnegative probabilities, normalization, tie70 and crossing28
  -> exact Chebyshev/power/Bernstein coefficient transformations
exact Gaussian-integer b4 construction + probability convolution
  -> fixed rational71-vertex mean library
floating LP support suggestion ONLY
  -> exact rational linear equations/sign/sum checks for EACH control point
  -> independently reconstructed POWER identity
  -> nonnegative normalized continuous mixture (mean-only conclusion)
```

All algebraic leaves below are internal elementary identities. Future source
enumeration and rational certificates are load-bearing computation leaves,
currently conditional/not run. There is no dependency from P52 floating
probabilities back into exact source coefficients or control coordinates.

## Normalization and quartic expansion reconstructed

Let the unnormalized Walsh forms be

```text
l0=v0+v1+v2+v3, l1=v0+v1-v2-v3,
l2=v0-v1+v2-v3, l3=v0-v1-v2+v3.
```

Pairing gives l0*l1=A+2B and l2*l3=A-2B, where
A=v0^2+v1^2-v2^2-v3^2 and B=v0*v1-v2*v3. Their product A^2-4B^2 expands
to sum(vj^4)-2sum(j<k)(vj^2 vk^2)+8prod(vj), with the stated PLUS8 sign.

In U[out,input], first-half source forms use A_j=X_j+X_(j+4); the second
half uses exp(i*j*theta)B_j, B_j=X_j-X_(j+4). Thus their product is exactly
the card's F(A)F_z(B), with exponents2j, j+k and3 in z=e^(i2theta).
No substitution z=e^(itheta) or extra phase is permissible. Expanding the
quartics in8 variables gives disjoint support types20+54+16=90 per factor;
their8100 products are a complete bounded construction, including cancellations.

Each matrix entry has denominator sqrt8. Eight source factors therefore have
denominator8^4, not8^8 in the AMPLITUDE. If C_n(z) is the UNNORMALIZED INTEGER
numerator coefficient, the actual monomial coefficient is C_n/8^4. Applying
the monomial to vacuum multiplies by sqrt(prod n_i!), hence probability is
prod(n_i!)*|C_n|^2/8^8. No input factorial occurs for CF inputs. A permanent
with repeated OUTPUT rows instead equals prod(n_i!)*C_n/8^4; confusing these
two coefficient conventions would reverse the factorial and invalidate proof.

C_n has degree<=6 in z. The real coefficients imply the cosine formula in the
card, with factor2 for every nonconstant autocorrelation. The source assignment
count proves sum_h|c_nh|<=8!/prod n_i!: each output assignment contributes a
single sign/phase monomial before cancellation. The complete state iterator
must retain every composition of8 into8, including zero coefficient vectors.
Exact normalization is sum_n a_n0=8^8 and sum_n a_nh=0 for h>0. Nonnegativity
is by squared amplitude on the unit circle, not sign tests on cosine coefficients.

For a4-photon b4 group, amplitude denominator is8^2 and probability denominator
8^4. At phase0/pi2 its ordinary numerator coefficients are Gaussian integers.
Probability numerator is prod(n_i!)*(real^2+imag^2). Distinguishable-species
convolution multiplies these PROBABILITIES; no final combined-occupation
factorial is added. All35 unordered splits at each phase remain required.

## Ties and exact polynomial maps

Uniform ties have reciprocal binomial multiplicity, independent of phase.
Admissible top4 denominators divide420. Three explicit count fixtures force
the factors20,35,6: (2,1,1,1,1,1,1,0), (8,0,0,0,0,0,0,0), and
(2,2,1,1,1,1,0,0). Hence the stated LCM420 is exact. In particular the uniform
occupation11111111 has denominator70, not a fixed priority or discarded event.
The mean/rank cosine lattice D=420*8^8 is correct.

The transform T_h(2x-1) uses T0=1,T1=y and T_(h+1)=2yT_h-T_(h-1).
For a power monomial x^k and degree d>=k,

    x^k = sum_(j=k)^d [C(j,k)/C(d,k)] B_(j,d)(x).

This follows by multiplying x^k by (x+(1-x))^(d-k), so the card's Bernstein
formula is correctly oriented. Hand units:1 has all controls1, x has controls
j/d, x^2 has j(j-1)/(d(d-1)). Degree6->12 elevation is exact convex averaging
with weights C(6,j)C(6,i-j)/C(12,i); Vandermonde gives their sum1. No sample
interpolation or floating rounding can replace these coefficient identities.

## Certificate and failure gate

For fixed library rows M_v, the exact support system is29 equations: sum1
plus28 coordinates. Its consistency and every original equation must be checked
over Fractions, not only pivot equations or selected independent rows.
The incident-edge equations have rank8: a left null vector obeys a_i+a_j=0
on every pair; a triangle forces all a_i=0. Thus affine dimension<=20 and a
convex representation, IF one exists, has some support<=21. This existence
bound does not guarantee the floating support or the free-zero RREF policy
will find it. Threshold/fallback supports are prospective candidate searches;
failure of either is inconclusive, not nonmembership.

For every required Bernstein control point, accepted weights must be EXACTLY
nonnegative, sum EXACTLY1 and satisfy ALL28 equalities. No floating weights,
rounded free variables or tolerance repairs are proof inputs. Lexicographic
exact RREF with free variables0 is a reproducible sufficient attempt only.
LP limits/failures remain inconclusive at the run gate even if a numerical or
exact candidate is retained separately. At most7+13 calls, each1s, no new
degree, solver, random restart or automatic subdivision.

If these checks succeed, Lambda_v(x)=sum_j B_(j,d)(x)lambda_jv is nonnegative
on[0,1], normalized and reconstructs the mean curve. An INDEPENDENT power-basis
expansion must match the ORIGINAL physical polynomial coefficient by coefficient;
re-evaluating a grid of angles or reusing the same transform as its own inverse
is weaker. The result gives expected-cut equality for every graph by linearity,
and at least one component has no larger mean. It says nothing about full70
probabilities, tails, best-of-shots, compiler/search cost, losses or scalability.

Bernstein success is only sufficient. The card's internal-face warning is
correct: at an interior x0 all B_j,d(x0)>0, so nonnegative controls whose face
functional sums to0 would ALL lie in that face. A nonconstant curve that touches
but does not stay in the face cannot have such a global certificate at ANY
finite degree. Failure at6/12 must not become a separating graph/advantage.

## Obligation matrix and remaining gap

| Obligation | Status in this review |
|---|---|
| F identity, phase exponents, wave/output normalization | passed algebraically |
|90x90 coverage bound,6435-state requirement | passed as design; iterator pending |
| Gaussian-integer source/probability convolution convention | passed algebraically; code pending |
| Tie LCM and exact coefficient domains | passed algebraically |
| Chebyshev/Bernstein/elevation and convex sufficiency | passed algebraically |
|20-fit bound, timeout/free-variable scope | coherent prospective gate; runtime pending |
| Exact coefficient tables, all library vectors and rational certificates | conditional on future computation |
| Implementation/preflight/independent power reconstruction | not addressed before source freeze |
| Continuous membership existence, optimality, full law, hardware positive | unproved/out of scope |

Smallest missing implication: construct and verify the proposed exact source
and control arrays, then produce all needed nonnegative rational weight vectors
and the coefficientwise continuous identity. There is no certificate yet.
Cheapest next check is source review plus the declared qualification; do not
add a competing P53 implementation or run here. No external source theorem is
needed for this elementary conditional route; no novelty conclusion is made.

Provenance: shared-context adversarial review. I authored the P52 numerical
primary and a related polynomial candidate, not the independent Perceval engine
or the P53 F-factor implementation. The core normalization/F identity above
was reconstructed directly from the displayed Walsh matrix. This is not an
external/blinded referee report and agreement between agents is not evidence
of implementation correctness. Future exact-source audit remains necessary.
