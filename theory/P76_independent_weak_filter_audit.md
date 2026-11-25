# P76: weak two-rail filters, leakage and a classical raw-law replacement

**Primary verdict: proved as written below**, for the explicitly separated
passive-vacuum no-leak factorization and diagonal-instrument replacement
claims. A weak final-postselected beam splitter is not a protected logical
filter. Even a valid protected diagonal filter supplied as an extra resource
does not beat uniform feasible proposals at equal raw-attempt counts from
a uniform Dicke input. Neither claim is an all-photonic no-go or a matched
total-cost theorem.

Independent static derivation, 25 November 2026, branch
`research/p75-code-review`, starting at
`10eee38701d9e0cf7f197cd556655b26cc08c277`. ROOT supplied the candidate
question and requested a derivation before author access. No other P76
source, disposition or review was read. Only this file is written. No
scientific code, import, AST parse, test, random draw, numerical probability,
circuit construction, source installation, backend, manuscript or QPU action
was performed. All calculations below are hand algebra; no external source
or theorem attribution is needed or claimed.

## 1. Physical basis and weak beam-splitter map

Use two dual-rail logical qubits with rails a0,a1 and b0,b1. The logical
state |ij> has one photon in ai and one in bj, i,j in{0,1}. Define the
passive real beam splitter on the two ACTIVE rails a1,b1 by

    a1^dagger -> c a1^dagger+s b1^dagger,
    b1^dagger -> -s a1^dagger+c b1^dagger,
    c=cos(theta), s=sin(theta).

The inactive rails a0,b0 are identity. This convention is unitary because
c^2+s^2=1. There are no nonvacuum ancillary photons. Ancilla modes, if
present but unused, remain vacuum and cannot flag signal leakage.

Expand creation operators, keeping normalized Fock occupations:

    |00> -> |00>,
    |01> -> c|01> -s a0^dagger a1^dagger|vac>,
    |10> -> c|10> +s b0^dagger b1^dagger|vac>,
    |11> -> (c^2-s^2)|11>
               -sqrt(2)cs |2_a1,0_b1>
               +sqrt(2)cs |0_a1,2_b1>.

The last two kets have no photons in the inactive rails. The |01> and
|10> failures instead have two photons in DIFFERENT rails of one qubit
and zero in the other; they are logical leakage even without same-mode
collisions. The |11> bunched amplitudes include their sqrt(2) Fock factors.
Their squared norms sum to4c^2s^2=sin^2(2theta), and the retained |11>
probability is cos^2(2theta). For |01>,|10> the leakage probability is s^2.

If P is the logical one-photon-per-qubit projector, then only the
PROJECTED map is

    P Gamma(U_theta) P=diag(1,c,c,q), q=cos(2theta).

Vacuum flags on ancillary modes do not apply P. On the stated leakage
branches those flags also report vacuum. Photon counting on the signal
rails at the end can recognize final logical occupation, but destroys the
register and does not supply intermediate protected code flags.

For example U_-theta U_theta=I. Both isolated projected maps have the
same diagonal because c and q are even in theta. Treating those projected
maps as two independently accepted filters would give success c^4 on
|01> and q^4 on |11>. The two physical inverse blocks instead return
each input with probability ONE. The discrepancy is the omitted term
P Gamma(U_-theta)(I-P) Gamma(U_theta) P. Weak leakage cannot simply be
ignored when composing blocks; it can reenter the final code.

## 2. A tempting ferromagnetic projected filter and its boundary

For 0<|theta|<pi/4, c>0, q>0 and

    k00*k11/(k01*k10)=q/c^2=1-tan^2(theta)<1.

Local nonzero diagonal attenuation multiplies k_ij by alpha_i beta_j
and leaves this cross ratio unchanged. To invert it, conjugate the
projected block by a logical X on the second qubit, giving diagonal
(c,1,q,c). Apply local amplitude attenuations

    A=diag(sqrt(q),1), B=diag(1,sqrt(q)).

The resulting PROJECTED diagonal is

    K_projected=diag(c sqrt(q),q,q,c sqrt(q))
               =t diag(1,r,r,1),
    t=c sqrt(q), r=sqrt(q)/c<1.

Its squared weight would suppress cut edges, so it has the desired
ferromagnetic sign. For edge weight w>=0, choosing

    exp(-beta w)=q/c^2=1-tan^2(theta)

would give |k_ij|^2=h exp[-beta w*1(i!=j)], where

    h=c^2 q=exp(-beta w)/(2-exp(-beta w))^2.

This profile tends to1 as beta w tends to0, and is not covered by an
unverified constant h<=1/2 statement. The theta=0 endpoint is identity;
the q=0 endpoint is excluded from the nonzero cross-ratio/log formulas.

