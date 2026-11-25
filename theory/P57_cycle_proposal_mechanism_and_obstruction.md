# P57: a genuine five-source phase response, and its exact countercontrols

Status: **analytical mechanism established; this two-layer route rejected
as a positive candidate**. It has a finite collective phase response beyond
four-source species and low moments, but admits a constant-bond classical
sampler. A specific one-swap barrier example is also defeated by an
independently retimed distinguishable/permutation control. These are scoped
obstructions, not an equal-cost no-go for all photonic proposals.

No code, import, numerical computation, graph draw, optical shot or QPU call
was used. The construction and arithmetic below are manual. Novelty remains
OPEN; no claim that collective cycle phases, suppression or tensor sampling
are new is made. No external theorem is needed for the explicit derivation.

## Passive circuit and an unconditioned collective event

Use L>=2 distinct single photons in the upper rail of L cells, lower rail vacuum.
Let C be a single cyclic permutation and Z=diag(z_j), |z_j|=1. Two layers of
balanced real beamsplitters, with the phased cyclic route between them, give

    B = (1/sqrt(2)) [[I,I],[I,-I]],
    U = B diag(I,ZC) B = (1/2) [[I+ZC,I-ZC],[I-ZC,I+ZC]].

These are ideal passive components and vacuum ancillas, without a nonlinear
phase oracle or free herald. Real Hadamard beamsplitters can be expressed
using phase shifts and the usual balanced optical splitter. Actual provider
mode, source and PNR availability is not established here.

Write exp(i Phi)=prod_j z_j. The transfer matrix to the L upper outputs is
M=(I+ZC)/2. Its support has exactly two perfect matchings, so

    per(M) = 2^(-L) (1+exp(i Phi)),
    p_B(one photon in every upper output) = (2+2 cos Phi)/4^L,
    p_D(the same event) = 2/4^L.

For L=5, any grouping into species of at most four has the same probability
as D. The interference cross term requires the entire five-input cycle;
a proper subset of input columns opens the cycle, and its phases can be
removed by input/output gauges. Indeed each proper-source species' entire
PNR law is phase independent, so all such regroupings are phase blind.
The same argument on reduced r-photon input mixtures proves invariance of
all joint factorial moments of total order r<L. At L=5 the first possible
response is fifth order, not the order-two effect of P54/P55. All entry
intensities are phase independent. One-mode B PGFs are
1+(z-1)/2+(z-1)^2/8, hence PMF(0,1,2)=(5/8,1/4,1/8).

The event is rare on the attempted-shot denominator: maximum4^(1-L),
equal1/256 for L=5. If all other observations are self-loops, they are still
retained attempts. Under uniform loss, this L-click event acquires eta^L;
discarding losses cannot restore a free conditional success rate.

## All phase-dependent outcomes and a mean-cost cancellation

Let q_j indicate whether source j takes the cyclic rail. Before the second
splitter, cell j contains 1-q_j+q_(j-1) photons. If any cell total is not1,
these equations determine the entire route word uniquely. Its probability
is phase independent. Only the all-cell-total1 sector has two routes:
q identically0 or identically1.

Thus the ONLY phase-dependent PNR outcomes have exactly one photon in each
cell. For a choice x of upper/lower outputs, with h upper outputs,

    p_B(x) = [2+2(-1)^(L-h) cos Phi]/4^L.                 (1)

Every other outcome is phase independent; no full-Fock cancellation is
being silently omitted. Summing (1) over all2^L choices cancels its phase
term. Its unconditional sector probability is2^(1-L).

To obtain a balanced proposal from an incumbent, let upper output j denote
an outside vertex B_j, lower j an incumbent vertex A_j. All other incumbent
vertices stay fixed. On the above CF sector the proposed candidate is the
clicked L-subset of these2L vertices. Elsewhere choose any fixed decoder or
a self-loop. A graph cut restricted to one choice per pair is a polynomial
of degree at most two in the L binary choices. For L>2,

    sum_x (-1)^|x| C_G(x) = 0.

Consequently **the mean decoded cut is phase independent** for every graph
and every fixed decoder that returns the clicked support on this CF sector.
The result does not cover a decoder that deliberately replaces that support
by another nonlinear proposal. It also does not imply tail/best-of-shot or
adaptive trajectory invariance: an improvement indicator is not quadratic.

## A real one-swap barrier and its decisive classical control

There is an elementary fourteen-vertex nonnegative weighted example. Make
five-vertex cliques A and B, each edge weight1/4. Make two-vertex cliques P
and Q, each edge weight10. Join each A vertex to Q_0 with weight1/2 and each
B vertex to P_0 with weight1/2. No other edges. The incumbent is A union P,
size7, and has cut5. All swaps A_i<->B_j cost+1. Any swap involving an anchor
vertex has positive change (at least9); an anchor's single-flip cost is at
least15/2, versus1/2 for an A/B vertex, with the nonnegative swap correction.
Thus the incumbent is a strict one-swap minimum over ALL balanced swaps.

If h of the five A vertices are replaced by B vertices, then

    C(h)=5+h-binomial(h,2).

Improvement occurs at h=4 or5. The all-B candidate has cut0. On the collective
sector, equation(1) gives total improvement probability1/256 at Phi=0 and
5/256 at Phi=pi. Let all other outcomes be self-loops. This is an exact
attempt-level difference1/64, not conditional-on-sector inflation. For
fixed balanced angles, D and every at-most-four species control give3/256.
It shows why a phase response must be tested against the full improvement
set rather than the probability of just the all-B optimum: the latter is
suppressed at the better Phi=pi setting.

