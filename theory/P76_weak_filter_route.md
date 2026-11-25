# P76: weak diagonal filters, physical flags and an exact classical control

Decision: **REJECT the proposed vacuum-flag gadget as a composable nonlocal
diagonal heralded filter, and REJECT diagonal-only conditional bias as a
distinct coherent optimizer mechanism. KEEP** the single-block projected
map and the abstract positive-filter model, with the exact control below.
**FOLLOWUP** requires an actual composable physical resource or a genuinely
coherent mixer/block whose complete raw law is analyzed anew. No such
implementation, optimization benefit, all-optics no-go or novelty result
is established here.

Independent static route analysis, 2026-11-25, branch
`research/p66-dark-barrier`, base
`2a3b4f6eed3d4e2dc014905e964729f9cadfadec`. ROOT supplied the question;
no P75 file, other agent's numerical source, or other P76 file/verdict
was read. Only this note is written. The derivations are self-contained;
no primary lookup was needed. No scientific code/import, AST, test,
simulation, probability query, graph draw, hardware circuit, experiment,
manuscript or QPU action was performed.

## 1. Source, rails and what a successful filter would mean

Take an even N of dual-rail logical qubits. A valid register has N signal
photons, one in each qubit's rail pair, before any extra resources. Write
|x> for its logical computational basis. Balanced feasibility is

    F={x in {0,1}^N: sum_i x_i=N/2},
    D=binom(N,N/2),     |Dicke>=D^(-1/2) sum_{x in F}|x>.

The coherent source and its preparation/heralding probability are not
free. The comparison below uses its known uniform basis probabilities;
it does not provide an optical Dicke preparation. Graph data are symmetric
nonnegative edge weights A_ij and

    C_A(x)=sum_{i<j} A_ij (x_i xor x_j).

No optimum, C*, selected solution mask or optimum-conditioned parameter
is used. Full source failures, loss, wrong rail occupations, heralds and
final counts must remain raw records.

A composable successful diagonal filter means an actual accepted Kraus
operator on the allowed logical state class, with no accepted code leakage.
Its success must be identified by a genuine disqualifying flag or another
validated instrument. A projector on data occupations applied only at
final detection supplies a different object: a projected terminal map,
not automatically a nondestructive filter inside a longer circuit.

## 2. The beam-splitter projected map and its missing flag

For a pair of qubits choose their logical-one rails a,b as active. The
logical-zero rails remain spectators. Use the real passive rotation

    R_theta=[c -s; s c],      c=cos(theta), s=sin(theta).

With creation operators as input columns, one active photon gives
|1,0> -> c|1,0>+s|0,1> and
|0,1> -> -s|1,0>+c|0,1>. Two active photons give

    |1,1> -> (c^2-s^2)|1,1>
                    -sqrt(2)cs|2,0>+sqrt(2)cs|0,2>.

The sqrt(2) factors are the normalized bunched-output factorials. With
one photon initially in every qubit pair, an active photon hopping from
a logical-one qubit to a logical-zero qubit leaves one qubit empty and
the other with two data photons. These are code failures, even though
no signal photon was lost.

In logical order 00,01,10,11, projection onto one photon per qubit gives

    K_projected=Pcode Gamma(R_theta) Pcode
               =diag(1,c,c,q),      q=cos(2theta).

Thus the proposed ordering and coefficients are correct as a projected
single-block map. For 0<theta<pi/4 they are positive and nonzero.
There is nevertheless no success flag here: all photons remain in data
modes, including the wrong-code paths. Vacuum/no-loss heralds do not
distinguish the bunched paths from the accepted logical component.

For example apply R_theta and then R_-theta without a logical-code
projection in between. The physical transformation is identity and final
code success is one. Multiplication of the two isolated projected maps
would give diag(1,c^2,c^2,q^2), with strictly smaller success on relevant
inputs. Leakage paths have reentered. This is exact algebra, not a circuit
simulation, and does not claim that either isolated map is a composable
logical operation.

Local attenuation can be heralded by mixing a rail with vacuum and
requiring zero photons in the loss output. It certifies no loss, not
one photon per qubit. In particular attenuating spectator logical-zero
rails does nothing to either bunched path from logical 11, since those
spectators are empty. With nonzero active-rail attenuations, both bunched
paths also retain nonzero no-loss amplitudes. Setting both of those
amplitudes to zero by zero transmissions would kill the desired full-
support logical component as well.

