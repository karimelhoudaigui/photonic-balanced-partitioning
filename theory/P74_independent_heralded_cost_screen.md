# P74: a conditional resource screen for monitored heralded proposals

Primary verdict: **proved as written below**, with actual monitored gate
count and a uniform conditional success envelope as explicit hypotheses.
The connected-graph corollary concerns the stipulated edgewise construction,
not a lower bound on all equivalent compilations. The result compares
proposal counts; equal CPU, photon or wall budgets require a separate
resource comparison.

Independent static derivation of ROOT's P74 candidate, 2026-11-25, branch
`research/p66-dark-barrier`, starting at
`4fe224bd866c44e955d67b7185a8fbd62256cbd8`. ROOT also supplied the
protected-flag variant as a question; it is derived in section 7. No other
P74 author file or verdict was read. Only this new file is written. No
scientific Python, import, script, test, numerical query, graph, random
draw, backend run, new hardware circuit or QPU call was used. No catalog
success fraction or hardware capability is assumed without verification;
none was needed for the generic theorem. No novelty claim is made.

## 1. Exact raw-attempt model

Let N>=2 be even. There are N logical qubits, encoded by N signal photons
in dual rail when preparation succeeds, hence 2N signal mode degrees of
freedom. The feasible set is

    F={S subset {1,...,N}: |S|=N/2},
    D=|F|=binom(N,N/2).

The objective C_G(S) is the specified graph cost on F. The graph encoding,
cost phase and controller use graph data, predeclared parameters and
ordinary observed costs, not an optimum mask or solution oracle. A
balanced Dicke state would supply a coherent uniform feasible input, but
its preparation, heralding, compilation and failures are not free.

A raw attempt begins before its input-source/preparation trial. Its
complete record includes preparation outcomes, all herald flags and
attempted operations, ancilla records and final signal detection. A
candidate S is credited only if every required gate flag reports success
and the final count/decoding is a valid feasible logical string. Otherwise
the record is a failure, denoted bottom, without a new optical candidate.
Vacua, wrong source states, wrong photon number, leakage, collisions,
unbalanced strings and failed heralds retain their raw mass and cost.

Each credited candidate must have passed at least g required monitored
stages, where g is a fixed nonnegative integer for the screen. Stage
choices can adapt to the preceding history. Once a failure is recorded,
the attempt supplies no candidate; there is no state recovery, retry-until-
success hidden within a stage, reentry that erases failure, or candidate
from a failed intermediate state. Continuing to operate after failure
is allowed only if that failure remains recorded and disqualifying.

Conditional on every complete successful prefix, every state in the
allowed logical state class, and all controls chosen before that stage's
herald, its success probability is at most the same h, 0<=h<=1. Recorded
success must preserve the state class for which the next bound is valid,
or the envelope must explicitly cover that actual conditional state too.
These are hypotheses about conditional physical operations, not deductions
from a final coincidence probability quoted for an isolated gate.

The simple exact logical profile K_success=sqrt(h)G, with G a unitary
logical gate, gives K_success^dagger K_success=hI. Thus its success
probability is exactly h for every normalized logical input, even one
entangled with a reference. A more general success effect bounded by hI
gives the required upper bound and need not have state-independent actual
success. Correct logical gate action is a separate property from that
probability envelope. The proof below needs the uniform conditional
envelope, not equality or independence.

## 2. All-pass probability without independent gates

Condition first on any outer history before the raw attempt. Let E0 be
successful preparation. Let Ei be the event that preparation and the first
i required monitored stages succeeded. After an abort, later Ei are false.
With H_(i-1) the full prefix information, conditional probability gives

    P(Ei)=E[1_{E(i-1)} P(stage i passes | H_(i-1))]
          <=h P(E(i-1)).

Induction yields

    P(Eg)<=h^g P(E0)<=h^g.

The same inequality holds conditional on each outer history. Extra
heralding or logical-validity checks only reduce the probability. If a
successful circuit sometimes uses more than g stages, survival through
its first g required stages is still necessary; no shorter successful
branch is covered by that same g. Adaptively choosing gates or their
input states does not require independent successes.

For every feasible S let q(S) be the unconditional probability that this
raw attempt returns that candidate, with every failed record retained in
the probability space. Then

    q(S)<=P(Eg)<=H,       H=h^g,
    sum_{S in F}q(S)<=H.

The deficit is failure/invalid-output mass, not a free conditioning
denominator. This remains a favorable upper bound even if an ideal
accepted logical circuit could concentrate entirely on the best S.

## 3. Uniform feasible proposals dominate under D h^g<=1

Suppose D H<=1. One uniform feasible draw returns each S with probability
1/D>=H>=q(S). Hence for every subset E of F,

    P_quantum(raw candidate in E)=sum_{S in E}q(S)
       <=|E|H<=|E|/D=P_uniform(candidate in E).

For objective assessment take only the ordinary cost sublevel sets

    E_b={S in F: C_G(S)<=b}.

This is a theorem for all mathematical thresholds b. It does not give
either algorithm an optimal-state mask, a known C*, a count oracle for
|E_b|, or a training target selected after looking at samples. The classical
algorithm just draws a balanced subset uniformly and evaluates its cost.
The sublevel sets and their cardinalities are analysis notation.

