# P57 — independent within-team static audit

Reviewed EXACT source commit5432b7df451dfb309bdf506124c9233302054541,
theory/P57_cycle_proposal_mechanism_and_obstruction.md; blob
e8a8f63ccbe7bca3ee7f41dbd769f026dbb450e2; content SHA256
372dbc7c20120451a7b0f7cc760087d6725a73dadd6cef8ad0f77c4c451bd464.

Reviewer is the adaptive agent, not an author of that note. Independence is
an independent derivation within the SAME team/broad context, NONBLIND to
the author's announced rejection and claims. No source was imported or run,
no graph/sample generated, no new simulation or external novelty check.

VERDICT: core probability, scope and rejection claims VERIFIED under the
stated ideal model; exact MPS AMPLITUDE identity NEEDS_LOCAL_INDEX_CORRECTION.
The correction does not change any Born probability or rejection conclusion.
No universal equal-cost no-go or positive optimizer is established.

CORRECTION HISTORY: ROOT caught an arithmetic error in this review BEFORE
acceptance of commit36d3ad1. The reviewer had incorrectly set C(4)=2,
overstating the added accepted-gain calculation. The correct value is3,
so the gains are2 and5, K_G=-5, and the accepted-gain difference is5/256.
The source note's improvement probabilities, strict swap-minimum and
rejection conclusion are unchanged. The original erroneous commit remains
in history; this is a separate documented correction, with no numerical run.

## Assumptions and probability reconstruction

Use L>=2, C:j->j+1, Z diagonal indexed by destination cell, occupied upper
inputs and lower vacuum, balanced passive splitters, ideal number counting.
The mean-cancellation claim additionally needs L>2 and a decoder independent
of the phase except through the observation. Species mean mutually
orthogonal internal labels, with coherent identical photons within a group.
The L=1 degenerate support is excluded from the two-matching D formula.

After the first layer choose the route word q. Its amplitude modulus is
2^(-L/2); cell j has (1-q_j,q_(j-1)). Cell totals other than all1 determine q
uniquely: a zero/two fixes adjacent bits and the recurrence propagates.
For totals all1, q is all0 or all1. Interference of those routes gives, for
one output per cell and sigma=(-1)^(number lower outputs),

    p(x)=(2+2*sigma*cosPhi)/4^L.

All other outcomes have one route and phase-independent probability. With
t two-photon cells their nonzero PNR probabilities are2^t/4^L: local HOM
puts both photons into one rail with probability1/2; one-photon cells are
fair and vacuum fixed. No bunching or missing cell is discarded.
The collective-sector mass is2^(1-L), independent of phase; the upper-only
event max is4^(1-L). For L5 these are1/16 and1/256, respectively. D gives
2/4^L for each collective outcome. Uniform loss multiplies a true L-photon
event by eta^L on the attempt denominator, with no conditional inflation.

For a proper subset S of sources, phase gauges satisfy
beta_(j+1)-beta_j=-arg(z_(j+1)) for j in S. Since at least one cycle edge
is missing, these equations are solvable; both rails in a cell use the
same output gauge. Thus the ENTIRE proper-source PNR law is phase blind.
Products/convolutions of such orthogonal species are phase blind. The
r<L reduced input is a mixture of proper r-source states, proving the
claimed joint-factorial-moment invariance. For one mode, the two input
intensities1/4 give PGF1+(z-1)/2+(z-1)^2/8 and PMF5/8,1/4,1/8, as stated.

The252 count is kinematic C(10,5). Only32 CF supports can have nonzero
probability in this circuit (16 at diagnostic flux0/pi): a cell receiving
two photons has exact HOM zero at output(1,1). This sharpens the wording
but does not invalidate exhaustive scoring of all252 as a STRONG control.
The2002 full-Fock dimension C(14,5) is also kinematic, not nonzero support.

## Mean cancellation and the barrier example

On the collective sector write x_j=1 for outside vertex B_j and0 for A_j.
Every membership bit is affine in x and every edge-crossing cost quadratic,
including edges to fixed incumbent vertices. Therefore for L>2 its full
Walsh parity coefficient is zero. Since every off-sector probability is
phase blind, the UNCONDITIONED proposal mean cut is phase invariant.
Nonlinear acceptance, improvement indicators, CVaR or best-of-many costs
are not covered. A decoder reading/changing the phase itself is not fixed.

