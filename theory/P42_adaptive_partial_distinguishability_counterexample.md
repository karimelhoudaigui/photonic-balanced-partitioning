# P42 — why internal indistinguishability cannot be weakened silently

Author p41_adaptive. Analytic counterexample to a BROADER READING, not to the
identical-photon threshold theorem. No numerical experiment was executed.
The construction uses m8,k4,N8, within a twelve-photon source cap.

Take U=(H2 tensor F3) direct-sum I2, with the usual normalized Hadamard and
three-mode Fourier matrices. In the active six-mode block, output rows0 and3
are respectively

    (1,1,1,1,1,1)/sqrt(6),
    (1,1,1,-1,-1,-1)/sqrt(6).

Inject one photon in every input mode. Inputs0,1,2 carry the same internal
state A; inputs3,4,5 carry an orthogonal internal state B. The two deterministic
spectators6,7 can have state A. Thus inputs are spatially singly occupied,
but all photons are NOT internally identical. Apply independent uniform loss
with survival eta and ideal threshold detection ignoring internal species.

Choose clicked support S={0,3,6,7}. Consider only the event in which spectators
6,7 both survive and exactly two of the six active photons survive. Every
specific surviving active pair has unconditional weight

    eta^4(1-eta)^4.

For a pair from one species, the amplitudes into active outputs0,3 add with
equal magnitude. Their collision-free probability is1/9. There are six such
pairs: binom(3,2) for each species. For a cross-species pair, its two label
routings add incoherently, giving probability1/18. There are nine such pairs.
The total coefficient is therefore

    6*(1/9) + 9*(1/18) = 7/6.

Consequently the FULL clicked-support probability, including its other
nonnegative sectors, satisfies

    p_partial(S) >= (7/6) eta^4(1-eta)^4.                     (1)

At eta=1/100 this exceeds the identical-photon simple cap
[eta/(1-eta)]^4. Indeed the ratio of the lower bound(1) to that cap is
(7/6)(99/100)^8, and Bernoulli gives

    (99/100)^8 >= 1-8/100 = 23/25 > 6/7.

The proof requires no decimal approximation. It does not depend on a graph,
known optimum or score evaluation. One could attach any graph objective
afterward; the counterexample concerns the physical support-probability cap.

For an overlap parameter x=|<A,B>|^2 rather than orthogonal species, the
active-pair coefficient becomes7/6-x/2. This is not a claim of violation at
the actual Lucy visibility, which has not been measured here. It establishes
that treating imperfect distinguishability as automatically less favorable
than the ideal model is invalid for this cap.

The reason is dimensional: after tracing internal degrees of freedom, the
spatial state need not remain in the totally symmetric spatial Fock sector.
The detector's support projector then includes internal/spatial multiplicities
not counted by binom(ell-1,k-1). Any robust extension must rederive the state
spectrum and observed projector, or add a justified perturbation bound.

No conclusion about the correctness of the stated IDENTICAL-photon theorem
changes. This example is a domain check to preserve in any eventual hardware
interpretation or attempted extension of P42.