The condition is sufficient, not necessary. Failure of D H<=1 proves no
advantage and supplies no positive optimizer. No graph optimum or favorable
set selection was used to obtain the uniform domination.

## 4. Adaptive best-of-T with a common incumbent

Let the optical proposal/controller adapt arbitrarily to its full past,
but maintain the same conditional envelope and required gate count after
every history. Compare exactly T raw attempts with T independent uniform
feasible proposals, for fixed deterministic T>=0. Both start from the
same known feasible incumbent S0 and report the best observed cost,
including that incumbent. A previously found classical solution is not
attributed as a fresh optical improvement. Classical candidates scored
during preparation or control optimization must be shared/accounted as
candidates too; they cannot bypass the raw-flag screen unnoticed.

Fix a threshold b and put p_b=|E_b|/D. If C_G(S0)<=b, both reports meet
the threshold with probability one. Otherwise, after every unsuccessful
optical history,

    P(next optical raw candidate in E_b | history)<=p_b.

Induction on conditional survival therefore gives

    P_quantum(no hit of E_b in T attempts)>=(1-p_b)^T.

Uniform iid draws have equality in the last expression, so

    P_quantum(best cost by T<=b)
       <=1-(1-p_b)^T
        =P_uniform(best cost by T<=b),       C_G(S0)>b.

Together with the incumbent case, this proves domination of the entire
best-cost distribution at every threshold. No independence of the quantum
attempts, gate outcomes or learned controls is required. An earlier adapted
stop can be padded by failures; replacing T raw trials by T accepted
optical outputs would be a different budget and is not this theorem.
Random achievable trial counts under a time or photon cap require their
own comparison; they cannot simply be replaced by T here.

## 5. Connected edgewise construction and the binomial bound

A connected graph on N vertices has at least N-1 edges: starting at one
vertex, connectivity allows a new vertex to be attached repeatedly by a
new edge, producing N-1 distinct edges of a spanning tree. If the actual
cost-phase construction uses at least one required monitored nontrivial
controlled-phase primitive per such graph edge, then g>=N-1. Additional
layers or other heralded operations can only increase the required count.

To prove D<=2^(N-1), partition all N-bit strings by the parity of their
Hamming weight. Flipping one fixed bit is a bijection between the two
classes, so each has size 2^(N-1). All strings of weight N/2 lie in one
of those classes. For N>=4 there also exist strings of weight N/2-2 in
the same parity class, outside the central layer. The inequality is
therefore strict for even N>=4. At N=2 the central odd layer is the whole
odd class and D=2=2^(N-1).

Consequently, for that edgewise construction and h<=1/2,

    D h^g<=D 2^(-g)<=D 2^(-(N-1))<=1,

with strict inequality when N>=4. This is a screen for the specified
monitored implementation. Connectivity alone is not a compiler lower
bound on g. Zero cost angles, algebraic cancellations, a different
primitive or simplification on the feasible subspace can omit edge gates.
For example the complete graph's balanced cut cost is constant on F, so
its restricted cost phase can be a global phase rather than a necessary
collection of gates. The actual retained g must be used.

## 6. Empty and extremal cases

- g=0: the empty all-pass condition has probability at most one; set h^0=1
  even at h=0. Since D>=2, this screen does not certify domination from
  gate failure alone. It does not establish usefulness of the zero-gate
  proposal either.
- h=0 and g>=1: no candidate passes the required stages. Uniform proposals
  dominate trivially; a normalized success-only gate branch is never seen.
- h=1: the envelope supplies no failure penalty, so D h^g<=1 fails for
  N>=2. Other probability bounds or protocols need separate analysis.
- N=2: connected edgewise g>=1 and h<=1/2 suffice; the combinatorial bound
  is an equality. At h=1/2,g=1 the pointwise comparison can be non-strict.
- T=0: both procedures return the common incumbent. Empty sublevels and
  a zero uniform cut variance introduce no exception to the inequalities.

For different deterministic per-stage envelopes h_i, the same induction
replaces h^g by product_i h_i. If the envelopes are history-random, retain
them within conditional expectations or first supply deterministic uniform
bounds; a realized random product is not an unconditional numerical bound.
No fixed small h can be inferred for arbitrary edge phases from a profile
for one controlled-Z angle. A profile that approaches one in a weak-phase
limit would not satisfy an unverified uniform h<=1/2 assertion. The profile
must be checked over the actual states, angles, flags and histories used.

## 7. Protected ancilla flags may be measured only at the end

There is a physically relevant abstract variant of individual monitoring.
For stage i, suppose its success projector Pi acts on a dedicated ancilla
flag subsystem Fi. No subsequent physical operation acts on Fi. The flag
subsystems are distinct, and each stage has the certified conditional
success envelope after all previous successful virtual projections.

For a fixed operation schedule U_g...U_1, Pi commutes with every U_j for
j>i and with every other flag projector. Moving those projectors through
later operations gives the exact operator identity

    (P_g...P_1) U_g...U_1
       =P_g U_g P_(g-1) U_(g-1)...P_1 U_1.