## 3. Sign of the weak bias, and an equalized min-cut candidate

The raw projected filter is not automatically a min-cut filter. Local
nonzero diagonal factors cannot change its cross ratio

    K00*K11/(K01*K10)=q/c^2=1-tan(theta)^2 < 1.

For weak theta its log probability on bits x_i,x_j is

    2log K(x_i,x_j)
       =-theta^2(x_i+x_j+2x_i x_j)+O(theta^4).

For a weighted weak step choose theta_e^2=t A_e, with t small enough
for every edge to stay in the stated interval, and let d_i=sum_j A_ij.
On a regular weighted graph at balanced weight, the summed expression
favors larger cut: sum A_ij(x_i+x_j+2x_i x_j)=2sum_i d_i x_i-C_A(x).
The field term is constant there, and the remaining sign is +t C_A.
On nonregular graphs the additional fields also matter. Local equalization
alone cannot reverse the nonlocal cross ratio.

There is a simple FORMAL way to reverse the orientation. First attenuate
the logical-zero rail of each qubit by amplitude sqrt(q), with no-loss
flags. The projected map becomes

    diag(q,u,u,q),       u=c sqrt(q).

This still favors opposite bits. Conjugating by a logical X on one qubit
(a code-preserving rail swap) instead gives

    G_theta=diag(u,q,q,u).

For 0<theta<pi/4, 0<q<u<1. This is a positive contraction favoring equal
bits. Its success probabilities are u^2 on aligned bits and q^2 on cut
bits; their ratio is

    rho=q^2/u^2=q/c^2=1-tan(theta)^2 in (0,1).

The maximum success probability h_theta=u^2 tends to one as theta tends
to zero. Therefore a fixed small-success screen cannot simply be assigned
to these hypothetical weak filters. Their success is state dependent;
they are not scalar multiples of unitary logical gates.

All these equalizations use only contractions and local relabeling, with
no amplitude gain or optimum information. They do NOT solve the missing
code-herald problem: G_theta is still the map obtained after projecting
the data code. Calling its loss-output flags a complete success herald
would be physically incorrect.

## 4. A precise vacuum-only obstruction for an exact diagonal primitive

The failure is more general than this one beam splitter. Assume two
dual-rail input photons, arbitrary vacuum ancillary modes, passive optics,
and a successful photon-count herald that leaves two photons in the four
retained data rails. Photon conservation forces every measured ancillary
output to be vacuum on that success branch. Its effective data map is
Gamma(T), where T is the retained one-particle submatrix, a contraction.

Suppose this branch is EXACTLY a full-support diagonal logical operation,
with no other retained data occupations:

    Gamma(T) a_i^dagger b_j^dagger|0>
           =k_ij a_i^dagger b_j^dagger|0>,
    i,j in {0,1},        every k_ij!=0.

Let u_i=T e_(a_i), v_j=T e_(b_j). In commuting creation coordinates the
assertion is the polynomial identity

    (u_i dot z)(v_j dot z)=k_ij z_(a_i) z_(b_j).

A product of two linear forms equal to a nonzero product of two distinct
coordinate variables must have those coordinate factors, in one order.
Indeed set one coordinate to zero; the restricted product is identically
zero in a polynomial ring with no zero divisors, so one restricted linear
form vanishes identically and is a multiple of that coordinate. The other
form is then the other coordinate. The no-zero-divisor fact follows by
the nonzero product of leading monomials.

For fixed i, u_i must therefore lie in either the a_i or b_0 line when
j=0, and either the a_i or b_1 line when j=1. Since b_0,b_1,a_i are
distinct coordinates, their only common allowed line is a_i. Hence

    u_i=alpha_i e_(a_i),    v_j=beta_j e_(b_j),
    k_ij=alpha_i beta_j.

Every such full-support diagonal heralded operation is separable in this
vacuum/passive/counting model. Its cross ratio is one. The nonseparable
G_theta above has cross ratio u^2/q^2>1 and cannot be that exact heralded
primitive. A code projection at final data detection evades the lemma's
no-leakage hypothesis, but restores the non-composability issue.