The attenuation itself is a genuine local vacuum-herald operation: couple
a rail to a vacuum loss port and select no photon in that port. However,
the preceding beam splitter's logical leakage remains nonzero at the
strictly positive attenuations above. Local swaps/attenuations do not
turn that leakage into a protected ancilla flag. Thus this calculation
does NOT implement the claimed complete logical filter with vacuum flags
alone. It describes the final logical projection of a larger physical
map. A proof that the whole proposed instrument has the required accepted
Kraus map is still necessary before composing it.

## 3. Passive-vacuum factorization with exact absence of signal leakage

Consider an arbitrary passive interferometer with the four signal rails
and any number of VACUUM ancillary inputs. Condition every ancillary output
to vacuum. Let T be the resulting four-by-four data block of the one-particle
unitary. The accepted two-photon map is exactly Gamma(T): projecting
ancillary output vacuum keeps only retained-signal terms in each input
creation factor. T is a contraction, although the algebra below does not
need that norm bound.

Assume this accepted map, on ALL FOUR logical inputs, has NO signal leakage
and is diagonal with nonzero amplitudes k_ij. This is the full-Fock identity

    Gamma(T)|ij>=k_ij|ij>, k_ij!=0,

not just the weaker projected identity P Gamma(T)P=diag(k_ij).
Write the retained creation polynomials of input rails ai and bj as
linear forms A_i and B_j in output variables x0,x1,y0,y1. Then

    A_i B_j=k_ij x_i y_j.

A product of two nonzero linear forms equal to a nonzero scalar times uv
forces those forms to be proportional to u and v in some order. Indeed,
restricting to u=0 makes the product vanish identically; one of the linear
restrictions must vanish, so that form is a multiple of u and the other
is a multiple of v. The polynomial ring has no zero divisors.

For fixed i, A_i occurs in BOTH x_i y0 and x_i y1. It cannot be proportional
to y0 in one and divide x_i y1 in the other. Hence A_i=alpha_i x_i.
It follows for both j that B_j=beta_j y_j. Therefore

    k_ij=alpha_i beta_j,
    k00*k11=k01*k10.

This proves the candidate factorization, including arbitrary complex
amplitudes, attenuations and passive vacuum circuits. Such a map cannot
produce a nontrivial controlled phase or nonzero full-support two-body
diagonal filter. Accepted no-leakage must be checked in the complete
two-photon signal sector, not inferred from its logical truth table.

If zero accepted amplitudes are allowed under the SAME no-leak identity,
k_ij=0 implies A_i=0 or B_j=0. Thus the nonzero support is a rectangle
I times J. Proper rectangles with a singleton row/column give only a
one-sided/single-entry filter; their amplitudes can still be factored,
but the statement that every column of T is the corresponding unchanged
rail no longer follows from four nonzero equations. This is why the
full-support hypothesis is a convenient exact physical-gate formulation.

Allowed LOCAL rail relabelings or a whole-qubit SWAP can be undone before
applying the diagonal statement. The theorem is not a classification of
every nondiagonal code-preserving transformation or every restricted
input subspace. For N>=4 the uniform balanced N-qubit state has all four
local bit assignments on any chosen pair, with suitable spectators; a
local gate claimed valid on its full supported register cannot omit
one assignment merely by appealing to global balance. N=2's balanced
subspace has only01/10 and needs a separate restricted-input analysis.

Nonvacuum ancillary photons, nonzero count heralds, non-number-conserving
resources, nondestructive code measurements, recovering leaked branches
or jointly using a different global code alter the polynomial premises.
Approximate leakage bounds need an error budget. None of these alternatives
is ruled out here, supplied for free or assumed native to the hardware.
Multiple vacuum-conditioned passive stages with only vacuum ancillary
inputs still compose to Gamma(T_net). Joint passive compilation alone
therefore does not evade this particular full-support, final-no-leak
factorization statement while keeping all its other premises.

## 4. A true diagonal instrument has an exact latent classical replacement

Now grant a DIFFERENT resource: a correctly implemented protected logical
instrument whose accepted map at stage e is diagonal,

    K_e=sum_{S in F} k_e(S)|S><S|, |k_e(S)|<=1,
    F={S subset{1,...,N}: |S|=N/2}, D=binom(N,N/2).

Here N>=2 is even. For an edge-local filter, k_e depends on its two endpoint
bits. Start with
the uniform Dicke input D^(-1/2)sum_{S in F}|S>. No noncommuting mixer or
source change occurs between filters. Abort/discard a trial after its first
failed accepted flag; any such failure remains paid and produces no candidate.

For a fixed sequence, the unnormalized all-success state is

    D^(-1/2)sum_S [product_e k_e(S)]|S>,

so its accepted candidate subprobability is

    q(S)=D^(-1)product_e |k_e(S)|^2.