Thus final simultaneous flag selection has exactly the same unnormalized
all-success branch as projecting each protected flag immediately after
its stage. Its probability obeys h^g by section 2. Failure branches cannot
erase an earlier orthogonal flag. With a fixed schedule and such protected
records, the probability theorem needs no fast intermediate readout or
failure-abort capability. Correct logical computation still requires the
appropriate success Kraus profile; this identity is not a substitute for
any required outcome-dependent corrections.

Resource use depends on the implementation. Always running the entire
schedule consumes all prepared stage resources on failures too. Real
intermediate abort may save on-demand future ancillas; it does not refund
photons already generated. Neither protected flags nor fast feedforward
are assumed available on the project hardware by this mathematical variant.

## 8. Final logical-code postselection does not multiply in general

An isolated optical primitive may satisfy

    P U_i P=alpha_i G_i

for a projector P onto logical occupancy and an advertised success fraction
|alpha_i|^2. Without an actual protected intermediate flag/projection,
that identity is insufficient to multiply success probabilities. Already
for two operations,

    P U_2 U_1 P
       =P U_2 P U_1 P +P U_2(I-P)U_1 P.

The second term is a failure/leakage path that can reenter the final
logical subspace. A purely algebraic counterexample uses a one-dimensional
logical subspace and one leakage dimension. For 0<h<1 let

    P=diag(1,0),
    R=[sqrt(h) -sqrt(1-h); sqrt(1-h) sqrt(h)],
    U_1=R,      U_2=R^dagger.

Both isolated logical blocks are P U_i P=sqrt(h)P. But
P U_2 U_1 P=P, so final success is one rather than h^2. This is an
abstract matrix counterexample, not a proposed hardware circuit or a
numerical simulation. It proves that isolated final-coincidence gate
fractions alone do not establish the monitored product assumption.

Logical-code postselection on reused signal modes is not a protected
ancilla flag. Detecting those photons after every gate can also destroy
the logical input; nondestructive monitoring cannot be assumed free.
This note authenticates neither a catalog postselected-CZ fraction nor
a heralded-CZ fraction. Applying the screen to a catalog primitive needs
its correct conditional Kraus/flag profile and a composable physical
realization, not just the name or a final postselection number.

## 9. Raw resource accounting and remaining boundary

This theorem does not identify one optical trial with one free classical
cut evaluation, CPU second, signal photon or total photon budget. A later
comparison must count at least input photons and failed input preparations,
balanced-Dicke preparation/entangling operations, every generated ancilla,
herald detectors, failed gates and source cycles, feedforward, compilation,
classical parameter/control work, decoding and candidate scores.

When aborting early, count actual resources: later on-demand ancillas may
never be generated, whereas ancillas prepared upfront are still paid even
if unused. It would be incorrect to charge all g ancilla blocks on every
aborted attempt without checking that preparation policy, or to omit the
failed prefixes. The count-screen gives neither of those photon ledgers.
It also gives no implementation guarantee for the initial source or a
small heralded circuit.

Recovery, error correction, repeat-until-success gates with retained states,
ancilla amplification, different primitive phase profiles, deterministic
interactions or accepting other failure records change the hypotheses or
the raw-trial definition. Their resources and performance remain OPEN,
not refuted by this result. A large ancilla supply can change h and must
be paid; a logical gate with eventual success one after retries cannot
be assigned a one-shot h^g penalty while forgetting the intervening trials.

## 10. Scoped decision and proof audit

| Obligation | Result |
|---|---|
| Uniform conditional envelope -> all-pass h^g | Proved by conditional expectation, no independence |
| Full normalized raw records and per-state q(S) | Failures retained; q(S)<=h^g |
| D h^g<=1 -> cost-sublevel domination | Proved for every threshold without an optimum oracle |
| Adaptive best-of-T and common incumbent | Proved at equal guaranteed raw counts |
| Connected graph and binomial inequality | Proved for the stipulated edgewise gate construction |
| g=0, h=0/1, N=2, T=0 | Explicitly separated |
| Deferred protected ancilla flags | Exact commutation identity; fixed-schedule interpretation |
| Unmonitored logical-code postselection | Product rule refuted in general by R^dagger R example |
| Equal CPU/photon/wall budget or actual gate catalog rate | Not established |
| Recovery, weak phases or amplified primitives | New models/resources, OPEN |
| Native hardware, positive optimizer or novelty | Not established |

KEEP the conditional proposal-count screen as a preregistered resource
check. REJECT multiplication of unmonitored coincidence fractions or
presentation of success-conditioned candidates as raw outputs. FOLLOWUP
any actual gate/source implementation only after its composable flags,
state/angle success envelope and full preparation ledger are supplied.
This is not a prohibition on every optical QAOA or recovered protocol.

Final mathematical proofreading covered the complete record definition,
conditional filtrations, gate-count premise, parity bound, best-of-T
inequalities, protected-flag commutations, the reentry counterexample and
all endpoint conventions. Only text/Git integrity checks accompany this
independent freeze. No scientific execution or hardware action occurred.