This is not a theorem about all ancilla resources, state preparation,
or every many-qubit circuit. Nonvacuum helper photons, non-number-
conserving resources, or a genuine nondestructive code measurement change
the assumptions. The lemma certifies a primitive on its full logical
code, not a source-specific transformation of one known entangled vector.
For N>=4 a local primitive promised on all globally balanced logical
inputs encounters all four local bit patterns, so restricting global
feasibility does not remove that requirement. Special-source cancellation
would require its own complete state/instrument analysis; it is not a
validated local gate profile.

## 5. Abstract composable positive filters can make a Boltzmann law

To separate feasibility from statistics, now ASSUME a genuine composable
diagonal success instrument G_e of the stated form is provided by some
paid resource. Its spectrum is a contraction, so an abstract binary
instrument with diagonal failure operator sqrt(I-G_e^dagger G_e) is
mathematically consistent. That algebra is not a passive optical
implementation or a free ancilla construction.

Choose beta>=0 and a graph edge weight A_e>=0. Set

    rho_e=exp(-beta A_e),
    theta_e=arctan sqrt(1-rho_e),
    q_e=rho_e/(2-rho_e),
    u_e^2=rho_e/(2-rho_e)^2.

At beta A_e=0 these are the identity limit. Otherwise theta_e is strictly
between zero and pi/4 and the preceding identities hold. The successful
probability on a computational string is

    p_e(x)=u_e^2 rho_e^(x_i xor x_j).

For a sequence of these diagonal success filters with no coherent mixer,
the unnormalized final amplitude on x is its initial amplitude multiplied
by the scalar filter factors. Per VALID PREPARED register, without
conditioning on filter success, the accepted-candidate masses are

    q_success(x)=(1/D) A0 exp(-beta C_A(x)),
    A0=product_e u_e^2,
    Pacc=A0 E_uniform[exp(-beta C_A)].

The conditional accepted law is exactly proportional to exp(-beta C_A),
for the ideal composable model. It has a genuine min-cut bias and h_e
approaching one at weak beta. If preparing that exact register succeeds
with flagged probability p_src, the complete source-cycle candidate mass
is p_src times this expression. Every other gadget-preparation herald
must likewise belong to its complete instrument or to an explicitly paid
extra failure stage. No filter or source implementation, success rate,
clock advantage or optimization benefit is supplied by these formulas.

## 6. Exact classical rejection/sequential control without C*

Draw one balanced string X uniformly. Evaluate the same local factors
p_e(X). For each edge/stage toss a classical coin of success probability
p_e(X), aborting on the first failure if that is the optical policy.
On all successes return X. This yields exactly

    P(classical X=x and all passes)=(1/D) product_e p_e(x),

the same candidate mass as the ideal diagonal optical model per valid
prepared register. It uses no optimum offset or mask. Rejections are paid;
its expected repetitions
can be large, and no free exact sample from the normalized distribution
has been assumed. A global rejection coin of probability exp(-beta C_A(X))
would even omit the common A0 penalty and keep the same conditional law,
since the graph cut is nonnegative. That stronger comparator also needs
no C*; its scoring/computation still belongs in a resource ledger.

The sequential version matches more than a final acceptance probability.
For arbitrary efficiently evaluated diagonal success maps

    K_j|x>=f_j(x)|x>,       p_j(x)=|f_j(x)|^2<=1,

the joint latent-string/success-prefix weight is
(1/D)product_{j<=m} p_j(x). Its sum over x is the optical prefix survival
probability, and the difference between consecutive survival probabilities
is the probability of first failure at that stage. Thus the accepted
string, success flags and first-failure index are matched exactly. Complex
diagonal phases do not change these probabilities when there is no
superposition-recombining operation.

If every outcome Kraus operator of the full instrument is diagonal,
K_(j,y)|x>=k_(j,y)(x)|x> with sum_y |k_(j,y)(x)|^2=1, then the stronger
full branch formula is

    P(x,y1,...,ym)=(1/D) product_j |k_(j,yj)(x)|^2.

Sampling X once and each outcome with those conditional local probabilities
reproduces the entire classical branch record and final measurement.
The selected diagonal operations may depend on earlier flags; the
classical simulator follows that SAME history-based rule, using X only
to sample the prescribed probabilities, not to give its controller
extra hidden information. Outer-attempt adaptation works the same way.