There is an exact classical latent construction: choose ONE uniform
balanced S at the beginning of the trial; for each reached stage toss
a coin with pass probability |k_e(S)|^2; stop at its first failure;
on all passes emit S. For every prefix the pass probability is
D^(-1)sum_S product_prefix |k_e(S)|^2, the quantum squared norm.
Every first-failure location and accepted S therefore has the same law.
No optimum, C*, optimal mask, partition function or Gibbs sampler is used.

Random/adaptive stage choices also work when determined by the same
observed classical prefix/controller. Condition on that controller record
and repeat the argument; summing records gives the same candidate/abort
law. Fixed-basis diagonal phases never affect these observations. If every
resolved FAILURE effect is diagonal, its labeled coin can also be included
before abort. An outcome on which computation CONTINUES instead needs its
Kraus maps diagonal in the same basis; diagonal effects alone do not prevent
a noncommuting state update. If only the accepted map is
specified and arbitrary failure effects are unresolved, this result covers
the COARSE binary pass/fail-and-abort record, not every microscopic failure
label, retained failed state, timing record or quantum-memory transcript.
Resuming a non-diagonal failed state instead of discarding it is outside
the assumptions.

Known real coin probabilities define an exact probability-law replacement.
An executable precision-controlled sampler must pay their evaluation and
random-bit costs, as well as uniform-subset generation, graph setup and
the same accepted cut scores. This is not an unmeasured exact-arithmetic
runtime advantage assertion. The quantum Dicke preparation, ancillas,
failed preparations and all reached failed operations remain physical costs.

## 5. Stronger count obstruction and the Gibbs special case

Each product factor is at most one, so immediately

    q(S)<=1/D for every S.

Thus a DIRECT uniform feasible draw pointwise dominates every successful
candidate subprobability of this diagonal-filter process at equal raw
attempt counts. Under an adaptive controller the bound holds conditionally
on each outer history because each fresh trial again starts from the same
uniform Dicke diagonal law. More general accepted branching still has
q(S)=(1/D)P(accepted | latent S)<=1/D.

For any mathematical cost sublevel A_b={S:C_G(S)<=b}, a trial's conditional
hit probability is at most p_b=|A_b|/D. With a common initial incumbent and
T fixed raw trials, induction on no-hit histories gives

    P_filter(best cost by T<=b)<=1-(1-p_b)^T
                              =P_iid_uniform(best cost by T<=b)

below the incumbent threshold; at/above its cost both CDFs are one. This
does not furnish either algorithm the threshold set or its size. Failed
filters are paid self-loops, not extra favorable candidates. Controller-
computed classical candidates must be shared/accounted and not credited
as an optical filter discovery.

For the abstract ferromagnetic edge profile of section2,

    |k_e(S)|^2=h_e exp[-beta w_e 1(edge e is cut)],
    q(S)=H/D exp[-beta C_G(S)], H=product_e h_e.

The success-CONDITIONED law is Gibbs, but the complete raw acceptance is
H times its uniform-proposal rejection acceptance. Classical latent coins
reproduce both the filter prefixes and that law exactly; omitting the
S-independent H would even increase raw acceptance. Direct uniform draws
already have the pointwise bound above. A favorable conditioned mean
alone is therefore not an optimum-blind raw-attempt optimization benefit.

The domination theorem compares RAW PROPOSALS, not matched CPU, energy,
photons, accepted-score counts or wall time. Direct uniform search may
score more candidates than the postselected quantum procedure. The latent
replacement instead matches reached filter-stage counts and accepted score
calls in law, but its actual operation costs still need measurement.
Neither construction licenses a total-resource claim without a full ledger.

## 6. Disposition and first genuinely open implication

KEEP the full-Fock weak-block calculation, the passive-vacuum no-leak
factorization and the diagonal-instrument classical replacement. REJECT
vacuum flags as a certificate of no signal leakage, repeated multiplication
of isolated final-code blocks, or pure diagonal postselection from a uniform
Dicke input as an equal-raw-proposal improvement over uniform feasible search.

A noncommuting mixer can make accumulated phases affect final probabilities
and breaks the latent-diagonal argument; its actual protected implementation,
leakage, preparation and total resources are the first missing bridge.
A changed source whose initial diagonal law is not cheaply classically
samplable is also outside the explicit uniform replacement, but must earn
that structure without optimum-dependent preparation and pay its full costs.
Nonvacuum-ancilla gates, recovery and jointly compiled accepted blocks need
their own complete Kraus/flag certification. A weak projected cross ratio
alone supplies none of those bridges.

No general Gaussian claim, arbitrary photonic mechanism obstruction, positive
optimizer, novel priority, hardware capability or QPU readiness follows.
The user's stronger research objective remains open.

Final hand proofreading checked beam-splitter signs, normalized bunched
amplitudes, weak-filter cross ratios, the difference between projected and
full accepted maps, factorization support exceptions, adaptive latent
records, Gibbs normalization and count-versus-total-resource scope. Only
text/hash/Git integrity checks accompany this independent freeze. No
scientific execution was performed.
