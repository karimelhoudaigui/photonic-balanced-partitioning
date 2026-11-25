# P53c same-phase control card: static physics/ring review

Card verdict: **mathematically coherent; implementation/qualification pending**.
Exact card `28e0fc513d55de5daceeeb7ff9ff3a619f556bae`, file
`research/P53c_SAME_PHASE_CONTROL_CARD.md`, SHA256
`e84b04dec9f5a6b4e40af778ad075b0e62a14e9ce53bf9d5cfd2228979222985`.
I read all111 lines after completing/sealing the P53b exact checker receipt.
No P53c source import, control law, ring coefficient, convolution, target,
native LP, sample or executable calculation was run. P53b's known outcome
motivates this explicitly post-result falsification; it is not a blind test.

Let xi=exp(i*pi/3). From xi²=xi-1 and conjugate(xi)=1-xi, integer-pair
multiplication is(ac-bd,ad+bc+bd), conjugation(a+b,-b), and squared modulus
a²+ab+b². The listed six powers follow by this multiplication, returning to1.
The norm is (a+b/2)²+3b²/4, so no negative probability or floating-root choice
is involved. An independent Q+Q*sqrt(-3) representation has coordinates
(a+b/2,b/2), suitable for a separate arithmetic fixture.

The card preserves U[out,input] from the full source: row j mod4 supplies
xi^j only for input columns4..7; the lower block contributes a minus sign
there. Walsh signs and D=diag(xi^j) have the exact block form
U=1/sqrt2[[W,DW],[W,-DW]]. W is unitary and D has unit-modulus entries, so
column orthogonality follows by block cancellation, with the same1/sqrt8
entry scale. It is the target's same theta=pi/3 interferometer, not a new
favorable circuit or a Gaussian-integer endpoint approximation.

Four DISTINCT occupied inputs in one species have creation coefficient C_n
divided by8². In normalized Fock coordinates amplitude multiplies sqrt(prod
n!), so probability is prod n!*norm(C_n)/8^4. The card's multiplier and
denominator are correct. In a direct-permanent fixture with repeated rows,
permanent=(prod n!)*C_n for the unnormalized entry matrix; divide by this
factorial when comparing raw creation coefficients. The alternative probability
formula norm(permanent)/(prod n!*8^4) is the same check.

Two mutually distinguishable four-photon species have a probability
convolution, denominator8^8, with no extra total-output factorial or coherent
cross-species sum. There are70 four-port groups,35 complementary partitions,
330 group occupations and6435 total occupations. Keeping all rows, exact
zeros and all35 new controls gives106 labeled vertices with the original71,
including duplicates. Exact420 tie weights are the same stochastic map;
incident4/total16 identities hold for every control and protect graph offsets.

The saved P53b functional and graph must remain FIXED for diagnostics. For
each new control, recompute its exact signed and normalized-graph margin
against the same target. A negative margin gives a better same-angle b4 mean
for that graph; a zero margin also invalidates its old strictly positive
separation, but neither sign alone proves vector membership. Check all35
margins rather than selecting a grouping. A new exact dual against106 is a
different mathematical functional, not a repaired optimizer benchmark.

Implementation hazard: P53b's `nonnegative_graph` hardcodes the ENDPOINT71
label. Reusing generic exact dual/native helpers is appropriate, but blindly
reusing that whole discriminator/graph wrapper for106 would mislabel or
promote a new graph. The new caller should keep old-graph diagnostics separate
and label any expanded-hull functional accurately, as the card requires.

Exact primal106 weights/all29 equalities or exact all106 strict dual margins
must remain independent of float LP proposals. Winning-arm status0/successTrue
gates, contradiction handling, fixed point, bounded two calls and no retry
remain appropriate. Failed old dual or failed LP/support search is not a
membership proof; expanded separation is not an all-angle/all-classical claim.

Planned finite arithmetic work and data volume are explicitly bounded; their
CPU20/wall30/64MiB scientific-data projection is not an observed benchmark.
Source/test/spec/contract freeze, static review, targeted qualification and
distinct main authorization are still required. The fixed N8 problem is
trivially searchable over70 cuts; no mean-hull result here establishes
optimization/total-budget/scalability/PNR-hardware/novelty success. No primary
artifact, source, manuscript or scientific status was edited by this review.
