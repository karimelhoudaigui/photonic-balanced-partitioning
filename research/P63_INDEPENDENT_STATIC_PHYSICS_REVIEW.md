# P63 independent static physics review

2026-11-25, review recorded at 19:24 UTC. No scientific code, import, matrix
evaluation, graph, random draw, numerical test or experiment was executed.

**Primary verdict: incomplete, with the smallest missing implication being an
unambiguous operational freeze of the paired SPSA probes.** The structural
physics claims below pass an analytic audit. This prospective architecture
card is not yet a source, cost, seed or execution contract. No useful N18
decoded-mean channel, algorithmic positive or QPU readiness is established.

## Exact claim, sources and dependency graph

Audited revision: `682d3573c47ffe4261ae4c018d2132af8e5d8a8e`.
Both complete author files were read without edits:

| Artifact | SHA256 |
| --- | --- |
| `research/P63_EXTENSIVE_PHASE_ARCHITECTURE_CARD.md` (169 lines) | `965885a17fae0221ee28ef1016a292ea9aab10696ed37c518f3db17eff50f92b` |
| `theory/P63_extensive_phase_structural_checks.md` (143 lines) | `56801fcf5d538ae816d3fc7a03304737e8f960146489e146af8c5dc6debe6d9e` |

Claim card: ideal identical photons in input `1^18`, complete PNR output of
`U=V(F3 tensor I6)D_Theta(I3 tensor F6)`, the stated ten gauge-fixed phases,
fixed rational output mixer on ports `(0,6)`, and top-nine decoding with fresh
uniform carried ties. Loss, source errors, postselection, physical timing and
other D architectures are outside this claim.

Internal dependencies: unitary composition -> fixed q -> complete one-mode
PMFs and the P56 full-square degree-three lemma; relative output unitary ->
support/locality -> joint invariant counts/totals -> P62 frontier limitation;
Fourier column identities -> identical three-photon species laws; phase
gauges -> full dephasing -> finite block sampler. Spherical invariance ->
exchangeability -> uniform balanced subsets. No external theorem or numerical
outcome is a load-bearing leaf of this audit. P56, P62, P50's FAST API and
product-marginal definition, and P55's pre-data cost amendment were also read.

## Obligations and decisive evidence

| Obligation | Finding |
| --- | --- |
| Unitarity and q | Passed: Fourier factors and the rational orthogonal mixer are unitary; mixed-row factors are `(3-4 omega^b)/(5 sqrt(18))` and `(4+3 omega^b)/(5 sqrt(18))`, giving exactly the stated q rows |
| Complete D law, B marginals and joint moments through order three | Passed under full square CF input; the P56 generating-polynomial argument applies, including repeated output indices |
| Ten generators / active union | Passed: five disjoint three-mode supports, with two orthogonal rank-one generators per support; outside `{0,6,12}` is unchanged |
| Joint conserved quantities | Passed: the joint projectors for the outside counts AND all six `M_i` commute with every relative phase operation; this is stronger than unchanged separate marginals |
| P62 | Passed with active size 15, including the stated feasible frontier sizes; it supplies no measured equal-wall-time theorem |
| j-aligned species | Passed: `U[:,G_j]=D_j U[:,G_0]`; V commutes with D_j at color zero. Species independence gives six iid three-photon PNR samples, not single-photon samples |
| Product marginals | Passed: their total is variable, including zero, and must never be conditioned to 18 |
| Spherical replacement | Passed: a full complex sphere gives uniform Fock occupations; exchangeability and uniform ties give a uniform nine-subset |
| Full phase average | Passed by the gauge quotient and dephasing argument below; not a sampler for targeted unaveraged B |
| SPSA sign, shot counts and bounds | Conditional only on the explicit paired-probe clarification below; minimizing cut uses the stated minus-gradient update |
| Cost, numerical guards, exact seed namespaces and finite implementation projection | Not addressed by an implementation: these remain prospective closure obligations |
| Fresh N18 benefit, independent numerical reproduction, held-out confirmation and hardware | Not established / out of scope |

For arbitrary intermediate phases alpha, the ten quotient coordinates are
`phi[b,i]=alpha[b,i]-alpha[0,i]-alpha[b,0]+alpha[0,0]`, for b=1,2 and i=1..5.
The removed color phases are invisible row phases; removed b phases commute
through F6 and multiply the fixed Fock input by a global phase. The surjective
torus homomorphism sends uniform independent port phases to uniform relative
phases. Complete dephasing therefore leaves three independent F6 occupation
draws followed, conditionally, by six independent three-mode transformations.
It does not assert unconditional independence between output color blocks.