With only diagonal SUCCESS Kraus operators, this proof guarantees the
accepted output and aggregated first-failure bookkeeping, not every
microscopic failed Fock pattern. Failure Kraus operators can otherwise
be nondiagonal. Matching detailed failure-dependent resources requires
their full instrument/ledger or the stronger diagonal-outcome hypothesis.
That distinction prevents a claim to simulate arbitrary physical failure
statistics from a success-only formula.

Local functions must actually be specified and efficiently evaluated,
as they are for the two-bit filters above. This is not a theorem that
an arbitrary hard global diagonal oracle has a cheap classical evaluator.
For known local filters the control needs a uniform feasible draw and
the same graph/controller arithmetic and coins, without photon sources.
No equality of clock rates is asserted from this algebra alone.

## 7. Where the exact control stops and what remains genuinely open

A known basis permutation is not an escape: update the latent classical
string accordingly between stages. Logical X conjugation used above
is of this type. A mixer that does not commute with a filter but is only
a permutation also remains classically tracked. The first missing
implication is a physically available operation that creates/recombines
distinct computational-basis paths, together with a real accepted
instrument and source preparation. After such mixing, amplitudes may sum
before squaring, and the local probability-product proof no longer applies.
That is a different proof obligation, not an established benefit.

Likewise, concatenating the bare beam splitters without protected code
checks is a coherent full-Fock block, not the product of their projected
diagonal maps. In some active-rail-only layouts the final code map can
still be diagonal, but its coefficients include leakage/reentry paths
and need not factor into local probabilities. A claimed advantage would
need its actual raw state/count law, failure accounting and controls;
non-composability itself supplies none of those conclusions.

An initial source with a genuinely difficult basis distribution changes
the classical starting draw. It must be specified and paid, rather than
silently replacing the known uniform feasible source. Strong-angle signs,
non-diagonal failure/recovery dynamics, active/nonvacuum ancillas and
additional modes also change the model. They are not rejected by the
diagonal-only control or the two-photon vacuum primitive lemma.

Source costs include every attempted Dicke/register preparation, all N
signal photons in valid inputs, ancillas generated before or after a
failure, detector records, lost photons, code/feasibility rejection,
controller/compilation work and cut scores. An intermediate nondestructive
code monitor cannot be obtained by detecting data photons and forgetting
their destruction. The success record of an accepted sample cannot be
substituted for this raw ledger. No generic hardware capability or
implementation budget is assumed here.

## 8. Scoped disposition and falsifiable checkpoints

| Claim/model | Disposition |
|---|---|
| One active BS has projected diag(1,c,c,cos(2theta)) | KEEP, with all leaked Fock paths retained |
| No-loss flags make that primitive code-correct/composable | REJECT; data leakage is unflagged |
| Weak bare/equalized filter favors min-cut automatically | REJECT; its cross ratio is anti-aligned |
| A bit-flipped positive projected map can favor min-cut with h->1 | KEEP as a formal projected map, not a heralded construction |
| Vacuum/passive/counting gives that exact full-support nonlocal diagonal primitive | REJECT under the proved primitive hypotheses |
| Protected local diagonal filters with uniform feasible input | Exact classical raw-candidate/prefix control; no separate coherent advantage |
| Detailed failed Fock records from success diagonals alone | Not established; full instrument needed |
| Stronger coherent block or non-monomial mixer | FOLLOWUP with physical Kraus/source/resource evidence |
| Hard source, active helpers or different measurements | New model and cost obligations, not free exceptions |
| Global optimizer no-go, full bosonic simulation, hardware or novelty | Not established |

The cheapest discriminating static evidence for a physical followup is
an accepted Kraus map with all noncode amplitudes accounted for, genuine
composable flag semantics, a source/preparation ledger, and an explicit
operation that defeats the local product control. A postselected truth
table or favorable conditional cut tilt is insufficient. This note
authorizes no implementation, calibration, computation or QPU action.

Final mathematical proofreading covered the rail basis, normalized bunched
amplitudes, cross-ratio sign, equalization contractions, vacuum primitive
lemma, Boltzmann parameters, branch normalization and the scope of exact
classical matching. Only text/Git integrity checks accompany this freeze.