For the14-vertex example, single-flip costs are1/2 on A/B,15/2 on P0/Q0,
and10 on P1/Q1. The balanced-swap correction is+2w_uv. The complete swap
types have deltas: A/B=1; A/Q0=P0/B=9; A/Q1=P1/B=21/2;
P0/Q0=15; P0/Q1=P1/Q0=35/2; P1/Q1=20. Hence ALL49 balanced swaps are
strictly worse. Directly summing clique and attachment cuts yields

    C(h)=5-h+h*(5-h)/2=5+h-binomial(h,2).

Only h4,5 improve, with costs3,0 and gains2,5. The six improvement patterns give success
(3-2*cosPhi)/256:1/256 at0,5/256 atpi, D/species3/256, difference1/64.
Retiming to theta0 maps upper sources to outside B deterministically; the
all-B+P partition has zero cut. The disconnected components and a paid
direct5-swap are decisive controls. The note correctly rejects this example.

## Coherent controls and normalization

The fixed-modulus control means v_j=exp(i t_j)/sqrt5 on the FIVE occupied
inputs, lower inputs zero, with independent continuous phases. Conditional
multinomial probability of a CF pattern is5!*product(intensities). Phase
averaging leaves constant32 and two oriented cycle terms, giving exactly

    p_phase(x)=5!*(32+2*sigma*cosPhi)/(5^5*4^5).

Its contrast ratio is24/625 and its improvement probability atpi is3/400.
For the spherical control the sphere is in C5, not C10. The INTENSITY
moment is per(M M^dagger)/(5)_rise5; event probability still multiplies5!.
The pentagon permanent gives82+2*sigma*cosPhi (32+40+10 plus cycle terms),
so p_sphere(x)=(82+2*sigma*cosPhi)/(126*4^5). The claimed contrast1/126
is correct. These are specified controls, not fully optimized classical laws.

## Corrected MPS identity and stronger direct sampler

With p=q_(j-1), q=q_j and C:j->j+1, the diagonal Z supplies the INCOMING
routed photon phase. The exact local amplitude is

    A_j(n)[p,q] = z_j^p*h_n(1-q,p)/sqrt2.

Equivalently assign outgoing edge phase z_(j+1)^q, not z_j^q unless the
phase labels are explicitly shifted or output-basis gauges declared.
For q=(1,0,...,0), the true phase is z_1 while the old expression gives z_0.
The accumulated flux and all probabilities remain unchanged. The doubled
4x4 transfer/trace and prefix-suffix construction are otherwise valid.
At0/pi its intermediate algebra can be Q(sqrt2), of fixed degree; bit sizes
stay O(L). Dyadic probability/conditional statements are correct, but do
not alone mean rational transfer entries or O(L) BIT operations.

A simpler exact classical sampler independently follows from the route proof:

1. Draw L independent fair q bits.
2. If q is not constant, use the fixed cell totals and sample local vacuum,
   single-photon fair rail, or HOM fair bunching. Return that full PNR event.
3. If q is constant (mass2^(1-L)), draw sigma with probabilities
   (1+sigma*cosPhi)/2. Draw L-1 output bits fair and fix the final bit to
   have that parity. Return one photon per cell.

The conditional collective law is(1+sigma*cosPhi)/2^L; multiplying its
sector mass reproduces equation(1) EXACTLY. Every other event is the unique
route law above. At0/pi this needs only O(L) fair bits and O(L) elementary
work, with no matrix or irrational arithmetic. For general phases specify
cosPhi representation; an error delta in cosPhi changes the whole PNR law
in TV by at most2^(-L)*delta. This is a full-law sampler, so the SAME decoder
and adaptive history can also be reproduced, with their actual costs paid.
It does not establish a universal measured equal-wall-time dominance claim.

## First useful cycle-to-cost coupling, without promoting the route

Let Delta_+(x)=[C_inc-C_G(x)]_+ and otherwise retain self-loops. Then

    E gain(Phi)=G0+(2/4^L)*cosPhi*K_G,
    K_G=sum_x (-1)^(number lower)*Delta_+(x).

The proposal mean's quadratic cancellation does not force K_G=0. In the
stated example sum Delta_+=5*2+5=15 and K_G=-5*2+5=-5. Thus
E gain=(30-10*cosPhi)/1024=(15-5*cosPhi)/512:5/256 at0,10/256 atpi.
That is a real all-attempt accepted-cost difference5/256, but the exact
classical sampler and deterministic five-swap defeat a search-advantage
claim. Computing K_G by scoring all core moves must credit those moves to
the classical incumbent. This is a useful physical mechanism equation,
not an optimization win or a license to hide rejection/preparation costs.