The source/permanent convention must be frozen explicitly: for normalized
Fock input x and output z of a unitary W, with equal total photon number,

    P(z|x) = |per W[z|x]|^2 / (product_r z_r! product_c x_c!),

where rows and columns are repeated with their occupations. The F6 source
has x=`1^6`; each subsequent tritter has a possibly bunched three-mode input.
Omitting its input factorials changes the law. The stated 462/1140/190 support
bounds include zero-probability outcomes; no suppression/collision filter is
permitted. The cache must have paid byte/operation bounds in the code contract.

## Required pre-source clarifications and the ROOT amendments

1. Card lines 66-67 can be read as independent perturbation directions for
   the two signs. Freeze ONE Delta_t per step and arm, with probes explicitly
   `Theta_t+c Delta_t` and `Theta_t-c Delta_t`. Only their count/tie streams
   are independent between signs; directions are independent between steps
   and arms. ROOT accepted this clarification during review. The formula and
   shot budget do not change. State the angle bound componentwise, or as
   `||Theta_3||_infinity<=3`; it is not a Euclidean-norm bound.
2. Freeze the continuous-field law, not only its phase alphabet:
   `z_j=exp(i phi_j)/sqrt(18)`, `p=|U z|^2`, `n~Multinomial(18,p)`, with iid
   uniform input phases, complete counts and a declared numerical guard.
   Freeze exact per-graph fresh means and the equally weighted normalized
   global mean, including zero-weight failure and equality/mixed-case labels.
3. Close B-only costs as disjoint measured fields. In particular P55's
   immutable factory returns its inner backend WALL: excluding the entire
   factory would lose the RNG/validation prefix. Charge that prefix and all
   required classical setup; report total factory CPU/WALL and mark an
   unavailable internal CPU split unknown. Optional control work cannot fund
   FAST. Freeze cold-import ownership and any cross-graph setup allocation.

ROOT additionally proposed a stage-one-only B80 + two fixed FAST veto. This
is a valid conservative staging amendment if frozen before data: one fixed
FAST mode no worse on BOTH graphs gives DEV_REJECTED_FIXED_FAST, with all
optional controls explicitly NOT_RUN_DUE_FAST_VETO. Otherwise stage one must
return OPTIONAL_REQUIRED, accepting no positive. It must not retune the B
trajectory/hyperparameters after seeing these raw shots or treat unrun
controls as defeated. Any later optional run needs its own reviewed closure;
the originally frozen controls/streams must be retained, not selected by B.

## Additional exact collision suppression checked at ROOT's request

Let P cycle j->j+1 modulo six in each input b block. Directly from the Fourier
entries, `UP=D U`, where D has diagonal entry `xi^i` on output `(a,i)` and
`xi=exp(2 pi imaginary_unit/6)`. V acts within i=0 and commutes with D. The
bosonic input `1^18` is invariant under P, with no permutation sign. Thus any
nonzero output amplitude must satisfy

    sum_i i M_i = 0 modulo 6.

For the collision-free output `1^18`, M_i=3 and this sum is 45, congruent to
3 modulo six. Its probability is exactly ZERO for every Theta. With 18 total
photons in 18 modes, every legal shot therefore contains a collision. This
does not invalidate the complete-count protocol. It invalidates any CF-only
sampler, retry rule or expectation of a nonzero collision-free rate. Check
the support on already required MAIN counts; no new native 18-photon probe
is needed or authorized. The phase-average control has the same joint M law
and shares this suppression, so it cannot supply an advantage claim.

## Provenance, validation boundary and remaining gap

Independent same-team analytic review in an isolated subagent/worktree,
`research/p63-physics-review`, with shared broad parent context; not external
or blind replication. Skills used: `mathbox:proof-audit`, then
`mathbox:proofread-math` on this report only. No author theorem, card, raw data,
source or manuscript was changed. Read-only shell/git/hash inspection preceded
this report. No project/scientific module, pytest, graph or RNG was executed;
existing tests must be checked by the authorized numerical worker before merge.

The strongest safe statement is the structural one above. The cheapest next
step is the corrected code-only contract/source review, including native
small-PNR normalization fixtures and analytic N18 identities, not a new N18
calibration. Useful decoded N18 response and superiority to the paid controls
remain open. No paper, external handoff or QPU action follows from this audit.
