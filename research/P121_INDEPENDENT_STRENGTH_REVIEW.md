# P121 independent catalytic-strength screen review

2026-11-26. Non-author MANUAL audit; no scientific execution.
Source FULL read: `research/P121_CATALYTIC_STRENGTH_BUDGET.md`, 150 lines,
commit `f132d13e5c73fb8d38fc16da2b359927925e5215`, SHA256
`12dcaa64a06f2bdc3b08877a472a31b40c81c26be6576d193aae64c0a6078644`.
Also read P116's 315 lines at fbe08686 for mathematical context; its complete
independent review remains another reviewer's task. P74's accepted screen
and protected-flag premises were previously read in full. Review parent:
`9d208e73cdff0ee0822e96cd21f57520100d4ca5`.

**PROVED under the explicit no-recovery/code/instrument/compiler premises.**
The h(gamma) substitution, norm product, dimension threshold and restricted
uniform comparison check. No blocking algebraic gap found. This is an
instantiation of P74, not a fresh gate-count lower bound or novelty finding.
Two conventions are essential: g counts COMPLETE two-helper K_e gate
instruments, not individual detector clicks; an uncorrected failure ends
the charged attempt, and any source reset/retry starts a new paid attempt.

## 1. Profile and exact threshold arithmetic

Reconstruct the P116 phase-free branch with s=3R-2>0. Its logical amplitudes
after the rail flip and local contractions are (H,Rs,Rs,H), where
H=sqrt(R)(2R-1)sqrt(s). Hence h=H^2=R(2R-1)^2s and
rho=(Rs/H)^2=Rs/(2R-1)^2. Put z=sqrt(1-rho), R=(1+z)/(1+2z).
Directly, 2R-1=1/(1+2z), s=(1-z)/(1+2z), giving
h=rho/(1+2z)^4. This checks the scalar profile without evaluating a circuit.
For finite gamma>0, rho=exp(-gamma) lies in (0,1), and R lies in (2/3,1).
The accepted logical map is sqrt(h)exp(-gamma Pi_e/2), with Pi_e a projector;
its norm is at most sqrt(h), not a state-independent success probability h.

If gamma>=log(64/63), rho<=63/64 and z>=1/8. Thus

    h<= (63/64)/(1+1/4)^4 =252/625<13/32,

since 252*32=8064<8125=13*625. No monotonicity assertion about the compiler
is needed for this bound. At the threshold R=9/10 provides a further
hand check: R(2R-1)^2(3R-2)=(9/10)(4/5)^2(7/10)=252/625.

## 2. Composable accepted instrument and arbitrary logical mixers

On the valid paired code let rho_in be any positive state of trace <=1,
including a register entangled across logical bits. For a single accepted
K_e, K_e^dagger K_e<=h_e I gives
Tr(K_e rho_in K_e^dagger)<=h_e Tr(rho_in). Interleaved code-preserving
unitaries have norm one. A fixed all-accepted product therefore has trace
at most product_e h_e, regardless of coherence and without assuming gate
success independence. Preparations/final readout that are genuinely physical
trace-nonincreasing stages cannot increase that unnormalized trace.

If acceptance combines corrected patterns alpha, the required statement is
SUM_alpha K_alpha^dagger K_alpha<=h_e I on the current code. A separate
bound for each pattern is insufficient. The scalar h from the one-pattern
P116 gadget does not automatically cap such a sum. Protected distinct flags
allow deferred measurements only when later full physical operations leave
those flags untouched. Then their projectors commute, as in P74.

The current accepted state must remain in the code. Code leakage followed
by reentry through a later physical mixer is not the asserted product of
logical K_e. Arbitrary logical unitaries are an optimistic mathematical grant
for the upper bound; their synthesis, success, modes, photons and time are
not free or certified by the grant. Fresh helpers and their input state are
part of the gate hypothesis, not reusable undetected ancilla resources.
For adaptive choices, P74's tower argument gives the same bound if EVERY
conditional TOTAL accepted cap holds and completion requires at least g
successes before ANY uncorrected failure. Internal retries after failure
or returning a repaired failure as a candidate require another instrument.

## 3. The dimension and power bound

The alphabet has D=2^L strings, selecting exactly one unit vertex per pair;
it is not the full binomial(2L,L) feasible alphabet. Weighted blocks qualify
only with the separate balance certificate promised in the source.
Complement strings represent the same unoriented partition; summing both
on BOTH sides preserves domination and creates no factor-two advantage.

Write q=13/32. Its fourth power is less than 1/32 because
13^4=28561<32768=32^3. Also q<1/2. For L>=5 and actual g>=L-1,

    product_e h_e<=q^g<=q^(L-1)
      =q^4 q^(L-5)<=2^(-5)2^(-(L-5))=2^(-L).

Every individual output probability is at most this TOTAL successful mass.
Thus q_B(y)<=1/D, even if mixers concentrate all surviving amplitude on y.
The argument needs neither a uniform quantum input nor an optimal-state mask.
It does need one credited successful candidate per declared attempt, with
all other branches held rather than silently counted as extra proposals.

## 4. Exact comparison and resource boundary

For a fixed set A of paired-code candidates, q_B(A)<=|A|/D. A uniform
classical bit string attains |A|/D and needs no C* or known solution.
Cut evaluations/setup remain paid. Below a common incumbent's cost, take
A to be the cost sublevel; retain-the-better CDF order follows. At/above
the incumbent both retained CDFs are one. This does NOT pointwise dominate
the complete repaired transition kernel, whose incumbent atom may be large.

If the same cap holds after every history on this SAME code, conditional
no-hit probability is at least 1-|A|/D. Induction gives quantum hit probability
at most 1-(1-|A|/D)^T, attained by iid uniform candidates. Independent
quantum shots are unnecessary. Changing pairings/candidate universes changes
the relevant A intersection and invalidates that fixed-rate formula.

At the abstract allowed-mesh level, disjoint one-photon Hadamards plus
straight helper routing realize the same uniform code law for D. This
bypass uses no bosonic effective Kraus shortcut. Its actual family/device
admissibility and equal preparation/readout law must still be established
for an experimental D comparison; the classical uniform theorem does not
depend on that hardware claim. A COMMON independent success factor preserves
the inequality; arbitrary path-dependent loss, missed flags or unequal
sources do not inherit the ideal instrument cap by a scalar substitution.

A completed g-gate chain consumes L data photons plus 2g fresh helpers.
A static spatial unrolling supplies these on every launch and has 2L+4g
ports before further resources. At L=5,g=4 this is 13 photons/26 modes,
outside the four-photon/eight-mode witness. Serial port reuse can reduce
simultaneous modes; actual early abort can avoid later helper injections.
Neither changes the no-recovery raw-attempt bound, and neither proves
an equal photon/time-budget comparison. All actual reached stages, source
attempts, preprocessing, scores and mixer costs require their own ledger.

## Disposition and open cases

Accept the sufficient screen under its stated premises. Graph connectedness
does not establish g>=L-1: constants, zero angles, cancellation and joint
compilation can remove gates. Gamma below threshold, L<=4, recovered/all-record
outcomes, enlarged accepted-pattern sums, helper reuse and changed primitives
remain outside this substitution unless a new TOTAL cap is proved.
Passing outside it is not positive evidence. Nothing here resolves P116's
all-record feed-forward proposal, a general optimizer comparison, actual
hardware support or novelty. Only this review was written; frozen sources
and negatives remain intact. No import/AST/test/RNG/script/native/QPU run.