This example is **not a positive benchmark**. It has two disconnected
seven-vertex components and a trivial zero cut. More directly, replace B by
B_theta=[[cI,sI],[sI,-cI]], c=cos(theta), s=sin(theta). The upper transfer is
c^2 I+s^2 ZC. D remains phase blind at every theta, but theta=0 routes all
five photons to the all-B candidate with probability1. It beats the
coherent attempted-shot improvement rate. A classical direct five-swap
also produces that candidate deterministically. Evaluating its delta was
already sufficient to credit the improved incumbent; choosing its phase
from that delta cannot be counted as quantum discovery.

The optical input/output port permutation connecting the upper source rail
to the outside-vertex outputs is part of this explicit circuit. It is not
an initial feasible partition state at identity, nor a reason to omit the
permutation control or its cost. This is precisely a preparation-bias trap.

## Phase/sphere controls and the small-core budget

For the fixed-modulus coherent control, draw independent input phases and
then Multinomial(L,|U z|^2), ||z||=1. At L=5 the probability of any one-per-cell
choice with h uppers is

    [5!/(5^5*4^5)] [32+2(-1)^(5-h) cos Phi].

The phase-dependent contrast is5!/5^5=24/625 times the B contrast. This follows
by expanding the product: after phase averaging only the all-diagonal32
term and the two oriented full-cycle terms remain. No D model is substituted
for this coherent realization. On the improvement sector at Phi=pi its
attempt-level success is3/400, below5/256 but still not a search advantage.

For a spherical coherent input, E(prod of five intensities)=per(MM*)/(5)_rise5.
The pentagon matching counts1,5,5 give per(MM*)=(82+2 cos Phi)/4^5 for the
all-upper event:32+40+10 diagonal/transposition terms and two oriented cycles.
Thus its phase contrast is1/126 of B's. Other upper/lower choices change
only the cycle sign. Again the issue is a finite distributional gap, not
superiority over a reoptimized sampler or solver.

For this five-photon/ten-mode core there are252 possible CF candidates and
2002 full-Fock occupations. Every scored preparation/single-swap/core
candidate must be credited to the classical incumbent. Exhaustive scoring
of the252 candidates, or exact small-core sampling, is a mandatory control;
unknown large-graph optima are unnecessary. All frontend graph extraction,
delta/phase choices, decoder work, rejected attempts and photons are paid.

## The scalable cycle still has a constant-bond exact sampler

Let p=q_(j-1), q=q_j. At cell j the local incoming Fock state is |1-q,p>.
Let h_n(1-q,p) be its normalized two-mode balanced-splitter amplitude for
the local PNR outcome n. It includes the HOM sqrt(2) normalization. Define

    [A_j(n)]_(p,q) = z_j^p h_n(1-q,p)/sqrt(2),    p,q in{0,1}.

Here C routes j to j+1 and Z is indexed by destination cell, so the phase
belongs to the incoming routed photon p. Equivalently put z_(j+1)^q on an
outgoing edge. The original5432b7d used z_j^q without that index shift;
independent review identified the amplitude-convention correction. Flux,
all Born probabilities and the negative conclusion are unchanged.

Then the exact full output amplitude is Tr prod_j A_j(n_j). Each cell has
only the six possible PNR patterns of at most two photons. The doubled
transfer T_j(n)=A_j(n) tensor conjugate(A_j(n)) is4x4, and a marginal or
prefix probability is Tr of the product with unobserved sites replaced by
sum_n T_j(n). Precompute suffix products; sequentially compute the six
conditional probabilities and update the prefix. This gives O(L) operations
on constant-size matrices and an exact-sampling specification, retaining
vacuum and bunching. It does not enumerate exponentially many Fock states.

This arithmetic-operation statement needs an arithmetic/precision model.
For the diagnostic fluxes0/pi, concentrate the phase on one route edge by
gauge transformations. U then has entries0,+/-1/2. All probabilities have
integer numerators over4^L: repeated rows make each permanent numerator
divisible by prod n!, as also follows directly from the integer creation
polynomial. Thus prefix probabilities and their exact conditional ratios
have O(L)-bit numerators/denominators. No uncontrolled transcendental oracle
or exponential precision is hidden in these diagnostic cases. Arbitrary
phases require specified coefficient representation/precision separately.

An independent route argument gives an even simpler complete classical
sampler. Draw L fair route bits q. If q is nonconstant, sample each cell's
fixed vacuum, fair single-photon rail or fair HOM-bunched rail. If q is
constant (probability2^(1-L)), draw parity sigma with probability
(1+sigma*cosPhi)/2, then draw L-1 fair output bits and fix the last to that
parity. The collective conditional law is(1+sigma*cosPhi)/2^L, exactly
reproducing(1) after multiplying the sector mass. At0/pi the entire sampler
uses O(L) fair bits/work; for general phases specify cosPhi representation.
An absolute cosine error delta causes total-variation error at most
2^(-L)*delta. Decoder and adaptive-history costs still have to be paid.

## First missing implication for a different architecture

Two coupling matchings with a routed cycle are therefore insufficient as
a new hard collective sampler. A bounded-depth network whose union of
matchings has growing contraction width is a genuinely different next
architecture; this note neither supplies nor approves one. It would still
need a sign relation between its coherent multi-cycle terms and a feasible
multi-swap improvement event after the SAME decoder, surviving retimed D,
all b4 regroupings, phase/sphere and a paid nonlocal classical proposal.
Encoding only a favorable event or precomputing an improving move does not
prove that relation. Polynomial simulation alone is not a universal
equal-cost veto; actual implementation constants and all preparation and
rejection costs would remain part of any subsequent comparison.
